"""Verify exact path membership and byte custody of lifetime-parent imports."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXPECTED_PATHS = frozenset({
    "imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md",
    "imports/lifetime_parent_20260925/MARKED_CYLINDER_CAP_PROOF.md",
})


def verify(root: Path = ROOT) -> dict:
    manifest = json.loads((root / "MANIFEST.json").read_text(encoding="utf-8"))
    records = manifest["files"]
    declared = [rec["path"] for rec in records]
    # A digest match for a basename cannot authenticate a different source path,
    # and a shortened manifest must not silently verify a smaller source set.
    if len(declared) != len(EXPECTED_PATHS) or set(declared) != EXPECTED_PATHS:
        raise SystemExit("manifest path/membership mismatch for lifetime-parent imports")

    checked = []
    for rec in records:
        path = root / Path(rec["path"]).name
        data = path.read_bytes()
        actual = hashlib.sha256(data).hexdigest()
        if len(data) != rec["bytes"]:
            raise SystemExit(f"size mismatch {path.name}: {len(data)} != {rec['bytes']}")
        if actual != rec["sha256"]:
            raise SystemExit(f"sha256 mismatch {path.name}: {actual} != {rec['sha256']}")
        checked.append({"path": path.name, "bytes": len(data), "sha256": actual})
    return {"object": manifest["object"], "checked": checked, "scientific_effect": "NONE"}


def main() -> None:
    print(json.dumps(verify(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
