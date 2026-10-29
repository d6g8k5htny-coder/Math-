"""Real ZIP/CLI fixtures for byte transport only; no Lean is executed."""
import hashlib
import importlib.util
import json
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
import warnings
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('determinant_artifact_integrity', ROOT / 'artifact_integrity.py')
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)
COMMIT = 'a' * 40
MANIFEST = 'b' * 64
LOGS = {'build.log': b'SYNTHETIC build fixture; NO LEAN EXECUTED\n',
        'kernel.log': b'SYNTHETIC kernel fixture; NO LEAN EXECUTED\n'}


class ArchiveIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='determinant-archive-test-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.archive = self.root / 'artifact.zip'

    def write(self, *, receipt=None, payloads=None, raw_receipt=None, extra=()):
        if receipt is None:
            receipt = {'schema_version': 1, 'checked_commit': COMMIT,
                       'manifest_sha256': MANIFEST,
                       'logs': {k: hashlib.sha256(v).hexdigest() for k, v in LOGS.items()}}
        if payloads is None:
            payloads = LOGS
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', UserWarning)
            with zipfile.ZipFile(self.archive, 'w', compression=zipfile.ZIP_DEFLATED) as bundle:
                for name, value in payloads.items():
                    bundle.writestr(name, value)
                bundle.writestr('receipt.json', raw_receipt if raw_receipt is not None else json.dumps(receipt))
                for name, value in extra:
                    bundle.writestr(name, value)
        return receipt

    def audit(self, commit=COMMIT, manifest=MANIFEST):
        return checker.inspect_archive(self.archive, commit, manifest)

    def reject(self, code):
        with self.assertRaises(checker.IntegrityError) as caught:
            self.audit()
        self.assertEqual(caught.exception.code, code)

    def test_complete_zip_authenticates_every_log_without_kernel_credit(self):
        self.write()
        report = self.audit()
        self.assertEqual(report['status'], 'PASS')
        self.assertEqual(report['verified_log_count'], 2)
        self.assertEqual(set(report['verified_logs']), set(LOGS))
        self.assertEqual(report['scope'], 'DOWNLOADED_BYTE_INTEGRITY_ONLY_NO_KERNEL_CREDIT')
        self.assertEqual(report['archive_sha256'], hashlib.sha256(self.archive.read_bytes()).hexdigest())

    def test_path_replacement_cannot_relabel_inspected_archive_bytes(self):
        self.write()
        original = self.archive.read_bytes()
        replacement_bytes = b'SYNTHETIC replacement after inspection; not a ZIP\n'
        replacement = self.root / 'replacement.zip'
        replacement.write_bytes(replacement_bytes)
        close_zip = zipfile.ZipFile.__exit__

        def replace_path_after_close(bundle, *exception):
            result = close_zip(bundle, *exception)
            replacement.replace(self.archive)
            return result

        # Only schedule a real pathname replacement; ZIP reads and hashing stay real.
        with mock.patch.object(zipfile.ZipFile, '__exit__', replace_path_after_close):
            report = self.audit()
        self.assertEqual(self.archive.read_bytes(), replacement_bytes)
        self.assertEqual(report['status'], 'PASS')
        self.assertEqual(report['archive_sha256'], hashlib.sha256(original).hexdigest())
        self.assertEqual(report['verified_log_count'], len(LOGS))

    def test_corrupt_payload_refused(self):
        self.write(payloads={**LOGS, 'kernel.log': b'changed after receipt'})
        self.reject('LOG_HASH_MISMATCH')

    def test_wrong_commit_refused(self):
        receipt = self.write()
        receipt['checked_commit'] = 'c' * 40
        self.write(receipt=receipt)
        self.reject('COMMIT_MISMATCH')

    def test_wrong_manifest_refused(self):
        receipt = self.write()
        receipt['manifest_sha256'] = 'c' * 64
        self.write(receipt=receipt)
        self.reject('MANIFEST_MISMATCH')

    def test_duplicate_members_refused(self):
        self.write(extra=[('kernel.log', LOGS['kernel.log'])])
        self.reject('DUPLICATE_MEMBER')

    def test_unsafe_extra_member_refused(self):
        self.write(extra=[('../unreferenced.txt', b'unsafe even when not in receipt')])
        self.reject('UNSAFE_MEMBER_PATH')

    def test_missing_log_refused(self):
        self.write(payloads={'build.log': LOGS['build.log']})
        self.reject('MISSING_LOG')

    def test_empty_log_inventory_refused(self):
        receipt = self.write()
        receipt['logs'] = {}
        self.write(receipt=receipt)
        self.reject('EMPTY_LOGS')

    def test_duplicate_json_key_refused(self):
        receipt = self.write()
        raw = json.dumps(receipt).replace('"schema_version": 1', '"schema_version": 1, "schema_version": 1')
        self.write(raw_receipt=raw)
        self.reject('DUPLICATE_JSON_KEY')

    def test_invalid_schema_and_logs_refused(self):
        baseline = self.write()
        for key, value, code in [('schema_version', True, 'INVALID_RECEIPT'),
                                 ('schema_version', 2, 'INVALID_RECEIPT'),
                                 ('logs', [], 'INVALID_LOGS')]:
            with self.subTest(key=key, value=value):
                self.write(receipt={**baseline, key: value})
                self.reject(code)

    def test_invalid_log_path_or_digest_refused(self):
        baseline = self.write()
        for logs in [{'../kernel.log': 'a' * 64}, {'kernel.log': 'A' * 64},
                     {'kernel.log': 1}, {'kernel.txt': 'a' * 64}]:
            with self.subTest(logs=logs):
                self.write(receipt={**baseline, 'logs': logs})
                self.reject('INVALID_LOG_RECORD')

    def test_missing_receipt_refused(self):
        with zipfile.ZipFile(self.archive, 'w') as bundle:
            bundle.writestr('kernel.log', LOGS['kernel.log'])
        self.reject('MISSING_RECEIPT')

    def test_symlink_member_refused(self):
        info = zipfile.ZipInfo('alias')
        info.create_system = 3
        info.external_attr = (stat.S_IFLNK | 0o777) << 16
        self.write(extra=[(info, 'kernel.log')])
        self.reject('SPECIAL_MEMBER')

    def test_encrypted_flag_refused_before_payload_read(self):
        self.write()
        raw = bytearray(self.archive.read_bytes())
        for marker, flag_offset in [(b'PK\x03\x04', 6), (b'PK\x01\x02', 8)]:
            start = 0
            while True:
                index = raw.find(marker, start)
                if index < 0:
                    break
                raw[index + flag_offset] |= 1
                start = index + len(marker)
        self.archive.write_bytes(raw)
        self.reject('ENCRYPTED_MEMBER')

    def test_declared_resource_limits_refuse_instead_of_skipping(self):
        self.write()
        for setting in ['MAX_ARCHIVE', 'MAX_TOTAL', 'MAX_ENTRIES']:
            with self.subTest(setting=setting), mock.patch.object(checker, setting, 1):
                self.reject('ARCHIVE_LIMIT')

    def test_invalid_independent_identity_refused(self):
        self.write()
        for commit, manifest in [('a', MANIFEST), (COMMIT, 'b'), ('A' * 40, MANIFEST)]:
            with self.subTest(commit=commit, manifest=manifest):
                with self.assertRaises(checker.IntegrityError) as caught:
                    self.audit(commit, manifest)
                self.assertEqual(caught.exception.code, 'INVALID_EXPECTED_IDENTITY')

    def test_real_cli_preserves_positive_and_intended_failure_reports(self):
        for corrupt in [False, True]:
            with self.subTest(corrupt=corrupt):
                self.write(payloads={**LOGS, 'kernel.log': b'corruption'} if corrupt else None)
                output = self.root / ('bad.json' if corrupt else 'good.json')
                command = [sys.executable, '-B', '-S'] + (['-O'] if sys.flags.optimize else []) + [
                    str(ROOT / 'artifact_integrity.py'), '--archive', str(self.archive),
                    '--expected-commit', COMMIT, '--expected-manifest', MANIFEST,
                    '--output', str(output)]
                run = subprocess.run(command, capture_output=True, text=True, timeout=30)
                self.assertEqual(run.returncode, 1 if corrupt else 0, run.stderr)
                report = json.loads(output.read_text())
                self.assertEqual(report['status'], 'FAIL' if corrupt else 'PASS')
                if corrupt:
                    self.assertEqual(report['code'], 'LOG_HASH_MISMATCH')
                else:
                    self.assertEqual(report['verified_log_count'], 2)


if __name__ == '__main__':
    unittest.main()
