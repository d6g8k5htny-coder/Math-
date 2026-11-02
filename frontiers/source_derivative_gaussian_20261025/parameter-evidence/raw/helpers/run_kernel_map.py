from pathlib import Path
import subprocess,hashlib,json,time,sys
out=Path('/workspace/scratch/source-smooth-parameter-space')
root=Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
label=sys.argv[1];source=out/'ParameterKernel.lean'
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
before=digest(source);(out/(label+'.source.lean')).write_bytes(source.read_bytes())
cmd=['/home/agent/.elan/bin/lake','env','sh','-c','LEAN_PATH=/workspace/scratch/source-smooth-parameter-space:"$LEAN_PATH" lean -DwarningAsError=true '+ ' '.join(sys.argv[2:])+ ' '+str(source)]
start=time.time();pr=subprocess.run(cmd,cwd=root,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
log=out/(label+'.log');log.write_bytes(pr.stdout)
r={'command':cmd,'cwd':str(root),'exit_code':pr.returncode,'source':str(source),'source_sha256_before':before,'source_sha256_after':digest(source),'log_sha256':digest(log),'elapsed_seconds':time.time()-start,'scope':'NEW scratch ParameterKernel ONLY; cached WeightedCarrier/topology/source imported unchanged'}
(out/(label+'.json')).write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r));print(pr.stdout.decode(),end='');sys.exit(pr.returncode)
