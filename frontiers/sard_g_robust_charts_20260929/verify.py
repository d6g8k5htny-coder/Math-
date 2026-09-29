"""Verify exact packet membership, both Python modes and intended semantic failures."""
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
 'allow-endpoint':'test_endpoint_hit_excluded',
 'ignore-earlier-closed':'test_earlier_endpoint_not_hidden_by_later_interior',
 'allow-terminal':'test_terminal_hit_excluded',
 'skip-tube':'test_compact_prefix_tube_clearance',
 'skip-local':'test_all_local_sections_checked',
 'nonstrict-gradient':'test_strict_gradient_threshold',
 'leave-covariance':'test_gaussian_residual_orthogonality',
 'count-singular-zero':'test_regular_zeros_only',
}

def require(ok,message):
    if not ok:raise ValueError(message)

def decode(text):
    def unique(pairs):
        d={}
        for k,v in pairs:
            require(k not in d,'duplicate JSON key: '+k);d[k]=v
        return d
    return json.loads(text,object_pairs_hook=unique)

def identity(path):
    require(path.is_file() and not path.is_symlink(),'regular source required')
    data=path.read_bytes()
    return dict(bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),
                git_blob=hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest())

def sources():
    identity(ROOT/'SOURCE_FILES.json')
    rows=decode((ROOT/'SOURCE_FILES.json').read_text())['files']
    names=[row['path'] for row in rows]
    require(len(names)==len(set(names)) and all(Path(n).name==n and n!='SOURCE_FILES.json' for n in names),
            'unique flat manifest paths required')
    require(sorted(p.name for p in ROOT.iterdir())==sorted(names+['SOURCE_FILES.json']), 'source membership differs')
    for row in rows:
        require(identity(ROOT/row['path'])=={k:row[k] for k in ('bytes','sha256','git_blob')},
                'source identity differs: '+row['path'])
    return {p.name:identity(p) for p in sorted(ROOT.iterdir())}

def child(mutant):
    import charts,test_charts
    charts.MUTANT=mutant
    result=unittest.TextTestRunner(stream=io.StringIO()).run(unittest.defaultTestLoader.loadTestsFromModule(test_charts))
    print(json.dumps(dict(tests=result.testsRun,passed=result.wasSuccessful(),
        failures=sorted(t.id().rsplit('.',1)[-1] for t,_ in result.failures),
        errors=sorted(t.id().rsplit('.',1)[-1] for t,_ in result.errors)),sort_keys=True))
    return 0 if result.wasSuccessful() else 1

def replay(out):
    out=out.resolve()
    require(not out.exists() and not out.is_relative_to(ROOT),'new output outside packet required')
    before=sources();out.mkdir(parents=True);records={}
    for case in ['baseline',*MUTANTS]:
        pair=[]
        for mode,flags in [('normal',[]),('optimized',['-O'])]:
            cmd=[sys.executable,'-B',*flags,'-S',str(ROOT/'verify.py'),'--child']
            if case!='baseline':cmd+=['--mutant',case]
            run=subprocess.run(cmd,capture_output=True,timeout=30)
            (out/(case+'_'+mode+'.stdout')).write_bytes(run.stdout)
            (out/(case+'_'+mode+'.stderr')).write_bytes(run.stderr)
            obj=decode(run.stdout.decode())
            require(not run.stderr and not obj['errors'],'execution error: '+case)
            require(obj['tests']==19,'wrong test count')
            if case=='baseline':require(run.returncode==0 and obj['passed'] and not obj['failures'],'baseline failed')
            else:require(run.returncode==1 and not obj['passed'] and MUTANTS[case] in obj['failures'],
                         'intended semantic assertion absent: '+case)
            pair.append(run.stdout)
        require(pair[0]==pair[1],'Python modes disagree: '+case)
        records[case]=decode(pair[0].decode())
    summary=dict(tests_per_mode=19,semantic_mutants_per_mode=8,identical_output_pairs=9,
                 all_intended_failures=True,scientific_effect='NONE',continuum_proof_verified_by_code=False)
    require(summary==decode((ROOT/'RESULTS.json').read_text()),'stored summary differs')
    require(before==sources(),'source changed during replay')
    (out/'REPORT.json').write_text(json.dumps(dict(summary=summary,cases=records,source_identities=before),indent=2,sort_keys=True)+'\n')
    print(json.dumps(summary,indent=2,sort_keys=True))
    return 0

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--child',action='store_true');g.add_argument('--output',type=Path)
    p.add_argument('--mutant',choices=MUTANTS);a=p.parse_args()
    require(a.child or a.mutant is None,'mutant requires child mode')
    raise SystemExit(child(a.mutant) if a.child else replay(a.output))
