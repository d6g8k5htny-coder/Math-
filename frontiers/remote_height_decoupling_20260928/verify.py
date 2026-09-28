"""Verify the exact flat packet, execute both modes, reject semantic mutants."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

EXPECTED_FAILURE = {
    'tv-factor':'test_probability_tv_half_convention',
    'wrong-marginal':'test_own_not_contact_marginal',
    'drop-pair-weight':'test_mean_needs_two_pair_points',
    'ignore-mass':'test_normalization_handles_small_mass',
    'allow-zero':'test_zero_mass_excluded',
}

def unique(items):
    result={}
    for key,value in items:
        if key in result:
            raise ValueError('duplicate JSON key: '+key)
        result[key]=value
    return result

def load(text):
    return json.loads(text,object_pairs_hook=unique)

def check_sources(root):
    entries=load((root/'SOURCE_FILES.json').read_text())['files']
    names=[e['path'] for e in entries]
    if len(names)!=len(set(names)) or any(Path(n).name!=n for n in names):
        raise ValueError('invalid flat source paths')
    if sorted(p.name for p in root.iterdir())!=sorted(names+['SOURCE_FILES.json']):
        raise ValueError('packet membership differs')
    for e in entries:
        p=root/e['path']
        if p.is_symlink() or not p.is_file():
            raise ValueError('nonregular source')
        data=p.read_bytes()
        if len(data)!=e['bytes'] or hashlib.sha256(data).hexdigest()!=e['sha256']:
            raise ValueError('source identity differs: '+p.name)

def main():
    root=Path(__file__).resolve().parent
    check_sources(root)
    baseline=load((root/'RESULTS.json').read_text())['baseline']
    records=[]
    for case in ['baseline',*EXPECTED_FAILURE]:
        outs=[]
        for flags in (['-B','-S'],['-B','-O','-S']):
            command=[sys.executable,*flags,str(root/'check.py')]
            if case!='baseline':
                command+=['--mutant',case]
            process=subprocess.run(command,capture_output=True,timeout=30)
            result=load(process.stdout.decode())
            if process.stderr or result['errors']:
                raise ValueError('execution error rather than semantic failure')
            if case=='baseline':
                if process.returncode!=0 or result!=baseline:
                    raise ValueError('baseline mismatch')
            elif process.returncode!=1 or result['passed'] or EXPECTED_FAILURE[case] not in result['failures']:
                raise ValueError('semantic mutant not rejected: '+case)
            outs.append(process.stdout)
        if outs[0]!=outs[1]:
            raise ValueError('normal and optimized outputs differ')
        records.append({'case':case,**load(outs[0].decode())})
    check_sources(root)
    print(json.dumps({'scientific_effect':'NONE','nonauthor_acceptance':False,
                      'tests_per_mode':baseline['tests'],'mutants_per_mode':len(EXPECTED_FAILURE),
                      'exact_sources':'PASS','all_output_pairs_identical':True,'cases':records},
                     indent=2,sort_keys=True))

if __name__=='__main__':
    main()
