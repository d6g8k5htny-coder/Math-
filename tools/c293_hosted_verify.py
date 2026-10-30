#!/usr/bin/env python3
"""C293-only hosted Lean replay. Engineering evidence, not scientific acceptance.

The source and historical execution receipts in PR #482 are immutable inputs.
Run in the pinned formal/ Lake environment (see the dedicated Actions workflow).
"""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "frontiers/morse_finite_critical_20261018"
FINAL = PACKAGE / "final-project"
NEGATIVE = PACKAGE / "negative-project/WithoutMorse.lean"
FORMAL = ROOT / "formal"
EVIDENCE = ROOT / ".lake/c293-hosted-evidence"
BUILD = ROOT / ".lake/c293-hosted-build"

SOURCE_COMMIT = "0ea97aff489f9420632b4cee81ad82dbec5fe88e"
MATHLIB_PIN = "d13f23b723b8a846827a245b89c10fc7d3f11612"
LEAN_VERSION = "4.34.1"
# These are SHA-256 hashes of the *published UTF-8 file bytes*, not Git blob IDs.
SOURCES = {
    "Lifetime": ("90f4892608e953ecc696bb32ea159d1c178ceb8a1c6edfd11acfceb14af462c6", 51383),
    "TorusTopology": ("ddb145b3f791c181d4f2a51e54e711937297bd6476ba55bcd5252b7ddb57cfe1", 12257),
    "MorseFiniteCritical": ("95a660134eda49eecfe6181884bd23b4e4ca210e228d2463de29e5f821df047b", 9445),
    "MorseFiniteControls": ("e6171c949ec60a3aea21a8cc028180e16c82e4946a232107d9e82bf8018cdac1", 2843),
    "MorseFiniteAxiomAudit": ("326a1cab271bf46a1c7db750ee1565e08dc4856c62e0abce3f5c9f90d923ce9d", 3025),
}
NEGATIVE_SHA = "4c9726b692dbb83237b82344e7b5aab621749da6da699c0187cf9893dca8d80f"
UPSTREAM = {
    "Lifetime": "specifications/lean_statements_20261010/Specifications/Lifetime.lean",
    "TorusTopology": "companions/torus_filtration_20261011/TorusTopology.lean",
}
# Published C293 objects, independently reproduced on a separate Linux machine.
OBJECTS = {
    "Lifetime": "b3e14c2951b452222ca0c7b1448458cf785225971da704e4e3e6f0cc93107da4",
    "TorusTopology": "ccb13e9469d55da8b5202706a1f013fa7a2755b2184542b8a0534f722d993125",
    "MorseFiniteCritical": "34ff2a9ed529609dd48a22204b8eacc66eeb943805e2d6e8dee4481cde8ef4e2",
    "MorseFiniteControls": "5eebfbb98a8cb05ac420d260dd08461ac037b2e086620fe79ee330defd345efa",
    "MorseFiniteAxiomAudit": "3c3f30110ec4a3c0a0c1ba6f1769634d0c04bfc4e444ab1bcfd46c5dffa4ff4b",
}
PACKAGE_PINS = {
    "plausible": "118aa17ee84656b8bd727fef7c458ee8c833385c",
    "LeanSearchClient": "ddf04cf3949fa556442341e87d47f9f6e6074707",
    "importGraph": "e928b72544873815af278d38681b31c0293588e3",
    "proofwidgets": "106ff4fafc74ef4ac99d81dbf3ab399118f497a5",
    "aesop": "355695d523e41d0554926416cba2a2b3544fbbc9",
    "Qq": "6a489d9af5d0c47e5b259e2e8bcdfc1811b5a259",
    "batteries": "f2effa3d803fda822b1f97b806c47cf2adfbcbc2",
    "Cli": "e92c9f15fdfacc8536f31cfb3b7ad26c3c8cd204",
    "mathlib": MATHLIB_PIN,
}
MODULE_COUNTS = {"Lifetime": 103, "TorusTopology": 38,
                 "MorseFiniteCritical": 20, "MorseFiniteControls": 8}


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def safe_source(path, root=ROOT):
    """Require a regular, in-tree file without symlinked ancestors."""
    path = Path(path)
    root = Path(root)
    if not path.is_relative_to(root):
        raise RuntimeError(f"source outside repository: {path}")
    parts = path.relative_to(root).parts
    for i in range(1, len(parts) + 1):
        if (root.joinpath(*parts[:i])).is_symlink():
            raise RuntimeError(f"symlink in source: {path}")
    if not path.is_file():
        raise RuntimeError(f"source missing or not regular: {path}")


def verify_sources(root=ROOT):
    """Check C293 source identities AND the actual upstream source crosswalk."""
    root = Path(root)
    prefix = root / "frontiers/morse_finite_critical_20261018"
    for module, (digest, size) in SOURCES.items():
        path = prefix / "final-project" / f"{module}.lean"
        safe_source(path, root)
        if path.stat().st_size != size or sha256(path) != digest:
            raise RuntimeError(f"C293 source identity mismatch: {module}")
        if module in UPSTREAM:
            other = root / UPSTREAM[module]
            safe_source(other, root)
            if other.read_bytes() != path.read_bytes():
                raise RuntimeError(f"upstream C293 input differs: {module}")
    neg = prefix / "negative-project/WithoutMorse.lean"
    safe_source(neg, root)
    if sha256(neg) != NEGATIVE_SHA:
        raise RuntimeError("C293 missing-premise control modified")
    toolchain = root / "formal/lean-toolchain"
    lakefile = root / "formal/lakefile.toml"
    manifest_file = root / "formal/lake-manifest.json"
    for path in (toolchain, lakefile, manifest_file):
        safe_source(path, root)
    if toolchain.read_text().strip() != "leanprover/lean4:v" + LEAN_VERSION:
        raise RuntimeError("Lean toolchain pin changed")
    if f'rev = "{MATHLIB_PIN}"' not in lakefile.read_text():
        raise RuntimeError("Lake mathlib pin changed")
    lock = json.loads(manifest_file.read_text())
    actual = {p["name"]: p["rev"] for p in lock["packages"]}
    if actual != PACKAGE_PINS:
        raise RuntimeError("C293 dependency pins differ from registered formal Lake lock")
    return {"source_commit": SOURCE_COMMIT, "module_sha256":
            {name: digest for name, (digest, _) in SOURCES.items()},
            "negative_sha256": NEGATIVE_SHA, "dependency_pins": actual}


def validate_audit(output):
    for module, count in MODULE_COUNTS.items():
        if f"MORSE_AUDIT_MODULE {module} COUNT {count}" not in output:
            raise RuntimeError(f"C293 audit missing {module} census")
    if "MORSE_AUDIT_STANDARD_ONLY_PASS COUNT 169" not in output:
        raise RuntimeError("C293 complete standard-only audit did not finish")
    declarations = re.findall(r"(?m)^MORSE_AUDIT_DECL ", output)
    if len(declarations) != 169:
        raise RuntimeError(f"C293 expected 169 declaration reports, got {len(declarations)}")
    if "quotientCriticalSet_finite' depends on axioms:" not in output:
        raise RuntimeError("C293 main theorem axiom report absent")


def validate_negative(returncode, output):
    """Reject a fake pass, import failure or unrelated syntax/error diagnostic."""
    required = ("error: Type mismatch", "quotientCriticalSet_finite d L hL g hs hp",
                "IsMorseDistinct d L g", "but is expected to have type")
    if returncode != 1 or output.count("error:") != 1 or not all(x in output for x in required):
        raise RuntimeError("C293 negative control did not reject the missing Morse premise")
    if any(s in output for s in ("unknown identifier", "unknown module",
                                  "file not found", "lean::memory_exception",
                                  "out of memory", "unexpected token")):
        raise RuntimeError("C293 negative control failed for an unrelated reason")


def git(*args, cwd=ROOT):
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def verify_packages():
    packages = FORMAL / ".lake/packages"
    out = {}
    for name, commit in PACKAGE_PINS.items():
        path = packages / name
        if not path.is_dir():
            raise RuntimeError(f"missing pinned dependency checkout: {name}")
        actual = git("-C", str(path), "rev-parse", "HEAD")
        if actual != commit:
            raise RuntimeError(f"wrong installed dependency commit: {name} {actual}")
        if git("-C", str(path), "status", "--porcelain", "--untracked-files=no"):
            raise RuntimeError(f"dirty installed dependency checkout: {name}")
        out[name] = actual
    return out


def verify_context():
    required = ("GITHUB_SHA", "GITHUB_RUN_ID", "GITHUB_RUN_ATTEMPT", "GITHUB_REPOSITORY")
    if any(not os.environ.get(x) for x in required):
        raise RuntimeError("hosted execution needs actual GitHub run identity")
    if os.environ["GITHUB_REPOSITORY"] != "d6g8k5htny-coder/Math-":
        raise RuntimeError("wrong execution repository")
    head = git("rev-parse", "HEAD")
    if head != os.environ["GITHUB_SHA"]:
        raise RuntimeError(f"tested checkout mismatch {head} != GITHUB_SHA")
    return {k.lower(): os.environ[k] for k in required}


def run_phase(name, args, cwd, env, expected_success=True, timeout=900):
    started = time.monotonic()
    try:
        result = subprocess.run(args, cwd=cwd, env=env, text=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                timeout=timeout, check=False)
        code, stdout, stderr = result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired as exc:
        code = "TIMEOUT"
        stdout = (exc.stdout or b"").decode("utf8", "replace") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        stderr = (exc.stderr or b"").decode("utf8", "replace") if isinstance(exc.stderr, bytes) else (exc.stderr or "")
    (EVIDENCE / f"{name}.stdout").write_text(stdout)
    (EVIDENCE / f"{name}.stderr").write_text(stderr)
    record = {"name": name, "command": args, "exit_code": code,
              "duration_seconds": round(time.monotonic() - started, 2),
              "stdout_sha256": sha256(EVIDENCE / f"{name}.stdout"),
              "stderr_sha256": sha256(EVIDENCE / f"{name}.stderr")}
    print(f"C293 {name}: exit={code} seconds={record['duration_seconds']}", flush=True)
    if (expected_success and code != 0) or (not expected_success and code == 0) or code == "TIMEOUT":
        print((stdout + stderr)[-4000:], flush=True)
        raise RuntimeError(f"C293 {name} unexpected exit: {code}")
    return record, stdout + stderr, code


def execute():
    context = verify_context()
    identity = verify_sources()
    EVIDENCE.mkdir(parents=True, exist_ok=False)
    BUILD.mkdir(parents=True, exist_ok=False)
    report = {"status": "HOLD_NOT_COMPLETED", "scientific_effect": "NONE",
              "scope": "C293 finite critical classes only", "context": context,
              "source_identity": identity, "memory_limit": "-M14000",
              "memory_limit_reason": "Six commands required -M14000 on provider-distinct Linux replay; original -M4096 receipts preserved.",
              "phase_results": []}
    def save():
        (EVIDENCE / "RESULT.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    save()
    try:
        packages_before = verify_packages()
        version = subprocess.check_output(["lean", "--version"], cwd=FORMAL, text=True).strip()
        (EVIDENCE / "toolchain.txt").write_text(version + "\n")
        if "version " + LEAN_VERSION not in version:
            raise RuntimeError(f"wrong Lean runtime: {version}")
        report["packages_before"] = packages_before
        env = dict(os.environ)
        env["LEAN_PATH"] = str(BUILD) + os.pathsep + env.get("LEAN_PATH", "")
        env["LEAN_NUM_THREADS"] = "2"
        for name in SOURCES:
            args = ["lean", "-j2", "-M14000"]
            if name.startswith("Morse"):
                args.append("-DwarningAsError=true")
            args += ["-o", str(BUILD / f"{name}.olean"), str(FINAL / f"{name}.lean")]
            rec, stdout, _ = run_phase("build-" + name, args, FINAL, env)
            report["phase_results"].append(rec)
            if name == "MorseFiniteAxiomAudit":
                validate_audit(stdout)
            digest = sha256(BUILD / f"{name}.olean")
            if digest != OBJECTS[name]:
                raise RuntimeError(f"C293 object digest mismatch: {name}: {digest}")
            rec["object_sha256"] = digest
            verify_sources()
            save()
        for name in ("MorseFiniteCritical", "MorseFiniteControls", "MorseFiniteAxiomAudit"):
            args = ["leanchecker", "-v", name]
            rec, _, _ = run_phase("kernel-" + name, args, FINAL, env)
            report["phase_results"].append(rec)
            save()
        args = ["lean", "-j2", "-M14000", str(NEGATIVE)]
        rec, stdout, code = run_phase("negative-WithoutMorse", args, NEGATIVE.parent, env, expected_success=False)
        validate_negative(code, stdout)
        report["phase_results"].append(rec)
        report["packages_after"] = verify_packages()
        report["source_identity_after"] = verify_sources()
        report["status"] = "PASS_HOSTED_C293_EXACT_TARGETS"
        save()
        print("C293_HOSTED_FORMAL_PASS: five exact objects, 169 audited declarations, "
              "three kernel replays and expected missing-premise rejection. "
              "No C292 or elder-rule scientific promotion.", flush=True)
    finally:
        save()


if __name__ == "__main__":
    if sys.argv[1:] == ["source"]:
        print(json.dumps(verify_sources(), sort_keys=True))
    elif sys.argv[1:] == ["execute"]:
        execute()
    else:
        raise SystemExit("usage: c293_hosted_verify.py source|execute")
