"""Real-process controls for the finite C2 source-mutator's kill classification."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
import copy
from unittest import mock

HERE = Path(__file__).resolve().parent
RUNNER = HERE / 'run_mutations.py'
ORIGINAL = HERE.parents[1] / 'reviews/c2_interval_audit_20261001/oracle.py'


class RunnerControls(unittest.TestCase):
    def setUp(self):
        self.assertTrue(RUNNER.is_file(), 'C2 mutation runner is not supplied')
        spec = importlib.util.spec_from_file_location('c2_runner_under_test', RUNNER)
        self.runner = importlib.util.module_from_spec(spec); spec.loader.exec_module(self.runner)
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name); self.source = ORIGINAL.read_text()

    def probe(self, text, case='test_q_fraction_inputs', intended=None):
        path = self.root / 'oracle.py'; path.write_text(text)
        return self.runner.probe(path, self.root / 'probe', [case], intended)

    def test_valid_baseline_process(self):
        result = self.probe(self.source)
        self.assertEqual(result['classification'], 'PASS')
        self.assertEqual(result['observation']['tests_run'], 1)

    def test_intended_assertion_is_a_kill(self):
        text = self.runner.substitute(self.source, "    if type(x) not in (int,F):raise TypeError('exact int/Fraction required')", '    pass')
        result = self.probe(text, 'test_q_exact_rejections', 'test_q_exact_rejections')
        self.assertEqual(result['classification'], 'KILLED')
        self.assertEqual(result['observation']['errors'], [])

    def test_surviving_source_is_not_a_kill(self):
        result = self.probe(self.source + '\n# surviving control\n', intended='test_q_fraction_inputs')
        self.assertEqual(result['classification'], 'SURVIVED')

    def test_startup_crash_is_not_a_kill(self):
        result = self.probe("raise RuntimeError('startup control')\n" + self.source,
                            intended='test_q_fraction_inputs')
        self.assertEqual(result['classification'], 'INVALID')

    def test_input_dependent_crash_is_not_a_kill(self):
        text = self.runner.substitute(self.source, '    return F(x)',
            "    if x == F(1,3):raise RuntimeError('input-dependent control')\n    return F(x)")
        result = self.probe(text, intended='test_q_fraction_inputs')
        self.assertEqual(result['classification'], 'INVALID')
        self.assertTrue(result['observation']['errors'])

    def test_skip_is_not_a_kill(self):
        result = self.probe("import unittest\nraise unittest.SkipTest('skip control')\n" + self.source,
                            intended='test_q_fraction_inputs')
        self.assertEqual(result['classification'], 'INVALID')

    def test_unintended_assertion_is_not_a_kill(self):
        text = self.runner.substitute(self.source, "    if type(x) not in (int,F):raise TypeError('exact int/Fraction required')", '    pass')
        result = self.probe(text, 'test_q_exact_rejections', 'test_root_brackets')
        self.assertEqual(result['classification'], 'INVALID')

    def test_stale_or_ambiguous_substitution_is_refused(self):
        for text, anchor in ((self.source, 'missing anchor'), ('xx', 'x')):
            with self.assertRaisesRegex(ValueError, 'anchor must occur exactly once'):
                self.runner.substitute(text, anchor, 'replacement')

    def test_changed_original_pin_is_refused(self):
        path = self.root / 'wrong-original.py'; path.write_text(self.source + '\n')
        with self.assertRaisesRegex(ValueError, 'oracle source pin mismatch'):
            self.runner.pinned_source(path)

    def test_complete_baseline_cannot_omit_a_new_case(self):
        driver = self.root / 'qualification.py'
        text = self.runner.TEST.read_text().replace(
            "if __name__ == '__main__': raise SystemExit(main())",
            "OracleQualification.test_added_case = lambda self: None\n"
            "if __name__ == '__main__': raise SystemExit(main())")
        driver.write_text(text)
        with mock.patch.object(self.runner, 'TEST', driver):
            result = self.runner.campaign(ORIGINAL, self.root / 'complete-cut')
        self.assertFalse(result['qualified_in_declared_scope'])
        self.assertEqual(result['baseline']['classification'], 'INVALID')

    def test_stale_campaign_refuses_before_execution(self):
        output = self.root / 'stale-cut'
        with self.assertRaisesRegex(ValueError, 'anchor must occur exactly once'):
            self.runner.campaign(ORIGINAL, output,
                [('stale', 'missing anchor', 'replacement', 'test_q_fraction_inputs')])
        self.assertFalse(output.exists())

    def test_source_changed_after_pin_cannot_qualify(self):
        source = self.root / 'changing-original.py'; source.write_text(self.source)
        original_pin = self.runner.pinned_source
        def changed_after_read(path):
            text = original_pin(path)
            source.write_text(text + '\n# changed after pin\n')
            return text
        with mock.patch.object(self.runner, 'pinned_source', changed_after_read):
            result = self.runner.campaign(source, self.root / 'changed-cut')
        self.assertFalse(result['qualified_in_declared_scope'])
        self.assertEqual(result['baseline']['classification'], 'INVALID')

    def fixture_probe(self, phase):
        method='test_q_fraction_inputs';marker=self.root/'body-entered'
        text=self.source+'\nimport sys as _sys\nfrom pathlib import Path as _Path\n_C=_sys.modules["__main__"].OracleQualification\n_original_body=_C.'+method+'\n'
        text+='def _body(self):\n    _Path('+repr(str(marker))+').write_text("entered")\n    _original_body(self)\n'
        if phase=='body':text+='    self.fail("body assertion control")\n'
        text+='_C.'+method+'=_body\n'
        if phase=='setup':text+='def _fixture(self):\n    self.fail("setup assertion control")\n_C.setUp=_fixture\n'
        elif phase=='teardown':text+='def _fixture(self):\n    self.fail("teardown assertion control")\n_C.tearDown=_fixture\n'
        elif phase=='cleanup':text+='def _fixture(self):\n    self.addCleanup(self.fail,"cleanup assertion control")\n_C.setUp=_fixture\n'
        result=self.probe(text,method,method)
        return result,marker.exists()

    def test_setup_assertion_is_not_a_body_kill(self):
        result,entered=self.fixture_probe('setup');self.assertFalse(entered)
        self.assertEqual(result['classification'],'INVALID')

    def test_teardown_assertion_is_not_a_body_kill(self):
        result,entered=self.fixture_probe('teardown');self.assertTrue(entered)
        self.assertEqual(result['classification'],'INVALID')

    def test_cleanup_assertion_is_not_a_body_kill(self):
        result,entered=self.fixture_probe('cleanup');self.assertTrue(entered)
        self.assertEqual(result['classification'],'INVALID')

    def test_genuine_body_kill_has_lifecycle_provenance(self):
        result,entered=self.fixture_probe('body');self.assertTrue(entered)
        self.assertEqual(result['classification'],'KILLED')
        self.assertIn('lifecycle',result['observation'])
        self.assertEqual(result['observation']['lifecycle']['events'],[{
            'id':'__main__.OracleQualification.test_q_fraction_inputs','phase':'body','kind':'failure',
            'exception':'AssertionError','assertion':True}])

    def test_all_baseline_bodies_are_observed(self):
        result=self.probe(self.source)
        self.assertIn('lifecycle',result['observation'])
        self.assertEqual(result['observation']['lifecycle']['tests'][0]['body_entered'],1)
        self.assertEqual(result['observation']['lifecycle']['tests'][0]['body_exited'],1)

    def test_inconsistent_lifecycle_counters_are_invalid(self):
        result,_=self.fixture_probe('body')
        for target,key,value in (('test','body_entered',True),('test','body_exited',0),
                                  ('test','failure_count',0),('event','phase','cleanup'),('event','assertion',False)):
            with self.subTest(key=key):
                report=copy.deepcopy(result['observation'])
                report['lifecycle']['tests' if target=='test' else 'events'][0][key]=value
                self.assertEqual(self.runner.classify(report,1,['test_q_fraction_inputs'],result['source_sha256'],
                    'test_q_fraction_inputs'),'INVALID')

    def test_existing_probe_output_cannot_reuse_stale_observation(self):
        self.probe(self.source);path=self.root/'probe/observation.json';original=path.read_bytes()
        with self.assertRaises(FileExistsError):self.probe('raise RuntimeError("startup control")\n'+self.source)
        self.assertEqual(path.read_bytes(),original)


if __name__ == '__main__': unittest.main()
