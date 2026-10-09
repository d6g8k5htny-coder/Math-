#!/usr/bin/env python3
"""Verify the stored records of lifetime notes V24 and DC, and replay their published author controls (standard
library only).

Every file in this packet except replay.py, README.md and SOURCES.json is one of two things:
  - an exact copy of a public comment body on main#229 (a note, claim, controls comment, read request, summons,
    review, correction or author response);
  - a control script or its stdout, extracted verbatim from its stored controls comment by the extraction rule that
    comment states (the rule of main#229 comment 5971055189). Each stdout is a ```json fence.
SOURCES.json pins each file by byte count and SHA-256 and lists each replay. This script performs four checks.

  1. The packet tree equals SOURCES.json's file list, with no symlinks, and every stored file has its pinned
     identity.
  2. Every extracted script and stdout equals the fenced payload inside its stored source comment, under the
     extraction rule (the stdout fence language follows the stored stdout's suffix: .json for ```json, .txt for ```text).
  3. Every control script runs under the current interpreter's -O/-S flags and reproduces its published stdout byte
     for byte (none prints an interpreter version), with empty stderr. Every listed mutant or invalid invocation
     must reproduce its exact source-bound rejection on BOTH captured streams, not merely exit 1 or 2.
  4. Negative controls must be rejected:
     - a one-byte change to a stored note (DC/PROOF.md);
     - a control script with one changed constant (v24_exact.py's constant 1/2000, Lemma J's lower bound for J,
       replaced by 1/1000).

Reproducibility only. The analytic notes and their reads carry the mathematics. These finite checks support
algebra, as the reads say. Nothing here reads or grades a proof.

Usage: python3 -B -S frontiers/v24_dc_two_thirds_sign_20261007/replay.py   (exit 0 iff every check passes)
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

# Exact rejection fingerprints of the extracted author controls (v24_exact.py from 6034161613, dc_exact.py from
# 6037458253), computed under both interpreter modes at incorporation and found identical.
# Each key is (script path, complete argv tail); each value is (exit, stdout SHA256,
# stderr SHA256, readable reason). References are frozen independently of this run.
# All 30 mutants and 10 invalid invocations were executed and their named reasons
# checked against their source. Exact fingerprints enforce the full contracts,
# including the empty stdout, the FAILED or usage line and its group name.
# No current failing output, generic exit code or broad regex creates a reference.
# Any source/runtime output drift fails closed and requires a reviewed amendment.
REJECTION_CONTRACTS = {
    ('V24/author_controls.py', ('--mutant', 'M1')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '292eead72f233827985c80e23d391c939164fff05ddbf6a23bcbef199d74c8df', 'FAILED: V1_covariance'),
    ('V24/author_controls.py', ('--mutant', 'M2')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '314e20300312da133a8b8c3c83ad335c5df5fd9ecc4dd1862636ff5d5c7974a8', 'FAILED: V2_image_bound'),
    ('V24/author_controls.py', ('--mutant', 'M3')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'dcd6d035b101e48ca001cab0095571a52fe5de2fc6ee33481c8f640cd79b49d0', 'FAILED: V3_sandwich'),
    ('V24/author_controls.py', ('--mutant', 'M4')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '6b100dde3d17c9a624b236901a03e1de957492eac07cbceb40f9c7b398ddffdb', 'FAILED: V4_gamma_parts'),
    ('V24/author_controls.py', ('--mutant', 'M5')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '6b100dde3d17c9a624b236901a03e1de957492eac07cbceb40f9c7b398ddffdb', 'FAILED: V4_gamma_parts'),
    ('V24/author_controls.py', ('--mutant', 'M6')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'ddfe08cddf797a54f45c072bb4ed4958a077e6b4ca82e38d84dba831591f2edd', 'FAILED: V6_J_bounds'),
    ('V24/author_controls.py', ('--mutant', 'M7')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '14878f4a6fe742a959167a9d9ebf377792b8ddb1692249b00121a2fb412cb8bd', 'FAILED: V7_lemma_K'),
    ('V24/author_controls.py', ('--mutant', 'M8')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '37fa3c448e0245d958c6f0fc13a05f65d5b52bb70c7a8a98014bd8c490d477de', 'FAILED: V5_moment_perturbation'),
    ('V24/author_controls.py', ('--mutant', 'M9')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'a9797739bf8963066ebb81ee434b85b3b1c1245c9bbcf7f8ebe99740bd9d4547', 'FAILED: V8_assembly'),
    ('V24/author_controls.py', ('--mutant', 'M10')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'd0501c81249cc1edd34137ed66b46d2cd99c217ae3723dc502e8767db9f6cd54', 'FAILED: V9_lemmaK_step1'),
    ('V24/author_controls.py', ('--mutant', 'M11')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '6b100dde3d17c9a624b236901a03e1de957492eac07cbceb40f9c7b398ddffdb', 'FAILED: V4_gamma_parts'),
    ('V24/author_controls.py', ('--mutant', 'M12')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'a9797739bf8963066ebb81ee434b85b3b1c1245c9bbcf7f8ebe99740bd9d4547', 'FAILED: V8_assembly'),
    ('V24/author_controls.py', ('--bogus',)):
        (2, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '2386523a35332edff8899d2aef480bf198509fad53fab0f79aae9336f3ea0d2a', 'usage: v24_exact.py [--mutant M1..M12]'),
    ('V24/author_controls.py', ('--mutant', 'M13')):
        (2, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '2386523a35332edff8899d2aef480bf198509fad53fab0f79aae9336f3ea0d2a', 'usage: v24_exact.py [--mutant M1..M12]'),
    ('V24/author_controls.py', ('--mutant',)):
        (2, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '2386523a35332edff8899d2aef480bf198509fad53fab0f79aae9336f3ea0d2a', 'usage: v24_exact.py [--mutant M1..M12]'),
    ('V24/author_controls.py', ('--mutant', 'm12')):
        (2, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '2386523a35332edff8899d2aef480bf198509fad53fab0f79aae9336f3ea0d2a', 'usage: v24_exact.py [--mutant M1..M12]'),
    ('V24/author_controls.py', ('--mutant', 'M1', 'extra')):
        (2, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '2386523a35332edff8899d2aef480bf198509fad53fab0f79aae9336f3ea0d2a', 'usage: v24_exact.py [--mutant M1..M12]'),
    ('DC/author_controls.py', ('--mutant', 'M1')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'befb0784c3fbca001c1476815d9c4840b590399b2327bc0ee0ce653557ae6dc4', 'FAILED: R2_monotone'),
    ('DC/author_controls.py', ('--mutant', 'M2')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '58adc08ca1292aa89d68c9aae6623fc64798521410dfca3169ae5d6ff386122d', 'FAILED: mills'),
    ('DC/author_controls.py', ('--mutant', 'M3')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '8c049dcddc052d669c2676aa34dc69d899ebb4b6e0777851e2a88969ed154a3f', 'FAILED: T2'),
    ('DC/author_controls.py', ('--mutant', 'M4')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'c73cf42d415022f8f5e0c2452ec58ff48b6e3e160e1546960018ea597e7960e0', 'FAILED: T1_moment'),
    ('DC/author_controls.py', ('--mutant', 'M5')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'ef6bfa7bd1b88668e57d98f9e1cbd01f431c2df6b00f07cda25fef4dfb7595c2', 'FAILED: T3_moment'),
    ('DC/author_controls.py', ('--mutant', 'M6')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '268e447b0c040f9b9f4376e868f17b0394e14247a13e91bc3fb77651eeab2527', 'FAILED: R2_formula'),
    ('DC/author_controls.py', ('--mutant', 'M7')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '752297ef40c867a7efca954b6a6ee461065c0a10f9dfeca3dac4327ab781f732', 'FAILED: partition'),
    ('DC/author_controls.py', ('--mutant', 'M8')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '661280ddfcc3b68e87eb5d881bfb664f0d37ccc73abc73f97f63e1280bb38e7a', 'FAILED: gamma'),
    ('DC/author_controls.py', ('--mutant', 'M9')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '978f4fd12123ad0cce06eace29416f5f23cc114cb646a971cb4182bd21cff50a', 'FAILED: theta_table'),
    ('DC/author_controls.py', ('--mutant', 'M10')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'a2229f52802e04eb0600658ad4de6dae5d698985d5db74041669fdc78f78edb1', 'FAILED: g_machinery'),
    ('DC/author_controls.py', ('--mutant', 'M11')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '25c4e26925f5b726dcdb7880213dc103ef852727a5475ef2c18b8d04766e0e07', 'FAILED: lemma4'),
    ('DC/author_controls.py', ('--mutant', 'M12')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '752297ef40c867a7efca954b6a6ee461065c0a10f9dfeca3dac4327ab781f732', 'FAILED: partition'),
    ('DC/author_controls.py', ('--mutant', 'M13')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '6c1299e44e560dc751cb456fb1c63b350e9830e0d49204ee713167b88aea811e', 'FAILED: corners'),
    ('DC/author_controls.py', ('--mutant', 'M14')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '6c1299e44e560dc751cb456fb1c63b350e9830e0d49204ee713167b88aea811e', 'FAILED: corners'),
    ('DC/author_controls.py', ('--mutant', 'M15')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '25c4e26925f5b726dcdb7880213dc103ef852727a5475ef2c18b8d04766e0e07', 'FAILED: lemma4'),
    ('DC/author_controls.py', ('--mutant', 'M16')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '6c1299e44e560dc751cb456fb1c63b350e9830e0d49204ee713167b88aea811e', 'FAILED: corners'),
    ('DC/author_controls.py', ('--mutant', 'M17')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '6c1299e44e560dc751cb456fb1c63b350e9830e0d49204ee713167b88aea811e', 'FAILED: corners'),
    ('DC/author_controls.py', ('--mutant', 'M18')):
        (1, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '25c4e26925f5b726dcdb7880213dc103ef852727a5475ef2c18b8d04766e0e07', 'FAILED: lemma4'),
    ('DC/author_controls.py', ('--bogus',)):
        (2, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'ab49f5b955d419d7b942781f60ed78707e526a5aa0dcbc2cc6784c858ea2c6ad', 'usage: dc_exact.py [--mutant M1..M18]'),
    ('DC/author_controls.py', ('--mutant', 'M19')):
        (2, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'ab49f5b955d419d7b942781f60ed78707e526a5aa0dcbc2cc6784c858ea2c6ad', 'usage: dc_exact.py [--mutant M1..M18]'),
    ('DC/author_controls.py', ('--mutant',)):
        (2, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'ab49f5b955d419d7b942781f60ed78707e526a5aa0dcbc2cc6784c858ea2c6ad', 'usage: dc_exact.py [--mutant M1..M18]'),
    ('DC/author_controls.py', ('--mutant', 'm18')):
        (2, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'ab49f5b955d419d7b942781f60ed78707e526a5aa0dcbc2cc6784c858ea2c6ad', 'usage: dc_exact.py [--mutant M1..M18]'),
    ('DC/author_controls.py', ('--mutant', 'M1', 'extra')):
        (2, 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'ab49f5b955d419d7b942781f60ed78707e526a5aa0dcbc2cc6784c858ea2c6ad', 'usage: dc_exact.py [--mutant M1..M18]'),
}

# Replacing v24_exact.py's constant 1/2000 (Lemma J's lower bound for J) by 1/1000 with MUT=None must fail
# specifically at V6, on stderr alone.
NEGATIVE_CONSTANT = (1, hashlib.sha256(b'').hexdigest(),
                     hashlib.sha256(b'FAILED: V6_J_bounds\n').hexdigest(), 'V6_J_bounds')


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
        target = copy / 'DC' / 'PROOF.md'
        data = bytearray(target.read_bytes())
        data[100] ^= 0x01
        target.write_bytes(bytes(data))
        if 'identity mismatch: DC/PROOF.md' not in tree_failures(copy, manifest):
            failures.append('negative control: a one-byte change to DC/PROOF.md was not detected')
        script = copy / 'V24' / 'author_controls.py'
        text = script.read_text(encoding='utf-8')
        old = 'claim = F(1, 1000) if MUT == "M6" else F(1, 2000)'
        if text.count(old) != 1:
            failures.append('negative control: the Lemma J constant line was not found exactly once')
        else:
            script.write_text(text.replace(old, 'claim = F(1, 1000) if MUT == "M6" else F(1, 1000)'), encoding='utf-8')
            result = run(script)
            mismatches = check_rejection(result, NEGATIVE_CONSTANT)
            failures.extend('negative control: changed Lemma J constant: ' + why for why in mismatches)
            if not mismatches:
                report_control('V24/author_controls.py', [], result, 'changed 1/2000 to 1/1000: V6_J_bounds')
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
        print('Lifetime notes V24 and DC incorporation replay (%s): %d failure(s)' % (mode, len(failures)))
        return 1
    print('Lifetime notes V24 and DC incorporation replay (%s): %d stored identities, %d extractions, %d checker stdouts, '
          '%d mutants, %d invalid invocations and 2 negative controls PASS' % (mode, n_files, 2 * n_scripts, n_scripts, n_mut, n_inv))
    return 0


if __name__ == '__main__':
    sys.exit(main())
