#!/usr/bin/env python3
"""Source-bound all-owned logical constant audit; no theorem-source changes."""
from __future__ import annotations

import argparse
import contextlib
import fcntl
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import signal
import stat
import sys
import threading

sys.path.insert(0, str(Path(__file__).resolve().parent))
from recorded_process import run_recorded
from owned_kernel_controls import (REASONS, render_control, render_graph_control,
    render_insertion_mutant, validate_graph_control, validate_mutant_escape, validate_rejection)

HERE = Path(__file__).resolve().parents[1]
LEAN_SHA = "e8baaa71855a616dc351028f3ad2200051b0671f423a1696a100e809302d5550"
MATHLIB_COMMIT = "d13f23b723b8a846827a245b89c10fc7d3f11612"
LEANCHECKER_SHA = "ccef1bfe9bfeecea65137d94a69033c1a89f360711f50fa3178e7ba3e696fcbe"
ALLOWED = {"propext", "Classical.choice", "Quot.sound"}
KINDS = {"theorem", "def", "opaque", "inductive", "ctor", "rec", "quot"}
BODY_KINDS = {"theorem", "def", "opaque"}
MODULE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*\Z")
NAT = re.compile(r"0|[1-9][0-9]*\Z")
MAX_CONSTANTS = 100000


def require(condition, message):
    if not condition: raise ValueError(message)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def inventory_files(root):
    """Inventory every ordinary file; never reinterpret unreadable or aliased trees as empty."""
    root = Path(root)
    paths = {}
    def unreadable(error):
        raise error
    try:
        mode = root.lstat().st_mode
        require(not stat.S_ISLNK(mode) and stat.S_ISDIR(mode), "unsupported or symlink inventory root")
        for directory, dirs, files in os.walk(root, followlinks=False, onerror=unreadable):
            base = Path(directory)
            for name in sorted(dirs + files):
                path = base/name
                mode = path.lstat().st_mode
                require(not stat.S_ISLNK(mode), "symlink inventory entry: " + str(path))
                if stat.S_ISDIR(mode):
                    continue
                require(stat.S_ISREG(mode), "unsupported special inventory entry: " + str(path))
                paths[path.relative_to(root).as_posix()] = path
    except OSError as exc:
        raise ValueError("unreadable filesystem inventory: " + str(exc)) from exc
    return dict(sorted(paths.items()))


def inventory_hashes(root):
    return {name: sha(path) for name, path in inventory_files(root).items()}


def write(path, value):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n")


def natural(value):
    require(type(value) is str and len(value) <= 12 and NAT.fullmatch(value), "noncanonical natural count")
    return int(value)


def encode_name(parts):
    require(type(parts) is list and bool(parts), "empty name")
    encoded = []
    for part in parts:
        if type(part) is str:
            encoded.append("s" + part.encode("utf-8", "strict").hex())
        elif type(part) is int and part >= 0:
            encoded.append("n" + str(part))
        else: raise ValueError("unsupported name component")
    return "/".join(encoded)


def decode_name(encoded):
    require(type(encoded) is str and 0 < len(encoded) <= 16384, "invalid encoded name")
    parts = []
    for component in encoded.split("/"):
        if component.startswith("s"):
            payload = component[1:]
            require(len(payload) % 2 == 0 and re.fullmatch(r"[0-9a-f]*", payload), "invalid string name component")
            try: parts.append(bytes.fromhex(payload).decode("utf-8", "strict"))
            except UnicodeError as exc: raise ValueError("invalid UTF-8 name component") from exc
        elif component.startswith("n"):
            parts.append(natural(component[1:]))
        else: raise ValueError("invalid name component tag")
    require(encode_name(parts) == encoded, "noncanonical encoded name")
    return parts


def dotted_name(value):
    require(type(value) is str and MODULE.fullmatch(value), "unsupported dotted Lean name")
    return encode_name(value.split("."))


def lean_name(encoded):
    result = "Name.anonymous"
    for part in decode_name(encoded):
        if type(part) is str: result = "(Name.str " + result + " " + json.dumps(part, ensure_ascii=False) + ")"
        else: result = "(Name.num " + result + " " + str(part) + ")"
    return result


def assert_acyclic_bodies(constants, dependencies):
    bodies = {row["name"] for row in constants if row["body"] == "body"}
    graph = {name: set() for name in bodies}
    for row in constants:
        if row["body"] == "body": graph[row["name"]].update(dependencies[row["id"]])
    visiting, done = set(), set()
    def visit(name):
        if name in done: return
        require(name not in visiting, "owned body dependency cycle: " + name)
        require(len(visiting) < 512, "owned body dependency depth limit exceeded")
        visiting.add(name)
        for dependency in graph[name]:
            if dependency in bodies: visit(dependency)
        visiting.remove(name); done.add(name)
    for name in sorted(bodies): visit(name)


def parse_inventory(text, expected_modules, explicit_targets):
    modules, constants, dependencies, extras, completion = {}, [], {}, [], None
    wanted = {dotted_name(x) for x in expected_modules}
    require(len(wanted) == len(expected_modules) and wanted, "empty/duplicate expected modules")
    for line in text.splitlines():
        if not line: continue
        fields = line.split("|"); tag = fields[0]
        if tag == "OWN_MODULE":
            require(len(fields) == 4, "malformed module row")
            module = fields[1]; decode_name(module)
            require(module in wanted and module not in modules, "missing, duplicate or foreign module")
            modules[module] = {"primary": natural(fields[2]), "extras": natural(fields[3])}
        elif tag == "OWN_CONST":
            require(len(fields) == 10, "malformed constant row")
            _, module, name, kind, origin, body, rules, safety, totality, source = fields
            decode_name(module); decode_name(name)
            require(module in wanted and kind in KINDS and origin in {"user", "aux"}, "foreign/unsupported constant")
            require(body == ("body" if kind in BODY_KINDS else "primitive"), "constant body classification mismatch")
            require(safety == "safe" and totality == "total", "unsafe or partial owned declaration")
            require(source in {"primary", "extra"}, "invalid constant inventory source")
            count = natural(rules)
            require(kind == "rec" or count == 0, "nonrecursor with reduction rules")
            constants.append(dict(id=module+"::"+name,module=module, name=name, kind=kind, origin=origin, body=body, rules=count, source=source))
            require(len(constants) <= MAX_CONSTANTS, "constant inventory exceeds limit")
        elif tag == "OWN_DEP":
            require(len(fields) == 3, "malformed dependency row")
            name = fields[1]
            identity=name.split("::");require(len(identity)==2,"malformed instance dependency ID")
            for component in identity:decode_name(component)
            require(name not in dependencies, "duplicate dependency inventory")
            deps = fields[2].split(",") if fields[2] else []
            for dependency in deps: decode_name(dependency)
            require(deps == sorted(set(deps)), "unsorted/duplicate dependency names")
            dependencies[name] = deps
        elif tag == "OWN_EXTRA":
            require(len(fields) == 4, "malformed extra row")
            module, name, status = fields[1:]; decode_name(module); decode_name(name)
            require(module in wanted and status in {"ir_only", "logical_existing", "logical_added"}, "unsupported extra classification")
            extras.append(dict(module=module, name=name, status=status))
        elif tag == "OWN_INVENTORY_COMPLETE":
            require(len(fields) == 4 and completion is None, "duplicate/malformed inventory completion")
            completion = tuple(natural(x) for x in fields[1:])
        else: raise ValueError("unrecognized inventory output: " + line[:160])
    names = [x["name"] for x in constants]
    identities=[x["id"] for x in constants]
    ordered=[(x["module"],x["name"]) for x in constants]
    require(names and len(set(identities)) == len(identities) and ordered == sorted(ordered), "empty, duplicate or unsorted constant inventory")
    require(set(modules) == wanted and completion == (len(wanted), len(constants), len(extras)), "incomplete module/constant inventory")
    require(set(dependencies) == set(identities) and all(set(x) <= set(names) for x in dependencies.values()), "omitted/foreign dependency inventory")
    require(len({(x["module"], x["name"]) for x in extras}) == len(extras), "duplicate extra inventory")
    by_name = {x["name"]: x for x in constants}
    by_instance={x["id"]:x for x in constants}
    for module, counts in modules.items():
        require(sum(x["module"] == module and x["source"] == "primary" for x in constants) == counts["primary"], "omitted primary constant")
        require(sum(x["module"] == module for x in extras) == counts["extras"], "omitted extra name")
    for extra in extras:
        value = by_instance.get(extra["module"]+"::"+extra["name"])
        if extra["status"] == "ir_only": require(extra["name"] not in by_name, "logical constant mislabeled IR-only")
        else:
            require(value is not None and value["module"] == extra["module"], "unresolved logical extra")
            require(value["source"] == ("extra" if extra["status"] == "logical_added" else "primary"), "logical-extra source mismatch")
    for row in constants:
        if row["source"] == "extra": require(any(x["name"] == row["name"] and x["module"]==row["module"] and x["status"] == "logical_added" for x in extras), "orphan logical extra")
    for target in explicit_targets:
        value = by_name.get(dotted_name(target))
        require(value is not None and value["kind"] == "theorem", "missing explicit theorem target: " + target)
    assert_acyclic_bodies(constants, dependencies)
    return dict(modules=modules, constants=constants, dependencies=dependencies, extras=extras,
                explicit_targets=list(explicit_targets))


def parse_checks(text, inventory, selected):
    require(selected and len(set(selected)) == len(selected), "empty/duplicate selected constants")
    known = {x["id"]: x for x in inventory["constants"]}
    require(all(x in known for x in selected), "foreign selected constant")
    rows, axioms, closure, complete = [], None, None, None
    for line in text.splitlines():
        if not line: continue
        fields = line.split("|")
        if fields[0] == "OWN_CHECK":
            require(len(fields) == 8, "malformed body-check row")
            _, module, name, kind, type_status, body_status, decl_status, rules = fields
            identity=module+"::"+name
            require(identity in known and identity in selected, "foreign checked constant")
            source = known[identity]
            require(module == source["module"] and kind == source["kind"] and type_status == "checked", "unchecked type or inventory drift")
            require(body_status == ("checked" if source["body"] == "body" else "absent"), "missing body check")
            require(decl_status == ("checked" if source["body"] == "body" else "primitive"), "missing checked declaration insertion")
            require(natural(rules) == source["rules"], "recursor rule body omission")
            rows.append(dict(id=identity,name=name, module=module, kind=kind, rules=natural(rules)))
        elif fields[0] == "OWN_AXIOMS":
            require(len(fields) == 2 and axioms is None, "missing/duplicate axiom closure")
            axioms = fields[1].split(",") if fields[1] else []
            for name in axioms: decode_name(name)
            require(len(set(axioms)) == len(axioms) and set(axioms) <= {dotted_name(x) for x in ALLOWED}, "forbidden axiom closure")
        elif fields[0] == "OWN_CLOSURE":
            require(len(fields) == 2 and closure is None, "duplicate/malformed closure count")
            closure = natural(fields[1])
        elif fields[0] == "OWN_AUDIT_COMPLETE":
            require(len(fields) == 2 and complete is None, "duplicate/malformed check completion")
            complete = natural(fields[1])
        else: raise ValueError("unrecognized kernel-check output: " + line[:160])
    require([x["id"] for x in rows] == selected and complete == len(selected), "incomplete/duplicate/out-of-order body audit")
    require(axioms is not None and closure is not None and closure >= len({known[x]["name"] for x in selected}), "missing transitive closure evidence")
    return dict(checked=rows, axioms=axioms, closure_size=closure)


def freeze_sources(source, output):
    source, output = Path(source).resolve(), Path(output)
    require(not output.exists(), "new source snapshot directory required")
    files = inventory_files(source/"formal")
    result = {"modules": [], "sources": {}}
    for path in files.values():
        require(path.suffix == ".lean", "unsupported formal source file")
        module = path.relative_to(source/"formal").with_suffix("").as_posix().replace("/", ".")
        dotted_name(module)
        relative = path.relative_to(source).as_posix()
        destination = output/relative; destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, destination)
        result["sources"][relative] = sha(path); result["modules"].append(module)
    require(result["modules"], "no owned proof modules")
    targets = source/"audit_targets.json"
    require(not targets.is_symlink() and stat.S_ISREG(targets.lstat().st_mode), "unsupported audit target source inventory")
    target_doc = json.loads(targets.read_text())
    result["explicit_targets"] = target_doc["names"]
    require(type(result["explicit_targets"]) is list and len(set(result["explicit_targets"])) == len(result["explicit_targets"]), "duplicate explicit targets")
    for target in result["explicit_targets"]: dotted_name(target)
    shutil.copyfile(targets, output/"audit_targets.json")
    result["sources"]["audit_targets.json"] = sha(targets)
    return result


def check_source_snapshot(source, snapshot):
    source = Path(source)
    current = {"formal/" + name for name in inventory_files(source/"formal")}
    require(current == set(snapshot["sources"]) - {"audit_targets.json"}, "formal source addition/removal")
    for name, expected in snapshot["sources"].items():
        path = source/name
        require(not path.is_symlink() and sha(path) == expected, "owned source drift: " + name)


def require_parent_lock(lock, lock_text=None, parent_pid=None):
    lock = Path(lock); info = lock.stat()
    text = Path("/proc/locks").read_text() if lock_text is None else lock_text
    parent_pid = os.getppid() if parent_pid is None else parent_pid
    ancestors = set()
    for _ in range(128):
        if parent_pid <= 0 or parent_pid in ancestors: break
        ancestors.add(parent_pid)
        if parent_pid == 1: break
        status = Path("/proc")/str(parent_pid)/"status"
        match = re.search(r"^PPid:\s+(\d+)\s*$", status.read_text(), re.M)
        require(match is not None, "cannot verify native-lock ancestor lineage")
        parent_pid = int(match[1])
    for line in text.splitlines():
        fields = line.split()
        if len(fields) < 6 or fields[1:4] != ["FLOCK", "ADVISORY", "WRITE"]: continue
        try:
            major, minor, inode = fields[5].split(":")
            matches = (int(fields[4]) in ancestors and int(major, 16) == os.major(info.st_dev)
                       and int(minor, 16) == os.minor(info.st_dev) and int(inode) == info.st_ino)
        except ValueError: continue
        if matches: return
    raise ValueError("verified parent lineage does not hold the exact native WRITE/FLOCK")


def stage_cache(source, destination, expected):
    source, destination = Path(source), Path(destination)
    paths = inventory_files(source)
    require({name: sha(path) for name, path in paths.items()} == expected, "cache inventory drift before staging")
    if destination.exists() or destination.is_symlink():
        require(not inventory_files(destination), "new empty staged cache required")
    else:
        destination.mkdir(parents=True)
    for relative, path in paths.items():
        target = destination/relative; target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
    require(inventory_hashes(destination) == expected, "staged cache mismatch")


@contextlib.contextmanager
def native_lock(parent_held):
    path = HERE/".native.lock"
    if parent_held:
        require_parent_lock(path); yield
    else:
        with path.open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX); yield


SUPPORT_BODY = r'''
open Lean
namespace OwnedKernelAudit
structure Entry where
  name : Name
  info : ConstantInfo
  owner : Name
  source : String
structure Extra where
  name : Name
  owner : Name
  status : String
def hex (s : String) : String :=
  s.toUTF8.foldl (fun acc b => acc ++ (if b.toNat < 16 then "0" else "") ++ String.ofList (Nat.toDigits 16 b.toNat)) ""
def join (a b : String) : String := if a.isEmpty then b else a ++ "/" ++ b
def enc : Name → String
  | .anonymous => ""
  | .str p s => join (enc p) ("s" ++ hex s)
  | .num p n => join (enc p) ("n" ++ toString n)
def kind : ConstantInfo → String
  | .thmInfo _ => "theorem" | .defnInfo _ => "def" | .opaqueInfo _ => "opaque"
  | .axiomInfo _ => "axiom" | .inductInfo _ => "inductive" | .ctorInfo _ => "ctor"
  | .recInfo _ => "rec" | .quotInfo _ => "quot"
def ruleCount : ConstantInfo → Nat
  | .recInfo v => v.rules.length | _ => 0
def expressions (ci : ConstantInfo) : Array Expr := Id.run do
  let mut es := #[ci.type]
  if let some value := ci.value? true then es := es.push value
  if let .recInfo v := ci then
    for rule in v.rules do es := es.push rule.rhs
  return es
def closed (e : Expr) : Bool := !e.hasFVar && !e.hasMVar && !e.hasLooseBVars
def inventory : CoreM (Array Entry × Array Extra × Array (Name × Nat × Nat)) := do
  let env ← getEnv
  let header := env.header
  let mut found : NameSet := {}
  let mut seen : NameSet := {}
  let mut instances : NameSet := {}
  let mut entries : Array Entry := #[]
  let mut extras : Array Extra := #[]
  let mut modules : Array (Name × Nat × Nat) := #[]
  for h : idx in [0:header.moduleNames.size] do
    let owner := header.moduleNames[idx]
    if ownedModules.contains owner then
      if found.contains owner then throwError "duplicate owned module"
      found := found.insert owner
      let data := header.moduleData[idx]!
      if data.constNames.size != data.constants.size then throwError "module inventory size mismatch"
      modules := modules.push (owner, data.constNames.size, data.extraConstNames.size)
      for h : pos in [0:data.constNames.size] do
        let name := data.constNames[pos]
        let identity := Name.str owner (enc name)
        if instances.contains identity then throwError "duplicate owned module occurrence"
        let info := data.constants[pos]!
        let some canonical := env.checked.get.find? name | throwError "owned constant missing from checked environment"
        match Kernel.isDefEq env {} info.type canonical.type with
        | .ok true => pure () | _ => throwError "module occurrence type differs from imported constant"
        if info.name != name then throwError "constant name mismatch"
        entries := entries.push ⟨name, info, owner, "primary"⟩
        seen := seen.insert name
        instances := instances.insert identity
      for name in data.extraConstNames do
        match env.checked.get.find? name with
        | none =>
          if (env.find? name).isSome then throwError "elaborator-only extra is not kernel-owned"
          extras := extras.push ⟨name, owner, "ir_only"⟩
        | some info =>
          if instances.contains (Name.str owner (enc name)) then
            let some old := entries.find? (fun e => e.name == name && e.owner == owner) | throwError "missing seen constant"
            if old.source != "primary" then throwError "ambiguous logical extra ownership"
            extras := extras.push ⟨name, owner, "logical_existing"⟩
          else
            entries := entries.push ⟨name, info, owner, "extra"⟩
            extras := extras.push ⟨name, owner, "logical_added"⟩
            seen := seen.insert name
            instances := instances.insert (Name.str owner (enc name))
  if found.size != ownedModules.length then throwError "missing owned module"
  for target in explicitTargets do
    if !seen.contains target then throwError "explicit theorem missing from owned module inventory"
    let some (.thmInfo _) := env.checked.get.find? target | throwError "explicit target is not a theorem"
  return (entries.qsort (fun a b => if a.owner == b.owner then enc a.name < enc b.name else enc a.owner < enc b.owner), extras, modules)
def dumpInventory : CoreM Unit := do
  let (entries, extras, modules) ← inventory
  for (owner, primary, extra) in modules do
    IO.println s!"OWN_MODULE|{enc owner}|{primary}|{extra}"
  let owned := entries.foldl (init := ({} : NameSet)) (fun s e => s.insert e.name)
  for e in entries do
    let origin := if (← findDeclarationRanges? e.name).isSome then "user" else "aux"
    let body := if e.info.hasValue true then "body" else "primitive"
    let safety := if e.info.isUnsafe then "unsafe" else "safe"
    let totality := if e.info.isPartial then "partial" else "total"
    IO.println s!"OWN_CONST|{enc e.owner}|{enc e.name}|{kind e.info}|{origin}|{body}|{ruleCount e.info}|{safety}|{totality}|{e.source}"
    let mut deps : NameSet := {}
    for expr in expressions e.info do
      for dependency in expr.getUsedConstants do
        if owned.contains dependency then deps := deps.insert dependency
    let encoded := (deps.toArray.map enc).qsort (· < ·)
    IO.println s!"OWN_DEP|{enc e.owner}::{enc e.name}|{String.intercalate "," encoded.toList}"
  for e in extras do IO.println s!"OWN_EXTRA|{enc e.owner}|{enc e.name}|{e.status}"
  IO.println s!"OWN_INVENTORY_COMPLETE|{modules.size}|{entries.size}|{extras.size}"
structure Closure where
  seen : NameSet := {}
  axioms : NameSet := {}
partial def collect (env : Environment) (name : Name) : StateT Closure CoreM Unit := do
  unless (← get).seen.contains name do
    modify fun s => {s with seen := s.seen.insert name}
    let some ci := env.checked.get.find? name | throwError "transitive constant missing from kernel environment"
    if let .axiomInfo _ := ci then modify fun s => {s with axioms := s.axioms.insert name}
    for expr in expressions ci do expr.getUsedConstants.forM (collect env)
    if let .inductInfo v := ci then v.ctors.forM (collect env)
def checkType (env : Environment) (e : Expr) : CoreM Unit := do
  if !closed e then throwError "OWN_REJECT_OPEN_TYPE"
  let inferred ← match Kernel.check env {} e with
    | .ok t => pure t | .error _ => throwError "OWN_REJECT_TYPE_KERNEL"
  match Kernel.whnf env {} inferred with
  | .ok (.sort _) => pure ()
  | _ => throwError "OWN_REJECT_TYPE_SORT"
def checkedBody (env : Environment) (ci : ConstantInfo) : CoreM Unit := do
  let some value := ci.value? true | throwError "owned body missing"
  if !closed value then throwError "OWN_REJECT_OPEN_BODY"
  let inferred ← match Kernel.check env {} value with
    | .ok t => pure t | .error _ => throwError "OWN_REJECT_BODY_KERNEL"
  match Kernel.isDefEq env {} inferred ci.type with
  | .ok true => pure () | _ => throwError "OWN_REJECT_BODY_TYPE"
  let fresh := Name.str `OwnedKernelAudit.Rechecked (enc ci.name)
  let declaration ← match ci with
    | .defnInfo v => pure (Declaration.defnDecl {v with name := fresh, all := [fresh]})
    | .thmInfo v => pure (Declaration.thmDecl {v with name := fresh, all := [fresh]})
    | .opaqueInfo v => pure (Declaration.opaqueDecl {v with name := fresh, all := [fresh]})
    | _ => throwError "unsupported body-bearing declaration"
  match env.addDeclCore 0 0 declaration none true with
  | .ok _ => pure () | .error _ => throwError "OWN_REJECT_DECLARATION"
def permitted (closure : Closure) : CoreM Unit := do
  for name in closure.axioms do
    if name != `propext && name != `Classical.choice && name != `Quot.sound then
      throwError "OWN_REJECT_FORBIDDEN_AXIOM"
def collectEntry (env : Environment) (ci : ConstantInfo) : StateT Closure CoreM Unit := do
  if ci.isAxiom then modify fun s => {s with axioms := s.axioms.insert ci.name}
  for expr in expressions ci do expr.getUsedConstants.forM (collect env)
  if let .inductInfo v := ci then v.ctors.forM (collect env)
  modify fun s => {s with seen := s.seen.insert ci.name}
def audit (selected : List (Name × Name)) : CoreM Unit := do
  let env ← getEnv
  let (entries, _, _) ← inventory
  let mut done : NameSet := {}
  let mut selectedEntries : Array Entry := #[]
  for (owner, name) in selected do
    let identity := Name.str owner (enc name)
    if done.contains identity then throwError "duplicate selected constant"
    done := done.insert identity
    let some e := entries.find? (fun e => e.name == name && e.owner == owner) | throwError "selected constant not owned"
    selectedEntries := selectedEntries.push e
    let ci := e.info
    if ci.isUnsafe || ci.isPartial then throwError "unsafe or partial owned declaration"
    if ci.isAxiom then throwError "new owned axiom"
    checkType env ci.type
    let mut bodyStatus := "absent"
    let mut declarationStatus := "primitive"
    if ci.hasValue true then
      checkedBody env ci
      bodyStatus := "checked"
      declarationStatus := "checked"
    if let .recInfo v := ci then
      for rule in v.rules do
        if !closed rule.rhs then throwError "open recursor reduction rule"
        match Kernel.check env {} rule.rhs with
        | .ok _ => pure () | .error _ => throwError "recursor rule body kernel check failed"
    IO.println s!"OWN_CHECK|{enc e.owner}|{enc name}|{kind ci}|checked|{bodyStatus}|{declarationStatus}|{ruleCount ci}"
  let (_, closure) ← (selectedEntries.forM (fun e => collectEntry env e.info)).run {}
  permitted closure
  let encoded := (closure.axioms.toArray.map enc).qsort (· < ·)
  IO.println s!"OWN_AXIOMS|{String.intercalate "," encoded.toList}"
  IO.println s!"OWN_CLOSURE|{closure.seen.size}"
  IO.println s!"OWN_AUDIT_COMPLETE|{selected.length}"
end OwnedKernelAudit
#eval OwnedKernelAudit.dumpInventory
'''


def render_support(modules, explicit_targets):
    require(type(modules) is list and modules and len(set(modules)) == len(modules), "empty/duplicate modules")
    for module in modules: dotted_name(module)
    require(type(explicit_targets) is list and len(set(explicit_targets)) == len(explicit_targets), "duplicate explicit targets")
    module_expr = ",\n  ".join(lean_name(dotted_name(x)) for x in modules)
    target_expr = ",\n  ".join(lean_name(dotted_name(x)) for x in explicit_targets)
    header = "".join("import " + x + "\n" for x in modules) + "import Lean\nopen Lean\nnamespace OwnedKernelAudit\n"
    header += "def ownedModules : List Name := [\n  " + module_expr + "]\n"
    header += "def explicitTargets : List Name := [\n  " + target_expr + "]\nend OwnedKernelAudit\n"
    return header + SUPPORT_BODY


def render_chunk(selected):
    require(type(selected) is list and selected and len(selected) <= 256 and len(set(selected)) == len(selected), "empty/large/duplicate audit chunk")
    pairs=[]
    for identity in selected:
        parts=identity.split("::");require(len(parts)==2,"invalid module-instance identity")
        pairs.append("("+lean_name(parts[0])+", "+lean_name(parts[1])+")")
    return "import OwnedKernelAudit.Support\nopen Lean\n#eval OwnedKernelAudit.audit [\n  " + ",\n  ".join(pairs) + "]\n"


def verify_prior(source, cache, evidence, snapshot):
    evidence = evidence/"results.json" if evidence.is_dir() else evidence
    result = json.loads(evidence.read_text())
    require(result["status"] == "PASS" and result["cache_was_fresh"] is True and result["old_project_cache_on_lean_path"] is False, "preceding fresh proof did not pass")
    require(len(snapshot["explicit_targets"]) == 198 and [x["name"] for x in result["audited_theorems"]] == snapshot["explicit_targets"], "original explicit198 audit is not preserved")
    for row in result["audited_theorems"]: require(set(row["axioms"]) <= ALLOWED, "prior theorem has forbidden axioms")
    order = result["order"]
    require(type(order) is list and order and len(set(order)) == len(order) and set(order) <= set(snapshot["modules"]), "preceding module order is empty, duplicate or foreign")
    expected_sources = {"formal/" + module.replace(".", "/") + ".lean" for module in order}
    require(set(result["sources"]) == expected_sources, "preceding source-key omission or addition")
    cached_modules = {path[:-6].replace("/", ".") for path in result["outputs"] if path.endswith(".olean")}
    require(cached_modules == set(order), "cached module/source binding coverage mismatch")
    for name, expected in result["sources"].items():
        require(snapshot["sources"].get(name) == expected and sha(source/name) == expected, "preceding proof source mismatch")
    files = inventory_hashes(cache)
    require(files == result["outputs"], "preceding compiled cache differs from receipt")
    require([x["module"] for x in result["records"]] == result["order"], "preceding module receipt omission")
    for row in result["records"]:
        expected_source = "formal/" + row["module"].replace(".", "/") + ".lean"
        require(row["source_sha256"] == result["sources"][expected_source], "preceding record source hash mismatch")
        relative = PurePosixPath(row["receipt"])
        require(not relative.is_absolute() and ".." not in relative.parts, "escaping preceding receipt")
        path = evidence.parent/relative; receipt = json.loads(path.read_text())
        require(all(json.dumps(row.get(key),sort_keys=True,allow_nan=False)==json.dumps(value,sort_keys=True,allow_nan=False) for key, value in receipt.items()), "preceding native receipt differs from campaign record")
        require(receipt["succeeded"] is True and type(receipt["returncode"]) is int and receipt["returncode"] == 0 and receipt["failure"] is None
                and receipt["timed_out"] is False and receipt["output_limit_exceeded"] is False, "preceding native child failed or has invalid typed flags")
        require(type(receipt["streams"]) is dict and set(receipt["streams"])=={"stdout.txt","stderr.txt"},"preceding stream coverage omission")
        for stream, metadata in receipt["streams"].items():
            require(type(metadata["bytes"])is int and metadata["bytes"]>=0 and type(metadata["sha256"])is str
                    and re.fullmatch(r"[0-9a-f]{64}",metadata["sha256"]) and sha(path.parent/stream) == metadata["sha256"]
                    and (path.parent/stream).stat().st_size == metadata["bytes"], "preceding receipt stream drift")
    last=evidence.parent/result["records"][-1]["receipt"]
    text=(last.parent/"stdout.txt").read_text(); audited=[]
    for line in text.splitlines():
        if line.startswith("P15_AUDIT|"):
            fields=line.split("|")
            require(len(fields)==6 and fields[2:5]==["closed","kernel","declaration"],"malformed original198 audit row")
            axioms=sorted(filter(None,fields[5].split(",")))
            require(set(axioms)<=ALLOWED,"original198 audit has forbidden axiom")
            audited.append({"name":fields[1],"axioms":axioms})
    require(audited==result["audited_theorems"] and text.splitlines().count("P15_AUDIT_COMPLETE|198")==1,"original198 stdout audit missing or substituted")
    return result, evidence


def bounded_native(command, output, cwd, env, expected=True):
    stop = threading.Event(); observations = {"samples": 0, "max_processes": 0, "max_rss_kib": 0, "violation": None}
    def monitor():
        try:
            while not stop.wait(0.05):
                started = output/"started.json"
                if not started.is_file(): continue
                pid = json.loads(started.read_text())["pid"]
                values = []
                for item in Path("/proc").iterdir():
                    if not item.name.isdigit(): continue
                    try:
                        if os.getpgid(int(item.name)) != pid: continue
                        argv = (item/"cmdline").read_bytes().split(b"\0")
                        if not argv or Path(os.fsdecode(argv[0])).name not in {"lean", "leanchecker"}: continue
                        match = re.search(r"^VmRSS:\s+(\d+)", (item/"status").read_text(), re.M)
                        if match: values.append(int(match[1]))
                    except (OSError, ProcessLookupError): continue
                observations["samples"] += 1
                observations["max_processes"] = max(observations["max_processes"], len(values))
                observations["max_rss_kib"] = max(observations["max_rss_kib"], sum(values))
                if len(values) > 1 or sum(values) > 11 * 1024 * 1024:
                    observations["violation"] = "parallel-native" if len(values) > 1 else "resident-limit"
                    try: os.killpg(pid, signal.SIGKILL)
                    except ProcessLookupError: pass
        except BaseException as exc:
            observations["violation"] = "monitor-failure:" + type(exc).__name__
            try:
                if (output/"started.json").is_file(): os.killpg(json.loads((output/"started.json").read_text())["pid"], signal.SIGKILL)
            except ProcessLookupError: pass
    thread = threading.Thread(target=monitor, daemon=True); thread.start()
    try:
        receipt = run_recorded(command, output, cwd=cwd, env=env, timeout=120, max_output_bytes=32 * 1024 * 1024)
    finally:
        stop.set(); thread.join(); write(output/"process-observation.json", observations)
    require(observations["violation"] is None, "native resource monitor violation")
    tree = receipt.get("process_tree")
    require(type(tree) is dict and tree.get("cleanup_complete") is True
            and tree.get("unexpected_descendants") is False
            and type(tree.get("survivors")) is list and tree["survivors"] == []
            and tree.get("supervisor_forced_exit") is False,
            "ordinary native outcome requires complete supervised lifecycle cleanup")
    require(receipt["failure"] is None and receipt["timed_out"] is False and receipt["output_limit_exceeded"] is False
            and type(receipt["returncode"])is int,"owned-audit child did not terminate normally within bounds")
    require(receipt["succeeded"] is True if expected else receipt["succeeded"]is False and receipt["returncode"]>0,
            "owned-audit native child failed its expected outcome")
    return receipt


def run(args):
    source, cache, evidence, lean, mathlib, output = [Path(x).resolve() for x in
        (args.source, args.formal_cache, args.formal_evidence, args.lean, args.mathlib_root, args.output)]
    require(not output.exists() and not output.is_relative_to(source) and not output.is_relative_to(cache), "new external evidence directory required")
    require(1 <= args.chunk_size <= 256, "invalid chunk size")
    output.mkdir(parents=True)
    result = {"schema": "cbz-owned-kernel-audit-v1", "status": "RUNNING", "cbz_zero": False,
              "records": [], "checked": [], "scope": "All logical constants in the exact owned modules; source-bound fresh environment, not dependency-source rebuild."}
    try:
        snapshot = freeze_sources(source, output/"source-snapshot"); result["snapshot"] = snapshot
        require(len(snapshot["modules"]) == 30, "expected exact30 owned source modules")
        prior, evidence = verify_prior(source, cache, evidence, snapshot)
        result["prior_evidence"] = {"path": str(evidence), "sha256": sha(evidence)}
        require(sha(lean) == LEAN_SHA and prior["runtime"]["lean_executable_sha256"] == LEAN_SHA, "Lean executable identity mismatch")
        # A direct Git read is nonnative metadata; no project build or network access.
        import subprocess
        commit = subprocess.check_output(["git", "-C", str(mathlib), "rev-parse", "HEAD"], text=True).strip()
        require(commit == MATHLIB_COMMIT and prior["runtime"]["mathlib_commit"] == commit, "Mathlib identity mismatch")
        require((mathlib/"lean-toolchain").read_text().strip() == "leanprover/lean4:v4.34.1", "Lean toolchain mismatch")
        helpers = {}
        for path in [Path(__file__).resolve(), Path(__file__).with_name("owned_kernel_controls.py"),
                     Path(__file__).with_name("recorded_process.py"), Path(__file__).with_name("process_supervisor.py")]:
            destination = output/"checker-snapshot"/path.name; destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, destination); helpers[str(path)] = sha(path)
        result["checker_sources"] = helpers
        generated = output/"generated"; generated_cache = output/"generated-cache"; overlay = output/"compiled-extra"
        generated.mkdir(); generated_cache.mkdir(); overlay.mkdir()
        stage_cache(cache, overlay, prior["outputs"])
        packages = mathlib/".lake/packages"
        paths = [generated_cache, overlay, mathlib/".lake/build/lib/lean"]
        if packages.is_dir(): paths += [p/".lake/build/lib/lean" for p in sorted(packages.iterdir()) if (p/".lake/build/lib/lean").is_dir()]
        paths.append(lean.parent.parent/"lib/lean")
        env = dict(os.environ, LEAN_PATH=os.pathsep.join(map(str, paths)), PYTHONDONTWRITEBYTECODE="1", LEAN_NUM_THREADS="1")
        env["PATH"]=str(lean.parent)+os.pathsep+env.get("PATH","")
        for key in ("LEAN_SRC_PATH", "LEAN_SYSROOT", "LAKE_HOME", "LAKE_OVERRIDE_LEAN"): env.pop(key, None)
        result["lean_path"] = list(map(str, paths)); result["runtime"] = dict(lean_sha256=LEAN_SHA, mathlib_commit=commit)
        def compile_module(module, path, root, destination, label, expected=True):
            target = destination/Path(*module.split(".")).with_suffix(".olean"); target.parent.mkdir(parents=True, exist_ok=True)
            argv = [str(lean), "-j1", "-M11000", "-DElab.async=false", "-DautoImplicit=false", "--root=" + str(root), "-o", str(target), str(path)]
            attempt = output/"native"/label
            try: receipt = bounded_native(argv, attempt, source, env,expected=expected)
            finally:
                if (attempt/"receipt.json").is_file():
                    result["records"].append({"label": label, "expected_success":expected,"source_sha256": sha(path), "receipt": str((attempt/"receipt.json").relative_to(output)),
                                              "record": json.loads((attempt/"receipt.json").read_text())})
            require(receipt["succeeded"] is expected, "native compile outcome mismatch")
            return (attempt/"stdout.txt").read_text()
        with native_lock(args.parent_lock_held):
            visiting, done = set(), set()
            def ensure_module(module):
                if module in done: return
                require(module not in visiting, "source import cycle")
                visiting.add(module)
                path = output/"source-snapshot/formal"/Path(*module.split(".")).with_suffix(".lean")
                for line in re.findall(r"^import\s+([^\n]+)", path.read_text(), re.M):
                    for imported in line.split():
                        if imported in snapshot["modules"]: ensure_module(imported)
                target = overlay/Path(*module.split(".")).with_suffix(".olean")
                if not target.is_file(): compile_module(module, path, output/"source-snapshot/formal", overlay, "extra-" + module)
                visiting.remove(module); done.add(module)
            for module in snapshot["modules"]: ensure_module(module)
            support = generated/"OwnedKernelAudit/Support.lean"; support.parent.mkdir(parents=True)
            support.write_text(render_support(snapshot["modules"], snapshot["explicit_targets"]))
            stdout = compile_module("OwnedKernelAudit.Support", support, generated, generated_cache, "inventory")
            inventory = parse_inventory(stdout, snapshot["modules"], snapshot["explicit_targets"])
            result["inventory"] = inventory; write(output/"inventory.json", inventory)
            result["native_controls"]=[]
            for kind in REASONS:
                path=generated/"OwnedKernelAudit"/("Control_"+kind+".lean")
                path.write_text(render_control(kind))
                stdout=compile_module("OwnedKernelAudit.Control_"+kind,path,generated,generated_cache,"control-"+kind,expected=False)
                record=result["records"][-1]
                stderr=(output/record["receipt"]).parent.joinpath("stderr.txt").read_text()
                result["native_controls"].append(validate_rejection(record["record"],stdout+stderr,kind))
            for kind in ("self_cycle","mutual_cycle"):
                path=generated/"OwnedKernelAudit"/("Control_"+kind+".lean")
                path.write_text(render_graph_control(kind)[0])
                stdout=compile_module("OwnedKernelAudit.Control_"+kind,path,generated,generated_cache,"control-"+kind)
                result["native_controls"].append(validate_graph_control(stdout,kind,dotted_name,assert_acyclic_bodies))
            mutant=generated/"OwnedKernelAuditMutation/Support.lean";mutant.parent.mkdir(parents=True)
            mutant.write_text(render_insertion_mutant(support.read_text()))
            compile_module("OwnedKernelAuditMutation.Support",mutant,generated,generated_cache,"control-mutant-support")
            mutant_control=generated/"OwnedKernelAuditMutation/Control.lean"
            mutant_control.write_text(render_control("universe","OwnedKernelAuditMutation"))
            stdout=compile_module("OwnedKernelAuditMutation.Control",mutant_control,generated,generated_cache,"control-mutant-escape")
            result["native_controls"].append(validate_mutant_escape(result["records"][-1]["record"],stdout))
            write(output/"native-controls.json",result["native_controls"])
            primitive_modules=sorted({x["module"]for x in inventory["constants"]if x["body"]=="primitive"})
            require(bool(primitive_modules)==any(x["body"]=="primitive"for x in inventory["constants"]),"primitive replay selection omission")
            leanchecker=lean.with_name("leanchecker")
            require(sha(leanchecker)==LEANCHECKER_SHA,"leanchecker executable identity mismatch")
            result["runtime"]["leanchecker_sha256"]=LEANCHECKER_SHA
            result["primitive_module_replays"]=[]
            for module in primitive_modules:
                decoded=decode_name(module)
                require(all(type(part)is str for part in decoded),"unsupported primitive module name")
                dotted=".".join(decoded);attempt=output/"native"/("primitive-replay-"+dotted)
                try:receipt=bounded_native([str(leanchecker),"-v",dotted],attempt,source,env)
                finally:
                    if(attempt/"receipt.json").is_file():result["records"].append({"label":"primitive-replay-"+dotted,"expected_success":True,
                        "receipt":str((attempt/"receipt.json").relative_to(output)),"record":json.loads((attempt/"receipt.json").read_text())})
                log=(attempt/"stdout.txt").read_text()
                require(log.splitlines()==["replaying "+dotted],"leanchecker replayed an unexpected module set")
                result["primitive_module_replays"].append({"module":module,"leanchecker_sha256":LEANCHECKER_SHA,"receipt":str((attempt/"receipt.json").relative_to(output))})
            names = [x["id"] for x in inventory["constants"]]
            for number, start in enumerate(range(0, len(names), args.chunk_size)):
                selected = names[start:start + args.chunk_size]
                path = generated/"OwnedKernelAudit"/("Chunk" + str(number) + ".lean")
                path.write_text(render_chunk(selected))
                stdout = compile_module("OwnedKernelAudit.Chunk" + str(number), path, generated, generated_cache, "chunk-" + str(number))
                checked = parse_checks(stdout, inventory, selected)
                result["checked"].extend(checked["checked"])
                write(output/("chunk-" + str(number) + ".json"), checked)
                check_source_snapshot(source, snapshot)
            require([x["id"] for x in result["checked"]] == names, "not every logical constant occurrence was checked")
            result["unique_logical_names"]=len({x["name"] for x in inventory["constants"]})
        check_source_snapshot(source, snapshot)
        verify_prior(source, cache, evidence, snapshot)
        for relative,expected in prior["outputs"].items():require(sha(overlay/relative)==expected,"staged baseline cache drift")
        require(all(sha(path) == expected for path, expected in helpers.items()), "checker helper source drift")
        result["generated_sources"] = {p.relative_to(output).as_posix(): sha(p) for p in generated.rglob("*.lean")}
        result["generated_outputs"] = {p.relative_to(output).as_posix(): sha(p) for p in output.rglob("*.olean")}
        result["status"] = "PASS"
        return result
    except BaseException as exc:
        result["status"] = "FAILED"; result["failure"] = {"type": type(exc).__name__, "message": str(exc)}
        raise
    finally: write(output/"results.json", result)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("source", "formal-cache", "formal-evidence", "lean", "mathlib-root", "output"):
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--chunk-size", type=int, default=64)
    parser.add_argument("--parent-lock-held", action="store_true")
    result = run(parser.parse_args(argv))
    print(json.dumps({"status": result["status"], "owned_constants": len(result["checked"]), "cbz_zero": False}))
    return 0


if __name__ == "__main__": raise SystemExit(main())
