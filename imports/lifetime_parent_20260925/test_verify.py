"""Standard-library negative controls for lifetime-parent source custody."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from verify import EXPECTED_PATHS, verify


class LifetimeParentImportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.records = []
        for index, source in enumerate(sorted(EXPECTED_PATHS)):
            data = ("import-payload-%d" % index).encode("ascii")
            (self.root / Path(source).name).write_bytes(data)
            self.records.append({"path": source, "bytes": len(data),
                                 "sha256": hashlib.sha256(data).hexdigest()})
        self.write_manifest()

    def write_manifest(self):
        (self.root / "MANIFEST.json").write_text(
            json.dumps({"object": "SYNTHETIC-CUSTODY", "files": self.records}),
            encoding="utf-8")

    def test_exact_original_path_set_succeeds(self):
        result = verify(self.root)
        self.assertEqual(len(result["checked"]), 2)
        self.assertEqual(result["scientific_effect"], "NONE")

    def test_wrong_directory_same_basename_rejected(self):
        self.records[0]["path"] = "unrelated/" + Path(self.records[0]["path"]).name
        self.write_manifest()
        with self.assertRaisesRegex(SystemExit, "path/membership mismatch"):
            verify(self.root)

    def test_missing_member_rejected(self):
        self.records.pop()
        self.write_manifest()
        with self.assertRaisesRegex(SystemExit, "path/membership mismatch"):
            verify(self.root)

    def test_duplicate_member_rejected(self):
        self.records[1] = self.records[0].copy()
        self.write_manifest()
        with self.assertRaisesRegex(SystemExit, "path/membership mismatch"):
            verify(self.root)

    def test_extra_member_rejected(self):
        self.records.append(self.records[0].copy())
        self.write_manifest()
        with self.assertRaisesRegex(SystemExit, "path/membership mismatch"):
            verify(self.root)

    def test_byte_tampering_rejected(self):
        file = self.root / Path(self.records[0]["path"]).name
        file.write_bytes(b"altered-source-bytes")
        with self.assertRaises(SystemExit):
            verify(self.root)

    def test_digest_tampering_rejected(self):
        self.records[0]["sha256"] = "0" * 64
        self.write_manifest()
        with self.assertRaisesRegex(SystemExit, "sha256 mismatch"):
            verify(self.root)

    def test_length_tampering_rejected(self):
        self.records[0]["bytes"] += 1
        self.write_manifest()
        with self.assertRaisesRegex(SystemExit, "size mismatch"):
            verify(self.root)


if __name__ == "__main__":
    unittest.main()
