"""Synthetic source-custody regressions; no upstream proof verification claim."""
import hashlib,json,pathlib,tempfile,unittest
import custody as c

class Custody(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=pathlib.Path(self.tmp.name);(self.root/'sub').mkdir()
        (self.root/'sub'/'proof.txt').write_bytes(b'proof\n')
        self.entry={'path':'sub/proof.txt',**c.identity(b'proof\n')}
    def test_valid_source(self):
        self.assertEqual(c.read_checked(self.root,self.entry),b'proof\n')
    def test_changed_or_missing(self):
        (self.root/'sub'/'proof.txt').write_bytes(b'amended\n')
        with self.assertRaises(ValueError):c.read_checked(self.root,self.entry)
        (self.root/'sub'/'proof.txt').unlink()
        with self.assertRaises((ValueError,FileNotFoundError)):c.read_checked(self.root,self.entry)
    def test_three_identity_fields(self):
        for field in ('bytes','sha256','git_blob'):
            bad=dict(self.entry);bad[field]=0 if field=='bytes' else '0'*len(bad[field])
            with self.assertRaises(ValueError):c.read_checked(self.root,bad)
    def test_unsafe_relative_path(self):
        for path in ('../proof','/proof','sub/../proof','sub//proof.txt'):
            bad=dict(self.entry,path=path)
            with self.assertRaises(ValueError):c.read_checked(self.root,bad)
    def test_file_and_parent_symlinks(self):
        p=self.root/'sub'/'proof.txt';p.rename(self.root/'real');p.symlink_to(self.root/'real')
        with self.assertRaises(ValueError):c.read_checked(self.root,self.entry)
        p.unlink();(self.root/'sub').rmdir();(self.root/'real').unlink()
        (self.root/'target').mkdir();(self.root/'target'/'proof.txt').write_bytes(b'proof\n')
        (self.root/'sub').symlink_to(self.root/'target',target_is_directory=True)
        with self.assertRaises(ValueError):c.read_checked(self.root,self.entry)
    def test_duplicate_json_and_source_paths(self):
        with self.assertRaises(ValueError):c.loads('{"a":1,"a":2}')
        with self.assertRaises(ValueError):c.unique_paths([self.entry,self.entry])

if __name__=='__main__':unittest.main()
