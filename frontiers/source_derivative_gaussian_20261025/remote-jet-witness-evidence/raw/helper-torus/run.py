import datetime, hashlib, json, pathlib, subprocess, sys, time

base = pathlib.Path('/workspace/scratch/remote-jet-torus-separation')
repo = pathlib.Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
source = base / 'TorusSeparation.lean'
kind = 'strict'
runs = base / 'runs'
runs.mkdir(exist_ok=True)
number = 1
while (runs / f'{kind}-{number:03}').exists():
    number += 1
out = runs / f'{kind}-{number:03}'
out.mkdir()
snapshot = source.read_bytes()
(out / source.name).write_bytes(snapshot)
cmd = ['/home/agent/.elan/bin/lake', 'env', 'lean', '--root=' + str(base), '-DwarningAsError=true',
       str(source), '-o', str(out / 'TorusSeparation.olean')]
start = datetime.datetime.now(datetime.timezone.utc).isoformat()
tick = time.monotonic()
process = subprocess.run(cmd, cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
(out / 'stdout.log').write_bytes(process.stdout)
(out / 'stderr.log').write_bytes(process.stderr)
record = {'kind': kind, 'run': out.name, 'start': start,
          'end': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'seconds': time.monotonic() - tick, 'command': cmd, 'cwd': str(repo),
          'exit': process.returncode, 'source_bytes': len(snapshot),
          'source_sha256': hashlib.sha256(snapshot).hexdigest(),
          'scope': 'New helper source only; no old proof replay or standalone qualification'}
(out / 'record.json').write_text(json.dumps(record, indent=2) + '\n')
with (base / 'RAW_LEDGER.jsonl').open('a') as ledger:
    ledger.write(json.dumps(record) + '\n')
print(json.dumps(record))
print(process.stdout.decode(), end='')
print(process.stderr.decode(), end='', file=sys.stderr)
sys.exit(process.returncode)
