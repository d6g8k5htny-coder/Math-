import json, hashlib, os, subprocess, time, datetime
from pathlib import Path
base=Path(__file__).resolve().parent
label=__import__('sys').argv[1]
rd=base/'runs'/label
rd.mkdir(exist_ok=False)
src=base/'RidgeSchur.lean'
obj=base/'build'/'RidgeSchur.olean'
def ident(p):
 return dict(path=str(p),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) if p.exists() else None
rd.joinpath('source.lean').write_bytes(src.read_bytes())
cmd=['/home/agent/.elan/bin/lake','env','lean','-R',str(base),'-DwarningAsError=true','-o',str(obj),'-i',str(base/'build'/'RidgeSchur.ilean'),str(src)]
start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.time()
before=ident(src)
r=subprocess.run(cmd,cwd='/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025',stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
rd.joinpath('output.log').write_bytes(r.stdout)
receipt=dict(label=label,command=cmd,cwd='/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025',started_utc=start,ended_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),elapsed_seconds=time.time()-t,exit_code=r.returncode,source=before,object=ident(obj) if r.returncode==0 else None,log=ident(rd/'output.log'))
rd.joinpath('receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(r.stdout.decode());print(json.dumps(receipt,indent=2))
raise SystemExit(r.returncode)
