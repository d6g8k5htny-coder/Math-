"""Replay only unresolved kernels after preserving exact child-discovery failure."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def now():
    return datetime.now(timezone.utc).isoformat()


def record(path):
    return {'path': path, 'sha256': hashlib.sha256((ROOT / path).read_bytes()).hexdigest()}


def main():
    old = json.loads((ROOT / 'FINAL_SEQUENCE_RECOVERED_RESULT.json').read_text())
    inv = json.loads((ROOT / 'FINAL_SOURCE_INVENTORY.json').read_text())
    assert old['status'] == 'HOLD_FAILED_RECOVERY_PHASE' and len(old['phases']) == 20
    assert [(p['kind'], p['module']) for p in old['phases'][:19]] == [('build', m) for m in inv['build_order']]
    assert all(p['returncode'] == 0 for p in old['phases'][:19])
    assert old['phases'][19]['kind'] == 'kernel' and old['phases'][19]['module'] == 'SourceThetaBridge' and old['phases'][19]['returncode'] == 1
    failedpath = 'final-runs/20261018T002219Z-kernel-SourceThetaBridge-9ba2eb35/RECEIPT.json'
    failed = json.loads((ROOT / failedpath).read_text())
    assert failed['returncode'] == 1 and not failed['timed_out'] and failed['timeout_seconds'] == 420
    assert failed['objects_before'] == failed['objects_after'] and len(failed['objects_after']) == 19
    assert failed['source_before'] == failed['source_after'] and failed['integrity_error'] is None
    parent = (ROOT / failedpath).parent
    text = (parent / 'stdout.txt').read_text() + (parent / 'stderr.txt').read_text()
    assert "could not execute external process 'lean'" in text
    actual = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT / 'final-build').iterdir() if p.is_file()}
    assert actual == failed['objects_after']
    recovery = {'failed_sequence': record('FINAL_SEQUENCE_RECOVERED_RESULT.json'),
                'failed_receipt': record(failedpath), 'reason': 'PINNED_LEAN_CHILD_NOT_ON_PATH',
                'runner_sha256': record('run_kernel_recovery_phase.py')['sha256']}
    start = {'started_utc': now(), 'kernel_recovery': recovery,
             'inventory_sha256': record('FINAL_SOURCE_INVENTORY.json')['sha256'],
             'objects_before': actual, 'driver_sha256': record('run_kernel_recovery_sequence.py')['sha256']}
    with (ROOT / 'FINAL_KERNEL_RECOVERY_START.json').open('x') as f:
        json.dump(start, f, indent=2); f.write('\n')
    report = {'started_utc': old['started_utc'], 'source_inventory_sha256': old['source_inventory_sha256'],
              'phases': old['phases'][:19], 'recovery': old['recovery'], 'kernel_recovery': recovery,
              'status': 'KERNEL_RECOVERY_RUNNING', 'scientific_effect': 'NONE'}
    for module in inv['new_modules']:
        started = now()
        code = subprocess.run([sys.executable, '-B', str(ROOT / 'run_kernel_recovery_phase.py'), 'kernel', module], cwd=ROOT).returncode
        report['phases'].append({'kind': 'kernel', 'module': module, 'started_utc': started,
                                 'ended_utc': now(), 'returncode': code})
        (ROOT / 'FINAL_KERNEL_RECOVERY_PROGRESS.json').write_text(json.dumps(report, indent=2) + '\n')
        if code != 0:
            report.update(status='HOLD_FAILED_KERNEL_RECOVERY_PHASE', ended_utc=now())
            break
    else:
        report.update(status='PASS_LOCAL_SOURCE_BUILD_AND_STANDARD_KERNEL_REPLAY', ended_utc=now())
    with (ROOT / 'FINAL_SEQUENCE_TERMINAL_RESULT.json').open('x') as f:
        json.dump(report, f, indent=2); f.write('\n')
    print(json.dumps({'stage': 'KERNEL_RECOVERY_FINISHED', 'status': report['status'], 'phases': len(report['phases'])}), flush=True)
    return 0 if report['status'].startswith('PASS_') else 1


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Python optimization is not supported')
    raise SystemExit(main())
