"""Fail-closed downstream promotion gate (main #90 / #86).

Scientific effect: NONE. This module never flips lemma_closed, prizes, or
premise registers. Green CI / hashes / same-author checks are not discharge.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
GRAPH_PATH = ROOT / 'GRAPH.json'

TERMINAL = frozenset({
    'PROVED_REVIEWED',
    'SUPERSEDED_NONBLOCKING',
    'REFUTED',
    'BLOCKED_ABSENT',
})

# Classifications that may appear on live nodes but are never terminal discharge.
NONTERMINAL = frozenset({
    'OPEN_HISTORICAL',
    'OPEN_ACTIVE',
    'AUTHOR_SIDE_CANDIDATE',
    'AUTHOR_SIDE_REDUCTION',
    'COVERED_BY_CANDIDATE',
    'ENGINEERING_CONTROL',
    'HOLD',
    'REVALIDATION_REQUIRED',
    'FALSE',
    'EXPLORATORY',
})

NON_DISCHARGE_DEFAULT = (
    'GREEN_CI',
    'HASH_MATCH',
    'ARCHITECTURAL_ADMISSION',
    'NUMERICAL_EXPERIMENT',
    'SAME_AUTHOR_REVIEW',
    'NAVIGATION_SUCCESS',
    'AUTHOR_SELF_CHECK',
)


def load_graph(path: Path | None = None) -> dict[str, Any]:
    data = json.loads((path or GRAPH_PATH).read_text())
    if data.get('schema_version') != 1:
        raise ValueError('unsupported graph schema_version')
    if 'nodes' not in data or 'edges' not in data:
        raise ValueError('graph requires nodes and edges')
    return data


def require_node(graph: dict[str, Any], node_id: str) -> dict[str, Any]:
    nodes = graph['nodes']
    if node_id not in nodes:
        raise KeyError('unknown node: ' + node_id)
    return nodes[node_id]


def required_dependencies(graph: dict[str, Any], node_id: str) -> list[str]:
    require_node(graph, node_id)
    return [e['to'] for e in graph['edges']
            if e['from'] == node_id and e.get('required', True)]


def all_dependencies(graph: dict[str, Any], node_id: str) -> list[str]:
    require_node(graph, node_id)
    return [e['to'] for e in graph['edges'] if e['from'] == node_id]


def transitive_required(graph: dict[str, Any], node_id: str) -> list[str]:
    """Depth-first required transitive closure, cycle-safe, deterministic order."""
    seen: set[str] = set()
    order: list[str] = []

    def walk(nid: str) -> None:
        for dep in required_dependencies(graph, nid):
            if dep in seen:
                continue
            seen.add(dep)
            order.append(dep)
            walk(dep)

    walk(node_id)
    return order


def dependents(graph: dict[str, Any], node_id: str, *, required_only: bool = False) -> list[str]:
    require_node(graph, node_id)
    out = []
    for e in graph['edges']:
        if e['to'] != node_id:
            continue
        if required_only and not e.get('required', True):
            continue
        out.append(e['from'])
    return sorted(set(out))


def transitive_dependents(graph: dict[str, Any], node_id: str) -> list[str]:
    seen: set[str] = set()
    order: list[str] = []

    def walk(nid: str) -> None:
        for child in dependents(graph, nid):
            if child in seen:
                continue
            seen.add(child)
            order.append(child)
            walk(child)

    walk(node_id)
    return order


def is_terminal(classification: str) -> bool:
    return classification in TERMINAL


def blocked_absent_hold(graph: dict[str, Any], node_id: str) -> list[str]:
    """Required transitive BLOCKED_ABSENT dependencies force HOLD."""
    return [dep for dep in transitive_required(graph, node_id)
            if require_node(graph, dep)['classification'] == 'BLOCKED_ABSENT']


def promotion_allowed(graph: dict[str, Any], node_id: str) -> dict[str, Any]:
    """Return whether node_id may become CONTROLLING under #90 rules."""
    node = require_node(graph, node_id)
    required = transitive_required(graph, node_id)
    missing_terminal = []
    blocked = []
    for dep in required:
        cls = require_node(graph, dep)['classification']
        if not is_terminal(cls):
            missing_terminal.append({'id': dep, 'classification': cls})
        if cls == 'BLOCKED_ABSENT':
            blocked.append(dep)

    reasons: list[str] = []
    if node.get('classification') == 'REVALIDATION_REQUIRED':
        reasons.append('node requires revalidation after a dependency change')
    if blocked:
        reasons.append('required BLOCKED_ABSENT dependency forces HOLD')
    if missing_terminal:
        reasons.append('required transitive dependency is not terminally classified')
    if node.get('classification') == 'FALSE' and node_id == 'hist.lemma_closed':
        reasons.append('lemma_closed register must remain FALSE; gate never promotes it')

    allowed = not reasons
    return {
        'node': node_id,
        'allowed': allowed,
        'would_be_controlling': allowed,
        'required_dependencies': required,
        'missing_terminal': missing_terminal,
        'blocked_absent': blocked,
        'reasons': reasons,
        'meaning': 'integrity decision only; not theorem acceptance',
    }


def refuse_non_discharge_promotion(
    graph: dict[str, Any],
    node_id: str,
    evidence_tokens: list[str] | tuple[str, ...],
) -> dict[str, Any]:
    """Fail closed when promotion is justified only by non-discharge tokens."""
    tokens = list(evidence_tokens)
    non_discharge = set(graph.get('non_discharge_tokens', NON_DISCHARGE_DEFAULT))
    unknown = [t for t in tokens if t not in non_discharge and t not in (
        'PROVED_REVIEWED', 'SUPERSEDED_NONBLOCKING', 'REFUTED', 'LINE_BY_LINE_ANALYTIC_REVIEW',
        'EXACT_COUNTEREXAMPLE', 'SUPERSESSION_CROSSWALK',
    )]
    only_non_discharge = bool(tokens) and all(t in non_discharge for t in tokens)
    base = promotion_allowed(graph, node_id)
    refused = only_non_discharge or (not base['allowed'])
    reasons = list(base['reasons'])
    if only_non_discharge:
        reasons.append('evidence consists only of non-discharge tokens')
    if unknown:
        reasons.append('unknown evidence tokens: ' + ','.join(unknown))
        refused = True
    return {
        'node': node_id,
        'refused': refused,
        'allowed': (not refused) and base['allowed'],
        'evidence_tokens': tokens,
        'reasons': reasons,
        'base': base,
    }


def apply_promotion(graph: dict[str, Any], node_id: str) -> dict[str, Any]:
    """Mutate a copy: set controlling only when legal; otherwise HOLD / refuse."""
    clone = json.loads(json.dumps(graph))
    decision = promotion_allowed(clone, node_id)
    node = clone['nodes'][node_id]
    if decision['blocked_absent']:
        node['controlling'] = False
        node['classification'] = 'HOLD'
        decision = {**decision, 'applied': 'HOLD', 'ok': False}
    elif not decision['allowed']:
        node['controlling'] = False
        decision = {**decision, 'applied': 'REFUSED', 'ok': False}
    else:
        node['controlling'] = True
        decision = {**decision, 'applied': 'CONTROLLING', 'ok': True}
    return {'graph': clone, 'decision': decision}


def reverse_impact(
    graph: dict[str, Any],
    changed_node: str,
    *,
    old_fingerprint: str | None = None,
    new_fingerprint: str | None = None,
    old_classification: str | None = None,
    new_classification: str | None = None,
) -> dict[str, Any]:
    """Mark transitive dependents REVALIDATION_REQUIRED after a dependency change."""
    require_node(graph, changed_node)
    clone = json.loads(json.dumps(graph))
    changed = False
    if old_fingerprint is not None and new_fingerprint is not None and old_fingerprint != new_fingerprint:
        changed = True
        clone['nodes'][changed_node]['fingerprint'] = new_fingerprint
    if old_classification is not None and new_classification is not None and old_classification != new_classification:
        changed = True
        clone['nodes'][changed_node]['classification'] = new_classification

    impacted: list[str] = []
    if changed:
        for dep in transitive_dependents(clone, changed_node):
            node = clone['nodes'][dep]
            if node.get('controlling') or node.get('classification') in (
                'AUTHOR_SIDE_CANDIDATE', 'AUTHOR_SIDE_REDUCTION', 'COVERED_BY_CANDIDATE',
                'PROVED_REVIEWED', 'SUPERSEDED_NONBLOCKING',
            ):
                node['classification'] = 'REVALIDATION_REQUIRED'
                node['controlling'] = False
                impacted.append(dep)

    return {
        'changed_node': changed_node,
        'dependency_changed': changed,
        'impacted': impacted,
        'graph': clone,
        'meaning': 'reverse-impact revalidation marks; not theorem discharge',
    }


def closure_report(graph: dict[str, Any]) -> dict[str, Any]:
    """Machine-readable D0–D7 closure report for the campaign queue."""
    by_layer: dict[str, list[dict[str, Any]]] = {}
    controlling_illegal: list[dict[str, Any]] = []
    for nid, node in sorted(graph['nodes'].items()):
        layer = node.get('layer', '?')
        by_layer.setdefault(layer, []).append({
            'id': nid,
            'classification': node['classification'],
            'controlling': bool(node.get('controlling')),
            'kind': node.get('kind'),
        })
        if node.get('controlling'):
            decision = promotion_allowed(graph, nid)
            if not decision['allowed']:
                controlling_illegal.append(decision)

    layers = sorted(by_layer)
    open_active = [nid for nid, n in sorted(graph['nodes'].items())
                   if n['classification'] in ('OPEN_ACTIVE', 'OPEN_HISTORICAL',
                                              'AUTHOR_SIDE_CANDIDATE', 'AUTHOR_SIDE_REDUCTION',
                                              'HOLD', 'REVALIDATION_REQUIRED')]
    blocked = [nid for nid, n in sorted(graph['nodes'].items())
               if n['classification'] == 'BLOCKED_ABSENT']
    return {
        'object': graph.get('object'),
        'layers': {layer: by_layer[layer] for layer in layers},
        'open_or_author_side': open_active,
        'blocked_absent': blocked,
        'illegal_controlling': controlling_illegal,
        'lemma_closed': False,
        'scientific_effect': 'NONE',
        'gate_ok': len(controlling_illegal) == 0,
        'meaning': 'dependency closure inventory; publication is not acceptance',
    }


def d4_region_complement(graph: dict[str, Any]) -> dict[str, Any]:
    """Explicit D4/D5 region map: what fixed-remote covers versus what remains open."""
    covered = []
    open_regions = []
    for nid, node in sorted(graph['nodes'].items()):
        if node.get('kind') != 'region':
            continue
        entry = {
            'id': nid,
            'classification': node['classification'],
            'fingerprint': node.get('fingerprint'),
            'notes': node.get('notes'),
        }
        if node['classification'] == 'COVERED_BY_CANDIDATE':
            covered.append(entry)
        else:
            open_regions.append(entry)
    return {
        'covered_by_fixed_remote_candidate': covered,
        'open_complement': open_regions,
        'no_event_to_expectation_reversal': True,
        'legacy_24jet_discharged': False,
        'meaning': 'region inventory for #76/#86 D4; not a numerical RN certificate',
    }


def results_payload(graph: dict[str, Any] | None = None) -> dict[str, Any]:
    g = graph or load_graph()
    # Spot-check promotions that must fail closed on the live author-side graph.
    illegal_attempts = {
        'promote_fixed_remote': refuse_non_discharge_promotion(
            g, 'math.rn-fixed-remote-window',
            ['GREEN_CI', 'HASH_MATCH', 'SAME_AUTHOR_REVIEW']),
        'promote_lifetime_remainder': promotion_allowed(g, 'math.lifetime-remainder'),
        'promote_side24': promotion_allowed(g, 'math.side24-coefficient'),
        'promote_historical_env_rescov': promotion_allowed(g, 'hist.ENV-RESCOV'),
    }
    impact = reverse_impact(
        g, 'math.uniform-matrix-cap-lifetime',
        old_fingerprint='main-63-author-side',
        new_fingerprint='main-63-amended-demo',
    )
    return {
        'object': g.get('object'),
        'schema_version': g.get('schema_version'),
        'gate_ok': closure_report(g)['gate_ok'],
        'lemma_closed': False,
        'scientific_effect': 'NONE',
        'illegal_promotion_refused': all(
            (v.get('refused') if 'refused' in v else not v.get('allowed'))
            for v in illegal_attempts.values()
        ),
        'illegal_attempts': {
            k: {key: val for key, val in v.items() if key != 'base'}
            for k, v in illegal_attempts.items()
        },
        'reverse_impact_demo': {
            'changed_node': impact['changed_node'],
            'impacted': impact['impacted'],
            'dependency_changed': impact['dependency_changed'],
        },
        'd4_region_complement': d4_region_complement(g),
        'closure': {
            'blocked_absent': closure_report(g)['blocked_absent'],
            'open_or_author_side_count': len(closure_report(g)['open_or_author_side']),
            'illegal_controlling_count': len(closure_report(g)['illegal_controlling']),
        },
        'meaning': (
            'same-author integrity controls for main #90/#86; '
            'not analytic review or theorem acceptance'
        ),
    }


def main() -> None:
    payload = results_payload()
    text = json.dumps(payload, indent=2, sort_keys=True) + '\n'
    print(text, end='')
    # When executed as the package entry point, compare to pinned RESULTS.json.
    expected = (ROOT / 'RESULTS.json').read_text()
    if text != expected:
        raise SystemExit('RESULTS.json byte mismatch; regenerate deliberately')


if __name__ == '__main__':
    main()
