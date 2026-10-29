#!/usr/bin/env python3
"""Execute a frozen package with the already self-tested bounded Lean replay.
This recorder does not replace Lean's kernel or authenticate supplied transcripts.
"""
from __future__ import annotations
import argparse
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

def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args])

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

def checked_domain(package, plan):
    if plan.get("schema") != "cbz-source514-exact-domain-v1" or plan.get("source_commit") != SOURCE_COMMIT:
        raise ValueError("plan identity differs from frozen source")
    configuration = tomllib.loads((package / "lakefile.toml").read_text())
    production = configuration["defaultTargets"]
    support = next(x for x in configuration["lean_lib"] if x["name"] == "SourceDerivativeInputs")["roots"]
    if production != plan["production"] or support != plan["support"]:  # MUTATION_DOMAIN
        raise ValueError("registered production/support domain differs from exact plan")
    modules = support + production
    if len(production) != 67 or len(support) != 25 or len(modules) != len(set(modules)):
        raise ValueError("expected exactly 67 production and 25 unique support modules")
    for module in modules:
        if not isinstance(module, str) or not all(p.isidentifier() and p.isascii() for p in module.split(".")):
            raise ValueError("unsupported module name")
    sources = ["inputs/" + m.replace(".", "/") + ".lean" for m in support]
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
  for modName in modules do
    let some idx := env.getModuleIdx? modName
      | throwError "missing independent census module: {modName}"
    let data := env.header.moduleData[idx]!
    let names := (data.constNames ++ data.extraConstNames).toList.eraseDups.toArray.qsort Name.lt
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
    rows = []
    seen = set()
    for line in text.splitlines():
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
    result["module_counts"] = {m: len(ns) for m, ns in result["module_declarations"].items()}
    return result, rows

def load(name, path, expected_sha256):
    data = Path(path).read_bytes()
    if sha(data) != expected_sha256:
        raise ValueError("loaded code differs from frozen source bytes")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    exec(compile(data, str(path), "exec"), module.__dict__)
    module.__source_sha256__ = sha(data)
    return module

def execute(source, replay, collector, plan_path, output):
    source, replay, collector, output = [p.resolve() for p in (source, replay, collector, output)]
    output.mkdir(parents=True, exist_ok=False)
    recorder_relative = "frontiers/regular_superlevel_geometry_20261020/c297_hosted_verify.py"
    recorder = load("c297_recorder", collector / recorder_relative, sha(git(collector, "cat-file", "blob", COLLECTOR_COMMIT + ":" + recorder_relative)))
    tool_path = replay / "cbz/evidence/kernel/additional/replay-tool/replay_tool.py"
    tool = load("bounded_replay", tool_path, sha(git(replay, "cat-file", "blob", REPLAY_COMMIT + ":cbz/evidence/kernel/additional/replay-tool/replay_tool.py")))
    plan = json.loads(plan_path.read_text())
    package = source / PACKAGE
    modules, sources = checked_domain(package, plan)
    paths = [PACKAGE + "/" + p for p in sources]
    report = {"schema": "cbz-source514-hosted-observation-v1", "status": "RUNNING",
              "started_utc": datetime.now(timezone.utc).isoformat(), "phase_results": [],
              "repository": os.environ.get("GITHUB_REPOSITORY"), "run_id": os.environ.get("GITHUB_RUN_ID"),
              "run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"), "owned_modules": modules,
              "scope": "Exact frozen 92-module registered import closure; seven unconsumed elder copies and mathematical application/nonvacuity claims remain outside this replay.",
              "recorder_sha256": recorder.__source_sha256__, "replay_tool_sha256": tool.__source_sha256__,
              "launcher_sha256": sha(Path(__file__).read_bytes()), "plan_sha256": sha(plan_path.read_bytes())}
    environment = dict(os.environ, LEAN_NUM_THREADS="2")
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
        dependencies = {}
        for dependency in lock["packages"]:
            if dependency["type"] != "git":
                raise ValueError("unexpected non-Git dependency")
            dep = package / ".lake/packages" / dependency["name"]
            head = git(dep, "rev-parse", "HEAD").decode().strip()
            if head != dependency["rev"] or git(dep, "status", "--porcelain", "--untracked-files=no"):
                raise ValueError("dependency source differs from lock: " + dependency["name"])
            dependencies[dependency["name"]] = head
        if dependencies != recorder.PACKAGE_PINS:
            raise ValueError("dependency vector differs from verified standard runtime")
        report["dependencies"] = dependencies
        for number, module in enumerate(modules):
            phase("build-" + str(number).zfill(2) + "-" + module.replace(".", "_"), ["lake", "build", "+" + module])
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
        objects_before = {str(p.relative_to(package)): sha(p.read_bytes()) for p in sorted((package / ".lake/build/lib/lean").rglob("*.olean*")) if p.is_file()}
        if not objects_before:
            raise ValueError("owned compiled objects absent")
        _, _, code = phase("bounded-kernel-replay", ["lake", "env", "lean", "-j2", "-M12000", program_path], timeout=2700)
        consistency = tool.validate_transcript((output / "bounded-kernel-replay.stdout").read_text(), expected,
            metadata["program_sha256"], exit_code=code, stderr=(output / "bounded-kernel-replay.stderr").read_text())
        objects_after = {str(p.relative_to(package)): sha(p.read_bytes()) for p in sorted((package / ".lake/build/lib/lean").rglob("*.olean*")) if p.is_file()}
        if objects_after != objects_before:
            raise ValueError("owned objects changed during kernel replay")
        report["source_after"] = bind(source, SOURCE_COMMIT, paths)
        if report["source_after"] != report["source_before"]:
            raise ValueError("bound source changed during execution")
        if bind(replay, REPLAY_COMMIT, ["cbz/evidence/kernel/additional/replay-tool/replay_tool.py"]) != report["replay_source"]:
            raise ValueError("replay source changed during execution")
        if bind(collector, COLLECTOR_COMMIT, ["formal/gate_helper.py", "frontiers/regular_superlevel_geometry_20261020/c297_hosted_verify.py"]) != report["collector_source"]:
            raise ValueError("collector/recorder source changed during execution")
        report["owned_objects"] = objects_after
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
    args = parser.parse_args()
    execute(args.source, args.replay, args.collector, args.plan, args.output)

if __name__ == "__main__":
    main()
