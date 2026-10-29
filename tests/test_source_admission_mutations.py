"""Portable source experiment acceptance controls; no Lean execution."""
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('source_mutations', Path(__file__).with_name('run_source_admission_mutations.py'))
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class RunnerControls(unittest.TestCase):
    def run_fixture(self, directory, fixture, label):
        root = Path(directory)
        (root / 'test_fixture.py').write_text('import unittest\n' + fixture)
        return runner.run_process(root, ['-m', 'unittest', 'discover', '-s', '.',
                                        '-p', 'test_fixture.py', '-v'], root, label, False)[0]

    def test_actual_lifecycle_failures_cannot_count_as_body_kills(self):
        fixtures = [
            ('setup', 'class Case(unittest.TestCase):\n    def setUp(self): self.fail("fixture initialization failed")\n    def test_check(self): print("BODY_ENTERED")\n', False),
            ('teardown', 'class Case(unittest.TestCase):\n    def tearDown(self): self.fail("fixture teardown failed")\n    def test_check(self): print("BODY_ENTERED")\n', True),
            ('cleanup', 'class Case(unittest.TestCase):\n    def test_check(self):\n        print("BODY_ENTERED")\n        self.addCleanup(self.fail, "fixture cleanup failed")\n', True),
            ('custom_teardown', 'class Case(unittest.TestCase):\n    def _callTearDown(self): self.fail("unsupported custom fixture")\n    def test_check(self): print("BODY_ENTERED")\n', True),
            ('class_setup', 'class Case(unittest.TestCase):\n    @classmethod\n    def setUpClass(cls): raise AssertionError("class fixture failed")\n    def test_check(self): print("BODY_ENTERED")\n', False),
            ('body_error', 'class Case(unittest.TestCase):\n    def test_check(self):\n        print("BODY_ENTERED")\n        raise RuntimeError("unexpected body error")\n', True),
            ('empty', '', False),
        ]
        for label, fixture, entered in fixtures:
            with self.subTest(fixture=label), tempfile.TemporaryDirectory() as directory:
                result = self.run_fixture(directory, fixture, label)
                self.assertEqual('BODY_ENTERED' in result.stdout, entered)
                classification = runner.classify(result, expected_count=1)
                self.assertFalse(classification['control_pass'], result.stderr)
                self.assertFalse(classification['killed'], result.stderr)

    def test_actual_body_assertion_is_a_kill_and_clean_body_is_a_control(self):
        for failure in (False, True):
            with self.subTest(failure=failure), tempfile.TemporaryDirectory() as directory:
                fixture = 'class Case(unittest.TestCase):\n    def test_check(self):\n        print("BODY_ENTERED")\n'
                fixture += '        self.fail("intended checker assertion")\n' if failure else '        self.assertTrue(True)\n'
                result = self.run_fixture(directory, fixture, 'body')
                self.assertIn('BODY_ENTERED', result.stdout)
                classification = runner.classify(result, expected_count=1)
                self.assertEqual(classification['killed'], failure, result.stderr)
                self.assertEqual(classification['control_pass'], not failure, result.stderr)

    def result(self, status=0, output='Ran 2 tests in 0.1s\n\nOK\n'):
        evidence = {'tests': [{'id': 'suite.test_check', 'body_entered': True},
                              {'id': 'suite.test_second', 'body_entered': True}],
                    'events': ([{'id': 'suite.test_check', 'phase': 'body', 'kind': 'failure'}]
                               if 'FAIL:' in output else [])}
        return subprocess.CompletedProcess([], status, '', output + 'SOURCE_MUTATION_PHASES|' + json.dumps(evidence) + '\n')

    def test_requires_positive_clean_baseline(self):
        self.assertTrue(runner.classify(self.result())['control_pass'])
        for output in ('Ran 0 tests in 0s\nOK\n', '', 'Ran 2 tests in 0s\nOK (skipped=1)\n',
                       'Ran 2 tests in 0s\nERROR: setup\nOK\n', 'Ran 2 tests in 0s\nOK\nRan 2 tests in 0s\nOK\n'):
            self.assertFalse(runner.classify(self.result(output=output))['control_pass'])
        self.assertFalse(runner.classify(self.result(status=1))['control_pass'])

    def test_kill_requires_actual_assertion_failure_and_matching_discovery(self):
        output = 'FAIL: test_check (suite.Test)\nAssertionError: missing refusal\nRan 2 tests in 0s\nFAILED (failures=1)\n'
        killed = runner.classify(self.result(1, output), expected_count=2)
        self.assertTrue(killed['killed'])
        for bad in (output.replace('FAIL:', 'ERROR:'), output.replace('AssertionError:', 'ImportError:'),
                    output.replace('Ran 2', 'Ran 0'), output.replace('Ran 2', 'Ran 3'),
                    output.replace('FAILED (failures=1)', 'FAILED (failures=1, errors=1)'), ''):
            self.assertFalse(runner.classify(self.result(1, bad), expected_count=2)['killed'])
        self.assertFalse(runner.classify(self.result(0, output), expected_count=2)['killed'])

    def test_missing_or_wrong_lifecycle_evidence_is_refused(self):
        output = 'FAIL: test_check (suite.Test)\nAssertionError: missing refusal\nRan 2 tests in 0s\nFAILED (failures=1)\n'
        good = self.result(1, output)
        for text in [output, good.stderr.replace('"body_entered": true', '"body_entered": false'),
                     good.stderr.replace('"phase": "body"', '"phase": "setup"'),
                     good.stderr.replace('"phase": "body"', '"phase": "teardown"'),
                     good.stderr.replace('"phase": "body"', '"phase": "cleanup"'),
                     good.stderr + 'SOURCE_MUTATION_PHASES|{}\n']:
            self.assertFalse(runner.classify(subprocess.CompletedProcess([], 1, '', text), 2)['killed'])

    def test_actual_timeout_never_produces_a_qualified_result(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'test_fixture.py').write_text('import time, unittest\nclass Case(unittest.TestCase):\n    def test_check(self): time.sleep(1)\n')
            with self.assertRaises(subprocess.TimeoutExpired):
                runner.run_process(root, ['-m', 'unittest', 'discover', '-s', '.', '-p', 'test_fixture.py'],
                                   root, 'timeout', False, timeout=0.02)

    def test_missing_or_ambiguous_anchor_refuses(self):
        self.assertEqual(runner.replace_anchor('before ANCHOR after', 'ANCHOR', 'NEW'), 'before NEW after')
        for source in ('missing', 'ANCHOR ANCHOR'):
            with self.assertRaisesRegex(ValueError, 'exactly once'):
                runner.replace_anchor(source, 'ANCHOR', 'NEW')

    def test_all_named_cases_and_modes_required_without_duplicates(self):
        names = [case[0] for case in runner.MUTATIONS] + ['control-helper', 'control-determinant', 'control-cap']
        self.assertEqual(len(runner.MUTATIONS), 15)
        self.assertEqual(len(set(names)), 18)
        records = [dict(name=name, optimized=mode, passed=True) for name in names for mode in (False, True)]
        self.assertTrue(runner.complete(records))
        for bad in (records[:-1], records + records[:1], [{**records[0], 'passed': False}] + records[1:],
                    [{**records[0], 'name': 'unknown'}] + records[1:]):
            self.assertFalse(runner.complete(bad))

    def test_existing_output_directory_refused(self):
        with self.assertRaises(FileExistsError):
            runner.prepare_output(Path(__file__).parent)

    def test_command_returns_nonzero_for_failed_matrix_or_setup(self):
        for setup_failure in (False, True):
            with self.subTest(setup_failure=setup_failure), tempfile.TemporaryDirectory() as directory:
                def failed_case(case, optimized, output, control=False):
                    if setup_failure:
                        raise ValueError('mutation anchor must occur exactly once')
                    return dict(name=case[0], optimized=optimized, passed=False)
                with patch.object(runner.sys, 'argv', ['runner', '--output', directory + '/fresh']), \
                     patch.object(runner, 'run_case', side_effect=failed_case), \
                     patch('builtins.print'):
                    self.assertNotEqual(runner.main(), 0)


if __name__ == '__main__':
    unittest.main()
