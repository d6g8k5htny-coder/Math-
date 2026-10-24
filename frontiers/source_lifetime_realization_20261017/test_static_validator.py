"""Read-only mutation controls for package validation; never invokes Lean or Lake."""

import json
import os
from pathlib import Path
import re
import subprocess
import sys
from unittest.mock import patch

import validate_static as checker


if not __debug__:
    raise RuntimeError("Static-validator controls require assertions; disable Python optimization.")


ROOT = Path(__file__).resolve().parent
AUDIT_OUTPUT = "evidence/SourceLifetimeAxiomAudit.development.stdout.txt"
SUMMARY = "evidence/DEVELOPMENT_COMPILE_SUMMARY.json"


def inventory():
    return {p.relative_to(ROOT).as_posix(): checker.sha(p.read_bytes())
            for p in ROOT.rglob("*") if p.is_file()}


def reject(label, overrides):
    read_bytes = Path.read_bytes
    read_text = Path.read_text

    def relative(path):
        try:
            return path.relative_to(ROOT).as_posix()
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
            checker.validate()
        except AssertionError as error:
            return {"case": label, "expected_rejection_observed": True,
                    "diagnostic": str(error)}
    raise RuntimeError("Validator accepted a required negative control: " + label)


def audit_overrides(text):
    data = text.encode("utf-8")
    summary = json.loads((ROOT / SUMMARY).read_text())
    receipt = next(r for r in summary["receipts"] if r["source"] == "SourceLifetimeAxiomAudit.lean")
    # Rebind the digest deliberately: these controls must reach the semantic
    # output-consistency checks rather than stop at the artifact hash check.
    receipt["stdout_sha256"] = checker.sha(data)
    return {AUDIT_OUTPUT: data, SUMMARY: (json.dumps(summary, indent=2) + "\n").encode()}


def main():
    before = inventory()
    baseline = checker.validate()
    results = []
    proof = "SourceThetaBridge.lean"
    results.append(reject("modified_proof_source", {proof: (ROOT / proof).read_bytes() + b"\n"}))

    manifest = json.loads((ROOT / "lake-manifest.json").read_text())
    manifest["packages"][0]["rev"] = "0" * 40
    results.append(reject("changed_dependency_pin", {
        "lake-manifest.json": (json.dumps(manifest, indent=2) + "\n").encode()
    }))

    config = (ROOT / "lakefile.toml").read_text()
    changed = config.replace(
        'defaultTargets = ["C291Inputs", "SourceLifetimeControls", "SourceLifetimeAxiomAudit"]',
        'defaultTargets = ["C291Inputs", "SourceLifetimeControls"]')
    assert changed != config
    results.append(reject("omitted_default_axiom_audit_target", {"lakefile.toml": changed.encode()}))
    results.append(reject("wrong_input_source_directory", {
        "lakefile.toml": config.replace('srcDir = "inputs"', 'srcDir = "."').encode()
    }))

    identity_path = "inputs/provenance/FILE_IDENTITIES.json"
    identities = json.loads((ROOT / identity_path).read_text())
    identities["files"] = [r for r in identities["files"] if r["path"] != "SourceLifetimeAxiomAudit.lean"]
    results.append(reject("omitted_audit_source_identity", {
        identity_path: (json.dumps(identities, indent=2) + "\n").encode()
    }))

    output = (ROOT / AUDIT_OUTPUT).read_text()
    missing = re.sub(r"^LIFETIME_AUDIT_DECL \S+ AXIOMS \[[^\]]*\]\n", "", output, count=1, flags=re.M)
    assert missing != output
    results.append(reject("omitted_audit_declaration_with_rebound_digest", audit_overrides(missing)))
    forbidden = output.replace("AXIOMS [propext", "AXIOMS [sorryAx", 1)
    assert forbidden != output
    results.append(reject("forbidden_axiom_with_rebound_digest", audit_overrides(forbidden)))

    readme = (ROOT / "README.md").read_bytes()
    results.append(reject("private_root_path", {
        "README.md": readme + b"\n/" + b"root/private-evidence.txt\n"}))
    results.append(reject("agent_prefix_is_not_a_path_allowlist", {
        "README.md": readme + b"\n/" + b"root/c291_nonauthor_review/private.txt\n"}))
    assert not checker.contains_private_path(b"OpenAI Codex `/" + b"root/c291_nonauthor_review`.")

    guards = []
    for label, options, environment in [
        ("explicit_python_optimization", ["-O", "-B"], dict(os.environ)),
        ("environment_python_optimization", ["-B"], dict(os.environ, PYTHONOPTIMIZE="1")),
    ]:
        run = subprocess.run([sys.executable] + options + ["validate_static.py"],
                             cwd=ROOT, env=environment, capture_output=True)
        assert run.returncode != 0
        assert b"Static validation requires assertions; disable Python optimization." in run.stderr
        guards.append({"case": label, "returncode": run.returncode,
                       "expected_rejection_observed": True,
                       "stdout_sha256": checker.sha(run.stdout),
                       "stderr_sha256": checker.sha(run.stderr)})
    assert inventory() == before, "package bytes changed during read-only controls"
    return {
        "schema_version": 1,
        "status": "PASS_STATIC_CONTROLS_ONLY",
        "scope": "Nine virtual file-content mutations, exact agent-token acceptance, and two optimized-Python rejection controls. No source file was mutated, and no Lean/Lake process, cache mutation, or network operation occurred.",
        "baseline_status": baseline["status"],
        "validator_sha256": checker.sha((ROOT / "validate_static.py").read_bytes()),
        "controls_sha256": checker.sha((ROOT / "test_static_validator.py").read_bytes()),
        "identity_manifest_sha256": baseline["identity_manifest_sha256"],
        "package_bytes_unchanged": True,
        "mutation_controls": results,
        "optimization_guards": guards,
    }


if __name__ == "__main__":
    print(json.dumps(main(), indent=2))
