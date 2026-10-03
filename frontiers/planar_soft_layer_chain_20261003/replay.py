#!/usr/bin/env python3
"""Verify the stored C91–C98 records and replay their published checkers (standard library only).

Every file in this packet is an exact copy of a public comment body on main#229, or a code/output fence
extracted verbatim from one, except this script, README.md and SOURCES.json. SOURCES.json pins each copy by
byte count and SHA256. This script:

  1. checks that the packet tree equals SOURCES.json's file list, with no symlinks, and that every stored
     file has its pinned identity;
  2. checks C96's frozen-proof suffix identity (7657 bytes, SHA256 7198ff63...) inside the native comment;
  3. runs each of the seven published independent checkers (C91, C92, C93, C94, C95 helper, C97, C98) under
     the current interpreter's -O/-S flags and requires its stdout to equal the published bytes;
  4. negative controls: a one-byte change to a stored body must fail step 1, and a checker with one changed
     constant must not reproduce its published stdout.

Reproducibility only. The analytic proofs and their reviews carry the mathematics; these finite checkers
support algebra, as each review says. Nothing here reads or grades a proof.

Usage: python3 -B -S frontiers/planar_soft_layer_chain_20261003/replay.py   (exit 0 iff every check passes)
"""
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
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
    expected = set(listed) | OWN
    for rel in sorted(present ^ expected):
        failures.append(('unlisted file: ' if rel in present else 'missing file: ') + rel)
    for rel, ident in sorted(listed.items()):
        if rel in present and identity((root / rel).read_bytes()) != ident:
            failures.append('identity mismatch: ' + rel)
    return failures


def run_checker(script):
    run = subprocess.run([sys.executable, *interpreter_flags(), str(script)], capture_output=True,
                         timeout=600, cwd=str(script.parent))
    return run.returncode, run.stdout


def main():
    manifest = json.loads((HERE / 'SOURCES.json').read_text(encoding='utf-8'))
    failures = tree_failures(HERE, manifest)

    native = (HERE / 'C96' / 'PROOF.md').read_bytes()
    if identity(native[-C96_SUFFIX[0]:]) != C96_SUFFIX:
        failures.append('C96 frozen-proof suffix identity mismatch')

    replays = {}
    for obj in manifest['objects']:
        checker = obj.get('checker')
        if not checker:
            continue
        code, out = run_checker(HERE / checker['path'])
        published = (HERE / checker['stdout_path']).read_bytes()
        replays[obj['tag']] = identity(out)[1]
        if code != 0:
            failures.append('%s checker exit code %d' % (obj['tag'], code))
        if out != published:
            failures.append('%s checker stdout differs from the published bytes' % obj['tag'])

    with tempfile.TemporaryDirectory() as tmp:
        copy = pathlib.Path(tmp) / 'packet'
        shutil.copytree(HERE, copy, symlinks=True)
        target = copy / 'C91' / 'PROOF.md'
        data = bytearray(target.read_bytes())
        data[100] ^= 0x01
        target.write_bytes(bytes(data))
        if not [f for f in tree_failures(copy, manifest) if f == 'identity mismatch: C91/PROOF.md']:
            failures.append('negative control: a one-byte change to C91/PROOF.md was not detected')
        script = copy / 'C93' / 'checker.py'
        source = script.read_text(encoding='utf-8')
        mutated = source.replace('24 * lam - gamma ** 2 + 12 * b', '24 * lam - gamma ** 2 + 13 * b', 1)
        if mutated == source:
            failures.append('negative control could not mutate the C93 checker')
        else:
            script.write_text(mutated, encoding='utf-8')
            code, out = run_checker(script)
            if code == 0 and out == (copy / 'C93' / 'checker_stdout.txt').read_bytes():
                failures.append('negative control: a mutated C93 checker reproduced its published stdout')

    print(json.dumps({'object': manifest['object'],
                      'interpreter_flags': interpreter_flags(),
                      'replayed_stdout_sha256': replays,
                      'failures': failures,
                      'scientific_effect': 'NONE'}, sort_keys=True, indent=1))
    return 0 if not failures else 1


if __name__ == '__main__':
    sys.exit(main())
