# Nonauthor review: D5 punctured-pin algebraic skeleton (P9, P17, P20)

Scientific effect: **NONE**. This file does not change `lemma_closed`, prizes,
premises, `STATUS`, `PROOF_INDEX`, `GRAPH`, or any author source. It records
verdicts on exact identities. Continuum Gaussian and Kac–Rice steps remain HOLD.

## Objects

All paths are on Math- `main` at `44345350f2fe70f6c8fbe954741da268300996bd`.

| Object | Path | Role |
|---|---|---|
| Live inner-disk candidate | `reviews/d5_local_collar_20260928/PUNCTURED_PIN_PROOF.md` | Author-side all-height punctured disk (P2) |
| Recorded obstruction | `reviews/d5_pin_microdisk_20260927/NOTE.md` | Nested-axis / 9-pin Gram singularity |
| Finite-r Hermite repair | `reviews/d5_finite_r_hermite_repair_20260925/REPAIR.md` | Longitudinal cubic + quartic relative term |

Reviewer: xAI / Grok team lane (Benjamin). Same GitHub account as every lane;
no organizational independence is claimed. The candidate author is OpenAI.

## Verdicts

| ID | Locus | Verdict |
|---|---|---|
| P4 cubic / quartic | (P4), relative remainder | **ACCEPT** as exact polynomial identities |
| P9 | three minors, Cauchy–Binet floor `9/131072` | **ACCEPT** |
| P17 | angle-free product `O(r^3(p^2+q^2))` | **ACCEPT** as a power identity; coarser than the 20260927 cubic on-axis product |
| Region II ledger | (P20) exponent `-10` then Gaussian absorption | **ACCEPT** the power count; HOLD the exponential and the `C^3` moment |
| Axis compactification | `χ=1/r` on `q=0` | **ACCEPT** |
| Nested disk sits in `D` | `p=rP`, `q=rQ` inside `|p|,|q|≤1/4` for small `r` | **ACCEPT** |
| 20260927 obstruction | nested axis | **Addressed as an algebraic device** by `Δ` plus (P17); not a theorem promotion |
| (P2) count lemma | all-height punctured disk | **HOLD** (needs Gaussian density (P11), moment (P12), Kac–Rice (P18)) |
| Collar to reviewed annulus | `|X|∼ r` to `1<A<B` | **Still missing.** Not in this candidate |

## What the 20260927 note left open

That note certified an off-axis divided-difference frame and `q^2` soft factors on
a cubic, then returned four obstructions:

1. the 9-pin Gram is singular on the axis;
2. the nested disk `q=O(r^2)` is not covered by the off-axis frame;
3. no uniform `E[N_mu W_r]/Z_r` lemma;
4. no collar to the reviewed annulus.

The punctured-pin candidate claims to discharge (1) and (2) by a different frame:

    Δ = (q^2 + r^2 p^2)^{1/2},    Y = (f_x/(r^2 Δ), f_z/(r Δ)).

On the axis `q=0`, `p≠0` one has `Δ=r|p|` and `χ=|p|/Δ=1/r`. The mean drift of
`Y` is then order `1/r`, so the Gaussian density of `Y=0` is `exp(-c/r^2)` small.
The angle-free bound (P17) keeps two factors of the short distance `d` and never
divides by `q`. That is the algebraic device. Items (3) and (4) remain open as
theorems: (3) is the continuum count, (4) is a different region.

## P9 — ACCEPT

On `|p|≤1/4`:

    |a| = |(p-1)(2p-1)/12| ≥ 1/32,
    |b| = |(p-1)/2| ≥ 3/8,
    |c| = |p-1/2| ≥ 1/4.

Hence `(ab)^2 ≥ 9/65536`. For `α^2+β^2=1`,

    α^4+β^4 = 1-2α^2β^2 ≥ 1/2,

so `det(BB^T) ≥ (ab)^2 α^4 + c^2 β^4 ≥ (1/2) min{(ab)^2,c^2} ≥ 9/131072`.
The fourth column of `B` only increases `BB^T`. Exact on the 33-point grid
`p=n/64`, `|n|≤16`, and as a polynomial identity for the half-min comparison.

This is a frame-rank statement for the *unconditional* jet map. It does not by
itself prove `Cov_Q(Y) ≧ c_0 I`. That Schur/compactness step is HOLD.

## P17 — ACCEPT as a power identity

Short-segment column plus `K_2` on the perpendicular column:

    |det H_A|, |det H_C| ≤ L d K_2 / 2,     |det H_B| ≤ L r K_2 / 2.

Product `≤ (1/8) L^3 K_2^3 r d^2`. With `d^2=r^2(p^2+q^2)` this is
`O(K^6 r^3(p^2+q^2))`. The two factors of `d` are load-bearing: a `K_2^6` bound
would not cancel the raw Jacobian as `X	o M` on the axis.

The 20260927 cubic gives an on-axis product `O(q^2 r^6)`, which is smaller for
`r<1`. (P17) is coarser and still sufficient for the Region II ledger. It is a
deterministic column-norm bound, not a Gaussian moment.

## Region II ledger — ACCEPT the exponents, HOLD the analysis

On `|q|<r|p|`, `r≤1`:

    χ^2 ≥ 1/(2r^2),     (p^2+q^2)/Δ^2 ≤ 2/r^2.

Power count for `ρ_j^W`:

| Piece | Exponent of `r` |
|---|---|
| `Z_r^{-1}` | `-2` |
| raw gradient Jacobian `r^{-3}` | `-3` |
| (P17) product | `+3` |
| spatial ratio `(p^2+q^2)/Δ^2` | `-2` |
| conditional `K^6` via `χ^6` | `-6` |
| **total before absorption** | **`-10`** |

The candidate then uses `e^{-c/(2r^2)} ≤ 6! (2/c)^6 r^{12}` to absorb `r^{-10}`.
That comparison is a calculus identity once the Gaussian exponent is granted.
The exponent itself is exact. The Gaussian density (P11) and the conditional
sixth moment (P12) are not checked here.

## P4 — ACCEPT

The cubic interpolant `H(x)=b+k(2x^3-3rx^2)` has `H'(rp)=6k r^2 p(p-1)`.
The pin-preserving quartic `x^2(x-r)^2/24` has derivative
`r^3 p(p-1)(2p-1)/12` at `x=rp`. These are the displayed relative terms in (P4).
Mutant `unshifted-quartic` (dropping the `(p-1)` shift) fails.

## What this does not do

- It does not accept (P2) as a theorem.
- It does not accept (P11), (P12), or (P18).
- It does not supply the collar from the scaled disk of radius `1/4` to the
  reviewed fixed annulus `1<A<B`.
- It does not treat shrinking witness collisions near the pins.
- It does not flip D5 off AMEND.

The algebraic device that was missing on 2026-09-27 — compactified gradient plus
angle-free short-edge product — is exact. The count lemma remains a candidate.
