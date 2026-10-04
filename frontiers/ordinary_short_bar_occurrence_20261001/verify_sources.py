"""Finite exact controls and source identity; not a continuum proof certificate."""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path, PurePosixPath

SOURCE_MANIFEST_SHA256 = '1676f2411b86e607aecbe061130cf10ba805c1cf39bba8fff56c5fa796b91d03'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def contained_file(root, relative):
    require(isinstance(relative, str) and bool(relative), 'invalid source path')
    parts = PurePosixPath(relative)
    require(not parts.is_absolute() and str(parts) == relative
            and all(p not in ('', '.', '..') for p in parts.parts)
            and '\\\\' not in relative, 'noncanonical source path')
    target = root
    for part in parts.parts:
        target = target / part
        require(not target.is_symlink(), 'symlink source')
    require(target.is_file() and root in target.resolve().parents,
            'source must be a contained regular file')
    return target


def verify_entry(root, entry):
    root = Path(root).resolve()
    data = contained_file(root, entry.get('local_path')).read_bytes()
    require(type(entry.get('bytes')) is int and len(data) == entry['bytes'],
            'source byte count')
    require(hashlib.sha256(data).hexdigest() == entry.get('sha256'),
            'source SHA256')
    blob = hashlib.sha1(b'blob '+str(len(data)).encode('ascii')+b'\0'+data).hexdigest()
    require(blob == entry.get('blob'), 'source Git blob')


def verify_sources(repo=None, manifest_path=None):
    script = Path(__file__).absolute()
    require(not script.is_symlink(), 'symlink checker')
    root = Path(repo).resolve() if repo is not None else script.resolve().parents[2]
    if manifest_path is None:
        manifest_path = contained_file(root, 'frontiers/ordinary_short_bar_occurrence_20261001/SOURCES.json')
    data = Path(manifest_path).read_bytes()
    require(hashlib.sha256(data).hexdigest() == SOURCE_MANIFEST_SHA256,
            'source manifest digest')
    manifest = json.loads(data)
    entries = manifest['sources']
    require(len(entries) == 7, 'seven exact sources required')
    require(len({e['key'] for e in entries}) == 7, 'duplicate source key')
    for entry in entries:
        verify_entry(root, entry)
    return len(entries)


if __name__ == "__main__":
    print(json.dumps({"verified_sources": verify_sources(), "scope": "Source identity only, not analytic acceptance"}))
