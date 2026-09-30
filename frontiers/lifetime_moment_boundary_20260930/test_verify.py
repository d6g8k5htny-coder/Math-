"""Real CLI controls for receipt selection and immutable local source copies."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
LIFETIME = Path('frontiers/lifetime_moment_boundary_20260930')
RADIAL = Path('reviews/radial_moment_corollaries_20260930')


class PublicationVerifierTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name) / 'repo'
        for packet in (LIFETIME, RADIAL):
            shutil.copytree(REPO / packet, self.root / packet,
                            ignore=shutil.ignore_patterns('__pycache__'))

    def replay(self):
        flags = ['-O'] if sys.flags.optimize else []
        return subprocess.run(
            [sys.executable, '-B', *flags, '-S',
             str(self.root / LIFETIME / 'verify.py')],
            cwd=self.root, capture_output=True, text=True, timeout=30)

    def test_clean_packet_replays_both_modes(self):
        result = self.replay()
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertTrue(report['passed'])
        self.assertEqual([row['mode'] for row in report['modes']],
                         ['normal', 'optimized'])

    def test_changed_optimized_lifetime_receipt_is_rejected(self):
        path = self.root / LIFETIME / 'CHECK_RECEIPT_OPTIMIZED.json'
        data = json.loads(path.read_text())
        data['good_quartic_cases'] += 1
        path.write_text(json.dumps(data))
        result = self.replay()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('lifetime replay differs', result.stderr)

    def test_changed_optimized_loss_receipt_is_rejected(self):
        path = self.root / LIFETIME / 'LOSS_CHECK_RECEIPT_OPTIMIZED.json'
        data = json.loads(path.read_text())
        data['rational_probability_cases'] += 1
        path.write_text(json.dumps(data))
        result = self.replay()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('loss replay differs', result.stderr)

    def test_changed_normal_receipt_remains_rejected(self):
        path = self.root / LIFETIME / 'CHECK_RECEIPT.json'
        data = json.loads(path.read_text())
        data['good_quartic_cases'] += 1
        path.write_text(json.dumps(data))
        result = self.replay()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('lifetime replay differs', result.stderr)

    def test_changed_optimized_radial_receipt_is_rejected_after_custody_check(self):
        path = self.root / RADIAL / 'moment-checks-optimized.json'
        data = json.loads(path.read_text())
        data['tests'] += 1
        path.write_text(json.dumps(data))
        # A self-consistent custody record must not replace actual replay.
        manifest = self.root / RADIAL / 'COROLLARY_CUSTODY.json'
        custody = json.loads(manifest.read_text())
        for row in custody['artifacts']:
            if row['path'] == path.name:
                row['bytes'] = path.stat().st_size
                row['sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
        manifest.write_text(json.dumps(custody))
        result = self.replay()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('radial replay differs', result.stderr)

    def check_alias_rejected(self, relative):
        path = self.root / relative
        target = self.root / 'byte-identical-target'
        path.rename(target)
        path.symlink_to(target, target_is_directory=target.is_dir())
        result = self.replay()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('symlink', result.stderr.lower())

    def test_byte_identical_lifetime_source_symlink_is_rejected(self):
        self.check_alias_rejected(LIFETIME / 'sources/P.md')

    def test_byte_identical_radial_source_symlink_is_rejected(self):
        self.check_alias_rejected(RADIAL / 'P.md')

    def test_lifetime_source_directory_symlink_is_rejected(self):
        self.check_alias_rejected(LIFETIME / 'sources')

    def test_lifetime_parent_directory_symlink_is_rejected(self):
        self.check_alias_rejected(Path('frontiers'))

    def test_radial_parent_directory_symlink_is_rejected(self):
        self.check_alias_rejected(Path('reviews'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
