#!/usr/bin/env python3
"""Read-only dependency tree and evidence profile for the downstream gate graph (standard library only).

Renders, for a node of frontiers/downstream_gate_20260925/GRAPH.json (or every math.* root), the tree of
its outgoing edges with each node's recorded classification, the providers its record names, and the
required dependencies that do not yet satisfy the hard gate. The graph is loaded and validated with the
gate's own strict loader; the dependency rule is the gate's (an edge is required unless it says
otherwise; only PROVED_REVIEWED satisfies a required premise).

This is the derived view proposed in main#275 (decision record v1.1, rows PROPOSED) and main#276
(governance/OP-CLOSURE-EVIDENCE-20261006.md, unmerged at publication): it writes
nothing, promotes nothing and is not a status record. Axes the graph does not record (blind
reconstruction, adversarial attack, formal evidence, numerical reproduction, novelty, human reading)
are listed as outside the graph rather than reported as passed or failed. Scientific effect: NONE.

With --eligibility, selected nodes also show the gate's own CONTROLLING eligibility decision and
reasons. This describes the supplied graph, not review sufficiency, an executed promotion or theorem
acceptance. The default text and JSON output are unchanged when this option is absent.

With --input-identity, include the SHA-256 and length of the exact graph bytes consumed. The
single captured buffer is both parsed and hashed; different serializations have different identities.
This is not freshness, authenticated Git provenance, program/runtime identity or acceptance evidence.
No path is reported. Without the flag, the existing loader and output remain unchanged.

Usage: python3 -B -S tools/evidence_profile.py [--graph PATH] [--node ID] [--json] [--eligibility] [--input-identity]
"""
import argparse
import hashlib
import io
import importlib.util
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE_DIR = ROOT / 'frontiers' / 'downstream_gate_20260925'
AXES_OUTSIDE_GRAPH = (
    'blind_reconstruction', 'adversarial_attack', 'formal_evidence',
    'numerical_reproduction', 'novelty', 'human_reading',
)
# Provider attribution grammar (EP381-02, review 5430026100 and delta 6018757501). A record string names a provider
# family only in this positive form, compared case-insensitively:
#     FAMILY_ALIAS ( ('/' | ' ') (FAMILY_ALIAS | DECORATION | VERSION) )*  [ ' (' note ')' ]
# where every alias belongs to the same family, DECORATION is one of the listed product/agent/session words, VERSION is
# a model or version identifier containing a digit (gpt-6, 4.7, grok-4.7-high-fast), and one trailing parenthetical
# scope note is ignored. Anything else ('possibly OpenAI', 'OpenAI or Anthropic', 'review requested from OpenAI',
# 'not OpenAI', 'claudette') names no family and is reported verbatim as unresolved.
FAMILY_ALIASES = {
    'openai': 'OpenAI', 'chatgpt': 'OpenAI', 'codex': 'OpenAI', 'gpt': 'OpenAI',
    'anthropic': 'Anthropic', 'claude': 'Anthropic',
    'xai': 'xAI', 'grok': 'xAI',
    'google': 'Google', 'gemini': 'Google',
}
DECORATIONS = frozenset({'via', 'cursor', 'pro', 'code', 'session', 'agent', 'cloud', 'bot', 'model', 'astra', 'sol',
                         'deepmind', 'high', 'fast'})
VERSION = re.compile(r'[a-z]*-?\d[a-z0-9.\-]*')


def load_gate():
    spec = importlib.util.spec_from_file_location('downstream_hard_gate', GATE_DIR / 'hard_gate.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def family(text):
    """Provider family named by a record string in the positive grammar above, else None (unresolved)."""
    match = re.fullmatch(r'\s*([^()]*?)\s*(?:\([^()]*\))?\s*', text)
    if match is None:
        return None
    tokens = [t for t in re.split(r'[\s/]+', match.group(1).lower()) if t]
    if not tokens or tokens[0] not in FAMILY_ALIASES:
        return None
    name = FAMILY_ALIASES[tokens[0]]
    for token in tokens[1:]:
        if token in FAMILY_ALIASES:
            if FAMILY_ALIASES[token] != name:
                return None
        elif token not in DECORATIONS and not VERSION.fullmatch(token):
            return None
    return name


def reviewer_strings(node):
    out = []
    for item in node.get('review_basis', []) or []:
        if isinstance(item, dict) and isinstance(item.get('provider'), str):
            out.append(item['provider'])
    providers = node.get('review_providers')
    if isinstance(providers, list):
        out.extend(p for p in providers if isinstance(p, str))
    if isinstance(node.get('review_provider'), str):
        out.append(node['review_provider'])
    return out


def provider_distinct(node):
    """'yes' if some recorded reviewer resolves to a family other than the recorded author's; 'no' only if
    every recorded reviewer resolves to the author's family; otherwise 'not recorded' (missing author or
    reviewers, or a reviewer string naming no single family). Never organizational independence."""
    author = node.get('author_provider')
    author_family = family(author) if isinstance(author, str) else None
    reviewer_families = [family(s) for s in reviewer_strings(node)]
    if author_family is None or not reviewer_families:
        return 'not recorded'
    if any(f is not None and f != author_family for f in reviewer_families):
        return 'yes'
    if all(f == author_family for f in reviewer_families):
        return 'no'
    return 'not recorded'


def profile(gate, graph, node_id, include_eligibility=False):
    node = gate.require_node(graph, node_id)
    unsatisfied = [dep for dep in gate.transitive_required(graph, node_id)
                   if graph['nodes'][dep]['classification'] not in gate.REQUIRED_SATISFIED]
    result = {
        'node': node_id,
        'classification': node['classification'],
        'review_disposition': node.get('review_disposition', 'not recorded'),
        'author_provider': node.get('author_provider', 'not recorded'),
        'reviewer_providers': reviewer_strings(node) or ['not recorded'],
        'provider_distinct': provider_distinct(node),
        'unresolved_reviewer_providers': [s for s in reviewer_strings(node) if family(s) is None],
        'unsatisfied_required': [{'node': dep, 'classification': graph['nodes'][dep]['classification']}
                                 for dep in unsatisfied],
        'axes_outside_graph': list(AXES_OUTSIDE_GRAPH),
    }
    if include_eligibility:
        result['controlling_eligibility'] = {
            'target': 'CONTROLLING',
            'decision': gate.promotion_allowed(graph, node_id),
        }
    return result


def roots(graph):
    """math.* nodes without an incoming edge, then, in sorted order, any math.* node not reached from those
    (a component whose math nodes all have incoming edges, e.g. a context-only cycle), so none is omitted."""
    targets = {e['to'] for e in graph['edges']}
    math_nodes = sorted(n for n in graph['nodes'] if n.startswith('math.'))
    chosen = [n for n in math_nodes if n not in targets]
    reached = set()

    def reach(nid):
        stack = [nid]
        while stack:
            cur = stack.pop()
            if cur in reached:
                continue
            reached.add(cur)
            stack.extend(e['to'] for e in graph['edges'] if e['from'] == cur)

    for n in chosen:
        reach(n)
    for n in math_nodes:
        if n not in reached:
            chosen.append(n)
            reach(n)
    return chosen


def tree_lines(gate, graph, node_id, include_eligibility=False):
    lines = []
    seen = set()

    def label(nid):
        p = profile(gate, graph, nid)
        return '%s  %s  [author %s; reviewers %s; provider-distinct %s]' % (
            nid, p['classification'], p['author_provider'], ', '.join(p['reviewer_providers']),
            p['provider_distinct'])

    def walk(nid, prefix):
        edges = sorted((e for e in graph['edges'] if e['from'] == nid), key=lambda e: e['to'])
        for i, e in enumerate(edges):
            last = i == len(edges) - 1
            kind = 'requires' if e.get('required', True) else 'context (%s)' % e.get('relation', '?')
            child = e['to']
            again = child in seen
            lines.append('%s%s %s %s%s' % (prefix, '└──' if last else '├──', kind, label(child),
                                          '  (expanded above)' if again else ''))
            if not again:
                seen.add(child)
                walk(child, prefix + ('    ' if last else '│   '))

    seen.add(node_id)
    lines.append(label(node_id))
    walk(node_id, '')
    unsatisfied = profile(gate, graph, node_id)['unsatisfied_required']
    if unsatisfied:
        lines.append('Unsatisfied required dependencies (%d): %s' % (len(unsatisfied), ', '.join(
            '%s (%s)' % (u['node'], u['classification']) for u in unsatisfied)))
    else:
        lines.append('Unsatisfied required dependencies: none')
    if include_eligibility:
        decision = gate.promotion_allowed(graph, node_id)
        lines.append('Selected-node CONTROLLING eligibility (recorded graph): '
                     + ('yes' if decision['allowed'] else 'no'))
        lines.extend('  - ' + reason for reason in decision['reasons'])
        lines.append('  ' + decision['meaning'])
    return lines


def report(gate, graph, node_ids, include_eligibility=False):
    return {
        'object': graph.get('object'),
        'profiles': [profile(gate, graph, nid, include_eligibility) for nid in node_ids],
        'axes_outside_graph': list(AXES_OUTSIDE_GRAPH),
        'meaning': 'derived read-only view of recorded graph fields; not a status record or acceptance',
        'status_authority': False,
        'lemma_closed': False,
        'scientific_effect': 'NONE',
    }



def load_graph_with_identity(gate, path):
    """Parse and identify one captured buffer using the gate's unchanged strict validation.

    TextIOWrapper matches Path.read_text's default decoding and universal-newline behavior;
    the fingerprint covers original bytes, not the decoded or reserialized JSON.
    """
    raw = path.read_bytes()
    with io.TextIOWrapper(io.BytesIO(raw)) as stream:
        graph = gate.load_json_strict(stream.read())
    gate.validate_graph_fail_closed(graph)
    identity = {
        'bytes': len(raw),
        'sha256': hashlib.sha256(raw).hexdigest(),
        'meaning': 'identity of graph input bytes only; not freshness, Git provenance, '
                   'program identity or acceptance',
    }
    return graph, identity


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--graph', default=str(GATE_DIR / 'GRAPH.json'))
    ap.add_argument('--node', action='append', help='node id (repeatable); default: every math.* root')
    ap.add_argument('--json', action='store_true', help='print the profiles as JSON instead of trees')
    ap.add_argument('--eligibility', action='store_true',
                    help='include the selected-node gate decision; not theorem acceptance')
    ap.add_argument('--input-identity', action='store_true',
                    help='include exact graph-input byte identity, not provenance or acceptance')
    args = ap.parse_args(argv)
    gate = load_gate()
    identity = None
    if args.input_identity:
        graph, identity = load_graph_with_identity(gate, pathlib.Path(args.graph))
    else:
        graph = gate.load_graph(pathlib.Path(args.graph))
    node_ids = args.node or roots(graph)
    for nid in node_ids:
        gate.require_node(graph, nid)
    if args.json:
        data = report(gate, graph, node_ids, args.eligibility)
        if identity is not None:
            data['input_identity'] = identity
        print(json.dumps(data, indent=2, sort_keys=True))
        return 0
    if identity is not None:
        print('Graph input SHA-256: %s (%d bytes)' % (identity['sha256'], identity['bytes']))
        print(identity['meaning'])
        print()
    for index, nid in enumerate(node_ids):
        if index:
            print()
        print('\n'.join(tree_lines(gate, graph, nid, args.eligibility)))
    print()
    print('Not in the graph (consult review records): ' + ', '.join(AXES_OUTSIDE_GRAPH))
    print('Derived view only: no status authority; scientific effect NONE.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
