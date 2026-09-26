"""Verify byte custody of the imported lifetime-parent sources."""
from __future__ import annotations
import hashlib, json
from pathlib import Path

ROOT=Path(__file__).resolve().parent

def main():
    manifest=json.loads((ROOT/"MANIFEST.json").read_text())
    checked=[]
    for rec in manifest["files"]:
        path=ROOT/Path(rec["path"]).name
        data=path.read_bytes()
        actual=hashlib.sha256(data).hexdigest()
        if len(data)!=rec["bytes"]:
            raise SystemExit(f"size mismatch {path.name}: {len(data)} != {rec['bytes']}")
        if actual!=rec["sha256"]:
            raise SystemExit(f"sha256 mismatch {path.name}: {actual} != {rec['sha256']}")
        checked.append({"path":path.name,"bytes":len(data),"sha256":actual})
    print(json.dumps({"object":manifest["object"],"checked":checked,"scientific_effect":"NONE"},indent=2,sort_keys=True))

if __name__=="__main__":
    main()
