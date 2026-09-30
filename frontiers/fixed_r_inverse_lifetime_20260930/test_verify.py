"""Real-Git regressions for the reused, narrowed source-verification driver."""
import hashlib,json,os,subprocess,tempfile,unittest
from pathlib import Path
import verify as v


def entry(path,data,**kw):
    return dict(path=path,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),
                git_blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest(),**kw)

class SourceTests(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory();self.addCleanup(t.cleanup);self.repo=Path(t.name)
        self.root=self.repo/'frontiers/packet';self.root.mkdir(parents=True)
        self.git('init','-q');self.data=b'source fixture\n'
        (self.repo/'P.md').write_bytes(self.data);self.git('add','P.md');self.git('commit','-qm','fixture')
        self.sha=self.git('rev-parse','HEAD').decode().strip();self.e=entry('P.md',self.data,id='P',commit=self.sha);self.write()
    def git(self,*args):
        env=os.environ.copy();env.pop('GIT_NO_REPLACE_OBJECTS',None)
        return subprocess.run(['git','-c','user.name=Fixture','-c','user.email=fixture@example.invalid',*args],cwd=self.repo,env=env,capture_output=True,check=True,timeout=15).stdout
    def write(self,es=None):
        (self.root/'SOURCES.json').write_text(json.dumps({'sources':[self.e] if es is None else es}))
    def test_original_nested_source(self):self.assertEqual(v.sources(self.root),1)
    def test_identity_drift(self):
        for k,x in [('bytes',0),('bytes',True),('sha256','0'*64),('git_blob','0'*40)]:
            self.write([dict(self.e,**{k:x})])
            with self.subTest(k=k),self.assertRaises(ValueError):v.sources(self.root)
    def test_empty_duplicate_sources(self):
        for es in ([],[self.e,self.e]):
            self.write(es)
            with self.assertRaises(ValueError):v.sources(self.root)
    def test_noncommit_and_unsafe_path(self):
        self.write([dict(self.e,commit=self.git('rev-parse','HEAD^{tree}').decode().strip())])
        with self.assertRaises(ValueError):v.sources(self.root)
        self.write([dict(self.e,path='../P.md')])
        with self.assertRaises(ValueError):v.sources(self.root)
    def test_replace_cannot_change_history(self):
        new=b'forged\n';(self.repo/'P.md').write_bytes(new);self.git('add','P.md');self.git('commit','-qm','change')
        self.git('replace',self.sha,self.git('rev-parse','HEAD').decode().strip())
        self.assertEqual(self.git('show',self.sha+':P.md'),new)
        self.assertEqual(v.sources(self.root),1)
        self.write([entry('P.md',new,id='P',commit=self.sha)])
        with self.assertRaises(ValueError):v.sources(self.root)
    def test_symlink_source(self):
        (self.repo/'P.md').unlink();(self.repo/'P.md').symlink_to('elsewhere')
        self.git('add','P.md');self.git('commit','-qm','link')
        self.write([dict(self.e,commit=self.git('rev-parse','HEAD').decode().strip())])
        with self.assertRaises(ValueError):v.sources(self.root)

class PacketTests(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory();self.addCleanup(t.cleanup);self.root=Path(t.name)
        self.data=b'packet\n';(self.root/'PROOF.md').write_bytes(self.data)
        (self.root/'MANIFEST.json').write_text(json.dumps({'files':[entry('PROOF.md',self.data)]}))
    def test_original(self):self.assertEqual(v.inventory(self.root),1)
    def test_changed_payload(self):
        (self.root/'PROOF.md').write_bytes(b'changed')
        with self.assertRaises(ValueError):v.inventory(self.root)
    def test_extra_file(self):
        (self.root/'extra').write_bytes(b'x')
        with self.assertRaises(ValueError):v.inventory(self.root)
    def test_duplicate_json(self):
        (self.root/'MANIFEST.json').write_text('{"files":[],"files":[]}')
        with self.assertRaises(ValueError):v.inventory(self.root)
    def test_symlink_payload(self):
        (self.root/'PROOF.md').unlink();(self.root/'PROOF.md').symlink_to('MANIFEST.json')
        with self.assertRaises(ValueError):v.inventory(self.root)

if __name__=='__main__':unittest.main()
