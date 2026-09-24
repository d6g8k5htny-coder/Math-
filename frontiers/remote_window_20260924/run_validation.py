"""Replay exact finite controls in both Python modes; preserve all mutation logs."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
MUTANTS = {
    'omit_cross_covariance': ('return x*y + 2*c*c','return x*y'),
    'wrong_height_power': ('return k*r**3','return k*r**2'),
    'repeat_normalizer': ('normalizer_power = 2','normalizer_power = 2*witnesses'),
    'repeat_endpoint_weight': ("'determinant_factors': witnesses+2","'determinant_factors': 3*witnesses"),
    'drop_pin_factor': ('[12/r**3,6/r**2,-12/r**3,6/r**2]','[6/r**3,3/r**2,-6/r**3,3/r**2]'),
    'drop_index_filter': ('return abs(determinant(a)) if inertia(a)[0] == index else Q(0)','return abs(determinant(a))'),
    'forget_ordering': ("'unordered_divisor': factorial(witnesses)","'unordered_divisor': 1"),
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def identities():
    return {p.name: {'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
            for p in ROOT.iterdir() if p.is_file()}


def execute(command, cwd, out, name, mutant=False):
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True, timeout=30)
    (out/(name+'.stdout')).write_text(result.stdout)
    (out/(name+'.stderr')).write_text(result.stderr)
    if mutant:
        require(result.returncode != 0 and 'AssertionError' in result.stderr and 'FAILED (failures=' in result.stderr,
                'mutation was not detected by a test assertion: '+name)
        require('SyntaxError' not in result.stderr and 'ImportError' not in result.stderr,
                'mutation caused an invalid-program error')
    else:
        require(result.returncode == 0, 'baseline failed: '+name)
        require('Ran 28 tests' in result.stderr and 'skipped=' not in result.stderr, 'unexpected test coverage')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args()
    out=args.output.resolve()
    require(not out.exists() and not out.is_relative_to(ROOT),'a new output outside the source directory is required')
    out.mkdir(parents=True)
    before=identities()
    source=(ROOT/'remote_window.py').read_text()
    report={'passed':False,'python':sys.version,'distinct_tests':28,
            'distinct_semantic_mutations':len(MUTANTS),'modes':[],
            'meaning':'same-author finite algebra/implementation checks; not numerical Gaussian integration or independent proof review'}
    try:
        for mode,flags in [('normal',[]),('optimized',['-O'])]:
            cmd=[sys.executable,'-B',*flags,'-S','-m','unittest','-v','test_remote_window']
            execute(cmd,ROOT,out,'tests_'+mode)
            output=subprocess.run([sys.executable,'-B',*flags,'-S','remote_window.py'],cwd=ROOT,capture_output=True,timeout=10)
            require(output.returncode==0 and output.stdout==(ROOT/'RESULTS.json').read_bytes(),'result byte mismatch')
            (out/('output_'+mode+'.json')).write_bytes(output.stdout)
            for name,(old,new) in MUTANTS.items():
                require(source.count(old)==1,'nonunique mutation: '+name)
                scratch=out/'mutants'/mode/name
                scratch.mkdir(parents=True)
                (scratch/'remote_window.py').write_text(source.replace(old,new))
                for filename in ('test_remote_window.py','RESULTS.json'):
                    shutil.copyfile(ROOT/filename,scratch/filename)
                execute(cmd,scratch,out,'mutation_'+mode+'_'+name,mutant=True)
            report['modes'].append(mode)
        require(before==identities(),'source files changed during execution')
        report.update(passed=True,sources_unchanged=True,source_files=before)
    finally:
        (out/'REPORT.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps(report,sort_keys=True))


if __name__=='__main__':
    main()
