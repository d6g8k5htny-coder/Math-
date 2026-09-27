"""Bounded replay for the D5 pin microdisk note; finite checks are not a proof."""
from __future__ import annotations
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
EXPECTED = 12
MUTANTS = {
    'lose_half_shift_in_divided_row': ('6 * k * p * (p - 1) / q + t * (p - Q(1, 2)) + c * q / 2',
                                       '6 * k * p * (p - 1) / q + t * p + c * q / 2'),
    'wrong_reduced_jacobian': ('return r ** 3 * q * q', 'return r * r * q * q'),
    'drop_d_term_from_axis_solution': ('return r * (c - d * q) / 2, c * q', 'return r * c / 2, c * q'),
    'lose_q_factor_at_X': ("'X': dets['X'] / q,", "'X': dets['X'],"),
    'promote_microdisk_closure': ("'uniform_microdisk_majorant_closed': False", "'uniform_microdisk_majorant_closed': True"),
}


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def identities():
    pins = json.loads((ROOT / 'SOURCE_FILES.json').read_text())['files']
    for name, identity in pins.items():
        path = ROOT / name
        require(path.is_file() and not path.is_symlink(), 'regular source required: ' + name)
        raw = path.read_bytes()
        require({'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()} == identity,
                'identity mismatch: ' + name)
    return pins


def run_cmd(cmd, cwd, out, name, mutant=False):
    result = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, timeout=30)
    (out / (name + '.stdout')).write_text(result.stdout)
    (out / (name + '.stderr')).write_text(result.stderr)
    require(f'Ran {EXPECTED} tests' in result.stderr and 'skipped=' not in result.stderr,
            'unexpected coverage: ' + name)
    if mutant:
        require(result.returncode != 0 and 'AssertionError' in result.stderr and 'FAILED (failures=' in result.stderr,
                'mutant not assertion-detected: ' + name)
        require('ERROR:' not in result.stderr and 'SyntaxError' not in result.stderr and 'ImportError' not in result.stderr,
                'invalid-program mutant: ' + name)
    else:
        require(result.returncode == 0, 'baseline failed: ' + name)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    out = parser.parse_args().output.resolve()
    require(not out.exists() and not out.is_relative_to(ROOT), 'new output outside source required')
    out.mkdir(parents=True)
    before = identities()
    source = (ROOT / 'microdisk_exact.py').read_text()
    report = {
        'passed': False,
        'python': sys.version,
        'distinct_tests': EXPECTED,
        'distinct_mutants': len(MUTANTS),
        'modes': [],
        'meaning': 'finite exact divided-difference and determinant-factor checks only; no continuum acceptance',
    }
    try:
        for mode, flags in (('normal', []), ('optimized', ['-O'])):
            cmd = [sys.executable, '-B', *flags, '-S', '-m', 'unittest', '-v', 'test_microdisk_exact']
            run_cmd(cmd, ROOT, out, 'baseline_' + mode)
            actual = subprocess.run([sys.executable, '-B', *flags, '-S', 'microdisk_exact.py'],
                                    cwd=ROOT, capture_output=True, timeout=10)
            require(actual.returncode == 0 and actual.stdout == (ROOT / 'RESULTS.json').read_bytes(),
                    'result byte mismatch: ' + mode)
            for name, (old, new) in MUTANTS.items():
                require(source.count(old) == 1, 'nonunique mutation: ' + name)
                temp = out / 'mutants' / mode / name
                temp.mkdir(parents=True)
                (temp / 'microdisk_exact.py').write_text(source.replace(old, new))
                for filename in ('test_microdisk_exact.py', 'RESULTS.json'):
                    shutil.copyfile(ROOT / filename, temp / filename)
                run_cmd(cmd, temp, out, 'mutation_' + mode + '_' + name, mutant=True)
            report['modes'].append(mode)
        require(before == identities(), 'sources changed during validation')
        report.update(passed=True, sources_unchanged=True, source_files=before)
    finally:
        (out / 'REPORT.json').write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps(report, sort_keys=True))


if __name__ == '__main__':
    main()
