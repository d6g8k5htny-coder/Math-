"""Source-pinned finite-pin validation; no mathematical acceptance is inferred."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
EXPECTED = 21
MUTANTS = {
    'omit_longitudinal_pin_offset': ('gx=6*k*(u*u-Q(1,4))', 'gx=6*k*u*u'),
    'omit_axial_transverse_pin_offset': ('gy_axial=Q(1,2)*q*(u*u-Q(1,4))', 'gy_axial=Q(1,2)*q*u*u'),
    'omit_midpoint_height_and_linear_offset': ('k*(2*u**3-Q(3,2)*u-Q(1,2))', 'k*(2*u**3)'),
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def verify_sources():
    pins = json.loads((ROOT/'SOURCE_FILES.json').read_text())['files']
    for name, identity in pins.items():
        path = ROOT/name
        require(path.is_file() and not path.is_symlink(), 'regular source required: '+name)
        raw = path.read_bytes()
        require(len(raw)==identity['bytes'] and hashlib.sha256(raw).hexdigest()==identity['sha256'], 'source mismatch: '+name)
    return pins


def run(command, cwd, out, name, mutant=False):
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True, timeout=30)
    (out/(name+'.stdout')).write_text(result.stdout)
    (out/(name+'.stderr')).write_text(result.stderr)
    require(f'Ran {EXPECTED} tests' in result.stderr and 'skipped=' not in result.stderr, 'unexpected coverage: '+name)
    if mutant:
        require(result.returncode != 0 and 'AssertionError' in result.stderr and 'FAILED (failures=' in result.stderr,
                'mutant not assertion-detected: '+name)
        require('\nERROR:' not in result.stderr and 'SyntaxError' not in result.stderr and 'ImportError' not in result.stderr,
                'invalid-program mutant: '+name)
    else:
        require(result.returncode==0, 'baseline failed: '+name)
    return {'returncode':result.returncode, 'stderr_sha256':hashlib.sha256(result.stderr.encode()).hexdigest()}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True,type=Path)
    out=parser.parse_args().output.resolve()
    require(not out.exists() and not out.is_relative_to(ROOT), 'new output outside source required')
    out.mkdir(parents=True)
    pins=verify_sources()
    source=(ROOT/'finite_r_contact.py').read_text()
    report={'passed':False,'python':sys.version,'distinct_tests':EXPECTED,
            'distinct_semantic_mutants':len(MUTANTS),'modes':[], 'sources':pins,
            'mathematical_acceptance':False,'scientific_effect':'NONE',
            'meaning':'exact finite regression controls; analytic C6 argument needs independent review'}
    try:
        for mode, flags in [('normal',[]),('optimized',['-O'])]:
            cmd=[sys.executable,'-B',*flags,'-S','-m','unittest','discover','-p','test_*.py','-v']
            run(cmd,ROOT,out,'tests_'+mode)
            for name,(old,new) in MUTANTS.items():
                require(source.count(old)==1,'nonunique mutation: '+name)
                mutated=source.replace(old,new)
                compile(mutated,'<'+name+'>','exec')
                scratch=out/'mutants'/mode/name
                shutil.copytree(ROOT,scratch,ignore=shutil.ignore_patterns('__pycache__'))
                (scratch/'finite_r_contact.py').write_text(mutated)
                run(cmd,scratch,out,'mutation_'+mode+'_'+name,mutant=True)
            report['modes'].append(mode)
        require(pins==verify_sources(),'sources changed')
        report.update(passed=True,sources_unchanged=True)
    finally:
        (out/'REPORT.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps(report,sort_keys=True))


if __name__=='__main__':
    main()
