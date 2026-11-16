import exec from "k6/execution";
import { sleep } from "k6";
import { Counter, Rate, Trend } from "k6/metrics";
import { jsonBody, login, readConfig, runOptions, summaryOf } from "./lib.js";

const config = readConfig(100);

const loginDuration = new Trend("login_duration", true);
const loginErrors = new Rate("login_errors");
const loginRequests = new Counter("login_requests");

export const options = runOptions(config, "login", {
  login_duration: ["p(95)<400"],
  login_errors: ["rate<0.005"],
});

export default function () {
  // Consecutive iterations walk the seed accounts, so every login is a fresh one.
  const response = login(config, exec.scenario.iterationInTest % config.users, "load");
  const session = jsonBody(response);
  const valid =
    response.status === 200 &&
    session !== null &&
    typeof session.access_token === "string" &&
    session.access_token.length > 0;
  loginRequests.add(1);
  loginDuration.add(response.timings.duration);
  loginErrors.add(!valid);
  sleep(1);
}

export function handleSummary(data) {
  return summaryOf(config, data, "login", {
    requests: "login_requests",
    errors: "login_errors",
    duration: "login_duration",
  });
}
