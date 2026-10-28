import ast
import contextlib
import io
import json
from pathlib import Path
import socket
import unittest
from unittest.mock import patch

from impulse_lab.__main__ import main
from impulse_lab.model import SCENARIOS, simulate


class LabTests(unittest.TestCase):
    def test_baseline_has_no_loss_or_wait(self):
        _, result = simulate("baseline", 20)
        self.assertEqual(result["completed"], 40)
        self.assertEqual(result["remaining"], 0)
        self.assertEqual(result["mean_wait_ticks"], 0)
        self.assertEqual(result["queue_dropped"], 0)

    def test_congestion_and_admission_control(self):
        _, congested = simulate("congestion", 20)
        _, limited = simulate("rate-limit", 20)
        self.assertGreater(congested["queue_dropped"], 0)
        self.assertGreater(congested["mean_wait_ticks"], 0)
        self.assertEqual(limited["queue_dropped"], 0)
        self.assertEqual(limited["rate_limited"], 60)
        self.assertEqual(limited["completed"], congested["completed"])
        self.assertEqual(limited["mean_wait_ticks"], 0)

    def test_accounting_and_capacity_for_every_valid_run(self):
        for scenario in SCENARIOS:
            for ticks in range(1, 101):
                events, result = simulate(scenario, ticks)
                self.assertEqual(len(events), ticks)
                self.assertEqual(result["offered"], sum(result[key] for key in
                    ("completed", "remaining", "rate_limited", "queue_dropped")))
                self.assertLessEqual(result["peak_queue_depth"], 12)
                for event in events:
                    self.assertGreaterEqual(event["queue_depth"], 0)
                    self.assertLessEqual(event["queue_depth"], 12)
                    self.assertEqual(event["offered"], event["admitted"] +
                        event["rate_limited"] + event["queue_dropped"])

    def test_reproducibility(self):
        self.assertEqual(simulate("congestion"), simulate("congestion"))

    def test_api_rejects_invalid_bounds(self):
        for value in (0, -1, 101, 10**9, True, 1.5, "20", None):
            with self.subTest(value=value), self.assertRaises(ValueError):
                simulate(ticks=value)
        with self.assertRaises(ValueError):
            simulate("external")

    def test_cli_rejects_legacy_and_invalid_options(self):
        for args in (["--target", "localhost"], ["--threads", "1"],
                     ["--method", "SMS"], ["--time", "1"], ["--ticks", "101"],
                     ["--ticks", "0"], ["--ticks", "x"], ["--tick", "2"],
                     ["--scenario", "unknown"]):
            with self.subTest(args=args), contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as error:
                    main(args)
                self.assertEqual(error.exception.code, 2)

    def test_jsonl_and_no_socket_or_dns_use(self):
        with patch.object(socket, "socket", side_effect=AssertionError("network forbidden")), \
             patch.object(socket, "getaddrinfo", side_effect=AssertionError("DNS forbidden")):
            for scenario in SCENARIOS:
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    main(["--scenario", scenario, "--ticks", "100", "--events"])
                records = [json.loads(line) for line in output.getvalue().splitlines()]
                self.assertEqual(len(records), 101)
                self.assertTrue(all(record["synthetic"] for record in records))
                self.assertEqual(records[-1]["type"], "summary")

    def test_runtime_import_allowlist(self):
        root = Path(__file__).resolve().parents[1]
        allowed = {"argparse", "json", "model"}
        for path in (root / "impulse_lab").glob("*.py"):
            for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
                if isinstance(node, ast.Import):
                    self.assertTrue(all(item.name in allowed for item in node.names))
                elif isinstance(node, ast.ImportFrom):
                    self.assertIn(node.module, allowed)
                elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                    self.assertNotIn(node.func.id, {"exec", "eval", "__import__", "open"})
        self.assertFalse((root / "tools").exists())
        self.assertFalse((root / "impulse.py").exists())
        self.assertFalse((root / "requirements.txt").exists())


if __name__ == "__main__":
    unittest.main()
