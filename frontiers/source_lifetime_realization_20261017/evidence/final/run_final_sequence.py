"""Execute the final stable source closure once, then standard kernel replay.

Each child is bounded and serialized by run_final_phase.py. This driver stops
at the first failure; it never retries a failed or successful phase silently.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def now():
    return datetime.now(timezone.utc).isoformat()


def main():
    inventory_path = ROOT / 'FINAL_SOURCE_INVENTORY.json'
    inventory = json.loads(inventory_path.read_text())
    output = ROOT / 'FINAL_SEQUENCE_RESULT.json'
    if output.exists():
        raise RuntimeError('final sequence already attempted; inspect the actual result')
    report = {'started_utc': now(), 'source_inventory_sha256': hashlib.sha256(
        inventory_path.read_bytes()).hexdigest(), 'phases': [],
        'status': 'RUNNING', 'scientific_effect': 'NONE'}
    # Exclusive creation also prevents concurrent drivers and silent crash retry.
    # A surviving START without RESULT is HOLD_INTERRUPTED, never a fresh run.
    with (ROOT / 'FINAL_SEQUENCE_START.json').open('x') as f:
        json.dump(report, f, indent=2)
        f.write('\n')
    phases = [('build', m) for m in inventory['build_order']]
    phases += [('kernel', m) for m in inventory['new_modules']]
    for kind, module in phases:
        command = [sys.executable, '-B', str(ROOT / 'run_final_phase.py'), kind, module]
        started = now()
        code = subprocess.run(command, cwd=ROOT).returncode
        report['phases'].append({'kind': kind, 'module': module,
                                 'started_utc': started, 'ended_utc': now(),
                                 'returncode': code})
        progress = ROOT / 'FINAL_SEQUENCE_PROGRESS.json'
        staged = progress.with_suffix('.json.pending')
        staged.write_text(json.dumps(report, indent=2) + '\n')
        staged.replace(progress)
        if code != 0:
            report.update(status='HOLD_FAILED_PHASE', ended_utc=now())
            with output.open('x') as f:
                json.dump(report, f, indent=2)
                f.write('\n')
            return 1
    report.update(status='PASS_LOCAL_SOURCE_BUILD_AND_STANDARD_KERNEL_REPLAY', ended_utc=now())
    with output.open('x') as f:
        json.dump(report, f, indent=2)
        f.write('\n')
    print(json.dumps({'stage': 'FINAL_SEQUENCE_FINISHED', 'status': report['status'],
                      'phases': len(report['phases'])}), flush=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
