import pathlib,sys,subprocess,json,datetime,time,hashlib
base=pathlib.Path('/workspace/scratch/remote-jet-witness-construct');repo=pathlib.Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
kind=sys.argv[1];runs=base/'runs';i=1
while (runs/f'{kind}-{i:03}').exists():i+=1
out=runs/f'{kind}-{i:03}';out.mkdir();src=repo/'SourceRemoteJetWitness.lean';obj=base/'build/SourceRemoteJetWitness.olean'
def ident(p):
 raw=p.read_bytes();return {'path':str(p),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
for p in [src,base/'Controls.lean',base/'Inventory.lean',base/'FalseCollisionMutation.lean']:
 if p.exists():(out/p.name).write_bytes(p.read_bytes())
before={'source':ident(src),'object':ident(obj)}
if kind=='kernel':
 assert not list(runs.glob('kernel-*/record.json')),'Exactly one named kernel permitted'
 inner='leanchecker SourceRemoteJetWitness'
else:
 file={'controls':'Controls.lean','inventory':'Inventory.lean','false-collision':'FalseCollisionMutation.lean'}[kind]
 inner=f'lean -DwarningAsError=true --root={base} {base/file} -o {out/(file.removesuffix(".lean")+".olean")}'
cmd=['lake','env','sh','-c',f'LEAN_PATH={base}/build:$LEAN_PATH exec {inner}']
start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic();p=subprocess.run(cmd,cwd=repo,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
(out/'stdout.log').write_bytes(p.stdout);(out/'stderr.log').write_bytes(p.stderr)
r={'kind':kind,'run':out.name,'start':start,'end':datetime.datetime.now(datetime.timezone.utc).isoformat(),'seconds':time.monotonic()-t,'command':cmd,'cwd':str(repo),'exit':p.returncode,'before':before,'after':{'source':ident(src),'object':ident(obj)},'stdout':ident(out/'stdout.log'),'stderr':ident(out/'stderr.log')}
(out/'record.json').write_text(json.dumps(r,indent=2)+'\n')
with (base/'RAW_LEDGER.jsonl').open('a') as f:f.write(json.dumps(r)+'\n')
print(json.dumps(r));print(p.stdout.decode(),end='');print(p.stderr.decode(),end='');sys.exit(p.returncode)
