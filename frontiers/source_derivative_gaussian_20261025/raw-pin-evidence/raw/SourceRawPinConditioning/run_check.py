import datetime,hashlib,json,pathlib,subprocess,sys,time
root=pathlib.Path('/workspace/scratch/raw-pin-conditioning')
packet=pathlib.Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
source=packet/'SourceRawPinConditioning.lean'
artifact=packet/'.lake/build/lib/lean/SourceRawPinConditioning.olean'
label,mode=sys.argv[1:3]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
cmd=['/home/agent/.elan/bin/lake','env']
control=None
if mode=='kernel':cmd+=['leanchecker','SourceRawPinConditioning']
else:
 control=pathlib.Path(sys.argv[3]);cmd+=['lean']
 if mode=='werror':cmd+=['-DwarningAsError=true']
 cmd+=[str(control)]
before={'source':sha(source),'artifact':sha(artifact)}
if control:before['control']=sha(control)
started=time.time();stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
result=subprocess.run(cmd,cwd=packet,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
log=root/(label+'.log');log.write_bytes(result.stdout)
after={'source':sha(source),'artifact':sha(artifact)}
if control:after['control']=sha(control)
data={'scope':'Only new SourceRawPinConditioning qualification; unchanged24modules/23inputs reused',
      'command':cmd,'cwd':str(packet),'exit_code':result.returncode,'sha256_before':before,
      'sha256_after':after,'log_sha256':sha(log),'log_bytes':len(result.stdout),
      'started_utc':stamp,'elapsed_seconds':time.time()-started}
(root/(label+'.json')).write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps(data));print(result.stdout.decode());sys.exit(result.returncode)
