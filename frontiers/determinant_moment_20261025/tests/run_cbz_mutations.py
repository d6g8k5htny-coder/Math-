"""Portable five-case CBZ engineering mutation gate. No Lean execution is performed."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
CASES = (
    ('omit-forbidden-closure', 'compiled_inventory.py',
     'for name in sorted(closure - ALLOWED_NAMES, key=encode):',
     'for name in ():  # MUTANT: forbidden package closure suppressed',
     ['-p', 'test_compiled_admission.py', '-k', 'unused_definition'],
     ['test_unused_definition_forbidden_closure_is_rejected']),
    ('omit-extra-theorem-admission', 'compiled_inventory.py',
     'if name not in wanted:', 'if False:  # MUTANT: admit unlisted user theorems',
     ['-p', 'test_compiled_admission.py', '-k', 'unlisted_axiom_free'],
     ['test_unlisted_axiom_free_theorem_is_rejected']),
    ('omit-bound-constant-admission', 'compiled_inventory.py',
     'if entry not in bound:', 'if False:  # MUTANT: admit unbound constants',
     ['-p', 'test_compiled_admission.py', '-k', 'compiler_shaped'],
     ['test_unbound_compiler_shaped_theorem_is_rejected']),
    ('omit-stale-receipt-removal', 'gate.py',
     "    (out / 'receipt.json').unlink(missing_ok=True)",
     '    pass  # MUTANT: stale receipt retained',
     ['-p', 'test_compiled_admission.py', '-k', 'stale'],
     ['test_missing_binding_removes_a_stale_receipt_on_execute']),
)


def source_inventory():
    records = {}
    for path in ROOT.rglob('*'):
        rel = path.relative_to(ROOT)
        if '.lake' in rel.parts or '__pycache__' in rel.parts:
            continue
        if path.is_symlink():
            raise ValueError('source symlink is unsupported: ' + str(rel))
        if path.is_file():
            records[rel.as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return records


def collected(stderr):
    matches = re.findall(r'^Ran ([0-9]+) tests? in ', stderr, re.M)
    return int(matches[0]) if len(matches) == 1 else 0


def execute_case(case, work, output):
    name, rel, old, new, selection, expected = case
    copy = work / name
    shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns('.lake', '__pycache__'))
    args = [sys.executable, '-B', '-S', '-m', 'unittest', 'discover', '-s', 'tests', *selection, '-v']
    env = {**os.environ, 'TMPDIR': str(work / 'test-tmp')}
    baseline = subprocess.run(args, cwd=copy, env=env, capture_output=True, text=True)
    (output / (name + '.baseline.stdout')).write_text(baseline.stdout)
    (output / (name + '.baseline.stderr')).write_text(baseline.stderr)
    if baseline.returncode != 0 or collected(baseline.stderr) != len(expected) or 'skipped=' in baseline.stderr:
        raise RuntimeError(name + ': unmodified selected controls are not green with the expected nonzero test count')
    path = copy / rel
    text = path.read_text()
    if text.count(old) != 1:
        raise RuntimeError(name + ': mutation location must occur exactly once')
    path.write_text(text.replace(old, new))
    manifest = json.loads((copy / 'manifest.json').read_text())
    manifest['files'][rel] = hashlib.sha256(path.read_bytes()).hexdigest()
    (copy / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    result = subprocess.run(args, cwd=copy, env=env, capture_output=True, text=True)
    (output / (name + '.stdout')).write_text(result.stdout)
    (output / (name + '.stderr')).write_text(result.stderr)
    failed = re.findall(r'^FAIL: (test_[A-Za-z0-9_]+)', result.stderr, re.M)
    errors = any(marker in result.stderr for marker in
                 ('ERROR:', 'ImportError', 'ModuleNotFoundError', 'FAILED (errors='))
    count = collected(result.stderr)
    intended = (result.returncode != 0 and count == len(expected) and count > 0
                and sorted(failed) == sorted(expected) and not errors
                and re.search(r'^FAILED \(failures=' + str(len(expected)) + r'\)$',
                              result.stderr, re.M) is not None)
    return {'name': name, 'file': rel, 'command': args, 'baseline_exit_code': baseline.returncode,
            'collected_tests': count, 'exit_code': result.returncode,
            'expected_failing_tests': expected, 'actual_failing_tests': failed,
            'import_or_test_errors': errors, 'killed_by_intended_assertions': intended,
            'mutation_location_count': 1, 'actual_lean': 'NOT_RUN'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='optional report directory outside the component source tree')
    args = parser.parse_args()
    try:
        before = source_inventory()
        temporary_root = Path(tempfile.gettempdir()).resolve()
        if temporary_root.is_relative_to(ROOT):
            raise ValueError('TMPDIR must be outside the component source tree')
        if args.output and args.output.resolve().is_relative_to(ROOT):
            raise ValueError('--output must be outside the component source tree')
        with tempfile.TemporaryDirectory(prefix='cbz-mutations-', dir=temporary_root) as temporary:
            work = Path(temporary)
            (work / 'test-tmp').mkdir()
            output = args.output.resolve() if args.output else work / 'reports'
            output.mkdir(parents=True, exist_ok=True)
            text = (ROOT / 'gate.py').read_text()
            start_marker = "    inventory_source = out / 'Inventory.lean'"
            end_marker = '    # Real counterexample/mutation controls'
            if text.count(start_marker) != 1 or text.count(end_marker) != 1:
                raise RuntimeError('runtime census mutation boundaries must occur exactly once')
            start, end = text.index(start_marker), text.index(end_marker)
            runtime_case = ('omit-runtime-census-and-controls', 'gate.py', text[start:end],
                            '    inventory = {}  # MUTANT: target-only path reaches receipt\n    compiled_admission = {}\n',
                            ['-p', 'test_gate.py', '-k', 'compiled'],
                            ['test_green_public_targets_do_not_hide_bad_compiled_inventory',
                             'test_missing_compiled_output_refuses_receipt'])
            records = [execute_case(case, work, output) for case in (*CASES, runtime_case)]
            report = {'mutations': records, 'source_preserved': before == source_inventory(),
                      'actual_lean': 'NOT_RUN'}
            (output / 'mutation_results.json').write_text(json.dumps(report, indent=2) + '\n')
            print(json.dumps(report, indent=2))
            return 0 if report['source_preserved'] and all(r['killed_by_intended_assertions'] for r in records) else 1
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
        print('CBZ_MUTATION_GATE_FAIL: ' + str(error), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())

