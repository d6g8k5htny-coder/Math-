#!/usr/bin/env python3
"""Replay the published C89 v1.1 reviewer controls against the exact sources (standard library only).

C89 v1.1, "Quantitative separated jets and a shrinking far-elder region" (Math- #188 comment 5963100306,
OpenAI / Codex), is kept in this packet as C89_V1_1_PROOF.md. Its full review (comment 5963217842) published
the script c89_reviewer_controls.py and that script's stdout; both are kept here byte for byte. The review ran
the script with --source-dir holding PROOF.md (the C89 proof), source/P.md ([P]) and source/G.md ([G], this
packet's PROOF.md). This wrapper assembles that layout from repository files in a temporary directory, runs the
script under the current interpreter's -O/-S flags, and requires its stdout to equal the published bytes. A
one-byte change to the C89 copy must change the replay (negative control).

Reproducibility only: the analytic proof and its review carry the mathematics, not this replay.

Usage: python3 -B -S frontiers/far_elder_flat_ridge_20260930/c89_replay.py   (exit 0 iff every check passes)
"""
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
P_SOURCE = ROOT / 'imports' / 'lifetime_parent_20260925' / 'UNIFORM_MATRIX_CAP_AND_LIFETIME.md'

# (bytes, SHA256) as published in the review 5963217842 and the delivery note 5963266074.
IDENTITIES = {
    'C89_V1_1_PROOF.md': (15039, '7d8d3063caa0dfb5edbfe75437d7ccff8ab74697d1dd92c4b47cca5926b02392'),
    'C89_V1_PROOF.md': (14742, '74af6322bdcccec0b718b6abcbfb36b139c40d07398849af9a35ad2000bc31f1'),
    'c89_reviewer_controls.py': (12190, '83982f11df2f145f8dcde55c1900ef8723d46b0820f269049e3c2f4f05da9fab'),
    'c89_reviewer_stdout.json': (1068, 'cee69d10a059a1cc62ef89624e85da7b035fa2e309c77bafe0eb87e8d450a074'),
    'PROOF.md': (29110, '967148439e32e8e5d6c06a12df5cc7c1eb2475fe6828e4aeb3748c48817a4cba'),
}
P_IDENTITY = (40261, '9350ad6eaba6626b93c3dedeef9e2ff816e5cdf1c8318e85fb27499141c84bc7')


def identity(data):
    return len(data), hashlib.sha256(data).hexdigest()


def interpreter_flags():
    flags = ['-B']
    if sys.flags.optimize:
        flags.append('-O')
    if sys.flags.no_site:
        flags.append('-S')
    return flags


def replay(proof_bytes):
    """Run the reviewer script on PROOF.md = proof_bytes, source/P.md = [P], source/G.md = [G]."""
    with tempfile.TemporaryDirectory() as tmp:
        src = pathlib.Path(tmp)
        (src / 'source').mkdir()
        (src / 'PROOF.md').write_bytes(proof_bytes)
        shutil.copyfile(P_SOURCE, src / 'source' / 'P.md')
        shutil.copyfile(HERE / 'PROOF.md', src / 'source' / 'G.md')
        run = subprocess.run([sys.executable, *interpreter_flags(), str(HERE / 'c89_reviewer_controls.py'),
                              '--source-dir', str(src)], capture_output=True, timeout=600)
        return run.returncode, run.stdout


def main():
    failures = []
    for name, expected in IDENTITIES.items():
        if identity((HERE / name).read_bytes()) != expected:
            failures.append('identity mismatch: ' + name)
    if identity(P_SOURCE.read_bytes()) != P_IDENTITY:
        failures.append('identity mismatch: [P] ' + str(P_SOURCE.relative_to(ROOT)))
    published = (HERE / 'c89_reviewer_stdout.json').read_bytes()
    proof = (HERE / 'C89_V1_1_PROOF.md').read_bytes()
    code, out = replay(proof)
    if code != 0:
        failures.append('reviewer script exit code %d' % code)
    if out != published:
        failures.append('reviewer stdout differs from the published bytes')
    altered = proof.replace(b'A_N = 24J + 12dN', b'A_N = 24J + 13dN', 1)
    if altered == proof:
        failures.append('negative control could not alter the C89 copy')
    else:
        code2, out2 = replay(altered)
        if code2 == 0 and out2 == published:
            failures.append('negative control: an altered C89 copy reproduced the published stdout')
    print(json.dumps({'object': 'C89 v1.1 reviewer-controls replay',
                      'interpreter_flags': interpreter_flags(),
                      'published_stdout_sha256': identity(published)[1],
                      'replay_stdout_sha256': identity(out)[1],
                      'failures': failures,
                      'scientific_effect': 'NONE'}, sort_keys=True))
    return 0 if not failures else 1


if __name__ == '__main__':
    sys.exit(main())
