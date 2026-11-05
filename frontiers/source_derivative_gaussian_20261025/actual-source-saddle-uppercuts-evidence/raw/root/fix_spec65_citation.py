from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, difflib
p = Path(__file__).resolve().parent
name = "SOURCE_ACTUAL_SADDLE_UPPERCUTS.md"
front = Path("/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025") / name
old = (p / name).read_text()
a = "The accepted design basis is\n`../REPORT.md` and `../DESIGN_DELTA.md`, retained unchanged as dated history.\n"
b = "The accepted design basis is retained unchanged as dated local adoption\nevidence in `/workspace/scratch/actual-source-saddle-uppercuts-preflight/REPORT.md`\nand its `DESIGN_DELTA.md`; independent review is retained under\n`/workspace/scratch/actual-source-saddle-uppercuts-source-review/`.\n"
if old.count(a) != 1:
    raise ValueError("Exact historical draft citation mismatch")
history = p / "history"
history.mkdir(exist_ok=True)
(history / "SPEC65.001.md").write_text(old)
new = old.replace(a, b, 1)
data = new.encode()
(p / name).write_bytes(data)
front.write_bytes(data)
patch = "".join(difflib.unified_diff(old.splitlines(True), new.splitlines(True), fromfile="proper/SPEC65.001.md", tofile="proper/SPEC65.002.md"))
(p / "adoption-patches" / "SPEC65-citation-002.patch").write_text(patch)
record = {
    "recorded_utc": datetime.now(timezone.utc).isoformat(),
    "scope": "Citation-only documentation correction; initial draft-relative parentREPORT references do not resolve from the adopted frontier",
    "actual_change": "Explicit local design/report/review evidence locations, no mathematical/public/control/role/timer change",
    "prior_ID": "PRECODE65_IDENTITIES.json initialSPEC8871B47566c5645adeca97ce357f41790950a9dbf8b5c138d7fed7eb2a2959f8402b8 retained unchanged",
    "prior_payload": str(history / "SPEC65.001.md"),
    "new_SPEC": {"path": str(front), "scratch_copy": str(p / name), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(), "origin": "FIRST new citation-amended payload ID once; exact byte copies reuse"},
    "patch": "adoption-patches/SPEC65-citation-002.patch",
    "all_other_proper65_IDs": "REUSE PRECODE65_IDENTITIES.json unchanged",
    "implementation": "INACTIVE/no65code/claim/GO/seat/timer",
    "publication": "PENDING EXTRAwithqualified64metadata,excluded64manifest/archive/registry"
}
(p / "PRECODE65_CITATION_AMENDMENT_001.json").write_text(json.dumps(record, indent=2) + "\n")
print(patch)
print(json.dumps(record, indent=2))
