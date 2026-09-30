"""Real isolated Git fixtures for the source/inventory verifier. No network."""
import copy
import hashlib
import json
from pathlib import Path
import shutil
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

    def changed_commit(self):
        (self.repo/'a.md').write_text('different historical source\n',encoding='utf-8')
        self.git('add','a.md')
        self.git('-c','user.name=Fixture','-c','user.email=fixture@example.invalid',
                 'commit','-qm','changed historical source')
        return self.git('rev-parse','HEAD').decode().strip()

    def accepts(self,entry):
        try:
            v.verify_source_entry(self.packet,entry)
        except (ValueError,subprocess.CalledProcessError):
            return False
        return True

    def test_replacement_cannot_forge_commit_binding(self):
        changed=self.changed_commit()
        entry=copy.deepcopy(self.entries[0]);entry['commit']=changed
        self.assertFalse(self.accepts(entry))
        self.git('replace',changed,self.commit)
        self.assertFalse(self.accepts(entry),'replacement ref forged historical source binding')

    def test_valid_original_ignores_replacement(self):
        changed=self.changed_commit()
        self.git('replace',self.commit,changed)
        self.assertTrue(self.accepts(self.entries[0]),'original immutable object was replaced')

    def test_tree_sha_is_not_a_commit(self):
        entry=copy.deepcopy(self.entries[0])
        entry['commit']=self.git('rev-parse',self.commit+'^{tree}').decode().strip()
        self.assertFalse(self.accepts(entry),'tree identity accepted as a commit')

    def test_annotated_tag_sha_is_not_a_commit(self):
        self.git('-c','user.name=Fixture','-c','user.email=fixture@example.invalid',
                 'tag','-a','fixture-tag','-m','tag fixture',self.commit)
        entry=copy.deepcopy(self.entries[0])
        entry['commit']=self.git('rev-parse','fixture-tag').decode().strip()
        self.assertFalse(self.accepts(entry),'tag identity accepted as a commit')

    def inventory_fixture(self):
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup)
        root=Path(temp.name)
        for path in Path(v.__file__).parent.iterdir():
            if path.is_file():shutil.copyfile(path,root/path.name)
        data=b'packet fixture\n'
        (root/'note.md').write_bytes(data)
        entry=self.fingerprint('note.md',data)
        entries=[self.fingerprint(p.name,p.read_bytes()) for p in sorted(root.iterdir())
                 if p.name!='MANIFEST.json']
        (root/'MANIFEST.json').write_text(json.dumps({'files':entries}))
        return root,entry

    def test_valid_packet(self):
        root,entry=self.inventory_fixture()
        self.assertEqual(v.verify_inventory(root),len(list(root.iterdir()))-1)

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


class PacketReviewBindingTests(unittest.TestCase):
    """Re-signing the inventory must not transfer an old review to new prose."""
    def setUp(self):
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup)
        self.root=Path(temp.name)
        for path in Path(v.__file__).parent.iterdir():
            if path.is_file():shutil.copyfile(path,self.root/path.name)
        self.resign()

    def resign(self):
        entries=[CustodyTests.fingerprint(p.name,p.read_bytes())
                 for p in sorted(self.root.iterdir()) if p.name!='MANIFEST.json']
        (self.root/'MANIFEST.json').write_text(json.dumps({'files':entries}))

    def test_current_reviewed_packet(self):
        self.assertEqual(v.verify_inventory(self.root),len(list(self.root.iterdir()))-1)

    def test_resigned_manuscript_change(self):
        for name in ('TWO_SCALE_LAW.md','RADIAL_TAIL.md'):
            with self.subTest(path=name):
                path=self.root/name;original=path.read_bytes()
                path.write_bytes(original+b'\nUnreviewed replacement conclusion.\n')
                self.resign()
                with self.assertRaises(ValueError):v.verify_inventory(self.root)
                path.write_bytes(original)

    def test_resigned_required_leaf_removal(self):
        for name in ('TWO_SCALE_LAW.md','RADIAL_TAIL.md','SOURCES.json',
                     'RESULTS.json','REVIEW_RECORD.md','REVIEW_RECORD.json',
                     'geometry.py','verify.py','test_geometry.py','test_custody.py'):
            with self.subTest(path=name):
                path=self.root/name;original=path.read_bytes();path.unlink()
                self.resign()
                with self.assertRaises(ValueError):v.verify_inventory(self.root)
                path.write_bytes(original)

    def test_resigned_source_declaration_change(self):
        path=self.root/'SOURCES.json'
        data=json.loads(path.read_text());data['sources'][0]['commit']='0'*40
        path.write_text(json.dumps(data));self.resign()
        with self.assertRaises(ValueError):v.verify_inventory(self.root)

    def record(self):
        return json.loads((self.root/'REVIEW_RECORD.json').read_text())

    def write_record(self,record):
        (self.root/'REVIEW_RECORD.json').write_text(json.dumps(record));self.resign()

    def test_resigned_proof_and_review_coedit(self):
        record=self.record()
        for name in ('TWO_SCALE_LAW.md','RADIAL_TAIL.md'):
            with self.subTest(path=name):
                path=self.root/name;original=path.read_bytes()
                path.write_bytes(original+b'\nUnreviewed replacement conclusion.\n')
                changed=copy.deepcopy(record)
                for i,proof in enumerate(changed['proofs']):
                    if proof['path']==name:
                        changed['proofs'][i]=CustodyTests.fingerprint(name,path.read_bytes())
                self.write_record(changed)
                with self.assertRaises(ValueError):v.verify_inventory(self.root)
                path.write_bytes(original)

    def test_missing_duplicate_or_swapped_reviews(self):
        original=self.record()
        records=[]
        missing=copy.deepcopy(original);missing['reviews'].pop();records.append(missing)
        duplicate=copy.deepcopy(original);duplicate['reviews'][1]=duplicate['reviews'][0]
        records.append(duplicate)
        swapped=copy.deepcopy(original)
        swapped['reviews'][0]['proof_path']='RADIAL_TAIL.md';records.append(swapped)
        for record in records:
            with self.subTest(reviews=record['reviews']):
                self.write_record(record)
                with self.assertRaises(ValueError):v.verify_inventory(self.root)

    def test_stale_commit_id_or_body_binding(self):
        original=self.record()
        for field,value in (('reviewed_commit','0'*40),('native_review_id',5360227992),
                            ('body_sha256','0'*64),('body_bytes',7841),
                            ('native_state','APPROVED')):
            with self.subTest(field=field):
                record=copy.deepcopy(original);record['reviews'][0][field]=value
                self.write_record(record)
                with self.assertRaises(ValueError):v.verify_inventory(self.root)

    def test_no_inferred_authentication_or_independence(self):
        original=self.record()
        for field in ('remote_review_authenticity_checked','mathematical_acceptance'):
            with self.subTest(field=field):
                record=copy.deepcopy(original);record[field]=True;self.write_record(record)
                with self.assertRaises(ValueError):v.verify_inventory(self.root)
        record=copy.deepcopy(original);record['exposure']['organizational_independence_credit']=1
        self.write_record(record)
        with self.assertRaises(ValueError):v.verify_inventory(self.root)

    def test_duplicate_json_or_wrong_identity_type(self):
        original=self.record()
        for value in (True,'17139',None):
            with self.subTest(value=value):
                record=copy.deepcopy(original);record['proofs'][0]['bytes']=value
                self.write_record(record)
                with self.assertRaises(ValueError):v.verify_inventory(self.root)
        path=self.root/'REVIEW_RECORD.json'
        path.write_text('{"schema":"forged","schema":"math166-scoped-review-binding-v1"}')
        self.resign()
        with self.assertRaises(ValueError):v.verify_inventory(self.root)


if __name__=='__main__':unittest.main()
