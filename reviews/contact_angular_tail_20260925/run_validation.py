"""Replay 26 finite checks and 9 deliberate valid-program mutants, both modes."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
MUTANTS={
 'omit_conditional_schur_term':('variance_v-=cov_av*cov_av/S[0][0]','variance_v-=0'),
 'drop_pin_shift':('q=6*k*(w-2*u)/v','q=6*k*w/v'),
 'wrong_height_coefficient':('2*theta+3*w*D','theta+3*w*D'),
 'reverse_max_type':('4*theta-(w+1)**2','4*theta-(w-1)**2'),
 'wrong_cd_jacobian':('+d*v**3/(12*k)','+d*v**3/(6*k)'),
 'halve_right_rate':('return 12*k*k*(u-Q(1,2))**6','return 6*k*k*(u-Q(1,2))**6'),
 'halve_left_amplitude':('T0=5832*k**6*D**8/u**6','T0=2916*k**6*D**8/u**6'),
 'wrong_gaussian_recurrence':('(j-1)*out[j-2]','j*out[j-2]'),
 'drop_jacobian_power':("'contact_prefactor_power':-13","'contact_prefactor_power':-12"),
}

def identities():
 return {p.name:{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
         for p in ROOT.iterdir() if p.is_file()}

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True)
 out=p.parse_args().output.resolve()
 if out.exists() or out.is_relative_to(ROOT):raise SystemExit('new output outside source directory required')
 out.mkdir(parents=True);before=identities();src=(ROOT/'angular_contact.py').read_text()
 report={'passed':False,'python':sys.version,'distinct_tests':26,'distinct_mutants':len(MUTANTS), 'mutation_names':sorted(MUTANTS),'modes':[],
         'scientific_acceptance':False,'meaning':'finite algebra/control replay; not analytic proof certification'}
 try:
  for mode,flags in [('normal',[]),('optimized',['-O'])]:
   cmd=[sys.executable,'-B',*flags,'-S','-m','unittest','-v','test_angular_contact']
   def run(cwd,name,mutant=False):
    x=subprocess.run(cmd,cwd=cwd,capture_output=True,text=True,timeout=30)
    (out/(name+'.stdout')).write_text(x.stdout);(out/(name+'.stderr')).write_text(x.stderr)
    if mutant:
     if x.returncode==0 or 'AssertionError' not in x.stderr or 'FAILED (failures=' not in x.stderr:
      raise RuntimeError('mutant not assertion-detected: '+name)
     if 'SyntaxError' in x.stderr or 'ImportError' in x.stderr or 'errors=' in x.stderr:
      raise RuntimeError('invalid-program mutant: '+name)
    elif x.returncode or 'Ran 26 tests' not in x.stderr:
     raise RuntimeError('baseline failed: '+name)
   run(ROOT,'tests_'+mode)
   for name,(old,new) in MUTANTS.items():
    if src.count(old)!=1:raise RuntimeError('mutation target nonunique: '+name)
    scratch=out/'mutants'/mode/name;scratch.mkdir(parents=True)
    (scratch/'angular_contact.py').write_text(src.replace(old,new))
    shutil.copyfile(ROOT/'test_angular_contact.py',scratch/'test_angular_contact.py')
    run(scratch,'mutant_'+mode+'_'+name,True)
   report['modes'].append(mode)
  if before!=identities():raise RuntimeError('source mutated during replay')
  report.update(passed=True,source_files=before,sources_unchanged=True)
 finally:
  (out/'REPORT.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
 print(json.dumps(report,sort_keys=True))
if __name__=='__main__':main()
