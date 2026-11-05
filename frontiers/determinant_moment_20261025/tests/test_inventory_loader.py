"""Source identity is a byte-execution boundary, including hostile pyc caches."""
import hashlib
import importlib._bootstrap_external
import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('determinant_outer_loader_test', ROOT / 'gate.py')
gate = importlib.util.module_from_spec(SPEC)
exec(compile((ROOT / 'gate.py').read_bytes(), str(ROOT / 'gate.py'), 'exec'), gate.__dict__)


class BoundInventoryLoaderTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.old_root, self.old_compiled = gate.ROOT, gate._compiled
        gate.ROOT, gate._compiled = self.base, None
        self.addCleanup(self.restore)
        shutil.copyfile(ROOT / 'compiled_inventory.py', self.base / 'compiled_inventory.py')

    def restore(self):
        gate.ROOT, gate._compiled = self.old_root, self.old_compiled

    def hostile_cache(self, path):
        raw = path.read_bytes()
        cached = Path(importlib.util.cache_from_source(str(path)))
        cached.parent.mkdir(exist_ok=True)
        code = compile("ALLOWED = {'HOSTILE_CACHED_IMPLEMENTATION'}\n", str(path), 'exec')
        cached.write_bytes(importlib._bootstrap_external._code_to_timestamp_pyc(
            code, int(path.stat().st_mtime), len(raw)))

    def test_exact_source_hash_cannot_authorize_stale_bytecode(self):
        path = self.base / 'compiled_inventory.py'
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),
                         'ff8a5374597772b2d37054fd722c2243c4b552a63802c69f7c605519832be6c4')
        self.hostile_cache(path)
        implementation = gate.compiled_implementation()
        self.assertEqual(implementation.ALLOWED, gate.ALLOWED)

    def test_changed_core_source_is_refused_before_execution(self):
        path = self.base / 'compiled_inventory.py'
        marker = self.base / 'changed-source-executed'
        path.write_text('from pathlib import Path\nPath(' + repr(str(marker)) + ").write_text('executed')\n")
        with self.assertRaisesRegex(ValueError, 'source-preserved core helper hash mismatch'):
            gate.compiled_implementation()
        self.assertFalse(marker.exists())

    def test_cached_module_does_not_hide_a_later_source_change(self):
        self.assertEqual(gate.compiled_implementation().ALLOWED, gate.ALLOWED)
        (self.base / 'compiled_inventory.py').write_text("raise RuntimeError('UNAUTHENTICATED_SOURCE_EXECUTED')\n")
        with self.assertRaisesRegex(ValueError, 'source-preserved core helper hash mismatch'):
            gate.compiled_implementation()


if __name__ == '__main__':
    unittest.main()
