"""Portable outer-gate mutations using the shared phase-aware unittest protocol.

Each invocation uses its current Python mode. No Lean execution is performed.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = '.github/workflows/determinant-moment-lean.yml'


def load_shared_runner():
    """Execute the one source read, independently of timestamp-valid bytecode."""
    path = Path(__file__).with_name('run_git_identity_mutations.py')
    if any(p.is_symlink() for p in (path, *path.parents)):
        raise ValueError('symlink shared mutation runner refused')
    raw = path.read_bytes()
    module = ModuleType('cbz_shared_git_identity_mutation_runner')
    module.__file__ = str(path)
    exec(compile(raw, str(path), 'exec'), module.__dict__)
    return module, hashlib.sha256(raw).hexdigest()


_shared, SHARED_RUNNER_SHA256 = load_shared_runner()
HARNESS_SOURCE = _shared.HARNESS_SOURCE
CASES = (
    ('omit-forbidden-closure', 'compiled_inventory.py',
     'for name in sorted(closure - ALLOWED_NAMES, key=encode):',
     'for name in ():  # MUTANT: forbidden package closure suppressed',
     ('test_compiled_admission.CompiledAdmissionTests.test_unused_definition_forbidden_closure_is_rejected',)),
    ('omit-extra-theorem-admission', 'compiled_inventory.py',
     'if name not in wanted:', 'if False:  # MUTANT: admit unlisted user theorems',
     ('test_compiled_admission.CompiledAdmissionTests.test_unlisted_axiom_free_theorem_is_rejected',)),
    ('omit-bound-constant-admission', 'compiled_inventory.py',
     'if entry not in bound:', 'if False:  # MUTANT: admit unbound constants',
     ('test_compiled_admission.CompiledAdmissionTests.test_unbound_compiler_shaped_theorem_is_rejected',)),
    ('omit-stale-receipt-removal', 'gate.py',
     "    (out / 'receipt.json').unlink(missing_ok=True)",
     '    pass  # MUTANT: stale receipt retained',
     ('test_compiled_admission.CompiledAdmissionTests.test_missing_binding_removes_a_stale_receipt_on_execute',)),
    ('execute-cached-inventory-bytecode', 'gate.py',
     "    exec(compile(raw, str(path), 'exec'), module.__dict__)",
     '    spec.loader.exec_module(module)  # MUTANT: may execute cached bytecode',
     ('test_inventory_loader.BoundInventoryLoaderTests.test_exact_source_hash_cannot_authorize_stale_bytecode',)),
    ('omit-execute-source-qualification', 'gate.py',
     '    source_preflight = source_qualification(m, digest)',
     '    source_preflight = {}  # MUTANT: mutable adapter precedes Git refusal',
     ('test_gate_git_qualification.GitQualificationIntegrationTests.test_execute_git_refusal_precedes_mutable_adapter_and_every_process',)),
    ('omit-cli-pre-helper-qualification', 'gate.py',
     '        m, digest = source_check(git_qualification=args.execute)',
     '        m, digest = source_check(git_qualification=False)  # MUTANT: CLI skips pre-helper Git qualification',
     ('test_gate_git_qualification.GitQualificationIntegrationTests.test_execute_cli_requests_pre_helper_git_qualification',)),
    ('omit-post-manifest-guard', 'gate.py',
     '    _, after = source_check(expected_manifest_sha256=digest)',
     '    _, after = source_check()  # MUTANT: expected post-execution manifest guard omitted',
     ('test_determinant_execute.V2ExecutionTests.test_v2_execution_reaches_both_compiled_and_five_proof_controls',)),
    ('omit-final-source-qualification', 'gate.py',
     '    source_final = source_qualification(m, digest, previous=source_preflight)',
     '    source_final = source_preflight  # MUTANT: final source endpoint skipped',
     ('test_determinant_execute.V2ExecutionTests.test_v2_execution_reaches_both_compiled_and_five_proof_controls',)),
    ('use-unqualified-late-receipt-identity', 'gate.py',
     "                   checked_commit=source_preflight['checked_commit'],",
     "                   checked_commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),  # MUTANT: unqualified late identity",
     ('test_determinant_execute.V2ExecutionTests.test_v2_execution_reaches_both_compiled_and_five_proof_controls',)),
    ('revert-console-capture-to-log', WORKFLOW,
     'tee "$RUNNER_TEMP/determinant-authoritative-gate.log"',
     'tee frontiers/determinant_moment_20261025/.lake/formal-evidence/authoritative-gate.log',
     ('test_determinant_workflow_console_capture.DeterminantConsoleCaptureTests.test_actual_gate_pipeline_preserves_final_receipt_log_hashes',)),
)


def mutation_cases():
    text = (ROOT / 'gate.py').read_text()
    start_marker = "    inventory_source = out / 'Inventory.lean'"
    end_marker = '    # Real counterexample/mutation controls'
    if text.count(start_marker) != 1 or text.count(end_marker) != 1:
        raise ValueError('runtime census mutation boundaries must occur exactly once')
    start, end = text.index(start_marker), text.index(end_marker)
    runtime_case = ('omit-runtime-census-and-controls', 'gate.py', text[start:end],
                    '    inventory = {}  # MUTANT: target-only path reaches receipt\n    compiled_admission = {}\n',
                    ('test_gate.RuntimeGuardTests.test_green_public_targets_do_not_hide_bad_compiled_inventory',
                     'test_gate.RuntimeGuardTests.test_missing_compiled_output_refuses_receipt'))
    return (*CASES, runtime_case)


def reject_symlinks(path):
    if any(p.is_symlink() for p in (path, *path.parents)):
        raise ValueError('symlink path or ancestor refused: ' + str(path))


def source_inventory():
    reject_symlinks(ROOT)
    records = {}
    for path in ROOT.rglob('*'):
        rel = path.relative_to(ROOT)
        if '.lake' in rel.parts or '__pycache__' in rel.parts:
            continue
        reject_symlinks(path)
        if path.is_file():
            records['component/' + rel.as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    for rel in ('tools/lean_packet_admission.py', WORKFLOW):
        path = ROOT.parents[1] / rel
        reject_symlinks(path)
        records[rel] = hashlib.sha256(path.read_bytes()).hexdigest()
    return records


def external_directory(path):
    path = Path(path).absolute()
    reject_symlinks(path)
    resolved = path.resolve()
    if resolved.is_relative_to(ROOT.parents[1].resolve()):
        raise ValueError('output and temporary directories must be outside the source repository')
    return resolved


def create_run_directory(parent):
    return _shared.create_run_directory(external_directory(parent))


def copy_component(destination):
    source_inventory()  # Refuse symlinks before copytree can dereference them.
    shutil.copytree(ROOT, destination, ignore=shutil.ignore_patterns('.lake', '__pycache__'))
    for rel in ('tools/lean_packet_admission.py', WORKFLOW):
        target = destination.parents[1] / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT.parents[1] / rel, target)


def validate_selections(selections):
    if (type(selections) is not tuple or not selections or
        any(type(selection) is not str or re.fullmatch(
            r'[A-Za-z_]\w*\.[A-Za-z_]\w*\.test_[A-Za-z_]\w*', selection) is None
            for selection in selections) or len(set(selections)) != len(selections)):
        raise ValueError('each mutation needs distinct exact single TestCase method selections')


def execute_case(case, work, output, *, mode=None, harness=None):
    name, rel, old, new, selections = case
    validate_selections(selections)
    mode = mode or ('optimized' if sys.flags.optimize else 'normal')
    if harness is None:
        harness = Path(output) / 'unittest_harness.py'
        with harness.open('x') as stream:
            stream.write(HARNESS_SOURCE)
    copy = Path(work) / name / 'repo/frontiers' / ROOT.name
    copy_component(copy)
    case_output = Path(output) / name / mode
    baselines = [_shared.run_selected(copy, selection, mode,
                 case_output / str(index) / 'baseline', harness)
                 for index, selection in enumerate(selections)]
    path = copy.parents[1] / rel if rel == WORKFLOW else copy / rel
    original = path.read_text()
    if original.count(old) != 1:
        raise ValueError(name + ': mutation location must occur exactly once')
    changed = original.replace(old, new, 1)
    if path.suffix == '.py':
        compile(changed, str(path), 'exec')
    path.write_text(changed)
    manifest = json.loads((copy / 'manifest.json').read_text())
    if rel == 'compiled_inventory.py':
        # Rebind the independent source-authentication boundary in this isolated
        # mutant only, so selected regressions measure the original policy deletions.
        gate_path = copy / 'gate.py'
        gate_text = gate_path.read_text()
        marker = "CORE_SHA256 = '" + hashlib.sha256(original.encode()).hexdigest() + "'"
        if gate_text.count(marker) != 1:
            raise ValueError(name + ': core authentication fixture binding must occur exactly once')
        gate_path.write_text(gate_text.replace(marker, "CORE_SHA256 = '" +
                             hashlib.sha256(path.read_bytes()).hexdigest() + "'", 1))
        manifest['files']['gate.py'] = hashlib.sha256(gate_path.read_bytes()).hexdigest()
    if rel != WORKFLOW:
        manifest['files'][rel] = hashlib.sha256(path.read_bytes()).hexdigest()
        (copy / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    pairs = []
    for index, (selection, baseline) in enumerate(zip(selections, baselines)):
        mutant = _shared.run_selected(copy, selection, mode, case_output / str(index) / 'mutant', harness)
        pair = _shared.classify_pair(baseline, mutant)
        row = dict(selection=selection, **pair, baseline=baseline, mutant=mutant)
        (case_output / str(index) / 'pair.json').write_text(json.dumps(row, indent=2) + '\n')
        pairs.append(row)
    baseline_exits = [row['baseline'].get('returncode') for row in pairs]
    mutant_exits = [row['mutant'].get('returncode') for row in pairs]
    record = dict(name=name, file=rel, mode=mode, mutation_location_count=1,
        mutated_source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
        selected_tests=list(selections), selection_results=pairs,
        collected_tests=sum(row['mutant'].get('tests_run', 0) for row in pairs),
        baseline_exit_codes=baseline_exits, exit_codes=mutant_exits,
        baseline_exit_code=baseline_exits[0] if all(code == baseline_exits[0] for code in baseline_exits) else None,
        exit_code=mutant_exits[0] if all(code == mutant_exits[0] for code in mutant_exits) else None,
        import_or_test_errors=any(row['mutant'].get('classification') == 'INVALID' for row in pairs),
        killed_by_intended_assertions=bool(pairs) and len(pairs) == len(selections) and all(row['killed'] for row in pairs),
        actual_lean='NOT_RUN')
    (case_output / 'result.json').write_text(json.dumps(record, indent=2) + '\n')
    return record


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='retained evidence parent outside the source repository; each run creates a unique child')
    args = parser.parse_args(argv)
    try:
        before = source_inventory()
        temporary_root = external_directory(tempfile.gettempdir())
        cases = mutation_cases()
        if not cases or len({case[0] for case in cases}) != len(cases):
            raise ValueError('mutation matrix must be nonempty with unique names')
        for case in cases:
            validate_selections(case[4])
        output = create_run_directory(args.output or temporary_root / 'cbz-mutation-evidence')
        harness = output / 'unittest_harness.py'
        with harness.open('x') as stream:
            stream.write(HARNESS_SOURCE)
        mode = 'optimized' if sys.flags.optimize else 'normal'
        records = [execute_case(case, output / 'work', output / 'cases', mode=mode, harness=harness)
                   for case in cases]
        preserved = before == source_inventory()
        expected_pairs = sum(len(case[4]) for case in cases)
        actual_pairs = sum(len(row['selection_results']) for row in records)
        report = dict(scope='OUTER_GATE_ENGINEERING_MUTATIONS_ONLY', mode=mode,
            actual_mutants=len(cases), execution_pairs=actual_pairs, expected_pairs=expected_pairs,
            mutations=records, source_preserved=preserved,
            baseline_source_inventory_sha256=hashlib.sha256(json.dumps(before, sort_keys=True).encode()).hexdigest(),
            shared_runner_sha256=SHARED_RUNNER_SHA256,
            all_killed=bool(records) and len(records) == len(cases) and actual_pairs == expected_pairs and
                       preserved and all(row['killed_by_intended_assertions'] for row in records),
            actual_lean='NOT_RUN', kernel_or_cbz_status='NOT_AWARDED')
        result_path = output / 'mutation_results.json'
        result_path.write_text(json.dumps(report, indent=2) + '\n')
        print(json.dumps(dict(results=str(result_path), mode=mode, actual_mutants=len(cases),
                             execution_pairs=actual_pairs, all_killed=report['all_killed']), indent=2))
        return 0 if report['all_killed'] else 1
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
        print('CBZ_MUTATION_GATE_FAIL: ' + str(error), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
