#!/usr/bin/env python3
"""Bind current-run formal evidence to an existing required check; no scientific authority."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

REPOSITORIES = {'d6g8k5htny-coder/main', 'd6g8k5htny-coder/Math-'}
LEAN_RELEASE = re.compile(r'Lean \(version 4\.34\.1, [^()\r\n]+, commit '
                          r'5045d0056413266e57c625dcd7c365b10e377c52, Release\)')
OBSERVATION_KEYS = {'lean_version', 'dependency_revisions', 'dependency_worktrees', 'manifest_sha256'}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def exact(value, pattern: str, name: str) -> str:
    require(isinstance(value, str) and re.fullmatch(pattern, value) is not None,
            'invalid '+name)
    return value


def strict_json(text: str):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'duplicate JSON key: '+key)
            result[key] = value
        return result
    def constant(value):
        raise ValueError('nonfinite JSON: '+value)
    return json.loads(text, object_pairs_hook=pairs, parse_constant=constant)


def context(env: dict) -> dict:
    repository = env.get('GITHUB_REPOSITORY')
    require(repository in REPOSITORIES, 'unexpected execution repository')
    return {
        'checked_commit': exact(env.get('GITHUB_SHA'), r'[0-9a-f]{40}', 'commit'),
        'repository': repository,
        'run_id': exact(env.get('GITHUB_RUN_ID'), r'[1-9][0-9]*', 'run ID'),
        'run_attempt': exact(env.get('GITHUB_RUN_ATTEMPT'), r'[1-9][0-9]*', 'attempt'),
    }


def dependency_lock(raw: bytes) -> dict:
    lock = strict_json(raw.decode('utf-8')).get('dependency_revisions')
    require(isinstance(lock, dict) and bool(lock) and all(
        isinstance(name, str) and isinstance(rev, str) and re.fullmatch(r'[0-9a-f]{40}', rev)
        for name, rev in lock.items()), 'manifest has no exact dependency lock')
    return lock


def runtime_observation(value, lock: dict, name: str) -> dict:
    """One producer observation: the pinned release, the locked dependencies, clean worktrees."""
    require(isinstance(value, dict) and set(value) == OBSERVATION_KEYS, 'invalid '+name+' observation')
    require(isinstance(value['lean_version'], str) and LEAN_RELEASE.fullmatch(value['lean_version']) is not None,
            name+' runtime is not the pinned Lean release')
    require(value['dependency_revisions'] == lock, name+' dependencies differ from the lock')
    require(value['dependency_worktrees'] == 'CLEAN', name+' dependency worktrees are not clean')
    return value


def manifest_identity(manifest: Path, raw: bytes) -> str:
    """Select one declared source identity; never downgrade an overlay receipt."""
    document = strict_json(raw.decode('utf-8'))
    require(isinstance(document, dict), 'manifest must be an object')
    overlay = manifest.with_name('manifest.overlay.json')
    if 'source_identity' not in document:
        require(not overlay.exists() and not overlay.is_symlink(), 'undeclared manifest overlay')
        return hashlib.sha256(raw).hexdigest()
    require(document['source_identity'] == {
        'schema': 'rf312-overlay-v1', 'overlay': 'manifest.overlay.json'},
        'unsupported source identity contract')
    require(not overlay.is_symlink() and overlay.is_file(),
            'missing or nonregular manifest overlay')
    overlay_raw = overlay.read_bytes()
    value = strict_json(overlay_raw.decode('utf-8'))
    require(isinstance(value, dict) and set(value) == {'schema_version', 'files'},
            'invalid manifest overlay keys')
    require(type(value['schema_version']) is int and value['schema_version'] == 1
            and isinstance(value['files'], dict), 'invalid manifest overlay schema')
    require(all(isinstance(name, str) and isinstance(digest, str)
                and re.fullmatch(r'[0-9a-f]{64}', digest) is not None
                for name, digest in value['files'].items()),
            'invalid manifest overlay file binding')
    return hashlib.sha256(raw + b'\0RF312-OVERLAY\0' + overlay_raw).hexdigest()


def bind_receipt(receipt: Path, manifest: Path, env: dict, git_head: str) -> dict:
    ctx = context(env)
    require(git_head == ctx['checked_commit'], 'checkout/tested commit mismatch')
    require(not receipt.is_symlink() and not manifest.is_symlink(), 'symlinked evidence')
    raw = receipt.read_bytes()
    record = strict_json(raw.decode('utf-8'))
    require(isinstance(record, dict), 'receipt must be an object')
    for key, expected in [('checked_commit', ctx['checked_commit']),
                          ('repository', ctx['repository']),
                          ('workflow_run_id', ctx['run_id']),
                          ('formalization_status', 'kernel-checked'),
                          ('scientific_effect', 'NONE')]:
        require(record.get(key) == expected, 'receipt mismatch: '+key)
    manifest_raw = manifest.read_bytes()
    require(record.get('manifest_sha256') == manifest_identity(manifest, manifest_raw),
            'manifest/receipt mismatch')
    # The producer's runtime fields are validated, not only hashed: the exact release, the
    # locked and clean dependencies, this attempt, and equal observations before the first
    # and after the last Lean execution. A missing or older-schema field refuses.
    lock = dependency_lock(manifest_raw)
    require(record.get('workflow_run_attempt') == ctx['run_attempt'], 'receipt mismatch: workflow_run_attempt')
    require(isinstance(record.get('lean_version'), str) and LEAN_RELEASE.fullmatch(record['lean_version']) is not None,
            'receipt runtime is not the pinned Lean release')
    require(record.get('dependency_revisions') == lock, 'receipt dependencies differ from the lock')
    require(record.get('dependency_worktrees') == 'CLEAN', 'receipt dependency worktrees are not clean')
    observations = record.get('observations')
    require(isinstance(observations, dict) and set(observations) == {'preflight', 'final'},
            'receipt lacks the preflight and final runtime observations')
    preflight = runtime_observation(observations['preflight'], lock, 'preflight')
    final = runtime_observation(observations['final'], lock, 'final')
    require(preflight == final, 'runtime changed between the preflight and final observations')
    require(final['lean_version'] == record['lean_version'] and final['manifest_sha256'] == record['manifest_sha256'],
            'final observation differs from the receipt')
    logs = record.get('logs')
    require(isinstance(logs, dict) and bool(logs), 'missing receipt log bindings')
    for name, digest in logs.items():
        exact(name, r'[A-Za-z0-9_-]+\.log', 'log name')
        exact(digest, r'[0-9a-f]{64}', 'log digest')
        log = receipt.parent/name
        require(not log.is_symlink(), 'symlinked log')
        require(hashlib.sha256(log.read_bytes()).hexdigest() == digest, 'log hash mismatch: '+name)
    return {**ctx, 'receipt_sha256': hashlib.sha256(raw).hexdigest()}


def aggregate(needs, env: dict) -> dict:
    ctx = context(env)
    require(isinstance(needs, dict) and set(needs) == {'checks', 'formal'},
            'exact checks/formal dependencies required')
    for name in ('checks', 'formal'):
        job = needs[name]
        require(isinstance(job, dict) and job.get('result') == 'success',
                'dependency did not succeed: '+name)
        require(isinstance(job.get('outputs'), dict), 'missing dependency outputs: '+name)
        require(job['outputs'].get('checked_commit') == ctx['checked_commit'],
                'dependency commit mismatch: '+name)
    outputs = needs['formal']['outputs']
    for key, value in ctx.items():
        require(outputs.get(key) == value, 'formal evidence mismatch: '+key)
    digest = exact(outputs.get('receipt_sha256'), r'[0-9a-f]{64}', 'receipt digest')
    return {**ctx, 'receipt_sha256': digest, 'conclusion': 'success',
            'scientific_effect': 'NONE',
            'meaning': 'Required engineering checks and current-run formal evidence only; not statement alignment or scientific acceptance.'}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=['receipt', 'aggregate'])
    args = parser.parse_args()
    try:
        env = dict(os.environ)
        if args.operation == 'receipt':
            folder = Path('formal/.lake/formal-evidence')
            head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True, timeout=30).strip()
            result = bind_receipt(folder/'receipt.json', Path('formal/manifest.json'), env, head)
            # Never rewrite the original gate receipt.
            (folder/'required-check-binding.json').write_text(json.dumps(result, indent=2)+'\n')
            with open(env['GITHUB_OUTPUT'], 'a', encoding='utf-8') as output:
                for key, value in result.items():
                    output.write(f'{key}={value}\n')
        else:
            result = aggregate(strict_json(env['REQUIRED_FORMAL_NEEDS']), env)
        print(json.dumps(result, indent=2))
        return 0
    except (ValueError, KeyError, OSError, subprocess.SubprocessError) as exc:
        print('REQUIRED_FORMAL_CHECK_FAILED: '+str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
