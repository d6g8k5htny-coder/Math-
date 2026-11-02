#!/usr/bin/env python3
"""Whole actual metadata wrapper/seal stdout/stderr/command/time capture."""
from pathlib import Path
from datetime import datetime,timezone
import json,os,subprocess,sys,time
R=Path('/workspace/scratch/actual-source-torus-regular-slab-packaging-proposal');A=R/'launcher-captures/metadata-attempt-001'
from archive_prepare import gate
gate(json.loads((R/'FINAL_INPUTS.json').read_text()))
if A.exists():raise RuntimeError('Prior actual capture exists; preserve and continue scoped, no restart.')
A.mkdir(parents=True)
def now():return datetime.now(timezone.utc).isoformat()
def syncdirs(directory):
    for p in [directory,*directory.parents]:
        if p==R or R in p.parents:
            fd=os.open(p,os.O_RDONLY|os.O_DIRECTORY)
            try:os.fsync(fd)
            finally:os.close(fd)
        if p==R:break
def put(p,obj):
    with p.open('w')as f:json.dump(obj,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
    syncdirs(p.parent)
cmd=[sys.executable,str(R/'run_finalization.py')];start=now();tick=time.monotonic()
put(A/'started.json',{'command':cmd,'cwd':'/workspace','started_utc':start,'capture':'Full actual separate binary stdout/stderr of metadata wrapper, including custody seal.'})
with(A/'stdout.log').open('wb')as out,(A/'stderr.log').open('wb')as err:
    proc=subprocess.run(cmd,cwd='/workspace',stdout=out,stderr=err)
    out.flush();os.fsync(out.fileno());err.flush();os.fsync(err.fileno())
syncdirs(A)
receipt={'command':cmd,'cwd':'/workspace','started_utc':start,'ended_utc':now(),'elapsed_seconds':time.monotonic()-tick,'exit_code':proc.returncode,'stdout':'stdout.log','stderr':'stderr.log','full_actual_capture':True,'capture_hashes_claimed':False}
put(A/'receipt.json',receipt);print(json.dumps(receipt,sort_keys=True));print((A/'stdout.log').read_text())
if proc.returncode:print((A/'stderr.log').read_text())
sys.exit(proc.returncode)
