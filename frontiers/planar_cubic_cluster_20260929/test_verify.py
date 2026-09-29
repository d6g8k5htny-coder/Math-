"""Verifier regression tests using a real isolated Git fixture, no network."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
import verify as v

class VerifyTests(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory(); self.addCleanup(t.cleanup)
        self.root=Path(t.name); self.data=b'exact local test fixture\n'
        (self.root/'source.md').write_bytes(self.data)
        self.git('init','-q'); self.git('add','source.md')
        self.git('-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','-qm','fixture')
        self.entry={'id':'source','path':'source.md','commit':self.git('rev-parse','HEAD').decode().strip(),
                    'bytes':len(self.data),'sha256':hashlib.sha256(self.data).hexdigest(),
                    'git_blob':self.git('rev-parse','HEAD:source.md').decode().strip()}
    def git(self,*args):
        return subprocess.run(['git',*args],cwd=self.root,check=True,capture_output=True,timeout=15).stdout
    def check(self,entry):
        (self.root/'SOURCES.json').write_text(json.dumps({'sources':[entry]}))
        v.verify_sources(self.root)
    def test_valid_source(self): self.check(self.entry)
    def test_wrong_identity_fields(self):
        for field,value in [('bytes',0),('sha256','0'*64),('git_blob','0'*40)]:
            entry=copy.deepcopy(self.entry); entry[field]=value
            with self.subTest(field=field), self.assertRaises(ValueError): self.check(entry)
    def test_missing_source(self):
        entry=copy.deepcopy(self.entry); entry['path']='missing.md'
        with self.assertRaises(subprocess.CalledProcessError): self.check(entry)
    def test_traversal_rejected(self):
        entry=copy.deepcopy(self.entry); entry['path']='../source.md'
        with self.assertRaises(ValueError): self.check(entry)
    def test_wrong_commit(self):
        entry=copy.deepcopy(self.entry); entry['commit']='0'*40
        with self.assertRaises(subprocess.CalledProcessError): self.check(entry)
    def test_duplicate_json(self):
        p=self.root/'duplicate.json'; p.write_text('{"a":1,"a":2}')
        with self.assertRaises(ValueError): v.read_json(p)

if __name__=='__main__': unittest.main()
