"""Exercise the real k6 runtime against a disposable HTTP contract fixture."""

import json
import unittest
from urllib.parse import parse_qs, urlsplit

from harness import JsonHandler, run_k6

CURSOR = "opaque/+?&="


class FeedTests(unittest.TestCase):
    def run_feed(self, mode="ok", **overrides):
        logins, reads = [], []

        class Handler(JsonHandler):
            def do_POST(self):
                body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                logins.append((self.path, body))
                if mode == "bad_login":
                    self.respond(401, {})
                else:
                    self.respond(
                        200,
                        {
                            "access_token": body["identifier"],
                            "expires_in": 1 if mode == "expired" else 900,
                        },
                    )

            def do_GET(self):
                url = urlsplit(self.path)
                cursor = parse_qs(url.query).get("cursor", [None])[0]
                reads.append((url.path, cursor, self.headers.get("Authorization")))
                if cursor is not None and mode == "server_error":
                    self.respond(503, {})
                elif cursor is not None and mode == "bad_contract":
                    self.respond(200, {"items": []})
                else:
                    self.respond(
                        200,
                        {
                            "items": [] if mode == "empty" else [{"id": "post"}],
                            "nextCursor": CURSOR if cursor is None else None,
                        },
                    )

        result, summary = run_k6("feed.js", Handler, **overrides)
        return result, summary, logins, reads

    def test_pagination_uses_distinct_accounts_and_excludes_setup_from_feed_metrics(self):
        result, summary, logins, reads = self.run_feed()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(logins), 2)
        self.assertEqual({path for path, _ in logins}, {"/api/auth/login"})
        self.assertEqual(
            {body["identifier"] for _, body in logins},
            {
                "seed.42.0000000000@example.com",
                "seed.42.0000000001@example.com",
            },
        )
        self.assertTrue(all(body["password"] == "fixture-password" for _, body in logins))
        self.assertEqual({path for path, _, _ in reads}, {"/api/feed"})
        self.assertEqual({cursor for _, cursor, _ in reads}, {None, CURSOR})
        self.assertEqual(
            {token for _, _, token in reads}, {f"Bearer {body['identifier']}" for _, body in logins}
        )
        self.assertEqual(summary["requests"]["count"], len(reads) - 2)
        self.assertEqual(summary["errors"]["rate"], 0)
        self.assertIn("p(50)", summary["first_page_duration"])
        self.assertIn("p(95)", summary["next_page_duration"])
        self.assertEqual(summary["empty_pages"]["count"], 0)
        self.assertEqual(summary["environment"], "contract-test")
        self.assertNotIn("fixture-password", json.dumps(summary))
        self.assertNotIn("Bearer", json.dumps(summary))

    def test_server_and_contract_errors_are_recorded_and_cross_the_error_threshold(self):
        for mode in ("server_error", "bad_contract"):
            with self.subTest(mode=mode):
                result, summary, _, reads = self.run_feed(mode)
                self.assertEqual(result.returncode, 99, result.stderr)
                expected_errors = sum(cursor is not None for _, cursor, _ in reads)
                self.assertGreater(expected_errors, 0)
                self.assertAlmostEqual(
                    summary["errors"]["rate"],
                    expected_errors / summary["requests"]["count"],
                )

    def test_invalid_accounts_empty_feeds_and_expiring_sessions_abort_before_load(self):
        for mode in ("bad_login", "empty", "expired"):
            with self.subTest(mode=mode):
                result, summary, _, reads = self.run_feed(mode)
                self.assertNotEqual(result.returncode, 0)
                self.assertTrue(summary is None or summary["requests"] is None)
                self.assertTrue(all(cursor is None for _, cursor, _ in reads))

    def test_invalid_configuration_does_not_send_requests(self):
        for overrides in ({"VUS": "101"}, {"USERS_SHA": "unknown"}, {"PAGES": "0"}):
            with self.subTest(overrides=overrides):
                result, _, logins, reads = self.run_feed(**overrides)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(logins, [])
                self.assertEqual(reads, [])


if __name__ == "__main__":
    unittest.main()
