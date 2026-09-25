"""Finite integrity-gate controls; not mathematical review or theorem acceptance."""
from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

import hard_gate as m

ROOT = Path(__file__).resolve().parent


class HardGateControls(unittest.TestCase):
    def setUp(self):
        self.graph = m.load_graph()

    def test_schema_and_terminal_set(self):
        self.assertEqual(self.graph['schema_version'], 1)
        self.assertEqual(
            set(self.graph['terminal_classifications']),
            set(m.TERMINAL),
        )
        for token in m.NON_DISCHARGE_DEFAULT:
            self.assertIn(token, self.graph['non_discharge_tokens'])

    def test_unknown_node_refused(self):
        with self.assertRaises(KeyError):
            m.require_node(self.graph, 'no.such.node')

    def test_historical_carriers_absent(self):
        for nid in (
            'hist.rnu_env.py',
            'hist.CL_ANTHROPIC_BUNDLE_2026-09-17_v5.zip',
            'hist.allcell_fdz_enclosures.json',
        ):
            self.assertEqual(self.graph['nodes'][nid]['classification'], 'BLOCKED_ABSENT')
            self.assertFalse(self.graph['nodes'][nid]['controlling'])

    def test_lemma_closed_never_true(self):
        node = self.graph['nodes']['hist.lemma_closed']
        self.assertEqual(node['classification'], 'FALSE')
        self.assertFalse(node['controlling'])
        report = m.closure_report(self.graph)
        self.assertIs(report['lemma_closed'], False)
        self.assertEqual(report['scientific_effect'], 'NONE')

    def test_lifetime_requires_parent(self):
        deps = m.required_dependencies(self.graph, 'math.lifetime-remainder')
        self.assertEqual(deps, ['math.uniform-matrix-cap-lifetime'])
        decision = m.promotion_allowed(self.graph, 'math.lifetime-remainder')
        self.assertFalse(decision['allowed'])
        self.assertTrue(any(x['id'] == 'math.uniform-matrix-cap-lifetime'
                            for x in decision['missing_terminal']))

    def test_side24_requires_parent(self):
        decision = m.promotion_allowed(self.graph, 'math.side24-coefficient')
        self.assertFalse(decision['allowed'])
        self.assertIn('math.uniform-matrix-cap-lifetime', decision['required_dependencies'])

    def test_fixed_remote_requires_count_interface(self):
        deps = m.transitive_required(self.graph, 'math.rn-fixed-remote-window')
        self.assertIn('math.rn-count-interface', deps)
        decision = m.promotion_allowed(self.graph, 'math.rn-fixed-remote-window')
        self.assertFalse(decision['allowed'])

    def test_mesoscopic_requires_fixed_remote(self):
        deps = m.required_dependencies(self.graph, 'math.rn-mesoscopic-reduction')
        self.assertEqual(deps, ['math.rn-fixed-remote-window'])

    def test_chart_j0_complements_pr7_reduction(self):
        node = self.graph['nodes']['math.rn-mesoscopic-chart-j0']
        self.assertEqual(node['classification'], 'AUTHOR_SIDE_CANDIDATE')
        self.assertFalse(node['controlling'])
        self.assertEqual(node['review_pr'], 9)
        self.assertEqual(
            node['fingerprint'],
            '907d6b8589c1111748cde423f2f633df6da58429',
        )
        deps = m.required_dependencies(self.graph, 'math.rn-mesoscopic-chart-j0')
        self.assertEqual(deps, ['math.rn-mesoscopic-reduction'])
        decision = m.promotion_allowed(self.graph, 'math.rn-mesoscopic-chart-j0')
        self.assertFalse(decision['allowed'])
        self.assertIn('PR9', self.graph['nodes'][
            'math.rn-region.mesoscopic-scaled-annulus']['notes'])

    def test_blocked_absent_forces_hold_on_historical_env(self):
        blocked = m.blocked_absent_hold(self.graph, 'hist.ENV-RESCOV')
        self.assertEqual(blocked, ['hist.rnu_env.py'])
        applied = m.apply_promotion(self.graph, 'hist.ENV-RESCOV')
        self.assertFalse(applied['decision']['ok'])
        self.assertEqual(applied['decision']['applied'], 'HOLD')
        self.assertEqual(
            applied['graph']['nodes']['hist.ENV-RESCOV']['classification'],
            'HOLD',
        )
        self.assertFalse(applied['graph']['nodes']['hist.ENV-RESCOV']['controlling'])

    def test_green_ci_alone_never_promotes(self):
        for tokens in (
            ['GREEN_CI'],
            ['HASH_MATCH', 'NAVIGATION_SUCCESS'],
            ['SAME_AUTHOR_REVIEW', 'AUTHOR_SELF_CHECK', 'NUMERICAL_EXPERIMENT'],
            ['GREEN_CI', 'HASH_MATCH', 'ARCHITECTURAL_ADMISSION'],
        ):
            result = m.refuse_non_discharge_promotion(
                self.graph, 'math.rn-fixed-remote-window', tokens)
            self.assertTrue(result['refused'])
            self.assertFalse(result['allowed'])

    def test_unknown_evidence_token_refused(self):
        result = m.refuse_non_discharge_promotion(
            self.graph, 'math.p15-price-boundary', ['VIBES'])
        self.assertTrue(result['refused'])

    def test_refuted_price_boundary_is_terminal(self):
        node = self.graph['nodes']['math.p15-price-boundary']
        self.assertEqual(node['classification'], 'REFUTED')
        self.assertTrue(m.is_terminal('REFUTED'))

    def test_full_price_boundary_refutation_is_not_a_required_premise(self):
        decision = m.promotion_allowed(self.graph, 'math.p15-full-price')
        self.assertEqual(decision['required_dependencies'], [])
        self.assertEqual(decision['missing_terminal'], [])
        self.assertEqual(decision['blocked_absent'], [])
        self.assertEqual(decision['refuted_required'], [])
        self.assertFalse(decision['allowed'])  # own node remains author-side
        edge = next(e for e in self.graph['edges']
                    if e['from'] == 'math.p15-full-price'
                    and e['to'] == 'math.p15-price-boundary')
        self.assertFalse(edge['required'])
        self.assertIn('boundary', edge['relation'])

    def test_reverse_impact_marks_dependents(self):
        impact = m.reverse_impact(
            self.graph,
            'math.uniform-matrix-cap-lifetime',
            old_fingerprint='main-63-author-side',
            new_fingerprint='main-63-changed',
        )
        self.assertTrue(impact['dependency_changed'])
        self.assertIn('math.lifetime-remainder', impact['impacted'])
        self.assertIn('math.side24-coefficient', impact['impacted'])
        for nid in impact['impacted']:
            node = impact['graph']['nodes'][nid]
            self.assertEqual(node['classification'], 'REVALIDATION_REQUIRED')
            self.assertFalse(node['controlling'])

    def test_reverse_impact_no_change_is_noop(self):
        impact = m.reverse_impact(
            self.graph,
            'math.uniform-matrix-cap-lifetime',
            old_fingerprint='same',
            new_fingerprint='same',
        )
        self.assertFalse(impact['dependency_changed'])
        self.assertEqual(impact['impacted'], [])

    def test_classification_change_triggers_impact(self):
        impact = m.reverse_impact(
            self.graph,
            'math.rn-count-interface',
            old_classification='AUTHOR_SIDE_CANDIDATE',
            new_classification='REFUTED',
        )
        self.assertTrue(impact['dependency_changed'])
        self.assertIn('math.rn-fixed-remote-window', impact['impacted'])
        # Mesoscopic depends on fixed-remote, so transitive impact reaches it.
        self.assertIn('math.rn-mesoscopic-reduction', impact['impacted'])

    def test_illegal_controlling_detected(self):
        bad = copy.deepcopy(self.graph)
        bad['nodes']['math.lifetime-remainder']['controlling'] = True
        report = m.closure_report(bad)
        self.assertFalse(report['gate_ok'])
        self.assertEqual(len(report['illegal_controlling']), 1)
        self.assertEqual(report['illegal_controlling'][0]['node'], 'math.lifetime-remainder')

    def test_live_graph_has_no_illegal_controlling(self):
        report = m.closure_report(self.graph)
        self.assertTrue(report['gate_ok'])
        self.assertEqual(report['illegal_controlling'], [])

    def test_d4_region_complement(self):
        regions = m.d4_region_complement(self.graph)
        covered_ids = {r['id'] for r in regions['covered_by_fixed_remote_candidate']}
        open_ids = {r['id'] for r in regions['open_complement']}
        self.assertEqual(covered_ids, {'math.rn-region.fixed-remote'})
        self.assertIn('math.rn-region.mesoscopic-scaled-annulus', open_ids)
        self.assertIn('math.rn-region.pin-collision', open_ids)
        self.assertIn('math.rn-region.intermediate-r-to-rho', open_ids)
        self.assertIn('math.rn-region.witness-collision', open_ids)
        self.assertFalse(regions['legacy_24jet_discharged'])
        self.assertTrue(regions['no_event_to_expectation_reversal'])

    def test_selector_region_matrix(self):
        table = m.load_selector_region()
        self.assertEqual(table['schema_version'], 1)
        report = m.selector_region_report(table)
        self.assertFalse(report['legacy_24jet_discharged'])
        self.assertTrue(report['no_event_to_expectation_reversal'])
        self.assertEqual(report['covered_region_ids'], ['math.rn-region.fixed-remote'])
        # CH-LIFT is bypassed on fixed-remote but reopened on the mesoscopic annulus.
        ch = table['selectors']['CH-LIFT']
        self.assertEqual(ch['fixed-remote'], 'BYPASSED_BY_FIXED_RHO')
        self.assertEqual(ch['mesoscopic-scaled-annulus'], 'REOPENED')
        piece = table['selectors']['Piece-2-annulus']
        self.assertEqual(
            piece['mesoscopic-scaled-annulus'],
            'PARTIAL_PR7_REDUCTION_PLUS_PR9_CHART_ROWS',
        )
        # Every open complement region still has at least one non-closed selector cell.
        open_regions = {c['region'] for c in report['open_or_partial_cells']}
        for region in (
            'mesoscopic-scaled-annulus', 'pin-collision',
            'intermediate-r-to-rho', 'witness-collision',
        ):
            self.assertIn(region, open_regions)
        self.assertGreaterEqual(len(report['open_or_partial_cells']), 15)

    def test_d0_ci_unblock_patch_ready(self):
        report = m.d0_ci_unblock_report()
        self.assertTrue(report['ready'])
        self.assertEqual(report['cursor_main_push'], 'DENIED_403')
        self.assertEqual(report['patch_bytes'], 3096)
        self.assertEqual(
            report['patch_sha256'],
            '84b7ad724e4da1c5b4b396c90ae03d4ddedc37771a6e45e1082a45fd80d7ff4a',
        )
        self.assertIn('unexpected files', report['ci_error'])
        self.assertIs(report['lemma_closed'], False)

    def test_pr87_hold_until_allowlist(self):
        node = self.graph['nodes']['eng.main-pr87-crosswalk']
        self.assertEqual(node['classification'], 'HOLD')
        decision = m.promotion_allowed(self.graph, 'eng.main-pr87-crosswalk')
        self.assertFalse(decision['allowed'])
        self.assertIn('eng.d0-packet-allowlist-fix', decision['required_dependencies'])

    def test_layer_coverage_d0_through_d7(self):
        layers = {n['layer'] for n in self.graph['nodes'].values()}
        self.assertEqual(layers, {'D0', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7'})
        self.assertIn('eng.d0-packet-allowlist-fix', self.graph['nodes'])
        self.assertIn('math.rn-selector-region-crosswalk', self.graph['nodes'])

    def test_results_bytes_match(self):
        payload = m.results_payload(self.graph)
        pinned = json.loads((ROOT / 'RESULTS.json').read_text())
        self.assertEqual(payload, pinned)
        self.assertTrue(payload['illegal_promotion_refused'])
        self.assertIs(payload['lemma_closed'], False)
        self.assertTrue(payload['d0_ci_unblock']['ready'])
        self.assertGreaterEqual(payload['selector_region']['open_or_partial_cell_count'], 15)

    def test_author_side_with_terminal_deps_cannot_become_controlling(self):
        g = copy.deepcopy(self.graph)
        g['nodes']['math.p15-price-boundary']['classification'] = 'REFUTED'
        g['nodes']['math.p15-full-price']['classification'] = 'AUTHOR_SIDE_CANDIDATE'
        decision = m.promotion_allowed(g, 'math.p15-full-price')
        self.assertFalse(decision['allowed'])
        self.assertTrue(any('not eligible' in reason for reason in decision['reasons']))
        applied = m.apply_promotion(g, 'math.p15-full-price')
        self.assertFalse(applied['decision']['ok'])
        self.assertEqual(applied['decision']['applied'], 'REFUSED')
        self.assertFalse(applied['graph']['nodes']['math.p15-full-price']['controlling'])

    def test_proved_reviewed_with_satisfied_required_dep_may_control(self):
        g = copy.deepcopy(self.graph)
        g['nodes']['math.uniform-matrix-cap-lifetime']['classification'] = 'PROVED_REVIEWED'
        g['nodes']['math.lifetime-remainder']['classification'] = 'PROVED_REVIEWED'
        decision = m.promotion_allowed(g, 'math.lifetime-remainder')
        self.assertTrue(decision['allowed'])
        applied = m.apply_promotion(g, 'math.lifetime-remainder')
        self.assertTrue(applied['decision']['ok'])
        self.assertEqual(applied['decision']['applied'], 'CONTROLLING')

    def test_still_required_superseded_label_does_not_satisfy_edge(self):
        g = copy.deepcopy(self.graph)
        g['nodes']['math.uniform-matrix-cap-lifetime']['classification'] = 'SUPERSEDED_NONBLOCKING'
        g['nodes']['math.lifetime-remainder']['classification'] = 'PROVED_REVIEWED'
        decision = m.promotion_allowed(g, 'math.lifetime-remainder')
        self.assertFalse(decision['allowed'])
        self.assertTrue(any(x['classification'] == 'SUPERSEDED_NONBLOCKING'
                            for x in decision['missing_terminal']))

    def test_still_required_refuted_dependency_forces_hold(self):
        g = copy.deepcopy(self.graph)
        g['nodes']['math.uniform-matrix-cap-lifetime']['classification'] = 'REFUTED'
        g['nodes']['math.lifetime-remainder']['classification'] = 'PROVED_REVIEWED'
        decision = m.promotion_allowed(g, 'math.lifetime-remainder')
        self.assertFalse(decision['allowed'])
        self.assertEqual(decision['refuted_required'], ['math.uniform-matrix-cap-lifetime'])
        applied = m.apply_promotion(g, 'math.lifetime-remainder')
        self.assertEqual(applied['decision']['applied'], 'HOLD')
        self.assertFalse(applied['graph']['nodes']['math.lifetime-remainder']['controlling'])

    def test_union_reverse_impact_survives_deleted_edge(self):
        old = copy.deepcopy(self.graph)
        new = copy.deepcopy(self.graph)
        old['nodes']['math.uniform-matrix-cap-lifetime']['fingerprint'] = 'old'
        new['nodes']['math.uniform-matrix-cap-lifetime']['fingerprint'] = 'new'
        new['edges'] = [e for e in new['edges']
                        if not (e['from'] == 'math.lifetime-remainder'
                                and e['to'] == 'math.uniform-matrix-cap-lifetime')]
        impact = m.reverse_impact_between(old, new)
        self.assertIn('math.lifetime-remainder', impact['impacted'])
        self.assertEqual(
            impact['graph']['nodes']['math.lifetime-remainder']['classification'],
            'REVALIDATION_REQUIRED')

    def test_malformed_or_cycle_graph_fails_closed(self):
        bad = copy.deepcopy(self.graph)
        bad['edges'].append({'from': 'missing', 'to': 'math.p15-full-price',
                             'required': True, 'relation': 'bad'})
        with self.assertRaises(ValueError):
            m.validate_graph_fail_closed(bad)
        cyc = copy.deepcopy(self.graph)
        cyc['edges'].extend([
            {'from': 'math.lifetime-remainder', 'to': 'math.side24-coefficient',
             'required': True, 'relation': 'cycle'},
            {'from': 'math.side24-coefficient', 'to': 'math.lifetime-remainder',
             'required': True, 'relation': 'cycle'},
        ])
        with self.assertRaises(ValueError):
            m.validate_graph_fail_closed(cyc)

    def test_edge_targets_exist(self):
        nodes = self.graph['nodes']
        for edge in self.graph['edges']:
            self.assertIn(edge['from'], nodes)
            self.assertIn(edge['to'], nodes)
            self.assertIn('required', edge)
            self.assertIn('relation', edge)

    def test_non_discharge_list_complete_for_issue_90(self):
        required = {
            'GREEN_CI', 'HASH_MATCH', 'ARCHITECTURAL_ADMISSION',
            'NUMERICAL_EXPERIMENT', 'SAME_AUTHOR_REVIEW', 'NAVIGATION_SUCCESS',
        }
        self.assertTrue(required.issubset(set(self.graph['non_discharge_tokens'])))


if __name__ == '__main__':
    unittest.main()