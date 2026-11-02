import datetime,json,pathlib,subprocess,sys,time
B=pathlib.Path('/workspace/scratch/actual-source-regular-local-collar-publication')
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
cmd=[sys.executable,str(B/'outer66.py')];start=utc();tick=time.monotonic()
with (B/'ENTRY66.stdout.log').open('wb') as out,(B/'ENTRY66.stderr.log').open('wb') as err:
    p=subprocess.run(cmd,cwd=B,stdout=out,stderr=err)
r={'command_argv':cmd,'cwd':str(B),'start_utc':start,'end_utc':utc(),'elapsed_seconds':time.monotonic()-tick,'exit_code':p.returncode,'stdout':str(B/'ENTRY66.stdout.log'),'stderr':str(B/'ENTRY66.stderr.log'),'scope':'Entry process starts here; caller tool external UTC uninstrumented; original caller command retained, no invented timing'}
(B/'ENTRY66.receipt.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r));raise SystemExit(p.returncode)
