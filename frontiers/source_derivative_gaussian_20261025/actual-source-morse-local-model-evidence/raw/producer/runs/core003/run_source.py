#!/usr/bin/env python3
"""Owned60 execution custody. No dependency hashes or support builds."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

TASK = Path('/workspace/scratch/actual-source-morse-local-model-construct')
PACKET = Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
SOURCE = PACKET / 'SourceActualMorseLocalModel.lean'
OBJECTS = TASK / 'objects'
IDENTITIES = TASK / 'ARTIFACT_IDENTITIES.json'

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def bind(path, role):
    data = path.read_bytes()
    store = json.loads(IDENTITIES.read_text()) if IDENTITIES.exists() else {'artifacts': []}
    for item in store['artifacts']:
        snapshot = Path(item['snapshot'])
        if item['role'] == role and snapshot.exists() and snapshot.read_bytes() == data:
            return dict(item, reused_identity=True)
    number = len(store['artifacts']) + 1
    snapshot = TASK / 'identities' / f'{number:04d}-{path.name}'
    snapshot.parent.mkdir(parents=True, exist_ok=True)
    snapshot.write_bytes(data)
    item = {'role': role, 'path': str(path), 'snapshot': str(snapshot),
            'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
            'first_bound_utc': now(), 'new_sha256_operations': 1}
    store['artifacts'].append(item)
    IDENTITIES.write_text(json.dumps(store, indent=2) + '\n')
    return dict(item, reused_identity=False)

label = sys.argv[1]
run = TASK / 'runs' / label
run.mkdir(parents=True, exist_ok=False)
OBJECTS.mkdir(parents=True, exist_ok=True)
source_identity = bind(SOURCE, 'owned_production_source')
harness_identity = bind(Path(__file__), 'owned_source_execution_harness')
shutil.copyfile(SOURCE, run / SOURCE.name)
shutil.copyfile(__file__, run / 'run_source.py')
command = ['lake', 'env', 'lean', '-DwarningAsError=true',
           '-o', str(OBJECTS / 'SourceActualMorseLocalModel.olean'), SOURCE.name]
record = {'label': label, 'cwd': str(PACKET), 'command': command,
          'start_utc': now(), 'source_identity': source_identity,
          'harness_identity': harness_identity,
          'scope': 'new owned60 source only; no helper execution or support rebuild'}
(run / 'RECORD.json').write_text(json.dumps(record, indent=2) + '\n')
with (run / 'stdout.txt').open('wb') as out, (run / 'stderr.txt').open('wb') as err:
    process = subprocess.run(command, cwd=PACKET, stdout=out, stderr=err, check=False)
record['exit_code'] = process.returncode
record['end_utc'] = now()
object_path = OBJECTS / 'SourceActualMorseLocalModel.olean'
if process.returncode == 0 and object_path.exists():
    record['object_identity'] = bind(object_path, 'owned_production_object')
(run / 'RECORD.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record, indent=2))
print('STDOUT:')
print((run / 'stdout.txt').read_text())
print('STDERR:')
print((run / 'stderr.txt').read_text())
sys.exit(process.returncode)
