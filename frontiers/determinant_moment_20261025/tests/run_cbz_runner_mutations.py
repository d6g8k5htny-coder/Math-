"""Adverse mutations of the outer wrapper itself; no Lean or gate receipt."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]
PAIR = '        pair = _shared.classify_pair(baseline, mutant)'
CASES = (
    ('execute-stale-shared-runner-bytecode', [(
      "\n    exec(compile(raw, str(path), 'exec'), module.__dict__)\n",
      "\n    import importlib.util\n    spec = importlib.util.spec_from_file_location(module.__name__, path)\n    spec.loader.exec_module(module)\n")],
     'test_shared_runner_uses_one_read_and_ignores_timestamp_valid_bytecode'),
    ('reread-shared-source-for-execution', [(
      "\n    exec(compile(raw, str(path), 'exec'), module.__dict__)\n",
      "\n    exec(compile(path.read_bytes(), str(path), 'exec'), module.__dict__)\n")],
     'test_shared_runner_uses_one_read_and_ignores_timestamp_valid_bytecode'),
    ('count-lifecycle-failures-as-kills', [(PAIR,
      "        pair = dict(same_harness=True, baseline_passed=True, killed=mutant.get('returncode') == 1, status='KILLED')")],
     'test_lifecycle_assertions_cannot_masquerade_as_intended_body_kills'),
    ('repair-mismatched-harness-identities', [(PAIR,
      "        pair = _shared.classify_pair(dict(baseline, **{key: mutant[key] for key in ('selection', 'mode', 'harness_sha256')}), mutant)")],
     'test_selection_mode_and_harness_mismatches_reject_actual_wrapper_pairs'),
    ('accept-invalid-baseline', [(PAIR,
      "        pair = _shared.classify_pair(dict(baseline, classification='PASS'), mutant)")],
     'test_invalid_baseline_cannot_qualify_an_actual_body_failure'),
    ('relabel-invalid-mutant-as-assertion', [(PAIR,
      "        pair = _shared.classify_pair(baseline, dict(mutant, classification='ASSERTION_FAILURE' if mutant.get('failure_ids') else mutant.get('classification')))")],
     'test_invalid_return_zero_wrong_and_skipped_reports_are_not_reclassified'),
    ('omit-exact-selection-validation', [(
      '    validate_selections(selections)\n',
      '    pass  # MUTANT: zero, duplicate and broad selections accepted\n')],
     'test_empty_duplicate_and_broad_selections_are_refused'),
    ('reuse-existing-evidence-directory', [(
      '    return _shared.create_run_directory(external_directory(parent))',
      '    destination = external_directory(parent)\n    destination.mkdir(parents=True, exist_ok=True)\n    return destination')],
     'test_output_children_are_retained_and_source_and_symlink_paths_refuse'),
    ('omit-output-symlink-refusal', [(
      '    reject_symlinks(path)\n    resolved = path.resolve()',
      '    resolved = path.resolve()  # MUTANT: output symlink ancestors accepted')],
     'test_output_children_are_retained_and_source_and_symlink_paths_refuse'),
    ('accept-empty-matrix-as-vacuous-success', [(
      "        if not cases or len({case[0] for case in cases}) != len(cases):",
      "        if len({case[0] for case in cases}) != len(cases):"), (
      '            all_killed=bool(records) and len(records) == len(cases) and actual_pairs == expected_pairs and',
      '            all_killed=len(records) == len(cases) and actual_pairs == expected_pairs and')],
     'test_empty_matrix_is_a_failure_instead_of_vacuous_success'),
    ('claim-source-preservation-without-comparison', [(
      '        preserved = before == source_inventory()',
      '        preserved = True  # MUTANT: actual source change ignored')],
     'test_matrix_refuses_a_source_change_even_when_every_mutant_was_killed'),
)


def shared_runner():
    path = ROOT / 'tests/run_git_identity_mutations.py'
    raw = path.read_bytes()
    module = ModuleType('outer_runner_mutation_protocol')
    module.__file__ = str(path)
    exec(compile(raw, str(path), 'exec'), module.__dict__)
    return module, hashlib.sha256(raw).hexdigest()


def inventory():
    records = {}
    for path in ROOT.rglob('*'):
        rel = path.relative_to(ROOT)
        if '.lake' in rel.parts or '__pycache__' in rel.parts:
            continue
        if any(p.is_symlink() for p in (path, *path.parents)):
            raise ValueError('symlink source refused')
        if path.is_file():
            records[rel.as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    for rel in ('tools/lean_packet_admission.py', '.github/workflows/determinant-moment-lean.yml'):
        path = ROOT.parents[1] / rel
        if any(p.is_symlink() for p in (path, *path.parents)):
            raise ValueError('symlink external fixture refused')
        records[rel] = hashlib.sha256(path.read_bytes()).hexdigest()
    return records


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='retained evidence parent outside source; unique child per run')
    args = parser.parse_args(argv)
    before = inventory()
    shared, shared_digest = shared_runner()
    parent = (args.output or Path(tempfile.gettempdir()) / 'cbz-wrapper-mutation-evidence').absolute()
    if (any(p.is_symlink() for p in (parent, *parent.parents)) or
        parent.resolve().is_relative_to(ROOT.parents[1].resolve())):
        raise ValueError('evidence must be outside source with no symlink ancestors')
    destination = shared.create_run_directory(parent)
    harness = destination / 'unittest_harness.py'
    harness.write_text(shared.HARNESS_SOURCE)
    original = (ROOT / 'tests/run_cbz_mutations.py').read_text()
    results = []
    for name, replacements, method in CASES:
        changed = original
        for old, new in replacements:
            if changed.count(old) != 1:
                raise ValueError('outer-wrapper mutation must identify one source site: ' + name)
            changed = changed.replace(old, new, 1)
        compile(changed, name, 'exec')
        selection = 'test_cbz_mutation_runner.OuterMutationRunnerTests.' + method
        for mode in ('normal', 'optimized'):
            case = destination / name / mode
            executions = {}
            for label, text in (('baseline', original), ('mutant', changed)):
                source = case / label / 'repo/frontiers' / ROOT.name
                shutil.copytree(ROOT, source, ignore=shutil.ignore_patterns('.lake', '__pycache__'))
                for rel in ('tools/lean_packet_admission.py', '.github/workflows/determinant-moment-lean.yml'):
                    target = source.parents[1] / rel
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(ROOT.parents[1] / rel, target)
                (source / 'tests/run_cbz_mutations.py').write_text(text)
                executions[label] = shared.run_selected(source, selection, mode, case / label / 'logs', harness)
            row = dict(mutation=name, mode=mode, selection=selection, replacement_sites=len(replacements),
                mutated_source_sha256=hashlib.sha256(changed.encode()).hexdigest(),
                **shared.classify_pair(executions['baseline'], executions['mutant']), **executions)
            (case / 'result.json').write_text(json.dumps(row, indent=2) + '\n')
            results.append(row)
    preserved = before == inventory()
    record = dict(scope='OUTER_MUTATION_WRAPPER_SELF_MUTATIONS_ONLY', actual_mutants=len(CASES),
        execution_pairs=len(results), modes=['normal', 'optimized'], source_preserved=preserved,
        baseline_source_sha256=hashlib.sha256(original.encode()).hexdigest(), shared_runner_sha256=shared_digest,
        all_killed=bool(results) and len(results) == 2 * len(CASES) and preserved and all(row['killed'] for row in results),
        results=results, actual_lean='NOT_RUN', kernel_or_cbz_status='NOT_AWARDED')
    path = destination / 'results.json'
    path.write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps(dict(results=str(path), actual_mutants=len(CASES), execution_pairs=len(results),
                         all_killed=record['all_killed']), indent=2))
    return 0 if record['all_killed'] else 1


if __name__ == '__main__':
    sys.exit(main())
