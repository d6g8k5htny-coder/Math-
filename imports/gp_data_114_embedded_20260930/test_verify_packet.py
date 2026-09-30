"""Packet-boundary controls; archived Python is copied and read as bytes only."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

import verify_packet as verifier

HERE = Path(__file__).resolve().parent
ORIGINAL_FILES = (
    'GP-DATA-114-v1.0_receipt.json',
    'GP-DATA-114-v1.0_uniform_q_degree4_interval.py',
    'MANIFEST.json', 'README.md', 'SOURCES.json', 'VALIDATION.json',
    'inert_decoder.py', 'test_inert_decoder.py',
)
WRAPPER_RAW = None


class PacketControls(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='gpdata114_packet_')
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name) / 'packet'
        self.directory.mkdir()
        for name in ORIGINAL_FILES:
            shutil.copyfile(HERE / name, self.directory / name)
        self.resign_manifest()
        self.wrapper = WRAPPER_RAW if WRAPPER_RAW is not None else Path('/tmp/gpdata114-public-wrapper.txt').read_bytes()

    def resign_manifest(self):
        manifest = json.loads((self.directory / 'MANIFEST.json').read_text())
        entries = []
        for name in ORIGINAL_FILES:
            if name == 'MANIFEST.json':
                continue
            data = (self.directory / name).read_bytes()
            framed = b'blob ' + str(len(data)).encode() + b'\0' + data
            entries.append({'path': name, 'bytes': len(data),
                            'sha256': hashlib.sha256(data).hexdigest(),
                            'git_blob': hashlib.sha1(framed).hexdigest()})
        manifest['files'] = entries
        (self.directory / 'MANIFEST.json').write_text(json.dumps(manifest, sort_keys=True))

    def test_reject_undeclared_packet_file(self):
        (self.directory / 'undeclared.py').write_bytes(b'inert unexpected bytes\n')
        with self.assertRaisesRegex(ValueError, 'file set'):
            verifier.verify_packet(self.directory, self.wrapper)

    def test_reject_false_sources_identity_after_manifest_resigning(self):
        original = (self.directory / 'SOURCES.json').read_text()
        wrong_values = {'label': 'OTHER', 'path': 'wrong.py', 'bytes': 9788,
                        'sha256': '0' * 64, 'git_blob': '0' * 40,
                        'gzip_bytes': 3417, 'gzip_sha256': '0' * 64}
        for field, value in wrong_values.items():
            with self.subTest(field=field):
                sources = json.loads(original)
                sources['payloads'][0][field] = value
                (self.directory / 'SOURCES.json').write_text(json.dumps(sources, sort_keys=True))
                self.resign_manifest()
                with self.assertRaisesRegex(ValueError, 'SOURCES payload'):
                    verifier.verify_packet(self.directory, self.wrapper)

    def test_known_eight_file_fixture_passes(self):
        report = verifier.verify_packet(self.directory, self.wrapper)
        self.assertTrue(report['passed'])
        self.assertEqual(report['packet_files'], 8)
        self.assertEqual(report['manifest_entries'], 7)
        self.assertEqual(report['sources_payload_bindings'], 2)
        self.assertEqual(report['scientific_effect'], 'NONE')
        self.assertFalse(report['archived_code_executed'])

    def test_reject_duplicate_manifest_path(self):
        manifest = json.loads((self.directory / 'MANIFEST.json').read_text())
        manifest['files'].append(dict(manifest['files'][0]))
        (self.directory / 'MANIFEST.json').write_text(json.dumps(manifest))
        with self.assertRaisesRegex(ValueError, 'duplicate manifest path'):
            verifier.verify_packet(self.directory, self.wrapper)

    def test_reject_missing_declared_file(self):
        (self.directory / 'README.md').unlink()
        with self.assertRaisesRegex(ValueError, 'file set'):
            verifier.verify_packet(self.directory, self.wrapper)

    def test_reject_unsafe_manifest_paths_before_reading(self):
        original = (self.directory / 'MANIFEST.json').read_text()
        for path in ('../README.md', 'nested/file', '/absolute', '\\absolute', '.', '..', '', 'bad\0name', 'MANIFEST.json'):
            with self.subTest(path=path):
                manifest = json.loads(original)
                manifest['files'][0]['path'] = path
                (self.directory / 'MANIFEST.json').write_text(json.dumps(manifest))
                with self.assertRaisesRegex(ValueError, 'unsafe manifest path'):
                    verifier.verify_packet(self.directory, self.wrapper)

    def test_reject_file_and_directory_symlinks(self):
        leaf = self.directory / 'README.md'
        leaf.unlink()
        leaf.symlink_to('SOURCES.json')
        with self.assertRaisesRegex(ValueError, 'symlink'):
            verifier.verify_packet(self.directory, self.wrapper)
        link = self.directory.parent / 'linked-packet'
        link.symlink_to(self.directory, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'symlink'):
            verifier.verify_packet(link, self.wrapper)

    def test_reject_nonfile_directory_entry(self):
        leaf = self.directory / 'README.md'
        leaf.unlink()
        leaf.mkdir()
        with self.assertRaisesRegex(ValueError, 'regular file'):
            verifier.verify_packet(self.directory, self.wrapper)

    def test_reject_changed_data_and_each_manifest_identity_field(self):
        readme = self.directory / 'README.md'
        original_bytes = readme.read_bytes()
        readme.write_bytes(original_bytes + b'changed')
        with self.assertRaisesRegex(ValueError, 'packet file identity'):
            verifier.verify_packet(self.directory, self.wrapper)
        readme.write_bytes(original_bytes)
        original_manifest = (self.directory / 'MANIFEST.json').read_text()
        for field, value in (('bytes', -1), ('sha256', '0' * 64), ('git_blob', '0' * 40)):
            with self.subTest(field=field):
                manifest = json.loads(original_manifest)
                entry = next(item for item in manifest['files'] if item['path'] == 'README.md')
                entry[field] = value
                (self.directory / 'MANIFEST.json').write_text(json.dumps(manifest))
                with self.assertRaisesRegex(ValueError, 'packet file identity'):
                    verifier.verify_packet(self.directory, self.wrapper)

    def test_reject_duplicate_and_missing_sources_payloads(self):
        original = (self.directory / 'SOURCES.json').read_text()
        for variant in ('duplicate', 'missing'):
            with self.subTest(variant=variant):
                sources = json.loads(original)
                payloads = sources['payloads']
                sources['payloads'] = [payloads[0], payloads[0]] if variant == 'duplicate' else payloads[:1]
                (self.directory / 'SOURCES.json').write_text(json.dumps(sources))
                self.resign_manifest()
                with self.assertRaisesRegex(ValueError, 'SOURCES payload'):
                    verifier.verify_packet(self.directory, self.wrapper)

    def test_reject_jointly_resigned_archived_bytes_and_sources(self):
        name = 'GP-DATA-114-v1.0_uniform_q_degree4_interval.py'
        payload = self.directory / name
        changed = payload.read_bytes() + b'\n'
        payload.write_bytes(changed)
        sources = json.loads((self.directory / 'SOURCES.json').read_text())
        source = sources['payloads'][0]
        source['bytes'] = len(changed)
        source['sha256'] = hashlib.sha256(changed).hexdigest()
        source['git_blob'] = hashlib.sha1(b'blob ' + str(len(changed)).encode() + b'\0' + changed).hexdigest()
        (self.directory / 'SOURCES.json').write_text(json.dumps(sources))
        self.resign_manifest()
        with self.assertRaisesRegex(ValueError, 'SOURCES payload'):
            verifier.verify_packet(self.directory, self.wrapper)

    def test_cli_failure_exits_one_and_matches_in_both_modes(self):
        (self.directory / 'undeclared.txt').write_bytes(b'extra')
        wrapper_path = self.directory.parent / 'wrapper.txt'
        wrapper_path.write_bytes(self.wrapper)
        outputs = []
        for flags in (('-B', '-S'), ('-B', '-O', '-S')):
            command = [sys.executable, *flags, str(HERE / 'verify_packet.py'),
                       '--packet', str(self.directory), '--wrapper-input', str(wrapper_path)]
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            summary = json.loads(result.stdout)
            self.assertFalse(summary['passed'])
            self.assertIn('file set', summary['error'])
            self.assertEqual(summary['scientific_effect'], 'NONE')
            outputs.append(result.stdout)
        self.assertEqual(*outputs)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--wrapper-input', default='/tmp/gpdata114-public-wrapper.txt')
    args = parser.parse_args()
    WRAPPER_RAW = Path(args.wrapper_input).read_bytes()
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(PacketControls))
    print(json.dumps({'tests_run': result.testsRun, 'failures': len(result.failures),
                      'errors': len(result.errors), 'passed': result.wasSuccessful(),
                      'scientific_effect': 'NONE', 'archived_code_executed': False}, sort_keys=True))
    sys.exit(0 if result.wasSuccessful() else 1)
