import datetime,hashlib,json,pathlib,subprocess,sys,time
root=pathlib.Path('/workspace/scratch/quartic-capture-production')
packet=pathlib.Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
source=packet/'SourceQuarticCaptureAlgebra.lean'
artifact=packet/'.lake/build/lib/lean/SourceQuarticCaptureAlgebra.olean'
label,controlname,mode=sys.argv[1:4]
control=root/controlname
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
before={'source':sha(source),'artifact':sha(artifact),'control':sha(control)}
(root/(label+'.source.lean')).write_bytes(control.read_bytes())
cmd=['/home/agent/.elan/bin/lake','env','lean']
if mode=='werror':cmd+=['-DwarningAsError=true']
cmd+=[str(control)]
started=time.time();stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
result=subprocess.run(cmd,cwd=packet,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
log=root/(label+'.log');log.write_bytes(result.stdout)
after={'source':sha(source),'artifact':sha(artifact),'control':sha(control)}
data={'scope':'Only new SourceQuarticCaptureAlgebra transfer-buffer/projection/orientation controls; prior closed Q2/Q3 control evidence reused unchanged, not rerun',
      'command':cmd,'cwd':str(packet),'exit_code':result.returncode,'sha256_before':before,
      'sha256_after':after,'log_sha256':sha(log),'log_bytes':len(result.stdout),
      'started_utc':stamp,'elapsed_seconds':time.time()-started,
      'author_side_helper_lineage':'OpenAI /root/palm_measure_transfer, no independent review credit'}
(root/(label+'.json')).write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps(data));print(result.stdout.decode());sys.exit(result.returncode)
