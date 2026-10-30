"""Custody regressions on real local Git objects, never on invented upstream data."""
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import verify as v


def entry(path,data,**kw):
    return dict(path=path,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),
                git_blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest(),**kw)

class SourceTests(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory();self.addCleanup(t.cleanup);self.repo=Path(t.name)
        self.root=self.repo/'frontiers'/'packet';self.root.mkdir(parents=True)
        self.git('init','-q');self.data=b'fixture\n'
        for name in ('R','SC','P'):(self.repo/(name+'.md')).write_bytes(self.data)
        self.git('add','R.md','SC.md','P.md');self.git('commit','-qm','fixture')
        self.commit=self.git('rev-parse','HEAD').decode().strip()
        self.es=[entry(x+'.md',self.data,id=x,commit=self.commit) for x in ('R','SC','P')];self.write()
    def git(self,*args):
        env=os.environ.copy();env.pop('GIT_NO_REPLACE_OBJECTS',None)
        return subprocess.run(['git','-c','user.name=Fixture','-c','user.email=fixture@example.invalid',*args],
                              cwd=self.repo,env=env,check=True,capture_output=True,timeout=15).stdout
    def write(self,es=None):
        (self.root/'SOURCES.json').write_text(json.dumps({'sources':self.es if es is None else es}))
    def test_valid_nested(self):self.assertEqual(v.sources(self.root),3)
    def test_identity_fields(self):
        for k,val in (('bytes',0),('bytes',True),('sha256','0'*64),('git_blob','0'*40)):
            es=copy.deepcopy(self.es);es[0][k]=val;self.write(es)
            with self.subTest(k=k,val=val),self.assertRaises(ValueError):v.sources(self.root)
    def test_missing_and_duplicate_inventory(self):
        for es in ([],self.es[:-1],self.es+[self.es[0]]):
            self.write(es)
            with self.assertRaises(ValueError):v.sources(self.root)
    def test_wrong_id(self):
        es=copy.deepcopy(self.es);es[0]['id']='X';self.write(es)
        with self.assertRaises(ValueError):v.sources(self.root)
    def test_unsafe_paths(self):
        for p in ('../R.md','/R.md','./R.md','x//R.md','x/../R.md',''):
            es=copy.deepcopy(self.es);es[0]['path']=p;self.write(es)
            with self.subTest(path=p),self.assertRaises(ValueError):v.sources(self.root)
    def test_missing_file(self):
        es=copy.deepcopy(self.es);es[0]['path']='missing.md';self.write(es)
        with self.assertRaises(ValueError):v.sources(self.root)
    def test_noncommit_tree(self):
        es=copy.deepcopy(self.es);es[0]['commit']=self.git('rev-parse','HEAD^{tree}').decode().strip();self.write(es)
        with self.assertRaises(ValueError):v.sources(self.root)
    def test_annotated_tag(self):
        self.git('tag','-a','tag','-m','tag');es=copy.deepcopy(self.es)
        es[0]['commit']=self.git('rev-parse','tag').decode().strip();self.write(es)
        with self.assertRaises(ValueError):v.sources(self.root)
    def test_missing_commit(self):
        es=copy.deepcopy(self.es);es[0]['commit']='0'*40;self.write(es)
        with self.assertRaises(ValueError):v.sources(self.root)
    def test_leaf_symlink(self):
        (self.repo/'R.md').unlink();(self.repo/'R.md').symlink_to('SC.md');self.git('add','R.md');self.git('commit','-qm','link')
        es=copy.deepcopy(self.es);es[0]['commit']=self.git('rev-parse','HEAD').decode().strip();self.write(es)
        with self.assertRaises(ValueError):v.sources(self.root)
    def test_replacements_disabled(self):
        changed=b'forged bytes\n';(self.repo/'R.md').write_bytes(changed);self.git('add','R.md');self.git('commit','-qm','changed')
        newer=self.git('rev-parse','HEAD').decode().strip();self.git('replace',self.commit,newer)
        self.assertEqual(self.git('show',self.commit+':R.md'),changed)
        self.assertEqual(v.sources(self.root),3)
        es=copy.deepcopy(self.es);es[0].update(entry('R.md',changed));self.write(es)
        with self.assertRaises(ValueError):v.sources(self.root)

class PacketTests(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory();self.addCleanup(t.cleanup);self.root=Path(t.name);self.data=b'payload\n'
        (self.root/'proof.md').write_bytes(self.data)
        self.entries=[entry('proof.md',self.data)];self.write()
    def write(self): (self.root/'MANIFEST.json').write_text(json.dumps({'files':self.entries}))
    def test_valid(self):self.assertEqual(v.inventory(self.root),1)
    def test_changed(self):
        (self.root/'proof.md').write_bytes(b'changed')
        with self.assertRaises(ValueError):v.inventory(self.root)
    def test_extra(self):
        (self.root/'extra').write_bytes(b'x')
        with self.assertRaises(ValueError):v.inventory(self.root)
    def test_missing(self):
        (self.root/'proof.md').unlink()
        with self.assertRaises(ValueError):v.inventory(self.root)
    def test_duplicate(self):
        self.entries+=self.entries;self.write()
        with self.assertRaises(ValueError):v.inventory(self.root)
    def test_symlink_payload(self):
        (self.root/'proof.md').unlink();(self.root/'proof.md').symlink_to('MANIFEST.json')
        with self.assertRaises(ValueError):v.inventory(self.root)
    def test_symlink_manifest(self):
        p=self.root/'MANIFEST.json';p.rename(self.root/'real');p.symlink_to('real')
        with self.assertRaises(ValueError):v.inventory(self.root)
    def test_json_duplicate(self):
        p=self.root/'MANIFEST.json';p.write_text('{"files":[],"files":[]}')
        with self.assertRaises(ValueError):v.inventory(self.root)

class WrapperProtocolTests(unittest.TestCase):
    def flags(self):
        return ['-B','-O','-S'] if sys.flags.optimize else ['-B','-S']

    def run_rate(self, *args):
        script=Path(__file__).with_name('rate.py')
        return subprocess.run([sys.executable,*self.flags(),str(script),*args],
                              cwd=script.parent,capture_output=True,timeout=45,
                              env=dict(os.environ,COLUMNS='80'))

    def test_actual_semantic_mutants_match_exact_reasons_in_executing_mode(self):
        for name in v.EXPECTED_MUTANT_ERRORS:
            with self.subTest(mutant=name):
                run=self.run_rate('--mutant',name)
                v.validate_mutant_result(name,run)

    def test_actual_unknown_label_matches_argparse_in_executing_mode(self):
        run=self.run_rate('--mutant','unknown')
        v.validate_unknown_result(run)

    def test_adverse_subprocess_results_are_rejected_in_executing_mode(self):
        expected=json.dumps({'error':v.EXPECTED_MUTANT_ERRORS['omit-shift'],
                             'passed':False},sort_keys=True)
        wrong=json.dumps({'error':'unrelated failure reason','passed':False},sort_keys=True)
        cases=(
            ('runtime-error',"raise RuntimeError('unrelated child crash')\n"),
            ('silent-exit-1',"raise SystemExit(1)\n"),
            ('wrong-reason',f"print({wrong!r})\nraise SystemExit(1)\n"),
            ('wrong-exit',f"print({expected!r})\nraise SystemExit(0)\n"),
            ('unexpected-stderr',f"print({expected!r})\nprint('unexpected stderr',file=sys.stderr)\nraise SystemExit(1)\n"),
        )
        with tempfile.TemporaryDirectory() as tmp:
            child=Path(tmp)/'child.py'
            for label,body in cases:
                child.write_text('import sys\n'+body)
                run=subprocess.run([sys.executable,*self.flags(),str(child)],
                                   cwd=tmp,capture_output=True,timeout=10)
                with self.subTest(case=label):
                    with self.assertRaises(ValueError):
                        v.validate_mutant_result('omit-shift',run)
            child.write_text('raise SystemExit(2)\n')
            run=subprocess.run([sys.executable,*self.flags(),str(child)],
                               cwd=tmp,capture_output=True,timeout=10)
            with self.assertRaises(ValueError):
                v.validate_unknown_result(run)
            child.write_text("import argparse\np=argparse.ArgumentParser(prog='rate.py')\np.error('unrelated parser failure')\n")
            run=subprocess.run([sys.executable,*self.flags(),str(child)],
                               cwd=tmp,capture_output=True,timeout=10)
            with self.assertRaises(ValueError):
                v.validate_unknown_result(run)

            expected = v.expected_unknown_stderr()
            parts = expected.splitlines()
            usage = b'\n'.join(parts[:-1]) + b'\n'
            diagnostic = parts[-1] + b'\n'
            cases = (
                ('wrong-usage-header', expected.replace(
                    b'usage: rate.py', b'usage: rate.py bogus', 1), 2, b''),
                ('extra-indented-stderr', usage + b'    unrelated indented stderr\\n' + diagnostic, 2, b''),
                ('missing-terminal-newline', expected[:-1], 2, b''),
                ('extra-terminal-output', expected + b'\n', 2, b''),
                ('wrong-exit', expected, 1, b''),
                ('unexpected-stdout', expected, 2, b'unexpected'),
            )
            for label, stderr, code, stdout in cases:
                bad = subprocess.CompletedProcess(['rate.py'], code, stdout, stderr)
                with self.subTest(case=label):
                    with self.assertRaises(ValueError):
                        v.validate_unknown_result(bad)


if __name__=='__main__':unittest.main()
