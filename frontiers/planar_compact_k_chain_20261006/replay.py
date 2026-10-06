#!/usr/bin/env python3
"""Verify the stored planar compact-K chain records (Corollary PD, QS addenda A4.1-A4.3) and replay their published author
controls (standard library only).

Every file in this packet except replay.py, README.md and SOURCES.json is one of two things:
  - an exact copy of a public comment body on main#229 (a note, claim, controls comment, review, pickup, release,
    erratum, support note or author response);
  - a control script or its stdout, extracted verbatim from a stored controls comment by the extraction rule that
    comment states (the rule of main#229 comment 5971055189); Corollary PD's ledger script and its stdout are extracted
    the same way from the stored note itself (its section 4). The stdouts of PD, A4.1 and A4.2 are ```text fences.
SOURCES.json pins each file by byte count and SHA-256 and lists each replay. This script performs four checks.

  1. The packet tree equals SOURCES.json's file list, with no symlinks, and every stored file has its pinned
     identity.
  2. Every extracted script and stdout equals the fenced payload inside its stored source comment, under the
     extraction rule (the stdout fence language follows the stored stdout's suffix: .json for ```json, .txt for ```text).
  3. Every control script runs under the current interpreter's -O/-S flags and reproduces its published stdout byte
     for byte (none prints an interpreter version), with empty stderr. Every listed mutant or invalid invocation
     must reproduce its exact source-bound rejection on BOTH captured streams, not merely exit 1 or 2.
  4. Negative controls must be rejected:
     - a one-byte change to a stored note (A4_3/PROOF.md);
     - a control script with one changed constant (A4.3's Lemma 1.1 constant 192 replaced by 96).

Reproducibility only. The analytic notes and their reads carry the mathematics. These finite checks support
algebra, as the reads say. Nothing here reads or grades a proof.

Usage: python3 -B -S frontiers/planar_compact_k_chain_20261006/replay.py   (exit 0 iff every check passes)
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

# Exact rejection fingerprints of the four extracted author controls (pd_ledger.py inside Corollary PD 5973476391,
# a41_exact.py from 5973265245, a42_exact.py from 5974567585, a43_exact.py from 6010511425), computed under both
# interpreter modes at incorporation and found identical.
# Each key is (script path, complete argv tail); each value is (exit, stdout SHA256,
# stderr SHA256, readable reason). References are frozen independently of this run.
# All 25 mutants and 9 invalid invocations were executed and their named reasons
# checked against their source. Different checkers intentionally use different
# streams/formats. Exact fingerprints enforce those full contracts, including
# JSON structure/types, labels, counts, usage text, and empty/nonempty streams.
# No current failing output, generic exit code or broad regex creates a reference.
# Any source/runtime output drift fails closed and requires a reviewed amendment.
REJECTION_CONTRACTS = {
    ('PD/ledger_control.py', ('RATE_THIRD',)):
        (1, 'b3625549e52f73ac357226dd30ab8dc82876e8711b031ce72a1c07fc9d5e24a9', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'FAIL C103 beta=1/4: relative error l^(beta/3)'),
    ('PD/ledger_control.py', ('CUM_HALF',)):
        (1, 'e04f7e4ce72ed23280afa97d59e193fd301dba43cb150d0ab12f376dd5d10c41', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'FAIL cumulative constant 1/(5/3) = 3/5'),
    ('PD/ledger_control.py', ('FRAC_ONE',)):
        (1, '4448e3ded55650616270258dbba6080acfbd7beadbd1c738063930702fcafa2a', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'FAIL C103 beta=1/4: fraction error l^(1+beta/3)'),
    ('PD/ledger_control.py', ('BOGUS',)):
        (2, 'a0758636c5e479dfd217fb60eadb689f69c39901577d819a78384952bb8a1762', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'unknown mutant label: BOGUS'),
    ('PD/ledger_control.py', ('RATE_THIRD', 'EXTRA')):
        (2, '8d32c66bfc82127eeca8ed9a31ee95cc2482a63ea207800bfa81afd71175c469', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'unknown mutant label: RATE_THIRD EXTRA'),
    ('A4_1/author_controls.py', ('K2_UNIT',)):
        (1, '2cfa3406fdd94d2c43e789aeac7b4adbd1884470eac93e62642e2b08c5de625b', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'W0 Lemma LE_K (i) on pinned fields at gap k     16088/16104  FAIL'),
    ('A4_1/author_controls.py', ('LE_36',)):
        (1, 'a9270097f59dfb568667edadc445b39736c111b3653b2ef14fae93caddcd6054', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'W1 Lemma LE (ii), k-free                        21185/24001  FAIL'),
    ('A4_1/author_controls.py', ('OLD_ENDPOINT',)):
        (1, 'd070ce0fe2cbebdad3c0d092d0452aaa864e18cbd37ac9d167059a79e892cb1f', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'W3 growing-Lambda ledger at compact K             157/169    FAIL'),
    ('A4_1/author_controls.py', ('P_TWO',)):
        (1, '98483a1fb6a7919f335d0e5c44b5a50219d6b6b9bd8725083b9218e0553686e1', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'W3 growing-Lambda ledger at compact K             159/169    FAIL'),
    ('A4_1/author_controls.py', ('W_HALF',)):
        (1, '2acf100cee2f986e8a9cd246222866287840cd0388e6c894f5535bb222709ceb', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'W3 growing-Lambda ledger at compact K             153/169    FAIL'),
    ('A4_1/author_controls.py', ('ALPHA_4',)):
        (1, 'fbb704105e1b694f4e247d782658925417e3a35a82476f3d431c12e74d9a8461', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'W3 growing-Lambda ledger at compact K             136/169    FAIL'),
    ('A4_1/author_controls.py', ('BOGUS',)):
        (2, 'a0758636c5e479dfd217fb60eadb689f69c39901577d819a78384952bb8a1762', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'unknown mutant label: BOGUS'),
    ('A4_1/author_controls.py', ('K2_UNIT', 'EXTRA')):
        (2, '03e2874a92d3f3800824ba21e0dd62d943d2cfe7cb664608cff633f838bb0fd5', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'unknown mutant label: K2_UNIT EXTRA'),
    ('A4_2/author_controls.py', ('K2_UNIT',)):
        (1, '7bc449b3b52fd7e7984f89f9ce0e895c30ad2cf092deb400f98a62773d9d0300', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'B0 compact-K constants                           4002/4003   FAIL'),
    ('A4_2/author_controls.py', ('DB_HALF',)):
        (1, '66f7b52804ff3b42730fc1a6498cc9c5143a781fb3a21806abc15a9ad169ef84', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'B2 Lemma DB_K                                    5563/6000   FAIL'),
    ('A4_2/author_controls.py', ('PD_79',)):
        (1, '14f9308f12f5946dab0cff8f59c8658eb2c3b8df015822095545c7086e2aa4c6', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'B5 Corollary PD_ER                               3208/3210   FAIL'),
    ('A4_2/author_controls.py', ('CUM_169',)):
        (1, 'b12ff6662dc7d8f43946f5b3dc2dcd4eb09d1f34f1b1228be4492343e0d2574f', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'B5 Corollary PD_ER                               3209/3210   FAIL'),
    ('A4_2/author_controls.py', ('FRAC_109',)):
        (1, '77c20b1957180d69d06c56fea7d98f2690d2529b98d63de6d6a2e4c82b16ebc6', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'B5 Corollary PD_ER                               3209/3210   FAIL'),
    ('A4_2/author_controls.py', ('LOG_ONE',)):
        (1, 'c8cb4921914f8a9951549da7092ba92384b47650187b4704008d960b05de500a', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'B5 Corollary PD_ER                               2216/3210   FAIL'),
    ('A4_2/author_controls.py', ('BOGUS',)):
        (2, 'a0758636c5e479dfd217fb60eadb689f69c39901577d819a78384952bb8a1762', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'unknown mutant label: BOGUS'),
    ('A4_2/author_controls.py', ('K2_UNIT', 'EXTRA')):
        (2, '03e2874a92d3f3800824ba21e0dd62d943d2cfe7cb664608cff633f838bb0fd5', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'unknown mutant label: K2_UNIT EXTRA'),
    ('A4_3/author_controls.py', ('--mutant', 'M1')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'a77e8384e66f898ba45d3a4810e5e5bc1d3b28ad784af5d5f135352f8bd171b6', 'FAILED: Z1_lemma11_constants'),
    ('A4_3/author_controls.py', ('--mutant', 'M2')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '239fc0d3592727173c67e1dfc91f52e276a70fbfdc58531ae70171ecaaeffe3a', 'FAILED: Z2_planar_integrals'),
    ('A4_3/author_controls.py', ('--mutant', 'M3')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'b9d23c047a77e2e18017f9a13ebcfe65801752310827a971d3f73b15cd190bb3', 'FAILED: Z3_margin_totals'),
    ('A4_3/author_controls.py', ('--mutant', 'M4')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '52c19fdd472914c19c5fbf4e8a50834a6b6c6f9fa7869e4f2f5092b705200a11', 'FAILED: Z4_endpoint_shell'),
    ('A4_3/author_controls.py', ('--mutant', 'M5')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '9e7ee4702277c6e06f37f36bda05db1d739ffb46cf234569061c8df4bab49e9f', 'FAILED: Z5_shell_sums'),
    ('A4_3/author_controls.py', ('--mutant', 'M6')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '203d48ca23b6a931f14be06f89cbff07de1d78d1ae1d0e2bd79c698c168525e8', 'FAILED: Z6_exponent_tables'),
    ('A4_3/author_controls.py', ('--mutant', 'M7')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '3b56ef2b44d8b4e952ce7cb1df1b4ae9d1cfec4d98cc240d0e672b57263cb906', 'FAILED: Z7_pd_constants'),
    ('A4_3/author_controls.py', ('--mutant', 'M8')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '239fc0d3592727173c67e1dfc91f52e276a70fbfdc58531ae70171ecaaeffe3a', 'FAILED: Z2_planar_integrals'),
    ('A4_3/author_controls.py', ('--mutant', 'M9')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '3b56ef2b44d8b4e952ce7cb1df1b4ae9d1cfec4d98cc240d0e672b57263cb906', 'FAILED: Z7_pd_constants'),
    ('A4_3/author_controls.py', ('--mutant', 'M10')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '4fcced418c5b3b94f936911ed889027be1cd2cde48516616b550cd1b4bb07c60', 'FAILED: Z8_k1_constants'),
    ('A4_3/author_controls.py', ('--bogus',)):
        (2, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '8e5fa75822c70bbf41668bd94fac3cddadc2113e41b362975cd2a95a27bbb21e', 'usage: a43_exact.py [--mutant M1..M10]'),
    ('A4_3/author_controls.py', ('--mutant', 'M11')):
        (2, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '8e5fa75822c70bbf41668bd94fac3cddadc2113e41b362975cd2a95a27bbb21e', 'usage: a43_exact.py [--mutant M1..M10]'),
    ('A4_3/author_controls.py', ('--mutant',)):
        (2, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '8e5fa75822c70bbf41668bd94fac3cddadc2113e41b362975cd2a95a27bbb21e', 'usage: a43_exact.py [--mutant M1..M10]'),
}

# Replacing A4.3's Lemma 1.1 constant 192 by 96 with MUT=None must fail specifically at Z1, on stderr alone.
NEGATIVE_CONSTANT = (1, hashlib.sha256(b'').hexdigest(),
                     hashlib.sha256(b'FAILED: Z1_lemma11_constants\n').hexdigest(), 'Z1_lemma11_constants')


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
        target = copy / 'A4_3' / 'PROOF.md'
        data = bytearray(target.read_bytes())
        data[100] ^= 0x01
        target.write_bytes(bytes(data))
        if 'identity mismatch: A4_3/PROOF.md' not in tree_failures(copy, manifest):
            failures.append('negative control: a one-byte change to A4_3/PROOF.md was not detected')
        script = copy / 'A4_3' / 'author_controls.py'
        text = script.read_text(encoding='utf-8')
        old = 'K192 = F(96) if MUT == "M1" else F(192)'
        if text.count(old) != 1:
            failures.append('negative control: the Lemma 1.1 constant line was not found exactly once')
        else:
            script.write_text(text.replace(old, 'K192 = F(96) if MUT == "M1" else F(96)'), encoding='utf-8')
            result = run(script)
            mismatches = check_rejection(result, NEGATIVE_CONSTANT)
            failures.extend('negative control: changed Lemma 1.1 constant: ' + why for why in mismatches)
            if not mismatches:
                report_control('A4_3/author_controls.py', [], result, 'changed 192 to 96: Z1_lemma11_constants')
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
        print('Planar compact-K chain (PD, A4.1-A4.3) incorporation replay (%s): %d failure(s)' % (mode, len(failures)))
        return 1
    print('Planar compact-K chain (PD, A4.1-A4.3) incorporation replay (%s): %d stored identities, %d extractions, %d checker stdouts, '
          '%d mutants, %d invalid invocations and 2 negative controls PASS' % (mode, n_files, 2 * n_scripts, n_scripts, n_mut, n_inv))
    return 0


if __name__ == '__main__':
    sys.exit(main())
