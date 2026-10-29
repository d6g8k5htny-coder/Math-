"""Finite, reason-bound source mutations and false-kill controls for core custody."""
import json
from pathlib import Path
import re
import secrets
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parents[1]
MARKER = 'CBZ_CUSTODY_TEST_RESULT '

DRIVER = r'''
import json, sys, unittest
requested, nonce = sys.argv[1:]
class Capture(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ids = []
    def startTest(self, test):
        self.ids.append(test.id())
        super().startTest(test)
suite = unittest.defaultTestLoader.loadTestsFromName(requested)
result = unittest.TextTestRunner(verbosity=2, resultclass=Capture).run(suite)
def rows(items):
    return [{'id': test.id(), 'detail': str(detail)} for test, detail in items]
data = dict(nonce=nonce, requested=requested, ids=result.ids, tests=result.testsRun,
            failures=rows(result.failures), errors=rows(result.errors),
            skipped=rows(result.skipped), expected_failures=rows(result.expectedFailures),
            unexpected_successes=[test.id() for test in result.unexpectedSuccesses],
            success=result.wasSuccessful())
print('CBZ_CUSTODY_TEST_RESULT ' + json.dumps(data, sort_keys=True), flush=True)
raise SystemExit(0 if result.wasSuccessful() else 1)
'''


def _record(result, test, nonce):
    if type(result.returncode) is not int or not isinstance(result.stdout, str):
        return None
    lines = [line[len(MARKER):] for line in result.stdout.splitlines()
             if line.startswith(MARKER)]
    if len(lines) != 1:
        return None
    try:
        data = json.loads(lines[0])
    except (ValueError, TypeError):
        return None
    keys = {'nonce', 'requested', 'ids', 'tests', 'failures', 'errors', 'skipped',
            'expected_failures', 'unexpected_successes', 'success'}
    if not isinstance(data, dict) or set(data) != keys:
        return None
    if (data['nonce'] != nonce or data['requested'] != test or data['ids'] != [test] or
            type(data['tests']) is not int or data['tests'] != 1):
        return None
    if any(data[key] != [] for key in ('errors', 'skipped', 'expected_failures',
                                       'unexpected_successes')):
        return None
    return data


def _accepted_baseline(result, test, nonce):
    data = _record(result, test, nonce)
    return (data is not None and result.returncode == 0 and
            data['success'] is True and data['failures'] == [])


def _accepted_failure(result, test, nonce, reason):
    data = _record(result, test, nonce)
    if data is None or not isinstance(data['failures'], list) or len(data['failures']) != 1:
        return False
    item = data['failures'][0]
    if not isinstance(item, dict) or set(item) != {'id', 'detail'}:
        return False
    detail = item['detail']
    method = test.rsplit('.', 1)[-1]
    return all((
        result.returncode == 1,
        data['success'] is False,
        item['id'] == test,
        isinstance(detail, str),
        isinstance(detail, str) and reason in detail,
        isinstance(detail, str) and ('in ' + method) in detail,
        isinstance(detail, str) and (reason != 'ValueError not raised' or 'with self.assertRaisesRegex' in detail),
    ))


def _run_one(root, test):
    nonce = secrets.token_hex(16)
    args = [sys.executable, '-B', '-S'] + (['-O'] if sys.flags.optimize else [])
    args += ['-c', DRIVER, test, nonce]
    result = subprocess.run(args, cwd=root / 'tests', text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60)
    return result, nonce


class CustodyMutationTests(unittest.TestCase):
    def test_grader_refuses_false_kills(self):
        test = 'case.Module.test_guard'
        nonce = 'unique-control-nonce'
        good = dict(nonce=nonce, requested=test, ids=[test], tests=1,
                    failures=[{'id': test, 'detail': 'in test_guard\nAssertionError: intended bypass'}],
                    errors=[], skipped=[], expected_failures=[], unexpected_successes=[], success=False)
        def sample(code, data, suffix=''):
            return subprocess.CompletedProcess([], code, MARKER + json.dumps(data) + '\n' + suffix)
        self.assertTrue(_accepted_failure(sample(1, good), test, nonce, 'intended bypass'))
        self.assertFalse(_accepted_failure(sample(2, good), test, nonce, 'intended bypass'))
        self.assertFalse(_accepted_failure(sample(86, good), test, nonce, 'intended bypass'))
        self.assertFalse(_accepted_failure(sample(1, dict(good, tests=0)), test, nonce, 'intended bypass'))
        self.assertFalse(_accepted_failure(sample(1, dict(good, errors=[{'id':test,'detail':'crash'}])),
                                           test, nonce, 'intended bypass'))
        self.assertFalse(_accepted_failure(sample(1, dict(good, skipped=[{'id':test,'detail':'skip'}])),
                                           test, nonce, 'intended bypass'))
        self.assertFalse(_accepted_failure(sample(1, dict(good, failures=[{'id':test,'detail':'in test_guard wrong'}])),
                                           test, nonce, 'intended bypass'))
        self.assertFalse(_accepted_failure(sample(1, dict(good, failures=[{'id':test,'detail':'in tearDown intended bypass'}])),
                                           test, nonce, 'intended bypass'))
        self.assertFalse(_accepted_failure(sample(1, good, MARKER + json.dumps(good)), test, nonce, 'intended bypass'))
        self.assertFalse(_accepted_failure(sample(1, dict(good, nonce='wrong')), test, nonce, 'intended bypass'))
        self.assertFalse(_accepted_failure(sample(1, dict(good, ids=['wrong.Module.test_guard'])), test, nonce, 'intended bypass'))
        self.assertFalse(_accepted_failure(sample(1, dict(good, requested='wrong.Module.test_guard')), test, nonce, 'intended bypass'))
        self.assertFalse(_accepted_failure(sample(1, dict(good, failures=[{'id':'wrong.Module.test_guard','detail':'in test_guard intended bypass'}])), test, nonce, 'intended bypass'))
        self.assertFalse(_accepted_failure(sample(1, dict(good, success=True)), test, nonce, 'intended bypass'))
        self.assertFalse(_accepted_failure(sample(1, dict(good, expected_failures=[{'id':test,'detail':'expected'}])), test, nonce, 'intended bypass'))
        self.assertFalse(_accepted_failure(sample(1, dict(good, unexpected_successes=[test])), test, nonce, 'intended bypass'))
        self.assertFalse(_accepted_baseline(sample(0, good), test, nonce))
        refusal = dict(good, failures=[{'id': test, 'detail': 'in test_guard\nValueError not raised'}])
        refusal_at_site = dict(good, failures=[{'id': test, 'detail':
            'in test_guard\nwith self.assertRaisesRegex(ValueError, expected):\nValueError not raised'}])
        self.assertFalse(_accepted_failure(sample(1, refusal), test, nonce, 'ValueError not raised'))
        self.assertTrue(_accepted_failure(sample(1, refusal_at_site), test, nonce, 'ValueError not raised'))
        self.assertFalse(_accepted_failure(subprocess.CompletedProcess([],1,'missing record'), test, nonce, 'intended bypass'))

    def test_grader_rejects_exit_two_even_with_plausible_failure_text(self):
        test = 'case.Module.test_guard'
        nonce = 'exit-two-control'
        data = dict(nonce=nonce, requested=test, ids=[test], tests=1,
                    failures=[{'id':test, 'detail':'in test_guard\nAssertionError: intended bypass'}],
                    errors=[], skipped=[], expected_failures=[], unexpected_successes=[], success=False)
        fake = subprocess.CompletedProcess([], 2, MARKER + json.dumps(data))
        self.assertFalse(_accepted_failure(fake, test, nonce, 'intended bypass'))

    def test_grader_detects_its_guard_source_mutants(self):
        source = Path(__file__).read_text()
        prefix, separator, suffix = source.partition('class CustodyMutationTests')
        self.assertTrue(separator)
        mutations = [
            ('always-accept', '    return all((\n', '    return True or all((\n'),
            ('exact-exit', 'result.returncode == 1,', 'True,'),
            ('nonce', "data['nonce'] != nonce", "False"),
            ('requested-test', "data['requested'] != test", "False"),
            ('executed-test', "data['ids'] != [test]", "False"),
            ('one-test', "type(data['tests']) is not int or data['tests'] != 1", "False"),
            ('error-or-skip', "data[key] != []", "False"),
            ('one-record', 'len(lines) != 1', 'False'),
            ('failing-test', "item['id'] == test,", "True,"),
            ('reason', 'reason in detail,', 'True,'),
            ('test-frame', "('in ' + method) in detail,", 'True,'),
            ('refusal-site',
             "reason != 'ValueError not raised' or 'with self.assertRaisesRegex' in detail",
             "True"),
            ('failure-status', "data['success'] is False,", "True,"),
            ('baseline-status', "return (data is not None and result.returncode == 0 and",
             "return (True or data is not None and result.returncode == 0 and"),
        ]
        for label, before, after in mutations:
            with self.subTest(mutant=label), tempfile.TemporaryDirectory() as td:
                self.assertEqual(prefix.count(before), 1, 'grader mutation site: ' + label)
                path = Path(td) / 'test_mutant.py'
                path.write_text(prefix.replace(before, after, 1) + separator + suffix)
                args = [sys.executable, '-B', '-S'] + (['-O'] if sys.flags.optimize else [])
                args += ['-m', 'unittest', '-v', 'test_mutant.CustodyMutationTests.test_grader_refuses_false_kills']
                result = subprocess.run(args, cwd=td, text=True, stdout=subprocess.PIPE,
                                        stderr=subprocess.STDOUT, timeout=60)
                self.assertEqual(result.returncode, 1, 'grader mutant exit must equal 1: ' + label)
                self.assertIn('test_grader_refuses_false_kills', result.stdout)
                self.assertIn('True is not false', result.stdout)
                self.assertIn('FAILED (failures=1)', result.stdout)

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
             'EFFECTIVE_CWD_MISMATCH'),
            ('git-directory-environment',
             "not key.startswith('GIT_') and key not in _UNTRUSTED_LEAN_ENV",
             "key not in _UNTRUSTED_LEAN_ENV",
             'test_source_custody.SourceCustodyTests.test_foreign_git_environment_cannot_redirect_source_identity',
             ' != '),
            ('git-alternate-index',
             "not key.startswith('GIT_') and key not in _UNTRUSTED_LEAN_ENV",
             "key not in _UNTRUSTED_LEAN_ENV",
             'test_source_custody.SourceCustodyTests.test_foreign_index_cannot_hide_staged_source',
             'ValueError not raised'),
            ('git-replacement-refs',
             "'GIT_NO_REPLACE_OBJECTS': '1'",
             "'GIT_NO_REPLACE_OBJECTS': '0'",
             'test_source_custody.SourceCustodyTests.test_replace_ref_cannot_redirect_committed_source',
             'REPLACEMENT_REF_REDIRECTED'),
            ('dependency-git-environment',
             "actual[name] = _git_bytes(repo, 'rev-parse', 'HEAD').decode('utf-8').strip()",
             "actual[name] = subprocess.check_output(['git', '-C', repo, 'rev-parse', 'HEAD'], text=True).strip()",
             'test_source_custody.SourceCustodyTests.test_dependency_ignores_foreign_git_environment',
             'DEPENDENCY_GIT_REDIRECTED'),
            ('helper-git-environment',
             "with _helper_execution_environment():",
             "if True:",
             'test_source_custody.SourceCustodyTests.test_execute_ignores_foreign_git_environment_in_helper',
             'HELPER_GIT_REDIRECTED'),
            ('lean-search-environment',
             "with _helper_execution_environment():",
             "if True:",
             'test_source_custody.SourceCustodyTests.test_execute_strips_external_lean_search_paths',
             '/untrusted/lean'),
            ('dependency-package-root-symlink',
             "not part.is_symlink() and part.is_dir()",
             "part.is_dir()",
             'test_source_custody.SourceCustodyTests.test_dependency_refuses_symlinked_package_root',
             'ValueError not raised'),
            ('dependency-packages-ancestor-symlink',
             "not part.is_symlink() and part.is_dir()",
             "part.is_dir()",
             'test_source_custody.SourceCustodyTests.test_dependency_refuses_symlinked_packages_ancestor',
             'ValueError not raised'),
            ('dependency-name-canonical',
             "name == Path(name).name and not Path(name).is_absolute()",
             "not Path(name).is_absolute()",
             'test_source_custody.SourceCustodyTests.test_dependency_rejects_noncanonical_name',
             'ValueError not raised'),
            ('dependency-lake-ancestor-symlink',
             "not part.is_symlink() and part.is_dir()",
             "part.is_dir()",
             'test_source_custody.SourceCustodyTests.test_dependency_refuses_symlinked_lake_ancestor',
             'ValueError not raised'),
        ]
        self.assertEqual(len(cases), 23, 'declared finite mutation set changed')
        results = []
        for label, before, after, test, reason in cases:
            with self.subTest(mutant=label), tempfile.TemporaryDirectory() as td:
                self.assertEqual(source.count(before), 1, 'mutation site must exist exactly once: ' + label)
                root = Path(td) / 'formal'
                (root / 'tests').mkdir(parents=True)
                gate = root / 'gate.py'
                gate.write_text(source)
                shutil.copyfile(HERE / 'gate_helper.py', root / 'gate_helper.py')
                for name in ('test_source_custody.py', 'test_gate_compatibility.py'):
                    shutil.copyfile(HERE / 'tests' / name, root / 'tests' / name)
                baseline, nonce = _run_one(root, test)
                self.assertTrue(_accepted_baseline(baseline, test, nonce),
                                'selected baseline did not pass exactly once: ' + label + '\n' + baseline.stdout)
                gate.write_text(source.replace(before, after, 1))
                result, nonce = _run_one(root, test)
                self.assertEqual(result.returncode, 1, 'exact mutation-test exit: ' + label)
                self.assertTrue(_accepted_failure(result, test, nonce, reason),
                                'intended assertion observation missing: ' + label + '\n' + result.stdout)
                results.append({'id': label, 'test': test, 'reason': reason, 'exit': result.returncode})
        print('CUSTODY_SOURCE_MUTATIONS ' + json.dumps({
            'threshold': '23/23 (100% finite declared set)',
            'optimized_children': bool(sys.flags.optimize), 'results': results}, sort_keys=True))


if __name__ == '__main__':
    unittest.main()
