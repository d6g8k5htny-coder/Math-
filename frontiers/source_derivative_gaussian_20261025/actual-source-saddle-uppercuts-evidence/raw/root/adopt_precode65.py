from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, difflib

here = Path(__file__).resolve().parent
cfg = json.loads((here / "PRECODE65_TEMPLATE.json").read_text())
drafts, frontier = Path(cfg["draft_dir"]), Path(cfg["frontier"])
stamp = datetime.now(timezone.utc).isoformat()
prepared = []
for spec in cfg["files"]:
    old = (drafts / spec["name"]).read_text()
    if old.count(spec["old"]) != 1:
        raise ValueError("Exact preamble mismatch: " + spec["name"])
    new = old.replace(spec["old"], spec["replacement"], 1)
    for a, b in cfg["more_replacements"]:
        new = new.replace(a, b)
    prepared.append((spec["name"], old, new))
contenders = {
    "stage": 65, "status": "PRECODE_ADOPTED_IMPLEMENTATION_INACTIVE",
    "adopted_utc": stamp, "qualified_baseline": cfg["baseline"],
    "future_dependency": "PUBLIC64 conditional/unqualified until qualification and publication",
    "proposed_module": "SourceActualSaddleUppercuts",
    "sole_public_Prop": "actualSource_quotient_saddle_uniform_closed_uppercuts",
    "public_data_global_instances": 0,
    "coordination": "Design adoption only; no native65 claim, author seat, GO, code or timer. Fresh reconciliation/claim required before implementation.",
    "active_unit": "64 creator6478705132; hard22:30UTC28Oct/end unchanged",
    "mathematical_scope": "One future public64 witness; SAMEphi all inherited nonnegative lower traces and uniform positive CLOSED uppercuts for0<eps<rho^2/4",
    "sole_mutation": "ONLYeps>0 to eps>=0; SAMEupperbound/chart/source/field/carrier/CLOSEDcuts; independent structural inverse vertical path at0, not inheritedlowerPC shortcut",
    "review": "/workspace/scratch/actual-source-saddle-uppercuts-source-review/PRECODE_REVIEW.md PASS_PRECODE_DESIGN/noamendments",
    "roles": "Unassigned future implementation. Atmost1optional private finitegeometry TEXT author; futureproducer owns transport/assembly/actualfixtures/ordinary/negative/executions.",
    "publication": "EXTRA with next qualified64 publication, excluded64 manifest/archive/registry; not a separate docs-only publication",
    "owner_reuse": "Completed applicable verification reused; no new agent/session/head/handoff replay; provider process separate",
    "science": "NONE/samefamily0/OpenDraft/noReady/noMerge",
    "global_gaps": "Regularcollars/finiteadjacency/lowerclopenseparation/actualcriticalevents/exhaustiveH0/elder/oncecount/Borel/Rice/PairLaw/Parent OPEN"
}
prepared.append(("SOURCE_ACTUAL_SADDLE_UPPERCUTS_CONTENDERS.json", "", json.dumps(contenders, indent=2) + "\n"))
patchdir = here / "adoption-patches"
patchdir.mkdir(exist_ok=True)
ids = []
for name, old, new in prepared:
    data = new.encode()
    (here / name).write_bytes(data)
    (frontier / name).write_bytes(data)
    (patchdir / (name + ".patch")).write_text("".join(difflib.unified_diff(old.splitlines(True), new.splitlines(True), fromfile="draft/" + name, tofile="proper/" + name)))
    ids.append({"path": str(frontier / name), "scratch_copy": str(here / name), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(), "identity_origin": "FIRST new proper payload ID once, exact known byte copies reuse"})
record = {
    "adopted_utc": stamp, "status": "ROOT_PRECODE65_ADOPTED_BEFORE_ANY65CODE",
    "root_reading": "FULLthree initial drafts untruncated8523tokens and FULLindependentPRECODE_REVIEW2507tokens; priorFULLdesignreports+deltas reused",
    "review": "PASS_PRECODE_DESIGN/no findings or amendments",
    "actual_changes": "Exact adoption preambles and implementation-gate wording only, full per-file patches retained; mathematical/control scope unchanged",
    "proper_documents": ids,
    "publication": "PENDING EXTRAwith64metadata; excluded64manifest/archive/registry",
    "future64": "UNQUALIFIED until qualification and publication; no65importavailability claim",
    "implementation": "INACTIVE/no65source/helperproof/harness/claim/GO/seat/timer",
    "roles": "Rootcontractadoption/metadata only; draftauthor+reviewer no65proofauthorship; futureproducerunassigned",
    "owner_reuse": "No mathematical verification, oldhash/check/object/CI replay; FOURnew proper payload IDs first-calculated once",
    "science": "NONE/samefamily0/OpenDraft/noReady/noMerge"
}
(here / "PRECODE65_IDENTITIES.json").write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps(record, indent=2))
