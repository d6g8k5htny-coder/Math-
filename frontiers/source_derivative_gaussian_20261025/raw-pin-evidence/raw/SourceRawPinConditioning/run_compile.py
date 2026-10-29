import hashlib,json,pathlib,subprocess,sys,time
root=pathlib.Path('/workspace/scratch/raw-pin-conditioning')
packet=pathlib.Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
source=packet/'SourceRawPinConditioning.lean'
label=sys.argv[1]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
before=sha(source)
(root/(label+'.source.lean')).write_bytes(source.read_bytes())
cmd=['/home/agent/.elan/bin/lake','env','lean','-DwarningAsError=true','-o','.lake/build/lib/lean/SourceRawPinConditioning.olean',str(source)]
started=time.time();result=subprocess.run(cmd,cwd=packet,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
log=root/(label+'.log');log.write_bytes(result.stdout)
data={'scope':'Only new SourceRawPinConditioning module; completed24modules/23inputs reused',
      'command':cmd,'cwd':str(packet),'exit_code':result.returncode,'source_sha256_before':before,
      'source_sha256_after':sha(source),'log_sha256':sha(log),'elapsed_seconds':time.time()-started}
(root/(label+'.json')).write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps(data));print(result.stdout.decode())
