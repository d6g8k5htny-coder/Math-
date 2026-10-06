"""Scoped adaptation of the existing Cap source-bound execution pattern."""
import hashlib,importlib.util,json,os,re,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
NAMES=['support_transfer','ninth_integrable_iff','ninth_integral_eq','outer_inputs']
OWN={'CapI4ResidualLaw.lean','Contract.lean','README.md','test_contract.py','replay.py'}
PINS={
 'companions/cap_i4_linear_20261006/replay.py':'01ccc2ef0c0af691a89d5836346a8d87535e4b2d',
 'formal/lean-toolchain':'ba8ebf2dbaf6a668cd2a0e086186d6d569b69ff5',
 'formal/lakefile.toml':'8117eae1b2897b7d95f5b2c42e8cf15222a1c5e8',
 'formal/lake-manifest.json':'d482b5f1e038b90397e239d2c0af82792cb0bd09',
 'companions/cap_i4_outer_composition_20261006/CapI4OuterComposition.lean':'4476b17ea0edfc2fb2115c44ebae84e78dd11857'}
WORKFLOW='.github/workflows/cap-i4-residual-law.yml'
def sha(d):return hashlib.sha256(d).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
def snapshot():
 if {p.name for p in HERE.iterdir()}!=OWN:raise ValueError('child inventory')
 for path,expected in PINS.items():
  if (ROOT/path).is_symlink() or git('hash-object',path)!=expected:raise ValueError('pinned input: '+path)
 paths=[str((HERE/n).relative_to(ROOT)) for n in sorted(OWN)]+[WORKFLOW]+list(PINS)
 if git('diff','--name-only','HEAD','--',*paths):raise ValueError('dirty tracked source')
 files={}
 for path in paths:
  p=ROOT/path
  if p.is_symlink() or not p.is_file():raise ValueError('nonregular source')
  files[path]=sha(p.read_bytes())
 deps={p['name']:p['rev'] for p in json.loads((ROOT/'formal/lake-manifest.json').read_text())['packages']}
 for name,rev in deps.items():
  if git('-C',str(ROOT/'formal/.lake/packages'/name),'rev-parse','HEAD')!=rev:raise ValueError('dependency: '+name)
 head=git('rev-parse','HEAD')
 if head!=os.environ.get('GITHUB_SHA',head):raise ValueError('tested HEAD')
 return dict(head=head,run=os.environ.get('GITHUB_RUN_ID','local'),attempt=os.environ.get('GITHUB_RUN_ATTEMPT','local'),files=files,dependencies=deps)
def main():
 out=ROOT/'.lake/cap-i4-residual-law';out.mkdir(parents=True,exist_ok=False)
 build=out/'build';build.mkdir()
 before=snapshot();(out/'before.json').write_text(json.dumps(before,sort_keys=True)+'\n')
 env=os.environ.copy()
 for key in ['LEAN_PATH','LEAN_SRC_PATH']:env[key]=str(build)+':'+env.get(key,'')
 records=[]
 def run(label,argv,expected=0):
  try:r=subprocess.run(argv,cwd=ROOT,capture_output=True,env=env,timeout=1200 if label=='leanchecker' else 300)
  except subprocess.TimeoutExpired as e:
   (out/(label+'.log')).write_bytes((e.stdout or b'')+(e.stderr or b''));raise
  data=r.stdout+r.stderr;(out/(label+'.log')).write_bytes(data)
  records.append(dict(label=label,argv=argv,exit=r.returncode,sha256=sha(data)))
  (out/'processes.json').write_text(json.dumps(records,indent=2)+'\n')
  if r.returncode!=expected:print(data.decode(errors='replace'));raise ValueError(label+' unexpected exit '+str(r.returncode))
  return data.decode()
 for mode,flags in [('normal',['-B','-S']),('optimized',['-B','-O','-S'])]:run('source-'+mode,[sys.executable,*flags,str(HERE/'test_contract.py')])
 if 'version 4.34.1,' not in run('toolchain',['lean','--version']):raise ValueError('wrong toolchain')
 (build/'CapI4ResidualLaw.lean').write_bytes((HERE/'CapI4ResidualLaw.lean').read_bytes())
 run('module',['lean','-DwarningAsError=true','--root='+str(build),'-o',str(build/'CapI4ResidualLaw.olean'),str(build/'CapI4ResidualLaw.lean')])
 (out/'Contract.lean').write_bytes((HERE/'Contract.lean').read_bytes())
 for name,command in [('Audit','#print axioms '),('Types','#check @')]:
  (out/(name+'.lean')).write_text('import CapI4ResidualLaw\n'+''.join(command+'CapI4ResidualLaw.'+n+'\n' for n in NAMES))
 for name,label in [('Contract','contract'),('Audit','axioms'),('Types','types')]:run(label,['lean','-DwarningAsError=true','--root='+str(out),str(out/(name+'.lean'))])
 helper=ROOT/'companions/cap_i4_linear_20261006/replay.py'
 spec=importlib.util.spec_from_file_location('parent_evidence',helper);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 m.axioms((out/'axioms.log').read_text(),['CapI4ResidualLaw.'+n for n in NAMES])
 text=(out/'types.log').read_text()
 if re.findall(r'^@?(CapI4ResidualLaw\.\w+)(?:\.\{[^}]*\})?\s*:',text,re.M)!=['CapI4ResidualLaw.'+n for n in NAMES] or re.search(r'\b(error|warning):',text):raise ValueError('types or diagnostics')
 run('leanchecker',['leanchecker','--fresh','CapI4ResidualLaw'])
 controls={'RejectMoment':'example : |(-2 : ℝ)|^9 = 2 := by\n  norm_num\n','RejectSupport':'example : (1 : ℝ) ≤ 0 := by\n  norm_num\n'}
 for name,body in controls.items():
  (out/(name+'.lean')).write_text('import CapI4ResidualLaw\n'+body)
  m.negative(run(name,['lean','-DwarningAsError=true','--root='+str(out),str(out/(name+'.lean'))],1),1)
 after=snapshot();(out/'after.json').write_text(json.dumps(after,sort_keys=True)+'\n')
 if before!=after:raise ValueError('source changed')
 (out/'verdict.json').write_text(json.dumps(dict(pass_=True,theorems=4,definitions=0,scope='source residual support and finite ninth moment transported to its marginal only',context=after),sort_keys=True)+'\n')
 (out/'SHA256SUMS').write_text(''.join(sha(p.read_bytes())+'  '+p.name+'\n' for p in sorted(out.iterdir()) if p.is_file()))
 print('PASS: residual-law input adapter; field support/moment construction remains separate')
if __name__=='__main__':main()
