# Statement read — finite-measure and interval-only companions

Scientific effect: **NONE**. Dylan Roy — delegated AI review. Actual performer: xAI / Grok 4.7, Cursor Cloud Agent session `bc-85fa10d4-a91c-4459-aa35-96e00514cdd1`, model `grok-4.7-high-fast`. Same-account organizational-independence credit: **0**. No human review is claimed.

Verdict: **scoped PASS**. No source change is requested. This is not a 40-target alignment acceptance, and no `alignment.json` is published. Frozen head `f6672c1a77d67b6257c43acaf5a4481b28fd87e0` was not edited.

## Pickup and identity

| Item | Observed value |
|---|---|
| Pull request | Math-#279, `chatgpt/lean-moment-generality-20261005` |
| Frozen head | `f6672c1a77d67b6257c43acaf5a4481b28fd87e0` |
| Tree | `a5a8efaa0421ee974f6bd97dcf42b0bd7c4cdef6` |
| Base | `a44db48f10ea27c93595840118457a39a5bbbea4` (merged #275) |
| Run | https://cursor.com/agents/bc-85fa10d4-a91c-4459-aa35-96e00514cdd1 |
| Runtime | Cursor Cloud Agent, source `scm`, `privateWorkerId` null, `usePrivateWorker` false |
| Reachable self-hosted workers | 0 (`list-self-hosted-workers`, scope all, totalCount 0). No historical roster was used. |
| Task helpers | None. The two-helper cap was not used. No nested fan-out. |
| Shell | This cloud VM. It is not a Dylan self-hosted or local worker. |

This session did not author Math-#277 or Math-#278. Its id is not either proposal session.

Proposal exposure during this read: both historical `.lean.txt` files were read in full, together with their notes' authorship lines, `MomentGenerality.lean`, `MOMENT_GENERALITY.md`, the new `SCOPE.md` section, retained `MomentTail.lean`, and the `weightedLaw` / `p02_lm008_probability_transfer` declarations those proofs call.

### Lineage, as authenticated

| Contribution | What this session can authenticate |
|---|---|
| Executable adaptation on #279 | OpenAI / GPT-6 Astra Pro, session `lean-moment-generality-20261005`, as credited by the frozen source header and PR body. This reviewer is not that session. |
| #278 agent7, head `cf58e5b812699cd7016441c0b477b86fecb7017f` | Cursor cloud run `bc-368b4374-1a7c-5a78-b7b6-ed5ee50532d8`, source `sand`, model `grok-4.7-high-fast`, `privateWorkerId` null. Same provider, family, and model slug as this reviewer. Different session. Metadata only; the transcript was not read. |
| #277 agent6, head `d1267a6106e8180eeb75fa008ce09de9ad8065ca` | Role label "Grok Bot agent 6" only. Not present among the 7 accessible cloud agents in this environment created on or after 2026-10-05. Underlying provider **UNKNOWN**. Not inferred from the role label. |
| Prior 36-target read #276 | Different session `bc-7023823a-e5a0-4485-abde-ef11860647cb`, also `grok-4.7-high-fast`. Its JSON is not reused. |

A new session does not create cross-provider independence. #278 is an authenticated same-provider, same-family, same-model proposal. #277's unknown provider is not independence. The gate compares a review's `author` object with its `reviewer` object. Recording the OpenAI implementer as author and this xAI session as reviewer would pass that string check and erase the proposal-author exposure. No 40-target `alignment.json` is published for that reason. Same-account organizational-independence credit stays 0.

## Scope actually checked

At the frozen head, compared with the proposals and the retained sources:

- the four declarations in `formal/ResearchFormalCoreR1/MomentGenerality.lean`
- `formal/MOMENT_GENERALITY.md` and the new generality section of `formal/SCOPE.md`
- call targets in byte-identical `MomentTail.lean`: `p02_lm009_markov_event`, `p02_lm009_badJet_subset`, `p02_lm009_moment40_weighted_r3`, and the original `p02_lm009_moment40_tail` / `p02_lm009_moment40_family_r3` types
- `weightedLaw` and `p02_lm008_probability_transfer` in byte-identical `WeightedLaw.lean`, for the lower-normalizer direction and the weight quotient
- manifest target prefix, the two-line `test_moment_tail.py` inventory edit, the new 12 tests, and the unchanged gate
- local source-gate and Python suite results below

Whitespace-normalized theorem tokens, comments removed:

- `p02_lm009_moment40_tail_finite` matches the #277 text.
- `p02_lm009_moment40_tail_of_finite` matches the #277 text.
- `p02_lm009_moment40_family_r3_interval` matches the #278 text, including `letI` inside the `r` case.
- `p02_lm009_moment40_family_r3_of_interval` keeps the #278 type. The proof is the disclosed simplification `⟨inferInstance, hdata r hr hrr0⟩` in place of the proposal's nested projections.

Not checked, and not claimed:

- a local `lake` build, `leanchecker` replay, elaborated-type dump, or axiom audit
- a completed hosted receipt for this 40-target head
- re-derivation of the earlier 29 proofs
- re-opening the pinned mathlib file for `mul_meas_ge_le_integral_of_nonneg` (the local Markov wrapper is the byte-identical theorem #276 cited)
- any concrete Gaussian, Palm, supremum, lower-normalizer estimate, uniformity theorem, good-event complement, P0.2 statement, or parent persistence closure

## Pins checked at this head

| Path | SHA-256 | Claim |
|---|---|---|
| `formal/ResearchFormalCoreR1/MomentGenerality.lean` | `fdec55f1602938cd8fdb5b71535962e76a9671bf230dea53868b14147fb3b509` | match |
| `formal/manifest.json` | `74c5a33861e282ef8432084f3cae0a9493e0d2273a1e8424d4571eddd8adcb54` | match |
| `formal/SCOPE.md` | `198bbc6c60fdb9148ae21c0f25b52d3b612de20c373dc1e6df818767987da452` | match |
| `formal/ResearchFormalCoreR1/MomentTail.lean` | `87fe3ee90afc52d8c2652881f1ae195d1b0b15a2ffc18c84d6166d1a4d0de2aa` | identical to base and to the #276 pin |
| `formal/ResearchFormalCoreR1/WeightedLaw.lean` | `f31dfd2cd048cc0c0446c54c46d89c9cdd5d7bb9d76e9d8d16b7c034f351d736` | identical to base and to the #276 pin |
| `formal/ResearchFormalCoreR1/MeasureBridge.lean` | `28ac130db490c3c3e2fbfabf3ac5be43c854ab1468bf573bf5a8c0dd2c50955f` | identical to base |
| `formal/ResearchFormalCoreR1/ProbabilityCompanionsV2.lean` | `338452a0c2ba24d016059354d543cc995b8cb29c9d4a41d98bb93499f5f8cb8f` | identical to base |
| `formal/ResearchFormalCoreR1/AlgebraV2.lean` | `4480708263c40a2f7f03f12ef7e15f0eb4f8193c2dccbb253921a7ec251863c3` | identical to base |
| `formal/gate.py` | `4f14a78bbc6e9b7f929648b13ad3a9ae467256db4be9792e3667680e697a5c94` | identical to base |
| `formal/lean-toolchain` | `d5edba4e4b8faad9c1baeadb265716d20d03be4d1a2647dc5e35b0c0325bea7b` | identical to base |
| `formal/lake-manifest.json` | `d63753befccc21923783a5085148e3ff028d97134ea52f5a08bd87ecf1b0b043` | identical to base; mathlib revision unchanged |

`git diff --name-only a44db48f10ea27c93595840118457a39a5bbbea4 HEAD` is exactly the eight packaging paths: `MOMENT_GENERALITY.md`, `README.md`, `ResearchFormalCoreR1.lean`, `MomentGenerality.lean`, `SCOPE.md`, `manifest.json`, `tests/test_moment_generality.py`, and `tests/test_moment_tail.py`. `.github/workflows/formal-lean.yml` has an empty diff. `MomentTail.lean` has the same git blob at #276's reviewed head `7206526ed53f7539838711ee45257a13b4b07e99` and at this head: `c8282f297ac22c25d68e94a5e432c2633bac0bab`.

Manifest: 36-target prefix equals the base list; four new names are the four declarations, in source order; `dependency_revisions` unchanged; `formalization_status` remains `proved`; `alignment_status` remains `PENDING_INDEPENDENT_REVIEW`; `scientific_effect` remains `NONE`. Disk hashes match the manifest. `python3 -B -S formal/gate.py` printed `SOURCE_IDENTITY_PASS` for `74c5a33861e282ef8432084f3cae0a9493e0d2273a1e8424d4571eddd8adcb54` and exited 0. That command does not run Lean.

The #276 record's manifest `ddaa37078805089b57a81f302c069fba7411a23af047c49fd3a4d2897b545e59` and scope `21c4ce34ff1e7536c88de86661c796a0751ad8572b034650631052ad0791f4a1` do not match this tree. That JSON was not copied or retitled as 40 targets.

## Local Python evidence

`python3 -B -S -m unittest discover -s formal/tests` and the same command with `-O` each ran **86** tests and passed. `test_moment_generality.py` is 12 of those, and its grid counter reaches 729. These are standard-library source and finite-model checks. They are not a Lean kernel run and not the hosted workflow.

## Hosted execution at publication

[Run 37334385439](https://github.com/d6g8k5htny-coder/Math-/actions/runs/37334385439) was still **in progress** on head `f6672c1a77d67b6257c43acaf5a4481b28fd87e0` at publication. `downstream-replay` had completed with success. `formal / formal-evidence` had no conclusion. No receipt, elaborated-type log, axiom report, or negative-control result for this head was downloaded. The earlier 36-target receipt on run 37316631037 is not rebound here. Success of the replay job is not kernel evidence.

## Findings

No blocker and no amend.

### MG-A1 — finite mass versus unit mass — no-finding

`p02_lm009_moment40_tail_finite` assumes `[IsFiniteMeasure μ]`. The conclusion is `(μ (badJetEvent R r ε)).toReal ≤ (M / ε ^ 8) * r ^ 8`. The proof calls `p02_lm009_markov_event`, whose instance is already finite measure, then divides by the positive threshold `(ε / r) ^ 8`. There is no hypothesis `μ(Ω) = 1` and no quotient by total mass. `IsFiniteMeasure` includes the zero measure and finite measures of mass greater than one. The probability theorem `p02_lm009_moment40_tail` is still present and unchanged in `MomentTail.lean`.

### MG-A2 — no extra division by total measure — no-finding

The calc is the retained chain `(μ A).toReal ≤ (∫ R ^ 40) / (ε / r) ^ 8 ≤ M / (ε / r) ^ 8 = (M / ε ^ 8) * r ^ 8`, closed by `field_simp [ne_of_gt hr, ne_of_gt hε]`. The specialization `p02_lm009_moment40_tail_of_finite` is one application of that theorem. It does not insert a division by one. The weighted theorems still divide by `∫ W` under `cZ * r ^ 2 ≤ ∫ W`; that quotient is the weight normalizer in unchanged `p02_lm008_probability_transfer`, not a normalization of the unweighted finite-measure tail.

`test_no_extra_total_mass_normalization` uses one atom of mass 2 at `R = 2`, `r = 1`, `ε = 30`. The event holds because `30 < 32`, the mass is 2, and half the Markov bound is too small for that mass. `test_mass_scaling` checks that event mass, moment, and bound scale together for scales 0, 1/2, 2, and 7.

### MG-A3 — integrability versus a totalized integral — no-finding

Both new tail declarations take `Integrable (fun x => R x ^ 40) μ` and pass it to `p02_lm009_markov_event`. Nonnegativity of `R ^ 40` is proved everywhere and supplied as an almost-everywhere fact. The module has no `∫⁻`. `0 ≤ M` is not added to the unweighted tail; it remains a hypothesis of the family theorems, where the square root is formed. This matches the proposal and the unchanged probability tail.

### MG-A4 — zero, signed, strict, and null edges — no-finding

The event stays `badJetEvent`, defined as `{x | ε < r * R x ^ 5}` in the unchanged module. The subset step is the unchanged `p02_lm009_badJet_subset`, which keeps equality out of the event and does not require a sign on `R`. The 729-case grid uses totals 0, 1/2, and 2, values in `{-2, 0, 2}`, and positive `(r, ε)` pairs: `3 * 3^3 * 3 * 3 = 729`. A separate case puts mass 2 at `R = 1` and mass 1 at `R = -1` outside the strict event `ε = r = 1`, and a null atom at `R = 100` inside the predicate with contribution 0. The zero measure with values `-10` and `100` gives event mass, moment, and bound all 0. These are finite rational models of the stated bound, not a kernel proof.

### MG-A5 — local probability instance — no-finding

`p02_lm009_moment40_family_r3_interval` has no `[∀ r, IsProbabilityMeasure (μ r)]` binder. `IsProbabilityMeasure (μ r)` is a conjunct of `hdata`, quantified only for `0 < r ≤ r0`. The proof introduces `letI` after destructuring that conjunct and before the call to `p02_lm009_moment40_weighted_r3`, which still requires a probability instance. The global binder `[∀ r, IsProbabilityMeasure (μ r)]` occurs only on `p02_lm009_moment40_family_r3_of_interval`, the specialization that recovers the old interface. Outside `0 < r ≤ r0`, the interval theorem states no probability instance and no bound. The finite-model test uses the zero measure for `r ∈ {-1, 0, 2}` when `r0 = 1`, and does not demand a conclusion there.

### MG-A6 — lower normalizer and the fixed constant — no-finding

`hdata` carries `cZ * r ^ 2 ≤ ∫ W r`, the same direction as `hlower` on `p02_lm009_moment40_weighted_r3` and on `p02_lm008_probability_transfer`. In the unchanged transfer proof, that inequality is used to obtain `0 < ∫ W` from `0 < cZ` and `0 < r`. It is not an upper bound and it is not proved from a field model.

The family witness is chosen before `intro r`:

`(Real.sqrt cW / cZ) * Real.sqrt (M / ε ^ 8)`.

`ε`, `M`, `cW`, `cZ`, and `r0` are parameters outside `∀ r`. The proof then uses `hrr0.trans hr0.2` for the retained `r ≤ 1` hypothesis of the cubic theorem. `test_r_dependent_coefficient_is_not_uniform` shows a pointwise identity `r ^ (-4) * r ^ 4 = 1` whose cubic ratios `1 / r ^ 3` grow. No theorem says every `r`-dependent constant is uniform.

### MG-A7 — specialization bridges — no-finding

`p02_lm009_moment40_tail_of_finite` is the probability statement applied to the finite-measure theorem. Elaboration of `IsProbabilityMeasure` to `IsFiniteMeasure` is the standard instance path and was not re-run in Lean here.

`p02_lm009_moment40_family_r3_of_interval` passes `⟨inferInstance, hdata r hr hrr0⟩`. The expected conjunct is `IsProbabilityMeasure (μ r) ∧` followed by the seven-conjunct package that `hdata` already returns. `And` has two fields, so the second field is that whole conjunction. This is the same type as the #278 projection tower. It does not add a conclusion. The interval theorem still concludes only `IsProbabilityMeasure (weightedLaw (μ r) (W r))` and the cubic bound on `0 < r ≤ r0`.

### MG-B1 — predecessor bytes and the inventory edit — no-finding

The five predecessor Lean modules, `gate.py`, the toolchain, the lockfile, and `formal-lean.yml` match the base blobs above. The moment-tail inventory test changes two lines: `targets[29:]` with length 36 becomes `targets[29:36]` with length at least 36. The seven names at that slice are unchanged. `test_moment_generality.py` binds `targets[36:]` to the four new names and `len(targets) == 40`. The unchanged gate requires the declaration list to equal `targets`. `README.md` now says the execute path audits 40 declarations; `gate.py` still takes that count from the manifest rather than from a hardcoded 36.

### MG-B2 — hosted 40-target kernel evidence — not observed

Run 37334385439 had not finished when this review was written. `downstream-replay` had succeeded; `formal / formal-evidence` had not concluded. No axiom report, type log, or negative-control result for the four new names is claimed. `alignment_status` stays `PENDING_INDEPENDENT_REVIEW`.

## Carry-forward of the earlier 36

The 36 names are the prefix of this manifest. Their five modules, the gate, the formal workflow, and the mathlib pin match the bytes #276 recorded at `7206526ed53f7539838711ee45257a13b4b07e99`. This session re-read `MomentTail.lean` and the weighted-law declarations the new proofs call. It does not re-derive the earlier 29 proofs. The #276 JSON stays a 36-target record for its own manifest and scope. It is not a 40-target acceptance.

## Why no alignment record was validated

`python formal/gate.py --alignment` accepts only `disposition = ACCEPTED`, full target coverage, current manifest and scope digests, and author/reviewer provider, family, and agent strings that all differ. A record that names OpenAI as author and this session as reviewer would pass those string checks. It would not preserve the authenticated same-provider relationship to #278, or the unknown provider of #277. Partial coverage would also fail the gate. No alignment file is included, and the gate was not pointed at one.

## Boundaries

This scoped PASS is a statement comparison for the four new declarations and a byte check of the retained proof modules and execution controls. It is not scientific acceptance, not a merge, and not a promotion of `lemma_closed` or any premise. Kernel evidence for this head still requires the hosted run's own receipt.
