#!/usr/bin/env python3
"""Verify recovered source custody only; never imports or accepts the mathematics."""
import hashlib
import json
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent


def main():
    manifest = json.loads((ROOT / 'MANIFEST.json').read_text())
    records = manifest['files']
    names = [x['path'] for x in records]
    if len(names) != 11 or len(set(names)) != 11:
        raise ValueError('expected eleven distinct raw files')
    if manifest['scientific_effect'] != 'NONE' or manifest['source_labels_adopted'] is not False:
        raise ValueError('custody must not adopt scientific labels')
    actual = {p.relative_to(ROOT).as_posix() for p in (ROOT / 'raw').rglob('*') if p.is_file()}
    if actual != set(names):
        raise ValueError('raw file inventory mismatch')
    for item in records:
        name = PurePosixPath(item['path'])
        if name.is_absolute() or '..' in name.parts or name.parts[0] != 'raw':
            raise ValueError('unsafe raw path')
        path = ROOT / name
        if any((ROOT / Path(*name.parts[:i])).is_symlink() for i in range(1, len(name.parts) + 1)):
            raise ValueError('symlink rejected')
        raw = path.read_bytes()
        dropbox = hashlib.sha256(b''.join(hashlib.sha256(raw[i:i+4194304]).digest()
                                for i in range(0, len(raw), 4194304))).hexdigest()
        blob = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        if (len(raw), hashlib.sha256(raw).hexdigest(), dropbox, blob) != (
                item['bytes'], item['sha256'], item['dropbox_content_hash'], item['git_blob_sha1']):
            raise ValueError('source identity mismatch: ' + item['path'])
    print('CUSTODY VERIFIED: 11 raw files; scientific effect NONE; no numerical certification')


if __name__ == '__main__':
    main()
