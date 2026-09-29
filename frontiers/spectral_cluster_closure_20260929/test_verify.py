"""Source-custody tests against a real isolated Git repository, not mocked Git."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
import verify as v

class CustodyTests(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        self.root=Path(temp.name); self.data=b'proof fixture\n'
        (self.root/'nested').mkdir(); (self.root/'nested'/'source.md').write_bytes(self.data)
        (self.root/'leaf.md').symlink_to('nested/source.md')
        (self.root/'alias').symlink_to('nested',target_is_directory=True)
        self.git('init','-q'); self.git('add','nested/source.md','leaf.md','alias')
        self.git('-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','-qm','fixture')
        self.entry={'id':'S','commit':self.git('rev-parse','HEAD').decode().strip(),
                    'path':'nested/source.md','bytes':len(self.data),
                    'sha256':hashlib.sha256(self.data).hexdigest(),
                    'git_blob':self.git('rev-parse','HEAD:nested/source.md').decode().strip()}
    def git(self,*args):
        return subprocess.run(['git',*args],cwd=self.root,check=True,capture_output=True,timeout=15).stdout
    def run_pins(self,entries):
        p=self.root/'SOURCES.json'; p.write_text(json.dumps({'sources':entries}))
        return v.verify_sources(self.root)
    def test_valid_source(self):
        self.assertEqual(self.run_pins([self.entry]),1)
    def test_wrong_size(self):
        e=copy.deepcopy(self.entry); e['bytes']=0
        with self.assertRaises(ValueError): self.run_pins([e])
    def test_wrong_sha(self):
        e=copy.deepcopy(self.entry); e['sha256']='0'*64
        with self.assertRaises(ValueError): self.run_pins([e])
    def test_wrong_blob(self):
        e=copy.deepcopy(self.entry); e['git_blob']='0'*40
        with self.assertRaises(ValueError): self.run_pins([e])
    def test_missing_path(self):
        e=copy.deepcopy(self.entry); e['path']='missing.md'
        with self.assertRaises((ValueError,subprocess.CalledProcessError)): self.run_pins([e])
    def test_bad_commit(self):
        e=copy.deepcopy(self.entry); e['commit']='0'*40
        with self.assertRaises((ValueError,subprocess.CalledProcessError)): self.run_pins([e])
    def test_unsafe_paths(self):
        for path in ('../source.md','/source.md','',':source.md','nested/../source.md','nested//source.md'):
            e=copy.deepcopy(self.entry); e['path']=path
            with self.subTest(path=path),self.assertRaises(ValueError): self.run_pins([e])
    def test_duplicate_source_ids(self):
        with self.assertRaises(ValueError): self.run_pins([self.entry,self.entry])
    def test_missing_inventory(self):
        with self.assertRaises(ValueError): self.run_pins([])
    def test_git_leaf_symlink(self):
        e=copy.deepcopy(self.entry); e['path']='leaf.md'
        e['git_blob']=self.git('rev-parse','HEAD:leaf.md').decode().strip()
        data=b'nested/source.md'; e['bytes']=len(data); e['sha256']=hashlib.sha256(data).hexdigest()
        with self.assertRaises(ValueError): self.run_pins([e])
    def test_git_parent_symlink(self):
        e=copy.deepcopy(self.entry); e['path']='alias/source.md'
        with self.assertRaises((ValueError,subprocess.CalledProcessError)): self.run_pins([e])
    def test_duplicate_json(self):
        p=self.root/'dup.json'; p.write_text('{"a":1,"a":2}')
        with self.assertRaises(ValueError): v.read_json(p)
    def test_packet_leaf_symlink(self):
        packet=self.root/'packet'; packet.mkdir()
        (packet/'file.md').symlink_to('../nested/source.md')
        e={k:value for k,value in self.entry.items() if k in ('bytes','sha256','git_blob')}; e['path']='file.md'
        (packet/'MANIFEST.json').write_text(json.dumps({'files':[e]}))
        with self.assertRaises(ValueError): v.verify_inventory(packet)

if __name__=='__main__': unittest.main()
