"""Small real-Git custody fixtures, separate from all mathematical claims."""
import hashlib,json,os,subprocess,tempfile,unittest
from pathlib import Path
import verify

class VerifyTests(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory();self.addCleanup(t.cleanup);self.root=Path(t.name)
        self.data=b'fixture only\n';(self.root/'x.md').write_bytes(self.data)
        self.entry={'path':'x.md','bytes':len(self.data),'sha256':hashlib.sha256(self.data).hexdigest(),
                    'git_blob':hashlib.sha1(b'blob '+str(len(self.data)).encode()+b'\0'+self.data).hexdigest()}
    def git(self,*args):
        env=dict(os.environ);env.pop('GIT_NO_REPLACE_OBJECTS',None)
        return subprocess.run(['git','-c','user.name=Fixture','-c','user.email=f@example.invalid',*args],
          cwd=self.root,env=env,check=True,capture_output=True,timeout=15).stdout
    def source(self):
        self.git('init','-q');self.git('add','x.md');self.git('commit','-qm','fixture')
        return dict(self.entry,commit=self.git('rev-parse','HEAD').decode().strip())
    def test_valid_identity(self):
        self.assertEqual(verify.identity(self.data,self.entry),True)
    def test_wrong_identity_rejects(self):
        for key,bad in [('bytes',0),('bytes',True),('sha256','0'*64),('git_blob','0'*40)]:
            with self.subTest(key=key),self.assertRaises(ValueError):
                verify.identity(self.data,dict(self.entry,**{key:bad}))
    def test_inventory_drift(self):
        (self.root/'MANIFEST.json').write_text(json.dumps({'files':[self.entry]}))
        self.assertEqual(verify.inventory(self.root),1)
        (self.root/'extra').write_text('unlisted')
        with self.assertRaises(ValueError):verify.inventory(self.root)
    def test_json_and_symlink(self):
        p=self.root/'j.json';p.write_text('{"a":1,"a":2}')
        with self.assertRaises(ValueError):verify.load(p)
        p.unlink();p.symlink_to('x.md')
        with self.assertRaises(ValueError):verify.load(p)
    def test_real_historical_read(self):
        entry=self.source();(self.root/'x.md').write_text('changed worktree')
        self.assertEqual(verify.historical(self.root,entry),self.data)
    def test_replacement_and_invalid_paths(self):
        entry=self.source();(self.root/'x.md').write_text('forged')
        self.git('add','x.md');self.git('commit','-qm','replacement')
        new=self.git('rev-parse','HEAD').decode().strip();self.git('replace',entry['commit'],new)
        self.assertEqual(self.git('show',entry['commit']+':x.md'),b'forged')
        self.assertEqual(verify.historical(self.root,entry),self.data)
        for path in ('../x.md','/x.md','a//x.md'):
            with self.subTest(path=path),self.assertRaises(ValueError):verify.historical(self.root,dict(entry,path=path))
        with self.assertRaises(ValueError):verify.historical(self.root,dict(entry,commit=self.entry['git_blob']))

if __name__=='__main__':unittest.main()
