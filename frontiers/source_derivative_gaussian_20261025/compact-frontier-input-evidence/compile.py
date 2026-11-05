import os, pathlib, subprocess, time, json, hashlib, datetime, sys
p=pathlib.Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
s=pathlib.Path('/workspace/scratch/reused-compact-frontier'); b=s/'build'
module='ReusedCompactFrontier'
source=p/'inputs/elder'/f'{module}.lean'
lean='/home/agent/.elan/toolchains/leanprover--lean4---v4.34.1/bin/lean'
records=[]
def observe(command,cwd):
 start=time.monotonic(); utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
 result=subprocess.run(command,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
 records.append({'command':command,'cwd':str(cwd),'started_utc':utc,'ended_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-start,'exit_code':result.returncode,'stdout':result.stdout,'stderr':result.stderr})
 if result.returncode: raise RuntimeError(result.stderr)
 return result.stdout.strip()
base_path=observe(['lake','env','printenv','LEAN_PATH'],p)
version=observe([lean,'--version'],p)
mathlib=(p/'.lake/packages/mathlib').resolve()
mathlib_head=observe(['git','rev-parse','HEAD'],mathlib)
assert version=='Lean (version 4.34.1, x86_64-unknown-linux-gnu, commit 5045d0056413266e57c625dcd7c365b10e377c52, Release)'
assert mathlib_head=='d13f23b723b8a846827a245b89c10fc7d3f11612'
env=os.environ.copy(); env['LEAN_PATH']=str(b)+':'+base_path
command=[lean,'-DwarningAsError=true','-o',str(b/f'{module}.olean'),'-i',str(b/f'{module}.ilean'),str(source)]
start=time.monotonic(); utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (s/'strict-01.stdout').open('w') as out,(s/'strict-01.stderr').open('w') as err:
 result=subprocess.run(command,cwd=p,env=env,stdout=out,stderr=err)
record={'command':command,'cwd':str(p),'LEAN_PATH':env['LEAN_PATH'],'started_utc':utc,'ended_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-start,'exit_code':result.returncode,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'stdout':str(s/'strict-01.stdout'),'stderr':str(s/'strict-01.stderr')}
(s/'strict-01.json').write_text(json.dumps(record,indent=2)+'\n')
(s/'environment.json').write_text(json.dumps({'lean_version':version,'mathlib_path':str(mathlib),'mathlib_head':mathlib_head,'observations':records},indent=2)+'\n')
print(json.dumps(record,indent=2)); print((s/'strict-01.stdout').read_text()); print((s/'strict-01.stderr').read_text())
if result.returncode: sys.exit(result.returncode)
artifacts={}
for suffix in ['olean','ilean']:
 path=b/f'{module}.{suffix}'
 artifacts[str(path)]={'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
(s/'ARTIFACTS.json').write_text(json.dumps(artifacts,indent=2)+'\n')
print(json.dumps(artifacts,indent=2))
