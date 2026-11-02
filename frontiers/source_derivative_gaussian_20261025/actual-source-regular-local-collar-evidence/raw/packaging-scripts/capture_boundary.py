"""Original stage66 metadata wrapper capture; import performs no action."""
from pathlib import Path
import os,subprocess,sys,time
import custody as f
import archive_prepare

def capture(scope,command):
    archive_prepare.gate(f.read(f.R/'FINAL_INPUTS.json'))
    folder=f.R/(scope+'-captures')/'metadata-attempt-001'
    f.require(not folder.exists(),'Prior actual66 wrapper exists; preserve it, no automatic restart')
    folder.mkdir(parents=True);start=f.now();tick=time.monotonic()
    intent={'scope':scope,'command_argv':command,'cwd':'/workspace','start_utc':start,
        'original_split_capture':True,'automatic_retry':False,'capture_hashes_claimed':False}
    f.put(folder/'STARTED.json',intent)
    code=None;failure=None
    try:
        with (folder/'stdout.log').open('xb') as out,(folder/'stderr.log').open('xb') as err:
            process=subprocess.run(command,cwd='/workspace',stdout=out,stderr=err)
            code=process.returncode;out.flush();os.fsync(out.fileno());err.flush();os.fsync(err.fileno())
    except BaseException as exc:failure=repr(exc)
    receipt={**intent,'end_utc':f.now(),'elapsed_seconds':time.monotonic()-tick,'child_exit_code':code,
        'spawn_or_wrapper_exception':failure,'stdout':'stdout.log','stderr':'stderr.log',
        'status':'PASS_ACTUAL_CHILD_EXIT_ZERO' if code==0 and failure is None else 'FAIL_PRESERVED_NO_RETRY',
        'closure':'Actual wrapper closes after worker immutable handoff; root may bind closed wrapper records as separate publication tail, no archive reseal.'}
    f.put(folder/'RECEIPT.json',receipt)
    print(f.read(folder/'RECEIPT.json'))
    return code if code is not None and code>=0 else 1
