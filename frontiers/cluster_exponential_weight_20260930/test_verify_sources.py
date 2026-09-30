"""Hostile custody controls in synthetic Git trees; no Gaussian claim is tested."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from verify_sources import no_duplicates, verify


class SourceCustodyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        entries, sources = [], []
        for label in ("MF", "SC"):
            data = ("Synthetic " + label + " custody fixture\n").encode()
            blob = self.git("hash-object", "-w", "--stdin", data=data).decode().strip()
            name = "parent/" + label + ".md"
            entries.append("100644 blob " + blob + "\t" + name + "\n")
            sources.append({"id": label, "path": name, "git_blob": blob,
                            "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)})
        sub = self.git("mktree", data="".join(e.replace("parent/", "") for e in entries).encode()).decode().strip()
        tree = self.git("mktree", data=("040000 tree " + sub + "\tparent\n").encode()).decode().strip()
        commit = self.git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                          "commit-tree", tree, data=b"Synthetic fixture\n").decode().strip()
        for source in sources:
            source["commit"] = commit
        self.manifest = {"schema": 1, "scientific_effect": "NONE", "sources": sources}

    def tearDown(self):
        self.temp.cleanup()

    def git(self, *args, data=None):
        return subprocess.run(["git", "-C", str(self.root), *args], input=data,
                              check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout

    def test_valid_historical_trees(self):
        self.assertEqual(len(verify(self.root, self.manifest)["historical_sources_verified"]), 2)

    def test_nested_caller_has_full_tree_semantics(self):
        nested = self.root / "frontiers" / "new-packet"
        nested.mkdir(parents=True)
        self.assertEqual(verify(nested, self.manifest), verify(self.root, self.manifest))

    def test_wrong_path_even_with_correct_blob(self):
        bad = copy.deepcopy(self.manifest)
        bad["sources"][0]["path"] = "MF.md"
        with self.assertRaises(ValueError):
            verify(self.root, bad)

    def test_wrong_digest_or_size(self):
        for key, wrong in (("sha256", "0" * 64), ("bytes", 1)):
            bad = copy.deepcopy(self.manifest)
            bad["sources"][0][key] = wrong
            with self.assertRaises(ValueError):
                verify(self.root, bad)

    def test_wrong_blob_in_real_commit(self):
        bad = copy.deepcopy(self.manifest)
        bad["sources"][0]["git_blob"] = bad["sources"][1]["git_blob"]
        with self.assertRaises(ValueError):
            verify(self.root, bad)

    def test_absent_commit_fails(self):
        bad = copy.deepcopy(self.manifest)
        bad["sources"][0]["commit"] = "0" * 40
        with self.assertRaises(subprocess.CalledProcessError):
            verify(self.root, bad)

    def test_tree_must_not_pass_as_commit(self):
        bad = copy.deepcopy(self.manifest)
        tree = self.git("rev-parse", bad["sources"][0]["commit"] + "^{tree}").decode().strip()
        for source in bad["sources"]:
            source["commit"] = tree
        with self.assertRaises(ValueError):
            verify(self.root, bad)

    def test_local_replace_cannot_substitute_historical_commit(self):
        empty_tree = self.git("mktree", data=b"").decode().strip()
        empty_commit = self.git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                                "commit-tree", empty_tree, data=b"No source paths\n").decode().strip()
        self.git("replace", empty_commit, self.manifest["sources"][0]["commit"])
        bad = copy.deepcopy(self.manifest)
        for source in bad["sources"]:
            source["commit"] = empty_commit
        with self.assertRaises(ValueError):
            verify(self.root, bad)

    def test_boolean_schema_rejected(self):
        bad = copy.deepcopy(self.manifest)
        bad["schema"] = True
        with self.assertRaises(ValueError):
            verify(self.root, bad)

    def test_unsafe_path_fails(self):
        for name in ("../parent/MF.md", "/parent/MF.md", "parent//MF.md"):
            bad = copy.deepcopy(self.manifest)
            bad["sources"][0]["path"] = name
            with self.assertRaises(ValueError):
                verify(self.root, bad)

    def test_duplicate_json_keys_fail(self):
        with self.assertRaises(ValueError):
            json.loads('{"schema":1,"schema":2}', object_pairs_hook=no_duplicates)


if __name__ == "__main__":
    unittest.main()
