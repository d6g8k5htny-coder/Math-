"""External qualification of the pinned nine-form oracle, not its analytic model."""
import argparse
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from math import factorial
import os
from pathlib import Path
import sys
import unittest
from unittest import mock

DEFAULT_ORACLE = Path(__file__).resolve().parents[2] / 'reviews/c2_interval_audit_20261001/oracle.py'
ORACLE = Path(os.environ.get('C2_ORACLE_UNDER_TEST', DEFAULT_ORACLE))
PAIRS = {
    '1.c': ('0.1101103789590410', '0.1101103789590625'),
    '1.c2': ('0.2300445802661503', '0.2300445802661998'),
    '1.ratio': ('2.089217950577392', '2.089217950578207'),
    '2.c': ('0.07340691930602738', '0.07340691930604167'),
    '2.c2': ('0.2215244106266632', '0.2215244106267110'),
    '2.ratio': ('3.017759261945122', '3.017759261946299'),
    '3.c': ('0.04177593184059426', '0.04177593184060272'),
    '3.c2': ('0.1612340491269447', '0.1612340491269810'),
    '3.ratio': ('3.859496174547095', '3.859496174548665'),
}


class OracleQualification(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location('qualified_c2_oracle', ORACLE)
        cls.o = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.o)

    def assert_table(self, report):
        self.assertEqual(set(report['values']), set(PAIRS))
        self.assertEqual(report['scope'], 'independent numerical certification of the nine supplied closed forms only')
        self.assertEqual(report['scientific_effect'], 'NONE')
        self.assertIs(report['source_analytic_derivation_revalidated'], False)
        self.assertIs(report['binary_float_used'], False)
        self.assertEqual((report['dyadic_bits'], report['Gamma_shift'], report['Gamma_terms']), (240, 40, 20))
        for key, item in report['values'].items():
            self.assertEqual(tuple(item['published_interval']), PAIRS[key])
            lo, hi = map(F, PAIRS[key])
            a, b = map(F, item['independent_rational_interval'])
            self.assertTrue(lo < a <= b < hi, key)
            self.assertIs(item['strictly_inside'], True)

    def test_q_exact_rejections(self):
        for value in (True, False, 0.5, '1/3', None):
            with self.subTest(value=value), self.assertRaises(TypeError): self.o.q(value)

    def test_q_fraction_inputs(self):
        for value in (-3, 0, 7, F(1, 3), -F(11, 17)):
            self.assertIs(type(self.o.q(value)), F)
            self.assertEqual(self.o.q(value), value)

    def test_cached_exact_inputs_reject_float_alias(self):
        for function in (self.o.log_bounds, self.o.lngamma_bounds, self.o.gamma_bounds):
            function.cache_clear(); function(F(1, 2))
            with self.subTest(function=function.__name__), self.assertRaises(TypeError): function(0.5)

    def test_enclosure_outward(self):
        grid = F(1, self.o.SCALE)
        for value in (grid / 3, -grid / 3):
            lo, hi = self.o.enclosure(value)
            self.assertTrue(lo <= value <= hi)
            self.assertEqual(hi - lo, grid)

    def test_enclosure_reversed(self):
        with self.assertRaises(ValueError): self.o.enclosure(F(2), F(1))

    def test_corner_arithmetic(self):
        a, b = (-F(7, 5), F(2, 3)), (-F(5, 3), -F(1, 7))
        for operation, exact in ((self.o.plus, lambda x, y: x+y),
                                 (self.o.minus, lambda x, y: x-y),
                                 (self.o.times, lambda x, y: x*y),
                                 (self.o.over, lambda x, y: x/y)):
            lo, hi = operation(a, b)
            for x in a:
                for y in b: self.assertTrue(lo <= exact(x, y) <= hi)

    def test_division_zero_guard(self):
        for divisor in ((-F(1), F(1)), (F(0), F(1)), (-F(1), F(0))):
            with self.subTest(divisor=divisor), self.assertRaises(ValueError):
                self.o.over((F(1), F(2)), divisor)

    def test_power_exact_negative(self):
        self.assertEqual(self.o.power((F(2), F(2)), -3), (F(1, 8), F(1, 8)))
        with self.assertRaises(TypeError): self.o.power((F(2), F(2)), True)

    def test_atan_remainder(self):
        lo, hi = self.o.atan_inv(5, terms=1)
        self.assertLessEqual(lo, F(74, 375))
        self.assertGreaterEqual(hi, F(1, 5))
        self.assertLess(lo, hi)

    def test_log_remainder(self):
        lo, hi = self.o._log_small(F(3, 2), terms=1)
        self.assertLessEqual(lo, F(2, 5))
        self.assertGreaterEqual(hi, F(2, 5) + F(2, 375))

    def test_log_domain(self):
        for value in (F(0), -F(1)):
            with self.assertRaises(ValueError): self.o.log_bounds(value)
        for value in (F(1, 2), F(3)):
            with self.assertRaises(ValueError): self.o._log_small(value)

    def test_exp_remainder(self):
        # A finer test-only output grid exposes the positive omitted term;
        # the oracle's immutable source and production 240-bit setting stay intact.
        with mock.patch.object(self.o, 'SCALE', 1 << 2048):
            lo, hi = self.o.exp_bounds(F(1, 2))
        positive_partial = sum((F(1, 2)**j / factorial(j) for j in range(102)), F(0))
        self.assertLess(lo, positive_partial)
        self.assertGreaterEqual(hi, positive_partial)

    def test_exp_zero_reciprocal(self):
        self.assertEqual(self.o.exp_bounds(F(0)), (F(1), F(1)))
        lo, hi = self.o.times(self.o.exp_bounds(F(7, 5)), self.o.exp_bounds(-F(7, 5)))
        self.assertTrue(lo <= 1 <= hi)

    def test_root_brackets(self):
        self.assertEqual(self.o.root_bounds(F(64), 6), (F(2), F(2)))
        for value, root in ((F(12), 6), (F(6), 2), (F(7, 3), 3)):
            lo, hi = self.o.root_bounds(value, root)
            self.assertTrue(lo**root <= value <= hi**root)
            self.assertLessEqual(hi-lo, F(1, self.o.SCALE))

    def test_root_domain(self):
        for value, root in ((-F(1), 2), (F(1), 0), (F(1), True)):
            with self.assertRaises(ValueError): self.o.root_bounds(value, root)

    def test_gamma_zero_log_at_one(self):
        lo, hi = self.o.lngamma_bounds(F(1))
        self.assertTrue(lo <= 0 <= hi, 'Gamma(1)=1 requires log-Gamma(1)=0')

    def test_gamma_domain(self):
        for value in (F(0), -F(1, 6)):
            with self.assertRaises(ValueError): self.o.gamma_bounds(value)

    def test_decimal_outward(self):
        for interval in ((F(1, 3), F(2, 3)), (-F(2, 3), -F(1, 3))):
            lo, hi = map(F, self.o.decimal_pair(interval, places=20))
            self.assertTrue(lo <= interval[0] <= interval[1] <= hi)

    def test_coefficients_nine_contained(self):
        values = self.o.coefficients()
        self.assertEqual(set(values), set(PAIRS))
        self.assertEqual(self.o.PUBLISHED, PAIRS)
        for key, (a, b) in values.items():
            lo, hi = map(F, PAIRS[key])
            self.assertTrue(lo < a <= b < hi, key)
            self.assertIs(type(a), F); self.assertIs(type(b), F)

    def test_results_table_and_scope(self):
        self.assert_table(self.o.results())

    def test_results_wrong_interval_rejected(self):
        wrong = dict(self.o.coefficients()); wrong['1.c'] = (F(2), F(3))
        with mock.patch.object(self.o, 'coefficients', return_value=wrong), self.assertRaises(ArithmeticError):
            self.o.results()

    def test_results_missing_reference_rejected(self):
        references = dict(PAIRS); del references['1.c']
        with mock.patch.object(self.o, 'PUBLISHED', references), self.assertRaises(KeyError):
            self.o.results()

    def test_qualification_rejects_missing_computed_key(self):
        incomplete = dict(self.o.coefficients()); del incomplete['1.ratio']
        with mock.patch.object(self.o, 'coefficients', return_value=incomplete):
            report = self.o.results()
        # The original results() itself does not enforce computed key completeness.
        with self.assertRaises(AssertionError): self.assert_table(report)

    def test_results_extra_computed_key_rejected(self):
        extra = dict(self.o.coefficients()); extra['extra'] = (F(1), F(1))
        with mock.patch.object(self.o, 'coefficients', return_value=extra), self.assertRaises(KeyError):
            self.o.results()

    def test_qualification_rejects_falsified_reference(self):
        references = dict(PAIRS); references['1.c'] = ('-1', '1')
        with mock.patch.object(self.o, 'PUBLISHED', references): report = self.o.results()
        with self.assertRaises(AssertionError): self.assert_table(report)


_PHASE_COUNTERS = ('setup_entered', 'setup_completed', 'body_entered', 'body_exited',
                   'teardown_entered', 'teardown_completed', 'cleanup_entered', 'cleanup_completed',
                   'failure_count', 'error_count')
_ACTIVE_TEST = None


class PhaseResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lifecycle = {'schema': 'unittest.body-phase/v1', 'tests': [], 'events': []}

    def startTest(self, test):
        global _ACTIVE_TEST
        supported = all(getattr(type(test), name) is getattr(unittest.TestCase, name)
                        for name in ('run', '_callSetUp', '_callTestMethod', '_callTearDown',
                                     '_callCleanup', 'doCleanups'))
        row = {'id': test.id(), 'supported': supported, **{name: 0 for name in _PHASE_COUNTERS}}
        test._qualification_record = row; test._qualification_phase = 'start'
        self.lifecycle['tests'].append(row); _ACTIVE_TEST = test
        super().startTest(test)

    def stopTest(self, test):
        global _ACTIVE_TEST
        _ACTIVE_TEST = None
        super().stopTest(test)

    def event(self, test, kind, err):
        event = {'id': test.id(), 'phase': getattr(test, '_qualification_phase', 'unknown'),
                 'kind': kind, 'exception': err[0].__name__, 'assertion': issubclass(err[0], AssertionError)}
        self.lifecycle['events'].append(event)
        row = getattr(test, '_qualification_record', None)
        if row is not None: row['failure_count' if kind == 'failure' else 'error_count'] += 1

    def addFailure(self, test, err):
        self.event(test, 'failure', err); super().addFailure(test, err)

    def addError(self, test, err):
        self.event(test, 'error', err); super().addError(test, err)

    def addSubTest(self, test, subtest, err):
        if err is not None:
            self.event(test, 'failure' if issubclass(err[0], test.failureException) else 'error', err)
        super().addSubTest(test, subtest, err)


def install_phases():
    originals = {}
    for method, phase, entered, completed in (
        ('_callSetUp', 'setup', 'setup_entered', 'setup_completed'),
        ('_callTestMethod', 'body', 'body_entered', 'body_exited'),
        ('_callTearDown', 'teardown', 'teardown_entered', 'teardown_completed'),
        ('_callCleanup', 'cleanup', 'cleanup_entered', 'cleanup_completed'),
    ):
        original = getattr(unittest.TestCase, method); originals[method] = original
        def tracked(test, *args, _original=original, _phase=phase, _entered=entered, _completed=completed, **kwargs):
            test._qualification_phase = _phase
            row = getattr(test, '_qualification_record', None)
            if row is None: return _original(test, *args, **kwargs)
            row[_entered] += 1
            if _phase == 'body':
                try: return _original(test, *args, **kwargs)
                finally: row[_completed] += 1
            answer = _original(test, *args, **kwargs)
            row[_completed] += 1
            return answer
        setattr(unittest.TestCase, method, tracked)
    return originals


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report-json', type=Path, required=True)
    parser.add_argument('--case', action='append')
    args = parser.parse_args()
    names = args.case or unittest.defaultTestLoader.getTestCaseNames(OracleQualification)
    if len(names) != len(set(names)) or any(name not in unittest.defaultTestLoader.getTestCaseNames(OracleQualification) for name in names):
        parser.error('unknown or duplicate case')
    if args.report_json.exists() or args.report_json.is_symlink(): parser.error('report output already exists')
    suite = unittest.TestSuite(OracleQualification(name) for name in names)
    identities = [test.id() for test in suite]
    originals = install_phases()
    try: result = unittest.TextTestRunner(verbosity=2, resultclass=PhaseResult).run(suite)
    finally:
        for name, original in originals.items(): setattr(unittest.TestCase, name, original)
    def identity(test): return getattr(test, 'test_case', test).id()
    report = {'schema': 'c2.oracle.qualification-observation.v1', 'test_ids': identities,
        'tests_run': result.testsRun, 'lifecycle': result.lifecycle,
        'expected_failures': [identity(test) for test, _ in result.expectedFailures], 'failures': [identity(test) for test, _ in result.failures],
        'errors': [identity(test) for test, _ in result.errors],
        'skipped': [identity(test) for test, _ in result.skipped],
        'unexpected_successes': [test.id() for test in result.unexpectedSuccesses],
        'was_successful': result.wasSuccessful(), 'oracle_sha256': hashlib.sha256(ORACLE.read_bytes()).hexdigest()}
    args.report_json.write_text(json.dumps(report, sort_keys=True, indent=2) + '\n')
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__': raise SystemExit(main())
