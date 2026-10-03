"""Real temporary Git fixtures; they do not authenticate the upstream repository."""
import hashlib,json,os,subprocess,tempfile,unittest
from pathlib import Path
import verify_sources as v

class SourceTests(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory();self.addCleanup(t.cleanup);self.root=Path(t.name)
        self.git('init','-q');self.data=b'original exact source\n'
        (self.root/'source').write_bytes(self.data);self.git('add','source');self.git('commit','-qm','source')
        self.sha=self.git('rev-parse','HEAD').decode().strip()
        self.entry={'path':'source','git_blob':self.git('rev-parse','HEAD:source').decode().strip(),'commit':self.sha,'bytes':len(self.data)}
    def git(self,*args):
        env=dict(os.environ);env.pop('GIT_NO_REPLACE_OBJECTS',None)
        return subprocess.run(['git','-c','user.name=Fixture','-c','user.email=f@example.invalid',*args],cwd=self.root,
               env=env,capture_output=True,check=True,timeout=15).stdout
    def test_original_bytes(self):self.assertEqual(v.read_source(self.root,self.sha,self.entry),self.data)
    def test_reject_wrong_blob(self):
        with self.assertRaises(ValueError):v.read_source(self.root,self.sha,dict(self.entry,git_blob='0'*40))
    def test_reject_noncommit(self):
        with self.assertRaises(ValueError):v.read_source(self.root,self.entry['git_blob'],self.entry)
    def test_reject_unsafe_paths(self):
        for path in ('../source','/source','x//source','x/./source'):
            with self.subTest(path=path),self.assertRaises(ValueError):v.read_source(self.root,self.sha,dict(self.entry,path=path))
    def test_ignore_changed_worktree(self):
        (self.root/'source').write_text('new')
        self.assertEqual(v.read_source(self.root,self.sha,self.entry),self.data)
    def test_ignore_replace_objects(self):
        (self.root/'source').write_text('new');self.git('add','source');self.git('commit','-qm','new')
        other=self.git('rev-parse','HEAD').decode().strip();self.git('replace',self.sha,other)
        self.assertEqual(self.git('show',self.sha+':source'),b'new')
        self.assertEqual(v.read_source(self.root,self.sha,self.entry),self.data)
    def test_reject_symlink_source(self):
        (self.root/'alias').symlink_to('source');self.git('add','alias');self.git('commit','-qm','symlink')
        sha=self.git('rev-parse','HEAD').decode().strip();blob=self.git('rev-parse','HEAD:alias').decode().strip()
        with self.assertRaises(ValueError):v.read_source(self.root,sha,{'path':'alias','git_blob':blob})
    def test_all_three_distinct_source_refs(self):
        entries=[dict(self.entry,tag=tag) for tag in ('P','RATE','O')]
        self.assertEqual(v.verify_bound_sources(self.root,{'files':entries}),3)
    def test_reject_missing_source(self):
        with self.assertRaises(ValueError):v.verify_bound_sources(self.root,{'files':[dict(self.entry,tag='P')]})
    def test_optional_size_and_sha(self):
        entries=[dict(self.entry,tag=tag,sha256=hashlib.sha256(self.data).hexdigest()) for tag in ('P','RATE','O')]
        self.assertEqual(v.verify_bound_sources(self.root,{'files':entries}),3)
        entries[1]['bytes']+=1
        with self.assertRaises(ValueError):v.verify_bound_sources(self.root,{'files':entries})
    def test_reject_sha_drift(self):
        entries=[dict(self.entry,tag=tag,sha256='0'*64) for tag in ('P','RATE','O')]
        with self.assertRaises(ValueError):v.verify_bound_sources(self.root,{'files':entries})

class InventoryTests(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory();self.addCleanup(t.cleanup);self.root=Path(t.name)
        data=b'exact\n';(self.root/'payload').write_bytes(data)
        self.entry={'path':'payload','bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
        (self.root/'MANIFEST.json').write_text(json.dumps({'files':[self.entry]}))
    def test_exact_inventory(self):self.assertEqual(v.inventory(self.root),1)
    def test_reject_extra(self):
        (self.root/'extra').write_text('extra')
        with self.assertRaises(ValueError):v.inventory(self.root)
    def test_reject_changed_bytes(self):
        (self.root/'payload').write_text('changed')
        with self.assertRaises(ValueError):v.inventory(self.root)
    def test_reject_symlink_payload(self):
        (self.root/'payload').unlink();(self.root/'payload').symlink_to('MANIFEST.json')
        with self.assertRaises(ValueError):v.inventory(self.root)
    def test_reject_duplicate_json_keys(self):
        (self.root/'MANIFEST.json').write_text('{"files":[],"files":[]}')
        with self.assertRaises(ValueError):v.inventory(self.root)

if __name__=='__main__':unittest.main()
