#!/usr/bin/env python3
"""Verify the stored A4 records and replay A4's published author controls (standard library only).

Every file in this packet except replay.py, README.md and SOURCES.json is one of two things:
  - an exact copy of a public comment body on main#229;
  - a payload extracted verbatim from such a comment.
SOURCES.json pins each file by byte count and SHA256. This script performs four checks.

  1. The packet tree equals SOURCES.json's file list, with no symlinks, and every stored file has its pinned
     identity.
  2. The extracted checker and stdout equal the fenced payloads inside the stored controls comment, under
     the extraction rule that comment states.
  3. The checker runs under the current interpreter's -O/-S flags and reproduces the published stdout
     byte for byte (it prints no interpreter version). Each of its six mutant labels exits 1, and the
     invalid label exits 2.
  4. Negative controls must be rejected:
     - a one-byte change to a stored proof;
     - a checker with one changed constant (the margin's 72 replaced by 36).

Reproducibility only. The analytic proof and its review carry the mathematics. These finite checks
support algebra, as the review says. Nothing here reads or grades a proof.

Usage: python3 -B -S frontiers/planar_rejected_endpoint_margin_20261003/replay.py   (exit 0 iff every check passes)
"""
import hashlib
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
OWN = {'README.md', 'SOURCES.json', 'replay.py'}


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
    listed = {}
    for obj in manifest['objects']:
        for f in obj['stored']:
            listed[f['path']] = (f['bytes'], f['sha256'])
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


def extraction_failures(root):
    body = (root / 'A4' / 'AUTHOR_CONTROLS_COMMENT.md').read_text(encoding='utf-8')
    section = body[body.index('### a4_exact.py'):]
    code = re.search(r'```python\n(.*?)\n```\n', section, re.S).group(1) + '\n'
    out = re.search(r'```text\n(.*?)\n```\n', section, re.S).group(1) + '\n'
    failures = []
    if code.encode('utf-8') != (root / 'A4' / 'author_controls.py').read_bytes():
        failures.append('A4/author_controls.py differs from the payload in the controls comment')
    if out.encode('utf-8') != (root / 'A4' / 'author_controls_stdout.txt').read_bytes():
        failures.append('A4/author_controls_stdout.txt differs from the payload in the controls comment')
    return failures


def run(script, *args):
    proc = subprocess.run([sys.executable, *interpreter_flags(), str(script), *args], capture_output=True,
                          timeout=900, cwd=str(script.parent))
    return proc.returncode, proc.stdout


def replay_failures(root, manifest):
    failures = []
    for obj in manifest['objects']:
        for replay in obj.get('replays', []):
            label = '%s %s' % (obj['tag'], replay['name'])
            script = root / replay['script']
            code, out = run(script)
            if code != 0:
                failures.append('%s: exit code %s' % (label, code))
            if out != (root / replay['stdout']).read_bytes():
                failures.append('%s: stdout differs from the published bytes' % label)
            for mutant in replay['mutants']:
                code, _ = run(script, mutant)
                if code != 1:
                    failures.append('%s: mutant %s exited %s, expected 1' % (label, mutant, code))
            code, _ = run(script, replay['invalid_label'])
            if code != 2:
                failures.append('%s: invalid label exited %s, expected 2' % (label, code))
    return failures


def main():
    manifest = json.loads((HERE / 'SOURCES.json').read_text(encoding='utf-8'))
    failures = tree_failures(HERE, manifest) + extraction_failures(HERE) + replay_failures(HERE, manifest)

    with tempfile.TemporaryDirectory() as tmp:
        copy = pathlib.Path(tmp) / 'packet'
        shutil.copytree(HERE, copy, symlinks=True)
        target = copy / 'A4' / 'PROOF.md'
        data = bytearray(target.read_bytes())
        data[100] ^= 0x01
        target.write_bytes(bytes(data))
        if 'identity mismatch: A4/PROOF.md' not in tree_failures(copy, manifest):
            failures.append('negative control: a one-byte change to A4/PROOF.md was not detected')
        script = copy / 'A4' / 'author_controls.py'
        text = script.read_text(encoding='utf-8')
        old = 'cst = F(36) if MUT == "LOCAL_36" else F(72)'
        if text.count(old) != 1:
            failures.append('negative control: the margin constant line was not found exactly once')
        else:
            script.write_text(text.replace(old, 'cst = F(36) if MUT == "LOCAL_36" else F(36)'), encoding='utf-8')
            code, out = run(script)
            if code == 0 or out == (HERE / 'A4' / 'author_controls_stdout.txt').read_bytes():
                failures.append('negative control: a checker with 72 replaced by 36 was not rejected')

    mode = ' '.join(interpreter_flags())
    if failures:
        for f in failures:
            print('FAIL ' + f)
        print('A4 incorporation replay (%s): %d failure(s)' % (mode, len(failures)))
        return 1
    print('A4 incorporation replay (%s): identities, extraction, checker stdout, 6 mutants, invalid label and 2 negative controls PASS' % mode)
    return 0


if __name__ == '__main__':
    sys.exit(main())
