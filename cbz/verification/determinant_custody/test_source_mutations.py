"""Reason-bound source mutations for determinant custody; no Lean credit."""
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
GATE = REPO / 'frontiers/determinant_moment_20261025/gate.py'

CASES = (
    ('dependency-bytes', "require(actual == oid, 'working bytes differ",
     "require(True, 'working bytes differ",
     'test_assume_unchanged_dependency_source_is_rejected', 'ValueError not raised'),
    ('staged-index', "require(index == tree, 'source index",
     "require(True, 'source index",
     'test_staged_only_change_is_rejected_when_working_bytes_are_original', 'ValueError not raised'),
    ('head-drift', "require(expected_head is None or head == expected_head, 'HEAD changed",
     "require(True, 'HEAD changed",
     'test_head_drift_is_rejected', 'ValueError not raised'),
    ('lean-path', "        environment.pop(key, None)",
     "        pass  # MUTANT: retain inherited Lean paths",
     'test_inherited_lean_search_paths_are_not_sent_to_execution', '/outside/lean'),
    ('git-child-environment',
     "    environment = {key: value for key, value in os.environ.items()\n                   if not key.startswith('GIT_')}",
     "    environment = os.environ.copy()  # MUTANT: retain Git redirects",
     'test_inherited_git_redirects_are_not_sent_to_execution', '/outside/git'),
    ('nested-build-symlink',
     "            require(not (Path(directory) / entry).is_symlink(), 'symlink in build directory')",
     "            pass  # MUTANT: follow build symlinks",
     'test_nested_build_symlinks_are_rejected_before_admission', 'unsafe build directory reached'),
    ('evidence-leaf',
     "    require(not target.is_symlink() and (not target.exists() or target.is_file()),",
     "    require(True,",
     'test_log_symlink_is_refused_without_overwriting_its_target', 'ValueError not raised'),
    ('admission-helper',
     "    verify_committed_files(repo, head, owned)",
     "    pass  # MUTANT: do not bind owned sources",
     'test_refreshed_external_admission_helper_is_rejected', 'ValueError not raised'),
    ('loaded-driver',
     "(root / 'gate.py').read_bytes() == _LOADED_SOURCE_BYTES and",
     "True and",
     'test_loaded_driver_substitution_is_rejected', 'ValueError not raised'),
    ('evidence-directory',
     "        require(all(not path.is_symlink() for path in out.iterdir()),",
     "        require(True,",
     'test_unreferenced_evidence_symlink_is_refused_before_use', 'ValueError not raised'),
)

def accepted_baseline(result, target):
    stderr = result.stderr
    passed = re.findall(r'^(test_[A-Za-z0-9_]+) \([^\n]*\) \.\.\. ok$', stderr, re.M)
    return (type(result.returncode) is int and result.returncode == 0 and passed == [target]
            and re.search(r'^Ran 1 test in ', stderr, re.M) is not None
            and re.search(r'^OK$', stderr, re.M) is not None
            and 'skipped=' not in stderr and 'ERROR:' not in stderr)

def accepted_failure(result, target, reason):
    stderr = result.stderr
    headers = list(re.finditer(r'^FAIL: (test_[A-Za-z0-9_]+) [^\n]*$', stderr, re.M))
    summary = re.search(r'^Ran 1 test in ', stderr, re.M)
    if len(headers) != 1 or summary is None or headers[0].group(1) != target:
        return False
    section = stderr[headers[0].end():summary.start()]
    return (type(result.returncode) is int and result.returncode == 1
            and 'ERROR:' not in stderr and 'skipped=' not in stderr
            and ('in ' + target) in section and reason in section
            and re.search(r'^FAILED \(failures=1\)$', stderr, re.M) is not None)

def trial(root, target):
    cmd = [sys.executable, '-B', '-S'] + (['-O'] if sys.flags.optimize else [])
    cmd += ['-m', 'unittest', 'discover', '-s', 'cbz/verification/determinant_custody',
            '-p', 'test_custody.py', '-k', target, '-v']
    environment = {key: value for key, value in os.environ.items()
                   if not key.startswith('GIT_') and not key.startswith('PYTHON')
                   and key not in ('LEAN_PATH', 'LEAN_SRC_PATH')}
    return subprocess.run(cmd, cwd=root, capture_output=True, text=True, timeout=60, env=environment)

class SourceMutationTests(unittest.TestCase):
    def test_grader_rejects_wrong_exit_missing_test_and_wrong_reason(self):
        target = 'test_control'
        text = ('FAIL: test_control (fixture)\nin test_control\n'
                'AssertionError: intended bypass\nRan 1 test in 0.001s\n\nFAILED (failures=1)\n')
        def sample(code, stderr):
            return subprocess.CompletedProcess([], code, stdout='', stderr=stderr)
        self.assertTrue(accepted_failure(sample(1, text), target, 'intended bypass'))
        self.assertFalse(accepted_failure(sample(2, text), target, 'intended bypass'))
        self.assertFalse(accepted_failure(sample(True, text), target, 'intended bypass'))
        self.assertFalse(accepted_failure(sample(1, text.replace('intended bypass', 'unrelated') + 'intended bypass\n'),
                                          target, 'intended bypass'))
        self.assertFalse(accepted_failure(sample(1, text.replace('intended bypass', 'unrelated')),
                                          target, 'intended bypass'))
        self.assertFalse(accepted_failure(sample(1, text.replace('Ran 1 test', 'Ran 0 tests')),
                                          target, 'intended bypass'))
        self.assertFalse(accepted_failure(sample(1, text + 'ERROR: foreign\n'),
                                          target, 'intended bypass'))

    def test_baseline_rejects_missing_wrong_skipped_and_error_cases(self):
        target = 'test_control'
        good = 'test_control (fixture) ... ok\nRan 1 test in 0.001s\n\nOK\n'
        def sample(code, stderr):
            return subprocess.CompletedProcess([], code, stdout='', stderr=stderr)
        self.assertTrue(accepted_baseline(sample(0, good), target))
        self.assertFalse(accepted_baseline(sample(0, good.replace('test_control', 'test_other')), target))
        self.assertFalse(accepted_baseline(sample(0, good.replace('Ran 1 test', 'Ran 0 tests')), target))
        self.assertFalse(accepted_baseline(sample(0, good + 'skipped=1\n'), target))
        self.assertFalse(accepted_baseline(sample(0, good + 'ERROR: unrelated\n'), target))
        self.assertFalse(accepted_baseline(sample(2, good), target))
        self.assertFalse(accepted_baseline(sample(False, good), target))

    def test_grader_source_mutation_is_detected(self):
        source = Path(__file__).read_text()
        old = 'type(result.returncode) is int and result.returncode == 1\n'
        self.assertEqual(source.count(old), 1)
        altered = source.replace(old, 'True\n', 1)
        namespace = {'__name__': 'det_custody_mutated_grader', '__file__': __file__}
        exec(compile(altered, __file__, 'exec'), namespace)
        fake = subprocess.CompletedProcess([], 2, stdout='', stderr=(
            'FAIL: test_control (fixture)\nin test_control\n'
            'AssertionError: intended bypass\nRan 1 test in 0.001s\n\nFAILED (failures=1)\n'))
        with self.assertRaisesRegex(AssertionError, 'True is not false'):
            self.assertFalse(namespace['accepted_failure'](fake, 'test_control', 'intended bypass'))

    def test_all_named_gate_source_mutants_fail_for_the_expected_reason(self):
        source = GATE.read_text()
        self.assertEqual(len(CASES), 10)
        for name, old, new, target, reason in CASES:
            with self.subTest(mutant=name):
                self.assertEqual(source.count(old), 1, 'mutation anchor must be unique: ' + name)
                with tempfile.TemporaryDirectory(prefix='det-custody-source-mutant-') as temporary:
                    root = Path(temporary)
                    driver = root / 'frontiers/determinant_moment_20261025/gate.py'
                    driver.parent.mkdir(parents=True)
                    tests = root / 'cbz/verification/determinant_custody'
                    tests.mkdir(parents=True)
                    shutil.copyfile(HERE / 'test_custody.py', tests / 'test_custody.py')
                    driver.write_text(source)
                    baseline = trial(root, target)
                    self.assertTrue(accepted_baseline(baseline, target), baseline.stderr)
                    driver.write_text(source.replace(old, new, 1))
                    mutant = trial(root, target)
                    self.assertTrue(accepted_failure(mutant, target, reason), mutant.stderr)
                    print('DETERMINANT_CUSTODY_MUTANT ' + name + ' ' + target + ' ' + reason, flush=True)

if __name__ == '__main__':
    unittest.main()
