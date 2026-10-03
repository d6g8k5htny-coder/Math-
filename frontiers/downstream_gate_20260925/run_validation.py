"""Bounded gate replay, semantic mutants, exact outputs and unchanged source checks."""
from pathlib import Path
import argparse
import hashlib
import json
import math
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
EXPECTED_TESTS = 71
MUTANTS = {
    'bypass_own_node_eligibility': ("if node_classification not in CONTROLLING_ELIGIBLE:", "if False:"),
    'allow_required_superseded_label': (
        "REQUIRED_SATISFIED = frozenset({'PROVED_REVIEWED'})",
        "REQUIRED_SATISFIED = frozenset({'PROVED_REVIEWED', 'SUPERSEDED_NONBLOCKING'})"),
    'allow_required_refutation': (
        "if cls == 'REFUTED':\n            refuted.append(dep)", "if False:\n            refuted.append(dep)"),
    'drop_old_edges_from_reverse_impact': (
        "union_edges = {(e['from'], e['to']) for g in (old_graph, new_graph) for e in g['edges']}",
        "union_edges = {(e['from'], e['to']) for e in new_graph['edges']}"),
    'allow_green_ci': ("only_non_discharge = bool(tokens) and all(t in non_discharge for t in tokens)", "only_non_discharge = False"),
    'ignore_blocked_absent': ("if cls == 'BLOCKED_ABSENT':\n            blocked.append(dep)", "if False:\n            blocked.append(dep)"),
    'skip_reverse_impact': (
        "node['classification'] = 'REVALIDATION_REQUIRED'\n                node['controlling'] = False\n                impacted.append(dep)",
        "impacted.append(dep)"),
    'flip_lemma_closed': (
        "'lemma_closed': False,\n        'scientific_effect': 'NONE',\n        'illegal_promotion_refused':",
        "'lemma_closed': True,\n        'scientific_effect': 'NONE',\n        'illegal_promotion_refused':"),
    'corrupt_d0_patch_marker': (
        "'d53b286029d034576245406152c188fe2470ccb089e51f73e9087e34bf5a0e10',",
        "'deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef',"),
    'allow_illegal_controlling_report': ("'gate_ok': len(controlling_illegal) == 0,", "'gate_ok': True,"),
    'accept_numeric_required': ("if type(edge['required']) is not bool:", "if False:"),
    'accept_numeric_controlling': ("if type(node.get('controlling')) is not bool:", "if False:"),
    'ignore_complete_node_change': ("if _json_identity(old_nodes[nid]) != _json_identity(new_nodes[nid]):", "if False:"),
    'ignore_edge_only_change': ("if _outgoing_signature(old_graph, nid) != _outgoing_signature(new_graph, nid):", "if False:"),
    'ignore_edge_metadata_change': (
        "return sorted(_json_identity(e) for e in graph['edges'] if e['from'] == nid)",
        "return sorted(_json_identity({k: e[k] for k in ('from', 'to', 'required', 'relation')}) for e in graph['edges'] if e['from'] == nid)"),
    'omit_changed_node_self_hold': ("impacted: set[str] = {nid for nid in changed if nid in new_nodes}", "impacted: set[str] = set()"),
    'ignore_graph_context': ("if context_changed:\n        changed.update(all_ids)", "if False:\n        changed.update(all_ids)"),
    'ignore_source_only_change': (
        "if old_sources is not None and _json_identity(old_sources[nid]) != _json_identity(new_sources[nid]):", "if False:"),
    'accept_duplicate_json_keys': ("if key in result:\n                raise ValueError('duplicate JSON key: ' + key)", "if False:\n                raise ValueError('duplicate JSON key: ' + key)"),
    'skip_public_promotion_validation': (
        '"""Return whether node_id may become CONTROLLING under #90 rules."""\n    validate_graph_fail_closed(graph)',
        '"""Return whether node_id may become CONTROLLING under #90 rules."""'),
    'accept_unknown_classification': ("if not isinstance(cls, str) or cls not in TERMINAL | NONTERMINAL:", "if False:"),
    'accept_contradictory_edges': ("key = (edge['from'], edge['to'], edge['relation'])", "key = (edge['from'], edge['to'], edge['relation'], edge['required'])"),
    'omit_legacy_self_hold': ("for dep in [changed_node, *transitive_dependents(clone, changed_node)]:", "for dep in transitive_dependents(clone, changed_node):"),
    'accept_boolean_schema': ("type(graph.get('schema_version')) is not int", "not isinstance(graph.get('schema_version'), int)"),
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def identities():
    return {p.relative_to(ROOT).as_posix(): {'bytes': len(p.read_bytes()), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
            for p in sorted(ROOT.rglob('*')) if p.is_file() and '__pycache__' not in p.parts}


def execute(command, cwd, out, name, mutant=False, *, mode, mutation=None):
    timeout_seconds = 30
    started = None
    clock_failure = None
    try:
        started = time.monotonic()
    except Exception as error:
        clock_failure = f'initial clock: {type(error).__name__}: {error}'
    try:
        result = subprocess.run(command, cwd=cwd, capture_output=True, text=True, timeout=timeout_seconds)
    except subprocess.TimeoutExpired as timeout:
        failures = []
        streams = {}
        # TimeoutExpired streams are bytes even with text=True. In particular,
        # a killed child can leave an incomplete UTF-8 sequence: never decode it.
        for stream, raw in [('stdout', timeout.stdout), ('stderr', timeout.stderr)]:
            streams[stream] = {'present': raw is not None, 'bytes': len(raw) if raw is not None else 0}
            path = out/(name+'.'+stream)
            try:
                path.write_bytes(raw if raw is not None else b'')
            except Exception as error:
                failure = f'{path.name}: {type(error).__name__}: {error}'
                failures.append(failure)
                timeout.add_note('Timeout evidence persistence failed: '+failure)
        elapsed = None
        if clock_failure is None:
            try:
                measured = time.monotonic() - started
                if not math.isfinite(measured) or measured < 0:
                    raise ValueError('elapsed time must be finite and nonnegative')
                elapsed = measured
            except Exception as error:
                clock_failure = f'elapsed clock: {type(error).__name__}: {error}'
        diagnostic_failures = [clock_failure] if clock_failure is not None else []
        if clock_failure is not None:
            timeout.add_note('Timeout evidence diagnostic failed: '+clock_failure)
        # Preserve the cwd argument actually supplied; filesystem resolution is
        # unnecessary and can itself fail while diagnosing the original timeout.
        record = {'argv': list(command), 'cwd': str(cwd),
                  'run_name': name, 'mode': mode, 'mutation': mutation, 'mutant': mutant,
                  'timeout_seconds': timeout_seconds, 'elapsed_seconds': elapsed,
                  'status': 'timed_out', 'streams': streams, 'persistence_failures': failures,
                  'diagnostic_failures': diagnostic_failures}
        path = out/(name+'.timeout.json')
        try:
            path.write_text(json.dumps(record, sort_keys=True, indent=2, allow_nan=False)+'\n')
        except Exception as error:
            timeout.add_note(f'Timeout evidence persistence failed: {path.name}: {type(error).__name__}: {error}')
        raise
    (out/(name+'.stdout')).write_text(result.stdout)
    (out/(name+'.stderr')).write_text(result.stderr)
    require(f'Ran {EXPECTED_TESTS} tests' in result.stderr and 'skipped=' not in result.stderr, 'unexpected test coverage: '+name)
    if mutant:
        require(result.returncode != 0 and 'AssertionError' in result.stderr and 'FAILED (failures=' in result.stderr,
                'mutation was not detected by a test assertion: '+name)
        require('SyntaxError' not in result.stderr and 'ImportError' not in result.stderr and '\nERROR:' not in result.stderr,
                'mutation caused a program error: '+name)
    else:
        require(result.returncode == 0, 'baseline failed: '+name)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    out = parser.parse_args().output.resolve()
    require(not out.exists() and not out.is_relative_to(ROOT), 'new output outside source required')
    out.mkdir(parents=True)
    before = identities()
    source = (ROOT/'hard_gate.py').read_text()
    report = {'passed': False, 'python': sys.version, 'distinct_tests': EXPECTED_TESTS,
              'distinct_semantic_mutations': len(MUTANTS), 'modes': [],
              'promotion_permission': False, 'scientific_effect': 'NONE',
              'meaning': 'software replay and mutation detection only; not independent analytic acceptance'}
    try:
        for mode, flags in [('normal', []), ('optimized', ['-O'])]:
            cmd = [sys.executable, '-B', *flags, '-S', '-m', 'unittest', 'discover', '-p', 'test_*.py', '-v']
            execute(cmd, ROOT, out, 'tests_'+mode, mode=mode)
            result = subprocess.run([sys.executable, '-B', *flags, '-S', 'hard_gate.py'], cwd=ROOT, capture_output=True, timeout=15)
            require(result.returncode == 0 and result.stdout == (ROOT/'RESULTS.json').read_bytes(), 'entry/result mismatch: '+mode)
            (out/('output_'+mode+'.json')).write_bytes(result.stdout)
            for name, (old, new) in MUTANTS.items():
                require(source.count(old) == 1, 'nonunique mutation: '+name)
                mutated = source.replace(old, new)
                compile(mutated, '<mutant '+name+'>', 'exec')
                scratch = out/'mutants'/mode/name
                shutil.copytree(ROOT, scratch, ignore=shutil.ignore_patterns('__pycache__'))
                (scratch/'hard_gate.py').write_text(mutated)
                execute(cmd, scratch, out, 'mutation_'+mode+'_'+name, mutant=True, mode=mode, mutation=name)
            report['modes'].append(mode)
        require(before == identities(), 'source files changed during replay')
        report.update(passed=True, sources_unchanged=True, source_files=before)
    finally:
        active_error = sys.exc_info()[1]
        try:
            (out/'REPORT.json').write_text(json.dumps(report, sort_keys=True, indent=2)+'\n')
        except Exception as error:
            if not isinstance(active_error, subprocess.TimeoutExpired):
                raise
            active_error.add_note(f'Timeout evidence persistence failed: REPORT.json: {type(error).__name__}: {error}')
    print(json.dumps(report, sort_keys=True))


if __name__ == '__main__': main()
