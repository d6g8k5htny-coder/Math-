from pathlib import Path
import subprocess,hashlib,json,time,sys
p=Path('/workspace/scratch/source-smooth-topology/DerivativeBCF.lean');out=p.parent
root=Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
label=sys.argv[1];cmd=['/home/agent/.elan/bin/lake','env','lean','-DwarningAsError=true',str(p)]
before=hashlib.sha256(p.read_bytes()).hexdigest();(out/(label+'.source.lean')).write_bytes(p.read_bytes())
start=time.time();pr=subprocess.run(cmd,cwd=root,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
log=out/(label+'.log');log.write_bytes(pr.stdout)
record={'command':cmd,'cwd':str(root),'exit_code':pr.returncode,'source_sha256_before':before,
 'source_sha256_after':hashlib.sha256(p.read_bytes()).hexdigest(),'log_sha256':hashlib.sha256(pr.stdout).hexdigest(),'elapsed_seconds':time.time()-start}
(out/(label+'.json')).write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record));print(pr.stdout.decode(),end='');sys.exit(pr.returncode)
