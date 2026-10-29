import os, pathlib, subprocess, time, json, sys, hashlib, datetime
p=pathlib.Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
s=pathlib.Path('/workspace/scratch/actual-fold-clearance-inputs')
b=s/'build'; b.mkdir(exist_ok=True)
module=sys.argv[1]; mode=sys.argv[2]
prior=list(s.glob(module+'-'+mode+'-*.json')); n=len(prior)+1; stem=f'{module}-{mode}-{n:02d}'
path_command=['lake','env','printenv','LEAN_PATH']
base_path=subprocess.check_output(path_command,cwd=p,text=True).strip()
env=os.environ.copy(); env['LEAN_PATH']=str(b)+':'+base_path
lean='/home/agent/.elan/toolchains/leanprover--lean4---v4.34.1/bin/lean'
source=p/'inputs/elder'/f'{module}.lean'
command=[lean]+(['-DwarningAsError=true'] if mode=='strict' else [])+['-o',str(b/f'{module}.olean'),'-i',str(b/f'{module}.ilean'),str(source)]
start=time.monotonic(); began=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (s/(stem+'.stdout')).open('w') as out, (s/(stem+'.stderr')).open('w') as err:
 result=subprocess.run(command,cwd=p,env=env,stdout=out,stderr=err)
record={'module':module,'mode':mode,'command':command,'cwd':str(p),'LEAN_PATH':env['LEAN_PATH'],'started_utc':began,'elapsed_seconds':time.monotonic()-start,'exit_code':result.returncode,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'stdout':str(s/(stem+'.stdout')),'stderr':str(s/(stem+'.stderr'))}
(s/(stem+'.json')).write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2)); print((s/(stem+'.stdout')).read_text()); print((s/(stem+'.stderr')).read_text())
sys.exit(result.returncode)
