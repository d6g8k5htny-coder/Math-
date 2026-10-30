"""Actual producer timing out and handling SIGTERM with exit0 must still refuse."""
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

HERE=Path(__file__).resolve().parent
PACKET=HERE if (HERE/'gate.py').is_file() else HERE.parent/'Math-/frontiers/cap_first_exit_lean_20261002'
spec=importlib.util.spec_from_file_location('cap_gate_timeout_review',PACKET/'gate.py')
gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)


class TimeoutExitZero(unittest.TestCase):
    def test_timed_out_zero_exit_is_refused_after_recording_streams(self):
        configured=os.environ.get('CBZ_CONTROL_OUTPUT')
        if configured:
            out=Path(configured);out.mkdir(parents=True,exist_ok=False)
        else:
            temporary=tempfile.TemporaryDirectory(prefix='cap-timeout-zero-')
            self.addCleanup(temporary.cleanup);out=Path(temporary.name)
        producer=('import signal,sys,time\n'
                  'signal.signal(signal.SIGTERM,lambda *_:sys.exit(0))\n'
                  'print("partial-before-timeout",flush=True)\n'
                  'time.sleep(60)\n')
        real=gate.run_process
        def bounded(command,cwd,timeout):return real(command,cwd,timeout=0.3)
        rejected=False
        with mock.patch.object(gate,'run_process',side_effect=bounded):
            try:
                gate.run([sys.executable,'-B','-S','-c',producer],'term_zero',out,cwd=out,pure_stream=True)
            except ValueError:
                rejected=True
        record=json.loads((out/'term_zero.process.json').read_text())
        self.assertTrue(record['timed_out'])
        self.assertEqual(record['exit'],0)
        self.assertIn('partial-before-timeout',(out/'term_zero.stdout').read_text())
        self.assertEqual((out/'term_zero.stderr').read_bytes(),b'')
        self.assertTrue(rejected,'gate accepted a timed-out producer merely because SIGTERM handler exited0')


if __name__=='__main__':unittest.main()
