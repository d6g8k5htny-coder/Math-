"""Behavior of tools/evidence_profile.py (standard library only; the live graph is read, never written)."""
import contextlib
import hashlib
import importlib.util
import io
import json
import pathlib
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
GRAPH = ROOT / 'frontiers' / 'downstream_gate_20260925' / 'GRAPH.json'
SPEC = importlib.util.spec_from_file_location('evidence_profile', ROOT / 'tools' / 'evidence_profile.py')
ep = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ep)
GATE = ep.load_gate()


def node(classification, **fields):
    return dict(classification=classification, controlling=False, **fields)


def synthetic():
    return {
        'schema_version': 1,
        'object': 'SYNTHETIC',
        'nodes': {
            'math.top': node('OPEN_ACTIVE'),
            'math.mid': node('PROVED_REVIEWED', author_provider='OpenAI',
                             review_basis=[{'provider': 'xAI'}, {'provider': 'Anthropic/Claude'}]),
            'math.leaf': node('AUTHOR_SIDE_CANDIDATE', author_provider='Anthropic',
                              review_provider='Anthropic Claude session'),
            'math.shared': node('PROVED_REVIEWED', author_provider='OpenAI', review_providers=['nonauthor']),
            'math.boundary': node('REFUTED'),
        },
        'edges': [
            {'from': 'math.top', 'to': 'math.mid', 'required': True, 'relation': 'uses'},
            {'from': 'math.top', 'to': 'math.shared', 'required': True, 'relation': 'uses'},
            {'from': 'math.top', 'to': 'math.boundary', 'required': False, 'relation': 'boundary_only'},
            {'from': 'math.mid', 'to': 'math.leaf', 'required': True, 'relation': 'imports'},
            {'from': 'math.mid', 'to': 'math.shared', 'required': True, 'relation': 'imports'},
        ],
    }


def run(argv):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code = ep.main(argv)
    return code, out.getvalue()


class SyntheticGraph(unittest.TestCase):
    def setUp(self):
        self.graph = synthetic()
        GATE.validate_graph_fail_closed(self.graph)

    def test_unsatisfied_required_is_transitive_and_ignores_context_edges(self):
        p = ep.profile(GATE, self.graph, 'math.top')
        self.assertEqual(p['unsatisfied_required'],
                         [{'node': 'math.leaf', 'classification': 'AUTHOR_SIDE_CANDIDATE'}])
        self.assertEqual(ep.profile(GATE, self.graph, 'math.shared')['unsatisfied_required'], [])

    def test_provider_distinct_reads_only_recorded_families(self):
        self.assertEqual(ep.provider_distinct(self.graph['nodes']['math.mid']), 'yes')
        self.assertEqual(ep.provider_distinct(self.graph['nodes']['math.leaf']), 'no')
        self.assertEqual(ep.provider_distinct(self.graph['nodes']['math.shared']), 'not recorded')
        self.assertEqual(ep.provider_distinct(self.graph['nodes']['math.top']), 'not recorded')
        self.assertIsNone(ep.family('OpenAI reviewed by xAI'))
        self.assertEqual(ep.family('xAI/Grok via Cursor'), 'xAI')

    def test_tree_marks_context_edges_and_expands_shared_nodes_once(self):
        lines = ep.tree_lines(GATE, self.graph, 'math.top')
        text = '\n'.join(lines)
        self.assertIn('context (boundary_only) math.boundary  REFUTED', text)
        self.assertEqual(sum('math.shared' in line for line in lines[1:-1]), 2)
        self.assertEqual(sum('(expanded above)' in line for line in lines), 1)
        self.assertEqual(lines[-1], 'Unsatisfied required dependencies (1): math.leaf (AUTHOR_SIDE_CANDIDATE)')

    def test_roots_are_math_nodes_without_incoming_edges(self):
        self.assertEqual(ep.roots(self.graph), ['math.top'])

    def test_cli_on_file_json_and_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / 'graph.json'
            path.write_text(json.dumps(self.graph))
            code, text = run(['--graph', str(path)])
            self.assertEqual(code, 0)
            self.assertTrue(text.startswith('math.top  OPEN_ACTIVE'))
            self.assertIn('no status authority; scientific effect NONE', text)
            code, text = run(['--graph', str(path), '--node', 'math.mid', '--json'])
            data = json.loads(text)
            self.assertEqual([p['node'] for p in data['profiles']], ['math.mid'])
            self.assertIs(data['status_authority'], False)
            self.assertIs(data['lemma_closed'], False)
            self.assertEqual(data['scientific_effect'], 'NONE')
            self.assertIn('blind_reconstruction', data['axes_outside_graph'])

    def test_invalid_graphs_and_unknown_nodes_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / 'graph.json'
            bad = synthetic()
            bad['edges'].append({'from': 'math.leaf', 'to': 'math.top', 'required': True, 'relation': 'cycle'})
            path.write_text(json.dumps(bad))
            with self.assertRaisesRegex(ValueError, 'required dependency cycle'):
                run(['--graph', str(path)])
            bad = synthetic()
            bad['nodes']['math.top']['classification'] = 'CLOSED'
            path.write_text(json.dumps(bad))
            with self.assertRaisesRegex(ValueError, 'unknown node classification'):
                run(['--graph', str(path)])
            path.write_text(json.dumps(synthetic()))
            with self.assertRaisesRegex(KeyError, 'unknown node'):
                run(['--graph', str(path), '--node', 'math.absent'])


class LiveGraph(unittest.TestCase):
    def test_live_graph_renders_without_writing(self):
        before = hashlib.sha256(GRAPH.read_bytes()).hexdigest()
        code, text = run([])
        self.assertEqual(code, 0)
        graph = GATE.load_graph(GRAPH)
        for root in ep.roots(graph):
            self.assertIn('\n' + root + '  ' if not text.startswith(root) else root, text)
        code, text = run(['--json'])
        data = json.loads(text)
        self.assertEqual(len(data['profiles']), len(ep.roots(graph)))
        for p in data['profiles']:
            self.assertEqual(p['classification'], graph['nodes'][p['node']]['classification'])
        self.assertEqual(hashlib.sha256(GRAPH.read_bytes()).hexdigest(), before)


if __name__ == '__main__':
    unittest.main()
