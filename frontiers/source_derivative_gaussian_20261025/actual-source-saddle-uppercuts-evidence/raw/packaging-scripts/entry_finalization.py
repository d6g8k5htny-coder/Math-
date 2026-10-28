#!/usr/bin/env python3
"""Prospective original metadata entry capture; run only after actual final65 GO."""
from pathlib import Path
from datetime import datetime,timezone
import json,os,subprocess,sys,time
R=Path('/workspace/scratch/actual-source-saddle-uppercuts-packaging')
A=R/'entry-captures/metadata-attempt-001'
from archive_prepare import gate
gate(json.loads((R/'FINAL_INPUTS.json').read_text()))
if A.exists():raise RuntimeError('Prior actual entry capture exists; preserve it, no automatic restart.')
A.mkdir(parents=True)
def now():return datetime.now(timezone.utc).isoformat()
def put(p,obj):
 with p.open('x') as f:json.dump(obj,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
cmd=[sys.executable,str(R/'launch_finalization.py')];start=now();tick=time.monotonic()
put(A/'started.json',{'command':cmd,'cwd':'/workspace','started_utc':start,'scope':'Actual metadata entry boundary; full original separate child stdout/stderr prepared before execution.'})
with (A/'stdout.log').open('xb') as out,(A/'stderr.log').open('xb') as err:
 proc=subprocess.run(cmd,cwd='/workspace',stdout=out,stderr=err)
 out.flush();os.fsync(out.fileno());err.flush();os.fsync(err.fileno())
receipt={'command':cmd,'cwd':'/workspace','started_utc':start,'ended_utc':now(),'elapsed_seconds':time.monotonic()-tick,'exit_code':proc.returncode,'stdout':'stdout.log','stderr':'stderr.log','full_actual_capture':True,'capture_hashes_claimed':False,'closure':'Actual entry finishes after immutable worker handoff; root may bind this fresh process record separately, no archive reseal.'}
put(A/'receipt.json',receipt);print(json.dumps(receipt,sort_keys=True));print((A/'stdout.log').read_text())
if proc.returncode:print((A/'stderr.log').read_text())
sys.exit(proc.returncode)
