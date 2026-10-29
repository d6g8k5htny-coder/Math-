import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

root = Path('/workspace/Math-wholefield-20261025/frontiers/source_derivative_gaussian_20261025')
out = Path('/workspace/scratch/source-smooth-conditional')
label, source, *extra = sys.argv[1:]
source = Path(source)
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
command = ['/home/agent/.elan/bin/lake', 'env', 'lean', '-DwarningAsError=true', *extra, str(source)]
before = digest(source)
production=root/'SourceSmoothConditionalKernel.lean'
production_before=digest(production)
start = time.time()
proc = subprocess.run(command, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
log = out / (label + '.log')
log.write_bytes(proc.stdout)
record = {'command':command, 'cwd':str(root), 'exit_code':proc.returncode,
          'source':str(source), 'source_sha256_before':before,
          'source_sha256_after':digest(source), 'log_sha256':digest(log),
          'production_source':str(production),
          'production_source_sha256_before':production_before,
          'production_source_sha256_after':digest(production),
          'elapsed_seconds':time.time()-start}
(out/(label+'.json')).write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record))
print(proc.stdout.decode(),end='')
sys.exit(proc.returncode)
