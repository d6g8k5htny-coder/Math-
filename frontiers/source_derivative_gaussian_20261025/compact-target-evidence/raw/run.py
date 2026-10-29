import hashlib, json, pathlib, subprocess, sys, time, datetime
root = pathlib.Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
out = pathlib.Path('/workspace/scratch/compact-target-moments')
label = sys.argv[1]
cmd = sys.argv[2:]
src = root / 'SourceCompactTargetMoments.lean'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
snap = out / (label + '.source.lean')
if src.exists(): snap.write_bytes(src.read_bytes())
inputs = {}
for i, arg in enumerate(cmd):
    path = pathlib.Path(arg)
    if path.suffix == '.lean':
        if not path.is_absolute(): path = root / path
        if path.exists():
            input_snap = out / (label + '.input-' + str(i) + '.lean')
            input_snap.write_bytes(path.read_bytes())
            inputs[str(path)] = dict(snapshot=str(input_snap), sha256=sha(input_snap))
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
t = time.time()
p = subprocess.run(cmd, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
log = out / (label + '.log')
log.write_bytes(p.stdout)
objects = {str(x):sha(x) for x in (root/'.lake/build/lib/lean').glob('SourceCompactTargetMoments.*') if x.is_file()}
record = dict(command=cmd, cwd=str(root), started_utc=started, elapsed_seconds=time.time()-t,
              exit_code=p.returncode, source=str(src), snapshot=str(snap),
              source_sha256_before=sha(snap) if snap.exists() else None,
              source_sha256_after=sha(src) if src.exists() else None,
              log_sha256=sha(log), object_sha256=objects, inputs=inputs)
(out/(label+'.json')).write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record))
print(p.stdout.decode(),end='')
sys.exit(p.returncode)
