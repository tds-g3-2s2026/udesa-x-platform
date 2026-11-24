import exec from "k6/execution";
import { sleep } from "k6";
import { Counter, Rate, Trend } from "k6/metrics";
import {
  currentSession,
  getAuthed,
  isPage,
  jsonBody,
  openSessions,
  readConfig,
  runOptions,
  summaryOf,
} from "./lib.js";

const config = readConfig(20);

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

export function setup() {
  const sessions = openSessions(config);
  const authors = new Set();
  sessions.forEach((session, i) => {
    const response = getAuthed(config, "/feed", session.token, "feed_first_page", "setup");
    const body = jsonBody(response);
    if (!isPage(response, body)) {
      throw new Error(`Feed de cuenta ${i} inválido (HTTP ${response.status}).`);
    }
    for (const item of body.items) {
      if (!item.authorDeleted) authors.add(item.authorId);
    }
  });
  // The profiles to open are the authors seen in the accounts' own feeds, so the
  // run depends on the data and not on how the seed derives its identifiers.
  if (authors.size === 0) {
    throw new Error("Los feeds no muestran autores; ¿está cargado el seed?");
  }
  return { sessions, authors: [...authors] };
}

export default function ({ sessions, authors }) {
  const session = currentSession(sessions, "el perfil");
  const author = authors[exec.scenario.iterationInTest % authors.length];

  const header = getAuthed(config, `/users/${author}`, session.token, "profile_header", "load");
  const headerBody = jsonBody(header);
  headerRequests.add(1);
  headerDuration.add(header.timings.duration);
  headerErrors.add(
    !(header.status === 200 && headerBody !== null && headerBody.id === author),
  );

  const posts = getAuthed(config, `/users/${author}/posts`, session.token, "profile_posts", "load");
  postsRequests.add(1);
  postsDuration.add(posts.timings.duration);
  postsErrors.add(!isPage(posts, jsonBody(posts)));
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
