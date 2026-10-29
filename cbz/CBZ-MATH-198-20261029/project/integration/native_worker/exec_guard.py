"""Linux runtime guard: kill the exec'd Lean child if its controller dies."""
import ctypes
import os
import signal
import sys

if __name__ == '__main__':
    parent=os.getppid()
    libc=ctypes.CDLL(None, use_errno=True)
    if libc.prctl(1, signal.SIGKILL, 0, 0, 0) != 0:
        raise OSError(ctypes.get_errno(), 'PR_SET_PDEATHSIG failed')
    if os.getppid() != parent or parent == 1:
        raise RuntimeError('worker controller exited before guard setup')
    os.execv(sys.argv[1], sys.argv[1:])
