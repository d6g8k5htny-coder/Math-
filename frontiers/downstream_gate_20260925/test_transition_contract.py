"""Independent failure modes; these tests award no theorem or reviewer credit."""
import copy
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
import hard_gate as m
import git_transition_audit as gitaudit


def graph():
    return {'schema_version': 1, 'nodes': {
        'L': {'classification': 'PROVED_REVIEWED', 'controlling': False, 'source': 'lemma.md'},
        'T': {'classification': 'PROVED_REVIEWED', 'controlling': False},
        'U': {'classification': 'PROVED_REVIEWED', 'controlling': False},
    }, 'edges': [{'from': 'T', 'to': 'L', 'required': True, 'relation': 'premise'}]}


class TransitionContract(unittest.TestCase):
    def test_unknown_classification_rejected(self):
        g = graph(); g['nodes']['L']['classification'] = 'GOOD_ENOUGH'
        with self.assertRaises(ValueError): m.validate_graph_fail_closed(g)

    def test_missing_controlling_rejected(self):
        g = graph(); del g['nodes']['L']['controlling']
        with self.assertRaises(ValueError): m.validate_graph_fail_closed(g)

    def test_non_object_graph_rejected(self):
        with self.assertRaises(ValueError): m.validate_graph_fail_closed([])

    def test_boolean_schema_rejected(self):
        g = graph(); g['schema_version'] = True
        with self.assertRaises(ValueError): m.validate_graph_fail_closed(g)

    def test_contradictory_duplicate_rejected(self):
        g = graph(); e = copy.deepcopy(g['edges'][0]); e['required'] = False; g['edges'].append(e)
        with self.assertRaises(ValueError): m.validate_graph_fail_closed(g)

    def test_promotion_boundary_checks_required_boolean(self):
        g = graph(); g['edges'][0]['required'] = 0
        with self.assertRaises(ValueError): m.promotion_allowed(g, 'T')

    def test_promotion_boundary_checks_cycles(self):
        g = graph(); g['edges'].append({'from': 'L', 'to': 'T', 'required': True, 'relation': 'premise'})
        with self.assertRaises(ValueError): m.promotion_allowed(g, 'T')

    def test_closure_report_checks_shape(self):
        g = graph(); g['nodes']['L']['controlling'] = 'false'
        with self.assertRaises(ValueError): m.closure_report(g)

    def test_edge_metadata_edit_seeds_child(self):
        a = graph(); b = copy.deepcopy(a); b['edges'][0]['scope'] = 'wider'
        self.assertEqual(m.reverse_impact_between(a, b)['changed_nodes'], ['T'])

    def test_context_change_seeds_all_nodes(self):
        a = graph(); b = copy.deepcopy(a); b['domain'] = 'changed'
        self.assertEqual(m.reverse_impact_between(a, b)['changed_nodes'], ['L', 'T', 'U'])

    def test_json_typed_node_change_detected(self):
        a = graph(); b = copy.deepcopy(a); a['nodes']['L']['data'] = True; b['nodes']['L']['data'] = 1
        self.assertEqual(m.reverse_impact_between(a, b)['impacted'], ['L', 'T'])

    def test_unrelated_stable_and_no_input_mutation(self):
        a = graph(); b = copy.deepcopy(a); b['nodes']['L']['domain'] = 'changed'
        frozen = copy.deepcopy((a, b)); r = m.reverse_impact_between(a, b)
        self.assertEqual((a, b), frozen)
        self.assertEqual(r['graph']['nodes']['U'], b['nodes']['U'])
        self.assertFalse(r['promotion_permission'])

    def test_noop_and_edge_reordering(self):
        a = graph(); b = copy.deepcopy(a); b['edges'].reverse()
        self.assertEqual(m.reverse_impact_between(a, b)['impacted'], [])

    def test_removed_node_and_old_edge_survive(self):
        a = graph(); b = copy.deepcopy(a); del b['nodes']['L']; b['edges'] = []
        r = m.reverse_impact_between(a, b)
        self.assertIn('T', r['impacted']); self.assertIn(['T', 'L'], r['traversal_edges'])

    def test_explicit_old_union_edge_evidence(self):
        a = graph(); b = copy.deepcopy(a); b['edges'] = []
        self.assertEqual(m.reverse_impact_between(a, b)['traversal_edges'], [['T', 'L']])

    def test_legacy_changed_node_holds_itself(self):
        r = m.reverse_impact(graph(), 'L', old_fingerprint='a', new_fingerprint='b')
        self.assertIn('L', r['impacted'])
        self.assertEqual(r['graph']['nodes']['L']['classification'], 'REVALIDATION_REQUIRED')

    def test_refutation_is_not_erased_by_revalidation(self):
        a = graph(); b = copy.deepcopy(a); b['nodes']['L']['classification'] = 'REFUTED'
        r = m.reverse_impact_between(a, b)
        self.assertEqual(r['graph']['nodes']['L']['classification'], 'REFUTED')
        self.assertEqual(r['graph']['nodes']['T']['classification'], 'REVALIDATION_REQUIRED')

    def test_source_only_edit_seeds_and_holds(self):
        a = graph(); x = {k: 'sha-a' for k in a['nodes']}; y = dict(x); y['L'] = 'sha-b'
        r = m.reverse_impact_between(a, a, old_sources=x, new_sources=y)
        self.assertEqual(r['impacted'], ['L', 'T']); self.assertTrue(r['source_snapshots_supplied'])

    def test_one_sided_source_snapshot_refused(self):
        with self.assertRaises(ValueError): m.reverse_impact_between(graph(), graph(), old_sources={})

    def test_partial_source_snapshot_refused(self):
        with self.assertRaises(ValueError): m.reverse_impact_between(graph(), graph(), old_sources={'L': 'x'}, new_sources={'L': 'x'})

    def test_duplicate_json_key_refused(self):
        with self.assertRaises(ValueError): m.load_json_strict('{"nodes": {}, "nodes": {}}')

    def test_nonfinite_json_refused(self):
        with self.assertRaises(ValueError): m.load_json_strict('{"value": NaN}')

    def test_report_includes_author_side_required_hold(self):
        g = graph(); g['nodes']['L']['classification'] = 'AUTHOR_SIDE_CANDIDATE'
        self.assertEqual(m.closure_report(g)['hold_proposals'], [{'node': 'T', 'unsatisfied_required': ['L']}])

    def test_report_includes_superseded_required_hold(self):
        g = graph(); g['nodes']['L']['classification'] = 'SUPERSEDED_NONBLOCKING'
        self.assertEqual(m.closure_report(g)['hold_proposals'], [{'node': 'T', 'unsatisfied_required': ['L']}])

    def test_green_ci_token_rejected_with_satisfied_nodes(self):
        decision = m.refuse_non_discharge_promotion(graph(), 'T', ['GREEN_CI'])
        self.assertTrue(decision['refused'])
        self.assertFalse(decision['allowed'])

    def test_git_source_only_change_on_real_commits(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            def run(*args):
                return subprocess.run(['git', '-C', tmp, *args], check=True, capture_output=True).stdout.decode().strip()
            run('init', '-q'); run('config', 'user.name', 'local test'); run('config', 'user.email', 'test@example.invalid')
            (repo/'GRAPH.json').write_text(json.dumps(graph())); (repo/'lemma.md').write_text('first statement')
            run('add', '.'); run('commit', '-qm', 'baseline'); old = run('rev-parse', 'HEAD')
            (repo/'lemma.md').write_text('changed statement')
            run('add', '.'); run('commit', '-qm', 'source-only edit'); new = run('rev-parse', 'HEAD')
            r = gitaudit.audit(repo, old, new, 'GRAPH.json')
            self.assertEqual(r['changed_nodes'], ['L']); self.assertEqual(r['impacted'], ['L', 'T'])
            self.assertTrue(r['check_passed']); self.assertFalse(r['promotion_permission'])
            g = graph(); g['nodes']['L']['controlling'] = True
            (repo/'GRAPH.json').write_text(json.dumps(g)); run('add', '.'); run('commit', '-qm', 'illegal promotion')
            r = gitaudit.audit(repo, new, run('rev-parse', 'HEAD'), 'GRAPH.json')
            self.assertFalse(r['check_passed']); self.assertEqual(r['controlling_impacted'], ['L'])

    def test_git_requires_immutable_revision(self):
        with self.assertRaises(ValueError): gitaudit.read_snapshot(Path('.'), 'main', 'GRAPH.json')

    def test_source_path_traversal_rejected(self):
        for p in ('../x', '/x', 'a:b', 'a\\b', ''):
            with self.subTest(path=p):
                with self.assertRaises(ValueError): gitaudit.relative_path(p)


if __name__ == '__main__': unittest.main()
