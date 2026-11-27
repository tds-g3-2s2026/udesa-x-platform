import exec from "k6/execution";
import { sleep } from "k6";
import { Counter, Rate, Trend } from "k6/metrics";
import { jsonBody, login, readConfig, runOptions, summaryOf } from "./lib.js";

const config = readConfig(10);

const preparationDuration = new Trend("login_preparation_duration", true);
const loginDuration = new Trend("login_duration", true);
const loginErrors = new Rate("login_errors");
const loginRequests = new Counter("login_requests");

export const options = runOptions(config, "login", {
  login_duration: ["p(95)<400"],
  login_errors: ["rate<0.005"],
});

function isSuccessfulLogin(response) {
  const session = jsonBody(response);
  return response.status === 200 && typeof session?.access_token === "string" &&
    session.access_token.length > 0;
}

export function setup() {
  for (let index = 0; index < config.vus; index++) {
    const response = login(config, index, "setup");
    if (!isSuccessfulLogin(response)) {
      throw new Error(`No se pudo preparar el login de la cuenta ${index}.`);
    }
    preparationDuration.add(response.timings.duration);
  }
}

export default function () {
  const response = login(config, exec.vu.idInTest - 1, "load");
  loginRequests.add(1);
  loginDuration.add(response.timings.duration);
  loginErrors.add(!isSuccessfulLogin(response));
  sleep(1);
}

export function handleSummary(data) {
  return summaryOf(config, data, "login", {
    requests: "login_requests",
    errors: "login_errors",
    duration: "login_duration",
    preparation_duration: "login_preparation_duration",
  });
}
