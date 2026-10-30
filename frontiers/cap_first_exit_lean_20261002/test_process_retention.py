"""Actual bounded Python processes exercise retention; no Lean build is run."""
import contextlib
import inspect
import io
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import gate
import lean_opaque_control as opaque
import run_cbz_mutations as runner


class ProcessRetention(unittest.TestCase):
    def output(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        return pathlib.Path(temporary.name)

    def require_bounded_api(self):
        self.assertIn('timeout', inspect.signature(runner.execute).parameters,
                      'runner has no bounded-retention timeout argument')

    def test_relative_opaque_cli_paths_are_resolved_before_child_cwd(self):
        root=self.output();fake=root/'fake-lean'
        module='s436170466972737445786974'
        hazard=module+'/s6f706171756548617a617264'
        protocol='MODULE|'+module+'|false|1|0\nINV|opaque|user|'+module+'|'+hazard+'|unsafe\nAXIOMS|\nCLOSURE|1\n'
        fake.write_text('#!'+sys.executable+'\nimport sys\n'
            'if "--version" in sys.argv:\n print("Lean (version 4.34.1, unit-fixture, commit 5045d0056413266e57c625dcd7c365b10e377c52, Release)")\n'
            'elif "Inventory.lean" in sys.argv:\n print('+repr(protocol)+',end="")\n')
        fake.chmod(0o755)
        result=subprocess.run([sys.executable,'-B','-S',str(pathlib.Path(opaque.__file__).resolve()),
            '--lean','./fake-lean','--output','relative-output'],cwd=root,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=10)
        self.assertEqual(result.returncode,0,result.stderr.decode())
        metadata=json.loads((root/'relative-output/compile.process.json').read_text())
        self.assertTrue(pathlib.Path(metadata['cwd']).is_absolute())
        self.assertIn('LEAN_PATH='+str((root/'relative-output').resolve()),metadata['command'])
        self.assertEqual(json.loads((root/'relative-output/RESULT.json').read_text())['tests'],1)

    def test_success_and_nonzero_exit_retain_separate_streams_and_metadata(self):
        for status in (0, 7):
            with self.subTest(status=status):
                out = self.output()
                command = [sys.executable, '-B', '-S', '-c',
                    'import sys;print("out");print("err",file=sys.stderr);sys.exit(' + str(status) + ')']
                process = runner.execute(command, out, out, 'observed')
                self.assertEqual(process.returncode, status)
                self.assertEqual((out/'observed.stdout').read_bytes(), b'out\n')
                self.assertEqual((out/'observed.stderr').read_bytes(), b'err\n')
                self.assertTrue((out/'observed.process.json').is_file(), 'process metadata was not retained')
                metadata = json.loads((out/'observed.process.json').read_text())
                self.assertEqual(metadata['exit'], status)
                self.assertFalse(metadata['timed_out'])

    def test_timeout_retains_partial_streams_and_cleans_owned_child(self):
        self.require_bounded_api()
        out = self.output()
        script = ('import subprocess,sys,time\n'
                  'child=subprocess.Popen([sys.executable,"-B","-S","-c","import time;time.sleep(60)"])\n'
                  'print("CHILD="+str(child.pid),flush=True)\n'
                  'print("partial-stderr",file=sys.stderr,flush=True)\n'
                  'time.sleep(60)\n')
        with self.assertRaisesRegex(RuntimeError, 'timed out'):
            runner.execute([sys.executable,'-B','-S','-c',script], out, out, 'timeout', timeout=0.3)
        stdout = (out/'timeout.stdout').read_text()
        self.assertIn('CHILD=', stdout)
        self.assertIn('partial-stderr', (out/'timeout.stderr').read_text())
        metadata = json.loads((out/'timeout.process.json').read_text())
        self.assertTrue(metadata['timed_out'])
        self.assertIn('SIGTERM', metadata['cleanup_signals'])
        child = stdout.split('CHILD=',1)[1].splitlines()[0]
        observed = subprocess.run(['ps','-p',child,'-o','stat='], stdout=subprocess.PIPE, text=True)
        self.assertTrue(observed.returncode != 0 or observed.stdout.strip().startswith('Z'))

    def test_timeout_that_exits_zero_is_still_refused_after_retention(self):
        self.require_bounded_api()
        out = self.output()
        script = ('import signal,sys,time\n'
                  'signal.signal(signal.SIGTERM,lambda *_:sys.exit(0))\n'
                  'print("before-timeout",flush=True)\ntime.sleep(60)\n')
        with self.assertRaisesRegex(RuntimeError, 'timed out'):
            runner.execute([sys.executable,'-B','-S','-c',script], out, out, 'zero', timeout=0.3)
        metadata = json.loads((out/'zero.process.json').read_text())
        self.assertTrue(metadata['timed_out'])
        self.assertEqual(metadata['exit'], 0)
        self.assertEqual((out/'zero.stdout').read_bytes(), b'before-timeout\n')
        self.assertEqual((out/'zero.stderr').read_bytes(), b'')

    def opaque_timeout_attempt(self, version_delay):
        self.assertTrue(hasattr(opaque, 'execute'), 'opaque control bypasses the retained process helper')
        out = self.output()/'attempt'
        fake = out.parent/'fake-lean'
        fake.write_text('#!' + sys.executable + '\nimport sys,time\n'
            'if "--version" in sys.argv:\n'
            ' time.sleep(' + repr(version_delay) + ')\n'
            ' print("Lean (version 4.34.1, control-only, commit 5045d0056413266e57c625dcd7c365b10e377c52, Release)")\n'
            'else:\n print("fixture-partial",flush=True);time.sleep(60)\n')
        fake.chmod(0o755)
        real_execute = runner.execute
        def bounded(command, cwd, output, label, **kwargs):
            # Expire the deliberately sleeping compile, after a successful probe.
            # Version startup latency must not be counted as a compile timeout.
            return real_execute(command, cwd, output, label,
                                timeout=2 if label == 'compile' else 10)
        expected_failure = io.StringIO()
        with mock.patch.object(sys,'argv',['lean_opaque_control.py','--lean',str(fake),'--output',str(out)]), \
                mock.patch.object(opaque,'execute',side_effect=bounded), \
                contextlib.redirect_stderr(expected_failure):
            self.assertEqual(opaque.main(), 1)
        self.assertIn('process timed out', expected_failure.getvalue())
        version = json.loads((out/'version.process.json').read_text())
        self.assertEqual(version['exit'], 0, 'fixture did not complete its version phase')
        self.assertFalse(version['timed_out'], 'fixture expired before compilation')
        self.assertIn('fixture-partial', (out/'compile.stdout').read_text())
        self.assertTrue(json.loads((out/'compile.process.json').read_text())['timed_out'])
        receipt = json.loads((out/'RESULT.json').read_text())
        self.assertFalse(receipt['success'])
        self.assertEqual(receipt['errors'], 1)


    def test_opaque_control_timeout_uses_retention_and_writes_failure_receipt(self):
        self.opaque_timeout_attempt(version_delay=0)

    def test_delayed_version_is_not_mistaken_for_compile_timeout(self):
        # Greater than the old all-phases 0.3s deadline, with no Lean dependency.
        self.opaque_timeout_attempt(version_delay=0.6)


if __name__ == '__main__':
    unittest.main()
