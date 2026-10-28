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

    def diagnostic_specimen(self, purpose):
        # Explicit contracts, independent of the producer's graph construction.
        expected = {
            'promote_fixed_remote': ('diagnostic.fixed-remote', 'PROVED_REVIEWED',
                                     'diagnostic.count-interface', 'PROVED_REVIEWED'),
            'promote_lifetime_remainder': ('diagnostic.lifetime-remainder', 'AUTHOR_SIDE_CANDIDATE',
                                           'diagnostic.lifetime-parent', 'PROVED_REVIEWED'),
            'promote_side24': ('diagnostic.side24', 'AUTHOR_SIDE_CANDIDATE',
                               'diagnostic.side24-parent', 'PROVED_REVIEWED'),
            'promote_historical_env_rescov': ('diagnostic.historical-env', 'PROVED_REVIEWED',
                                             'diagnostic.absent-carrier', 'BLOCKED_ABSENT'),
            'promote_pr87_before_allowlist': ('diagnostic.crosswalk', 'PROVED_REVIEWED',
                                             'diagnostic.allowlist', 'AUTHOR_SIDE_CANDIDATE'),
        }
        self.assertTrue(hasattr(m, '_negative_control_specimens'), 'explicit diagnostic specimens required')
        specimens = m._negative_control_specimens()
        self.assertEqual(set(specimens), set(expected))
        for name, (target, own, premise, classification) in expected.items():
            with self.subTest(specimen=name):
                specimen = specimens[name]
                self.assertEqual(set(specimen), {'graph', 'node'})
                self.assertEqual(specimen['node'], target)
                g = specimen['graph']
                self.assertIs(type(g['schema_version']), int)
                self.assertEqual(g['schema_version'], 1)
                self.assertEqual(g['nodes'], {
                    target: {'classification': own, 'controlling': False},
                    premise: {'classification': classification, 'controlling': False},
                })
                for node in g['nodes'].values():
                    self.assertIs(node['controlling'], False)
                self.assertEqual(g['edges'], [
                    {'from': target, 'to': premise, 'required': True, 'relation': 'diagnostic prerequisite'}])
                self.assertIs(g['edges'][0]['required'], True)
                self.assertEqual(g['non_discharge_tokens'], [
                    'GREEN_CI', 'HASH_MATCH', 'ARCHITECTURAL_ADMISSION', 'NUMERICAL_EXPERIMENT',
                    'SAME_AUTHOR_REVIEW', 'NAVIGATION_SUCCESS', 'AUTHOR_SELF_CHECK'])
                m.validate_graph_fail_closed(g)
        target, _, premise, _ = expected[purpose]
        return specimens[purpose]['graph'], target, premise

    def check_target_and_premise_controls(self, purpose):
        g, target, premise = self.diagnostic_specimen(purpose)
        decision = m.promotion_allowed(g, target)
        self.assertIs(decision['allowed'], False)
        self.assertEqual(decision['missing_terminal'], [])
        self.assertEqual(decision['reasons'], [
            'node classification is not eligible for positive CONTROLLING status: AUTHOR_SIDE_CANDIDATE'])
        g['nodes'][target]['classification'] = 'PROVED_REVIEWED'
        allowed = m.promotion_allowed(g, target)
        self.assertIs(allowed['allowed'], True)
        self.assertEqual(allowed['reasons'], [])
        g['nodes'][premise]['classification'] = 'AUTHOR_SIDE_CANDIDATE'
        blocked = m.promotion_allowed(g, target)
        self.assertIs(blocked['allowed'], False)
        self.assertEqual(blocked['missing_terminal'], [
            {'id': premise, 'classification': 'AUTHOR_SIDE_CANDIDATE'}])
        self.assertEqual(blocked['reasons'], ['required transitive dependency is not satisfied'])

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
        self.assertEqual(deps.count('math.uniform-matrix-cap-lifetime'), 1)
        self.check_target_and_premise_controls('promote_lifetime_remainder')

    def test_d1_reading_rule_components_bound_and_reviewed(self):
        # Every mandatory reading-rule component is its own source node, required by D1, so a byte change
        # in any of them reaches D1, D2 and D3 through reverse impact. Each carries the review its role needs.
        d1 = 'math.uniform-matrix-cap-lifetime'
        roles = {
            'imports/lifetime_parent_20260925/ERRATUM_CONGRUENCE.md': 'amendment',
            'reviews/d1_section9_borel_repair_20260925/REPAIR.md': 'amendment',
            'imports/lifetime_parent_20260925/MARKED_CYLINDER_CAP_PROOF.md': 'deterministic_support',
            'reviews/d1_chain_reconciliation_20260928/': 'reading_rule_record',
        }
        nodes = self.graph['nodes']
        author = nodes[d1]['author_provider']
        components = [c for c in m.required_dependencies(self.graph, d1)]
        bound = {nodes[c]['source']: c for c in components}
        self.assertEqual(len(bound), len(components))
        self.assertEqual(set(bound), set(roles))
        for path, role in roles.items():
            node = nodes[bound[path]]
            self.assertEqual(node['classification'], 'PROVED_REVIEWED')
            self.assertFalse(node['controlling'])
            self.assertEqual((node['component_of'], node['component_role']), (d1, role))
            basis = node['review_basis']
            if role == 'reading_rule_record':
                self.assertNotEqual(node['author_provider'], author)
                self.assertFalse(any(author in (b.get('provider'), b.get('raised_by_provider')) for b in basis))
                self.assertTrue(node['technical_checks_non_discharge'])
                self.assertTrue(all(c['provider'] == author for c in node['technical_checks_non_discharge']))
            else:
                self.assertEqual(node['author_provider'], author)
                self.assertTrue(any(b['provider'] != author and b['verdict'] == 'ACCEPT' and b['depth'] == 'full'
                                    for b in basis))
        for child in ('math.lifetime-remainder', 'math.side24-coefficient'):
            self.assertTrue(set(components) <= set(m.transitive_required(self.graph, child)))
        # An unreviewed component still blocks both dependents.
        pre = copy.deepcopy(self.graph)
        pre['nodes'][bound['reviews/d1_section9_borel_repair_20260925/REPAIR.md']]['classification'] = 'AUTHOR_SIDE_CANDIDATE'
        decision = m.promotion_allowed(pre, 'math.side24-coefficient')
        self.assertIn(bound['reviews/d1_section9_borel_repair_20260925/REPAIR.md'],
                      [x['id'] for x in decision['missing_terminal']])

    def test_side24_requires_parent(self):
        self.assertIn('math.uniform-matrix-cap-lifetime',
                      m.transitive_required(self.graph, 'math.side24-coefficient'))
        self.check_target_and_premise_controls('promote_side24')

    def test_fixed_remote_requires_count_interface(self):
        deps = m.transitive_required(self.graph, 'math.rn-fixed-remote-window')
        self.assertIn('math.rn-count-interface', deps)
        g, target, premise = self.diagnostic_specimen('promote_fixed_remote')
        self.assertIs(m.promotion_allowed(g, target)['allowed'], True)
        g['nodes'][premise]['classification'] = 'AUTHOR_SIDE_CANDIDATE'
        decision = m.promotion_allowed(g, target)
        self.assertIs(decision['allowed'], False)
        self.assertEqual(decision['missing_terminal'], [
            {'id': premise, 'classification': 'AUTHOR_SIDE_CANDIDATE'}])
        self.assertEqual(decision['reasons'], ['required transitive dependency is not satisfied'])

    def test_mesoscopic_requires_fixed_remote(self):
        deps = m.required_dependencies(self.graph, 'math.rn-mesoscopic-reduction')
        self.assertEqual(deps, ['math.rn-fixed-remote-window'])

    def test_blocked_absent_forces_hold_on_historical_env(self):
        blocked = m.blocked_absent_hold(self.graph, 'hist.ENV-RESCOV')
        self.assertEqual(blocked, ['hist.rnu_env.py'])
        applied = m.apply_promotion(self.graph, 'hist.ENV-RESCOV')
        self.assertFalse(applied['decision']['ok'])
        self.assertEqual(applied['decision']['applied'], 'HOLD')
        self.assertEqual(applied['graph']['nodes']['hist.ENV-RESCOV']['classification'], 'HOLD')
        self.assertIs(applied['graph']['nodes']['hist.ENV-RESCOV']['controlling'], False)
        g, target, premise = self.diagnostic_specimen('promote_historical_env_rescov')
        decision = m.promotion_allowed(g, target)
        self.assertEqual(decision['blocked_absent'], [premise])
        self.assertEqual(decision['reasons'], ['required BLOCKED_ABSENT dependency forces HOLD'])
        self.assertIs(decision['allowed'], False)
        self.assertEqual(m.apply_promotion(g, target)['decision']['applied'], 'HOLD')
        g['nodes'][premise]['classification'] = 'PROVED_REVIEWED'
        self.assertIs(m.promotion_allowed(g, target)['allowed'], True)
        self.assertEqual(m.apply_promotion(g, target)['decision']['applied'], 'CONTROLLING')

    def test_green_ci_alone_never_promotes(self):
        g, target, _ = self.diagnostic_specimen('promote_fixed_remote')
        self.assertIs(m.promotion_allowed(g, target)['allowed'], True)
        for tokens in (
            ['GREEN_CI'],
            ['HASH_MATCH', 'NAVIGATION_SUCCESS'],
            ['SAME_AUTHOR_REVIEW', 'AUTHOR_SELF_CHECK', 'NUMERICAL_EXPERIMENT'],
            ['GREEN_CI', 'HASH_MATCH', 'ARCHITECTURAL_ADMISSION'],
            ['GREEN_CI', 'HASH_MATCH', 'SAME_AUTHOR_REVIEW'],
        ):
            result = m.refuse_non_discharge_promotion(g, target, tokens)
            self.assertIs(result['base']['allowed'], True)
            self.assertIs(result['refused'], True)
            self.assertIs(result['allowed'], False)
            self.assertEqual(result['reasons'], ['evidence consists only of non-discharge tokens'])
        positive = m.refuse_non_discharge_promotion(g, target, ['LINE_BY_LINE_ANALYTIC_REVIEW'])
        self.assertIs(positive['allowed'], True)
        self.assertIs(positive['refused'], False)
        self.assertEqual(positive['reasons'], [])

    def test_unknown_evidence_token_refused(self):
        result = m.refuse_non_discharge_promotion(
            self.graph, 'math.p15-price-boundary', ['VIBES'])
        self.assertTrue(result['refused'])

    def test_refuted_price_boundary_is_terminal(self):
        node = self.graph['nodes']['math.p15-price-boundary']
        self.assertEqual(node['classification'], 'REFUTED')
        self.assertTrue(m.is_terminal('REFUTED'))

    def test_full_price_boundary_refutation_is_not_a_required_premise(self):
        edge = next(e for e in self.graph['edges']
                    if e['from'] == 'math.p15-full-price'
                    and e['to'] == 'math.p15-price-boundary')
        self.assertIs(edge['required'], False)
        self.assertIn('boundary', edge['relation'])
        # Historical contextual boundary, with no required positive premise.
        g = {'schema_version': 1, 'nodes': {
            'diagnostic.price': {'classification': 'AUTHOR_SIDE_CANDIDATE', 'controlling': False},
            'diagnostic.boundary': {'classification': 'REFUTED', 'controlling': False},
        }, 'edges': [{'from': 'diagnostic.price', 'to': 'diagnostic.boundary',
                      'required': False, 'relation': 'contextual refuted boundary'}]}
        decision = m.promotion_allowed(g, 'diagnostic.price')
        for key in ('required_dependencies', 'missing_terminal', 'blocked_absent', 'refuted_required'):
            self.assertEqual(decision[key], [])
        self.assertIs(decision['allowed'], False)
        g['nodes']['diagnostic.price']['classification'] = 'PROVED_REVIEWED'
        self.assertIs(m.promotion_allowed(g, 'diagnostic.price')['allowed'], True)
        # Separately reviewed additional positive dependencies are legal.
        g['nodes']['diagnostic.positive'] = {'classification': 'PROVED_REVIEWED', 'controlling': False}
        g['edges'].append({'from': 'diagnostic.price', 'to': 'diagnostic.positive',
                           'required': True, 'relation': 'positive premise'})
        decision = m.promotion_allowed(g, 'diagnostic.price')
        self.assertIs(decision['allowed'], True)
        self.assertEqual(decision['required_dependencies'], ['diagnostic.positive'])
        self.assertEqual(decision['refuted_required'], [])

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
        # A small valid graph establishes the forbidden own-node precondition.
        target, parent = 'diagnostic.controlling', 'math.uniform-matrix-cap-lifetime'
        bad = {'schema_version': 1, 'nodes': {
            target: {'classification': 'AUTHOR_SIDE_CANDIDATE', 'controlling': True},
            parent: {'classification': 'PROVED_REVIEWED', 'controlling': False},
        }, 'edges': [{'from': target, 'to': parent, 'required': True, 'relation': 'premise'}]}
        frozen = copy.deepcopy(bad)
        report = m.closure_report(bad)
        self.assertIs(report['gate_ok'], False)
        self.assertEqual([d['node'] for d in report['illegal_controlling']], [target])
        self.assertEqual(report['illegal_controlling'][0]['reasons'], [
            'node classification is not eligible for positive CONTROLLING status: AUTHOR_SIDE_CANDIDATE'])
        payload = m.results_payload(bad)
        self.assertIs(payload['gate_ok'], False)
        self.assertEqual(payload['closure']['illegal_controlling_count'], 1)
        self.assertIs(payload['illegal_promotion_refused'], True)
        self.assertEqual(bad, frozen)
        good = copy.deepcopy(bad)
        good['nodes'][target]['classification'] = 'PROVED_REVIEWED'
        positive = m.closure_report(good)
        self.assertIs(positive['gate_ok'], True)
        self.assertEqual(positive['illegal_controlling'], [])
        self.assertIs(m.results_payload(good)['gate_ok'], True)

    def test_live_graph_has_no_illegal_controlling(self):
        report = m.closure_report(self.graph)
        self.assertTrue(report['gate_ok'])
        self.assertEqual(report['illegal_controlling'], [])

    def test_d4_region_complement(self):
        # Explicit classification categories; these are not eternal live statuses.
        categories = {
            'math.rn-region.fixed-remote': ('COVERED_BY_CANDIDATE', 'math.rn-fixed-remote-window'),
            'math.rn-region.fixed-annulus-window': ('COVERED_BY_CANDIDATE', 'math.rn-fixed-annulus-window'),
            'math.rn-region.mesoscopic-scaled-annulus': ('PROVED_REVIEWED', None),
            'math.rn-region.pin-collision': ('PROVED_REVIEWED', None),
            'math.rn-region.intermediate-r-to-rho': ('PROVED_REVIEWED', None),
            'math.rn-region.witness-collision': ('OPEN_ACTIVE', None),
        }
        g = {'schema_version': 1, 'nodes': {}, 'edges': []}
        for nid, (classification, source) in categories.items():
            self.assertEqual(self.graph['nodes'][nid]['kind'], 'region')
            g['nodes'][nid] = {'kind': 'region', 'classification': classification,
                               'controlling': False, 'coverage_source': source,
                               'fingerprint': 'explicit scoped fixture: ' + nid,
                               'notes': 'fixture source limits are not live closure evidence'}
        witness_note = ('sharp global order is reviewed and merged through Math-#145; '
                        'the regional shrinking mechanism remains open in this historical specimen')
        g['nodes']['math.rn-region.witness-collision']['notes'] = witness_note
        regions = m.d4_region_complement(g)
        expected = {
            'covered_by_fixed_remote_candidate': {'math.rn-region.fixed-remote'},
            'covered_by_other_scoped_candidates': {'math.rn-region.fixed-annulus-window'},
            'proved_reviewed_regions': {'math.rn-region.mesoscopic-scaled-annulus',
                                        'math.rn-region.pin-collision', 'math.rn-region.intermediate-r-to-rho'},
            'open_complement': {'math.rn-region.witness-collision'},
        }
        for bucket, ids in expected.items():
            self.assertEqual({r['id'] for r in regions[bucket]}, ids)
            for entry in regions[bucket]:
                for field in ('classification', 'coverage_source', 'fingerprint', 'notes'):
                    self.assertEqual(entry[field], g['nodes'][entry['id']][field])
        self.assertEqual(regions['open_complement'][0]['notes'], witness_note)
        self.assertIs(regions['legacy_24jet_discharged'], False)
        self.assertIs(regions['no_event_to_expectation_reversal'], True)

    def test_selector_region_matrix(self):
        live = m.load_selector_region()
        self.assertEqual(live['schema_version'], 1)
        self.assertIs(live['legacy_24jet_discharged'], False)
        self.assertIs(live['no_event_to_expectation_reversal'], True)
        regions = ['fixed-remote', 'mesoscopic-scaled-annulus', 'pin-collision',
                   'intermediate-r-to-rho', 'witness-collision']
        table = {'schema_version': 1, 'regions': regions,
                 'no_event_to_expectation_reversal': True, 'legacy_24jet_discharged': False,
                 'covered_region_ids': ['math.rn-region.fixed-remote'],
                 'open_region_ids': ['math.rn-region.' + r for r in regions[1:]],
                 'selectors': {
                     'CH-LIFT': dict(zip(regions, ['BYPASSED_BY_FIXED_RHO', 'REOPENED',
                                                  'OPEN_ACTIVE', 'NOT_DISCHARGED', 'NOT_APPLICABLE'])),
                     'diagnostic.all-categories': dict(zip(regions, ['PARTIAL_COVER_ONLY',
                         'PARTIAL_PR7_REDUCTION', 'OPEN_HISTORICAL', 'PARTIAL_COVER_DECLARED_REGION', 'NOT_REQUIRED']))}}
        table['selectors']['CH-LIFT']['notes'] = 'not a region cell'
        frozen = copy.deepcopy(table)
        report = m.selector_region_report(table)
        self.assertEqual(table, frozen)
        self.assertIs(report['legacy_24jet_discharged'], False)
        self.assertIs(report['no_event_to_expectation_reversal'], True)
        self.assertEqual(report['covered_region_ids'], ['math.rn-region.fixed-remote'])
        self.assertEqual(report['open_region_ids'], table['open_region_ids'])
        self.assertEqual({(c['selector'], c['region'], c['status']) for c in report['open_or_partial_cells']}, {
            ('CH-LIFT', 'mesoscopic-scaled-annulus', 'REOPENED'),
            ('CH-LIFT', 'pin-collision', 'OPEN_ACTIVE'),
            ('CH-LIFT', 'intermediate-r-to-rho', 'NOT_DISCHARGED'),
            ('diagnostic.all-categories', 'fixed-remote', 'PARTIAL_COVER_ONLY'),
            ('diagnostic.all-categories', 'mesoscopic-scaled-annulus', 'PARTIAL_PR7_REDUCTION'),
            ('diagnostic.all-categories', 'pin-collision', 'OPEN_HISTORICAL'),
            ('diagnostic.all-categories', 'intermediate-r-to-rho', 'PARTIAL_COVER_DECLARED_REGION')})
        self.assertEqual({(c['selector'], c['region'], c['status']) for c in report['covered_bypassed_or_na_cells']}, {
            ('CH-LIFT', 'fixed-remote', 'BYPASSED_BY_FIXED_RHO'),
            ('CH-LIFT', 'witness-collision', 'NOT_APPLICABLE'),
            ('diagnostic.all-categories', 'witness-collision', 'NOT_REQUIRED')})

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
        g, target, premise = self.diagnostic_specimen('promote_pr87_before_allowlist')
        decision = m.promotion_allowed(g, target)
        self.assertIs(decision['allowed'], False)
        self.assertEqual(decision['missing_terminal'], [{'id': premise, 'classification': 'AUTHOR_SIDE_CANDIDATE'}])
        self.assertEqual(decision['reasons'], ['required transitive dependency is not satisfied'])
        g['nodes'][premise]['classification'] = 'PROVED_REVIEWED'
        self.assertIs(m.promotion_allowed(g, target)['allowed'], True)

    def test_layer_coverage_d0_through_d7(self):
        layers = {n['layer'] for n in self.graph['nodes'].values()}
        self.assertEqual(layers, {'D0', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7'})
        self.assertIn('eng.d0-packet-allowlist-fix', self.graph['nodes'])
        self.assertIn('math.rn-selector-region-crosswalk', self.graph['nodes'])

    def test_results_bytes_match(self):
        frozen_graph = copy.deepcopy(self.graph)
        frozen_inputs = {name: (ROOT / name).read_bytes() for name in ('GRAPH.json', 'SELECTOR_REGION.json')}
        payload = m.results_payload(self.graph)
        # These direct predicates observe reporter mutants before any stale golden.
        self.assertIs(payload['lemma_closed'], False)
        self.assertEqual(payload['scientific_effect'], 'NONE')
        self.assertIs(payload['illegal_promotion_refused'], True)
        self.assertEqual(payload.get('illegal_attempts_context'), 'synthetic_negative_controls')
        self.assertEqual(payload, json.loads((ROOT / 'RESULTS.json').read_text()))
        self.assertTrue(payload['d0_ci_unblock']['ready'])
        table = json.loads(frozen_inputs['SELECTOR_REGION.json'])
        open_statuses = {'OPEN_ACTIVE', 'OPEN_HISTORICAL', 'NOT_DISCHARGED', 'PARTIAL_COVER_ONLY',
                         'PARTIAL_PR7_REDUCTION', 'REOPENED', 'PARTIAL_COVER_DECLARED_REGION'}
        count = sum(row[region] in open_statuses for row in table['selectors'].values() for region in table['regions'])
        self.assertEqual(payload['selector_region']['open_or_partial_cell_count'], count)
        self.assertEqual(payload['selector_region']['covered_bypassed_or_na_cell_count'],
                         len(table['selectors']) * len(table['regions']) - count)
        # Real statuses may become eligible without changing invariant diagnostics.
        eligible = copy.deepcopy(self.graph)
        for target in ('math.lifetime-remainder', 'math.side24-coefficient', 'math.rn-fixed-remote-window'):
            for nid in [target, *m.transitive_required(eligible, target)]:
                eligible['nodes'][nid]['classification'] = 'PROVED_REVIEWED'
            self.assertIs(m.promotion_allowed(eligible, target)['allowed'], True)
        later = m.results_payload(eligible)
        self.assertIs(later['illegal_promotion_refused'], True)
        self.assertEqual(later['illegal_attempts'], payload['illegal_attempts'])
        self.assertEqual(self.graph, frozen_graph)
        self.assertEqual({name: (ROOT / name).read_bytes() for name in frozen_inputs}, frozen_inputs)
        for invalid in ({}, [], '', 0):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                m.results_payload(invalid)

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


    def test_edge_only_deletion_seeds_changed_child(self):
        old = copy.deepcopy(self.graph)
        new = copy.deepcopy(self.graph)
        new['edges'] = [e for e in new['edges']
                        if not (e['from'] == 'math.lifetime-remainder'
                                and e['to'] == 'math.uniform-matrix-cap-lifetime')]
        impact = m.reverse_impact_between(old, new)
        self.assertIn('math.lifetime-remainder', impact['changed_nodes'])
        self.assertIn('math.lifetime-remainder', impact['impacted'])

    def test_required_true_to_false_seeds_changed_child(self):
        old = copy.deepcopy(self.graph)
        new = copy.deepcopy(self.graph)
        for e in new['edges']:
            if e['from'] == 'math.lifetime-remainder' and e['to'] == 'math.uniform-matrix-cap-lifetime':
                e['required'] = False
        impact = m.reverse_impact_between(old, new)
        self.assertIn('math.lifetime-remainder', impact['changed_nodes'])

    def test_statement_change_without_fingerprint_seeds_revalidation(self):
        old = copy.deepcopy(self.graph)
        new = copy.deepcopy(self.graph)
        nid = 'math.lifetime-remainder'
        new['nodes'][nid]['notes'] = str(new['nodes'][nid].get('notes', '')) + ' amended'
        impact = m.reverse_impact_between(old, new)
        self.assertIn(nid, impact['changed_nodes'])
        self.assertIn(nid, impact['impacted'])
        self.assertEqual(impact['graph']['nodes'][nid]['classification'], 'REVALIDATION_REQUIRED')

    def test_changed_controlling_node_holds_itself(self):
        old = copy.deepcopy(self.graph)
        new = copy.deepcopy(self.graph)
        nid = 'math.lifetime-remainder'
        old['nodes'][nid]['classification'] = 'PROVED_REVIEWED'
        old['nodes'][nid]['controlling'] = True
        new['nodes'][nid] = copy.deepcopy(old['nodes'][nid])
        new['nodes'][nid]['fingerprint'] = 'changed'
        impact = m.reverse_impact_between(old, new)
        self.assertIn(nid, impact['impacted'])
        self.assertFalse(impact['graph']['nodes'][nid]['controlling'])
        self.assertEqual(impact['graph']['nodes'][nid]['classification'], 'REVALIDATION_REQUIRED')

    def test_required_flag_must_be_exact_boolean(self):
        bad = copy.deepcopy(self.graph)
        bad['edges'][0]['required'] = 0
        with self.assertRaises(ValueError):
            m.validate_graph_fail_closed(bad)

    def test_controlling_flag_must_be_exact_boolean(self):
        bad = copy.deepcopy(self.graph)
        nid = next(iter(bad['nodes']))
        bad['nodes'][nid]['controlling'] = 0
        with self.assertRaises(ValueError):
            m.validate_graph_fail_closed(bad)

    def test_duplicate_edge_fails_closed(self):
        bad = copy.deepcopy(self.graph)
        bad['edges'].append(copy.deepcopy(bad['edges'][0]))
        with self.assertRaises(ValueError):
            m.validate_graph_fail_closed(bad)


if __name__ == '__main__':
    unittest.main()
