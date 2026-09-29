"""Verify exact source membership and both-mode finite controls. Standard library only."""
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
 'omit-monomial':'test_clearing_keeps_laurent_values',
 'degree-without-dimension':'test_total_degree_attains_2dm',
 'planar-cap-everywhere':'test_cap_dimension_not_always_planar',
 'exponential-all-dimensions':'test_count_tail_power',
 'oversized-lipschitz-cutoff':'test_all_three_cutoff_terms_decay',
 'planar-log-everywhere':'test_factorial_logarithm_exponents',
 'single-cutoff-event':'test_measurable_degree_is_a_union',
 'drop-conditional-mean':'test_conditional_mean_must_be_retained',
 'drop-cauchy-square-root':'test_original_tilt_keeps_square_root',
}

def require(ok,message):
    if not ok: raise ValueError(message)

def loads(text):
    def pairs(items):
        d={}
        for k,v in items:
            require(k not in d,'duplicate JSON key: '+k);d[k]=v
        return d
    return json.loads(text,object_pairs_hook=pairs)

def identity(path):
    require(path.is_file() and not path.is_symlink(),'regular source required: '+str(path))
    b=path.read_bytes()
    return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),
            'git_blob':hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()}

def sources():
    identity(ROOT/'SOURCE_FILES.json')
    entries=loads((ROOT/'SOURCE_FILES.json').read_text())['files']
    names=[e['path'] for e in entries]
    require(len(names)==len(set(names)) and all(Path(n).name==n and n!='SOURCE_FILES.json' for n in names),'flat unique paths required')
    require(sorted(p.name for p in ROOT.iterdir())==sorted(names+['SOURCE_FILES.json']),'source membership differs')
    for e in entries:
        require(identity(ROOT/e['path'])=={k:e[k] for k in ('bytes','sha256','git_blob')},'source identity differs: '+e['path'])
    return {p.name:identity(p) for p in sorted(ROOT.iterdir())}

def upstream(repo):
    repo=repo.resolve()
    data=loads((ROOT/'SOURCE_MAP.json').read_text())
    for e in data['sources']:
        rel=Path(e['path'])
        require(not rel.is_absolute() and '..' not in rel.parts,'upstream path escapes root')
        require(not any(repo.joinpath(*rel.parts[:i]).is_symlink() for i in range(1,len(rel.parts)+1)),'upstream symlink')
        actual=identity(repo/rel)
        require(actual['sha256']==e['sha256'] and actual['git_blob']==e['git_blob'],'upstream identity differs: '+e['id'])
    return len(data['sources'])

def child(mutant):
    import fourier, test_fourier
    fourier.MUTANT=mutant
    result=unittest.TextTestRunner(stream=io.StringIO()).run(unittest.defaultTestLoader.loadTestsFromModule(test_fourier))
    payload={'tests':result.testsRun,'passed':result.wasSuccessful(),
             'failures':sorted(t.id().split('.')[-1] for t,_ in result.failures),
             'errors':sorted(t.id().split('.')[-1] for t,_ in result.errors)}
    print(json.dumps(payload,sort_keys=True))
    return 0 if result.wasSuccessful() else 1

def replay(out,repo):
    out=out.resolve()
    require(not out.exists() and not out.is_relative_to(ROOT),'new external output directory required')
    before=sources(); up=upstream(repo) if repo else None
    out.mkdir(parents=True)
    records={}
    for name in ['baseline',*MUTANTS]:
        outputs=[]
        for mode,flags in [('normal',[]),('optimized',['-O'])]:
            cmd=[sys.executable,'-B',*flags,'-S',str(ROOT/'verify.py'),'--child']
            if name!='baseline':cmd+=['--mutant',name]
            p=subprocess.run(cmd,capture_output=True,timeout=30)
            (out/(name+'_'+mode+'.stdout')).write_bytes(p.stdout)
            (out/(name+'_'+mode+'.stderr')).write_bytes(p.stderr)
            result=loads(p.stdout.decode())
            require(not p.stderr and not result['errors'] and result['tests']==18,'execution error or wrong count: '+name)
            if name=='baseline':require(p.returncode==0 and result['passed'] and not result['failures'],'baseline failed')
            else:require(p.returncode==1 and not result['passed'] and MUTANTS[name] in result['failures'],'intended semantic failure missing: '+name)
            outputs.append(p.stdout)
        require(outputs[0]==outputs[1],'mode outputs differ: '+name)
        records[name]=loads(outputs[0].decode())
    summary={'tests_per_mode':18,'mutants_per_mode':9,'identical_output_pairs':10,
             'scientific_effect':'NONE','analytic_acceptance':False}
    require(summary==loads((ROOT/'RESULTS.json').read_text()),'stored summary differs')
    require(sources()==before,'sources changed during execution')
    report={**summary,'sources_unchanged':True,'upstream_verified_count':up,
            'source_identities':before,'cases':records}
    (out/'REPORT.json').write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')
    print(json.dumps(summary,sort_keys=True,indent=2))
    return 0

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--child',action='store_true');g.add_argument('--output',type=Path)
    p.add_argument('--mutant',choices=MUTANTS);p.add_argument('--repo',type=Path)
    a=p.parse_args();require(a.child or a.mutant is None,'mutant needs child mode')
    raise SystemExit(child(a.mutant) if a.child else replay(a.output,a.repo))
