import hashlib,json,pathlib,subprocess,sys,time
root=pathlib.Path('/workspace/scratch/actual-geometric-palm-join')
source=root/'RawConfluentLift.lean'
label=sys.argv[1]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
before=sha(source)
cmd=['/home/agent/.elan/bin/lake','env','lean','-DwarningAsError=true',str(source)]
cwd='/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025'
started=time.time()
result=subprocess.run(cmd,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
log=root/(label+'.log');log.write_bytes(result.stdout)
data={'scope':'Only new scratch RawConfluentLift algebra; no baseline checks or Kac–Rice formalization',
      'command':cmd,'cwd':cwd,'exit_code':result.returncode,'source_sha256_before':before,
      'source_sha256_after':sha(source),'log_sha256':sha(log),'elapsed_seconds':time.time()-started}
(root/(label+'.json')).write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps(data));print(result.stdout.decode())
