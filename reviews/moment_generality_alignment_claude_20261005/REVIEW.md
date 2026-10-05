# Source-to-statement alignment of Math-#279: all 40 targets

Scientific effect: **NONE**. Dylan Roy, delegated AI review. Actual performer:
Anthropic / Claude, Claude Code session `session_015wNj8LPTKXsaT68G3DgPPh`,
running in a managed cloud container. No Task helpers and no human review are claimed.
Same-account organizational-independence credit: **0**.

**Verdict: PASS on all 40 targets, scoped to their displayed hypotheses. No
source change is requested.** All 40 Lean statements match their scope notes and
cited sources. The four new statements match their proposals token for token.
The one adapted proof proves the identical type.

**The accepted machine record is withheld.** The reason is lineage only: the
provider behind the #277 proposal is UNKNOWN (see "Lineage"). The fail-closed
candidate `alignment.candidate.json` beside this file is not ACCEPTED, so
`gate.py --alignment` rejects it. The frozen head was not edited.

## Identity of what was reviewed

| Item | Value |
|---|---|
| Pull request | Math-#279, `chatgpt/lean-moment-generality-20261005` |
| Frozen head / tree | `f6672c1a77d67b6257c43acaf5a4481b28fd87e0` / `a5a8efaa0421ee974f6bd97dcf42b0bd7c4cdef6` |
| Base | `a44db48f10ea27c93595840118457a39a5bbbea4` (merged #275, 36 targets) |
| `formal/manifest.json` SHA-256 | `74c5a33861e282ef8432084f3cae0a9493e0d2273a1e8424d4571eddd8adcb54` (local `gate.py`: SOURCE_IDENTITY_PASS, same digest) |
| `formal/SCOPE.md` SHA-256 | `198bbc6c60fdb9148ae21c0f25b52d3b612de20c373dc1e6df818767987da452` |
| `MomentGenerality.lean` / `MOMENT_GENERALITY.md` | `fdec55f1…b509` / `5386c763…0cf2` (equal to the manifest entries) |
| #277 proposal (agent 6), `d1267a6106e8180eeb75fa008ce09de9ad8065ca` | `reviews/lean_cycle2_20261005/agent6/MomentTail_finite_MT_N2.lean.txt`, SHA-256 `4650d373bff434c6f3dafcbd84d7cfab9014a2145f045ab9b00e63832f3915ce` |
| #278 proposal (agent 7), `cf58e5b812699cd7016441c0b477b86fecb7017f` | `reviews/lean_cycle2_20261005/agent7/MomentTail_family_interval_MT_N1.lean.txt`, SHA-256 `f55e12d972b59ab173319ef03c439847a33195e039da241befa80cad9b954635` |
| Analytic source | P02-LM-008, `imports/hardening_ebedb780/P02-LM-008/proof.md.export.txt` at `22876edaaec054d3ab8b0b16668ce3ff8cbf8c73`, SHA-256 `06967d0ba2c2d20550f3bd86ddc97981e324e5f94cd7710996445d507ae2285b` |
| Hosted kernel evidence | run 37334385439 attempt 1, `pull_request` on the frozen head. `formal / formal-evidence` job 111845319753, `downstream-replay` and `math-downstream-gates` all SUCCESS. Step 5 "Build, recheck, audit axioms and execute negative controls" succeeded. This session cannot download artifacts, so the receipt digest is not re-hashed here. |

## Lineage

| Contribution | What I can establish |
|---|---|
| 36 retained targets (#272, #273, #275) and the #279 adaptation | OpenAI / GPT-6 Astra Pro, as credited in the source headers and scope notes |
| #278 proposal (agent 7: the interval family and its bridge) | Cursor cloud run `bc-368b4374-1a7c-5a78-b7b6-ed5ee50532d8`, reported as xAI / Grok 4.7 by #280 and CoS 5997929589 |
| #277 proposal (agent 6: the finite tail and its specialization) | Role label "Grok Bot agent 6" only. Provider **UNKNOWN** (CoS 5997929589). I cannot exclude that the underlying model is Anthropic. |
| This reviewer | Anthropic / Claude. I authored none of #272–#280, the GP-FOR-192 originals, or the P02-LM sources. |

Anthropic is distinct from OpenAI (36 targets plus the adaptation) and from xAI
(#278). It is not established as distinct from the #277 proposer.

What #277 actually contributes:
- `p02_lm009_moment40_tail_finite` has the same proof as the OpenAI-authored
  `p02_lm009_moment40_tail` (identical after removing comments and
  normalizing whitespace).
- Its type differs from that theorem only in `[IsFiniteMeasure μ]` replacing
  `[IsProbabilityMeasure μ]`.
- `p02_lm009_moment40_tail_of_finite` is a one-line specialization.

The exposure is therefore narrow, but it is not zero. The gate compares one
`author` string with one `reviewer` string. Writing "OpenAI" as the author would
pass that check while hiding the UNKNOWN proposer, and the request forbids
exactly that. So the record is published as a candidate only, and the decision
belongs to the coordinator or owner. If they rule that this exposure is
acceptable, or #277's provider is established as non-Anthropic, the change is
one field: `"disposition": "ACCEPTED"`. Everything else is already bound.

## A. The four new targets

The comparison removed comments and normalized whitespace. Each theorem was
split at its first `:=`.

| Declaration | Type vs proposal | Proof vs proposal | Relation to retained theorem |
|---|---|---|---|
| `p02_lm009_moment40_tail_finite` | identical (#277) | identical | Proof identical to `p02_lm009_moment40_tail`. Type differs only in the instance (finite measure instead of probability measure). |
| `p02_lm009_moment40_tail_of_finite` | identical (#277) | identical | Type identical to `p02_lm009_moment40_tail`. |
| `p02_lm009_moment40_family_r3_interval` | identical (#278) | identical | `IsProbabilityMeasure (μ r)` moves from a global instance into `hdata` for each `0<r≤r0`. The `letI` acts inside the `r` case only. |
| `p02_lm009_moment40_family_r3_of_interval` | identical (#278) | **different, disclosed** | Type identical to `p02_lm009_moment40_family_r3`. The proof uses `⟨inferInstance, hdata r hr hrr0⟩` instead of seven projections. Since `∧` is right-associative this builds the same term, and the kernel accepted it. |

Semantic checks requested in 5998011633:

1. **Mass, not probability.** `tail_finite` bounds `(μ (badJetEvent R r ε)).toReal`
   with no division by `μ univ`, so the mass may exceed 1. Taking total mass 2
   and the whole space as the event shows that an extra normalization would be
   false. This matches `test_no_extra_total_mass_normalization`.
2. **Zero measure.** `IsFiniteMeasure 0` holds, so the zero measure is allowed.
   The left side is 0, and `∫ = 0 ≤ M` forces `M ≥ 0`, so the bound is
   nonnegative and correct.
3. **Signed and strict cases.** The event is `ε < r·R^5`. With `r, ε > 0`,
   membership forces `R^5 > ε/r > 0`, and `badJet_subset` (unchanged) gives
   `(ε/r)^8 ≤ R^40` without any sign assumption on `R`. At the boundary
   `ε = r·R^5` the point is excluded. A null atom contributes zero mass.
4. **Integrability.** `Integrable (fun x => R x ^ 40) μ` is explicit. No
   divergent integral that Lean would silently total to zero is used.
5. **Local probability instance.** In the interval theorem nothing at all is
   assumed for `r ∉ (0, r0]`, so `μ r` may be the zero measure there.
6. **Fixed constants.** `∃ C, 0 ≤ C ∧ ∀ r, 0<r → r≤r0 → …` puts `C` before `r`.
   The witness `(√cW/cZ)·√(M/ε^8)` is built from `M, cW, cZ, ε` only, and
   these are bound outside `hdata`. Nothing derives uniformity from pointwise
   constants.
7. **Lower-normalizer direction.** `cZ * r^2 ≤ ∫ W r ∂(μ r)` is a **lower**
   bound on the normalizer, as P02-LM-008 requires: lines 101–104 state the
   premise `Z_r ≥ c_Z r²`, and line 242 says "An upper bound on the ratio uses
   the lower bound". The upper bound
   of GP214 cannot be substituted. The retained target
   `p02_lm008_upper_normalizer_counterexample` exhibits that failure.
8. **Domain.** `0 < r0 ≤ 1` and `r ≤ r0` give `r ≤ 1`, which is what the
   `r^4 → r^3` step in `moment40_weighted_r3` needs.

## B. The 36 retained targets: identity plus an independent read

- **Identity.** These files are byte-identical between the head that #276
  reviewed (`7206526ed53f7539838711ee45257a13b4b07e99`) and `f6672c1`:
  - the source modules `AlgebraV2`, `ProbabilityCompanionsV2`, `MeasureBridge`,
    `WeightedLaw` and `MomentTail`;
  - `originals/`, `gate.py`, `lean-toolchain`, `lakefile.toml` and
    `lake-manifest.json`;
  - the scope notes `MEASURE_BRIDGE.md`, `WEIGHTED_LAW.md` and `MOMENT_TAIL.md`.

  The xAI record on #276 binds `REVIEW.md` at
  `0cb17c1b836651144486d55788eef8d7cf532081` with SHA-256 `65c9be8f…1f79`. I
  re-hashed that file, and it matches. That JSON is **not** relabeled or
  reused here.
- **Independent read.** I read every one of the 36 statements against
  `SCOPE.md`, `COMPATIBILITY.md`, `MEASURE_BRIDGE.md`, `WEIGHTED_LAW.md`,
  `MOMENT_TAIL.md`, the blueprint and P02-LM-008. Results:
  - **Scalar pilot (13).** These are exact algebraic identities or conditional
    inequalities, matching the SCOPE table. Hand check for EC-005:
    `V_s(s) − V_s(−s) = 4s³/3 = (2s)³/6`. The noncomputable annotation and the
    two removed `ring` calls agree with COMPATIBILITY items 1–3.
  - **MeasureBridge (7).**
    - `integral_cs` has no probability instance, as its note states.
    - `event_cs`, `event_numerator` and `measure_transfer` use one `μ` and
      one `W` throughout. They need no independence assumption, and they derive
      a positive normalizer from the lower bound.
    - `measure_transfer` is P02-LM-008's displayed inequality, with `n/z` in
      place of `P_r(E)`.
    - The two counterexamples are true scalar propositions. Checked by hand:
      `1 = 2·½`, `1 > ½`.
  - **WeightedLaw (9).**
    - `weightedLaw = ofReal(∫W)⁻¹ • μ.withDensity(ofReal ∘ W)`.
    - The probability property is proved under integrability, a.e.
      nonnegativity and a positive normalizer.
    - `probability_transfer` states P02-LM-008 for the constructed `P_r` (PT1),
      with `Q_r = μ`.
    - The behaviour of zero and unit weights, null sets and a.e.-equal weights
      matches the note.
  - **MomentTail (7).** The Markov step holds on a finite measure. The strict
    event is measurable from `Measurable R`. The tail is `(M/ε^8)r^8`, and the
    weighted bounds are `C r^4` and then `C r^3` on `r ≤ 1`, with `C` exactly
    as in `MOMENT_TAIL.md`. The family theorem keeps its stronger global
    instance; MT-N1 describes this accurately.

  I found no mismatch between any statement and its note or source.

## C. Package wiring

- **Manifest.**
  - `targets` lists exactly 40 names: the earlier 36 in their original order,
    then the four new ones.
  - The new module is added to `source_modules` and to the root import.
  - The file hashes for the README, root module, SCOPE and the new files match
    their bytes; `gate.py` source check: PASS.
  - `scientific_effect` is NONE and `alignment_status` stays
    `PENDING_INDEPENDENT_REVIEW`.
- **Tests.** I ran `python3 -m unittest discover -s formal/tests` locally with
  Python 3.11.15: 86 tests pass, both normally and under `-O`.
- **Inventory guards.** `test_moment_tail.py` now pins the 29:36 slice and
  `len ≥ 36`. `test_moment_generality.py` pins 36:40 and `len == 40`, and the
  unchanged gate enforces the complete inventory, so no target can drop
  unnoticed.
- **Workflows, gate, toolchain and pins.** All unchanged relative to the base.

## D. Local kernel replay

I replayed the frozen head in this container with Lean 4.34.1, mathlib
`d13f23b723b8a846827a245b89c10fc7d3f11612` from the pinned cache, and Python 3.11.15.

| Step | Result |
|---|---|
| `lake build` (fresh, after the gate deleted `.lake/build`) | exit 0. 8931 jobs; the only warnings are the retained unused-variable and style lints. |
| `leanchecker ResearchFormalCoreR1` | **Not reproduced locally.** The container's memory cgroup killed it at about 13.5 GB resident (exit 137, OOM). Hosted run 37334385439 step 5 is the only recheck evidence. |
| `#print axioms` for all 40 targets | exit 0. Every target uses exactly `propext`, `Classical.choice` and `Quot.sound`. |
| `#check` with `pp.explicit` for all 40 targets | exit 0. 40 declarations elaborated; the types match section A. |
| Five negative controls | `false_fold` and `false_power` REJECTED_BY_LEAN; `sorry`, `custom_imported` and `native` REJECTED_BY_AXIOM_GATE |
| Version and dependency HEADs, and recheck of the manifest after execution | pass; manifest digest `74c5a338…cb54`, checked commit `f6672c1…` |

The run used an unmodified `gate.py --execute`, except that one line was
replaced in a throwaway copy that was never committed: the `leanchecker`
call became a printed `SKIPPED_LOCAL_OOM`. The unmodified gate fails here only
at that step. The local receipt is **not** trusted evidence, as the README
says, and it is not offered as any. Local log SHA-256 values:
- `build.log`: `26cf627f…107f`
- `axioms.log`: `11de3a5b…63e3`
- `elaborated-types.log`: `5e64a67c…7aa9`
- `receipt.json`: `73fe3be8…4a`

## Optional observations (not blocking, no change requested)

- **O1.** In both family theorems, `hM : 0 ≤ M` follows from the hypotheses:
  the interval is nonempty and `∫ R^40 ≥ 0 ≤ M`. Keeping a stronger-than-needed
  hypothesis matches the stated SCOPE policy.
- **O2.** `test_moment_tail.py` relaxes `len == 36` to `len ≥ 36`. Coverage is
  kept by the new exact `len == 40` test and by the gate's own inventory check.

## Not claimed

- No concrete Gaussian, typed-Palm, derivative-supremum, moment,
  lower-normalizer (P02-LM-006), uniformity, GT5, P0.2 or parent-persistence
  result.
- No change to the L8/L9 gap maps.
- No merge, readiness change, flag flip, or edit to source, gate, workflow or
  register.
- No organizational-independence credit (everything runs on the same account).
