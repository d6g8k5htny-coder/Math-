#!/usr/bin/env python3
"""Ten reason-bound source mutations of the source514 recorder's custody/domain guards."""
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
 ("domain",'if production != plan["production"] or support != plan["support"] or elder != plan["elder"]:  # MUTATION_DOMAIN','if False:  # MUTATION_DOMAIN',"RegisteredDomainTests.test_reordered_domain_rejected"),
 ("elder_identities",'if elder != ["SuperlevelBar", "ElderClearance", "ReusedCompactFrontier", "ClosedSuperlevel", "OrdinaryH0", "ElderInterval", "ElderBridge"]:  # MUTATION_ELDER_IDENTITIES','if False:  # MUTATION_ELDER_IDENTITIES',"RegisteredDomainTests.test_plan_and_configuration_cannot_replace_elder_root"),
 ("object_root_symlink",'if parent.is_symlink():  # MUTATION_ROOT_SYMLINK','if False:  # MUTATION_ROOT_SYMLINK',"CompiledObjectCustodyTests.test_symlinked_build_root_is_rejected"),
 ("object_nested_symlink",'if path.is_symlink():  # MUTATION_NESTED_SYMLINK','if False:  # MUTATION_NESTED_SYMLINK',"CompiledObjectCustodyTests.test_symlinked_nested_directory_is_rejected"),
 ("ambiguous_overlap",'len(candidates) != 1 or not isinstance(candidates[0], str)','False or not isinstance(candidates[0], str)',"IndependentCensusTests.test_ambiguous_extra_provenance_rejected"),
 ("missing_overlap",'if name not in result["module_declarations"][owner]:','if False:',"IndependentCensusTests.test_selected_overlap_missing_from_owner_rejected"),
 ("generator_anchor",'if program.count(REPLAY_OWNER_ORIGINAL) != 1:','if False:',"IndependentCensusTests.test_replay_generator_rejects_missing_original_ownership_anchor"),
 ("metadata_consistency",'if name in metadata_observations and metadata_observations[name] != observation:  # MUTATION_OVERLAP_CONSISTENCY','if False:  # MUTATION_OVERLAP_CONSISTENCY',"IndependentCensusTests.test_same_extra_name_cannot_have_inconsistent_classification")]
report={"schema":"cbz-source514-recorder-mutations-v1","threshold":"all ten source mutants in normal and optimized Python modes","source_sha256":hashlib.sha256(source.read_bytes()).hexdigest(),"executions":[],"status":"NOT_PASS"}
try:
 for mode in ["normal","optimized"]:
  optimize=["-O"] if mode=="optimized" else []
  command=[sys.executable,"-B","-S",*optimize,"-m","unittest","discover","-s","tests","-p","test_cbz_source514_hosted.py","-v"]
  result=subprocess.run(command,cwd=root,capture_output=True)
  (args.output/(mode+"-baseline.stdout")).write_bytes(result.stdout)
  (args.output/(mode+"-baseline.stderr")).write_bytes(result.stderr)
  report["executions"].append({"mode":mode,"label":"baseline","exit":result.returncode})
  if result.returncode:
   sys.stdout.buffer.write(result.stdout)
   sys.stderr.buffer.write(result.stderr)
   raise RuntimeError("unmodified recorder suite must pass before mutation")
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
 report["status"]="ALL_TEN_REASON_BOUND_MUTANTS_KILLED_IN_BOTH_MODES"
finally:
 (args.output/"REPORT.json").write_text(json.dumps(report,indent=2)+"\n")
print(report["status"])
