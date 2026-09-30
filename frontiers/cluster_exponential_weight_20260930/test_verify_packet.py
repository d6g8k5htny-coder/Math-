"""Fail-closed packet custody regressions; no mathematical claim is tested."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


CHECKER = Path(__file__).with_name('verify_packet.py')


class PacketIdentityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / 'packet'
        self.root.mkdir()
        (self.root / 'PROOF.md').write_bytes(b'Exact synthetic proof.\n')
        (self.root / 'SOURCES.json').write_bytes(b'{"synthetic":true}\n')
        (self.root / 'README.md').write_bytes(b'Original custody fixture.\n')
        self.validation = {'schema': 1, 'scientific_effect': 'NONE',
                           'proof_sha256': hashlib.sha256(b'Exact synthetic proof.\n').hexdigest(),
                           'preserved_failures': ['Historical fixture, not finite output.']}
        self.write_validation()
        proof = (self.root / 'PROOF.md').read_bytes()
        self.review = {'schema': 1, 'scientific_effect': 'NONE', 'proof': {
            'path': 'PROOF.md', 'bytes': len(proof),
            'sha256': hashlib.sha256(proof).hexdigest(),
            'git_blob': hashlib.sha1(b'blob '+str(len(proof)).encode()+b'\0'+proof).hexdigest()}}
        (self.root / 'REVIEW_RECORD.json').write_text(json.dumps(self.review) + '\n')
        self.resign()

    def tearDown(self):
        self.temp.cleanup()

    def write_validation(self):
        (self.root / 'VALIDATION.json').write_text(json.dumps(self.validation) + '\n')

    def resign(self):
        self.manifest = {'schema': 1, 'scientific_effect': 'NONE',
                         'manifest_self_excluded': True, 'files': []}
        for p in sorted(self.root.iterdir()):
            if p.name != 'MANIFEST.json':
                b = p.read_bytes()
                self.manifest['files'].append({'path': p.name, 'bytes': len(b),
                    'sha256': hashlib.sha256(b).hexdigest(),
                    'git_blob': hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()})
        self.write_manifest()

    def write_manifest(self):
        (self.root / 'MANIFEST.json').write_text(json.dumps(self.manifest) + '\n')

    def check(self, accepted=False):
        flags = ['-B', '-S'] + (['-O'] if sys.flags.optimize else [])
        p = subprocess.run([sys.executable, *flags, str(CHECKER), '--packet-root', str(self.root)],
                           capture_output=True)
        if accepted:
            self.assertEqual(p.returncode, 0, p.stderr.decode())
            result = json.loads(p.stdout)
            self.assertEqual(result['packet_files_verified'], 5)
            self.assertTrue(result['validation_proof_identity_verified'])
            self.assertTrue(result['review_proof_identity_verified'])
            self.assertFalse(result['mathematical_acceptance'])
        else:
            self.assertEqual(p.returncode, 1, 'bad packet accepted or wrong failure: '+p.stdout.decode()+p.stderr.decode())
            self.assertEqual(p.stdout, b'')
            self.assertIn(b'packet identity failed:', p.stderr)

    def test_valid_packet_cli_and_historical_validation(self):
        self.check(accepted=True)

    def test_stale_file_bytes_rejected(self):
        (self.root / 'README.md').write_bytes(b'Changed but unrecorded.\n')
        self.check()

    def test_each_recorded_identity_is_enforced(self):
        original = json.loads(json.dumps(self.manifest))
        for key, wrong in [('bytes', 1), ('sha256', '0'*64), ('git_blob', '0'*40)]:
            with self.subTest(key=key):
                self.manifest = json.loads(json.dumps(original))
                self.manifest['files'][0][key] = wrong
                self.write_manifest()
                self.check()

    def test_unlisted_file_rejected(self):
        (self.root / 'EXTRA.txt').write_bytes(b'Unlisted.\n')
        self.check()

    def test_missing_declared_file_rejected(self):
        (self.root / 'README.md').unlink()
        self.check()

    def test_duplicate_manifest_path_rejected(self):
        self.manifest['files'].append(dict(self.manifest['files'][0]))
        self.write_manifest()
        self.check()

    def test_empty_manifest_rejected(self):
        self.manifest['files'] = []
        self.write_manifest()
        self.check()

    def test_essential_proof_cannot_be_removed_and_resigned(self):
        (self.root / 'PROOF.md').unlink()
        self.resign()
        self.check()

    def test_essential_validation_cannot_be_removed_and_resigned(self):
        (self.root / 'VALIDATION.json').unlink()
        self.resign()
        self.check()

    def test_manifest_self_exclusion_must_be_true_boolean(self):
        for wrong in [False, 1, 'true', None]:
            with self.subTest(value=wrong):
                self.manifest['manifest_self_excluded'] = wrong
                self.write_manifest()
                self.check()

    def test_boolean_schema_rejected(self):
        self.manifest['schema'] = True
        self.write_manifest()
        self.check()

    def test_invalid_size_types_rejected(self):
        for wrong in [True, -1, 1.0, '1', None]:
            with self.subTest(value=wrong):
                self.manifest['files'][0]['bytes'] = wrong
                self.write_manifest()
                self.check()

    def test_unsafe_or_nonflat_paths_rejected(self):
        for wrong in ['', '.', '..', '../PROOF.md', '/PROOF.md', './PROOF.md',
                      'a//b', 'a/b', 'a\\b', 'C:proof', 'bad\0name', 7]:
            with self.subTest(path=wrong):
                self.manifest['files'][0]['path'] = wrong
                self.write_manifest()
                self.check()

    def test_duplicate_manifest_json_key_rejected(self):
        text = (self.root / 'MANIFEST.json').read_text()
        (self.root / 'MANIFEST.json').write_text(text.replace('"schema": 1', '"schema": 1, "schema": 1'))
        self.check()

    def test_duplicate_record_key_rejected(self):
        text = (self.root / 'MANIFEST.json').read_text()
        (self.root / 'MANIFEST.json').write_text(text.replace('"bytes": ', '"bytes": 0, "bytes": ', 1))
        self.check()

    def test_manifest_symlink_rejected(self):
        manifest = self.root / 'MANIFEST.json'
        outside = self.root.parent / 'outside.json'
        manifest.replace(outside)
        manifest.symlink_to(outside)
        self.check()

    def test_payload_symlink_rejected_even_when_bytes_match(self):
        path = self.root / 'README.md'
        outside = self.root.parent / 'outside.md'
        path.replace(outside)
        path.symlink_to(outside)
        self.check()

    def test_unlisted_directory_rejected(self):
        (self.root / 'extra').mkdir()
        self.check()

    def test_listed_directory_rejected(self):
        p = self.root / 'README.md'
        p.unlink()
        p.mkdir()
        self.check()

    def test_symlink_packet_root_rejected(self):
        original = self.root
        self.root = original.parent / 'linked'
        self.root.symlink_to(original, target_is_directory=True)
        self.check()

    def test_false_validation_proof_rejected_after_manifest_resign(self):
        self.validation['proof_sha256'] = '0'*64
        self.write_validation()
        self.resign()
        self.check()

    def test_boolean_validation_schema_rejected_after_manifest_resign(self):
        self.validation['schema'] = True
        self.write_validation()
        self.resign()
        self.check()

    def test_missing_validation_digest_rejected_after_manifest_resign(self):
        del self.validation['proof_sha256']
        self.write_validation()
        self.resign()
        self.check()

    def test_duplicate_validation_key_rejected_after_manifest_resign(self):
        p = self.root / 'VALIDATION.json'
        text = p.read_text().replace('"schema": 1', '"schema": 1, "schema": 1')
        p.write_text(text)
        self.resign()
        self.check()

    def test_nonfinite_json_rejected_after_manifest_resign(self):
        self.validation['unexpected_number'] = float('nan')
        self.write_validation()
        self.resign()
        self.check()

    def test_validation_history_not_compared_to_finite_output(self):
        self.validation['local_runs'] = {'old_count': 23, 'old_missing_objects': True}
        self.write_validation()
        self.resign()
        self.check(accepted=True)

    def test_overflowed_json_number_rejected_after_manifest_resign(self):
        p = self.root / 'VALIDATION.json'
        text = p.read_text().replace('"schema": 1', '"unbounded": 1e999, "schema": 1')
        p.write_text(text)
        self.resign()
        self.check()

    def test_review_cannot_transfer_after_proof_validation_manifest_resign(self):
        (self.root / 'PROOF.md').write_bytes(b'New proof with stale old review.\n')
        self.validation['proof_sha256'] = hashlib.sha256((self.root / 'PROOF.md').read_bytes()).hexdigest()
        self.write_validation()
        self.resign()
        self.check()

    def test_each_review_proof_identity_is_enforced_after_resign(self):
        original = json.loads(json.dumps(self.review))
        for key, wrong in [('bytes', True), ('git_blob', '0'*40), ('sha256', '0'*64), ('path', 'README.md')]:
            with self.subTest(key=key):
                self.review = json.loads(json.dumps(original))
                self.review['proof'][key] = wrong
                (self.root / 'REVIEW_RECORD.json').write_text(json.dumps(self.review) + '\n')
                self.resign()
                self.check()

    def test_review_record_cannot_be_removed_and_manifest_resigned(self):
        (self.root / 'REVIEW_RECORD.json').unlink()
        self.resign()
        self.check()


if __name__ == '__main__':
    unittest.main()
