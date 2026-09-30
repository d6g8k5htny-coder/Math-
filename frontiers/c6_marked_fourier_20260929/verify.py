"""Exact packet controls and named negative variants. No analytic acceptance."""
from pathlib import Path
import sys,unittest,io,json,argparse,hashlib,subprocess
ROOT=Path(__file__).resolve().parent
MUTANTS={'forget-holder-two':'test_holder_needs_twice_the_rate','exponential-every-d':'test_dimension_exponent','drop-mean':'test_conditional_mean_is_not_dropped','drop-prefactor':'test_tail_prefactor_is_retained','duplicate-weight':'test_one_original_weight_and_normalizer','drop-count-mark':'test_count_weight_is_required','nonempty-is-palm':'test_nonempty_and_sizebiased_are_distinct','drop-tail-count':'test_cluster_tail_includes_n'}
def require(ok,msg):
 if not ok:raise ValueError(msg)
def identity(p):
 require(p.is_file() and not p.is_symlink(),'regular file required')
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def decode(s):
 def pairs(xs):
  d={}
  for k,v in xs:
   require(k not in d,'duplicate JSON key');d[k]=v
  return d
 return json.loads(s,object_pairs_hook=pairs)
def sources():
 identity(ROOT/'SOURCE_FILES.json');m=decode((ROOT/'SOURCE_FILES.json').read_text())['files']
 require(sorted(p.name for p in ROOT.iterdir())==sorted([*m,'SOURCE_FILES.json']),'packet membership differs')
 for n,e in m.items():
  require(Path(n).name==n and identity(ROOT/n)==e,'source identity differs: '+n)
 return m

def child(mutant):
 import marked,test_marked
 marked.MUTANT=mutant
 r=unittest.TextTestRunner(stream=io.StringIO()).run(unittest.defaultTestLoader.loadTestsFromModule(test_marked))
 print(json.dumps({'tests':r.testsRun,'passed':r.wasSuccessful(),'failures':sorted(t.id().split('.')[-1] for t,_ in r.failures),'errors':sorted(t.id().split('.')[-1] for t,_ in r.errors)},sort_keys=True))
 return 0 if r.wasSuccessful() else 1

def replay(out):
 out=out.resolve();require(not out.exists() and not out.is_relative_to(ROOT),'new external output required');before=sources();out.mkdir(parents=True)
 cases={}
 for name in ['baseline',*MUTANTS]:
  pair=[]
  for mode,flags in [('normal',[]),('optimized',['-O'])]:
   cmd=[sys.executable,'-B',*flags,'-S',str(ROOT/'verify.py'),'--child']
   if name!='baseline':cmd+=['--mutant',name]
   p=subprocess.run(cmd,capture_output=True,timeout=30);r=decode(p.stdout.decode())
   (out/(name+'_'+mode+'.stdout')).write_bytes(p.stdout);(out/(name+'_'+mode+'.stderr')).write_bytes(p.stderr)
   require(not p.stderr and not r['errors'] and r['tests']==17,'execution error or test-count mismatch')
   if name=='baseline':require(p.returncode==0 and r['passed'],'baseline failed')
   else:require(p.returncode==1 and not r['passed'] and MUTANTS[name] in r['failures'],'intended semantic failure absent')
   pair.append(p.stdout)
  require(pair[0]==pair[1],'mode mismatch');cases[name]=decode(pair[0].decode())
 require(before==sources(),'source mutation')
 report={'tests_per_mode':17,'semantic_mutants_per_mode':8,'identical_output_pairs':9,'all_passed':True,'sources_unchanged':True,'analytic_acceptance':False,'verification_scope':'local packet; upstream check separate','cases':cases}
 (out/'REPORT.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='cases'},sort_keys=True))
if __name__=='__main__':
 p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True);g.add_argument('--child',action='store_true');g.add_argument('--output',type=Path);p.add_argument('--mutant',choices=MUTANTS);a=p.parse_args()
 require(a.child or a.mutant is None,'mutant requires child');raise SystemExit(child(a.mutant) if a.child else replay(a.output))
