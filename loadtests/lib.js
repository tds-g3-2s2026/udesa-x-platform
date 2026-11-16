import http from "k6/http";

export function positiveInteger(name, fallback) {
  const value = Number(__ENV[name] || fallback);
  if (!Number.isSafeInteger(value) || value < 1) {
    throw new Error(`${name} debe ser un entero positivo.`);
  }
  return value;
}

/** Reads and validates the settings every flow shares; throws before any request. */
export function readConfig(defaultVus) {
  const baseUrl = (__ENV.BASE_URL || "").replace(/\/+$/, "");
  if (!/^https?:\/\/[^/?#]+\/api$/.test(baseUrl)) {
    throw new Error("Definí BASE_URL con el origen y el prefijo /api.");
  }
  if (!__ENV.SEED_PASSWORD) throw new Error("Definí SEED_PASSWORD.");

  const seed = Number(__ENV.SEED || 42);
  if (!Number.isSafeInteger(seed)) throw new Error("SEED debe ser un entero.");
  const users = positiveInteger("SEED_USERS", 100);
  const vus = positiveInteger("VUS", defaultVus);
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
  return { baseUrl, seed, users, vus, rampSeconds, durationSeconds, serviceShas };
}

/** `thresholds` are the flow's service-level objectives; a breach exits with code 99. */
export function runOptions(config, scenario, thresholds) {
  return {
    scenarios: {
      [scenario]: {
        executor: "ramping-vus",
        startVUs: 0,
        stages: stagesOf(config),
        gracefulRampDown: "30s",
        gracefulStop: "30s",
      },
    },
    thresholds,
    setupTimeout: "5m",
    summaryTrendStats: ["avg", "min", "p(50)", "p(95)", "max"],
    systemTags: ["status", "method", "name", "scenario", "expected_response"],
  };
}

export function stagesOf(config) {
  return [
    { duration: `${config.rampSeconds}s`, target: config.vus },
    { duration: `${config.durationSeconds}s`, target: config.vus },
    { duration: `${config.rampSeconds}s`, target: 0 },
  ];
}

export function jsonBody(response) {
  try {
    return response.json();
  } catch (_) {
    return null;
  }
}

export function accountEmail(config, index) {
  return `seed.${config.seed}.${String(index).padStart(10, "0")}@example.com`;
}

/** Logs the seed account `index` in; the caller decides what a valid answer is. */
export function login(config, index, phase) {
  return http.post(
    `${config.baseUrl}/auth/login`,
    JSON.stringify({
      identifier: accountEmail(config, index),
      password: __ENV.SEED_PASSWORD,
    }),
    {
      headers: { "Content-Type": "application/json" },
      tags: { name: "login", phase },
      redirects: 0,
      timeout: "10s",
    },
  );
}

/** Logs the account in during setup; a session that cannot be opened stops the run. */
export function openSession(config, index) {
  const started = Date.now();
  const response = login(config, index, "setup");
  const session = jsonBody(response);
  if (
    response.status !== 200 ||
    !session ||
    typeof session.access_token !== "string" ||
    !session.access_token ||
    !Number.isFinite(session.expires_in) ||
    session.expires_in <= 0
  ) {
    throw new Error(`Login de cuenta ${index} inválido (HTTP ${response.status}).`);
  }
  return { token: session.access_token, expiresAt: started + session.expires_in * 1000 };
}

/** Tokens are never renewed during the load, so they must outlive the whole run. */
export function assertSessionsLast(config, sessions) {
  const requiredUntil =
    Date.now() + (2 * config.rampSeconds + config.durationSeconds + 30) * 1000;
  if (sessions.some((session) => session.expiresAt <= requiredUntil)) {
    throw new Error("La duración supera la vigencia de los tokens; reducí la corrida.");
  }
}

/** One session per virtual user, each on its own seed account. */
export function openSessions(config) {
  const sessions = [];
  for (let i = 0; i < config.vus; i++) sessions.push(openSession(config, i));
  assertSessionsLast(config, sessions);
  return sessions;
}

/** Builds handleSummary's output: `fields` maps a summary key to a metric name. */
export function summaryOf(config, data, flow, fields, details = {}) {
  const values = (name) => (data.metrics[name] ? data.metrics[name].values : null);
  const summary = {
    recorded_at: new Date().toISOString(),
    environment: __ENV.ENVIRONMENT || "eks",
    base_url: config.baseUrl,
    service_shas: config.serviceShas,
    seed: config.seed,
    seed_users: config.users,
    vus: config.vus,
    ...details,
    stages: stagesOf(config),
    duration_ms: data.state.testRunDurationMs,
    ...Object.fromEntries(Object.entries(fields).map(([key, metric]) => [key, values(metric)])),
    metrics: data.metrics,
  };
  const report = JSON.stringify(summary, null, 2);
  return {
    stdout: `${report}\n`,
    [__ENV.SUMMARY_PATH || `/tmp/${flow}-summary.json`]: report,
  };
}
