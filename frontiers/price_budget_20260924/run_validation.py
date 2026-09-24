"""Bounded same-author replay of exact price-budget sources. No network operations."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
MUTANTS={
 'drop_demand_condition': ('return demand >= 2 and max(ps)', 'return max(ps)'),
 'replace_hazard_upper_by_p': ('p / (1 - p)', 'p'),
 'reverse_budget_comparison': ('elif upper <= q:', 'elif upper >= q:'),
 'incorrect_capacity_cutoff': ('return 1 - sum(row)', 'return 1 - sum(row[:-1])'),
 'wrong_ratio_exponent': ('/ (1 - p) ** n', '/ (1 - p) ** (n - 1)'),
}


def verify():
    rows=json.loads((ROOT/'SOURCE_FILES.json').read_text())
    for name,identity in rows.items():
        if Path(name).name!=name or (ROOT/name).is_symlink(): raise ValueError('unsafe source path')
        raw=(ROOT/name).read_bytes()
        if len(raw)!=identity['bytes'] or hashlib.sha256(raw).hexdigest()!=identity['sha256']:
            raise ValueError('source mismatch: '+name)
    return rows


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',required=True,type=Path)
    args=p.parse_args()
    out=args.output.resolve()
    if out.exists() or out==ROOT or out.is_relative_to(ROOT): raise ValueError('new output outside source required')
    out.mkdir(parents=True)
    rows=verify()
    source=(ROOT/'price_budget.py').read_text()
    result={'passed':False,'python':sys.version,'distinct_tests':26,'distinct_semantic_mutations':len(MUTANTS),
            'modes':[],'meaning':'finite exact checks and same-author replay; not independent analytic acceptance'}
    try:
        for mode,flags in [('normal',[]),('optimized',['-O'])]:
            base=[sys.executable,'-B',*flags,'-S']
            proc=subprocess.run(base+['-m','unittest','-v','test_price_budget'],cwd=ROOT,capture_output=True,text=True,timeout=45)
            (out/(mode+'.stdout')).write_text(proc.stdout)
            (out/(mode+'.stderr')).write_text(proc.stderr)
            if proc.returncode or 'Ran 26 tests' not in proc.stderr or 'skipped=' in proc.stderr: raise RuntimeError('baseline failed: '+mode)
            run=subprocess.run(base+['price_budget.py'],cwd=ROOT,capture_output=True,timeout=45)
            (out/(mode+'.json')).write_bytes(run.stdout)
            if run.returncode or run.stdout!=(ROOT/'RESULTS.json').read_bytes(): raise RuntimeError('output mismatch')
            for tag,(old,new) in MUTANTS.items():
                if source.count(old)!=1: raise RuntimeError('nonunique mutation: '+tag)
                scratch=out/'mutants'/mode/tag; scratch.mkdir(parents=True)
                (scratch/'price_budget.py').write_text(source.replace(old,new))
                for name in ('test_price_budget.py','RESULTS.json'): shutil.copyfile(ROOT/name,scratch/name)
                proc=subprocess.run(base+['-m','unittest','-v','test_price_budget'],cwd=scratch,capture_output=True,text=True,timeout=45)
                (out/(tag+'-'+mode+'.stderr')).write_text(proc.stderr)
                if proc.returncode==0 or 'AssertionError' not in proc.stderr: raise RuntimeError('mutation not assertion-detected: '+tag)
            result['modes'].append(mode)
        verify()
        result.update(passed=True,sources_unchanged=True,source_files_verified=len(rows))
    finally:
        (out/'REPORT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__': main()
