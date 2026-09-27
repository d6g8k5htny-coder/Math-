"""Source custody controls; no mathematical acceptance is inferred."""
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
PACKAGES=('bf_six_pin_scalar_20260926','bf_six_pin_hessian_20260926')

class SourceIntegrityTests(unittest.TestCase):
    def setUp(self):
        script=ROOT/'certificates/bf_source_integrity.py'
        self.assertTrue(script.is_file(),'Missing immutable source verifier')
        spec=importlib.util.spec_from_file_location('bf_integrity_subject',script)
        self.m=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.m)
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        for name in PACKAGES:shutil.copytree(ROOT/'certificates'/name,self.root/'certificates'/name)
    def test_ten_exact_files_are_verified(self):
        result=self.m.verify(self.root)
        self.assertEqual(result['source_files'],10)
        self.assertEqual(result['scientific_effect'],'NONE')
        self.assertIs(result['scientific_acceptance'],False)
    def test_changed_proof_is_refused(self):
        p=self.root/'certificates'/PACKAGES[1]/'PROOF.md';p.write_bytes(p.read_bytes()+b'\n')
        with self.assertRaises(ValueError):self.m.verify(self.root)
    def test_same_size_proof_tamper_is_refused(self):
        p=self.root/'certificates'/PACKAGES[1]/'PROOF.md';raw=p.read_bytes();p.write_bytes(b'!'+raw[1:])
        with self.assertRaises(ValueError):self.m.verify(self.root)
    def test_missing_source_is_refused(self):
        (self.root/'certificates'/PACKAGES[0]/'certificate.py').unlink()
        with self.assertRaises((ValueError,OSError)):self.m.verify(self.root)
    def test_manifest_commit_relabel_is_refused(self):
        folder=self.root/'certificates'/PACKAGES[0]
        p=folder/'SOURCE_MANIFEST.json';d=json.loads(p.read_text());d['source_commit']='1'*40;p.write_text(json.dumps(d))
        with self.assertRaises(ValueError):self.m.verify(self.root)
    def test_matching_mutated_proof_and_manifest_are_refused(self):
        folder=self.root/'certificates'/PACKAGES[0]
        source=folder/'PROOF.md';raw=source.read_bytes()+b'changed';source.write_bytes(raw)
        manifest=folder/'SOURCE_MANIFEST.json';data=json.loads(manifest.read_text())
        row=next(row for row in data['files'] if row['path']=='PROOF.md')
        row.update(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),git_blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest())
        manifest.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
        with self.assertRaises(ValueError):self.m.verify(self.root)
    def test_missing_manifest_is_not_a_skip(self):
        (self.root/'certificates'/PACKAGES[0]/'SOURCE_MANIFEST.json').unlink()
        with self.assertRaises((ValueError,OSError)):self.m.verify(self.root)
    def test_symlink_payload_is_refused(self):
        p=self.root/'certificates'/PACKAGES[0]/'PROOF.md';target=self.root/'other';p.rename(target);p.symlink_to(target)
        with self.assertRaises(ValueError):self.m.verify(self.root)
    def test_symlink_manifest_is_refused(self):
        p=self.root/'certificates'/PACKAGES[0]/'SOURCE_MANIFEST.json';target=self.root/'other';p.rename(target);p.symlink_to(target)
        with self.assertRaises(ValueError):self.m.verify(self.root)
    def test_symlink_package_is_refused(self):
        p=self.root/'certificates'/PACKAGES[0];target=self.root/'other';p.rename(target);p.symlink_to(target,target_is_directory=True)
        with self.assertRaises(ValueError):self.m.verify(self.root)
    def test_symlink_certificates_root_is_refused(self):
        p=self.root/'certificates';target=self.root/'other';p.rename(target);p.symlink_to(target,target_is_directory=True)
        with self.assertRaises(ValueError):self.m.verify(self.root)
    def test_symlink_verification_root_is_refused(self):
        p=self.root/'root_link';p.symlink_to(self.root,target_is_directory=True)
        with self.assertRaises(ValueError):self.m.verify(p)
    def test_cli_requires_no_network_and_is_mode_identical(self):
        outputs=[]
        for flags in ([],['-O']):
            r=subprocess.run([sys.executable,*flags,'-B','-S',str(ROOT/'certificates/bf_source_integrity.py'),'--root',str(self.root)],capture_output=True,text=True,timeout=10)
            self.assertEqual(r.returncode,0,r.stderr);outputs.append(r.stdout)
        self.assertEqual(*outputs);self.assertEqual(json.loads(outputs[0])['source_files'],10)
if __name__=='__main__':unittest.main()
