"""Exact packet membership and finite controls; no continuum proof claim."""
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
 'wrong-unstable-weight':'test_contraction_denominators',
 'wrong-stable-weight':'test_contraction_denominators',
 'drop-constant-forcing':'test_constant_forcing_retained',
 'reverse-unstable-integral':'test_constant_path_solves_original_vector_field',
 'omit-hit-time-projection':'test_projection_annihilates_time_direction',
 'pretend-Lipschitz-eigenline':'test_eigenline_derivative_loss_counterexample',
 'omit-height-difference':'test_distinct_value_mesh_exponent',
 'ignore-singular-slab':'test_morse_mesh_exponent',
 'wrong-residual-scale':'test_gaussian_residual_independence_identity',
}

def need(ok,message):
    if not ok:raise ValueError(message)

def decode(text):
    def unique(items):
        out={}
        for k,v in items:
            need(k not in out,'duplicate JSON key: '+k);out[k]=v
        return out
    return json.loads(text,object_pairs_hook=unique)

def identity(p):
    need(p.is_file() and not p.is_symlink(),'regular source required: '+p.name)
    b=p.read_bytes()
    return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),
            'git_blob':hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()}

def sources():
    identity(ROOT/'SOURCE_FILES.json')
    entries=decode((ROOT/'SOURCE_FILES.json').read_text())['files']
    names=[e['path'] for e in entries]
    need(len(names)==len(set(names)) and all(Path(n).name==n and n!='SOURCE_FILES.json' for n in names),
         'unique flat paths required')
    need(sorted(p.name for p in ROOT.iterdir())==sorted(names+['SOURCE_FILES.json']),
         'source membership differs')
    for e in entries:
        need(identity(ROOT/e['path'])=={k:e[k] for k in ['bytes','sha256','git_blob']},'source identity differs: '+e['path'])
    return {p.name:identity(p) for p in sorted(ROOT.iterdir())}

def child(mutant):
    import a2, test_a2
    a2.MUTANT=mutant
    res=unittest.TextTestRunner(stream=io.StringIO()).run(unittest.defaultTestLoader.loadTestsFromModule(test_a2))
    data={'tests':res.testsRun,'passed':res.wasSuccessful(),
          'failures':sorted(t.id().rsplit('.',1)[-1] for t,_ in res.failures),
          'errors':sorted(t.id().rsplit('.',1)[-1] for t,_ in res.errors)}
    print(json.dumps(data,sort_keys=True))
    return 0 if res.wasSuccessful() else 1

def replay(path):
    path=path.resolve()
    need(not path.exists() and not path.is_relative_to(ROOT),'new output outside packet required')
    before=sources();path.mkdir(parents=True)
    cases={}
    for case in ['baseline',*MUTANTS]:
        outputs=[]
        for mode,flags in [('normal',[]),('optimized',['-O'])]:
            cmd=[sys.executable,'-B',*flags,'-S',str(ROOT/'verify.py'),'--child']
            if case!='baseline':cmd+=['--mutant',case]
            run=subprocess.run(cmd,capture_output=True,timeout=30)
            (path/(case+'_'+mode+'.stdout')).write_bytes(run.stdout)
            (path/(case+'_'+mode+'.stderr')).write_bytes(run.stderr)
            record=decode(run.stdout.decode())
            need(not run.stderr and not record['errors'],'execution error, not intended failure: '+case)
            need(record['tests']==18,'incorrect test count')
            if case=='baseline':need(run.returncode==0 and record['passed'] and not record['failures'],'baseline failed')
            else:need(run.returncode==1 and not record['passed'] and MUTANTS[case] in record['failures'],'semantic mutant escaped: '+case)
            outputs.append(run.stdout)
        need(outputs[0]==outputs[1],'normal/optimized mismatch: '+case)
        cases[case]=decode(outputs[0].decode())
    summary={'tests_per_mode':18,'semantic_mutants_per_mode':9,'identical_output_pairs':10,
             'all_intended_failures':True,'scientific_effect':'NONE','continuum_verified_by_code':False}
    need(summary==decode((ROOT/'RESULTS.json').read_text()),'stored summary differs')
    need(before==sources(),'source changed during execution')
    (path/'REPORT.json').write_text(json.dumps({**summary,'cases':cases,'sources':before,'sources_unchanged':True},indent=2,sort_keys=True)+'\n')
    print(json.dumps(summary,sort_keys=True));return 0

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--child',action='store_true');g.add_argument('--output',type=Path)
    p.add_argument('--mutant',choices=MUTANTS);o=p.parse_args()
    need(o.child or o.mutant is None,'mutant requires child mode')
    raise SystemExit(child(o.mutant) if o.child else replay(o.output))
