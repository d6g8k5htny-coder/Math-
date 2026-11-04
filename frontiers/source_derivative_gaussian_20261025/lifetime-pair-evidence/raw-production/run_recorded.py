from pathlib import Path
import subprocess,sys,json,hashlib,datetime
out=Path('/workspace/scratch/lifetime-pair-finiteness')
root=Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
name=sys.argv[1]
command=sys.argv[2:]
def digest(p):
 return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} if p.exists() else {'path':str(p),'absent':True}
paths=[root/'SourceLifetimePairFiniteness.lean',root/'inputs/Lifetime.lean',root/'inputs/SourceLifetimeGeometry.lean']
paths += [root/'.lake/build/lib/lean'/f'{n}.olean' for n in ['SourceLifetimePairFiniteness','Lifetime','SourceLifetimeGeometry']]
record={'command_argv':command,'cwd':str(root),'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'before':[digest(p) for p in paths]}
with (out/f'{name}.log').open('wb') as log:
 result=subprocess.run(command,cwd=root,stdout=log,stderr=subprocess.STDOUT)
record.update(exit_code=result.returncode,ended_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),after=[digest(p) for p in paths],log=digest(out/f'{name}.log'))
(out/f'{name}.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'name':name,'exit_code':result.returncode,'log':str(out/f'{name}.log')}))
sys.exit(result.returncode)
