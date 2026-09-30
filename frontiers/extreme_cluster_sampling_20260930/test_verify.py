"""Real-Git custody regressions; no network and no mocked Git responses."""
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
import verify as v


def entry_for(path, data, identifier=None, commit=None):
    ans={'path':path,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),
         'git_blob':hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()}
    if identifier is not None: ans.update(id=identifier,commit=commit)
    return ans


class SourceTests(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        self.root=Path(temp.name)
        self.git('init','-q')
        self.git('config','user.name','Fixture')
        self.git('config','user.email','fixture@example.invalid')
        (self.root/'imports').mkdir()
        self.data=b'exact source fixture\n'
        (self.root/'imports/source.md').write_bytes(self.data)
        self.git('add','imports/source.md'); self.git('commit','-qm','source')
        self.commit=self.git('rev-parse','HEAD').decode().strip()
        self.entry=entry_for('imports/source.md',self.data,'fixture',self.commit)
        self.packet=self.root/'frontiers/packet'; self.packet.mkdir(parents=True)
    def git(self,*args):
        # The hostile fixture must exercise ordinary replacement behavior even
        # when the surrounding verification workflow disables replacements.
        env=os.environ.copy(); env.pop('GIT_NO_REPLACE_OBJECTS',None)
        return subprocess.run(['git',*args],cwd=self.root,env=env,check=True,
                              capture_output=True,timeout=20).stdout
    def check(self,entries=None,ids=frozenset({'fixture'})):
        if entries is None: entries=[self.entry]
        (self.packet/'SOURCES.json').write_text(json.dumps({'sources':entries}),encoding='utf-8')
        return v.verify_sources(self.packet,required_ids=ids)
    def test_valid_source_from_nested_packet(self):
        self.assertEqual(self.check(),1)
    def test_source_bytes_not_worktree(self):
        (self.root/'imports/source.md').write_bytes(b'not the historical source\n')
        self.assertEqual(self.check(),1)
    def test_all_identity_fields(self):
        for key,value in [('bytes',0),('sha256','0'*64),('git_blob','0'*40)]:
            e=copy.deepcopy(self.entry); e[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError): self.check([e])
    def test_boolean_size_rejected(self):
        e=dict(self.entry,bytes=True)
        with self.assertRaises(ValueError): self.check([e])
    def test_missing_path(self):
        with self.assertRaises(ValueError): self.check([dict(self.entry,path='missing.md')])
    def test_missing_commit(self):
        with self.assertRaises(ValueError): self.check([dict(self.entry,commit='0'*40)])
    def test_malformed_commit(self):
        for text in ('HEAD','F'*40,'0'*39,'0'*40+':path'):
            with self.subTest(text=text),self.assertRaises(ValueError):
                self.check([dict(self.entry,commit=text)])
    def test_unsafe_paths(self):
        for path in ('../source.md','/imports/source.md','imports//source.md',
                     'imports/./source.md','imports/../source.md','',
                     'imports\\source.md','imports/source.md/','x\0y'):
            with self.subTest(path=path),self.assertRaises(ValueError):
                self.check([dict(self.entry,path=path)])
    def test_empty_inventory(self):
        with self.assertRaises(ValueError): self.check([])
    def test_duplicate_ids(self):
        with self.assertRaises(ValueError): self.check([self.entry,self.entry])
    def test_duplicate_commit_path(self):
        with self.assertRaises(ValueError):
            self.check([self.entry,dict(self.entry,id='second')],{'fixture','second'})
    def test_missing_required_id(self):
        with self.assertRaises(ValueError): self.check(ids={'fixture','missing'})
    def test_unexpected_source_id(self):
        with self.assertRaises(ValueError): self.check([dict(self.entry,id='unexpected')])
    def test_noncommit_tree_and_blob(self):
        values=[self.git('rev-parse','HEAD^{tree}').decode().strip(),self.entry['git_blob']]
        for sha in values:
            with self.subTest(sha=sha),self.assertRaises(ValueError):
                self.check([dict(self.entry,commit=sha)])
    def test_annotated_tag_not_commit(self):
        self.git('tag','-a','fixture-tag','-m','tag')
        sha=self.git('rev-parse','fixture-tag').decode().strip()
        with self.assertRaises(ValueError): self.check([dict(self.entry,commit=sha)])
    def test_leaf_symlink(self):
        (self.root/'link.md').symlink_to('imports/source.md')
        self.git('add','link.md'); self.git('commit','-qm','link')
        e=entry_for('link.md',b'imports/source.md','fixture',self.git('rev-parse','HEAD').decode().strip())
        with self.assertRaises(ValueError): self.check([e])
    def test_ancestor_symlink(self):
        (self.root/'linked').symlink_to('imports',target_is_directory=True)
        self.git('add','linked'); self.git('commit','-qm','ancestor')
        e=dict(self.entry,path='linked/source.md',commit=self.git('rev-parse','HEAD').decode().strip())
        with self.assertRaises(ValueError): self.check([e])
    def replacement(self):
        changed=b'forged replacement source\n'
        (self.root/'imports/source.md').write_bytes(changed)
        self.git('add','imports/source.md'); self.git('commit','-qm','changed')
        newer=self.git('rev-parse','HEAD').decode().strip()
        self.git('replace',self.commit,newer)
        # Verify the hostile fixture actually intercepts an ordinary Git read.
        self.assertEqual(self.git('show',self.commit+':imports/source.md'),changed)
        return changed
    def test_replacement_cannot_invalidate_authentic_source(self):
        self.replacement()
        self.assertEqual(self.check(),1)
    def test_replacement_cannot_authenticate_forged_source(self):
        forged=self.replacement()
        with self.assertRaises(ValueError):
            self.check([entry_for(self.entry['path'],forged,'fixture',self.commit)])


class InventoryTests(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        self.root=Path(temp.name); self.data=b'packet file\n'
        (self.root/'README.md').write_bytes(self.data)
        self.entry=entry_for('README.md',self.data)
    def write(self,entries=None):
        if entries is None: entries=[self.entry]
        (self.root/'MANIFEST.json').write_text(json.dumps({'files':entries}))
    def test_valid(self):
        self.write(); self.assertEqual(v.verify_inventory(self.root),1)
    def test_extra_file(self):
        self.write(); (self.root/'extra').write_text('no')
        with self.assertRaises(ValueError): v.verify_inventory(self.root)
    def test_missing_file(self):
        self.write(); (self.root/'README.md').unlink()
        with self.assertRaises(ValueError): v.verify_inventory(self.root)
    def test_changed_file(self):
        self.write(); (self.root/'README.md').write_bytes(b'changed')
        with self.assertRaises(ValueError): v.verify_inventory(self.root)
    def test_duplicate_entry(self):
        self.write([self.entry,self.entry])
        with self.assertRaises(ValueError): v.verify_inventory(self.root)
    def test_empty_manifest(self):
        self.write([])
        with self.assertRaises(ValueError): v.verify_inventory(self.root)
    def test_packet_symlink(self):
        self.write(); (self.root/'README.md').unlink()
        (self.root/'README.md').symlink_to('MANIFEST.json')
        with self.assertRaises(ValueError): v.verify_inventory(self.root)
    def test_manifest_symlink(self):
        temp=tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        real=Path(temp.name)/'manifest'; real.write_text(json.dumps({'files':[self.entry]}))
        (self.root/'MANIFEST.json').symlink_to(real)
        with self.assertRaises(ValueError): v.verify_inventory(self.root)
    def test_nonflat_path(self):
        self.write([dict(self.entry,path='sub/README.md')])
        with self.assertRaises(ValueError): v.verify_inventory(self.root)
    def test_parent_symlink(self):
        self.write()
        temp=tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        link=Path(temp.name)/'packet'; link.symlink_to(self.root,target_is_directory=True)
        with self.assertRaises(ValueError): v.verify_inventory(link)
    def test_duplicate_json_key(self):
        p=self.root/'duplicate.json'; p.write_text('{"x":1,"x":2}')
        with self.assertRaises(ValueError): v.read_json(p)
    def test_invalid_json_top_type(self):
        p=self.root/'list.json'; p.write_text('[]')
        with self.assertRaises(ValueError): v.read_json(p)


if __name__=='__main__': unittest.main()
