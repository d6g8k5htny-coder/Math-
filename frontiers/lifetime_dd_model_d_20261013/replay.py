#!/usr/bin/env python3
"""Verify the stored records of lifetime note DD and replay its certificate (standard library only).

The packet stores, byte for byte:
  - public comment bodies of main#307 (the note, the controls comment, the claim, the summonses, the nonauthor
    verdicts, the author's read-complete note), under DD/;
  - the certificate pinned by the controls comment (the eleven Python/JSON files, the twelve node files and the
    recorded stdout of the controls, the mutants and the assembly), under certificate/.
SOURCES.json pins every stored file by byte count and SHA-256. This script performs five checks.

  1. The packet tree equals SOURCES.json's file list, with no symlinks, and every stored file has its pinned identity.
  2. Every certificate file named in the table of the stored controls comment (DD/AUTHOR_CONTROLS_COMMENT.md, 23 files)
     and in the table of the stored controls addendum (DD/AUTHOR_CONTROLS_ADDENDUM_C10.md, 3 files) has the byte count
     and SHA-256 the comment states (the comments pin the files at Math- commits; the packet holds the same bytes).
  3. Replays under the current interpreter's -O/-S flags, each with stdout byte-identical to the stored record and
     empty stderr: certificate/dd_controls.py (C1-C9), certificate/dd_mutants.py (nine mutants, each rejected),
     certificate/dd_gapcheck.py on the stored cells (control C10, the sliver-gap enclosure), and certificate/dd_exact.py
     on the stored cells and node files (the tiling checks, every cell remainder recomputed, 24 node values recomputed,
     D and the corollary). The assembly takes about 20 minutes.
  4. Negative controls, each in a temporary copy, must be rejected:
     - a one-byte change to the stored note (DD/PROOF.md) fails check 1;
     - one changed digit in one stored node value (certificate/nodes/nodes_3.json) makes dd_exact.py's stdout differ
       from the stored record (or fail);
     - dd_exact.py with one node file missing exits 1 ('incomplete node values').
  5. Each stored verdict, summons and author record names the byte counts and SHA-256 of the stored bodies it refers to
     (SOURCES.json, names_identities: the slice verdicts name the note they read, v1.0, and the controls comment; the
     readback names v1.0 and v1.1; the C10 read names v1.1, v1.2 and the controls addendum; the read-complete notes name
     the versions they cover).

Reproducibility only. The note and its reads carry the mathematics. Nothing here reads or grades a proof.

Usage: python3 -B -S frontiers/lifetime_dd_model_d_20261013/replay.py [--quick]   (exit 0 iff every check passes)
--quick skips the assembly replay and the node-mutation control (for local runs; the hosted workflow runs everything).
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
PROCESS_TIMEOUT_SECONDS = 3600


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


PINNING_COMMENTS = (('DD/AUTHOR_CONTROLS_COMMENT.md', 23, 'controls comment'), ('DD/AUTHOR_CONTROLS_ADDENDUM_C10.md', 3, 'controls addendum'))


def controls_table_failures(root):
    """the stored controls comment and addendum pin the certificate files: | `dd/<name>` | <bytes> | `<sha256>` |"""
    failures = []
    for rel, expected, label in PINNING_COMMENTS:
        body = (root / rel).read_text(encoding='utf-8')
        rows = re.findall(r'^\| `dd/([^`]+)` \| (\d+) \| `([0-9a-f]{64})` \|$', body, re.M)
        if len(rows) != expected:
            failures.append('%s: expected %d pinned files, found %d' % (label, expected, len(rows)))
        for name, nbytes, sha in rows:
            p = root / 'certificate' / name
            if not p.is_file():
                failures.append('pinned file missing: ' + name)
                continue
            if identity(p.read_bytes()) != (int(nbytes), sha):
                failures.append('pinned identity mismatch: ' + name)
    return failures


def named_identities_failures(root, manifest):
    """a stored record with names_identities = [paths] names the byte count and SHA-256 of each of those stored files
    (the verdicts name the note they read and the controls comment; the readback and the read-complete note name both
    versions of the note)."""
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


def run(script, *args, cwd=None):
    command = [sys.executable, *interpreter_flags(), str(script), *args]
    cwd = str(cwd or script.parent)
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


def replay_failures(root, manifest, quick):
    failures = []
    cert = root / 'certificate'
    nodes = [cert / 'nodes' / ('nodes_%d.json' % k) for k in range(12)]
    for rep in manifest['replays']:
        if quick and rep.get('long'):
            print(json.dumps(dict(replay=rep['name'], skipped='--quick')))
            continue
        script = cert / rep['script']
        args = [str(cert / a) if a.endswith('.json') else a for a in rep['args']]      # file arguments are packet paths; others (an nproc) pass through
        result = run(script, *args)
        report(rep['name'], result, 'exit 0, stdout equals ' + rep['stdout'])
        code, out, err = result
        if code != 0:
            failures.append('%s: exit %d' % (rep['name'], code))
        if out != (root / rep['stdout']).read_bytes():
            failures.append('%s: stdout differs from the stored record' % rep['name'])
        if err:
            failures.append('%s: stderr not empty' % rep['name'])
    return failures


def negative_failures(root, manifest, quick):
    failures = []
    # (a) a one-byte change to the stored note fails the tree check
    with tempfile.TemporaryDirectory() as tmp:
        copy = pathlib.Path(tmp) / 'packet'
        shutil.copytree(root, copy, ignore=shutil.ignore_patterns('__pycache__'))
        p = copy / 'DD' / 'PROOF.md'
        data = bytearray(p.read_bytes())
        data[len(data) // 2] ^= 0x01
        p.write_bytes(bytes(data))
        if not any(f.startswith('identity mismatch: DD/PROOF.md') for f in tree_failures(copy, manifest)):
            failures.append('negative control (a): the mutated note was not rejected')
        else:
            print(json.dumps(dict(negative='one-byte change to DD/PROOF.md', rejected=True)))
    # (c) a missing node file makes dd_exact.py exit 1
    cert = root / 'certificate'
    nodes = [str(cert / 'nodes' / ('nodes_%d.json' % k)) for k in range(11)]      # nodes_11 omitted
    code, out, err = run(cert / 'dd_exact.py', str(cert / 'cells_full.json'), *nodes, '--no-recheck', '--no-sample')
    report('dd_exact.py with nodes_11.json missing', (code, out, err), 'exit 1, AssertionError: incomplete node values')
    if code != 1 or b'incomplete node values' not in err:
        failures.append('negative control (c): a missing node file was not rejected as intended')
    if quick:
        print(json.dumps(dict(negative='one changed digit in nodes_3.json', skipped='--quick')))
        return failures
    # (b) one changed digit in one stored node value changes (or fails) the assembly
    with tempfile.TemporaryDirectory() as tmp:
        copy = pathlib.Path(tmp) / 'certificate'
        shutil.copytree(cert, copy, ignore=shutil.ignore_patterns('__pycache__'))
        p = copy / 'nodes' / 'nodes_3.json'
        d = json.loads(p.read_text(encoding='utf-8'))
        key = sorted(d, key=int)[7]
        lo = d[key][0][0]
        if lo == 'FAIL':
            raise AssertionError('stored node record is a failure')
        # lower the lower end by one percent of its magnitude plus 1e-6 (keeps lo <= hi; changes the assembled sum visibly)
        from decimal import Decimal, getcontext
        getcontext().prec = 40
        d[key][0][0] = str(Decimal(lo) - abs(Decimal(lo)) * Decimal('0.01') - Decimal('0.000001'))
        p.write_text(json.dumps(d), encoding='utf-8')
        nodes = [str(copy / 'nodes' / ('nodes_%d.json' % k)) for k in range(12)]
        code, out, err = run(copy / 'dd_exact.py', str(copy / 'cells_full.json'), *nodes, '--no-recheck', '--no-sample')
        report('dd_exact.py with one changed node digit (no recheck, no sample)', (code, out, err), 'stdout differs from the record or exit 1')
        # compare with the stored record's final lines (the record was produced with the recheck and the sample; strip the two C9 lines)
        stored = (root / 'certificate' / 'results' / 'assembly_stdout.txt').read_bytes()
        stored_tail = b'\n'.join(l for l in stored.split(b'\n') if not l.startswith(b'C9'))
        if code == 0 and out == stored_tail:
            failures.append('negative control (b): a changed node value was not detected')
        else:
            print(json.dumps(dict(negative='one changed digit in nodes_3.json', rejected=True)))
    return failures


def main(argv):
    quick = '--quick' in argv
    manifest = json.loads((HERE / 'SOURCES.json').read_text(encoding='utf-8'))
    failures = []
    failures += tree_failures(HERE, manifest)
    failures += controls_table_failures(HERE)
    failures += named_identities_failures(HERE, manifest)
    if not failures:
        failures += replay_failures(HERE, manifest, quick)
        failures += negative_failures(HERE, manifest, quick)
    for f in failures:
        print('FAIL ' + f)
    mode = ' '.join(interpreter_flags())
    if failures:
        print('Lifetime note DD incorporation replay (%s): %d failure(s)' % (mode, len(failures)))
        return 1
    n_replays = sum(1 for r in manifest['replays'] if not (quick and r.get('long')))
    print('Lifetime note DD incorporation replay (%s): %d stored records, %d certificate files, %d replays and %d negative controls PASS%s' % (
        mode, sum(1 for f in manifest['stored'] if f['path'].startswith('DD/')), sum(1 for f in manifest['stored'] if f['path'].startswith('certificate/')),
        n_replays, 2 if quick else 3, ' (--quick: the assembly replay and the node-mutation control were skipped)' if quick else ''))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
