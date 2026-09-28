"""Finite-law replay and mutation checks, no Gaussian or theorem automation."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
MUTANTS={
 'omit_tv_half':(')),F(0))/2',')),F(0))'),
 'multi_event_instead_of_point_mass':('len(c)*w for c,w in p.items() if len(c)>=2','w for c,w in p.items() if len(c)>=2'),
 'erase_multiplicity':('for x in c:','for x in set(c):'),
 'wrong_nonempty_normalizer':('mass=sum((w for c,w in p.items() if c),F(0))','mass=sum((len(c)*w for c,w in p.items()),F(0))'),
 'wrong_empty_mass':('return {():1-m,','return {():m,'),
 'square_instead_of_factorial':('len(c)*(len(c)-1)*w','len(c)*len(c)*w'),
}


def require(ok,msg):
    if not ok:raise RuntimeError(msg)


def identity(p):
    require(p.is_file() and not p.is_symlink(),'not a regular file: '+p.name)
    b=p.read_bytes()
    return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),
            'git_blob':hashlib.sha1(('blob '+str(len(b))+'\0').encode()+b).hexdigest()}


def sources():
    rows=json.loads((ROOT/'SOURCE_FILES.json').read_text())['files']; seen=set()
    for row in rows:
        name=row['path']
        require(name not in seen and Path(name).name==name and name!='SOURCE_FILES.json','invalid source path')
        seen.add(name)
        require(identity(ROOT/name)=={k:row[k] for k in ['bytes','sha256','git_blob']},'source mismatch: '+name)
    require({p.name for p in ROOT.iterdir()}==seen|{'SOURCE_FILES.json'},'extra/missing source member')
    return {p.name:identity(p) for p in sorted(ROOT.iterdir())}


def main():
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('--output',type=Path,required=True)
    out=ap.parse_args().output.resolve()
    require(not out.exists() and not out.is_relative_to(ROOT),'new output path outside source required')
    before=sources(); out.mkdir(parents=True); code=(ROOT/'finite_law.py').read_text()
    report={'passed':False,'scientific_effect':'NONE','continuum_verified':False,'source_files':before,'modes':{}}
    try:
        for mode,flags in [('normal',[]),('optimized',['-O'])]:
            results={}
            for name,pair in [('baseline',None),*MUTANTS.items()]:
                cwd=ROOT
                if pair:
                    old,new=pair; require(code.count(old)==1,'mutation not unique: '+name)
                    cwd=out/'mutants'/mode/name; cwd.mkdir(parents=True)
                    (cwd/'finite_law.py').write_text(code.replace(old,new))
                    (cwd/'test_finite_law.py').write_bytes((ROOT/'test_finite_law.py').read_bytes())
                r=subprocess.run([sys.executable,'-B',*flags,'-S','-m','unittest','-v','test_finite_law'],
                                 cwd=cwd,capture_output=True,timeout=30)
                (out/(name+'_'+mode+'.stdout')).write_bytes(r.stdout)
                (out/(name+'_'+mode+'.stderr')).write_bytes(r.stderr)
                t=r.stderr.decode('utf8','replace')
                require('Ran 14 tests' in t and 'skipped=' not in t,'test count: '+name)
                if pair:
                    require(r.returncode==1 and 'AssertionError' in t and 'FAILED (failures=' in t and 'errors=' not in t,
                            'mutant did not assertion-reject: '+name)
                else:require(r.returncode==0 and t.rstrip().endswith('OK'),'baseline failed')
                results[name]={'exit_code':r.returncode,'assertion_rejected':bool(pair)}
            report['modes'][mode]=results
        summary={'named_tests_per_mode':14,'distinct_mutants':6,'modes':['normal','optimized'],
                 'baseline_passed':True,'all_mutants_assertion_rejected':True,
                 'scientific_effect':'NONE','continuum_verified':False}
        raw=(json.dumps(summary,sort_keys=True,indent=2)+'\n').encode()
        require((ROOT/'RESULTS.json').read_bytes()==raw,'stored summary mismatch')
        for mode in ['normal','optimized']:(out/('summary_'+mode+'.json')).write_bytes(raw)
        require(sources()==before,'source mutation detected')
        report.update(passed=True,sources_unchanged=True,deterministic_summaries_equal=True)
        print(raw.decode(),end='')
    finally:(out/'REPORT.json').write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')
if __name__=='__main__':main()
