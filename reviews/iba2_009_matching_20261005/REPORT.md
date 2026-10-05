# IBA2-009: a half-power matching layer invisible to compact cusp parity

**Object:** IBA2-009-MATCHING-20261005-v1. **Date:** 2026-10-05.
**Actual author:** OpenAI / GPT-6 Astra Pro, session
`github-rules-and-closure-round5-20261005`, Dylan Roy — delegated AI work.
**Scientific effect: NONE.** Author-side analytical audit contribution, requiring
nonauthor review; no historical verdict, proof, flag or register is changed.
Organizational-independence credit: 0. This is not a claim of informational
blindness: the original audit's coverage map and repository discussion were read.

## 1. Result, limits, and source pin

The compact-to-global implication in main#259 IBA2-009 needs a genuine matching
estimate. Here are three concrete outputs:

1. An exact formula for the actual rejected-density contribution in the moving
   band `a <= k^3/r <= b`: it has an `ell^(1/2)` prefactor and an explicitly
   weighted rescaled-kernel integral.
2. An abstract kernel family with a nonzero half-power contribution that is
   invisible in every fixed compact cusp window and at every fixed positive
   gap. It obeys the selected upper bounds below, including the C7 K2 scale.
3. Sufficient weighted-tail conditions for a correctly matched residual to be
   `o(ell^(1/2))`, stating exactly what compact parity does not supply.

**Not proved:** that the Gaussian field has this nonzero profile, that its
half-power coefficient exists or vanishes, or that all its other probabilistic
interfaces admit the abstract family. This is not a counterexample to Theorem N
or to the persistence law. It is a counterexample to inferring global absence
from the listed estimate-level premises alone. IBA2-009 remains open for the
actual field. A positive contribution from one moving band alone also does not
establish the coefficient of a full asymptotic expansion after other regions and
lower-order terms are matched.

All source reads use Math- commit
`dcd2a886e322738324a745adcad12fd3735bd2c5`:

| Source | Exact path / Git blob | Scope read and consumed |
|---|---|---|
| N | `frontiers/elder_cusp_parity_20261002/PROOF.md` / `16a1db0658918057ff741df888c13702763d9919` | Statement, Corollary N-prime and its section 6 proof; section 7 Remark 1. Selected section 5 bookkeeping was read, not re-audited. |
| T | `frontiers/third_order_rate_20261001/PROOF.md` / `110ed33a57902bef11873807e722fde3888b59fb` | Section 0 kernel definitions, E3-plus/R-plus remainders and W-plus small-gap window. |
| K | `frontiers/c7_total_bounded_20260929/PROOF.md` / `28748b086ec6761ef467dc67cba475fbdf8b7455` | K1/K2 and section 4 unnormalized marked-intensity identity and Gaussian pin-density envelope. |

N already explicitly limits its no-linear-term theorem to fixed compact
`kappa=k/r` intervals. Its Remark 1 distinguishes the two uncontrolled ends and
says that even a hypothetical uniform `O(r^2+k^2)` estimate would not finish the
global half-power question. This report quantifies a specific obstruction to
that inference; it does not attribute an unrestricted claim to N.

## 2. Exact moving-band formula for the actual nonnegative kernel

Use the source conventions, without dividing by the full normalizer:

    A_rej(r,b,k,u) = 12 pi_r(v_r) E_Q[(W_r/r^2)(1-e)],
    B_r(k) = integral_b integral_u A_rej(r,b,k,u) d sigma(u) db >= 0,
    nu_rej^near(ell) = integral_0^r0 r^(-2) B_r(ell/r^3) dr.

This is K section 4 in the separation variable. The cap implication
`1-e <= 1_{G_r^c}`, K2 and the Gaussian pin-density envelope give

    0 <= B_r(k) <= C r^3/k,       0 < r <= min(k,r0), 0 < k <= 1.       (2.1)

Integration over birth and direction, and absorption of polynomial gap growth
on `0<k<=1`, are included in C. Fix `0<a<b<infinity`. Set

    y = k^3/r = ell^3/r^10,
    r_ell(y) = ell^(3/10) y^(-1/10),
    k_ell(y) = ell^(1/10) y^(3/10),
    J_ell(y) = k_ell(y) B_{r_ell(y)}(k_ell(y))/r_ell(y)^3.             (2.2)

For all sufficiently small ell (depending on a,b,r0), the whole band satisfies
`r<=min(k,r0)` and `k<=1`. Substitution of (2.2), including `dr`, gives exactly

    nu_[a,b](ell)
      = ell^(1/2)/10 * integral_a^b J_ell(y) y^(-3/2) dy.              (2.3)

Indeed `r/k = ell^(1/5)y^(-2/5)` and
`|dr/dy| = ell^(3/10)y^(-11/10)/10`. By (2.1), `0<=J_ell<=C` on
this fixed band. Therefore this actual band contribution is `O(ell^(1/2))`.
If `J_ell -> J` almost everywhere on [a,b], dominated convergence yields

    ell^(-1/2) nu_[a,b](ell) -> (1/10) integral_a^b J(y)y^(-3/2)dy.    (2.4)

More generally convergence of that weighted integral suffices. A uniform
`J_ell -> 0` proves a little-o contribution from this band. K2 supplies a
bounded J, not a vanishing J. Establishing its actual limit is a sharply
localized analytic task; the present report does not assume a limit exists.

The band has

    r ~ ell^(3/10),  k ~ ell^(1/10),  kappa ~ ell^(-1/5).              (2.5)

Thus k tends to zero while kappa tends to infinity. Neither fixed-positive-k
Taylor expansion nor compact-kappa parity describes the passage uniformly.

## 3. An explicit estimate-level obstruction

First omit a harmless gap cutoff. Let

    h(t) = (t-1)^4(2-t)^4 for 1<=t<=2, and 0 otherwise,
    psi(y) = h(sqrt(y)),
    H(r,kappa) = r^2 kappa^2 psi(r^2 kappa^3)
                 = k^2 psi(k^3/r),              k=kappa r.          (3.1)

Here H is a **scaled** kernel perturbation; its raw kernel is `D=r^2 H`.
The polynomial bump is C^3, is nonnegative, and is bounded by 1. The support
is `1<=k^3/r<=4`.

### 3.1 Why the usual estimates do not see it

- At fixed kappa, (3.1) is even in r. On every fixed compact kappa interval it
  is identically zero for all sufficiently small |r|. In particular it has
  zero linear term and satisfies compact `O(r^2)` estimates.
- At any fixed k>0 it is identically zero once `r<k^3/4`. It changes no
  coefficient in a fixed-k asymptotic expansion.
- Globally, `0<=H<=k^2<=r^2+k^2`. It therefore meets even the hypothetical
  quadratic bound discussed in N Remark 1.
- On `k<=1`, `H<=k<=r(1+kappa)`, the CE-plus-plus scale.
- On its support, `D=r^2 k^2 psi <=4r^3/k`, the K2 scale, with the original
  `r<=k` condition satisfied whenever k<=1. The raw-versus-scaled distinction
  and the lifetime Jacobian are essential here.
- If `k<=r<=1`, then `k^3/r<=r^2<=1`, so D is zero. The W-plus small-gap
  window is unaffected by this perturbation.

The family can respect positivity and a Gaussian-envelope-type upper bound.
Choose an even smooth cutoff theta(k) with `0<=theta<=1`, theta=1 for
`|k|<=1/2`, and theta=0 for `|k|>=1`, and replace H,D by theta(k)H,theta(k)D.
As an explicit abstract nonnegative split on `0<r<=1`, take

    A_cand(r,k) = k^2 theta(k),
    A_rej(r,k)  = r^2 k^2 theta(k) psi(k^3/r),
    A_eld(r,k)  = A_cand(r,k)-A_rej(r,k).                            (3.2)

Then `0<=A_rej<=A_cand`, and `A_eld>=0`. These raw kernels obey a K1-sized
majorant; on the compact k support they also obey a polynomial times
`exp(-c k^2)` majorant, after enlarging the constant. Multiplication by a
normalized Gaussian birth envelope and normalized angular measure preserves
these statements. This is only an abstract kernel construction, not a
realization as Gaussian critical points, an elder mark, or a Palm law.

### 3.2 Exact half-power mass

For ell sufficiently small that the whole support is inside `0<r<=r0` and
`k<=1/2`, theta=1 on the support. It suffices to take
`ell <= min(2^(-16), r0^(10/3))`, with `0<r0<=1`. Put
`t=ell^(3/2)/r^5`; then `k^3/r=t^2` and

    integral r^(-2) A_rej(r,ell/r^3) dr
      = integral ell^2 r^(-6) h(ell^(3/2)/r^5) dr
      = ell^(1/2)/5 * integral_1^2 (t-1)^4(2-t)^4 dt
      = ell^(1/2)/3150.                                           (3.3)

The integration range is `[ell^(3/10)2^(-1/5),ell^(3/10)]`.
The coefficient is exact: after v=t-1, the bump integral is
`integral_0^1 v^4(1-v)^4 dv = 1/630`.

C^3 regularity is not the reason this occurs. Replacing h by any nonzero,
nonnegative C-infinity bump supported inside (1,2), bounded by 1, preserves
all the estimates and produces coefficient `(1/5)integral h>0`.
The explicit rational coefficient (3.3) is reserved for the polynomial h;
no closed-form value is asserted for the smooth variant.

An added half-power correction is smaller than the existing
`O(ell^(3/7))` remainder and `O(ell^(4/9)log(1/ell))` upper scale. It is
therefore not excluded merely by those error orders. The model's perturbation
is zero on the small-kappa region; it does not purport to reconstruct the
sources' complete leading laws or all cross-region matching identities.

## 4. A sufficient global passage, with the required subtraction explicit

Let E_ell(kappa) denote a **correctly matched residual**: the known fold, cusp,
and common terms must already have been subtracted with no double counting.
Constructing this residual is itself part of the missing analysis. It is NOT
permissible simply to label the raw difference in N.1 as this residual:
that difference can still contain the fold contribution to the ell^(1/3)
coefficient when integrated globally.

Suppose the residual density has the exact representation

    R(ell) = ell^(1/4)/4 * integral_0^infinity
               E_ell(kappa) kappa^(-5/4) d kappa + F(ell),           (4.1)

where the integrand is extended by zero below the physical lower cutoff
`kappa=ell/r0^4`, and `F(ell)=o(ell^(1/2))` accounts for separately controlled
far/matching remainders. Assume on every fixed `0<a<b<infinity`,

    integral_a^b |E_ell(kappa)| kappa^(-5/4)d kappa = O_(a,b)(ell^(1/2)).

This is the type of compact control furnished by an O(r^2) estimate after
`r=(ell/kappa)^(1/4)`, provided the subtraction also has that property. A
sufficient missing tail condition is

    lim_(a down to 0, b up to infinity) limsup_(ell down to 0)
      ell^(-1/4) * [integral_0^a + integral_b^infinity]
      |E_ell(kappa)| kappa^(-5/4)d kappa = 0.                        (4.2)

Split (4.1) into those two tails and [a,b], divide by ell^(1/2), first let
ell tend to zero, then exhaust the interval. The compact part is O(ell^(1/4))
after division, and (4.2) controls the tails. Hence `R(ell)=o(ell^(1/2))`.

For a stronger convenient sufficient estimate, an all-domain bound

    |E_ell(kappa)| <= C ell^(1/2) kappa^(-1/2) M(kappa),
    integral_0^infinity M(kappa) kappa^(-7/4)d kappa < infinity

gives an O(ell^(3/4)) integral in (4.1). For example the integral condition
holds for nonnegative, locally integrable M with M=O(kappa^p) near 0, p>3/4, and
M=O(kappa^q) near infinity, q<3/4. These are sufficient assumptions, not
established properties of the actual Gaussian kernel.

The obstruction (3.1) violates (4.2): its normalized weighted mass stays
positive while its support escapes to kappa=infinity. Pointwise convergence
and compact parity thus cannot replace quantitative control of these tails.

## 5. Reproduction, coverage and next mathematical target

Run `python3 -B -S boundary_layer_check.py`, and repeat with `-O`.
The deterministic JSON reports 25 moving-layer, 30 compact-cusp, 25 fixed-gap,
20 small-gap and 3 exact-integral cases. The explicit finite checks verify
identities and inequalities, not the Gaussian realization or the general
claims by sampling; the proofs are sections 2–4 above.

Negative controls (each must exit 1 with its named failure):

| Variant | Deliberate error | Failure |
|---|---|---|
| M1 | k^3/r^2 instead of k^3/r | MOVING_LAYER_ARGUMENT |
| M2 | omit r^2 between raw and scaled kernels | LIFETIME_JACOBIAN |
| M3 | omit the 1/5 substitution factor | INTEGRATION_FACTOR_ONE_FIFTH |
| M4 | ignore the moving support at fixed kappa | COMPACT_CUSP_VANISHING |
| M5 | replace the half-power x^5 by x^6, ell=x^10 | HALF_POWER_SCALING |

Example: `python3 -B -S boundary_layer_check.py --mutant M2`.
Invalid arguments exit 2. All fourteen CLI cases were run in normal/optimized
modes, and the positive JSON was byte-identical. A separate seven-test local
contract suite passed both modes after its expected missing-source failure.
No local Lean execution is claimed. Existing hosted repository checks are
separate and do not automatically execute this newly added standalone script.

**Actionable target:** determine the actual nonnegative profile in (2.2) on a
fixed positive y-band, rather than extrapolating fixed-kappa parity. Uniform
vanishing would remove that band's half-power mass; a nonzero limiting profile
would require explicit incorporation into global matching. Neither outcome is
assumed. Both ends of the matched residual in (4.2) still require control before
a global absence statement. Historical IBA2-009, IBA2-010, IBA2-012 and all
scientific acceptance fields remain unchanged by this contribution.
