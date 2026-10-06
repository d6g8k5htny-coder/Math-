#!/usr/bin/env python3
"""Verify the stored records of lifetime note TS and replay its published author controls (standard library only).

Every file in this packet except replay.py, README.md and SOURCES.json is one of two things:
  - an exact copy of a public comment body on main#229 or main#259 (a note, claim, pickup, controls comment, read
    request, review, release or author response);
  - the control script or its stdout, extracted verbatim from the stored controls comment by the extraction rule that
    comment states (the rule of main#229 comment 5971055189). The stdout is a ```json fence.
SOURCES.json pins each file by byte count and SHA-256 and lists each replay. This script performs four checks.

  1. The packet tree equals SOURCES.json's file list, with no symlinks, and every stored file has its pinned
     identity.
  2. Every extracted script and stdout equals the fenced payload inside its stored source comment, under the
     extraction rule (the stdout fence language follows the stored stdout's suffix: .json for ```json, .txt for ```text).
  3. Every control script runs under the current interpreter's -O/-S flags and reproduces its published stdout byte
     for byte (none prints an interpreter version), with empty stderr. Every listed mutant or invalid invocation
     must reproduce its exact source-bound rejection on BOTH captured streams, not merely exit 1 or 2.
  4. Negative controls must be rejected:
     - a one-byte change to a stored note (TS/PROOF.md);
     - a control script with one changed constant (S3's constant C4 = 131 replaced by 130).

Reproducibility only. The analytic notes and their reads carry the mathematics. These finite checks support
algebra, as the reads say. Nothing here reads or grades a proof.

Usage: python3 -B -S frontiers/ts_small_kappa_20261006/replay.py   (exit 0 iff every check passes)
Optional QS_REPLAY_EVIDENCE_DIR (outside the checkout) retains raw child streams and process records.
Each invocation gets a new directory; records describe execution, never mathematical acceptance.
Required evidence I/O fails the run; a timeout/spawn error remains the primary exception.
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

# Exact rejection fingerprints of the extracted author controls (ts_exact.py from 6020799284), computed under both
# interpreter modes at incorporation and found identical.
# Each key is (script path, complete argv tail); each value is (exit, stdout SHA256,
# stderr SHA256, readable reason). References are frozen independently of this run.
# All 10 mutants and 3 invalid invocations were executed and their named reasons
# checked against their source. Exact fingerprints enforce the full contracts,
# including the empty stdout, the FAILED or usage line and its group name.
# No current failing output, generic exit code or broad regex creates a reference.
# Any source/runtime output drift fails closed and requires a reviewed amendment.
REJECTION_CONTRACTS = {
    ('TS/author_controls.py', ('--mutant', 'M1')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '411e1ec4cdc647244fdb31ce5d96305ae154cfae97ff736762e3cd48fea0fded', 'FAILED: S1_pins'),
    ('TS/author_controls.py', ('--mutant', 'M2')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'd002479358decef62e3b2b07b742be78028c9fe95c928a0b48645a28cbe1aed8', 'FAILED: S2_barrier'),
    ('TS/author_controls.py', ('--mutant', 'M3')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'd002479358decef62e3b2b07b742be78028c9fe95c928a0b48645a28cbe1aed8', 'FAILED: S2_barrier'),
    ('TS/author_controls.py', ('--mutant', 'M4')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '0579129f9a73f09e7e61e58ee1a98f1d1b25fcd320ff0bc5cffd55d4617b0514', 'FAILED: S3_constants'),
    ('TS/author_controls.py', ('--mutant', 'M5')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '85159f6de6b828949c1de1dfd89acd96d24e9f9337e9a6aafefa19dc230a6a0d', 'FAILED: S5_ledger'),
    ('TS/author_controls.py', ('--mutant', 'M6')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '85159f6de6b828949c1de1dfd89acd96d24e9f9337e9a6aafefa19dc230a6a0d', 'FAILED: S5_ledger'),
    ('TS/author_controls.py', ('--mutant', 'M7')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '85159f6de6b828949c1de1dfd89acd96d24e9f9337e9a6aafefa19dc230a6a0d', 'FAILED: S5_ledger'),
    ('TS/author_controls.py', ('--mutant', 'M8')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '4f9648bdf8eaf78a329bb589a5bebab143cfaf55784076a3e412acf6ddff29f0', 'FAILED: S6_monomials'),
    ('TS/author_controls.py', ('--mutant', 'M9')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'ab341f1dc8ad3336cede12eb515613d487604d5811997620737afc4595135a61', 'FAILED: S4_edge_model'),
    ('TS/author_controls.py', ('--mutant', 'M10')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'd002479358decef62e3b2b07b742be78028c9fe95c928a0b48645a28cbe1aed8', 'FAILED: S2_barrier'),
    ('TS/author_controls.py', ('--bogus',)):
        (2, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '220f99affcd6e96b091c4c09a1fbbc87dbf47910680b7db2a28de7672269b27c', 'usage: ts_exact.py [--mutant M1..M10]'),
    ('TS/author_controls.py', ('--mutant', 'M11')):
        (2, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '220f99affcd6e96b091c4c09a1fbbc87dbf47910680b7db2a28de7672269b27c', 'usage: ts_exact.py [--mutant M1..M10]'),
    ('TS/author_controls.py', ('--mutant',)):
        (2, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '220f99affcd6e96b091c4c09a1fbbc87dbf47910680b7db2a28de7672269b27c', 'usage: ts_exact.py [--mutant M1..M10]'),
}

# Replacing S3's constant C4 = 131 by 130 with MUT=None must fail specifically at S3, on stderr alone.
NEGATIVE_CONSTANT = (1, hashlib.sha256(b'').hexdigest(),
                     hashlib.sha256(b'FAILED: S3_constants\n').hexdigest(), 'S3_constants')


def check_rejection(result, expected):
    """Compare both full captured streams, not a permissive failure-message pattern."""
    code, out, err = result
    failures = []
    if type(code) is not int or code != expected[0]:
        failures.append('wrong exit code')
    if type(out) is not bytes or hashlib.sha256(out).hexdigest() != expected[1]:
        failures.append('stdout differs from intended diagnostic')
    if type(err) is not bytes or hashlib.sha256(err).hexdigest() != expected[2]:
        failures.append('stderr differs from intended diagnostic')
    return failures


def rejection_inventory_failures(manifest):
    listed = {}
    for obj in manifest['objects']:
        for replay in obj['replays']:
            for kind, code in (('mutants', 1), ('invalid', 2)):
                for args in replay[kind]:
                    key = replay['script'], tuple(args)
                    if key in listed:
                        return ['duplicate rejection invocation: ' + repr(key)]
                    listed[key] = code
    if set(listed) != set(REJECTION_CONTRACTS):
        return ['rejection invocation inventory differs from frozen contracts']
    if any(REJECTION_CONTRACTS[key][0] != code for key, code in listed.items()):
        return ['rejection invocation category differs from frozen contracts']
    return []


def report_control(script, args, result, reason):
    code, out, err = result
    print(json.dumps(dict(script=script, args=list(args), returncode=code,
                          stdout_sha256=hashlib.sha256(out).hexdigest(),
                          stderr_sha256=hashlib.sha256(err).hexdigest(),
                          expected_reason=reason), sort_keys=True))


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


def extraction_failures(root, manifest):
    """Re-extract every script and stdout from its stored source comment and compare with the stored payloads."""
    failures = []
    for obj in manifest['objects']:
        extracted = [f for f in obj['stored'] if 'extracted_from' in f]
        for script in [f for f in extracted if f['path'].endswith('.py')]:
            stdout = [f for f in extracted if f['extracted_from'] == script['extracted_from']
                      and f['heading'] == script['heading'] and not f['path'].endswith('.py')]
            if len(stdout) != 1:
                failures.append('%s: no single stdout record for %s' % (obj['tag'], script['path']))
                continue
            stdout = stdout[0]
            fence = {'json': 'json', 'txt': 'text'}.get(stdout['path'].rsplit('.', 1)[-1])
            if fence is None:
                failures.append('%s: unsupported stdout suffix for %s' % (obj['tag'], stdout['path']))
                continue
            body = (root / script['extracted_from']).read_text(encoding='utf-8')
            if body.count(script['heading']) < 1:
                failures.append('%s: heading %r not found in %s' % (obj['tag'], script['heading'], script['extracted_from']))
                continue
            section = body[body.index(script['heading']):]
            m1 = re.search(r'```python\n(.*?)\n```\n', section, re.S)
            m2 = re.search(r'```%s\n(.*?)\n```\n' % fence, section[m1.end():], re.S) if m1 else None
            if not (m1 and m2):
                failures.append('%s: fences not found after %r' % (obj['tag'], script['heading']))
                continue
            if (m1.group(1) + '\n').encode('utf-8') != (root / script['path']).read_bytes():
                failures.append('%s: %s differs from the payload in %s' % (obj['tag'], script['path'], script['extracted_from']))
            if (m2.group(1) + '\n').encode('utf-8') != (root / stdout['path']).read_bytes():
                failures.append('%s: %s differs from the payload in %s' % (obj['tag'], stdout['path'], stdout['extracted_from']))
    return failures


PROCESS_TIMEOUT_SECONDS = 1800  # Unchanged production budget; tests shorten it for real timeout children.


def evidence_directory(script):
    """An explicit destination opts in; never put generated evidence in source directories."""
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


def save_process_evidence(folder, record, out, err):
    """Attempt every write independently. None is unavailable, not an observed empty stream."""
    record['streams'] = {}
    record['evidence_errors'] = []
    for name, data in (('stdout', out), ('stderr', err)):
        entry = dict(available=data is not None, bytes=len(data) if data is not None else None,
                     sha256=hashlib.sha256(data).hexdigest() if data is not None else None, saved=False)
        record['streams'][name] = entry
        try:
            (folder / (name + '.bin')).write_bytes(data if data is not None else b'')
            entry['saved'] = True
        except Exception as exc:
            record['evidence_errors'].append('%s.bin: %s: %s' % (name, type(exc).__name__, exc))
    try:
        data = (json.dumps(record, sort_keys=True, indent=2, allow_nan=False) + '\n').encode('utf-8')
        (folder / 'process.json').write_bytes(data)
    except Exception as exc:
        record['evidence_errors'].append('process.json: %s: %s' % (type(exc).__name__, exc))


def run(script, *args):
    command = [sys.executable, *interpreter_flags(), str(script), *args]
    folder = evidence_directory(script)  # Invalid/unwritable setup stops before starting a child.
    record = dict(schema=1, command=command, cwd=str(script.parent),
                  timeout_seconds=PROCESS_TIMEOUT_SECONDS, scientific_effect='NONE')
    try:
        proc = subprocess.run(command, capture_output=True, timeout=PROCESS_TIMEOUT_SECONDS,
                              cwd=str(script.parent))
    except (subprocess.TimeoutExpired, OSError) as exc:
        if folder is not None:
            record.update(status='timeout' if isinstance(exc, subprocess.TimeoutExpired) else 'spawn_error',
                          returncode=None, exception=dict(type=type(exc).__name__, message=str(exc)))
            exc.evidence_record = record
            try:
                save_process_evidence(folder, record, getattr(exc, 'stdout', None), getattr(exc, 'stderr', None))
                if record['evidence_errors']:
                    exc.add_note('QS replay evidence errors: ' + '; '.join(record['evidence_errors']))
            except Exception as secondary:
                exc.add_note('QS replay evidence recording failed: %s: %s' % (type(secondary).__name__, secondary))
        raise  # Never replace the primary timeout or launch error with a recording error.
    if folder is not None:
        record.update(status='completed', returncode=proc.returncode, exception=None)
        save_process_evidence(folder, record, proc.stdout, proc.stderr)
        if record['evidence_errors']:
            exc = RuntimeError('QS replay evidence errors: ' + '; '.join(record['evidence_errors']))
            exc.evidence_record = record
            raise exc  # Even exit 0 is not success when explicitly required evidence is missing.
    return proc.returncode, proc.stdout, proc.stderr


def replay_failures(root, manifest):
    failures = rejection_inventory_failures(manifest)
    if failures:
        return failures  # Do not execute an incomplete/changed control inventory.
    for obj in manifest['objects']:
        for replay in obj['replays']:
            label = '%s %s' % (obj['tag'], replay['name'])
            script = root / replay['script']
            code, out, err = run(script, *replay['args'])
            baseline_failures = []
            if code != 0:
                baseline_failures.append('%s: exit code %s' % (label, code))
            if out != (root / replay['stdout']).read_bytes():
                baseline_failures.append('%s: stdout differs from the published bytes' % label)
            if err:
                baseline_failures.append('%s: unexpected baseline stderr' % label)
            if baseline_failures:
                failures.extend(baseline_failures)
                continue
            report_control(replay['script'], replay['args'], (code, out, err), 'exact published baseline')
            for kind in ('mutants', 'invalid'):
                for args in replay[kind]:
                    expected = REJECTION_CONTRACTS[replay['script'], tuple(args)]
                    result = run(script, *args)
                    mismatches = check_rejection(result, expected)
                    failures.extend('%s %r: %s' % (label, args, why) for why in mismatches)
                    if not mismatches:
                        report_control(replay['script'], args, result, expected[3])
    return failures


def negative_control_failures(root, manifest):
    failures = []
    with tempfile.TemporaryDirectory() as tmp:
        copy = pathlib.Path(tmp) / 'packet'
        shutil.copytree(root, copy, symlinks=True)
        target = copy / 'TS' / 'PROOF.md'
        data = bytearray(target.read_bytes())
        data[100] ^= 0x01
        target.write_bytes(bytes(data))
        if 'identity mismatch: TS/PROOF.md' not in tree_failures(copy, manifest):
            failures.append('negative control: a one-byte change to TS/PROOF.md was not detected')
        script = copy / 'TS' / 'author_controls.py'
        text = script.read_text(encoding='utf-8')
        old = 'c4 = F(130) if MUT == "M4" else F(131)'
        if text.count(old) != 1:
            failures.append('negative control: the C4 constant line was not found exactly once')
        else:
            script.write_text(text.replace(old, 'c4 = F(130) if MUT == "M4" else F(130)'), encoding='utf-8')
            result = run(script)
            mismatches = check_rejection(result, NEGATIVE_CONSTANT)
            failures.extend('negative control: changed C4 constant: ' + why for why in mismatches)
            if not mismatches:
                report_control('TS/author_controls.py', [], result, 'changed 131 to 130: S3_constants')
    return failures


def main():
    manifest = json.loads((HERE / 'SOURCES.json').read_text(encoding='utf-8'))
    failures = tree_failures(HERE, manifest)
    if not failures:
        failures = extraction_failures(HERE, manifest)
    if not failures:
        failures = replay_failures(HERE, manifest)
    if not failures:
        failures = negative_control_failures(HERE, manifest)
    n_scripts = sum(len(o['replays']) for o in manifest['objects'])
    n_mut = sum(len(r['mutants']) for o in manifest['objects'] for r in o['replays'])
    n_inv = sum(len(r['invalid']) for o in manifest['objects'] for r in o['replays'])
    n_files = sum(len(o['stored']) for o in manifest['objects'])
    mode = ' '.join(interpreter_flags())
    if failures:
        for f in failures:
            print('FAIL ' + f)
        print('Lifetime note TS incorporation replay (%s): %d failure(s)' % (mode, len(failures)))
        return 1
    print('Lifetime note TS incorporation replay (%s): %d stored identities, %d extractions, %d checker stdouts, '
          '%d mutants, %d invalid invocations and 2 negative controls PASS' % (mode, n_files, 2 * n_scripts, n_scripts, n_mut, n_inv))
    return 0


if __name__ == '__main__':
    sys.exit(main())
