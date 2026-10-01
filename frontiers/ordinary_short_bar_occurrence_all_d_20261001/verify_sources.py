"""Source identity for C52-ALL-D: the seven current_required sources must match bytes, SHA256 and Git blob on the
tree.  The two cited_unmerged C52 files (Math-#235) are recorded only; they are not premises.  Identity only, not
analytic acceptance.

    python3 -B -S verify_sources.py"""
import hashlib
import json
import sys
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MANIFEST_SHA256 = '44fc416116eca6bbf56c029329930212c0b108ee1bb9174ca8f3b41ad1b78991'


def require(cond, msg):
    if not cond:
        raise ValueError(msg)


def contained(rel):
    require(isinstance(rel, str) and rel, 'invalid path')
    parts = PurePosixPath(rel)
    require(not parts.is_absolute() and str(parts) == rel and all(p not in ('', '.', '..') for p in parts.parts),
            'noncanonical path ' + rel)
    t = ROOT
    for p in parts.parts:
        t = t / p
        require(not t.is_symlink(), 'symlink ' + rel)
    require(t.is_file() and ROOT in t.resolve().parents, 'not a contained regular file: ' + rel)
    return t


def verify():
    raw = contained('frontiers/ordinary_short_bar_occurrence_all_d_20261001/SOURCES.json').read_bytes()
    require(hashlib.sha256(raw).hexdigest() == MANIFEST_SHA256, 'manifest digest')
    man = json.loads(raw)
    req = man['current_required']
    require(len(req) == 7 and len({e['key'] for e in req}) == 7, 'seven distinct required sources')
    for e in req:
        data = contained(e['local_path']).read_bytes()
        require(type(e['bytes']) is int and len(data) == e['bytes'], 'bytes ' + e['key'])
        require(hashlib.sha256(data).hexdigest() == e['sha256'], 'sha256 ' + e['key'])
        blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        require(blob == e['blob'], 'blob ' + e['key'])
    require(all(e['pr'] == 'Math-#235' for e in man['cited_unmerged']), 'cited entries')
    return len(req)


if __name__ == '__main__':
    try:
        n = verify()
    except ValueError as exc:
        print('source verification FAILED:', exc)
        sys.exit(1)
    print(json.dumps({'verified_sources': n, 'scope': 'source identity only, not analytic acceptance'}))
