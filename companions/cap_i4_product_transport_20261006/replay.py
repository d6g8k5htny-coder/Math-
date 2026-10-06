"""Bounded source-bound replay; parent proof/evidence helpers are reused at exact blobs."""
import hashlib, importlib.util, json, os, re, subprocess, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
NAMES=['positive_test_measurable','withDensity_positive_spectral_bound','residual_iterated_positive_spectral_bound','product_positive_spectral_bound','jointLaw_positive_spectral_bound','dominated_weight_spectral_bound']
PINS={
 'companions/cap_i4_polar_20261006/CapI4Polar.lean':'9d0bdbfb5ad77c159fe623cf2dcad31cc9402ba4',
 'companions/cap_i4_linear_20261006/CapI4Linear.lean':'3c571603f2aabae49144cdba4bc52cd94a6f4d82',
 'companions/cap_i4_angular_20261006/CapI4Angular.lean':'fab5589a93a2b700cabac5e2617360cf99cba688',
 'companions/cap_i4_entry_volume_20261006/CapI4EntryVolume.lean':'46621995dd93120a6d0456b4d0f0f9fa8a849abd',
 'companions/cap_i4_spectral_assembly_20261006/CapI4SpectralAssembly.lean':'cf60892c9233352ae861d8dacc7ab1d591014980',
 'companions/cap_i4_linear_20261006/replay.py':'01ccc2ef0c0af691a89d5836346a8d87535e4b2d',
 'formal/lean-toolchain':'ba8ebf2dbaf6a668cd2a0e086186d6d569b69ff5',
 'formal/lakefile.toml':'8117eae1b2897b7d95f5b2c42e8cf15222a1c5e8',
 'formal/lake-manifest.json':'d482b5f1e038b90397e239d2c0af82792cb0bd09',
 'imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md':'dfed3b8d318a3ab1950957f393307733a4bef3f2',
 'imports/lifetime_parent_20260925/ERRATUM_CONGRUENCE.md':'213594d6ca6a86fb938110f4d166d9ce275a02d0'}
OWN={'CapI4ProductTransport.lean','Contract.lean','README.md','replay.py','test_contract.py'}
WORKFLOW='.github/workflows/cap-i4-product-transport.yml'
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
def snapshot():
 if {p.name for p in HERE.iterdir()}!=OWN:raise ValueError('child membership mismatch')
 for path,expected in PINS.items():
  if (ROOT/path).is_symlink() or git('hash-object',path)!=expected:raise ValueError('parent source mismatch: '+path)
 paths=[str((HERE/n).relative_to(ROOT)) for n in sorted(OWN)]+[WORKFLOW]+list(PINS)
 if git('diff','--name-only','HEAD','--',*paths):raise ValueError('dirty source')
 files={}
 for path in paths:
  p=ROOT/path
  if p.is_symlink() or not p.is_file():raise ValueError('nonregular source')
  files[path]=sha(p.read_bytes())
 deps={p['name']:p['rev'] for p in json.loads((ROOT/'formal/lake-manifest.json').read_text())['packages']}
 for name,rev in deps.items():
  if git('-C',str(ROOT/'formal/.lake/packages'/name),'rev-parse','HEAD')!=rev:raise ValueError('dependency mismatch: '+name)
 head=git('rev-parse','HEAD')
 if head!=os.environ.get('GITHUB_SHA',head):raise ValueError('tested head mismatch')
 return dict(head=head,run=os.environ.get('GITHUB_RUN_ID','local'),attempt=os.environ.get('GITHUB_RUN_ATTEMPT','local'),files=files,dependencies=deps)
def main():
 out=ROOT/'.lake/cap-i4-product-transport';out.mkdir(parents=True,exist_ok=False)
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
 if 'version 4.34.1,' not in run('toolchain',['lean','--version']):raise ValueError('wrong Lean toolchain')
 parents=list(PINS)[:5]
 for path in parents:(build/Path(path).name).write_bytes((ROOT/path).read_bytes())
 (build/'CapI4ProductTransport.lean').write_bytes((HERE/'CapI4ProductTransport.lean').read_bytes())
 for module in ['CapI4Polar','CapI4Linear','CapI4Angular','CapI4EntryVolume','CapI4SpectralAssembly','CapI4ProductTransport']:
  run(module,['lean','-DwarningAsError=true','--root='+str(build),'-o',str(build/(module+'.olean')),str(build/(module+'.lean'))])
 (out/'Contract.lean').write_bytes((HERE/'Contract.lean').read_bytes())
 for name,command in [('Audit','#print axioms '),('Types','#check @')]:
  (out/(name+'.lean')).write_text('import CapI4ProductTransport\n'+''.join(command+'CapI4ProductTransport.'+n+'\n' for n in NAMES))
 for name,label in [('Contract','contract'),('Audit','axioms'),('Types','types')]:run(label,['lean','-DwarningAsError=true','--root='+str(out),str(out/(name+'.lean'))])
 helper=ROOT/'companions/cap_i4_linear_20261006/replay.py'
 spec=importlib.util.spec_from_file_location('parent_evidence',helper);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 m.axioms((out/'axioms.log').read_text(),['CapI4ProductTransport.'+n for n in NAMES])
 types=(out/'types.log').read_text()
 if re.findall(r'^@?(CapI4ProductTransport\.\w+)(?:\.\{[^}]*\})?\s*:',types,re.M)!=['CapI4ProductTransport.'+n for n in NAMES] or re.search(r'\b(error|warning):',types):raise ValueError('type inventory/diagnostic mismatch')
 run('leanchecker',['leanchecker','--fresh','CapI4ProductTransport'])
 controls={'RejectFactor':'example : (2 : ℝ)*2*(1/4) = 2 := by\n  norm_num\n','RejectSign':'example : CapI4Linear.tracePair (CapI4Linear.spectralPair (2,1)) = (2,1) := by\n  rw [CapI4Linear.tracePair_spectralPair]\n  norm_num\n'}
 for name,body in controls.items():
  (out/(name+'.lean')).write_text('import CapI4ProductTransport\n'+body)
  m.negative(run(name,['lean','-DwarningAsError=true','--root='+str(out),str(out/(name+'.lean'))],1),1)
 after=snapshot();(out/'after.json').write_text(json.dumps(after,sort_keys=True)+'\n')
 if before!=after:raise ValueError('source changed during execution')
 (out/'verdict.json').write_text(json.dumps(dict(pass_=True,theorems=6,scope='density and explicit joint-product-law transport only; concrete Gaussian inputs remain open',context=after),sort_keys=True)+'\n')
 (out/'SHA256SUMS').write_text(''.join(sha(p.read_bytes())+'  '+p.name+'\n' for p in sorted(out.iterdir()) if p.is_file()))
 print('PASS: conditional density/product-law transport; concrete Gaussian Cap I4 remains open')
if __name__=='__main__':main()
