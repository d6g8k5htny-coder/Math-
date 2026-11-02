from pathlib import Path
import subprocess,hashlib,json,time,sys
out=Path('/workspace/scratch/smooth-parameter-production')
root=Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
production=root/'SourceSmoothParameterSpace.lean'
label,kind,source,*args=sys.argv[1:];source=Path(source)
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
before=digest(source);pb=digest(production);(out/(label+'.source.lean')).write_bytes(source.read_bytes())
artifact=root/'.lake/build/lib/lean/SourceSmoothParameterSpace.olean'
ab=digest(artifact) if artifact.exists() else None
cmd=['/home/agent/.elan/bin/lake','env',kind,'-DwarningAsError=true',*args,str(source)]
start=time.time();pr=subprocess.run(cmd,cwd=root,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
log=out/(label+'.log');log.write_bytes(pr.stdout)
r={'command':cmd,'cwd':str(root),'exit_code':pr.returncode,'source':str(source),
 'source_sha256_before':before,'source_sha256_after':digest(source),
 'production_source_sha256_before':pb,'production_source_sha256_after':digest(production),
 'olean_sha256_before':ab,'olean_sha256_after':digest(artifact) if artifact.exists() else None,
 'log_sha256':digest(log),'elapsed_seconds':time.time()-start,
 'scope':'ONLY new SourceSmoothParameterSpace module; completed dependencies reused without rechecks'}
(out/(label+'.json')).write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r));print(pr.stdout.decode(),end='');sys.exit(pr.returncode)
