"""Negative controls for the Layer 1 formal gate. Software behavior only; scientific effect NONE."""
from __future__ import annotations

import contextlib
import hashlib
import io
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import formal_gate as gate  # noqa: E402

COPY = (
    'formal/FORMALIZATION_STATUS.json',
    'formal/FORMAL_RESULTS.json',
    'claims/LANDING_CLAIMS.json',
    'frontiers/downstream_gate_20260925/hard_gate.py',
    'frontiers/downstream_gate_20260925/GRAPH.json',
)


def make_fixture(root: Path) -> None:
    for rel in COPY:
        dst = root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / rel, dst)
    src = ROOT / 'formal' / 'lean'
    shutil.copytree(src, root / 'formal' / 'lean', ignore=shutil.ignore_patterns('.lake'))


class FormalGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        make_fixture(self.root)
        self.registry_path = self.root / 'formal' / 'FORMALIZATION_STATUS.json'

    def tearDown(self):
        self.tmp.cleanup()

    # ----------------------------------------------------------------- helpers
    def registry(self) -> dict:
        return gate.strict_json(self.registry_path.read_text())

    def write_registry(self, reg: dict) -> None:
        self.registry_path.write_text(json.dumps(reg, indent=2) + '\n')

    def entry(self, reg: dict, claim_id: str = 'side24-coefficient') -> dict:
        return next(e for e in reg['entries'] if e['claim_id'] == claim_id)

    def assertRefused(self, fragment: str) -> None:
        with self.assertRaises(gate.FormalGateError) as ctx:
            gate.validate(self.root)
        self.assertIn(fragment, str(ctx.exception))

    def repin(self) -> None:
        gate.refresh_pins(self.root)

    # ----------------------------------------------------------------- positive
    def test_live_registry_validates_and_results_are_pinned(self):
        report = gate.validate(ROOT)
        self.assertEqual(report['claims_covered'], 10)
        self.assertFalse(report['promotion_permission'])
        self.assertFalse(report['lemma_closed'])
        self.assertEqual(report['scientific_effect'], 'NONE')
        pinned = (ROOT / 'formal' / 'FORMAL_RESULTS.json').read_text()
        self.assertEqual(json.dumps(report, indent=2, sort_keys=True) + '\n', pinned)

    def test_pilot_lane_is_specified_not_kernel_checked(self):
        report = gate.validate(self.root)
        lane = report['lanes']['side24-coefficient']
        self.assertEqual(lane['status'], 'specified')
        self.assertEqual(lane['lane_verdict'], 'FORMAL_SPECIFIED')
        self.assertEqual(lane['alignment'], 'REVIEW_REQUIRED')
        self.assertGreater(lane['component_counts']['kernel_checked'], 0)
        for cid, lane in report['lanes'].items():
            if cid != 'side24-coefficient':
                self.assertEqual(lane['lane_verdict'], 'FORMAL_NONE')

    def test_layer0_refuses_every_formal_token_alone(self):
        report = gate.validate(self.root)
        for record in report['layer0_composition'].values():
            self.assertFalse(record['layer0_promotion_allowed'])
            self.assertEqual(set(record['formal_tokens_alone'].values()), {'REFUSED'})

    def test_fixture_copy_validates(self):
        self.assertEqual(gate.validate(self.root)['claims_covered'], 10)

    # ----------------------------------------------------------------- vocabulary
    def test_promotion_permission_true_refused(self):
        reg = self.registry(); reg['promotion_permission'] = True; self.write_registry(reg)
        self.assertRefused('promotion_permission')

    def test_lemma_closed_true_refused(self):
        reg = self.registry(); reg['lemma_closed'] = True; self.write_registry(reg)
        self.assertRefused('lemma_closed')

    def test_extra_allowed_axiom_refused(self):
        reg = self.registry(); reg['allowed_axioms'].append('Lean.ofReduceBool'); self.write_registry(reg)
        self.assertRefused('allowed_axioms')

    def test_unknown_status_refused(self):
        reg = self.registry(); self.entry(reg)['status'] = 'verified'; self.write_registry(reg)
        self.assertRefused('unknown status')

    def test_duplicate_json_key_refused(self):
        text = self.registry_path.read_text().replace('"schema_version": 1,', '"schema_version": 1,\n  "schema_version": 1,', 1)
        self.registry_path.write_text(text)
        self.assertRefused('duplicate JSON key')

    # ----------------------------------------------------------------- claim coverage
    def test_missing_claim_refused(self):
        reg = self.registry(); reg['entries'] = [e for e in reg['entries'] if e['claim_id'] != 'p15-full-price']; self.write_registry(reg)
        self.assertRefused('missing=')

    def test_unknown_claim_refused(self):
        reg = self.registry()
        reg['entries'].append({**self.entry(reg, 'p15-full-price'), 'claim_id': 'invented-claim'})
        self.write_registry(reg)
        self.assertRefused('unknown=')

    def test_informal_blob_drift_refused(self):
        reg = self.registry(); self.entry(reg)['informal']['blob'] = '0' * 40; self.write_registry(reg)
        self.assertRefused('alignment is stale')

    def test_unknown_graph_node_refused(self):
        reg = self.registry(); self.entry(reg)['graph_node'] = 'math.invented'; self.write_registry(reg)
        self.assertRefused('not in the dependency graph')

    # ----------------------------------------------------------------- status consistency
    def test_specified_claim_cannot_claim_theorem_statement(self):
        reg = self.registry(); self.entry(reg)['statement']['kind'] = 'theorem'; self.write_registry(reg)
        self.assertRefused('specified requires a prop_specification')

    def test_kernel_checked_claim_requires_theorem_statement(self):
        reg = self.registry(); self.entry(reg)['status'] = 'kernel_checked'; self.write_registry(reg)
        self.assertRefused('requires a theorem statement')

    def test_kernel_checked_claim_with_prop_decl_relabeled_as_theorem_refused(self):
        reg = self.registry()
        e = self.entry(reg); e['status'] = 'kernel_checked'; e['statement']['kind'] = 'theorem'
        self.write_registry(reg)
        self.assertRefused('not found as theorem')

    def test_kernel_checked_component_absent_from_audit_refused(self):
        reg = self.registry()
        comp = next(c for c in self.entry(reg)['components'] if c['id'] == 'image-constant')
        comp['decl'] = 'MathFormalCore.Side24.imageConstant'
        self.write_registry(reg)
        self.assertRefused('not found as theorem')

    def test_theorem_missing_from_pinned_audit_refused(self):
        reg = self.registry()
        audit = self.root / 'formal' / 'lean' / 'core' / 'AXIOMS.expected'
        lines = [l for l in audit.read_text().splitlines() if 'imageConstant_eq' not in l]
        audit.write_text('\n'.join(lines) + '\n')
        self.write_registry(reg); self.repin()
        self.assertRefused('absent from the pinned axiom audit')

    def test_specification_registered_but_audited_as_theorem_refused(self):
        reg = self.registry()
        comp = next(c for c in self.entry(reg)['components'] if c['id'] == 'transfer-lemma')
        comp['kind'] = 'prop_specification'; comp['status'] = 'specified'
        self.write_registry(reg)
        self.assertRefused('not found as prop_specification')

    def test_theorem_component_status_specified_refused(self):
        reg = self.registry()
        comp = next(c for c in self.entry(reg)['components'] if c['id'] == 'transfer-lemma')
        comp['status'] = 'specified'
        self.write_registry(reg)
        self.assertRefused('theorem status must be proved or kernel_checked')

    def test_none_claim_with_components_refused(self):
        reg = self.registry()
        e = self.entry(reg, 'p15-full-price'); e['components'] = [self.entry(reg)['components'][0]]
        self.write_registry(reg)
        self.assertRefused('status none forbids')

    def test_prose_interface_requires_note(self):
        reg = self.registry()
        comp = next(c for c in self.entry(reg)['components'] if c['kind'] == 'interface')
        del comp['note']
        self.write_registry(reg)
        self.assertRefused('requires a note')

    # ----------------------------------------------------------------- Lean sources
    def test_lean_source_drift_refused(self):
        path = self.root / 'formal' / 'lean' / 'core' / 'MathFormalCore' / 'Side24' / 'Arithmetic.lean'
        path.write_text(path.read_text().replace('21175738586478', '21175738586479'))
        self.assertRefused('pinned Lean source drift')

    def test_sorry_refused_even_when_repinned(self):
        path = self.root / 'formal' / 'lean' / 'core' / 'MathFormalCore' / 'Side24' / 'Arithmetic.lean'
        path.write_text(path.read_text().replace(':= by decide\n', ':= by sorry\n', 1))
        self.repin()
        self.assertRefused('forbidden construct (sorry)')

    def test_native_decide_refused_even_when_repinned(self):
        path = self.root / 'formal' / 'lean' / 'core' / 'MathFormalCore' / 'Side24' / 'Arithmetic.lean'
        path.write_text(path.read_text().replace(':= by decide\n', ':= by native_decide\n', 1))
        self.repin()
        self.assertRefused('forbidden construct (native_decide)')

    def test_axiom_declaration_refused_even_when_repinned(self):
        path = self.root / 'formal' / 'lean' / 'core' / 'MathFormalCore' / 'Side24' / 'Arithmetic.lean'
        path.write_text(path.read_text().replace('end MathFormalCore.Side24', 'axiom parent : True\n\nend MathFormalCore.Side24'))
        self.repin()
        self.assertRefused('forbidden construct (axiom declaration)')

    def test_unpinned_new_lean_file_refused(self):
        (self.root / 'formal' / 'lean' / 'core' / 'MathFormalCore' / 'Extra.lean').write_text('theorem t : True := trivial\n')
        self.assertRefused('unpinned Lean source')

    def test_forbidden_axiom_in_pinned_audit_refused(self):
        audit = self.root / 'formal' / 'lean' / 'core' / 'AXIOMS.expected'
        audit.write_text(audit.read_text().replace('imageConstant_eq -', 'imageConstant_eq sorryAx'))
        self.repin()
        self.assertRefused('non-allowed axioms')

    def test_toolchain_mismatch_refused(self):
        (self.root / 'formal' / 'lean' / 'core' / 'lean-toolchain').write_text('leanprover/lean4:v4.0.0\n')
        self.repin()
        self.assertRefused('toolchain')

    def test_mathlib_manifest_commit_mismatch_refused(self):
        reg = self.registry(); reg['toolchain']['mathlib']['commit'] = '1' * 40; self.write_registry(reg)
        self.assertRefused('Mathlib commit differs')

    def test_module_outside_library_refused(self):
        reg = self.registry(); self.entry(reg)['statement']['module'] = 'Mathlib.Data.Real.Basic'; self.write_registry(reg)
        self.assertRefused('outside library')

    # ----------------------------------------------------------------- alignment lane
    def test_alignment_accept_without_record_refused(self):
        reg = self.registry(); self.entry(reg)['alignment_review'] = {'status': 'ACCEPT', 'record': None}; self.write_registry(reg)
        self.assertRefused('requires a record')

    def test_alignment_accept_by_formal_author_refused(self):
        reg = self.registry()
        e = self.entry(reg)
        record_path = self.root / 'reviews' / 'formal_alignment_side24' / 'REVIEW.md'
        record_path.parent.mkdir(parents=True)
        record_path.write_text('# alignment review\n')
        raw = record_path.read_bytes()
        e['alignment_review'] = {'status': 'ACCEPT', 'record': {
            'path': 'reviews/formal_alignment_side24/REVIEW.md',
            'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
            'reviewer': {'provider': 'anthropic', 'agent': 'cursor[bot]'},
            'organizational_independence': False,
            'reviewed_informal_blob': e['informal']['blob'],
            'reviewed_sources': {k: v for k, v in reg['sources'].items() if k.endswith('.lean')},
        }}
        self.write_registry(reg)
        self.assertRefused('distinct agent/session')

    def test_alignment_accept_valid_record_yields_author_side_verdict_only_when_kernel_checked(self):
        reg = self.registry()
        e = self.entry(reg)
        record_path = self.root / 'reviews' / 'formal_alignment_side24' / 'REVIEW.md'
        record_path.parent.mkdir(parents=True)
        record_path.write_text('# alignment review\n')
        raw = record_path.read_bytes()
        e['alignment_review'] = {'status': 'ACCEPT', 'record': {
            'path': 'reviews/formal_alignment_side24/REVIEW.md',
            'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
            'reviewer': {'provider': 'xai', 'agent': 'grok-review-session'},
            'organizational_independence': False,
            'reviewed_informal_blob': e['informal']['blob'],
            'reviewed_sources': {k: v for k, v in reg['sources'].items() if k.endswith('.lean')},
        }}
        self.write_registry(reg)
        report = gate.validate(self.root)
        # Alignment ACCEPT on a merely specified claim does not make it kernel-checked/aligned.
        self.assertEqual(report['lanes']['side24-coefficient']['lane_verdict'], 'FORMAL_SPECIFIED')
        self.assertFalse(report['layer0_composition']['side24-coefficient']['layer0_promotion_allowed'])

    def test_alignment_record_with_stale_lean_source_refused(self):
        reg = self.registry()
        e = self.entry(reg)
        record_path = self.root / 'reviews' / 'formal_alignment_side24' / 'REVIEW.md'
        record_path.parent.mkdir(parents=True)
        record_path.write_text('# alignment review\n')
        raw = record_path.read_bytes()
        stale = {k: {'bytes': v['bytes'], 'sha256': 'f' * 64} for k, v in reg['sources'].items() if k.endswith('.lean')}
        e['alignment_review'] = {'status': 'ACCEPT', 'record': {
            'path': 'reviews/formal_alignment_side24/REVIEW.md',
            'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
            'reviewer': {'provider': 'xai', 'agent': 'grok-review-session'},
            'organizational_independence': False,
            'reviewed_informal_blob': e['informal']['blob'],
            'reviewed_sources': stale,
        }}
        self.write_registry(reg)
        self.assertRefused('stale Lean source')

    def test_unformalized_claim_cannot_carry_alignment(self):
        reg = self.registry(); self.entry(reg, 'p15-full-price')['alignment_review'] = {'status': 'REVIEW_REQUIRED', 'record': None}; self.write_registry(reg)
        self.assertRefused('cannot carry an alignment review')

    # ----------------------------------------------------------------- Layer 0 composition
    def test_controlling_node_observed_refused(self):
        graph_path = self.root / 'frontiers' / 'downstream_gate_20260925' / 'GRAPH.json'
        graph = json.loads(graph_path.read_text())
        graph['nodes']['math.side24-coefficient']['controlling'] = True
        graph_path.write_text(json.dumps(graph, indent=2) + '\n')
        self.assertRefused('controlling node')

    def test_axiom_audit_parser_rejects_malformed_line(self):
        with self.assertRaises(gate.FormalGateError):
            gate.parse_axiom_audit('MathFormalCore.Side24.x propext extra\n')
        table = gate.parse_axiom_audit('scripts/Axioms.lean:1:0: info: MathFormalCore.Side24.x -\nMathFormalCore.Side24.y propext,Quot.sound\n')
        self.assertEqual(table, {'MathFormalCore.Side24.x': [], 'MathFormalCore.Side24.y': ['propext', 'Quot.sound']})

    def test_lane_verdict_table(self):
        base = {'alignment_review': {'status': 'REVIEW_REQUIRED'}}
        self.assertEqual(gate.lane_verdict({**base, 'status': 'none'}), 'FORMAL_NONE')
        self.assertEqual(gate.lane_verdict({**base, 'status': 'specified'}), 'FORMAL_SPECIFIED')
        self.assertEqual(gate.lane_verdict({**base, 'status': 'proved'}), 'FORMAL_PROVED_UNREPLAYED')
        self.assertEqual(gate.lane_verdict({**base, 'status': 'kernel_checked'}), 'FORMAL_KERNEL_CHECKED_AUTHOR_SIDE')
        self.assertEqual(gate.lane_verdict({'status': 'kernel_checked', 'alignment_review': {'status': 'ACCEPT'}}),
                         'FORMAL_KERNEL_CHECKED_ALIGNED')

    def test_cli_refuses_results_drift(self):
        (self.root / 'formal' / 'FORMAL_RESULTS.json').write_text('{}\n')
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(gate.main(['--root', str(self.root)]), 2)
            self.assertEqual(gate.main(['--root', str(self.root), '--no-results-check']), 0)


if __name__ == '__main__':
    unittest.main()
