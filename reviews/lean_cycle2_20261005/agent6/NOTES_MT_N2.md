# L6 / MT-N2 — finite-measure 40th-moment tail companion

**Status:** UNCOMPILED proposal (`.lean.txt`). Scientific effect **NONE**.
**Worker:** Grok Bot agent 6 (Grok Bot support agent; non-Claude, nonauthor lane)
**Pickup:** main#229 [5996213216](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5996213216)
**Readback:** [5996215908](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5996215908)
**Ask:** [5995761095](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5995761095)
**Frozen head used:** `7206526ed53f7539838711ee45257a13b4b07e99` (Math-#275 live head)
**Alignment note:** #276 REVIEW.md §MT-N2 at `reviews/moment_tail_alignment_20261005/` (head `3718fc1564c537971636a3f4091224964e20f9f9`)

## What changed (proposal only)

| Item | Accepted (frozen) | L6 companion |
|---|---|---|
| Name | `p02_lm009_moment40_tail` | `p02_lm009_moment40_tail_finite` (new) |
| Measure hypothesis | `[IsProbabilityMeasure μ]` | `[IsFiniteMeasure μ]` |
| Constant | `(M / ε ^ 8) * r ^ 8` | **exact same** |
| Integrable premise | `Integrable (fun x => R x ^ 40) μ` | **exact same** |
| Proof body | Markov via `p02_lm009_markov_event` + field_simp | **same steps** (that lemma already needs finite measure) |

No edit/rename of the accepted theorem. No weighted/family theorems. No formal-source / manifest / workflow edits on this lane.

## Why this is a real relaxation (not wording)

`p02_lm009_markov_event` already assumes `[IsFiniteMeasure μ]`. The unweighted tail proof never uses `μ(Ω) = 1`, renormalization, or any probability-only identity. Requiring `IsProbabilityMeasure` therefore excludes legitimate finite measures of mass ≠ 1 that still satisfy the same Markov arithmetic.

## Explicit finite-measure checks (analytic / finite-model; not Lean kernel)

### Mass = 2

Ω = {*}, μ = 2 · Dirac(*), R(*) = 2, r = ε = 1.
badJetEvent = Ω, μ(A) = 2. ∫ R^40 dμ = 2 · 2^40. With M = ∫, RHS = M. Markov at threshold (ε/r)^8 = 1 gives μ(A) ≤ ∫ = 2·2^40 (true). Mass-2 scales both sides; probability instance not required.

### Mass = 1/2

Same singleton, μ = (1/2) · Dirac(*), R(*) = 2, r = ε = 1.
μ(A) = 1/2, ∫ R^40 = (1/2)·2^40. With M = ∫, RHS = M ≥ μ(A). Finite-measure Markov applies; no μ(Ω) normalization.

### Strict event / boundary

badJetEvent is `{ε < r R^5}` (strict). Equality ε = r R^5 is outside the event. Subset weakens to ≤ on the 40th-power threshold. Matches frozen `test_strict_boundary_and_signed_jet`.

### Zero / null cases

- Empty A ⇒ μ(A)=0 ≤ RHS whenever hypotheses hold.
- Null sets do not affect Bochner ∫ or a.e. nonnegativity of R^40.
- Zero measure μ ≡ 0 is finite: both sides 0 when Integrable and M ≥ 0.

### Signed R

On the event, R^5 > ε/r > 0. R^40 ≥ 0 globally. No global sign hypothesis.

## Compile / toolchain honesty

| Probe | Result |
|---|---|
| Lean on box | 4.34.1 (`5045d005…`) |
| mathlib pin | `d13f23b723b8…` |
| Shared mathlib oleans | **0** |
| lake build of companion | **NOT EXECUTED** |

**Verdict:** UNCOMPILED `.lean.txt`. Proof-containing text ≠ accepted Lean. Do not cite #275 CI as kernel evidence for this companion.

## Out of scope (respected)

formal-source / manifest / workflow edits; merges; flag flips; weighted/family (L7); SoT invention; OBL stays OPEN.

## Files

- `MomentTail_finite_MT_N2.lean.txt` — proposed companion (UNCOMPILED)
- `NOTES_MT_N2.md` — this file
- `BUILD_STATUS.md` — compact compile status receipt
