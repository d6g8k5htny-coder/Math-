"""Resume only the unresolved audit and unstarted kernels; preserve first attempt."""
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
    old = json.loads((ROOT / 'FINAL_SEQUENCE_RESULT.json').read_text())
    inv = json.loads((ROOT / 'FINAL_SOURCE_INVENTORY.json').read_text())
    assert old['status'] == 'HOLD_FAILED_PHASE' and len(old['phases']) == 19
    assert [(p['kind'], p['module']) for p in old['phases']] == [('build', m) for m in inv['build_order']]
    assert all(p['returncode'] == 0 for p in old['phases'][:18]) and old['phases'][18]['returncode'] == 1
    failedpath = 'final-runs/20261018T000515Z-build-SourceLifetimeAxiomAudit-93b1c912/RECEIPT.json'
    failed = json.loads((ROOT / failedpath).read_text())
    assert failed['returncode'] == -15 and failed['timed_out'] and failed['timeout_seconds'] == 420
    assert failed['objects_before'] == failed['objects_after'] and len(failed['objects_after']) == 18
    assert failed['source_before'] == failed['source_after'] and failed['integrity_error'] is None
    assert not (ROOT / 'final-build/SourceLifetimeAxiomAudit.olean').exists()
    actual = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT / 'final-build').iterdir() if p.is_file()}
    assert actual == failed['objects_after']
    recovery = {'failed_sequence': record('FINAL_SEQUENCE_RESULT.json'),
                'failed_receipt': record(failedpath),
                'reason': 'OBSERVED_420_SECOND_AUDIT_TIMEOUT',
                'recovered_runner_sha256': record('run_recovery_phase.py')['sha256']}
    start = {'started_utc': now(), 'recovery': recovery,
             'inventory_sha256': record('FINAL_SOURCE_INVENTORY.json')['sha256'],
             'objects_before': actual, 'driver_sha256': record('run_recovery_sequence.py')['sha256']}
    with (ROOT / 'FINAL_RECOVERY_START.json').open('x') as f:
        json.dump(start, f, indent=2); f.write('\n')
    report = {'started_utc': old['started_utc'], 'source_inventory_sha256': old['source_inventory_sha256'],
              'phases': old['phases'][:18], 'recovery': recovery,
              'status': 'RECOVERY_RUNNING', 'scientific_effect': 'NONE'}
    phases = [('build', 'SourceLifetimeAxiomAudit')] + [('kernel', m) for m in inv['new_modules']]
    for kind, module in phases:
        runner = 'run_recovery_phase.py' if kind == 'build' else 'run_final_phase.py'
        started = now()
        code = subprocess.run([sys.executable, '-B', str(ROOT / runner), kind, module], cwd=ROOT).returncode
        report['phases'].append({'kind': kind, 'module': module, 'started_utc': started,
                                 'ended_utc': now(), 'returncode': code})
        (ROOT / 'FINAL_RECOVERY_PROGRESS.json').write_text(json.dumps(report, indent=2) + '\n')
        if code != 0:
            report.update(status='HOLD_FAILED_RECOVERY_PHASE', ended_utc=now())
            break
    else:
        report.update(status='PASS_LOCAL_SOURCE_BUILD_AND_STANDARD_KERNEL_REPLAY', ended_utc=now())
    with (ROOT / 'FINAL_SEQUENCE_RECOVERED_RESULT.json').open('x') as f:
        json.dump(report, f, indent=2); f.write('\n')
    print(json.dumps({'stage': 'RECOVERY_FINISHED', 'status': report['status'], 'phases': len(report['phases'])}), flush=True)
    return 0 if report['status'].startswith('PASS_') else 1


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Python optimization is not supported')
    raise SystemExit(main())
