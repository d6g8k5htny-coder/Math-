"""Finite controls only; require a new output directory outside the source tree."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
MUTANTS={
 'degree_four_instead_of_five':('def jet_matrix(points, degree=5):','def jet_matrix(points, degree=4):'),
 'erase_cardinal_derivative_correction':('h=multiply([1+2*slope*ti,-2*slope],sq)','h=sq'),
 'erase_transverse_midpoint_column':('return [[u*v,v*v/2,F(0)],[F(0),F(0),v]]','return [[u*v,F(0),F(0)],[F(0),F(0),v]]'),
 'drop_original_normalizer':('normalizer=-2','normalizer=0'),
 'condition_auxiliary_ninth_value':("'actual_conditioning':8","'actual_conditioning':9"),
 'insert_height_window':("'height_window_factor':0","'height_window_factor':3"),
}

def require(ok,message):
    if not ok: raise RuntimeError(message)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',required=True,type=Path)
    out=p.parse_args().output.resolve()
    require(not out.exists() and not out.is_relative_to(ROOT),'new output directory outside source required')
    out.mkdir(parents=True)
    names=['collar_algebra.py','test_collar_algebra.py','run_collar_validation.py']
    before={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in names}
    code=(ROOT/'collar_algebra.py').read_text()
    report={'scientific_effect':'NONE','continuum_verified':False,'passed':False,'modes':{},'sources':before}
    try:
        for mode,flags in [('normal',[]),('optimized',['-O'])]:
            records={}
            for label,mutation in [('baseline',None),*MUTANTS.items()]:
                cwd=ROOT
                if mutation:
                    old,new=mutation;require(code.count(old)==1,'mutation target not unique')
                    cwd=out/'mutants'/mode/label;cwd.mkdir(parents=True)
                    (cwd/'collar_algebra.py').write_text(code.replace(old,new))
                    (cwd/'test_collar_algebra.py').write_bytes((ROOT/'test_collar_algebra.py').read_bytes())
                run=subprocess.run([sys.executable,'-B',*flags,'-S','-m','unittest','-v','test_collar_algebra'],cwd=cwd,capture_output=True,timeout=30)
                (out/f'{label}_{mode}.stdout').write_bytes(run.stdout)
                (out/f'{label}_{mode}.stderr').write_bytes(run.stderr)
                text=run.stderr.decode('utf-8','replace')
                require('Ran 10 tests' in text,'coverage mismatch')
                if mutation:
                    require(run.returncode!=0 and 'AssertionError' in text and 'FAILED (failures=' in text and 'errors=' not in text,'mutant not assertion-rejected: '+label)
                else: require(run.returncode==0 and text.rstrip().endswith('OK'),'baseline failed')
                records[label]={'exit_code':run.returncode,'assertion_rejected':bool(mutation)}
            report['modes'][mode]=records
        require(before=={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in names},'sources changed')
        summary={'named_tests_per_mode':10,'rank_fixtures':35,'cardinal_node_triples':3,'transverse_gram_fixtures':12,'distinct_mutants':6,'modes':['normal','optimized'],'all_passed':True,'all_mutants_assertion_rejected':True,'continuum_verified':False,'scientific_effect':'NONE'}
        raw=(json.dumps(summary,indent=2,sort_keys=True)+'\n').encode()
        for mode in ['normal','optimized']:(out/f'summary_{mode}.json').write_bytes(raw)
        expected=ROOT/'COLLAR_RESULTS.json'
        if expected.exists():require(expected.read_bytes()==raw,'stored summary mismatch')
        report.update(passed=True,sources_unchanged=True)
        print(raw.decode(),end='')
    finally:(out/'REPORT.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
if __name__=='__main__':main()
