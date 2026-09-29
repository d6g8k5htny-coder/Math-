"""Exact packet and both-mode finite verification. No network or proof-status writes."""
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
 'height-jacobian-in-gradient-frame':'test_gradient_only_density_jacobian',
 'drop-soft-determinants':'test_radial_power_independent_of_dimension',
 'lose-overlap-three':'test_integrated_overlap_coefficient',
 'include-divergent-endpoint':'test_inverse_endpoint_is_not_finite',
 'lose-cdf-half':'test_small_separation_cdf_has_half',
 'reverse-height-sign':'test_exact_polynomial_fold_data',
 'two-height-windows-at-fixed-r':'test_t_to_T_and_coefficient_conversion',
 'event-not-factorial-weight':'test_probability_size_bias_not_event_sampling',
}

def require(ok, message):
    if not ok:raise ValueError(message)

def decode(text):
    def pairs(items):
        out={}
        for k,v in items:
            require(k not in out,'duplicate JSON key: '+k);out[k]=v
        return out
    return json.loads(text,object_pairs_hook=pairs)

def identity(path):
    require(path.is_file() and not path.is_symlink(),'regular source required')
    data=path.read_bytes()
    return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),
            'git_blob':hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()}

def source_check():
    identity(ROOT/'SOURCE_FILES.json')
    entries=decode((ROOT/'SOURCE_FILES.json').read_text())['files']
    names=[e['path'] for e in entries]
    require(len(names)==len(set(names)) and all(Path(n).name==n and n!='SOURCE_FILES.json' for n in names),'unique flat paths required')
    require(sorted(p.name for p in ROOT.iterdir())==sorted(names+['SOURCE_FILES.json']),'source membership differs')
    for e in entries:
        require(identity(ROOT/e['path'])=={k:e[k] for k in ['bytes','sha256','git_blob']},'source identity differs: '+e['path'])
    return {p.name:identity(p) for p in sorted(ROOT.iterdir())}

def child(mutant):
    import inverse
    import test_inverse
    inverse.MUTANT=mutant
    result=unittest.TextTestRunner(stream=io.StringIO()).run(unittest.defaultTestLoader.loadTestsFromModule(test_inverse))
    out={'tests':result.testsRun,'passed':result.wasSuccessful(),
         'failures':sorted(t.id().rsplit('.',1)[-1] for t,_ in result.failures),
         'errors':sorted(t.id().rsplit('.',1)[-1] for t,_ in result.errors)}
    print(json.dumps(out,sort_keys=True))
    return 0 if result.wasSuccessful() else 1

def replay(output):
    output=output.resolve()
    require(not output.exists() and not output.is_relative_to(ROOT),'new output directory outside packet required')
    before=source_check();output.mkdir(parents=True)
    records={}
    for case in ['baseline',*MUTANTS]:
        outputs=[]
        for mode,flags in [('normal',[]),('optimized',['-O'])]:
            cmd=[sys.executable,'-B',*flags,'-S',str(ROOT/'verify.py'),'--child']
            if case!='baseline':cmd+=['--mutant',case]
            p=subprocess.run(cmd,capture_output=True,timeout=30)
            (output/(case+'_'+mode+'.stdout')).write_bytes(p.stdout)
            (output/(case+'_'+mode+'.stderr')).write_bytes(p.stderr)
            r=decode(p.stdout.decode())
            require(not p.stderr and not r['errors'],'execution error rather than semantic test: '+case)
            require(r['tests']==12,'wrong finite test count')
            if case=='baseline':require(p.returncode==0 and r['passed'] and not r['failures'],'baseline failed')
            else:require(p.returncode==1 and not r['passed'] and MUTANTS[case] in r['failures'],'intended assertion did not reject: '+case)
            outputs.append(p.stdout)
        require(outputs[0]==outputs[1],'Python modes disagree: '+case)
        records[case]=decode(outputs[0].decode())
    summary={'tests_per_mode':12,'semantic_mutants_per_mode':8,'identical_output_pairs':9,
             'all_intended_failures':True,'scientific_effect':'NONE','continuum_analysis_verified_by_code':False}
    require(summary==decode((ROOT/'RESULTS.json').read_text()),'stored summary differs')
    require(source_check()==before,'source changed during execution')
    (output/'REPORT.json').write_text(json.dumps({**summary,'sources_unchanged':True,'source_identities':before,'cases':records},sort_keys=True,indent=2)+'\n')
    print(json.dumps(summary,sort_keys=True,indent=2));return 0

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--child',action='store_true');g.add_argument('--output',type=Path)
    p.add_argument('--mutant',choices=MUTANTS);a=p.parse_args()
    require(a.child or a.mutant is None,'mutant requires child mode')
    raise SystemExit(child(a.mutant) if a.child else replay(a.output))
