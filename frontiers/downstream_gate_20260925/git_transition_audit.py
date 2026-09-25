"""Read exact Git revisions and report loss-only dependency revalidation proposals.

No network, worktree mutation, scientific-state write, or promotion permission.
External references are explicitly unresolved; only repository objects are bound.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import hard_gate as gate


def git(repo: Path, *args: str, missing: bool = False) -> bytes | None:
    result = subprocess.run(['git', '-C', str(repo), *args], capture_output=True, timeout=30)
    if result.returncode:
        if missing:
            return None
        raise ValueError('Git object unavailable for the requested pinned revision')
    return result.stdout


def relative_path(value: str) -> str:
    path = PurePosixPath(value)
    if not value or path.is_absolute() or '..' in path.parts or ':' in value or '\\' in value:
        raise ValueError('repository-relative source path required')
    return path.as_posix()


def read_snapshot(repo: Path, revision: str, graph_path: str) -> tuple[dict, dict]:
    if not re.fullmatch(r'[0-9a-f]{40}|[0-9a-f]{64}', revision):
        raise ValueError('a full lowercase immutable commit ID is required')
    if git(repo, 'cat-file', '-t', revision).strip() != b'commit':
        raise ValueError('revision is not a commit')
    raw = git(repo, 'show', revision + ':' + relative_path(graph_path))
    graph = gate.load_json_strict(raw.decode('utf-8'))
    gate.validate_graph_fail_closed(graph)
    sources = {}
    for nid, node in graph['nodes'].items():
        reference = node.get('source')
        if reference is None:
            sources[nid] = {'kind': 'record_only'}
            continue
        if not isinstance(reference, str) or not reference.strip():
            raise ValueError('source reference must be a nonempty string')
        if reference.startswith(('https://', 'http://', 'external:')):
            sources[nid] = {'kind': 'external_unresolved', 'reference': reference}
            continue
        path = relative_path(reference)
        object_spec = revision + ':' + path.rstrip('/')
        kind = git(repo, 'cat-file', '-t', object_spec, missing=True)
        if kind is None:
            sources[nid] = {'kind': 'missing', 'reference': reference}
            continue
        kind = kind.decode().strip()
        if kind not in ('blob', 'tree'):
            raise ValueError('source object must be a blob or directory tree')
        body = git(repo, 'cat-file', '-p', object_spec)
        sources[nid] = {
            'kind': kind, 'reference': reference, 'bytes': len(body),
            'sha256': hashlib.sha256(body).hexdigest(),
        }
    return graph, sources


def audit(repo: Path, base: str, head: str, graph_path: str) -> dict:
    old, old_sources = read_snapshot(repo, base, graph_path)
    new, new_sources = read_snapshot(repo, head, graph_path)
    impact = gate.reverse_impact_between(old, new, old_sources=old_sources, new_sources=new_sources)
    report = gate.closure_report(new)
    controlling_impacted = [nid for nid in impact['impacted'] if new['nodes'][nid]['controlling']]
    unresolved_controlling = [nid for nid, n in new['nodes'].items()
                              if n['controlling'] and new_sources[nid]['kind'] not in ('blob', 'tree')]
    return {
        'base_commit': base, 'head_commit': head, 'graph_path': graph_path,
        'input_graphs_unchanged': True, 'old_sources': old_sources, 'new_sources': new_sources,
        'changed_nodes': impact['changed_nodes'], 'impacted': impact['impacted'],
        'traversal_edges': impact['traversal_edges'],
        'revalidation_proposals': {nid: impact['graph']['nodes'][nid]['classification'] for nid in impact['impacted']},
        'hold_proposals': report['hold_proposals'],
        'controlling_impacted': controlling_impacted,
        'unresolved_controlling_sources': unresolved_controlling,
        'illegal_controlling': report['illegal_controlling'],
        'check_passed': not (controlling_impacted or unresolved_controlling or report['illegal_controlling']),
        'promotion_permission': False, 'scientific_effect': 'NONE',
        'meaning': 'source-bound workflow integrity only; external refs are not independently fetched or accepted',
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path('.'))
    parser.add_argument('--base', required=True)
    parser.add_argument('--head', required=True)
    parser.add_argument('--graph', default='frontiers/downstream_gate_20260925/GRAPH.json')
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    try:
        repo, out = args.repo.resolve(), args.output.resolve()
        if out.exists() or out.is_relative_to(repo):
            raise ValueError('output must be new and outside the repository')
        result = audit(repo, args.base, args.head, args.graph)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
        print(json.dumps({k: result[k] for k in ('check_passed', 'changed_nodes', 'controlling_impacted', 'promotion_permission')}))
        return 0 if result['check_passed'] else 2
    except (ValueError, OSError, UnicodeError, subprocess.TimeoutExpired) as exc:
        print('TRANSITION_CHECK_REFUSED: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
