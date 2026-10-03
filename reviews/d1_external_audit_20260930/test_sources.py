"""Local real-Git fixtures test custody behavior, not the project premises."""
import hashlib
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
import verify_sources as v

class SourcesTests(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory();self.addCleanup(t.cleanup);self.repo=Path(t.name)
        (self.repo/'imports').mkdir();self.data=b'fixture source only\n'
        (self.repo/'imports/P.md').write_bytes(self.data)
        self.git('init','-q');self.git('add','imports');self.git('commit','-qm','original')
        self.commit=self.git('rev-parse','HEAD').decode().strip()
        self.entry={'path':'imports/P.md','git_blob':self.git('rev-parse','HEAD:imports/P.md').decode().strip(),
                    'bytes':len(self.data),'sha256':hashlib.sha256(self.data).hexdigest()}
        self.nested=self.repo/'reviews/packet';self.nested.mkdir(parents=True)
    def git(self,*args):
        env=os.environ.copy();env.pop('GIT_NO_REPLACE_OBJECTS',None)
        return subprocess.run(['git','-c','user.name=Fixture','-c','user.email=fixture@example.invalid',*args],
            cwd=self.repo,env=env,capture_output=True,check=True,timeout=15).stdout
    def test_valid_from_nested_directory(self):
        self.assertEqual(v.verify_bindings(self.nested,self.commit,[self.entry]),1)
    def test_bad_identities(self):
        for key,val in [('git_blob','0'*40),('bytes',0),('sha256','0'*64)]:
            with self.subTest(key=key),self.assertRaises(ValueError):
                v.verify_bindings(self.nested,self.commit,[dict(self.entry,**{key:val})])
    def test_bad_paths_and_inventories(self):
        for path in ['../P.md','/imports/P.md','imports//P.md','missing.md']:
            with self.subTest(path=path),self.assertRaises(ValueError):
                v.verify_bindings(self.nested,self.commit,[dict(self.entry,path=path)])
        with self.assertRaises(ValueError):v.verify_bindings(self.nested,self.commit,[])
        with self.assertRaises(ValueError):v.verify_bindings(self.nested,self.commit,[self.entry,self.entry])
    def test_only_real_commit(self):
        for obj in ['HEAD^{tree}','HEAD:imports/P.md']:
            with self.subTest(obj=obj),self.assertRaises(ValueError):
                v.verify_bindings(self.nested,self.git('rev-parse',obj).decode().strip(),[self.entry])
    def test_symlink_source(self):
        p=self.repo/'imports/P.md';p.unlink();p.symlink_to('../target')
        self.git('add','imports');self.git('commit','-qm','link')
        with self.assertRaises(ValueError):v.verify_bindings(self.nested,self.git('rev-parse','HEAD').decode().strip(),[self.entry])
    def test_replacement_does_not_forge_or_invalidate(self):
        forged=b'replaced\n';(self.repo/'imports/P.md').write_bytes(forged)
        self.git('add','imports');self.git('commit','-qm','replacement')
        new=self.git('rev-parse','HEAD').decode().strip();self.git('replace',self.commit,new)
        self.assertEqual(self.git('show',self.commit+':imports/P.md'),forged)
        self.assertEqual(v.verify_bindings(self.nested,self.commit,[self.entry]),1)
        altered=dict(self.entry,git_blob=self.git('rev-parse','HEAD:imports/P.md').decode().strip(),bytes=len(forged),sha256=hashlib.sha256(forged).hexdigest())
        with self.assertRaises(ValueError):v.verify_bindings(self.nested,self.commit,[altered])

if __name__=='__main__':unittest.main()
