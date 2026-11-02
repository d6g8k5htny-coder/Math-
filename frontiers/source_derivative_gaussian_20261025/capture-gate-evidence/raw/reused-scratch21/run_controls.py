from pathlib import Path
import subprocess,hashlib,json,time,sys
out=Path('/workspace/scratch/quartic-capture-algebra')
root=Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
label=sys.argv[1];source=out/'Controls.lean'
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
before=digest(source);(out/(label+'.source.lean')).write_bytes(source.read_bytes())
shell='LEAN_PATH=/workspace/scratch/quartic-capture-algebra:"$LEAN_PATH" lean -DwarningAsError=true /workspace/scratch/quartic-capture-algebra/Controls.lean'
cmd=['/home/agent/.elan/bin/lake','env','sh','-c',shell]
start=time.time();pr=subprocess.run(cmd,cwd=root,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
log=out/(label+'.log');log.write_bytes(pr.stdout)
r={'command':cmd,'cwd':str(root),'exit_code':pr.returncode,'source':str(source),'source_sha256_before':before,'source_sha256_after':digest(source),'log_sha256':digest(log),'elapsed_seconds':time.time()-start,'scope':'NEW scratch Controls ONLY; GeometrySupport and quartic cached imports reused'}
(out/(label+'.json')).write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r));print(pr.stdout.decode(),end='');sys.exit(pr.returncode)
