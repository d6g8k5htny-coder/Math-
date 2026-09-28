"""Exact source and finite-control replay; no network or repository mutation."""
import argparse
import hashlib
import importlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parent
MUTANTS={
 'wrong-nine-tail':('36*z*z - 63*z + 28','36*z*z - 62*z + 28','test_exact_nine_tail_identity'),
 'omit-exp-tail':('return lower, lower + remainder','return lower, lower','test_exponential_bracket'),
 'omit-log-tail':('return lower, lower+remainder','return lower, lower','test_logarithm_remainder_is_retained'),
 'lose-read-two':('return 2/upper_h, 2/lower_h','return 1/upper_h, 1/lower_h','test_tight_factor_enclosure'),
 'lose-chernoff-half':('return F(1, 2)*F(5, 16)**a','return F(5, 16)**a','test_even_chernoff_envelope'),
 'max-not-load-sum':('sum((w for b, w in zip(blocks, weights) if v in b), F(0))','max((w for b, w in zip(blocks, weights) if v in b), default=F(0))','test_weighted_overlap_load_is_sum'),
 'charge-inactive':('if d == max(demands)','if d <= max(demands)','test_active_minimal_cover_unchanged_scope'),
}


def require(condition,message):
    if not condition:
        raise ValueError(message)


def unique_json(text):
    def pairs(rows):
        result={}
        for key,value in rows:
            require(key not in result,'duplicate JSON key: '+key)
            result[key]=value
        return result
    return json.loads(text,object_pairs_hook=pairs)


def identity(path):
    require(path.is_file() and not path.is_symlink(),'regular source required: '+path.name)
    data=path.read_bytes()
    return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),
            'git_blob':hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()}


def sources():
    identity(ROOT/'SOURCE_FILES.json')
    rows=unique_json((ROOT/'SOURCE_FILES.json').read_text())['files']
    names=[row['path'] for row in rows]
    require(len(names)==len(set(names)) and all(Path(n).name==n and n!='SOURCE_FILES.json' for n in names),'unique flat source paths required')
    require(sorted(p.name for p in ROOT.iterdir())==sorted(names+['SOURCE_FILES.json']),'source membership mismatch')
    for row in rows:
        require(identity(ROOT/row['path'])=={k:row[k] for k in ['bytes','sha256','git_blob']},'source identity mismatch: '+row['path'])
    return {p.name:identity(p) for p in sorted(ROOT.iterdir())}


def child(directory):
    sys.path.insert(0,str(directory))
    module=importlib.import_module('test_certificate')
    result=unittest.TextTestRunner(stream=io.StringIO()).run(unittest.defaultTestLoader.loadTestsFromModule(module))
    record={'tests':result.testsRun,'passed':result.wasSuccessful(),
            'failures':sorted(test.id().rsplit('.',1)[-1] for test,_ in result.failures),
            'errors':sorted(test.id().rsplit('.',1)[-1] for test,_ in result.errors)}
    print(json.dumps(record,sort_keys=True))
    return 0 if result.wasSuccessful() else 1


def replay(output):
    output=output.resolve()
    require(not output.exists() and not output.is_relative_to(ROOT),'new output outside source required')
    before=sources()
    output.mkdir(parents=True)
    code=(ROOT/'certificate.py').read_text()
    records={}
    for name in ['baseline',*MUTANTS]:
        with tempfile.TemporaryDirectory(prefix='p15-tail-load-') as temporary:
            directory=Path(temporary)
            shutil.copyfile(ROOT/'test_certificate.py',directory/'test_certificate.py')
            text=code
            if name!='baseline':
                old,new,_=MUTANTS[name]
                require(code.count(old)==1,'mutation anchor not unique: '+name)
                text=code.replace(old,new)
            (directory/'certificate.py').write_text(text)
            pair=[]
            for mode,flags in [('normal',[]),('optimized',['-O'])]:
                process=subprocess.run([sys.executable,'-B',*flags,'-S',str(ROOT/'verify.py'),'--child',str(directory)],capture_output=True,timeout=30)
                (output/(name+'_'+mode+'.stdout')).write_bytes(process.stdout)
                (output/(name+'_'+mode+'.stderr')).write_bytes(process.stderr)
                result=unique_json(process.stdout.decode())
                require(not process.stderr and not result['errors'],'execution error: '+name)
                require(result['tests']==15,'wrong test count: '+name)
                if name=='baseline':
                    require(process.returncode==0 and result['passed'] and not result['failures'],'baseline failed')
                else:
                    require(process.returncode==1 and not result['passed'] and MUTANTS[name][2] in result['failures'],'intended assertion did not reject: '+name)
                pair.append(process.stdout)
            require(pair[0]==pair[1],'Python mode output mismatch: '+name)
            records[name]=unique_json(pair[0].decode())
    summary={'tests_per_mode':15,'semantic_mutants_per_mode':7,'output_pairs_identical':8,
             'baseline_passed':True,'all_mutants_assertion_rejected':True,
             'scientific_effect':'NONE','continuum_verified':False}
    require(summary==unique_json((ROOT/'RESULTS.json').read_text()),'stored summary differs')
    require(sources()==before,'source mutation')
    report={**summary,'source_identities':before,'sources_unchanged':True,'cases':records}
    (output/'REPORT.json').write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')
    print(json.dumps(summary,sort_keys=True,indent=2))
    return 0


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--output',type=Path)
    group.add_argument('--child',type=Path)
    args=parser.parse_args()
    raise SystemExit(child(args.child.resolve()) if args.child else replay(args.output))
