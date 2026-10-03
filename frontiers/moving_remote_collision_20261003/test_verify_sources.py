"""Failure-case custody tests; no scientific claims or network use."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import verify_sources as v


class PacketTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(
            prefix="c107-custody-", dir=os.environ.get("C107_TEST_TMPDIR"))
        self.root = Path(self.temp.name)
        self.packet = self.root / "packet"
        self.packet.mkdir()
        for name in v.FROZEN_FILES:
            (self.packet/name).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(v.HERE/name, self.packet/name)
        if not (self.packet/"review").exists():
            shutil.copytree(v.HERE/"review", self.packet/"review")
        shutil.copytree(v.HERE/"sources", self.packet/"sources")

    def tearDown(self):
        self.temp.cleanup()

    def test_actual_packet_and_historical_sources(self):
        self.assertEqual(v.verify(self.packet, v.ROOT), 6)

    def test_proof_mutation_rejected(self):
        with (self.packet/"PROOF.md").open("ab") as f:
            f.write(b"\nchanged\n")
        with self.assertRaisesRegex(ValueError, "frozen anchor"):
            v.verify(self.packet, v.ROOT)

    def test_control_mutation_rejected(self):
        with (self.packet/"author_controls.py").open("ab") as f:
            f.write(b"\n# changed\n")
        with self.assertRaisesRegex(ValueError, "frozen anchor"):
            v.verify(self.packet, v.ROOT)

    def test_independent_control_substitution_rejected(self):
        (self.packet/"review"/"independent_controls.py").write_text(
            'print(\'{"status":"PASS","positive_evaluations":425,'
            '"rejected_mutant_evaluations":46}\')\n')
        with self.assertRaisesRegex(ValueError, "frozen anchor"):
            v.verify(self.packet, v.ROOT)

    def test_review_prose_drift_rejected(self):
        with (self.packet/"review"/"REVIEW.md").open("ab") as f:
            f.write(b"\nUnreviewed extension.\n")
        with self.assertRaisesRegex(ValueError, "frozen anchor"):
            v.verify(self.packet, v.ROOT)

    def test_review_receipt_drift_rejected(self):
        with (self.packet/"review"/"REVIEW_RECEIPT.json").open("ab") as f:
            f.write(b"\n")
        with self.assertRaisesRegex(ValueError, "frozen anchor"):
            v.verify(self.packet, v.ROOT)

    def test_snapshot_mutation_rejected(self):
        with (self.packet/"sources"/"RC.md").open("ab") as f:
            f.write(b"\nchanged\n")
        with self.assertRaisesRegex(ValueError, "source bytes mismatch"):
            v.verify(self.packet, v.ROOT)

    def test_resigned_manifest_rejected(self):
        manifest=json.loads((self.packet/"SOURCE_IDENTITIES.json").read_text())
        data=b"substituted source\n"
        (self.packet/"sources"/"RC.md").write_bytes(data)
        e=manifest["sources"]["RC"]
        e.update(bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),
                 git_blob=v.blob_id(data))
        (self.packet/"SOURCE_IDENTITIES.json").write_text(json.dumps(manifest))
        with self.assertRaisesRegex(ValueError, "frozen anchor"):
            v.verify(self.packet, v.ROOT)

    def test_missing_source_rejected(self):
        (self.packet/"sources"/"E1.md").unlink()
        with self.assertRaisesRegex(ValueError, "regular file"):
            v.verify(self.packet, v.ROOT)

    def test_symlink_leaf_rejected_even_when_bytes_match(self):
        leaf=self.packet/"sources"/"P.md"
        saved=self.root/"original.md"
        leaf.rename(saved)
        leaf.symlink_to(saved)
        with self.assertRaisesRegex(ValueError, "symlink"):
            v.verify(self.packet, v.ROOT)

    def test_symlink_ancestor_rejected(self):
        saved=self.root/"original_sources"
        (self.packet/"sources").rename(saved)
        (self.packet/"sources").symlink_to(saved,target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlink"):
            v.verify(self.packet, v.ROOT)

    def test_unsafe_paths_and_duplicate_keys_rejected(self):
        for bad in ("../P.md","/P.md","sources//P.md","sources/./P.md",
                    "sources\\P.md","sources/../P.md","x\0y"):
            with self.subTest(path=bad), self.assertRaises(ValueError):
                v.canonical(bad)
        with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
            v.unique_json(b'{"x":1,"x":2}')


class HistoricalTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(
            prefix="c107-git-",dir=os.environ.get("C107_TEST_TMPDIR"))
        self.root=Path(self.temp.name)
        self.git("init","-q")
        self.git("config","user.name","Local custody fixture")
        self.git("config","user.email","fixture@example.invalid")
        (self.root/"docs").mkdir()
        self.data=b"original fixture proof\n"
        (self.root/"docs"/"source.md").write_bytes(self.data)
        self.git("add","docs/source.md")
        self.git("commit","-qm","original fixture")
        self.cut=self.git("rev-parse","HEAD").decode().strip()
        self.entry={"source_path":"docs/source.md","bytes":len(self.data),
                    "sha256":hashlib.sha256(self.data).hexdigest(),
                    "git_blob":v.blob_id(self.data)}

    def tearDown(self):
        self.temp.cleanup()

    def git(self,*args):
        return subprocess.run(["git","-C",str(self.root),*args],
                              check=True,capture_output=True).stdout

    def changed_commit(self):
        (self.root/"docs"/"source.md").write_bytes(b"different fixture\n")
        self.git("add","docs/source.md")
        self.git("commit","-qm","changed fixture")
        return self.git("rev-parse","HEAD").decode().strip()

    def test_real_historical_binding_and_wrong_commit(self):
        v.historical(self.root,self.cut,self.entry)
        changed=self.changed_commit()
        with self.assertRaisesRegex(ValueError,"commit/path/blob mismatch"):
            v.historical(self.root,changed,self.entry)

    def test_current_source_drift_rejected(self):
        v.current_source(self.root,self.entry)
        self.changed_commit()
        with self.assertRaisesRegex(ValueError,"source bytes mismatch"):
            v.current_source(self.root,self.entry)

    def test_wrong_path_and_noncommit_rejected(self):
        e=dict(self.entry,source_path="docs/missing.md")
        with self.assertRaisesRegex(ValueError,"commit/path/blob mismatch"):
            v.historical(self.root,self.cut,e)
        with self.assertRaisesRegex(ValueError,"not a commit"):
            v.historical(self.root,self.entry["git_blob"],self.entry)
        with self.assertRaises(ValueError):
            v.historical(self.root,"0"*40,self.entry)

    def test_symlink_git_mode_rejected(self):
        path=self.root/"docs"/"source.md"
        path.unlink()
        path.symlink_to("elsewhere")
        self.git("add","docs/source.md")
        self.git("commit","-qm","symlink fixture")
        cut=self.git("rev-parse","HEAD").decode().strip()
        data=b"elsewhere"
        e=dict(self.entry,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),
               git_blob=v.blob_id(data))
        with self.assertRaisesRegex(ValueError,"commit/path/blob mismatch"):
            v.historical(self.root,cut,e)

    def test_replacement_objects_cannot_redirect_pins(self):
        changed=self.changed_commit()
        self.git("replace",self.cut,changed)
        env=dict(os.environ)
        env.pop("GIT_NO_REPLACE_OBJECTS",None)
        replaced=subprocess.run(
            ["git","-C",str(self.root),"show",self.cut+":docs/source.md"],
            check=True,capture_output=True,env=env).stdout
        self.assertNotEqual(replaced,self.data)
        # Even an explicit parent environment requesting replacement must not
        # redirect the original source commit in the verifier.
        with patch.dict(os.environ,{"GIT_NO_REPLACE_OBJECTS":"0"}):
            v.historical(self.root,self.cut,self.entry)


if __name__=="__main__":
    unittest.main()
