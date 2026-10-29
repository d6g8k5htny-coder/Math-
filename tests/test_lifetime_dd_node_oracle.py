"""Finite process-contract regressions, not mathematical certification."""
import contextlib
import hashlib
import importlib.util
import io
import inspect
import json
from pathlib import Path
import sys
import types
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
WRAPPER = ROOT / 'frontiers/lifetime_dd_model_d_20261013/replay.py'
EXPECTED = (ROOT / 'tests/fixtures/lifetime_dd_changed_node_stdout.txt').read_bytes()
MISSING_TEMPLATE = (ROOT / 'tests/fixtures/lifetime_dd_missing_node_stderr.txt').read_bytes()
MISSING = MISSING_TEMPLATE.replace(b'<CERTIFICATE_V2>', str(WRAPPER.parent / 'certificate_v2').encode())


def load():
    spec = importlib.util.spec_from_file_location('dd_oracle_subject', WRAPPER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Finite unittest assertion helpers used by the frozen controls below. Code
# identity, not filenames, function names or formatted traceback text, admits
# an origin. This is a trusted-process test aid, not hostile-code attestation.
_ASSERTION_CODES = frozenset(getattr(unittest.TestCase, name).__code__ for name in
    ('assertTrue', 'assertFalse', 'assertEqual', 'assertListEqual', 'assertSequenceEqual',
     '_baseAssertEqual', 'fail'))


class OracleOriginResult(unittest.TestResult):
    def __init__(self, cases):
        super().__init__()
        self.expected = tuple(case.id() for case in cases)
        self.started = []
        self.stopped = []
        self.entered = []
        self.active = None
        self.escaping = {}
        self.origins = []
        self.success_ids = []
        self.failure_ids = []
        self.body_codes = {case.id(): getattr(case, case._testMethodName).__func__.__code__
                           for case in cases}

    def startTest(self, test):
        self.started.append(test.id())
        super().startTest(test)

    def stopTest(self, test):
        self.stopped.append(test.id())
        super().stopTest(test)

    def origin(self, test, err):
        if err[0] is not AssertionError:
            return False
        codes = []
        trace = err[2]
        while trace is not None:
            codes.append(trace.tb_frame.f_code)
            trace = trace.tb_next
        body = self.body_codes.get(test.id())
        positions = [i for i, code in enumerate(codes) if code is body]
        return (len(positions) == 1 and
                all(code in _ASSERTION_CODES for code in codes[positions[0] + 1:]))

    def addSuccess(self, test):
        self.success_ids.append(test.id())
        super().addSuccess(test)

    def addFailure(self, test, err):
        # A regular failure must be the identical exception escaping the actual
        # selected method invocation, not setup/teardown/cleanup or callbacks.
        self.failure_ids.append(test.id())
        self.origins.append(self.escaping.pop((test.id(), id(err[1])), False))
        super().addFailure(test, err)

    def addSubTest(self, test, subtest, err):
        if err is not None:
            self.failure_ids.append(test.id())
            self.origins.append(self.active == test.id() and self.origin(test, err))
        super().addSubTest(test, subtest, err)

    def admitted(self, killed):
        complete = (len(set(self.expected)) == len(self.expected) and bool(self.expected)
                    and tuple(self.started) == self.expected
                    and tuple(self.stopped) == self.expected
                    and tuple(self.entered) == self.expected
                    and self.testsRun == len(self.expected))
        clean = not (self.errors or self.skipped or self.expectedFailures or self.unexpectedSuccesses)
        terminal = (len(self.success_ids) == len(set(self.success_ids))
                    and not set(self.success_ids).intersection(self.failure_ids)
                    and set(self.success_ids).union(self.failure_ids) == set(self.expected))
        if killed:
            return bool(complete and terminal and clean and self.failures and self.origins and all(self.origins)
                        and len(self.origins) == len(self.failures))
        return bool(complete and terminal and clean and not self.failures and not self.origins
                    and tuple(self.success_ids) == self.expected)


def run_oracle_cases(case_class, methods):
    cases = [case_class(method) for method in methods]
    result = OracleOriginResult(cases)
    for case in cases:
        def call(selected, method):
            code = getattr(method, '__func__', None)
            if (code is None or code.__code__ is not result.body_codes[selected.id()]
                    or inspect.iscoroutinefunction(code) or inspect.isgeneratorfunction(code)
                    or inspect.isasyncgenfunction(code)):
                raise RuntimeError('unsupported oracle body')
            result.entered.append(selected.id())
            result.active = selected.id()
            try:
                outcome = method()
                if outcome is not None:
                    if inspect.iscoroutine(outcome):
                        outcome.close()
                    raise RuntimeError('non-None oracle body result')
                return None
            except BaseException as exc:
                result.escaping[(selected.id(), id(exc))] = result.origin(
                    selected, (type(exc), exc, exc.__traceback__))
                raise
            finally:
                result.active = None
        case._callTestMethod = types.MethodType(call, case)
    unittest.TestSuite(cases).run(result)
    return result


class NodeOracleTests(unittest.TestCase):
    def outcome(self, missing, changed=None):
        m = load()
        manifest = json.loads((WRAPPER.parent / 'SOURCES.json').read_text())
        outputs = [missing] if changed is None else [missing, changed]
        capture = io.StringIO()
        with mock.patch.object(m, 'run', side_effect=outputs):
            with contextlib.redirect_stdout(capture):
                failures = m.negative_failures(WRAPPER.parent, manifest, quick=changed is None)
        return failures, capture.getvalue()

    def test_changed_rejects_unrelated_results(self):
        cases = [(1,b'',b'Traceback: crash\n'), (17,b'failed',b'oom'), (-9,b'',b''),
                 (0,b'',b''), (0,b'unrelated',b''), (1,EXPECTED,b''),
                 (17,EXPECTED,b''), (-9,EXPECTED,b''), (0,EXPECTED,b'warning'),
                 (0,EXPECTED[:-1],b''), (0,EXPECTED+b'noise',b''),
                 (0,EXPECTED+b'\n',b''), (0,b'noise'+EXPECTED,b''),
                 (0,EXPECTED+EXPECTED,b''),
                 (0,EXPECTED.replace(b'0.075705195564',b'0.075705195565'),b'')]
        for case in cases:
            with self.subTest(case=case):
                failures,_ = self.outcome((1,b'',MISSING),case)
                self.assertTrue(any('negative control (b)' in f for f in failures),failures)

    def test_changed_accepts_exact_sensitivity(self):
        failures, output = self.outcome((1,b'',MISSING),(0,EXPECTED,b''))
        self.assertEqual(failures,[])
        records=[json.loads(line) for line in output.splitlines()]
        records=[r for r in records if r.get('output_sensitivity_verified') is True]
        self.assertEqual(len(records),1)
        self.assertNotIn('rejected',records[0])

    def test_changed_fixture_identity(self):
        self.assertEqual(len(EXPECTED),989)
        self.assertEqual(hashlib.sha256(EXPECTED).hexdigest(),
                         '1e547fee84313e3fd62d822c97f9c76b08335112bcd71337e00bc06ea4a31bf8')
        stored=(WRAPPER.parent/'certificate_v2/results/assembly_stdout.txt').read_bytes()
        self.assertNotEqual(EXPECTED,b'\n'.join(x for x in stored.split(b'\n') if not x.startswith(b'C9')))

    def test_missing_rejects_inexact_results(self):
        cases=[(1,b'noise',MISSING),(1,b'',b'error incomplete node values\n'),
               (1,b'',MISSING.replace(b'2194 of 2393',b'0 of 1')),
               (1,b'',MISSING.replace(b'AssertionError:',b'RuntimeError:')),
               (1,b'',MISSING.replace(b'ddcore.py',b'other.py')),
               (1,b'',MISSING.replace(b'line 23,',b'line 24,')),
               (1,b'',MISSING[:-1]),(1,b'',MISSING+b'\n'),
               (1,b'',MISSING+b'noise'),(1,b'',b'noise'+MISSING),
               (1,b'',MISSING+MISSING),
               (1,b'',MISSING.replace(str(WRAPPER.parent).encode(),b'/wrong')),
               (1,b'',b''),(0,b'',MISSING),(17,b'',MISSING),(-9,b'',MISSING)]
        for case in cases:
            with self.subTest(case=case):
                failures,_=self.outcome(case)
                self.assertTrue(any('negative control (c)' in f for f in failures),failures)

    def test_missing_accepts_exact_completeness_rejection(self):
        failures,output=self.outcome((1,b'',MISSING))
        self.assertEqual(failures,[])
        self.assertIn('"input_completeness_rejection_verified": true',output)

    def test_missing_fixture_identity(self):
        self.assertEqual(hashlib.sha256(MISSING_TEMPLATE).hexdigest(),
                         '74c9a35ac855ac1abba7c48a3eb1f25333b277738fd75da47fa8c73fe402833b')

    def test_real_bounded_specimens(self):
        m=load()
        capture=io.StringIO()
        with contextlib.redirect_stdout(capture):
            failures=m.negative_failures(WRAPPER.parent,json.loads((WRAPPER.parent/'SOURCES.json').read_text()),False)
        self.assertEqual(failures,[])
        self.assertIn('"output_sensitivity_verified": true',capture.getvalue())
        self.assertIn('"input_completeness_rejection_verified": true',capture.getvalue())

    def test_workflow_binding(self):
        text=(ROOT/'.github/workflows/lifetime-dd-model-d.yml').read_text()
        for name in ('tests/test_lifetime_dd_node_oracle.py',
                     'tests/fixtures/lifetime_dd_changed_node_stdout.txt',
                     'tests/fixtures/lifetime_dd_missing_node_stderr.txt'):
            self.assertIn("      - '"+name+"'",text)
            self.assertIn('cp '+name,text)
        self.assertIn('-p test_lifetime_dd_node_oracle.py -v',text)

    def mutations(self, needle, variants, methods):
        source=WRAPPER.read_text()
        self.assertEqual(source.count(needle),1)
        for name,replacement in variants.items():
            with self.subTest(mutation=name):
                baseline = run_oracle_cases(NodeOracleTests, methods)
                self.assertTrue(baseline.admitted(False), 'oracle baseline not admitted')
                subject=types.ModuleType('mutated_dd_oracle')
                subject.__file__=str(WRAPPER)
                exec(compile(source.replace(needle,replacement),str(WRAPPER),'exec'),subject.__dict__)
                capture=io.StringIO()
                with mock.patch.object(sys.modules[__name__],'load',return_value=subject):
                    with contextlib.redirect_stdout(capture):
                        result=run_oracle_cases(NodeOracleTests, methods)
                self.assertEqual(result.testsRun,2)
                self.assertEqual(result.errors,[],capture.getvalue())
                self.assertGreater(len(result.failures),0,capture.getvalue())
                self.assertTrue(result.admitted(True), 'failure did not originate in selected oracle body')

    def test_changed_mutations(self):
        self.mutations("if (code, out, err) != (0, CHANGED_NODE_STDOUT, b''):",{
            'generic_difference':"if code == 0 and out == b'unchanged baseline':",
            'ignore_exit':"if (out, err) != (CHANGED_NODE_STDOUT, b''):",
            'ignore_stderr':"if (code, out) != (0, CHANGED_NODE_STDOUT):",
            'ignore_stdout':"if (code, err) != (0, b''):",
            'strip':"if (code, out.strip(), err) != (0, CHANGED_NODE_STDOUT.strip(), b''):",
            'prefix':"if code != 0 or err or not out.startswith(CHANGED_NODE_STDOUT):",
            'accept':'if False:', 'reject':'if True:'},
            ('test_changed_rejects_unrelated_results','test_changed_accepts_exact_sensitivity'))

    def test_missing_mutations(self):
        self.mutations("if (code, out, err) != (1, b'', expected_missing):",{
            'substring':"if code != 1 or b'incomplete node values' not in err:",
            'ignore_exit':"if (out, err) != (b'', expected_missing):",
            'ignore_stdout':"if (code, err) != (1, expected_missing):",
            'ignore_stderr':"if (code, out) != (1, b''):",
            'strip':"if (code, out, err.strip()) != (1, b'', expected_missing.strip()):",
            'prefix':"if code != 1 or out or not err.startswith(expected_missing):",
            'accept':'if False:', 'reject':'if True:'},
            ('test_missing_rejects_inexact_results','test_missing_accepts_exact_completeness_rejection'))


def _foreign_assertion():
    raise AssertionError('subject origin, not test oracle')


class OracleOriginSelfTests(unittest.TestCase):
    def observe(self, behavior):
        class Probe(unittest.TestCase):
            def setUp(self):
                self.fixture = False
                if behavior == 'setup':
                    self.fail('setup')
                if behavior in ('setup-calls-body', 'setup-subtest', 'teardown-subtest'):
                    self.test_body()
                if behavior == 'cleanup':
                    self.addCleanup(self.fail, 'cleanup')
            def tearDown(self):
                if behavior == 'teardown-subtest':
                    self.fixture = True
                    self.test_body()
                if behavior == 'teardown':
                    self.fail('teardown')
            def helper(self):
                self.fail('test helper, not authorized body')
            def test_body(self):
                if behavior in ('assertion', 'setup-calls-body'):
                    self.assertEqual(1, 2)
                elif behavior == 'direct':
                    raise AssertionError('direct selected oracle')
                elif behavior in ('subtest', 'setup-subtest') or (behavior == 'teardown-subtest' and self.fixture):
                    with self.subTest(value=1):
                        self.assertTrue(False)
                elif behavior == 'subject':
                    _foreign_assertion()
                elif behavior == 'helper':
                    self.helper()
                elif behavior == 'nested':
                    (lambda: _foreign_assertion())()
                elif behavior == 'subtest-subject':
                    with self.subTest(value=1):
                        _foreign_assertion()
                elif behavior == 'skip':
                    self.skipTest('skip')
                elif behavior == 'runtime':
                    raise RuntimeError('runtime')
        return run_oracle_cases(Probe, ('test_body',))

    def test_accepts_genuine_body_and_subtest_assertions(self):
        for kind in ('assertion', 'direct', 'subtest'):
            with self.subTest(kind=kind):
                self.assertTrue(self.observe(kind).admitted(True))

    def test_baseline_requires_actual_success(self):
        self.assertTrue(self.observe('pass').admitted(False))
        self.assertFalse(self.observe('assertion').admitted(False))
        self.assertFalse(self.observe('pass').admitted(True))

    def test_rejects_setup_teardown_cleanup_and_manual_body(self):
        for kind in ('setup', 'teardown', 'cleanup', 'setup-calls-body', 'setup-subtest', 'teardown-subtest'):
            with self.subTest(kind=kind):
                self.assertFalse(self.observe(kind).admitted(True))

    def test_rejects_subject_helper_nested_and_subtest_origin(self):
        for kind in ('subject', 'helper', 'nested', 'subtest-subject'):
            with self.subTest(kind=kind):
                self.assertFalse(self.observe(kind).admitted(True))

    def test_rejects_runtime_and_skip(self):
        for kind in ('runtime', 'skip'):
            with self.subTest(kind=kind):
                self.assertFalse(self.observe(kind).admitted(True))
                self.assertFalse(self.observe(kind).admitted(False))

    def test_rejects_expected_and_unexpected_success(self):
        class Expected(unittest.TestCase):
            @unittest.expectedFailure
            def test_bad(self): self.fail('expected')
            @unittest.expectedFailure
            def test_good(self): pass
        for method in ('test_bad', 'test_good'):
            result = run_oracle_cases(Expected, (method,))
            self.assertFalse(result.admitted(True))
            self.assertFalse(result.admitted(False))

    def test_rejects_empty_duplicate_and_missing_execution(self):
        class Passing(unittest.TestCase):
            def test_body(self): pass
        for methods in ((), ('test_body', 'test_body')):
            self.assertFalse(run_oracle_cases(Passing, methods).admitted(False))
        result = self.observe('assertion')
        result.entered.clear()
        self.assertFalse(result.admitted(True))
        result = self.observe('pass')
        result.stopped.clear()
        self.assertFalse(result.admitted(False))

    def test_rejects_missing_and_duplicate_success_events(self):
        class Missing(unittest.TestCase):
            def test_body(self): pass
            def run(self, result):
                result.startTest(self)
                self._callTestMethod(self.test_body)
                result.stopTest(self)
        class Duplicate(unittest.TestCase):
            def test_body(self): pass
            def run(self, result):
                super().run(result)
                result.addSuccess(self)
        for case in (Missing, Duplicate):
            self.assertFalse(run_oracle_cases(case, ('test_body',)).admitted(False))
        result = self.observe('assertion')
        result.success_ids.append(result.expected[0])
        self.assertFalse(result.admitted(True))

    def test_rejects_returned_deferred_and_non_none_values(self):
        class Returned(unittest.TestCase):
            def test_iterator(self): return iter(())
            def test_value(self): return 1
        for method in ('test_iterator', 'test_value'):
            self.assertFalse(run_oracle_cases(Returned, (method,)).admitted(False))

    def test_rejects_lazy_body(self):
        class Lazy(unittest.TestCase):
            def test_body(self): yield 1
        self.assertFalse(run_oracle_cases(Lazy, ('test_body',)).admitted(False))

    def test_grader_source_safeguards_are_assertion_killed(self):
        source = Path(__file__).read_text()
        controls = (
            ('origin', 'all(code in _ASSERTION_CODES for code in codes[positions[0] + 1:])',
             'True', 'test_rejects_subject_helper_nested_and_subtest_origin'),
            ('escaping', 'self.escaping.pop((test.id(), id(err[1])), False)',
             'True', 'test_rejects_setup_teardown_cleanup_and_manual_body'),
            ('phase', 'self.active == test.id() and self.origin(test, err)',
             'self.origin(test, err)', 'test_rejects_setup_teardown_cleanup_and_manual_body'),
            ('population', 'complete and terminal and clean', 'True and terminal and clean',
             'test_rejects_empty_duplicate_and_missing_execution'),
            ('terminal', 'terminal = (', 'terminal = True or (',
             'test_rejects_missing_and_duplicate_success_events'),
            ('skip', 'self.errors or self.skipped or self.expectedFailures or self.unexpectedSuccesses',
             'self.errors or self.expectedFailures or self.unexpectedSuccesses',
             'test_rejects_runtime_and_skip'),
            ('expected', 'self.errors or self.skipped or self.expectedFailures or self.unexpectedSuccesses',
             'self.errors or self.skipped', 'test_rejects_expected_and_unexpected_success'),
        )
        # Only implementation preceding this self-test class is mutated; these
        # frozen mutation literals cannot become alternative replacement sites.
        implementation, tests = source.split('class OracleOriginSelfTests', 1)
        for name, before, after, method in controls:
            with self.subTest(safeguard=name):
                baseline = run_oracle_cases(OracleOriginSelfTests, (method,))
                self.assertTrue(baseline.admitted(False))
                count = implementation.count(before)
                self.assertEqual(count, 2 if name == 'population' else 1)
                mutated = implementation.replace(before, after) + 'class OracleOriginSelfTests' + tests
                module = types.ModuleType('dd_origin_mutant_' + name)
                module.__file__ = __file__
                with mock.patch.dict(sys.modules, {module.__name__: module}):
                    exec(compile(mutated, __file__, 'exec'), module.__dict__)
                    # The outer, unchanged grader authenticates failures in the
                    # selected self-test. The mutant cannot grade itself green.
                    result = run_oracle_cases(module.OracleOriginSelfTests, (method,))
                if name in ('skip', 'expected'):
                    # These isolated omissions are behaviorally redundant under
                    # exact terminal accounting; retain and assert non-kill,
                    # rather than inflate the effective mutation inventory.
                    self.assertTrue(result.admitted(False), name)
                else:
                    self.assertTrue(result.admitted(True), name)

    def test_subject_mutant_is_not_admitted(self):
        with self.assertRaisesRegex(AssertionError, 'selected oracle body'):
            NodeOracleTests().mutations(
                "if (code, out, err) != (0, CHANGED_NODE_STDOUT, b''):",
                {'subject': "if (_ for _ in ()).throw(AssertionError('subject')):"},
                ('test_changed_rejects_unrelated_results', 'test_changed_accepts_exact_sensitivity'))


if __name__ == '__main__':
    unittest.main()
