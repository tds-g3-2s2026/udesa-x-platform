import http from "k6/http";
import exec from "k6/execution";
import { sleep } from "k6";
import { Counter, Rate, Trend } from "k6/metrics";
import { jsonBody, openSessions, readConfig, runOptions, summaryOf } from "./lib.js";

const config = readConfig(100);
const terms = JSON.parse(open("./search-terms.json"));

const searchDuration = new Trend("search_duration", true);
const searchErrors = new Rate("search_errors");
const searchRequests = new Counter("search_requests");
const emptyResults = new Counter("search_empty_results");

export const options = runOptions(config, "search", {
  search_duration: ["p(95)<800"],
  search_errors: ["rate<0.01"],
});

function search(token, term, phase) {
  const response = http.get(
    `${config.baseUrl}/search/posts?q=${encodeURIComponent(term)}`,
    {
      headers: { Authorization: `Bearer ${token}` },
      tags: { name: "search_posts", phase },
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
    searchRequests.add(1);
    searchDuration.add(response.timings.duration);
    searchErrors.add(!valid);
    emptyResults.add(valid && body.items.length === 0 ? 1 : 0);
  }
  return { valid, status: response.status, body };
}

export function setup() {
  const sessions = openSessions(config);
  const result = search(sessions[0].token, terms[0], "setup");
  if (!result.valid || result.body.items.length === 0) {
    throw new Error(
      `La búsqueda de "${terms[0]}" es inválida o no devuelve resultados (HTTP ${result.status}); ¿está cargado el seed?`,
    );
  }
  return sessions;
}

export default function (sessions) {
  const session = sessions[exec.vu.idInTest - 1];
  if (!session || Date.now() >= session.expiresAt) {
    exec.test.abort("Cuenta sin sesión vigente; la corrida no mide la búsqueda.");
  }
  search(session.token, terms[exec.scenario.iterationInTest % terms.length], "load");
  sleep(1);
}

export function handleSummary(data) {
  return summaryOf(
    config,
    data,
    "search",
    {
      requests: "search_requests",
      errors: "search_errors",
      empty_results: "search_empty_results",
      duration: "search_duration",
    },
    { terms },
  );
}
