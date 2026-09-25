"""Source-bound local/CI algebra replay. No scientific-state writes or network."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parent
MUTANTS={
    'missing_axis_column':('p.mul(a,alpha),p.mul(p.u,beta),{}','{},p.mul(p.u,beta),{}'),
    'missing_outer_column':('[{},p.mul(b,alpha),beta]','[{},p.mul(b,alpha),{}]'),
    'unshifted_gap':('p.constant(Q(-1,4))','p.constant(Q(0))'),
    'wrong_quartic_coefficient':('p.scale(p.mul(p.u,gap),Q(1,6))','p.scale(p.mul(p.u,gap),Q(1,3))'),
    'wrong_count_power':('return -3-7*gamma','return -2-7*gamma'),
}

def identities():
    return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(ROOT.iterdir()) if p.is_file()}

def require(condition,message):
    if not condition:raise RuntimeError(message)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True,type=Path)
    output=parser.parse_args().output.resolve()
    require(not output.exists() and not output.is_relative_to(ROOT),'new output outside source required')
    output.mkdir(parents=True)
    source=(ROOT/'two_scale.py').read_text(); before=identities(); outcomes=[]
    for mode,flags in [('normal',[]),('optimized',['-O'])]:
        command=[sys.executable,'-B','-S',*flags,'-m','unittest','discover','-p','test_*.py','-v']
        for name,mutation in [('baseline',None),*MUTANTS.items()]:
            with tempfile.TemporaryDirectory() as temporary:
                work=Path(temporary)
                for filename in ('thin_tube.py','test_thin_tube.py','two_scale.py','test_two_scale.py'):
                    shutil.copyfile(ROOT/filename,work/filename)
                if mutation:
                    old,new=mutation
                    require(source.count(old)==1,'nonunique mutation '+name)
                    mutated=source.replace(old,new);compile(mutated,name,'exec')
                    (work/'two_scale.py').write_text(mutated)
                result=subprocess.run(command,cwd=work,capture_output=True,text=True,timeout=30)
                log=result.stdout+result.stderr
                (output/f'{mode}-{name}.txt').write_text(log)
                require('Ran 28 tests' in log and 'skipped=' not in log,'coverage mismatch '+name)
                if mutation:
                    require(result.returncode!=0 and 'AssertionError' in log and 'FAILED (failures=' in log
                            and '\nERROR:' not in log and 'errors=' not in log,'mutant not assertion-detected '+name)
                else:require(result.returncode==0,'baseline failed '+mode)
                outcomes.append({'mode':mode,'case':name,'returncode':result.returncode,'log_sha256':hashlib.sha256(log.encode()).hexdigest()})
        for module in ('thin_tube.py','two_scale.py'):
            result=subprocess.run([sys.executable,'-B','-S',*flags,str(ROOT/module)],capture_output=True,check=True,timeout=10)
            (output/f'{mode}-{module}.json').write_bytes(result.stdout)
    require(before==identities(),'sources changed during replay')
    report={'object':'D5-TWO-SCALE-20260925-v1','python':sys.version,'distinct_tests':28,
            'old_tests':15,'new_tests':13,'semantic_mutants':len(MUTANTS),'modes':['normal','optimized'],
            'passed':True,'source_hashes':before,'outcomes':outcomes,
            'scientific_effect':'NONE','analytic_verification':False,'independent_review':False}
    (output/'REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('passed','distinct_tests','semantic_mutants','modes','scientific_effect')}))

if __name__=='__main__':main()
