"""Deterministic synthetic policy fixtures. These are not a scientific corpus."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def sha(value):
    return hashlib.sha256(value).hexdigest()


def content_id(prefix, value):
    return prefix + ":" + sha(encoded(value))


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def ref(root, relative, value):
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(value, bytes):
        path.write_bytes(value)
    else:
        write_json(path, value)
    return {"path": relative, "sha256": sha(path.read_bytes())}


def build_fixture(root: Path):
    root.mkdir(parents=True, exist_ok=True)
    artifacts, records, family_split = {}, [], {}
    for index, split in enumerate(("train", "test")):
        task = "fixture.task." + str(index)
        stem = "artifacts/" + str(index)
        source_ref = ref(root, stem + "/source.txt", ("SYNTHETIC SOURCE " + str(index)).encode())
        proof_ref = ref(root, stem + "/proof.txt", ("SYNTHETIC PROOF RECEIPT FIXTURE " + str(index)).encode())
        target_ref = ref(root, stem + "/target.txt", ("SyntheticFixture.Target" + str(index)).encode())
        binding = {"task_id": task, "target": "SyntheticFixture.Target" + str(index),
                   "target_ref": target_ref, "source_ref": source_ref, "proof_ref": proof_ref,
                   "runtime_id": "synthetic-runtime-v1", "baseline_id": "synthetic-baseline-v1",
                   "kind": "fixture"}
        artifact_id = content_id("artifact", binding)
        families = {key: [key + ".fixture." + str(index)]
                    for key in ("theorem", "derivation", "source", "transport")}
        for key, values in families.items():
            for value in values:
                family_split[key + ":" + value] = split
        receipt = {"schema": "ul-corpus-root-acceptance-v1", "artifact_id": artifact_id,
                   "task_id": task, "target": binding["target"],
                   "source_sha256": source_ref["sha256"], "proof_sha256": proof_ref["sha256"],
                   "target_sha256": target_ref["sha256"], "runtime_id": binding["runtime_id"],
                   "baseline_id": binding["baseline_id"], "status": "accepted",
                   "root_closed": True, "kernel_checked": True, "checked_insertion": True,
                   "exact_target_match": True, "metavariable_count": 0, "free_variable_count": 0,
                   "axioms": ["propext"], "synthetic_fixture": True}
        receipt_ref = ref(root, stem + "/receipt.json", receipt)
        provenance = {"schema": "ul-corpus-provenance-v1", "artifact_id": artifact_id,
                      "origin_id": "synthetic.fixture." + str(index), "source_exposed": False,
                      "blocked_trace": False, "historical_trace_id": "",
                      "disclosure_complete": True,
                      "source_history": ["Synthetic data generated for verifier branch testing only."],
                      "synthetic_fixture": True}
        provenance_ref = ref(root, stem + "/provenance.json", provenance)
        attestation = {"schema": "ul-corpus-policy-attestation-v1", "artifact_id": artifact_id,
                       "review_id": "synthetic.review." + str(index), "reviewer": "fixture-reviewer",
                       "provenance_sha256": provenance_ref["sha256"], "source_exposed": False,
                       "self_theorem_local": False, "exposure_reviewed": True,
                       "proof_dependency_reviewed": True, "source_lineage_reviewed": True,
                       "review_outcome": "approved_for_fixture", "families": families,
                       "permitted_splits": [split], "synthetic_fixture": True}
        attestation_ref = ref(root, stem + "/attestation.json", attestation)
        artifacts[artifact_id] = dict(binding, acceptance_receipt_ref=receipt_ref,
                                      provenance_ref=provenance_ref, attestation_ref=attestation_ref)
        identity = {"artifact_id": artifact_id, "split": split, "families": families}
        records.append(dict(identity, id=content_id("record", identity)))
    policy = {"schema": "ul-corpus-trusted-policy-v1", "policy_id": "synthetic-policy-fixture-v1",
              "mode": "fixture_only", "reviewers": ["fixture-reviewer"],
              "artifacts": artifacts, "family_split": family_split}
    dataset = {"schema": "ul-corpus-proposal-v1", "dataset_id": "synthetic-fixture-only",
               "records": records, "claimed_eligible": True}
    write_json(root / "policy.json", policy)
    write_json(root / "dataset.json", dataset)
    return root / "dataset.json", root / "policy.json", sha((root / "policy.json").read_bytes())


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit("output must not exist")
    dataset, policy, pin = build_fixture(args.output)
    print(json.dumps({"dataset": str(dataset), "policy": str(policy), "policy_sha256": pin,
                      "synthetic_fixture": True, "scientific_corpus": False}, sort_keys=True))
