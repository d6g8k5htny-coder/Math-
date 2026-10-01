"""Source identity for C52-ALL-D.  Identity only, not analytic acceptance.

current_required (seven): for each entry the working-tree copy at `local_path` and the historical entry
`commit:path` must both be the recorded blob, with the recorded byte count and SHA256 (`git ls-tree --full-tree`).
cited_unmerged (two C52 files of Math-#235): checked the same way when the commit object is present locally, otherwise
reported as unavailable.  They are not premises.  CI checks out full history (fetch-depth: 0).  Git replacement objects
are disabled (--no-replace-objects, GIT_NO_REPLACE_OBJECTS=1), so a local refs/replace entry cannot redirect a pin.

    python3 -B -S verify_sources.py"""
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MANIFEST_SHA256 = '44fc416116eca6bbf56c029329930212c0b108ee1bb9174ca8f3b41ad1b78991'


def require(cond, msg):
    if not cond:
        raise ValueError(msg)


GIT_ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')  # refs/replace must never redirect a pinned commit (OA-236-ENG-01)


def git(*args):
    p = subprocess.run(['git', '--no-replace-objects', '-C', str(ROOT)] + list(args), capture_output=True, env=GIT_ENV)
    if p.returncode:
        raise ValueError('git %s failed: %s' % (args[0], p.stderr.decode(errors='replace').strip()))
    return p.stdout


def canonical(rel):
    require(isinstance(rel, str) and rel, 'invalid path')
    parts = PurePosixPath(rel)
    require(not parts.is_absolute() and str(parts) == rel and all(p not in ('', '.', '..') for p in parts.parts),
            'noncanonical path ' + rel)
    return parts


def contained(rel):
    parts = canonical(rel)
    t = ROOT
    for p in parts.parts:
        t = t / p
        require(not t.is_symlink(), 'symlink ' + rel)
    require(t.is_file() and ROOT in t.resolve().parents, 'not a contained regular file: ' + rel)
    return t


def identity_ok(data, e):
    blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    return len(data) == e['bytes'] and hashlib.sha256(data).hexdigest() == e['sha256'] and blob == e['blob']


def historical(e):
    """commit:path must be exactly the recorded regular-file blob, whose bytes match the record"""
    commit, path, blob = e['commit'], e['path'], e['blob']
    require(re.fullmatch('[0-9a-f]{40}', commit) and re.fullmatch('[0-9a-f]{40}', blob), 'identity format ' + e['key'])
    canonical(path)
    require(git('cat-file', '-t', commit).strip() == b'commit', e['key'] + ': not a commit')
    listing = git('ls-tree', '--full-tree', '-z', commit, '--', path)
    require(listing == ('100644 blob %s\t%s\0' % (blob, path)).encode(), e['key'] + ': commit/path/blob mismatch')
    require(identity_ok(git('cat-file', 'blob', blob), e), e['key'] + ': historical bytes mismatch')


def commit_present(commit):
    p = subprocess.run(['git', '--no-replace-objects', '-C', str(ROOT), 'cat-file', '-t', commit], capture_output=True,
                       env=GIT_ENV)
    return p.returncode == 0 and p.stdout.strip() == b'commit'


def verify():
    raw = contained('frontiers/ordinary_short_bar_occurrence_all_d_20261001/SOURCES.json').read_bytes()
    require(hashlib.sha256(raw).hexdigest() == MANIFEST_SHA256, 'manifest digest')
    man = json.loads(raw)
    req = man['current_required']
    require(len(req) == 7 and len({e['key'] for e in req}) == 7, 'seven distinct required sources')
    for e in req:
        require(type(e['bytes']) is int and e['bytes'] > 0, 'bytes ' + e['key'])
        require(e['local_path'] == e['path'], 'local path differs from pinned path ' + e['key'])
        require(identity_ok(contained(e['local_path']).read_bytes(), e), 'working-tree bytes ' + e['key'])
        historical(e)
    cited = {}
    for e in man['cited_unmerged']:
        require(e['pr'] == 'Math-#235', 'cited entry ' + e['key'])
        if commit_present(e['commit']):
            historical(e)
            cited[e['key']] = 'verified'
        else:
            cited[e['key']] = 'commit not present locally (not a premise)'
    return len(req), cited


if __name__ == '__main__':
    try:
        n, cited = verify()
    except ValueError as exc:
        print('source verification FAILED:', exc)
        sys.exit(1)
    print(json.dumps({'verified_sources': n, 'cited_unmerged': cited,
                      'scope': 'source identity only, not analytic acceptance'}))
