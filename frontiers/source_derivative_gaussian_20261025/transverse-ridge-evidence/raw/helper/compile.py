from pathlib import Path
import datetime, hashlib, json, os, shutil, subprocess, sys
base=Path('/workspace/scratch/transverse-ridge-jets')
packet=Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
src=base / (sys.argv[1] if len(sys.argv)>1 else 'TransverseRidgeJets.lean')
n=len(list((base/'runs').glob('run-*')))+1
run=base/'runs'/f'run-{n:03d}'
run.mkdir()
snapshot=run/src.name
shutil.copy2(src,snapshot)
out=base/'build'/src.with_suffix('.olean').name
cmd=['lake','env','bash','-c','export LEAN_PATH="$1:$LEAN_PATH"; printenv LEAN_PATH; exec lean -R "$4" -o "$2" "$3"','_ ',str(base/'build'),str(out),str(src),str(base)]
start=datetime.datetime.now(datetime.timezone.utc)
p=subprocess.run(cmd,cwd=packet,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
end=datetime.datetime.now(datetime.timezone.utc)
(run/'stdout.log').write_text(p.stdout)
record={'command_argv':cmd,'cwd':str(packet),'source':str(src),'snapshot':str(snapshot),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'output':str(out),'start_utc':start.isoformat(),'end_utc':end.isoformat(),'seconds':(end-start).total_seconds(),'exit_code':p.returncode,'purpose':'Elaborate new helper source only; unchanged completed 31-module/25-input evidence reused.'}
if p.returncode==0: record['artifact_sha256']=hashlib.sha256(out.read_bytes()).hexdigest()
(run/'record.json').write_text(json.dumps(record,indent=2)+'\n')
print(f'RUN {n:03d} exit={p.returncode} seconds={record["seconds"]}')
print(p.stdout)
sys.exit(p.returncode)
