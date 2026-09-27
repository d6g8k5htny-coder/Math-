"""Run bounded algebra controls and deliberate faults; no proof acceptance."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
EXPECTED=21
MUTANTS={
 'omit_three_hessian_gain':('three_hessians_r=6','three_hessians_r=0'),
 'drop_original_normalizer':('normalizer_r=-2','normalizer_r=0'),
 'use_only_two_hessians':('(r/abs(v))**6','(r/abs(v))**4'),
 'omit_finite_pin_shift':('6*k*(u*u-Q(1,4))','6*k*u*u'),
 'drop_outer_aspect_direction':('[[aq*alpha,u*beta,Q(0)]','[[aq*alpha,Q(0),Q(0)]'),
 'insert_spurious_height_window':("'height_window_r_power':0","'height_window_r_power':3"),
 'self_award_mathematical_acceptance':("'mathematical_acceptance':False","'mathematical_acceptance':True"),
}


def require(ok,message):
    if not ok:
        raise RuntimeError(message)


def identities():
    pins=json.loads((ROOT/'SOURCE_FILES.json').read_text())['files']
    for name,entry in pins.items():
        require(PurePosixPath(name).name==name,'flat source filename required')
        p=ROOT/name
        require(p.is_file() and not p.is_symlink(),'regular file required')
        data=p.read_bytes()
        require(len(data)==entry['bytes'] and hashlib.sha256(data).hexdigest()==entry['sha256'],'identity mismatch: '+name)
    return pins


def run(command,cwd,out,name,mutant=False):
    r=subprocess.run(command,cwd=cwd,text=True,capture_output=True,timeout=30)
    (out/(name+'.stdout')).write_text(r.stdout)
    (out/(name+'.stderr')).write_text(r.stderr)
    require(f'Ran {EXPECTED} tests' in r.stderr and 'skipped=' not in r.stderr,'wrong test scope: '+name)
    if mutant:
        require(r.returncode!=0 and 'AssertionError' in r.stderr and 'FAILED (failures=' in r.stderr,'undetected mutant: '+name)
        require('\nERROR:' not in r.stderr and 'SyntaxError' not in r.stderr and 'ImportError' not in r.stderr,'invalid-program mutant: '+name)
    else:
        require(r.returncode==0,'baseline failed: '+name)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    out=p.parse_args().output.resolve()
    require(not out.exists() and not out.is_relative_to(ROOT),'new output outside source required')
    out.mkdir(parents=True)
    before=identities()
    source=(ROOT/'annulus_bridge.py').read_text()
    report={'passed':False,'python':sys.version,'distinct_tests':EXPECTED,
            'distinct_semantic_mutants':len(MUTANTS),'modes':[],
            'source_files':before,'scientific_effect':'NONE',
            'mathematical_acceptance':False,
            'meaning':'finite algebra/scaling replay, not continuum proof verification'}
    try:
        for mode,flags in [('normal',[]),('optimized',['-O'])]:
            cmd=[sys.executable,'-B',*flags,'-S','-m','unittest','-v','test_annulus_bridge']
            run(cmd,ROOT,out,'tests_'+mode)
            result=subprocess.run([sys.executable,'-B',*flags,'-S','annulus_bridge.py'],cwd=ROOT,capture_output=True,timeout=15)
            require(result.returncode==0 and result.stdout==(ROOT/'RESULTS.json').read_bytes(),'result mismatch')
            (out/('output_'+mode+'.json')).write_bytes(result.stdout)
            for name,(old,new) in MUTANTS.items():
                require(source.count(old)==1,'nonunique mutation: '+name)
                changed=source.replace(old,new)
                compile(changed,name,'exec')
                scratch=out/'mutants'/mode/name
                scratch.mkdir(parents=True)
                (scratch/'annulus_bridge.py').write_text(changed)
                shutil.copyfile(ROOT/'test_annulus_bridge.py',scratch/'test_annulus_bridge.py')
                run(cmd,scratch,out,'mutation_'+mode+'_'+name,True)
            report['modes'].append(mode)
        require(before==identities(),'sources changed during replay')
        report.update(passed=True,sources_unchanged=True)
    finally:
        (out/'REPORT.json').write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')
    print(json.dumps(report,sort_keys=True))


if __name__=='__main__':
    main()
