import hashlib
import json
from pathlib import Path
import subprocess
import time

root=Path('/workspace/Math-wholefield-20261025/frontiers/source_derivative_gaussian_20261025')
out=Path('/workspace/scratch/source-smooth-conditional')
source=root/'SourceSmoothConditionalKernel.lean'
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
command=['/home/agent/.elan/bin/lake','env','leanchecker','SourceSmoothConditionalKernel']
before=digest(source)
start=time.time()
proc=subprocess.run(command,cwd=root,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
log=out/'11-kernel-replay.log'
log.write_bytes(proc.stdout)
record={'command':command,'cwd':str(root),'exit_code':proc.returncode,
        'source':str(source),'source_sha256_before':before,
        'source_sha256_after':digest(source),'log_sha256':digest(log),
        'elapsed_seconds':time.time()-start}
(out/'11-kernel-replay.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record))
print(proc.stdout.decode(),end='')
raise SystemExit(proc.returncode)
