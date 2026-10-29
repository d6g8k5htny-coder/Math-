"""Execute the literal LM006 workflow shell against an actual poisoned test cache."""
import importlib.util
import os
from pathlib import Path
import py_compile
import struct
import subprocess
import sys
import tempfile
import unittest

REPO=Path(__file__).resolve().parents[3]
WORKFLOW=REPO/'.github/workflows/lm006-oned-coefficient.yml'

def workflow_script(text,mode):
    start='      - name: Replay controls and frozen 1024-panel certificate\n        shell: bash\n        run: |\n'
    end='      - name: Preserve success or failure evidence\n'
    if text.count(start)!=1 or text.count(end)!=1:
        raise ValueError('workflow step boundary changed')
    block=text.split(start,1)[1].split(end,1)[0]
    lines=block.splitlines()
    if not lines or any(not line.startswith('          ') for line in lines):
        raise ValueError('workflow indentation changed')
    script='\n'.join(line[10:] for line in lines)+'\n'
    return script.replace('$'+'{{ matrix.mode }}',mode).replace('$'+'{{ github.run_attempt }}','1')

def exercise(test,workflow,mode):
    with tempfile.TemporaryDirectory(prefix='lm006-outer-cache-') as temporary:
        root=Path(temporary)/'repo'
        tests=root/'tests'
        tools=root/'tools'
        runner=Path(temporary)/'runner'
        cache=Path(temporary)/'external-pyc'
        for p in (tests,tools,runner,cache): p.mkdir(parents=True)
        source=b"import unittest\nclass Fixture(unittest.TestCase):\n def test_exact(self):\n  print('ACTUAL_OUTER_SOURCE')\n  self.assertEqual(1,1)\n"
        original=b'self.assertEqual(1,1)'
        poison=b'self.assertEqual(1,0)'
        test.assertEqual(len(original),len(poison))
        test.assertEqual(source.count(original),1)
        path=tests/'test_lm006_oned_coefficient_replay.py'
        path.write_bytes(source.replace(original,poison,1))
        os.utime(path,(1700000000,1700000000))
        previous=sys.pycache_prefix
        try:
            sys.pycache_prefix=str(cache)
            pyc=py_compile.compile(str(path),doraise=True,optimize=1 if mode=='optimized' else 0,
                                   invalidation_mode=py_compile.PycInvalidationMode.TIMESTAMP)
        finally:
            sys.pycache_prefix=previous
        magic,flags,mtime,size=struct.unpack('<4sIII',Path(pyc).read_bytes()[:16])
        test.assertEqual(magic,importlib.util.MAGIC_NUMBER)
        test.assertEqual((flags,mtime,size),(0,1700000000,len(source)))
        path.write_bytes(source)
        os.utime(path,(1700000000,1700000000))
        (tools/'lm006_oned_coefficient_replay.py').write_text("print('DRIVER_REACHED')\n")
        env=dict(os.environ,RUNNER_TEMP=str(runner),PYTHONPYCACHEPREFIX=str(cache),
                 CBZ_TEST_POISON_CACHE=str(cache))
        result=subprocess.run(['bash','-c',workflow_script(workflow,mode)],cwd=root,env=env,
                              stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=60)
        return result.returncode,result.stdout

class OuterEntryTests(unittest.TestCase):
    def test_outer_discovery_ignores_a_valid_poisoned_cache(self):
        mode=os.environ.get('CBZ_MODE','normal')
        self.assertIn(mode,('normal','optimized'))
        exit_code,output=exercise(self,WORKFLOW.read_text(),mode)
        self.assertEqual(exit_code,0,output)
        self.assertIn('ACTUAL_OUTER_SOURCE',output)
        self.assertIn('DRIVER_REACHED',output)
        self.assertIn('Ran 1 test',output)
        self.assertIn('\nOK\n',output)

if __name__=='__main__':
    unittest.main(verbosity=2)
