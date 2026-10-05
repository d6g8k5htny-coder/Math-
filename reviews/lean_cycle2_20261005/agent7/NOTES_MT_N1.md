# L7 / MT-N1 — interval-only family formulation

**Status:** UNCOMPILED proposal (`.lean.txt`). Scientific effect **NONE**.
**Worker:** Grok Bot agent 7 (Grok Bot support agent; non-Claude, nonauthor lane)
**Pickup:** main#229 [5996231433](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5996231433)
**Readback:** [5996234080](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5996234080)
**Ask:** [5995761095](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5995761095)
**CoS route:** [5996179903](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5996179903)
**Frozen head used:** `7206526ed53f7539838711ee45257a13b4b07e99` (Math-#275 live head)
**Alignment note:** #276 REVIEW.md §MT-N1 at
`reviews/moment_tail_alignment_20261005/REVIEW.md`
(REVIEW commit `0cb17c1b836651144486d55788eef8d7cf532081`,
record tip `3718fc1564c537971636a3f4091224964e20f9f9`)

## What changed (proposal only)

| Item | Accepted (frozen) | L7 companion |
|---|---|---|
| Name | `p02_lm009_moment40_family_r3` | `p02_lm009_moment40_family_r3_interval` (new) |
| Probability instance | `[∀ r, IsProbabilityMeasure (μ r)]` for **all** `ℝ` | `IsProbabilityMeasure (μ r)` **inside** `hdata` for each `0 < r ≤ r0` only |
| Fixed outside `r` | `M, cW, cZ, ε, r0`, witness `C` | **exact same** |
| Conclusion | `∃ C, ∀ r ∈ (0,r0], weighted cubic ≤ C r³` | **exact same shape** |
| Proof body | call `p02_lm009_moment40_weighted_r3` per `r` | same call, with `letI` from the per-`r` hypothesis |

No edit/rename of the accepted theorem. No unweighted/finite-measure theorems
(MT-N2 is agent6). No formal-source / manifest / workflow edits on this lane.

## Why this is a real relaxation (not wording)

The frozen family type carries a section/instance binder

`[∀ (r : Real), IsProbabilityMeasure (μ r)]`

that is elaborated for every real `r`, including values outside `(0, r0]`.
The bound premises (`hdata`) and the conclusion quantify only over
`0 < r ≤ r0`. No step of the proof uses probability for an out-of-interval
`r`. Requiring a global instance therefore excludes families that are
probability measures on the working interval but arbitrary (e.g. zero)
elsewhere — a strictly stronger hypothesis than the stated analytic scope in
`MOMENT_TAIL.md` / MT-N1.

The L7 companion moves the probability requirement into `hdata`'s quantified
case. `M, cW, cZ, ε` and the witness `C` remain parameters **outside** `r`
(no per-`r` constant; no new uniformity premise).

## Outside-interval zero-measure test (why the relaxation is real)

Fix any `r0 ∈ (0,1]`, and define a family `μ : ℝ → Measure Ω` by:

- for `0 < r ≤ r0`: `μ r` is any probability measure satisfying the usual
  `hdata` package (e.g. a Dirac probability used in frozen finite models);
- for every other real `r` (including `r ≤ 0` and `r > r0`): `μ r = 0`
  (the zero measure).

**Under the accepted theorem type:** the instance
`[∀ r, IsProbabilityMeasure (μ r)]` **fails**, because the zero measure is
not a probability measure (`μ(Ω) = 0 ≠ 1`). The family cannot even be fed to
`p02_lm009_moment40_family_r3`, despite agreeing with every in-interval
hypothesis and conclusion obligation.

**Under the L7 companion:** `hdata` only asks for `IsProbabilityMeasure (μ r)`
when `0 < r ≤ r0`. Outside that interval the zero measure is allowed; the
existential `C` and the in-interval cubic bound are unchanged. Therefore the
companion admits a model the frozen type rejects — a real relaxation, not a
rewording of the same type.

(This test is analytic / type-theoretic. It is **not** a Lean kernel run of
the companion. Zero measure outside the interval is also the explicit L7 ask
in 5995761095.)

## Compile / toolchain honesty

| Probe | Result |
|---|---|
| `elan` | 4.2.4 present on box |
| default toolchain | **NONE configured** (`lean`/`lake` error: no default toolchain) |
| Hosted #275 Lean (for context only) | 4.34.1 / mathlib `d13f23b7…` on frozen CI — **not** a kernel receipt for this companion |
| Local kernel build of companion | **NOT RUN** |
| Unrelated green CI | Must **not** be cited as kernel evidence for this proposal |

**Verdict for integrator:** treat as **UNCOMPILED** `.lean.txt`. Register/audit
only after source review and a real kernel execution on an authorized formal
path. Proof-containing text ≠ accepted Lean.

## Out of scope (respected)

- formal-source / manifest / workflow edits
- merges; flag flips (`lemma_closed`, `prizes_solved`, `discharges_OBL_H5_JETMOD`,
  `certified_C_H`, freeze, `inventable_attempt_accepted`)
- MT-N2 finite-measure unweighted companion (agent6)
- SoT / scientific-status invention; OBL stays OPEN

## Files in this directory

- `MomentTail_family_interval_MT_N1.lean.txt` — proposed companion (UNCOMPILED)
- `NOTES_MT_N1.md` — this file
- `BUILD_STATUS.md` — compact compile status receipt
