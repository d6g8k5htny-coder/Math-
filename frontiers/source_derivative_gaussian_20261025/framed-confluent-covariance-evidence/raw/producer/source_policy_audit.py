import pathlib,json,re,datetime,sys
b=pathlib.Path('/workspace/scratch/framed-confluent-covariance-construct');f=json.loads((b/'FROZEN.json').read_text());p=pathlib.Path(f['source']['path']);start=datetime.datetime.now(datetime.timezone.utc).isoformat();s=p.read_text();out=[];i=0;depth=0
while i<len(s):
 if depth:
  if s.startswith('/-',i):depth+=1;i+=2
  elif s.startswith('-/',i):depth-=1;i+=2
  else:i+=1
 elif s.startswith('/-',i):depth=1;i+=2
 elif s.startswith('--',i):
  k=s.find('\n',i);i=len(s) if k<0 else k
 else:out.append(s[i]);i+=1
code=''.join(out);findings=re.findall(r'\b(?:sorry|admit|native_decide|implemented_by|axiom)\b|_private\.',code)
findings += re.findall(r'^\s*import\s+Mathlib\s*$',code,re.M)
r={'scope':'Frozen new module only; first lexical policy audit. No old dependency audit/replay.','start':start,'end':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':['python',str(b/'source_policy_audit.py')],'sourceIdentityReusedFrom':'FROZEN.json','uncoveredObligation':'Explicit absence of forbidden admissions/native implementations/private foreign-name references and umbrella import, beyond transitive axiom inventory.','findings':findings,'imports':re.findall(r'^import (\S+)',code,re.M),'exit':0 if not findings else 1}
text=json.dumps(r,indent=2)+'\n';(b/'SOURCE_POLICY_AUDIT.json').write_text(text);(b/'SOURCE_POLICY_AUDIT.stdout.log').write_text(text);(b/'SOURCE_POLICY_AUDIT.stderr.log').write_text('');print(text,end='');sys.exit(r['exit'])
