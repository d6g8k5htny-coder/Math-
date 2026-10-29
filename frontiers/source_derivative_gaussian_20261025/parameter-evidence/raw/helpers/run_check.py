from pathlib import Path
import subprocess,hashlib,json,time,sys
out=Path('/workspace/scratch/source-smooth-parameter-space')
root=Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
source=out/'WeightedCarrier.lean';label=sys.argv[1]
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
cmd=['/home/agent/.elan/bin/lake','env','lean','-DwarningAsError=true','--root='+str(out),'-o',str(out/'WeightedCarrier.olean'),str(source)]
before=digest(source);(out/(label+'.source.lean')).write_bytes(source.read_bytes())
start=time.time();p=subprocess.run(cmd,cwd=root,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
log=out/(label+'.log');log.write_bytes(p.stdout)
r={'command':cmd,'cwd':str(root),'exit_code':p.returncode,'source_sha256_before':before,'source_sha256_after':digest(source),'log_sha256':digest(log),'elapsed_seconds':time.time()-start}
(out/(label+'.json')).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r));print(p.stdout.decode(),end='');sys.exit(p.returncode)
