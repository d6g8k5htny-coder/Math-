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

MODULE_PATH = Path(__file__).with_name('c299_hosted_verify.py')


class HostedVerifierTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if MODULE_PATH.exists():
            spec = importlib.util.spec_from_file_location('c299_hosted_verify', MODULE_PATH)
            cls.v = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(cls.v)
        else:
            cls.v = None

    def verifier(self):
        self.assertIsNotNone(self.v, 'the scoped verifier is not implemented')
        return self.v

    def test_environment_contract_strips_overrides_and_uses_declared_path(self):
        """An inherited tool/loader override must not survive or leak its value."""
        v = self.verifier()
        self.assertTrue(hasattr(v, 'build_environment'), 'environment contract is missing')
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            bindir = root / 'bin'
            bindir.mkdir()
            launcher = bindir / 'lean'
            launcher.write_text('# inert launcher locator fixture; never executed\n')
            launcher.chmod(0o700)
            inherited = {'PATH': str(bindir), 'LEAN_PATH': '/pinned/lake/library',
                         'LEAN_NUM_THREADS': '64', 'LEAN_SYSROOT': 'secret-lean-value',
                         'LAKE_HOME': 'secret-lake-value', 'LD_PRELOAD': 'secret-loader-value',
                         'DYLD_LIBRARY_PATH': 'secret-dyld-value', 'TOKEN': 'secret-token-value'}
            env, contract = v.build_environment(inherited, root / 'objects')
            self.assertEqual(env['LEAN_PATH'], str(root / 'objects') + os.pathsep + '/pinned/lake/library')
            self.assertEqual(env['LEAN_NUM_THREADS'], '2')
            self.assertEqual(v.resolve_lean_launcher(env), launcher.resolve())
            self.assertEqual(contract['removed_variable_names'],
                             ['DYLD_LIBRARY_PATH', 'LAKE_HOME', 'LD_PRELOAD', 'LEAN_NUM_THREADS', 'LEAN_SYSROOT'])
            for key in ('LEAN_SYSROOT', 'LAKE_HOME', 'LD_PRELOAD', 'DYLD_LIBRARY_PATH'):
                self.assertNotIn(key, env)
            self.assertEqual(env['TOKEN'], 'secret-token-value')
            self.assertNotIn('secret-', json.dumps(contract))
            empty, _ = v.build_environment({'PATH': str(bindir)}, root / 'empty')
            self.assertEqual(empty['LEAN_PATH'], str(root / 'empty'))

    def test_phase_environment_mutation_is_blocked_and_receipted(self):
        """A changed search path or injected loader must fail before the child runs."""
        v = self.verifier()
        self.assertTrue(hasattr(v, 'build_environment'), 'environment contract is missing')
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            env, contract = v.build_environment(dict(os.environ), root / 'objects')
            report = {'status': 'HOLD_NOT_COMPLETED', 'phase_results': [],
                      'environment_contract': contract}
            rec, output, _ = v.run_phase('environment-valid',
                [sys.executable, '-c', 'import os; print(os.environ["LEAN_NUM_THREADS"])'],
                root, env, root, report, timeout=10)
            self.assertEqual(output.strip(), '2')
            self.assertEqual(rec['selected_environment'], contract['selected_environment'])
            self.assertEqual(rec['environment_contract_sha256'], contract['sha256'])
            self.assertIsNone(rec['environment_validation_error'])
            for n, changes in enumerate(({'LEAN_PATH': '/unbound/library'}, {'LD_PRELOAD': 'secret-injection'})):
                altered = dict(env, **changes)
                with self.assertRaisesRegex(RuntimeError, 'environment'):
                    v.run_phase('environment-mutated-' + str(n),
                        [sys.executable, '-c', 'from pathlib import Path;Path("CHILD_RAN").write_text("bad")'],
                        root, altered, root, report, timeout=10)
                receipt = json.loads((root / ('environment-mutated-' + str(n) + '.receipt.json')).read_text())
                self.assertEqual(receipt['status'], 'FAIL')
                self.assertIsNone(receipt['exit_code'])
                self.assertIsNotNone(receipt['environment_validation_error'])
                self.assertFalse((root / 'CHILD_RAN').exists())
                self.assertNotIn('secret-injection', json.dumps(receipt))
                self.assertEqual(receipt, report['phase_results'][-1])

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
            'CRITICAL_RIDGE_AUDIT_MODULE A COUNT 1\n'
            'CRITICAL_RIDGE_AUDIT_DECL A.target AXIOMS [propext]\n'
            'CRITICAL_RIDGE_AUDIT_MODULE B COUNT 1\n'
            'CRITICAL_RIDGE_AUDIT_DECL B.target AXIOMS []\n'
            'CRITICAL_RIDGE_AUDIT_STANDARD_ONLY_PASS COUNT 2\n')
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
            'CRITICAL_RIDGE_AUDIT_MODULE Lifetime COUNT 1\n'
            'CRITICAL_RIDGE_AUDIT_DECL UniversalLaw.Spec.Lifetime.IsUnrestrictedLeadingCoefficient AXIOMS [propext,\n'
            ' Classical.choice,\n'
            ' Quot.sound]\n'
            'CRITICAL_RIDGE_AUDIT_STANDARD_ONLY_PASS COUNT 1\n')
        args = {'modules': ('Lifetime',),
                'required': ('UniversalLaw.Spec.Lifetime.IsUnrestrictedLeadingCoefficient',)}
        self.assertEqual(v.validate_audit(proper, **args)['declaration_count'], 1)
        for bad in (proper.replace(' Quot.sound]', ' sorryAx]'),
                    proper.replace(' Quot.sound]\n', ''),
                    proper.replace(' Quot.sound]', ' Quot.sound] trailing garbage'),
                    proper[:proper.index(' Quot.sound]')]):
            with self.subTest(bad=bad), self.assertRaises(RuntimeError):
                v.validate_audit(bad, **args)

    def test_pending_final_acceptance_fails_closed(self):
        """Collecting diagnostics must not silently qualify final acceptance."""
        v = self.verifier()
        with self.assertRaisesRegex(RuntimeError, 'PENDING_C299_NEGATIVE_PREDICATES'):
            v.require_final_predicates()

    def test_source_preflight_can_collect_before_final_predicate_qualification(self):
        """An early final-acceptance gate would block needed actual diagnostics."""
        v = self.verifier()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            packet = root / v.PREFIX
            files = {}
            for rel in ([f'project/{m}.lean' for m in v.MODULES] +
                        [f'negative-project/{m}.lean' for m in v.NEGATIVES]):
                path = packet / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b'-- inert source fixture\n')
                files[rel] = {'bytes': 24, 'sha256': hashlib.sha256(b'-- inert source fixture\n').hexdigest()}
            upstream = root / 'specifications/lean_statements_20261010/Specifications/Lifetime.lean'
            upstream.parent.mkdir(parents=True)
            upstream.write_bytes(b'-- inert source fixture\n')
            formal = root / 'formal'
            formal.mkdir()
            (formal / 'lean-toolchain').write_text('leanprover/lean4:v4.34.1\n')
            (formal / 'lakefile.toml').write_text('rev = "d13f23b723b8a846827a245b89c10fc7d3f11612"\n')
            (formal / 'lake-manifest.json').write_text(json.dumps({'packages': [
                {'name': name, 'rev': rev} for name, rev in v.PACKAGE_PINS.items()]}))
            for rel in (v.WORKFLOW, v.PREFIX + '/c299_hosted_verify.py',
                        v.PREFIX + '/test_c299_hosted_verify.py'):
                path = root / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b'inert support fixture\n')
            manifest = {'schema_version': 1, 'scientific_effect': 'NONE', 'files': files,
                        'source_origins': {name: {'commit': 'a' * 40, 'path': name + '.lean'}
                                           for name in ('Lifetime', 'TorusTopology', 'MorseFiniteCritical')}}
            manifest_path = packet / v.MANIFEST
            manifest_path.write_text(json.dumps(manifest))
            digest = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
            measured = v.verify_sources(root, digest)
            self.assertEqual(measured['files'], files)
            with self.assertRaisesRegex(RuntimeError, 'PENDING_C299_NEGATIVE_PREDICATES'):
                v.require_final_predicates()

    def test_inactive_draft_negative_sections_reject_forged_fields(self):
        """Section/token-only matching would accept unrelated existential fields."""
        v = self.verifier()
        # Pinned to the C7 rendering observed locally (Lean v4.34.1) at L21:2.
        conclusion = (
            '∃ r, r 0 = 0 ∧ ContDiffAt ℝ 2 r 0 ∧ '
            '(∀ᶠ (w : E d) in 𝓝 0, ∀ (z : ↥V), (fderiv ℝ f (p + w + ↑(r w))) ↑z = 0) ∧ '
            '∀ (w : E d) (z : ↥V), hessian d f p (w + ↑((fderiv ℝ r 0) w)) ↑z = 0')
        target = 'TorusCriticalRidge.exists_negative_partial_gradient_ridge'
        for name, expression, premise in (
                ('WithoutCriticality',
                 'fun hcritical => ' + target + ' f p V hsmooth hcritical hneg',
                 'IsCriticalPoint d f p'),
                ('WithoutNegativeDefiniteness',
                 target + ' f p V hsmooth hcritical',
                 '(∀ v ∈ V, v ≠ 0 → hessian d f p v v < 0)')):
            proper = (name + '.lean:21:2: error: Type mismatch\n  ' + expression
                      + '\nhas type\n  ' + premise + ' → ' + conclusion
                      + '\nbut is expected to have type\n  ' + conclusion + '\n')
            result = v.validate_negative_draft(name, 1, proper)
            self.assertTrue(result['draft_only'])
            self.assertFalse(result['actual_diagnostic_observed'])
            for code, bad in (
                    (0, proper), (-9, proper),
                    (1, proper.replace(name + '.lean', 'Other.lean')),
                    (1, proper.replace('.lean:21:2:', '.lean:23:2:')),
                    (1, proper.replace('.lean:21:2:', '.lean:21:3:')),
                    (1, proper.replace('(∀ᶠ (w : E d) in', '(∀ᶠ w in')),
                    (1, proper.replace('ContDiffAt ℝ 2 r 0', 'True')),
                    (1, proper.replace('fderiv ℝ f', 'fderiv ℝ other')),
                    (1, proper.replace(premise + ' → ', 'Continuous f → ', 1)),
                    (1, proper + 'Other.lean:1:1: error: unknown identifier\n'),
                    (1, proper.replace('but is expected to have type', 'unrelated log tokens'))):
                with self.subTest(name=name, code=code, bad=bad), self.assertRaises(RuntimeError):
                    v.validate_negative_draft(name, code, bad)

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
        good = dict(previous, **{'CriticalRidge.olean': {'bytes': 3, 'sha256': 'b' * 64}})
        v.validate_objects(previous, good, 'CriticalRidge')
        for bad in (dict(good, **{'Unrelated.olean': {'bytes': 1, 'sha256': 'c' * 64}}),
                    previous,
                    dict(good, **{'Lifetime.olean': {'bytes': 2, 'sha256': 'd' * 64}})):
            with self.subTest(bad=bad), self.assertRaises(RuntimeError):
                v.validate_objects(previous, bad, 'CriticalRidge')

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
