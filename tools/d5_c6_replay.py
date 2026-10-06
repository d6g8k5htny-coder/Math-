"""Fail-closed process contracts for the unchanged D5/C6 finite checkers.

The workflows authenticate packet membership and bytes before calling replay.
D5 and Palm deliberately raise AssertionError; their child adapter recognizes
only the measured message AND the original require/caller traceback origin.
Factorial keeps its native JSON result, with its exact single failed check.
This is an execution protocol, not a sandbox or a mathematical acceptance test.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import runpy
import subprocess
import sys


ASSERTIONS = {
    'd5': {
        'drop-frobenius-order': ('check_x', 'two-soft-direction exterior inequality failed in d=3'),
        'drop-s0-block': ('check_g', 'frame rank drop in d=2'),
        'drop-a4-column': ('check_g', 'frame rank drop in d=2'),
        'degree-four': ('check_r', 'degree-four axis rank is not d'),
        'row-operation-third': ('check_ro', 'height row has a negative power of s'),
        'euler-coefficient': ('check_eu', 'Euler identity remainder is not minus the quartic part'),
        'adjugate-sign': ('check_tb', 'block determinant identity failed'),
        'one-soft-direction': ('check_l', 'pin region I ledger is not r^3'),
        'flat-shell': ('check_l', 'shell sum is not bounded by the dyadic constants'),
        'weight-one-less-power': ('check_w', 'pin weight is not integrable in d=2'),
    },
    'palm': {
        'no-slab': ('check_pk', 'retained ball within zeta_0/2 of the witness sphere'),
        'weak-zeta': ('check_pk', 'zeta_0 exceeds eta_j/8'),
        'lambda-too-large': ('check_ex', 'Markov term does not decay in d=2'),
        'series-ratio': ('check_tl', 'no index makes the series ratio fall below 2^(-1/(4d)) for d=2 p=1'),
        'factorial-power': ('check_pw', '(N)_q <= N Psi^(q-1) fails at N=3 Psi=5 q=2'),
        'schur-upper': ('check_sc', 'Schur complement is not bounded above by c I'),
        'forget-mark-power': ('check_lg', 'R1 region II absorption power is not 6+3d in d=2'),
    },
}
FACTORIAL_FAILURES = {
    'wrong-elimination': 'ELIMINATION', 'touching-balls': 'PACKING',
    'no-log': 'RADIAL', 'short-remainder': 'REMAINDER',
}
FACTORIAL_CHECKS = {'ELIMINATION', 'CAP_ATTAINED', 'REMAINDER', 'PACKING', 'RADIAL'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def strict_json(raw):
    """Reject duplicates, nonfinite numbers, and floats (none is in this protocol)."""
    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, 'duplicate JSON key: ' + key)
            result[key] = value
        return result

    def invalid_number(value):
        raise ValueError('non-integer protocol number: ' + value)

    return json.loads(raw.decode('utf-8'), object_pairs_hook=unique,
                      parse_constant=invalid_number, parse_float=invalid_number)


def exact_value(actual, expected):
    """JSON structural equality without bool/int or integer/float coercion."""
    if type(actual) is not type(expected):
        return False
    if isinstance(expected, dict):
        return actual.keys() == expected.keys() and all(
            exact_value(actual[key], value) for key, value in expected.items())
    if isinstance(expected, list):
        return len(actual) == len(expected) and all(
            exact_value(a, b) for a, b in zip(actual, expected))
    return actual == expected


def assertion_report(family, mutant):
    caller, message = ASSERTIONS[family][mutant]
    return {'schema': 1, 'family': family, 'mutant': mutant,
            'failed_check': caller, 'message': message, 'passed': False,
            'scientific_effect': 'NONE'}


def assertion_child(family, script, mutant):
    """Run one authenticated script in a fresh process without editing it."""
    require(family in ASSERTIONS and mutant in ASSERTIONS[family], 'unknown assertion control')
    script = Path(script)
    require(script.is_file() and not script.is_symlink(), 'regular checker file required')
    script = script.resolve()
    caller, message = ASSERTIONS[family][mutant]
    sys.argv = [str(script), '--mutant', mutant]
    try:
        runpy.run_path(str(script), run_name='__main__')
    except AssertionError as exc:
        frames = []
        tb = exc.__traceback__
        while tb is not None:
            frames.append((tb.tb_frame.f_code.co_filename, tb.tb_frame.f_code.co_name))
            tb = tb.tb_next
        if (type(exc) is not AssertionError or exc.args != (message,) or
                frames[-2:] != [(str(script), caller), (str(script), 'require')]):
            raise  # A different crash/assertion is NOT an intended rejection.
        # Earlier stdout/stderr is deliberately not suppressed: the parent will
        # reject it as extra output, malformed JSON, or nonempty stderr.
        print(json.dumps(assertion_report(family, mutant), sort_keys=True))
        return 1
    return 0  # A mutant that completes normally must fail the parent's check.


def replay(script, expected, mutants, family, flags, timeout):
    """Exact baseline, then every named rejection, with real child processes."""
    contract = FACTORIAL_FAILURES if family == 'factorial' else ASSERTIONS.get(family)
    require(contract is not None and list(mutants) == list(contract), 'control inventory mismatch')
    require(tuple(flags) in (('-B', '-S'), ('-B', '-O', '-S')), 'unexpected Python flags')
    baseline = subprocess.run([sys.executable, *flags, str(script)],
                              capture_output=True, timeout=timeout)
    require(baseline.returncode == 0 and baseline.stderr == b'' and baseline.stdout == expected,
            'baseline failed or stdout/stderr differs under ' + ' '.join(flags))
    reference = None
    if family == 'factorial':
        reference = strict_json(expected)
        require(type(reference) is dict and set(reference) == {'object', 'checks', 'passed', 'scope'},
                'factorial baseline schema mismatch')
        require(reference['object'] == 'CL-C6-FACTORIAL-20260929-v1' and
                reference['scope'] == 'finite identities and one quadrature only; the analytic proof is PROOF.md' and
                reference['passed'] is True and type(reference['checks']) is dict and
                set(reference['checks']) == FACTORIAL_CHECKS and
                all(value is True for value in reference['checks'].values()),
                'factorial baseline identity/checks mismatch')
    for mutant in mutants:
        if family == 'factorial':
            command = [sys.executable, *flags, str(script), '--mutant', mutant]
            wanted = dict(reference, checks=dict(reference['checks']), passed=False)
            wanted['checks'][FACTORIAL_FAILURES[mutant]] = False
        else:
            command = [sys.executable, *flags, str(Path(__file__).resolve()),
                       '--assertion', family, str(script), mutant]
            wanted = assertion_report(family, mutant)
        result = subprocess.run(command, capture_output=True, timeout=timeout)
        require(result.returncode == 1 and result.stderr == b'',
                family + '/' + mutant + ': unexpected exit/stderr (not intended rejection)')
        require(exact_value(strict_json(result.stdout), wanted),
                family + '/' + mutant + ': wrong rejection identity, fields, types, or failed-check set')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--assertion', choices=sorted(ASSERTIONS), required=True)
    parser.add_argument('script', type=Path)
    parser.add_argument('mutant')
    args = parser.parse_args()
    if args.mutant not in ASSERTIONS[args.assertion]:
        parser.error('unknown mutant for assertion family')
    return assertion_child(args.assertion, args.script, args.mutant)


if __name__ == '__main__':
    raise SystemExit(main())
