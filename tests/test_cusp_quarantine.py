"""One-packet A3 quarantine boundary controls; no arithmetic certification."""
from __future__ import annotations

import json
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools/check_cusp_quarantine.py"
PACKET = "frontiers/cusp_coefficient_certified_20261001"
RECORD = "quarantine/Q-CUSP-BINARY64-20261029.json"
QID = "Q-CUSP-BINARY64-20261029"


class CuspQuarantine(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="cusp-quarantine-")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        shutil.copytree(ROOT / PACKET, self.root / PACKET)
        (self.root / "PROOF_INDEX.md").write_bytes((ROOT / "PROOF_INDEX.md").read_bytes())
        target = self.root / RECORD
        target.parent.mkdir(parents=True)
        if (ROOT / RECORD).is_file():
            target.write_bytes((ROOT / RECORD).read_bytes())

    def cli(self, *args):
        flags = ["-B", "-S"] + ["-O"] * sys.flags.optimize
        env = {key: value for key, value in os.environ.items()
               if key not in {"PYTHONHOME", "PYTHONPATH", "PYTHONOPTIMIZE"}}
        return subprocess.run(
            [sys.executable, *flags, str(SCRIPT), "--root", str(self.root), *args],
            cwd=self.root, env=env, capture_output=True, text=True, timeout=10,
            check=False,
        )

    def report(self, result):
        self.assertTrue(result.stdout.startswith("{"), result)
        self.assertEqual(result.stderr, "", result)
        return json.loads(result.stdout)

    def change_record(self, callback):
        path = self.root / RECORD
        doc = json.loads(path.read_text()) if path.is_file() else {}
        callback(doc)
        path.write_text(json.dumps(doc, indent=2) + "\n")

    def refused(self, diagnostic, *args):
        result = self.cli(*args)
        self.assertEqual(result.returncode, 1, result)
        doc = self.report(result)
        self.assertFalse(doc["cbz_certificate_admitted"])
        self.assertTrue(any(diagnostic in item for item in doc["problems"]), doc)

    def test_record_integrity_never_certifies_arithmetic(self):
        result = self.cli()
        self.assertEqual(result.returncode, 0, result)
        doc = self.report(result)
        self.assertEqual(doc["status"], "QUARANTINE_INTEGRITY_OK")
        self.assertEqual(doc["layer_a_status"], "A3_NOT_PROVEN")
        self.assertFalse(doc["cbz_certificate_admitted"])
        self.assertEqual(doc["preserved_packet_files"], 16)

    def test_packet_cannot_be_consumed_as_cbz_certificate(self):
        self.refused("quarantined numerical source", "--consume", PACKET + "/certificate.py")

    def test_normalized_packet_alias_cannot_evade_denial(self):
        for path in ("./" + PACKET + "/RESULTS.json",
                     "frontiers/unused/../cusp_coefficient_certified_20261001/ia.py"):
            with self.subTest(path=path):
                self.refused("quarantined numerical source", "--consume", path)

    def test_inherited_absolute_intervals_cannot_be_consumed(self):
        self.refused(
            "quarantined numerical source", "--consume",
            "frontiers/cusp_torus_transfer_20261001/RESULTS.json",
        )

    def test_renamed_packet_copy_cannot_evade_denial(self):
        path = self.root / "mirror/replay.py"
        path.parent.mkdir()
        path.write_bytes((self.root / PACKET / "certificate.py").read_bytes())
        self.refused("quarantined numerical source", "--consume", "mirror/replay.py")

    def test_unrelated_source_is_not_silently_certified(self):
        result = self.cli("--consume", "formal/Basic.lean")
        self.assertEqual(result.returncode, 2, result)
        doc = self.report(result)
        self.assertEqual(doc["status"], "NOT_COVERED")
        self.assertFalse(doc["cbz_certificate_admitted"])

    def test_missing_record_and_empty_source_inventory_fail_closed(self):
        path = self.root / RECORD
        if path.is_file():
            path.unlink()
        self.refused("missing quarantine record")

    def test_empty_packet_source_inventory_cannot_pass(self):
        self.change_record(lambda doc: doc.update(source_files=[]))
        self.refused("exact packet inventory")

    def test_record_cannot_admit_certificate_or_drop_denials(self):
        self.change_record(lambda doc: doc.update(cbz_certificate_admitted=True))
        self.refused("certificate admission must remain false")
        self.change_record(lambda doc: doc.update(cbz_certificate_admitted=False,
                                                  denied_certificate_sources=[]))
        self.refused("denied source inventory")

    def test_owner_and_maintenance_are_explicit(self):
        self.change_record(lambda doc: doc.update(owner="invented owner", maintenance=1))
        self.refused("owner must remain unassigned")
        self.change_record(lambda doc: doc.update(owner=None))
        self.refused("maintenance must remain zero")

    def test_packet_bytes_and_tree_are_preserved(self):
        path = self.root / PACKET / "ia.py"
        path.write_bytes(path.read_bytes() + b"\n# changed\n")
        self.refused("packet source identity mismatch")
        path = self.root / PACKET / "extra.py"
        path.write_text("pass\n")
        self.refused("packet tree differs")

    def test_manifest_cannot_rebind_itself_to_modified_packet(self):
        changed = self.root / PACKET / "ia.py"
        changed.write_bytes(changed.read_bytes() + b"\n# altered arithmetic\n")
        def identity(path):
            raw = path.read_bytes()
            return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(),
                    "git_blob": hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()}
        path = self.root / PACKET / "SOURCE_FILES.json"
        manifest = json.loads(path.read_text())
        for row in manifest["files"]:
            if row["path"] == "ia.py":
                row.update(identity(changed))
        path.write_text(json.dumps(manifest) + "\n")
        def rebind_record(doc):
            for row in doc["source_files"]:
                if row["path"] in (PACKET + "/ia.py", PACKET + "/SOURCE_FILES.json"):
                    row.update(identity(self.root / row["path"]))
            doc["source_snapshot"]["manifest"].update(identity(path))
        self.change_record(rebind_record)
        self.refused("frozen packet manifest identity")

    def test_index_must_explicitly_classify_the_quarantine(self):
        (self.root / "PROOF_INDEX.md").write_text("# historical index without classification\n")
        self.refused("canonical index quarantine")

    def test_index_denial_must_be_boolean_false(self):
        path = self.root / "PROOF_INDEX.md"
        path.write_text(path.read_text().replace('"cbz_certificate_admitted":false',
                                                 '"cbz_certificate_admitted":0'))
        self.refused("canonical index quarantine")

    def test_source_byte_count_must_remain_an_exact_integer(self):
        self.change_record(lambda doc: doc["source_files"][0].update(
            bytes=float(doc["source_files"][0]["bytes"])))
        self.refused("exact packet inventory")

    def test_snapshot_manifest_identity_cannot_disagree_with_frozen_source(self):
        self.change_record(lambda doc: doc["source_snapshot"]["manifest"].update(git_blob="0" * 40))
        self.refused("snapshot manifest identity")

    def test_duplicate_record_members_fail_before_overwrite(self):
        path = self.root / RECORD
        raw = path.read_text() if path.is_file() else "{}"
        raw = raw.rstrip().removesuffix("}") + ',"cbz_certificate_admitted":true,"cbz_certificate_admitted":false}'
        path.write_text(raw)
        self.refused("duplicate JSON member")

    def test_empty_or_escaping_consumer_paths_do_not_pass(self):
        for path in ("", "../outside.py", "/tmp/certificate.py"):
            with self.subTest(path=path):
                self.refused("unsafe consumer path", "--consume", path)


if __name__ == "__main__":
    unittest.main()
