# Statement alignment — fortieth-moment tail, 36 targets

Scientific effect: **NONE**. Dylan Roy — delegated AI review. Actual performer: xAI / Grok 4.7, Cursor Cloud Agent session `bc-7023823a-e5a0-4485-abde-ef11860647cb`, model `grok-4.7-high-fast`. Same-account organizational-independence credit: **0**. No human review is claimed.

Verdict: **PASS**. No source change is requested. Head `7206526ed53f7539838711ee45257a13b4b07e99` stays frozen.

## Pickup

| Item | Observed value |
|---|---|
| Pull request | Math-#275, `chatgpt/lean-moment-tail-20261005` |
| Frozen head | `7206526ed53f7539838711ee45257a13b4b07e99` |
| Tree | `f791d7c26c2c3ebeb13513000f6803312f0961d5` |
| Stacked base | Math-#273 `dce1b197be3431673289905259be38b450e9b898` |
| Run | https://cursor.com/agents/bc-7023823a-e5a0-4485-abde-ef11860647cb |
| Runtime | Cursor Cloud Agent, source `scm`, `privateWorkerId` null, `usePrivateWorker` false |
| Reachable self-hosted workers | 0 (`list-self-hosted-workers`, scope all, totalCount 0). No historical roster was used. |
| Task helpers | Two local Task agents, launched after that count was known. No further fan-out. |

Helpers, both read-only:

- Scope A, source-to-type and family quantifiers: `bc-57bd47a3-bb73-5727-b68b-ef4014b80e8b`
- Scope B, inventory, retained bytes, repair chronology, finite models: `bc-6ddca7f0-1186-5eef-b15c-7267c8ad4068`

This reviewer re-read `MomentTail.lean`, `MOMENT_TAIL.md`, the new `SCOPE.md` section, the predecessor statements those proofs call, and the pinned mathlib Markov lemma. Helper reports were checked against those sources. Neither helper edited the tree.

## Scope actually checked

Compared, at the frozen head:

- definition `badJetEvent` and the seven new theorems in `formal/ResearchFormalCoreR1/MomentTail.lean`
- `formal/MOMENT_TAIL.md` and the additive section of `formal/SCOPE.md`
- predecessor bytes of `AlgebraV2.lean`, `ProbabilityCompanionsV2.lean`, `MeasureBridge.lean`, `WeightedLaw.lean`
- pinned mathlib `d13f23b723b8a846827a245b89c10fc7d3f11612`, theorem `MeasureTheory.mul_meas_ge_le_integral_of_nonneg` in `Mathlib/MeasureTheory/Integral/Bochner/Basic.lean` (lines 1161–1172 of that revision)
- manifest pins, gate inventory, the 20:29 test adjustment, the repair diff `4fe5826..7206526`, and `formal/tests/test_moment_tail.py`
- hosted runs 37315764990 and 37316631037

The 29 earlier theorem modules are byte-identical to Math-#274's reviewed head `dce1b197be3431673289905259be38b450e9b898`. Their statements are carried forward on that comparison. The #274 JSON is not relabeled: its manifest `d843ba7b96457a95e6485a4bc30678a8a252acf405d369b26dab81832c596c39` and scope `e8ef291bb7daa334812451a675788b4ee902c0974d9bcd3197407b6b56b63548` are stale for this package. Main#267's 20-target record was not edited.

Not checked here: a local `lake` build or `leanchecker` replay. Kernel evidence below is the hosted artifact only. This review does not merge, does not edit `formal/`, and does not change `alignment_status`.

## Pins checked at this head

| Path | SHA-256 | Claim |
|---|---|---|
| `formal/ResearchFormalCoreR1/MomentTail.lean` | `87fe3ee90afc52d8c2652881f1ae195d1b0b15a2ffc18c84d6166d1a4d0de2aa` | match |
| `formal/manifest.json` | `ddaa37078805089b57a81f302c069fba7411a23af047c49fd3a4d2897b545e59` | match |
| `formal/SCOPE.md` | `21c4ce34ff1e7536c88de86661c796a0751ad8572b034650631052ad0791f4a1` | match |
| `formal/evidence/moment-tail-initial-build-failure.log` | `61bee2d55d0dd548b0bccc4d2e40970f654fca8ab1385af7f371592d45c0ab08` | match |
| `formal/MOMENT_TAIL.md` | `20ecddcd830c41935dc4b366882db4d0432240932af6632d025b981f90e044bd` | recorded |
| `formal/gate.py` | `4f14a78bbc6e9b7f929648b13ad3a9ae467256db4be9792e3667680e697a5c94` | unchanged from `dce1b19` |
| `formal/ResearchFormalCoreR1/WeightedLaw.lean` | `f31dfd2cd048cc0c0446c54c46d89c9cdd5d7bb9d76e9d8d16b7c034f351d736` | unchanged |
| `formal/ResearchFormalCoreR1/ProbabilityCompanionsV2.lean` | `338452a0c2ba24d016059354d543cc995b8cb29c9d4a41d98bb93499f5f8cb8f` | unchanged |
| `formal/ResearchFormalCoreR1/MeasureBridge.lean` | `28ac130db490c3c3e2fbfabf3ac5be43c854ab1468bf573bf5a8c0dd2c50955f` | unchanged |
| `formal/ResearchFormalCoreR1/AlgebraV2.lean` | `4480708263c40a2f7f03f12ef7e15f0eb4f8193c2dccbb253921a7ec251863c3` | unchanged |

`python3 -B -S formal/gate.py` printed `SOURCE_IDENTITY_PASS` for manifest `ddaa37078805089b57a81f302c069fba7411a23af047c49fd3a4d2897b545e59` and exited 0. That command does not run Lean. `git diff --exit-code dce1b19 HEAD` is empty on the four predecessor modules, `formal/gate.py`, and `.github/workflows/formal-lean.yml`.

## Hosted execution actually observed

Initial run [37315764990](https://github.com/d6g8k5htny-coder/Math-/actions/runs/37315764990) completed **failure** on head `4fe582656032ba02ed16c78ce7d096609fb2a007`. The preserved log's first error is the set-membership mismatch at `MomentTail.lean:56`: term `hp` has type `(ε / r) ^ 8 ≤ R x ^ 40` and was expected to have type `x ∈ {x | (ε / r) ^ 8 ≤ R x ^ 40}`. That log is history, not a success receipt.

Repair run [37316631037](https://github.com/d6g8k5htny-coder/Math-/actions/runs/37316631037) completed **success** on PR head `7206526ed53f7539838711ee45257a13b4b07e99`. Checks: `downstream-replay` pass, `formal / formal-evidence` pass, `math-downstream-gates` pass.

The formal artifact `formal-evidence-37316631037-1` was downloaded in this session. Its `required-check-binding.json` records `checked_commit` `f934f9a1467d99f3f0d3121bc3385342b95294ec`, run `37316631037`, attempt `1`, receipt SHA-256 `7f52455e13b93e4dad69d374be0041c51ca6f4567010189be8f9c3b4119367f7`. Rehashing the downloaded `receipt.json` reproduced that digest. Every log digest in the receipt matches the downloaded log bytes.

That checked commit is the pull-request merge `Merge 7206526… into dce1b19…`, parents `dce1b197be3431673289905259be38b450e9b898` and `7206526ed53f7539838711ee45257a13b4b07e99`. Its tree equals the frozen head's tree `f791d7c26c2c3ebeb13513000f6803312f0961d5`. `git diff` between them is empty. The receipt's `manifest_sha256` is the frozen manifest. The required-check contract records this synthetic merge commit; it is not a different source tree.

Receipt contents used here:

- `formalization_status` `kernel-checked`; `alignment_status` remains `PENDING_INDEPENDENT_REVIEW`
- Lean `version 4.34.1`, commit `5045d0056413266e57c625dcd7c365b10e377c52`
- mathlib revision `d13f23b723b8a846827a245b89c10fc7d3f11612`
- 36 axiom entries, exactly the manifest targets, each `{Classical.choice, Quot.sound, propext}`
- negative controls: `custom_imported`, `native`, and `sorry` are `REJECTED_BY_AXIOM_GATE`; `false_fold` and `false_power` are `REJECTED_BY_LEAN`
- `build.log` ends `Build completed successfully (8930 jobs)` and includes `Built ResearchFormalCoreR1.MomentTail`
- `leanchecker.log` is empty. Its digest is the empty-file SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. The hosted gate accepted that exit. This session did not re-run `leanchecker`.

`python3 -B -S -m unittest formal.tests.test_moment_tail` and the same command with `-O` each ran 12 tests and passed. Those tests do not invoke Lean.

## Findings

No blocker and no amend. `MT-N1` and `MT-N2` are non-blocking notes. They do not request a push.

### MT-A1 — finite mass versus infinite-mass collapse — no-finding

Pinned mathlib, revision `d13f23b7…`, states

`ε * μ.real {x | ε ≤ f x} ≤ ∫ f`

for an a.e.-nonnegative integrable `f`, with no finite-measure hypothesis. Its `⊤` branch rewrites `μ.real` through `measureReal_def`, and `(⊤).toReal = 0`, so an infinite superlevel becomes the trivial `0 ≤ ∫ f`.

`p02_lm009_markov_event` adds `[IsFiniteMeasure μ]` and `0 < a`, then proves

`(μ A).toReal ≤ (μ {x | a ≤ Y x}).toReal`

by `ENNReal.toReal_mono (by finiteness)` before dividing by `a`. Finiteness is what keeps that comparison from sending an infinite mass to zero. The divisor is the threshold `a`, not `μ(Ω)`. There is no `μ(A)/μ(Ω)` step.

The fortieth-moment theorem applies this on `[IsProbabilityMeasure μ]`. The weighted bound's renormalizer is the separate quotient from `p02_lm008_probability_transfer`, which divides by `∫ W` under `cZ * r ^ 2 ≤ ∫ W` and `0 < cZ`.

### MT-A2 — generic event versus one scalar event — no-finding

`p02_lm009_markov_event` quantifies over an arbitrary `A : Set Ω` with only `A ⊆ {x | a ≤ Y x}`. It does not mention `badJetEvent` and does not require `MeasurableSet A`. Mathlib's lemma itself is the superlevel; the arbitrary-event step is the local monotonicity argument.

`p02_lm009_moment40_tail` instantiates `A` only as `badJetEvent R r ε`. Later theorems use that same set. Measurability is a separate theorem, supplied to `p02_lm008_probability_transfer` by `p02_lm009_badJet_measurable`.

### MT-A3 — integrability versus a totalized integral — no-finding

Both the generic lemma and `p02_lm009_moment40_tail` take `Integrable` and conclude with the Bochner integral. The module contains no `∫⁻` and no integral-default hypothesis. Nonnegativity of `R ^ 40` is proved everywhere, then passed as an almost-everywhere fact. `0 ≤ M` is not a hypothesis of the unweighted tail; it is required where `Real.sqrt (M / ε ^ 8)` is formed.

### MT-A4 — strict event and signed `R` — no-finding

`badJetEvent R r ε` is `{x | ε < r * R x ^ 5}`. With `0 < r` and `0 < ε`, `p02_lm009_bad_event_threshold` gives `ε / r < R x ^ 5`, so a negative value is outside the event. `R ^ 40` is nonnegative for every real `R`. The subset theorem weakens `<` to `≤` before the eighth power:

`badJetEvent R r ε ⊆ {x | (ε / r) ^ 8 ≤ R x ^ 40}`.

The equality case stays out of the event. `Measurable R → MeasurableSet (badJetEvent R r ε)` is separate. The hosted elaboration of `p02_lm009_badJet_subset` is that subset, with right-hand power `40` and left-hand power `8`.

### MT-A5 — exponents `40 → 8` and `ε ^ 8` — no-finding

`p02_lm009_power40_identity` is `(R ^ 5) ^ 8 = R ^ 40`. On the event, `0 < ε / r ≤ R ^ 5`, so `(ε / r) ^ 8 ≤ R ^ 40`. Markov at that positive threshold yields

`(μ A).toReal ≤ (∫ R ^ 40) / (ε / r) ^ 8 ≤ M / (ε / r) ^ 8 = (M / ε ^ 8) * r ^ 8`.

The Lean calc is that chain, closed by `field_simp [ne_of_gt hr, ne_of_gt hε]`. Both `r` and `ε` are positive, and the exponent 8 is even.

### MT-A6 — `r ^ 4`, then `r ^ 3` on `0 < r ≤ 1` — no-finding

`p02_lm008_probability_transfer` gives

`(weightedLaw μ W A).toReal ≤ (Real.sqrt cW / cZ) * Real.sqrt ((μ A).toReal)`.

From `(μ A).toReal ≤ (M / ε ^ 8) * r ^ 8` and `0 ≤ M`, `Real.sqrt_mul` and `Real.sqrt_sq` produce `Real.sqrt ((μ A).toReal) ≤ Real.sqrt (M / ε ^ 8) * r ^ 4`. The product is

`((Real.sqrt cW / cZ) * Real.sqrt (M / ε ^ 8)) * r ^ 4`.

`p02_lm009_moment40_weighted_r4` has no `r ≤ 1` hypothesis. The cubic theorem adds `r ≤ 1` and calls `p02_lm009_palm_r4_to_r3`, whose predecessor `p02_lm009_r4_le_r3` proves `r ^ 4 ≤ r ^ 3` on `0 ≤ r ≤ 1`. For `r ∈ (0, 1)` the fourth-order bound is the tighter one. At `r = 1` the powers agree. The cubic theorem does not claim `r > 1`.

### MT-A7 — one constant, uniform in `r` — no-finding

`ε`, `M`, `cW`, `cZ`, and `r0` are parameters outside `∀ r`. The per-`r` package uses those same constants. The conclusion is `∃ C, 0 ≤ C ∧ ∀ r, 0 < r → r ≤ r0 → … ≤ C * r ^ 3`. The proof witness, chosen before `intro r`, is `(Real.sqrt cW / cZ) * Real.sqrt (M / ε ^ 8)`. Hosted elaboration shows the same binder order, including `[∀ (r : Real), IsProbabilityMeasure (μ r)]` and `hdata : ∀ (r : Real), …`.

### MT-A8 — one scalar threshold — no-finding

The event is exactly `{ε < r * R ^ 5}`. `M`, `∫ W ^ 2 ≤ cW * r ^ 4`, and `cZ * r ^ 2 ≤ ∫ W` are premises. The import is only `ResearchFormalCoreR1.WeightedLaw`. No Gaussian, Palm, supremum, GT5, or good-event-complement theorem is proved. `MOMENT_TAIL.md` lines 70–79 and `SCOPE.md` lines 64–68 state that limit. The `p02_lm009_` names are labels on these conditional implications.

### MT-B1 through MT-B3, MT-B5 through MT-B7 — no-finding

Pins, predecessor bytes, and the workflow comparison are the tables above. The gate counts `theorem`/`lemma` declarations. The five modules contribute 6, 7, 7, 9, and 7 theorems, total 36, equal to `manifest.json` `targets`. `def badJetEvent` is outside that count, as are `foldPotential` and `weightedLaw`.

`formal/tests/test_weighted_law.py` `test_exact_target_inventory` binds `targets[20:29]` and `len ≥ 29`. `formal/tests/test_moment_tail.py` `test_exact_inventory` binds `targets[29:]` to the seven new names and `len = 36`. The finite model asserts 243 tail/threshold cases and 972 weighted-event cases, and rejects omitted `ε ^ 8`, a 20th moment in place of the 40th, and an `r ^ 16` rate. `test_strict_boundary_and_signed_jet` puts `R = 1` and `R = -1` at `r = ε = 1` outside the strict event.

### MT-B4 — repair chronology — no-finding

`4fe5826..7206526` changes `MOMENT_TAIL.md`, `MomentTail.lean`, the preserved failure log, and `manifest.json`. All seven theorem texts through `:= by` stay in place. Two proof bodies change, and both are the repair the writer described: `p02_lm009_badJet_subset` inserts `change ε < r * R x ^ 5 at hx` and `change (ε / r) ^ 8 ≤ R x ^ 40`; `p02_lm009_moment40_tail` drops the trailing `<;> ring` after `field_simp`. `SCOPE.md` is identical across that pair. The hosted success above is for the repaired head, not for `4fe5826`.

### MT-N1 — note, non-blocking

`p02_lm009_moment40_family_r3` assumes `[∀ r, IsProbabilityMeasure (μ r)]` for every real `r`. The bound premises and the conclusion quantify only over `0 < r ≤ r0` with `0 < r0 ≤ 1`. The constant still does not depend on `r`. The extra instance is a stronger hypothesis than the interval stated in `MOMENT_TAIL.md`. It does not make the proved bound false. No change is requested.

### MT-N2 — note, non-blocking

`p02_lm009_markov_event` assumes a finite measure. `p02_lm009_moment40_tail` assumes a probability measure. A probability is a finite measure, so the Markov step applies. The unweighted tail does not use any probability-only fact beyond that instance. `MOMENT_TAIL.md` attributes finite measure to the generic lemma and does not claim the tail theorem for every finite measure. No change is requested.

## Carry-forward of the earlier 29

Math-#274 at `8cf6b74472d77a62f4775a5e3568e79d4407adff` accepted the 29 targets at `dce1b19`, evidence review `8f70c102550a6080c2b8f472df8a601fc7f61081`, SHA-256 `f061aae9e9d1f98b4e5de373d3e0b9f244f43fa37c594d23981ebbb650e2ffbd`. Those 29 names are the prefix of this manifest. The four modules that contain them, the gate, the formal workflow, and the mathlib pin are unchanged. This record covers 36 targets because the seven new statements were read here, not because the old JSON was copied. The old manifest and scope digests do not validate against this tree.

## Boundaries

Concrete moment, normalizer, Gaussian, Palm, and supremum bounds remain premises. This PASS is statement alignment for the displayed hypotheses, plus the hosted kernel receipt identified above. It is not scientific acceptance, not a merge, and not a promotion of `lemma_closed` or any premise.
