"""Actual CLI stale-receipt regressions; all execution fixtures are synthetic."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('cbz_cli_gate', ROOT / 'gate.py')
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


class CliReceiptBoundaryTests(unittest.TestCase):
    def fixture(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name) / 'repo/frontiers/component'
        shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns('.lake', '__pycache__'))
        helper = root.parents[1] / 'tools/lean_packet_admission.py'
        helper.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT.parents[1] / 'tools/lean_packet_admission.py', helper)
        active = root / '.lake/formal-evidence/receipt.json'
        active.parent.mkdir(parents=True)
        active.write_text('{"synthetic_test_fixture":"stale active receipt"}')
        historical = {p.relative_to(root): p.read_bytes() for p in (root / 'evidence/final').rglob('*')
                      if p.is_file()}
        self.assertTrue(historical, 'original immutable final evidence fixture missing')
        return root, active, historical

    def invoke(self, root, *args):
        return subprocess.run([sys.executable, '-B', '-S', str(root / 'gate.py'), *args],
                              cwd=root, capture_output=True, text=True)

    def assert_preserved(self, root, historical):
        for rel, data in historical.items():
            self.assertEqual((root / rel).read_bytes(), data, str(rel))

    def test_source_hash_failure_clears_active_receipt_before_source_check(self):
        for args in ((), ('--execute',)):
            with self.subTest(args=args):
                root, active, historical = self.fixture()
                readme = root / 'README.md'
                readme.write_bytes(readme.read_bytes() + b'\nchanged bound control\n')
                result = self.invoke(root, *args)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('source hash mismatch: README.md', result.stderr)
                self.assertFalse(active.exists(), 'source failure retained active success receipt')
                self.assert_preserved(root, historical)

    def test_invalid_manifest_clears_active_receipt_before_qualification(self):
        for args in ((), ('--execute',)):
            with self.subTest(args=args):
                root, active, historical = self.fixture()
                (root / 'manifest.json').write_text('{')
                result = self.invoke(root, *args)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('FORMAL_GATE_FAIL', result.stderr)
                self.assertFalse(active.exists(), 'manifest failure retained active success receipt')
                self.assert_preserved(root, historical)

    def test_missing_binding_clears_active_receipt_in_both_cli_modes(self):
        for args in ((), ('--execute',)):
            with self.subTest(args=args):
                root, active, historical = self.fixture()
                result = self.invoke(root, *args)
                self.assertEqual(result.returncode, 1)
                self.assertIn('CBZ_COMPILED_INVENTORY_UNQUALIFIED', result.stderr)
                self.assertFalse(active.exists(), 'quarantine retained active success receipt')
                self.assert_preserved(root, historical)

    def test_structural_binding_source_only_refusal_clears_receipt(self):
        root, active, historical = self.fixture()
        m = json.loads((root / 'manifest.json').read_text())
        m['compiled_inventory'] = []  # Synthetic qualification input, not a real census.
        (root / 'manifest.json').write_text(json.dumps(m))
        result = self.invoke(root)
        self.assertEqual(result.returncode, 1)
        self.assertIn('CBZ_KERNEL_EXECUTION_REQUIRED', result.stderr)
        self.assertFalse(active.exists())
        self.assert_preserved(root, historical)

    def test_missing_or_invalid_bound_helper_cannot_prevent_invalidation(self):
        for fault in ('missing', 'invalid'):
            with self.subTest(fault=fault):
                root, active, historical = self.fixture()
                helper = root / 'compiled_inventory.py'
                if fault == 'missing':
                    helper.unlink()
                else:
                    helper.write_text('not valid python (')
                result = self.invoke(root, '--execute')
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(active.exists(), 'bound helper failed before active receipt invalidation')
                self.assert_preserved(root, historical)

    def test_cli_never_follows_lake_or_evidence_directory_symlinks(self):
        for relative in ('.lake', '.lake/formal-evidence', '.lake/build'):
            with self.subTest(relative=relative):
                root, active, historical = self.fixture()
                external = root.parent / 'outside-active-path'
                external.mkdir()
                target = external / 'receipt.json'
                target.write_text('{"synthetic_test_fixture":"external must survive"}')
                path = root / relative
                if path.exists():
                    if path.is_dir():
                        shutil.rmtree(path)
                    else:
                        path.unlink()
                path.parent.mkdir(parents=True, exist_ok=True)
                path.symlink_to(external, target_is_directory=True)
                result = self.invoke(root, '--execute')
                self.assertEqual(result.returncode, 1)
                self.assertIn('symlink', result.stderr)
                self.assertEqual(target.read_text(), '{"synthetic_test_fixture":"external must survive"}')
                self.assert_preserved(root, historical)

    def test_receipt_symlink_is_unlinked_without_touching_target(self):
        root, active, historical = self.fixture()
        external = root.parent / 'outside-active-receipt.json'
        external.write_text('{"synthetic_test_fixture":"external receipt"}')
        active.unlink()
        active.symlink_to(external)
        result = self.invoke(root)
        self.assertEqual(result.returncode, 1)
        self.assertIn('CBZ_COMPILED_INVENTORY_UNQUALIFIED', result.stderr)
        self.assertFalse(active.is_symlink())
        self.assertEqual(external.read_text(), '{"synthetic_test_fixture":"external receipt"}')
        self.assert_preserved(root, historical)

    def test_argument_help_and_parse_failure_also_invalidate_active_receipt(self):
        for args, expected in ((('--help',), 0), (('--unrecognized-option',), 2)):
            with self.subTest(args=args):
                root, active, historical = self.fixture()
                result = self.invoke(root, *args)
                self.assertEqual(result.returncode, expected)
                self.assertFalse(active.exists(), 'CLI attempt retained active receipt')
                self.assert_preserved(root, historical)


class QuarantineRecordTests(unittest.TestCase):
    def test_complete_record_binds_every_original_lean_module_without_self_hash(self):
        path = ROOT / 'QUARANTINE.json'
        self.assertTrue(path.is_file(), 'complete component quarantine record missing')
        q = json.loads(path.read_text())
        self.assertEqual(set(q), {'id', 'title', 'location', 'layer_a_status', 'exact_boundary',
                                 'blocking_reason', 'attempted', 'resumption_cost', 'isolation',
                                 'owner', 'maintenance'})
        self.assertIsNone(q['owner'])
        self.assertEqual(q['maintenance'], 'zero')
        m = json.loads((ROOT / 'manifest.json').read_text())
        records = q['location']['modules']
        self.assertEqual({x['path'] for x in records}, set(m['source_modules']) | {'ResearchFormalCoreR1.lean'})
        for record in records:
            self.assertEqual(record['sha256'], hashlib.sha256((ROOT / record['path']).read_bytes()).hexdigest())
        self.assertEqual(q['layer_a_status']['A2'], 'UNESTABLISHED_PACKAGE_WIDE_EVIDENCE')
        self.assertEqual(q['layer_a_status']['A8'], 'UNESTABLISHED_PACKAGE_WIDE_EVIDENCE')
        self.assertNotIn('manifest_sha256', q['location'])

    def test_quarantine_record_cannot_be_omitted_from_control_manifest(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name) / 'repo/frontiers/component'
        shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns('.lake', '__pycache__'))
        helper = root.parents[1] / 'tools/lean_packet_admission.py'
        helper.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT.parents[1] / 'tools/lean_packet_admission.py', helper)
        m = json.loads((root / 'manifest.json').read_text())
        m['files'].pop('QUARANTINE.json', None)
        (root / 'manifest.json').write_text(json.dumps(m))
        old = gate.ROOT
        gate.ROOT = root
        try:
            with self.assertRaisesRegex(ValueError, 'unbound control or scope file'):
                gate.source_check()
        finally:
            gate.ROOT = old


class PortableMutationRunnerTests(unittest.TestCase):
    def test_component_copy_runs_all_five_mutations_with_intended_failures(self):
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            root = base / 'repo/frontiers/cold-start-component'
            shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns('.lake', '__pycache__'))
            helper = root.parents[1] / 'tools/lean_packet_admission.py'
            helper.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT.parents[1] / 'tools/lean_packet_admission.py', helper)
            before = {p.relative_to(root): p.read_bytes() for p in root.rglob('*') if p.is_file()}
            output = base / 'reports'
            result = subprocess.run([sys.executable, '-B', '-S', str(root / 'tests/run_cbz_mutations.py'),
                                     '--output', str(output)], cwd=base, capture_output=True, text=True,
                                    env={**os.environ, 'TMPDIR': str(base)})
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            report = json.loads((output / 'mutation_results.json').read_text())
            self.assertEqual(len(report['mutations']), 5)
            self.assertTrue(report['source_preserved'])
            for record in report['mutations']:
                self.assertGreater(record['collected_tests'], 0)
                self.assertEqual(record['baseline_exit_code'], 0)
                self.assertNotEqual(record['exit_code'], 0)
                self.assertTrue(record['killed_by_intended_assertions'])
                self.assertFalse(record['import_or_test_errors'])
            after = {p.relative_to(root): p.read_bytes() for p in root.rglob('*') if p.is_file()}
            self.assertEqual(after, before)


if __name__ == '__main__':
    unittest.main()

