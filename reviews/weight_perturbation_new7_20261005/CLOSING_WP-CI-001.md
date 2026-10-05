# Closing readback — WP-CI-001 execution on `8739dbe`

Scientific effect: **NONE**. Organizational-independence credit: **0**.
This note closes the runtime side of WP-CI-001. It does not replace the
statement read or the historical AMEND, and it does not accept the 47-target
package. #281 stays WITHHELD. `alignment_status` stays
`PENDING_INDEPENDENT_REVIEW`. No integration reservation.

Dylan Roy — delegated AI review.
Actual performer: xAI Grok 4.7, Cursor cloud agent, model `grok-4.7-high-fast`,
session `bc-b8309e55-05c6-40e7-bc27-a1223d285487`.
Runtime: Cursor-managed public VM. No local `lake` / `lean` / `leanchecker`
replay. The evidence below is the hosted run and its original artifact.

History left unchanged: `reviews/weight_perturbation_new7_20261005/REVIEW.md`
at commit `03ceeee2e9f3aeec7188eceb80975a304ee73096`,
SHA256 `e082a8b7d46237c7bde63e9f0f21f4fd8f78e46b0e158d584fcce642a36475cd`,
git blob `fc58e93c61dd394f16fc02608c255c7b0f756b80`.
That file records **AMEND WP-CI-001** on `559e1223658f9b7cc20154824e3d13e6348b9b2f`
and the source readback of `8739dbe20ecc7321cfc640738405c2c995edca94`.

## Disposition

**Scoped new-seven execution PASS** on corrected head
`8739dbe20ecc7321cfc640738405c2c995edca94`.

WP-CI-001's unknown identifier `abs_add` is absent from this run. The fresh
build of `ResearchFormalCoreR1.WeightPerturbation` completed, `leanchecker`
returned exit 0, and all 47 axiom and type reports were extracted. This PASS
covers the corrected seven-target module's hosted kernel execution together
with the unchanged gate's package run. It is not a full-47 alignment acceptance.

## Run identity

[Run 37360921503](https://github.com/d6g8k5htny-coder/Math-/actions/runs/37360921503),
attempt 1, event `pull_request`, conclusion **success** on head
`8739dbe20ecc7321cfc640738405c2c995edca94`.

| Job | id | conclusion |
|---|---|---|
| `downstream-replay` | 111935011339 | success |
| `formal / formal-evidence` | 111935011660 | success |
| `math-downstream-gates` | 111936563229 | success |

Tested commit in the receipt and in the aggregate output:
`90edceb281fb9eaa01dfe9e233d51ece0671e8b8`.
Parents: `dcd2a886e322738324a745adcad12fd3735bd2c5` and
`8739dbe20ecc7321cfc640738405c2c995edca94`.
Tree: `e6923fa5baf798617631343c7a8a00b59404ba63`, the same tree as `8739dbe`.
The aggregate log checks that commit out as
`Merge 8739dbe20ecc7321cfc640738405c2c995edca94 into dcd2a886e322738324a745adcad12fd3735bd2c5`.

## Artifact recomputed here

Artifact `formal-evidence-37360921503-1`, id `11366797243`, 13213 bytes.

| Object | SHA256 |
|---|---|
| ZIP | `6e65e1d423029614de005ca52bd3771f78170cbbb8ed339459fd3cac50bad23c` |
| `receipt.json` | `facf45479aff1318ea01b5195cafb9df7b1aec8e595872b5a3f5f9c0db1b66bf` |

`required-check-binding.json` carries the same receipt digest, repository
`d6g8k5htny-coder/Math-`, run `37360921503`, attempt `1`, and checked commit
`90edceb281fb9eaa01dfe9e233d51ece0671e8b8`.

All 10 receipt log digests match the ZIP members. Manifest digest in the
receipt is `db678e22bc6cee792a3918fd501b94b6253d4bac276909ea5663cd8c4710d14b`.
Lean version string is 4.34.1, commit `5045d0056413266e57c625dcd7c365b10e377c52`.
Mathlib revision is `d13f23b723b8a846827a245b89c10fc7d3f11612`. Nine dependency
revisions are recorded. `scientific_effect` is `NONE`.

## What the formal job log shows

Step "Gate tests and exact source identity": `Ran 125 tests` / `OK`, then
`Ran 125 tests` / `OK`, then

`SOURCE_IDENTITY_PASS (not a Lean build or scientific acceptance): db678e22bc6cee792a3918fd501b94b6253d4bac276909ea5663cd8c4710d14b`.

`leanprover/lean-action` is invoked with `leanchecker: false`, and its own
leanchecker, nanoda, and axiom-audit actions end `skipped`. The executing
command is the later `python3 formal/gate.py --execute`, which prints:

- `build: exit 0`
- `leanchecker: exit 0`
- `axioms: exit 0`
- `elaborated-types: exit 0`
- `false_fold: exit 1`
- `false_power: exit 1`
- `sorry: exit 0`
- `custom_imported: exit 0`
- `native: exit 0`
- `version: exit 0`

`leanchecker.log` is empty. Its digest is the empty-file SHA256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`,
paired with `leanchecker: exit 0` from that gate command.

`build.log` records `Built ResearchFormalCoreR1.WeightPerturbation` and
`Build completed successfully (8932 jobs)`. One nonblocking linter hint remains
at `WeightPerturbation.lean:73` (`unnecessarySeqFocus` on `<;>`). It did not
fail the build. No new source repair is requested for it.

The receipt lists 47 axiom reports. Every report is exactly
`Classical.choice`, `Quot.sound`, and `propext`. The seven
`weightPerturbation_*` / `weightedLaw_event_perturbation*` names are present
in both `axioms.log` and `elaborated-types.log`.

Negative controls in the receipt and in the logs:

| Control | Receipt | Log |
|---|---|---|
| `false_fold` | `REJECTED_BY_LEAN` | `unsolved goals` / `⊢ False` |
| `false_power` | `REJECTED_BY_LEAN` | `unsolved goals` / `⊢ False` |
| `sorry` | `REJECTED_BY_AXIOM_GATE` | `'injected' depends on axioms: [sorryAx]` |
| `custom_imported` | `REJECTED_BY_AXIOM_GATE` | `'injected' depends on axioms: [hiddenPremise]` |
| `native` | `REJECTED_BY_AXIOM_GATE` | native_decide axiom |

`math-downstream-gates` prints `conclusion: success` for run `37360921503`,
attempt `1`, receipt `facf45479aff1318ea01b5195cafb9df7b1aec8e595872b5a3f5f9c0db1b66bf`,
checked commit `90edceb281fb9eaa01dfe9e233d51ece0671e8b8`, with the aggregate's
own meaning line: required engineering checks and current-run formal evidence
only.

Initial run `37360023323` stays a failed build. Its preserved log is not
relabeled.

The earlier failed head `559e122` remains the AMEND record. This closing PASS
binds only the corrected head `8739dbe` and the tree-identical tested merge
`90edceb`.
