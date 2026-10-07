"""Bounded driver tests and exact rational supplements; not kernel evidence."""
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

SIDE = Path(__file__).resolve().parent
if (SIDE/'replay.py').exists():
    spec=importlib.util.spec_from_file_location('fold_replay', SIDE/'replay.py')
    replay=importlib.util.module_from_spec(spec);spec.loader.exec_module(replay)
else:
    replay=None

class DriverTest(unittest.TestCase):
    def api(self,name):
        self.assertIsNotNone(replay,'bounded replay driver is missing')
        self.assertTrue(callable(getattr(replay,name,None)), 'missing driver behavior '+name)
        return getattr(replay,name)

    def test_absolute_value_token_spacing(self):
        for name in ('FoldAffineBridge.lean','Contract.lean'):
            with self.subTest(name=name):
                self.assertNotIn('|*',(SIDE/name).read_text(), 'absolute-value close must not form the Lean |* token')

    def test_strict_json_accepts_object(self):
        self.assertEqual(self.api('strict_json')('{"x":1}'), {'x':1})

    def test_strict_json_rejects_duplicates(self):
        fn=self.api('strict_json')
        for raw in ['{"x":1,"x":2}', '{"a":{"x":1,"x":1}}']:
            with self.subTest(raw=raw),self.assertRaisesRegex(ValueError,'duplicate'):
                fn(raw)

    def test_strict_json_rejects_nonfinite(self):
        fn=self.api('strict_json')
        for value in ['NaN','Infinity','-Infinity']:
            with self.subTest(value=value),self.assertRaises(ValueError):fn(value)

    def test_identity(self):
        self.assertEqual(self.api('identity')(b'hello\n'),
            {'bytes':6,'sha256':'5891b5b522d5df086d0ff0b110fbd9d21bb4fc7163af34d08286a2e846f6be03',
             'git_blob':'ce013625030ba8dba906f756967f9e9ca394464a'})

    def test_negative_exact_reason(self):
        fn=self.api('validate_negative')
        for label in ('RejectMissingScale','RejectZeroNondegenerate','RejectSignedCurvature'):
            raw=f'/tmp/build/{label}.lean:3:2: error: unsolved goals\n⊢ False\n'.encode()
            self.assertEqual(fn(label,1,raw,b''),label)

    def test_negative_refuses_other_failures(self):
        fn=self.api('validate_negative');label='RejectMissingScale'
        good=f'{label}.lean:3:2: error: unsolved goals\n⊢ False\n'.encode()
        for code,out,err in [(0,good,b''),(2,good,b''),(True,good,b''),
                (1,b'unknown module prefix FoldAffineBridge\n',b''),
                (1,good,b'unrelated error'),(1,b'crash\n'+good,b''),
                (1,good.replace(b'RejectMissingScale',b'Other'),b''),
                (1,good.replace(b'False',b'True'),b''),(1,b'',b''),
                (1,good+good,b'')]:
            with self.subTest(code=code,out=out,err=err),self.assertRaises(ValueError):
                fn(label,code,out,err)

    def test_negative_refuses_unknown_label(self):
        fn=self.api('validate_negative')
        with self.assertRaises(ValueError):fn('Other',1,b'',b'')

    def test_metadata_strict_scope(self):
        fn=self.api('validate_metadata')
        meta={'version':1,'scientific_effect':'NONE','core_tree':replay.CORE_TREE,
              'targets':list(replay.TARGETS),'definitions':list(replay.DEFINITIONS),
              'files':{p:{'bytes':0,'sha256':'0'*64,'git_blob':'0'*40} for p in replay.PAYLOADS}}
        fn(meta)
        for key,value in [('version',True),('scientific_effect','ACCEPTED'),('core_tree','0'*40),
                          ('targets',[]),('definitions',[]),('files',{})]:
            bad={**meta,key:value}
            with self.subTest(key=key),self.assertRaises(ValueError):fn(bad)
        with self.assertRaises(ValueError):fn({**meta,'extra':1})

    def test_process_preserves_both_streams_and_status(self):
        fn=self.api('run_process')
        with tempfile.TemporaryDirectory() as d:
            out=Path(d)
            code=fn(out,'child',[sys.executable,'-c','import sys; print("one"); print("two",file=sys.stderr); sys.exit(7)'],timeout=3,require_success=False)
            self.assertEqual(code,7)
            self.assertEqual((out/'child.stdout').read_bytes(),b'one\n')
            self.assertEqual((out/'child.stderr').read_bytes(),b'two\n')
            record=json.loads((out/'child.status.json').read_text())
            self.assertEqual(record['exit_code'],7);self.assertFalse(record['timed_out'])

    def test_process_failure_does_not_pass(self):
        fn=self.api('run_process')
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaisesRegex(RuntimeError,'exit 7'):
                fn(Path(d),'fail',[sys.executable,'-c','raise SystemExit(7)'],timeout=3)
            self.assertEqual(json.loads((Path(d)/'fail.status.json').read_text())['exit_code'],7)

    def test_timeout_is_preserved_and_not_negative_success(self):
        fn=self.api('run_process')
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaisesRegex(RuntimeError,'timed out'):
                fn(Path(d),'slow',[sys.executable,'-u','-c','import time; print("started"); time.sleep(10)'],timeout=.1,require_success=False)
            self.assertTrue(json.loads((Path(d)/'slow.status.json').read_text())['timed_out'])
            self.assertIn(b'started', (Path(d)/'slow.stdout').read_bytes())

    def test_exact_rational_signed_controls(self):
        result=self.api('rational_controls')()
        self.assertEqual(result['reference'],{'separation':'1','absolute_gap':'4'})
        self.assertGreater(result['cases'],100)
        self.assertEqual(result['failed'],0)

if __name__=='__main__':unittest.main()
