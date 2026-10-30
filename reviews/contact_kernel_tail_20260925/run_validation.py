"""Bounded replay; finite checks and detected mutants are not analytic acceptance."""
from __future__ import annotations
from pathlib import Path
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
TEST_COUNT=24
MUTANTS={
 'lose_midpoint_shift':('u*u-u*w+Q(1,4)','u*u-u*w'),
 'wrong_q_parameter':('q=6*k*(w-2*u)/v','q=6*k*(w-u)/v'),
 'lose_endpoint_k2':('return (24*k)*(6*k)*(9*k*k)**3/(36*k*k)','return (24*k)*(6*k)*(9*k*k)**3/36'),
 'wrong_type_region':('((lower_left,-3,-1),(lower_right,-1,1))','((lower_left,-3,-1),(lower_left,-1,1))'),
 'wrong_height_orientation':('return -2*u**3-Q(3,2)*u-1+2*t+3*w*(u*u-Q(1,4))','return -2*u**3-Q(3,2)*u+1-2*t+3*w*(u*u-Q(1,4))'),
 'wrong_gaussian_moment':('(n-1)*out[n-2]/(2*a)','(n+1)*out[n-2]/(2*a)'),
 'promote_small_gap_uniformity':("'finite_r_small_k_uniformity':False","'finite_r_small_k_uniformity':True"),
}
EXPECTED_FAILURES={
 'lose_midpoint_shift':frozenset({
  'test_contact_tools.ContactTests.test_critical_constraints',
  'test_contact_tools.ContactTests.test_exact_contact_fixture',
  'test_contact_tools.ContactTests.test_typed_determinant_forms',
 }),
 'wrong_q_parameter':frozenset({
  'test_contact_tools.ContactTests.test_critical_constraints',
  'test_contact_tools.ContactTests.test_exact_contact_fixture',
  'test_contact_tools.ContactTests.test_typed_determinant_forms',
 }),
 'lose_endpoint_k2':frozenset({
  'test_contact_tools.ContactTests.test_w_jacobian_is_counted_once',
 }),
 'wrong_type_region':frozenset({
  'test_contact_tools.ContactTests.test_claim_scope_metadata',
  'test_contact_tools.ContactTests.test_exact_shape_integral',
  'test_contact_tools.ContactTests.test_two_pieces',
  'test_contact_tools.ContactTests.test_type_area',
  'test_contact_tools.ContactTests.test_universal_rational_coefficient',
 }),
 'wrong_height_orientation':frozenset({
  'test_contact_tools.ContactTests.test_critical_constraints',
  'test_contact_tools.ContactTests.test_saddle_side_remainder_identity',
 }),
 'wrong_gaussian_moment':frozenset({
  'test_contact_tools.ContactTests.test_gaussian_moments_symmetric',
  'test_contact_tools.ContactTests.test_gaussian_polynomial_reduction_against_simpson',
 }),
 'promote_small_gap_uniformity':frozenset({
  'test_contact_tools.ContactTests.test_claim_scope_metadata',
 }),
}
FAIL_RE=re.compile(r'^FAIL: ([^\s]+) \(([^)]+)\)$',re.MULTILINE)
ERROR_RE=re.compile(r'^ERROR: ',re.MULTILINE)
RUN_RE=re.compile(r'^Ran (\d+) tests? in [^\n]+$',re.MULTILINE)
FAILED_RE=re.compile(r'^FAILED \(failures=(\d+)\)$',re.MULTILINE)

def require(ok,message):
    if not ok:raise RuntimeError(message)

def identities():
    pins=json.loads((ROOT/'SOURCE_FILES.json').read_text())['files']
    for name,identity in pins.items():
        p=ROOT/name
        require(p.name==name and not p.is_symlink() and p.is_file(),'flat regular source required')
        raw=p.read_bytes()
        require({'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}==identity,'identity mismatch: '+name)
    return pins

def _failure_ids(stderr,name):
    matches=list(FAIL_RE.finditer(stderr))
    ids=[]
    for match in matches:
        short,full=match.groups()
        require(short==full.rsplit('.',1)[-1],'malformed unittest failure identity '+name)
        ids.append(full)
        block_end=matches[matches.index(match)+1].start() if matches.index(match)+1<len(matches) else len(stderr)
        block=stderr[match.end():block_end]
        require('AssertionError:' in block,'non-assertion failure block '+full+' in '+name)
    require(len(ids)==len(set(ids)),'duplicate unittest failure identity '+name)
    return frozenset(ids)

def run_cmd(cmd,cwd,out,name,mutant=None):
    p=subprocess.run(cmd,cwd=cwd,capture_output=True,text=True,timeout=30)
    (out/(name+'.stdout')).write_text(p.stdout)
    (out/(name+'.stderr')).write_text(p.stderr)
    count=RUN_RE.search(p.stderr)
    require(count is not None and int(count.group(1))==TEST_COUNT,'unexpected test coverage '+name)
    require(not ERROR_RE.search(p.stderr),'unittest error '+name)
    require(not re.search(r'\bskipped\b',p.stderr,re.IGNORECASE),'skipped test '+name)
    require(not p.stdout,'unexpected test stdout '+name)
    failures=_failure_ids(p.stderr,name)
    if mutant is None:
        require(p.returncode==0 and not failures and re.search(r'^OK$',p.stderr,re.MULTILINE) is not None,'baseline failure '+name)
        return []
    expected=EXPECTED_FAILURES[mutant]
    summary=FAILED_RE.search(p.stderr)
    require(p.returncode==1,'mutant did not exit with unittest failure '+name)
    require(summary is not None and int(summary.group(1))==len(expected),'unexpected failure summary '+name)
    require(failures==expected,'wrong mutant failure identity '+name+': expected '+repr(sorted(expected))+' got '+repr(sorted(failures)))
    return sorted(failures)

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True)
    out=parser.parse_args().output.resolve()
    require(not out.exists() and not out.is_relative_to(ROOT),'new output outside source required')
    out.mkdir(parents=True);before=identities();source=(ROOT/'contact_tools.py').read_text()
    require(set(MUTANTS)==set(EXPECTED_FAILURES),'mutant/failure contract keys differ')
    report={'passed':False,'python':sys.version,'distinct_tests':TEST_COUNT,'distinct_mutants':len(MUTANTS),'modes':[],
            'expected_failure_ids':{k:sorted(v) for k,v in EXPECTED_FAILURES.items()},
            'observed_failure_ids':{},
            'meaning':'finite exact algebra and diagnostic implementation checks, not independent continuum review'}
    try:
        for mode,flags in [('normal',[]),('optimized',['-O'])]:
            cmd=[sys.executable,'-B',*flags,'-S','-m','unittest','-v','test_contact_tools']
            run_cmd(cmd,ROOT,out,'baseline_'+mode)
            result=subprocess.run([sys.executable,'-B',*flags,'-S','contact_tools.py'],cwd=ROOT,capture_output=True,timeout=10)
            require(result.returncode==0 and result.stdout==(ROOT/'RESULTS.json').read_bytes(),'output byte mismatch')
            for name,(old,new) in MUTANTS.items():
                require(source.count(old)==1,'nonunique mutation '+name)
                temp=out/'mutants'/mode/name;temp.mkdir(parents=True)
                (temp/'contact_tools.py').write_text(source.replace(old,new))
                shutil.copyfile(ROOT/'test_contact_tools.py',temp/'test_contact_tools.py')
                observed=run_cmd(cmd,temp,out,'mutation_'+mode+'_'+name,mutant=name)
                report['observed_failure_ids'].setdefault(name,{})[mode]=observed
            report['modes'].append(mode)
        require(before==identities(),'sources changed')
        report.update(passed=True,sources_unchanged=True,source_files=before)
    finally:
        (out/'REPORT.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps(report,sort_keys=True))

if __name__=='__main__':main()
