"""Run each stable-input final phase once; stop on the first unresolved failure."""
from pathlib import Path
import json, subprocess, sys
from run_final_phase import ROOT, NEW, now, sha, write, require

def main():
    invp=ROOT/'FINAL_SOURCE_INVENTORY.json'
    inv=json.loads(invp.read_text())
    require(not (ROOT/'FINAL_SEQUENCE_START.json').exists(), 'sequence already started')
    write(ROOT/'FINAL_SEQUENCE_START.json',{'started_utc':now(),'inventory_sha256':sha(invp),
          'driver_sha256':sha(Path(__file__)),'scientific_effect':'NONE'})
    result={'started_utc':now(),'inventory_sha256':sha(invp),'phases':[],'scientific_effect':'NONE'}
    phases=[('build',m) for m in inv['build_order']]+[('kernel',m) for m in NEW]
    for kind,module in phases:
        start=now()
        print(json.dumps({'stage':'STARTING','kind':kind,'module':module}),flush=True)
        code=subprocess.run([sys.executable,'-B',str(ROOT/'run_final_phase.py'),kind,module],cwd=ROOT).returncode
        result['phases'].append({'kind':kind,'module':module,'started_utc':start,'ended_utc':now(),'returncode':code})
        if code:
            result['status']='HOLD_FAILED_PHASE';break
    else: result['status']='PASS_FROZEN_BUILD_AND_STANDARD_KERNEL_REPLAY'
    result['ended_utc']=now()
    write(ROOT/'FINAL_SEQUENCE_RESULT.json',result)
    print(json.dumps({'status':result['status'],'phases':len(result['phases'])}),flush=True)
    return 0 if result['status'].startswith('PASS_') else 1

if __name__=='__main__':raise SystemExit(main())
