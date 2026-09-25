"""Replay hard-gate controls in both Python modes; preserve mutation logs."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
EXPECTED_TESTS = 32
MUTANTS = {
    'bypass_own_node_eligibility': (
        "if node_classification not in CONTROLLING_ELIGIBLE:",
        "if False:",
    ),
    'allow_required_superseded_label': (
        "CONTROLLING_ELIGIBLE = frozenset({'PROVED_REVIEWED'})",
        "CONTROLLING_ELIGIBLE = frozenset({'PROVED_REVIEWED', 'SUPERSEDED_NONBLOCKING'})",
    ),
    'allow_required_refutation': (
        "if cls == 'REFUTED':\n            refuted.append(dep)",
        "if False:\n            refuted.append(dep)",
    ),
    'drop_old_edges_from_reverse_impact': (
        "union_edges = {(e['from'], e['to']) for g in (old_graph, new_graph) for e in g['edges']}",
        "union_edges = {(e['from'], e['to']) for e in new_graph['edges']}",
    ),
    'allow_green_ci': (
        "only_non_discharge = bool(tokens) and all(t in non_discharge for t in tokens)",
        "only_non_discharge = False",
    ),
    'ignore_blocked_absent': (
        "if cls == 'BLOCKED_ABSENT':\n            blocked.append(dep)",
        "if False:\n            blocked.append(dep)",
    ),
    'treat_author_side_terminal': (
        "def is_terminal(classification: str) -> bool:\n    return classification in TERMINAL",
        "def is_terminal(classification: str) -> bool:\n    return classification in TERMINAL or classification == 'AUTHOR_SIDE_CANDIDATE'",
    ),
    'skip_reverse_impact': (
        "node['classification'] = 'REVALIDATION_REQUIRED'\n                node['controlling'] = False\n                impacted.append(dep)",
        "impacted.append(dep)",
    ),
    'flip_lemma_closed': (
        "'lemma_closed': False,\n        'scientific_effect': 'NONE',\n        'illegal_promotion_refused':",
        "'lemma_closed': True,\n        'scientific_effect': 'NONE',\n        'illegal_promotion_refused':",
    ),
    'corrupt_d0_patch_marker': (
        "'d53b286029d034576245406152c188fe2470ccb089e51f73e9087e34bf5a0e10',",
        "'deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef',",
    ),
    'allow_illegal_controlling_report': (
        "'gate_ok': len(controlling_illegal) == 0,",
        "'gate_ok': True,",
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
    source = (ROOT / 'hard_gate.py').read_text()
    report = {
        'passed': False,
        'python': sys.version,
        'distinct_tests': EXPECTED_TESTS,
        'distinct_semantic_mutations': len(MUTANTS),
        'modes': [],
        'meaning': (
            'same-author integrity-gate checks for main #90/#86; '
            'not analytic review or theorem acceptance'
        ),
    }
    try:
        for mode, flags in [('normal', []), ('optimized', ['-O'])]:
            cmd = [sys.executable, '-B', *flags, '-S', '-m', 'unittest', '-v', 'test_hard_gate']
            execute(cmd, ROOT, out, 'tests_' + mode)
            output = subprocess.run(
                [sys.executable, '-B', *flags, '-S', 'hard_gate.py'],
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
                (scratch / 'hard_gate.py').write_text(source.replace(old, new))
                for filename in (
                    'test_hard_gate.py', 'RESULTS.json', 'GRAPH.json',
                    'SELECTOR_REGION.json', 'D0_CI_UNBLOCK.md',
                ):
                    shutil.copyfile(ROOT / filename, scratch / filename)
                shutil.copytree(ROOT / 'patches', scratch / 'patches')
                execute(cmd, scratch, out, 'mutation_' + mode + '_' + name, mutant=True)
            report['modes'].append(mode)
        require(before == identities(), 'source files changed during execution')
        report.update(passed=True, sources_unchanged=True, source_files=before)
    finally:
        (out / 'REPORT.json').write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps(report, sort_keys=True))


if __name__ == '__main__':
    main()