import datetime, hashlib, json, pathlib, subprocess, sys, time
base=pathlib.Path('/workspace/scratch/actual-fold-candidate-construct')
repo=pathlib.Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
kind=sys.argv[1]
runs=base/'runs'; runs.mkdir(exist_ok=True)
i=1
while (runs/f'{kind}-{i:03}').exists(): i+=1
out=runs/f'{kind}-{i:03}'; out.mkdir()
src=repo/'SourceActualFoldCandidate.lean'
(out/src.name).write_bytes(src.read_bytes())
cmd=['lake','env','lean','-DwarningAsError=true',str(src),'-o',str(out/'SourceActualFoldCandidate.olean')]
start=datetime.datetime.now(datetime.timezone.utc).isoformat(); t=time.monotonic()
p=subprocess.run(cmd,cwd=repo,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
(out/'output.log').write_bytes(p.stdout)
record={'kind':kind,'run':out.name,'start':start,'end':datetime.datetime.now(datetime.timezone.utc).isoformat(),'seconds':time.monotonic()-t,'command':cmd,'cwd':str(repo),'exit':p.returncode,'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest()}
(out/'record.json').write_text(json.dumps(record,indent=2)+'\n')
with (base/'RAW_LEDGER.jsonl').open('a') as f:f.write(json.dumps(record)+'\n')
print(json.dumps(record)); print(p.stdout.decode(),end='')
sys.exit(p.returncode)
