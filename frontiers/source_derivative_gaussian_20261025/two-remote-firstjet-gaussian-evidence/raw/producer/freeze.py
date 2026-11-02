from pathlib import Path
import hashlib,json,datetime,shutil
b=Path('/workspace/scratch/two-remote-firstjet-gaussian-construct');src=Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025/SourceTwoRemoteFirstJetGaussian.lean')
assert not (b/'FROZEN_SOURCE.json').exists()
records=[json.loads(p.read_text()) for p in sorted((b/'runs').glob('develop-*/record.json'))]
r=records[-1];assert r['exit']==0
out=b/'runs'/r['run'];assert src.read_bytes()==(out/src.name).read_bytes()
(b/'build').mkdir(exist_ok=True);obj=out/'SourceTwoRemoteFirstJetGaussian.olean';dest=b/'build'/obj.name
shutil.copyfile(obj,dest);raw=obj.read_bytes();identity={'path':str(dest),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
f={'frozen_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source':r['source'],'object':identity,'strict_run':r['run'],'strict_receipt':str(out/'record.json'),'strict_success_reused_on_exact_bytes':True,'no_freshness_compile':True,'production_cache_copy':False,'eligible_own_object_only':True,'all_prior_attempts_retained':True,'exactly_one_final_own_module_kernel_still_pending':True}
(b/'FROZEN_SOURCE.json').write_text(json.dumps(f,indent=2)+'\n');print(json.dumps(f,indent=2))
