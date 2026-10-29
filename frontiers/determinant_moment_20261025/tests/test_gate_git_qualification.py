"""Producer orchestration and real isolated Git probes; no Lean is executed."""
import contextlib
import hashlib
import inspect
import io
import json
import os
from pathlib import Path
import py_compile
import shutil
import subprocess
import tempfile
from types import ModuleType
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
COMPONENT = Path('frontiers/determinant_moment_20261025')


def load_gate():
    module = ModuleType('git_qualified_gate_probe')
    module.__file__ = str(ROOT / 'gate.py')
    exec(compile((ROOT / 'gate.py').read_bytes(), module.__file__, 'exec'), module.__dict__)
    return module


class GitQualificationIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.gate = load_gate()
        temporary = tempfile.TemporaryDirectory(prefix='determinant-git-producer-')
        self.addCleanup(temporary.cleanup)
        self.repo = Path(temporary.name) / 'repo'
        self.package = self.repo / COMPONENT
        shutil.copytree(ROOT, self.package, ignore=shutil.ignore_patterns('.lake', '__pycache__'))
        helper = self.repo / 'tools/lean_packet_admission.py'
        helper.parent.mkdir(parents=True)
        shutil.copyfile(REPO / 'tools/lean_packet_admission.py', helper)
        self.gate.ROOT = self.package
        self.gate.REPO = self.repo
        self.manifest = json.loads((self.package / 'manifest.json').read_bytes())
        self.rebind()
        self.active = self.package / '.lake/formal-evidence/receipt.json'
        self.active.parent.mkdir(parents=True)
        self.active.write_text('SYNTHETIC stale receipt, no kernel evidence\n')
        self.historical = self.active.parent / 'historical-marker.txt'
        self.historical.write_text('preserve\n')

    def rebind(self):
        self.manifest['files'] = {p.relative_to(self.package).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in self.package.rglob('*') if p.is_file() and p.name != 'manifest.json'
            and '.lake' not in p.relative_to(self.package).parts and '__pycache__' not in p.relative_to(self.package).parts}
        raw = (json.dumps(self.manifest, indent=2) + '\n').encode()
        (self.package / 'manifest.json').write_bytes(raw)
        self.digest = hashlib.sha256(raw).hexdigest()

    def require_api(self):
        self.assertTrue(callable(getattr(self.gate, 'source_qualification', None)),
                        'pre/post raw Git source qualification is missing')

    def test_execute_git_refusal_precedes_mutable_adapter_and_every_process(self):
        self.require_api()
        with patch.object(self.gate, 'source_qualification', side_effect=ValueError('ISOLATED Git refusal')) as identity, \
             patch.object(self.gate, 'compiled_contract', side_effect=ValueError('MUTABLE ADAPTER REACHED BEFORE REFUSAL')) as adapter, \
             patch.object(self.gate, 'run') as run:
            with self.assertRaisesRegex(ValueError, 'ISOLATED Git refusal'):
                self.gate.execute(self.manifest, self.digest)
        identity.assert_called_once_with(self.manifest, self.digest)
        adapter.assert_not_called(); run.assert_not_called()
        self.assertFalse(self.active.exists())
        self.assertEqual(self.historical.read_text(), 'preserve\n')

    def test_qualified_source_refusal_precedes_manifest_controlled_helper(self):
        self.require_api()
        self.assertIn('git_qualification', inspect.signature(self.gate.source_check).parameters)
        with patch.object(self.gate, 'source_qualification', side_effect=ValueError('ISOLATED Git refusal')) as identity, \
             patch.object(self.gate, 'load_admission') as helper:
            with self.assertRaisesRegex(ValueError, 'ISOLATED Git refusal'):
                self.gate.source_check(git_qualification=True)
        identity.assert_called_once_with(self.manifest, self.digest)
        helper.assert_not_called()

    def test_expected_manifest_digest_refuses_before_shared_helper_execution(self):
        self.assertIn('expected_manifest_sha256', inspect.signature(self.gate.source_check).parameters,
                      'post-execution manifest identity must precede helper loading')
        with patch.object(self.gate, 'load_admission') as helper:
            with self.assertRaisesRegex(ValueError, 'manifest changed during execution'):
                self.gate.source_check(expected_manifest_sha256='0' * 64)
        helper.assert_not_called()

    def test_manifest_cannot_rebind_the_trusted_git_implementation(self):
        self.require_api()
        marker = self.repo / 'UNAUTHENTICATED_CODE_RAN'
        malicious = ('from pathlib import Path\nPath(' + repr(str(marker)) + ').write_text("ran")\n'
                     'def qualify_source(*args, **kwargs): return {"checked_commit": "fake"}\n')
        (self.package / 'determinant_git_identity.py').write_text(malicious)
        self.rebind()
        with self.assertRaisesRegex(ValueError, 'Git identity.*(binding|hash)'):
            self.gate.source_qualification(self.manifest, self.digest)
        self.assertFalse(marker.exists())

    def test_timestamp_valid_pyc_cannot_replace_authenticated_git_helper(self):
        self.require_api()
        path = self.package / 'determinant_git_identity.py'
        authentic = path.read_bytes(); timestamp = int(path.stat().st_mtime)
        marker = self.repo / 'CACHED_CODE_RAN'
        fake = ('from pathlib import Path\nPath(' + repr(str(marker)) + ').write_text("ran")\n'
                'def qualify_source(*args, **kwargs): return {"checked_commit": "fake"}\n').encode()
        self.assertLess(len(fake), len(authentic))
        path.write_bytes(fake + b'#' * (len(authentic) - len(fake)))
        os.utime(path, (timestamp, timestamp))
        py_compile.compile(str(path), doraise=True)
        path.write_bytes(authentic); os.utime(path, (timestamp, timestamp))
        with self.assertRaisesRegex(ValueError, 'Git source identity command failed'):
            self.gate.source_qualification(self.manifest, self.digest)
        self.assertFalse(marker.exists())

    def test_real_git_qualified_producer_rejects_rebound_dirty_source(self):
        self.require_api()
        environment = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
        environment.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull)
        def git(*args):
            result = subprocess.run(['git', '-C', str(self.repo), *args], env=environment, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr.decode(errors='replace'))
            return result.stdout.decode().strip()
        git('init', '-q'); git('config', 'user.name', 'Isolated producer fixture')
        git('config', 'user.email', 'fixture@example.invalid'); git('config', 'core.autocrlf', 'false')
        git('add', '--all'); git('commit', '-q', '-m', 'Exact isolated source')
        identity = self.gate.source_qualification(self.manifest, self.digest)
        self.assertEqual(identity['checked_commit'], git('rev-parse', 'HEAD'))
        self.assertEqual(self.gate.source_qualification(self.manifest, self.digest, previous=identity), identity)
        (self.package / 'README.md').write_text('Self-consistently rebound dirty source\n')
        self.rebind()
        with self.assertRaisesRegex(ValueError, 'source bytes differ from HEAD blob'):
            self.gate.source_qualification(self.manifest, self.digest)

    def test_execute_cli_requests_pre_helper_git_qualification(self):
        self.require_api()
        with patch.object(self.gate.sys, 'argv', ['gate.py', '--execute']), \
             patch.object(self.gate, 'source_check', side_effect=ValueError('ISOLATED CLI source refusal')) as source, \
             patch.object(self.gate, 'execute') as execution, contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(self.gate.main(), 1)
        source.assert_called_once_with(git_qualification=True)
        execution.assert_not_called()
        self.assertFalse(self.active.exists())


if __name__ == '__main__':
    unittest.main()
