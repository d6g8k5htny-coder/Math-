"""Source-bound finite-algebra replay; never interprets an arbitrary crash as a mutant PASS."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent
PAYLOAD={'PROOF.md','README.md','algebra.py','test_adapter.py','replay.py'}
MUTANTS={
 'double_angle': ("'entry_angular_over_pi': F(1)","'entry_angular_over_pi': F(2)",
                  {'test_angle_and_volume_normalizations'}),
 'omit_frobenius_scale': ("'frobenius_over_entry_squared': F(2)","'frobenius_over_entry_squared': F(1)",
                  {'test_angle_and_volume_normalizations'}),
 'drop_mixed_soft': ('return upper**3/3 + shift*upper**2/2','return upper**3/3',
                  {'test_soft_primitive_retains_mixed_term','test_ninth_moment_radius_factorization',
                   'test_order_bound_precedes_interval_extension'}),
 'eighth_envelope': ('*top*top*(J+top)**9','*top*top*(J+top)**8',
                  {'test_ninth_moment_radius_factorization'}),
 'wrong_normalizer': ('return (C*r**5)/(z_floor*r**2)','return (C*r**5)/(z_floor*r**5)',
                  {'test_full_normalizer_once'}),
}

def sha(data): return hashlib.sha256(data).hexdigest()

def strict_json(text):
    def pairs(items):
        out={}
        for key,value in items:
            if key in out: raise ValueError('duplicate JSON key')
            out[key]=value
        return out
    def invalid(value): raise ValueError('nonfinite JSON constant: '+value)
    return json.loads(text,object_pairs_hook=pairs,parse_constant=invalid)

def authenticate():
    raw=(HERE/'SOURCES.json').read_bytes()
    manifest=strict_json(raw.decode('utf-8'))
    if manifest['schema']!=1 or set(manifest['files'])!=PAYLOAD:
        raise ValueError('manifest payload inventory mismatch')
    if {p.name for p in HERE.iterdir()}!=PAYLOAD|{'SOURCES.json'}:
        raise ValueError('unexpected/missing packet member')
    result={'SOURCES.json':sha(raw)}
    for name in sorted(PAYLOAD):
        p=HERE/name
        if p.is_symlink() or not p.is_file(): raise ValueError('nonregular payload')
        data=p.read_bytes(); row=manifest['files'][name]
        blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        if len(data)!=row['bytes'] or sha(data)!=row['sha256'] or blob!=row['git_blob']:
            raise ValueError('payload identity mismatch: '+name)
        result[name]=sha(data)
    return result

def run_suite(directory,flags,expected):
    done=subprocess.run([sys.executable,*flags,'test_adapter.py'],cwd=directory,
                        capture_output=True,text=True,timeout=20)
    summary=strict_json(done.stdout)
    fields={'scope','tests','failures','errors','success'}
    if (set(summary)!=fields or type(summary['tests']) is not int or summary['tests']!=14
        or type(summary['success']) is not bool or not isinstance(summary['failures'],list)
        or len(summary['failures'])!=len(set(summary['failures'])) or summary['errors']!=[]
        or set(summary['failures'])!=expected or summary['success']!=(not expected)
        or done.returncode!=(1 if expected else 0)):
        raise ValueError('wrong exit, test inventory, or rejection reason')
    if f'Ran 14 tests in ' not in done.stderr:
        raise ValueError('missing unittest execution record')
    return {'exit':done.returncode,'summary':summary,
            'stdout_sha256':sha(done.stdout.encode()),'stderr':done.stderr}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--mode',choices=['normal','optimized'],required=True)
    ap.add_argument('--evidence',type=Path)
    args=ap.parse_args(); before=authenticate()
    flags=['-B','-S'] if args.mode=='normal' else ['-B','-O','-S']
    records={'baseline':run_suite(HERE,flags,set())}
    algebra=(HERE/'algebra.py').read_text(); tests=(HERE/'test_adapter.py').read_text()
    for name,(old,new,expected) in MUTANTS.items():
        if algebra.count(old)!=1: raise ValueError('mutant replacement not unique: '+name)
        with tempfile.TemporaryDirectory(prefix='cap-d3-'+name+'-') as td:
            directory=Path(td)
            (directory/'algebra.py').write_text(algebra.replace(old,new))
            (directory/'test_adapter.py').write_text(tests)
            records[name]=run_suite(directory,flags,expected)
    if authenticate()!=before: raise ValueError('source changed during execution')
    result={'scope':'finite algebra only; no analytic or Lean acceptance','mode':args.mode,
            'baseline_tests':14,'intended_mutants':len(MUTANTS),'source_sha256':before,
            'pass':True,'executions':records}
    if args.evidence:
        args.evidence.parent.mkdir(parents=True,exist_ok=True)
        with args.evidence.open('x') as f: json.dump(result,f,indent=2,sort_keys=True); f.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k!='executions'},indent=2,sort_keys=True))

if __name__=='__main__':
    main()
