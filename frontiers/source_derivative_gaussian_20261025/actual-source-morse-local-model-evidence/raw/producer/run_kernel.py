"""Exactly ONE final owned-module kernel invocation after freeze/inventory."""
import datetime
import json
import subprocess
from pathlib import Path
from bind_owned import bind

TASK = Path('/workspace/scratch/actual-source-morse-local-model-construct')
PACKET = Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
SOURCE = PACKET / 'SourceActualMorseLocalModel.lean'
FREEZE = TASK / 'FROZEN_SOURCE.json'
if not FREEZE.exists():
    raise SystemExit('Final source freeze required before the ONE kernel.')
guard = TASK / 'EXACTLY_ONE_KERNEL_STARTED.json'
with guard.open('x') as stream:
    json.dump({'start_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'module': 'SourceActualMorseLocalModel', 'invocation_number': 1}, stream)
run = TASK / 'runs' / 'kernel-001'
run.mkdir(parents=True, exist_ok=False)
now = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
source_identity = bind(SOURCE, 'owned_production_source')
object_identity = bind(TASK / 'objects' / 'SourceActualMorseLocalModel.olean', 'owned_production_object')
harness_identity = bind(Path(__file__), 'owned_one_kernel_harness')
command = ['lake', 'env', 'sh', '-c',
           'LEAN_PATH=' + str(TASK / 'objects') + ':$LEAN_PATH exec leanchecker SourceActualMorseLocalModel']
record = {'label': 'kernel-001', 'start_utc': now(), 'cwd': str(PACKET), 'command': command,
          'source_identity': source_identity, 'object_identity': object_identity,
          'harness_identity': harness_identity, 'invocation_number': 1}
(run / 'RECORD.json').write_text(json.dumps(record, indent=2) + '\n')
with (run / 'stdout.txt').open('wb') as out, (run / 'stderr.txt').open('wb') as err:
    result = subprocess.run(command, cwd=PACKET, stdout=out, stderr=err, check=False)
record.update(end_utc=now(), exit_code=result.returncode)
(run / 'RECORD.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record, indent=2))
print('STDOUT:\n' + (run / 'stdout.txt').read_text())
print('STDERR:\n' + (run / 'stderr.txt').read_text())
raise SystemExit(result.returncode)
