# Statement alignment — 29-target weighted probability package

Dylan Roy — delegated AI review. Actual performer: xAI / Grok 4.7, Cursor Cloud Agent, model `grok-4.7-high-fast`, session `bc-3ab4d42c-6316-48de-a53d-152dd0faeb46` (https://cursor.com/agents/bc-3ab4d42c-6316-48de-a53d-152dd0faeb46). Transport: Cursor Cloud (`usePrivateWorker: false`, `privateWorkerId: null`). `list-self-hosted-workers` returned no connected worker. `lake` and `lean` are not on `PATH`; Lean was not re-executed.

Scientific effect: **NONE**. Same-account organizational-independence credit: **0**.

**Verdict: PASS.** Finding IDs: none. Alignment disposition for this package: **ACCEPTED**, covering exactly the 29 manifest targets at the hashes below. This record belongs to Math-#273 head `dce1b197be3431673289905259be38b450e9b898`. It does not rewrite the #272 manifest `845d372a459d32f6b4ffb0a4dceb69363ffe27c4ca6da8838238ce8979d9244d` or the #272 scope `e303550bdd71aa969703fd33dc9808383db13b08072437577d192a7f149a3edb`.

## Exposure

Before the comparison finished I had read the PR body, request comment 5994278916, author execution comment 5994302705, and the earlier seven-target report 5994130542. The statement comparison then used the frozen source, `imports/hardening_ebedb780/P02-LM-008/proof.md.export.txt` at `22876edaaec054d3ab8b0b16668ce3ff8cbf8c73`, and the hosted artifact below. No implementation file was edited.

## Hashes recomputed at `dce1b197be3431673289905259be38b450e9b898`

| Object | SHA-256 |
|---|---|
| `formal/manifest.json` | `d843ba7b96457a95e6485a4bc30678a8a252acf405d369b26dab81832c596c39` |
| `formal/SCOPE.md` | `e8ef291bb7daa334812451a675788b4ee902c0974d9bcd3197407b6b56b63548` |
| `formal/ResearchFormalCoreR1/WeightedLaw.lean` | `f31dfd2cd048cc0c0446c54c46d89c9cdd5d7bb9d76e9d8d16b7c034f351d736` |
| `formal/WEIGHTED_LAW.md` | `a530dc957923c4c9111b734d8fcc0f4cd3cdba45b08480cfc2e241ecefc5fba4` |
| `formal/ResearchFormalCoreR1/MeasureBridge.lean` | `28ac130db490c3c3e2fbfabf3ac5be43c854ab1468bf573bf5a8c0dd2c50955f` |
| `formal/MEASURE_BRIDGE.md` | `bdb6c06f359f17d493d6057adbed61edb20236b7a3a3ca4880ae0b33d8a7200e` |
| `formal/originals/Algebra.lean.txt` | `4c196820c4db8fafc288dd35642828ba577e3544d60aba7d1d6d24f14ad1e8ae` |
| `formal/originals/ProbabilityCompanions.lean.txt` | `4ace6600a476859982c8851ae9097c89b082d3c96291b3c8330bd4cc00bae65d` |
| `formal/ResearchFormalCoreR1/AlgebraV2.lean` | `4480708263c40a2f7f03f12ef7e15f0eb4f8193c2dccbb253921a7ec251863c3` |
| `formal/ResearchFormalCoreR1/ProbabilityCompanionsV2.lean` | `338452a0c2ba24d016059354d543cc995b8cb29c9d4a41d98bb93499f5f8cb8f` |
| `formal/COMPATIBILITY.md` | `33721aad32f82131a6956a06b58c5bc41f5d28f26efe840a99a4d51ad60cf247` |

`MeasureBridge.lean` git blob `11843e5586ec44c7430f077694c90ac8586c50c0` is identical at #272 head `270167900b71539d0e2135131a3a96f1f04289f6` and at this head. `python3 formal/gate.py` printed `SOURCE_IDENTITY_PASS` with manifest digest `d843ba7b96457a95e6485a4bc30678a8a252acf405d369b26dab81832c596c39`.

## Scope A — nine new declarations

Definition, read from source:

`weightedLaw μ W = (ENNReal.ofReal (∫ W ∂μ))⁻¹ • μ.withDensity (fun x => ENNReal.ofReal (W x))`.

That is the formula in `WEIGHTED_LAW.md`. It is a `Measure` for every real `W`. Probability is a later theorem.

Hosted `elaborated-types.log` (`fe71196d1ed77e8a86aacf4584c2e6ced2c6857282999e2e44feae9c018eb5f3`) with `pp.explicit true` gives the following types. Informal source for PT1 and the event bound: `proof.md.export.txt` lines 80–98 and 215–219, and theorem P02-LM-008 at lines 117–123.

| Target | Elaborated statement | Scope row |
|---|---|---|
| `weightedLaw_apply` | `Integrable W μ`, `0 ≤ᵐ[μ] W`, `MeasurableSet A` imply `weightedLaw μ W A = (ofReal (∫ W ∂μ))⁻¹ * ofReal (∫_A W ∂μ)`, with the set integral elaborated as `μ.restrict A` | Measurable-event ENNReal mass equals inverse ofReal normalizer times ofReal set integral |
| `weightedLaw_isProbabilityMeasure` | Same integrability and a.e. nonnegativity, plus `0 < ∫ W ∂μ`, imply `IsProbabilityMeasure (weightedLaw μ W)`. No `IsProbabilityMeasure μ` hypothesis | Integrability, a.e. nonnegativity, and positive normalizer imply total mass one |
| `weightedLaw_event_real` | Those hypotheses imply `(weightedLaw μ W A).toReal = (∫_A W ∂μ) / (∫ W ∂μ)` | Real event mass is the same-law integral ratio |
| `weightedLaw_absolutelyContinuous` | For every `W`, `weightedLaw μ W ≪ μ`. No nonnegativity, integrability, or independence hypothesis | Original-law null sets remain null |
| `weightedLaw_congr_ae` | `W =ᵐ[μ] V` implies `weightedLaw μ W = weightedLaw μ V` | Null-set changes of the weight leave the measure unchanged |
| `weightedLaw_zero` | Constant `0` yields the zero measure | Zero weight yields zero measure |
| `weightedLaw_one` | `IsProbabilityMeasure μ` and constant `1` yield `μ` | Unit weight on a probability space recovers `μ` |
| `p02_lm008_probability_transfer` | On a probability `μ`, `MemLp W 2 μ`, `0 ≤ᵐ[μ] W`, measurable `A`, `0 < r`, `0 ≤ cW`, `0 < cZ`, `∫ W² ∂μ ≤ cW * r^4`, and `cZ * r^2 ≤ ∫ W ∂μ` imply `IsProbabilityMeasure (weightedLaw μ W)` and `(weightedLaw μ W A).toReal ≤ (sqrt cW / cZ) * sqrt ((μ A).toReal)` | Constructs a probability law and its event bound from the same premises as #272 |
| `p02_lm009_probability_transfer_r8_to_r3` | The same premises, plus `r ≤ 1`, `0 ≤ K`, and `(μ A).toReal ≤ K * r^8`, imply that probability property and `(weightedLaw μ W A).toReal ≤ ((sqrt cW / cZ) * sqrt K) * r^3` | Composes the supplied eighth-order event bound with the cubic transfer |

### Attacks

**Positive normalizer versus totalized integral.** Both identification theorems take `Integrable W μ` and, where a probability or a real ratio is concluded, `0 < ∫ W ∂μ`. The scalar in the definition is `ENNReal.ofReal` of that Bochner integral. A non-integrable function is outside `weightedLaw_apply`, `weightedLaw_isProbabilityMeasure`, and `weightedLaw_event_real`. The probability theorem derives `0 < ∫ W` from `0 < cZ`, `0 < r`, and `cZ * r^2 ≤ ∫ W`; it does not assume `IsProbabilityMeasure` of the result.

**A.e. nonnegativity versus `ofReal` clipping.** `weightedLaw_apply` rewrites `withDensity` by `ofReal_integral_eq_lintegral_ofReal` under `hW.integrableOn` and `ae_restrict_of_ae hW0`. The signed pair `W = (-1, 3)` on two equal atoms has signed mass `1` and clipped `ofReal` mass `3/2`. That witness is the rational model in `tests/test_weighted_law.py` and the prose in `WEIGHTED_LAW.md`. It is not one of the 29 kernel targets. The kernel equalities require `0 ≤ᵐ[μ] W`, so they do not apply to that signed pair.

**Measurable-event formula.** `hA : MeasurableSet A` is in the elaborated types of `weightedLaw_apply`, `weightedLaw_event_real`, and both composed transfers. The set integral is `μ.restrict A`.

**Absolute continuity and a.e. invariance.** `weightedLaw_absolutelyContinuous` is `≪` for an arbitrary real weight, which is the informal edge `Q(E) = 0 ⇒ P(E) = 0` once the law is interpreted, and it is stronger in hypotheses because it does not need nonnegativity. `weightedLaw_congr_ae` is equality of the whole measure. Together with `weightedLaw_zero`, an a.e.-zero weight has the zero law; the audited zero statement itself is the constant function.

**Zero and unit edges.** Constant `0` is the zero measure, so it fails `IsProbabilityMeasure`. Constant `1` recovers `μ` only under `IsProbabilityMeasure μ`, matching `Z = 1` and `P(E) = Q(E)` when `W = 1`.

**Composed transfer.** `p02_lm008_probability_transfer` derives `Integrable` from `MemLp W 2` by `MemLp.integrable` at exponent `2` on a probability space, derives a positive integral from the lower normalizer, concludes `IsProbabilityMeasure (weightedLaw μ W)`, rewrites `(weightedLaw μ W A).toReal` by `weightedLaw_event_real`, and calls `p02_lm008_measure_transfer` with `μ`, `W`, `A`, `hW`, `hW0`, `hA`, `r`, `cW`, `cZ`, `hr`, `hcW`, `hcZ`, `hsecond`, and `hlower`. The cubic theorem passes those plus `hr1`, `hK`, and `htail` into `p02_lm009_measure_transfer_r8_to_r3`. The elaborated conclusions are the probability property and the event inequality on `(weightedLaw μ W A).toReal`. Moment, lower-normalizer, and tail hypotheses stay premises. Informal consequences B and C, a uniform family in `r`, a concrete Gaussian or typed Palm law, GT5, P0.2, and parent persistence remain outside this module, as `WEIGHTED_LAW.md` and the new SCOPE section state.

The construction does not require `μ` itself to be finite or a probability measure. The two applications do require `IsProbabilityMeasure μ`. That split matches `WEIGHTED_LAW.md`.

## Scope B — original 13, then the unchanged seven

### Original 13 against `originals/*.lean.txt` and `COMPATIBILITY.md`

`SuccessorTests` passed. An independent extraction of each `theorem … := by` block found 6 algebraic and 7 probability statements identical between the preserved originals and `AlgebraV2.lean` / `ProbabilityCompanionsV2.lean`. The only textual diffs are the three COMPATIBILITY repairs:

1. `def foldPotential` becomes `noncomputable def foldPotential`. The right-hand side `-(x ^ 3) / 3 + (s ^ 2) * x` is unchanged.
2. The surplus `ring` after `field_simp [hr]` in `ec014_contact_power` is deleted.
3. The surplus `ring` after `field_simp [hr, hcZ]` in `p02_lm008_r2_cancel` is deleted.

Hosted `build.log` still warns that `hcW` and `hq` in `ProbabilityCompanionsV2.lean:22` are not explicitly referenced. COMPATIBILITY says those warnings stay. SCOPE says some algebraic assumptions are stronger than necessary and that preserving them is intentional. The statements still carry `0 ≤ cW` and `0 ≤ q`.

| Targets | Statement compared with the SCOPE row |
|---|---|
| `ec005_fold_gap` | For every real `s`, `foldPotential s s - foldPotential s (-s) = (2 * s) ^ 3 / 6`. Scalar fold gap. Random-field normal form and persistence stay outside the statement. |
| `ec008_factor_expansion` | The displayed polynomial identity in real `c, s`. Matrix construction stays outside. |
| `ec010_generic`, `ec010_transverse` | The two displayed polynomial identities for arbitrary real parameters. Chart validity stays outside. |
| `ec011_scalar_cancellation` | `(-h * w) * g + w * (h * g) = 0`. ODE, adjoint transport, and Hessian symmetry stay outside. |
| `ec014_contact_power` | For `r ≠ 0`, `(r ^ 3 / 6) * (1 / r ^ 5) * r ^ 2 = 1 / 6`. Six-pin determinant and Kac–Rice density stay outside. |
| `p02_lm008_r2_cancel` | For `r ≠ 0` and `cZ ≠ 0`, the displayed `r ^ 2` cancellation. Nonzero, matching the SCOPE row. Conditioning stays outside. |
| `p02_lm008_cross_multiplied`, `p02_lm008_quotient_bound` | From `0 < r`, `0 ≤ cW`, `0 < cZ`, `0 ≤ q`, `cZ * r ^ 2 ≤ z`, and `n ≤ sqrt(cW) * r ^ 2 * sqrt(q)`, the cross-multiplied inequality; the quotient adds `0 < z` and concludes `n / z ≤ (sqrt(cW) / cZ) * sqrt(q)`. Conditional Cauchy–Schwarz, moment estimates, and existence or uniformity of the lower normalizer stay outside these two statements. |
| `p02_lm009_bad_event_threshold` | `0 < r` and `ε < r * R ^ 5` imply `ε / r < R ^ 5`. Markov and tail measurability stay outside. |
| `p02_lm009_power40_identity` | `(R ^ 5) ^ 8 = R ^ 40`. |
| `p02_lm009_r4_le_r3` | `0 ≤ r ≤ 1` implies `r ^ 4 ≤ r ^ 3`. |
| `p02_lm009_palm_r4_to_r3` | `0 ≤ C`, `0 ≤ r ≤ 1`, and `p ≤ C * r ^ 4` imply `p ≤ C * r ^ 3`. Existence of a uniform `C`, an all-small-`r` stochastic theorem, and parent closure stay outside. |

The current SCOPE diff against `2701679` rewords one sentence from "The package now registers 20 declarations" to "This retained layer consists of 20 declarations" and adds the weighted-law section. The original 13 rows and the seven bridge rows are otherwise unchanged.

### Seven-target reuse, completing coverage of 20

`MeasureBridge.lean` and `MEASURE_BRIDGE.md` are byte-identical to the files hashed in comment 5994130542. That comment's PASS for the seven declarations is reused at those bytes. This session also re-read `MeasureBridge.lean` and `MEASURE_BRIDGE.md`. The seven statements still match that scope note: Bochner Cauchy–Schwarz for nonnegative `L²` functions; the indicator event form under one probability; the `r²` numerator from `∫ W² ≤ cW * r^4`; the ratio bound from the explicit lower normalizer; the `r^8` input composed through an intermediate `r^4` bound and `p02_lm009_palm_r4_to_r3` on `0 < r ≤ 1`; and the two scalar witnesses for a missing square root and an upper normalizer. PT1 stays outside `MeasureBridge.lean`, which is why `WeightedLaw.lean` exists.

Coverage of the retained 20 is the original 13 comparison in this file plus that unchanged seven-target read. No source mismatch appeared.

### Coverage of 29

The 29 are those 20 plus the nine in Scope A, in manifest order. Both composed theorems call the unchanged bridge theorems and add the constructed probability measure. That is the full target list required by `gate.py` `check_alignment`.

## Inventory and gate

`git diff 2701679..dce1b19 -- formal/tests/test_measure_bridge.py` is exactly two lines:

- `manifest['targets'][13:]` becomes `manifest['targets'][13:20]`
- `len(manifest['targets']) == 20` becomes `len(manifest['targets']) >= 20`

`test_weighted_law.py` requires `manifest['targets'][20:]` to be the nine names and `len == 29`. `gate.py` `source_check` requires the theorem declaration order to equal `manifest['targets']`. The first 20 names match the #272 manifest. `gate.py`, `lean-toolchain`, and the five rejection controls are unchanged. Blueprint links still resolve for the previous six declarations. The nine new names are not `\lean{...}` links. The gate requires every link to be a target; it does not require every target to be a link, and SCOPE does not claim those nine links.

`alignment_status` in `formal/manifest.json` remains `PENDING_INDEPENDENT_REVIEW`. This review file is the separate record. The source manifest does not self-award acceptance.

## Hosted kernel evidence, separate from this alignment

Run [37307996351 attempt 1](https://github.com/d6g8k5htny-coder/Math-/actions/runs/37307996351) completed `success` on pull_request head `dce1b197be3431673289905259be38b450e9b898`. Receipt `checked_commit` is `0283a20729681a77a102d99cdddd88cded0bf891`. That commit's tree equals this head's tree (`1426f9be6b68a9fed9d5390b685c8e58ebe36b3c`); `git diff` between them is empty.

Artifact `formal-evidence-37307996351-1` (id 11344895896): receipt SHA-256 `937930970cbd5141e5af116ac26924715f665f0204193f4e48e8659deacab6c1`, matching `required-check-binding.json`. All 10 receipt log digests matched the extracted files, including empty `leanchecker.log`. Receipt contents: Lean 4.34.1 commit `5045d0056413266e57c625dcd7c365b10e377c52`, mathlib `d13f23b723b8a846827a245b89c10fc7d3f11612`, manifest `d843ba7b…`, 29 declarations, axioms only `propext` / `Classical.choice` / `Quot.sound`, negative controls `false_fold` and `false_power` `REJECTED_BY_LEAN`, `sorry` / `custom_imported` / `native` `REJECTED_BY_AXIOM_GATE`. Receipt `alignment_status` remains `PENDING_INDEPENDENT_REVIEW`. Build log: `WeightedLaw` built with no warning; the only warnings are the pre-existing unused `hcW` and `hq`.

Local Python, not Lean: `python3 -B -S -m unittest discover -s formal/tests -v` and the same command with `-O` each ran 62 tests, OK.

## Boundary of this acceptance

Accepted here: each of the 29 Lean statements and the `weightedLaw` definition, compared with `SCOPE.md`, `WEIGHTED_LAW.md`, `MEASURE_BRIDGE.md`, `COMPATIBILITY.md`, the preserved originals, and the cited informal PT1 / P02-LM-008 interface.

Left outside this record: a concrete typed Palm or Gaussian identification; discharged moment, lower-normalizer, or event-tail premises; uniformity in `r`; informal corollaries B and C; GT5; P0.2; parent persistence; scientific-register or `lemma_closed` changes; and any claim that #272's distinct manifest already carries this acceptance. Kernel execution remains the hosted receipt above. This session did not run Lean.
