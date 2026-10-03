"""Real local source-object fixtures, never an upstream execution substitute."""
import hashlib,json,os,subprocess,tempfile,unittest
from pathlib import Path
import verify

class SourceTests(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory();self.addCleanup(t.cleanup);self.repo=Path(t.name)
        self.root=self.repo/'nested/packet';self.root.mkdir(parents=True)
        self.git('init','-q');self.data=b'exact source fixture\n';(self.repo/'proof.md').write_bytes(self.data)
        self.git('add','proof.md');self.git('commit','-qm','source')
        self.sha=self.git('rev-parse','HEAD').decode().strip()
        self.entry={'path':'proof.md','git_blob':self.git('rev-parse','HEAD:proof.md').decode().strip()}
    def git(self,*args):
        env=dict(os.environ);env.pop('GIT_NO_REPLACE_OBJECTS',None)
        return subprocess.run(['git','-c','user.name=Fixture','-c','user.email=f@example.invalid',*args],cwd=self.repo,
               check=True,capture_output=True,env=env,timeout=15).stdout
    def test_source(self):self.assertEqual(verify.read_source(self.root,self.sha,self.entry),self.data)
    def test_wrong_binding(self):
        with self.assertRaises(ValueError):verify.read_source(self.root,self.sha,dict(self.entry,git_blob='0'*40))
    def test_wrong_kind(self):
        with self.assertRaises(ValueError):verify.read_source(self.root,self.entry['git_blob'],self.entry)
    def test_unsafe_path(self):
        for p in ('../proof.md','/proof.md','x//proof.md','x/./proof.md'):
            with self.subTest(path=p),self.assertRaises(ValueError):verify.read_source(self.root,self.sha,dict(self.entry,path=p))
    def test_replacement_does_not_intercept(self):
        new=b'forged\n';(self.repo/'proof.md').write_bytes(new);self.git('add','proof.md');self.git('commit','-qm','new')
        other=self.git('rev-parse','HEAD').decode().strip();self.git('replace',self.sha,other)
        self.assertEqual(self.git('show',self.sha+':proof.md'),new)
        self.assertEqual(verify.read_source(self.root,self.sha,self.entry),self.data)
    def test_historical_not_worktree(self):
        (self.repo/'proof.md').write_text('changed')
        self.assertEqual(verify.read_source(self.root,self.sha,self.entry),self.data)

class PacketTests(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory();self.addCleanup(t.cleanup);self.root=Path(t.name)
        self.data=b'exact\n';(self.root/'payload').write_bytes(self.data)
        self.entry={'path':'payload','bytes':len(self.data),'sha256':hashlib.sha256(self.data).hexdigest()}
        (self.root/'MANIFEST.json').write_text(json.dumps({'files':[self.entry]}))
    def test_membership(self):self.assertEqual(verify.inventory(self.root),1)
    def test_drift(self):
        (self.root/'payload').write_bytes(b'drift')
        with self.assertRaises(ValueError):verify.inventory(self.root)
    def test_extra(self):
        (self.root/'extra').write_bytes(b'x')
        with self.assertRaises(ValueError):verify.inventory(self.root)
    def test_symlink(self):
        (self.root/'payload').unlink();(self.root/'payload').symlink_to('MANIFEST.json')
        with self.assertRaises(ValueError):verify.inventory(self.root)
    def test_duplicate_json(self):
        (self.root/'MANIFEST.json').write_text('{"files":[],"files":[]}')
        with self.assertRaises(ValueError):verify.inventory(self.root)

if __name__=='__main__':unittest.main()
