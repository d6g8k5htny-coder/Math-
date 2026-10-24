"""Static-validator controls using temporary copies; never invokes Lean or Lake."""

import argparse
import builtins
from contextlib import contextmanager, ExitStack
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from unittest.mock import patch

import validate_static as checker


if not __debug__:
    raise RuntimeError("Static-validator controls require assertions; disable Python optimization.")


ROOT = Path(__file__).resolve().parent
AUDIT_OUTPUT = "evidence/SourceLifetimeAxiomAudit.development.stdout.txt"
SUMMARY = "evidence/DEVELOPMENT_COMPILE_SUMMARY.json"
CENSUS_FAILURE = "module mapping does not match package Lean sources"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def inventory(allow_lake_build=False):
    return {p.relative_to(checker.ROOT).as_posix(): checker.sha(p.read_bytes())
            for p in checker.package_paths(allow_lake_build) if p.is_file()}


@contextmanager
def copied_package():
    # Do not copy or descend into a real caller's potentially large cache.
    def ignore_cache(directory, names):
        return {".lake"} if Path(directory) == ROOT and ".lake" in names else set()

    with tempfile.TemporaryDirectory(prefix="c291-static-controls-") as temporary:
        package = Path(temporary) / "package"
        shutil.copytree(ROOT, package, symlinks=True, ignore=ignore_cache)
        with patch.object(checker, "ROOT", package):
            yield package


def check_success(result, allow_lake_build):
    expected = "PASS_SOURCE_STATIC_ONLY" if allow_lake_build else "PASS_STATIC_ONLY"
    require(result["status"] == expected, "wrong validation status")
    require(result["validation_mode"] == (
        "source_workspace" if allow_lake_build else "publication"), "wrong validation mode")
    require(result["excluded_paths"] == ([".lake"] if allow_lake_build else []),
            "wrong cache exclusion report")
    require(result["cache_excluded_from_package_scan"] is allow_lake_build,
            "wrong package-scan exclusion claim")
    require(result["cache_validation"] == "NOT_PERFORMED", "must not claim cache validation")
    require(result["module_count"] == 19, "wrong source module count")
    require(result["recorded_development_audit_declarations"] == 409,
            "wrong retained audit count")


def reject(label, overrides, allow_lake_build):
    read_bytes = Path.read_bytes
    read_text = Path.read_text

    def relative(path):
        try:
            return path.relative_to(checker.ROOT).as_posix()
        except ValueError:
            return None

    def changed_bytes(path):
        key = relative(path)
        return overrides[key] if key in overrides else read_bytes(path)

    def changed_text(path, *args, **kwargs):
        key = relative(path)
        return overrides[key].decode("utf-8") if key in overrides else read_text(path, *args, **kwargs)

    with patch.object(Path, "read_bytes", changed_bytes), patch.object(Path, "read_text", changed_text):
        try:
            checker.validate(allow_lake_build=allow_lake_build)
        except AssertionError as error:
            return {"case": label, "allow_lake_build": allow_lake_build,
                    "expected_rejection_observed": True, "diagnostic": str(error)}
    raise RuntimeError("Validator accepted a required negative control: " + label)


def audit_overrides(text):
    data = text.encode("utf-8")
    summary = json.loads((checker.ROOT / SUMMARY).read_text())
    receipt = next(r for r in summary["receipts"] if r["source"] == "SourceLifetimeAxiomAudit.lean")
    # Reach the semantic output checks instead of stopping at the stream hash.
    receipt["stdout_sha256"] = checker.sha(data)
    return {AUDIT_OUTPUT: data, SUMMARY: (json.dumps(summary, indent=2) + "\n").encode()}


def content_controls(allow_lake_build):
    root = checker.ROOT
    results = []
    proof = "SourceThetaBridge.lean"
    results.append(reject("modified_proof_source", {
        proof: (root / proof).read_bytes() + b"\n"}, allow_lake_build))
    manifest = json.loads((root / "lake-manifest.json").read_text())
    manifest["packages"][0]["rev"] = "0" * 40
    results.append(reject("changed_dependency_pin", {
        "lake-manifest.json": (json.dumps(manifest, indent=2) + "\n").encode()
    }, allow_lake_build))
    config = (root / "lakefile.toml").read_text()
    changed = config.replace(
        'defaultTargets = ["C291Inputs", "SourceLifetimeControls", "SourceLifetimeAxiomAudit"]',
        'defaultTargets = ["C291Inputs", "SourceLifetimeControls"]')
    require(changed != config, "missing default-target mutation anchor")
    results.append(reject("omitted_default_axiom_audit_target", {
        "lakefile.toml": changed.encode()}, allow_lake_build))
    results.append(reject("wrong_input_source_directory", {
        "lakefile.toml": config.replace('srcDir = "inputs"', 'srcDir = "."').encode()
    }, allow_lake_build))
    identity_path = "inputs/provenance/FILE_IDENTITIES.json"
    identities = json.loads((root / identity_path).read_text())
    identities["files"] = [r for r in identities["files"] if r["path"] != "SourceLifetimeAxiomAudit.lean"]
    results.append(reject("omitted_audit_source_identity", {
        identity_path: (json.dumps(identities, indent=2) + "\n").encode()
    }, allow_lake_build))
    output = (root / AUDIT_OUTPUT).read_text()
    missing = re.sub(r"^LIFETIME_AUDIT_DECL \S+ AXIOMS \[[^\]]*\]\n", "", output, count=1, flags=re.M)
    require(missing != output, "missing audit-declaration mutation anchor")
    results.append(reject("omitted_audit_declaration_with_rebound_digest",
                          audit_overrides(missing), allow_lake_build))
    forbidden = output.replace("AXIOMS [propext", "AXIOMS [sorryAx", 1)
    require(forbidden != output, "missing forbidden-axiom mutation anchor")
    results.append(reject("forbidden_axiom_with_rebound_digest",
                          audit_overrides(forbidden), allow_lake_build))
    readme = (root / "README.md").read_bytes()
    results.append(reject("private_root_path", {
        "README.md": readme + b"\n/" + b"root/private-evidence.txt\n"}, allow_lake_build))
    results.append(reject("agent_prefix_is_not_a_path_allowlist", {
        "README.md": readme + b"\n/" + b"root/c291_nonauthor_review/private.txt\n"
    }, allow_lake_build))
    require(not checker.contains_private_path(b"OpenAI Codex `/" + b"root/c291_nonauthor_review`."),
            "disclosed agent token was rejected")
    return results


def expect_filesystem_rejection(label, mode, expected):
    try:
        checker.validate(allow_lake_build=mode)
    except AssertionError as error:
        diagnostic = str(error)
        require(expected in diagnostic, label + ": unrelated rejection: " + diagnostic)
        return {"case": label, "allow_lake_build": mode,
                "expected_rejection_observed": True, "diagnostic": diagnostic}
    raise RuntimeError("Validator accepted filesystem negative control: " + label)


def add_file(package, relative, data):
    path = package / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def filesystem_controls():
    results = []
    fixtures = [
        ("extra_root_lean", "Unregistered.lean", b"def unexpected : Nat := 0\n", CENSUS_FAILURE),
        ("extra_input_lean", "inputs/Unregistered.lean", b"def unexpected : Nat := 0\n", CENSUS_FAILURE),
        ("cache_name_lookalike", ".lake-copy/Unregistered.lean", b"def unexpected : Nat := 0\n", CENSUS_FAILURE),
        ("outside_compiled_object", "outside.olean", b"\xff\x00", "outside.olean"),
        ("outside_private_path", "extra.txt", b"/" + b"root/private.txt\n", "extra.txt"),
        ("nested_cache", "inputs/.lake/probe.txt", b"opaque\n", "inputs/.lake"),
        ("outside_python_cache", "__pycache__/probe.pyc", b"\xff\x00", "__pycache__"),
        ("nested_python_cache", "inputs/__pycache__/probe.pyc", b"\xff\x00", "inputs/__pycache__"),
        ("cache_is_file", ".lake", b"not a directory\n", ".lake"),
    ]
    for label, relative, data, expected in fixtures:
        with copied_package() as package:
            add_file(package, relative, data)
            for mode in (False, True):
                results.append(expect_filesystem_rejection(label, mode, expected))
    for label, relative in (("cache_symlink_escape", ".lake"),
                            ("outside_symlink_escape", "escape.txt")):
        with copied_package() as package:
            outside = package.parent / "outside"
            outside.mkdir()
            (outside / "private.txt").write_bytes(b"uninspected\n")
            (package / relative).symlink_to(outside, target_is_directory=True)
            for mode in (False, True):
                results.append(expect_filesystem_rejection(label, mode, relative))
    return results


def opaque_cache_control():
    with copied_package() as package:
        add_file(package, ".lake/packages/Fake/CacheProbe.lean", b"axiom cacheOnly : False\n")
        add_file(package, ".lake/build/Opaque.olean", b"\xff\x00/" + b"root/cache-only.txt\n")
        add_file(package, ".lake/nested/__pycache__/probe.pyc", b"\xff\x00")
        strict = expect_filesystem_rejection("strict_rejects_build_cache", False, ".lake")
        cache = package / ".lake"
        blocked = []

        def guarded(original, name):
            def invoke(path, *args, **kwargs):
                if not isinstance(path, int):
                    candidate = Path(os.fsdecode(path)).absolute()
                    if candidate == cache or cache in candidate.parents:
                        blocked.append(name)
                        raise RuntimeError("opaque cache access: " + name)
                return original(path, *args, **kwargs)
            return invoke

        targets = [(os, "scandir"), (Path, "iterdir"), (Path, "glob"), (Path, "rglob"),
                   (Path, "read_bytes"), (Path, "read_text"), (builtins, "open"), (io, "open")]
        with ExitStack() as stack:
            for owner, name in targets:
                stack.enter_context(patch.object(owner, name, guarded(getattr(owner, name), name)))
            # First prove that every instrumented entrypoint is actually guarded.
            probes = [lambda: os.scandir(cache), lambda: cache.iterdir(),
                      lambda: cache.glob("*"), lambda: cache.rglob("*"),
                      lambda: (cache / "probe").read_bytes(),
                      lambda: (cache / "probe").read_text(),
                      lambda: builtins.open(cache / "probe"), lambda: io.open(cache / "probe")]
            for probe in probes:
                try:
                    probe()
                except RuntimeError as error:
                    require(str(error).startswith("opaque cache access:"), "wrong guard error")
                else:
                    raise RuntimeError("opaque-cache guard did not reject its probe")
            require(len(blocked) == len(targets), "incomplete opaque-cache guard probes")
            blocked.clear()
            before = inventory(True)
            result = checker.validate(allow_lake_build=True)
            check_success(result, True)
            require(inventory(True) == before, "workspace source inventory changed")
            require(blocked == [], "workspace validation accessed the excluded cache")

        # Reintroduce the original inventory defect without editing any source.
        original_paths = checker.package_paths

        def leaked_cache_paths(allow_lake_build=False):
            paths = list(original_paths(allow_lake_build))
            return paths + [cache / "packages/Fake/CacheProbe.lean"]

        with patch.object(checker, "package_paths", leaked_cache_paths):
            mutant = expect_filesystem_rejection("cache_inventory_leak_mutant", True, CENSUS_FAILURE)
        return {"case": "opaque_build_cache", "workspace_status": result["status"],
                "excluded_paths": result["excluded_paths"],
                "cache_excluded_from_package_scan": True, "cache_validation": "NOT_PERFORMED",
                "optional_direct_source_arguments": "NOT_SUPPLIED",
                "guard_self_probes": len(targets), "guarded_cache_accesses": len(blocked),
                "instrumented_entrypoints": [owner.__name__ + "." + name for owner, name in targets],
                "strict_rejection": strict, "cache_inventory_mutant": mutant}


def optional_source_controls():
    # Requested direct import files may live inside the excluded cache. These
    # inert comments test presence/hash reporting, never Lean validity.
    with copied_package() as package:
        baseline = checker.validate(allow_lake_build=True)
        mathlib = package / ".lake/optional-mathlib"
        lean = package / ".lake/optional-lean"
        expected = {"mathlib": {}, "lean": {}}
        paths = {"mathlib": [], "lean": []}
        for module in baseline["external_imports"]:
            family = "lean" if module == "Lean" or module.startswith("Lean.") else "mathlib"
            relative = module.replace(".", "/") + ".lean"
            directory = lean if family == "lean" else mathlib
            data = ("-- inert direct-source fixture: " + module + "\n").encode()
            path = directory / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            expected[family][module] = checker.sha(data)
            paths[family].append((path, relative))
        require(expected["mathlib"] and expected["lean"], "direct-source fixture lacks an import family")
        before = inventory(True)

        def validate_requested():
            return checker.validate(mathlib_source=mathlib, lean_source=lean, allow_lake_build=True)

        result = validate_requested()
        check_success(result, True)
        require(result["external_source_check"] == "DIRECT_MATHLIB_SOURCE_FILES_PRESENT",
                "requested Mathlib presence check missing")
        require(result["toolchain_source_check"] == "DIRECT_LEAN_SOURCE_FILES_PRESENT",
                "requested Lean presence check missing")
        require({r["module"]: r["sha256"] for r in result["external_source_files"]} == expected["mathlib"],
                "direct Mathlib file hashes do not match")
        require({r["module"]: r["sha256"] for r in result["toolchain_source_files"]} == expected["lean"],
                "direct Lean file hashes do not match")
        missing = []
        for family in ("mathlib", "lean"):
            path, relative = paths[family][0]
            data = path.read_bytes()
            path.unlink()
            try:
                try:
                    validate_requested()
                except AssertionError as error:
                    diagnostic = str(error)
                    prefix = "missing pinned external source: " if family == "mathlib" else "missing pinned toolchain source: "
                    require(diagnostic == prefix + relative, "unrelated direct-source failure")
                    missing.append({"family": family, "expected_rejection_observed": True,
                                    "diagnostic": diagnostic})
                else:
                    raise RuntimeError("missing requested " + family + " source was accepted")
            finally:
                path.write_bytes(data)
        require(inventory(True) == before, "optional-source checks changed included package bytes")
        return {"case": "optional_direct_sources_inside_cache",
                "scope": "Synthetic direct-file presence and hash checks; not authentic dependency or Lean validation.",
                "cache_excluded_from_package_scan": True, "cache_validation": "NOT_PERFORMED",
                "direct_mathlib_records": len(expected["mathlib"]),
                "direct_lean_records": len(expected["lean"]),
                "direct_record_hashes_match": True, "missing_source_controls": missing}


def optimization_controls():
    guards = []
    for mode in (False, True):
        for label, options, environment in [
            ("explicit_python_optimization", ["-O", "-B", "-S"], dict(os.environ)),
            ("environment_python_optimization", ["-B", "-S"], dict(os.environ, PYTHONOPTIMIZE="1")),
        ]:
            command = [sys.executable] + options + ["validate_static.py"]
            if mode:
                command.append("--allow-lake-build")
            run = subprocess.run(command, cwd=ROOT, env=environment,
                                 capture_output=True, timeout=15)
            require(run.returncode == 1 and run.stdout == b"", "wrong optimized-Python failure")
            require(b"Static validation requires assertions; disable Python optimization." in run.stderr,
                    "optimization refusal diagnostic missing")
            guards.append({"case": label, "allow_lake_build": mode,
                           "returncode": run.returncode, "expected_rejection_observed": True,
                           "stdout_sha256": checker.sha(run.stdout),
                           "stderr_sha256": checker.sha(run.stderr)})
    return guards


def main(allow_lake_build=False):
    before = inventory(allow_lake_build)
    baseline = checker.validate(allow_lake_build=allow_lake_build)
    check_success(baseline, allow_lake_build)
    mutations = []
    with copied_package():
        for mode in (False, True):
            check_success(checker.validate(allow_lake_build=mode), mode)
            mutations.extend(content_controls(mode))
    fixtures = filesystem_controls()
    cache = opaque_cache_control()
    optional = optional_source_controls()
    guards = optimization_controls()
    require(len(mutations) == 18 and len(fixtures) == 22 and len(guards) == 4,
            "incomplete static-control campaign")
    require(inventory(allow_lake_build) == before, "audited package bytes changed during controls")
    return {
        "schema_version": 2,
        "status": "PASS_STATIC_CONTROLS_ONLY",
        "scope": "Nine virtual content corruptions in both modes, real copied-package filesystem controls, opaque-cache access instrumentation and a cache-inventory leak mutant, plus two optimization refusals in both modes. Temporary fixtures only; no Lean/Lake, network, or original-source mutation.",
        "validation_mode": baseline["validation_mode"],
        "excluded_paths": baseline["excluded_paths"],
        "cache_excluded_from_package_scan": baseline["cache_excluded_from_package_scan"],
        "cache_validation": baseline["cache_validation"],
        "baseline_status": baseline["status"],
        "validator_sha256": checker.sha((ROOT / "validate_static.py").read_bytes()),
        "controls_sha256": checker.sha((ROOT / "test_static_validator.py").read_bytes()),
        "identity_manifest_sha256": baseline["identity_manifest_sha256"],
        "outside_cache_package_bytes_unchanged": True,
        "mutation_controls": mutations,
        "filesystem_controls": fixtures,
        "opaque_cache_control": cache,
        "optional_source_controls": optional,
        "optimization_guards": guards,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--allow-lake-build", action="store_true")
    args = parser.parse_args()
    print(json.dumps(main(args.allow_lake_build), indent=2))
