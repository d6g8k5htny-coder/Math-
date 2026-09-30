"""Exact packet replay with optional real upstream Git verification."""
import argparse,io,json,pathlib,subprocess,sys,unittest
import custody
ROOT=pathlib.Path(__file__).resolve().parent
MUTANTS={
 'wrong-schur-derivative':'test_reduced_third_derivative',
 'half-hermite':'test_hermite_integral_normalization',
 'linear-norm-threshold':'test_threshold_quadratic_norm',
 'lose-rare-scale':'test_rare_norm_tail_keeps_scale',
 'normalizer-twice':'test_mixed_local_remote_ledger',
 'omit-remote-singletons':'test_global_rates_and_factorials',
 'ignore-middle-region':'test_missing_middle_is_not_automatic',
 'palm-equals-nonempty':'test_nonempty_and_sizebiased_differ',
}

def source_ids():
    mp=ROOT/'SOURCE_FILES.json'
    custody.require(not mp.is_symlink() and mp.is_file(),'regular manifest required')
    entries=custody.loads(mp.read_text())['files'];custody.unique_paths(entries)
    custody.require(sorted(x.name for x in ROOT.iterdir())==sorted([e['path'] for e in entries]+['SOURCE_FILES.json']),'packet membership differs')
    for e in entries:
        custody.require(pathlib.Path(e['path']).name==e['path'],'packet must be flat')
        custody.read_checked(ROOT,e)
    return {p.name:custody.identity(p.read_bytes()) for p in sorted(ROOT.iterdir())}

def child(mutant):
    import controls,test_controls,test_custody
    controls.MUTANT=mutant
    suite=unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromModule(x) for x in (test_controls,test_custody)])
    result=unittest.TextTestRunner(stream=io.StringIO()).run(suite)
    print(json.dumps({'tests':result.testsRun,'passed':result.wasSuccessful(),
         'failures':sorted(t.id().split('.')[-1] for t,_ in result.failures),
         'errors':sorted(t.id().split('.')[-1] for t,_ in result.errors)},sort_keys=True))
    return 0 if result.wasSuccessful() else 1

def replay(out,repo):
    out=out.resolve();custody.require(not out.exists() and not out.is_relative_to(ROOT),'new external output required')
    before=source_ids();count=custody.upstream(repo,custody.loads((ROOT/'SOURCE_MAP.json').read_text())['sources']) if repo else None
    out.mkdir(parents=True);records={}
    for case in ['baseline',*MUTANTS]:
        pair=[]
        for mode,flags in [('normal',[]),('optimized',['-O'])]:
            cmd=[sys.executable,'-B',*flags,'-S',str(ROOT/'verify.py'),'--child']
            if case!='baseline':cmd+=['--mutant',case]
            p=subprocess.run(cmd,capture_output=True,timeout=30)
            (out/(case+'_'+mode+'.stdout')).write_bytes(p.stdout);(out/(case+'_'+mode+'.stderr')).write_bytes(p.stderr)
            r=custody.loads(p.stdout.decode());custody.require(not p.stderr and not r['errors'] and r['tests']==18,'execution error')
            if case=='baseline':custody.require(p.returncode==0 and r['passed'],'baseline failed')
            else:custody.require(p.returncode==1 and not r['passed'] and MUTANTS[case] in r['failures'],'intended semantic failure missing')
            pair.append(p.stdout)
        custody.require(pair[0]==pair[1],'Python mode disagreement');records[case]=custody.loads(pair[0].decode())
    summary={'tests_per_mode':18,'mathematical_tests':12,'custody_fixture_tests':6,'semantic_mutants_per_mode':8,
             'paired_outputs_identical':9,'scientific_effect':'NONE','analytic_acceptance':False}
    custody.require(summary==custody.loads((ROOT/'RESULTS.json').read_text()),'stored summary differs')
    custody.require(before==source_ids(),'sources changed')
    (out/'REPORT.json').write_text(json.dumps({**summary,'upstream_verified_count':count,'source_identities':before,'cases':records},sort_keys=True,indent=2)+'\n')
    print(json.dumps(summary,sort_keys=True,indent=2));return 0

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--child',action='store_true');g.add_argument('--output',type=pathlib.Path)
    p.add_argument('--mutant',choices=MUTANTS);p.add_argument('--repo',type=pathlib.Path)
    a=p.parse_args();custody.require(a.child or a.mutant is None,'mutant needs child mode')
    raise SystemExit(child(a.mutant) if a.child else replay(a.output,a.repo))
