"""Run finite controls and semantic mutations. This does not certify analytic proofs."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
MUTANTS={
 'missing_inertia_filter':('if zero==0 and neg==index else Q(0)','if zero==0 else Q(0)'),
 'offdiagonal_r_squared':('return r*abs(adjugate_quadratic(a,beta))','return r*r*abs(adjugate_quadratic(a,beta))'),
 'wrong_contact_cancellation':('6/r**2*(fp(a)+fp(b)','6/r*(fp(a)+fp(b)'),
 'missing_height_jacobian':('return (d-1)+3-(d+3)+2','return (d-1)+2-(d+3)+2'),
 'wrong_outer_gap_power':("'outer_loss':1-Q(11,3)*split","'outer_loss':1-Q(8,3)*split"),
 'missing_holder_root':('return (3*(p-1)-beta)/p','return 3*(p-1)-beta'),
 'reverse_event_count':("'mean':n*probability","'mean':probability"),
 'wrong_original_block_size':('sizes=tuple(x*y+1 for x,y in zip(a,d))','sizes=tuple(x*y for x,y in zip(a,d))'),
 'sum_instead_of_product_price':('value*=p','value+=p'),
 'incomplete_transversal_family':('return frozenset(out)','return frozenset(sorted(out)[1:])'),
}

def check(condition,message):
    if not condition: raise RuntimeError(message)

def main():
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--output',required=True,type=Path)
    args=p.parse_args(); out=args.output.resolve()
    check(not out.exists() and not out.is_relative_to(ROOT),'new output outside source directory required')
    out.mkdir(parents=True); env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
    source=ROOT/'frontier_math.py'; tests=ROOT/'test_frontiers.py'
    original={x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in (source,tests)}
    text=source.read_text(); results=[]
    def run(cmd,cwd,label,mutation=False):
        proc=subprocess.run(cmd,cwd=cwd,env=env,capture_output=True,text=True,timeout=60)
        (out/(label+'.stdout')).write_text(proc.stdout)
        (out/(label+'.stderr')).write_text(proc.stderr)
        if mutation:
            check(proc.returncode!=0 and 'AssertionError' in proc.stderr,'mutant not assertion-detected: '+label)
        else:
            check(proc.returncode==0,'validation failed: '+label)
        return proc
    try:
        for mode,flags in (('normal',[]),('optimized',['-O'])):
            cmd=[sys.executable,'-B',*flags,'-S']
            baseline=run(cmd+['-m','unittest','-v','test_frontiers'],ROOT,'tests_'+mode)
            check('Ran 54 tests' in baseline.stderr and 'skipped=' not in baseline.stderr,'unexpected or skipped tests')
            actual=run(cmd+['frontier_math.py'],ROOT,'candidate_'+mode)
            check(actual.stdout.encode()==(ROOT/'RESULTS.json').read_bytes(),'output changed')
            for name,(old,new) in MUTANTS.items():
                check(text.count(old)==1,'nonunique mutation '+name)
                tmp=out/'mutations'/mode/name; tmp.mkdir(parents=True)
                (tmp/source.name).write_text(text.replace(old,new)); shutil.copyfile(tests,tmp/tests.name)
                run(cmd+['-m','unittest','-v','test_frontiers'],tmp,name+'_'+mode,True)
            results.append({'mode':mode,'tests_passed':54,'semantic_mutations_detected':len(MUTANTS)})
        check(original=={x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in (source,tests)},'original sources changed')
        report={'passed':True,'python':sys.version,'distinct_tests':54,'distinct_semantic_mutations':len(MUTANTS),
                'modes':results,'source_sha256':original,'sources_unchanged':True,
                'scope':'finite algebra, abstract probability examples and bounded original-coordinate P15 enumeration; not independent analytic review',
                'loop_cases':{'block_index_inequality_checks':3888,'three_by_three_determinant_comparisons':729,
                              'three_block_clutters':9,'clutter_cover_avoiding_sets':243},
                'not_claimed':['Gaussian samples','formal analytic proof','nonauthor acceptance','RN triple-integral evaluation','large P15 witness enumeration']}
        (out/'REPORT.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
        print(json.dumps(report,sort_keys=True))
    except Exception as exc:
        (out/'FAILURE.json').write_text(json.dumps({'error':str(exc),'completed_modes':results},indent=2)+'\n')
        raise

if __name__=='__main__': main()
