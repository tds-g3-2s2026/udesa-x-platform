import http from "k6/http";
import exec from "k6/execution";
import { sleep } from "k6";
import { Counter, Rate, Trend } from "k6/metrics";
import {
  assertSessionsLast,
  jsonBody,
  openSession,
  readConfig,
  runOptions,
  summaryOf,
} from "./lib.js";

const config = readConfig(200);

const headerDuration = new Trend("profile_header_duration", true);
const headerErrors = new Rate("profile_header_errors");
const headerRequests = new Counter("profile_header_requests");
const postsDuration = new Trend("profile_posts_duration", true);
const postsErrors = new Rate("profile_posts_errors");
const postsRequests = new Counter("profile_posts_requests");

export const options = runOptions(config, "profile", {
  profile_header_duration: ["p(95)<400"],
  profile_header_errors: ["rate<0.01"],
  profile_posts_duration: ["p(95)<400"],
  profile_posts_errors: ["rate<0.01"],
});

function get(path, name, token) {
  return http.get(`${config.baseUrl}${path}`, {
    headers: { Authorization: `Bearer ${token}` },
    tags: { name, phase: "load" },
    redirects: 0,
    timeout: "10s",
  });
}

export function setup() {
  const sessions = [];
  const authors = new Set();
  for (let i = 0; i < config.vus; i++) {
    const session = openSession(config, i);
    const response = http.get(`${config.baseUrl}/feed`, {
      headers: { Authorization: `Bearer ${session.token}` },
      tags: { name: "feed_first_page", phase: "setup" },
      redirects: 0,
      timeout: "10s",
    });
    const body = jsonBody(response);
    if (response.status !== 200 || !body || !Array.isArray(body.items)) {
      throw new Error(`Feed de cuenta ${i} inválido (HTTP ${response.status}).`);
    }
    for (const item of body.items) {
      if (!item.authorDeleted) authors.add(item.authorId);
    }
    sessions.push(session);
  }
  assertSessionsLast(config, sessions);
  // The profiles to open are the authors seen in the accounts' own feeds, so the
  // run depends on the data and not on how the seed derives its identifiers.
  if (authors.size === 0) {
    throw new Error("Los feeds no muestran autores; ¿está cargado el seed?");
  }
  return { sessions, authors: [...authors] };
}

export default function ({ sessions, authors }) {
  const session = sessions[exec.vu.idInTest - 1];
  if (!session || Date.now() >= session.expiresAt) {
    exec.test.abort("Cuenta sin sesión vigente; la corrida no mide el perfil.");
  }
  const author = authors[exec.scenario.iterationInTest % authors.length];

  const header = get(`/users/${author}`, "profile_header", session.token);
  const headerBody = jsonBody(header);
  headerRequests.add(1);
  headerDuration.add(header.timings.duration);
  headerErrors.add(
    !(header.status === 200 && headerBody !== null && headerBody.id === author),
  );

  const posts = get(`/users/${author}/posts`, "profile_posts", session.token);
  const postsBody = jsonBody(posts);
  postsRequests.add(1);
  postsDuration.add(posts.timings.duration);
  postsErrors.add(
    !(
      posts.status === 200 &&
      postsBody !== null &&
      Array.isArray(postsBody.items) &&
      (postsBody.nextCursor === null ||
        (typeof postsBody.nextCursor === "string" && postsBody.nextCursor.length > 0))
    ),
  );
  sleep(1);
}

export function handleSummary(data) {
  return summaryOf(config, data, "profile", {
    header_requests: "profile_header_requests",
    header_errors: "profile_header_errors",
    header_duration: "profile_header_duration",
    posts_requests: "profile_posts_requests",
    posts_errors: "profile_posts_errors",
    posts_duration: "profile_posts_duration",
  });
}
