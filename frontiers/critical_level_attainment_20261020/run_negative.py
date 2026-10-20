"""One missing-closed-LPC-premise rejection against the actual final compiled theorem."""
from pathlib import Path
import fcntl, json, os, signal, subprocess, time
from run_final_phase import ROOT, PROJECT, BUILD, BIN, require, now, sha, write, runtime, source_map, objects

def main():
    with (ROOT / 'lean-slot.lock').open('a+') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        run = ROOT / 'negative-final'
        run.mkdir()
        src = ROOT / 'negative-project/WithoutClosedLPC.lean'
        source_sha = sha(src)
        frozen_sources, frozen_objects = source_map(), objects()
        require('CriticalLevelAttainment.olean' in frozen_objects, 'actual final theorem not built')
        _, paths = runtime()
        env = {k:v for k,v in os.environ.items() if not k.startswith(('LEAN','LAKE','LD_','DYLD_'))}
        env.update(PATH=os.pathsep.join([str(BIN),'/usr/bin','/bin']), LEAN_PATH=os.pathsep.join(paths), LEAN_NUM_THREADS='2')
        command = [str(BIN/'lean'), '-j2', '-M4096', str(src)]
        r = {'started_utc':now(), 'source_sha256':source_sha, 'command':command,
             'source_before':frozen_sources, 'objects_before':frozen_objects,
             'lean_sha256':sha(BIN/'lean'), 'inventory_sha256':sha(ROOT/'FINAL_SOURCE_INVENTORY.json'),
             'runner_sha256':sha(Path(__file__)), 'timeout_seconds':600,
             'meaning':'Interface rejection for the omitted actual closed-level LPC input; not a counterexample to the open Morse-to-LPC implication.'}
        write(run/'START.json',r)
        start=time.monotonic()
        with (run/'stdout.txt').open('xb') as out, (run/'stderr.txt').open('xb') as err:
            p=subprocess.Popen(command,cwd=src.parent,env=env,stdout=out,stderr=err,start_new_session=True)
            timedout=False
            try: code=p.wait(timeout=600)
            except subprocess.TimeoutExpired:
                timedout=True; os.killpg(p.pid,signal.SIGTERM)
                try: code=p.wait(timeout=5)
                except subprocess.TimeoutExpired: os.killpg(p.pid,signal.SIGKILL); code=p.wait()
        text=(run/'stdout.txt').read_text()+(run/'stderr.txt').read_text()
        diagnostic=('type mismatch' in text.lower() and 'LocallyPathConnectedSpace' in text and
                    not any(s in text.lower() for s in ['unknown module','unknown identifier','unexpected token','object file']))
        good=(code!=0 and not timedout and diagnostic and sha(src)==source_sha and
              source_map()==frozen_sources and objects()==frozen_objects)
        r.update(ended_utc=now(),seconds=time.monotonic()-start,returncode=code,timed_out=timedout,
                 child_pid=p.pid,diagnostic_match=diagnostic,source_unchanged=sha(src)==source_sha,
                 imported_sources_unchanged=source_map()==frozen_sources,
                 imported_objects_unchanged=objects()==frozen_objects,
                 stdout_sha256=sha(run/'stdout.txt'),stderr_sha256=sha(run/'stderr.txt'),
                 status='PASS_EXPECTED_MISSING_PREMISE_REJECTION' if good else 'HOLD')
        write(run/'RECEIPT.json',r)
        print(json.dumps({'status':r['status'],'seconds':r['seconds']}),flush=True)
        return 0 if good else 1

if __name__=='__main__': raise SystemExit(main())
