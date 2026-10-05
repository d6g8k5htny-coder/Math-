# Review — same-law weight perturbation, seven new targets

Scientific effect: **NONE**. Organizational-independence credit: **0**.
This is a statement-and-engineering read of the new seven declarations.
It does not accept the package, does not relabel the inherited #281 withheld
lineage, and does not manufacture a 47-target alignment record.

Dylan Roy — delegated AI review.
Actual performer: xAI Grok 4.7, Cursor cloud agent, model `grok-4.7-high-fast`,
session `bc-b8309e55-05c6-40e7-bc27-a1223d285487`
(https://cursor.com/agents/bc-b8309e55-05c6-40e7-bc27-a1223d285487).
Runtime: Cursor-managed cloud VM, public worker. No self-hosted worker was
connected. `lake`, `lean`, and `leanchecker` are absent on this VM, so no local
kernel replay was run or claimed.

Reviewed source:
`d6g8k5htny-coder/Math-` branch `chatgpt/lean-weight-perturbation-20261005`,
base `dcd2a886e322738324a745adcad12fd3735bd2c5`.
The read opened on head `559e1223658f9b7cc20154824e3d13e6348b9b2f`.
Before this record was pushed, the branch moved to successor
`8739dbe20ecc7321cfc640738405c2c995edca94`. The readback of that successor
is below. This review branch does not edit the source branch.
Source author: OpenAI / GPT-6 Astra Pro, session `lean-weight-perturbation-20261005`.

## Verdict

**AMEND**, finding **WP-CI-001** only.

The seven theorem types match `formal/WEIGHT_PERTURBATION.md` and the unchanged
`weightedLaw` construction. Hosted execution of this exact head failed before
`leanchecker`, the axiom audit, and the rejection controls. The failure is one
unknown identifier in the quotient proof script.

### WP-CI-001 — required repair

Hosted run `37360023323` at head `559e1223658f9b7cc20154824e3d13e6348b9b2f`
(https://github.com/d6g8k5htny-coder/Math-/actions/runs/37360023323):

- `downstream-replay`: success
- `formal / formal-evidence`: failure in **Build, recheck, audit axioms and execute negative controls**
- `math-downstream-gates`: failure, as required when formal evidence fails

Artifact `formal-evidence-37360023323-1` (id `11366965020`) contains `build.log`
with SHA256 `2abe4ec4bcfa4de282e7983ffebb225af21308c60b84083a1696bcced31b9c7c`.
That log's only error is:

```
error: ResearchFormalCoreR1/WeightPerturbation.lean:78:34: Unknown identifier `abs_add`
```

`ResearchFormalCoreR1.WeightedLaw` built in the same log. The new module did not.
There is no successful execution receipt on this run.

Pinned mathlib `d13f23b723b8a846827a245b89c10fc7d3f11612`,
`Mathlib/Algebra/Order/Group/Unbundled/Abs.lean`, declares

```lean
@[to_additive /-- The absolute value satisfies the triangle inequality. -/]
lemma mabs_mul_le (a b : α) : |a * b|ₘ ≤ |a|ₘ * |b|ₘ
```

The additive name is `abs_add_le`, with statement `|a + b| ≤ |a| + |b|`.
Line 78 uses that inequality:

```lean
div_le_div_of_nonneg_right (abs_add _ _) ht.le
```

Exact repair on the source branch, by the source author:

1. Replace `abs_add` with `abs_add_le` at that call.
2. Rebind `formal/manifest.json` key
   `ResearchFormalCoreR1/WeightPerturbation.lean` to the new file SHA256.

The seven declarations through `:= by` stay unchanged. Leave the target list,
hypotheses, factor, SCOPE mathematical claims, gate, lineage validator,
dependencies, and workflows unchanged.

Same-commit cleanup that is **not** a second finding: line 138 is
`field_simp [ne_of_gt hr, ne_of_gt hc] <;> ring`, and the same log warns that
`ring` is never executed. Deleting ` <;> ring` may ride with the repair.
Preserving `build.log` under `formal/evidence/` and binding its hash may also
ride with the repair. A later readback checks the byte diff.

This ID is the one already published in PR #292 comment 6001159217.
The log line and the pinned `mabs_mul_le` / `abs_add_le` declaration were
checked again here. No second identifier, and no parallel repair branch.

Current source disposition: `8739dbe` contains that repair. See the successor
readback. The open item on `8739dbe` is the hosted kernel run, which had not
finished when this file was written.

## Statement read of the new seven

Consumed construction `formal/ResearchFormalCoreR1/WeightedLaw.lean` is blob
`b51ca969a13b27b7e41a1401ea9e10e7dee39fb8` at `559e122`, at base `dcd2a88`, and
at `5b012335b279d1f93b930e7b906da09164332c47`. SHA256
`f31dfd2cd048cc0c0446c54c46d89c9cdd5d7bb9d76e9d8d16b7c034f351d736`.
`weightedLaw` is `(ENNReal.ofReal (∫ W))⁻¹ • μ.withDensity (ENNReal.ofReal ∘ W)`.
`ofReal` clips negatives, so the probability theorems carry `0 ≤ᵐ[μ]`.

| Target | Read |
|---|---|
| `weightPerturbation_integral` | Integrable `W`,`V` give `\|∫W − ∫V\| ≤ ∫\|W−V\|` via `integral_sub` and `abs_integral_le_integral_abs`. Signed weights stay allowed. Pinned `abs_integral_le_integral_abs` needs no extra integrability argument. |
| `weightPerturbation_setIntegral` | The same comparison on `μ.restrict A`, then `setIntegral_le_integral`. Pinned mathlib states that lemma for an arbitrary set from `Integrable` and `0 ≤ᵐ[μ]`, with no `MeasurableSet` argument. |
| `weightPerturbation_normalizer_lower` | `\|∫W − ∫V\| ≤ δ` and `c ≤ ∫V` give `∫W ≥ c − δ` from the lower half of `abs_le`. |
| `weightPerturbation_event_integral_bounds` | `0 ≤ᵐ[μ] W` gives `0 ≤ ∫_A W ≤ ∫ W` by `ae_restrict_of_ae` and `setIntegral_le_integral`. |
| `weightPerturbation_quotient_bound` | Identity `a/z − b/t = ((a−b) + (a/z)·(t−z))/t` holds for `z,t ≠ 0`. With `0 ≤ a/z ≤ 1` the numerator is at most `2δ`, so the quotient is at most `2δ/t`. The denominator kept in the statement is the reference `t`. No sign hypothesis on `b`. The factor is attained when `a = z`, `b = a − δ`, and `t = z + δ`. The note calls 2 convenient and does not claim optimality. |
| `weightedLaw_event_perturbation` | One measure `μ`. `∫\|W−V\| ≥ 0` and `≤ δ` produce `δ ≥ 0`. Then `∫W ≥ c − δ ≥ c/2 > 0`, so both `weightedLaw μ W` and `weightedLaw μ V` are probability measures. For every `MeasurableSet A`, `weightedLaw_event_real` rewrites both probabilities as integral ratios, the scalar lemma bounds them by `2δ/(∫V)`, and `∫V ≥ c > 0` weakens the denominator to `c`. |
| `weightedLaw_event_perturbation_r2` | `η ≤ c/2` and `r > 0` give `η r² ≤ (c r²)/2` with `sq_nonneg`, including `r > 1`. The parent theorem supplies the probability bound `2 (η r²) / (c r²)`, and `field_simp` cancels to `2η/c`. |

Attack notes, each checked on the frozen text:

- Ambient measure versus finite integral. The measure is an arbitrary `Measure Ω`. Finiteness enters as the `Integrable` hypotheses, which make the Bochner integrals the ones appearing in `weightedLaw`. There is no `[IsProbabilityMeasure μ]` and no finite-mass hypothesis.
- Almost-everywhere signs. Probability and event-ratio steps use `0 ≤ᵐ[μ]`. Values on null sets are outside those hypotheses. Theorems 1–3 do not require a sign.
- Reference versus perturbed normalizer. The scalar bound divides by `t = ∫ V`. The event theorem then uses `c ≤ ∫ V` to replace that denominator by `c`. It does not divide by the perturbed normalizer.
- Signed `b`. The scalar lemma's hypotheses are `0 < z`, `0 < t`, `0 ≤ a ≤ z`, `|a−b| ≤ δ`, and `|z−t| ≤ δ`. The probability application gets `a`'s bounds from the nonnegative weight `W`; `b` is controlled only through `|a−b|`.
- Every measurable `A`. The quantifier is `∀ A, MeasurableSet A → …`, and `hA` is passed to `weightedLaw_event_real`.
- `δ ≥ 0`. Derived in `weightedLaw_event_perturbation` as `0 ≤ ∫|W−V| ≤ δ`. The scaled theorem inherits it for `η r²` with `r² > 0`.
- `r²` cancellation for `r > 1`. Algebraic, using `r ≠ 0` and `c ≠ 0`. No `r ≤ 1` hypothesis is present. The sibling transfer `p02_lm009_probability_transfer_r8_to_r3` still has `r ≤ 1`; this module does not import that restriction.
- Different base measures. Both laws are `weightedLaw μ _`. The type has one `μ`. The note says a different-base application needs its own common-measure representation.
- Concrete L1 estimate and reference floor. `c`, `δ`, `η`, and the integral hypotheses are premises. No Gaussian, Palm, determinant, or numerical floor is proved.
- Factor 2. Documented as unoptimized. The scalar inequality is sharp for its own hypotheses; the module does not claim a smaller universal constant.

No `sorry`, axiom, or `native_decide` appears in the new module.

## Engineering inventory

Diff `dcd2a88...559e122` is exactly these eight paths:

- `formal/ResearchFormalCoreR1/WeightPerturbation.lean`
- `formal/WEIGHT_PERTURBATION.md`
- `formal/SCOPE.md`
- `formal/README.md`
- `formal/ResearchFormalCoreR1.lean` (one import)
- `formal/manifest.json`
- `formal/tests/test_weight_perturbation.py`
- `formal/tests/test_moment_generality.py` (`targets[36:40]` kept, length lower bound `≥ 40`)

SHA256 at `559e122`, matching the request pins and the manifest:

| Path | SHA256 |
|---|---|
| `WeightPerturbation.lean` | `27d9714eef848d180700fb0fb1d82da2388393ae5e6dfa5be603b0287cfccd13` |
| `manifest.json` | `02536325ff94f6fa1377b79667ad9753ef8f6c078e04196278238e6ef8b470a7` |
| `SCOPE.md` | `36e0714bcb79a158a6e50ff5b1e5e772939800ba023d865944901e4e7ae34838` |
| `WEIGHT_PERTURBATION.md` | `0ac969b86f5b2cc4e84b4bb61790c7497164b923dc5f3fc5be99195b75b1b212` |

Declaration order equals `manifest.targets`: 47 names, and the first 40 equal the base manifest. The new test locks `targets[40:]` and `len == 47`. `gate.py` `source_check` requires `names == targets` and is byte-identical to base (blob `f946c38aa38a`). `alignment_status` remains `PENDING_INDEPENDENT_REVIEW`. `scientific_effect` remains `NONE`. `LINEAGE_VALIDATION.md`, `test_alignment_lineage.py`, `lakefile.toml`, `lake-manifest.json`, `lean-toolchain`, and `.github/workflows/formal-lean.yml` match the base blobs. The six earlier Lean modules match the base blobs. README's execute sentence says 47 declarations, and the unchanged gate audits `m['targets']`.

`python3 -B -S formal/gate.py` on `559e122` printed
`SOURCE_IDENTITY_PASS (not a Lean build or scientific acceptance): 02536325ff94f6fa1377b79667ad9753ef8f6c078e04196278238e6ef8b470a7`.

## Finite controls actually run

These are stdlib fraction checks. They are not a Lean replay.

On `559e122`, Python 3.12.3:

```sh
python3 -B -S -m unittest formal.tests.test_weight_perturbation formal.tests.test_moment_generality -v
python3 -B -O -S -m unittest formal.tests.test_weight_perturbation formal.tests.test_moment_generality -v
```

Both runs: 28 tests, OK. The weight-perturbation file contributes 16, and both modes agree. The hosted gate step of run `37360023323` also logged those 16 as ok before the Lean build failed.

A separate fraction script, not the package test, checked the scalar identity, sharpness of factor 2, a negative `b`, the reference-denominator direction, a non-probability ambient mass with a null atom, `r = 7` cancellation, distinct base measures, signed-integral cancellation against `∫|W−V|`, the half-budget endpoint, and a vanishing-normalizer pair whose probability gap stays 1. That script printed `independent finite checks PASS`.

## Successor readback — `559e122..8739dbe`

Commit `8739dbe20ecc7321cfc640738405c2c995edca94`, message
`formal: repair pinned triangle-inequality lemma reference`, changes three paths:

- `WeightPerturbation.lean`: `abs_add` becomes `abs_add_le` at the quotient
  triangle step, and the unused ` <;> ring` after `field_simp` is deleted.
- `manifest.json`: the module digest becomes
  `50ce15709a133da12a0b4333cc653d26c5fd8a412976c975a7c2f3b25ed5c00f`,
  and the failure log is bound. Manifest SHA256
  `db678e22bc6cee792a3918fd501b94b6253d4bac276909ea5663cd8c4710d14b`.
- `formal/evidence/weight-perturbation-initial-build-failure.log`, SHA256
  `2abe4ec4bcfa4de282e7983ffebb225af21308c60b84083a1696bcced31b9c7c`.
  `cmp` against artifact `11366965020`'s `build.log` was equal.

`grep '^theorem'` is identical on the two heads. SCOPE, the extension note,
the test, the target list, the gate, and `WeightedLaw.lean` are outside the
diff. The statement read above therefore stands on `8739dbe`.

WP-CI-001 is closed as a source defect on `8739dbe`. That closure is the
byte readback. It is not kernel success.

Hosted run `37360921503` on `8739dbe` was **in progress** when this readback
was recorded
(https://github.com/d6g8k5htny-coder/Math-/actions/runs/37360921503).
`leanchecker`, the axiom audit, and the rejection controls are not claimed
for `8739dbe`.

## Reconciliation and limits

PR #292 comment 6001128958 (CoS) records that this cloud agent already holds the @cursor ask. Numbered Grok lanes were asked to stand by. Comment 6001159217 is a read-only diagnosis of the same compiler line. Comment 6001157499 is the author describing this repair before publication. This verdict does not edit `chatgpt/lean-weight-perturbation-20261005`.

Not claimed: `leanchecker`, transitive axiom audit, or the five rejection controls on this head. Those steps stand after the build. Not claimed: full-package alignment, a change to #281, or scientific acceptance.
