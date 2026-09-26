"""Verify byte custody of the hardening-commit proof imports.

Scientific effect: NONE. This checks sizes, SHA256 digests, and git blob
identities. It does not interpret proofs or change claim status.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
BEGIN = b"----- BEGIN GITHUB ISSUE BODY -----\n"
END = b"\n----- END GITHUB ISSUE BODY -----\n"


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def fail(message: str) -> None:
    raise SystemExit(message)


def check_byte_copy(rec: dict) -> dict:
    if rec.get("kind") != "BYTE_COPY":
        fail(f"{rec.get('id')} is not a byte copy")
    path = ROOT / rec["destination"]
    if not path.is_file() or path.is_symlink():
        fail(f"missing regular file: {rec['destination']}")
    data = path.read_bytes()
    actual = hashlib.sha256(data).hexdigest()
    if len(data) != rec["bytes"]:
        fail(f"size mismatch {rec['id']}: {len(data)} != {rec['bytes']}")
    if actual != rec["sha256"]:
        fail(f"sha256 mismatch {rec['id']}: {actual} != {rec['sha256']}")
    blob = git_blob_sha1(data)
    if blob != rec["source_blob"]:
        fail(f"git blob mismatch {rec['id']}: {blob} != {rec['source_blob']}")
    if rec.get("source_label_adopted") is not False:
        fail(f"{rec['id']} must not adopt the source label")
    return {"id": rec["id"], "bytes": len(data), "sha256": actual, "blob": blob}


def check_transcription(rec: dict) -> dict:
    if rec.get("kind") != "TRANSCRIPTION" or rec.get("not_original_bytes") is not True:
        fail("issue 59 carrier must be labeled as a transcription")
    path = ROOT / rec["destination"]
    if not path.is_file() or path.is_symlink():
        fail(f"missing regular file: {rec['destination']}")
    data = path.read_bytes()
    actual = hashlib.sha256(data).hexdigest()
    if len(data) != rec["destination_bytes"] or actual != rec["destination_sha256"]:
        fail("issue 59 carrier bytes drifted")
    start = data.find(BEGIN)
    if start < 0:
        fail("issue 59 begin marker missing")
    body_start = start + len(BEGIN)
    body_end = data.find(END, body_start)
    if body_end < 0:
        fail("issue 59 end marker missing")
    body = data[body_start:body_end]
    if hashlib.sha256(body).hexdigest() != rec["body_sha256"]:
        fail("issue 59 body sha256 mismatch")
    if len(body) != rec["body_utf8_bytes"]:
        fail("issue 59 body byte count mismatch")
    text = body.decode("utf-8")
    if len(text) != rec["body_characters"]:
        fail("issue 59 body character count mismatch")
    if body == data:
        fail("issue 59 carrier must not be only the original body")
    carrier_text = data.decode("utf-8")
    if "not the original bytes" not in carrier_text:
        fail("issue 59 carrier must say it is not the original bytes")
    for comment in rec["comments"]:
        if str(comment["id"]) not in carrier_text or comment["html_url"] not in carrier_text:
            fail(f"issue 59 comment identity missing: {comment['id']}")
    if rec.get("source_label_adopted") is not False:
        fail("issue 59 must not adopt a source label")
    return {"id": rec["id"], "body_sha256": rec["body_sha256"], "carrier_sha256": actual}


def main() -> None:
    manifest = json.loads((HERE / "MANIFEST.json").read_text(encoding="utf-8"))
    if manifest.get("scientific_effect") != "NONE":
        fail("scientific_effect must stay NONE")
    readme = (HERE / "README.md").read_text(encoding="utf-8")
    checked = [check_byte_copy(rec) for rec in manifest["byte_copies"]]
    transcribed = [check_transcription(rec) for rec in manifest["transcriptions"]]
    for rec in manifest["byte_copies"] + manifest["transcriptions"]:
        if rec["destination"] not in readme:
            fail(f"ledger omits {rec['destination']}")
    print(json.dumps({
        "object": manifest["object"],
        "checked": checked,
        "transcribed": transcribed,
        "scientific_effect": "NONE",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
