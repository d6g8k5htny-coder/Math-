import hashlib,json,subprocess,sys,time
from pathlib import Path
root=Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
out=Path('/workspace/scratch/source-curvature-implementation')
label,source,*args=sys.argv[1:]
source=Path(source);production=root/'SourceCurvatureDecomposition.lean'
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
before=digest(source);pb=digest(production)
(out/(label+'.source.lean')).write_bytes(source.read_bytes())
cmd=['/home/agent/.elan/bin/lake','env','lean','-DwarningAsError=true',*args,str(source)]
start=time.time();pr=subprocess.run(cmd,cwd=root,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
log=out/(label+'.log');log.write_bytes(pr.stdout)
record={'command':cmd,'cwd':str(root),'exit_code':pr.returncode,'source':str(source),
 'source_sha256_before':before,'source_sha256_after':digest(source),
 'production_source_sha256_before':pb,'production_source_sha256_after':digest(production),
 'log_sha256':digest(log),'elapsed_seconds':time.time()-start}
(out/(label+'.json')).write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record));print(pr.stdout.decode(),end='');sys.exit(pr.returncode)
