#!/usr/bin/env python3
import pathlib,subprocess,datetime,time,json,hashlib,sys
B=pathlib.Path('/workspace/scratch/actual-source-quotient-saddle-collar-construct')
P=pathlib.Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
O=B/'documentary-outer/final-package-001';O.mkdir(parents=True,exist_ok=True)
me=pathlib.Path(__file__);data=me.read_bytes();st=me.stat()
ident={'path':str(me),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'identity_origin':'FIRST new prospective outer-driver payload identity, seeded before worker capture'}
cache=json.loads((B/'OWN_ID_CACHE.json').read_text());cache[str(me)]={'stamp':[st.st_size,st.st_mtime_ns],'identity':ident};(B/'OWN_ID_CACHE.json').write_text(json.dumps(cache,indent=2)+'\n')
cmd=['python3',str(B/'record_run.py'),'documentary-final-package-001','python3',str(B/'freeze_documents.py')]
r={'command':cmd,'cwd':str(P),'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'driver_identity':ident,'stdout_path':str(O/'stdout.log'),'stderr_path':str(O/'stderr.log'),'driver_entry_stdout_path':str(O/'driver.stdout.log'),'driver_entry_stderr_path':str(O/'driver.stderr.log')}
(O/'OUTER_INTENT.json').write_text(json.dumps(r,indent=2)+'\n');start=time.monotonic()
with open(O/'stdout.log','wb') as out,open(O/'stderr.log','wb') as err: code=subprocess.run(cmd,cwd=P,stdout=out,stderr=err).returncode
r.update({'exit_code':code,'ended_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-start})
for k in ['stdout','stderr']:
 p=O/(k+'.log');d=p.read_bytes();r[k]={'path':str(p),'bytes':len(d),'sha256':hashlib.sha256(d).hexdigest(),'identity_origin':'FIRST new actual completed outer stream identity'}
(O/'OUTER_RECEIPT.json').write_text(json.dumps(r,indent=2)+'\n')
sys.exit(code)
