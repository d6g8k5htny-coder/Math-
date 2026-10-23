#!/usr/bin/env python3
"""Verify the stored records of lifetime note C3-R (a rate after the l^{2/3} term) and replay its controls (standard library only).

The packet stores, byte for byte:
  - public comment bodies of main#307 (the task, the claim, the note in its versions, the controls comment, the summonses,
    the nonauthor verdicts, the author's records), under C3R/;
  - the control script and the mutant driver pinned by the controls comment, with their recorded stdout, under controls/.
SOURCES.json pins every stored file by byte count and SHA-256. This script performs five checks.

  1. The packet tree equals SOURCES.json's file list, with no symlinks, and every stored file has its pinned identity.
  2. Every file named in the table of the stored controls comment (C3R/AUTHOR_CONTROLS_COMMENT.md, 4 files) has the byte
     count and SHA-256 the comment states (the comment pins the files at a Math- commit; the packet holds the same bytes).
  3. Replays under the current interpreter's -O/-S flags, each with exit 0, stdout byte-identical to the stored record and
     empty stderr: c3r_exact.py (controls E1-E3) and c3r_mutants.py (four mutants, each rejected).
  4. Negative controls, each in a temporary copy, must be rejected:
     - a one-byte change to the stored note (C3R/PROOF.md) fails check 1;
     - c3r_exact.py with the stated delta(3) = 1/50 replaced by 1/49 exits nonzero.
  5. Each stored verdict, summons and author record listed with names_identities in SOURCES.json names the byte count and
     SHA-256 of each stored body it refers to.

Reproducibility only. The note and its reads carry the mathematics. Nothing here reads or grades a proof.

Usage: python3 -B -S frontiers/lifetime_c3r_rate_20261013/replay.py   (exit 0 iff every check passes; about ten seconds)
Optional QS_REPLAY_EVIDENCE_DIR (outside the checkout) retains raw child streams and process records.
"""
import hashlib
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
OWN = {'README.md', 'SOURCES.json', 'replay.py'}
PROCESS_TIMEOUT_SECONDS = 600
CONTROLS_COMMENT = 'C3R/AUTHOR_CONTROLS_COMMENT.md'
CONTROLS_ROWS = 4


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
    listed = {f['path']: (f['bytes'], f['sha256']) for f in manifest['stored']}
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


def stored_path(name):
    """the controls comment names files by their branch names; the packet keeps scripts in controls/ and outputs in controls/results/"""
    return ('controls/results/' + name) if name.endswith('.txt') else ('controls/' + name)


def controls_table_failures(root):
    """the stored controls comment pins the files: | `<name>` | <bytes, with thousands commas> | `<sha256>` | `<git blob>` |"""
    failures = []
    body = (root / CONTROLS_COMMENT).read_text(encoding='utf-8')
    rows = re.findall(r'^\| `([^`/]+)` \| ([\d,]+) \| `([0-9a-f]{64})` \| `[0-9a-f]{40}` \|$', body, re.M)
    if len(rows) != CONTROLS_ROWS:
        failures.append('controls comment: expected %d pinned files, found %d' % (CONTROLS_ROWS, len(rows)))
    for name, nbytes, sha in rows:
        p = root / stored_path(name)
        if not p.is_file():
            failures.append('pinned file missing: ' + name)
        elif identity(p.read_bytes()) != (int(nbytes.replace(',', '')), sha):
            failures.append('pinned identity mismatch: ' + name)
    return failures


def named_identities_failures(root, manifest):
    """a stored record with names_identities = [paths] names the byte count and SHA-256 of each of those stored files."""
    failures = []
    ids = {f['path']: (f['bytes'], f['sha256']) for f in manifest['stored']}
    for f in manifest['stored']:
        for path in f.get('names_identities') or []:
            if path not in ids:
                failures.append('%s: names_identities refers to an unstored path %s' % (f['path'], path))
                continue
            nbytes, sha = ids[path]
            text = (root / f['path']).read_text(encoding='utf-8')
            if sha not in text:
                failures.append('%s does not name the SHA-256 of %s' % (f['path'], path))
            if ('{:,}'.format(nbytes) not in text) and (str(nbytes) not in text):
                failures.append('%s does not name the byte count of %s' % (f['path'], path))
    return failures


def evidence_directory(script):
    raw = os.environ.get('QS_REPLAY_EVIDENCE_DIR')
    if raw is None:
        return None
    if not raw:
        raise ValueError('QS_REPLAY_EVIDENCE_DIR must not be empty')
    root = pathlib.Path(raw).expanduser().resolve()
    if root.is_relative_to(HERE.resolve().parents[1]) or root.is_relative_to(script.parent.resolve()):
        raise ValueError('QS replay evidence must be outside the checkout and child source directory')
    root.mkdir(parents=True, exist_ok=True)
    return pathlib.Path(tempfile.mkdtemp(prefix='invocation-', dir=root))


def run(script, *args):
    command = [sys.executable, *interpreter_flags(), str(script), *args]
    cwd = str(script.parent)
    folder = evidence_directory(script)
    record = dict(schema=1, command=command, cwd=cwd, timeout_seconds=PROCESS_TIMEOUT_SECONDS, scientific_effect='NONE')
    try:
        proc = subprocess.run(command, capture_output=True, timeout=PROCESS_TIMEOUT_SECONDS, cwd=cwd)
        out, err, code, status = proc.stdout, proc.stderr, proc.returncode, 'completed'
    except subprocess.TimeoutExpired as ex:
        out, err, code, status = ex.stdout or b'', ex.stderr or b'', None, 'timeout'
    record.update(status=status, returncode=code,
                  stdout=dict(bytes=len(out), sha256=hashlib.sha256(out).hexdigest()),
                  stderr=dict(bytes=len(err), sha256=hashlib.sha256(err).hexdigest()))
    if folder is not None:
        (folder / 'stdout.bin').write_bytes(out)
        (folder / 'stderr.bin').write_bytes(err)
        (folder / 'process.json').write_bytes((json.dumps(record, sort_keys=True, indent=2) + '\n').encode('utf-8'))
    if status == 'timeout':
        raise subprocess.TimeoutExpired(command, PROCESS_TIMEOUT_SECONDS, output=out, stderr=err)
    return code, out, err


def report(name, result, expected_reason):
    code, out, err = result
    print(json.dumps(dict(replay=name, returncode=code, stdout_sha256=hashlib.sha256(out).hexdigest(),
                          stderr_sha256=hashlib.sha256(err).hexdigest(), expected=expected_reason), sort_keys=True))


def replay_failures(root, manifest):
    failures = []
    for rep in manifest['replays']:
        result = run(root / rep['script'])
        report(rep['name'], result, 'exit 0, stdout equals ' + rep['stdout'])
        code, out, err = result
        if code != 0:
            failures.append('%s: exit %s' % (rep['name'], code))
        if out != (root / rep['stdout']).read_bytes():
            failures.append('%s: stdout differs from the stored record' % rep['name'])
        if err:
            failures.append('%s: stderr not empty' % rep['name'])
    return failures


def negative_failures(root, manifest):
    failures = []
    # (a) a one-byte change to the stored note fails the tree check
    with tempfile.TemporaryDirectory() as tmp:
        copy = pathlib.Path(tmp) / 'packet'
        shutil.copytree(root, copy, ignore=shutil.ignore_patterns('__pycache__'))
        p = copy / 'C3R' / 'PROOF.md'
        data = bytearray(p.read_bytes())
        data[len(data) // 2] ^= 0x01
        p.write_bytes(bytes(data))
        if not any(f.startswith('identity mismatch: C3R/PROOF.md') for f in tree_failures(copy, manifest)):
            failures.append('negative control (a): the mutated note was not rejected')
        else:
            print(json.dumps(dict(negative='one-byte change to C3R/PROOF.md', rejected=True)))
    # (b) the stated delta(3) = 1/50 replaced by 1/49 is rejected by the controls
    with tempfile.TemporaryDirectory() as tmp:
        script = pathlib.Path(tmp) / 'c3r_exact.py'
        src = (root / 'controls' / 'c3r_exact.py').read_text(encoding='utf-8')
        old = 'stated = {2: (Fr(1, 50), a_star'
        if src.count(old) != 1:
            raise AssertionError('negative control (b): the text to change occurs %d times' % src.count(old))
        script.write_text(src.replace(old, 'stated = {2: (Fr(1, 49), a_star'), encoding='utf-8')
        result = run(script)
        report('c3r_exact.py with delta(3) = 1/49', result, 'nonzero exit')
        if result[0] == 0:
            failures.append('negative control (b): delta(3) = 1/49 was not rejected')
        else:
            print(json.dumps(dict(negative='delta(3) = 1/49 in c3r_exact.py', rejected=True)))
    return failures


def main(argv):
    manifest = json.loads((HERE / 'SOURCES.json').read_text(encoding='utf-8'))
    failures = []
    failures += tree_failures(HERE, manifest)
    failures += controls_table_failures(HERE)
    failures += named_identities_failures(HERE, manifest)
    if not failures:
        failures += replay_failures(HERE, manifest)
        failures += negative_failures(HERE, manifest)
    for f in failures:
        print('FAIL ' + f)
    mode = ' '.join(interpreter_flags())
    if failures:
        print('Lifetime note C3-R incorporation replay (%s): %d failure(s)' % (mode, len(failures)))
        return 1
    print('Lifetime note C3-R incorporation replay (%s): %d stored records, %d control files, %d replays and 2 negative controls PASS' % (
        mode, sum(1 for f in manifest['stored'] if f['path'].startswith('C3R/')),
        sum(1 for f in manifest['stored'] if f['path'].startswith('controls/')), len(manifest['replays'])))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
