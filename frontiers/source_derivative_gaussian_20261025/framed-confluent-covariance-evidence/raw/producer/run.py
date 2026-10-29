import datetime,hashlib,json,pathlib,subprocess,sys,time
base=pathlib.Path('/workspace/scratch/framed-confluent-covariance-construct');repo=pathlib.Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
kind=sys.argv[1];runs=base/'runs';runs.mkdir(exist_ok=True);i=1
if kind=='factor-six':assert not list(runs.glob('factor-six-*')),'Exactly one sole factor-six mutation permitted'
while (runs/f'{kind}-{i:03}').exists():i+=1
out=runs/f'{kind}-{i:03}';out.mkdir();src=repo/'SourceFramedConfluentCovariance.lean'
for p in [src,*base.glob('*.lean')]:
 if p.exists():(out/p.name).write_bytes(p.read_bytes())
def ident(p):
 raw=p.read_bytes();return {'path':str(p),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
if kind=='develop':
 cmd=['/home/agent/.elan/bin/lake','env','lean','-DwarningAsError=true',str(src),'-o',str(out/'SourceFramedConfluentCovariance.olean')]
elif kind=='kernel':
 assert not list(runs.glob('kernel-*/record.json')),'Exactly one own final module kernel permitted'
 cmd=['/home/agent/.elan/bin/lake','env','sh','-c',f'LEAN_PATH={base}/build:$LEAN_PATH exec leanchecker SourceFramedConfluentCovariance']
else:
 file={'controls':'Controls.lean','inventory':'Inventory.lean','factor-six':'FactorSixMutation.lean'}[kind]
 cmd=['/home/agent/.elan/bin/lake','env','sh','-c',f'LEAN_PATH={base}/build:$LEAN_PATH exec lean -DwarningAsError=true --root={base} {base/file} -o {out/(file.removesuffix(".lean")+".olean")}']
start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic();p=subprocess.run(cmd,cwd=repo,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
(out/'stdout.log').write_bytes(p.stdout);(out/'stderr.log').write_bytes(p.stderr)
r={'kind':kind,'run':out.name,'start':start,'end':datetime.datetime.now(datetime.timezone.utc).isoformat(),'seconds':time.monotonic()-t,'command':cmd,'cwd':str(repo),'exit':p.returncode,'source':ident(src),'stdout':ident(out/'stdout.log'),'stderr':ident(out/'stderr.log')}
(out/'record.json').write_text(json.dumps(r,indent=2)+'\n')
with (base/'RAW_LEDGER.jsonl').open('a') as f:f.write(json.dumps(r)+'\n')
print(json.dumps(r));print(p.stdout.decode(),end='');print(p.stderr.decode(),end='');sys.exit(p.returncode)
