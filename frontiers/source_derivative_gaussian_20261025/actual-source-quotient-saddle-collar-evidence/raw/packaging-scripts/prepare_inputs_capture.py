#!/usr/bin/env python3
"""Prospective original split capture for one final-input composition, no validation/hash."""
from pathlib import Path
from datetime import datetime,timezone
import json,subprocess,sys,time
R=Path('/workspace/scratch/actual-source-quotient-saddle-collar-packaging-proposal');A=R/'input-preparation-captures'
A.mkdir()
def now():return datetime.now(timezone.utc).isoformat()
cmd=[sys.executable,str(R/'prepare_final_inputs.py')];start=now();tick=time.monotonic()
(A/'started.json').write_text(json.dumps({'command':cmd,'cwd':'/workspace','started_utc':start,'prospective_original_separate_streams':True},indent=2)+'\n')
with (A/'stdout.log').open('wb') as out,(A/'stderr.log').open('wb') as err:p=subprocess.run(cmd,cwd='/workspace',stdout=out,stderr=err)
r={'command':cmd,'cwd':'/workspace','started_utc':start,'ended_utc':now(),'elapsed_seconds':time.monotonic()-tick,'exit_code':p.returncode,'stdout':'stdout.log','stderr':'stderr.log','scope':'Input composition ONLY, no hash/validation/math/assembly'}
(A/'receipt.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r));print((A/'stdout.log').read_text());print((A/'stderr.log').read_text());sys.exit(p.returncode)
