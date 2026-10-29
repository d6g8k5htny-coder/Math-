import importlib.util
import json
import pathlib
import sys
import tempfile
import types
import unittest
from unittest import mock

HERE = pathlib.Path(__file__).resolve().parents[1]

class CompatibilityTests(unittest.TestCase):
    def load(self):
        helper = types.ModuleType('gate_helper')
        helper.__file__ = str(HERE / 'gate_helper.py')  # synthetic import metadata
        helper.ROOT = HERE
        helper.load_json = json.loads
        helper.source_check = lambda: ({'source_modules': [], 'targets': [], 'files': {}}, 'old')
        helper.execute = lambda m, d: {'manifest_sha256': d}
        helper.run = lambda *a, **k: 'Lean (version 4.34.1, x86_64-unknown-linux-gnu, commit 5045d0056413266e57c625dcd7c365b10e377c52, Release)\n'
        helper.check_alignment = lambda *a: None
        spec = importlib.util.spec_from_file_location('gate_under_test', HERE / 'gate.py')
        module = importlib.util.module_from_spec(spec)
        # The synthetic helper must not leak into other real-wrapper imports.
        with mock.patch.dict(sys.modules, {'gate_helper': helper}):
            spec.loader.exec_module(module)
        return module, helper

    def test_exact_release_guard(self):
        gate, _ = self.load()
        good = 'Lean (version 4.34.1, x86_64-unknown-linux-gnu, commit 5045d0056413266e57c625dcd7c365b10e377c52, Release)'
        self.assertEqual(gate.check_lean_version(good + '\n'), good)
        for bad in ('', good.replace('5045d005', '00000000'), good + '\nnoise'):
            with self.assertRaises(ValueError):
                gate.check_lean_version(bad)

    def test_overlay_is_files_only(self):
        gate, _ = self.load()
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            gate.ROOT = root; gate.OVERLAY = root / 'manifest.overlay.json'
            gate.OVERLAY.write_text(json.dumps({'schema_version': 1, 'files': {'gate.py': '0' * 64}}))
            base = {'source_modules': [], 'targets': [], 'files': {'x': '1' * 64}}
            merged = gate._effective_manifest(json.dumps(base))
            self.assertEqual(merged['files']['gate.py'], '0' * 64)
            gate.OVERLAY.write_text(json.dumps({'schema_version': 1, 'files': {}, 'targets': []}))
            with self.assertRaises(ValueError): gate._effective_manifest(json.dumps(base))

    def test_execute_augments_receipt(self):
        gate, helper = self.load()
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td); (root / '.lake/formal-evidence').mkdir(parents=True)
            gate.ROOT = root; helper.ROOT = root
            gate.run = helper.run
            gate.source_check = lambda: ({'dependency_revisions': {'x': 'a' * 40}}, 'digest')
            gate.dependency_state = lambda m: dict(m['dependency_revisions'])
            helper.execute = lambda m, d: {'manifest_sha256': d, 'logs': {}, 'checked_commit': 'b' * 40}
            gate._HELPER_EXECUTE = helper.execute
            custody_calls = []
            def source_commit(manifest, digest, expected_head=None):
                self.assertEqual(manifest, {'dependency_revisions': {'x': 'a' * 40}})
                self.assertEqual(digest, 'digest')
                custody_calls.append(expected_head)
                return 'b' * 40
            with mock.patch.dict(gate.os.environ, {'GITHUB_RUN_ATTEMPT': '7'}), \
                 mock.patch.object(gate, 'checked_source_commit', side_effect=source_commit):
                receipt = gate.execute({'dependency_revisions': {'x': 'a' * 40}}, 'digest')
            self.assertEqual(custody_calls, [None, 'b' * 40])
            self.assertEqual(receipt['checked_commit'], 'b' * 40)
            self.assertEqual(receipt['workflow_run_attempt'], '7')
            self.assertEqual(receipt['observations']['preflight'], receipt['observations']['final'])
            self.assertEqual(json.loads((root / '.lake/formal-evidence/receipt.json').read_text()), receipt)

    def test_run_uses_current_root_and_preserves_explicit_cwd_and_exit_contract(self):
        gate, _ = self.load()
        with tempfile.TemporaryDirectory() as td:
            first = pathlib.Path(td) / 'first'
            second = pathlib.Path(td) / 'second'
            first.mkdir(); second.mkdir()
            out = second / 'logs'
            observed = []
            def helper_run(command, label, evidence, expect_success=True, cwd=None):
                observed.append((command, label, evidence, expect_success, cwd))
                return 'controlled transcript'
            with mock.patch.object(gate, '_HELPER_RUN', side_effect=helper_run):
                gate.ROOT = first
                self.assertEqual(gate.run(['probe'], 'first', out, False), 'controlled transcript')
                gate.ROOT = second
                self.assertEqual(gate.run(['probe'], 'second', out), 'controlled transcript')
                copied = first / 'compiled-copy'
                self.assertEqual(gate.run(['probe'], 'copy', out, False, cwd=copied), 'controlled transcript')
            self.assertEqual(observed, [
                (['probe'], 'first', out, False, first),
                (['probe'], 'second', out, True, second),
                (['probe'], 'copy', out, False, copied),
            ], 'EFFECTIVE_CWD_MISMATCH')

if __name__ == '__main__': unittest.main()
