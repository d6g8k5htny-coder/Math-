import hashlib,json,subprocess,time
from pathlib import Path
root=Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
out=Path('/workspace/scratch/source-smooth-topology')
source=root/'SourceSmoothTopology.lean'
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
before=digest(source)
cmd=['/home/agent/.elan/bin/lake','env','leanchecker','SourceSmoothTopology']
start=time.time();pr=subprocess.run(cmd,cwd=root,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
log=out/'09-kernel-replay.log';log.write_bytes(pr.stdout)
record={'command':cmd,'cwd':str(root),'exit_code':pr.returncode,
 'source_sha256_before':before,'source_sha256_after':digest(source),
 'log_sha256':digest(log),'elapsed_seconds':time.time()-start}
(out/'09-kernel-replay.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record));print(pr.stdout.decode(),end='');raise SystemExit(pr.returncode)
