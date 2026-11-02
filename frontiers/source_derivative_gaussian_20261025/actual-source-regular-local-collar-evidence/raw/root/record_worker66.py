import datetime,hashlib,json,pathlib,shutil,subprocess,sys,time
B=pathlib.Path('/workspace/scratch/actual-source-regular-local-collar-publication')
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
snap=B/'runtime-before-first-worker';snap.mkdir(exist_ok=False)
rows=[]
for p in sorted(B.glob('*.py')):
    data=p.read_bytes();row={'path':str(p),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'first_observed_utc':utc(),'origin':'NEW runtime script FIRST ID calculatedONCE'}
    dst=snap/p.name;dst.write_bytes(data);row['immutable_snapshot']=str(dst);row['snapshot_identity']='Exact bytecopy IDreused, no snapshot rehash';rows.append(row)
(B/'RUNTIME66_FIRST_IDS.json').write_text(json.dumps(rows,indent=2)+'\n')
cmd=[sys.executable,str(B/'adopt66_worker.py')];start=utc();tick=time.monotonic()
with (B/'WORKER66.stdout.log').open('wb') as out,(B/'WORKER66.stderr.log').open('wb') as err:
    result=subprocess.run(cmd,cwd=B,stdout=out,stderr=err)
r={'command_argv':cmd,'cwd':str(B),'start_utc':start,'end_utc':utc(),'elapsed_seconds':time.monotonic()-tick,'exit_code':result.returncode,'stdout':str(B/'WORKER66.stdout.log'),'stderr':str(B/'WORKER66.stderr.log'),'scope':'Documentary proper66adoption only; no proof/source/Lean/mathcheck'}
(B/'WORKER66.receipt.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r));raise SystemExit(result.returncode)
