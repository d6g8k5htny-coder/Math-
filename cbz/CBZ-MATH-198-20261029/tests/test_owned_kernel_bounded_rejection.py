"""A failing leader with unfinished descendants is not an ordinary native rejection."""
from pathlib import Path
import json
import os
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'tools'))
import owned_kernel_audit as audit


class NativeRejectionLifecycleTests(unittest.TestCase):
    def test_expected_failure_refuses_real_exit_one_with_unfinished_descendant(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); pidfile=root/'child.pid'
            child='import os,sys,time; from pathlib import Path; Path(sys.argv[1]).write_text(str(os.getpid())); time.sleep(15)'
            leader='import subprocess,sys,time; from pathlib import Path; subprocess.Popen([sys.executable,"-c",sys.argv[1],sys.argv[2]],start_new_session=True); p=Path(sys.argv[2]); exec("for _ in range(200):\\n if p.exists(): break\\n time.sleep(.005)"); raise SystemExit(1)'
            with self.assertRaisesRegex(ValueError, 'cleanup|descendant|lifecycle|ordinary'):
                audit.bounded_native([sys.executable,'-B','-c',leader,child,str(pidfile)],root/'attempt',root,dict(os.environ),expected=False)
            receipt=json.loads((root/'attempt/receipt.json').read_text())
            self.assertEqual(receipt['returncode'],1)
            self.assertTrue(receipt['process_tree']['unexpected_descendants'])
            self.assertTrue(receipt['process_tree']['cleanup_complete'])
            self.assertEqual(receipt['process_tree']['survivors'],[])
            pid=int(pidfile.read_text())
            if Path('/proc',str(pid),'stat').exists():
                state=Path('/proc',str(pid),'stat').read_text().rsplit(')',1)[1].split()[0]
                self.assertIn(state,('Z','X'))

    def test_expected_failure_requires_complete_typed_supervision_evidence(self):
        base={'succeeded':False,'returncode':1,'failure':None,'timed_out':False,'output_limit_exceeded':False,
              'process_tree':{'cleanup_complete':True,'unexpected_descendants':False,'survivors':[], 'supervisor_forced_exit':False}}
        variants=[dict(base,process_tree={}),
                  dict(base,process_tree={**base['process_tree'],'cleanup_complete':False}),
                  dict(base,process_tree={**base['process_tree'],'cleanup_complete':1}),
                  dict(base,process_tree={**base['process_tree'],'unexpected_descendants':True}),
                  dict(base,process_tree={**base['process_tree'],'supervisor_forced_exit':True}),
                  dict(base,process_tree={**base['process_tree'],'survivors':[123]})]
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for number,receipt in enumerate(variants):
                with self.subTest(receipt=receipt), patch.object(audit,'run_recorded',return_value=receipt):
                    with self.assertRaisesRegex(ValueError,'cleanup|descendant|lifecycle|ordinary'):
                        audit.bounded_native([sys.executable,'-c','pass'],root/str(number),root,dict(os.environ),expected=False)

if __name__=='__main__': unittest.main()
