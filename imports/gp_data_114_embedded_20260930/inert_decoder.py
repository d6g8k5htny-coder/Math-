"""Decode one pinned public wrapper as inert data; never execute its payloads."""
import argparse
import base64
import binascii
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
import sys
import zlib


@dataclass(frozen=True)
class Identity:
    name: str
    bytes: int
    sha256: str
    blob: str = ""


@dataclass(frozen=True)
class PayloadSpec:
    label: str
    source: Identity
    gzip: Identity


WRAPPER_IDENTITY = Identity(
    "GP-DATA-114-v1.1 public wrapper", 9220,
    "948881341e610800b126623e559c9a45a6a1160a55b6fc69e172ef47ca107c37",
    "0a1a98169a5283b7a253890fe8bb54a8a91cfe71")
SPECS = (
    PayloadSpec("SOURCE", Identity(
        "GP-DATA-114-v1.0_uniform_q_degree4_interval.py", 9787,
        "9d7cb5d6e13579533c5b485775e67c77da83c149c0bf8bbbe7b7bf85aefdb4ef",
        "bbbfacee088332b4e4df9953079d579400f2282c"), Identity(
        "source gzip", 3416,
        "18c8768cf37d4557a8c04a9ae6e60523a185098012527403c0e627b259ff1e5c")),
    PayloadSpec("RECEIPT", Identity(
        "GP-DATA-114-v1.0_receipt.json", 5047,
        "8472209ee589f44f1f3c472c7040d183494743a89e21ad9487a1879d192003bc",
        "77c511eaaab0dcd7863d4eebadfd2dcc69c9cb71"), Identity(
        "receipt gzip", 1692,
        "88bb5bce0b875ac2959d7cbcaff235db7ea60249e3124faeccc0d26fe8351222")),
)


def git_blob(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()


def check_identity(raw, expected, context):
    if len(raw) != expected.bytes:
        raise ValueError(f"{context} size mismatch")
    if hashlib.sha256(raw).hexdigest() != expected.sha256:
        raise ValueError(f"{context} sha256 mismatch")
    if expected.blob and git_blob(raw) != expected.blob:
        raise ValueError(f"{context} Git blob mismatch")


def safe_basename(name):
    if not name or name in {".", ".."} or any(c in name for c in "/\\\0"):
        raise ValueError("unsafe filename")


def decode_member(compressed, spec):
    safe_basename(spec.source.name)
    check_identity(compressed, spec.gzip, "gzip")
    inflater = zlib.decompressobj(wbits=31)
    try:
        raw = inflater.decompress(compressed, spec.source.bytes + 1)
    except zlib.error as exc:
        raise ValueError("invalid gzip CRC/header/stream") from exc
    if len(raw) > spec.source.bytes or inflater.unconsumed_tail:
        raise ValueError("payload size exceeds declared limit")
    if not inflater.eof:
        raise ValueError("incomplete gzip stream")
    if inflater.unused_data:
        raise ValueError("trailing gzip bytes or concatenated member")
    check_identity(raw, spec.source, "payload")
    return raw


def declared(section, key):
    values = re.findall(r"^" + re.escape(key) + r": ([^\r\n]+)$", section, re.MULTILINE)
    if len(values) != 1:
        raise ValueError(f"declared {key} count")
    return values[0]


def decode_wrapper(raw, wrapper_identity=None):
    check_identity(raw, wrapper_identity or WRAPPER_IDENTITY, "wrapper")
    try:
        text = raw.decode("utf-8-sig").replace("\r\n", "\n")
    except UnicodeDecodeError as exc:
        raise ValueError("wrapper is not UTF-8") from exc
    result = {}
    for spec in SPECS:
        begin = f"BEGIN_{spec.label}_GZIP_BASE64"
        end = f"END_{spec.label}_GZIP_BASE64"
        if text.count(begin) != 1 or text.count(end) != 1:
            raise ValueError("marker count must be exactly one pair per payload")
        before, rest = text.split(begin)
        encoded, after = rest.split(end)
        if before.rfind("\n" + spec.label + "\n") == -1:
            raise ValueError("missing payload declaration heading")
        section = before[before.rfind("\n" + spec.label + "\n"):]
        fields = (("filename", spec.source.name), ("bytes", str(spec.source.bytes)),
                  ("sha256", spec.source.sha256), ("gzip bytes", str(spec.gzip.bytes)),
                  ("gzip sha256", spec.gzip.sha256))
        for key, expected in fields:
            if declared(section, key) != expected:
                raise ValueError(f"declared {key} mismatch")
        compact = re.sub(r"[\r\n\t ]", "", encoded)
        try:
            compressed = base64.b64decode(compact, validate=True)
        except (binascii.Error, ValueError) as exc:
            raise ValueError("invalid base64") from exc
        result[spec.source.name] = decode_member(compressed, spec)
    return result


def verify_existing(directory, decoded):
    directory = Path(directory)
    if directory.is_symlink():
        raise ValueError("directory symlink")
    for name, raw in decoded.items():
        safe_basename(name)
        path = directory / name
        if path.is_symlink():
            raise ValueError("payload symlink")
        if not path.is_file() or path.read_bytes() != raw:
            raise ValueError(f"existing payload mismatch: {name}")


def report(decoded):
    return {"scientific_effect": "NONE", "archived_code_executed": False,
            "complete_single_gzip_member_per_payload": True,
            "payloads": [{"path": name, "bytes": len(raw),
                          "sha256": hashlib.sha256(raw).hexdigest(), "git_blob": git_blob(raw)}
                         for name, raw in decoded.items()]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wrapper-input", required=True, help="Exact UTF-8 wrapper file, or '-' for stdin bytes")
    output = parser.add_mutually_exclusive_group(required=True)
    output.add_argument("--verify-existing", type=Path, help="Verify the original two payload files")
    output.add_argument("--write-new", type=Path, help="Create a NEW directory only after both payloads verify")
    args = parser.parse_args()
    try:
        raw = sys.stdin.buffer.read(65537) if args.wrapper_input == "-" else Path(args.wrapper_input).read_bytes()
        decoded = decode_wrapper(raw)
        if args.verify_existing:
            verify_existing(args.verify_existing, decoded)
        else:
            if args.write_new.is_symlink() or args.write_new.exists():
                raise ValueError("output directory must not already exist")
            args.write_new.mkdir()
            for name, payload in decoded.items():
                (args.write_new / name).write_bytes(payload)
        print(json.dumps(report(decoded), sort_keys=True))
        return 0
    except (ValueError, OSError) as exc:
        print(json.dumps({"passed": False, "error": str(exc)}, sort_keys=True), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
