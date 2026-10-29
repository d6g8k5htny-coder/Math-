"""Bounded mutation-runner regressions; real Python subprocesses, no Lean calls."""
import copy
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('adapter_mutation_runner', ROOT/'tests/run_adapter_mutations.py')
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)
SELECTION = 'test_fixture.Fixture.test_selected'


class MutationRunnerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=ROOT)
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)

    def test_real_assertion_failures_count_but_runtime_errors_do_not(self):
        harness = self.base/'harness.py'
        harness.write_text(runner.HARNESS_SOURCE)
        for mode in ('normal', 'optimized'):
            results = {}
            for name, body in (('baseline', 'self.assertTrue(True)'),
                               ('assertion', "self.fail('intended adverse assertion')"),
                               ('error', "raise RuntimeError('synthetic harness error')")):
                source = self.base/(mode+'-'+name)
                (source/'tests').mkdir(parents=True)
                (source/'tests/test_fixture.py').write_text(
                    'import unittest\nclass Fixture(unittest.TestCase):\n'
                    '    def test_selected(self):\n        '+body+'\n')
                results[name] = runner.run_selected(source, SELECTION, mode,
                    self.base/(mode+'-'+name+'-evidence'), harness, self.base/'unused-core')
            self.assertEqual(results['baseline']['classification'], 'PASS')
            self.assertEqual(results['assertion']['classification'], 'ASSERTION_FAILURE')
            self.assertEqual(results['error']['classification'], 'INVALID')
            self.assertTrue(runner.classify_pair(results['baseline'], results['assertion'])['killed'])
            self.assertFalse(runner.classify_pair(results['baseline'], results['error'])['killed'])
            self.assertFalse(runner.classify_pair(results['error'], results['assertion'])['killed'])

    def test_same_selection_mode_and_harness_are_required(self):
        baseline = dict(classification='PASS', selection=SELECTION, mode='normal', harness_sha256='a'*64)
        mutant = dict(baseline, classification='ASSERTION_FAILURE')
        self.assertTrue(runner.classify_pair(baseline, mutant)['killed'])
        for field, value in (('selection', SELECTION+'other'), ('mode', 'optimized'), ('harness_sha256', 'b'*64)):
            changed = dict(mutant, **{field:value})
            with self.subTest(field=field):
                self.assertFalse(runner.classify_pair(baseline, changed)['killed'])

    def test_zero_wrong_skipped_and_error_results_are_invalid(self):
        clean = dict(returncode=0, selection=SELECTION, loaded_test_ids=[SELECTION], tests_run=1,
            failure_ids=[], error_ids=[], skipped_ids=[], expected_failure_ids=[], unexpected_success_ids=[],
            failure_details=[], successful=True)
        self.assertEqual(runner.classify_execution(clean), 'PASS')
        mutations = [dict(tests_run=0), dict(loaded_test_ids=['other']),
                     dict(skipped_ids=[SELECTION]), dict(expected_failure_ids=[SELECTION]),
                     dict(unexpected_success_ids=[SELECTION]),
                     dict(returncode=1, successful=False, error_ids=[SELECTION]),
                     dict(returncode=1, successful=False, failure_ids=['other']),
                     dict(returncode=2, successful=False, failure_ids=[SELECTION]),
                     dict(returncode=False), dict(returncode=True, successful=False,
                        failure_ids=[SELECTION], failure_details=[dict(test_id=SELECTION,
                            parent_test_id=SELECTION, phase='test', is_assertion=True, exception_type='AssertionError')])]
        for changes in mutations:
            with self.subTest(changes=changes):
                self.assertEqual(runner.classify_execution(dict(copy.deepcopy(clean), **changes)), 'INVALID')
        adverse = dict(clean, returncode=1, successful=False, failure_ids=[SELECTION+' (case=1)'],
            failure_details=[dict(test_id=SELECTION+' (case=1)', parent_test_id=SELECTION,
                                 phase='test', is_assertion=True, exception_type='AssertionError')])
        self.assertEqual(runner.classify_execution(adverse), 'ASSERTION_FAILURE')

    def test_only_test_body_assertions_qualify_including_subtests(self):
        harness=self.base/'phase-harness.py';harness.write_text(runner.HARNESS_SOURCE)
        variants={
            'setup': "    def setUp(self):\n        self.fail('setup assertion')\n    def test_selected(self):\n        self.assertTrue(True)\n",
            'teardown': "    def tearDown(self):\n        self.fail('teardown assertion')\n    def test_selected(self):\n        self.assertTrue(True)\n",
            'cleanup': "    def setUp(self):\n        self.addCleanup(lambda: self.fail('cleanup assertion'))\n    def test_selected(self):\n        self.assertTrue(True)\n",
            'setup_subtest': "    def setUp(self):\n        with self.subTest(stage='setup'):\n            self.fail('setup subtest assertion')\n    def test_selected(self):\n        self.assertTrue(True)\n",
            'test_subtest': "    def test_selected(self):\n        with self.subTest(stage='test'):\n            self.fail('test body subtest assertion')\n",
        }
        for mode in ('normal','optimized'):
            for name,body in variants.items():
                with self.subTest(mode=mode,phase=name):
                    source=self.base/(mode+'-'+name);(source/'tests').mkdir(parents=True)
                    (source/'tests/test_fixture.py').write_text('import unittest\nclass Fixture(unittest.TestCase):\n'+body)
                    result=runner.run_selected(source,SELECTION,mode,
                        self.base/(mode+'-'+name+'-evidence'),harness,self.base/'unused-core')
                    self.assertEqual(result['classification'], 'ASSERTION_FAILURE' if name=='test_subtest' else 'INVALID')

    def test_evidence_runs_are_unique_and_existing_logs_are_retained(self):
        first = runner.create_run_directory(self.base/'evidence')
        sentinel = first/'old.log'
        sentinel.write_text('retained')
        second = runner.create_run_directory(self.base/'evidence')
        self.assertNotEqual(first, second)
        self.assertEqual(sentinel.read_text(), 'retained')


if __name__ == '__main__':
    unittest.main()
