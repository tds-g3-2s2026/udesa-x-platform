"""Regression checks for operational measurement and deployment invariants."""

import json
import os
import unittest
from urllib.parse import urlencode
from urllib.request import urlopen

from render import render


class ObservabilityTests(unittest.TestCase):
    def setUp(self):
        self.payloads = render(
            "metrics-uid", "tempo-uid", "logs-uid", "folder-uid", "Existing Email"
        )

    def test_render_uses_existing_resources_and_keeps_query_variables(self):
        dashboard = self.payloads["dashboard"]
        self.assertFalse(dashboard["overwrite"])
        self.assertEqual(dashboard["folderUid"], "folder-uid")
        self.assertIn("$__rate_interval", json.dumps(dashboard))
        self.assertIn("$service", json.dumps(dashboard))
        self.assertNotIn("${METRICS_UID}", json.dumps(self.payloads))
        for rule in self.payloads["alerts"]:
            self.assertEqual(rule["notification_settings"]["receiver"], "Existing Email")
            self.assertEqual(rule["folderUID"], "folder-uid")
            self.assertEqual(rule["data"][0]["datasourceUid"], "metrics-uid")

    def test_deployment_requires_concrete_resource_identifiers(self):
        with self.assertRaises(ValueError):
            render("${METRICS_UID}", "tempo", "loki", "folder", "Email")
        with self.assertRaises(ValueError):
            render("metrics", "tempo", "loki", "folder", " ")

    def test_alerts_separate_the_six_flows_and_preserve_slo_thresholds(self):
        expected = {
            "login": (0.4, 0.005),
            "feed_first": (0.5, 0.01),
            "feed_next": (0.3, 0.01),
            "create_post": (0.4, 0.01),
            "search_posts": (0.8, 0.01),
            "profile": (0.4, 0.01),
        }
        rules = self.payloads["alerts"]
        self.assertEqual(len({rule["uid"] for rule in rules}), 12)
        for rule in rules:
            flow = rule["labels"]["flow"]
            expression = rule["data"][0]["model"]["expr"]
            self.assertIn(f'udesa_http_flow="{flow}"', expression)
            threshold = rule["data"][1]["model"]["conditions"][0]["evaluator"]["params"][0]
            kind = 0 if rule["uid"].endswith("latency") else 1
            self.assertEqual(threshold, expected[flow][kind])

    def test_idle_flows_do_not_raise_no_data_or_division_by_zero_alerts(self):
        for rule in self.payloads["alerts"]:
            self.assertEqual(rule["noDataState"], "OK")
            self.assertEqual(rule["execErrState"], "Error")
            self.assertEqual(rule["for"], "5m")
            expr = rule["data"][0]["model"]["expr"]
            self.assertIn("[5m]", expr)
            if rule["uid"].endswith("errors"):
                self.assertIn('http_response_status_code=~"5.."', expr)
                self.assertIn("clamp_min", expr)
                self.assertIn("or vector(0)", expr)

    def test_replica_buckets_are_combined_before_quantiles(self):
        for rule in self.payloads["alerts"]:
            if rule["uid"].endswith("latency"):
                self.assertIn(
                    "histogram_quantile(0.95, sum by (le)", rule["data"][0]["model"]["expr"]
                )
        for panel in self.payloads["dashboard"]["dashboard"]["panels"]:
            for target in panel["targets"]:
                self.assertNotIn("service_name", target["expr"])

    def test_correlations_use_exemplar_context_and_structured_log_metadata(self):
        settings = self.payloads["correlation"]
        exemplar = settings["metrics"]["jsonData"]["exemplarTraceIdDestinations"][0]
        self.assertEqual(exemplar["name"], "trace_id")
        self.assertEqual(exemplar["datasourceUid"], "tempo-uid")
        logs = settings["tempo"]["jsonData"]["tracesToLogsV2"]
        self.assertEqual(logs["datasourceUid"], "logs-uid")
        self.assertIn("${__trace.traceId}", logs["query"])
        self.assertEqual(settings["loki"]["jsonData"]["derivedFields"][0]["matcherType"], "label")

    def test_error_ratio_axis_stays_between_zero_and_one(self):
        panels = self.payloads["dashboard"]["dashboard"]["panels"]
        ratios = [
            panel["fieldConfig"]["defaults"]
            for panel in panels
            if panel["fieldConfig"]["defaults"].get("unit") == "percentunit"
        ]
        self.assertTrue(ratios)
        for settings in ratios:
            self.assertEqual(settings["min"], 0)
            self.assertEqual(settings["max"], 1)

    @unittest.skipUnless(os.getenv("PROMETHEUS_URL"), "requires an isolated Prometheus")
    def test_all_queries_are_accepted_by_prometheus(self):
        expressions = [rule["data"][0]["model"]["expr"] for rule in self.payloads["alerts"]]
        for panel in self.payloads["dashboard"]["dashboard"]["panels"]:
            expressions.extend(
                target["expr"]
                .replace("$__rate_interval", "5m")
                .replace("$service", ".*")
                .replace("$health_job", ".*")
                for target in panel["targets"]
            )
        for expression in expressions:
            with self.subTest(expression=expression):
                query = urlencode({"query": expression})
                with urlopen(
                    os.environ["PROMETHEUS_URL"].rstrip("/") + "/api/v1/query?" + query, timeout=10
                ) as response:
                    self.assertEqual(json.load(response)["status"], "success")


if __name__ == "__main__":
    unittest.main()
