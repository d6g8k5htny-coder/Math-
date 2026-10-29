#!/usr/bin/env python3
"""Execute a frozen package with the already self-tested bounded Lean replay.
This recorder does not replace Lean's kernel or authenticate supplied transcripts.
"""
from __future__ import annotations
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tomllib

SOURCE_COMMIT = "86c00d4c08c6c2af0529ec1744693de3ca6ac6e4"
REPLAY_COMMIT = "66c54f8c161c3af467e5d1d715066c96b3a0561b"
COLLECTOR_COMMIT = "8151f592918a845bf19eb8eafaf8444540a32734"
COLLECTOR_SHA256 = "ff8a5374597772b2d37054fd722c2243c4b552a63802c69f7c605519832be6c4"
PACKAGE = "frontiers/source_derivative_gaussian_20261025"
STANDARD = {"Classical.choice", "Quot.sound", "propext"}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def lean_environment():
    environment = os.environ.copy()
    for key in ("LEAN_PATH", "LEAN_SRC_PATH"):
        environment.pop(key, None)
    environment["LEAN_NUM_THREADS"] = "2"
    return environment

def git_environment():
    environment = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    environment.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
                       GIT_NO_REPLACE_OBJECTS="1", GIT_OPTIONAL_LOCKS="0")
    return environment

def git_command(repo, *args):
    return ["git", "--no-replace-objects", "--literal-pathspecs",
            "-c", "core.fsmonitor=false", "-c", "core.hooksPath=/dev/null",
            "-C", str(repo), *args]

def git(repo, *args):
    return subprocess.check_output(git_command(repo, *args), env=git_environment(), timeout=60)

def bind(repo, expected_commit, paths):
    actual = git(repo, "rev-parse", "HEAD").decode().strip()
    if actual != expected_commit:  # MUTATION_HEAD
        raise ValueError("source HEAD differs from frozen commit")
    records = {}
    for relative in paths:
        path = Path(relative)
        if path.is_absolute() or ".." in path.parts:
            raise ValueError("unsafe bound source path")
        absolute = Path(repo) / path
        if any(absolute.parents[i].is_symlink() for i in range(len(path.parts)-1)) or absolute.is_symlink():
            raise ValueError("symlinked bound source")
        expected = git(repo, "cat-file", "blob", expected_commit + ":" + path.as_posix())
        actual_bytes = absolute.read_bytes()
        if actual_bytes != expected:  # MUTATION_BYTES
            raise ValueError("source bytes differ from frozen Git blob: " + relative)
        records[relative] = {"bytes": len(actual_bytes), "sha256": sha(actual_bytes)}
    return {"commit": actual, "files": records}

def bind_dependency(repo, expected_commit):
    repo = Path(repo).resolve()
    if git(repo, "rev-parse", "HEAD").decode().strip() != expected_commit:
        raise ValueError("dependency HEAD differs from frozen commit")
    tree = {}
    for record in git(repo, "ls-tree", "-r", "-z", expected_commit).split(b"\0"):
        if not record:
            continue
        metadata, path = record.split(b"\t", 1)
        mode, kind, oid = metadata.split()
        if kind != b"blob" or mode not in {b"100644", b"100755", b"120000"}:
            raise ValueError("unsupported dependency Git entry")
        tree[os.fsdecode(path)] = (mode.decode(), oid.decode())
    index = {}
    for record in git(repo, "ls-files", "--stage", "-z").split(b"\0"):
        if not record:
            continue
        metadata, path = record.split(b"\t", 1)
        mode, oid, stage = metadata.split()
        if stage != b"0":
            raise ValueError("dependency index has unresolved entries")
        index[os.fsdecode(path)] = (mode.decode(), oid.decode())
    if not tree or index != tree:
        raise ValueError("dependency index differs from frozen tree")
    visible = git(repo, "ls-files", "--others", "--exclude-standard", "-z")
    if visible:
        raise ValueError("untracked dependency paths outside the cache")
    for raw in git(repo, "ls-files", "--others", "--ignored", "--exclude-standard", "-z").split(b"\0"):
        if not raw:
            continue
        path = Path(os.fsdecode(raw))
        if ".lake" not in path.parts and (path.suffix == ".lean" or ".olean" in path.name or ".ilean" in path.name):
            raise ValueError("untracked Lean shadow outside the compiled cache")
    oids = list(dict.fromkeys(oid for mode, oid in tree.values()))
    batch = subprocess.run(git_command(repo, "cat-file", "--batch"),
                           input=("\n".join(oids) + "\n").encode(), capture_output=True, check=True,
                           env=git_environment(), timeout=60).stdout
    blobs, offset = {}, 0
    for wanted in oids:
        end = batch.index(b"\n", offset)
        oid, kind, size = batch[offset:end].split()
        size = int(size)
        if oid.decode() != wanted or kind != b"blob":
            raise ValueError("unexpected immutable Git blob response")
        start = end + 1
        blobs[wanted] = batch[start:start + size]
        if len(blobs[wanted]) != size or batch[start + size:start + size + 1] != b"\n":
            raise ValueError("truncated immutable Git blob response")
        offset = start + size + 1
    if offset != len(batch):
        raise ValueError("trailing immutable Git blob response")
    records = {}
    for relative, (mode, oid) in tree.items():
        path = repo / relative
        if mode == "120000":
            if not path.is_symlink():
                raise ValueError("dependency symlink mode differs")
            actual = os.fsencode(os.readlink(path))
        else:
            if path.is_symlink() or any(parent.is_symlink() for parent in path.parents if parent != repo and parent.is_relative_to(repo)):
                raise ValueError("dependency path aliases another source")
            actual = path.read_bytes()
            if bool(path.stat().st_mode & 0o111) != (mode == "100755"):
                raise ValueError("dependency executable mode differs")
        if actual != blobs[oid]:
            raise ValueError("dependency source bytes differ from frozen Git blob: " + relative)
        records[relative] = {"mode": mode, "git_blob": oid, "bytes": len(actual), "sha256": sha(actual)}
    return {"commit": expected_commit, "files": records}

@contextmanager
def frozen_dependencies(package, lock):
    def snapshot():
        result = {}
        for row in lock["packages"]:
            if row["type"] != "git" or row["name"] in result:
                raise ValueError("unsupported or duplicate dependency")
            result[row["name"]] = bind_dependency(package / ".lake/packages" / row["name"], row["rev"])
        return result
    before = snapshot()
    try:
        yield before
    finally:
        after = snapshot()
        if after != before:
            raise ValueError("dependency identities changed during execution")

def object_snapshot(package, dependencies):
    roots = [package / ".lake/build"] + [package / ".lake/packages" / name / ".lake/build" for name in dependencies]
    records = {}
    root_presence = {}
    for index, root in enumerate(roots):
        relative = root.relative_to(package)
        for parent in [package.joinpath(*relative.parts[:i]) for i in range(1,len(relative.parts)+1)]:
            if parent.is_symlink():  # MUTATION_ROOT_SYMLINK
                raise ValueError("symlink in compiled-object root")
        root_presence[str(relative)] = root.is_dir()
        if not root.is_dir():
            if index == 0:
                raise ValueError("owned compiled object directory absent")
            continue
        for path in sorted(root.rglob("*")):
            if path.is_symlink():  # MUTATION_NESTED_SYMLINK
                raise ValueError("symlink within compiled-object root")
            if path.is_file() and (".olean" in path.name or ".ilean" in path.name or path.suffix in {".so", ".a"}):
                if path.is_symlink():
                    raise ValueError("aliased compiled object")
                raw = path.read_bytes()
                records[str(path.relative_to(package))] = {"bytes": len(raw), "sha256": sha(raw)}
    if not records:
        raise ValueError("compiled objects absent")
    return {"root_presence": root_presence, "objects": records}

@contextmanager
def frozen_objects(package, dependencies):
    before = object_snapshot(package, dependencies)
    try:
        yield before
    finally:
        if object_snapshot(package, dependencies) != before:
            raise ValueError("compiled objects changed during census/kernel replay")

def execution_inputs(carrier, carrier_head, loaded_launcher_sha256, plan_path):
    carrier = Path(carrier).resolve()
    plan_relative = Path(plan_path).resolve().relative_to(carrier).as_posix()
    launcher_relative = "tools/cbz_source514_hosted.py"
    binding = bind(carrier, carrier_head, [launcher_relative, plan_relative])
    if loaded_launcher_sha256 != binding["files"][launcher_relative]["sha256"]:
        raise ValueError("loaded launcher differs from frozen Git source")
    plan_bytes = git(carrier, "cat-file", "blob", carrier_head + ":" + plan_relative)
    return json.loads(plan_bytes), binding

def checked_domain(package, plan):
    if plan.get("schema") != "cbz-source514-exact-domain-v1" or plan.get("source_commit") != SOURCE_COMMIT:
        raise ValueError("plan identity differs from frozen source")
    configuration = tomllib.loads((package / "lakefile.toml").read_text())
    production = configuration["defaultTargets"]
    support = next(x for x in configuration["lean_lib"] if x["name"] == "SourceDerivativeInputs")["roots"]
    elder_library = next(x for x in configuration["lean_lib"] if x["name"] == "SourceElderInputs")
    elder = elder_library["roots"]
    if elder_library.get("srcDir") != "inputs/elder":
        raise ValueError("registered elder source directory differs from exact plan")
    if production != plan["production"] or support != plan["support"] or elder != plan["elder"]:  # MUTATION_DOMAIN
        raise ValueError("registered production/support/elder domain differs from exact plan")
    if elder != ["SuperlevelBar", "ElderClearance", "ReusedCompactFrontier", "ClosedSuperlevel", "OrdinaryH0", "ElderInterval", "ElderBridge"]:  # MUTATION_ELDER_IDENTITIES
        raise ValueError("registered elder roots differ from frozen source")
    modules = elder + support + production
    if len(production) != 67 or len(support) != 25 or len(elder) != 7 or len(modules) != len(set(modules)):  # MUTATION_ELDER_COUNT
        raise ValueError("expected exactly 67 production and 32 unique support modules")
    for module in modules:
        if not isinstance(module, str) or not all(p.isidentifier() and p.isascii() for p in module.split(".")):
            raise ValueError("unsupported module name")
    sources = ["inputs/elder/" + m.replace(".", "/") + ".lean" for m in elder]
    sources += ["inputs/" + m.replace(".", "/") + ".lean" for m in support]
    sources += [m.replace(".", "/") + ".lean" for m in production]
    sources += ["lakefile.toml", "lake-manifest.json", "lean-toolchain"]
    if any(not (package / p).is_file() for p in sources):
        raise ValueError("registered source is absent")
    return modules, sources

def census_program(modules):
    literal = "#[" + ", ".join(chr(96) + m for m in modules) + "]"
    return "\n".join("import " + m for m in modules) + r'''
import Lean
open Lean Elab Command in
run_cmd do
  let env := (← getEnv).setExporting false
  let modules : Array Name := MODLITERAL
  let mut extras : Array (Name × Name) := #[]
  let mut extraNames : Std.HashSet Name := {}
  for modName in modules do
    let some idx := env.getModuleIdx? modName
      | throwError "missing independent census module: {modName}"
    for extraName in env.header.moduleData[idx]!.extraConstNames do
      extras := extras.push (modName, extraName)
      extraNames := extraNames.insert extraName
  let mut owners : Std.HashMap Name (Array Name) := {}
  for idx in [:env.header.moduleData.size] do
    let owner := env.header.moduleNames[idx]!
    for name in env.header.moduleData[idx]!.constNames do
      if extraNames.contains name then
        owners := owners.insert name ((owners[name]?.getD #[]).push owner)
  for (modName, extraName) in extras do
    let candidates := owners[extraName]?.getD #[]
    if (env.find? extraName).isSome then
      if candidates.size != 1 then
        throwError "kernel overlap has non-unique declaration provenance: {extraName} {candidates}"
      let resolved := (env.getModuleIdxFor? extraName).map fun idx => toString (env.header.moduleNames[idx]!)
      let metadata := Json.mkObj [
        ("module", Json.str (toString modName)), ("name", Json.str (toString extraName)),
        ("classification", Json.str "KERNEL_CODE_GENERATOR_OVERLAP"),
        ("declaring_modules", toJson (candidates.map toString)),
        ("resolved_module", toJson resolved)]
      liftIO <| IO.println s!"SOURCE514_CODEGEN_METADATA {metadata.compress}"
    else
      if !candidates.isEmpty then
        throwError "non-kernel extra has declaration-table provenance: {extraName}"
      let metadata := Json.mkObj [
        ("module", Json.str (toString modName)), ("name", Json.str (toString extraName)),
        ("classification", Json.str "NON_KERNEL_CODE_GENERATOR_OWNERSHIP")]
      liftIO <| IO.println s!"SOURCE514_CODEGEN_METADATA {metadata.compress}"
  for modName in modules do
    let some idx := env.getModuleIdx? modName
      | throwError "missing independent census module: {modName}"
    let data := env.header.moduleData[idx]!
    let names := data.constNames.qsort Name.lt
    if names.isEmpty then throwError "empty independent census module: {modName}"
    for name in names do
      let some ci := env.find? name | throwError "missing census declaration: {name}"
      if (env.checked.get.find? name).isNone then
        throwError "census declaration has no kernel declaration: {name}"
      let typeText ← liftTermElabM do
        return toString (← Lean.Meta.ppExpr ci.type)
      let kind := match ci with
        | .thmInfo _ => "theorem" | .defnInfo _ => "definition"
        | .axiomInfo _ => "axiom" | .opaqueInfo _ => "opaque"
        | .inductInfo _ => "inductive" | .ctorInfo _ => "constructor"
        | .recInfo _ => "recursor" | .quotInfo _ => "quotient"
      let userWritten := (← findDeclarationRanges? name).isSome
      let row := Json.mkObj [
        ("module", Json.str (toString modName)), ("name", Json.str (toString name)),
        ("kind", Json.str kind), ("type", Json.str typeText),
        ("user_written", toJson userWritten),
        ("user_name", Json.str (toString ((privateToUserName? name).getD name)))]
      liftIO <| IO.println s!"SOURCE514_CENSUS {row.compress}"
'''.replace("MODLITERAL", literal)

def parse_census(text, modules):
    def unique(pairs):
        value = {}
        for key, item in pairs:
            if key in value:
                raise ValueError("duplicate census JSON key")
            value[key] = item
        return value
    result = {"module_counts": {}, "module_declarations": {}}
    rows, extra_codegen, kernel_overlaps = [], [], []
    seen, extra_seen = set(), set()
    for line in text.splitlines():
        if line.startswith("SOURCE514_CODEGEN_METADATA "):
            metadata = json.loads(line.removeprefix("SOURCE514_CODEGEN_METADATA "), object_pairs_hook=unique)
            if not isinstance(metadata, dict):
                raise ValueError("invalid code-generator metadata")
            module, name = metadata.get("module"), metadata.get("name")
            if module not in modules or not isinstance(name, str) or not name:
                raise ValueError("invalid code-generator metadata identity")
            pair = (module, name)
            if pair in extra_seen:
                raise ValueError("duplicate code-generator metadata pair")
            extra_seen.add(pair)
            classification = metadata.get("classification")
            if classification == "NON_KERNEL_CODE_GENERATOR_OWNERSHIP":
                if set(metadata) != {"module", "name", "classification"}:
                    raise ValueError("invalid non-kernel code-generator metadata")
                extra_codegen.append(metadata)
            elif classification == "KERNEL_CODE_GENERATOR_OVERLAP":
                if set(metadata) != {"module", "name", "classification", "declaring_modules", "resolved_module"}:
                    raise ValueError("invalid kernel overlap metadata")
                candidates, resolved = metadata["declaring_modules"], metadata["resolved_module"]
                if not isinstance(candidates, list) or len(candidates) != 1 or not isinstance(candidates[0], str) or not candidates[0]:
                    raise ValueError("kernel overlap lacks unique declaration provenance")
                if resolved is not None and (not isinstance(resolved, str) or not resolved):
                    raise ValueError("invalid ownership-map observation")
                kernel_overlaps.append(metadata)
            else:
                raise ValueError("invalid code-generator metadata classification")
            continue
        if not line.startswith("SOURCE514_CENSUS "):
            raise ValueError("unrecognized independent census output")
        row = json.loads(line.removeprefix("SOURCE514_CENSUS "), object_pairs_hook=unique,
                         parse_constant=lambda value: (_ for _ in ()).throw(ValueError("nonfinite census JSON")) )
        if set(row) != {"module", "name", "kind", "type", "user_written", "user_name"}:
            raise ValueError("invalid census record fields")
        module, name = row["module"], row["name"]
        if module not in modules or name in seen or not isinstance(name, str) or not name:
            raise ValueError("invalid or duplicate census declaration")
        if row["kind"] not in {"theorem", "definition", "axiom", "opaque", "inductive", "constructor", "recursor", "quotient"}:
            raise ValueError("unsupported census declaration kind")
        if not isinstance(row["user_name"], str) or not row["user_name"]:
            raise ValueError("invalid census user name")
        if not isinstance(row["type"], str) or not row["type"] or type(row["user_written"]) is not bool:
            raise ValueError("invalid literal type/origin")
        seen.add(name)
        result["module_declarations"].setdefault(module, []).append(name)
        rows.append(row)
    if set(result["module_declarations"]) != set(modules):
        raise ValueError("independent census omitted a registered module")
    if seen & {item["name"] for item in extra_codegen}:
        raise ValueError("non-kernel code-generator metadata overlaps kernel census")
    for item in kernel_overlaps:
        owner, name = item["declaring_modules"][0], item["name"]
        if owner in modules:
            if name not in result["module_declarations"][owner]:
                raise ValueError("selected kernel overlap missing from unique declaring module")
        elif name in seen:
            raise ValueError("external kernel overlap incorrectly included in selected census")
    result["module_counts"] = {m: len(ns) for m, ns in result["module_declarations"].items()}
    if extra_codegen:
        result["non_kernel_codegen_ownership"] = extra_codegen
    if kernel_overlaps:
        result["kernel_codegen_overlaps"] = kernel_overlaps
    return result, rows

# The legacy replay program uses getModuleIdxFor?, whose ownership metadata
# may overlap a declaration actually owned by another module.  Preserve the
# original collector and proof-closure logic; replace only seed ownership with
# unique provenance from the complete imported constNames tables.
REPLAY_OWNER_ORIGINAL = '''  let mut seeds : Array Name := #[]
  for modName in modules do
    let some idx := env.getModuleIdx? modName
      | throwError "missing candidate module: {modName}"
    let names := (env.constants.toList.filterMap fun (name, _) =>
      if env.getModuleIdxFor? name == some idx then some name else none).toArray.qsort Name.lt'''

REPLAY_OWNER_REPLACEMENT = '''  -- REPLAY_DECLARATION_TABLE_PROVENANCE
  let mut tableOwners : Std.HashMap Name Name := {}
  for idx in [:env.header.moduleData.size] do
    let owner := env.header.moduleNames[idx]!
    for name in env.header.moduleData[idx]!.constNames do
      if (tableOwners[name]?).isSome then
        throwError "kernel declaration has ambiguous table provenance: {name}"
      tableOwners := tableOwners.insert name owner
  let mut seeds : Array Name := #[]
  for modName in modules do
    let some _idx := env.getModuleIdx? modName
      | throwError "missing candidate module: {modName}"
    let names := (env.constants.toList.filterMap fun (name, _) =>
      if tableOwners[name]? == some modName then some name else none).toArray.qsort Name.lt'''

def corrected_replay_program(tool, helper, modules):
    program, metadata = tool.generate_program(helper, COLLECTOR_SHA256, modules, modules)
    if program.count(REPLAY_OWNER_ORIGINAL) != 1:
        raise ValueError("unexpected original replay ownership program")
    corrected = program.replace(REPLAY_OWNER_ORIGINAL, REPLAY_OWNER_REPLACEMENT, 1)
    metadata = dict(metadata)
    metadata["original_program_sha256"] = metadata["program_sha256"]
    metadata["program_sha256"] = sha(corrected.encode())
    metadata["seed_ownership"] = "unique declaration-table provenance; getModuleIdxFor is not used"
    return corrected, metadata

def load(name, path, expected_sha256):
    data = Path(path).read_bytes()
    if sha(data) != expected_sha256:
        raise ValueError("loaded code differs from frozen source bytes")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    exec(compile(data, str(path), "exec"), module.__dict__)
    module.__source_sha256__ = sha(data)
    return module

def execute(source, replay, collector, plan_path, output, carrier, carrier_head, loaded_launcher_sha256):
    source, replay, collector, output = [p.resolve() for p in (source, replay, collector, output)]
    output.mkdir(parents=True, exist_ok=False)
    recorder_relative = "frontiers/regular_superlevel_geometry_20261020/c297_hosted_verify.py"
    recorder = load("c297_recorder", collector / recorder_relative, sha(git(collector, "cat-file", "blob", COLLECTOR_COMMIT + ":" + recorder_relative)))
    tool_path = replay / "cbz/evidence/kernel/additional/replay-tool/replay_tool.py"
    tool = load("bounded_replay", tool_path, sha(git(replay, "cat-file", "blob", REPLAY_COMMIT + ":cbz/evidence/kernel/additional/replay-tool/replay_tool.py")))
    plan, execution_before = execution_inputs(carrier, carrier_head, loaded_launcher_sha256, plan_path)
    package = source / PACKAGE
    modules, sources = checked_domain(package, plan)
    paths = [PACKAGE + "/" + p for p in sources]
    report = {"schema": "cbz-source514-hosted-observation-v1", "status": "RUNNING",
              "started_utc": datetime.now(timezone.utc).isoformat(), "phase_results": [],
              "repository": os.environ.get("GITHUB_REPOSITORY"), "run_id": os.environ.get("GITHUB_RUN_ID"),
              "run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"), "owned_modules": modules,
              "scope": "Exact frozen 99-module registered import closure; mathematical application and premise-inhabitation claims remain outside this replay.",
              "recorder_sha256": recorder.__source_sha256__, "replay_tool_sha256": tool.__source_sha256__,
              "launcher_sha256": loaded_launcher_sha256, "execution_inputs_before": execution_before}
    environment = lean_environment()
    def phase(name, command, cwd=package, timeout=1800):
        return recorder.run_phase(name, [str(x) for x in command], cwd, environment, output, report, timeout=timeout)
    try:
        report["source_before"] = bind(source, SOURCE_COMMIT, paths)
        report["replay_source"] = bind(replay, REPLAY_COMMIT, ["cbz/evidence/kernel/additional/replay-tool/replay_tool.py"])
        report["collector_source"] = bind(collector, COLLECTOR_COMMIT, [
            "formal/gate_helper.py", "frontiers/regular_superlevel_geometry_20261020/c297_hosted_verify.py"])
        helper = collector / "formal/gate_helper.py"
        if sha(helper.read_bytes()) != COLLECTOR_SHA256:
            raise ValueError("collector bytes differ from declared verified helper")
        version, _, _ = phase("runtime-version", ["lake", "env", "lean", "--version"])
        version_text = (output / "runtime-version.stdout").read_text()
        if "Lean (version 4.34.1," not in version_text or "commit 5045d0056413266e57c625dcd7c365b10e377c52" not in version_text:
            raise ValueError("runtime differs from exact pinned Lean release")
        lock = json.loads((package / "lake-manifest.json").read_text())
        expected_revisions = {row["name"]: row["rev"] for row in lock["packages"]}
        if expected_revisions != recorder.PACKAGE_PINS:
            raise ValueError("dependency vector differs from verified standard runtime")
        with frozen_dependencies(package, lock) as dependency_records:
            report["dependencies"] = dependency_records
            for number, module in enumerate(modules):
                phase("build-" + str(number).zfill(2) + "-" + module.replace(".", "_"), ["lake", "build", "+" + module])
            with frozen_objects(package, expected_revisions) as object_records:
                # The source packet itself supplies a reproducible genuine
                # extraConstNames/constNames overlap.  Require the overlap,
                # kernel replay its actual owner once, and execute an omitted
                # seed mutant that the transcript validator must reject for
                # the exact beginning/completion count discrepancy.
                fixture_module = "SourceFourierSeries"
                fixture_name = "_private.SourceFourierSeries.0.I4Source.modeCoefficient.match_1.splitter"
                fixture_census_path = output / "OverlapFixtureCensus.lean"
                fixture_census_path.write_text(census_program([fixture_module]))
                phase("overlap-fixture-census", ["lake", "env", "lean", "-j2", "-M12000", fixture_census_path], timeout=2700)
                if (output / "overlap-fixture-census.stderr").read_bytes():
                    raise ValueError("overlap fixture census emitted stderr")
                fixture_expected, _ = parse_census((output / "overlap-fixture-census.stdout").read_text(), [fixture_module])
                fixture_overlaps = [item for item in fixture_expected.get("kernel_codegen_overlaps", [])
                                    if item["name"] == fixture_name]
                if not fixture_overlaps or any(item["declaring_modules"] != [fixture_module] for item in fixture_overlaps):
                    raise ValueError("actual fixture did not establish the declared kernel overlap and owner")
                if fixture_expected["module_declarations"][fixture_module].count(fixture_name) != 1:
                    raise ValueError("actual fixture overlap is not present exactly once in the kernel census")
                fixture_program, fixture_metadata = corrected_replay_program(tool, helper, [fixture_module])
                fixture_program_path = output / "OverlapFixtureReplay.lean"
                fixture_program_path.write_text(fixture_program)
                _, _, fixture_code = phase("overlap-fixture-replay", ["lake", "env", "lean", "-j2", "-M12000", fixture_program_path], timeout=2700)
                fixture_result = tool.validate_transcript(
                    (output / "overlap-fixture-replay.stdout").read_text(), fixture_expected,
                    fixture_metadata["program_sha256"], exit_code=fixture_code,
                    stderr=(output / "overlap-fixture-replay.stderr").read_text())
                original_seed = "      seeds := seeds.push name"
                mutated_seed = "      if name != `" + fixture_name + " then seeds := seeds.push name"
                if fixture_program.count(original_seed) != 1:
                    raise ValueError("overlap fixture seed mutation target is not unique")
                mutated_program = fixture_program.replace(original_seed, mutated_seed, 1)
                mutated_path = output / "OverlapFixtureOmittedSeed.lean"
                mutated_path.write_text(mutated_program)
                _, _, mutated_code = phase("overlap-fixture-omitted-seed", ["lake", "env", "lean", "-j2", "-M12000", mutated_path], timeout=2700)
                try:
                    tool.validate_transcript(
                        (output / "overlap-fixture-omitted-seed.stdout").read_text(), fixture_expected,
                        sha(mutated_program.encode()), exit_code=mutated_code,
                        stderr=(output / "overlap-fixture-omitted-seed.stderr").read_text())
                except ValueError as error:
                    if str(error) != "replay beginning/completion/census counts disagree":
                        raise ValueError("overlap mutant failed for an unintended reason") from error
                else:
                    raise ValueError("overlap omitted-seed mutant was not detected")
                report["actual_overlap_fixture"] = {"name": fixture_name, "observations": fixture_overlaps,
                    "positive_replay": fixture_result, "omitted_seed_mutant": "EXPECTED_COUNT_MISMATCH"}
                census_path = output / "IndependentCensus.lean"
                census_path.write_text(census_program(modules))
                phase("independent-compiled-census", ["lake", "env", "lean", "-j2", "-M12000", census_path], timeout=2700)
                stderr = (output / "independent-compiled-census.stderr").read_bytes()
                if stderr:
                    raise ValueError("independent census emitted stderr")
                expected, literals = parse_census((output / "independent-compiled-census.stdout").read_text(), modules)
                (output / "compiled-census.json").write_text(json.dumps(expected, indent=2) + "\n")
                (output / "compiled-literal-types.json").write_text(json.dumps(literals, indent=2, ensure_ascii=False) + "\n")
                program, metadata = tool.generate_program(helper, COLLECTOR_SHA256, modules, modules)
                program_path = output / "BoundedKernelReplay.lean"
                program_path.write_text(program)
                (output / "replay-program.json").write_text(json.dumps(metadata, indent=2) + "\n")
                _, _, code = phase("bounded-kernel-replay", ["lake", "env", "lean", "-j2", "-M12000", program_path], timeout=2700)
                consistency = tool.validate_transcript((output / "bounded-kernel-replay.stdout").read_text(), expected,
                    metadata["program_sha256"], exit_code=code, stderr=(output / "bounded-kernel-replay.stderr").read_text())
            report["compiled_objects"] = object_records
        report["source_after"] = bind(source, SOURCE_COMMIT, paths)
        if report["source_after"] != report["source_before"]:
            raise ValueError("bound source changed during execution")
        if bind(replay, REPLAY_COMMIT, ["cbz/evidence/kernel/additional/replay-tool/replay_tool.py"]) != report["replay_source"]:
            raise ValueError("replay source changed during execution")
        if bind(collector, COLLECTOR_COMMIT, ["formal/gate_helper.py", "frontiers/regular_superlevel_geometry_20261020/c297_hosted_verify.py"]) != report["collector_source"]:
            raise ValueError("collector/recorder source changed during execution")
        _, execution_after = execution_inputs(carrier, carrier_head, loaded_launcher_sha256, plan_path)
        if execution_after != execution_before:
            raise ValueError("launcher/plan execution inputs changed")
        report["execution_inputs_after"] = execution_after
        report["replay_observation"] = consistency
        report["literal_records"] = len(literals)
        report["user_theorems"] = sum(r["kind"] == "theorem" and r["user_written"] for r in literals)
        report["status"] = "ACTUAL_BUILD_AND_EMPTY_KERNEL_REPLAY_PASS"
    except BaseException as error:
        report["status"] = "NOT_PASS"
        report["error"] = repr(error)
        raise
    finally:
        report["finished_utc"] = datetime.now(timezone.utc).isoformat()
        recorder.save_report(output, report)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ["source", "replay", "collector", "plan", "output"]:
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--carrier", type=Path, required=True)
    parser.add_argument("--carrier-head", required=True)
    args = parser.parse_args()
    execute(args.source, args.replay, args.collector, args.plan, args.output, args.carrier, args.carrier_head, globals().get("_CBZ_LOADED_SHA256"))

if __name__ == "__main__":
    if globals().get("_CBZ_LOADED_SHA256") is None:
        carrier = Path(__file__).resolve().parents[1]
        head = git(carrier, "rev-parse", "HEAD").decode().strip()
        relative = "tools/cbz_source514_hosted.py"
        immutable = git(carrier, "cat-file", "blob", head + ":" + relative)
        if Path(__file__).read_bytes() != immutable:
            raise ValueError("launcher working bytes differ from immutable Git source")
        namespace = {"__name__": "__main__", "__file__": str(carrier / relative),
                     "_CBZ_LOADED_SHA256": sha(immutable)}
        exec(compile(immutable, str(carrier / relative), "exec"), namespace)
    else:
        main()
