"""Verify exact packet custody; never execute, import or compile archived code.

Only the new inert_decoder module is imported. Both recovered payloads,
including the archived .py file, are handled solely as bytes. A re-signed
manifest cannot override the decoder's independent original payload pins.
This verifier supplies custody checks, not mathematical or status acceptance.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

import inert_decoder as decoder

MANIFEST = 'MANIFEST.json'
DEFAULT_WRAPPER = '/tmp/gpdata114-public-wrapper.txt'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON key: ' + key)
        result[key] = value
    return result


def load_record(raw, context):
    value = json.loads(raw, object_pairs_hook=unique_object)
    require(isinstance(value, dict), context + ' must be a JSON object')
    return value


def safe_manifest_path(name):
    require(isinstance(name, str) and name and name not in {'.', '..', MANIFEST}
            and not any(c in name for c in '/\\\0'), 'unsafe manifest path')


def identity(raw):
    framed = b'blob ' + str(len(raw)).encode('ascii') + b'\0' + raw
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
            'git_blob': hashlib.sha1(framed).hexdigest()}


def exact_field(record, field, expected, context):
    actual = record.get(field)
    require(type(actual) is type(expected) and actual == expected,
            context + ': ' + field)


def verify_packet(directory, wrapper_raw):
    directory = Path(directory)
    require(not directory.is_symlink(), 'packet directory symlink')
    require(directory.is_dir(), 'packet must be a directory')
    observed = {}
    for path in directory.iterdir():
        require(not path.is_symlink(), 'packet file symlink: ' + path.name)
        require(path.is_file(), 'packet entry must be a regular file: ' + path.name)
        observed[path.name] = path
    require(MANIFEST in observed, 'packet file set missing MANIFEST.json')
    manifest = load_record(observed[MANIFEST].read_bytes(), 'manifest')
    require(manifest.get('manifest_self_excluded') is True, 'manifest self-exclusion required')
    require(isinstance(manifest.get('files'), list), 'manifest files must be a list')
    entries = {}
    for entry in manifest['files']:
        require(isinstance(entry, dict), 'manifest entry must be an object')
        name = entry.get('path')
        safe_manifest_path(name)
        require(name not in entries, 'duplicate manifest path: ' + name)
        entries[name] = entry
    expected_names = set(entries) | {MANIFEST}
    actual_names = set(observed)
    require(actual_names == expected_names,
            'packet file set mismatch: extra=' + ','.join(sorted(actual_names - expected_names))
            + ' missing=' + ','.join(sorted(expected_names - actual_names)))

    stored = {}
    for name, entry in entries.items():
        data = observed[name].read_bytes()
        for field, expected in identity(data).items():
            exact_field(entry, field, expected, 'packet file identity mismatch: ' + name)
        stored[name] = data

    require('SOURCES.json' in stored, 'SOURCES record missing from manifest')
    sources = load_record(stored['SOURCES.json'], 'SOURCES')
    payloads = sources.get('payloads')
    require(isinstance(payloads, list) and len(payloads) == len(decoder.SPECS),
            'SOURCES payload list must contain exactly the canonical pair')
    source_entries = {}
    for payload in payloads:
        require(isinstance(payload, dict), 'SOURCES payload must be an object')
        label = payload.get('label')
        require(isinstance(label, str) and label not in source_entries,
                'SOURCES payload duplicate or invalid label')
        source_entries[label] = payload
    require(set(source_entries) == {spec.label for spec in decoder.SPECS},
            'SOURCES payload labels differ from canonical pair')

    require(isinstance(wrapper_raw, bytes), 'wrapper input must be exact bytes')
    decoded = decoder.decode_wrapper(wrapper_raw)
    wrapper = sources.get('wrapper')
    require(isinstance(wrapper, dict), 'SOURCES wrapper must be an object')
    wrapper_pin = decoder.WRAPPER_IDENTITY
    for field, expected in (('bytes', wrapper_pin.bytes), ('sha256', wrapper_pin.sha256),
                            ('git_blob', wrapper_pin.blob)):
        exact_field(wrapper, field, expected, 'SOURCES wrapper identity mismatch')

    for spec in decoder.SPECS:
        payload = source_entries[spec.label]
        expected_fields = {
            'label': spec.label, 'path': spec.source.name, 'bytes': spec.source.bytes,
            'sha256': spec.source.sha256, 'git_blob': spec.source.blob,
            'gzip_bytes': spec.gzip.bytes, 'gzip_sha256': spec.gzip.sha256,
        }
        for field, expected in expected_fields.items():
            exact_field(payload, field, expected, 'SOURCES payload identity mismatch: ' + spec.label)
        require(spec.source.name in entries, 'payload missing from manifest: ' + spec.label)
        # decode_wrapper already binds each compressed member, its declarations,
        # and decoded bytes to SPECS. Bind the resulting raw identity again to
        # both independently pinned SPECS and the two packet metadata records.
        for field, actual in identity(decoded[spec.source.name]).items():
            exact_field(payload, field, actual, 'SOURCES payload decoded identity mismatch: ' + spec.label)
            exact_field(entries[spec.source.name], field, actual, 'manifest decoded payload identity mismatch: ' + spec.label)
    decoder.verify_existing(directory, decoded)
    report = decoder.report(decoded)
    report.update({'passed': True, 'packet_files': len(observed),
                   'manifest_entries': len(entries), 'sources_payload_bindings': len(source_entries),
                   'archived_code_imported': False, 'archived_code_compiled': False})
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--packet', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--wrapper-input', type=Path, default=Path(DEFAULT_WRAPPER))
    args = parser.parse_args()
    try:
        with args.wrapper_input.open('rb') as stream:
            wrapper_raw = stream.read(65537)
        report = verify_packet(args.packet, wrapper_raw)
        exit_code = 0
    except (OSError, ValueError) as exc:
        report = {'passed': False, 'error': str(exc), 'scientific_effect': 'NONE',
                  'archived_code_executed': False, 'archived_code_imported': False,
                  'archived_code_compiled': False}
        exit_code = 1
    print(json.dumps(report, sort_keys=True))
    return exit_code


if __name__ == '__main__':
    sys.exit(main())
