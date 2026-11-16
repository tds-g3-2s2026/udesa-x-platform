import http from "k6/http";
import exec from "k6/execution";
import { sleep } from "k6";
import { Counter, Rate, Trend } from "k6/metrics";
import {
  currentSession,
  jsonBody,
  openSessions,
  positiveInteger,
  readConfig,
  runOptions,
  runSeconds,
  summaryOf,
} from "./lib.js";

const config = readConfig(100);
const thinkSeconds = positiveInteger("THINK_SECONDS", 10);
// posts-api caps the posts per account and hour; a run past the cap measures 429s.
const postsPerHour = positiveInteger("POST_RATE_LIMIT", 30);
const postsPerAccount = Math.ceil(runSeconds(config) / thinkSeconds);
if (postsPerAccount > postsPerHour) {
  throw new Error(
    `La corrida publicaría hasta ${postsPerAccount} posts por cuenta y el límite es ${postsPerHour} por hora; subí THINK_SECONDS o reducí la corrida.`,
  );
}

const createDuration = new Trend("create_post_duration", true);
const createErrors = new Rate("create_post_errors");
const createRequests = new Counter("create_post_requests");
const rateLimited = new Counter("create_post_rate_limited");

export const options = runOptions(config, "create_post", {
  create_post_duration: ["p(95)<400"],
  create_post_errors: ["rate<0.01"],
});

export function setup() {
  return openSessions(config);
}

export default function (sessions) {
  const session = currentSession(sessions, "la publicación");
  const response = http.post(
    `${config.baseUrl}/posts`,
    JSON.stringify({
      content: `Prueba de carga ${exec.scenario.iterationInTest}. ¿Quién se suma a repasar álgebra?`,
    }),
    {
      headers: {
        Authorization: `Bearer ${session.token}`,
        "Content-Type": "application/json",
      },
      tags: { name: "create_post", phase: "load" },
      redirects: 0,
      timeout: "10s",
    },
  );
  const body = jsonBody(response);
  const valid = response.status === 201 && body !== null && typeof body.id === "string";
  createRequests.add(1);
  createDuration.add(response.timings.duration);
  createErrors.add(!valid);
  rateLimited.add(response.status === 429 ? 1 : 0);
  sleep(thinkSeconds);
}

export function handleSummary(data) {
  return summaryOf(
    config,
    data,
    "create-post",
    {
      requests: "create_post_requests",
      errors: "create_post_errors",
      rate_limited: "create_post_rate_limited",
      duration: "create_post_duration",
    },
    { think_seconds: thinkSeconds },
  );
}
