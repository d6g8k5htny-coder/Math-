"""Engineering controls only. No Lean invocation or scientific acceptance."""
import hashlib
import importlib.util
import inspect
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

MODULE_PATH = Path(__file__).with_name('c297_hosted_verify.py')


class HostedVerifierTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if MODULE_PATH.exists():
            spec = importlib.util.spec_from_file_location('c297_hosted_verify', MODULE_PATH)
            cls.v = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(cls.v)
        else:
            cls.v = None

    def verifier(self):
        self.assertIsNotNone(self.v, 'the scoped verifier is not implemented')
        return self.v

    def test_modified_source_bytes_are_rejected(self):
        """Dropping size/hash verification would accept the modified file."""
        v = self.verifier()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'Proof.lean'
            path.write_bytes(b'abc')
            expected = {'bytes': 3, 'sha256':
                        'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad'}
            v.verify_file(path, expected, Path(tmp))
            path.write_bytes(b'abd')
            with self.assertRaisesRegex(RuntimeError, 'identity mismatch'):
                v.verify_file(path, expected, Path(tmp))

    def test_audit_cannot_omit_required_target_or_hide_axiom(self):
        """Count-only validation would accept a substituted target or sorryAx."""
        v = self.verifier()
        good = (
            'SUPERLEVEL_AUDIT_MODULE A COUNT 1\n'
            'SUPERLEVEL_AUDIT_DECL A.target AXIOMS [propext]\n'
            'SUPERLEVEL_AUDIT_MODULE B COUNT 1\n'
            'SUPERLEVEL_AUDIT_DECL B.target AXIOMS []\n'
            'SUPERLEVEL_AUDIT_STANDARD_ONLY_PASS COUNT 2\n')
        got = v.validate_audit(good, modules=('A', 'B'), required=('A.target', 'B.target'))
        self.assertEqual(got['declaration_count'], 2)
        for bad in (good.replace('B.target', 'B.other'),
                    good.replace('[propext]', '[sorryAx]'),
                    good.replace('B.target AXIOMS []', 'A.target AXIOMS []')):
            with self.subTest(bad=bad), self.assertRaises(RuntimeError):
                v.validate_audit(bad, modules=('A', 'B'), required=('A.target', 'B.target'))

    def test_pinned_lean_multiline_axiom_records(self):
        """Actual pinned Lean wraps the unchanged Lifetime axiom arrays."""
        v = self.verifier()
        proper = (
            'SUPERLEVEL_AUDIT_MODULE Lifetime COUNT 1\n'
            'SUPERLEVEL_AUDIT_DECL UniversalLaw.Spec.Lifetime.IsUnrestrictedLeadingCoefficient AXIOMS [propext,\n'
            ' Classical.choice,\n'
            ' Quot.sound]\n'
            'SUPERLEVEL_AUDIT_STANDARD_ONLY_PASS COUNT 1\n')
        args = {'modules': ('Lifetime',),
                'required': ('UniversalLaw.Spec.Lifetime.IsUnrestrictedLeadingCoefficient',)}
        self.assertEqual(v.validate_audit(proper, **args)['declaration_count'], 1)
        for bad in (proper.replace(' Quot.sound]', ' sorryAx]'),
                    proper.replace(' Quot.sound]\n', ''),
                    proper.replace(' Quot.sound]', ' Quot.sound] trailing garbage'),
                    proper[:proper.index(' Quot.sound]')]):
            with self.subTest(bad=bad), self.assertRaises(RuntimeError):
                v.validate_audit(bad, **args)

    def test_fake_negative_or_import_failure_cannot_pass(self):
        """Exit-only or theorem-name-only validation accepts the wrong rejection."""
        v = self.verifier()
        proper = (
            'WithoutRegularOrInterior.lean:25:2: error: Type mismatch\n'
            '  TorusRegularSuperlevel.closed_superlevel_path_connected_basis hsmooth a x\n'
            'has type\n  a < g ↑x ∨ ¬IsCriticalPoint d g ↑x → (𝓝 x).HasBasis basis id\n'
            'but is expected to have type\n  (𝓝 x).HasBasis basis id\n')
        v.validate_negative('WithoutRegularOrInterior', 1, proper)
        for code, output in ((0, proper), (-9, proper),
                             (1, proper.replace('a < g ↑x ∨ ¬IsCriticalPoint d g ↑x →', 'Continuous g →')),
                             (1, proper + 'unknown module RegularSuperlevel\n'),
                             (1, proper.replace('Type mismatch', 'unexpected token'))):
            with self.subTest(code=code, output=output), self.assertRaises(RuntimeError):
                v.validate_negative('WithoutRegularOrInterior', code, output)
        coordinate = (
            'WithoutCoordinateIdentity.lean:26:2: error: Type mismatch\n'
            '  TorusRegularSuperlevel.closed_superlevel_basis_of_chart a x p hx\n'
            'has type\n  (∀ y ∈ p.source, (p y).fst = g y) → (𝓝 x).HasBasis basis id\n'
            'but is expected to have type\n  (𝓝 x).HasBasis basis id\n')
        v.validate_negative('WithoutCoordinateIdentity', 1, coordinate)
        with self.assertRaises(RuntimeError):
            v.validate_negative('WithoutCoordinateIdentity', 1,
                                coordinate.replace('(p y).fst = g y', 'True'))

    def test_failed_phase_receipt_and_exact_streams_survive_abort(self):
        """Raising before persistence would discard the actual failing phase."""
        v = self.verifier()
        with tempfile.TemporaryDirectory() as tmp:
            evidence = Path(tmp)
            report = {'status': 'HOLD_NOT_COMPLETED', 'phase_results': []}
            with self.assertRaisesRegex(RuntimeError, 'unexpected exit'):
                v.run_phase('deliberate-failure',
                            [sys.executable, '-c',
                             'import sys;sys.stdout.buffer.write(b"out\\xff");sys.stderr.write("err");sys.exit(7)'],
                            evidence, dict(os.environ), evidence, report, timeout=10)
            saved = json.loads((evidence / 'RESULT.json').read_text())
            phase = saved['phase_results'][0]
            self.assertEqual(phase['exit_code'], 7)
            self.assertEqual(phase['status'], 'FAIL')
            self.assertFalse(phase['timed_out'])
            self.assertEqual((evidence / 'deliberate-failure.stdout').read_bytes(), b'out\xff')
            self.assertEqual((evidence / 'deliberate-failure.stderr').read_bytes(), b'err')
            self.assertEqual(phase['stdout_sha256'], hashlib.sha256(b'out\xff').hexdigest())
            self.assertTrue((evidence / 'deliberate-failure.receipt.json').exists())


    def test_timeout_preserves_partial_stream_and_receipt(self):
        """Timeout handling must not discard the child output or phase result."""
        v = self.verifier()
        with tempfile.TemporaryDirectory() as tmp:
            evidence = Path(tmp)
            report = {'status': 'HOLD_NOT_COMPLETED', 'phase_results': []}
            with self.assertRaises(RuntimeError):
                v.run_phase('deliberate-timeout',
                            [sys.executable, '-u', '-c',
                             'import time;print("before timeout");time.sleep(3)'],
                            evidence, dict(os.environ), evidence, report, timeout=0.1)
            receipt = json.loads((evidence / 'deliberate-timeout.receipt.json').read_text())
            self.assertTrue(receipt['timed_out'])
            self.assertEqual(receipt['status'], 'FAIL')
            self.assertEqual((evidence / 'deliberate-timeout.stdout').read_bytes(), b'before timeout\n')

    def test_phase_rejects_imported_object_mutation(self):
        """A successful compiler process may not alter a prior input object."""
        v = self.verifier()
        self.assertIn('build_dir', inspect.signature(v.run_phase).parameters, 'object input monitoring is not implemented')
        with tempfile.TemporaryDirectory() as tmp:
            evidence = Path(tmp)
            build = evidence / 'objects'
            build.mkdir()
            (build / 'Lifetime.olean').write_bytes(b'frozen input')
            report = {'status': 'HOLD_NOT_COMPLETED', 'phase_results': []}
            with self.assertRaises(RuntimeError):
                v.run_phase('deliberate-object-mutation',
                            [sys.executable, '-c',
                             'from pathlib import Path;Path("objects/Lifetime.olean").write_bytes(b"changed")'],
                            evidence, dict(os.environ), evidence, report,
                            timeout=10, build_dir=build)
            receipt = json.loads((evidence / 'deliberate-object-mutation.receipt.json').read_text())
            self.assertEqual(receipt['exit_code'], 0)
            self.assertEqual(receipt['status'], 'FAIL')
            self.assertIn('Lifetime.olean', receipt['objects_before'])
            self.assertNotEqual(receipt['objects_before'], receipt['objects_after'])
            self.assertIsNotNone(receipt['object_validation_error'])

    def test_build_allows_only_its_own_outputs(self):
        """A build may add its target object, not an unrelated replacement."""
        v = self.verifier()
        self.assertTrue(hasattr(v, 'validate_objects'), 'object change validation is not implemented')
        previous = {'Lifetime.olean': {'bytes': 2, 'sha256': 'a' * 64}}
        good = dict(previous, **{'RegularSuperlevel.olean': {'bytes': 3, 'sha256': 'b' * 64}})
        v.validate_objects(previous, good, 'RegularSuperlevel')
        for bad in (dict(good, **{'Unrelated.olean': {'bytes': 1, 'sha256': 'c' * 64}}),
                    previous,
                    dict(good, **{'Lifetime.olean': {'bytes': 2, 'sha256': 'd' * 64}})):
            with self.subTest(bad=bad), self.assertRaises(RuntimeError):
                v.validate_objects(previous, bad, 'RegularSuperlevel')

    def test_amended_phase_receipt_matches_aggregate(self):
        """Semantic/object metadata must not exist only in the aggregate receipt."""
        v = self.verifier()
        self.assertTrue(hasattr(v, 'save_phase'), 'amended receipt persistence is not implemented')
        with tempfile.TemporaryDirectory() as tmp:
            evidence = Path(tmp)
            report = {'status': 'HOLD_NOT_COMPLETED', 'phase_results': []}
            rec, _, _ = v.run_phase('valid-phase', [sys.executable, '-c', 'pass'],
                                    evidence, dict(os.environ), evidence, report, timeout=10)
            rec['intended_missing_premise_rejection'] = True
            v.save_phase(evidence, report, rec)
            self.assertEqual(json.loads((evidence / 'valid-phase.receipt.json').read_text()),
                             json.loads((evidence / 'RESULT.json').read_text())['phase_results'][0])


if __name__ == '__main__':
    unittest.main()
