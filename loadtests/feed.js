import http from "k6/http";
import exec from "k6/execution";
import { sleep } from "k6";
import { Counter, Rate, Trend } from "k6/metrics";
import {
  assertSessionsLast,
  jsonBody,
  openSession,
  positiveInteger,
  readConfig,
  runOptions,
  summaryOf,
} from "./lib.js";

const config = readConfig(200);
const pages = positiveInteger("PAGES", 5);

const feedDuration = new Trend("feed_duration", true);
const firstPageDuration = new Trend("feed_first_page_duration", true);
const nextPageDuration = new Trend("feed_next_page_duration", true);
const feedErrors = new Rate("feed_errors");
const feedRequests = new Counter("feed_requests");
const emptyPages = new Counter("feed_empty_pages");

export const options = runOptions(config, "feed", {
  feed_first_page_duration: ["p(95)<500"],
  feed_next_page_duration: ["p(95)<300"],
  feed_errors: ["rate<0.01"],
});

function readPage(token, cursor, phase) {
  const response = http.get(
    `${config.baseUrl}/feed${cursor ? `?cursor=${encodeURIComponent(cursor)}` : ""}`,
    {
      headers: { Authorization: `Bearer ${token}` },
      tags: { name: cursor ? "feed_next_page" : "feed_first_page", phase },
      redirects: 0,
      timeout: "10s",
    },
  );
  const body = jsonBody(response);
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
  for (let i = 0; i < config.vus; i++) {
    const session = openSession(config, i);
    const page = readPage(session.token, null, "setup");
    if (!page.valid || page.body.items.length === 0) {
      throw new Error(
        `Feed de cuenta ${i} inválido o vacío (HTTP ${page.status}).`,
      );
    }
    sessions.push(session);
  }
  assertSessionsLast(config, sessions);
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
  return summaryOf(
    config,
    data,
    "feed",
    {
      requests: "feed_requests",
      errors: "feed_errors",
      empty_pages: "feed_empty_pages",
      duration: "feed_duration",
      first_page_duration: "feed_first_page_duration",
      next_page_duration: "feed_next_page_duration",
    },
    { pages_per_iteration: pages },
  );
}
