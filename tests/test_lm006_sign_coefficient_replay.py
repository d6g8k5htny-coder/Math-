"""Real-process and source-custody controls; no new mathematical verdict."""
import importlib.util
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import tempfile
import time
import unittest

DRIVER = Path(__file__).resolve().parents[1] / 'tools/lm006_sign_coefficient_replay.py'

class ReplayTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(DRIVER.is_file(), 'replay implementation missing')
        spec = importlib.util.spec_from_file_location('lm006_replay', DRIVER)
        self.m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.m)
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'repo'
        self.root.mkdir()
        self.logs = Path(self.tmp.name) / 'logs'
        self.logs.mkdir()

    def fixture(self):
        pins = {}
        for name in self.m.PINS:
            p = self.root / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(('fixture: ' + name + '\n').encode())
            pins[name] = self.m.git_blob(p.read_bytes())
        return pins

    def child(self, code, expected=b'ok\n', kind='exact', timeout=3, name='child'):
        return self.m.run_step([sys.executable, '-B', '-S', '-c', code], self.root,
                               self.logs, name, expected, kind, timeout)

    def test_source_identity_and_exact_membership(self):
        pins = self.fixture()
        identities = self.m.validate_snapshot(self.root, pins)
        self.assertEqual(set(identities), set(pins))
        for name, pin in pins.items():
            self.assertEqual(identities[name]['git_blob'], pin)
            self.assertRegex(identities[name]['sha256'], '^[0-9a-f]{64}$')
        extra = self.root / self.m.PACKET / 'extra.txt'
        extra.write_text('extra')
        with self.assertRaisesRegex(self.m.ReplayError, 'packet_membership'):
            self.m.validate_snapshot(self.root, pins)

    def test_changed_or_missing_payload_and_upstream(self):
        pins = self.fixture()
        for name in pins:
            p = self.root / name
            old = p.read_bytes()
            p.write_bytes(old+b'changed')
            with self.assertRaisesRegex(self.m.ReplayError, 'source_identity'):
                self.m.validate_snapshot(self.root, pins)
            p.unlink()
            with self.assertRaisesRegex(self.m.ReplayError, 'source_missing'):
                self.m.validate_snapshot(self.root, pins)
            p.write_bytes(old)

    def test_symlink_leaf_and_parent_rejected(self):
        pins = self.fixture()
        p = self.root / self.m.PACKET / 'RESULTS.json'
        old = p.read_bytes()
        outside = Path(self.tmp.name)/'outside'
        outside.write_bytes(old)
        p.unlink();p.symlink_to(outside)
        with self.assertRaisesRegex(self.m.ReplayError, 'source_symlink'):
            self.m.validate_snapshot(self.root,pins)
        p.unlink();p.write_bytes(old)
        directory = self.root / 'reviews'
        moved = self.root / 'moved'
        directory.rename(moved);directory.symlink_to(moved,target_is_directory=True)
        with self.assertRaisesRegex(self.m.ReplayError, 'source_symlink'):
            self.m.validate_snapshot(self.root,pins)

    def test_path_validation(self):
        for name in ('../x','/x','a/../b','a//b','a\\b','a/./b',''):
            with self.subTest(name=name),self.assertRaises(self.m.ReplayError):
                self.m.source_file(self.root,name)

    def test_success_process_evidence(self):
        row = self.child("print('ok')")
        self.assertEqual(row['returncode'],0)
        self.assertFalse(row['timed_out'])
        self.assertEqual(row['status'],'PASS')
        self.assertEqual((self.logs/'child.stdout').read_bytes(),b'ok\n')
        self.assertEqual((self.logs/'child.stderr').read_bytes(),b'')
        self.assertEqual(json.loads((self.logs/'child.process.json').read_bytes()),row)

    def test_wrong_exit_silent_garbage_and_stderr(self):
        for i,(code,reason) in enumerate([
            ("raise RuntimeError('unrelated failure')",'unexpected_exit'),
            ("pass",'stdout_mismatch'),
            ("print('garbage')",'stdout_mismatch'),
            ("import sys;print('ok');print('warning',file=sys.stderr)",'unexpected_stderr')]):
            name='bad'+str(i)
            with self.subTest(code=code),self.assertRaisesRegex(self.m.ReplayError,reason):
                self.child(code,name=name)
            rec=json.loads((self.logs/(name+'.process.json')).read_bytes())
            self.assertEqual(rec['status'],'FAIL')
            self.assertEqual(rec['failure'],reason)

    def test_timeout_preserves_both_streams_and_process_record(self):
        with self.assertRaisesRegex(self.m.ReplayError,'timeout'):
            self.child("import sys,time;print('started',flush=True);print('partial',file=sys.stderr,flush=True);time.sleep(20)",timeout=0.3)
        rec=json.loads((self.logs/'child.process.json').read_bytes())
        self.assertTrue(rec['timed_out'])
        self.assertEqual(rec['failure'],'timeout')
        self.assertEqual((self.logs/'child.stdout').read_bytes(),b'started\n')
        self.assertEqual((self.logs/'child.stderr').read_bytes(),b'partial\n')
        self.assertIsInstance(rec['returncode'],int)

    @unittest.skipUnless(os.name=='posix','workflow and process groups are POSIX')
    def test_timeout_stops_child_process_group(self):
        marker=Path(self.tmp.name)/'late-marker'
        grandchild="import time;from pathlib import Path;time.sleep(1);Path("+repr(str(marker))+").write_text('bad')"
        code="import subprocess,sys,time;subprocess.Popen([sys.executable,'-c',"+repr(grandchild)+"]);print('ready',flush=True);time.sleep(20)"
        with self.assertRaisesRegex(self.m.ReplayError,'timeout'):
            self.child(code,timeout=0.3)
        time.sleep(1.1)
        self.assertFalse(marker.exists())

    def test_spawn_failure_has_record(self):
        with self.assertRaisesRegex(self.m.ReplayError,'spawn_error'):
            self.m.run_step(['/nonexistent/lm006-executable'],self.root,self.logs,'spawn',b'','exact',1)
        row=json.loads((self.logs/'spawn.process.json').read_bytes())
        self.assertEqual(row['status'],'FAIL');self.assertIsNone(row['returncode'])
        self.assertIn('FileNotFoundError',row['detail'])

    def test_existing_step_evidence_never_overwritten(self):
        self.child("print('ok')")
        old={p.name:p.read_bytes() for p in self.logs.iterdir()}
        with self.assertRaisesRegex(self.m.ReplayError,'step_evidence_exists'):
            self.child("print('changed')")
        self.assertEqual(old,{p.name:p.read_bytes() for p in self.logs.iterdir()})

    def test_unittest_contract_requires_all_named_passes(self):
        good=('\n'.join(name+' (test_enclosure.EnclosureTests.'+name+') ... ok' for name in self.m.TEST_NAMES)
             +'\n\n'+'-'*70+'\nRan 15 tests in 0.001s\n\nOK\n').encode()
        self.m.check_output(b'',good,None,'tests')
        altered=[good.replace(b' ... ok',b' ... skipped',1),good+b'noise',
                 good.replace(b'Ran 15',b'Ran 0'),good.replace(b' ... ok',b' ... FAIL',1),
                 good[good.index(b'\n\n')+2:],good.replace(self.m.TEST_NAMES[0].encode(),b'wrong_test',1)]
        for bad in altered:
            with self.assertRaisesRegex(self.m.ReplayError,'test_report_mismatch'):
                self.m.check_output(b'',bad,None,'tests')
        with self.assertRaisesRegex(self.m.ReplayError,'test_report_mismatch'):
            self.m.check_output(b'noise',good,None,'tests')

    def test_exact_output_contract_keeps_json_types_and_scope(self):
        want=b'{"independently_reviewed": false, "grid": 2048}\n'
        self.m.check_output(want,b'',want,'exact')
        for bad in (b'',want.replace(b'false',b'0'),want.replace(b'false',b'true'),want+b'\n'):
            with self.assertRaisesRegex(self.m.ReplayError,'stdout_mismatch'):
                self.m.check_output(bad,b'',want,'exact')
        with self.assertRaisesRegex(self.m.ReplayError,'unknown_contract'):
            self.m.check_output(b'',b'',b'','unknown')

    def test_host_identity_and_strict_run_identifiers(self):
        head='1'*40
        env={'GITHUB_ACTIONS':'true','GITHUB_REPOSITORY':self.m.REPOSITORY,
             'GITHUB_SHA':head,'GITHUB_RUN_ID':'123','GITHUB_RUN_ATTEMPT':'1'}
        self.m.host_identity(head,env)
        for key,bad in [('GITHUB_SHA','2'*40),('GITHUB_REPOSITORY','elsewhere/repo'),
                        ('GITHUB_RUN_ID','0'),('GITHUB_RUN_ID','１２３'),('GITHUB_RUN_ATTEMPT','01')]:
            changed=dict(env);changed[key]=bad
            with self.assertRaisesRegex(self.m.ReplayError,'host_identity'):
                self.m.host_identity(head,changed)
        self.m.host_identity(head,{})

    def test_execution_sources_are_committed_and_clean(self):
        for name in self.m.EXECUTION_FILES:
            p=self.root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('test fixture\n')
        subprocess.run(['git','init','-q'],cwd=self.root,check=True)
        subprocess.run(['git','add','.'],cwd=self.root,check=True)
        subprocess.run(['git','-c','user.name=Fixture','-c','user.email=fixture@example.invalid',
                        '-c','commit.gpgsign=false','-c','maintenance.auto=false','commit','-qm','fixture'],cwd=self.root,check=True)
        head=self.m.git_head(self.root)
        self.m.execution_sources(self.root,head)
        target=self.root/self.m.EXECUTION_FILES[0];target.write_text('changed')
        with self.assertRaisesRegex(self.m.ReplayError,'execution_source_drift'):
            self.m.execution_sources(self.root,head)

    def test_preflight_failure_writes_failed_receipt(self):
        output=Path(self.tmp.name)/'preflight'
        with self.assertRaises(self.m.ReplayError):
            self.m.execute(self.root,output,'normal')
        receipt=json.loads((output/'receipt.json').read_bytes())
        self.assertEqual(receipt['status'],'FAIL');self.assertFalse(receipt['scientific_acceptance'])
        self.assertEqual(receipt['steps'],{})
        self.assertIn('failure',receipt)

    def test_rejects_existing_or_internal_evidence_directory(self):
        out=Path(self.tmp.name)/'existing';out.mkdir();sentinel=out/'keep';sentinel.write_text('keep')
        with self.assertRaisesRegex(self.m.ReplayError,'evidence_exists'):
            self.m.execute(self.root,out,'normal')
        self.assertEqual(sentinel.read_text(),'keep')
        with self.assertRaisesRegex(self.m.ReplayError,'evidence_inside_source'):
            self.m.execute(self.root,self.root/'logs','normal')
        with self.assertRaisesRegex(self.m.ReplayError,'invalid_mode'):
            self.m.execute(self.root,Path(self.tmp.name)/'other','wrong')

    def test_cli_rejects_invalid_arguments(self):
        for args in ([],['--mode','wrong','--output','x'],['--mode','normal','--output','x','--grid','8']):
            p=subprocess.run([sys.executable,'-B','-S',str(DRIVER),*args],capture_output=True)
            self.assertEqual(p.returncode,2)

    def synthetic_project(self, coefficient_suffix='', coefficient_output='synthetic', bad_test=False):
        """Real committed temporary source; alternate in-memory pins are TEST ONLY."""
        import shutil
        # This disposable Git repository is not the Actions checkout. Keep the
        # production host check intact; only this synthetic test's environment
        # is isolated, then restored even when the test fails.
        previous = os.environ.get('GITHUB_ACTIONS')
        def restore():
            if previous is None:
                os.environ.pop('GITHUB_ACTIONS', None)
            else:
                os.environ['GITHUB_ACTIONS'] = previous
        self.addCleanup(restore)
        os.environ['GITHUB_ACTIONS'] = 'false'
        pins = self.fixture()
        packet = self.root / self.m.PACKET
        (packet / 'RESULTS.json').write_text('synthetic\n')
        methods = '\n'.join('    def '+name+'(self): self.assertTrue('+('False' if bad_test and i==0 else 'True')+')'
                            for i,name in enumerate(self.m.TEST_NAMES))
        (packet / 'test_enclosure.py').write_text('import unittest\nclass EnclosureTests(unittest.TestCase):\n'+methods+'\n')
        (packet / 'enclose.py').write_text("import sys\nassert sys.argv[1:]==['--grid','2048']\nprint("+repr(coefficient_output)+")\n"+coefficient_suffix+'\n')
        for name in self.m.EXECUTION_FILES:
            dest=self.root/name;dest.parent.mkdir(parents=True,exist_ok=True)
            source=DRIVER.parents[1]/name
            shutil.copyfile(source,dest)
        (self.root/'other.txt').write_text('unchanged')
        subprocess.run(['git','init','-q'],cwd=self.root,check=True)
        subprocess.run(['git','add','.'],cwd=self.root,check=True)
        subprocess.run(['git','-c','user.name=Fixture','-c','user.email=fixture@example.invalid',
                        '-c','commit.gpgsign=false','-c','maintenance.auto=false','commit','-qm','synthetic inputs'],cwd=self.root,check=True)
        spec=importlib.util.spec_from_file_location('fixture_replay',self.root/self.m.EXECUTION_FILES[0])
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        module.PINS={name:module.git_blob((self.root/name).read_bytes()) for name in pins}
        return module

    def test_complete_orchestration_with_real_fixture(self):
        module=self.synthetic_project()
        out=Path(self.tmp.name)/'success'
        receipt=module.execute(self.root,out,'optimized')
        self.assertEqual(receipt['status'],'PASS')
        self.assertEqual(set(receipt['steps']),{'tests','coefficient'})
        self.assertEqual(receipt['tested_commit'],module.git_head(self.root))
        self.assertEqual((out/'coefficient.stdout').read_bytes(),b'synthetic\n')
        self.assertIn('-O',receipt['steps']['coefficient']['record']['command'])

    def test_failed_test_stops_before_coefficient(self):
        module=self.synthetic_project(bad_test=True)
        out=Path(self.tmp.name)/'failed-tests'
        with self.assertRaisesRegex(module.ReplayError,'unexpected_exit'):
            module.execute(self.root,out,'normal')
        rec=json.loads((out/'receipt.json').read_bytes())
        self.assertEqual(rec['status'],'FAIL')
        self.assertEqual(set(rec['steps']),{'tests'})
        self.assertFalse((out/'coefficient.stdout').exists())

    def test_wrong_coefficient_cannot_produce_success_receipt(self):
        module=self.synthetic_project(coefficient_output='wrong')
        out=Path(self.tmp.name)/'wrong-coefficient'
        with self.assertRaisesRegex(module.ReplayError,'stdout_mismatch'):
            module.execute(self.root,out,'normal')
        rec=json.loads((out/'receipt.json').read_bytes())
        self.assertEqual(rec['status'],'FAIL')
        self.assertEqual(rec['steps']['tests']['record']['status'],'PASS')
        self.assertEqual(rec['steps']['coefficient']['record']['status'],'FAIL')

    def test_valid_output_followed_by_packet_edit_is_rejected(self):
        module=self.synthetic_project("from pathlib import Path;Path('NOTE.md').write_text('edited')")
        out=Path(self.tmp.name)/'drift'
        with self.assertRaisesRegex(module.ReplayError,'source_identity'):
            module.execute(self.root,out,'normal')
        rec=json.loads((out/'receipt.json').read_bytes())
        self.assertEqual(rec['status'],'FAIL')
        self.assertEqual(rec['steps']['coefficient']['record']['status'],'PASS')
        self.assertIn('source_identity',rec['failure'])

    def test_oversized_stream_is_retained_and_rejected(self):
        with self.assertRaisesRegex(self.m.ReplayError,'output_too_large'):
            self.child("import sys;sys.stdout.write('x'*"+str(self.m.MAX_STREAM_BYTES+1)+")")
        self.assertEqual((self.logs/'child.stdout').stat().st_size,self.m.MAX_STREAM_BYTES+1)
        row=json.loads((self.logs/'child.process.json').read_bytes())
        self.assertEqual(row['status'],'FAIL')
        self.assertEqual(row['failure'],'output_too_large')

    def test_workflow_triggers_and_preserves_failure_artifacts(self):
        workflow=DRIVER.parents[1]/'.github/workflows/lm006-sign-coefficient.yml'
        self.assertTrue(workflow.is_file(),'dedicated workflow missing')
        text=workflow.read_text()
        for path in [self.m.PACKET+'/**',*self.m.EXECUTION_FILES,*self.m.DEPENDENCIES]:
            self.assertEqual(text.count("- '"+path+"'"),2,path)
        for phrase in ('permissions:\n  contents: read','fail-fast: false',
                       'mode: [normal, optimized]','if: always()',
                       'persist-credentials: false',"python-version: '3.13.5'",
                       "-p 'test_lm006_sign_coefficient_replay.py'",'if-no-files-found: error'):
            self.assertIn(phrase,text)
        self.assertNotIn('continue-on-error:',text)
        self.assertNotIn('pull_request_target:',text)
        self.assertEqual(len(re.findall(r'uses: actions/[a-z-]+@[0-9a-f]{40}',text)),3)

if __name__=='__main__':
    unittest.main()
