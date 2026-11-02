import argparse, datetime, hashlib, json, os, pathlib, shutil, subprocess, time

BASE = pathlib.Path('/workspace/scratch/actual-source-saddle-uppercuts-construct')
PROJECT = pathlib.Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def read_cache():
    p=BASE/'FIRST_ID_CACHE.json'
    return json.loads(p.read_text()) if p.exists() else {}
def identity(path,cache):
    p=pathlib.Path(path); key=str(p)
    if not p.is_file(): return None
    st=p.stat(); marker=[st.st_size,st.st_mtime_ns]
    old=cache.get(key)
    if old and old.get('marker')==marker: return old
    row={'path':key,'bytes':st.st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
         'marker':marker,'first_observed_utc':utc(),'origin':'new actual version identity, calculated once'}
    cache[key]=row
    return row
def copied_identity(src,dst,row,cache):
    shutil.copyfile(src,dst); st=pathlib.Path(dst).stat()
    cache[str(dst)]={**row,'path':str(dst),'marker':[st.st_size,st.st_mtime_ns],
                    'origin':'known byte-copy identity reused','copied_from':str(src)}

ap=argparse.ArgumentParser(); ap.add_argument('label'); ap.add_argument('kind');
ap.add_argument('command',nargs=argparse.REMAINDER); args=ap.parse_args()
cmd=args.command[1:] if args.command[:1]==['--'] else args.command
run=BASE/'runs'/args.label
run.mkdir(parents=True,exist_ok=False)
cache=read_cache()
paths=[BASE/'CONTEXT.md',*sorted((BASE/'runner').glob('*.py')),
       PROJECT/'SourceActualSaddleUppercuts.lean',
       BASE/'build/SourceActualSaddleUppercuts.olean',
       BASE/'SaddleUppercutsControls.lean',BASE/'build/SaddleUppercutsControls.olean']
paths+=sorted(BASE.glob('*.lean'))
paths=list(dict.fromkeys(paths))
before={}; snapshots={}
snap=run/'before'; snap.mkdir()
for i,p in enumerate(paths):
    row=identity(p,cache); before[str(p)]=row
    if row:
        dst=snap/(str(i)+'-'+p.name); copied_identity(p,dst,row,cache)
        snapshots[str(p)]=str(dst)
(BASE/'FIRST_ID_CACHE.json').write_text(json.dumps(cache,indent=2)+'\n')
started=utc(); tick=time.monotonic()
with (run/'stdout.log').open('wb') as out,(run/'stderr.log').open('wb') as err:
    proc=subprocess.run(cmd,cwd=PROJECT,stdout=out,stderr=err)
ended=utc(); elapsed=time.monotonic()-tick
cache=read_cache()
after={str(p):identity(p,cache) for p in paths}
streams={s:identity(run/s,cache) for s in ['stdout.log','stderr.log']}
receipt={'label':args.label,'scope_kind':args.kind,'command_argv':cmd,'cwd':str(PROJECT),
 'start_utc':started,'end_utc':ended,'elapsed_seconds':elapsed,'exit_code':proc.returncode,
 'before':before,'before_snapshots':snapshots,'after':after,'streams':streams,
 'worker_capture':'full original separate stdout/stderr, no truncation',
 'outer_capture_dir':str(BASE/'outer'/args.label)}
(run/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
(BASE/'FIRST_ID_CACHE.json').write_text(json.dumps(cache,indent=2)+'\n')
print(json.dumps({'label':args.label,'exit_code':proc.returncode,'receipt':str(run/'receipt.json')}))
raise SystemExit(proc.returncode)
