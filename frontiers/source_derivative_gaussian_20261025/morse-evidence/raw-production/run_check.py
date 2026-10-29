from pathlib import Path
import hashlib, json,subprocess,sys,datetime
root=Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025');ev=Path('/workspace/scratch/morse-incidence-production')
label=sys.argv[1];args=sys.argv[2:];src=root/'SourceMorseIncidence.lean'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
before=sha(src);(ev/(label+'.source.lean')).write_bytes(src.read_bytes());start=datetime.datetime.now(datetime.timezone.utc).isoformat();r=subprocess.run(args,cwd=root,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);log=ev/(label+'.log');log.write_bytes(r.stdout)
(ev/(label+'.json')).write_text(json.dumps({'command':args,'cwd':str(root),'started_utc':start,'ended_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit':r.returncode,'source_sha256_before':before,'source_sha256_after':sha(src),'log_sha256':sha(log)},indent=2)+'\n');print(r.stdout.decode());print('exit='+str(r.returncode));sys.exit(r.returncode)
