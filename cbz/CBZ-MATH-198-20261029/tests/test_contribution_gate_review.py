"""Independent real-child controls for gate preflight and bounded process trees."""
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
import unittest


TOOL = Path(__file__).resolve().parents[1] / "tools/contribution_gate.py"


class ContributionGateReviewTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        spec = importlib.util.spec_from_file_location("cbz_contribution_gate_review", TOOL)
        self.gate = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.gate)

    def job(self, name, script, *args, **extra):
        return {"id": name, "argv": [sys.executable, "-B", "-c", script, *map(str, args)],
                "cwd": str(self.root), **extra}

    def live(self, pid):
        try:
            status = Path(f"/proc/{pid}/stat").read_text()
        except FileNotFoundError:
            return False
        return status.rsplit(")", 1)[1].split()[0] not in ("Z", "X")

    def cleanup_group(self, pid):
        if pid is None:
            return
        try:
            os.killpg(pid, signal.SIGKILL)
        except ProcessLookupError:
            pass

    def test_preexisting_source_drift_cannot_be_repaired_by_the_first_child(self):
        source = self.root / "source.py"
        source.write_bytes(b"original source\n")
        frozen = {str(source): hashlib.sha256(source.read_bytes()).hexdigest()}
        source.write_bytes(b"drift before campaign\n")
        marker = self.root / "child-ran"
        job = self.job("repair", "from pathlib import Path; import sys; "
                       "Path(sys.argv[1]).write_bytes(b'original source\\n'); "
                       "Path(sys.argv[2]).write_text('ran')", source, marker)
        result = None
        try:
            result = self.gate.execute_jobs([job], self.root / "campaign", frozen)
        except ValueError:
            pass
        self.assertFalse(marker.exists(), "a child executed against an already drifted input")
        self.assertEqual(source.read_bytes(), b"drift before campaign\n")
        if result is not None:
            self.assertEqual(result["status"], "FAILED")
            self.assertEqual(result["failure"], "SOURCE_DRIFT")

    def test_entire_job_plan_is_validated_before_any_child_launch(self):
        invalid = (
            ("empty-argv", {"argv": []}),
            ("string-argv", {"argv": sys.executable}),
            ("nonliteral-argument", {"argv": [sys.executable, "-c", "pass", 17]}),
            ("missing-cwd", {"cwd": str(self.root / "nonexistent directory")}),
            ("nan-timeout", {"timeout": math.nan}),
            ("infinite-timeout", {"timeout": math.inf}),
            ("negative-timeout", {"timeout": -1}),
            ("boolean-timeout", {"timeout": True}),
        )
        for name, fields in invalid:
            with self.subTest(invalid=name):
                marker = self.root / (name + "-child-ran")
                first = self.job("first", "from pathlib import Path; import sys; "
                                 "Path(sys.argv[1]).write_text('ran')", marker)
                bad = {**self.job("invalid", "pass"), **fields}
                result = None
                try:
                    result = self.gate.execute_jobs([first, bad], self.root / name, {})
                except Exception:
                    pass
                self.assertFalse(marker.exists(), "an invalid later job did not prevent first launch")
                if result is not None:
                    self.assertEqual(result["status"], "FAILED")

    def test_literal_argv_metacharacters_are_not_interpreted_by_a_shell(self):
        marker = self.root / "shell-expanded"
        arguments = [f"$(touch {marker})", f"x; touch {marker}", "one argument with spaces", "*"]
        job = self.job("literal", "import json,sys; print(json.dumps(sys.argv[1:]))", *arguments)
        result = self.gate.execute_jobs([job], self.root / "literal campaign", {})
        self.assertEqual(result["status"], "LOCAL_CONTRIBUTION_PASS")
        actual = json.loads((self.root / "literal campaign/literal/stdout.txt").read_text())
        self.assertEqual(actual, arguments)
        self.assertFalse(marker.exists())

    def test_recorded_process_rejects_nonfinite_or_invalid_bounds_before_launch(self):
        settings = (
            {"timeout": math.nan}, {"timeout": math.inf}, {"timeout": -1}, {"timeout": True},
            {"max_output_bytes": math.nan}, {"max_output_bytes": math.inf},
            {"max_output_bytes": -1}, {"max_output_bytes": True},
        )
        for number, setting in enumerate(settings):
            with self.subTest(setting=setting):
                marker = self.root / ("invalid-bound-child-" + str(number))
                command = self.job("unused", "from pathlib import Path; import sys; "
                                   "Path(sys.argv[1]).write_text('ran')", marker)["argv"]
                rejected = False
                try:
                    self.gate.run_recorded(command, self.root / ("invalid-bound-" + str(number)),
                                           cwd=self.root, **setting)
                except (ValueError, TypeError):
                    rejected = True
                self.assertFalse(marker.exists(), "invalid process bounds still launched a child")
                self.assertTrue(rejected, "invalid process bounds were accepted")

    def test_timeout_kills_a_nested_recorder_child_in_its_own_session(self):
        pidfile = self.root / "nested-child.pid"
        child = "import os,time; from pathlib import Path; import sys; " \
                "Path(sys.argv[1]).write_text(str(os.getpid())); time.sleep(5)"
        launcher = "import sys; sys.path.insert(0,sys.argv[1]); " \
                   "from recorded_process import run_recorded; " \
                   "run_recorded([sys.executable,'-B','-c',sys.argv[2],sys.argv[3]]," \
                   "sys.argv[4],timeout=10)"
        command = [sys.executable, "-B", "-c", launcher, str(TOOL.parent), child,
                   str(pidfile), str(self.root / "inner recorder")]
        pid = None
        try:
            receipt = self.gate.run_recorded(command, self.root / "outer recorder",
                                             timeout=0.6, cwd=self.root)
            self.assertTrue(receipt["timed_out"])
            self.assertTrue(pidfile.is_file(), "nested fixture never launched its tiny child")
            pid = int(pidfile.read_text())
            self.assertFalse(self.live(pid), "nested recorder child survived its outer timeout")
            self.assertTrue(receipt["process_tree"]["cleanup_complete"])
            # The inner supervisor may reap its child before the outer one
            # reaps that supervisor.  The outer recorder must reap its own
            # leader; it need not personally reap every transitive descendant.
            self.assertIn(receipt["pid"], receipt["process_tree"]["reaped_pids"])
            self.assertEqual(receipt["process_tree"]["survivors"], [])
        finally:
            if pid is None and pidfile.is_file():
                pid = int(pidfile.read_text())
            self.cleanup_group(pid)

    def test_leader_exit_does_not_leave_stream_writing_descendants_alive(self):
        pidfile = self.root / "survivor.pid"
        child = "import os,sys,time; from pathlib import Path; " \
                "Path(sys.argv[1]).write_text(str(os.getpid())); " \
                "print('descendant ready',flush=True); time.sleep(5)"
        launcher = "import subprocess,sys,time; from pathlib import Path; " \
                   "subprocess.Popen([sys.executable,'-B','-c',sys.argv[1],sys.argv[2]]); " \
                   "p=Path(sys.argv[2]); " \
                   "exec('for _ in range(200):\\n if p.exists(): break\\n time.sleep(.005)')"
        command = [sys.executable, "-B", "-c", launcher, child, str(pidfile)]
        receipt = None
        try:
            receipt = self.gate.run_recorded(command, self.root / "leader exited", timeout=2,
                                             cwd=self.root)
            self.assertTrue(pidfile.is_file(), "descendant fixture did not start")
            pid = int(pidfile.read_text())
            self.assertFalse(self.live(pid), "receipt published while its descendant still held recorded streams")
            self.assertFalse(receipt["succeeded"], "a leader with unfinished descendants received success")
            self.assertTrue(receipt["process_tree"]["cleanup_complete"])
            self.assertTrue(receipt["process_tree"]["unexpected_descendants"])
            self.assertIn(pid, receipt["process_tree"]["reaped_pids"])
        finally:
            if receipt is not None:
                self.cleanup_group(receipt["pid"])
            if pidfile.is_file():
                try:
                    os.kill(int(pidfile.read_text()), signal.SIGKILL)
                except ProcessLookupError:
                    pass

    def test_timeout_reaps_a_setsid_double_fork_descendant(self):
        pidfile = self.root / "double-fork.pid"
        daemon = "import os,sys,time; from pathlib import Path\n" \
                 "if os.fork(): os._exit(0)\n" \
                 "os.setsid()\n" \
                 "if os.fork(): os._exit(0)\n" \
                 "Path(sys.argv[1]).write_text(str(os.getpid()))\ntime.sleep(5)\n"
        launcher = "import subprocess,sys,time; " \
                   "subprocess.Popen([sys.executable,'-B','-c',sys.argv[1],sys.argv[2]],start_new_session=True); " \
                   "time.sleep(5)"
        command = [sys.executable, "-B", "-c", launcher, daemon, str(pidfile)]
        try:
            receipt = self.gate.run_recorded(command, self.root / "double fork", timeout=0.6,
                                             cwd=self.root)
            self.assertTrue(receipt["timed_out"])
            self.assertTrue(pidfile.is_file(), "double-fork fixture did not start")
            self.assertFalse(self.live(int(pidfile.read_text())), "setsid/double-fork escaped timeout cleanup")
            self.assertTrue(receipt["process_tree"]["cleanup_complete"])
            self.assertIn(int(pidfile.read_text()), receipt["process_tree"]["reaped_pids"])
        finally:
            if pidfile.is_file():
                try:
                    os.kill(int(pidfile.read_text()), signal.SIGKILL)
                except ProcessLookupError:
                    pass

    def test_recorder_parent_death_still_cleans_its_owned_child(self):
        pidfile = self.root / "parentdeath-child.pid"
        child = "import os,sys,time; from pathlib import Path; " \
                "Path(sys.argv[1]).write_text(str(os.getpid())); time.sleep(5)"
        wrapper = "import sys; sys.path.insert(0,sys.argv[1]); " \
                  "from recorded_process import run_recorded; " \
                  "run_recorded([sys.executable,'-B','-c',sys.argv[2],sys.argv[3]],sys.argv[4],timeout=10)"
        command = [sys.executable, "-B", "-c", wrapper, str(TOOL.parent), child,
                   str(pidfile), str(self.root / "parentdeath recorder")]
        parent = subprocess.Popen(command, cwd=self.root, start_new_session=True,
                                  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            deadline = time.monotonic() + 2
            while not pidfile.exists() and parent.poll() is None and time.monotonic() < deadline:
                time.sleep(0.01)
            self.assertTrue(pidfile.is_file(), "parentdeath fixture did not start")
            parent.kill()
            parent.wait(timeout=2)
            pid = int(pidfile.read_text())
            deadline = time.monotonic() + 1.5
            while self.live(pid) and time.monotonic() < deadline:
                time.sleep(0.01)
            self.assertFalse(self.live(pid), "owned child survived recorder parent death")
            tree = self.root / "parentdeath recorder/process_tree.json"
            deadline = time.monotonic() + 1
            while time.monotonic() < deadline:
                if tree.is_file() and json.loads(tree.read_text())["cleanup_complete"]:
                    break
                time.sleep(0.01)
            state = json.loads(tree.read_text())
            self.assertTrue(state["cleanup_complete"])
            self.assertIn(pid, state["reaped_pids"])
        finally:
            if parent.poll() is None:
                parent.kill()
                parent.wait(timeout=2)
            if pidfile.is_file():
                self.cleanup_group(int(pidfile.read_text()))

    def test_short_lived_output_overflow_cannot_receive_success(self):
        receipt = self.gate.run_recorded([sys.executable, "-B", "-c", "print('x'*8192)"],
                                         self.root / "output overflow", max_output_bytes=128)
        self.assertFalse(receipt["succeeded"])
        self.assertTrue(receipt["output_limit_exceeded"])
        self.assertTrue(receipt["process_tree"]["cleanup_complete"])
        for name, row in receipt["streams"].items():
            data = (self.root / "output overflow" / name).read_bytes()
            self.assertEqual(row["sha256"], hashlib.sha256(data).hexdigest())
            self.assertEqual(row["bytes"], len(data))

    def test_timeout_cleanup_does_not_signal_an_unrelated_owned_sibling(self):
        sibling = subprocess.Popen([sys.executable, "-B", "-c", "import time; time.sleep(5)"],
                                   start_new_session=True, stdout=subprocess.DEVNULL,
                                   stderr=subprocess.DEVNULL)
        try:
            receipt = self.gate.run_recorded([sys.executable, "-B", "-c", "import time; time.sleep(5)"],
                                             self.root / "isolated timeout", timeout=0.15)
            self.assertTrue(receipt["timed_out"])
            self.assertTrue(receipt["process_tree"]["cleanup_complete"])
            self.assertIsNone(sibling.poll(), "a different caller child was signalled by job cleanup")
            self.assertNotIn(sibling.pid, receipt["process_tree"]["observed_pids"])
        finally:
            if sibling.poll() is None:
                sibling.kill()
            sibling.wait(timeout=2)


if __name__ == "__main__":
    unittest.main()
