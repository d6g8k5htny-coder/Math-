# CBZ-MATH-198 contribution

This is a self-contained source contribution to the 29 October 2026 Crystalline
Baseline mission. Federation integration is coordinated in
[d6g8k5htny-coder/main#684](https://github.com/d6g8k5htny-coder/main/issues/684).
It does not declare the federation at CBZ-0.

## Mathematical boundary

The frozen `Specifications/P15.lean` retains the original source SHA256
`a30d9e6938b64d4e2728c5380d41b3a627cde42448df254069293e3839a41ca6`.
The explicit audit covers 198 theorem bodies: 49 original P15 packet targets,
4 supporting completion results, 96 general results, and 49 exact native-task
wrappers. `audit_targets.json` and the endpoint maps identify each declaration.
`evidence/final02/results.json` records the prior fresh 29-module PASS. The new
baseline replay must be read separately; historical receipts never become a
new gate result by copying them.

General results include palette-separated local-to-global assembly, independent
block probability factorization, weighted Holder/Finner inequalities, the
Bernoulli/subset bridge, overlapping-witness price assembly and witness-load
bounds. The local-cover premise is explicitly relative to each block. A positive
two-block empty-local-cover example and a proof that the old ambient premise
fails are included to prevent vacuous localization.

`General/Threshold.lean` defines the historical Talagrand prize and modern
threshold conjectures and proves a conditional reduction from explicit uniform
palette-price certificates. Universal existence of those certificates and the
unrestricted conjectures remain QUARANTINED. Valid definitions and conditional
implications are CLOSED; they do not prove the existential conjectures. The
realized-family bounds preserve all original hypotheses, including demand at
least two. Demand-one exclusions are explicit theorems.

Only `propext`, `Classical.choice`, and `Quot.sound` are allowed in the
transitive axiom audit. Exact real/rational Lean proofs certify all mathematical
bounds. Timings and memory measurements have no mathematical certification role.

## Engineering boundary

`integration/engine_audit` contains the versioned 49-endpoint evidence catalog
and bounded search transport. It separates proof acceptance from cleanup and
reserves requests for verification, state release and shutdown.
`integration/native_worker` supplies fixed typed proof-reuse actions, exports
structural certificates and rechecks them in a fresh kernel worker. This is
source-exposed proof reuse. It establishes neither autonomous discovery nor a
learning or performance improvement.

`integration/corpus_admission` tests strict provenance, contamination and split
admission policy. Its positive examples are fixtures. No representative eligible
training corpus, trained RL policy, or orders-of-magnitude improvement is claimed.

Failed/interrupted prior campaigns and their cost receipts are retained as
inactive forensic evidence. Legacy root `run_lean.py`, `verify_saved.py`, and
`seal.py` are not supported baseline commands. Consult the federation's
QUARANTINE.json for their exact dispositions.

## Replay

The federation contribution includes `tools/contribution_gate.py`, a tested
local campaign driver. Its documented command accepts explicit source, pinned
Lean/Mathlib, new build directory and new evidence directory. It runs auditor
self-tests, the exact formal source inventory, normal/optimized regressions,
fresh source/kernel/axiom verification, native compilation and fresh-worker
rechecks. It always reports `cbz_zero: false`; federation hygiene and all other
repositories require their own final gates.

Without that driver, the proof chain can be rebuilt directly:

```sh
python -B rebuild.py --lean /ABS/LEAN_4_34_1/bin/lean \
  --mathlib-root /ABS/MATHLIB_D13F23B7 \
  --build-dir /ABS/NEW_FORMAL_CACHE --output /ABS/NEW_FORMAL_EVIDENCE
```

Lean executable SHA256:
`e8baaa71855a616dc351028f3ad2200051b0671f423a1696a100e809302d5550`.
Mathlib commit: `d13f23b723b8a846827a245b89c10fc7d3f11612`.
Its eight pinned package dependencies and precompiled cache are external trusted
runtime inputs. The executable hash alone does not bind shared libraries or
prove the full Mathlib source tree; the trust boundary is explicit in receipts.
Serialize heavy Lean processes on this 16 GiB host.

All current and historical scientific acceptance, eligibility, novelty and
performance boundaries remain explicit. No approval from a human or model-family
quorum is required by this contribution's operational governance.
