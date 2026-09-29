"""Source-bound exact finite controls; not a verification of Gaussian analysis."""
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
 'wrong-schur-sign':'test_nonorthogonal_shear_cancels_midpoint_cross_terms',
 'omit-shear':'test_nonorthogonal_shear_cancels_midpoint_cross_terms',
 'rare-every-direction':'test_raw_chart_volume_is_one_power_of_r',
 'all-directions-soft':'test_stiff_modes_do_not_change_weight_power',
 'drop-band-jacobian':'test_raw_chart_volume_is_one_power_of_r',
 'duplicate-cubic-pin':'test_complete_contact_jet_labels',
 'drop-transverse-linear':'test_plane_pins_with_free_transverse_cubic',
 'ignore-cross-schur':'test_endpoint_cross_blocks_need_schur_correction',
 'positive-stiff':'test_stiff_modes_do_not_change_weight_power',
 'omit-loss-factor':'test_density_loss_ledger',
}

def require(ok,message):
    if not ok:raise ValueError(message)

def decode(text):
    def unique(items):
        d={}
        for k,v in items:
            require(k not in d,'duplicate JSON key: '+k);d[k]=v
        return d
    return json.loads(text,object_pairs_hook=unique)

def ident(path):
    require(path.is_file() and not path.is_symlink(),'regular source required')
    data=path.read_bytes()
    return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),
            'git_blob':hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()}

def sources():
    ident(ROOT/'SOURCE_FILES.json')
    entries=decode((ROOT/'SOURCE_FILES.json').read_text())['files']
    names=[e['path'] for e in entries]
    require(len(names)==len(set(names)) and all(Path(n).name==n and n!='SOURCE_FILES.json' for n in names),'unique flat paths required')
    require(sorted(p.name for p in ROOT.iterdir())==sorted(names+['SOURCE_FILES.json']),'source membership differs')
    for e in entries:require(ident(ROOT/e['path'])=={k:e[k] for k in ['bytes','sha256','git_blob']},'source identity differs: '+e['path'])
    return {p.name:ident(p) for p in sorted(ROOT.iterdir())}

def child(mutant):
    import lift
    import test_lift
    lift.MUTANT=mutant
    result=unittest.TextTestRunner(stream=io.StringIO()).run(unittest.defaultTestLoader.loadTestsFromModule(test_lift))
    print(json.dumps({'tests':result.testsRun,'passed':result.wasSuccessful(),
      'failures':sorted(t.id().rsplit('.',1)[-1] for t,_ in result.failures),
      'errors':sorted(t.id().rsplit('.',1)[-1] for t,_ in result.errors)},sort_keys=True))
    return 0 if result.wasSuccessful() else 1

def replay(out):
    out=out.resolve()
    require(not out.exists() and not out.is_relative_to(ROOT),'new output outside source required')
    before=sources();out.mkdir(parents=True)
    records={}
    for case in ['baseline',*MUTANTS]:
        pair=[]
        for mode,flags in [('normal',[]),('optimized',['-O'])]:
            command=[sys.executable,'-B',*flags,'-S',str(ROOT/'verify.py'),'--child']
            if case!='baseline':command+=['--mutant',case]
            proc=subprocess.run(command,capture_output=True,timeout=30)
            (out/(case+'_'+mode+'.stdout')).write_bytes(proc.stdout)
            (out/(case+'_'+mode+'.stderr')).write_bytes(proc.stderr)
            result=decode(proc.stdout.decode())
            require(not proc.stderr and not result['errors'],'execution error: '+case)
            require(result['tests']==18,'wrong test count')
            if case=='baseline':require(proc.returncode==0 and result['passed'] and not result['failures'],'baseline failed')
            else:require(proc.returncode==1 and not result['passed'] and MUTANTS[case] in result['failures'],'intended semantic failure absent: '+case)
            pair.append(proc.stdout)
        require(pair[0]==pair[1],'Python modes disagree: '+case)
        records[case]=decode(pair[0].decode())
    summary={'tests_per_mode':18,'semantic_mutants_per_mode':10,'identical_output_pairs':11,
             'all_intended_failures':True,'scientific_effect':'NONE','gaussian_analysis_verified_by_code':False}
    require(summary==decode((ROOT/'RESULTS.json').read_text()),'stored summary differs')
    require(sources()==before,'sources changed during replay')
    report={**summary,'source_identities':before,'sources_unchanged':True,'cases':records}
    (out/'REPORT.json').write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')
    print(json.dumps(summary,sort_keys=True,indent=2))
    return 0

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--child',action='store_true');g.add_argument('--output',type=Path)
    p.add_argument('--mutant',choices=MUTANTS);a=p.parse_args()
    require(a.child or a.mutant is None,'mutant requires child mode')
    raise SystemExit(child(a.mutant) if a.child else replay(a.output))
