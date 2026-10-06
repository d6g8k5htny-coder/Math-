"""Exact output contracts for the C6 numerical replay, not numerical certification.

The workflow authenticates the packet and consumed pins before calling replay.
Expectations below were measured from unchanged coefficients.py blob
bd45a9fdecf300111b646644384dcead20c2e529 in normal and optimized Python modes.
They are fixed source, never learned from the invocation being validated.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

MUTANT_REASONS = {
    'cubic-sign': 'classifier agrees with the direct critical-point count on the typed domain',
    'antiderivative': '[LM] cubic mass 48 k^5 on n = 2',
    'typed-boundary': 'classifier agrees with the direct critical-point count on the typed domain',
}


class ProtocolError(RuntimeError):
    """A completed child did not satisfy its fixed report contract."""


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate JSON key: ' + key)
        result[key] = value
    return result


def reject_number(value):
    raise ValueError('numerical JSON value is outside the report schema: ' + value)


def verify_report(result: subprocess.CompletedProcess, mutant: str | None = None) -> None:
    """Require the whole typed report, actual exit and captured empty stderr."""
    if mutant is not None and mutant not in MUTANT_REASONS:
        raise ValueError('unrecognized C6 numerical mutant: ' + repr(mutant))
    expected = ({'mode': 'check', 'passed': True, 'scientific_effect': 'NONE'}
                if mutant is None else {'error': MUTANT_REASONS[mutant], 'passed': False})
    code = 0 if mutant is None else 1
    label = 'baseline' if mutant is None else mutant
    if type(result.returncode) is not int or result.returncode != code:
        raise ProtocolError(label + ': unexpected return code ' + repr(result.returncode))
    if type(result.stdout) is not bytes or type(result.stderr) is not bytes:
        raise ProtocolError(label + ': both raw output streams must be captured')
    if result.stderr != b'':
        raise ProtocolError(label + ': unexpected stderr, SHA256=' + hashlib.sha256(result.stderr).hexdigest())
    try:
        report = json.loads(result.stdout.decode('utf-8'), object_pairs_hook=unique_object,
                            parse_int=reject_number, parse_float=reject_number, parse_constant=reject_number)
    except (ValueError, UnicodeError, RecursionError) as exc:
        raise ProtocolError(label + ': invalid UTF-8/JSON report') from exc
    if type(report) is not dict or report.keys() != expected.keys():
        raise ProtocolError(label + ': report fields differ from the fixed contract')
    for key, value in expected.items():
        if type(report[key]) is not type(value) or report[key] != value:
            raise ProtocolError(label + ': wrong type or value for ' + key)


def replay(root: Path) -> None:
    """Execute the original two-mode, four-stage inventory with strict reports.

    Caller must first validate the full packet and current consumed-source pins.
    Timeout and process-launch exceptions propagate; they are never rejections.
    This function never calls the RESULTS-regenerating no-argument path.
    """
    root = Path(root).resolve()
    script = str(root / 'coefficients.py')
    for flags in (['-B', '-S'], ['-B', '-O', '-S']):
        for mutant in (None, *MUTANT_REASONS):
            args = ['--check'] + ([] if mutant is None else ['--mutant', mutant])
            result = subprocess.run([sys.executable, *flags, script, *args], cwd=root,
                                    capture_output=True, timeout=900)
            verify_report(result, mutant)
            print(json.dumps({'flags': flags, 'mutant': mutant, 'returncode': result.returncode,
                              'stdout_sha256': hashlib.sha256(result.stdout).hexdigest(),
                              'stderr_sha256': hashlib.sha256(result.stderr).hexdigest(),
                              'scientific_effect': 'NONE'}, sort_keys=True), flush=True)
