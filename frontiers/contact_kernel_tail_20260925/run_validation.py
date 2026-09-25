"""Source-pinned exact replay with preserved, assertion-detected semantic faults."""
import argparse, hashlib, json, shutil, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
EXPECTED=22
MUTANTS={
 'omit_q_jacobian_six':('return 104976*k**8','return 17496*k**8'),
 'wrong_transverse_power':('z0*abs(v)**13','z0*abs(v)**12'),
 'wrong_gap_power':('104976*k**8','104976*k**7'),
 'lose_finite_pin_shift':('c=12*k*(u*u+Q(1,4)-u*w)','c=12*k*(u*u-u*w)'),
 'signed_measure_jacobian':('return 6*k/abs(v)','return 6*k/v'),
 'omit_gamma_factorial':('Q(factorial(5),factorial(j))','Q(1,factorial(j))'),
 'omit_second_side':('return 2*B*C/c**6*P,x','return B*C/c**6*P,x'),
 'self_award_gluing':("'full_annulus_asymptotic_accepted':False","'full_annulus_asymptotic_accepted':True"),
}

def require(c,msg):
    if not c:raise RuntimeError(msg)

def pins():
    data=json.loads((ROOT/'SOURCE_FILES.json').read_text())['files']
    for name,spec in data.items():
        p=ROOT/name
        require(p.parent==ROOT and p.is_file() and not p.is_symlink(),'invalid source')
        raw=p.read_bytes()
        require(len(raw)==spec['bytes'] and hashlib.sha256(raw).hexdigest()==spec['sha256'],'source mismatch '+name)
    return data

def execute(cmd,cwd,out,name,mutant=False):
    result=subprocess.run(cmd,cwd=cwd,capture_output=True,text=True,timeout=30)
    (out/(name+'.stdout')).write_text(result.stdout)
    (out/(name+'.stderr')).write_text(result.stderr)
    require(f'Ran {EXPECTED} tests' in result.stderr and 'skipped=' not in result.stderr,'wrong test count')
    if mutant:
        require(result.returncode!=0 and 'AssertionError' in result.stderr and 'FAILED (failures=' in result.stderr,'mutant not detected '+name)
        require('\nERROR:' not in result.stderr and 'SyntaxError' not in result.stderr and 'ImportError' not in result.stderr,'invalid program mutant')
    else:require(result.returncode==0,'baseline failure '+name)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    out=parser.parse_args().output.resolve()
    require(not out.exists() and not out.is_relative_to(ROOT),'new output outside source required')
    out.mkdir(parents=True)
    identities=pins();source=(ROOT/'kernel_tail.py').read_text()
    report={'passed':False,'python':sys.version,'tests':EXPECTED,'mutants':len(MUTANTS),'modes':[],
            'sources':identities,'scientific_effect':'NONE','analytic_acceptance':False}
    try:
        for mode,flags in [('normal',[]),('optimized',['-O'])]:
            cmd=[sys.executable,'-B',*flags,'-S','-m','unittest','-v','test_kernel_tail']
            execute(cmd,ROOT,out,'tests_'+mode)
            actual=subprocess.run([sys.executable,'-B',*flags,'-S','kernel_tail.py'],cwd=ROOT,capture_output=True,timeout=15)
            require(actual.returncode==0 and actual.stdout==(ROOT/'RESULTS.json').read_bytes(),'output mismatch')
            (out/('results_'+mode+'.json')).write_bytes(actual.stdout)
            for name,(old,new) in MUTANTS.items():
                require(source.count(old)==1,'mutation not unique '+name)
                changed=source.replace(old,new);compile(changed,name,'exec')
                scratch=out/'mutants'/mode/name;scratch.mkdir(parents=True)
                (scratch/'kernel_tail.py').write_text(changed)
                shutil.copyfile(ROOT/'test_kernel_tail.py',scratch/'test_kernel_tail.py')
                execute(cmd,scratch,out,mode+'_'+name,True)
            report['modes'].append(mode)
        require(identities==pins(),'sources changed')
        report.update(passed=True,sources_unchanged=True)
    finally:(out/'REPORT.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps(report,sort_keys=True))
if __name__=='__main__':main()
