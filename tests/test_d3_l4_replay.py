"""Real-process replay-protocol tests; synthetic fixtures are not coefficient evidence."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
DRIVER = ROOT / 'tools' / 'd3_l4_replay.py'


class ReplayTests(unittest.TestCase):
    def load(self):
        self.assertTrue(DRIVER.is_file(), 'source-bound d3 L4 replay driver is missing')
        if hasattr(self, '_module'):
            return self._module
        spec = importlib.util.spec_from_file_location('d3_l4_replay', DRIVER)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self._module = module
        return module

    def fixture(self, module, root):
        packet = root / module.PACKET
        packet.mkdir(parents=True)
        records = []
        for name in module.FILE_NAMES:
            data = ('synthetic protocol fixture: ' + name + '\n').encode()
            (packet / name).write_bytes(data)
            records.append({'path': name, 'bytes': len(data),
                            'sha256': hashlib.sha256(data).hexdigest(),
                            'git_blob': module.git_blob(data)})
        (root / 'source.txt').write_bytes(b'synthetic upstream\n')
        manifest = {'object': module.OBJECT, 'scientific_effect': 'NONE',
                    'source_commit': module.SOURCE_COMMIT,
                    'source_repository': module.REPOSITORY,
                    'files': records,
                    'upstream_pins': [{'path': 'source.txt',
                                       'git_blob': module.git_blob(b'synthetic upstream\n')}]}
        raw = (json.dumps(manifest, sort_keys=True) + '\n').encode()
        (packet / 'SOURCE_FILES.json').write_bytes(raw)
        return packet, hashlib.sha256(raw).hexdigest()

    def test_00_driver_exists(self):
        self.assertTrue(DRIVER.is_file(), 'source-bound d3 L4 replay driver is missing')

    def test_valid_synthetic_snapshot(self):
        m = self.load()
        with tempfile.TemporaryDirectory() as t:
            root = Path(t); _, pin = self.fixture(m, root)
            self.assertEqual(len(m.validate_snapshot(root, pin)['files']), 9)

    def test_manifest_pin_required(self):
        m = self.load()
        with tempfile.TemporaryDirectory() as t:
            root = Path(t); self.fixture(m, root)
            with self.assertRaisesRegex(m.ReplayError, 'manifest_pin'):
                m.validate_snapshot(root, '0' * 64)

    def test_corrupt_missing_extra_and_directory(self):
        m = self.load()
        for mutation in ('corrupt', 'missing', 'extra', 'directory'):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as t:
                root = Path(t); p, pin = self.fixture(m, root)
                path = p / 'PROOF.md'
                if mutation == 'corrupt': path.write_text('changed')
                elif mutation == 'missing': path.unlink()
                elif mutation == 'extra': (p / 'unlisted.txt').write_text('extra')
                else: path.unlink(); path.mkdir()
                with self.assertRaises(m.ReplayError): m.validate_snapshot(root, pin)

    def test_symlink_file_and_parent_rejected(self):
        m = self.load()
        for parent in (False, True):
            with self.subTest(parent=parent), tempfile.TemporaryDirectory() as t:
                root = Path(t); p, pin = self.fixture(m, root)
                path = p.parent if parent else p / 'PROOF.md'
                moved = root / 'displaced'
                path.rename(moved); path.symlink_to(moved, target_is_directory=parent)
                with self.assertRaisesRegex(m.ReplayError, 'symlink'):
                    m.validate_snapshot(root, pin)

    def test_upstream_corruption(self):
        m = self.load()
        with tempfile.TemporaryDirectory() as t:
            root = Path(t); _, pin = self.fixture(m, root)
            (root / 'source.txt').write_text('corrupt')
            with self.assertRaisesRegex(m.ReplayError, 'git_blob'):
                m.validate_snapshot(root, pin)

    def test_paths_reject_escape_absolute_and_aliases(self):
        m = self.load()
        with tempfile.TemporaryDirectory() as t:
            for path in ('../x', '/x', './x', 'a/../x', 'a//x', 'a\\x', ''):
                with self.subTest(path=path), self.assertRaises(m.ReplayError):
                    m.safe_file(Path(t), path)

    def test_json_duplicate_and_nonfinite_rejected(self):
        m = self.load()
        for value in (b'{"a":1,"a":2}', b'{"a":NaN}', b'{"a":Infinity}', b'{"a":1e999}', b'{} trailing'):
            with self.subTest(value=value), self.assertRaises(m.ReplayError): m.strict_json(value)

    def test_exact_result_mismatch_not_accepted(self):
        m = self.load()
        with self.assertRaisesRegex(m.ReplayError, 'stdout_mismatch'):
            m.compare_output(b'{"coefficient":1}\n', b'{"coefficient":2}\n', 'exact')

    def crosscheck(self):
        return {'source_sha256': 'abc', 'rows': [{'D_interval': ['2.3','2.4'],
                 'disk_diagnostic_is_certificate': False,
                 'independent_disk_midpoint_diagnostic': 2.35}], 'reference_checks': {}}

    def test_crosscheck_diagnostic_float_portability_only(self):
        m = self.load(); expected = self.crosscheck(); actual = self.crosscheck()
        actual['rows'][0]['independent_disk_midpoint_diagnostic'] = 2.3500000000000005
        m.compare_output(json.dumps(actual).encode(), json.dumps(expected).encode(), 'crosschecks')
        actual['rows'][0]['D_interval'] = ['2.2','2.4']
        with self.assertRaisesRegex(m.ReplayError, 'crosscheck_exact_fields'):
            m.compare_output(json.dumps(actual).encode(), json.dumps(expected).encode(), 'crosschecks')

    def test_crosscheck_bad_diagnostic_rejected(self):
        m = self.load(); expected = self.crosscheck()
        for diagnostic in (float('nan'), float('inf'), 5, '2.35', True):
            actual = self.crosscheck(); actual['rows'][0]['independent_disk_midpoint_diagnostic'] = diagnostic
            with self.subTest(diagnostic=diagnostic), self.assertRaises(m.ReplayError):
                m.compare_output(json.dumps(actual).encode(), json.dumps(expected).encode(), 'crosschecks')

    def test_unittest_summary_required(self):
        m = self.load()
        for stderr in (b'', b'Ran 0 tests\n\nOK\n', b'Ran 7 tests\n\nFAILED\n'):
            with self.assertRaisesRegex(m.ReplayError, 'test_summary'):
                m.compare_output(b'', None, 'tests', stderr)
        m.compare_output(b'', None, 'tests', b'.......\n----------------------------------------------------------------------\nRan 7 tests in 0.2s\n\nOK\n')

    def run_fixture(self, source, expected=b'ok\n', timeout=5):
        m = self.load()
        with tempfile.TemporaryDirectory() as t:
            root = Path(t); script = root / 'fixture.py'; script.write_text(source)
            logs = root / 'logs'; logs.mkdir()
            return m.run_step([sys.executable, '-B', '-S', str(script)], root, logs,
                              'fixture', expected, 'exact', timeout)

    def test_real_process_success(self):
        self.assertEqual(self.run_fixture("print('ok')")['returncode'], 0)

    def test_real_process_crash_wrong_exit_and_stderr(self):
        m = self.load()
        for source, code in [("raise RuntimeError('not a mathematical rejection')", 'exit'),
                             ("print('ok');raise SystemExit(1)", 'exit'),
                             ("import sys;print('bad',file=sys.stderr);print('ok')", 'stderr')]:
            with self.subTest(source=source), self.assertRaisesRegex(m.ReplayError, code):
                self.run_fixture(source)

    def test_real_process_timeout_fails_closed(self):
        m = self.load()
        with self.assertRaisesRegex(m.ReplayError, 'timeout'):
            self.run_fixture('import time;time.sleep(30)', timeout=0.1)

    def test_cli_invalid_mode_is_refused(self):
        self.load()
        run = subprocess.run([sys.executable, '-B', '-S', str(DRIVER), '--mode', 'pretend-pass'],
                             capture_output=True)
        self.assertEqual(run.returncode, 2)

    def test_execution_identities_reject_dirty_tool(self):
        m = self.load()
        self.assertTrue(hasattr(m, 'execution_identities'), 'execution-source binding is missing')
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            for name in ('tools/d3_l4_replay.py', 'tests/test_d3_l4_replay.py',
                         '.github/workflows/d3-l4-anisotropic.yml'):
                p = root / name; p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text('synthetic execution-source fixture\n')
            def git(*args):
                return subprocess.run(['git', *args], cwd=root, check=True, capture_output=True).stdout.decode().strip()
            git('init', '-q'); git('add', '.')
            git('-c', 'user.name=Protocol fixture', '-c', 'user.email=fixture@example.invalid',
                '-c', 'commit.gpgsign=false', 'commit', '-qm', 'synthetic fixture')
            head = git('rev-parse', 'HEAD')
            self.assertEqual(len(m.execution_identities(root, head)), 3)
            (root / 'tools/d3_l4_replay.py').write_text('dirty execution source')
            with self.assertRaisesRegex(m.ReplayError, 'execution_source_drift'):
                m.execution_identities(root, head)

    def test_cli_missing_source_retains_failed_receipt(self):
        self.load()
        for mode in ('normal', 'optimized'):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as t:
                root = Path(t); output = root / 'evidence'
                run = subprocess.run([sys.executable, '-B', '-S', str(DRIVER),
                                      '--mode', mode, '--root', str(root), '--output', str(output)],
                                     capture_output=True)
                self.assertNotEqual(run.returncode, 0)
                self.assertEqual(run.stdout, b'')
                receipt = json.loads((output / 'receipt.json').read_text())
                self.assertEqual(receipt['status'], 'FAIL')
                self.assertEqual(receipt['mode'], mode)
                self.assertIn('missing_or_nonregular_source', receipt['failure'])

    def test_cli_refuses_reusing_existing_evidence(self):
        self.load()
        with tempfile.TemporaryDirectory() as t:
            root = Path(t); output = root / 'evidence'; output.mkdir()
            old = output / 'receipt.json'; old.write_text('historical receipt')
            run = subprocess.run([sys.executable, '-B', '-S', str(DRIVER), '--mode', 'normal',
                                  '--root', str(root), '--output', str(output)], capture_output=True)
            self.assertNotEqual(run.returncode, 0)
            self.assertIn(b'evidence_directory_already_exists', run.stderr)
            self.assertEqual(old.read_text(), 'historical receipt')

    def test_workflow_fetches_history_for_proof_reachability(self):
        text = (ROOT / '.github/workflows/d3-l4-anisotropic.yml').read_text()
        checkout = text.split('uses: actions/checkout@', 1)[1].split('      - ', 1)[0]
        self.assertIn('fetch-depth: 0', checkout,
                      'proof-reachability tests consume historical Git objects')

    def test_workflow_covers_packet_dependencies_and_both_modes(self):
        self.load(); wf = ROOT / '.github/workflows/d3-l4-anisotropic.yml'
        self.assertTrue(wf.is_file())
        text = wf.read_text()
        for target in ('coefficients/d3_l4_anisotropic_20261005/**',
                       'coefficients/side24_v1/PROOF.md', 'coefficients/side24_v1/ENCLOSURE.json',
                       'imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md',
                       'reviews/iba1_periodic_jet_claude_20261005/periodic_jet_check.py',
                       'tests/test_d3_l4_replay.py', 'tools/d3_l4_replay.py',
                       "mode: [normal, optimized]", 'contents: read',
                       'persist-credentials: false', 'if: always()', '--mode "${{ matrix.mode }}"'):
            self.assertIn(target, text)
        self.assertNotIn('pull_request_target:', text)


if __name__ == '__main__': unittest.main()
