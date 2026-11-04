from pathlib import Path
import json
import shutil
import subprocess
import time
from datetime import datetime, timezone

root = Path('/workspace/scratch/actual-fold-chart-jets')
src = root / 'ActualFoldChartJets.lean'
runs = root / 'runs'
number = len(list(runs.iterdir())) + 1
run = runs / f'{number:03d}'
run.mkdir()
snapshot = run / src.name
shutil.copy2(src, snapshot)
cmd = ['lake', 'env', 'lean', '--root=' + str(run), '-DwarningAsError=true', '-o',
       str(run / 'ActualFoldChartJets.olean'), str(snapshot)]
started = datetime.now(timezone.utc).isoformat()
start = time.perf_counter()
with (run / 'stdout.log').open('w') as out, (run / 'stderr.log').open('w') as err:
    result = subprocess.run(cmd, cwd='/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025',
                            stdout=out, stderr=err)
elapsed = time.perf_counter() - start
meta = {'command': cmd, 'cwd': '/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025',
        'started_utc': started, 'elapsed_seconds': elapsed, 'exit_code': result.returncode}
(run / 'meta.json').write_text(json.dumps(meta, indent=2) + '\n')
print(json.dumps(meta, indent=2))
print((run / 'stdout.log').read_text())
print((run / 'stderr.log').read_text())
