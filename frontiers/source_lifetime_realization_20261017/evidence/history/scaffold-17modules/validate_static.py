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


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git_blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


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


def validate(mathlib_source=None):
    identity_path = ROOT / "inputs/provenance/FILE_IDENTITIES.json"
    identities = json.loads(identity_path.read_text())["files"]
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
    assert set(config["defaultTargets"]) <= set(library_names)
    mapping = {}
    for lib in libraries:
        for module in lib.get("roots", [lib["name"]]):
            assert module not in mapping, "duplicate module: " + module
            path = Path(lib.get("srcDir", ".")) / (module.replace(".", "/") + ".lean")
            assert not path.is_absolute() and ".." not in path.parts
            assert (ROOT / path).is_file(), path.as_posix()
            mapping[module] = path.as_posix()
    assert set(mapping.values()) == {p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*.lean")}
    assert set(mapping.values()) <= {record["path"] for record in identities}
    old_roots = [lib["name"] for lib in original_config["lean_lib"]]
    input_lib = next(lib for lib in libraries if lib["name"] == "C291Inputs")
    assert input_lib["srcDir"] == "inputs"
    assert input_lib["roots"] == old_roots + ["Lifetime"]

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

    files = sorted(p for p in ROOT.rglob("*") if p.is_file())
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        assert not path.is_symlink(), relative.as_posix()
        assert ".lake" not in relative.parts and "__pycache__" not in relative.parts
        assert path.suffix not in {".olean", ".ilean", ".o", ".a", ".so", ".dylib", ".pyc"}
        if path.is_file():
            data = path.read_bytes()
            assert not re.search(rb"/(?:Users|home|root)/", data), relative.as_posix()
            data.decode("utf-8")
    receipts = json.loads((ROOT / "evidence/DEVELOPMENT_COMPILE_SUMMARY.json").read_text())
    empty_sha = sha(b"")
    for receipt in receipts["receipts"]:
        assert sha((ROOT / receipt["source"]).read_bytes()) == receipt["source_sha256"]
        assert receipt["returncode"] == 0 and not receipt["timed_out"]
        assert receipt["source_unchanged"]
        assert receipt["stdout_sha256"] == empty_sha and receipt["stderr_sha256"] == empty_sha

    return {
        "schema_version": 1,
        "status": "PASS_STATIC_ONLY",
        "scope": "File identities, generated TOML subset, module mappings, direct import resolution, acyclic local imports, unchanged dependency manifest entries, and text-only public package hygiene.",
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
        "dependency_pins": {p["name"]: p["rev"] for p in manifest["packages"]},
        "file_count_at_validation": len(files),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mathlib-source", type=Path)
    args = parser.parse_args()
    print(json.dumps(validate(args.mathlib_source), indent=2))
