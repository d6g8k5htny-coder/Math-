"""Mutation custody and child-health controls; a crashed CLI never kills a mutant."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
import sys
import ast
from unittest.mock import patch

PATH = Path(__file__).resolve().parents[1] / "tools/c8_quarantine_mutations.py"
h = None
if PATH.exists():
    spec = importlib.util.spec_from_file_location("c8_mutation_harness", PATH)
    h = importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
SELECTOR = "test_c8_quarantine.C8Quarantine.test_unknown_output_is_not_coverage_or_admission"


class HarnessControls(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(h, "C8 mutation harness is missing")

    def result(self):
        return {"returncode": 1, "tests_run": 1, "failures": [{"id": SELECTOR, "kind": "AssertionError"}],
                "errors": [], "skipped": [], "expected_failures": [], "unexpected_successes": [],
                "selected_ids": [SELECTOR], "lifecycle": self.lifecycle([SELECTOR], [SELECTOR]),
                "cli_health": [{"healthy": True, "test_id": SELECTOR, "phase": "body"}], "smoke": {"healthy": True}}

    def lifecycle(self, ids, failures):
        rows=[]
        for identity in ids:
            rows.append({"id":identity,"supported":True,"setup_entered":1,"setup_completed":1,
                "body_entered":1,"body_exited":1,"teardown_entered":1,"teardown_completed":1,
                "cleanup_entered":0,"cleanup_completed":0,"failure_count":failures.count(identity),"error_count":0})
        return {"schema":"unittest.body-phase/v1","tests":rows,"events":[{
            "id":identity,"phase":"body","kind":"failure","exception":"AssertionError","assertion":True}
            for identity in failures]}

    def test_intended_assertion_is_the_only_accepted_kill(self):
        h.check_run(self.result(), 1, SELECTOR)

    def test_success_errors_skips_wrong_selector_and_zero_are_not_kills(self):
        changes = [{"returncode": 0}, {"errors": [{"id": SELECTOR}]}, {"skipped": [SELECTOR]},
                   {"tests_run": 0}, {"failures": [{"id": "other", "kind": "AssertionError"}]},
                   {"failures": [{"id": SELECTOR, "kind": "RuntimeError"}]}]
        for change in changes:
            with self.subTest(change=change), self.assertRaises(h.MutationError):
                result = self.result();result.update(change);h.check_run(result, 1, SELECTOR)

    def test_all_cli_health_is_required_even_after_a_healthy_smoke(self):
        result = self.result();result["cli_health"].append({"healthy": False})
        with self.assertRaisesRegex(h.MutationError, "unhealthy CLI"):
            h.check_run(result, 1, SELECTOR)

    def test_zero_cli_calls_do_not_qualify_a_cli_control(self):
        result = self.result();result["cli_health"] = []
        with self.assertRaises(h.MutationError):h.check_run(result, 1, SELECTOR)

    def test_healthy_baseline_requires_all_41_methods_and_no_errors_or_skips(self):
        result = self.result();result.update(returncode=0, tests_run=41, failures=[])
        tree=ast.parse((h.ROOT/h.TEST).read_text())
        names=sorted(n.name for c in tree.body if isinstance(c,ast.ClassDef) and c.name=="C8Quarantine"
                     for n in c.body if isinstance(n,ast.FunctionDef) and n.name.startswith("test_"))
        ids=["test_c8_quarantine.C8Quarantine."+name for name in names]
        result.update(selected_ids=ids,lifecycle=self.lifecycle(ids,[]))
        h.check_run(result, 41)
        result["tests_run"] = 40
        with self.assertRaises(h.MutationError):h.check_run(result, 41)

    def test_stale_noop_duplicate_and_noncompiling_mutations_refuse(self):
        for source, before, after in (("x=1", "missing", "x=2"), ("x=1", "x=1", "x=1"),
                                       ("x=1\nx=1", "x=1", "x=2"), ("x=1", "x=1", "def invalid(")):
            with self.subTest(before=before), self.assertRaises(h.MutationError):h.apply_mutation(source, before, after)

    def actual(self, replacement, method):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d);work = root / "work";out = root / "out";out.mkdir()
            h.materialize(work)
            source = (work / h.TOOL).read_text()
            (work / h.TOOL).write_text(replacement(source))
            return h.run_suite(work, out, "probe", "optimized" if sys.flags.optimize else "normal", method)

    def test_input_dependent_invalid_json_cannot_fake_an_assertion_kill(self):
        def bad(source):
            return 'import sys\n' + source.replace('    raise SystemExit(main())',
                '    if "--consume-output" in sys.argv:\n        print("not-json"); raise SystemExit(1)\n    raise SystemExit(main())')
        result = self.actual(bad, SELECTOR)
        self.assertTrue(result["smoke"]["healthy"])
        self.assertEqual((len(result["failures"]), len(result["errors"])), (1, 0))
        with self.assertRaisesRegex(h.MutationError, "unhealthy CLI"):h.check_run(result, 1, SELECTOR)

    def test_input_dependent_runtime_crash_cannot_fake_an_assertion_kill(self):
        def bad(source):
            return 'import sys\n' + source.replace('    raise SystemExit(main())',
                '    if "--consume-output" in sys.argv:\n        raise RuntimeError("input-dependent crash")\n    raise SystemExit(main())')
        result = self.actual(bad, SELECTOR)
        self.assertTrue(result["smoke"]["healthy"])
        self.assertEqual((len(result["failures"]), len(result["errors"])), (1, 0))
        with self.assertRaisesRegex(h.MutationError, "unhealthy CLI"):h.check_run(result, 1, SELECTOR)

    def test_input_dependent_malformed_counter_structure_is_not_a_kill(self):
        def bad(source):
            return source.replace('    print(json.dumps(report, indent=2, sort_keys=True))',
                '    if args.consume_output:\n        report["denied_output_count"] = "not-an-integer"\n    print(json.dumps(report, indent=2, sort_keys=True))').replace('        code = 2', '        code = 1')
        result = self.actual(bad, SELECTOR)
        self.assertTrue(result["smoke"]["healthy"])
        with self.assertRaisesRegex(h.MutationError, "unhealthy CLI"):h.check_run(result, 1, SELECTOR)

    def test_startup_crash_never_counts_as_a_kill(self):
        result = self.actual(lambda s: 'raise RuntimeError("startup crash")\n' + s, SELECTOR)
        with self.assertRaisesRegex(h.MutationError, "unhealthy CLI"):h.check_run(result, 1, SELECTOR)

    def test_healthy_semantic_false_clear_is_an_actual_assertion_kill(self):
        selector = "test_c8_quarantine.C8Quarantine.test_all_106_published_denied_outputs_are_mechanically_denied"
        result = self.actual(lambda s: s.replace('if path in checked["denied"]:', 'if False:'), selector)
        h.check_run(result, 1, selector)
        self.assertTrue(all(v["healthy"] for v in result["cli_health"]))

    def test_subtest_failures_are_counted_and_multiple_failures_do_not_qualify(self):
        selector = "test_c8_quarantine.C8Quarantine.test_packet_and_normalized_source_aliases_refuse"
        result = self.actual(lambda s: s.replace('if denied:\n                report["problems"]',
                                               'if False:\n                report["problems"]'), selector)
        self.assertEqual(len(result["failures"]), 3)
        with self.assertRaises(h.MutationError):h.check_run(result, 1, selector)

    def test_subtest_runtime_error_is_retained_and_never_qualifies(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d);work = root / "work";out = root / "out";out.mkdir();h.materialize(work)
            path = work / h.TEST;source = path.read_text()
            start = source.index('    def test_unknown_output_is_not_coverage_or_admission(self):')
            end = source.index('\n    def ', start + 5)
            source = source[:start] + '    def test_unknown_output_is_not_coverage_or_admission(self):\n        with self.subTest(probe=True):\n            raise RuntimeError("subtest crash")\n' + source[end:]
            path.write_text(source);result = h.run_suite(work, out, "error-probe", "normal", SELECTOR)
            self.assertEqual(result["errors"], [{"id": SELECTOR, "kind": "RuntimeError"}])
            with self.assertRaises(h.MutationError):h.check_run(result, 1, SELECTOR, 0)

    def test_early_refusal_preserves_prior_receipt_and_clears_current_pass(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "mutations";out.mkdir();(out / "result.json").write_text('{"status":"PASS","synthetic":true}\n')
            with patch.object(h, "CASES", []), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(h.main(["--output", str(out)]), 1)
            self.assertEqual(json.loads((out / "result.json").read_text())["status"], "REFUSED")
            self.assertTrue(any(json.loads(p.read_text()).get("synthetic") for p in (out / "history").rglob("result.json")))

    def fixture_probe(self, phase, minimum=1):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d);work = root / "work";out = root / "out";out.mkdir();h.materialize(work)
            method = ("test_fraction_checker_rejects_a_false_endpoint" if minimum == 0
                      else "test_unknown_output_is_not_coverage_or_admission")
            selector = "test_c8_quarantine.C8Quarantine." + method
            marker = root / "body-entered"
            extra = '\n_original_setup=C8Quarantine.setUp\n_original_body=C8Quarantine.' + method + '\n'
            extra += 'def _body(self):\n    Path(' + repr(str(marker)) + ').write_text("entered")\n    _original_body(self)\n'
            if phase == "body":extra += '    self.fail("body assertion control")\n'
            extra += 'C8Quarantine.' + method + '=_body\n'
            if phase == "setup":
                extra += 'def _fixture(self):\n    _original_setup(self)\n'
                if minimum:extra += '    self.cli()\n'
                extra += '    self.fail("setup assertion control")\nC8Quarantine.setUp=_fixture\n'
            elif phase == "teardown":
                extra += 'def _fixture(self):\n    self.fail("teardown assertion control")\nC8Quarantine.tearDown=_fixture\n'
            elif phase == "cleanup":
                extra += 'def _fixture(self):\n    _original_setup(self)\n    self.addCleanup(self.fail,"cleanup assertion control")\nC8Quarantine.setUp=_fixture\n'
            path = work / h.TEST;path.write_text(path.read_text() + extra)
            result = h.run_suite(work, out, "fixture", "optimized" if sys.flags.optimize else "normal", selector)
            return result, selector, marker.exists()

    def test_setup_assertion_is_not_an_intended_body_kill(self):
        result, selector, entered = self.fixture_probe("setup")
        self.assertFalse(entered);self.assertTrue(all(v["healthy"] for v in result["cli_health"]))
        with self.assertRaises(h.MutationError):h.check_run(result, 1, selector)

    def test_teardown_assertion_is_not_an_intended_body_kill(self):
        result, selector, entered = self.fixture_probe("teardown")
        self.assertTrue(entered)
        with self.assertRaises(h.MutationError):h.check_run(result, 1, selector)

    def test_cleanup_assertion_is_not_an_intended_body_kill(self):
        result, selector, entered = self.fixture_probe("cleanup")
        self.assertTrue(entered)
        with self.assertRaises(h.MutationError):h.check_run(result, 1, selector)

    def test_fraction_setup_without_cli_is_not_an_intended_body_kill(self):
        result, selector, entered = self.fixture_probe("setup", 0)
        self.assertFalse(entered)
        with self.assertRaises(h.MutationError):h.check_run(result, 1, selector, 0)

    def test_genuine_body_assertion_records_completed_fixture_and_body(self):
        result, selector, entered = self.fixture_probe("body")
        self.assertTrue(entered);h.check_run(result, 1, selector)
        self.assertIn("lifecycle", result)
        self.assertEqual(result["lifecycle"]["events"], [{"id": selector, "phase": "body", "kind": "failure",
            "exception":"AssertionError","assertion":True}])
        self.assertEqual(result["lifecycle"]["tests"][0]["body_exited"], 1)

    def test_missing_baseline_body_evidence_refuses(self):
        result = self.result();result["lifecycle"] = {"schema": "unittest.body-phase/v1", "tests": [], "events": []}
        with self.assertRaises(h.MutationError):h.check_run(result, 1, SELECTOR)

    def test_phase_counter_provenance_is_required(self):
        for target,key,value in (("test","body_entered",True),("test","body_exited",0),
                                  ("test","failure_count",0),("event","phase","cleanup"),("event","assertion",False)):
            with self.subTest(key=key):
                result=self.result();result["lifecycle"]["tests" if target=="test" else "events"][0][key]=value
                with self.assertRaises(h.MutationError):h.check_run(result,1,SELECTOR)

    def test_stale_observation_cannot_survive_a_later_startup_failure(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);work=root/"work";out=root/"out";out.mkdir();h.materialize(work)
            source=(work/h.TOOL).read_text();(work/h.TOOL).write_text(source.replace('        code = 2','        code = 0'))
            mode="optimized" if sys.flags.optimize else "normal"
            first=h.run_suite(work,out,"reuse",mode,SELECTOR);h.check_run(first,1,SELECTOR)
            receipt=out/("reuse-"+mode+".json");original=receipt.read_bytes()
            path=work/h.TEST;path.write_text('raise RuntimeError("startup control")\n'+path.read_text())
            with self.assertRaises(h.MutationError):
                second=h.run_suite(work,out,"reuse",mode,SELECTOR);h.check_run(second,1,SELECTOR)
            self.assertEqual(receipt.read_bytes(),original)


if __name__ == "__main__":
    unittest.main()
