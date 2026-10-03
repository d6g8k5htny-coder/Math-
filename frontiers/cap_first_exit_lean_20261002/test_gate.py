"""Unit tests for gate.py (standard library only; no Lean needed)."""
import json
import pathlib
import shutil
import sys
import tempfile
import unittest

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import gate  # noqa: E402

ALLOWED = ['propext', 'Classical.choice', 'Quot.sound']


class SourceGate(unittest.TestCase):
    def test_tree_passes(self):
        m = gate.source_check()
        self.assertEqual(len(m["targets"]), 64)
        self.assertEqual(m['scientific_effect'], 'NONE')

    def copy(self):
        tmp = pathlib.Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp)
        repo = tmp / 'repo'
        packet = repo / 'frontiers' / HERE.name
        packet.mkdir(parents=True)
        for p in HERE.iterdir():
            if p.is_file():
                shutil.copy2(p, packet / p.name)
        m = json.loads((HERE / 'MANIFEST.json').read_text())
        for pin in m['pins_on_main']:
            dst = repo / pin['path']
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(gate.REPO / pin['path'], dst)
        return repo, packet

    def assertGateFails(self, repo, packet, fragment):
        with self.assertRaises(ValueError) as ctx:
            gate.source_check(packet, repo)
        self.assertIn(fragment, str(ctx.exception))

    def test_copy_passes(self):
        repo, packet = self.copy()
        gate.source_check(packet, repo)

    def test_modified_lean_rejected(self):
        repo, packet = self.copy()
        p = packet / 'CapFirstExit.lean'
        p.write_text(p.read_text().replace('h ≤ s := by', 'h < s := by', 1))
        self.assertGateFails(repo, packet, 'source identity mismatch')

    def test_extra_file_rejected(self):
        repo, packet = self.copy()
        (packet / 'Extra.lean').write_text('import Mathlib\n')
        self.assertGateFails(repo, packet, 'packet tree differs')

    def test_pin_drift_rejected(self):
        repo, packet = self.copy()
        m = json.loads((HERE / 'MANIFEST.json').read_text())
        p = repo / m['pins_on_main'][0]['path']
        p.write_bytes(p.read_bytes() + b'\n')
        self.assertGateFails(repo, packet, 'pinned source drifted')


class Tokens(unittest.TestCase):
    def test_comments_ignored(self):
        self.assertEqual(gate.forbidden_tokens('/- sorry -/\n-- axiom\ntheorem t : True := trivial\n'), [])

    def test_nested_comment(self):
        self.assertEqual(gate.forbidden_tokens('/- a /- sorry -/ b -/\ntheorem t : True := trivial\n'), [])

    def test_code_detected(self):
        self.assertEqual(gate.forbidden_tokens('theorem t : False := by sorry\n'), ['sorry'])
        self.assertEqual(gate.forbidden_tokens('set_option maxHeartbeats 0\n'), ['set_option'])
        self.assertEqual(gate.forbidden_tokens('axiom p : False\n'), ['axiom'])
        self.assertEqual(gate.forbidden_tokens('/- x -/ example : 1 = 1 := by native_decide\n'), ['native_decide'])

    def test_unterminated_comment(self):
        with self.assertRaises(ValueError):
            gate.forbidden_tokens('/- open\n')


class Declarations(unittest.TestCase):
    def test_namespaces(self):
        text = ('namespace A\ntheorem x : True := trivial\nnamespace B\nnoncomputable def y : Nat := 0\n'
                'end B\nstructure Z : Prop where\n  p : True\nend A\n')
        self.assertEqual(gate.declarations(text), ['A.x', 'A.B.y', 'A.Z'])

    def test_sections_do_not_prefix(self):
        text = ('namespace A\nsection S\ntheorem x : True := trivial\nend S\n'
                'theorem y : True := trivial\nend A\n')
        self.assertEqual(gate.declarations(text), ['A.x', 'A.y'])

    def test_anonymous_section_rejected(self):
        with self.assertRaises(ValueError):
            gate.declarations('section\ntheorem x : True := trivial\nend\n')

    def test_unbalanced(self):
        with self.assertRaises(ValueError):
            gate.declarations('namespace A\nend B\n')
        with self.assertRaises(ValueError):
            gate.declarations('namespace A\ntheorem x : True := trivial\n')


class Pins(unittest.TestCase):
    def test_version_exact(self):
        ok = 'Lean (version 4.34.1, x86_64-unknown-linux-gnu, commit abc, Release)\n'
        self.assertTrue(gate.check_lean_version(ok, 'leanprover/lean4:v4.34.1').startswith('Lean (version 4.34.1,'))
        for bad in ('Lean (version 4.34.2, x86_64, Release)', 'Lean (version 4.34.10, x86_64, Release)',
                    'Lean (version 4.34.1-rc1, x86_64, Release)', ''):
            with self.assertRaises(ValueError):
                gate.check_lean_version(bad, 'leanprover/lean4:v4.34.1')
        with self.assertRaises(ValueError):
            gate.pinned_lean_version('leanprover/lean4:nightly')

    def test_worktree_clean(self):
        gate.check_worktree_clean('mathlib', '')
        for status in (' M Mathlib/Order/Basic.lean\n', 'M  Mathlib/Order/Basic.lean\n', '?? extra.lean\n'):
            with self.assertRaises(ValueError):
                gate.check_worktree_clean('mathlib', status)


class Axioms(unittest.TestCase):
    def test_allowed(self):
        text = ("'A.x' depends on axioms: [propext, Classical.choice, Quot.sound]\n"
                "'A.y' does not depend on any axioms\n")
        self.assertEqual(gate.audit_axioms(text, ['A.x', 'A.y'], ALLOWED),
                         {'A.x': ['Classical.choice', 'Quot.sound', 'propext'], 'A.y': []})

    def test_forbidden(self):
        for bad in ('sorryAx', 'Lean.ofReduceBool', 'hiddenPremise'):
            with self.assertRaises(ValueError) as ctx:
                gate.audit_axioms("'A.x' depends on axioms: [propext, " + bad + "]\n", ['A.x'], ALLOWED)
            self.assertIn('forbidden transitive axiom', str(ctx.exception))

    def test_missing_and_duplicate(self):
        with self.assertRaises(ValueError):
            gate.audit_axioms("'A.x' does not depend on any axioms\n", ['A.x', 'A.y'], ALLOWED)
        with self.assertRaises(ValueError):
            gate.audit_axioms("'A.x' does not depend on any axioms\n" * 2, ['A.x'], ALLOWED)
        with self.assertRaises(ValueError):
            gate.audit_axioms("'A.z' does not depend on any axioms\n", ['A.x'], ALLOWED)


if __name__ == '__main__':
    unittest.main()
