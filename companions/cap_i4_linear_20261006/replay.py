"""Source-bound linear-volume replay. Run through the repository's pinned lake env."""
import argparse,hashlib,json,os,re,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
ALLOW={'propext','Classical.choice','Quot.sound'}

def strict_json(text):
 def pairs(rows):
  out={}
  for k,v in rows:
   if k in out:raise ValueError('duplicate JSON key')
   out[k]=v
  return out
 def reject(v):raise ValueError('nonfinite JSON number')
 return json.loads(text,object_pairs_hook=pairs,parse_constant=reject)

def sha(data):return hashlib.sha256(data).hexdigest()

def axioms(text,names):
 p=re.compile(r"'([^']+)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)")
 matches=list(p.finditer(text))
 if [m.group(1) for m in matches]!=names or p.sub('',text).strip():raise ValueError('axiom inventory or unmatched output')
 for m in matches:
  if not {s.strip() for s in (m.group(2) or '').split(',') if s.strip()}<=ALLOW:raise ValueError('forbidden axiom')

def types(text,names):
 # Inventory/diagnostic validation only; Contract.lean checks the critical exact types.
 p=re.compile(r'^@?(CapI4Linear\.\w+)(?:\.\{[^}]*\})?\s*:',re.M)
 matches=list(p.finditer(text))
 if [m.group(1) for m in matches]!=names or not matches or text[:matches[0].start()].strip():raise ValueError('type inventory mismatch')
 if re.search(r'\b(?:error|warning):',text) or re.search(r'^[A-Za-z_]\w*\.\w+\s*:',p.sub('',text),re.M):raise ValueError('foreign declaration or diagnostic')

def negative(text,status):
 if status!=1 or not re.fullmatch(r'(?:[^\n]*:\d+:\d+: )?error: unsolved goals\n⊢ False\s*',text):raise ValueError('not intended false-goal rejection')

def manifest():
 m=strict_json((HERE/'SOURCES.json').read_text())
 if set(p.name for p in HERE.iterdir())!=set(m['files'])|{'SOURCES.json'}:raise ValueError('packet membership')
 for name,row in m['files'].items():
  p=HERE/name
  if p.is_symlink() or not p.is_file():raise ValueError('nonregular packet member')
  d=p.read_bytes();blob=hashlib.sha1(b'blob '+str(len(d)).encode()+b'\0'+d).hexdigest()
  if (len(d),sha(d),blob)!=(row['bytes'],row['sha256'],row['blob']):raise ValueError('source identity: '+name)
 return m

def snapshot(root,m):
 def git(*args):return subprocess.check_output(['git',*args],cwd=root,text=True).strip()
 paths=['companions/cap_i4_linear_20261006','.github/workflows/cap-i4-linear.yml',*m['source_blobs']]
 if git('diff','--name-only','HEAD','--',*paths):raise ValueError('dirty consumed source')
 for path,blob in m['source_blobs'].items():
  p=root/path
  if p.is_symlink() or git('hash-object',path)!=blob:raise ValueError('consumed source: '+path)
 packages=strict_json((root/'formal/lake-manifest.json').read_text())['packages']
 for p in packages:
  got=git('-C',str(root/'formal/.lake/packages'/p['name']),'rev-parse','HEAD')
  if got!=p['rev']:raise ValueError('dependency revision: '+p['name'])
 head=git('rev-parse','HEAD')
 if head!=os.environ.get('GITHUB_SHA',head):raise ValueError('tested head mismatch')
 return {'head':head,'run':os.environ.get('GITHUB_RUN_ID','local'),'attempt':os.environ.get('GITHUB_RUN_ATTEMPT','local'),
  'manifest_sha256':sha((HERE/'SOURCES.json').read_bytes()),'source_blobs':m['source_blobs'],
  'workflow_sha256':sha((root/'.github/workflows/cap-i4-linear.yml').read_bytes())}

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--check-source',action='store_true');args=ap.parse_args()
 m=manifest()
 if args.check_source:print(json.dumps(m,sort_keys=True));return
 root=HERE.parent.parent;out=root/'.lake/cap-i4-linear'
 out.mkdir(parents=True,exist_ok=False);build=out/'build';build.mkdir()
 before=snapshot(root,m);(out/'before.json').write_text(json.dumps(before,sort_keys=True)+'\n')
 records=[]
 env=os.environ.copy();env['LEAN_PATH']=str(build)+':'+env.get('LEAN_PATH','');env['LEAN_SRC_PATH']=str(build)+':'+env.get('LEAN_SRC_PATH','')
 def execute(label,cmd,expected=0):
  try:r=subprocess.run(cmd,cwd=root,capture_output=True,timeout=300,env=env)
  except subprocess.TimeoutExpired as e:
   (out/(label+'.log')).write_bytes((e.stdout or b'')+(e.stderr or b''));raise
  data=r.stdout+r.stderr;(out/(label+'.log')).write_bytes(data)
  records.append({'label':label,'argv':cmd,'exit':r.returncode,'log_sha256':sha(data)})
  (out/'processes.json').write_text(json.dumps(records,indent=2)+'\n')
  if r.returncode!=expected:print(data.decode(errors='replace'));raise ValueError(label+' exit '+str(r.returncode))
  return data.decode()
 for mode,flags in [('normal',['-B','-S']),('optimized',['-B','-O','-S'])]:
  for suite in ['test_linear','test_evidence']:
   execute(suite+'-'+mode,[sys.executable,*flags,str(HERE/(suite+'.py'))])
 version=execute('toolchain',['lean','--version'])
 if 'version 4.34.1,' not in version:raise ValueError('wrong Lean version')
 (build/'CapI4Linear.lean').write_bytes((HERE/'CapI4Linear.lean').read_bytes())
 execute('build',['lean','-DwarningAsError=true','--root='+str(build),'-o',str(build/'CapI4Linear.olean'),str(build/'CapI4Linear.lean')])
 (out/'Contract.lean').write_bytes((HERE/'Contract.lean').read_bytes())
 names=m['declarations']
 (out/'Audit.lean').write_text('import CapI4Linear\n'+''.join('#print axioms '+n+'\n' for n in names))
 (out/'Types.lean').write_text('import CapI4Linear\nset_option pp.universes true\n'+''.join('#check @'+n+'\n' for n in names))
 for name,label in [('Contract','contract'),('Audit','axioms'),('Types','types')]:execute(label,['lean','-DwarningAsError=true','--root='+str(out),str(out/(name+'.lean'))])
 axioms((out/'axioms.log').read_text(),names);types((out/'types.log').read_text(),names)
 execute('leanchecker',['leanchecker','--fresh','CapI4Linear'])
 probes={
 'RejectDet':'example : LinearMap.det CapI4Linear.tracePair = -(1 : ℝ) := by\n  rw [CapI4Linear.det_tracePair]\n  norm_num\n',
 'RejectOrder':'example : CapI4Linear.spectralPair (0, 1) = (1, -1) := by\n  rw [CapI4Linear.spectralPair_apply]\n  norm_num\n'}
 for name,body in probes.items():
  (out/(name+'.lean')).write_text('import CapI4Linear\n'+body)
  text=execute(name,['lean','-DwarningAsError=true','--root='+str(out),str(out/(name+'.lean'))],1);negative(text,1)
 after=snapshot(root,manifest())
 if before!=after:raise ValueError('source changed during replay')
 (out/'after.json').write_text(json.dumps(after,sort_keys=True)+'\n')
 result={'pass':True,'context':before,'declarations':len(names),'scope':'two linear-volume changes; not full Gaussian Cap I4'}
 (out/'verdict.json').write_text(json.dumps(result,sort_keys=True)+'\n')
 hashed=[p for p in out.iterdir() if p.is_file()]
 (out/'SHA256SUMS').write_text(''.join(sha(p.read_bytes())+'  '+p.name+'\n' for p in sorted(hashed)))
 print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
