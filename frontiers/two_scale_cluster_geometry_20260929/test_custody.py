"""Real isolated Git fixtures for the source/inventory verifier. No network."""
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
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.repo = Path(temp.name)
        self.packet = self.repo/'frontiers'/'fixture'
        self.packet.mkdir(parents=True)
        for name in ('a','b','c','d','e','f'):
            (self.repo/(name+'.md')).write_text('fixture '+name+'\n', encoding='utf-8')
        (self.repo/'link.md').symlink_to('a.md')
        (self.repo/'dirlink').symlink_to('frontiers',target_is_directory=True)
        self.git('init','-q')
        self.git('add','.')
        self.git('-c','user.name=Fixture','-c','user.email=fixture@example.invalid',
                 'commit','-qm','fixture')
        self.commit=self.git('rev-parse','HEAD').decode().strip()
        self.entries=[]
        for ident,name in zip(('SC','CUB','RM','C6','P','D5'),('a','b','c','d','e','f')):
            data=(self.repo/(name+'.md')).read_bytes()
            self.entries.append({'id':ident,'commit':self.commit,
                                 **self.fingerprint(name+'.md',data)})
        self.write_sources(self.entries)

    @staticmethod
    def fingerprint(path,data):
        return {'path':path,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),
                'git_blob':hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()}

    def git(self,*args):
        return subprocess.run(['git',*args],cwd=self.repo,check=True,
                              capture_output=True,timeout=20).stdout

    def write_sources(self,entries):
        (self.packet/'SOURCES.json').write_text(json.dumps({'sources':entries}),encoding='utf-8')

    def test_valid_from_nested_packet(self):
        self.assertEqual(v.verify_sources(self.packet),6)

    def test_wrong_size(self):
        e=copy.deepcopy(self.entries[0]);e['bytes']+=1
        with self.assertRaises(ValueError):v.verify_source_entry(self.packet,e)

    def test_wrong_sha256(self):
        e=copy.deepcopy(self.entries[0]);e['sha256']='0'*64
        with self.assertRaises(ValueError):v.verify_source_entry(self.packet,e)

    def test_wrong_git_blob(self):
        e=copy.deepcopy(self.entries[0]);e['git_blob']='0'*40
        with self.assertRaises(ValueError):v.verify_source_entry(self.packet,e)

    def test_missing_source(self):
        e=copy.deepcopy(self.entries[0]);e['path']='missing.md'
        with self.assertRaises(ValueError):v.verify_source_entry(self.packet,e)

    def test_malformed_commit(self):
        e=copy.deepcopy(self.entries[0]);e['commit']='HEAD'
        with self.assertRaises(ValueError):v.verify_source_entry(self.packet,e)

    def test_unsafe_paths(self):
        for path in ('../a.md','/a.md','a//b','a/./b','','a\\b'):
            e=copy.deepcopy(self.entries[0]);e['path']=path
            with self.subTest(path=path),self.assertRaises(ValueError):v.verify_source_entry(self.packet,e)

    def test_source_symlink(self):
        e=copy.deepcopy(self.entries[0]);e['path']='link.md'
        with self.assertRaises(ValueError):v.verify_source_entry(self.packet,e)

    def test_source_parent_symlink(self):
        e=copy.deepcopy(self.entries[0]);e['path']='dirlink/fixture/a.md'
        with self.assertRaises(ValueError):v.verify_source_entry(self.packet,e)

    def test_missing_inventory_entry(self):
        self.write_sources(self.entries[:-1])
        with self.assertRaises(ValueError):v.verify_sources(self.packet)

    def test_duplicate_inventory_entry(self):
        self.write_sources(self.entries+[self.entries[0]])
        with self.assertRaises(ValueError):v.verify_sources(self.packet)

    def test_empty_inventory(self):
        self.write_sources([])
        with self.assertRaises(ValueError):v.verify_sources(self.packet)

    def test_duplicate_json(self):
        path=self.packet/'bad.json';path.write_text('{"x":1,"x":2}')
        with self.assertRaises(ValueError):v.read_json(path)

    def test_source_inventory_symlink(self):
        path=self.packet/'SOURCES.json';path.unlink()
        path.symlink_to(self.repo/'a.md')
        with self.assertRaises(ValueError):v.verify_sources(self.packet)

    def inventory_fixture(self):
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup)
        root=Path(temp.name);data=b'packet fixture\n'
        (root/'note.md').write_bytes(data)
        entry=self.fingerprint('note.md',data)
        (root/'MANIFEST.json').write_text(json.dumps({'files':[entry]}))
        return root,entry

    def test_valid_packet(self):
        root,entry=self.inventory_fixture()
        self.assertEqual(v.verify_inventory(root),1)

    def test_changed_packet(self):
        root,entry=self.inventory_fixture();(root/'note.md').write_text('changed')
        with self.assertRaises(ValueError):v.verify_inventory(root)

    def test_extra_packet_leaf(self):
        root,entry=self.inventory_fixture();(root/'extra').write_text('extra')
        with self.assertRaises(ValueError):v.verify_inventory(root)

    def test_packet_symlink(self):
        root,entry=self.inventory_fixture();(root/'note.md').unlink()
        (root/'note.md').symlink_to(self.repo/'a.md')
        with self.assertRaises(ValueError):v.verify_inventory(root)

    def test_manifest_symlink(self):
        root,entry=self.inventory_fixture();(root/'MANIFEST.json').unlink()
        (root/'MANIFEST.json').symlink_to(self.repo/'a.md')
        with self.assertRaises(ValueError):v.verify_inventory(root)


if __name__=='__main__':unittest.main()
