"""Real-Git source-custody contracts for the determinant gate."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

REPOSITORY = Path(__file__).resolve().parents[3]
DRIVER = REPOSITORY / "frontiers/determinant_moment_20261025/gate.py"

def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], stderr=subprocess.STDOUT, text=True).strip()

def digest(data):
    return hashlib.sha256(data).hexdigest()

class SourceCustody(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.repo = Path(tmp.name)
        git(self.repo, "init", "-q")
        git(self.repo, "config", "user.name", "CBZ test")
        git(self.repo, "config", "user.email", "test@example.invalid")
        self.root = self.repo / "frontiers" / "determinant"
        self.root.mkdir(parents=True)
        self.driver = self.root / "gate.py"
        self.driver.write_bytes(DRIVER.read_bytes())
        self.proof = self.root / "Claim.lean"
        self.proof.write_text("theorem claim : True := by trivial\n")
        self.manifest = self.root / "manifest.json"
        self._write_manifest()
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-qm", "initial")
        self.initial_head = git(self.repo, "rev-parse", "HEAD")
        spec = importlib.util.spec_from_file_location("determinant_custody_test_driver", self.driver)
        self.gate = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.gate)

    def _write_manifest(self):
        self.m = {"files": {"Claim.lean": digest(self.proof.read_bytes()), "gate.py": digest(self.driver.read_bytes())}}
        self.manifest.write_text(json.dumps(self.m, sort_keys=True) + "\n")

    def call_guard(self, expected_head=None):
        guard = getattr(self.gate, "source_custody", None)
        self.assertTrue(callable(guard), "source_custody guard is missing")
        return guard(self.m, digest(self.manifest.read_bytes()), expected_head=expected_head)

    def test_clean_committed_source_is_admitted(self):
        self.assertEqual(self.call_guard(expected_head=self.initial_head), self.initial_head)

    def test_dirty_refreshed_manifest_is_rejected(self):
        self.proof.write_text("theorem claim : True := by exact True.intro\n")
        self._write_manifest()
        with self.assertRaisesRegex(ValueError, "source|manifest|working"):
            self.call_guard(expected_head=self.initial_head)

    def test_staged_change_is_rejected(self):
        self.proof.write_text("theorem claim : True := by exact True.intro\n")
        self._write_manifest()
        git(self.repo, "add", ".")
        with self.assertRaisesRegex(ValueError, "index|source|manifest"):
            self.call_guard(expected_head=self.initial_head)

    def test_assume_unchanged_cannot_hide_source_bytes(self):
        git(self.repo, "update-index", "--assume-unchanged", str(self.proof.relative_to(self.repo)))
        self.proof.write_text("different\n")
        self.assertEqual(git(self.repo, "status", "--porcelain"), "")
        with self.assertRaisesRegex(ValueError, "source|working"):
            self.call_guard(expected_head=self.initial_head)

    def test_skip_worktree_cannot_hide_source_bytes(self):
        git(self.repo, "update-index", "--skip-worktree", str(self.proof.relative_to(self.repo)))
        self.proof.write_text("different\n")
        self.assertEqual(git(self.repo, "status", "--porcelain"), "")
        with self.assertRaisesRegex(ValueError, "source|working"):
            self.call_guard(expected_head=self.initial_head)

    def test_head_drift_is_rejected(self):
        (self.repo / "change.txt").write_text("change\n")
        git(self.repo, "add", "change.txt")
        git(self.repo, "commit", "-qm", "new head")
        with self.assertRaisesRegex(ValueError, "HEAD|head|commit"):
            self.call_guard(expected_head=self.initial_head)

    def test_loaded_driver_substitution_is_rejected(self):
        self.driver.write_bytes(self.driver.read_bytes() + b"\n# replacement\n")
        self._write_manifest()
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-qm", "replace loaded driver")
        new_head = git(self.repo, "rev-parse", "HEAD")
        with self.assertRaisesRegex(ValueError, "driver|loaded|identity"):
            self.call_guard(expected_head=new_head)


    def test_ambient_git_environment_cannot_redirect_the_checked_commit(self):
        from unittest import mock
        foreign = self.repo.parent / (self.repo.name + '-foreign')
        foreign.mkdir()
        self.addCleanup(lambda: __import__('shutil').rmtree(foreign, ignore_errors=True))
        git(foreign, 'init', '-q')
        git(foreign, 'config', 'user.name', 'foreign fixture')
        git(foreign, 'config', 'user.email', 'fixture@example.invalid')
        (foreign / 'foreign.txt').write_text('foreign\n')
        git(foreign, 'add', '.')
        git(foreign, 'commit', '-qm', 'foreign')
        with mock.patch.dict(os.environ, {'GIT_DIR': str(foreign / '.git'),
                                         'GIT_WORK_TREE': str(foreign)}):
            self.assertEqual(self.call_guard(expected_head=self.initial_head), self.initial_head)

    def test_replace_refs_cannot_relabel_the_committed_source(self):
        self.proof.write_text('replacement\n')
        self._write_manifest()
        git(self.repo, 'add', '.')
        git(self.repo, 'commit', '-qm', 'replacement')
        other = git(self.repo, 'rev-parse', 'HEAD')
        git(self.repo, 'checkout', '-q', '--detach', self.initial_head)
        git(self.repo, 'replace', self.initial_head, other)
        self.m = json.loads(self.manifest.read_text())
        self.assertEqual(self.call_guard(expected_head=self.initial_head), self.initial_head)

    def test_inherited_lean_search_paths_are_not_sent_to_execution(self):
        import sys
        from unittest import mock
        out = self.repo / 'logs'
        out.mkdir()
        code = ("import os,json;print(json.dumps({k:os.environ.get(k) "
                "for k in ('LEAN_PATH','LEAN_SRC_PATH')}))")
        with mock.patch.dict(os.environ, {'LEAN_PATH': '/outside/lean',
                                         'LEAN_SRC_PATH': '/outside/source'}):
            result = self.gate.run([sys.executable, '-c', code], 'environment', out)
        self.assertEqual(json.loads(result), {'LEAN_PATH': None, 'LEAN_SRC_PATH': None})

    def test_owned_symlink_source_is_rejected(self):
        data = self.proof.read_bytes()
        self.proof.unlink()
        outside = self.repo / 'other.lean'
        outside.write_bytes(data)
        self.proof.symlink_to(outside)
        with self.assertRaisesRegex(ValueError, 'symlink|source'):
            self.call_guard(expected_head=self.initial_head)



    def test_nested_build_symlinks_are_rejected_before_admission(self):
        from unittest import mock
        build = self.root / '.lake' / 'build'
        external = self.repo / 'external-build'
        external.mkdir()
        calls = []
        def fake_run(command, label, out, expect_success=True):
            calls.append(label)
            if label not in ('version-preflight', 'build'):
                self.fail('unsafe build directory reached ' + label)
            if label == 'build':
                build.mkdir(parents=True)
                (build / 'nested').symlink_to(external, target_is_directory=True)
            return 'fixture version'
        with mock.patch.object(self.gate, 'source_custody', return_value=self.initial_head), \
             mock.patch.object(self.gate, 'compiled_contract', return_value=({}, {})), \
             mock.patch.object(self.gate, 'check_lean_version', return_value='fixture'), \
             mock.patch.object(self.gate, 'dependency_state', return_value={}), \
             mock.patch.object(self.gate, 'run', side_effect=fake_run):
            with self.assertRaisesRegex(ValueError, 'symlink|build'):
                self.gate.execute(self.m, digest(self.manifest.read_bytes()))
        self.assertEqual(calls, ['version-preflight', 'build'])
        self.assertFalse((self.root / '.lake/formal-evidence/receipt.json').exists())



    def test_staged_only_change_is_rejected_when_working_bytes_are_original(self):
        original = self.proof.read_bytes()
        self.proof.write_bytes(original + b'-- staged only\n')
        git(self.repo, 'add', str(self.proof.relative_to(self.repo)))
        self.proof.write_bytes(original)
        with self.assertRaisesRegex(ValueError, 'index|source'):
            self.call_guard(expected_head=self.initial_head)

    def test_refreshed_external_admission_helper_is_rejected(self):
        helper = self.repo / 'tools' / 'lean_packet_admission.py'
        helper.parent.mkdir()
        helper.write_text('# original helper\n')
        self.m['source_admission'] = {'helper_sha256': digest(helper.read_bytes())}
        self.manifest.write_text(json.dumps(self.m, sort_keys=True) + '\n')
        git(self.repo, 'add', '.')
        git(self.repo, 'commit', '-qm', 'bind helper')
        head = git(self.repo, 'rev-parse', 'HEAD')
        helper.write_text('# altered helper\n')
        self.m['source_admission']['helper_sha256'] = digest(helper.read_bytes())
        self.manifest.write_text(json.dumps(self.m, sort_keys=True) + '\n')
        with self.assertRaisesRegex(ValueError, 'source|manifest|working'):
            self.call_guard(expected_head=head)



    def test_log_symlink_is_refused_without_overwriting_its_target(self):
        import sys
        out = self.root / '.lake/formal-evidence'
        out.mkdir(parents=True)
        victim = self.repo / 'preserved.txt'
        victim.write_text('original\n')
        (out / 'probe.log').symlink_to(victim)
        with self.assertRaisesRegex(ValueError, 'symlink|evidence'):
            self.gate.run([sys.executable, '-c', "print('overwritten')"], 'probe', out)
        self.assertEqual(victim.read_text(), 'original\n')

    def test_generated_audit_symlink_is_refused_before_overwrite(self):
        from unittest import mock
        out = self.root / '.lake/formal-evidence'
        out.mkdir(parents=True)
        victim = self.repo / 'preserved.txt'
        victim.write_text('original\n')
        (out / 'Audit.lean').symlink_to(victim)
        calls = []
        def fake_run(command, label, output, expect_success=True):
            calls.append(label)
            if label == 'build':
                (self.root / '.lake/build').mkdir(parents=True)
            if label not in ('version-preflight', 'build', 'leanchecker'):
                self.fail('unsafe audit file reached ' + label)
            return 'fixture version'
        with mock.patch.object(self.gate, 'source_custody', return_value=self.initial_head), \
             mock.patch.object(self.gate, 'compiled_contract', return_value=({}, {})), \
             mock.patch.object(self.gate, 'check_lean_version', return_value='fixture'), \
             mock.patch.object(self.gate, 'dependency_state', return_value={} ), \
             mock.patch.object(self.gate, 'run', side_effect=fake_run):
            with self.assertRaisesRegex(ValueError, 'symlink|evidence'):
                self.gate.execute(self.m, digest(self.manifest.read_bytes()))
        self.assertEqual(victim.read_text(), 'original\n')



    def test_mutation_grader_rejects_wrong_exit_even_with_forged_failure_text(self):
        from unittest import mock
        runner_path = DRIVER.parent / 'tests/run_cbz_mutations.py'
        spec = importlib.util.spec_from_file_location('determinant_mutation_runner_fixture', runner_path)
        runner = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(runner)
        case = next(row for row in runner.CASES if row[0] == 'omit-artifact-log-hash')
        work = self.repo / 'mutant-work'
        output = self.repo / 'mutant-output'
        work.mkdir()
        output.mkdir()
        target = 'test_corrupt_payload_refused'
        baseline = subprocess.CompletedProcess([], 0, stdout='', stderr='Ran 1 test in 0.001s\n\nOK\n')
        counterfeit = subprocess.CompletedProcess([], 2, stdout='', stderr=(
            'FAIL: ' + target + ' (fixture)\n'
            'Ran 1 test in 0.001s\n\nFAILED (failures=1)\n'))
        with mock.patch.object(runner.subprocess, 'run', side_effect=[baseline, counterfeit]):
            result = runner.execute_case(case, work, output)
        self.assertFalse(result['killed_by_intended_assertions'])


class DependencyCustody(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        dep = self.root / ".lake" / "packages" / "dep"
        dep.mkdir(parents=True)
        git(dep, "init", "-q")
        git(dep, "config", "user.name", "CBZ test")
        git(dep, "config", "user.email", "test@example.invalid")
        (dep / ".gitignore").write_text("*.lean\n")
        (dep / "A.lean").write_text("theorem a : True := by trivial\n")
        git(dep, "add", "-f", "A.lean")
        git(dep, "add", ".gitignore")
        git(dep, "commit", "-qm", "dependency")
        self.dep = dep
        self.m = {"dependency_revisions": {"dep": git(dep, "rev-parse", "HEAD")}}
        spec = importlib.util.spec_from_file_location("dependency_custody_test_driver", DRIVER)
        self.gate = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.gate)
        self.gate.ROOT = self.root

    def test_clean_dependency_is_admitted(self):
        self.assertEqual(self.gate.dependency_state(self.m), self.m["dependency_revisions"])

    def test_assume_unchanged_dependency_source_is_rejected(self):
        git(self.dep, "update-index", "--assume-unchanged", "A.lean")
        (self.dep / "A.lean").write_text("different\n")
        self.assertEqual(git(self.dep, "status", "--porcelain"), "")
        with self.assertRaisesRegex(ValueError, "dependency.*(source|tracked|working)"):
            self.gate.dependency_state(self.m)

    def test_skip_worktree_dependency_source_is_rejected(self):
        git(self.dep, "update-index", "--skip-worktree", "A.lean")
        (self.dep / "A.lean").write_text("different\n")
        self.assertEqual(git(self.dep, "status", "--porcelain"), "")
        with self.assertRaisesRegex(ValueError, "dependency.*(source|tracked|working)"):
            self.gate.dependency_state(self.m)

    def test_ignored_untracked_lean_source_is_rejected(self):
        (self.dep / "Hidden.lean").write_text("axiom hidden : False\n")
        self.assertEqual(git(self.dep, "status", "--porcelain"), "")
        with self.assertRaisesRegex(ValueError, "dependency.*(Lean|source|untracked)"):
            self.gate.dependency_state(self.m)

if __name__ == "__main__":
    unittest.main()
