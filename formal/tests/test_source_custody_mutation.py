"""Finite source mutation checks: every mutant must fail its intended real observation."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

HERE = Path(__file__).resolve().parents[1]


class CustodyMutationTests(unittest.TestCase):
    def test_grader_rejects_exit_two_even_with_plausible_failure_text(self):
        false_evidence = subprocess.CompletedProcess(
            args=[], returncode=2,
            stdout='Ran 1 test\\nValueError not raised\\nTrue is not false\\n'
                   'POISONED_CACHED_HELPER\\nAssertionError\\n')
        with mock.patch.object(subprocess, 'run', return_value=false_evidence):
            with self.assertRaisesRegex(AssertionError, 'exact mutation-test exit'):
                self.test_all_declared_source_mutants_are_detected_for_their_reason()

    def test_all_declared_source_mutants_are_detected_for_their_reason(self):
        source = (HERE / 'gate.py').read_text()
        cases = [
            ('committed-domain',
             "    verify_committed_files(repo, head, [prefix + name for name in names])",
             "    pass  # planted committed-domain bypass",
             'test_source_custody.SourceCustodyTests.test_execute_refuses_dirty_overlay_before_kernel',
             'ValueError not raised'),
            ('dependency-working-bytes',
             "require(actual == oid, 'working bytes differ",
             "require(True, 'working bytes differ",
             'test_source_custody.SourceCustodyTests.test_dependency_assume_unchanged_lean_is_refused',
             'ValueError not raised'),
            ('symlink-working-bytes',
             "require(actual == oid, 'working bytes differ",
             "require(True, 'working bytes differ",
             'test_source_custody.SourceCustodyTests.test_dependency_hidden_symlink_retargeting_is_refused',
             'ValueError not raised'),
            ('symlink-target-boundary',
             "require(target.is_relative_to(repo) and\n                    target.relative_to(repo).as_posix() in tree and\n                    tree[target.relative_to(repo).as_posix()][0] in ('100644', '100755') and target.is_file(),",
             "require(True,",
             'test_source_custody.SourceCustodyTests.test_dependency_refuses_symlink_target_outside_bound_tree',
             'ValueError not raised'),
            ('index',
             "require(index == tree, 'source index",
             "require(True, 'source index",
             'test_source_custody.SourceCustodyTests.test_staged_bytes_are_refused',
             'ValueError not raised'),
            ('head-drift',
             "require(expected_head is None or head == expected_head, 'HEAD changed",
             "require(True, 'HEAD changed",
             'test_source_custody.SourceCustodyTests.test_commit_drift_is_refused',
             'ValueError not raised'),
            ('loaded-wrapper',
             "(root / 'gate.py').read_bytes() == _WRAPPER_SOURCE_BYTES and",
             "True and",
             'test_source_custody.SourceCustodyTests.test_loaded_wrapper_cannot_claim_replaced_committed_source',
             'ValueError not raised'),
            ('loaded-helper',
             "_HELPER_SOURCE_BYTES is not None and\n            (root / 'gate_helper.py').read_bytes() == _HELPER_SOURCE_BYTES",
             "True",
             'test_source_custody.SourceCustodyTests.test_loaded_helper_cannot_claim_replaced_committed_source',
             'ValueError not raised'),
            ('ignored-lean-input',
             "require(relative in tracked, 'unexpected Lean source",
             "require(True, 'unexpected Lean source",
             'test_source_custody.SourceCustodyTests.test_dependency_ignored_extra_lean_is_refused',
             'ValueError not raised'),
            ('stale-receipt',
             "    (out / 'receipt.json').unlink(missing_ok=True)\n    # Keep",
             "    # Keep",
             'test_source_custody.SourceCustodyTests.test_execute_removes_stale_receipt_on_preflight_failure',
             'True is not false'),
            ('helper-receipt-commit',
             "require(receipt.get('checked_commit') == checked_head, 'helper checked commit",
             "require(True, 'helper checked commit",
             'test_source_custody.SourceCustodyTests.test_execute_refuses_helper_receipt_for_another_commit',
             'ValueError not raised'),
            ('helper-bytecode-cache',
             "exec(compile(_HELPER_SOURCE_BYTES, str(_helper_path), 'exec', dont_inherit=True), _core.__dict__)",
             "_helper_spec.loader.exec_module(_core)",
             'test_source_custody.SourceCustodyTests.test_helper_loader_ignores_poisoned_bytecode_cache',
             'POISONED_CACHED_HELPER'),
            ('effective-cwd',
             "cwd=_sync_root() if cwd is None else cwd)",
             "cwd=cwd)",
             'test_gate_compatibility.CompatibilityTests.test_run_uses_current_root_and_preserves_explicit_cwd_and_exit_contract',
             'AssertionError'),
        ]
        results = []
        for label, before, after, test, reason in cases:
            with self.subTest(mutant=label), tempfile.TemporaryDirectory() as td:
                self.assertEqual(source.count(before), 1, 'mutation site must exist exactly once: ' + label)
                root = Path(td) / 'formal'
                (root / 'tests').mkdir(parents=True)
                (root / 'gate.py').write_text(source.replace(before, after, 1))
                shutil.copyfile(HERE / 'gate_helper.py', root / 'gate_helper.py')
                for name in ('test_source_custody.py', 'test_gate_compatibility.py'):
                    shutil.copyfile(HERE / 'tests' / name, root / 'tests' / name)
                args = [sys.executable, '-B', '-S'] + (['-O'] if sys.flags.optimize else [])
                args += ['-m', 'unittest', '-v', test]
                result = subprocess.run(args, cwd=root / 'tests', text=True,
                                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60)
                self.assertNotEqual(result.returncode, 0, 'mutant escaped: ' + label)
                self.assertIn(reason, result.stdout, 'mutant failed for another reason: ' + label + '\n' + result.stdout)
                self.assertIn('Ran 1 test', result.stdout, 'child did not execute its selected control')
                self.assertNotIn('SyntaxError', result.stdout, 'invalid source mutation')
                results.append({'id': label, 'test': test, 'reason': reason, 'exit': result.returncode})
        print('CUSTODY_SOURCE_MUTATIONS ' + json.dumps({
            'threshold': '13/13 (100% finite declared set)',
            'optimized_children': bool(sys.flags.optimize), 'results': results}, sort_keys=True))


if __name__ == '__main__':
    unittest.main()
