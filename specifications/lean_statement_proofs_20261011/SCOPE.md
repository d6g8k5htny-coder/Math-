# Scope of the proof packet

Scientific effect: **NONE**. Scientific status authority: none. Alignment status of every registered
statement proved here: **PENDING_INDEPENDENT_REVIEW**. Organizational-independence credit: 0.

## In scope

* Theorems whose type is exactly a registered `def … : Prop` of
  `specifications/lean_statements_20261010/REGISTER.json`, applied to the theorem's own parameters,
  with proofs the Lean kernel accepts under `propext`, `Classical.choice` and `Quot.sound` only.
* Helper lemmas and definitions needed by those proofs, `private` or under an `Aux` namespace, never
  counted as inventory and audited for axioms like everything else.
* The gate (`check.py`), its tests, the replay script and the CI workflow that produce a run receipt.

## Out of scope (and refused by the gate where it can see them)

* Editing any statement module or the register. A proof that needs a statement changed, or an extra
  hypothesis to go through, is a **finding** about the statement: report it; do not smuggle the
  premise into the theorem (`theorem foo (h : …) : P` and `theorem foo : P → P` are refused), do not
  narrow the statement (`theorem foo (n : ℕ) : P (n + 1)` is refused).
* Any proof of an informal claim as such. The register's claim-level `formal_progress` stays what the
  register says (`none` or `specified`); no research claim of this programme is `proved`.
* Alignment verdicts (ALIGNED / ALIGNED AT NARROWER SCOPE / MISALIGNED): written only by an
  independent reviewer, never here.
* Transcribed LANDING_CLAIMS dispositions: never re-derived or changed.
* The vault, `legacy/`, `quarantine/` material, and anything under
  `02_LEGACY_Q0_ARCHIVE`: not cited, not used.

## What a kernel-checked theorem here means, per family

| family | the theorems establish | not established |
|---|---|---|
| P15 (`Specifications.P15`, modules P15Elementary, P15Structure, P15Hazard, P15Covers, P15Budget, P15Interpolation) | exact finite arithmetic and finite combinatorics of the registered Props: generator prices, the demand-one refutation data, `ρ* < 6/7` and its certificate, the 816-benchmark counts, palette identities, cover (816 and not 815) and union bound (P11); Proposition P1; both halves of Theorem P2 as the Props state them (the cover criterion (P7) and the hazard bound (P8) for prices `0 ≤ c_v ≤ p_v`) with the local statements (P2)-(P5); the restricted transformed-price budget (T1) with (T4), (T5) and the six-block transformed range; (F9), (F13), the sharpness clause of `ρ*` for the triple block; the hazard interpolation (F5)-(F8) (separate coordinatewise concavity of `t ↦ -log μ_{p(t)}(A)` for a proper downset, the product bound, the `φ` bound, the full-ground price bound and its exactness `iff`), the local bound (F12), Theorem F as `FullTransformedPriceBudget` states it ((F2): for every `p ∈ [0,1]^X`, every `0 ≤ c_v ≤ φ(p_v)` and `K ≥ K_H(d)`, `coverCost ≤ cappedHazard ρ* μ`) and the 20-digit enclosure (F3) of `ρ*`; all for the formal `RealizedData` record, downset, `coverCost` (an `sInf`) and `mu` | the informal P15 claims (P15-PRICE-BOUNDARY, P15-REALIZED-COVERS, FULL-PRICE, PRICE-BUDGET), their dispositions, Theorem F itself: the hazard interpolation (F4)-(F8), the block bound (F12) and the budget (F2), the 20-digit `ρ*` enclosure (F3); attainment of the `sInf`; alignment of `RealizedData`/`IsRealizedFamily`/`downset`/`coverCost`/`mu` with the informal objects (PENDING_INDEPENDENT_REVIEW), any prize statement |
| Side24 (`Specifications.Side24`) | elementary exponential bounds, a term-ratio bound, the D2 cone-moment algebra, the reference-coefficient identity, the elementary cone integral, as the Props state them | the coefficient enclosure `c_{d,24}` (REVIEWED_SCOPED is transcribed, not derived), the Gaussian-moment and derivative-bound statements, the lattice image sum over a `tsum`, the interface-level statements |
| RN (`Specifications.RN`) | the elementary probability identities and bounds N1–N5 as the Props state them, for the interface objects they quantify over | the Radon–Nikodym uniformity lemma `D3-LEMMA-RN-UNIF` (OPEN), the five validity premises of Theorem D1 v2.2(2) (OPEN), any identification of the interface with the actual field |
| Lifetime, Field | nothing is expected to be provable (interface-level statements); no theorem is inventoried | everything |

The three lines of each theorem's docstring (`Proves:`, `Method:`, `Does not establish:`) are the
per-theorem version of this table and are required by the gate.

## Labels

* Source mode prints `formalization_status: "proved"`: the label of a committed proof package.
* The run receipt prints `formalization_status: "kernel-checked"`: a label that appears only in a
  receipt, about the inventoried theorems, after a fresh build, `leanchecker` and `#print axioms`.
* `alignment_status: "PENDING_INDEPENDENT_REVIEW"` everywhere.
* `scientific_effect: "NONE"`, `scientific_status_authority: false` everywhere.
* A receipt produced with `--allow-dirty` says `worktree: "UNVERIFIED"` and is not evidence about
  any commit.

## Next step

Independent (not same-provider) alignment review of each registered statement against its Layer 0
anchor, recorded in the review lane; nothing in this packet substitutes for it.
