import datetime
import hashlib
import json
import os
import pathlib
import subprocess
import sys
import time

ROOT = pathlib.Path('/workspace/scratch/actual-h0-support-inputs')
PACKET = pathlib.Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
LEAN = '/home/agent/.elan/toolchains/leanprover--lean4---v4.34.1/bin/lean'

def identity(path):
    path = pathlib.Path(path)
    if not path.is_file():
        return None
    data = path.read_bytes()
    return {'path': str(path), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

module = sys.argv[1]
assert module in ['ClosedSuperlevel', 'OrdinaryH0', 'ElderInterval', 'ElderBridge']
number = len(list((ROOT / 'runs').glob(module + '-strict-*'))) + 1 if (ROOT / 'runs').exists() else 1
run = ROOT / 'runs' / f'{module}-strict-{number:03}'
run.mkdir(parents=True, exist_ok=False)
source = PACKET / 'inputs/elder' / f'{module}.lean'
snapshot = run / f'{module}.lean'
snapshot.write_bytes(source.read_bytes())
environment = json.loads((ROOT / 'environment.json').read_text())
env = os.environ.copy()
env['LEAN_PATH'] = str(ROOT / 'build') + ':' + environment['base_lean_path']
command = [LEAN, '-DwarningAsError=true', '-o', str(ROOT / 'build' / f'{module}.olean'),
    '-i', str(ROOT / 'build' / f'{module}.ilean'), str(source)]
record = {'label': run.name, 'module': module, 'reason': 'New narrow-import successor composition; no old proof/kernel/control/audit replay.',
    'cwd': str(PACKET), 'command': command, 'environment': {'LEAN_PATH': env['LEAN_PATH']},
    'environment_record': str(ROOT / 'environment.json'), 'source_before': identity(source),
    'source_snapshot': identity(snapshot), 'runner': identity(__file__),
    'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
start = time.monotonic()
with (run / 'stdout.log').open('w') as out, (run / 'stderr.log').open('w') as err:
    result = subprocess.run(command, cwd=PACKET, env=env, stdout=out, stderr=err)
record.update({'exit_code': result.returncode, 'elapsed_seconds': time.monotonic() - start,
    'ended_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'source_after': identity(source),
    'stdout': identity(run / 'stdout.log'), 'stderr': identity(run / 'stderr.log'),
    'olean': identity(ROOT / 'build' / f'{module}.olean'), 'ilean': identity(ROOT / 'build' / f'{module}.ilean')})
assert record['source_before'] == record['source_after']
(run / 'receipt.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record, indent=2))
print((run / 'stdout.log').read_text())
print((run / 'stderr.log').read_text())
sys.exit(result.returncode)
