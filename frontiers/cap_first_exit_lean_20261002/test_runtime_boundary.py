"""Actual process and evidence-boundary controls; no Lean package build."""
import pathlib
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import gate
from test_gate import packet_copy


class RuntimeBoundary(unittest.TestCase):
    def test_lake_symlink_cannot_move_or_remove_external_evidence(self):
        repo,packet=packet_copy(self)
        with tempfile.TemporaryDirectory() as temporary:
            external=pathlib.Path(temporary)
            (external/'evidence').mkdir();(external/'evidence/sentinel').write_bytes(b'preserve')
            (packet/'.lake').symlink_to(external,target_is_directory=True)
            with mock.patch.object(gate,'ROOT',packet),mock.patch.object(gate,'REPO',repo), \
                    mock.patch.object(gate,'observe',side_effect=ValueError('probe boundary')):
                with self.assertRaises(ValueError):gate.execute({})
            self.assertTrue((external/'evidence/sentinel').is_file(),'symlink target evidence was moved before refusal')
            self.assertEqual((external/'evidence/sentinel').read_bytes(),b'preserve')

    def test_timeout_retains_streams_and_cleans_owned_descendants(self):
        self.assertTrue(hasattr(gate,'run_process'),'owned process cleanup implementation missing')
        script=('import subprocess,sys,time\n'
                'p=subprocess.Popen([sys.executable,"-c","import time;time.sleep(60)"])\n'
                'print("CHILD="+str(p.pid),flush=True)\n'
                'print("partial-error",file=sys.stderr,flush=True)\n'
                'time.sleep(60)\n')
        process=gate.run_process([sys.executable,'-B','-S','-c',script],cwd=pathlib.Path.cwd(),timeout=0.3)
        self.assertTrue(process.timed_out)
        self.assertIn('CHILD=',process.stdout)
        self.assertIn('partial-error',process.stderr)
        self.assertNotEqual(process.returncode,0)
        pid=process.stdout.split('CHILD=',1)[1].splitlines()[0]
        observed=subprocess.run(['ps','-p',pid,'-o','stat='],stdout=subprocess.PIPE,text=True)
        self.assertTrue(observed.returncode!=0 or observed.stdout.strip().startswith('Z'),
                        'owned descendant still running after timeout cleanup')


if __name__=='__main__':unittest.main()
