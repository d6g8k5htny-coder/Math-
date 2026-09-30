"""Synthetic byte-custody controls; not analytic or upstream theorem verification."""
from pathlib import Path
import hashlib
import tempfile
import unittest
import source_check as m

class SourceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root/'sources').mkdir()
        self.data = b'original source\n'
        (self.root/'sources'/'proof.md').write_bytes(self.data)
        self.entry = {'id':'F','path':'sources/proof.md','bytes':len(self.data),
                      'sha256':hashlib.sha256(self.data).hexdigest(),
                      'git_blob':hashlib.sha1(f'blob {len(self.data)}\0'.encode()+self.data).hexdigest()}
    def test_original_passes(self):
        self.assertEqual(m.verify_files(self.root,[self.entry]),1)
    def test_changed_byte_fails(self):
        (self.root/'sources'/'proof.md').write_bytes(b'changed source!\n')
        with self.assertRaises(ValueError):m.verify_files(self.root,[self.entry])
    def test_missing_file_fails(self):
        (self.root/'sources'/'proof.md').unlink()
        with self.assertRaises(ValueError):m.verify_files(self.root,[self.entry])
    def test_wrong_length_fails(self):
        with self.assertRaises(ValueError):m.verify_files(self.root,[dict(self.entry,bytes=1)])
    def test_wrong_sha_fails(self):
        with self.assertRaises(ValueError):m.verify_files(self.root,[dict(self.entry,sha256='0'*64)])
    def test_wrong_blob_fails(self):
        with self.assertRaises(ValueError):m.verify_files(self.root,[dict(self.entry,git_blob='0'*40)])
    def test_traversal_fails(self):
        with self.assertRaises(ValueError):m.verify_files(self.root,[dict(self.entry,path='../proof.md')])
    def test_leaf_link_fails(self):
        (self.root/'original').write_bytes(self.data)
        p=self.root/'sources'/'proof.md';p.unlink();p.symlink_to('../original')
        with self.assertRaises(ValueError):m.verify_files(self.root,[self.entry])
    def test_parent_link_fails(self):
        (self.root/'sources').rename(self.root/'actual')
        (self.root/'sources').symlink_to('actual',target_is_directory=True)
        with self.assertRaises(ValueError):m.verify_files(self.root,[self.entry])
    def test_duplicate_fails(self):
        with self.assertRaises(ValueError):m.verify_files(self.root,[self.entry,self.entry])

if __name__=='__main__':unittest.main()
