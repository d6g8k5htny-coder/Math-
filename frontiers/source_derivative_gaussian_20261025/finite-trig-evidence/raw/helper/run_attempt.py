from pathlib import Path
from datetime import datetime, timezone
import json, subprocess, sys, time
root = Path('/workspace/scratch/finite-trig-source-conversion')
name = sys.argv[1]
run = root / 'raw' / name
src = run / 'AtomConversion.lean'
obj = run / 'AtomConversion.olean'
cmd = ['lake', 'env', 'lean', '-DwarningAsError=true', '--root=' + str(run), str(src), '-o', str(obj)]
record = {'attempt': name, 'cwd':'/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025', 'command':cmd, 'start_utc':datetime.now(timezone.utc).isoformat()}
(run / 'command.json').write_text(json.dumps(record, indent=2)+'\n')
t0=time.monotonic()
with (run/'stdout.log').open('wb') as out, (run/'stderr.log').open('wb') as err:
    result=subprocess.run(cmd, cwd=record['cwd'], stdout=out, stderr=err)
record.update(end_utc=datetime.now(timezone.utc).isoformat(), elapsed_seconds=time.monotonic()-t0, exit_code=result.returncode)
(run/'result.json').write_text(json.dumps(record, indent=2)+'\n')
print(json.dumps(record))
print((run/'stdout.log').read_text())
print((run/'stderr.log').read_text())
sys.exit(result.returncode)
