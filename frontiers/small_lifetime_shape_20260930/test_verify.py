"""Real local Git fixtures for source and packet custody, not upstream evidence."""
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
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup);self.repo=Path(temp.name)
        self.root=self.repo/'frontiers/packet';self.root.mkdir(parents=True)
        self.git('init','-q');self.data=b'exact local fixture\n'
        (self.repo/'imports').mkdir()
        for label in ('E','C'):(self.repo/f'imports/{label}.md').write_bytes(self.data)
        self.git('add','imports');self.git('commit','-qm','fixture')
        self.commit=self.git('rev-parse','HEAD').decode().strip()
        self.es=[entry(f'imports/{s}.md',self.data,id=s,commit=self.commit) for s in ('E','C')];self.write()
    def git(self,*args):
        env=os.environ.copy();env.pop('GIT_NO_REPLACE_OBJECTS',None)
        return subprocess.run(['git','-c','user.name=Fixture','-c','user.email=fixture@example.invalid',*args],
                              cwd=self.repo,env=env,check=True,capture_output=True,timeout=15).stdout
    def write(self,es=None):
        (self.root/'SOURCES.json').write_text(json.dumps({'sources':self.es if es is None else es}))
    def test_valid_nested_sources(self):self.assertEqual(verify.sources(self.root),2)
    def test_required_identity_fields(self):
        for key,val in (('sha256','0'*64),('git_blob','0'*40),('bytes',0),('bytes',True)):
            es=copy.deepcopy(self.es);es[0][key]=val;self.write(es)
            with self.subTest(key=key,val=val),self.assertRaises(ValueError):verify.sources(self.root)
        es=copy.deepcopy(self.es);del es[0]['bytes'];self.write(es)
        with self.assertRaises(ValueError):verify.sources(self.root)
    def test_missing_duplicate_or_unexpected_source(self):
        bad=[[],self.es[:-1],self.es+[self.es[0]],[dict(self.es[0],id='X'),self.es[1]]]
        for es in bad:
            self.write(es)
            with self.subTest(es=es),self.assertRaises(ValueError):verify.sources(self.root)
    def test_wrong_object_type(self):
        self.git('tag','-a','fixture-tag','-m','tag')
        for obj in ('HEAD^{tree}','HEAD:imports/E.md','fixture-tag'):
            es=copy.deepcopy(self.es);es[0]['commit']=self.git('rev-parse',obj).decode().strip();self.write(es)
            with self.subTest(obj=obj),self.assertRaises(ValueError):verify.sources(self.root)
    def test_missing_or_unsafe_path(self):
        for path in ('missing.md','../E.md','/imports/E.md','imports//E.md','imports/./E.md','imports/../E.md'):
            es=copy.deepcopy(self.es);es[0]['path']=path;self.write(es)
            with self.subTest(path=path),self.assertRaises(ValueError):verify.sources(self.root)
    def test_bad_commit(self):
        for commit in ('0'*40,'HEAD','A'*40):
            es=copy.deepcopy(self.es);es[0]['commit']=commit;self.write(es)
            with self.subTest(commit=commit),self.assertRaises(ValueError):verify.sources(self.root)
    def test_leaf_symlink_rejected(self):
        p=self.repo/'imports/E.md';p.unlink();p.symlink_to('C.md')
        self.git('add','imports/E.md');self.git('commit','-qm','symlink')
        es=copy.deepcopy(self.es);es[0]['commit']=self.git('rev-parse','HEAD').decode().strip();self.write(es)
        with self.assertRaises(ValueError):verify.sources(self.root)
    def test_ancestor_symlink_rejected(self):
        (self.repo/'alias').symlink_to('imports',target_is_directory=True)
        self.git('add','alias');self.git('commit','-qm','alias')
        es=copy.deepcopy(self.es);es[0].update(commit=self.git('rev-parse','HEAD').decode().strip(),path='alias/E.md');self.write(es)
        with self.assertRaises(ValueError):verify.sources(self.root)
    def test_replacement_cannot_forge_or_invalidate(self):
        changed=b'forged source\n';(self.repo/'imports/E.md').write_bytes(changed)
        self.git('add','imports/E.md');self.git('commit','-qm','changed')
        later=self.git('rev-parse','HEAD').decode().strip();self.git('replace',self.commit,later)
        self.assertEqual(self.git('show',self.commit+':imports/E.md'),changed)
        self.assertEqual(verify.sources(self.root),2)
        es=copy.deepcopy(self.es);es[0].update(entry('imports/E.md',changed));self.write(es)
        with self.assertRaises(ValueError):verify.sources(self.root)
    def test_original_source_not_worktree(self):
        (self.repo/'imports/E.md').write_bytes(b'worktree different\n')
        self.assertEqual(verify.sources(self.root),2)

class PacketTests(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup);self.root=Path(temp.name)
        self.data=b'proof fixture\n';(self.root/'PROOF.md').write_bytes(self.data)
        self.es=[entry('PROOF.md',self.data)];self.write()
    def write(self):(self.root/'MANIFEST.json').write_text(json.dumps({'files':self.es}))
    def test_valid(self):self.assertEqual(verify.inventory(self.root),1)
    def test_changed_payload(self):
        (self.root/'PROOF.md').write_bytes(b'changed')
        with self.assertRaises(ValueError):verify.inventory(self.root)
    def test_extra_missing_payload(self):
        (self.root/'extra').write_text('extra')
        with self.assertRaises(ValueError):verify.inventory(self.root)
        (self.root/'extra').unlink();(self.root/'PROOF.md').unlink()
        with self.assertRaises(ValueError):verify.inventory(self.root)
    def test_invalid_inventory(self):
        for es in ([],self.es*2,[dict(self.es[0],path='a/PROOF.md')]):
            self.es=es;self.write()
            with self.assertRaises(ValueError):verify.inventory(self.root)
    def test_symlink_payload_and_manifest(self):
        (self.root/'PROOF.md').unlink();(self.root/'PROOF.md').symlink_to('MANIFEST.json')
        with self.assertRaises(ValueError):verify.inventory(self.root)
        (self.root/'PROOF.md').unlink();(self.root/'PROOF.md').write_bytes(self.data)
        (self.root/'MANIFEST.json').rename(self.root/'real');(self.root/'MANIFEST.json').symlink_to('real')
        with self.assertRaises(ValueError):verify.inventory(self.root)
    def test_duplicate_json_and_nonobject(self):
        for text in ('{"files":[],"files":[]}','[]'):
            (self.root/'MANIFEST.json').write_text(text)
            with self.assertRaises(ValueError):verify.inventory(self.root)

if __name__=='__main__':unittest.main()
