"""Bounded, single-session JSONL transport for the closed-proof worker."""
import json
import math
import os
from pathlib import Path
import selectors
import signal
import subprocess
import threading
import time
import uuid

PROTOCOL = 'ul-closed-proof-v1'

def _positive_finite(value):
    if type(value) not in (int, float): return False
    try: return value > 0 and math.isfinite(value)
    except OverflowError: return False

class WorkerError(RuntimeError):
    pass

class LeanWorker:
    @property
    def active_state_count(self):
        """Session-wide live handle count, including other search invocations."""
        with self._lock:
            return len(self._states)

    @property
    def remaining_requests(self):
        """Remaining admitted requests under client and pinned native caps."""
        with self._lock:
            # ClosedProofWorker.loop has a fixed256-request protocol limit.
            return max(0, min(self.max_requests, 256)-self._id)

    def __init__(self, command, *, session=None, timeout=30, startup_timeout=75,
                 receipt_dir, max_message_bytes=1048576, max_requests=256,
                 max_lifetime=300, env=None, metadata=None):
        self.session = session or uuid.uuid4().hex
        self.timeout, self.max_message_bytes = timeout, max_message_bytes
        self.max_requests, self.max_lifetime = max_requests, max_lifetime
        if (type(self.session) is not str or not self.session
                or not all(_positive_finite(v) for v in (timeout, startup_timeout, max_lifetime))
                or type(max_message_bytes) is not int or max_message_bytes <= 0
                or type(max_requests) is not int or max_requests <= 0):
            raise ValueError('invalid worker limits or session')
        self.receipt_dir = Path(receipt_dir)
        self.receipt_dir.mkdir(parents=True, exist_ok=False)
        self._events = (self.receipt_dir / 'events.jsonl').open('x', encoding='utf-8')
        self._lock = threading.RLock()
        self._stdout, self._stderr, self._pending = bytearray(), bytearray(), bytearray()
        self._stdout_total = self._stderr_total = 0
        self._states = set()
        self._id = 0
        self._alive = True
        self._reaped = False
        self._watchdog = None
        self._started = time.monotonic()
        self.process = None
        self._event('session_start', command=list(command), session=self.session, metadata=metadata or {}, cost_boundary={'request_wall':'per-request monotonic wall time including nested action work','worker_wait4':'whole-worker CPU and max RSS, recorded at stop'}, limits={'max_message_bytes':max_message_bytes,'max_requests':max_requests,'max_lifetime':max_lifetime})
        try:
            self.process = subprocess.Popen([*map(str, command), self.session], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, start_new_session=True, bufsize=0)
            for stream in (self.process.stdin, self.process.stdout, self.process.stderr): os.set_blocking(stream.fileno(), False)
            ready = self._read_record(self._started + min(startup_timeout, max_lifetime))
            if not isinstance(ready, dict) or ready.get('event') != 'ready' or ready.get('protocol') != PROTOCOL or ready.get('session') != self.session or not isinstance(ready.get('max_states'), int) or not isinstance(ready.get('tasks'), list) or not isinstance(ready.get('actions'), list):
                raise WorkerError('invalid ready record')
            self.ready = ready
            self._event('worker_ready', ready=ready, wall_seconds=time.monotonic()-self._started)
            self._watchdog = threading.Timer(max(0, self._started+self.max_lifetime-time.monotonic()), self._expire)
            self._watchdog.daemon = True
            self._watchdog.start()
        except BaseException as exc:
            self._stop(str(exc))
            raise

    def _event(self, event, **data):
        self._events.write(json.dumps({'event':event, **data}, ensure_ascii=True, separators=(',', ':'))+'\n')
        self._events.flush()

    def _retain(self, which, data):
        buf = self._stdout if which == 'stdout' else self._stderr
        total_name = '_'+which+'_total'
        setattr(self, total_name, getattr(self, total_name)+len(data))
        buf.extend(data)
        if len(buf) > self.max_message_bytes:
            del buf[:-self.max_message_bytes]
        # Bound total output as well as retained output, allowing multiple records.
        if getattr(self, total_name) > self.max_message_bytes * (self.max_requests + 2):
            raise WorkerError(which+' stream limit exceeded')

    def _pump(self, deadline, outgoing=None):
        with selectors.DefaultSelector() as sel:
            sel.register(self.process.stdout, selectors.EVENT_READ, 'stdout')
            if not self.process.stderr.closed: sel.register(self.process.stderr, selectors.EVENT_READ, 'stderr')
            if outgoing is not None and len(outgoing): sel.register(self.process.stdin, selectors.EVENT_WRITE, 'stdin')
            remaining = deadline-time.monotonic()
            if remaining <= 0: raise TimeoutError('worker deadline exceeded')
            events = sel.select(remaining)
            if not events: raise TimeoutError('worker deadline exceeded')
            for key, _ in events:
                if key.data == 'stdin':
                    try: n = os.write(key.fd, outgoing)
                    except BrokenPipeError as exc: raise WorkerError('worker stdin closed') from exc
                    del outgoing[:n]
                else:
                    try: data = os.read(key.fd, 65536)
                    except BlockingIOError: continue
                    if not data:
                        if key.data == 'stdout': raise WorkerError('worker stdout EOF')
                        # Avoid repeatedly selecting an EOF stderr descriptor.
                        self.process.stderr.close()
                        continue
                    self._retain(key.data, data)
                    if key.data == 'stdout':
                        self._pending.extend(data)
                        if len(self._pending.split(b'\n',1)[0]) > self.max_message_bytes: raise WorkerError('response too large')

    def _read_record(self, deadline):
        while b'\n' not in self._pending:
            self._pump(deadline)
        raw, _, rest = self._pending.partition(b'\n')
        self._pending = bytearray(rest)
        if len(raw) > self.max_message_bytes: raise WorkerError('response too large')
        try: return json.loads(raw.decode('utf-8'))
        except (ValueError, UnicodeError) as exc: raise WorkerError('malformed response') from exc

    def request(self, op, *, timeout=None, **payload):
        if timeout is not None and (isinstance(timeout, bool) or not isinstance(timeout, (int, float)) or not math.isfinite(timeout) or timeout <= 0):
            raise ValueError('timeout must be finite and positive')
        with self._lock:
            if not self._alive: raise WorkerError('worker session is closed')
            if not isinstance(op, str) or not op or set(payload) & {'protocol','session','id','op'}: raise ValueError('invalid request fields')
            if op in ('attempt','inspect','drop') and (type(payload.get('state')) not in (int, str) or payload['state'] not in self._states): raise ValueError('unknown or stale state')
            if op == 'verify' and ('task' not in payload or 'certificate' not in payload): raise ValueError('verify requires trusted task and certificate')
            if self._id >= self.max_requests or time.monotonic()-self._started >= self.max_lifetime:
                self._stop('worker limit exceeded'); raise WorkerError('worker limit exceeded')
            self._id += 1
            reqid = self._id
            started = time.monotonic()
            deadline = min(started+self.timeout, started+timeout if timeout is not None else float('inf'), self._started+self.max_lifetime)
            request = {'protocol':PROTOCOL,'session':self.session,'id':reqid,'op':op,**payload}
            event_started = False
            try:
                raw = json.dumps(request, ensure_ascii=True, separators=(',', ':')).encode()+b'\n'
                if len(raw)-1 > self.max_message_bytes: raise WorkerError('request too large')
                self._event('request_started', id=reqid, op=op, request=request)
                event_started = True
                outgoing = bytearray(raw)
                while outgoing: self._pump(deadline, outgoing)
                response = self._read_record(deadline)
                if time.monotonic() > deadline: raise TimeoutError('worker deadline exceeded')
                if not isinstance(response, dict) or response.get('protocol') != PROTOCOL or response.get('session') != self.session or type(response.get('id')) is not int or response['id'] != reqid or type(response.get('ok')) is not bool or not isinstance(response.get('status'), str): raise WorkerError('invalid response envelope')
                if response['ok'] and op in ('open','attempt') and 'state' in response:
                    if type(response['state']) not in (int, str) or response['state'] == '' or (type(response['state']) is int and response['state'] < 0): raise WorkerError('invalid state handle')
                    self._states.add(response['state'])
                if response['ok'] and op == 'drop' and response['status'] == 'dropped': self._states.remove(payload['state'])
                self._event('request_completed', id=reqid, op=op, wall_seconds=time.monotonic()-started, response=response)
                return response
            except BaseException as exc:
                if not event_started: self._event('request_started', id=reqid, op=op, request_unrecorded_reason=str(exc))
                self._event('request_failed', id=reqid, op=op, wall_seconds=time.monotonic()-started, error=type(exc).__name__, detail=str(exc))
                self._stop(str(exc))
                raise

    def _expire(self):
        with self._lock:
            if self._alive: self._stop('worker lifetime exceeded')

    def _stop(self, reason, graceful=False):
        if self._reaped: return
        self._alive = False
        if self._watchdog is not None: self._watchdog.cancel()
        self._states.clear()
        usage = None
        if self.process is not None:
            reaped = False
            if graceful:
                end = min(time.monotonic() + 0.3, self._started + self.max_lifetime)
                while time.monotonic() < end:
                    try:
                        pid, status, usage = os.wait4(self.process.pid, os.WNOHANG)
                    except ChildProcessError:
                        reaped = True
                        break
                    if pid:
                        self.process.returncode = os.waitstatus_to_exitcode(status)
                        reaped = True
                        break
                    time.sleep(0.01)
            if not reaped:
                try: os.killpg(self.process.pid, signal.SIGKILL)
                except ProcessLookupError: pass
                try:
                    _, status, usage = os.wait4(self.process.pid, 0)
                    self.process.returncode = os.waitstatus_to_exitcode(status)
                except ChildProcessError: pass
            for stream in (self.process.stdin, self.process.stdout, self.process.stderr):
                if stream and not stream.closed:
                    if stream in (self.process.stdout, self.process.stderr):
                        while True:
                            try: data = os.read(stream.fileno(), 65536)
                            except (BlockingIOError, OSError): break
                            if not data: break
                            try: self._retain('stdout' if stream is self.process.stdout else 'stderr', data)
                            except WorkerError: pass
                    stream.close()
        self._reaped = True
        (self.receipt_dir/'stdout.bin').write_bytes(self._stdout)
        (self.receipt_dir/'stderr.bin').write_bytes(self._stderr)
        accounting = {'user_seconds':usage.ru_utime,'system_seconds':usage.ru_stime,'max_rss_platform_units':usage.ru_maxrss} if usage else None
        receipt = {'cost_boundary':{'request_wall':'monotonic wall time per request, including nested action work','worker_wait4':'final whole-worker CPU and max RSS; do not add nested action time to worker wall'},'session':self.session,'reason':reason,'returncode':self.process.returncode if self.process else None,'worker_wall_seconds':time.monotonic()-self._started,'wait4':accounting,'stdout_bytes':self._stdout_total,'stderr_bytes':self._stderr_total,'stdout_retained':len(self._stdout),'stderr_retained':len(self._stderr),'stdout_retention':'tail','stderr_retention':'tail','stdout_truncated':self._stdout_total > len(self._stdout),'stderr_truncated':self._stderr_total > len(self._stderr),'stdout_discarded_bytes':self._stdout_total-len(self._stdout),'stderr_discarded_bytes':self._stderr_total-len(self._stderr)}
        self._event('worker_stopped', **receipt)
        (self.receipt_dir/'receipt.json').write_text(json.dumps(receipt, indent=2)+'\n', encoding='utf-8')
        self._events.close()

    def close(self):
        with self._lock:
            if not self._alive: return
            try:
                previous_timeout = self.timeout
                self.timeout = min(self.timeout, 1.0)
                self.request('shutdown')
                self.timeout = previous_timeout
            except Exception:
                return
            self._stop('closed', graceful=True)
    def __enter__(self): return self
    def __exit__(self, *args): self.close()
