"""Linux per-job subreaper for ordinary descendants; this is not an OS sandbox."""
import ctypes
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time


def _prctl(option, value):
    libc = ctypes.CDLL(None, use_errno=True)
    if libc.prctl(option, value, 0, 0, 0) != 0:
        raise OSError(ctypes.get_errno(), "Linux process supervision prctl failed")


def _write(path, value):
    path = Path(path)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")
    os.replace(temporary, path)


def _children():
    pid = os.getpid()
    children_file = Path(f"/proc/self/task/{pid}/children")
    if children_file.is_file():
        return [int(value) for value in children_file.read_text().split()]
    # Some kernels omit CONFIG_CHECKPOINT_RESTORE's children file.  Parent PID
    # still identifies only this isolated supervisor's unreaped direct children.
    children = []
    for path in Path('/proc').iterdir():
        if not path.name.isdigit():
            continue
        try:
            fields = (path / 'stat').read_text().rsplit(')', 1)[1].split()
        except (FileNotFoundError, ProcessLookupError, PermissionError):
            continue
        if int(fields[1]) == pid:
            children.append(int(path.name))
    return children


def supervise(request):
    output = Path(request["output"])
    state = {"supervisor_pid": os.getpid(), "leader_pid": None, "returncode": None,
             "cleanup_complete": False, "unexpected_descendants": False,
             "termination_signal": None, "observed_pids": [], "terminated_pids": [],
             "reaped_pids": [], "survivors": [], "failure": None,
             "boundary": "Owned ordinary descendants including setsid/double-fork; "
                         "not a sandbox against same-UID attacks or unkillable kernel tasks."}
    child = None
    observed, terminated, reaped = set(), set(), set()

    def requested(signum, frame):
        state["termination_signal"] = signum

    def save():
        state.update(observed_pids=sorted(observed), terminated_pids=sorted(terminated),
                     reaped_pids=sorted(reaped))
        _write(output / "process_tree.json", state)

    def collect():
        while True:
            try:
                pid, status, _ = os.wait4(-1, os.WNOHANG)
            except ChildProcessError:
                return False
            if not pid:
                return True
            observed.add(pid)
            reaped.add(pid)
            if child is not None and pid == child.pid:
                child.returncode = os.waitstatus_to_exitcode(status)
                state["returncode"] = child.returncode

    def cleanup():
        deadline = time.monotonic() + request["cleanup_seconds"]
        while True:
            has_children = collect()
            children = _children()
            observed.update(children)
            state["survivors"] = children
            save()
            if not children and not has_children:
                state["cleanup_complete"] = True
                return
            # These PIDs cannot be reused while they remain our unreaped children.
            for signum in (signal.SIGSTOP, signal.SIGKILL):
                for pid in children:
                    try:
                        os.kill(pid, signum)
                        if signum == signal.SIGKILL:
                            terminated.add(pid)
                    except ProcessLookupError:
                        pass
            collect()
            if time.monotonic() >= deadline:
                state["survivors"] = _children()
                state["cleanup_complete"] = not state["survivors"] and not collect()
                return
            time.sleep(0.01)

    try:
        for signum in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP):
            signal.signal(signum, requested)
        _prctl(36, 1)  # PR_SET_CHILD_SUBREAPER, confined to this helper process.
        _prctl(1, signal.SIGTERM)  # PR_SET_PDEATHSIG requests cleanup on recorder death.
        if os.getppid() != request["parent_pid"]:
            state["termination_signal"] = signal.SIGTERM
        if state["termination_signal"] is None:
            supervisor_pid = os.getpid()

            def guard_child():
                _prctl(1, signal.SIGKILL)
                if os.getppid() != supervisor_pid:
                    os._exit(125)

            child = subprocess.Popen(request["command"], cwd=request["cwd"],
                                     start_new_session=True, preexec_fn=guard_child)
            observed.add(child.pid)
            state["leader_pid"] = child.pid
            _write(output / "started.json", {"command": request["command"], "pid": child.pid,
                   "supervisor_pid": os.getpid(), "started_unix_ns": request["started_unix_ns"]})
            save()
            while True:
                collect()
                if state["termination_signal"] is not None:
                    break
                if state["returncode"] is not None:
                    children = _children()
                    observed.update(children)
                    state["unexpected_descendants"] = bool(children)
                    break
                time.sleep(0.01)
    except BaseException as exc:
        state["failure"] = {"type": type(exc).__name__, "message": str(exc)}
    finally:
        try:
            cleanup()
        except BaseException as exc:
            state["cleanup_complete"] = False
            state["failure"] = {"type": type(exc).__name__, "message": str(exc)}
        save()
    return 0 if state["cleanup_complete"] else 3


if __name__ == "__main__":
    request = json.loads(Path(sys.argv[1]).read_text())
    raise SystemExit(supervise(request))
