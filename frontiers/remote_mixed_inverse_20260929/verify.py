"""Verify the flat source packet and both-mode finite semantic controls.

No network, external dependencies, repository writes or Gaussian-proof claim.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT=Path(__file__).resolve().parent
MUTANTS={
 'lose-cubic-gap':'test_cubic_gap_domain',
 'include-boundary':'test_strict_endpoint',
 'omit-triangle-half':'test_beta_normalization_by_integer_substitution',
 'uncoupled-denominator':'test_coefficient_parts',
 'normalized-not-physical-gap':'test_physical_gap_not_normalized_gap',
 'retain-beta-in-T':'test_T_exponent_beta_cancels',
 'wrong-height-frame':'test_dimension_cancellation_and_fixed_r_boundary',
 'independent-heights':'test_height_correlation',
}

def require(ok,message):
    if not ok:
        raise ValueError(message)

def decode(text):
    def unique(items):
        answer={}
        for key,value in items:
            require(key not in answer,'duplicate JSON key: '+key)
            answer[key]=value
        return answer
    return json.loads(text,object_pairs_hook=unique)

def identity(path):
    require(path.is_file() and not path.is_symlink(),'regular source required')
    data=path.read_bytes()
    return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),
            'git_blob':hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()}

def sources():
    identity(ROOT/'SOURCE_FILES.json')
    entries=decode((ROOT/'SOURCE_FILES.json').read_text())['files']
    names=[entry['path'] for entry in entries]
    require(len(names)==len(set(names)) and all(Path(n).name==n and n!='SOURCE_FILES.json' for n in names),
            'unique flat source paths required')
    require(sorted(p.name for p in ROOT.iterdir())==sorted(names+['SOURCE_FILES.json']),
            'source membership differs')
    for entry in entries:
        require(identity(ROOT/entry['path'])=={k:entry[k] for k in ('bytes','sha256','git_blob')},
                'source identity differs: '+entry['path'])
    return {p.name:identity(p) for p in sorted(ROOT.iterdir())}

def child(mutant):
    import mixed
    import test_mixed
    mixed.MUTANT=mutant
    suite=unittest.defaultTestLoader.loadTestsFromModule(test_mixed)
    result=unittest.TextTestRunner(stream=io.StringIO()).run(suite)
    print(json.dumps({'tests':result.testsRun,'passed':result.wasSuccessful(),
          'failures':sorted(t.id().rsplit('.',1)[-1] for t,_ in result.failures),
          'errors':sorted(t.id().rsplit('.',1)[-1] for t,_ in result.errors)},sort_keys=True))
    return 0 if result.wasSuccessful() else 1

def replay(output):
    output=output.resolve()
    require(not output.exists() and not output.is_relative_to(ROOT),'new output outside packet required')
    before=sources()
    output.mkdir(parents=True)
    cases={}
    for case in ['baseline',*MUTANTS]:
        pair=[]
        for mode,flags in (('normal',[]),('optimized',['-O'])):
            cmd=[sys.executable,'-B',*flags,'-S',str(ROOT/'verify.py'),'--child']
            if case!='baseline':
                cmd+=['--mutant',case]
            run=subprocess.run(cmd,capture_output=True,timeout=30)
            (output/(case+'_'+mode+'.stdout')).write_bytes(run.stdout)
            (output/(case+'_'+mode+'.stderr')).write_bytes(run.stderr)
            result=decode(run.stdout.decode())
            require(not run.stderr and not result['errors'],'execution error: '+case)
            require(result['tests']==18,'wrong test count')
            if case=='baseline':
                require(run.returncode==0 and result['passed'] and not result['failures'],'baseline failed')
            else:
                require(run.returncode==1 and not result['passed'] and MUTANTS[case] in result['failures'],
                        'intended semantic assertion did not reject: '+case)
            pair.append(run.stdout)
        require(pair[0]==pair[1],'normal and optimized outputs differ: '+case)
        cases[case]=decode(pair[0].decode())
    summary={'tests_per_mode':18,'semantic_mutants_per_mode':8,'identical_output_pairs':9,
             'all_intended_failures':True,'scientific_effect':'NONE','continuum_proof_verified_by_code':False}
    require(summary==decode((ROOT/'RESULTS.json').read_text()),'stored summary differs')
    require(before==sources(),'source changed during replay')
    (output/'REPORT.json').write_text(json.dumps({**summary,'cases':cases,'source_identities':before,
                                                'sources_unchanged':True},indent=2,sort_keys=True)+'\n')
    print(json.dumps(summary,indent=2,sort_keys=True))
    return 0

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--child',action='store_true')
    group.add_argument('--output',type=Path)
    parser.add_argument('--mutant',choices=MUTANTS)
    args=parser.parse_args()
    require(args.child or args.mutant is None,'mutant requires child mode')
    raise SystemExit(child(args.mutant) if args.child else replay(args.output))
