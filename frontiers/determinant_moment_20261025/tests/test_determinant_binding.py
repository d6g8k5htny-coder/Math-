"""Version-2 integration controls using an authenticated historical Lean census.

These are Python policy tests; they do not execute Lean or qualify this gate.
"""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('determinant_binding_gate', ROOT / 'gate.py')
gate = importlib.util.module_from_spec(SPEC)
exec(compile((ROOT / 'gate.py').read_bytes(), str(ROOT / 'gate.py'), 'exec'), gate.__dict__)


class DeterminantBindingTests(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads((ROOT / 'tests/fixtures/actual_manifest_v2_fields.json').read_text())
        adapter = ROOT / 'determinant_inventory.py'
        self.manifest['files'] = {'determinant_inventory.py': hashlib.sha256(adapter.read_bytes()).hexdigest()
                                  if adapter.exists() else '0' * 64}
        self.text = (ROOT / 'tests/fixtures/actual_inventory_4ccc.log').read_text()

    def test_actual_typed_binding_admits_every_compiled_constant(self):
        report = gate.audit_compiled(self.text, self.manifest, {})
        self.assertEqual(report['declarations'], 157)
        self.assertEqual(report['internal_user_proofs'], 20)
        self.assertEqual(report['auxiliary_theorems'], 51)
        self.assertEqual(report['closure'], 58421)
        self.assertEqual(report['kernel_or_cbz_status'], 'NOT_AWARDED')

    def test_version_two_closure_cannot_hide_a_non_target_axiom(self):
        text = self.text.replace('AXIOMS|', 'AXIOMS|s48696464656e/s556e617070726f766564,')
        with self.assertRaisesRegex(ValueError, 'forbidden_axiom'):
            gate.audit_compiled(text, self.manifest, {})

    def test_version_two_adapter_identity_is_required_before_policy_execution(self):
        m = copy.deepcopy(self.manifest)
        m['files']['determinant_inventory.py'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'determinant adapter source hash mismatch'):
            gate.audit_compiled(self.text, m, {})

    def test_unsupported_inventory_version_cannot_select_a_legacy_policy(self):
        m = copy.deepcopy(self.manifest)
        m['compiled_inventory_version'] = 3
        with self.assertRaisesRegex(ValueError, 'unsupported compiled inventory version'):
            gate.audit_compiled(self.text, m, {})


if __name__ == '__main__':
    unittest.main()
