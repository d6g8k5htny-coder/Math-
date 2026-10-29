"""Portable CBZ engineering mutations. No Lean execution is performed."""
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
    ('omit-artifact-log-hash', 'artifact_integrity.py',
     'if actual != expected_hash:', 'if False:  # MUTANT: corrupted log accepted',
     ['-p', 'test_artifact_integrity.py', '-k', 'corrupt_payload'],
     ['test_corrupt_payload_refused']),
    ('omit-artifact-commit-binding', 'artifact_integrity.py',
     "if receipt.get('checked_commit') != expected_commit:", 'if False:  # MUTANT: wrong commit accepted',
     ['-p', 'test_artifact_integrity.py', '-k', 'wrong_commit'],
     ['test_wrong_commit_refused']),
    ('omit-artifact-manifest-binding', 'artifact_integrity.py',
     "if receipt.get('manifest_sha256') != expected_manifest:", 'if False:  # MUTANT: wrong manifest accepted',
     ['-p', 'test_artifact_integrity.py', '-k', 'wrong_manifest'],
     ['test_wrong_manifest_refused']),
    ('omit-artifact-duplicate-refusal', 'artifact_integrity.py',
     'if name in infos:', 'if False:  # MUTANT: duplicate member accepted',
     ['-p', 'test_artifact_integrity.py', '-k', 'duplicate_members'],
     ['test_duplicate_members_refused']),
    ('omit-artifact-path-refusal', 'artifact_integrity.py',
     '            validate_member_path(name)', '            pass  # MUTANT: unsafe path accepted',
     ['-p', 'test_artifact_integrity.py', '-k', 'unsafe_extra_member'],
     ['test_unsafe_extra_member_refused']),
    ('omit-artifact-empty-inventory-refusal', 'artifact_integrity.py',
     'if not logs:', 'if False:  # MUTANT: empty log inventory accepted',
     ['-p', 'test_artifact_integrity.py', '-k', 'empty_log_inventory'],
     ['test_empty_log_inventory_refused']),
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
    ('execute-cached-inventory-bytecode', 'gate.py',
     "    exec(compile(raw, str(path), 'exec'), module.__dict__)",
     '    spec.loader.exec_module(module)  # MUTANT: may execute cached bytecode',
     ['-p', 'test_inventory_loader.py', '-k', 'exact_source_hash'],
     ['test_exact_source_hash_cannot_authorize_stale_bytecode']),
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
    copy = work / name / 'frontiers' / ROOT.name
    shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns('.lake', '__pycache__'))
    helper = copy.parents[1] / 'tools/lean_packet_admission.py'
    helper.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT.parents[1] / 'tools/lean_packet_admission.py', helper)
    args = [sys.executable, '-B', '-S', *(['-O'] if sys.flags.optimize else []),
            '-m', 'unittest', 'discover', '-s', 'tests', *selection, '-v']
    env = {**os.environ, 'TMPDIR': str(work / 'test-tmp')}
    baseline = subprocess.run(args, cwd=copy, env=env, capture_output=True, text=True)
    (output / (name + '.baseline.stdout')).write_text(baseline.stdout)
    (output / (name + '.baseline.stderr')).write_text(baseline.stderr)
    passed = re.findall(r'^(test_[A-Za-z0-9_]+) \([^\n]*\) \.\.\. ok$', baseline.stderr, re.M)
    if (baseline.returncode != 0 or collected(baseline.stderr) != len(expected)
            or sorted(passed) != sorted(expected) or 'skipped=' in baseline.stderr
            or re.search(r'^OK$', baseline.stderr, re.M) is None):
        raise RuntimeError(name + ': unmodified exact selected controls did not pass')
    path = copy / rel
    text = path.read_text()
    if text.count(old) != 1:
        raise RuntimeError(name + ': mutation location must occur exactly once')
    path.write_text(text.replace(old, new))
    manifest = json.loads((copy / 'manifest.json').read_text())
    if rel == 'compiled_inventory.py':
        # Rebind the independent source-authentication boundary in this isolated
        # mutant only, so the selected regression measures the policy deletion.
        gate_path = copy / 'gate.py'
        gate_text = gate_path.read_text()
        original_digest = hashlib.sha256(text.encode()).hexdigest()
        marker = "CORE_SHA256 = '" + original_digest + "'"
        if gate_text.count(marker) != 1:
            raise RuntimeError(name + ': core authentication fixture binding must occur exactly once')
        gate_path.write_text(gate_text.replace(marker, "CORE_SHA256 = '" +
                             hashlib.sha256(path.read_bytes()).hexdigest() + "'", 1))
        manifest['files']['gate.py'] = hashlib.sha256(gate_path.read_bytes()).hexdigest()
    manifest['files'][rel] = hashlib.sha256(path.read_bytes()).hexdigest()
    (copy / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    result = subprocess.run(args, cwd=copy, env=env, capture_output=True, text=True)
    (output / (name + '.stdout')).write_text(result.stdout)
    (output / (name + '.stderr')).write_text(result.stderr)
    failed = re.findall(r'^FAIL: (test_[A-Za-z0-9_]+)', result.stderr, re.M)
    errors = any(marker in result.stderr for marker in
                 ('ERROR:', 'ImportError', 'ModuleNotFoundError', 'FAILED (errors='))
    count = collected(result.stderr)
    reason_by_mutant = {
        'omit-artifact-log-hash': 'IntegrityError not raised',
        'omit-artifact-commit-binding': 'IntegrityError not raised',
        'omit-artifact-manifest-binding': 'IntegrityError not raised',
        'omit-artifact-duplicate-refusal': 'IntegrityError not raised',
        'omit-artifact-path-refusal': 'IntegrityError not raised',
        'omit-artifact-empty-inventory-refusal': 'IntegrityError not raised',
        'omit-forbidden-closure': 'ValueError not raised',
        'omit-extra-theorem-admission': 'ValueError not raised',
        'omit-bound-constant-admission': 'ValueError not raised',
        'omit-stale-receipt-removal': 'stale receipt survived a refused execution',
        'execute-cached-inventory-bytecode': 'HOSTILE_CACHED_IMPLEMENTATION',
        'omit-runtime-census-and-controls': 'ValueError not raised',
    }
    reason = reason_by_mutant.get(name)
    headers = list(re.finditer(r'^FAIL: (test_[A-Za-z0-9_]+) [^\n]*$', result.stderr, re.M))
    summary = re.search(r'^Ran [0-9]+ tests? in ', result.stderr, re.M)
    reason_ok = reason is not None and summary is not None and len(headers) == len(expected)
    if reason_ok:
        for index, match in enumerate(headers):
            end = headers[index + 1].start() if index + 1 < len(headers) else summary.start()
            section = result.stderr[match.end():end]
            if reason not in section or ('in ' + match.group(1)) not in section:
                reason_ok = False
                break
    intended = (result.returncode == 1 and count == len(expected) and count > 0
                and sorted(failed) == sorted(expected) and not errors and reason_ok
                and re.search(r'^FAILED \(failures=' + str(len(expected)) + r'\)$',
                              result.stderr, re.M) is not None)
    return {'name': name, 'file': rel, 'command': args, 'intended_failure_reason': reason, 'baseline_exit_code': baseline.returncode,
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

