#!/usr/bin/env python3
"""Verify the stored records of lifetime note DD and replay its certificate (standard library only).

The packet stores, byte for byte:
  - public comment bodies of main#307 and Math-#448/#449 (the note in its versions, the controls comments, the claim, the
    summonses, the nonauthor verdicts, the author's records), under DD/;
  - certificate v1, pinned by the controls comment and read by the slice reads (the eleven Python/JSON files, control
    C10, the twelve node files and the recorded stdout of the controls, the mutants, C10 and the assembly), under
    certificate/; and certificate v2 (exact sliver geometry; two modules changed, the node files recomputed), pinned by
    the controls comment v2, under certificate_v2/.
SOURCES.json pins every stored file by byte count and SHA-256. This script performs five checks.

  1. The packet tree equals SOURCES.json's file list, with no symlinks, and every stored file has its pinned identity.
  2. Every certificate file named in the tables of the stored pinning comments (DD/AUTHOR_CONTROLS_COMMENT.md, 23 files
     and DD/AUTHOR_CONTROLS_ADDENDUM_C10.md, 3 files, both for certificate/; DD/AUTHOR_CONTROLS_COMMENT_V2.md, 32 files,
     for certificate_v2/) has the byte count and SHA-256 the comment states (the comments pin the files at Math-
     commits; the packet holds the same bytes).
  3. Replays under the current interpreter's -O/-S flags, each with stdout byte-identical to the stored record and
     empty stderr, for each certificate: dd_controls.py (C1-C9), dd_mutants.py (nine mutants, each rejected),
     dd_gapcheck.py on the stored cells (control C10, the sliver-gap enclosure), and dd_exact.py on the stored cells and
     node files (the tiling checks, every cell remainder recomputed, 24 node values recomputed, D and the corollary).
     Each assembly takes about 20 minutes.
  4. Negative controls and a separate output-sensitivity control:
     - a one-byte change to the stored note (DD/PROOF.md) fails check 1;
     - the fixed perturbation of certificate_v2/nodes/nodes_3.json matches the complete successful
       CHANGED_NODE_STDOUT transcript and empty stderr (output sensitivity, not mathematical rejection);
     - missing nodes_11.json matches exit 1, empty stdout and the exact supported-runtime traceback
       (input-completeness rejection, not mathematical certification).
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


# Independently observed CPython 3.11.16 process contracts, both modes.
# Changed-node is output sensitivity, not rejection or a certified new bound.
CHANGED_NODE_STDOUT = b"""Gauss region: sum [0.0764960693454651862061373880206, 0.0771096748441041862088778512743] (node-width 0.0006136054986390000027404632537), remainder 0.000699415225762334605564277483154
region S: [-0.0000204104527369070204567316057495, -0.0000200429419006537600186550090259]; omega tails 0.0000138351995650080053539807820619; tau tail 0.0000572129033171405130248937123594
D in [0.0757051955640837960617375044371, 0.0778600952308480155728023482430]  width 0.0021548996667642195110648438059
q = J/30 - I~_quad - D in [0.672471569882485317760530985090, 0.674626571425916203938262495564]
(c3 - R_{2/3})(L), d=2, L>=10: [0.0614650917123430310676033072575, 0.0616634937440884512761309021742]
(c3 - R_{2/3})(L), d=2, L>=24: [0.0614658061059116856127442435421, 0.0616627793505197967309899658896]
(c3 - R_{2/3})(L), d=3, L>=10: [0.0772809592715861738273260172417, 0.0776431580674687676951576755071]
(c3 - R_{2/3})(L), d=3, L>=24: [0.0773381398169425878649879319988, 0.0775859775221123536574957607500]
"""

# Only the known certificate path is substituted in this expected template.
# No normalization of actual streams: runtime/source drift fails closed.
MISSING_NODE_STDERR_TEMPLATE = b"""Traceback (most recent call last):
  File "<CERTIFICATE_V2>/dd_exact.py", line 95, in <module>
    main(args[0], *args[1:], recheck='--no-recheck' not in sys.argv, sample=0 if '--no-sample' in sys.argv else 24)
  File "<CERTIFICATE_V2>/dd_exact.py", line 37, in main
    require(len(done) == len(cells), 'incomplete node values: %d of %d cells' % (len(done), len(cells)))
  File "<CERTIFICATE_V2>/ddcore.py", line 23, in require
    if not cond: raise AssertionError(msg)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: incomplete node values: 2194 of 2393 cells
"""


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


# (stored comment, expected rows, label, the table's path prefix in the comment, the packet directory it pins)
PINNING_COMMENTS = (('DD/AUTHOR_CONTROLS_COMMENT.md', 23, 'controls comment', 'dd', 'certificate'),
                    ('DD/AUTHOR_CONTROLS_ADDENDUM_C10.md', 3, 'controls addendum', 'dd', 'certificate'),
                    ('DD/AUTHOR_CONTROLS_COMMENT_V2.md', 32, 'controls comment v2', 'dd_v2', 'certificate_v2'))


def controls_table_failures(root):
    """the stored pinning comments pin the certificate files: | `<prefix>/<name>` | <bytes> | `<sha256>` |"""
    failures = []
    for rel, expected, label, prefix, cert_dir in PINNING_COMMENTS:
        body = (root / rel).read_text(encoding='utf-8')
        rows = re.findall(r'^\| `' + re.escape(prefix) + r'/([^`]+)` \| (\d+) \| `([0-9a-f]{64})` \|$', body, re.M)
        if len(rows) != expected:
            failures.append('%s: expected %d pinned files, found %d' % (label, expected, len(rows)))
        for name, nbytes, sha in rows:
            p = root / cert_dir / name
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
    for rep in manifest['replays']:
        cert = root / rep.get('certificate', 'certificate')
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
    # (c) a missing node file makes dd_exact.py exit 1 (certificate v2, the certificate of record)
    cert = root / 'certificate_v2'
    nodes = [str(cert / 'nodes' / ('nodes_%d.json' % k)) for k in range(11)]      # nodes_11 omitted
    code, out, err = run(cert / 'dd_exact.py', str(cert / 'cells_full.json'), *nodes, '--no-recheck', '--no-sample')
    report('dd_exact.py with nodes_11.json missing', (code, out, err), 'exit 1, empty stdout, exact input-completeness traceback')
    expected_missing = MISSING_NODE_STDERR_TEMPLATE.replace(b'<CERTIFICATE_V2>', os.fsencode(cert))
    if (code, out, err) != (1, b'', expected_missing):
        failures.append('negative control (c): missing-node result does not match the exact input-completeness rejection')
    else:
        print(json.dumps(dict(control='nodes_11.json missing', input_completeness_rejection_verified=True)))
    if quick:
        print(json.dumps(dict(negative='one changed digit in nodes_3.json', skipped='--quick')))
        return failures
    # (b) exact successful output sensitivity with recomputation disabled.
    with tempfile.TemporaryDirectory() as tmp:
        copy = pathlib.Path(tmp) / 'certificate_v2'
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
        report('dd_exact.py with one changed node digit (no recheck, no sample)', (code, out, err),
               'exit 0, exact changed-node stdout, empty stderr (output sensitivity only)')
        if (code, out, err) != (0, CHANGED_NODE_STDOUT, b''):
            failures.append('negative control (b): node-coupling result does not match the exact successful transcript')
        else:
            print(json.dumps(dict(control='one changed digit in nodes_3.json', output_sensitivity_verified=True)))
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
    print('Lifetime note DD incorporation replay (%s): %d stored records, %d certificate files (v1 %d, v2 %d), %d replays, 2 negative controls and %d output-sensitivity controls PASS%s' % (
        mode, sum(1 for f in manifest['stored'] if f['path'].startswith('DD/')), sum(1 for f in manifest['stored'] if f['path'].startswith('certificate')),
        sum(1 for f in manifest['stored'] if f['path'].startswith('certificate/')), sum(1 for f in manifest['stored'] if f['path'].startswith('certificate_v2/')),
        n_replays, 0 if quick else 1, ' (--quick: the assembly replays and the node-mutation control were skipped)' if quick else ''))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
