"""Exact packet and finite semantic verification; not a Gaussian-proof verifier."""
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
 'wrong-rarity':'test_rare_first_moment',
 'planar-only-cap':'test_arbitrary_fixed_dimension',
 'ordinary-not-factorial':'test_second_factorial_exact',
 'nonempty-not-size-biased':'test_size_bias_differs_from_nonempty_conditioning',
 'drop-normalizer':'test_full_normalizer_once',
 'omit-prescribed-pins':'test_prescribed_pin_offset',
}

def require(ok,message):
    if not ok:raise ValueError(message)

def decode(data):
    def unique(items):
        result={}
        for k,v in items:
            require(k not in result,'duplicate JSON key: '+k)
            result[k]=v
        return result
    return json.loads(data,object_pairs_hook=unique)

def identity(path):
    require(path.is_file() and not path.is_symlink(),'regular source required')
    data=path.read_bytes()
    return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),
            'git_blob':hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()}

def sources():
    identity(ROOT/'SOURCE_FILES.json')
    entries=decode((ROOT/'SOURCE_FILES.json').read_text())['files']
    names=[e['path'] for e in entries]
    require(len(names)==len(set(names)) and all(Path(n).name==n and n!='SOURCE_FILES.json' for n in names),'unique flat paths required')
    require(sorted(p.name for p in ROOT.iterdir())==sorted(names+['SOURCE_FILES.json']),'packet membership differs')
    for e in entries:
        require(identity(ROOT/e['path'])=={k:e[k] for k in ('bytes','sha256','git_blob')},'source identity differs: '+e['path'])
    return {p.name:identity(p) for p in sorted(ROOT.iterdir())}

def child(mutant):
    import barrier
    import test_barrier
    barrier.MUTANT=mutant
    suite=unittest.defaultTestLoader.loadTestsFromModule(test_barrier)
    result=unittest.TextTestRunner(stream=io.StringIO()).run(suite)
    print(json.dumps({'tests':result.testsRun,'passed':result.wasSuccessful(),
                     'failures':sorted(t.id().rsplit('.',1)[-1] for t,_ in result.failures),
                     'errors':sorted(t.id().rsplit('.',1)[-1] for t,_ in result.errors)},sort_keys=True))
    return 0 if result.wasSuccessful() else 1

def replay(output):
    output=output.resolve()
    require(not output.exists() and not output.is_relative_to(ROOT),'new output outside packet required')
    before=sources();output.mkdir(parents=True)
    cases={}
    for case in ['baseline',*MUTANTS]:
        pair=[]
        for mode,flags in [('normal',[]),('optimized',['-O'])]:
            cmd=[sys.executable,'-B',*flags,'-S',str(ROOT/'verify.py'),'--child']
            if case!='baseline':cmd+=['--mutant',case]
            run=subprocess.run(cmd,capture_output=True,timeout=30)
            (output/(case+'_'+mode+'.stdout')).write_bytes(run.stdout)
            (output/(case+'_'+mode+'.stderr')).write_bytes(run.stderr)
            value=decode(run.stdout.decode())
            require(not run.stderr and not value['errors'],'execution error: '+case)
            require(value['tests']==15,'unexpected test count')
            if case=='baseline':
                require(run.returncode==0 and value['passed'] and not value['failures'],'baseline failed')
            else:
                require(run.returncode==1 and not value['passed'] and MUTANTS[case] in value['failures'],'intended semantic failure missing: '+case)
            pair.append(run.stdout)
        require(pair[0]==pair[1],'Python modes disagree: '+case)
        cases[case]=decode(pair[0].decode())
    result={'tests_per_mode':15,'semantic_mutants_per_mode':6,'identical_output_pairs':7,
            'scientific_effect':'NONE','gaussian_analysis_verified':False}
    require(result==decode((ROOT/'RESULTS.json').read_text()),'stored summary differs')
    require(sources()==before,'source changed during execution')
    (output/'REPORT.json').write_text(json.dumps({**result,'cases':cases,'source_identities':before,'sources_unchanged':True},indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))
    return 0

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--child',action='store_true');group.add_argument('--output',type=Path)
    parser.add_argument('--mutant',choices=MUTANTS)
    args=parser.parse_args()
    require(args.child or args.mutant is None,'mutant requires child mode')
    raise SystemExit(child(args.mutant) if args.child else replay(args.output))
