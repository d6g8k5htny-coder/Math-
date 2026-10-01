"""Real local Git regression fixtures; they do not authenticate project inputs."""
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
import verify


def entry(path,data,**kw):
    return dict(path=path,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),
                git_blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest(),**kw)

class SourceTests(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup);self.repo=Path(tmp.name)
        self.root=self.repo/'frontiers/packet';self.root.mkdir(parents=True)
        self.git('init','-q');self.data=b'fixture source only\n'
        for label in ('R','C','D','ELDER2','ELDERD'):
            (self.repo/(label+'.md')).write_bytes(self.data)
        self.git('add','*.md');self.git('commit','-qm','fixture')
        self.sha=self.git('rev-parse','HEAD').decode().strip()
        self.es=[entry(x+'.md',self.data,id=x,commit=self.sha) for x in ('R','C','D','ELDER2','ELDERD')]
        self.write()
    def git(self,*args):
        env=os.environ.copy();env.pop('GIT_NO_REPLACE_OBJECTS',None)
        return subprocess.run(['git','-c','user.name=Fixture','-c','user.email=fixture@example.invalid',*args],
                              cwd=self.repo,env=env,check=True,capture_output=True,timeout=15).stdout
    def write(self,es=None):
        (self.root/'SOURCES.json').write_text(json.dumps({'sources':self.es if es is None else es}))
    def test_valid_nested_sources(self):self.assertEqual(verify.sources(self.root),5)
    def test_required_identity_changes(self):
        for key,val in (('sha256','0'*64),('git_blob','0'*40),('bytes',0),('bytes',True)):
            es=copy.deepcopy(self.es);es[0][key]=val;self.write(es)
            with self.subTest(key=key),self.assertRaises(ValueError):verify.sources(self.root)
    def test_inventory_incomplete(self):
        for es in ([],self.es[:-1],self.es+[self.es[0]]):
            self.write(es)
            with self.assertRaises(ValueError):verify.sources(self.root)
    def test_wrong_source_kind(self):
        for obj in ('HEAD^{tree}','HEAD:R.md'):
            es=copy.deepcopy(self.es);es[0]['commit']=self.git('rev-parse',obj).decode().strip();self.write(es)
            with self.assertRaises(ValueError):verify.sources(self.root)
    def test_missing_and_unsafe_path(self):
        for p in ('missing.md','../R.md','/R.md','./R.md','dir//R.md'):
            es=copy.deepcopy(self.es);es[0]['path']=p;self.write(es)
            with self.subTest(p=p),self.assertRaises(ValueError):verify.sources(self.root)
    def test_regular_leaf_only(self):
        (self.repo/'R.md').unlink();(self.repo/'R.md').symlink_to('C.md')
        self.git('add','R.md');self.git('commit','-qm','symlink')
        es=copy.deepcopy(self.es);es[0]['commit']=self.git('rev-parse','HEAD').decode().strip();self.write(es)
        with self.assertRaises(ValueError):verify.sources(self.root)
    def test_git_replacement_cannot_forge_source(self):
        new=b'forged historical bytes\n';(self.repo/'R.md').write_bytes(new)
        self.git('add','R.md');self.git('commit','-qm','new')
        head=self.git('rev-parse','HEAD').decode().strip();self.git('replace',self.sha,head)
        self.assertEqual(self.git('show',self.sha+':R.md'),new)
        self.assertEqual(verify.sources(self.root),5)
        es=copy.deepcopy(self.es);es[0].update(entry('R.md',new));self.write(es)
        with self.assertRaises(ValueError):verify.sources(self.root)

class PacketTests(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory();self.addCleanup(t.cleanup);self.root=Path(t.name)
        self.data=b'payload\n';(self.root/'PROOF.md').write_bytes(self.data)
        self.es=[entry('PROOF.md',self.data)];self.write()
    def write(self):(self.root/'MANIFEST.json').write_text(json.dumps({'files':self.es}))
    def test_valid(self):self.assertEqual(verify.inventory(self.root),1)
    def test_changed(self):
        (self.root/'PROOF.md').write_bytes(b'changed')
        with self.assertRaises(ValueError):verify.inventory(self.root)
    def test_extra_missing(self):
        (self.root/'extra').write_text('x')
        with self.assertRaises(ValueError):verify.inventory(self.root)
        (self.root/'extra').unlink();(self.root/'PROOF.md').unlink()
        with self.assertRaises(ValueError):verify.inventory(self.root)
    def test_duplicate(self):
        self.es+=self.es;self.write()
        with self.assertRaises(ValueError):verify.inventory(self.root)
    def test_symlink_payload_manifest(self):
        (self.root/'PROOF.md').unlink();(self.root/'PROOF.md').symlink_to('MANIFEST.json')
        with self.assertRaises(ValueError):verify.inventory(self.root)
        (self.root/'PROOF.md').unlink();(self.root/'PROOF.md').write_bytes(self.data)
        (self.root/'MANIFEST.json').rename(self.root/'real')
        (self.root/'MANIFEST.json').symlink_to('real')
        with self.assertRaises(ValueError):verify.inventory(self.root)
    def test_duplicate_json(self):
        (self.root/'MANIFEST.json').write_text('{"files":[],"files":[]}')
        with self.assertRaises(ValueError):verify.inventory(self.root)

if __name__=='__main__':unittest.main()
