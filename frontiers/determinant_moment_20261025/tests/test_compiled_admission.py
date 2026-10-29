"""CBZ regression controls. Protocol text below is synthetic unit input, never Lean evidence."""
import copy
import importlib.util
import json
import os
import shutil
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('cbz_candidate_gate', ROOT / 'gate.py')
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)
MODULE = 'ResearchFormalCoreR1.AlgebraV2'
TARGET = 'ResearchFormalCoreR1.ec005_fold_gap'


def enc(name):
    return '/'.join('n' + str(x) if isinstance(x, int) else 's' + x.encode().hex()
                    for x in name)


def transcript(extra=(), axioms=(), closure=20, modules=None):
    # Independent, hand-sized protocol fixture: one public theorem, no hidden defaults.
    rows = [('theorem', 'user', tuple(MODULE.split('.')), tuple(TARGET.split('.')))] + list(extra)
    result = ['MODULE|' + enc(('ResearchFormalCoreR1',)) + '|false|0|0',
              'MODULE|' + enc(tuple(MODULE.split('.'))) + '|false|' + str(len(rows)) + '|0']
    if modules is not None:
        result = modules
    result += ['INV|' + k + '|' + o + '|' + enc(m) + '|' + enc(n) for k, o, m, n in rows]
    result += ['AXIOMS|' + ','.join(enc(tuple(a.split('.'))) for a in axioms),
               'CLOSURE|' + str(closure)]
    return '\n'.join(result) + '\n'


def manifest():
    return {'targets': [TARGET], 'source_modules': ['ResearchFormalCoreR1/AlgebraV2.lean'],
            'compiled_inventory': []}


class CompiledAdmissionTests(unittest.TestCase):
    def audit(self, text, m=None, reported=None):
        self.assertTrue(callable(getattr(gate, 'audit_compiled', None)),
                        'compiled-package admission is missing')
        return gate.audit_compiled(text, m or manifest(), reported or {TARGET: []})

    def test_current_cli_refuses_unknown_compiled_inventory(self):
        # A source-only regex pass must not return a successful gate status.
        run = subprocess.run([sys.executable, '-B', '-S', str(ROOT / 'gate.py')],
                             cwd=ROOT, capture_output=True, text=True)
        self.assertNotEqual(run.returncode, 0, 'unqualified package returned green')
        self.assertIn('CBZ_COMPILED_INVENTORY_UNQUALIFIED', run.stderr)
        self.assertNotIn('SOURCE_IDENTITY_PASS', run.stdout)

    def test_execute_refuses_before_external_process_without_compiled_binding(self):
        previous = gate.ROOT
        with tempfile.TemporaryDirectory() as d:
            gate.ROOT = Path(d)
            try:
                with patch.object(gate, 'run', side_effect=AssertionError('external execution before qualification')):
                    with self.assertRaisesRegex(ValueError, 'CBZ_COMPILED_INVENTORY_UNQUALIFIED'):
                        gate.execute({'targets': [TARGET], 'source_modules': ['ResearchFormalCoreR1/AlgebraV2.lean']}, 'a' * 64)
                self.assertFalse((gate.ROOT / '.lake/formal-evidence/receipt.json').exists())
            finally:
                gate.ROOT = previous

    def test_clean_compiled_inventory_accepts(self):
        result = self.audit(transcript())
        self.assertEqual(result['public_theorems'], [TARGET])
        self.assertEqual(result['axioms'], [])

    def test_missing_binding_removes_a_stale_receipt_on_execute(self):
        previous = gate.ROOT
        with tempfile.TemporaryDirectory() as d:
            gate.ROOT = Path(d)
            stale = gate.ROOT / '.lake/formal-evidence/receipt.json'
            stale.parent.mkdir(parents=True)
            stale.write_text('{"synthetic_test_fixture": "stale"}')
            try:
                with self.assertRaisesRegex(ValueError, 'CBZ_COMPILED_INVENTORY_UNQUALIFIED'):
                    gate.execute({'targets': [TARGET], 'source_modules': ['ResearchFormalCoreR1/AlgebraV2.lean']}, 'a' * 64)
                self.assertFalse(stale.exists(), 'stale receipt survived a refused execution')
            finally:
                gate.ROOT = previous

    def test_source_only_cli_never_reports_kernel_gate_success(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / 'component'
            shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns('.lake', '__pycache__'))
            m = json.loads((root / 'manifest.json').read_text())
            m['compiled_inventory'] = []  # Synthetic binding, not observed Lean constants.
            (root / 'manifest.json').write_text(json.dumps(m))
            run = subprocess.run([sys.executable, '-B', '-S', str(root / 'gate.py')],
                                 cwd=root, capture_output=True, text=True)
            self.assertNotEqual(run.returncode, 0)
            self.assertIn('CBZ_KERNEL_EXECUTION_REQUIRED', run.stderr)
            self.assertNotIn('SOURCE_IDENTITY_PASS', run.stdout)

    def test_indented_forbidden_theorem_cannot_hide_behind_green_public_target(self):
        # The predecessor public-only axiom audit is genuinely green on this input.
        self.assertEqual(gate.audit_axioms("'" + TARGET + "' does not depend on any axioms", [TARGET]),
                         {TARGET: []})
        extra = [('theorem', 'user', tuple(MODULE.split('.')), ('ResearchFormalCoreR1', 'hiddenIndented'))]
        with self.assertRaisesRegex(ValueError, 'extra_theorem.*hiddenIndented|forbidden_axiom.*sorryAx'):
            self.audit(transcript(extra, ['sorryAx']))

    def test_unlisted_axiom_free_theorem_is_rejected(self):
        extra = [('theorem', 'user', tuple(MODULE.split('.')), ('ResearchFormalCoreR1', 'hiddenIndented'))]
        with self.assertRaisesRegex(ValueError, 'extra_theorem'):
            self.audit(transcript(extra))

    def test_unused_custom_axiom_is_rejected(self):
        extra = [('axiom', 'user', tuple(MODULE.split('.')), ('ResearchFormalCoreR1', 'unusedPremise'))]
        with self.assertRaisesRegex(ValueError, 'package_axiom|forbidden_axiom'):
            self.audit(transcript(extra, ['ResearchFormalCoreR1.unusedPremise']))

    def test_unused_definition_forbidden_closure_is_rejected(self):
        m = manifest()
        m['compiled_inventory'] = [['def', 'user', MODULE, 'ResearchFormalCoreR1.unusedDefinition']]
        extra = [('def', 'user', tuple(MODULE.split('.')), ('ResearchFormalCoreR1', 'unusedDefinition'))]
        with self.assertRaisesRegex(ValueError, 'forbidden_axiom'):
            self.audit(transcript(extra, ['Hidden.importedAxiom']), m)

    def test_unbound_compiler_shaped_theorem_is_rejected(self):
        extra = [('theorem', 'aux', tuple(MODULE.split('.')), tuple(TARGET.split('.')) + ('_proof_999',))]
        with self.assertRaisesRegex(ValueError, 'unregistered_constant'):
            self.audit(transcript(extra))

    def test_omitted_bound_definition_is_rejected(self):
        m = manifest()
        m['compiled_inventory'] = [['def', 'user', MODULE, 'ResearchFormalCoreR1.requiredDefinition']]
        with self.assertRaisesRegex(ValueError, 'missing_constant'):
            self.audit(transcript(), m)

    def test_missing_module_is_rejected(self):
        m = manifest()
        m['source_modules'].append('ResearchFormalCoreR1/Missing.lean')
        with self.assertRaisesRegex(ValueError, 'missing_module'):
            self.audit(transcript(), m)

    def test_duplicate_module_is_rejected(self):
        root = 'MODULE|' + enc(('ResearchFormalCoreR1',)) + '|false|0|0'
        module = 'MODULE|' + enc(tuple(MODULE.split('.'))) + '|false|1|0'
        with self.assertRaisesRegex(ValueError, 'duplicate_module'):
            self.audit(transcript(modules=[root, module, module]))

    def test_target_axiom_cannot_disappear_from_package_closure(self):
        with self.assertRaisesRegex(ValueError, 'reported_axiom_omitted'):
            self.audit(transcript(), reported={TARGET: ['Classical.choice']})

    def test_empty_or_missing_closure_output_is_rejected(self):
        for text in ('', transcript().replace('AXIOMS|\n', ''), transcript().replace('CLOSURE|20\n', '')):
            with self.subTest(text=text), self.assertRaises(ValueError):
                self.audit(text)

    def test_impossible_closure_size_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'impossible_closure'):
            self.audit(transcript(closure=0))

    def test_forged_bound_user_theorem_is_rejected(self):
        m = manifest()
        m['compiled_inventory'] = [['theorem', 'user', MODULE, 'ResearchFormalCoreR1.hiddenIndented']]
        with self.assertRaisesRegex(ValueError, 'user-written theorems belong in targets'):
            self.audit(transcript(), m)

    def test_noncanonical_source_module_path_is_rejected(self):
        m = manifest()
        m['source_modules'] = ['ResearchFormalCoreR1/../Hidden.lean']
        with self.assertRaisesRegex(ValueError, 'source module'):
            self.audit(transcript(), m)


if __name__ == '__main__':
    unittest.main()

