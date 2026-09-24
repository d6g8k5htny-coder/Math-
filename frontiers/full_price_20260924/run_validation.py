"""Replay exact finite tests and deliberate faults; outputs must be a new directory."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
MUTATIONS={
 'concavity_sign':('return -A*B*z/(A+B*z)**2','return A*B*z/(A+B*z)**2'),
 'admit_demand_one':("'full_price_uniform_guarantee':d>=2","'full_price_uniform_guarantee':d>=1"),
 'omit_extra_original_vertex':("'block_size':a*d+1","'block_size':a*d"),
 'drop_probability_one_cap':('return Q(1), Q(1)','return Q(0), Q(0)'),
 'wrong_reference_size':('def reference_bounds(n=3, a=1):','def reference_bounds(n=2, a=1):'),
 'lose_capacity_boundary':('return sum(state, Q(0))','return sum(state[:-1], Q(0))'),
 'omit_log_tail':('return total, total+tail','return total, total-tail'),
}

def run(argv, cwd, out, name, fail=False):
    p=subprocess.run(argv,cwd=cwd,capture_output=True,text=True,timeout=45)
    (out/(name+'.stdout')).write_text(p.stdout)
    (out/(name+'.stderr')).write_text(p.stderr)
    if fail:
        if p.returncode==0 or 'AssertionError' not in p.stderr:
            raise RuntimeError('mutant not caught by an assertion: '+name)
    elif p.returncode or 'Ran 36 tests' not in p.stderr or 'skipped=' in p.stderr:
        raise RuntimeError('baseline failed or incomplete: '+name)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True,type=Path)
    parser.add_argument('--mode',choices=['normal','optimized','both'],default='both')
    opts=parser.parse_args()
    out=opts.output.resolve()
    if out.exists() or out.is_relative_to(ROOT): raise ValueError('new external output path required')
    out.mkdir(parents=True)
    paths=sorted(p for p in ROOT.iterdir() if p.is_file())
    identity={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    source=(ROOT/'full_price.py').read_text()
    modes=[('normal',[]),('optimized',['-O'])]
    modes=[m for m in modes if opts.mode=='both' or m[0]==opts.mode]
    for mode,flags in modes:
        args=[sys.executable,'-B',*flags,'-S','-m','unittest','-v','test_full_price']
        run(args,ROOT,out,'baseline_'+mode)
        calc=subprocess.run([sys.executable,'-B',*flags,'-S','full_price.py'],cwd=ROOT,capture_output=True,timeout=30)
        (out/('output_'+mode+'.json')).write_bytes(calc.stdout)
        if calc.returncode or calc.stdout!=(ROOT/'RESULTS.json').read_bytes(): raise RuntimeError('output mismatch')
        for name,(old,new) in MUTATIONS.items():
            if source.count(old)!=1: raise ValueError('mutation site not unique: '+name)
            scratch=out/'mutants'/mode/name;scratch.mkdir(parents=True)
            (scratch/'full_price.py').write_text(source.replace(old,new))
            shutil.copyfile(ROOT/'test_full_price.py',scratch/'test_full_price.py')
            run(args,scratch,out,name+'_'+mode,fail=True)
    if identity!={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}: raise RuntimeError('source changed')
    report={'passed':True,'distinct_tests':36,'distinct_semantic_mutations':len(MUTATIONS),
            'modes':[m[0] for m in modes],'python':sys.version,'sources_unchanged':True,
            'source_sha256':identity,'meaning':'same-author finite checks; not nonauthor analytic acceptance'}
    (out/'REPORT.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps(report,sort_keys=True))

if __name__=='__main__': main()
