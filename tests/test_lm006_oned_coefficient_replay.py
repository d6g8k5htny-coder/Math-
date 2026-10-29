"""Execution/custody controls for the frozen PR380 one-dimensional coefficient."""
import importlib.util, json, os, subprocess, sys, tempfile, time, unittest
from pathlib import Path

DRIVER=Path(__file__).resolve().parents[1]/'tools/lm006_oned_coefficient_replay.py'

def load_driver(path):
    spec=importlib.util.spec_from_file_location('trusted_driver',path)
    module=importlib.util.module_from_spec(spec)
    raw=Path(path).read_bytes()
    exec(compile(raw,str(path),'exec',dont_inherit=True),module.__dict__)  # SOURCE_ONLY_LOADER
    module._LOADED_SOURCE=raw
    return module

class ReplayTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(DRIVER.is_file(),'replay implementation missing')
        self.m=load_driver(DRIVER)
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)/'repo';self.root.mkdir();self.logs=Path(self.tmp.name)/'logs';self.logs.mkdir()

    def fixture(self):
        pins={}
        for name in self.m.PINS:
            p=self.root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(('fixture:'+name+'\n').encode())
            pins[name]=self.m.git_blob(p.read_bytes())
        return pins

    def child(self, code, expected=b'ok\n', timeout=3, name='child'):
        return self.m.run_step([sys.executable,'-B','-S','-c',code],self.root,self.logs,name,expected,'exact',timeout)

    def test_timestamp_valid_poisoned_bytecode_cannot_replace_source(self):
        import py_compile
        source=DRIVER.read_bytes()
        original=b"REPOSITORY='d6g8k5htny-coder/Math-'"
        poisoned=b"REPOSITORY='x6g8k5htny-coder/Math-'"
        self.assertEqual(source.count(original),1)
        self.assertEqual(len(original),len(poisoned))
        path=self.root/'poisoned_driver.py'
        guard=b"if sys._getframe().f_code != compile(_LOADED_SOURCE,sys._getframe().f_code.co_filename,'exec',dont_inherit=True): raise RuntimeError('loaded_driver_drift')  # VERIFY_LOADED_CODE"
        self.assertEqual(source.count(guard),1)
        guardless=b"#"+b" "*(len(guard)-1)
        path.write_bytes(source.replace(original,poisoned,1).replace(guard,guardless,1))
        timestamp=1700000000
        os.utime(path,(timestamp,timestamp))
        py_compile.compile(str(path),doraise=True,optimize=sys.flags.optimize)
        path.write_bytes(source)
        os.utime(path,(timestamp,timestamp))
        self.assertEqual(path.stat().st_size,len(source))
        spec=importlib.util.spec_from_file_location('unsafe_demonstration',path)
        unsafe=importlib.util.module_from_spec(spec);spec.loader.exec_module(unsafe)
        self.assertEqual(unsafe.REPOSITORY,'x6g8k5htny-coder/Math-','fixture must actually load poisoned bytecode')
        self.assertEqual(unsafe._LOADED_SOURCE,source,'loaded-source read alone does not bind executed code')
        verified=load_driver(path)
        self.assertEqual(verified.REPOSITORY,'d6g8k5htny-coder/Math-')
        self.assertEqual(verified._LOADED_SOURCE,source)

    def test_poisoned_bytecode_control_kills_loader_mutation(self):
        import shutil
        source=Path(__file__).read_text()
        anchor="exec(compile(raw,str(path),'exec',dont_inherit=True),"+"module.__dict__)  # SOURCE_ONLY_LOADER"
        replacement="spec.loader.exec_module(module)  # SOURCE_ONLY_LOADER"
        self.assertEqual(source.count(anchor),1)
        with tempfile.TemporaryDirectory(prefix='lm006-loader-mutation-') as directory:
            root=Path(directory)
            test_path=root/'tests/test_lm006_oned_coefficient_replay.py'
            driver_path=root/'tools/lm006_oned_coefficient_replay.py'
            test_path.parent.mkdir(parents=True)
            driver_path.parent.mkdir(parents=True)
            shutil.copyfile(DRIVER,driver_path)
            command=[sys.executable,'-B','-S']+(['-O'] if sys.flags.optimize else [])+['-m','unittest','discover','-s','tests','-p','test_lm006_oned_coefficient_replay.py','-k','test_timestamp_valid_poisoned','-v']
            test_path.write_text(source)
            good=subprocess.run(command,cwd=root,capture_output=True,timeout=30)
            self.assertEqual(good.returncode,0,good.stderr.decode())
            self.assertIn(b'Ran 1 test in',good.stderr)
            self.assertTrue(good.stderr.endswith(b'\nOK\n'))
            test_path.write_text(source.replace(anchor,replacement,1))
            mutant=subprocess.run(command,cwd=root,capture_output=True,timeout=30)
            self.assertEqual(mutant.returncode,1,mutant.stderr.decode())
            self.assertEqual(mutant.stdout,b'')
            self.assertIn(b'Ran 1 test in',mutant.stderr)
            self.assertIn(b'FAILED (failures=1)',mutant.stderr)
            self.assertIn(b"AssertionError: 'x6g8k5htny-coder/Math-'",mutant.stderr)
            self.assertNotIn(b'ERROR:',mutant.stderr)

    def test_direct_import_detects_timestamp_valid_stale_code(self):
        import py_compile
        source=DRIVER.read_bytes()
        old=b"REPOSITORY='d6g8k5htny-coder/Math-'"
        new=b"REPOSITORY='x6g8k5htny-coder/Math-'"
        self.assertEqual(source.count(old),1)
        path=self.root/'drift_driver.py'
        path.write_bytes(source.replace(old,new,1))
        os.utime(path,(1700000000,1700000000))
        py_compile.compile(str(path),doraise=True,optimize=sys.flags.optimize)
        path.write_bytes(source)
        os.utime(path,(1700000000,1700000000))
        spec=importlib.util.spec_from_file_location('drift_driver',path)
        module=importlib.util.module_from_spec(spec)
        with self.assertRaisesRegex(RuntimeError,'^loaded_driver_drift$'):
            spec.loader.exec_module(module)
        self.assertEqual(module._LOADED_SOURCE,source)

    def test_direct_import_guard_mutation_is_rejected(self):
        import shutil
        driver=DRIVER.read_text()
        anchor="if sys._getframe().f_code != compile(_LOADED_SOURCE,sys._getframe().f_code.co_filename,'exec',dont_inherit=True): raise RuntimeError('loaded_driver_drift')  # VERIFY_LOADED_CODE"
        self.assertEqual(driver.count(anchor),1)
        with tempfile.TemporaryDirectory(prefix='lm006-guard-mutation-') as directory:
            root=Path(directory)
            test_path=root/'tests/test_lm006_oned_coefficient_replay.py'
            driver_path=root/'tools/lm006_oned_coefficient_replay.py'
            test_path.parent.mkdir(parents=True)
            driver_path.parent.mkdir(parents=True)
            shutil.copyfile(Path(__file__),test_path)
            driver_path.write_text(driver)
            command=[sys.executable,'-B','-S']+(['-O'] if sys.flags.optimize else [])+['-m','unittest','discover','-s','tests','-p','test_lm006_oned_coefficient_replay.py','-k','test_direct_import_detects_timestamp_valid_stale_code','-v']
            good=subprocess.run(command,cwd=root,capture_output=True,timeout=30)
            self.assertEqual(good.returncode,0,good.stderr.decode())
            self.assertIn(b'Ran 1 test in',good.stderr)
            self.assertTrue(good.stderr.endswith(b'\nOK\n'))
            driver_path.write_text(driver.replace(anchor,'# guard removed',1))
            mutant=subprocess.run(command,cwd=root,capture_output=True,timeout=30)
            self.assertEqual(mutant.returncode,1,mutant.stderr.decode())
            self.assertEqual(mutant.stdout,b'')
            self.assertIn(b'Ran 1 test in',mutant.stderr)
            self.assertIn(b'FAILED (failures=1)',mutant.stderr)
            self.assertIn(b'AssertionError: RuntimeError not raised',mutant.stderr)
            self.assertNotIn(b'ERROR:',mutant.stderr)

    def test_snapshot_and_exact_packet_membership(self):
        pins=self.fixture();ids=self.m.validate_snapshot(self.root,pins)
        self.assertEqual(set(ids),set(pins))
        extra=self.root/self.m.PACKET/'extra';extra.write_text('x')
        with self.assertRaisesRegex(self.m.ReplayError,'packet_membership'): self.m.validate_snapshot(self.root,pins)

    def test_changed_missing_and_symlink_sources_rejected(self):
        pins=self.fixture();name=next(iter(pins));p=self.root/name;old=p.read_bytes()
        p.write_bytes(old+b'x')
        with self.assertRaisesRegex(self.m.ReplayError,'source_identity'): self.m.validate_snapshot(self.root,pins)
        p.unlink()
        with self.assertRaisesRegex(self.m.ReplayError,'source_missing'): self.m.validate_snapshot(self.root,pins)
        p.write_bytes(old); outside=Path(self.tmp.name)/'outside';outside.write_bytes(old);p.unlink();p.symlink_to(outside)
        with self.assertRaisesRegex(self.m.ReplayError,'source_symlink'): self.m.validate_snapshot(self.root,pins)

    def test_path_validation(self):
        for name in ('../x','/x','a/../b','a//b','a\\b','a/./b',''):
            with self.assertRaises(self.m.ReplayError): self.m.source_file(self.root,name)

    def test_success_process_record(self):
        row=self.child("print('ok')");self.assertEqual(row['status'],'PASS');self.assertFalse(row['timed_out'])
        self.assertEqual((self.logs/'child.stdout').read_bytes(),b'ok\n')

    def test_wrong_exit_output_and_stderr_rejected(self):
        cases=[("raise RuntimeError('x')",'unexpected_exit'),('pass','stdout_mismatch'),("print('bad')",'stdout_mismatch'),("import sys;print('ok');print('w',file=sys.stderr)",'unexpected_stderr')]
        for i,(code,reason) in enumerate(cases):
            with self.assertRaisesRegex(self.m.ReplayError,reason): self.child(code,name='bad'+str(i))

    def test_timeout_retains_partial_evidence(self):
        with self.assertRaisesRegex(self.m.ReplayError,'timeout'):
            self.child("import sys,time;print('s',flush=True);print('e',file=sys.stderr,flush=True);time.sleep(10)",timeout=.2)
        row=json.loads((self.logs/'child.process.json').read_text());self.assertTrue(row['timed_out']);self.assertEqual(row['failure'],'timeout')

    def test_existing_evidence_not_overwritten(self):
        self.child("print('ok')");before={p.name:p.read_bytes() for p in self.logs.iterdir()}
        with self.assertRaisesRegex(self.m.ReplayError,'step_evidence_exists'): self.child("print('changed')")
        self.assertEqual(before,{p.name:p.read_bytes() for p in self.logs.iterdir()})

    def test_test_report_contract_requires_all_named_passes(self):
        good=('\n'.join(n+' (test_oned.OneDimensionalTests.'+n+') ... ok' for n in self.m.TEST_NAMES)+'\n\n'+'-'*70+'\nRan 15 tests in 0.001s\n\nOK\n').encode()
        self.m.check_output(b'',good,None,'tests')
        for bad in (good.replace(b' ... ok',b' ... FAIL',1),good+b'noise',good.replace(b'Ran 15',b'Ran 0')):
            with self.assertRaisesRegex(self.m.ReplayError,'test_report_mismatch'): self.m.check_output(b'',bad,None,'tests')

    def test_exact_output_contract_is_byte_exact(self):
        want=b'{"panels":1024,"independently_reviewed":false}\n';self.m.check_output(want,b'',want,'exact')
        for bad in (b'',want+b'\n',want.replace(b'false',b'true')):
            with self.assertRaisesRegex(self.m.ReplayError,'stdout_mismatch'): self.m.check_output(bad,b'',want,'exact')

    def test_host_identity(self):
        h='1'*40;env={'GITHUB_ACTIONS':'true','GITHUB_REPOSITORY':self.m.REPOSITORY,'GITHUB_SHA':h,'GITHUB_RUN_ID':'1','GITHUB_RUN_ATTEMPT':'2'}
        self.m.host_identity(h,env)
        env['GITHUB_SHA']='2'*40
        with self.assertRaisesRegex(self.m.ReplayError,'host_identity'): self.m.host_identity(h,env)

    def test_invalid_cli(self):
        for args in ([],['--mode','bad','--output','x'],['--mode','normal','--output','x','--panels','2048']):
            p=subprocess.run([sys.executable,'-B','-S',str(DRIVER),*args],capture_output=True);self.assertEqual(p.returncode,2)

    def test_workflow_contract(self):
        wf=DRIVER.parents[1]/'.github/workflows/lm006-oned-coefficient.yml';self.assertTrue(wf.is_file(),'workflow missing')
        text=wf.read_text()
        for phrase in ('permissions:\n  contents: read','fail-fast: false','mode: [normal, optimized]','if: always()',"python-version: '3.11.16'",'persist-credentials: false','if-no-files-found: error'):
            self.assertIn(phrase,text)
        self.assertNotIn('continue-on-error:',text);self.assertNotIn('pull_request_target:',text)


    def synthetic_project(self, bad_test=False, output='synthetic', mutate=False):
        import shutil
        previous=os.environ.get('GITHUB_ACTIONS')
        self.addCleanup(lambda: os.environ.pop('GITHUB_ACTIONS',None) if previous is None else os.environ.__setitem__('GITHUB_ACTIONS',previous))
        os.environ['GITHUB_ACTIONS']='false'
        pins=self.fixture(); packet=self.root/self.m.PACKET
        (packet/'RESULTS.json').write_text('synthetic\n')
        methods='\n'.join('    def '+n+'(self): self.assertTrue('+('False' if bad_test and i==0 else 'True')+')' for i,n in enumerate(self.m.TEST_NAMES))
        (packet/'test_oned.py').write_text('import unittest\nclass OneDimensionalTests(unittest.TestCase):\n'+methods+'\n')
        suffix="\nfrom pathlib import Path;Path('NOTE.md').write_text('changed')" if mutate else ''
        (packet/'oned.py').write_text("import sys\nassert sys.argv[1:]==['--panels','1024']\nprint("+repr(output)+")"+suffix+'\n')
        for name in self.m.EXECUTION_FILES:
            d=self.root/name;d.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(DRIVER.parents[1]/name,d)
        subprocess.run(['git','init','-q'],cwd=self.root,check=True);subprocess.run(['git','add','.'],cwd=self.root,check=True)
        subprocess.run(['git','-c','user.name=Fixture','-c','user.email=f@example.invalid','-c','commit.gpgsign=false','commit','-qm','fixture'],cwd=self.root,check=True)
        mod=load_driver(self.root/self.m.EXECUTION_FILES[0])
        mod.PINS={n:mod.git_blob((self.root/n).read_bytes()) for n in pins}
        return mod

    def test_complete_orchestration_real_subprocesses(self):
        mod=self.synthetic_project();out=Path(self.tmp.name)/'ok';receipt=mod.execute(self.root,out,'optimized')
        self.assertEqual(receipt['status'],'PASS');self.assertEqual(set(receipt['steps']),{'tests','coefficient'});self.assertEqual((out/'coefficient.stdout').read_bytes(),b'synthetic\n')

    def test_failed_tests_stop_before_coefficient(self):
        mod=self.synthetic_project(bad_test=True);out=Path(self.tmp.name)/'badtests'
        with self.assertRaisesRegex(mod.ReplayError,'unexpected_exit'): mod.execute(self.root,out,'normal')
        self.assertFalse((out/'coefficient.stdout').exists());self.assertEqual(json.loads((out/'receipt.json').read_text())['status'],'FAIL')

    def test_wrong_output_cannot_pass(self):
        mod=self.synthetic_project(output='wrong');out=Path(self.tmp.name)/'wrong'
        with self.assertRaisesRegex(mod.ReplayError,'stdout_mismatch'): mod.execute(self.root,out,'normal')
        row=json.loads((out/'receipt.json').read_text());self.assertEqual(row['steps']['tests']['record']['status'],'PASS');self.assertEqual(row['steps']['coefficient']['record']['status'],'FAIL')

    def test_postflight_source_drift_rejected(self):
        mod=self.synthetic_project(mutate=True);out=Path(self.tmp.name)/'drift'
        with self.assertRaisesRegex(mod.ReplayError,'source_identity'): mod.execute(self.root,out,'normal')
        self.assertEqual(json.loads((out/'receipt.json').read_text())['status'],'FAIL')

    def test_secondary_timeout_still_writes_process_record(self):
        from unittest.mock import patch
        waits=[]
        class Stuck:
            pid=424242
            def __init__(self,*args,**kwargs):
                kwargs['stdout'].write(b'started\n')
                kwargs['stderr'].write(b'partial\n')
            def wait(self,timeout=None):
                waits.append(timeout)
                raise subprocess.TimeoutExpired(['controlled-no-process'],timeout)
        with patch.object(self.m.subprocess,'Popen',Stuck),patch.object(self.m.os,'killpg') as kill:
            with self.assertRaisesRegex(self.m.ReplayError,'timeout'):
                self.m.run_step(['controlled-no-process'],self.root,self.logs,'stuck',b'','exact',1)
            kill.assert_called_once_with(424242,self.m.signal.SIGKILL)
        self.assertEqual(waits,[1,5])
        row=json.loads((self.logs/'stuck.process.json').read_text())
        self.assertEqual((row['status'],row['failure'],row['timed_out'],row['returncode']),('FAIL','timeout',True,None))
        self.assertEqual(row['detail'],'process-group termination did not finish in 5 seconds')
        for side,value in [('stdout',b'started\n'),('stderr',b'partial\n')]:
            self.assertEqual((self.logs/('stuck.'+side)).read_bytes(),value)
            self.assertEqual(row[side+'_bytes'],len(value))
            self.assertEqual(row[side+'_sha256'],self.m.sha256(value))


    def check_custody_child_mode(self):
        requested=os.environ.get('LM006_EXPECT_OPTIMIZE')
        if requested is not None:
            self.assertEqual(sys.flags.optimize,int(requested))

    def test_git_replacement_cannot_relabel_a_frozen_blob(self):
        self.check_custody_child_mode()
        mod=self.synthetic_project()
        relative=self.m.PACKET+'/NOTE.md'
        expected=(self.root/relative).read_text().strip()
        original=mod.git_head(self.root)
        (self.root/relative).write_text('replacement source bytes\n')
        subprocess.run(['git','add',relative],cwd=self.root,check=True)
        subprocess.run(['git','-c','user.name=Fixture','-c','user.email=f@example.invalid','-c','commit.gpgsign=false','commit','-qm','replacement target'],cwd=self.root,check=True)
        replacement=mod.git_head(self.root)
        subprocess.run(['git','replace',original,replacement],cwd=self.root,check=True)
        self.assertEqual(mod.git(self.root,'show',original+':'+relative),expected)

    def test_ambient_git_environment_cannot_redirect_source_checks(self):
        self.check_custody_child_mode()
        from unittest.mock import patch
        mod=self.synthetic_project()
        own=mod.git_head(self.root)
        foreign=Path(self.tmp.name)/'foreign';foreign.mkdir()
        (foreign/'foreign.txt').write_text('different committed repository\n')
        subprocess.run(['git','init','-q'],cwd=foreign,check=True)
        subprocess.run(['git','add','.'],cwd=foreign,check=True)
        subprocess.run(['git','-c','user.name=Fixture','-c','user.email=f@example.invalid','-c','commit.gpgsign=false','commit','-qm','foreign'],cwd=foreign,check=True)
        with patch.dict(os.environ,{'GIT_DIR':str(foreign/'.git'),'GIT_WORK_TREE':str(foreign)}):
            self.assertEqual(mod.git_head(self.root),own)

    def test_loaded_driver_cannot_claim_a_later_committed_source(self):
        self.check_custody_child_mode()
        mod=self.synthetic_project()
        driver=self.root/self.m.EXECUTION_FILES[0]
        driver.write_bytes(driver.read_bytes()+b'\n# committed after this module was loaded\n')
        subprocess.run(['git','add',self.m.EXECUTION_FILES[0]],cwd=self.root,check=True)
        subprocess.run(['git','-c','user.name=Fixture','-c','user.email=f@example.invalid','-c','commit.gpgsign=false','commit','-qm','source successor'],cwd=self.root,check=True)
        out=Path(self.tmp.name)/'loaded-drift'
        with self.assertRaisesRegex(mod.ReplayError,'loaded_driver_drift'):
            mod.execute(self.root,out,'normal')
        self.assertEqual(json.loads((out/'receipt.json').read_text())['status'],'FAIL')
        self.assertFalse((out/'tests.stdout').exists())


    def test_custody_guards_reject_three_real_source_mutations(self):
        import base64, shutil
        source=DRIVER.read_text()
        cases=[
            ('ambient',"env={key:value for key,value in os.environ.items() if not key.startswith('GIT_')}  # MUTATION_GIT_ENV",
             "env=dict(os.environ)  # MUTATION_GIT_ENV",
             'test_ambient_git_environment_cannot_redirect_source_checks',
             b'self.assertEqual(mod.git_head(self.root),own)'),
            ('replacement',"GIT_NO_REPLACE_OBJECTS='1',","",
             'test_git_replacement_cannot_relabel_a_frozen_blob',
             b"self.assertEqual(mod.git(self.root,'show',original+':'+relative),expected)"),
            ('loaded',"require(raw==_LOADED_SOURCE,'loaded_driver_drift')  # MUTATION_LOADED_DRIVER",
             "require(True,'loaded_driver_drift')  # MUTATION_LOADED_DRIVER",
             'test_loaded_driver_cannot_claim_a_later_committed_source',
             b'AssertionError: ReplayError not raised'),
        ]
        for label,anchor,replacement,target,reason in cases:
            with self.subTest(source_mutation=label):
                self.assertEqual(source.count(anchor),1,'unique source mutation anchor')
                with tempfile.TemporaryDirectory(prefix='lm006-custody-source-mutant-') as temporary:
                    scratch=Path(temporary)
                    for relative in self.m.EXECUTION_FILES:
                        destination=scratch/relative
                        destination.parent.mkdir(parents=True,exist_ok=True)
                        shutil.copyfile(DRIVER.parents[1]/relative,destination)
                    command=[sys.executable,'-B','-S']+(['-O'] if sys.flags.optimize else [])+['-m','unittest','discover','-s','tests','-p','test_lm006_oned_coefficient_replay.py','-k',target,'-v']
                    environment=dict(os.environ,LM006_EXPECT_OPTIMIZE=str(sys.flags.optimize))
                    baseline=subprocess.run(command,cwd=scratch,env=environment,capture_output=True,timeout=30)
                    self.assertEqual(baseline.returncode,0,baseline.stderr.decode())
                    self.assertIn(b'Ran 1 test in',baseline.stderr)
                    self.assertTrue(baseline.stderr.endswith(b'\nOK\n'))
                    (scratch/self.m.EXECUTION_FILES[0]).write_text(source.replace(anchor,replacement,1))
                    mutant=subprocess.run(command,cwd=scratch,env=environment,capture_output=True,timeout=30)
                    self.assertEqual(mutant.returncode,1,mutant.stderr.decode())
                    self.assertEqual(mutant.stdout,b'')
                    self.assertIn(b'Ran 1 test in',mutant.stderr)
                    self.assertIn(b'FAILED (failures=1)',mutant.stderr)
                    self.assertNotIn(b'ERROR:',mutant.stderr)
                    self.assertIn(reason,mutant.stderr)
                    self.assertNotIn(b'self.assertEqual(sys.flags.optimize',mutant.stderr)
                    record={'label':label,'optimize':sys.flags.optimize,'command':command,
                            'baseline_exit':baseline.returncode,'mutant_exit':mutant.returncode,
                            'driver_sha256':self.m.sha256(source.encode()),
                            'stdout_base64':base64.b64encode(mutant.stdout).decode(),
                            'stderr_base64':base64.b64encode(mutant.stderr).decode()}
                    print('LM006_CUSTODY_SOURCE_MUTATION '+json.dumps(record,sort_keys=True),file=sys.stderr)

if __name__=='__main__': unittest.main()
