# CBZ-MATH-198-20261029

A scoped proof and verification contribution for
[main#684](https://github.com/d6g8k5htny-coder/main/issues/684).
This directory never declares federation CBZ-0. The federation's canonical
integration writer owns shared status, cross-repository pin refresh and cleanup.

`project/README.md` describes the mathematical and engineering boundary.
`project/audit_targets.json` lists 198 explicit theorem checks. The historical
fresh result is preserved in `project/evidence/final02/results.json`. New replay
results are separate source-bound evidence, never inferred from that receipt.
The all-owned audit additionally checks every module-table occurrence, including
private/generated declarations; duplicated equation-theorem occurrences must be
checked individually.

Seven public relevant quarantine records are an exact projection of the private
canonical contribution index, identified by `QUARANTINE_PROJECTION.json`.
Unrestricted Talagrand/modern threshold existence, the uniform certificate premise,
a representative eligible RL corpus and any learned/performance advantage remain
unproved or unestablished. Definitions and conditional reductions are distinguished
from existential proofs. All 49 native endpoint actions are source-exposed proof
reuse and remain training-ineligible.

## Reproduce from a clone

Use Linux x86_64, Python3.12+, Git, `/proc`, supported `prctl` process controls,
and at least16GiB RAM. Serialize heavy Lean execution. Install Lean4.34.1 and
Mathlib at commit `d13f23b723b8a846827a245b89c10fc7d3f11612` with its eight
lake-manifest-pinned dependencies and the official precompiled cache.
`RUNTIME.md` gives the standalone provisioning commands and dependency pins.
The compiler binary must hash to
`e8baaa71855a616dc351028f3ad2200051b0671f423a1696a100e809302d5550`.
External compiler/shared libraries and dependency caches remain explicit trust
inputs; no independent compiler or complete Mathlib source rebuild is claimed.

From this directory, with fresh external output destinations:

```sh
python -B tools/contribution_gate.py --source "$PWD/project" \
  --lean /ABS/LEAN_4_34_1/bin/lean --mathlib-root /ABS/MATHLIB_D13F23B7 \
  --build-dir /ABS/NEW_BUILD --output /ABS/NEW_EVIDENCE
```

The driver checks its documented local scope and always emits `cbz_zero:false`.
A success is `LOCAL_CONTRIBUTION_PASS`. It runs normal/optimized adverse tests,
complete formal-source inventory, fresh proof compilation, all-owned kernel/axiom
checks, native build, fresh-worker certificates and saved-wire bindings. Linux
process supervision records and cleans the owned process subtree. Any failed
child, source-file-set/hash drift, omitted audit coverage or incomplete cleanup
prevents success. Every attempted campaign keeps its terminal receipt and streams.

Existing main/Math formal packages and federation inventory/snapshot/infrastructure
gates have separate recorded evidence; this command does not substitute for them.
It also does not certify live branch/PR hygiene or a tagged federation cold start.

`SOURCE_COPY.json` records the initial source-copy cut and subsequent changes.
Its initial file map is historical provenance, not the final payload manifest.
Private repository metadata, private Git bundles, operational build caches,
unsupported old executable entrypoints and third-party PDF payloads are excluded
from this public contribution. Original bytes remain preserved privately.
