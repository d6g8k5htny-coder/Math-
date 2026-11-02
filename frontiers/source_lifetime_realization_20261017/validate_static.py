"""Validate package identities and static mappings without Lean, Lake, or writes.

The TOML reader accepts only the generated configuration's JSON-compatible
assignments and array-of-table headers. It is not a general TOML implementation.
"""

import argparse
import hashlib
import json
from pathlib import Path
import re


if not __debug__:
    raise RuntimeError("Static validation requires assertions; disable Python optimization.")


ROOT = Path(__file__).resolve().parent
NEW_MODULES = {
    "SourceThetaBridge", "SourceLifetimeGeometry", "SourceLifetimeField",
    "SourceLifetimeControls", "SourceLifetimeAxiomAudit",
}


def package_paths(allow_lake_build=False):
    """List inspected paths without entering the explicitly excluded cache.

    Publication mode admits no cache. Workspace mode ignores only a real
    top-level .lake directory; its contents are outside this validator's claim.
    Check symlinks before directory descent, including the excluded root.
    """
    paths = []

    def visit(directory):
        for path in sorted(directory.iterdir()):
            relative = path.relative_to(ROOT)
            label = relative.as_posix()
            assert not path.is_symlink(), "symlink is not allowed: " + label
            if allow_lake_build and relative.parts == (".lake",):
                assert path.is_dir(), "top-level .lake must be a real directory: " + label
                continue
            assert ".lake" not in relative.parts, "cache outside allowed scope: " + label
            assert "__pycache__" not in relative.parts, "Python cache is not allowed: " + label
            assert path.suffix not in {".olean", ".ilean", ".o", ".a", ".so", ".dylib", ".pyc"}, \
                "compiled artifact is not allowed: " + label
            paths.append(path)
            if path.is_dir():
                visit(path)
            else:
                assert path.is_file(), "non-regular entry is not allowed: " + label

    visit(ROOT)
    return paths


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git_blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def contains_private_path(data):
    # Exact disclosed agent identifiers are provenance, not filesystem roots.
    # A trailing slash or path-like continuation remains prohibited.
    without_agents = re.sub(
        rb"/(?:root)/(?:c291_nonauthor_review|c291_field_feasibility|c290_theta_bridge)(?![A-Za-z0-9_./-])",
        b"DISCLOSED_AGENT", data)
    return re.search(rb"/(?:Users|home|root)/", without_agents) is not None


def read_generated_toml(path):
    result = {}
    current = result
    lines = iter(path.read_text().splitlines())
    for raw in lines:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        header = re.fullmatch(r"\[\[([A-Za-z_][A-Za-z_0-9]*)\]\]", line)
        if header:
            current = {}
            result.setdefault(header.group(1), []).append(current)
            continue
        assignment = re.fullmatch(r"([A-Za-z_][A-Za-z_0-9]*)\s*=\s*(.*)", line)
        assert assignment, "unsupported generated TOML syntax: " + line
        key, value = assignment.groups()
        if value.startswith("[") and not value.endswith("]"):
            while not value.rstrip().endswith("]"):
                value += "\n" + next(lines).strip()
        value = re.sub(r",\s*\]$", "]", value)
        assert key not in current, "duplicate generated TOML key: " + key
        current[key] = json.loads(value)
    return result


def validate(mathlib_source=None, lean_source=None, allow_lake_build=False):
    paths = package_paths(allow_lake_build)
    identity_path = ROOT / "inputs/provenance/FILE_IDENTITIES.json"
    identities = json.loads(identity_path.read_text())["files"]
    assert len(identities) == 22, "expected 19 Lean sources and 3 original build files"
    assert len({r["path"] for r in identities}) == len(identities)
    for record in identities:
        path = ROOT / record["path"]
        assert path.is_file() and not path.is_symlink(), record["path"]
        data = path.read_bytes()
        assert len(data) == record["bytes"], record["path"]
        assert sha(data) == record["sha256"], record["path"]
        assert git_blob(data) == record["git_blob"], record["path"]
        if "expected_git_blob" in record:
            assert record["git_blob"] == record["expected_git_blob"], record["path"]

    config = read_generated_toml(ROOT / "lakefile.toml")
    original_config = read_generated_toml(ROOT / "inputs/provenance/source-lakefile.toml")
    manifest = json.loads((ROOT / "lake-manifest.json").read_text())
    original = json.loads((ROOT / "inputs/provenance/source-lake-manifest.json").read_text())
    expected_manifest = dict(original, name="source_lifetime_realization")
    assert manifest == expected_manifest, "manifest changed beyond root package name"
    assert config["name"] == manifest["name"]
    assert config["require"] == original_config["require"]
    assert len(manifest["packages"]) == 9
    assert len({p["name"] for p in manifest["packages"]}) == 9
    assert all(p["type"] == "git" and re.fullmatch(r"[0-9a-f]{40}", p["rev"])
               for p in manifest["packages"])
    mathlib = next(p for p in manifest["packages"] if p["name"] == "mathlib")
    assert mathlib["rev"] == config["require"][0]["rev"]
    toolchain = (ROOT / "lean-toolchain").read_bytes()
    assert toolchain == (ROOT / "inputs/provenance/source-lean-toolchain").read_bytes()
    assert toolchain == b"leanprover/lean4:v4.34.1\n"

    libraries = config["lean_lib"]
    library_names = [lib["name"] for lib in libraries]
    assert len(library_names) == len(set(library_names))
    assert set(library_names) == NEW_MODULES | {"C291Inputs"}
    assert config["defaultTargets"] == [
        "C291Inputs", "SourceLifetimeControls", "SourceLifetimeAxiomAudit"
    ], "default targets must include both controls and complete axiom audit"
    mapping = {}
    for lib in libraries:
        for module in lib.get("roots", [lib["name"]]):
            assert module not in mapping, "duplicate module: " + module
            path = Path(lib.get("srcDir", ".")) / (module.replace(".", "/") + ".lean")
            assert not path.is_absolute() and ".." not in path.parts
            assert (ROOT / path).is_file(), path.as_posix()
            mapping[module] = path.as_posix()
    assert set(mapping.values()) == {p.relative_to(ROOT).as_posix()
                                     for p in paths if p.is_file() and p.suffix == ".lean"}, \
        "module mapping does not match package Lean sources"
    assert set(mapping.values()) <= {record["path"] for record in identities}
    old_roots = [lib["name"] for lib in original_config["lean_lib"]]
    input_lib = next(lib for lib in libraries if lib["name"] == "C291Inputs")
    assert input_lib["srcDir"] == "inputs"
    assert input_lib["roots"] == old_roots + ["Lifetime"]
    assert len(old_roots) == 13 and len(mapping) == 19

    local_imports = {}
    external = set()
    for module, relative in mapping.items():
        imports = [name for line in (ROOT / relative).read_text().splitlines()
                   if line.startswith("import ")
                   for name in line[7:].split("--", 1)[0].split()]
        local_imports[module] = [name for name in imports if name in mapping]
        for name in imports:
            assert (name in mapping or name == "Mathlib" or name.startswith("Mathlib.")
                    or name == "Lean" or name.startswith("Lean.")), name
            if name not in mapping:
                external.add(name)
    pending = set(mapping)
    order = []
    while pending:
        available = sorted(m for m in pending if set(local_imports[m]) <= set(order))
        assert available, "local import cycle"
        order.extend(available)
        pending.difference_update(available)
    external_records = []
    if mathlib_source is not None:
        for name in sorted(external):
            if name == "Lean" or name.startswith("Lean."):
                continue
            relative = name.replace(".", "/") + ".lean"
            path = mathlib_source / relative
            assert path.is_file(), "missing pinned external source: " + relative
            external_records.append({"module": name, "path_in_mathlib": relative,
                                     "sha256": sha(path.read_bytes())})
    toolchain_records = []
    if lean_source is not None:
        for name in sorted(external):
            if name != "Lean" and not name.startswith("Lean."):
                continue
            relative = name.replace(".", "/") + ".lean"
            path = lean_source / relative
            assert path.is_file(), "missing pinned toolchain source: " + relative
            toolchain_records.append({"module": name, "path_in_toolchain_source": relative,
                                      "sha256": sha(path.read_bytes())})

    files = [p for p in paths if p.is_file()]
    for path in paths:
        relative = path.relative_to(ROOT)
        if path.is_file():
            data = path.read_bytes()
            assert not contains_private_path(data), relative.as_posix()
            data.decode("utf-8")
    receipts = json.loads((ROOT / "evidence/DEVELOPMENT_COMPILE_SUMMARY.json").read_text())
    empty_sha = sha(b"")
    assert len(receipts["receipts"]) == 5
    assert {r["source"] for r in receipts["receipts"]} == {m + ".lean" for m in NEW_MODULES}
    for receipt in receipts["receipts"]:
        assert sha((ROOT / receipt["source"]).read_bytes()) == receipt["source_sha256"]
        assert receipt["returncode"] == 0 and not receipt["timed_out"]
        assert receipt["source_unchanged"]
        for stream in ("stdout", "stderr"):
            if stream + "_artifact" in receipt:
                relative = Path(receipt[stream + "_artifact"])
                assert not relative.is_absolute() and ".." not in relative.parts
                assert sha((ROOT / relative).read_bytes()) == receipt[stream + "_sha256"]
            else:
                assert receipt[stream + "_sha256"] == empty_sha

    audit_receipt = next(r for r in receipts["receipts"] if r["source"] == "SourceLifetimeAxiomAudit.lean")
    audit_text = (ROOT / audit_receipt["stdout_artifact"]).read_text()
    modules = re.findall(r"^LIFETIME_AUDIT_MODULE (\S+) COUNT (\d+)$", audit_text, re.M)
    declarations = re.findall(r"^LIFETIME_AUDIT_DECL (\S+) AXIOMS \[([^\]]*)\]", audit_text, re.M)
    terminal = re.findall(r"^LIFETIME_AUDIT_STANDARD_ONLY_PASS COUNT (\d+)$", audit_text, re.M)
    expected_audited = set(mapping) - {"SourceLifetimeAxiomAudit"}
    assert len(modules) == 18 and {m for m, _ in modules} == expected_audited
    assert sum(int(count) for _, count in modules) == 409
    assert len(declarations) == 409 and len({name for name, _ in declarations}) == 409, \
        "expected 409 distinct recorded audit declarations"
    assert terminal == ["409"], "missing or inconsistent development audit pass marker"
    for name, axioms in declarations:
        assert {a.strip() for a in axioms.split(",") if a.strip()} <= {
            "propext", "Classical.choice", "Quot.sound"
        }, "forbidden axiom in recorded declaration: " + name

    return {
        "schema_version": 1,
        "status": "PASS_SOURCE_STATIC_ONLY" if allow_lake_build else "PASS_STATIC_ONLY",
        "validation_mode": "source_workspace" if allow_lake_build else "publication",
        "excluded_paths": [".lake"] if allow_lake_build else [],
        "cache_excluded_from_package_scan": allow_lake_build,
        "cache_validation": "NOT_PERFORMED",
        "scope": "File identities, generated TOML subset, module mappings, direct import resolution, acyclic local imports, unchanged dependency manifest entries, five development receipt bindings, and recorded 409-declaration audit output. Audit-output parsing does not rerun Lean axiom collection. " + (
            "The top-level .lake cache is excluded from the package inventory, module census and hygiene scan. Explicit optional external-source checks separately read the requested direct import files, which may be inside that cache; their hashes are reported below. This is not clean-publication hygiene or cache/dependency-object validation."
            if allow_lake_build else "Text-only public package hygiene; no cache directory is admitted."),
        "lake_loader": "NOT_RUN",
        "lean_compile": "NOT_RUN_BY_THIS_VALIDATION",
        "hosted_ci": "NOT_OBSERVED",
        "network_or_cache_mutation": "NONE",
        "generated_toml_parser": "Restricted JSON-compatible assignment and array-of-table subset; not the Lake TOML loader.",
        "identity_records_verified": len(identities),
        "identity_manifest_sha256": sha(identity_path.read_bytes()),
        "lakefile_sha256": sha((ROOT / "lakefile.toml").read_bytes()),
        "lake_manifest_sha256": sha((ROOT / "lake-manifest.json").read_bytes()),
        "toolchain_sha256": sha(toolchain),
        "module_count": len(mapping),
        "module_mapping": mapping,
        "local_imports": local_imports,
        "topological_module_order": order,
        "external_imports": sorted(external),
        "external_source_check": "DIRECT_MATHLIB_SOURCE_FILES_PRESENT" if mathlib_source is not None else "NOT_REQUESTED",
        "external_toolchain_imports": sorted(name for name in external if name == "Lean" or name.startswith("Lean.")),
        "external_source_files": external_records,
        "toolchain_source_check": "DIRECT_LEAN_SOURCE_FILES_PRESENT" if lean_source is not None else "NOT_REQUESTED",
        "toolchain_source_files": toolchain_records,
        "development_receipts_verified": len(receipts["receipts"]),
        "recorded_development_audit_modules": {m: int(n) for m, n in modules},
        "recorded_development_audit_declarations": len(declarations),
        "dependency_pins": {p["name"]: p["rev"] for p in manifest["packages"]},
        "file_count_at_validation": len(files),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mathlib-source", type=Path)
    parser.add_argument("--lean-source", type=Path)
    parser.add_argument("--allow-lake-build", action="store_true",
                        help="Inspect a built source workspace, excluding only its real top-level .lake directory; not an export-hygiene pass.")
    args = parser.parse_args()
    print(json.dumps(validate(args.mathlib_source, args.lean_source, args.allow_lake_build), indent=2))
