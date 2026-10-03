#!/usr/bin/env python3
"""Historical-source regressions using real isolated Git repositories.

Removing historical commit/path verification must make the current-only path
and changed historical blob tests fail. Fixture SOURCE_COMMIT values are pinned
to temporary commits; no Git subprocess or source verifier is mocked.
"""
import hashlib
import importlib.util
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location(
    "unique_replacement_check", Path(__file__).with_name("check_exact.py"))
c = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(c)


class HistoricalSourceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="c50-history-")
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name).resolve() / "repo"
        self.repo.mkdir()
        self.saved_pin = c.SOURCE_COMMIT
        self.addCleanup(setattr, c, "SOURCE_COMMIT", self.saved_pin)
        self.git("init", "--quiet")
        self.git("config", "user.name", "Source fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("config", "commit.gpgsign", "false")
        self.git("config", "core.hooksPath", str(self.repo / "no-hooks"))
        self.path = "source.md"
        self.write(b"historical source\n")
        self.commit = self.commit_all()
        c.SOURCE_COMMIT = self.commit

    def git(self, *args, repo=None):
        env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
                   GIT_TERMINAL_PROMPT="0")
        return subprocess.check_output(
            ["git", "-C", str(repo or self.repo), *args],
            env=env, stderr=subprocess.PIPE).decode().strip()

    def write(self, data, path=None):
        (self.repo / (path or self.path)).write_bytes(data)

    def commit_all(self):
        self.git("add", "-A")
        self.git("commit", "--quiet", "-m", "fixture source")
        return self.git("rev-parse", "HEAD")

    def entry(self, path=None):
        relative = path or self.path
        data = (self.repo / relative).read_bytes()
        return {"key": "P", "commit": c.SOURCE_COMMIT, "path": relative,
                "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
                "blob": hashlib.sha1(
                    b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()}

    def environment(self, **changes):
        before = {k: os.environ.get(k) for k in changes}
        os.environ.update(changes)
        def restore():
            for key, old in before.items():
                if old is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = old
        self.addCleanup(restore)

    def test_accepts_exact_historical_regular_blob(self):
        self.assertEqual(c.verify_source_entry(self.repo, self.entry()), "P")

    def test_rejects_current_only_path(self):
        self.write(b"valid current file absent from pinned commit\n", "later.md")
        self.commit_all()
        with self.assertRaises(RuntimeError):
            c.verify_source_entry(self.repo, self.entry("later.md"))

    def test_rejects_changed_historical_blob_even_with_matching_current_manifest(self):
        self.write(b"updated source with matching manifest\n")
        self.commit_all()
        with self.assertRaises(RuntimeError):
            c.verify_source_entry(self.repo, self.entry())

    def test_rejects_missing_historical_commit(self):
        c.SOURCE_COMMIT = "f" * 40
        with self.assertRaises(RuntimeError):
            c.verify_source_entry(self.repo, self.entry())

    def test_rejects_tree_object_as_source_commit(self):
        c.SOURCE_COMMIT = self.git("rev-parse", self.commit + "^{tree}")
        with self.assertRaises(RuntimeError):
            c.verify_source_entry(self.repo, self.entry())

    def test_rejects_tag_object_as_source_commit(self):
        self.git("tag", "-a", "source-tag", "-m", "fixture tag")
        c.SOURCE_COMMIT = self.git("rev-parse", "source-tag")
        with self.assertRaises(RuntimeError):
            c.verify_source_entry(self.repo, self.entry())

    def test_rejects_historical_symlink_with_matching_current_regular_bytes(self):
        (self.repo / self.path).unlink()
        (self.repo / self.path).symlink_to("target.md")
        c.SOURCE_COMMIT = self.commit_all()
        (self.repo / self.path).unlink()
        self.write(b"target.md")
        with self.assertRaises(RuntimeError):
            c.verify_source_entry(self.repo, self.entry())

    def test_commit_replacement_cannot_make_wrong_history_pass(self):
        self.write(b"replacement commit content\n")
        replacement = self.commit_all()
        self.git("replace", self.commit, replacement)
        self.environment(GIT_NO_REPLACE_OBJECTS="0")
        with self.assertRaises(RuntimeError):
            c.verify_source_entry(self.repo, self.entry())

    def test_blob_replacement_is_ignored_for_valid_history(self):
        old_blob = self.git("rev-parse", self.commit + ":" + self.path)
        self.write(b"replacement blob content\n")
        self.commit_all()
        replacement_blob = self.git("rev-parse", "HEAD:" + self.path)
        self.git("replace", old_blob, replacement_blob)
        self.write(b"historical source\n")
        self.assertEqual(c.verify_source_entry(self.repo, self.entry()), "P")

    def test_hostile_git_environment_does_not_redirect_valid_repository(self):
        self.environment(GIT_DIR=str(self.repo / "nonexistent"),
                         GIT_WORK_TREE=str(self.repo / "wrong-worktree"),
                         GIT_COMMON_DIR=str(self.repo / "wrong-common"),
                         GIT_OBJECT_DIRECTORY=str(self.repo / "wrong-objects"),
                         GIT_CONFIG_COUNT="1", GIT_CONFIG_KEY_0="core.bare",
                         GIT_CONFIG_VALUE_0="true")
        self.assertEqual(c.verify_source_entry(self.repo, self.entry()), "P")

    def test_external_git_directory_cannot_supply_missing_local_history(self):
        empty = Path(self.tmp.name).resolve() / "empty"
        empty.mkdir()
        self.git("init", "--quiet", repo=empty)
        (empty / self.path).write_bytes(b"historical source\n")
        entry = self.entry()
        self.environment(GIT_DIR=str(self.repo / ".git"),
                         GIT_WORK_TREE=str(self.repo))
        with self.assertRaises(RuntimeError):
            c.verify_source_entry(empty, entry)

    def test_parent_repository_cannot_substitute_for_requested_repository(self):
        nested = self.repo / "nested"
        nested.mkdir()
        (nested / self.path).write_bytes(b"historical source\n")
        with self.assertRaises(RuntimeError):
            c.verify_source_entry(nested, self.entry())

    def test_existing_working_file_digest_guard_remains_active(self):
        entry = self.entry()
        self.write(b"modified after manifest\n")
        with self.assertRaises(RuntimeError):
            c.verify_source_entry(self.repo, entry)


if __name__ == "__main__":
    unittest.main(verbosity=2)

