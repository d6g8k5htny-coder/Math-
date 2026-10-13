"""Source-bound output protocol for the unchanged remainder-rate finite controls.

The caller authenticates the full packet, consumed/cited inputs and the pinned
unmerged dependency first. Fixed report values were measured from checker blob
3293ca22ab89bd650f361832c62b03724a976f03; no running child supplies its own oracle.
This is engineering validation, not a proof of the accompanying rate theorem.
"""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys

BASELINE = {'checks': {'E1_exponent_ledger': {'info': {'grid_points': 208, 'relative_exponents': {'v1': '1/2', 'v1.1': '7/12'}, 'twelfth_power_points': 4, 'v1': {'rate': '1/6', 'theta': '1/6'}, 'v1.1': {'rate': '1/4', 'theta': '1/12'}}, 'passed': True}, 'E2_barrier_arithmetic': {'info': {'barrier_cases': 48, 'solved_form_points': 4}, 'passed': True}, 'E3_soft_eigenvalue_determinant': {'info': {'matrices': 5, 'sizes': [2, 3, 4]}, 'passed': True}, 'E4_integrals_and_cutoff_ledger': {'info': {'cutoff_ledger_points': 3, 'integral_points': 3, 'window_integral_points': 3}, 'passed': True}, 'E5_sign_window': {'info': {'exact_equality_cases': 0, 'near_boundary_case': True, 'same_sign_instances': 13858, 'typed_instances': 15962}, 'passed': True}}, 'mutant': None, 'object': 'CL-D2-REMAINDER-RATE-20260930-v1.1', 'passed': True, 'scientific_effect': 'NONE'}
# Only these observed check records change; every other nested field stays fixed.
MUTATIONS = {'M1': ('E1_exponent_ledger', {'info': 'v1.1 ledger minimum at theta = 1/12 is 1/4, not the claimed rate 1/3', 'passed': False}), 'M2': ('E2_barrier_arithmetic', {'info': 'cubic term not dominated at t = 3/25 (lambda 1/5, K 3)', 'passed': False}), 'M3': ('E3_soft_eigenvalue_determinant', {'info': "det <= lambda_min lambda_max^(d-1) fails (spectrum ['1/100', '2'])", 'passed': False}), 'M4': ('E5_sign_window', {'info': '|det K_i| bound fails at (Fraction(0, 1), Fraction(-2, 1), Fraction(-3, 1), Fraction(1, 3), Fraction(-2, 5), Fraction(1, 10))', 'passed': False})}
MUTANTS = ('M1', 'M2', 'M3', 'M4')


class ProtocolError(RuntimeError):
    """A completed invocation did not satisfy its complete fixed contract."""


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate JSON key: ' + key)
        result[key] = value
    return result


def reject_float(value):
    raise ValueError('floating or nonfinite JSON value: ' + value)


def typed_equal(actual, expected):
    """Recursive equality without Boolean/integer or integer/float coercion."""
    if type(actual) is not type(expected):
        return False
    if type(expected) is dict:
        return actual.keys() == expected.keys() and all(
            typed_equal(actual[key], value) for key, value in expected.items())
    if type(expected) is list:
        return len(actual) == len(expected) and all(
            typed_equal(a, b) for a, b in zip(actual, expected))
    return actual == expected


def verify_report(result, label, baseline_bytes):
    if label not in ('baseline', *MUTANTS, 'M9'):
        raise ValueError('unknown protocol stage')
    expected_exit = 0 if label == 'baseline' else 2 if label == 'M9' else 1
    if type(result.returncode) is not int or result.returncode != expected_exit:
        raise ProtocolError(label + ': unexpected exit ' + repr(result.returncode))
    if type(result.stdout) is not bytes or type(result.stderr) is not bytes:
        raise ProtocolError(label + ': both binary streams must be captured')
    if label == 'M9':
        if result.stdout != b'' or result.stderr != b'unknown mutant label\n':
            raise ProtocolError('M9: unknown-label diagnostic differs')
        return
    if result.stderr != b'':
        raise ProtocolError(label + ': unexpected stderr')
    if label == 'baseline' and result.stdout != baseline_bytes:
        raise ProtocolError('baseline: output differs from frozen RESULTS.json bytes')
    try:
        report = json.loads(result.stdout.decode('utf-8'), object_pairs_hook=unique_object,
                            parse_float=reject_float, parse_constant=reject_float)
    except (ValueError, UnicodeError, RecursionError) as exc:
        raise ProtocolError(label + ': invalid complete UTF-8/JSON report') from exc
    expected = copy.deepcopy(BASELINE)
    if label != 'baseline':
        check, value = MUTATIONS[label]
        expected['mutant'] = label
        expected['passed'] = False
        expected['checks'][check] = value
    if not typed_equal(report, expected):
        raise ProtocolError(label + ': complete typed report differs from fixed contract')


def replay(root, mutants):
    """Run exactly twelve original invocations, preserving the 600-second budget.

    Launch and timeout exceptions propagate unchanged and stop subsequent work.
    Children inherit the caller's working directory, as in the original workflow.
    """
    if type(mutants) is not list or mutants != list(MUTANTS):
        raise ProtocolError('full ordered M1-M4 inventory required')
    root = Path(root).resolve()
    expected = (root / 'RESULTS.json').read_bytes()
    script = str(root / 'rate_ledger_check.py')
    for flags in (['-B', '-S'], ['-B', '-O', '-S']):
        for label in ('baseline', *MUTANTS, 'M9'):
            args = [] if label == 'baseline' else ['--mutant', label]
            result = subprocess.run([sys.executable, *flags, script, *args],
                                    capture_output=True, timeout=600)
            verify_report(result, label, expected)
            print(json.dumps({'flags': flags, 'stage': label, 'returncode': result.returncode,
                              'stdout_sha256': hashlib.sha256(result.stdout).hexdigest(),
                              'stderr_sha256': hashlib.sha256(result.stderr).hexdigest(),
                              'scientific_effect': 'NONE'}, sort_keys=True), flush=True)
