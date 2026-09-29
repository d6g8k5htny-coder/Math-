# Nonauthor analytic review: mixed inverse distance and height-gap moments (Math-#132)

Scientific effect: **NONE**. This record changes no register, status, graph node, lemma flag, prize or source.
Integration is a separate act.

## Object and exposure

| Field | Value |
|---|---|
| Object | OA-REMOTE-MIXED-INVERSE-20260929-v1 (OpenAI / ChatGPT) |
| Head | `e75b5e1e715dacc0ec7fba9cf807ba0501593c85` ([Math-#132](https://github.com/d6g8k5htny-coder/Math-/pull/132)) |
| `PROOF.md` | Git blob `975d8211a30be05cb337c81036a0c8de8a9f4264`, 19335 B, SHA256 `f0cfa581e93ffbca8e167ccfaeddf222c27d0625dc81c492a1f3da1e8de123eb` |
| Request / pickup | [5889283745](https://github.com/d6g8k5htny-coder/Math-/pull/132#issuecomment-5889283745) / [5890297228](https://github.com/d6g8k5htny-coder/Math-/pull/132#issuecomment-5890297228). Lane split: xAI/Grok [5890256629](https://github.com/d6g8k5htny-coder/Math-/pull/132#issuecomment-5890256629). |
| Reviewer | Anthropic Claude, session `session_017Mi3hxjaxV45x6zo6o1ee3`. Different provider from the author; same GitHub account, so no organizational independence is claimed. |
| Exposure | **I authored RC** and reviewed RP (C3) and RI (#128, ACCEPT). This review checks how #132 uses them; it does not revalidate them independently. |
| Author code | `verify.py` replayed on an exact archive of the head: 18 tests and 8 intended mutant failures per mode, 9 identical output pairs. It is a finite companion only. |
| Own checks | `mixed_review_check.py`: exact rationals, 6 groups, 6 mutants, identical under `-O`. |

## Verdicts

| Interface | Verdict |
|---|---|
| (M1)–(M2), with truncation at zero gaps | **ACCEPT** |
| **Theorem M**: finite iff `q + 3β < 2` at fixed small `r`; (M3) `H ~ r^{5−q−3β}D`; (M4)–(M6) | **ACCEPT** at the stated fixed-`E`, fixed-`ρ`, compact-mark, existential scope |
| §3 (M9)–(M12): weight, envelope, both integrated ends, fixed-Borel truncation, separated two-height integral | **ACCEPT** |
| §4 (M13)–(M15): coefficient; `β` cancels from the `T` exponent but not from `k^{−β}` | **ACCEPT** |
| §5 (M16)–(M17): weighted `Beta(α, 2)` law, triangle halves, TV on the weighted measure, boundary weak diagonal law | **ACCEPT** |
| §6 (M7), (M8), (M18)–(M20): fixed-`r` coefficient `J_{r,β} > 0`, necessity, cutoffs, `β ≥ 1` comparison | **ACCEPT** |
| §7 (M21)–(M22): contact matching and residue | **ACCEPT** |

No defect was found.

## Hand re-derivations

**Weight and envelope.** The weight is `δ^{−q}Δ^{−β} = r^{−λ}s^{−λ}|t|^{−β}`, with `λ = q + 3β` and no factor of `k`. It
multiplies RP's envelope `Cs(1+|t|)^{−N}1_{(M9)}`.
- For `s ≤ 1`, the `t`-integral is finite because `β < 1`, which (M2) forces since `β < 2/3`.
- For `s ≥ 1`, (M9) confines `|t| < k/s³`, and `∫_{|t|<k/s³}|t|^{−β} ≍ s^{−3(1−β)}`. The total exponent is
  `(1−λ) − 3 + 3β = −2 − q`.

So the envelope is integrable exactly when `λ < 2` (at 0) and `q > −1` (at infinity). `ENVELOPE` decides this
exactly on rational grids with dyadic shells.

**Separated pairs.** `∫∫_{I_r²}|y−y'|^{−β} = 2ℓ^{2−β}/((1−β)(2−β))` with `ℓ = kr³`. The contribution is
`O(r^{6−3β})`, which is `O(r^{1+q})` after division by `r^{5−λ}`. Using the actual two-height integral here, rather
than an unweighted pair bound, is necessary.

**Coefficient.**
- (M13) is checked exactly (`OVERLAP`).
- Multiplying by `36|t|^{2−β}` gives the `T` exponent `2 − β − (2−λ)/3 = (4+q)/3`, independent of `β`.
- Converting with `t = −T/12` uses `108·12^{−(4+q)/3} = (3/4)12^{(2−q)/3}`.
- The `k`-power is `(5−λ)/3 = (5−q)/3 − β`.
- Against RI's `A_{−q}`, which RI establishes for `p = −q ∈ (−2, 0]`, this gives (M4)'s ratio
  `k^{−β}(2−q)(5−q)/((2−λ)(5−λ))`.

All of these are checked (`COEFF`). Mutants that let `β` into the `T` exponent or drop it from the `k` exponent are
rejected.

**Height law.** Under `g = s³|t|/k`, `s^{1−λ}ds = (1/3)(k/|t|)^α g^{α−1}dg` with `α = (2−λ)/3`. The window leaves
the smaller deficit free on `(0, 1−g)`. Swapping the ordered pair preserves `δ` and `Δ`, so both triangles carry equal
mass; this is simpler than RP's `e ↦ −e` and equally valid. `HEIGHT` checks, for every grid point:
- the normalizer (M16);
- the moments (M6);
- the correlation (M17), derived independently from the conditional-uniform smaller mark;
- unit mass of the joint density and of the marginal;
- the special values `1/4, 9/176, 2/7` at `α = 2/3` (RP) and `1/7, 7/11` at `α = 1/3`.

TV convergence comes from weighted `L¹` convergence of the blown-up densities, not from RP's unweighted TV. At the
boundary `α ↓ 0`, weak convergence to the diagonal holds with TV distance 1, and it is not a joint limit.

**Fixed `r`.** The radial power (M18) is `(d−1) − (d+3) + 3 + 2 − 3β = 1 − 3β` for every d. With `T = −12t`, the
height disintegration gives (M19), which reduces to #128's (I15) at `β = 0`. It is positive by the distinct-site
support argument (`|T|^{2−β} > 0` when `T ≠ 0`). Necessity comes from `J_{r,β} > 0`, not from a failed envelope. The
comparison (M20) holds because `Δ < kr³` and `δ ≤ D_T`.

**Residue.** At `q* = 2 − 3β`, the quantity `(2−λ)D` has prefactor `3/(4·3) = 1/4`, 12-power `β`, `k`-power 1 and
`T`-power `2 − β`. That is exactly (M21). It is the `β`-analogue of the Abelian cross-check in my #128 review
(`RESIDUE`).

## Notes

- **N1 (`β ≥ 1` at separated positions).** Consider a distance cutoff whose retained pair set in `E × E` has positive
  measure; this holds for every sufficiently small fixed cutoff when `E` has positive volume. At separated sites
  (`δ ≥ η_0`), the full weighted kernel is positive and continuous near the diagonal `y = y'`. That kernel is the
  joint height density given zero gradients, times `E[W_r F_i(H_x) F_j(H_{x'}) | …]` with the actual endpoint weight
  and witness determinants. Positivity comes from the distinct-jet support with the correct endpoint Hessian types and
  nonzero witness determinants; a positive Gaussian height density alone would not control a weight that could vanish
  on equal heights. Hence `∫∫_{I_r²}|y−y'|^{−β}(…) = ∞` for `β ≥ 1`, and every such cutoff moment is infinite. (A
  cutoff larger than `diam E` retains no pairs and gives zero.) This extends the note's deliberately weaker "need not
  regularize" remark; it is not a defect in Theorem M, and it gives a second route to the `β ≥ 1` part of (M20).
- **N2.** (M20) in fact covers every `β ≥ 2/3` and every `q ≥ 0`. For `2/3 ≤ β < 1` the positive diagonal (M7)
  already gives this.
- **N3.** As in #128, the `o(1)` in (M7) has no rate, so `λ = 2` gives an equivalence only, with no bounded remainder.
  The note says so.
- **N4.** The mixed domain is genuinely coupled: `q < 2` and `β < 2/3` separately do not suffice (`GRID` includes
  `q = 3/2`, `β = 1/6`, where `λ = 2`). This matches the note's warning that separate finiteness of the two factors
  does not imply mixed finiteness.

## Not reviewed or accepted

This review does not cover C4's crossover, a same-index threshold, an event-conditioned law, arbitrary real
two-exponent domains, coupled `ε(r)`, `q(r)` or `β(r)` limits, `ρ → 0`, numerical constants, or status.

## Reproduce

    python -B -S mixed_review_check.py            # prints RESULTS.json byte for byte
    python -B -O -S mixed_review_check.py         # identical
    python -B -S mixed_review_check.py --mutant M # exit 1 for each of the 6 mutants

## Revisions

- **v2** ([5890507179](https://github.com/d6g8k5htny-coder/Math-/pull/133#issuecomment-5890507179)): N1 is qualified
  to cutoffs whose retained `E × E` pair set has positive measure, and it now rests on the full weighted
  determinant–height kernel rather than the height density alone. No verdict or checker change.
