#!/usr/bin/env python3
"""Bounded source/inventory checks. A PASS never grants kernel proof credit."""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import sys
import unicodedata

MAX_FILE_BYTES = 2 * 1024 * 1024
MAX_TOTAL_BYTES = 64 * 1024 * 1024
MAX_FILES = 10000
MAX_ROOTS = 1000
MAX_INVENTORY_ENTRIES = 20000
MAX_TOKENS = 500000
MAX_COMMENT_DEPTH = 256
MAX_ISSUES = 2000
MAX_DEPENDENCY_DEPTH = 512
MAX_RATIONAL_DIGITS = 1000
MAX_INEQUALITIES = 10000
FORBIDDEN = {"sorry", "admit", "sorryAx", "native_decide", "axiom",
             "native", "ofReduceBool", "ofReduceNat", "unsafe", "extern", "implemented_by",
             "skipKernel", "skipKernelTC", "addDeclWithoutChecking"}
METAPROGRAMMING = {"macro", "macro_rules", "elab", "elab_rules", "syntax", "notation",
                  "infix", "infixl", "infixr", "prefix", "postfix", "declare_syntax_cat",
                  "opaque", "constant", "constants", "run_tac", "run_elab", "run_cmd", "run_meta",
                  "initialize", "builtin_initialize"}
KINDS = {"lean_proof", "lean_auditor", "rational_certificate", "operational_record", "operational_source", "unsupported"}
SHA = re.compile(r"[0-9a-f]{64}\Z")
RATIONAL = re.compile(r"(-?(?:0|[1-9][0-9]*))(?:/([1-9][0-9]*))?\Z")
RAW_STRING = re.compile(r'r(#*)"')
INTEGER = re.compile(r'[0-9](?:_?[0-9])*')
NUMBER = re.compile(r'[0-9](?:_?[0-9])*(?:\.[0-9_]*(?:[eE][+-]?[0-9][0-9_]*)?|[eE][+-]?[0-9][0-9_]*)?')
Q_FIELDS = {"id", "title", "layer_a_status", "exact_boundary", "blocking_reason", "attempted",
            "resumption_cost", "isolation", "owner", "maintenance", "location"}


class Reject(Exception):
    def __init__(self, code, message, path="", line=1, column=1):
        self.issue = dict(code=code, message=message, path=path, line=line, column=column, severity="error")
        super().__init__(message)


@dataclass(frozen=True)
class Token:
    kind: str
    value: str
    line: int
    column: int


def require(condition, code, message, path="", line=1, column=1):
    if not condition:
        raise Reject(code, message, path, line, column)


def no_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key: " + key)
        result[key] = value
    return result


def load_json(data, path):
    def invalid_constant(value):
        raise ValueError("nonfinite JSON constant: " + value)
    try:
        result = json.loads(data, object_pairs_hook=no_duplicate_keys, parse_constant=invalid_constant)
        def finite(value):
            if isinstance(value, str):
                value.encode("utf-8", "strict")
            if isinstance(value, float) and not math.isfinite(value):
                raise ValueError("nonfinite JSON float")
            if isinstance(value, dict):
                for x, y in value.items(): finite(x); finite(y)
            elif isinstance(value, list):
                for x in value: finite(x)
        finite(result)
        return result
    except (ValueError, UnicodeError, RecursionError) as exc:
        raise Reject("INVALID_JSON", str(exc), path) from exc


def canonical_path(value):
    return (type(value) is str and 0 < len(value) <= 1024 and "\\" not in value
            and not any(unicodedata.category(c).startswith("C") for c in value)
            and not value.startswith("/") and all(x not in ("", ".", "..") and len(x.encode("utf-8")) <= 255 for x in value.split("/")))


def has_symlink(path):
    require(len(str(path)) <= 4096, "RESOURCE_LIMIT", "filesystem path length exceeded", str(path)[:200])
    try:
        return any(part.is_symlink() for part in [path, *path.parents])
    except OSError as exc:
        raise Reject("FILESYSTEM_ERROR", str(exc), str(path)) from exc


def read_bounded(path, label):
    require(not has_symlink(path), "SYMLINK", "symlink file or ancestor", label)
    try:
        with path.open("rb") as stream:
            data = stream.read(MAX_FILE_BYTES + 1)
    except OSError as exc:
        raise Reject("MISSING_FILE", str(exc), label) from exc
    require(len(data) <= MAX_FILE_BYTES, "RESOURCE_LIMIT", "file exceeds byte limit", label)
    return data


def ident_start(c):
    return c == "_" or unicodedata.category(c).startswith("L")


def ident_continue(c):
    return ident_start(c) or c == "'" or unicodedata.category(c)[0] in "MN"


def valid_module(value):
    return (type(value) is str and bool(value) and all(
        bool(part) and ident_start(part[0]) and all(ident_continue(c) for c in part[1:])
        for part in value.split(".")))


def lex_lean(text, path):
    """A conservative Lean lexical subset; embedded string-macro terms are not trusted."""
    tokens, index, line, column = [], 0, 1, 1
    length = len(text)
    def consume(end):
        nonlocal index, line, column
        part = text[index:end]
        if "\n" in part:
            line += part.count("\n"); column = len(part.rsplit("\n", 1)[1]) + 1
        else:
            column += len(part)
        index = end
    def emit(kind, value, start_line, start_column):
        require(len(tokens) < MAX_TOKENS, "RESOURCE_LIMIT", "token limit exceeded", path, start_line, start_column)
        tokens.append(Token(kind, value, start_line, start_column))
    while index < length:
        c, start_line, start_column = text[index], line, column
        if c.isspace():
            consume(index + 1); continue
        if text.startswith("--", index):
            end = text.find("\n", index + 2); consume(length if end < 0 else end); continue
        if text.startswith("/-", index):
            depth, end = 1, index + 2
            while end < length and depth:
                if text.startswith("/-", end): depth += 1; end += 2
                elif text.startswith("-/", end): depth -= 1; end += 2
                else: end += 1
                require(depth <= MAX_COMMENT_DEPTH, "RESOURCE_LIMIT", "nested comment depth exceeded", path, start_line, start_column)
            require(depth == 0, "LEXICAL_ERROR", "unterminated block comment", path, start_line, start_column)
            consume(end); continue
        require(not text.startswith("-/", index), "LEXICAL_ERROR", "unexpected block-comment terminator", path, line, column)
        raw = RAW_STRING.match(text, index) if c == "r" else None
        if raw:
            begin = raw.end(); delimiter = '"' + raw.group(1)
            end = text.find(delimiter, begin)
            require(end >= 0, "LEXICAL_ERROR", "unterminated raw string", path, line, column)
            emit("STRING", text[begin:end], line, column); consume(end + len(delimiter)); continue
        if c == '"':
            begin, end = index + 1, index + 1
            while end < length:
                if text[end] == "\\": end += 2
                elif text[end] == '"': break
                else: end += 1
            require(end < length, "LEXICAL_ERROR", "unterminated string", path, line, column)
            emit("STRING", text[begin:end], line, column); consume(end + 1); continue
        if text.startswith("''", index) or text.startswith("⁻¹'", index):
            notation = "''" if c == "'" else "⁻¹'"
            emit("PUNCT", notation, line, column); consume(index + len(notation)); continue
        if c == "'":
            end = index + 1
            while end < length and text[end] != "\n":
                if text[end] == "\\": end += 2
                elif text[end] == "'": break
                else: end += 1
            require(end < length and text[end] == "'", "LEXICAL_ERROR", "unterminated character literal", path, line, column)
            content = text[index + 1:end]
            require(len(content) == 1 or (content.startswith("\\") and len(content) > 1),
                    "LEXICAL_ERROR", "unsupported character literal", path, line, column)
            emit("CHAR", content, line, column); consume(end + 1); continue
        if c == "«":
            end = text.find("»", index + 1)
            require(end >= 0, "LEXICAL_ERROR", "unterminated escaped identifier", path, line, column)
            value = text[index + 1:end]
            require(bool(value) and not any(unicodedata.category(x).startswith("C") for x in value),
                    "LEXICAL_ERROR", "unsupported escaped identifier", path, line, column)
            emit("QIDENT", value, line, column); consume(end + 1); continue
        if ident_start(c):
            end = index + 1
            while end < length and ident_continue(text[end]): end += 1
            emit("IDENT", text[index:end], line, column); consume(end); continue
        if c.isascii() and c.isdigit():
            # After a projection dot, 2.1 is two integer projections, not a decimal.
            pattern = INTEGER if tokens and tokens[-1].value == "." else NUMBER
            match = pattern.match(text, index)
            emit("NUMBER", match.group(), line, column); consume(match.end()); continue
        require(not unicodedata.category(c).startswith("C"), "LEXICAL_ERROR", "unsupported control/format character", path, line, column)
        pair = text[index:index + 2]
        punctuation = pair if pair in {":=", "=>", "->", "<-"} else c
        emit("PUNCT", punctuation, line, column); consume(index + len(punctuation))
    return tokens


def scan_lean(data, entry):
    path, kind = entry["path"], entry["kind"]
    try: text = data.decode("utf-8", "strict")
    except UnicodeError as exc: raise Reject("LEXICAL_ERROR", "invalid UTF-8", path) from exc
    tokens = lex_lean(text, path)
    issues, imports, stack = [], [], []
    def issue(code, message, token):
        require(len(issues) < MAX_ISSUES, "RESOURCE_LIMIT", "issue limit exceeded", path, token.line, token.column)
        issues.append(dict(code=code, message=message, path=path, line=token.line, column=token.column, severity="error"))
    for index, token in enumerate(tokens):
        if token.kind in {"IDENT", "QIDENT"}:
            if token.value in FORBIDDEN:
                issue("FORBIDDEN_TOKEN", "prohibited Lean identifier: " + token.value, token)
            if kind == "lean_proof" and token.value in METAPROGRAMMING:
                issue("UNSUPPORTED_METAPROGRAMMING", "proof metaprogramming requires separate execution review: " + token.value, token)
            if kind == "lean_proof" and token.value in {"Float", "Float32", "Float64"}:
                issue("INEXACT_PROOF_NUMBER", "direct floating proof representation unsupported", token)
            if index + 2 < len(tokens) and tokens[index + 1].value == "!" and tokens[index + 2].kind == "STRING":
                literal = tokens[index + 2]
                simple = re.sub(r'\{[^{}]+\}', '', literal.value)
                expressions = re.findall(r'\{([^{}]+)\}', literal.value)
                acceptable = token.value == "s" and "{" not in simple and "}" not in simple and all(valid_module(x) for x in expressions)
                for expression in expressions:
                    if valid_module(expression) and any(part in FORBIDDEN for part in expression.split(".")):
                        issue("FORBIDDEN_TOKEN", "prohibited executable string interpolation: " + expression, token)
                if kind == "lean_proof" or not acceptable:
                    issue("UNSUPPORTED_STRING_MACRO", "embedded string-macro code is outside the supported proof subset", token)
        if token.kind == "PUNCT":
            if token.value in ("(", "[", "{", "⟨"): stack.append(token)
            elif token.value in (")", "]", "}", "⟩"):
                expected = {")": "(", "]": "[", "}": "{", "⟩": "⟨"}[token.value]
                if not stack or stack[-1].value != expected:
                    issue("LEXICAL_ERROR", "unbalanced delimiter", token)
                else: stack.pop()
            if kind == "lean_proof" and token.value == "`":
                issue("UNSUPPORTED_METAPROGRAMMING", "syntax/name quotations require separate execution review", token)
    for token in stack: issue("LEXICAL_ERROR", "unclosed delimiter", token)
    if tokens and tokens[-1].value in {"by", ":=", "=>", "where", ":", "import"}:
        issue("TRUNCATED_SOURCE", "incomplete terminal source construct", tokens[-1])
    lines = {}
    for token in tokens: lines.setdefault(token.line, []).append(token)
    header = True
    prelude = False
    for group in lines.values():
        start = 1 if len(group) > 1 and group[0].value in {"public", "private"} else 0
        if group[start].value == "prelude" and start == 0 and len(group) == 1 and header:
            prelude = True; continue
        if group[start].value != "import":
            if any(t.kind == "IDENT" and t.value == "import" for t in group):
                issue("UNSUPPORTED_IMPORT", "import outside a supported header", group[0])
            header = False; continue
        if not header:
            issue("UNSUPPORTED_IMPORT", "late import outside source header", group[start])
        cursor = start + 1
        if cursor == len(group): issue("UNSUPPORTED_IMPORT", "empty import command", group[start])
        while cursor < len(group):
            token = group[cursor]
            if token.kind != "IDENT" or not valid_module(token.value):
                issue("UNSUPPORTED_IMPORT", "unsupported module syntax", token); break
            parts = [token.value]; cursor += 1
            while cursor < len(group) and group[cursor].value == ".":
                cursor += 1
                if cursor == len(group) or group[cursor].kind != "IDENT" or not valid_module(group[cursor].value):
                    issue("UNSUPPORTED_IMPORT", "incomplete module name", token); break
                parts.append(group[cursor].value); cursor += 1
            imports.append((".".join(parts), token.line, token.column))
    if not prelude: imports.append(("Init", 1, 1))
    return issues, imports


def validate_manifest(manifest):
    require(type(manifest) is dict and set(manifest) == {"schema", "roots", "external_imports", "files"}
            and manifest["schema"] == "cbz-layer-a-manifest-v1", "INVALID_MANIFEST", "unsupported manifest schema/fields")
    roots, files, external = manifest["roots"], manifest["files"], manifest["external_imports"]
    require(type(roots) is list and 0 < len(roots) <= MAX_ROOTS and all(canonical_path(x) for x in roots)
            and len(set(roots)) == len(roots), "INVALID_MANIFEST", "roots must be distinct canonical relative directories")
    root_set = set(roots)
    require(not any(parent.as_posix() in root_set for scope in roots for parent in PurePosixPath(scope).parents),
            "INVALID_MANIFEST", "overlapping inventory roots")
    require(type(files) is list and 0 < len(files) <= MAX_FILES, "INVALID_MANIFEST", "empty/oversize file inventory")
    require(type(external) is dict and len(external) <= MAX_FILES, "INVALID_MANIFEST", "external imports must be a bounded exact map")
    for module, trust in external.items():
        require(valid_module(module) and type(trust) is dict and set(trust) == {"identity", "reason"}
                and all(type(x) is str and bool(x.strip()) for x in trust.values()),
                "INVALID_MANIFEST", "every external module needs an identity and reason")
    entries, modules = {}, {}
    for entry in files:
        require(type(entry) is dict and type(entry.get("kind")) is str and entry["kind"] in KINDS,
                "INVALID_MANIFEST", "unsupported file kind")
        lean = entry["kind"] in {"lean_proof", "lean_auditor"}
        require(set(entry) == ({"path", "sha256", "kind", "module"} if lean else {"path", "sha256", "kind"}),
                "INVALID_MANIFEST", "unsupported entry fields")
        path = entry["path"]
        require(canonical_path(path) and any(path.startswith(x + "/") for x in roots)
                and type(entry["sha256"]) is str and SHA.fullmatch(entry["sha256"]) is not None,
                "INVALID_MANIFEST", "noncanonical path or invalid file hash", str(path))
        require(path not in entries, "INVALID_MANIFEST", "duplicate file path", path)
        require((PurePosixPath(path).suffix == ".lean") == lean, "INVALID_MANIFEST", "Lean extension/role mismatch", path)
        if lean:
            module = entry["module"]
            require(valid_module(module), "INVALID_MANIFEST", "invalid module identifier", path)
            require(module not in modules, "DUPLICATE_MODULE", "duplicate local module: " + module, path)
            search_root = next(x for x in roots if path.startswith(x + "/"))
            expected_module = path[len(search_root) + 1:-5].replace("/", ".")
            require(module == expected_module, "MODULE_PATH_MISMATCH", "module must match its path below the declared search root", path)
            require(module not in external, "EXTERNAL_SHADOW", "external import shadows local module: " + module, path)
            modules[module] = path
        entries[path] = entry
    return roots, entries, modules, external


def quarantine_matches(root, quarantine, entries):
    require(type(quarantine) is dict and set(quarantine) == {"schema", "entries"}
            and quarantine["schema"] == "cbz-quarantine-v1" and type(quarantine["entries"]) is list,
            "INVALID_QUARANTINE", "unsupported quarantine schema")
    require(len(quarantine["entries"]) <= MAX_FILES, "INVALID_QUARANTINE", "quarantine record limit exceeded")
    matched, ids, outside, obligations = {}, set(), [], []
    for record in quarantine["entries"]:
        require(type(record) is dict and set(record) == Q_FIELDS, "INVALID_QUARANTINE", "quarantine record fields do not match canonical schema")
        require(all(type(record[x]) is str and bool(record[x].strip()) for x in Q_FIELDS - {"location"})
                and record["owner"] == "none" and record["maintenance"] == "zero",
                "INVALID_QUARANTINE", "quarantine requires full boundaries, owner none and maintenance zero")
        require(record["id"] not in ids, "INVALID_QUARANTINE", "duplicate quarantine ID")
        ids.add(record["id"])
        require(type(record["location"]) is list and bool(record["location"]), "INVALID_QUARANTINE", "empty location array")
        for loc in record["location"]:
            require(type(loc) is dict and set(loc) == {"path", "sha256", "scope"}
                    and type(loc["path"]) is str and bool(loc["path"])
                    and type(loc["sha256"]) is str and SHA.fullmatch(loc["sha256"]) is not None
                    and type(loc["scope"]) is str and loc["scope"] in {"file", "directory", "repo-ref", "obligation"},
                    "INVALID_QUARANTINE", "invalid quarantine location")
            if loc["scope"] == "repo-ref":
                outside.append({"id": record["id"], **loc}); continue
            location_path = loc["path"]
            target = None
            if loc["scope"] == "obligation":
                location_path, separator, target = location_path.rpartition("#")
                require(bool(separator) and 0 < len(target) <= 2048
                        and not any(unicodedata.category(c).startswith("C") for c in target),
                        "INVALID_QUARANTINE", "obligation needs a named source fragment")
            require(len(location_path) <= 4096, "INVALID_QUARANTINE", "filesystem location exceeds path limit")
            raw = Path(location_path)
            require(".." not in raw.parts and "\\" not in loc["path"] and "\x00" not in loc["path"],
                    "INVALID_QUARANTINE", "noncanonical quarantine path")
            if raw.is_absolute():
                absolute = raw
            else:
                require(canonical_path(location_path), "INVALID_QUARANTINE", "noncanonical quarantine path")
                absolute = root / raw
            if loc["scope"] == "directory":
                require(not has_symlink(absolute), "INVALID_QUARANTINE", "directory quarantine may not use symlink aliases")
                require(not any((root / path).is_relative_to(absolute) for path in entries),
                        "INVALID_QUARANTINE", "active-directory exclusions need individual file boundaries", location_path)
            try: relative = absolute.relative_to(root).as_posix()
            except ValueError:
                outside.append({"id": record["id"], **loc}); continue
            if loc["scope"] == "directory":
                require(not any(x == relative or x.startswith(relative + "/") for x in entries),
                        "INVALID_QUARANTINE", "active-directory exclusions need individual file boundaries", relative)
                outside.append({"id": record["id"], **loc}); continue
            if relative not in entries:
                outside.append({"id": record["id"], **loc}); continue
            if loc["scope"] == "obligation":
                require(loc["sha256"] == entries[relative]["sha256"], "QUARANTINE_HASH_MISMATCH", "obligation source hash differs from inventory", relative)
                require(entries[relative]["kind"].startswith("lean_"), "INVALID_QUARANTINE", "obligation must identify Lean source", relative)
                require(valid_module(target.replace("::", ".")), "INVALID_QUARANTINE", "unsupported Lean obligation fragment", relative)
                obligations.append({"id": record["id"], "path": relative, "declaration": target,
                                    "exact_boundary": record["exact_boundary"], "blocking_reason": record["blocking_reason"]})
                continue
            require(relative not in matched, "INVALID_QUARANTINE", "duplicate/overlapping quarantine location", relative)
            require(loc["sha256"] == entries[relative]["sha256"], "QUARANTINE_HASH_MISMATCH", "quarantine hash differs from inventory", relative)
            matched[relative] = record
    return matched, outside, obligations


def rational_certificate(data, path):
    document = load_json(data, path)
    require(type(document) is dict and set(document) == {"schema", "inequalities"}
            and document["schema"] == "cbz-rational-certificate-v1"
            and type(document["inequalities"]) is list and 0 < len(document["inequalities"]) <= MAX_INEQUALITIES,
            "INVALID_RATIONAL_CERTIFICATE", "unsupported exact-certificate schema", path)
    def number(value):
        require(type(value) is str and len(value) <= 2 * MAX_RATIONAL_DIGITS + 2,
                "INVALID_RATIONAL_CERTIFICATE", "rationals must be bounded canonical strings", path)
        match = RATIONAL.fullmatch(value)
        require(match is not None and len(match[1].lstrip("-")) <= MAX_RATIONAL_DIGITS
                and (match[2] is None or len(match[2]) <= MAX_RATIONAL_DIGITS),
                "INVALID_RATIONAL_CERTIFICATE", "invalid integer/rational syntax", path)
        return Fraction(int(match[1]), int(match[2] or "1"))
    for row in document["inequalities"]:
        require(type(row) is dict and set(row) == {"left", "relation", "right"}
                and type(row["relation"]) is str and row["relation"] in {"<", "<=", "=", ">=", ">"},
                "INVALID_RATIONAL_CERTIFICATE", "invalid rational relation", path)
        left, right = number(row["left"]), number(row["right"])
        holds = {"<": left < right, "<=": left <= right, "=": left == right,
                 ">=": left >= right, ">": left > right}[row["relation"]]
        require(holds, "FALSE_RATIONAL_CERTIFICATE", "exact rational inequality is false", path)


def audit_tree(root, manifest, quarantine=None):
    report = {"schema": "cbz-layer-a-scan-v1", "ok": False, "status": "FAIL", "kernel_verified": False,
              "issues": [], "files_checked": 0, "quarantined_files": [], "trusted_auditor_files": [],
              "exact_certificates_checked": [], "operational_records_checked": [], "operational_sources_checked": [],
              "unproved_obligations": [], "imports": {},
              "external_trust": {}, "quarantine_references_outside_scope": [],
              "thresholds": {"max_file_bytes": MAX_FILE_BYTES, "max_total_bytes": MAX_TOTAL_BYTES,
                             "max_files": MAX_FILES, "max_roots": MAX_ROOTS, "max_inventory_entries": MAX_INVENTORY_ENTRIES,
                             "max_tokens_per_file": MAX_TOKENS,
                             "max_comment_depth": MAX_COMMENT_DEPTH, "max_rational_digits": MAX_RATIONAL_DIGITS}}
    try:
        root = Path(root).absolute()
        require(".." not in root.parts, "INVALID_MANIFEST", "root must have no parent-traversal components", str(root))
        require(not has_symlink(root), "SYMLINK", "root or ancestor is a symlink", str(root))
        require(root.is_dir(), "MISSING_FILE", "root is not a directory", str(root))
        roots, entries, modules, external = validate_manifest(manifest)
        require(quarantine is not None, "INVALID_QUARANTINE", "an explicit canonical quarantine index is required")
        quarantined, outside, obligations = quarantine_matches(root, quarantine, entries)
        report["quarantined_files"] = sorted(quarantined)
        report["quarantine_references_outside_scope"] = outside
        report["unproved_obligations"] = obligations
        report["external_trust"] = external
        actual, inventory_entries = set(), 0
        def add_issue(finding):
            require(len(report["issues"]) < MAX_ISSUES, "RESOURCE_LIMIT", "total issue limit exceeded")
            report["issues"].append(finding)
        def walk_error(exc):
            raise Reject("INVENTORY_IO_ERROR", str(exc), str(exc.filename))
        for scope in roots:
            directory = root / scope
            require(not has_symlink(directory), "SYMLINK", "inventory root has symlink ancestor", scope)
            require(directory.is_dir(), "MISSING_FILE", "inventory root is absent", scope)
            for parent, directories, files in os.walk(directory, followlinks=False, onerror=walk_error):
                for name in sorted(directories + files):
                    inventory_entries += 1
                    require(inventory_entries <= MAX_INVENTORY_ENTRIES, "RESOURCE_LIMIT", "inventory entry limit exceeded", scope)
                    child = Path(parent) / name
                    relative = child.relative_to(root).as_posix()
                    require(not child.is_symlink(), "SYMLINK", "symlink in inventory", relative)
                    if child.is_file(): actual.add(relative)
                    elif not child.is_dir(): raise Reject("UNSUPPORTED_FILE", "nonregular inventory entry", relative)
                require(len(actual) <= MAX_FILES, "RESOURCE_LIMIT", "inventory exceeds file limit", scope)
        for path in sorted(actual):
            if path not in entries:
                add_issue(Reject("UNLISTED_FILE", "file omitted from manifest", path).issue)
        for path in sorted(set(entries) - actual):
            add_issue(Reject("MISSING_FILE", "manifest file missing from inventory", path).issue)
        total = 0
        for path in sorted(set(entries) & actual):
            entry = entries[path]
            try:
                data = read_bounded(root / path, path); total += len(data)
                require(total <= MAX_TOTAL_BYTES, "RESOURCE_LIMIT", "total byte limit exceeded", path)
                require(hashlib.sha256(data).hexdigest() == entry["sha256"], "SOURCE_HASH_MISMATCH", "source hash differs from frozen manifest", path)
                report["files_checked"] += 1
                findings = []
                if entry["kind"].startswith("lean_"):
                    findings, imports = scan_lean(data, entry)
                    report["imports"][entry["module"]] = [name for name, _, _ in imports]
                    if entry["kind"] == "lean_auditor": report["trusted_auditor_files"].append(path)
                    for name, line, column in imports:
                        if name not in modules and name not in external:
                            findings.append(Reject("UNRESOLVED_IMPORT", "import not in local inventory or exact external pins: " + name, path, line, column).issue)
                        if path not in quarantined and name in modules and modules[name] in quarantined:
                            findings.append(Reject("QUARANTINE_DEPENDENCY", "active import reaches quarantined source: " + name, path, line, column).issue)
                elif entry["kind"] == "rational_certificate":
                    rational_certificate(data, path)
                    report["exact_certificates_checked"].append(path)
                elif entry["kind"] == "operational_record":
                    load_json(data, path)
                    report["operational_records_checked"].append(path)
                elif entry["kind"] == "operational_source":
                    try: data.decode("utf-8", "strict")
                    except UnicodeError as exc: raise Reject("UNSUPPORTED_FILE", "operational source must be UTF-8", path) from exc
                    report["operational_sources_checked"].append(path)
                else:
                    raise Reject("UNSUPPORTED_FILE", "unsupported content requires explicit quarantine", path)
                if path in quarantined:
                    for finding in findings:
                        finding["severity"] = "quarantined"
                        finding["quarantine_id"] = quarantined[path]["id"]
                for finding in findings: add_issue(finding)
            except Reject as exc:
                # Hash/inventory corruption can never be waived by quarantine.
                if path in quarantined and exc.issue["code"] not in {"SOURCE_HASH_MISMATCH", "MISSING_FILE", "SYMLINK", "RESOURCE_LIMIT"}:
                    exc.issue.update(severity="quarantined", quarantine_id=quarantined[path]["id"])
                add_issue(exc.issue)
        # Explicit cycle checking avoids a source inventory masquerading as a valid build DAG.
        visiting, done = set(), set()
        def visit(module):
            if module in done: return
            require(module not in visiting, "IMPORT_CYCLE", "local import cycle: " + module, modules[module])
            require(len(visiting) < MAX_DEPENDENCY_DEPTH, "RESOURCE_LIMIT", "dependency depth limit exceeded", modules[module])
            visiting.add(module)
            for dependency in report["imports"].get(module, []):
                if dependency in modules and modules[dependency] not in quarantined: visit(dependency)
            visiting.remove(module); done.add(module)
        for module in sorted(modules):
            if modules[module] not in quarantined: visit(module)
        report["ok"] = not any(x["severity"] == "error" for x in report["issues"])
        if report["ok"]: report["status"] = "PASS_WITH_QUARANTINE" if quarantined or obligations else "PASS"
        report["total_bytes_checked"] = total
    except (Reject, RecursionError) as exc:
        report["issues"].append(exc.issue if isinstance(exc, Reject) else Reject("RESOURCE_LIMIT", "dependency recursion limit exceeded").issue)
    return report


class JsonArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise Reject("INVALID_ARGUMENT", message, "<arguments>")


def main(argv=None):
    parser = JsonArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--quarantine", required=True, type=Path)
    try:
        args = parser.parse_args(argv)
        manifest = load_json(read_bounded(args.manifest.absolute(), str(args.manifest)), str(args.manifest))
        quarantine = load_json(read_bounded(args.quarantine.absolute(), str(args.quarantine)), str(args.quarantine)) if args.quarantine else None
        report = audit_tree(args.root, manifest, quarantine)
        for issue in report["issues"]:
            if not issue["path"]:
                issue["path"] = str(args.quarantine if "QUARANTINE" in issue["code"] else args.manifest)
    except Reject as exc:
        report = {"schema": "cbz-layer-a-scan-v1", "ok": False, "status": "FAIL", "kernel_verified": False, "issues": [exc.issue]}
    print(json.dumps(report, sort_keys=True, ensure_ascii=True, allow_nan=False))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
