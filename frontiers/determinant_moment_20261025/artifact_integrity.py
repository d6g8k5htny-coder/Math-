#!/usr/bin/env python3
"""Check downloaded determinant receipt/log bytes; never award a kernel result."""
import argparse
import hashlib
from io import BytesIO
import json
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import zipfile

HEX40 = re.compile(r'[0-9a-f]{40}')
HEX64 = re.compile(r'[0-9a-f]{64}')
MAX_ARCHIVE = 64 * 1024 * 1024
MAX_TOTAL = 256 * 1024 * 1024
MAX_ENTRIES = 10000


class IntegrityError(ValueError):
    def __init__(self, code, message):
        self.code = code
        super().__init__(message)


def fail(code, message):
    raise IntegrityError(code, message)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            fail('DUPLICATE_JSON_KEY', 'duplicate receipt JSON key: ' + key)
        result[key] = value
    return result


def validate_member_path(name):
    path = PurePosixPath(name)
    normalized = str(path) + ('/' if name.endswith('/') else '')
    if not name or name != normalized or path.is_absolute() or '..' in path.parts or '\\' in name:
        fail('UNSAFE_MEMBER_PATH', 'unsafe archive member path')


def inspect_archive(archive, expected_commit, expected_manifest):
    if not isinstance(expected_commit, str) or not HEX40.fullmatch(expected_commit):
        fail('INVALID_EXPECTED_IDENTITY', 'expected commit must be a full lowercase Git SHA')
    if not isinstance(expected_manifest, str) or not HEX64.fullmatch(expected_manifest):
        fail('INVALID_EXPECTED_IDENTITY', 'expected manifest must be a full lowercase SHA256')
    archive = Path(archive)
    with archive.open('rb') as stream:
        archive_bytes = stream.read(MAX_ARCHIVE + 1)
    if len(archive_bytes) > MAX_ARCHIVE:
        fail('ARCHIVE_LIMIT', 'compressed artifact exceeds the declared byte limit')
    with zipfile.ZipFile(BytesIO(archive_bytes)) as bundle:
        members = bundle.infolist()
        if not members or len(members) > MAX_ENTRIES:
            fail('ARCHIVE_LIMIT', 'empty artifact or too many entries')
        infos = {}
        total = 0
        for info in members:
            name = info.filename
            validate_member_path(name)
            if name in infos:
                fail('DUPLICATE_MEMBER', 'duplicate archive member: ' + name)
            mode = stat.S_IFMT(info.external_attr >> 16)
            if mode not in (0, stat.S_IFREG, stat.S_IFDIR):
                fail('SPECIAL_MEMBER', 'symlink or special archive member')
            if info.flag_bits & 1:
                fail('ENCRYPTED_MEMBER', 'encrypted archive member')
            total += info.file_size
            if info.file_size > MAX_TOTAL or total > MAX_TOTAL:
                fail('ARCHIVE_LIMIT', 'expanded artifact exceeds the declared byte limit')
            infos[name] = info
        if 'receipt.json' not in infos or infos['receipt.json'].is_dir():
            fail('MISSING_RECEIPT', 'missing root receipt.json')
        receipt = json.loads(bundle.read(infos['receipt.json']).decode('utf-8'),
                             object_pairs_hook=unique_object)
        if not isinstance(receipt, dict) or type(receipt.get('schema_version')) is not int or receipt['schema_version'] != 1:
            fail('INVALID_RECEIPT', 'unsupported receipt object/schema')
        if receipt.get('checked_commit') != expected_commit:
            fail('COMMIT_MISMATCH', 'receipt checked_commit differs from the independently supplied run commit')
        if receipt.get('manifest_sha256') != expected_manifest:
            fail('MANIFEST_MISMATCH', 'receipt manifest differs from the independently supplied source manifest')
        logs = receipt.get('logs')
        if not isinstance(logs, dict):
            fail('INVALID_LOGS', 'receipt logs must be an object')
        if not logs:
            fail('EMPTY_LOGS', 'empty log inventory cannot establish artifact integrity')
        results = {}
        for name, expected_hash in logs.items():
            if (not isinstance(name, str) or not name.endswith('.log')
                    or PurePosixPath(name).name != name or '\\' in name
                    or not isinstance(expected_hash, str) or not HEX64.fullmatch(expected_hash)):
                fail('INVALID_LOG_RECORD', 'unsafe log name or invalid SHA256')
            if name not in infos or infos[name].is_dir():
                fail('MISSING_LOG', 'missing receipt-bound log: ' + name)
            actual = hashlib.sha256(bundle.read(infos[name])).hexdigest()
            if actual != expected_hash:
                fail('LOG_HASH_MISMATCH', 'receipt-bound log hash mismatch: ' + name)
            results[name] = actual
    return {
        'schema_version': 1,
        'status': 'PASS',
        'scope': 'DOWNLOADED_BYTE_INTEGRITY_ONLY_NO_KERNEL_CREDIT',
        'archive_sha256': hashlib.sha256(archive_bytes).hexdigest(),
        'archive_entries': len(members),
        'archive_uncompressed_bytes': total,
        'checked_commit': expected_commit,
        'manifest_sha256': expected_manifest,
        'verified_log_count': len(results),
        'verified_logs': results,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', required=True, type=Path)
    parser.add_argument('--expected-commit', required=True)
    parser.add_argument('--expected-manifest', required=True)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        report = inspect_archive(args.archive, args.expected_commit, args.expected_manifest)
    except IntegrityError as error:
        report = {'schema_version': 1, 'status': 'FAIL', 'code': error.code,
                  'error': str(error), 'scope': 'NO_KERNEL_CREDIT'}
    except (OSError, ValueError, UnicodeError, zipfile.BadZipFile, RuntimeError) as error:
        report = {'schema_version': 1, 'status': 'FAIL', 'code': 'INPUT_ERROR',
                  'error': str(error), 'scope': 'NO_KERNEL_CREDIT'}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps(report, sort_keys=True))
    return 0 if report['status'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
