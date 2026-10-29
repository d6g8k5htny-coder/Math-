"""Retain standard-library regression/CLI receipts without touching input files."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import resource
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, sort_keys=True, indent=2) + '\n')


def inventory():
    return {str(p.relative_to(ROOT)): sha(p.read_bytes()) for p in sorted(ROOT.rglob('*'))
            if p.is_file() and 'evidence' not in p.relative_to(ROOT).parts
            and '__pycache__' not in p.relative_to(ROOT).parts}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists():
        raise SystemExit('output must not exist')
    output.mkdir(parents=True)
    before = inventory()
    write(output / 'source_inventory.json', before)
    for relative, expected in before.items():
        data = (ROOT / relative).read_bytes()
        if sha(data) != expected:
            raise SystemExit('input changed during source snapshot')
        target = output / 'frozen_sources' / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    policy = ROOT / 'fixtures/positive/policy.json'
    dataset = ROOT / 'fixtures/positive/dataset.json'
    rejected = ROOT / 'fixtures/positive/rejected_duplicate_dataset.json'
    pin = sha(policy.read_bytes())
    results = []
    started = time.monotonic_ns()
    for optimized in (False, True):
        mode = 'optimized' if optimized else 'normal'
        flags = ['-B'] + (['-O'] if optimized else [])
        cases = [
            ('tests', ['-m', 'unittest', 'discover', '-s', 'tests', '-v'], 0, None),
            ('fixture', ['admission.py', str(dataset), '--policy', str(policy),
                         '--expected-policy-sha256', pin], 0, 'policy_admitted_fixture'),
            ('duplicate_denial', ['admission.py', str(rejected), '--policy', str(policy),
                                  '--expected-policy-sha256', pin], 1, 'denied')]
        for name, arguments, expected_exit, expected_status in cases:
            leaf = output / (mode + '_' + name)
            leaf.mkdir()
            command = [sys.executable] + flags + arguments
            prior = resource.getrusage(resource.RUSAGE_CHILDREN)
            tick = time.monotonic_ns()
            completed = subprocess.run(command, cwd=ROOT, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE, env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
            elapsed = time.monotonic_ns() - tick
            after = resource.getrusage(resource.RUSAGE_CHILDREN)
            (leaf / 'stdout.txt').write_bytes(completed.stdout)
            (leaf / 'stderr.txt').write_bytes(completed.stderr)
            valid = completed.returncode == expected_exit
            count = None
            if expected_status is None:
                match = re.search(rb'Ran (\d+) tests?', completed.stderr)
                count = int(match.group(1)) if match else None
                valid = valid and count is not None and b'\nOK\n' in completed.stderr
            else:
                try:
                    body = json.loads(completed.stdout)
                    valid = valid and body.get('status') == expected_status
                    valid = valid and body.get('actual_training_authorized') is False
                    valid = valid and body.get('scientific_corpus_established') is False
                    valid = valid and body.get('kernel_executed') is False
                    if expected_status == 'denied':
                        valid = valid and any(v.get('code') == 'duplicate_record_id'
                                              for v in body.get('violations', []))
                except (ValueError, AttributeError):
                    valid = False
            receipt = {'schema': 'ul-corpus-verification-child-v1', 'name': name,
                       'mode': mode, 'command': command, 'exit_code': completed.returncode,
                       'expected_exit_code': expected_exit, 'status': 'pass' if valid else 'fail',
                       'wall_seconds': elapsed / 1e9,
                       'child_user_cpu_seconds': after.ru_utime - prior.ru_utime,
                       'child_system_cpu_seconds': after.ru_stime - prior.ru_stime,
                       'stdout_sha256': sha(completed.stdout), 'stderr_sha256': sha(completed.stderr),
                       'test_count': count, 'native_worker_launched': False}
            write(leaf / 'receipt.json', receipt)
            results.append(receipt)
    unchanged = before == inventory()
    counts = [row['test_count'] for row in results if row['name'] == 'tests']
    modes_equal = all((output / ('normal_' + name) / 'stdout.txt').read_bytes() ==
                      (output / ('optimized_' + name) / 'stdout.txt').read_bytes()
                      for name in ('fixture', 'duplicate_denial'))
    valid = unchanged and all(r['status'] == 'pass' for r in results) and len(set(counts)) == 1 and modes_equal
    summary = {'schema': 'ul-corpus-verification-campaign-v1', 'status': 'pass' if valid else 'fail',
               'launches': len(results), 'tests_each_mode': counts[0],
               'inputs_unchanged': unchanged, 'cli_json_byte_equal_across_modes': modes_equal,
               'source_inventory_sha256': sha((output / 'source_inventory.json').read_bytes()),
               'fixture_policy_sha256': pin, 'wall_seconds': (time.monotonic_ns() - started) / 1e9,
               'native_work': False, 'RL_training': False, 'scientific_corpus_established': False,
               'results': results}
    write(output / 'results.json', summary)
    print(json.dumps({key: value for key, value in summary.items() if key != 'results'}, sort_keys=True))
    return 0 if valid else 1


if __name__ == '__main__':
    raise SystemExit(main())
