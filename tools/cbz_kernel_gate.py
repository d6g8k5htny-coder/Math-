#!/usr/bin/env python3
"""Fresh native Lean kernel/axiom evidence. Never promotes scientific status."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import time
import tomllib
import uuid

PROJECTS = (
    "formal",
    "specifications/lean_statements_20261010",
    "specifications/lean_statement_proofs_20261011",
    "frontiers/cap_first_exit_lean_20261002",
    "frontiers/determinant_moment_20261025",
    "frontiers/source_smooth_realization_20261011",
    "frontiers/source_lifetime_realization_20261017",
    "frontiers/source_derivative_gaussian_20261025",
)
ALLOWED_AXIOMS = frozenset({"propext", "Classical.choice", "Quot.sound"})
ALLOWED_AXIOM_NAMES = frozenset({("propext",), ("Classical", "choice"), ("Quot", "sound")})
TOOLCHAIN = "leanprover/lean4:v4.34.1"
LEAN_COMMIT = "5045d0056413266e57c625dcd7c365b10e377c52"
MATHLIB_REV = "d13f23b723b8a846827a245b89c10fc7d3f11612"
MODULE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*")
SAFE_KINDS = frozenset({"theorem", "def", "inductive", "ctor", "rec"})

# Complete link census of the nine pinned dependency trees. These exact aliases
# are not compiler inputs to this gate. Never resolve their targets or extend
# this reviewed catalog from checkout contents or an invocation parameter.
DEPENDENCY_METADATA_LINKS = {
    ("batteries", "f2effa3d803fda822b1f97b806c47cf2adfbcbc2"): {
        "docs/README.md": {"git_blob": "32d46ee883b58d6a383eed06eb98f33aa6530ded",
                           "payload_hex": "2e2e2f524541444d452e6d64", "role": "documentation alias"}},
    ("mathlib", MATHLIB_REV): {
        "scripts/bench/build/fake-root/bin/lean.py": {
            "git_blob": "819298943e1a8c331413fb55e2c4bbc98d05e562", "payload_hex": "6c65616e",
            "role": "inactive benchmark alias; not gate runtime or compiler input"},
        "scripts/bench/size/run.py": {
            "git_blob": "e5224d533ef27b001224859a9b36696846a7e7fe", "payload_hex": "72756e",
            "role": "inactive benchmark alias; not gate runtime or compiler input"}},
}

class GateError(ValueError):
    pass

class AuditRefused(GateError):
    def __init__(self, bad_axioms, bad_declarations, declarations=()):
        self.bad_axioms = set(bad_axioms)
        self.bad_declarations = list(bad_declarations)
        self.declarations = list(declarations)
        details = []
        if self.bad_axioms:
            details.append("forbidden transitive axiom: " + ", ".join(sorted(render_name(v) for v in self.bad_axioms)))
        details.extend("forbidden compiled declaration kind: " + row["kind"] + " " + row["name"] for row in self.bad_declarations)
        super().__init__("; ".join(details))

def require(ok, message):
    if not ok:
        raise GateError(message)

def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    require(not path.is_symlink(), "symlink evidence destination: " + str(path))
    temp = path.with_name(path.name + ".tmp")
    require(not temp.is_symlink(), "symlink temporary evidence destination")
    temp.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    temp.replace(path)

def begin_execution(output):
    """Fresh attempt directory; prior successes/failures and separate G0 evidence survive."""
    output = Path(output)
    require(not output.is_symlink(), "symlink execution output")
    output.mkdir(parents=True, exist_ok=True)
    runs = output / "executions"
    require(not runs.is_symlink(), "symlink execution history")
    runs.mkdir(exist_ok=True)
    history = output / "reference-history"
    for name in ("receipt.json", "current-execution.json", "result.json"):
        old = output / name
        if old.exists() or old.is_symlink():
            require(not history.is_symlink(), "symlink reference history")
            history.mkdir(exist_ok=True)
            old.replace(history / (uuid.uuid4().hex + "-" + name))
    run = runs / ("attempt-" + uuid.uuid4().hex)
    run.mkdir()
    state = {"status": "RUNNING", "execution": run.relative_to(output).as_posix()}
    write_json(output / "current-execution.json", state)
    write_json(output / "result.json", state)
    return run

def finish_execution(output, run, status):
    output = Path(output)
    relative = Path(run).relative_to(output).as_posix() if run is not None else None
    current_path = output / "current-execution.json"
    current = json.loads(current_path.read_text()) if current_path.is_file() else {}
    # Skip an already-replaced reference; same-output callers must serialize.
    # This check is not an atomic concurrency lock.
    if relative is not None and current.get("execution") != relative:
        return
    state = {"status": status, "execution": relative}
    write_json(current_path, state)
    write_json(output / "result.json", state)

def project_inventory(repo, relative):
    repo = Path(repo).resolve()
    selected = Path(relative)
    require(not selected.is_absolute() and selected.parts and ".." not in selected.parts
            and selected.as_posix() == relative, "unsafe project path or escape: " + relative)
    root = repo / selected
    for ancestor in [repo, *[repo.joinpath(*selected.parts[:i]) for i in range(1, len(selected.parts) + 1)]]:
        require(not ancestor.is_symlink(), "symlink project ancestor: " + str(ancestor))
    require(root.resolve().is_relative_to(repo), "native project escape")
    require(root.is_dir() and not root.is_symlink(), "missing or symlink project: " + relative)
    config = {}
    for name in ("lean-toolchain", "lakefile.toml", "lake-manifest.json"):
        p = root / name
        require(p.is_file() and not p.is_symlink(), "missing or symlink project configuration: " + str(p))
        config[name] = digest(p)
    require((root / "lean-toolchain").read_text().strip() == TOOLCHAIN, "unexpected Lean toolchain: " + relative)
    lake = tomllib.loads((root / "lakefile.toml").read_text())
    libs = lake.get("lean_lib", [])
    require(libs and all(isinstance(v.get("name"), str) and MODULE.fullmatch(v["name"]) for v in libs),
            "missing or malformed native library inventory")
    src_dirs = {Path(v.get("srcDir", ".")) for v in libs}
    require(all(not p.is_absolute() and ".." not in p.parts for p in src_dirs), "unsafe native srcDir")
    require(all(".lake" not in p.parts for p in src_dirs), "native srcDir cannot use the excluded .lake cache")
    src_dirs = sorted(src_dirs, key=lambda p: len(p.parts), reverse=True)
    modules = []
    names = set()
    paths, excluded_cache_dirs = native_source_files(root)
    for p in paths:
        rel = p.relative_to(root)
        require(not p.is_symlink() and not any(q.is_symlink() for q in p.parents if q != root.parent),
                "symlink native Lean source: " + str(rel))
        src = next((d for d in src_dirs if rel.is_relative_to(d)), None)
        require(src is not None, "unmapped native Lean source: " + str(rel))
        name = ".".join(rel.relative_to(src).with_suffix("").parts)
        require(MODULE.fullmatch(name) is not None, "invalid native module identity: " + name)
        require(name not in names, "duplicate module identity: " + name)
        names.add(name)
        modules.append({"module": name, "path": rel.as_posix(), "sha256": digest(p), "bytes": p.stat().st_size})
    require(modules, "empty native source inventory: " + relative)
    for library in libs:
        roots = library.get("roots", [library["name"]])
        require(isinstance(roots, list) and roots and all(isinstance(v, str) and MODULE.fullmatch(v) for v in roots),
                "malformed declared native library roots")
        for declared in roots:
            require(any(name == declared or name.startswith(declared + ".") for name in names),
                    "missing declared native library root: " + declared)
    lock = json.loads((root / "lake-manifest.json").read_text())
    return {"project": relative, "modules": sorted(modules, key=lambda x: x["module"]),
            "libraries": [v["name"] for v in libs], "configuration_sha256": config,
            "dependency_records": lock.get("packages", []), "excluded_cache_dirs": excluded_cache_dirs}

def native_source_files(root):
    """Visit every source directory explicitly; traversal errors are never an empty census."""
    paths, excluded = [], []
    readable = stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH
    executable = stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
    def walk(directory):
        try:
            mode = directory.lstat().st_mode
            require(stat.S_ISDIR(mode) and not stat.S_ISLNK(mode), "symlink or non-directory source path: " + str(directory))
            require(mode & readable and mode & executable, "unreadable or inaccessible source directory: " + str(directory))
            with os.scandir(directory) as scan:
                entries = sorted(scan, key=lambda e: e.name)
            for entry in entries:
                path = Path(entry.path)
                mode = entry.stat(follow_symlinks=False).st_mode
                require(not stat.S_ISLNK(mode), "symlink source entry: " + str(path))
                if directory == root and entry.name == ".lake":
                    require(stat.S_ISDIR(mode), "native .lake cache must be a directory")
                    excluded.append(".lake")
                    continue
                if stat.S_ISDIR(mode):
                    walk(path)
                else:
                    require(stat.S_ISREG(mode), "nonregular native source entry: " + str(path))
                    if path.suffix == ".lean":
                        require(mode & readable, "unreadable native source file: " + str(path))
                        try:
                            text = path.read_bytes().decode("utf-8")
                        except UnicodeDecodeError as exc:
                            raise GateError("native source is not UTF-8: " + str(path)) from exc
                        # Conservative source preflight; the compiled module-header check
                        # below is authoritative even if future syntax evades this spelling.
                        require(re.search(r"(?m)^\s*module(?:\s|$)", text) is None,
                                "native module-system sidecars are not qualified: " + str(path))
                        paths.append(path)
        except OSError as exc:
            raise GateError("inaccessible native source traversal: " + str(directory) + ": " + str(exc)) from exc
    walk(root)
    return sorted(paths), excluded

def require_tracked_coverage(snapshot, tracked):
    prefixes = [row["project"] + "/" for row in snapshot["projects"]]
    expected = {p for p in tracked if p.endswith(".lean") and any(p.startswith(prefix) for prefix in prefixes)}
    observed = {row["project"] + "/" + module["path"] for row in snapshot["projects"] for module in row["modules"]}
    require(expected == observed, "native tracked/filesystem Lean coverage mismatch: missing="
            + repr(sorted(expected - observed)) + " extra=" + repr(sorted(observed - expected)))

def require_unchanged(snapshot, root):
    for relative, expected in snapshot.items():
        p = Path(root) / relative
        require(p.is_file() and not p.is_symlink() and digest(p) == expected, "source changed: " + relative)

def fresh_build_directory(project):
    project = Path(project)
    lake = project / ".lake"
    require(not lake.is_symlink(), "symlink native .lake directory")
    build = lake / "build"
    require(not build.is_symlink(), "symlink native build directory")
    if build.exists():
        require(build.is_dir(), "native build path is not a directory")
        shutil.rmtree(build)

def decode_name(encoded):
    require(isinstance(encoded, str) and encoded, "empty encoded declaration name")
    parts = []
    for component in encoded.split("/"):
        if component.startswith("s"):
            raw = component[1:]
            require(bool(raw) and len(raw) % 2 == 0 and re.fullmatch("[0-9a-f]+", raw), "malformed encoded string name")
            try:
                value = bytes.fromhex(raw).decode("utf-8")
            except (ValueError, UnicodeDecodeError) as exc:
                raise GateError("malformed encoded UTF-8 name") from exc
            parts.append(value)
        elif component.startswith("n") and re.fullmatch("0|[1-9][0-9]*", component[1:]):
            parts.append(int(component[1:]))
        else:
            raise GateError("malformed encoded declaration name")
    return tuple(parts)

def render_name(parts):
    return ".".join(str(p) for p in parts)

def parse_audit(text, expected_modules):
    require(len(expected_modules) == len(set(expected_modules)) and expected_modules, "invalid expected module inventory")
    require(all(MODULE.fullmatch(m) for m in expected_modules), "invalid expected native module name")
    expected_names = {tuple(m.split(".")) for m in expected_modules}
    counts = {}
    declarations = []
    names = set()
    axioms = None
    terminal = None
    for line in text.splitlines():
        if not line.startswith("CBZ|"):
            continue
        require(terminal is None, "protocol record after terminal END marker")
        fields = line.split("|")
        tag = fields[1] if len(fields) > 1 else ""
        if tag == "MODULE" and len(fields) == 5:
            name = decode_name(fields[2])
            require(name not in counts, "duplicate audited module")
            require(fields[3].isdigit() and fields[4].isdigit(), "malformed module count")
            first, second = int(fields[3]), int(fields[4])
            require(first == second, "independent compiled census disagreement: " + render_name(name))
            counts[name] = first
        elif tag == "DECL" and len(fields) == 5:
            module = decode_name(fields[2])
            encoded_name = decode_name(fields[3])
            name = render_name(encoded_name)
            require(encoded_name not in names, "duplicate compiled declaration")
            names.add(encoded_name)
            declarations.append({"module": render_name(module), "_module": module,
                                 "encoded_module": fields[2], "name": name, "encoded_name": fields[3], "kind": fields[4]})
        elif tag == "AXIOMS" and len(fields) == 3:
            require(axioms is None, "duplicate axiom closure")
            encoded = [] if not fields[2] else [decode_name(v) for v in fields[2].split(",")]
            require(len(encoded) == len(set(encoded)), "duplicate transitive axiom")
            axioms = encoded
        elif tag == "END" and len(fields) == 5:
            require(terminal is None and all(v.isdigit() for v in fields[2:]), "malformed or duplicate END")
            terminal = tuple(int(v) for v in fields[2:])
        else:
            raise GateError("unrecognized CBZ audit protocol record: " + line)
    require(terminal is not None, "missing END audit marker")
    require(axioms is not None, "missing transitive axiom closure")
    require(set(counts) == expected_names, "compiled module inventory differs from registered native sources")
    require(terminal[:2] == (len(counts), len(declarations)), "terminal audit count mismatch")
    require(len(declarations) > 0, "empty project declaration inventory")
    require(terminal[2] >= len(declarations), "transitive closure count is smaller than declaration count")
    for module, expected_count in counts.items():
        require(sum(x["_module"] == module for x in declarations) == expected_count, "per-module declaration count mismatch")
    for row in declarations:
        require(row["_module"] in counts, "declaration outside native module inventory")
    declarations = [{k: v for k, v in row.items() if k != "_module"} for row in declarations]
    bad = set(axioms) - ALLOWED_AXIOM_NAMES
    bad_declarations = [row for row in declarations if row["kind"] not in SAFE_KINDS]
    if bad or bad_declarations:
        raise AuditRefused(bad, bad_declarations, declarations)
    return {"declaration_count": len(declarations), "module_counts": {render_name(k): v for k, v in counts.items()},
            "declarations": declarations, "axioms": sorted(render_name(v) for v in axioms), "closure_count": terminal[2],
            "protocol_sha256": hashlib.sha256("\n".join(x for x in text.splitlines() if x.startswith("CBZ|")).encode()).hexdigest()}

def command_environment():
    env = dict(os.environ)
    # Local identity checks must inspect the supplied checkout, even when the caller
    # inherited a foreign Git selector or a command-line configuration injection.
    for name in list(env):
        if name in {"GIT_DIR", "GIT_WORK_TREE", "GIT_COMMON_DIR", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
                    "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_REPLACE_REF_BASE"} or name.startswith("GIT_CONFIG"):
            env.pop(name)
    env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull,
               GIT_NO_REPLACE_OBJECTS="1", GIT_OPTIONAL_LOCKS="0", GIT_TERMINAL_PROMPT="0")
    env.pop("LEAN_PATH", None)
    return env

def run_logged(command, label, out, cwd, timeout):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    require(re.fullmatch("[A-Za-z0-9_.-]+", label), "unsafe command log label")
    stdout, stderr = out / (label + ".stdout"), out / (label + ".stderr")
    require(not stdout.is_symlink() and not stderr.is_symlink(), "symlink command log")
    env = command_environment()
    start = time.monotonic()
    with stdout.open("wb") as so, stderr.open("wb") as se:
        try:
            proc = subprocess.run(command, cwd=cwd, env=env, stdout=so, stderr=se, timeout=timeout)
            code = proc.returncode
        except subprocess.TimeoutExpired:
            code = 124
        except OSError as exc:
            se.write(str(exc).encode())
            code = 127
    result = {"argv": [str(v) for v in command], "cwd": str(cwd), "returncode": code,
              "elapsed_seconds": time.monotonic() - start, "timeout_seconds": timeout,
              "stdout_sha256": digest(stdout), "stderr_sha256": digest(stderr)}
    write_json(out / (label + ".json"), result)
    require(code == 0, label + ": child exit " + str(code))
    return result

def audit_source(modules):
    require(modules and len(modules) == len(set(modules)) and all(MODULE.fullmatch(m) for m in modules),
            "unsafe or duplicate generated audit module")
    imports = "\n".join("import " + m for m in modules)
    names = ", ".join(chr(96) + m for m in modules)
    return imports + "\nimport Lean\n" + r"""
open Lean Elab Command
set_option maxRecDepth 100000
set_option maxHeartbeats 0
namespace CBZInternalAudit
def hex (s : String) : String :=
  s.toUTF8.foldl (fun acc b => acc ++ (if b.toNat < 16 then "0" else "") ++ String.ofList (Nat.toDigits 16 b.toNat)) ""
def join (a b : String) : String := if a.isEmpty then b else a ++ "/" ++ b
def enc : Name → String
  | .anonymous => ""
  | .str p s => join (enc p) ("s" ++ hex s)
  | .num p k => join (enc p) ("n" ++ toString k)
def kind (ci : ConstantInfo) : String :=
  if ci.isUnsafe then "unsafe" else
  match ci with
  | .thmInfo _ => "theorem"
  | .defnInfo v => if v.safety == .safe then "def" else "partial"
  | .axiomInfo _ => "axiom"
  | .opaqueInfo _ => "opaque"
  | .inductInfo _ => "inductive"
  | .ctorInfo _ => "ctor"
  | .recInfo _ => "rec"
  | .quotInfo _ => "quot"
structure St where
  visited : NameSet := {}
  axioms : NameSet := {}
  missing : NameSet := {}
partial def collect (env : Environment) (c : Name) : StateM St Unit := do
  unless (← get).visited.contains c do
    modify fun s => { s with visited := s.visited.insert c }
    let expr (e : Expr) : StateM St Unit := e.getUsedConstants.forM (collect env)
    match env.find? c with
    | some (.axiomInfo v) => modify (fun s => { s with axioms := s.axioms.insert c }) *> expr v.type
    | some (.defnInfo v) => expr v.type *> expr v.value
    | some (.thmInfo v) => expr v.type *> expr v.value
    | some (.opaqueInfo v) => expr v.type *> expr v.value
    | some (.quotInfo _) => pure ()
    | some (.ctorInfo v) => expr v.type
    | some (.recInfo v) => expr v.type
    | some (.inductInfo v) => expr v.type *> v.ctors.forM (collect env)
    | none => modify fun s => { s with missing := s.missing.insert c }
end CBZInternalAudit
run_cmd do
  let env := (← getEnv).setExporting false
  let modules : Array Name := #[""" + names + r"""]
  let constants := env.constants.toList
  let mut audited : Array Name := #[]
  for modName in modules do
    let some idx := env.getModuleIdx? modName
      | throwError "missing native module {modName}"
    let data := env.header.moduleData[idx]!
    if data.isModule then
      throwError "CBZ module-system sidecars are not qualified: {modName}"
    let table := data.constants
    let headerNames := (table.map (·.name)).qsort Name.lt
    let originNames := (constants.filterMap fun (name, _) =>
      if env.getModuleIdxFor? name == some idx then some name else none).toArray.qsort Name.lt
    unless headerNames == originNames do
      let headerOnly := headerNames.filter fun name => !originNames.contains name
      let originOnly := originNames.filter fun name => !headerNames.contains name
      throwError "independent compiled census disagreement {modName}: {headerNames.size} versus {originNames.size}; header-only {headerOnly}; origin-only {originOnly}"
    liftIO <| IO.println s!"CBZ|MODULE|{CBZInternalAudit.enc modName}|{headerNames.size}|{originNames.size}"
    for name in originNames do
      if (env.checked.get.find? name).isNone then
        throwError "missing checked kernel declaration {name}"
      let some ci := env.find? name | throwError "missing declaration {name}"
      liftIO <| IO.println s!"CBZ|DECL|{CBZInternalAudit.enc modName}|{CBZInternalAudit.enc name}|{CBZInternalAudit.kind ci}"
      audited := audited.push name
  let (_, closure) := (audited.forM (CBZInternalAudit.collect env)).run {}
  unless closure.missing.isEmpty do
    throwError "missing transitive closure declaration {closure.missing.toArray}"
  let axioms := (closure.axioms.toArray.map CBZInternalAudit.enc).qsort (· < ·)
  liftIO <| IO.println s!"CBZ|AXIOMS|{",".intercalate axioms.toList}"
  liftIO <| IO.println s!"CBZ|END|{modules.size}|{audited.size}|{closure.visited.size}"
"""

def native_snapshot(repo):
    reports = [project_inventory(repo, p) for p in PROJECTS]
    binding = {}
    for r in reports:
        for f in r["modules"]:
            binding[r["project"] + "/" + f["path"]] = f["sha256"]
        for name, sha in r["configuration_sha256"].items():
            binding[r["project"] + "/" + name] = sha
    return {"schema_version": 1, "status": "SOURCE_INVENTORY_ONLY", "scientific_effect": "NONE",
            "projects": reports, "project_count": len(reports), "module_count": sum(len(p["modules"]) for p in reports),
            "source_binding": binding, "kernel_status": "NOT_EVALUATED"}

def git_output(repo, *args):
    result = subprocess.run(["git", "--no-replace-objects", "-C", str(repo), *args],
                            text=True, capture_output=True, env=command_environment())
    require(result.returncode == 0, "git identity check failed: " + result.stderr.strip())
    return result.stdout.strip()

def git_tree_entries(repo, commit):
    require(re.fullmatch("[0-9a-f]{40}", commit or ""), "canonical tree requires an exact commit")
    result = subprocess.run(["git", "--no-replace-objects", "--literal-pathspecs", "-C", str(repo),
                             "ls-tree", "-r", "-z", "--full-tree", commit],
                            capture_output=True, env=command_environment())
    require(result.returncode == 0, "cannot read canonical Git tree")
    entries = {}
    for record in result.stdout.split(b"\0"):
        if not record:
            continue
        try:
            metadata, raw_path = record.split(b"\t", 1)
            mode, kind, blob = metadata.decode("ascii").split(" ")
            path = raw_path.decode("utf-8")
        except (ValueError, UnicodeError) as exc:
            raise GateError("malformed canonical Git tree record") from exc
        require(path not in entries and re.fullmatch("[0-9a-f]{40}", blob), "duplicate or malformed Git tree entry")
        entries[path] = {"mode": mode, "kind": kind, "blob": blob}
    require(entries, "empty canonical Git tree")
    return entries

def attest_sources(repo, commit, paths, entries=None, *, dependency=None):
    """Bind actual consumed bytes to commit blobs; index flags/status cannot substitute."""
    repo = Path(repo).absolute()
    require(not any(p.is_symlink() for p in [repo, *repo.parents]), "symlink source checkout ancestor")
    entries = git_tree_entries(repo, commit) if entries is None else entries
    metadata_links = DEPENDENCY_METADATA_LINKS.get((dependency, commit), {})
    rows = []
    for relative in sorted(paths):
        pure = Path(relative)
        require(not pure.is_absolute() and ".." not in pure.parts and pure.as_posix() == relative,
                "unsafe consumed source path")
        entry = entries.get(relative)
        require(entry is not None and entry["kind"] == "blob"
                and (entry["mode"] in {"100644", "100755"}
                     or entry["mode"] == "120000" and relative in metadata_links),
                "unsupported or missing HEAD blob source mode: " + relative)
        path = repo / pure
        ancestors = [repo.joinpath(*pure.parts[:i]) for i in range(1, len(pure.parts))]
        require(not any(p.is_symlink() for p in ancestors), "symlink HEAD blob source ancestor: " + relative)
        if entry["mode"] == "120000":
            reviewed = metadata_links[relative]
            require(entry["blob"] == reviewed["git_blob"], "unreviewed metadata Git blob: " + relative)
            require(path.is_symlink(), "reviewed metadata link lost Git symlink mode: " + relative)
            data = os.readlink(os.fsencode(path))
            link_blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
            require(link_blob == entry["blob"] and data.hex() == reviewed["payload_hex"],
                    "symlink payload differs from HEAD blob: " + relative)
            rows.append({"path": relative, "git_blob": link_blob, "sha256": hashlib.sha256(data).hexdigest(),
                         "mode": entry["mode"], "kind": "symlink_payload", "payload_hex": data.hex(),
                         "role": reviewed["role"], "target_followed": False})
            continue
        require(path.is_file() and not path.is_symlink(),
                "missing or symlink HEAD blob source: " + relative)
        data = path.read_bytes()
        blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        require(blob == entry["blob"], "consumed bytes differ from HEAD blob: " + relative)
        rows.append({"path": relative, "git_blob": blob, "sha256": hashlib.sha256(data).hexdigest(), "mode": entry["mode"]})
    return {"commit": commit, "files": len(rows), "source_records": rows,
            "symlink_files": sum(row.get("kind") == "symlink_payload" for row in rows),
            "records_sha256": hashlib.sha256(json.dumps(rows, sort_keys=True).encode()).hexdigest()}

def dependency_pins(snapshot):
    expected = None
    for project in snapshot["projects"]:
        records = project["dependency_records"]
        require(isinstance(records, list), "malformed native dependency lock")
        pins = {}
        for record in records:
            if record.get("type") == "path":
                require(project["project"] == "specifications/lean_statement_proofs_20261011"
                        and record.get("name") == "universal_law_specifications"
                        and record.get("dir") == "../lean_statements_20261010", "unexpected path dependency")
                continue
            require(record.get("type") == "git" and isinstance(record.get("name"), str)
                    and re.fullmatch("[0-9a-f]{40}", record.get("rev", "")), "invalid Git dependency lock")
            require(record["name"] not in pins, "duplicate dependency lock")
            pins[record["name"]] = record["rev"]
        require(pins.get("mathlib") == MATHLIB_REV, "unexpected Mathlib revision")
        require(expected is None or pins == expected, "native projects have inconsistent dependency revisions")
        expected = pins
    return expected

def share_dependencies(repo, snapshot, pins):
    shared = Path(repo) / "formal/.lake/packages"
    verified = {}
    for name, revision in pins.items():
        path = shared / name
        require(path.is_dir() and git_output(path, "rev-parse", "HEAD") == revision, "dependency checkout differs from pinned revision: " + name)
        require(not git_output(path, "status", "--porcelain", "--untracked-files=normal"), "dirty dependency checkout: " + name)
        entries = git_tree_entries(path, revision)
        attestation = attest_sources(path, revision, set(entries), entries, dependency=name)
        verified[name] = {"revision": revision, "path": str(path.resolve()), "tracked_source_attestation": attestation,
                          "compiled_cache_trust": "Pinned dependency cache accepted; dependency objects are not claimed freshly rebuilt or independently source-qualified."}
    for report in snapshot["projects"]:
        packages = Path(repo) / report["project"] / ".lake/packages"
        if packages == shared:
            continue
        require(not packages.is_symlink(), "symlink packages root")
        packages.mkdir(parents=True, exist_ok=True)
        for name in pins:
            dest = packages / name
            target = shared / name
            if dest.exists() or dest.is_symlink():
                require(dest.resolve() == target.resolve(), "pre-existing unrelated dependency materialization: " + str(dest))
            else:
                dest.symlink_to(target.resolve(), target_is_directory=True)
    return verified

def import_names(text):
    # Actual native compilation remains authoritative for unsupported import syntax.
    clean = re.sub(r"/-.*?-/", "", text, flags=re.S)
    result = []
    for line in clean.splitlines():
        line = line.split("--", 1)[0].strip()
        if line.startswith("import ") or line.startswith("public import "):
            names = line.removeprefix("public ").removeprefix("import ").split()
            require(all(MODULE.fullmatch(n) for n in names), "unsupported native import syntax")
            result.extend(names)
    return result

def compile_missing(project, modules, out, timeout):
    by_name = {m["module"]: m for m in modules}
    done = set()
    active = set()
    def visit(name):
        if name in done:
            return
        require(name not in active, "cyclic native imports: " + name)
        active.add(name)
        row = by_name[name]
        for dep in import_names((project / row["path"]).read_text()):
            if dep in by_name:
                visit(dep)
        obj = project / ".lake/build/lib/lean" / (name.replace(".", "/") + ".olean")
        if not obj.is_file():
            obj.parent.mkdir(parents=True, exist_ok=True)
            run_logged(["lake", "env", "lean", "-o", str(obj), row["path"]], "orphan-" + name, out, project, timeout)
        require(obj.is_file() and not obj.is_symlink(), "native module did not produce fresh object: " + name)
        active.remove(name)
        done.add(name)
    for name in by_name:
        visit(name)

def validate_control(text, module, label):
    try:
        parse_audit(text, [module])
    except AuditRefused as exc:
        expected = {"sorry": {("sorryAx",)}}
        if label == "unused_axiom":
            require(len(exc.bad_declarations) == 1 and exc.bad_declarations[0]["kind"] == "axiom"
                    and decode_name(exc.bad_declarations[0]["encoded_name"]) == ("unusedCBZPremise",)
                    and exc.bad_axioms == {("unusedCBZPremise",)}, "unused-axiom control refused for an unrelated finding")
        elif label == "native":
            # Lean 4.34.1 Native.lean: nativeEqTrue adds a generated axiom via
            # mkAuxDeclName (`_native ++ `native_decide ++ `ax). CoreM appends
            # positive elaboration indices. This is qualified by a real hosted fixture;
            # no concrete helper name is claimed observed before that execution.
            require(len(exc.bad_declarations) == 1 and exc.bad_declarations[0]["kind"] == "axiom",
                    "native control must expose its one generated axiom")
            name = decode_name(exc.bad_declarations[0]["encoded_name"])
            require(len(name) == 4 and name[:3] == ("unusedCBZNative", "_native", "native_decide")
                    and isinstance(name[3], str) and re.fullmatch(r"ax_[1-9][0-9]*(?:_[1-9][0-9]*)*", name[3]),
                    "native control refused an unrelated generated axiom")
            require(exc.bad_axioms == {name}, "native control closure differs from its generated axiom")
            require(any(row["kind"] == "theorem" and decode_name(row["encoded_name"]) == ("unusedCBZNative",)
                        for row in exc.declarations), "native control omitted its actual theorem")
        else:
            require(label in expected and exc.bad_axioms == expected[label] and not exc.bad_declarations,
                    "negative control refused for an unrelated forbidden declaration or axiom: " + label)
        return {"outcome": "REJECTED_EXPECTED_FORBIDDEN_DECLARATION_OR_AXIOM", "diagnostic": str(exc),
                "forbidden_axioms": sorted(render_name(v) for v in exc.bad_axioms)}
    raise GateError("negative control escaped: " + label)

def generated_theorem_value_mutation(project, out, timeout, module):
    """A real compiled sorry fixture must expose omitted theorem-value traversal."""
    original = audit_source([module])
    before = "| some (.thmInfo v) => expr v.type *> expr v.value"
    after = "| some (.thmInfo v) => expr v.type"
    require(original.count(before) == 1, "stale generated-auditor theorem-value mutation")
    path = out / "MutatedTheoremValueAudit.lean"
    path.write_text(original.replace(before, after, 1))
    run = run_logged(["lake", "env", "lean", str(path)], "generated-theorem-value-mutant", out, project, timeout)
    require(not (out / "generated-theorem-value-mutant.stderr").read_text().strip(),
            "generated auditor mutant produced unexpected diagnostics")
    text = (out / "generated-theorem-value-mutant.stdout").read_text()
    # The deliberately broken collector must run and parse, then the compiled sorry
    # control must detect its false clear result. A Lean crash is never a mutation kill.
    accepted = parse_audit(text, [module])
    require("sorryAx" not in accepted["axioms"], "generated theorem-value mutant did not remove the intended dependency")
    try:
        validate_control(text, module, "sorry")
    except GateError as exc:
        require(type(exc) is GateError and str(exc) == "negative control escaped: sorry",
                "generated auditor mutant failed for an unrelated reason")
        diagnostic = str(exc)
    else:
        raise GateError("generated theorem-value mutant was not detected by the compiled control")
    result = {"id": "omit_generated_theorem_value_traversal", "outcome": "KILLED_BY_COMPILED_SORRY_CONTROL",
              "scope": "One actual generated Lean collector mutation; not a general generated-code mutation certificate.",
              "mutation_location_count": 1, "baseline_source_sha256": hashlib.sha256(original.encode()).hexdigest(),
              "mutant_source_sha256": digest(path), "command": run,
              "mutated_audit_report": accepted, "control_diagnostic": diagnostic}
    write_json(out / "generated-theorem-value-result.json", result)
    return result

def negative_controls(project, out, timeout):
    out.mkdir(parents=True, exist_ok=True)
    # Exercise the generated Lean API and the empty-aggregator case before any long build.
    positive = project / ".lake/CBZControl_positive.lean"
    empty = project / ".lake/CBZControl_empty.lean"
    positive.write_text("import Lean\ndef cbzValidValue : Nat := 2\ntheorem cbzValidProof : cbzValidValue = 2 := rfl\n")
    empty.write_text("import CBZControl_positive\n")
    retained = out / "sources"
    retained.mkdir(parents=True, exist_ok=True)
    positive_sources = {source.name: digest(source) for source in (positive, empty)}
    for source in (positive, empty):
        shutil.copyfile(source, retained / source.name)
    positive_objects = {}
    target = project / ".lake/build/lib/lean"
    target.mkdir(parents=True, exist_ok=True)
    for source in (positive, empty):
        module = source.stem
        run_logged(["lake", "env", "lean", "--root=" + str(project / ".lake"),
                    "-o", str(target / (module + ".olean")), str(source)],
                   "positive-" + module + "-compile", out, project, timeout)
        positive_objects[module] = digest(target / (module + ".olean"))
        run_logged(["lake", "env", "leanchecker", module], "positive-" + module + "-kernel", out, project, timeout)
    baseline = out / "PositiveAudit.lean"
    baseline.write_text(audit_source([positive.stem, empty.stem]))
    run_logged(["lake", "env", "lean", str(baseline)], "positive-audit", out, project, timeout)
    positive_report = parse_audit((out / "positive-audit.stdout").read_text(), [positive.stem, empty.stem])
    require(positive_report["module_counts"][empty.stem] == 0, "empty-aggregator positive control is not empty")
    require({"cbzValidValue", "cbzValidProof"} <= {r["name"] for r in positive_report["declarations"]},
            "positive control omitted its actual named declarations")
    positive_sources_after = {source.name: digest(source) for source in (positive, empty)}
    positive_objects_after = {name: digest(target / (name + ".olean")) for name in positive_objects}
    require(positive_sources_after == positive_sources and positive_objects_after == positive_objects,
            "positive fixture source or object changed during preflight")
    positive_report.update(sources_before=positive_sources, sources_after=positive_sources_after,
                           objects_before=positive_objects, objects_after=positive_objects_after)
    write_json(out / "positive-result.json", positive_report)
    cases = {
        "unused_axiom": ("axiom unusedCBZPremise : False\n", "axiom"),
        "sorry": ("private theorem unusedCBZProof : True := by sorry\n", "sorryAx"),
        "native": ("theorem unusedCBZNative : (2 : Nat) + 2 = 4 := by native_decide\n", "Lean.ofReduceBool"),
    }
    reports = {"positive": positive_report}
    for label, (body, expected) in cases.items():
        module = "CBZControl_" + label
        path = project / ".lake" / (module + ".lean")
        path.write_text("import Lean\n" + body)
        source_before = digest(path)
        shutil.copyfile(path, retained / path.name)
        obj = project / ".lake/build/lib/lean" / (module + ".olean")
        run_logged(["lake", "env", "lean", "--root=" + str(project / ".lake"), "-o", str(obj), str(path)],
                   "control-" + label + "-compile", out, project, timeout)
        object_before = digest(obj)
        run_logged(["lake", "env", "leanchecker", module], "control-" + label + "-kernel", out, project, timeout)
        audit = out / ("ControlAudit_" + label + ".lean")
        audit.write_text(audit_source([module]))
        run_logged(["lake", "env", "lean", str(audit)], "control-" + label + "-audit", out, project, timeout)
        text = (out / ("control-" + label + "-audit.stdout")).read_text()
        reports[label] = validate_control(text, module, label)
        source_after, object_after = digest(path), digest(obj)
        require(source_before == source_after and object_before == object_after,
                "negative fixture source or object changed during preflight: " + label)
        reports[label].update(source_before=source_before, source_after=source_after,
                              object_before=object_before, object_after=object_after)
        write_json(out / (label + "-result.json"), reports[label])
        if label == "sorry":
            reports["generated_theorem_value_mutation"] = generated_theorem_value_mutation(project, out, timeout, module)
            require(digest(path) == source_before and digest(obj) == object_before,
                    "compiled sorry fixture changed during generated-auditor mutation")
    write_json(out / "controls-result.json", reports)
    return reports

def execute(repo, out, expected_commit, timeout):
    require(re.fullmatch("[0-9a-f]{40}", expected_commit or ""), "execute requires a full expected commit")
    require(git_output(repo, "rev-parse", "HEAD") == expected_commit, "tested commit differs from expected commit")
    require(not git_output(repo, "status", "--porcelain", "--untracked-files=no"), "tracked source worktree is dirty")
    snapshot = native_snapshot(repo)
    tree_entries = git_tree_entries(repo, expected_commit)
    tracked = set(tree_entries)
    require(set(snapshot["source_binding"]) <= tracked, "untracked native proof/configuration source")
    require_tracked_coverage(snapshot, tracked)
    gate_files = {"tools/cbz_kernel_gate.py", "tools/cbz_kernel_registry.json",
                  "tests/test_cbz_kernel_gate.py", ".github/workflows/cbz-kernel.yml",
                  "tools/cbz_kernel_mutations.py", "tests/test_cbz_kernel_mutations.py"}
    require(gate_files <= tracked, "untracked CBZ gate implementation/configuration")
    require(Path(__file__).resolve() == (Path(repo) / "tools/cbz_kernel_gate.py").resolve(),
            "running CBZ gate differs from the tested checkout")
    gate_binding = {name: digest(Path(repo) / name) for name in gate_files}
    canonical_binding = attest_sources(repo, expected_commit, set(snapshot["source_binding"]) | gate_files, tree_entries)
    for relative in set(snapshot["source_binding"]) | gate_files:
        dest = out / "sources" / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(Path(repo) / relative, dest)
    write_json(out / "source-inventory.json", snapshot)
    pins = dependency_pins(snapshot)
    for row in snapshot["projects"]:
        fresh_build_directory(Path(repo) / row["project"])
    dependencies = share_dependencies(repo, snapshot, pins)
    run_logged(["lake", "env", "lean", "--version"], "lean-version", out, Path(repo) / "formal", timeout)
    version = (out / "lean-version.stdout").read_text().strip()
    require(re.fullmatch(r"Lean \(version 4\.34\.1, [^()\r\n]+, commit " + LEAN_COMMIT + r", Release\)", version),
            "unexpected actual Lean runtime: " + version)
    run_logged(["lake", "env", "lean", "--print-prefix"], "lean-prefix", out, Path(repo) / "formal", timeout)
    prefix = Path((out / "lean-prefix.stdout").read_text().strip())
    runtime = {name: {"path": str(prefix / "bin" / name), "sha256": digest(prefix / "bin" / name)}
               for name in ("lean", "lake", "leanchecker")}
    controls = negative_controls(Path(repo) / "formal", out / "controls", timeout)
    reports = []
    object_binding = {}
    progress = {"projects": [{"project": row["project"], "status": "NOT_EVALUATED"} for row in snapshot["projects"]]}
    write_json(out / "progress.json", progress)
    for index, row in enumerate(snapshot["projects"]):
        progress["projects"][index]["status"] = "RUNNING"
        write_json(out / "progress.json", progress)
        project = Path(repo) / row["project"]
        logs = out / ("project-" + str(index))
        logs.mkdir(parents=True)
        run_logged(["lake", "build"], "native-default-build", logs, project, timeout)
        run_logged(["lake", "build", *row["libraries"]], "all-native-libraries-build", logs, project, timeout)
        compile_missing(project, row["modules"], logs, timeout)
        objects = {}
        for module in row["modules"]:
            name = module["module"]
            obj = project / ".lake/build/lib/lean" / (name.replace(".", "/") + ".olean")
            before = digest(obj)
            run_logged(["lake", "env", "leanchecker", name], "kernel-" + name, logs, project, timeout)
            require(digest(obj) == before, "compiled object changed during kernel replay: " + name)
            objects[name] = {"sha256": before, "bytes": obj.stat().st_size}
            object_binding[obj.relative_to(repo).as_posix()] = before
        names = [m["module"] for m in row["modules"]]
        audit = logs / "Environment.lean"
        audit.write_text(audit_source(names))
        run_logged(["lake", "env", "lean", str(audit)], "environment", logs, project, timeout)
        report = parse_audit((logs / "environment.stdout").read_text(), names)
        require_unchanged(snapshot["source_binding"], repo)
        report.update(project=row["project"], objects=objects, audit_source_sha256=digest(audit))
        write_json(logs / "audit-report.json", report)
        reports.append(report)
        progress["projects"][index]["status"] = "KERNEL_AND_AXIOM_AUDIT_PASSED"
        write_json(out / "progress.json", progress)
        print(json.dumps({"project": row["project"], "modules": len(names), "declarations": report["declaration_count"], "status": "KERNEL_AND_AXIOM_AUDIT_PASSED"}), flush=True)
    require_unchanged(snapshot["source_binding"], repo)
    require_unchanged(gate_binding, repo)
    require_unchanged(object_binding, repo)
    require(attest_sources(repo, expected_commit, set(snapshot["source_binding"]) | gate_files) == canonical_binding,
            "canonical consumed source attestation changed")
    require(git_output(repo, "rev-parse", "HEAD") == expected_commit, "tested checkout HEAD changed during execution")
    require(native_snapshot(repo)["source_binding"] == snapshot["source_binding"], "native source inventory changed")
    require(not git_output(repo, "status", "--porcelain", "--untracked-files=no"), "tracked source changed during native execution")
    share_dependencies(repo, snapshot, pins)
    receipt = {"schema_version": 1, "status": "KERNEL_AND_AXIOM_AUDIT_PASSED", "scientific_effect": "NONE",
               "checked_commit": expected_commit, "checked_tree": git_output(repo, "rev-parse", "HEAD^{tree}"),
               "repository": os.environ.get("GITHUB_REPOSITORY"), "run_id": os.environ.get("GITHUB_RUN_ID"),
               "run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"), "lean_version": version, "runtime": runtime,
               "dependency_checkouts": dependencies, "dependency_objects_rebuilt_from_source": False,
               "allowed_axioms": sorted(ALLOWED_AXIOMS), "projects": reports, "negative_controls": controls,
               "source_inventory_sha256": digest(out / "source-inventory.json"),
               "gate_source_binding": gate_binding,
               "canonical_source_attestation": canonical_binding,
               "scope": "Eight native packages only; no semantic or scientific-status closure."}
    write_json(out / "receipt.json", receipt)
    return receipt

def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    action = p.add_mutually_exclusive_group(required=True)
    action.add_argument("--inventory", action="store_true")
    action.add_argument("--execute", action="store_true")
    p.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    p.add_argument("--output", type=Path, default=Path(".lake/cbz-kernel"))
    p.add_argument("--expected-commit")
    p.add_argument("--timeout", type=int, default=1800, help="Actual timeout for each compiler/audit command")
    args = p.parse_args(argv)
    repo = args.root.resolve()
    out = args.output if args.output.is_absolute() else repo / args.output
    require(not out.is_symlink(), "symlink evidence output")
    out.mkdir(parents=True, exist_ok=True)
    run = out
    try:
        if args.execute:
            run = begin_execution(out)
        require(args.timeout > 0, "nonpositive command timeout")
        if args.inventory:
            result = native_snapshot(repo)
            dependency_pins(result)
            write_json(out / "source-inventory.json", result)
        else:
            result = execute(repo, run, args.expected_commit, args.timeout)
        write_json(run / "result.json", {"status": result["status"], "scientific_effect": "NONE"})
        if args.execute:
            finish_execution(out, run, result["status"])
        print(json.dumps({k: v for k, v in result.items() if k in ("status", "project_count", "module_count", "kernel_status", "checked_commit")}, sort_keys=True))
        return 0
    except (GateError, OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        if run != out:
            (run / "receipt.json").unlink(missing_ok=True)
        if (run / "progress.json").is_file():
            progress = json.loads((run / "progress.json").read_text())
            for row in progress["projects"]:
                if row["status"] == "RUNNING":
                    row.update(status="REFUSED", reason=str(exc))
            write_json(run / "progress.json", progress)
        write_json(run / "result.json", {"status": "REFUSED", "scientific_effect": "NONE", "reason": str(exc),
                                        "kernel_status": "NOT_ESTABLISHED"})
        if args.execute:
            finish_execution(out, run if run != out else None, "REFUSED")
        print("CBZ kernel gate REFUSED: " + str(exc), file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())

