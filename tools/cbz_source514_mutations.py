#!/usr/bin/env python3
"""Three reason-bound source mutations of the source514 recorder's custody/domain guards."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import hashlib
import argparse
parser=argparse.ArgumentParser()
parser.add_argument("--output",type=Path,required=True)
args=parser.parse_args()
args.output.mkdir(parents=True,exist_ok=False)
root=Path(__file__).resolve().parents[1]
source=root/"tools/cbz_source514_hosted.py"
test=root/"tests/test_cbz_source514_hosted.py"
mutations=[
 ("head",'if actual != expected_commit:  # MUTATION_HEAD','if False:  # MUTATION_HEAD',"SourceBindingTests.test_wrong_head_rejected"),
 ("bytes",'if actual_bytes != expected:  # MUTATION_BYTES','if False:  # MUTATION_BYTES',"SourceBindingTests.test_dirty_bytes_rejected_even_assume_unchanged"),
 ("domain",'if production != plan["production"] or support != plan["support"]:  # MUTATION_DOMAIN','if False:  # MUTATION_DOMAIN',"RegisteredDomainTests.test_reordered_domain_rejected")]
report={"schema":"cbz-source514-recorder-mutations-v1","threshold":"all three source mutants in normal and optimized Python modes","source_sha256":hashlib.sha256(source.read_bytes()).hexdigest(),"executions":[],"status":"NOT_PASS"}
try:
 for mode in ["normal","optimized"]:
  optimize=["-O"] if mode=="optimized" else []
  command=[sys.executable,"-B","-S",*optimize,"-m","unittest","discover","-s","tests","-p","test_cbz_source514_hosted.py","-v"]
  result=subprocess.run(command,cwd=root,capture_output=True)
  (args.output/(mode+"-baseline.stdout")).write_bytes(result.stdout)
  (args.output/(mode+"-baseline.stderr")).write_bytes(result.stderr)
  report["executions"].append({"mode":mode,"label":"baseline","exit":result.returncode})
  if result.returncode: raise RuntimeError("unmodified recorder suite must pass before mutation")
  for label,anchor,replacement,target in mutations:
   text=source.read_text()
   if text.count(anchor)!=1: raise RuntimeError("unique mutation anchor absent: "+label)
   with tempfile.TemporaryDirectory(prefix="cbz-source514-mutant-") as temporary:
    scratch=Path(temporary);(scratch/"tools").mkdir();(scratch/"tests").mkdir()
    (scratch/"tools/cbz_source514_hosted.py").write_text(text.replace(anchor,replacement,1))
    shutil.copyfile(test,scratch/"tests/test_cbz_source514_hosted.py")
    command=[sys.executable,"-B","-S",*optimize,"-m","unittest","discover","-s","tests","-p","test_cbz_source514_hosted.py","-k",target,"-v"]
    result=subprocess.run(command,cwd=scratch,capture_output=True)
    stdout=result.stdout.decode();stderr=result.stderr.decode()
    prefix=mode+"-"+label
    (args.output/(prefix+".stdout")).write_bytes(result.stdout);(args.output/(prefix+".stderr")).write_bytes(result.stderr)
    intended=(result.returncode==1 and "AssertionError: ValueError not raised" in stderr and "FAILED (failures=1)" in stderr and "Ran 1 test" in stderr and "ERROR:" not in stderr)
    report["executions"].append({"mode":mode,"label":label,"exit":result.returncode,"intended_guard_failure":intended})
    if not intended: raise RuntimeError("mutant not killed for its named guard: "+prefix)
 report["status"]="ALL_THREE_REASON_BOUND_MUTANTS_KILLED_IN_BOTH_MODES"
finally:
 (args.output/"REPORT.json").write_text(json.dumps(report,indent=2)+"\n")
print(report["status"])
