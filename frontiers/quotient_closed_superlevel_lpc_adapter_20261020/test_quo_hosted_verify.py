"""UNEXECUTED R2 inert controls; R1 failed its generic credential substring check."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('quo_hosted_verify', Path(__file__).with_name('quo_hosted_verify.py'))
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)


class InertCollectorControls(unittest.TestCase):
    def test_exact_existing_branch_compare_and_swap_event_route(self):
        self.assertEqual(v.EXPECTED_BRANCH,
                         'codex/quotient-closed-superlevel-lpc-adapter-20261020-r2')
        event = {'before': v.EXPECTED_BASE, 'after': 'a' * 40, 'created': False,
                 'deleted': False, 'forced': False, 'ref': 'refs/heads/' + v.EXPECTED_BRANCH}
        v.validate_push_event(event, 'a' * 40)
        for change in ({'created': True}, {'before': 'b' * 40}, {'after': 'c' * 40},
                       {'forced': True}, {'deleted': True}, {'ref': 'refs/heads/main'},
                       {'ref': 'refs/heads/codex/quotient-closed-superlevel-lpc-adapter-20261020'}):
            with self.subTest(change=change), self.assertRaises(RuntimeError):
                v.validate_push_event(dict(event, **change), 'a' * 40)

    def test_actual_git_tab_records_and_exact_publication_path_fence(self):
        v.validate_publication_changes(['A\t' + v.PREFIX + '/project/Proof.lean',
                                        'A\t' + v.WORKFLOW])
        for bad in ([], ['A\\t' + v.WORKFLOW], ['M\t' + v.WORKFLOW],
                    ['A\tformal/lakefile.toml'], ['A\tfrontiers/Other/Proof.lean']):
            with self.subTest(bad=bad), self.assertRaises(RuntimeError):
                v.validate_publication_changes(bad)

    def diagnostic(self):
        expected = 'LocallyPathConnectedSpace { q // a ≤ descendedHeight d L hL g hperiodic q }'
        return ('OmittedEuclideanLPC.lean:25:2: error: Type mismatch\n  '
                + v.REQUIRED[2] + ' d L hL g hperiodic a\nhas type\n  '
                + 'LocallyPathConnectedSpace { x // a ≤ g x } → ' + expected
                + '\nbut is expected to have type\n  ' + expected + '\n')

    def test_missing_explicit_argument_is_distinct_from_other_failures(self):
        good = self.diagnostic()
        got = v.validate_negative('OmittedEuclideanLPC', 1, good)
        self.assertTrue(got['explicit_missing_argument'])
        for code, bad in ((0, good), (-15, good),
                          (1, good.replace(':25:', ':24:')),
                          (1, good.replace('a ≤ g x', 'a < g x')),
                          (1, good.replace(v.REQUIRED[2], 'Other.target')),
                          (1, good.replace(' → LocallyPathConnectedSpace', '')),
                          (1, good + 'Other.lean:1:0: error: unknown module\n'),
                          (1, 'failed to synthesize instance LocallyPathConnectedSpace')):
            with self.subTest(code=code, bad=bad), self.assertRaises(RuntimeError):
                v.validate_negative('OmittedEuclideanLPC', code, bad)

    def test_audit_requires_exact_four_targets_and_standard_axioms(self):
        good = '\n'.join("'" + name + "' depends on axioms: [propext,\n Classical.choice, Quot.sound]"
                         for name in v.REQUIRED)
        self.assertEqual(set(v.validate_audit(good)['target_axioms']), set(v.REQUIRED))
        for bad in (good.replace(v.REQUIRED[0], 'Other.target'),
                    good.replace('[propext,', '[sorryAx,'),
                    good + '\n' + "'" + v.REQUIRED[0] + "' does not depend on any axioms",
                    '\n'.join(good.splitlines()[2:])):
            with self.subTest(bad=bad), self.assertRaises(RuntimeError):
                v.validate_audit(bad)
        with self.assertRaises(RuntimeError):
            v.validate_audit(good, required=())

    def test_source_hash_refuses_missing_changed_and_symlink_sources(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / 'Proof.lean'
            path.write_bytes(b'abc')
            expected = {'bytes': 3, 'sha256': hashlib.sha256(b'abc').hexdigest()}
            v.verify_file(path, expected, root)
            path.write_bytes(b'abd')
            with self.assertRaises(RuntimeError):
                v.verify_file(path, expected, root)
            path.unlink()
            with self.assertRaises(RuntimeError):
                v.verify_file(path, expected, root)
            (root / 'Other').write_bytes(b'abc')
            path.symlink_to(root / 'Other')
            with self.assertRaises(RuntimeError):
                v.verify_file(path, expected, root)

    def test_positive_object_emission_and_link_are_required(self):
        before = {'Lifetime.olean': {'bytes': 3, 'sha256': 'a' * 64}}
        good = dict(before, **{'QuoClosedSuperlevelAdapter.olean': {'bytes': 5, 'sha256': 'b' * 64}})
        v.validate_objects(before, good, 'QuoClosedSuperlevelAdapter')
        for bad in (before, dict(good, **{'Other.olean': {'bytes': 1, 'sha256': 'c' * 64}}),
                    dict(good, **{'Lifetime.olean': {'bytes': 3, 'sha256': 'd' * 64}})):
            with self.subTest(bad=bad), self.assertRaises(RuntimeError):
                v.validate_objects(before, bad, 'QuoClosedSuperlevelAdapter')
        with self.assertRaises(RuntimeError):
            v.validate_objects(good, before)

    def test_effective_environment_is_allowlisted_and_mutation_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            loader_credential = 'INERT_ONLY_LOADER_CREDENTIAL_SENTINEL_20261020_R2'
            token_credential = 'INERT_ONLY_TOKEN_CREDENTIAL_SENTINEL_20261020_R2'
            env, contract = v.build_environment({'PATH': '/usr/bin:/bin', 'LEAN_PATH': '/pinned/lib',
                                                 'LEAN_NUM_THREADS': '64', 'LD_PRELOAD': loader_credential,
                                                 'TOKEN': token_credential}, Path(tmp))
            self.assertEqual(env['LEAN_NUM_THREADS'], '2')
            self.assertNotIn('LD_PRELOAD', env)
            self.assertNotIn('TOKEN', env)
            for credential in (loader_credential, token_credential):
                self.assertNotIn(credential, env.values())
                self.assertNotIn(credential, json.dumps(env))
                self.assertNotIn(credential, json.dumps(contract))
            self.assertIsNone(v.phase_environment(env, contract)[3])
            self.assertIsNotNone(v.phase_environment(dict(env, LEAN_PATH='/stale'), contract)[3])

    def test_failure_receipt_and_raw_streams_survive_and_no_resume_is_assumed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            report = {'status': 'HOLD_NOT_COMPLETED', 'phase_results': []}
            with self.assertRaises(RuntimeError):
                v.run_phase('inert-failure', [sys.executable, '-c',
                    'import sys;sys.stdout.buffer.write(b"out\\xff");sys.stderr.write("err");sys.exit(7)'],
                    root, dict(os.environ), root, report, timeout=5)
            self.assertEqual((root / 'inert-failure.stdout').read_bytes(), b'out\xff')
            self.assertEqual((root / 'inert-failure.stderr').read_bytes(), b'err')
            receipt = json.loads((root / 'inert-failure.receipt.json').read_text())
            self.assertEqual(receipt['exit_code'], 7)
            self.assertEqual(receipt['status'], 'FAIL')
            with self.assertRaises(FileExistsError):
                v.run_phase('inert-failure', [sys.executable, '-c', 'pass'],
                            root, dict(os.environ), root, report, timeout=5)

    def test_new_negative_format_cannot_self_qualify(self):
        with self.assertRaisesRegex(RuntimeError, 'PENDING_ADAPTER_NEGATIVE_PREDICATE'):
            v.require_final_predicates()


if __name__ == '__main__':
    unittest.main()
