from pathlib import Path
import hashlib,json,subprocess,time,sys
out=Path('/workspace/scratch/smooth-parameter-production')
root=Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
source=root/'SourceSmoothParameterSpace.lean'
artifact=root/'.lake/build/lib/lean/SourceSmoothParameterSpace.olean'
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
label=sys.argv[1];sb=digest(source);ab=digest(artifact)
cmd=['/home/agent/.elan/bin/lake','env','leanchecker','SourceSmoothParameterSpace']
start=time.time();pr=subprocess.run(cmd,cwd=root,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
log=out/(label+'.log');log.write_bytes(pr.stdout)
r={'command':cmd,'cwd':str(root),'exit_code':pr.returncode,'production_source_sha256_before':sb,'production_source_sha256_after':digest(source),'olean_sha256_before':ab,'olean_sha256_after':digest(artifact),'log_sha256':digest(log),'elapsed_seconds':time.time()-start,'scope':'ONLY new SourceSmoothParameterSpace; dependencies reused without rechecks'}
(out/(label+'.json')).write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r));print(pr.stdout.decode(),end='');sys.exit(pr.returncode)
