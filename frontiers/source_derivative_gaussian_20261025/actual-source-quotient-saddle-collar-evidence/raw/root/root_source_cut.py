from pathlib import Path
from datetime import datetime, timezone
import subprocess, json, shutil, sys, traceback
pub = Path(__file__).resolve().parent
started = datetime.now(timezone.utc).isoformat()
repo = Path("/workspace/Math-curvature-20261026")
construct = Path("/workspace/scratch/actual-source-quotient-saddle-collar-construct")
rel = "frontiers/source_derivative_gaussian_20261025/SourceActualQuotientSaddleCollar.lean"
baseline = "f4825c3e3bd0e2d2c46157096e76b9ab17dbbb71"
outer = {"command": ["python3", str(Path(__file__).resolve())], "cwd": "/workspace", "started_utc_observed_inside_process": started, "stdout": str(pub / "ROOT_SOURCE_CUT_OUTER.stdout.txt"), "stderr": str(pub / "ROOT_SOURCE_CUT_OUTER.stderr.txt"), "scope": "RootGit/sourcecut and exactlyone newownobject bytecopy; no mathematicalcheck/hash/replay"}
commands = []
def git(label, args):
    cmd = ["git", "-C", str(repo)] + args
    a = datetime.now(timezone.utc).isoformat()
    r = subprocess.run(cmd, cwd="/workspace", capture_output=True)
    b = datetime.now(timezone.utc).isoformat()
    (pub / (label + ".stdout.txt")).write_bytes(r.stdout)
    (pub / (label + ".stderr.txt")).write_bytes(r.stderr)
    row = {"label": label, "command": cmd, "cwd": "/workspace", "started_utc": a, "ended_utc": b, "exit_code": r.returncode, "stdout": str(pub / (label + ".stdout.txt")), "stderr": str(pub / (label + ".stderr.txt"))}
    commands.append(row)
    (pub / "ROOT_SOURCE_CUT_COMMANDS.json").write_text(json.dumps(commands, indent=2) + "\n")
    if r.returncode: raise RuntimeError("Gitfailed " + label)
    return r.stdout.decode().strip()
try:
    if (pub / "ROOT_SOURCE_CUT.json").exists() or (pub / "ROOT_OWN_OBJECT_COPY.json").exists():
        raise RuntimeError("Sourcecut/copy alreadyrecorded: no duplicateaction")
    receipts = {x: json.loads((construct / "runs" / x / "receipt.json").read_text()) for x in ["fixtures-002", "inventory-001", "kernel-001"]}
    if len(list((construct / "runs").glob("kernel-*/receipt.json"))) != 1 or any(r["exit_code"] != 0 for r in receipts.values()):
        raise RuntimeError("Newqualificationrecord preconditionfailed")
    ids = json.loads((construct / "FINAL_SOURCE_OBJECT_IDS.PRE_KERNEL.json").read_text())
    src_id, obj_id = ids["source"], ids["object"]
    if src_id["sha256"] != "e0e0a0f77bd75bbbd8994d620ee43b18b2edd50d7649cd8cb9837e7148762265" or obj_id["sha256"] != "a57489eb917c4f2fd4d314ab5f7ae9dea60619caf9160e044700114551c1e15e":
        raise RuntimeError("Unexpected recordedidentity")
    for r in receipts.values():
        for name, identity in [(src_id["path"], src_id), (obj_id["path"], obj_id)]:
            if r["after"][name]["sha256"] != identity["sha256"]:
                raise RuntimeError("Actualreceiptbinding mismatch")
    if Path(src_id["path"]).stat().st_size != src_id["bytes"] or Path(obj_id["path"]).stat().st_size != obj_id["bytes"]:
        raise RuntimeError("Frozensizemetadata mismatch; do notrehash")
    scope = json.loads(Path("/workspace/scratch/actual-source-quotient-saddle-collar-source-review/scope.json").read_text())
    if scope["verdicts"]["full_production_source"] != "PASS" or scope["verdicts"]["complete_owned_inventory_std3"] != "PASS":
        raise RuntimeError("Requiredactualreviewmissing")
    parent = git("SOURCE_CUT_01", ["rev-parse", "HEAD"])
    if parent != baseline: raise RuntimeError("Unexpectedlocalparent")
    git("SOURCE_CUT_02", ["add", "--", rel])
    git("SOURCE_CUT_03", ["commit", "--only", "-m", "Formalize actual quotient saddle collar and local branches", "--", rel])
    cut = git("SOURCE_CUT_04", ["rev-parse", "HEAD"])
    committed_parent = git("SOURCE_CUT_05", ["rev-parse", "HEAD^"])
    blob = git("SOURCE_CUT_06", ["rev-parse", "HEAD:" + rel])
    changed = git("SOURCE_CUT_07", ["diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD"])
    if committed_parent != parent or changed != rel: raise RuntimeError("Source-onlycut ownershipmismatch")
    cut_record = {"recorded_utc": datetime.now(timezone.utc).isoformat(), "source_cut": cut, "parent": parent, "qualified_baseline": baseline, "source_path": rel, "source_blob": blob, "source_identity_reused": src_id, "only_new_source_committed": True, "future65_EXTRAnotcommitted": True, "publication": "LOCALONLY ordinary/custody/finalmetadata stillpending", "mathematical_checks": 0, "payload_hashes": 0}
    (pub / "ROOT_SOURCE_CUT.json").write_text(json.dumps(cut_record, indent=2) + "\n")
    dest = repo / "frontiers/source_derivative_gaussian_20261025/.lake/build/lib/lean/SourceActualQuotientSaddleCollar.olean"
    if dest.exists(): raise RuntimeError("Newownobjectdestinationunexpectedlyexists; no overwrite/secondcopy")
    intent = {"created_utc": datetime.now(timezone.utc).isoformat(), "source_cut": cut, "source": obj_id["path"], "destination": str(dest), "source_identity": src_id, "eligible_own_object_identity": obj_id, "qualification_receipts": {k: {"receipt": str(construct / "runs" / k / "receipt.json"), "started_utc": v["started_utc"], "ended_utc": v["ended_utc"], "exit_code": v["exit_code"]} for k,v in receipts.items()}, "copy_once": True, "copy_scope": "ONLYnewfinal64own.olean; nohelper/Controls/ilean/oldobject", "all_further_copy_actions": "SKIP"}
    (pub / "ROOT_OWN_OBJECT_COPY_INTENT.json").write_text(json.dumps(intent, indent=2) + "\n")
    shutil.copyfile(obj_id["path"], dest)
    done = dict(intent, completed_utc=datetime.now(timezone.utc).isoformat(), action="COPIED_ONCE", destination_size_metadata=dest.stat().st_size, identity_reused_no_rehash=obj_id["sha256"], mathematical_checks=0, payload_hashes=0, old_object_copies=0, helper_or_controls_copies=0, ilean_copies=0)
    (pub / "ROOT_OWN_OBJECT_COPY.json").write_text(json.dumps(done, indent=2) + "\n")
    print(json.dumps({"source_cut": cut_record, "own_object_copy": done}, indent=2))
    outer["exit_code"] = 0
except BaseException:
    outer["exit_code"] = 1
    traceback.print_exc()
finally:
    outer["ended_utc_observed_inside_process"] = datetime.now(timezone.utc).isoformat()
    (pub / "ROOT_SOURCE_CUT_OUTER.json").write_text(json.dumps(outer, indent=2) + "\n")
sys.exit(outer["exit_code"])
