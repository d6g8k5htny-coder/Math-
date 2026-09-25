"""Replay mesoscopic-chart controls in both Python modes; preserve mutation logs."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
EXPECTED_TESTS = 13
MUTANTS = {
    'wrong_grad_x_power': (
        "'grad_x': 2,",
        "'grad_x': 1,",
    ),
    'wrong_grad_y_power': (
        "'grad_y': 1,",
        "'grad_y': 2,",
    ),
    'drop_height_dependence': (
        "return exact(y[1]) / 2",
        "return exact(0)",
    ),
    'omit_k_term': (
        "j_x = 6 * k * y1 * y1 + b * y1 * y2 + (c * y2 * y2) / 2",
        "j_x = b * y1 * y2 + (c * y2 * y2) / 2",
    ),
    'claim_height_independent': (
        "'height_row_independent_at_this_order': False,",
        "'height_row_independent_at_this_order': True,",
    ),
    'claim_annulus_closed': (
        "'full_annulus_closed': False,",
        "'full_annulus_closed': True,",
    ),
    'flip_24jet': (
        "'legacy_24jet_discharged': False,",
        "'legacy_24jet_discharged': True,",
    ),
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def identities():
    return {
        p.name: {
            'bytes': p.stat().st_size,
            'sha256': hashlib.sha256(p.read_bytes()).hexdigest(),
        }
        for p in ROOT.iterdir() if p.is_file()
    }


def execute(command, cwd, out, name, mutant=False):
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True, timeout=30)
    (out / (name + '.stdout')).write_text(result.stdout)
    (out / (name + '.stderr')).write_text(result.stderr)
    if mutant:
        require(
            result.returncode != 0
            and 'AssertionError' in result.stderr
            and 'FAILED (failures=' in result.stderr,
            'mutation was not detected by a test assertion: ' + name,
        )
        require(
            'SyntaxError' not in result.stderr and 'ImportError' not in result.stderr,
            'mutation caused an invalid-program error',
        )
    else:
        require(result.returncode == 0, 'baseline failed: ' + name)
        require(
            f'Ran {EXPECTED_TESTS} tests' in result.stderr and 'skipped=' not in result.stderr,
            'unexpected test coverage',
        )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    out = args.output.resolve()
    require(
        not out.exists() and not out.is_relative_to(ROOT),
        'a new output outside the source directory is required',
    )
    out.mkdir(parents=True)
    before = identities()
    source = (ROOT / 'mesoscopic_chart.py').read_text()
    report = {
        'passed': False,
        'python': sys.version,
        'distinct_tests': EXPECTED_TESTS,
        'distinct_semantic_mutations': len(MUTANTS),
        'modes': [],
        'meaning': (
            'same-author exact chart algebra for d=2 transverse J0; '
            'not analytic review or RN closure'
        ),
    }
    try:
        for mode, flags in [('normal', []), ('optimized', ['-O'])]:
            cmd = [sys.executable, '-B', *flags, '-S', '-m', 'unittest', '-v', 'test_mesoscopic_chart']
            execute(cmd, ROOT, out, 'tests_' + mode)
            output = subprocess.run(
                [sys.executable, '-B', *flags, '-S', 'mesoscopic_chart.py'],
                cwd=ROOT, capture_output=True, timeout=10,
            )
            require(output.returncode == 0, 'entry point failed: ' + mode)
            require(
                output.stdout == (ROOT / 'RESULTS.json').read_bytes(),
                'result byte mismatch',
            )
            (out / ('output_' + mode + '.json')).write_bytes(output.stdout)
            for name, (old, new) in MUTANTS.items():
                require(source.count(old) == 1, 'nonunique mutation: ' + name)
                scratch = out / 'mutants' / mode / name
                scratch.mkdir(parents=True)
                (scratch / 'mesoscopic_chart.py').write_text(source.replace(old, new))
                for filename in ('test_mesoscopic_chart.py', 'RESULTS.json'):
                    shutil.copyfile(ROOT / filename, scratch / filename)
                execute(cmd, scratch, out, 'mutation_' + mode + '_' + name, mutant=True)
            report['modes'].append(mode)
        require(before == identities(), 'source files changed during execution')
        report.update(passed=True, sources_unchanged=True, source_files=before)
    finally:
        (out / 'REPORT.json').write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps(report, sort_keys=True))


if __name__ == '__main__':
    main()
