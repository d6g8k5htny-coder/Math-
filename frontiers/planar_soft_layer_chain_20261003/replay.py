#!/usr/bin/env python3
"""Verify the stored C91–C103 records and replay their published checkers (standard library only).

Every file in this packet except replay.py, README.md and SOURCES.json is one of two things:
  - an exact copy of a public comment body on main#229;
  - a payload extracted verbatim from such a comment.
SOURCES.json pins each file by byte count and SHA256. This script performs four checks.

  1. The packet tree equals SOURCES.json's file list, with no symlinks, and every stored file has its pinned
     identity. C96's frozen proof (7657 bytes, SHA256 7198ff63...) is the tail of its native comment.
  2. Each published checker in SOURCES.json runs under the current interpreter's -O/-S flags. Its stdout must
     equal the published bytes. A few checkers print their interpreter version, and SOURCES.json records
     which line. On that line only, the published version is replaced by the replaying interpreter's
     version, and every other byte must be identical. This is the reconciliation the C99/C101/C103
     handoffs ask for; it does not claim whole-stdout identity across Python versions.
  3. C102's checker reads a source tree. It is assembled in a temporary directory from the stored copies
     and the repository paths named in C102/SOURCE_IDENTITIES.json, each identity-checked first.
  4. Negative controls must be rejected:
     - a one-byte change to a stored proof;
     - a C93 checker with one changed constant;
     - a changed byte outside a version line.

Reproducibility only. The analytic proofs and their reviews carry the mathematics. These finite checkers
support algebra, as each review says. Nothing here reads or grades a proof.

Usage: python3 -B -S frontiers/planar_soft_layer_chain_20261003/replay.py   (exit 0 iff every check passes)
"""
import hashlib
import json
import pathlib
import platform
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OWN = {'README.md', 'SOURCES.json', 'replay.py'}
C96_SUFFIX = (7657, '7198ff636e330749428ded6938776dad612f6bdb51ad62359b445f016df13a7a')


def identity(data):
    return len(data), hashlib.sha256(data).hexdigest()


def interpreter_flags():
    flags = ['-B']
    if sys.flags.optimize:
        flags.append('-O')
    if sys.flags.no_site:
        flags.append('-S')
    return flags


def tree_failures(root, manifest):
    failures = []
    listed = {f['path']: (f['bytes'], f['sha256']) for f in manifest['files']}
    present = set()
    for path in sorted(root.rglob('*')):
        rel = path.relative_to(root).as_posix()
        if path.is_symlink():
            failures.append('symlink: ' + rel)
        elif path.is_file():
            present.add(rel)
    for rel in sorted(present ^ (set(listed) | OWN)):
        failures.append(('unlisted file: ' if rel in present else 'missing file: ') + rel)
    for rel, ident in sorted(listed.items()):
        if rel in present and identity((root / rel).read_bytes()) != ident:
            failures.append('identity mismatch: ' + rel)
    return failures


def same_output(published, replayed, version_line):
    """Exact equality, or equality except the recorded version line rendered at this interpreter."""
    if version_line is None:
        return replayed == published
    pub, rep = published.decode('utf-8').split('\n'), replayed.decode('utf-8', 'replace').split('\n')
    index, template = version_line['index'], version_line['template']
    if len(pub) != len(rep) or pub[index] != template.format(version=version_line['published_version']):
        return False
    if rep[index] != template.format(version=platform.python_version()):
        return False
    return all(a == b for i, (a, b) in enumerate(zip(pub, rep)) if i != index)


def run(script, cwd):
    proc = subprocess.run([sys.executable, *interpreter_flags(), str(script)], capture_output=True,
                          timeout=900, cwd=str(cwd))
    return proc.returncode, proc.stdout


def run_with_tree(packet, replay):
    """C102: BASE/PROOF.md, BASE/SOURCE_IDENTITIES.json, BASE/sources/<key>.md, BASE/review/<script>."""
    tree = replay['tree']
    rows = json.loads((packet / tree['identities']).read_text(encoding='utf-8'))
    with tempfile.TemporaryDirectory() as tmp:
        base = pathlib.Path(tmp)
        (base / 'sources').mkdir()
        (base / 'review').mkdir()
        shutil.copyfile(packet / replay['script'].split('/')[0] / 'PROOF.md', base / 'PROOF.md')
        shutil.copyfile(packet / tree['identities'], base / 'SOURCE_IDENTITIES.json')
        for row in rows:
            rel = tree['sources'][row['key']]
            source = packet / rel if rel.startswith('C9') else ROOT / rel
            data = source.read_bytes()
            if identity(data) != (row['bytes'], row['sha256']):
                return None, b'source identity mismatch: ' + row['key'].encode()
            (base / row['local_path']).write_bytes(data)
        script = base / 'review' / pathlib.Path(replay['script']).name
        shutil.copyfile(packet / replay['script'], script)
        return run(script, base)


def replay_all(packet, manifest):
    failures, digests = [], {}
    for obj in manifest['objects']:
        for replay in obj.get('replays', []):
            label = '%s %s' % (obj['tag'], replay['name'])
            if 'tree' in replay:
                code, out = run_with_tree(packet, replay)
            else:
                script = packet / replay['script']
                code, out = run(script, script.parent)
            digests[label] = identity(out)[1]
            if code != 0:
                failures.append('%s: exit code %s' % (label, code))
            if not same_output((packet / replay['stdout']).read_bytes(), out, replay.get('version_line')):
                failures.append('%s: stdout differs from the published bytes' % label)
    return failures, digests


def main():
    manifest = json.loads((HERE / 'SOURCES.json').read_text(encoding='utf-8'))
    failures = tree_failures(HERE, manifest)
    if identity((HERE / 'C96' / 'PROOF.md').read_bytes()[-C96_SUFFIX[0]:]) != C96_SUFFIX:
        failures.append('C96 frozen-proof suffix identity mismatch')
    replay_failures, digests = replay_all(HERE, manifest)
    failures += replay_failures

    with tempfile.TemporaryDirectory() as tmp:
        copy = pathlib.Path(tmp) / 'packet'
        shutil.copytree(HERE, copy, symlinks=True)
        target = copy / 'C91' / 'PROOF.md'
        data = bytearray(target.read_bytes())
        data[100] ^= 0x01
        target.write_bytes(bytes(data))
        if 'identity mismatch: C91/PROOF.md' not in tree_failures(copy, manifest):
            failures.append('negative control: a one-byte change to C91/PROOF.md was not detected')
        script = copy / 'C93' / 'checker.py'
        source = script.read_text(encoding='utf-8')
        mutated = source.replace('24 * lam - gamma ** 2 + 12 * b', '24 * lam - gamma ** 2 + 13 * b', 1)
        if mutated == source:
            failures.append('negative control could not mutate the C93 checker')
        else:
            script.write_text(mutated, encoding='utf-8')
            code, out = run(script, script.parent)
            if code == 0 and out == (copy / 'C93' / 'checker_stdout.txt').read_bytes():
                failures.append('negative control: a mutated C93 checker reproduced its published stdout')
    c99 = next(r for o in manifest['objects'] if o['tag'] == 'C99' for r in o['replays'] if r['name'] == 'checker')
    published = (HERE / c99['stdout']).read_bytes()
    vline = c99['version_line']
    lines = published.decode('utf-8').split('\n')
    lines[vline['index']] = vline['template'].format(version=platform.python_version())
    good = '\n'.join(lines).encode('utf-8')
    other = 0 if vline['index'] != 0 else 1
    lines[other] = lines[other] + ' '
    bad = '\n'.join(lines).encode('utf-8')
    if not same_output(published, good, vline) or same_output(published, bad, vline):
        failures.append('negative control: the version-line comparison is not exact outside its line')

    print(json.dumps({'object': manifest['object'],
                      'interpreter': platform.python_version(),
                      'interpreter_flags': interpreter_flags(),
                      'replayed_stdout_sha256': digests,
                      'failures': failures,
                      'scientific_effect': 'NONE'}, sort_keys=True, indent=1))
    return 0 if not failures else 1


if __name__ == '__main__':
    sys.exit(main())
