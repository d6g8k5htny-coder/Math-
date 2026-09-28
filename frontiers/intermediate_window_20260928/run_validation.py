"""Source-bound finite controls. Not a Gaussian integrator or theorem checker."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
MUTANTS={
 'degree_four':('def observation_matrix(eps,u,v,degree=5):','def observation_matrix(eps,u,v,degree=4):'),
 'raw_collision_instead_of_contact':('first=[evaluate(q,0,0) for q in ps]','first=[F(0)]*6'),
 'wrong_value_row_operation':('(height-s*v*fz/2)/s**3','(height-s*v*fz/3)/s**3'),
 'missing_transverse_column':('[[u*v,v*v/2,F(0),F(0)]','[[u*v,F(0),F(0),F(0)]'),
 'wrong_euler_degree':('degree_coefficient=3','degree_coefficient=2'),
 'erase_height_window':('return abs(height)<=k*r**3/2','return True'),
 'drop_original_normalizer':('normalizer=-2','normalizer=0'),
 'eight_not_nine_observations':('actual_observations=9','actual_observations=8'),
 'two_dimensional_density':('raw_density=-15','raw_density=-10'),
 'non_summable_flat_shell':('return (r/s)**2+s*s','return (r/s)**2+s*s+1'),
}


def require(ok,message):
    if not ok:raise RuntimeError(message)


def identity(p):
    require(p.is_file() and not p.is_symlink(),'regular file required: '+p.name)
    b=p.read_bytes()
    return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),
            'git_blob':hashlib.sha1(('blob '+str(len(b))+'\0').encode()+b).hexdigest()}


def source_check():
    manifest=json.loads((ROOT/'SOURCE_FILES.json').read_text())
    expected=set()
    for row in manifest['files']:
        name=row['path']
        require(Path(name).name==name and name not in expected and name!='SOURCE_FILES.json','bad source name')
        expected.add(name)
        require(identity(ROOT/name)=={k:row[k] for k in ['bytes','sha256','git_blob']},'source mismatch: '+name)
    actual={p.name for p in ROOT.iterdir() if p.name!='SOURCE_FILES.json'}
    require(actual==expected,'missing/extra source entry')
    return {p.name:identity(p) for p in sorted(ROOT.iterdir())}


def controls(out):
    code=(ROOT/'algebra.py').read_text()
    logs={}
    for mode,flags in [('normal',[]),('optimized',['-O'])]:
        rows={}
        for label,mutation in [('baseline',None),*MUTANTS.items()]:
            cwd=ROOT
            if mutation:
                old,new=mutation;require(code.count(old)==1,'mutation target not unique')
                cwd=out/'mutants'/mode/label;cwd.mkdir(parents=True)
                (cwd/'algebra.py').write_text(code.replace(old,new))
                (cwd/'test_algebra.py').write_bytes((ROOT/'test_algebra.py').read_bytes())
            r=subprocess.run([sys.executable,'-B',*flags,'-S','-m','unittest','-v','test_algebra'],
                              cwd=cwd,capture_output=True,timeout=30)
            (out/(label+'_'+mode+'.stdout')).write_bytes(r.stdout)
            (out/(label+'_'+mode+'.stderr')).write_bytes(r.stderr)
            text=r.stderr.decode('utf-8','replace')
            require('Ran 15 tests' in text and 'skipped=' not in text,'coverage mismatch: '+label)
            if mutation:
                require(r.returncode==1 and 'AssertionError' in text and 'FAILED (failures=' in text
                        and 'errors=' not in text,'mutant not assertion-rejected: '+label)
            else:require(r.returncode==0 and text.rstrip().endswith('OK'),'baseline failed: '+mode)
            rows[label]={'exit_code':r.returncode,'assertion_rejected':bool(mutation)}
        logs[mode]=rows
    summary={'named_tests_per_mode':15,'confluent_rank_fixtures':24,'pinned_cubic_fixtures':48,
             'transverse_minor_fixtures':18,'distinct_mutants':len(MUTANTS),
             'modes':['normal','optimized'],'all_tests_passed':True,'all_mutants_assertion_rejected':True,
             'continuum_verified':False,'scientific_effect':'NONE'}
    return summary,logs


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True,type=Path)
    out=parser.parse_args().output.resolve()
    require(not out.exists() and not out.is_relative_to(ROOT),'new output path outside sources required')
    before=source_check();out.mkdir(parents=True)
    report={'passed':False,'scientific_effect':'NONE','continuum_verified':False,'sources':before}
    try:
        summary,logs=controls(out)
        raw=(json.dumps(summary,sort_keys=True,indent=2)+'\n').encode()
        require((ROOT/'RESULTS.json').read_bytes()==raw,'stored result mismatch')
        require(source_check()==before,'sources changed')
        for mode in ['normal','optimized']:(out/('summary_'+mode+'.json')).write_bytes(raw)
        report.update(passed=True,modes=logs,sources_unchanged=True,deterministic_summaries_equal=True)
        print(raw.decode(),end='')
    finally:(out/'REPORT.json').write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')
if __name__=='__main__':main()
