"""Exercise each flow in the real k6 runtime against a disposable HTTP contract fixture."""

import importlib.util
import json
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from harness import JsonHandler, run_k6

THRESHOLD_CROSSED = 99
LOADTESTS = Path(__file__).resolve().parent


def run_flow(script, mode="ok", **overrides):
    """Run `script` against the fixture; returns (result, summary, requests).

    Each request is (method, path, authorization, payload), where payload is the
    JSON body of a POST or the parsed query of a GET.
    """
    requests = []

    class Handler(JsonHandler):
        def do_POST(self):
            body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            requests.append(("POST", self.path, self.headers.get("Authorization"), body))
            if self.path == "/api/auth/login":
                if mode == "bad_login":
                    self.respond(401, {})
                else:
                    self.respond(200, {"access_token": body["identifier"], "expires_in": 900})
            elif mode == "rate_limited":
                self.respond(429, {})
            else:
                self.respond(201, {"id": "post"})

        def do_GET(self):
            url = urlsplit(self.path)
            requests.append(("GET", url.path, self.headers.get("Authorization"), parse_qs(url.query)))
            if url.path == "/api/feed":
                authors = [] if mode == "no_authors" else [
                    {"authorId": "author-a", "authorDeleted": False},
                    {"authorId": "author-gone", "authorDeleted": True},
                ]
                self.respond(200, {"items": authors, "nextCursor": None})
            elif url.path == "/api/search/posts":
                self.respond(200, {"items": [] if mode == "empty" else [{"id": "post"}], "nextCursor": None})
            elif url.path.endswith("/posts"):
                self.respond(200, {"items": [], "nextCursor": None})
            elif mode == "header_error":
                self.respond(500, {})
            else:
                self.respond(200, {"id": url.path.rsplit("/", 1)[1]})

    result, summary = run_k6(script, Handler, **overrides)
    return result, summary, requests


def paths(requests, method, path):
    return [request for request in requests if request[0] == method and request[1] == path]


class LoginTests(unittest.TestCase):
    def test_every_iteration_logs_in_a_seed_account_and_is_measured(self):
        result, summary, requests = run_flow(
            "login.js", SEED_USERS="3", DURATION_SECONDS="2"
        )
        logins = paths(requests, "POST", "/api/auth/login")
        accounts = {body["identifier"] for _, _, _, body in logins}
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertLessEqual(accounts, {f"seed.42.{i:010d}@example.com" for i in range(3)})
        self.assertGreaterEqual(len(accounts), 2)
        self.assertEqual(summary["requests"]["count"], len(logins))
        self.assertEqual(summary["errors"]["rate"], 0)
        self.assertIn("p(95)", summary["duration"])

    def test_rejected_logins_cross_the_error_threshold(self):
        result, summary, _ = run_flow("login.js", "bad_login")
        self.assertEqual(result.returncode, THRESHOLD_CROSSED)
        self.assertEqual(summary["errors"]["rate"], 1)


class CreatePostTests(unittest.TestCase):
    OVERRIDES = {"THINK_SECONDS": "1", "DURATION_SECONDS": "2"}

    def test_each_virtual_user_posts_with_its_own_session(self):
        result, summary, requests = run_flow("create-post.js", **self.OVERRIDES)
        posts = paths(requests, "POST", "/api/posts")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            {token for _, _, token, _ in posts},
            {f"Bearer seed.42.{i:010d}@example.com" for i in range(2)},
        )
        self.assertTrue(all(body["content"].startswith("Prueba de carga") for *_, body in posts))
        self.assertEqual(summary["requests"]["count"], len(posts))
        self.assertEqual(summary["errors"]["rate"], 0)
        self.assertEqual(summary["rate_limited"]["count"], 0)

    def test_rate_limited_posts_are_counted_apart_and_cross_the_error_threshold(self):
        result, summary, _ = run_flow("create-post.js", "rate_limited", **self.OVERRIDES)
        self.assertEqual(result.returncode, THRESHOLD_CROSSED)
        self.assertEqual(summary["rate_limited"]["count"], summary["requests"]["count"])

    def test_a_run_past_the_hourly_post_cap_sends_nothing(self):
        result, _, requests = run_flow("create-post.js", POST_RATE_LIMIT="1", THINK_SECONDS="1")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(requests, [])


class SearchTests(unittest.TestCase):
    def test_searches_use_the_term_list_and_exclude_setup_from_the_metrics(self):
        result, summary, requests = run_flow("search.js", DURATION_SECONDS="2")
        searches = paths(requests, "GET", "/api/search/posts")
        terms = json.loads((LOADTESTS / "search-terms.json").read_text())
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertLessEqual({query["q"][0] for *_, query in searches}, set(terms))
        self.assertEqual(summary["requests"]["count"], len(searches) - 1)
        self.assertEqual(summary["errors"]["rate"], 0)
        self.assertEqual(summary["empty_results"]["count"], 0)

    def test_a_search_without_results_aborts_before_load(self):
        result, _, requests = run_flow("search.js", "empty")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(len(paths(requests, "GET", "/api/search/posts")), 1)

    def test_every_search_term_occurs_in_the_seed_vocabulary(self):
        spec = importlib.util.spec_from_file_location(
            "seed_content", LOADTESTS.parent / "scripts" / "seed" / "content.py"
        )
        content = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(content)
        vocabulary = " ".join(word for group in content.SUBJECTS for word in group).lower()
        for term in json.loads((LOADTESTS / "search-terms.json").read_text()):
            with self.subTest(term=term):
                self.assertIn(term.lower(), vocabulary)


class ProfileTests(unittest.TestCase):
    def test_header_and_posts_are_measured_apart_for_authors_seen_in_the_feed(self):
        result, summary, requests = run_flow("profile.js", DURATION_SECONDS="2")
        self.assertEqual(result.returncode, 0, result.stderr)
        profile_paths = {path for _, path, _, _ in requests if path.startswith("/api/users/")}
        self.assertEqual(profile_paths, {"/api/users/author-a", "/api/users/author-a/posts"})
        self.assertGreater(summary["header_requests"]["count"], 0)
        self.assertEqual(summary["header_requests"]["count"], summary["posts_requests"]["count"])
        self.assertEqual(summary["header_errors"]["rate"], 0)
        self.assertEqual(summary["posts_errors"]["rate"], 0)
        self.assertIn("p(95)", summary["header_duration"])
        self.assertIn("p(95)", summary["posts_duration"])

    def test_a_failing_header_crosses_only_its_own_threshold(self):
        result, summary, _ = run_flow("profile.js", "header_error")
        self.assertEqual(result.returncode, THRESHOLD_CROSSED)
        self.assertEqual(summary["header_errors"]["rate"], 1)
        self.assertEqual(summary["posts_errors"]["rate"], 0)

    def test_feeds_without_authors_abort_before_load(self):
        result, _, requests = run_flow("profile.js", "no_authors")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual([path for _, path, _, _ in requests if path.startswith("/api/users/")], [])


if __name__ == "__main__":
    unittest.main()
