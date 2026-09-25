"""Bounded source-identity, exact-algebra and semantic-mutation replay."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parent
MUTATIONS={
    'drop_pin_offset': ('offset = u*u - F(1,4)','offset = u*u'),
    'drop_unconditioned_counterterm': ('gx - hprime - r*r*w*lp','gx - hprime'),
    'wrong_longitudinal_scale': (') / r**3,',') / r**2,'),
    'wrong_density_jacobian': ('return r**5','return r**4'),
    'wrong_hermite_first_derivative': ('(3*D0-S1)/2','D0'),
}


def hashes():
    return {p.name:hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(ROOT.iterdir()) if p.name in
            ('contact.py','test_contact.py','run_validation.py','PROOF.md','RECONNAISSANCE.md')}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    out=args.output.resolve()
    if out==ROOT or ROOT in out.parents:
        parser.error('Output must be outside the source directory')
    out.mkdir(parents=True,exist_ok=False)
    before=hashes()
    source=(ROOT/'contact.py').read_text()
    reports=[]
    for mode,flags in [('normal',[]),('optimized',['-O'])]:
        command=[sys.executable,*flags,'-B','-S','-m','unittest','test_contact','-v']
        proc=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=30)
        (out/f'{mode}.log').write_text(proc.stdout+proc.stderr)
        passed=proc.returncode==0 and 'Ran 15 tests' in proc.stderr and '\nOK\n' in proc.stderr
        mutants={}
        for name,(old,new) in MUTATIONS.items():
            if source.count(old)!=1:
                raise RuntimeError(f'Mutation anchor is not unique: {name}')
            with tempfile.TemporaryDirectory(prefix='axial-mutant-') as temp:
                folder=Path(temp)
                shutil.copyfile(ROOT/'test_contact.py',folder/'test_contact.py')
                (folder/'contact.py').write_text(source.replace(old,new))
                run=subprocess.run(command,cwd=folder,capture_output=True,text=True,timeout=30)
            log=run.stdout+run.stderr
            (out/f'{mode}_{name}.log').write_text(log)
            # Reject crashes, import failures and unexercised mutations as evidence.
            mutants[name]=(run.returncode==1 and 'FAILED (failures=' in run.stderr
                           and 'ERROR:' not in run.stderr and 'AssertionError' in run.stderr)
        reports.append({'mode':mode,'tests_passed':passed,'distinct_tests':15,
                        'mutants_assertion_detected':mutants})
    after=hashes()
    result={'python':sys.version,'source_sha256':before,'source_unchanged':before==after,
            'runs':reports,'passed':before==after and all(x['tests_passed'] and all(x['mutants_assertion_detected'].values()) for x in reports),
            'scope':'Exact algebra only. No covariance enclosure, analytic acceptance, full-repository or hosted-CI claim.'}
    (out/'REPORT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    return 0 if result['passed'] else 1


if __name__=='__main__':
    raise SystemExit(main())
