# Retain lifetime dependence in the R81 far-sector remainder

## 1. Conditional statement and inherited inputs

Use the exact R81 core `QUANTITATIVE_COMPACT_MARKED_TRANSFER_V1.md`,
22,757 bytes, SHA-256
`e4db3edff5716cbb117561611c6e6c2e9a6e9f54721b977073426ad3d532f800`,
published in [Math193/6293293133](https://github.com/d6g8k5htny-coder/Math-/issues/193#issuecomment-6293293133)
and conditionally adopted in [6293464537](https://github.com/d6g8k5htny-coder/Math-/issues/193#issuecomment-6293464537).
All its original-law, canonical-density, GAD, Kac--Rice, Morse/elder and
coefficient-identification premises remain assumptions here. This addendum
does not independently discharge those inherited results.

In particular the law is the normalized **full** Gaussian Fourier law on the
physical torus `(R/24Z)^2`, including DC. Derivatives are physical derivatives.
The observable is the height-integrated intensity of positive finite ordinary
superlevel-H0 elder bars, counted once; zero and essential bars are excluded.
Write its admitted canonical density as `rho(ell)` and its measure as
`I(J) = integral_J rho(ell) d ell`. Its ideal lifetime measure is absolutely
continuous on positive lifetimes under the inherited premises.

Keep the R81 near/far separation `r0`, with `0 < r0 <= 1/4`. Keep its compact
comparison radius `R_cap` separately, with `0 < R_cap <= r0`.
For its normalized H7 norm, write

    H(f)^2 = sum_m (1 + |h m|^2)^7 |f_hat(m)|^2,   h = pi/12,
    Theta = E H(F)^2,
    S4(f) <= e_emb H(f).

R81 K1--K2 give finite positive `Theta` and `e_emb`, with the original infinite
spectral tails. R81 K19 supplies the unchanged uniform floor

    mu = (r0/12)^6 / 2787840000 > 0,
    Sigma_v = Cov O_v >= mu I5,
    O_v = (grad F(0), grad F(v), F(0) - F(v)),

throughout the far displacement region `v in [-12,12]^2`, `|v| >= r0`.
No sharper floor or new numerical evaluation is used here.

Define the positive constants

    p_far = (2 pi)^(-5/2) mu^(-5/2),
    A = 576 p_far * 3 e_emb^4 Theta^2.

The first result is

    0 <= rho_far(ell) <= A (1 + ell^2/mu)^2,       (F1)

for `0 < ell <= 1`, with the same raw far-sector Kac--Rice representation as
R81 K20. Inserting (F1) into the R81 near-sector argument gives

    |ell^(1/3) rho(ell) - C_alg(2,24)|
      <= S(q) + T(B) + c Delta(ell^(1/3)/q)
                       + A ell^(1/3) (1 + ell^2/mu)^2,     (F2)

where `c = 2 pi (B-q)`, `0 < q <= 1`, integer `B >= 1`, and
`0 < ell <= min{1, (q R_cap)^3}`. All compact cutoffs, functions and constants
are exactly those of R81 K9--K21. The result is a conditional upper bound,
not a claim of a usable evaluated lifetime window.

## 2. Keep both conditional mean and residual

View `F` as a centered real Gaussian random variable in the real H7 Hilbert
space. Let `C` be its covariance operator, so `tr C = Theta`. For a fixed far
displacement, let `L_v` be the bounded linear observation map from H7 to R5
whose value on `F` is `O_v`. Then `Sigma = L_v C L_v* >= mu I5`.
Set

    T = C L_v* Sigma^(-1/2),
    K = T T*,
    Q = C - K.

Gaussian regression gives `0 <= K <= C`, `Q >= 0`. The canonical conditional
field at the literal target `o = (0,0,ell)` is `m + G`, where the two zero
entries denote two-dimensional zero gradient blocks and

    m = T Sigma^(-1/2) o,
    G is centered Gaussian with covariance Q.

This is the canonical regression law at the target, rather than conditioning
on a positive-probability event. Its use consumes the same canonical-law
premise as R81. The target has Euclidean squared norm `ell^2`, hence

    ||m||^2 <= ||T||_HS^2 ||Sigma^(-1/2) o||^2
            <= tr(K) ell^2/mu <= Theta ell^2/mu,
    tr Q <= Theta.

The exact Gaussian fourth-moment identity is

    E ||m+G||^4
      = ||m||^4 + 2 ||m||^2 tr Q + 4 <m,Qm>
                         + (tr Q)^2 + 2 tr(Q^2).

Since `Q >= 0`, its operator norm and Hilbert--Schmidt norm are bounded by
`tr Q`. With `x = ell^2/mu >= 0`, this gives

    E ||m+G||^4 <= Theta^2 (x^2 + 6x + 3)
                 <= 3 Theta^2 (1+x)^2.                    (F3)

One may obtain the identity in H7 by finite orthogonal projections and
monotone convergence of the fourth powers of the projected norms; the
trace expressions converge for the positive trace-class covariance.
Thus (F3) requires neither a centered conditional law nor independence
between the conditional mean and a discarded bad event.

Apply `S4 <= e_emb H` to (F3). For each of the two physical 2-by-2 Hessians,
`|det Hess| <= S4^2`, so their product is at most `S4^4`. The type/elder marks
lie in `[0,1]` and can be discarded for an upper bound. The raw five-dimensional
Gaussian observation density at `o` is at most `p_far`. Integrating over the
far displacement region, whose area is at most `576`, proves (F1).

The stationary base-point volume was already canceled in the original
normalization. The `576` in `A` is the displacement-area bound once.
There is no further base-point volume or compact radial Jacobian `12 r^-5`
in this raw far calculation. The far split stays at `r0`; shrinking the
compact radius does not introduce an uncharged annulus.

## 3. Normalized-density envelope and fixed-cutoff window

The compact near-sector estimate used in deriving R81 K21 is unchanged.
Add its absolute error bound to the nonnegative far contribution, now bounded
by (F1) rather than the coarsened K20 constant. This proves (F2).

Write the R81 polynomial `Delta(r) = alpha0 + alpha1 r + alpha2 r^2`, where

    alpha0 = 12 p_* (Tail + Z^2 eta^2/2),
    alpha1 = 12 p_* E_g (2 M^2 + Z eta),
    alpha2 = 12 [p_* E_g^2 + D_p Z^2 J_B/4].

These are direct expansions of R81 K15/K17, with all symbols inherited and
all coefficients nonnegative. `alpha2` is not R81's observation-error
constant `d_2` from K3.

For fixed admissible `q,B,eta,M0` and all their derived constants, put

    P(R) = S(q) + T(B) + c Delta(R)
                       + A qR (1 + (qR)^6/mu)^2
         = S(q) + T(B) + c Delta(R)
                       + A qR + (2 A q^7/mu) R^7
                              + (A q^13/mu^2) R^13.       (F4)

For `0 < R <= R_cap`, (F2) is at most `P(R)` on the whole interval
`0 < ell <= (qR)^3`. Indeed `ell^(1/3)/q <= R`, `Delta` is nondecreasing,
and each term of the far envelope is nondecreasing in `ell`. Also
`(qR)^3 <= 1` from the inherited bounds on `q` and `R_cap`.

If an owner supplies a positive rational `E`, or a positive computable real
with certified interval access, and the fixed cutoffs satisfy

    P(0) = S(q) + T(B) + c alpha0 < E,

then continuity gives a positive `R <= R_cap` with `P(R) < E`. The nonnegative
polynomial has no undecidable monotonicity condition to infer. Strict slack
permits a future rational search with outward interval certification to
terminate, assuming certified access to the inherited computable constants.
This paper executes no such search and chooses no scientific `E`.

Alternatively preserve R81's five budget allocations and its safe `2 pi B`
relaxation. Its last radius inequality becomes

    2 pi B [Delta(R) - Delta(0)]
             + A qR (1 + (qR)^6/mu)^2 <= E/4.             (F5)

The left side is a nonnegative-coefficient polynomial vanishing at zero,
so the same strict-slack construction remains available. Nothing in this
substitution changes the earlier cutoff selection or compact cap hypotheses.

For `ell <= 1`, the new far envelope is at most the original
`A (1+1/mu)^2`. Consequently any fixed-cutoff radius satisfying the original
inequality also satisfies its refined counterpart. This is a comparison of
upper certificates; it guarantees no numerical improvement in the actual
maximal usable radius and no lower bound on the physical error.
Conditionally, if a prospective window satisfies `ell_*^2 <= mu`, then
`rho_far(ell) <= 4A` throughout that window. That additional inequality has
not been evaluated or asserted for the project's study.

## 4. Integrate the density envelope for ideal half-open bins

Define nonnegative constants

    N0 = S(q) + T(B) + c alpha0,
    N1 = c alpha1/q,
    N2 = c alpha2/q^2.

Dividing (F2) by `ell^(1/3)` gives directly

    |rho(ell) - C_alg(2,24) ell^(-1/3)|
      <= N0 ell^(-1/3) + N1 + N2 ell^(1/3)
                          + A [1 + 2 ell^2/mu + ell^4/mu^2].

Thus for `0 < a < b <= min{1,(q R_cap)^3}`,

    |I([a,b)) - (3/2) C_alg(2,24) (b^(2/3)-a^(2/3))|
      <= (3/2) N0 (b^(2/3)-a^(2/3))
             + N1 (b-a) + (3/4) N2 (b^(4/3)-a^(4/3))
             + A [(b-a) + 2(b^3-a^3)/(3mu)
                              + (b^5-a^5)/(5mu^2)].       (F6)

This follows by the triangle inequality for the integral and elementary
antiderivatives. The same formula with `a=0` holds for `I((0,b))` by monotone
convergence for the nonnegative density and integrability of the displayed
envelope at zero. Endpoints at positive lifetimes have zero mass for this
ideal absolutely continuous measure. This reasoning does not remove atoms
in a finite-word sampling law or substitute for a finite-field/full-field
matching certificate. No cumulative estimate was differentiated.

The coefficient in (F6) is the exact `C_alg`. If a consumer substitutes an
enclosure `[C_lo,C_hi]`, its coefficient-width allowance is additional and
must be propagated through the chosen comparison; it is not included in `N0`.

## 5. Paper adverse cases and boundaries

These are analytical checks, not executed controls:

- A nonzero target can give a nonzero mean. Dropping `m` would incorrectly
  remove the `ell^2/mu` dependence; (F3) retains it explicitly.
- As `mu` tends to zero at a fixed positive lifetime, the displayed envelope
  can diverge. The conditional `4A` simplification requires `ell_*^2 <= mu`
  and cannot be applied merely because `ell_*` is called small.
- `R_cap < r0` does not move the far region. The compact argument and
  R81's existing small/large sectors still cover their original domains.
- An extra `576` or `12 r^-5` is incompatible with the raw observation used
  in Section 2. The source's normalized volume and near radial change of
  variables have distinct roles.
- Integrating only the normalized far error `A ell^(1/3)(...)` would be
  incorrect for bin counts. Section 4 first divides by `ell^(1/3)`.
- `P(0)=E` alone does not guarantee a positive certified radius when a
  positive linear term is present. The method requires strict constant-term
  slack, not failure to find a counterexample or a post-hoc target.

The suggestion to retain lifetime in K20 is credited to Anthropic
Claude017's released [input6294643099](https://github.com/d6g8k5htny-coder/Math-/issues/193#issuecomment-6294643099).
That input includes its own disclosed integer-check execution; this new
derivation is paper only and borrows no unreported execution or approval.
OpenAI/Codex `/root/far_sector_refinement_design` supplied source-exposed
analytical design assistance. The author checked the argument above; a fresh
exact-final nonauthor review remains distinct from that assistance.

This conditional addendum changes no accepted source, engine, input, runtime,
permission, scientific register or review disposition. R83-EXEC-01 and the
occupied R85 engineering role remain unchanged. No numerical constant,
window, P2 reach sign, current-study compatibility, source-word/IID law,
full-field count-tail/unclipping, informative width, confidence, power,
resource feasibility or scientific admission follows from this paper.
