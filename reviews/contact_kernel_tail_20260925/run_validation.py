"""Bounded replay; finite checks and detected mutants are not analytic acceptance."""
from __future__ import annotations
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
MUTANTS={
 'lose_midpoint_shift':('u*u-u*w+Q(1,4)','u*u-u*w'),
 'wrong_q_parameter':('q=6*k*(w-2*u)/v','q=6*k*(w-u)/v'),
 'lose_endpoint_k2':('return (24*k)*(6*k)*(9*k*k)**3/(36*k*k)','return (24*k)*(6*k)*(9*k*k)**3/36'),
 'wrong_type_region':('((lower_left,-3,-1),(lower_right,-1,1))','((lower_left,-3,-1),(lower_left,-1,1))'),
 'wrong_height_orientation':('return -2*u**3-Q(3,2)*u-1+2*t+3*w*(u*u-Q(1,4))','return -2*u**3-Q(3,2)*u+1-2*t+3*w*(u*u-Q(1,4))'),
 'wrong_gaussian_moment':('(n-1)*out[n-2]/(2*a)','(n+1)*out[n-2]/(2*a)'),
 'promote_small_gap_uniformity':("'finite_r_small_k_uniformity':False","'finite_r_small_k_uniformity':True"),
}

def require(ok,message):
    if not ok:raise RuntimeError(message)

def identities():
    pins=json.loads((ROOT/'SOURCE_FILES.json').read_text())['files']
    for name,identity in pins.items():
        p=ROOT/name
        require(p.name==name and not p.is_symlink() and p.is_file(),'flat regular source required')
        raw=p.read_bytes()
        require({'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}==identity,'identity mismatch: '+name)
    return pins

def run_cmd(cmd,cwd,out,name,mutant=False):
    p=subprocess.run(cmd,cwd=cwd,capture_output=True,text=True,timeout=30)
    (out/(name+'.stdout')).write_text(p.stdout)
    (out/(name+'.stderr')).write_text(p.stderr)
    require('Ran 24 tests' in p.stderr and 'skipped=' not in p.stderr,'unexpected test coverage '+name)
    if mutant:
        require(p.returncode!=0 and 'AssertionError' in p.stderr and 'FAILED (failures=' in p.stderr,'mutant not assertion-detected: '+name)
        require('ERROR:' not in p.stderr and 'SyntaxError' not in p.stderr and 'ImportError' not in p.stderr,'invalid-program mutation: '+name)
    else:
        require(p.returncode==0,'baseline failure '+name)

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True)
    out=parser.parse_args().output.resolve()
    require(not out.exists() and not out.is_relative_to(ROOT),'new output outside source required')
    out.mkdir(parents=True);before=identities();source=(ROOT/'contact_tools.py').read_text()
    report={'passed':False,'python':sys.version,'distinct_tests':24,'distinct_mutants':len(MUTANTS),'modes':[],
            'meaning':'finite exact algebra and diagnostic implementation checks, not independent continuum review'}
    try:
        for mode,flags in [('normal',[]),('optimized',['-O'])]:
            cmd=[sys.executable,'-B',*flags,'-S','-m','unittest','-v','test_contact_tools']
            run_cmd(cmd,ROOT,out,'baseline_'+mode)
            result=subprocess.run([sys.executable,'-B',*flags,'-S','contact_tools.py'],cwd=ROOT,capture_output=True,timeout=10)
            require(result.returncode==0 and result.stdout==(ROOT/'RESULTS.json').read_bytes(),'output byte mismatch')
            for name,(old,new) in MUTANTS.items():
                require(source.count(old)==1,'nonunique mutation '+name)
                temp=out/'mutants'/mode/name;temp.mkdir(parents=True)
                (temp/'contact_tools.py').write_text(source.replace(old,new))
                shutil.copyfile(ROOT/'test_contact_tools.py',temp/'test_contact_tools.py')
                run_cmd(cmd,temp,out,'mutation_'+mode+'_'+name,True)
            report['modes'].append(mode)
        require(before==identities(),'sources changed')
        report.update(passed=True,sources_unchanged=True,source_files=before)
    finally:
        (out/'REPORT.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps(report,sort_keys=True))

if __name__=='__main__':main()
