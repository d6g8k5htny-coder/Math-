import datetime,hashlib,json,pathlib,subprocess,sys,time
p=pathlib.Path(__file__).parent
name=sys.argv[1]
f=p/name
source=pathlib.Path('SourcePinCurvatureBounds.lean')
olean=pathlib.Path('.lake/build/lib/lean/SourcePinCurvatureBounds.olean')
sha=lambda q:hashlib.sha256(q.read_bytes()).hexdigest()
before={'source':sha(source),'olean':sha(olean),'control':sha(f)}
cmd=['lake','env','lean',str(f)]
start=time.time()
r=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
label=name.removesuffix('.lean')
(p/(label+'.log')).write_bytes(r.stdout)
meta={'command':cmd,'cwd':str(pathlib.Path.cwd()),'exit_code':r.returncode,'duration_seconds':time.time()-start,'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sha256_before':before,'sha256_after':{'source':sha(source),'olean':sha(olean),'control':sha(f)},'author_side_helper_lineage':'OpenAI/Codex /root/dm2_landed_composition/peano_strategy','scope':'NEW_SOURCE_PIN_CURVATURE_CONTROLS_ONLY'}
(p/(label+'.json')).write_text(json.dumps(meta,indent=2)+'\n')
print(json.dumps(meta));print(r.stdout.decode(),end='')
raise SystemExit(r.returncode)
