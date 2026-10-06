"""QS raw-child evidence controls. Synthetic children are not mathematical evidence."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
WRAPPER = ROOT / 'frontiers/qs_d3_soft_layer_chain_20261005/replay.py'


class ChildEvidenceTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location('qs_capture_subject', WRAPPER)
        self.q = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.q)
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def recorder(self, name='evidence'):
        self.assertTrue(hasattr(self.q, 'ChildEvidence'),
                        'QS has no optional raw child-evidence recorder')
        return self.q.ChildEvidence(self.root / name)

    def command(self, text):
        return [sys.executable, *self.q.interpreter_flags(), '-c', text]

    def record(self, sink, index=1):
        return json.loads((sink.directory / ('%04d' % index) / 'process.json').read_text())

    def check_stream(self, sink, record, key, data, index=1):
        row = record['streams'][key]
        self.assertEqual(row['available'], data is not None)
        if data is None:
            self.assertIsNone(row['bytes']); self.assertIsNone(row['sha256'])
            self.assertFalse(row['saved'])
            self.assertFalse((sink.directory / ('%04d' % index) / (key+'.bin')).exists())
        else:
            self.assertEqual(row['bytes'], len(data))
            self.assertEqual(row['sha256'], hashlib.sha256(data).hexdigest())
            self.assertTrue(row['saved'])
            self.assertEqual((sink.directory / ('%04d' % index) / (key+'.bin')).read_bytes(), data)

    def test_exact_completed_binary_and_empty_streams(self):
        sink = self.recorder()
        command = self.command("import os; os.write(1,b'\\x00\\xffQS\\n'); os.write(2,b'')")
        result = sink.run(command, cwd=str(self.root), timeout=5)
        self.assertEqual(result, (0, b'\x00\xffQS\n', b''))
        record = self.record(sink)
        self.assertEqual(record['command'], command)
        self.assertEqual(record['cwd'], str(self.root)); self.assertEqual(record['timeout_seconds'], 5)
        self.assertEqual(record['status'], 'completed'); self.assertEqual(record['returncode'], 0)
        self.assertTrue(record['capture_complete']); self.assertIsNone(record['exception'])
        self.check_stream(sink, record, 'stdout', result[1]); self.check_stream(sink, record, 'stderr', b'')
        self.assertEqual(record['evidence_errors'], [])

    def test_crash_streams_are_preserved_and_not_accepted(self):
        sink = self.recorder()
        result = sink.run(self.command("import os; os.write(1,b'\\x00pre'); raise RuntimeError('synthetic unrelated crash')"),
                          cwd=str(self.root), timeout=5)
        self.assertEqual(result[0], 1); self.assertIn(b'RuntimeError: synthetic unrelated crash', result[2])
        record = self.record(sink)
        self.assertEqual(record['returncode'], 1)
        self.check_stream(sink, record, 'stdout', result[1]); self.check_stream(sink, record, 'stderr', result[2])
        self.assertTrue(self.q.check_rejection(result, self.q.NEGATIVE_HARDGAP))

    def test_wrong_response_is_preserved_without_changing_matcher(self):
        sink = self.recorder()
        result = sink.run(self.command("import sys; print('{bad-json}'); sys.exit(1)"), cwd=str(self.root), timeout=5)
        self.check_stream(sink, self.record(sink), 'stdout', b'{bad-json}\n')
        self.assertTrue(self.q.check_rejection(result, self.q.NEGATIVE_HARDGAP))

    def test_actual_timeout_preserves_binary_prefix_and_exception(self):
        sink = self.recorder()
        command = self.command("import os,time; os.write(1,b'\\x00\\xffpartial'); os.write(2,b'\\xfeerr'); time.sleep(5)")
        with self.assertRaises(subprocess.TimeoutExpired) as caught:
            sink.run(command, cwd=str(self.root), timeout=0.6)
        exc = caught.exception; record = self.record(sink)
        self.assertIsNone(record['returncode']); self.assertEqual(record['status'], 'timeout')
        self.assertFalse(record['capture_complete']); self.assertEqual(record['timeout_seconds'], 0.6)
        self.assertEqual(exc.stdout, b'\x00\xffpartial'); self.assertEqual(exc.stderr, b'\xfeerr')
        self.check_stream(sink, record, 'stdout', exc.stdout); self.check_stream(sink, record, 'stderr', exc.stderr)
        self.assertEqual(exc.qs_evidence, record)

    def test_unavailable_is_not_captured_empty(self):
        for index, (out, err) in enumerate(((None,None),(b'',None),(None,b''),(b'',b''))):
            sink = self.recorder('case%d'%index)
            original = subprocess.TimeoutExpired(['fake'], 7, output=out, stderr=err)
            with mock.patch.object(self.q.subprocess, 'run', side_effect=original):
                with self.assertRaises(subprocess.TimeoutExpired) as caught:
                    sink.run(['fake'], cwd=str(self.root), timeout=7)
            self.assertIs(caught.exception, original)
            record = self.record(sink)
            self.check_stream(sink, record, 'stdout', out); self.check_stream(sink, record, 'stderr', err)

    def test_real_spawn_error_has_no_invented_capture(self):
        sink = self.recorder()
        with self.assertRaises(FileNotFoundError) as caught:
            sink.run([str(self.root/'not-an-executable')], cwd=str(self.root), timeout=5)
        record = self.record(sink)
        self.assertEqual(record['status'], 'execution_error'); self.assertIsNone(record['returncode'])
        self.assertEqual(record['exception']['type'], 'FileNotFoundError')
        self.check_stream(sink, record, 'stdout', None); self.check_stream(sink, record, 'stderr', None)
        self.assertEqual(caught.exception.qs_evidence, record)

    def test_independent_writes_preserve_primary_timeout(self):
        for mask in range(8):
            with self.subTest(mask=mask):
                sink = self.recorder('mask%d'%mask); real = sink._write
                names = ['stdout.bin','stderr.bin','process.json']; attempted = []
                def write(path, data):
                    attempted.append(path.name)
                    if mask & (1 << names.index(path.name)):
                        raise OSError('synthetic write failure '+path.name)
                    return real(path, data)
                original = subprocess.TimeoutExpired(['fake'], 5, output=b'out\x00', stderr=b'err\xff')
                with mock.patch.object(sink, '_write', side_effect=write), \
                     mock.patch.object(self.q.subprocess, 'run', side_effect=original):
                    with self.assertRaises(subprocess.TimeoutExpired) as caught:
                        sink.run(['fake'], cwd=str(self.root), timeout=5)
                self.assertIs(caught.exception, original); self.assertEqual(attempted, names)
                record = original.qs_evidence
                self.assertIsNone(record['returncode'])
                self.assertEqual(len(record['evidence_errors']), mask.bit_count())
                for bit, name in enumerate(names):
                    self.assertEqual((sink.directory/'0001'/name).exists(), not bool(mask & (1 << bit)))

    def test_evidence_write_failure_never_promotes_completed_child(self):
        for code in (0,1,2):
            sink = self.recorder('exit%d'%code)
            with mock.patch.object(sink, '_write', side_effect=OSError('synthetic disk failure')):
                with self.assertRaises(self.q.ChildEvidenceError) as caught:
                    sink.run(self.command('import sys; print("data"); sys.exit(%d)'%code), cwd=str(self.root), timeout=5)
            self.assertEqual(caught.exception.child_result, (code,b'data\n',b''))
            self.assertEqual(caught.exception.qs_evidence['returncode'], code)
            self.assertEqual(len(caught.exception.qs_evidence['evidence_errors']), 3)

    def test_invalid_clock_is_qualified_without_masking_timeout(self):
        cases = [(10.,9.9999999),(10.,float('nan')),(10.,float('inf')),
                 (True,11.),(OSError('clock-start'),11.),(10.,OSError('clock-end'))]
        for i, clocks in enumerate(cases):
            sink = self.recorder('clock%d'%i)
            original = subprocess.TimeoutExpired(['fake'],5)
            with mock.patch.object(self.q.time, 'monotonic', side_effect=clocks), \
                 mock.patch.object(self.q.subprocess, 'run', side_effect=original):
                with self.assertRaises(subprocess.TimeoutExpired) as caught:
                    sink.run(['fake'],cwd=str(self.root),timeout=5)
            self.assertIs(caught.exception,original);record=self.record(sink)
            self.assertIsNone(record['elapsed_seconds']);self.assertTrue(record['clock_error'])

    def test_fresh_directory_and_no_overwrite(self):
        sink = self.recorder()
        with self.assertRaises((FileExistsError,ValueError)):
            self.q.ChildEvidence(sink.directory)
        (sink.directory/'0001').mkdir()
        (sink.directory/'0001'/'sentinel').write_bytes(b'keep')
        with mock.patch.object(self.q.subprocess,'run',side_effect=AssertionError('must not run')):
            with self.assertRaises(FileExistsError):
                sink.run(['fake'],cwd=str(self.root),timeout=5)
        self.assertEqual((sink.directory/'0001'/'sentinel').read_bytes(),b'keep')

    def test_evidence_inside_checkout_or_symlink_alias_is_refused(self):
        self.assertTrue(hasattr(self.q,'ChildEvidence'),'missing external evidence directory guard')
        checkout=self.root/'checkout';(checkout/'frontiers'/'packet').mkdir(parents=True)
        with mock.patch.object(self.q,'HERE',checkout/'frontiers'/'packet'):
            for directory in (checkout/'evidence',checkout/'frontiers'/'packet'/'evidence'):
                with self.assertRaises(ValueError): self.q.ChildEvidence(directory)
            (self.root/'alias').symlink_to(checkout,target_is_directory=True)
            with self.assertRaises(ValueError): self.q.ChildEvidence(self.root/'alias'/'evidence')
        self.assertFalse((checkout/'evidence').exists())

    def test_separate_records_for_identical_invocations(self):
        sink=self.recorder(); command=self.command('print("same")')
        for _ in range(2): sink.run(command,cwd=str(self.root),timeout=5)
        self.assertEqual(sorted(p.name for p in sink.directory.iterdir()),['0001','0002'])
        self.assertEqual(self.record(sink,1)['sequence'],1);self.assertEqual(self.record(sink,2)['sequence'],2)

    def test_run_without_capture_retains_original_contract(self):
        script=self.root/'checker.py';script.write_text('print("unchanged")\n')
        result=self.q.run(script)
        self.assertEqual(result,(0,b'unchanged\n',b''))
        self.assertEqual(sorted(p.name for p in self.root.iterdir()),['checker.py'])

    def test_run_with_capture_keeps_original_flags_cwd_timeout(self):
        sink=self.recorder();script=self.root/'checker.py';script.write_text('print("same")\n')
        with mock.patch.object(self.q,'ACTIVE_EVIDENCE',sink): result=self.q.run(script)
        record=self.record(sink)
        self.assertEqual(result,(0,b'same\n',b''));self.assertEqual(record['timeout_seconds'],1800)
        self.assertEqual(record['command'],[sys.executable,*self.q.interpreter_flags(),str(script)])
        self.assertEqual(record['cwd'],str(script.parent))

    def test_main_restores_recorder_and_does_not_continue_after_exception(self):
        self.assertTrue(hasattr(self.q,'_replay_main'),'missing scoped evidence opt-in')
        destination=self.root/'main-capture'; original=RuntimeError('primary synthetic failure')
        def failing():
            self.assertIsNotNone(self.q.ACTIVE_EVIDENCE)
            raise original
        with mock.patch.dict(os.environ,{'QS_REPLAY_EVIDENCE_DIR':str(destination)}), \
             mock.patch.object(self.q,'_replay_main',side_effect=failing):
            with self.assertRaises(RuntimeError) as caught: self.q.main()
        self.assertIs(caught.exception,original);self.assertIsNone(self.q.ACTIVE_EVIDENCE)
        self.assertTrue(destination.is_dir())

    def test_intended_rejection_keeps_exact_diagnostic(self):
        sink=self.recorder()
        command=self.command("import sys; sys.stderr.write('FAILED: X9_hardgap\\n'); sys.exit(1)")
        result=sink.run(command,cwd=str(self.root),timeout=5)
        self.assertEqual(self.q.check_rejection(result,self.q.NEGATIVE_HARDGAP),[])
        self.check_stream(sink,self.record(sink),'stderr',b'FAILED: X9_hardgap\n')

    def test_real_orchestration_stops_after_first_timeout(self):
        self.recorder('capability-probe')
        original=subprocess.TimeoutExpired(['synthetic timeout'],1800,output=b'partial')
        with mock.patch.dict(os.environ,{'QS_REPLAY_EVIDENCE_DIR':str(self.root/'orchestration')}), \
             mock.patch.object(self.q.subprocess,'run',side_effect=original) as child, \
             mock.patch.object(self.q,'negative_control_failures',side_effect=AssertionError('must not continue')):
            with self.assertRaises(subprocess.TimeoutExpired) as caught: self.q.main()
        self.assertIs(caught.exception,original);self.assertEqual(child.call_count,1)
        self.assertIsNone(self.q.ACTIVE_EVIDENCE)
        record=json.loads((self.root/'orchestration'/'0001'/'process.json').read_text())
        self.assertEqual(record['status'],'timeout');self.assertEqual(record['timeout_seconds'],1800)

    def test_workflow_enables_capture_only_for_real_replay_and_preserves_it(self):
        text=(ROOT/'.github/workflows/qs-d3-soft-layer-chain.yml').read_text()
        self.assertIn("'tests/test_qs_failure_evidence.py'",text)
        self.assertIn('-p test_qs_failure_evidence.py -v',text)
        self.assertIn('QS_REPLAY_EVIDENCE_DIR="$out/children" python ${{ matrix.mode }}',text)
        self.assertIn('path: ${{ runner.temp }}/qs-replay-evidence/',text)
        self.assertIn('if-no-files-found: error',text)
        self.assertEqual(text.count('if: always()'),2)
        self.assertIn('set -euo pipefail',text)


if __name__ == '__main__':
    unittest.main()
