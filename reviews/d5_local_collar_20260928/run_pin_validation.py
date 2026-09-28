"""Replay only finite rational controls and their deliberate mutants.

This is not a Gaussian integrator, a continuum proof checker, or scientific
acceptance. No network operations. Require a new output directory outside the
source tree; preserve unmodified source identities and complete process logs.
"""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
MUTANTS = {
    'omit_quartic_axis_column': ('a*alpha, c*beta', 'F(0), c*beta'),
    'omit_mixed_axis_column': ('[F(0), b*alpha, beta, F(0)]', '[F(0), F(0), beta, F(0)]'),
    'erase_endpoint_remainder_factor': ('return r**4*p*(5*p**3-9*p+4)', 'return r**4*(5*p**3-9*p+4)'),
    'drop_original_normalizer': ('normalizer_power = -2', 'normalizer_power = 0'),
    'insert_spurious_height_factor': ('height_window_power = 0', 'height_window_power = 3'),
    'exclude_axis_as_if_it_were_the_pin': ('return 0<r<=1 and 0<p*p+q*q<=F(1,16)',
                                        'return 0<r<=1 and q!=0 and 0<p*p+q*q<=F(1,16)'),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def identity(path: Path) -> dict:
    require(path.is_file() and not path.is_symlink(), 'regular file required: '+path.name)
    data=path.read_bytes()
    return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),
            'git_blob':hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()}


def snapshot() -> dict:
    return {p.name:identity(p) for p in sorted(ROOT.iterdir()) if p.is_file()}


def execute(command: list[str], cwd: Path, out: Path, label: str, mutant: bool) -> dict:
    proc=subprocess.run(command,cwd=cwd,capture_output=True,timeout=30)
    stdout,stderr=proc.stdout,proc.stderr
    (out/(label+'.stdout')).write_bytes(stdout)
    (out/(label+'.stderr')).write_bytes(stderr)
    text=stderr.decode('utf-8','replace')
    require('Ran 11 tests' in text and 'skipped=' not in text,'wrong coverage: '+label)
    if mutant:
        require(proc.returncode!=0 and 'AssertionError' in text and 'FAILED (failures=' in text,
                'mutant not rejected by assertions: '+label)
        require('errors=' not in text and 'SyntaxError' not in text and 'ImportError' not in text,
                'invalid-program failure is not a detection: '+label)
    else:
        require(proc.returncode==0 and text.rstrip().endswith('OK'),'baseline failed: '+label)
    return {'exit_code':proc.returncode,
            'stdout_sha256':hashlib.sha256(stdout).hexdigest(),
            'stderr_sha256':hashlib.sha256(stderr).hexdigest(),
            'assertion_rejected':mutant}


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args()
    out=args.output.resolve()
    require(not out.exists() and not out.is_relative_to(ROOT),
            'use a new output directory outside the source tree')
    out.mkdir(parents=True)
    before=snapshot()
    code=(ROOT/'pin_frame.py').read_text()
    test_bytes=(ROOT/'test_pin_frame.py').read_bytes()
    report={'passed':False,'scientific_effect':'NONE','remote_ci':False,
            'continuum_proof_checked':False,'python':sys.version,'modes':{},'source_files':before}
    summaries=[]
    try:
        for mode,flags in [('normal',[]),('optimized',['-O'])]:
            cmd=[sys.executable,'-B',*flags,'-S','-m','unittest','-v','test_pin_frame']
            records={'baseline':execute(cmd,ROOT,out,'baseline_'+mode,False),'mutations':{}}
            for label,(old,new) in MUTANTS.items():
                require(code.count(old)==1,'nonunique mutation target: '+label)
                scratch=out/'mutants'/mode/label
                scratch.mkdir(parents=True)
                (scratch/'pin_frame.py').write_text(code.replace(old,new),encoding='utf-8')
                (scratch/'test_pin_frame.py').write_bytes(test_bytes)
                records['mutations'][label]=execute(cmd,scratch,out,label+'_'+mode,True)
            report['modes'][mode]=records
            summary={'distinct_tests':11,'quartic_gradient_fixtures':192,
                     'principal_minor_fixtures':75,'gram_floor_fixtures':216,
                     'distinct_mutants':len(MUTANTS),'baseline_passed':True,
                     'all_mutants_assertion_rejected':True,'scientific_effect':'NONE',
                     'continuum_proof_checked':False}
            raw=(json.dumps(summary,indent=2,sort_keys=True)+'\n').encode()
            (out/('finite_summary_'+mode+'.json')).write_bytes(raw)
            summaries.append(raw)
        require(summaries[0]==summaries[1],'normal/optimized finite result mismatch')
        require(snapshot()==before,'source files changed during validation')
        expected=ROOT/'PIN_RESULTS.json'
        if expected.exists():
            require(expected.read_bytes()==summaries[0],'stored finite result mismatch')
        report.update(passed=True,sources_unchanged=True,finite_summaries_byte_identical=True)
    finally:
        (out/'REPORT.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(summaries[0].decode(),end='')

if __name__=='__main__':
    main()
