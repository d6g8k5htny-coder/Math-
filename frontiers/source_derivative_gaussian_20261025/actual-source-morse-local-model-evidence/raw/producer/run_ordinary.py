"""New own ordinary Lean harnesses, importing only the qualified own object."""
import datetime
import difflib
import json
import shutil
import subprocess
from pathlib import Path
import sys
from bind_owned import bind

TASK = Path('/workspace/scratch/actual-source-morse-local-model-construct')
PACKET = Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
label, source_name = sys.argv[1:]
source = Path(source_name)
run = TASK / 'runs' / label
run.mkdir(parents=True, exist_ok=False)
objects = TASK / 'objects'
output = objects / (source.stem + '.olean')
now = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
binding = bind(source, 'owned_ordinary_source_' + source.stem)
harness = bind(Path(__file__), 'owned_ordinary_execution_harness')
production = bind(objects / 'SourceActualMorseLocalModel.olean', 'owned_production_object')
controls_object = None
if source.stem == 'OmittedTaylorWeightFalse':
    positive_record = json.loads((TASK / 'runs' / 'controls-003' / 'RECORD.json').read_text())
    if positive_record['exit_code'] != 0:
        raise SystemExit('Actual independent Controls counterproof must pass first.')
    controls_object = bind(objects / 'MorseLocalModelControls.olean',
                           'owned_ordinary_object_MorseLocalModelControls')
    if controls_object['sha256'] != positive_record['object_identity']['sha256']:
        raise SystemExit('Qualified ordinary Controls object changed.')
    with (TASK / 'EXACTLY_ONE_FALSE_STARTED.json').open('x') as stream:
        json.dump({'start_utc': now(), 'label': label,
                   'passed_counterproof': str(TASK / 'runs' / 'controls-003' / 'RECORD.json'),
                   'controls_object_identity': controls_object, 'invocation_number': 1}, stream)
shutil.copyfile(source, run / source.name)
shutil.copyfile(__file__, run / Path(__file__).name)
original = TASK / 'controls-originals' / 'CONTROLS_SECTION.lean.txt'
if source.stem == 'MorseLocalModelControls' and original.exists():
    body = source.read_text().split('/- Complete ordinary Controls-only', 1)[1]
    actual = '/- Complete ordinary Controls-only' + body
    patch = ''.join(difflib.unified_diff(original.read_text().splitlines(True),
        actual.splitlines(True), fromfile='frozen-ordinary-original', tofile='actual-ordinary-controls'))
    (run / 'CONTROLS_FULL_AMENDMENTS.patch').write_text(patch)
inner = ('import os,subprocess,sys; '
         'os.environ["LEAN_PATH"]=sys.argv[1]+os.pathsep+os.environ.get("LEAN_PATH",""); '
         'sys.exit(subprocess.run(["lean","-DwarningAsError=true","--root="+sys.argv[2],'
         '"-o",sys.argv[3],sys.argv[4]],check=False).returncode)')
command = ['lake', 'env', 'python', '-c', inner, str(objects), str(source.parent), str(output), str(source)]
record = {'label': label, 'cwd': str(PACKET), 'command': command, 'start_utc': now(),
          'source_identity': binding, 'harness_identity': harness,
          'production_object_identity': production,
          'coverage': 'ordinary source only, separate from production kernel'}
if controls_object is not None:
    record['controls_object_identity'] = controls_object
    record['expected_failure'] = 'ONE false omitted-weight entry=1; actual counterproof gives2'
(run / 'RECORD.json').write_text(json.dumps(record, indent=2) + '\n')
with (run / 'stdout.txt').open('wb') as out, (run / 'stderr.txt').open('wb') as err:
    result = subprocess.run(command, cwd=PACKET, stdout=out, stderr=err, check=False)
record.update(exit_code=result.returncode, end_utc=now())
if result.returncode == 0 and output.exists():
    record['object_identity'] = bind(output, 'owned_ordinary_object_' + source.stem)
(run / 'RECORD.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record, indent=2))
print('STDOUT:\n' + (run / 'stdout.txt').read_text())
print('STDERR:\n' + (run / 'stderr.txt').read_text())
sys.exit(result.returncode)
