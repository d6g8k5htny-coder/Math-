"""The mutation harness must accept only intended assertion kills, never broken tests."""
import importlib.util
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

PATH = Path(__file__).resolve().parents[1] / "tools/cbz_kernel_mutations.py"
harness = None
if PATH.exists():
    spec = importlib.util.spec_from_file_location("cbz_kernel_mutations", PATH)
    harness = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(harness)

SELECTOR = "test_cbz_kernel_gate.NativeGateTests.test_target"
KILL = """FAIL: test_target (test_cbz_kernel_gate.NativeGateTests.test_target)
AssertionError: guard escaped
Ran 1 test in 0.001s
FAILED (failures=1)
"""

def machine_text(text, count=1, failure=True):
    ids = [SELECTOR] if count == 1 else ["synthetic.NativeGateTests.test_" + str(i) for i in range(count)]
    row = {"schema": "cbz.kernel.mutation-lifecycle/v1", "tests_run": count, "expected_ids": ids,
           "body_started": ids, "body_returned": [] if failure else ids,
           "failure_events": [{"test": SELECTOR, "phase": "body", "assertion": True}] if failure else [],
           "error_events": [], "skipped": 0, "expected_failures": 0, "unexpected_successes": 0}
    return text + "CBZM|" + json.dumps(row, sort_keys=True) + "\n"

KILL = machine_text(KILL)


class MutationHarnessTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(harness, "kernel mutation harness is not implemented")

    def lifecycle_fixture(self, body, selector=SELECTOR):
        with tempfile.TemporaryDirectory() as d:
            work = Path(d);(work / "tests").mkdir();output = work / "evidence";output.mkdir()
            (work / "tests/test_cbz_kernel_gate.py").write_text(
                "import unittest\nclass NativeGateTests(unittest.TestCase):\n" + body)
            return harness.run_suite(work, output, "lifecycle", "normal", selector)

    def test_setup_assertion_never_counts_as_selected_body_kill(self):
        result = self.lifecycle_fixture(
            '    def setUp(self): self.fail("setup sentinel")\n'
            '    def test_target(self): raise RuntimeError("body must not execute")\n')
        self.assertEqual(result["assertion_failures"], 1)
        self.assertEqual(result["test_errors"], 0)
        with self.assertRaises(harness.MutationError):
            harness.require_kill(result, SELECTOR)

    def test_teardown_assertion_never_counts_as_selected_body_kill(self):
        result = self.lifecycle_fixture(
            '    def tearDown(self): self.fail("teardown sentinel")\n'
            '    def test_target(self): pass\n')
        with self.assertRaises(harness.MutationError):
            harness.require_kill(result, SELECTOR)

    def test_cleanup_assertion_never_counts_as_selected_body_kill(self):
        result = self.lifecycle_fixture(
            '    def test_target(self): self.addCleanup(lambda: self.fail("cleanup sentinel"))\n')
        with self.assertRaises(harness.MutationError):
            harness.require_kill(result, SELECTOR)

    def test_expected_failure_is_not_a_healthy_baseline_body(self):
        result = self.lifecycle_fixture(
            '    @unittest.expectedFailure\n'
            '    def test_target(self): self.fail("expected body failure")\n')
        with patch.object(harness, "EXPECTED_BASELINE_TESTS", 1), self.assertRaises(harness.MutationError):
            harness.require_baseline(result)

    def test_exact_assertion_failure_is_a_kill(self):
        result = harness.suite_result(1, KILL)
        harness.require_kill(result, SELECTOR)
        self.assertEqual(result["assertion_failures"], 1)

    def test_clean_success_is_not_a_mutant_kill(self):
        result = harness.suite_result(0, "Ran 1 test in 0.001s\nOK\n")
        with self.assertRaises(harness.MutationError):
            harness.require_kill(result, SELECTOR)

    def test_test_errors_are_not_kills(self):
        text = KILL.replace("FAIL:", "ERROR:").replace("failures=1", "errors=1")
        with self.assertRaises(harness.MutationError):
            harness.require_kill(harness.suite_result(1, text), SELECTOR)

    def test_zero_tests_and_missing_summaries_are_not_kills(self):
        for text in ("Ran 0 tests in 0.000s\nOK\n", "Traceback: startup crash\n"):
            with self.subTest(text=text), self.assertRaises(harness.MutationError):
                harness.require_kill(harness.suite_result(1, text), SELECTOR)

    def test_skipped_tests_are_not_kills(self):
        text = KILL.replace("failures=1", "failures=1, skipped=1")
        with self.assertRaises(harness.MutationError):
            harness.require_kill(harness.suite_result(1, text), SELECTOR)

    def test_unrelated_assertion_does_not_kill_declared_mutant(self):
        text = KILL.replace("test_target", "test_other")
        with self.assertRaises(harness.MutationError):
            harness.require_kill(harness.suite_result(1, text), SELECTOR)

    def test_timeout_or_launch_failure_is_not_a_kill(self):
        for code in (124, 127, -9):
            with self.subTest(code=code), self.assertRaises(harness.MutationError):
                harness.require_kill(harness.suite_result(code, KILL), SELECTOR)

    def test_baseline_requires_all_66_healthy_tests(self):
        harness.require_baseline(harness.suite_result(0, machine_text("Ran 66 tests in 0.1s\nOK\n", count=66, failure=False)))
        for text in ("Ran 0 tests in 0.1s\nOK\n", "Ran 65 tests in 0.1s\nOK\n",
                     "Ran 66 tests in 0.1s\nOK (skipped=1)\n"):
            with self.subTest(text=text), self.assertRaises(harness.MutationError):
                harness.require_baseline(harness.suite_result(0, text))

    def test_stale_duplicate_or_noop_anchor_is_not_a_valid_mutation(self):
        for source, before, after in (("x=1\n", "missing", "x=2"),
                                      ("x=1\nx=1\n", "x=1", "x=2"),
                                      ("x=1\n", "x=1", "x=1")):
            with self.subTest(source=source), self.assertRaises(harness.MutationError):
                harness.apply_mutation(source, before, after)

    def test_mutant_must_be_syntactically_valid_before_test_execution(self):
        self.assertEqual(harness.apply_mutation("x=1\n", "x=1", "x=2"), "x=2\n")
        with self.assertRaises(harness.MutationError):
            harness.apply_mutation("x=1\n", "x=1", "def invalid(")

    def test_early_failure_replaces_current_pass_and_preserves_it_as_history(self):
        with tempfile.TemporaryDirectory() as d:
            output = Path(d) / "mutations";output.mkdir()
            (output / "result.json").write_text('{"status":"PASS","synthetic_test":true}\n')
            with patch.object(harness, "CASES", []), contextlib.redirect_stderr(io.StringIO()):
                result = harness.main(["--output", str(output)])
            self.assertEqual(result, 1)
            self.assertEqual(json.loads((output / "result.json").read_text())["status"], "REFUSED")
            self.assertTrue(any(json.loads(p.read_text()).get("synthetic_test")
                                for p in (output / "history").rglob("result.json")))

    def kernel(self):
        path = PATH.with_name("cbz_kernel_gate.py")
        spec = importlib.util.spec_from_file_location("cbz_kernel_custody_test", path)
        module = importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        return module

    def test_two_execution_attempts_preserve_receipt_logs_and_g0_evidence(self):
        kernel = self.kernel()
        with tempfile.TemporaryDirectory() as d:
            output = Path(d);(output / "mutations").mkdir()
            (output / "mutations/result.json").write_text('{"status":"PASS","synthetic_test":true}\n')
            first = kernel.begin_execution(output)
            (first / "receipt.json").write_text('{"synthetic_test":true}\n')
            (first / "control.log").write_text("first actual-attempt log fixture\n")
            kernel.finish_execution(output, first, "PASS")
            second = kernel.begin_execution(output)
            kernel.finish_execution(output, second, "REFUSED")
            self.assertNotEqual(first, second)
            self.assertTrue((first / "receipt.json").is_file())
            self.assertEqual((first / "control.log").read_text(), "first actual-attempt log fixture\n")
            self.assertFalse((second / "receipt.json").exists())
            self.assertEqual(json.loads((output / "current-execution.json").read_text())["status"], "REFUSED")
            self.assertTrue(json.loads((output / "mutations/result.json").read_text())["synthetic_test"])

    def test_failed_execution_cannot_leave_a_current_success_reference(self):
        kernel = self.kernel()
        with tempfile.TemporaryDirectory() as d:
            root = Path(d);output = root / "evidence"
            first = kernel.begin_execution(output)
            (first / "receipt.json").write_text('{"synthetic_test":true}\n')
            kernel.finish_execution(output, first, "PASS")
            with contextlib.redirect_stderr(io.StringIO()):
                result = kernel.main(["--execute", "--root", str(root), "--output", str(output),
                                      "--expected-commit", "not-a-commit"])
            self.assertEqual(result, 1)
            current = json.loads((output / "current-execution.json").read_text())
            self.assertEqual(current["status"], "REFUSED")
            self.assertFalse((output / current["execution"] / "receipt.json").exists())
            self.assertTrue((first / "receipt.json").is_file())

if __name__ == "__main__":
    unittest.main()

