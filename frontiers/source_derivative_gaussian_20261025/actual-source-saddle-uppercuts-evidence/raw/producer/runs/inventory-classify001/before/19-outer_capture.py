import datetime,json,pathlib,subprocess,sys,time
BASE=pathlib.Path('/workspace/scratch/actual-source-saddle-uppercuts-construct')
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
label=sys.argv[1]; dest=BASE/'outer'/label
cmd=[sys.executable,str(BASE/'runner/record_run.py'),*sys.argv[1:]]
start=utc(); tick=time.monotonic()
with (dest/'outer.stdout.log').open('wb') as out,(dest/'outer.stderr.log').open('wb') as err:
    p=subprocess.run(cmd,cwd=BASE,stdout=out,stderr=err)
record={'label':label,'command_argv':cmd,'cwd':str(BASE),'start_utc':start,'end_utc':utc(),
 'elapsed_seconds':time.monotonic()-tick,'exit_code':p.returncode,
 'stdout':str(dest/'outer.stdout.log'),'stderr':str(dest/'outer.stderr.log')}
(dest/'outer.receipt.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record))
raise SystemExit(p.returncode)
