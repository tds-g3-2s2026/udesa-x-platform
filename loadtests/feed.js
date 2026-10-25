import http from "k6/http";
import exec from "k6/execution";
import { sleep } from "k6";
import { Counter, Rate, Trend } from "k6/metrics";

function positiveInteger(name, fallback) {
  const value = Number(__ENV[name] || fallback);
  if (!Number.isSafeInteger(value) || value < 1) {
    throw new Error(`${name} debe ser un entero positivo.`);
  }
  return value;
}

const baseUrl = (__ENV.BASE_URL || "").replace(/\/+$/, "");
if (!/^https?:\/\/[^/?#]+\/api$/.test(baseUrl)) {
  throw new Error("Definí BASE_URL con el origen y el prefijo /api.");
}
if (!__ENV.SEED_PASSWORD) throw new Error("Definí SEED_PASSWORD.");

const seed = Number(__ENV.SEED || 42);
if (!Number.isSafeInteger(seed)) throw new Error("SEED debe ser un entero.");
const users = positiveInteger("SEED_USERS", 100);
const vus = positiveInteger("VUS", 20);
const pages = positiveInteger("PAGES", 5);
const rampSeconds = positiveInteger("RAMP_SECONDS", 30);
const durationSeconds = positiveInteger("DURATION_SECONDS", 120);
if (vus > users) throw new Error("VUS no puede superar SEED_USERS.");
const serviceShas = {
  users: __ENV.USERS_SHA,
  posts: __ENV.POSTS_SHA,
  gateway: __ENV.GATEWAY_SHA,
};
for (const [service, sha] of Object.entries(serviceShas)) {
  if (!/^[a-f0-9]{40}$/i.test(sha || "")) {
    throw new Error(`Definí el SHA desplegado completo de ${service}.`);
  }
}

const feedDuration = new Trend("feed_duration", true);
const firstPageDuration = new Trend("feed_first_page_duration", true);
const nextPageDuration = new Trend("feed_next_page_duration", true);
const feedErrors = new Rate("feed_errors");
const feedRequests = new Counter("feed_requests");
const emptyPages = new Counter("feed_empty_pages");

const stages = [
  { duration: `${rampSeconds}s`, target: vus },
  { duration: `${durationSeconds}s`, target: vus },
  { duration: `${rampSeconds}s`, target: 0 },
];

export const options = {
  scenarios: {
    feed: {
      executor: "ramping-vus",
      startVUs: 0,
      stages,
      gracefulRampDown: "30s",
      gracefulStop: "30s",
    },
  },
  setupTimeout: "5m",
  summaryTrendStats: ["avg", "min", "p(50)", "p(95)", "max"],
  systemTags: ["status", "method", "name", "scenario", "expected_response"],
};

function readPage(token, cursor, phase) {
  const response = http.get(
    `${baseUrl}/feed${cursor ? `?cursor=${encodeURIComponent(cursor)}` : ""}`,
    {
      headers: { Authorization: `Bearer ${token}` },
      tags: { name: cursor ? "feed_next_page" : "feed_first_page", phase },
      redirects: 0,
      timeout: "10s",
    },
  );
  let body;
  try {
    body = response.json();
  } catch (_) {
    body = null;
  }
  const valid =
    response.status === 200 &&
    body !== null &&
    Array.isArray(body.items) &&
    (body.nextCursor === null ||
      (typeof body.nextCursor === "string" && body.nextCursor.length > 0));
  if (phase === "load") {
    feedRequests.add(1);
    feedDuration.add(response.timings.duration);
    (cursor ? nextPageDuration : firstPageDuration).add(
      response.timings.duration,
    );
    feedErrors.add(!valid);
    emptyPages.add(valid && body.items.length === 0 ? 1 : 0);
  }
  return { valid, status: response.status, body };
}

export function setup() {
  const sessions = [];
  for (let i = 0; i < vus; i++) {
    const loginStarted = Date.now();
    const response = http.post(
      `${baseUrl}/auth/login`,
      JSON.stringify({
        identifier: `seed.${seed}.${String(i).padStart(10, "0")}@example.com`,
        password: __ENV.SEED_PASSWORD,
      }),
      {
        headers: { "Content-Type": "application/json" },
        tags: { name: "login", phase: "setup" },
        redirects: 0,
        timeout: "10s",
      },
    );
    let session;
    try {
      session = response.json();
    } catch (_) {
      session = null;
    }
    if (
      response.status !== 200 ||
      !session ||
      typeof session.access_token !== "string" ||
      !session.access_token ||
      !Number.isFinite(session.expires_in) ||
      session.expires_in <= 0
    ) {
      throw new Error(
        `Login de cuenta ${i} inválido (HTTP ${response.status}).`,
      );
    }
    const page = readPage(session.access_token, null, "setup");
    if (!page.valid || page.body.items.length === 0) {
      throw new Error(
        `Feed de cuenta ${i} inválido o vacío (HTTP ${page.status}).`,
      );
    }
    sessions.push({
      token: session.access_token,
      expiresAt: loginStarted + session.expires_in * 1000,
    });
  }
  const requiredUntil =
    Date.now() + (2 * rampSeconds + durationSeconds + 30) * 1000;
  if (sessions.some((session) => session.expiresAt <= requiredUntil)) {
    throw new Error(
      "La duración supera la vigencia de los tokens; reducí la corrida.",
    );
  }
  return sessions;
}

export default function (sessions) {
  const session = sessions[exec.vu.idInTest - 1];
  if (!session || Date.now() >= session.expiresAt) {
    exec.test.abort("Cuenta sin sesión vigente; la corrida no mide el feed.");
  }
  let cursor = null;
  for (let page = 0; page < pages; page++) {
    const result = readPage(session.token, cursor, "load");
    if (!result.valid || !result.body.nextCursor) break;
    cursor = result.body.nextCursor;
  }
  sleep(1);
}

export function handleSummary(data) {
  const values = (name) =>
    data.metrics[name] ? data.metrics[name].values : null;
  const summary = {
    recorded_at: new Date().toISOString(),
    environment: __ENV.ENVIRONMENT || "eks",
    base_url: baseUrl,
    service_shas: serviceShas,
    seed,
    seed_users: users,
    vus,
    pages_per_iteration: pages,
    stages,
    duration_ms: data.state.testRunDurationMs,
    requests: values("feed_requests"),
    errors: values("feed_errors"),
    empty_pages: values("feed_empty_pages"),
    duration: values("feed_duration"),
    first_page_duration: values("feed_first_page_duration"),
    next_page_duration: values("feed_next_page_duration"),
    metrics: data.metrics,
  };
  const report = JSON.stringify(summary, null, 2);
  return {
    stdout: `${report}\n`,
    [__ENV.SUMMARY_PATH || "/tmp/feed-summary.json"]: report,
  };
}
