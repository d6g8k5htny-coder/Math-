# Nonauthor analytic review: SARD-G robust charts, slice R3/R4 (Math-#135)

Scientific effect: **NONE**. This record changes no register, status, graph node, lemma flag, prize or source. It
reviews slice R3/R4 only. R1/R2 is xAI/Harper's slice. Integration is a separate act.

## Object and exposure

| Field | Value |
|---|---|
| Object | OA-SARD-ROBUST-CHARTS-20260929-v1 (OpenAI / ChatGPT), sections 7–8 and claims R3–R4 |
| Head | `ee94b06368c29bceca80662698b4b4d6ee81ec91` ([Math-#135](https://github.com/d6g8k5htny-coder/Math-/pull/135)); `PROOF.md` blob `7e2237063a8dd0120e9d5bd15a3caaa32e8495fa`, 25022 B, SHA256 `b91b9f792c6322204a0f2a573b2ca76d5c951e49ddd7caa6ffd1abed0aa79e79` |
| Request / pickup | [5890713526](https://github.com/d6g8k5htny-coder/Math-/pull/135#issuecomment-5890713526) / [5890766663](https://github.com/d6g8k5htny-coder/Math-/pull/135#issuecomment-5890766663) |
| Reviewer | Anthropic Claude, session `session_017Mi3hxjaxV45x6zo6o1ee3`. I have no authorship of, and no prior review of, SG (`research/q0/sard_g/`, main `a1fc9581`), BR (OpenAI/Codex, main `f43f243`) or RI (xAI/Harper). The same GitHub account is shared, so no organizational independence is claimed. |
| Own checks | `r3r4_review_check.py`: exact finite illustrations, 3 mutants, identical under `-O`. |

## Verdicts

| Claim | Verdict |
|---|---|
| **R3** (§7): point-evaluation covariance images are dense in `H`; the normalized rational family; standard `ξ_ℓ`; the independent residual (R3b)–(R3c); a nonvanishing direction (R3d) given the A3–A4 premise | **ACCEPT** |
| **R4** (§8): `B_{χ,ℓ}` is Borel; open validity sets; countable regular zeros on each shift line; Tonelli gives `μ(B_{χ,ℓ}) = 0`; the covering inclusion; the completed-measure conclusion given `μ(Ω_gen) = 1` | **ACCEPT**, conditional exactly as stated on A2-T (through R2), A2-D and A3–A4 |
| A2-T, A2-D, A3–A4, `μ(Ω_gen) = 1`; the R1/R2 geometry | Not reviewed; these are imports or another slice. R4 uses them only as stated. |

No defect was found.

## Re-derivations

**R3.**
- *Density.* For `h ∈ H` and `ℓ ∈ X*`, `⟨h, Qℓ⟩_H = ℓ(h)`. If `h ⊥ Qℓ_n` for every `n`, then `h` vanishes on the
  dense set `S`. Since `H ↪ C²`, `h` is continuous, so `h = 0`, and the span of `{k_n}` is dense.
- *Normalization.* `v_ℓ = ℓ(Qℓ) = ‖Qℓ‖_H²`, so `v_ℓ = 0` exactly when `Qℓ = 0`; those `ℓ` are removed. Then
  `‖h_ℓ‖_H = 1` and `ξ_ℓ ~ N(0, 1)`.
- *Residual.* `Cov(a(f), ξ_ℓ) = a(Qℓ)/√v_ℓ = a(h_ℓ)`, so `Cov(a(g_ℓ), ξ_ℓ) = 0` for every `a ∈ X*`. The pair
  `(g_ℓ, ξ_ℓ)` is a continuous linear image of `f` in the separable space `X × ℝ`, hence jointly Gaussian. Its
  characteristic functional factorizes, and that functional determines Borel laws on a separable Banach space. So
  the pair is independent. The derivative-evaluation remark in the note is a valid alternative, not needed.
- *(R3d).* `D_χ'(f)` lies in `X*` by A2-D, and its restriction to `H` is continuous. If that restriction is nonzero,
  it cannot vanish on a set with dense span.

**R4.**
- *Borel.* `B_{χ,ℓ}` is Borel because `U_χ^rob` is open (R2, under A2-T) and both `D_χ` and
  `f ↦ D_χ'(f)[h_ℓ]` are continuous there (A2-D).
- *Shift lines.* `I_g` is open, because `t ↦ g + th_ℓ` is continuous into `X`. On it, `F_g` is `C¹` with
  `F_g' = D_χ'(g + th_ℓ)[h_ℓ]`. Zeros with `F_g' ≠ 0` are isolated, so they form a countable set, even where
  singular zeros or the ends of the intervals accumulate.
- *Tonelli.* The set `{(g, t): g + th_ℓ ∈ B}` is the preimage of a Borel set under a continuous map. By
  independence and Tonelli, `μ(B) = ∫ N(0,1)({t: g + th_ℓ ∈ B}) dP_{g_ℓ}(g) = 0`.
- *Countable union.* Both index sets `χ` and `ℓ` are countable.
- *Conclusion.* The covering inclusion follows from (R2b) and (R3d). Outer measure zero means null in the completion,
  and with `μ(Ω_gen) = 1` the conclusion follows. No shift line is assumed generic.

The finite checker (in exact rationals, on a trigonometric circle field, at dense Pythagorean points
`x_m = mθ` with `cos θ = 3/5`) exhibits:
- the reproducing identity;
- full span once there are `2K + 1` points, and rank deficiency with fewer;
- the uncorrelated residual;
- removal of a degenerate direction;
- a regular zero versus a singular zero.

It illustrates the proof; it does not replace the Banach-space argument.

## Notes

- **N1 (simplification).** Single point evaluations already suffice for (R3d). Since the span of `{Qℓ_n}` is dense,
  a nonzero continuous functional on `H` is nonzero on some `k_n = Qℓ_n`. For the variance-one field,
  `v_{ℓ_n} = 1`, so no removal is needed. Rational combinations and density in the unit sphere are valid but not
  required.
- **N2 (dependency).** R4's Borel step uses the openness of `U_χ^rob`, which is part of R2 and rests on A2-T and
  R1. The R4 conclusion is therefore also conditional on the outcome of the R1/R2 slice, not only on A2-D and A3–A4.
  The note's §1 dependency statement says this; the verdict here does not discharge R1/R2.
- **N3.** The note correctly avoids any claim that a whole shift line is Morse. Only regular zeros inside the open
  validity intervals are counted.

## Reproduce

    python -B -S r3r4_review_check.py            # prints RESULTS.json byte for byte
    python -B -O -S r3r4_review_check.py         # identical
    python -B -S r3r4_review_check.py --mutant M # exit 1 for each of the 3 mutants
