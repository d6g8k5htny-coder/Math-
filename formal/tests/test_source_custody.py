"""Real Git custody checks; Lean outcomes are simulated only in orchestration cases."""
import contextlib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest import mock

HERE = Path(__file__).resolve().parents[1]
VERSION = 'Lean (version 4.34.1, x86_64-unknown-linux-gnu, commit 5045d0056413266e57c625dcd7c365b10e377c52, Release)\n'


class SourceCustodyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        self.root = self.repo / 'formal'
        self.root.mkdir()
        for name in ('gate.py', 'gate_helper.py'):
            shutil.copyfile(HERE / name, self.root / name)
        (self.root / 'proof.lean').write_text('theorem exactIdentity : True := True.intro\n')
        self.manifest = {'dependency_revisions': {}, 'files': {
            name: self.sha((self.root / name).read_bytes())
            for name in ('gate.py', 'gate_helper.py', 'proof.lean')}}
        (self.root / 'manifest.json').write_text(json.dumps(self.manifest))
        (self.root / 'manifest.overlay.json').write_text('{"schema_version":1,"files":{}}\n')
        self.git('init', '-q')
        self.git('config', 'user.name', 'Custody Fixture')
        self.git('config', 'user.email', 'fixture@example.invalid')
        self.git('config', 'commit.gpgsign', 'false')
        self.commit()
        spec = importlib.util.spec_from_file_location('custody_fixture_gate', self.root / 'gate.py')
        self.gate = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.gate)
        # Dynamic import can create a cache inside this disposable fixture when
        # callers omit -B. Remove only that generated cache before clean-status
        # assertions; keep the full unfiltered Git status checks below.
        cache = self.root / '__pycache__'
        if cache.is_dir():
            shutil.rmtree(cache)
        self.refresh_digest()

    @staticmethod
    def sha(data):
        return hashlib.sha256(data).hexdigest()

    def refresh_digest(self):
        self.digest = self.sha((self.root / 'manifest.json').read_bytes() + b'\0RF312-OVERLAY\0' +
                               (self.root / 'manifest.overlay.json').read_bytes())

    def git(self, *args):
        return subprocess.check_output(['git', '-C', str(self.repo), *args], text=True).strip()

    def commit(self):
        self.git('add', '.')
        self.git('commit', '-qm', 'fixture source')
        return self.git('rev-parse', 'HEAD')

    def checked(self, expected=None):
        self.assertTrue(callable(getattr(self.gate, 'checked_source_commit', None)),
                        'commit custody verifier is missing')
        return self.gate.checked_source_commit(self.manifest, self.digest, expected)

    def execute(self, during=None, checked_commit=None):
        calls = []
        def kernel(manifest, digest):
            calls.append('kernel')
            if during:
                during()
            receipt = {'checked_commit': checked_commit or self.git('rev-parse', 'HEAD'), 'logs': {}}
            (self.root / '.lake/formal-evidence/receipt.json').write_text(json.dumps(receipt))
            return receipt
        with mock.patch.object(self.gate, 'run', return_value=VERSION), \
             mock.patch.object(self.gate, 'dependency_state', return_value={}), \
             mock.patch.object(self.gate, 'source_check', return_value=(self.manifest, self.digest)), \
             mock.patch.object(self.gate, '_HELPER_EXECUTE', side_effect=kernel), \
             contextlib.redirect_stdout(io.StringIO()):
            result = self.gate.execute(self.manifest, self.digest)
        return result, calls

    def test_execute_accepts_clean_committed_source(self):
        receipt, calls = self.execute()
        self.assertEqual(calls, ['kernel'])
        self.assertEqual(receipt['checked_commit'], self.git('rev-parse', 'HEAD'))

    def test_execute_refuses_dirty_overlay_before_kernel(self):
        overlay = self.root / 'manifest.overlay.json'
        overlay.write_bytes(overlay.read_bytes() + b'\n')
        self.refresh_digest()
        with self.assertRaisesRegex(ValueError, 'committed source'):
            self.execute()
        self.assertFalse((self.root / '.lake/formal-evidence/receipt.json').exists())

    def test_execute_refuses_head_drift_and_removes_receipt(self):
        def move_head():
            (self.repo / 'outside.txt').write_text('new head\n')
            self.git('add', 'outside.txt')
            self.git('commit', '-qm', 'move head during execution')
        with self.assertRaisesRegex(ValueError, 'HEAD changed'):
            self.execute(move_head)
        self.assertFalse((self.root / '.lake/formal-evidence/receipt.json').exists())

    def test_execute_removes_stale_receipt_on_preflight_failure(self):
        out = self.root / '.lake/formal-evidence'
        out.mkdir(parents=True)
        (out / 'receipt.json').write_text('{"old":"not this run"}\n')
        overlay = self.root / 'manifest.overlay.json'
        overlay.write_bytes(overlay.read_bytes() + b'\n')
        self.refresh_digest()
        with self.assertRaises(ValueError):
            self.execute()
        self.assertFalse((out / 'receipt.json').exists())

    def test_execute_refuses_helper_receipt_for_another_commit(self):
        with self.assertRaisesRegex(ValueError, 'helper checked commit'):
            self.execute(checked_commit='d' * 40)
        self.assertFalse((self.root / '.lake/formal-evidence/receipt.json').exists())

    def test_helper_loader_ignores_poisoned_bytecode_cache(self):
        from importlib._bootstrap_external import _code_to_timestamp_pyc
        helper = self.root / 'gate_helper.py'
        info = helper.stat()
        poison = compile("raise RuntimeError('POISONED_CACHED_HELPER')\n", str(helper), 'exec')
        cache = Path(importlib.util.cache_from_source(str(helper)))
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_bytes(_code_to_timestamp_pyc(poison, int(info.st_mtime), info.st_size))
        spec = importlib.util.spec_from_file_location('custody_poisoned_cache_gate', self.root / 'gate.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual(module._HELPER_EXECUTE.__name__, 'execute')

    def test_clean_committed_source_is_bound_to_exact_head(self):
        self.assertEqual(self.checked(), self.git('rev-parse', 'HEAD'))

    def test_uncommitted_overlay_is_refused_even_with_refreshed_digest(self):
        overlay = self.root / 'manifest.overlay.json'
        overlay.write_bytes(overlay.read_bytes() + b'\n')
        self.refresh_digest()
        with self.assertRaisesRegex(ValueError, 'committed source'):
            self.checked()

    def test_refreshed_manifest_cannot_launder_dirty_proof(self):
        proof = self.root / 'proof.lean'
        proof.write_bytes(proof.read_bytes() + b'-- changed\n')
        self.manifest['files']['proof.lean'] = self.sha(proof.read_bytes())
        (self.root / 'manifest.json').write_text(json.dumps(self.manifest))
        self.refresh_digest()
        with self.assertRaisesRegex(ValueError, 'committed source'):
            self.checked()

    def test_staged_bytes_are_refused(self):
        path = self.root / 'proof.lean'
        original = path.read_bytes()
        path.write_bytes(original + b'-- staged\n')
        self.git('add', 'formal/proof.lean')
        path.write_bytes(original)
        with self.assertRaisesRegex(ValueError, 'index'):
            self.checked()

    def test_assume_unchanged_bytes_are_refused(self):
        self.git('update-index', '--assume-unchanged', 'formal/proof.lean')
        path = self.root / 'proof.lean'
        path.write_bytes(path.read_bytes() + b'-- hidden\n')
        self.assertEqual(self.git('status', '--porcelain'), '')
        with self.assertRaisesRegex(ValueError, 'committed source'):
            self.checked()

    def test_skip_worktree_bytes_are_refused(self):
        self.git('update-index', '--skip-worktree', 'formal/proof.lean')
        path = self.root / 'proof.lean'
        path.write_bytes(path.read_bytes() + b'-- hidden\n')
        self.assertEqual(self.git('status', '--porcelain'), '')
        with self.assertRaisesRegex(ValueError, 'committed source'):
            self.checked()

    def test_foreign_git_environment_cannot_redirect_source_identity(self):
        expected = self.git('rev-parse', 'HEAD')
        with tempfile.TemporaryDirectory() as temporary:
            foreign = Path(temporary) / 'foreign'
            subprocess.check_call(['git', 'clone', '-q', str(self.repo), str(foreign)])
            subprocess.check_call(['git', '-C', str(foreign), 'config', 'user.name', 'Foreign Fixture'])
            subprocess.check_call(['git', '-C', str(foreign), 'config', 'user.email', 'foreign@example.invalid'])
            (foreign / 'outside.txt').write_text('foreign head\\n')
            subprocess.check_call(['git', '-C', str(foreign), 'add', 'outside.txt'])
            subprocess.check_call(['git', '-C', str(foreign), 'commit', '-qm', 'foreign head'])
            with mock.patch.dict(os.environ, {'GIT_DIR': str(foreign / '.git'), 'GIT_WORK_TREE': str(self.repo)}):
                self.assertEqual(self.checked(), expected)

    def test_replace_ref_cannot_redirect_committed_source(self):
        expected = self.git('rev-parse', 'HEAD')
        path = self.root / 'proof.lean'
        path.write_bytes(path.read_bytes() + b'-- replacement tree\\n')
        self.git('add', 'formal/proof.lean')
        tree = self.git('write-tree')
        replacement = self.git('commit-tree', tree, '-m', 'replacement commit')
        self.git('reset', '--hard', '-q', expected)
        self.git('replace', expected, replacement)
        clean_env = dict(os.environ)
        clean_env.pop('GIT_NO_REPLACE_OBJECTS', None)
        with mock.patch.dict(os.environ, clean_env, clear=True):
            self.assertEqual(self.checked(), expected)

    def test_commit_drift_is_refused(self):
        first = self.checked()
        (self.repo / 'outside.txt').write_text('new head\n')
        self.commit()
        with self.assertRaisesRegex(ValueError, 'HEAD changed'):
            self.checked(first)

    def test_loaded_wrapper_cannot_claim_replaced_committed_source(self):
        path = self.root / 'gate.py'
        path.write_bytes(path.read_bytes().replace(b"'symlink build directory'", b"'changed build directory'"))
        self.manifest['files']['gate.py'] = self.sha(path.read_bytes())
        (self.root / 'manifest.json').write_text(json.dumps(self.manifest))
        self.commit()
        self.refresh_digest()
        with self.assertRaisesRegex(ValueError, 'loaded wrapper'):
            self.checked()

    def test_loaded_helper_cannot_claim_replaced_committed_source(self):
        path = self.root / 'gate_helper.py'
        path.write_bytes(path.read_bytes() + b'\n# replaced helper\n')
        self.manifest['files']['gate_helper.py'] = self.sha(path.read_bytes())
        (self.root / 'manifest.json').write_text(json.dumps(self.manifest))
        self.commit()
        self.refresh_digest()
        with self.assertRaisesRegex(ValueError, 'loaded helper'):
            self.checked()

    def test_symlink_owned_source_is_refused(self):
        path = self.root / 'proof.lean'
        data = path.read_bytes()
        path.unlink()
        outside = self.repo / 'outside.lean'
        outside.write_bytes(data)
        path.symlink_to(outside)
        with self.assertRaisesRegex(ValueError, 'symlink'):
            self.checked()


    def dependency_fixture(self):
        self.dep = self.root / '.lake/packages/probe'
        self.dep.mkdir(parents=True)
        def git(*args):
            return subprocess.check_output(['git', '-C', str(self.dep), *args], text=True).strip()
        self.dep_git = git
        git('init', '-q')
        git('config', 'user.name', 'Dependency Fixture')
        git('config', 'user.email', 'dependency@example.invalid')
        git('config', 'commit.gpgsign', 'false')
        (self.dep / 'Proof.lean').write_text('theorem depIdentity : True := True.intro\n')
        (self.dep / 'build.py').write_text('print("source identity only")\n')
        (self.dep / '.gitignore').write_text('.lake/\n*.ignored.lean\n')
        git('add', '.')
        git('commit', '-qm', 'dependency source')
        return {'dependency_revisions': {'probe': git('rev-parse', 'HEAD')}}

    def tracked_symlink_dependency(self):
        manifest = self.dependency_fixture()
        (self.dep / 'Alternate.lean').write_bytes((self.dep / 'Proof.lean').read_bytes())
        (self.dep / 'Linked.lean').symlink_to('Proof.lean')
        self.dep_git('add', '.')
        self.dep_git('commit', '-qm', 'tracked immutable source symlink')
        manifest['dependency_revisions']['probe'] = self.dep_git('rev-parse', 'HEAD')
        return manifest

    def test_dependency_accepts_tracked_symlink_with_bound_target(self):
        manifest = self.tracked_symlink_dependency()
        self.assertEqual(self.gate.dependency_state(manifest), manifest['dependency_revisions'])

    def test_dependency_hidden_symlink_retargeting_is_refused(self):
        manifest = self.tracked_symlink_dependency()
        self.dep_git('update-index', '--assume-unchanged', 'Linked.lean')
        path = self.dep / 'Linked.lean'
        path.unlink()
        path.symlink_to('Alternate.lean')
        self.assertEqual(self.dep_git('status', '--porcelain'), '')
        with self.assertRaisesRegex(ValueError, 'working bytes differ from committed source'):
            self.gate.dependency_state(manifest)

    def test_dependency_refuses_symlink_target_outside_bound_tree(self):
        manifest = self.dependency_fixture()
        (self.dep.parent / 'outside.lean').write_text('theorem external : True := True.intro\n')
        (self.dep / 'Linked.lean').symlink_to('../outside.lean')
        self.dep_git('add', '.')
        self.dep_git('commit', '-qm', 'outside target is not source-bound')
        manifest['dependency_revisions']['probe'] = self.dep_git('rev-parse', 'HEAD')
        with self.assertRaisesRegex(ValueError, 'unbound symlink target'):
            self.gate.dependency_state(manifest)

    def test_dependency_ignores_foreign_git_environment(self):
        manifest = self.dependency_fixture()
        with tempfile.TemporaryDirectory() as temporary:
            foreign = Path(temporary) / 'foreign-dependency'
            subprocess.check_call(['git', 'clone', '-q', str(self.dep), str(foreign)])
            subprocess.check_call(['git', '-C', str(foreign), 'config', 'user.name', 'Foreign Fixture'])
            subprocess.check_call(['git', '-C', str(foreign), 'config', 'user.email', 'foreign@example.invalid'])
            (foreign / 'outside.txt').write_text('different dependency head\\n')
            subprocess.check_call(['git', '-C', str(foreign), 'add', 'outside.txt'])
            subprocess.check_call(['git', '-C', str(foreign), 'commit', '-qm', 'foreign dependency'])
            with mock.patch.dict(os.environ, {'GIT_DIR': str(foreign / '.git'), 'GIT_WORK_TREE': str(self.dep)}):
                self.assertEqual(self.gate.dependency_state(manifest), manifest['dependency_revisions'])

    def test_dependency_accepts_exact_clean_committed_tree(self):
        manifest = self.dependency_fixture()
        self.assertEqual(self.gate.dependency_state(manifest), manifest['dependency_revisions'])

    def test_dependency_assume_unchanged_lean_is_refused(self):
        manifest = self.dependency_fixture()
        self.dep_git('update-index', '--assume-unchanged', 'Proof.lean')
        path = self.dep / 'Proof.lean'
        path.write_bytes(path.read_bytes() + b'-- hidden proof bytes\n')
        self.assertEqual(self.dep_git('status', '--porcelain'), '')
        with self.assertRaisesRegex(ValueError, 'committed source'):
            self.gate.dependency_state(manifest)

    def test_dependency_skip_worktree_build_input_is_refused(self):
        manifest = self.dependency_fixture()
        self.dep_git('update-index', '--skip-worktree', 'build.py')
        (self.dep / 'build.py').write_text('print("changed ignored index flag")\n')
        self.assertEqual(self.dep_git('status', '--porcelain'), '')
        with self.assertRaisesRegex(ValueError, 'committed source'):
            self.gate.dependency_state(manifest)

    def test_dependency_ignored_extra_lean_is_refused(self):
        manifest = self.dependency_fixture()
        (self.dep / 'Extra.ignored.lean').write_text('axiom unexpected : False\n')
        self.assertEqual(self.dep_git('status', '--porcelain'), '')
        with self.assertRaisesRegex(ValueError, 'unexpected Lean source'):
            self.gate.dependency_state(manifest)


if __name__ == '__main__':
    unittest.main()
