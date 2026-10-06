# Cap I4 in d=3: explicit spectral pushforward and a ninth-moment envelope

**Object:** CAP-I4-D3-SPECTRAL-20261005-v1.0.  
**Author:** OpenAI / GPT-6 Astra Pro, session `cap-i4-explicit-d3-adapter-20261005`, acting for Dylan Roy.  
**Disposition:** additive ordinary-mathematical proposal; nonauthor review pending. No Lean implementation or kernel verification of this new adapter is claimed. Scientific/status effect NONE; organizational-independence credit 0.  
**Pickup:** main#229 comment 6006586304.

## 1. Source and scope

Repository `d6g8k5htny-coder/Math-`, source cut `f4c33a98a982d50aa490e49ce9327c755682527c`.

P is `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md`, Git blob `dfed3b8d318a3ab1950957f393307733a4bef3f2`. Consumed interfaces: matrix-density majorant (3.5), full-field residual independence and moments (4.2)-(4.3), full normalizer (5.5), typed determinant inequality (6.2), and the depth/exception events in section 7. Read section 5 with `ERRATUM_CONGRUENCE.md`, not its historical multiplying-sqrt(r) wording. No re-review of every ancestor is claimed.

The existing Cap companion at `f4079f65a3e5e95c9993e51ac5995a54344d4130`, `companions/cap_i4_source_bridge_20261005/CapI4.lean`, blob `4769930d132a485f88b75c4f4d901a3c4db7d43e`, proves the conditional integral/normalizer ledger. It does not prove its concrete `MatrixDepthTransport` premise. The general spectral-measure reduction in main#229 comment 6006128867 is credited as motivation, not consumed as an already-accepted theorem.

This note proves the 2x2 version of the spectral measure domination directly by trace and polar coordinates, fixes its exact volume convention, and retains one more hard-eigenvalue factor in the depth estimate. The resulting sufficient residual moment is order **9**, instead of order 10 in P's coarser m=2 envelope. This is a moment-sufficiency refinement, not an optimality claim or a guaranteed improvement in the numerical size of the constant.

Fixed ambient dimension d=3, so the transverse dimension is m=2. There is no assertion for m=1 by inserting zero-dimensional coordinates, no d>=4 theorem, no numerical coefficient c_(3,L), no evaluated finite-radius threshold, and no all-mark or all-volume uniformity. Exact scalar moment algebra is not a continuum or Lean proof.

## 2. Volume conventions and the exact change of variables

Write

    B = [[a,b],[b,d]],   dB_entry = da db dd,
    t = (a+d)/2,  x = (a-d)/2,  y = b.

Thus `||B||_F^2 = a^2+2b^2+d^2 = 2(t^2+x^2+y^2)` and

    dB_entry = 2 dt dx dy.                                  (1)

On the complement of the polar cut and origin, put `x=rho cos(theta)`, `y=rho sin(theta)`, with `rho>0` and `-pi<theta<pi`. The cut, including its product with the t axis, is entry-Lebesgue null. The increasingly ordered eigenvalues are

    lambda=t-rho,   Lambda=t+rho,
    t=(lambda+Lambda)/2,   rho=(Lambda-lambda)/2.

The linear determinant for `(lambda,Lambda)->(t,rho)` is 1/2. Combining it with (1) and the polar determinant rho gives

    dB_entry = ((Lambda-lambda)/2) d lambda d Lambda d theta. (2)

For a direct check, the derivative of `(a,b,d)` with respect to `(lambda,Lambda,theta)` is

    [[(1-cos theta)/2, (1+cos theta)/2, -rho sin theta],
     [-sin theta/2,     sin theta/2,      rho cos theta],
     [(1+cos theta)/2, (1-cos theta)/2,   rho sin theta]].

Its determinant is `rho(cos^2 theta+sin^2 theta)=rho`, not twice rho. This parameterization covers each nonscalar matrix once off the polar cut. There is no extra factor for the signs of eigenvectors and no unordered-eigenvalue factorial. The eigenvector rotation angle would be half theta, with a different interval and Jacobian; that is not the coordinate used here.

For a nonnegative measurable function p on entry space, its positive-cone spectral pushforward has density, almost everywhere on `0<lambda<Lambda`,

    q_+(lambda,Lambda)
      = (Lambda-lambda)/2 * integral_{-pi}^{pi}
          p(t+rho cos theta, rho sin theta, t-rho cos theta) d theta. (3)

This follows first for nonnegative integrands by the change of variables and Tonelli. It then identifies the pushed-forward measure by all nonnegative measurable spectral tests. No choice of measurable eigenvectors is required: the two eigenvalues are explicit continuous functions of a,b,d.

Repeated eigenvalues form the line `x=y=0` in entry coordinates and have entry-Lebesgue measure zero. Formula (3) does not discard any neighborhood of that line. It also imposes no positive lower cutoff on Lambda; both eigenvalues may approach zero. Any measure dominated by an entry density also assigns zero mass to the line. Assertions here are about that absolute-continuity class, not arbitrary singular matrix laws.

**Frobenius-volume warning.** In the orthonormal coordinates `(a,sqrt(2)b,d)`, volume is

    dB_F = sqrt(2) dB_entry.

Therefore (2) has an additional sqrt(2) for dB_F. A Gaussian density quoted with respect to orthonormal Frobenius coordinates must be multiplied by sqrt(2) before using it as an entry density.

**Independent normalization check.** The integral of `exp(-||B||_F^2)` over all entry coordinates is `pi^(3/2)/sqrt(2)`. The spectral formula gives

    pi * integral_{lambda<Lambda} (Lambda-lambda)
                       exp(-lambda^2-Lambda^2) d lambda d Lambda
    = 4pi * integral_R exp(-2t^2)dt * integral_0^infty rho exp(-2rho^2)d rho
    = pi^(3/2)/sqrt(2).

The angle, ordering, and off-diagonal-volume constants consequently agree. This checks the reference measure, not rotational invariance of the actual law.

## 3. Explicit non-isotropic spectral domination

Suppose the law of B has entry-coordinate density p satisfying

    p(B) <= C0 exp(-c||B||_F^2),  C0>=0, c>0.             (4)

No invariance is assumed for p. The majorant is radial in Frobenius coordinates. By (3),

    q_+(lambda,Lambda)
      <= pi C0 (Lambda-lambda) exp(-c(lambda^2+Lambda^2))
                           1_{0<lambda<Lambda}.           (5)

Equivalently, with `e(B)=(lambda,Lambda)`,

    e_*(Law(B) restricted to {B>0}) <= sigma_2,
    sigma_2 = pi C0 (Lambda-lambda) exp(-c(lambda^2+Lambda^2))
                         1_{0<lambda<Lambda} d lambda d Lambda. (S2)

The left side is a subprobability; sigma_2 is a dominating finite measure, not a normalized eigenvalue law. It is important that the factor is **pi C0**, for the entry-coordinate convention in (4). Under a Frobenius-volume density majorant C_F, use `C0=sqrt(2)C_F`.

For a concrete Gaussian covariance bound, let `X=(a,sqrt(2)b,d)` have mean m and positive-definite covariance Sigma. If

    lambda_max(Sigma)<=S,  det(Sigma)>=delta>0,  ||m||<=M,

then one valid choice is

    c=1/(4S),
    C_F=(2pi)^(-3/2) delta^(-1/2) exp(M^2/(2S)),
    C0=sqrt(2)C_F.                                        (6)

Indeed, `(X-m)^T Sigma^(-1)(X-m)>=||X-m||^2/S`, and

    ||X-m||^2 >= ||X||^2/2-||m||^2,

because the difference is `||X-2m||^2/2>=0`. Insert these estimates in the Gaussian density. Formula (6) is conditional on valid covariance/mean bounds; it is not an evaluated bound for any given L or r. P(3.5) already supplies the existence of uniform C0,c on its fixed-d,L compact-mark/frame family.

## 4. Probability and weight hypotheses

Work on a probability space with original law Q. Assume:

1. B is a measurable symmetric 2x2 matrix satisfying (4). J is measurable, `J>=1`, independent of the **entire B**, and `E_Q[J^9]<=M9<infinity`.
2. `0<r<=1`, `k>=k_floor>0`, K>0. W is nonnegative and integrable. On `{W>0}`, B>0, h=M3>=0, `h<=K(J+Lambda)`, and the m=2 case of P(6.2) holds:

       W <= r^2 h^2/4 * lambda(lambda+(3/2)rh) * Lambda(Lambda+rh). (7)

3. The depth event is `E_lambda={lambda<=[4/(3k)] r h^2}`. Outside `{W>0}`, the values of h and the event do not affect its weighted numerator. All events used for normalized probabilities are measurable.

P(4.3) gives `h<=K0(J+||B||_F)`; on the positive cone `||B||_F<=sqrt(2)Lambda`, so choosing `K=sqrt(2)K0` suffices. This norm-conversion factor must not be dropped. The source has moments of every finite order, so the ninth moment here is available at its stated compact scope.

The proof never conditions the original independence assumption on the typed event. Typing can couple B and J. Instead we majorize the weighted integrand on typed support by a function of B,J and then integrate under the ORIGINAL product law. Independence of W, h, or separate eigenvalues is neither assumed nor inferred.

## 5. Retain the hard eigenvalue: the r^5 numerator from moment nine

Set

    U=J+Lambda>=1,  D=4K^2/(3k_floor),  E=3K/2,
    A=K^2(1+K)/4,  B_* = D^3/3+ED^2/2.

On weighted depth support, `0<lambda<=DrU^2`. Since r<=1 and Lambda<=U,

    Lambda(Lambda+rh) <= (1+K)Lambda U,
    h^2/4 <= K^2 U^2/4.

Hence (7) gives the stronger pre-integration majorant

    W 1_E_lambda <= A r^2 Lambda U^3 lambda(lambda+ErU)
                        1_{0<lambda<=Lambda, lambda<=DrU^2}. (8)

The retained factor Lambda is the difference from the coarser `U^4` prefactor used in P for m=2. Apply independence and the spectral measure domination (S2) to the nonnegative right side. On the ORIGINAL ordered domain, `Lambda-lambda<=Lambda`. Drop only the small-variable Gaussian `exp(-c lambda^2)<=1`. Keeping J,Lambda fixed is legitimate because m=2, and now extend the nonnegative lambda integral from `[0,min(Lambda,DrU^2)]` to `[0,DrU^2]`. This yields

    E_Q[W 1_E_lambda]
      <= pi C0 A r^2 E_J integral_0^infty Lambda^2 U^3 exp(-cLambda^2)
                   [integral_0^(DrU^2) lambda(lambda+ErU)d lambda] d Lambda.

Do NOT carry the signed factor Lambda-lambda onto the enlarged domain: it becomes negative when lambda>Lambda. Its bound by Lambda has already been made on the original domain.

The exact inner integral, also proved in the existing companion, is

    r^3[(D^3/3)U^6+(ED^2/2)U^5].

Therefore

    E_Q[W 1_E_lambda]
      <= pi C0 A r^5 E_J integral_0^infty Lambda^2 exp(-cLambda^2)
                         [(D^3/3)U^9+(ED^2/2)U^8]d Lambda
      <= pi C0 A B_* r^5 E_J integral_0^infty Lambda^2 (J+Lambda)^9
                                                    exp(-cLambda^2)d Lambda. (9)

All steps use nonnegative integration, so Tonelli applies before integrability has been established. The following finite bound supplies integrability afterwards:

    (J+Lambda)^9 <= 256(J^9+Lambda^9),
    integral_0^infty Lambda^2 exp(-cLambda^2)d Lambda = sqrt(pi)/(4c^(3/2)),
    integral_0^infty Lambda^11 exp(-cLambda^2)d Lambda = 60/c^6.

Consequently a fully displayed sufficient constant is

    C_depth = 256 pi C0 A B_* [M9 sqrt(pi)/(4c^(3/2)) + 60/c^6],
    E_Q[W 1_E_lambda] <= C_depth r^5.                      (10)

The two Gaussian integrals follow by `y=c Lambda^2` and Gamma(3/2)=sqrt(pi)/2, Gamma(6)=120. No Monte Carlo, unweighted tail substitution, inverse eigenvalue, or positive hard-eigenvalue cutoff is used. The estimate covers corank-two NEIGHBORHOODS and the small-Lambda region directly.

Order nine is sufficient, not claimed necessary. A family with bounded eighth moment and unbounded ninth moment shows only that one cannot replace M9 by M8 in the particular separated envelope (9) without another argument. It does not refute the possibility of a better proof under fewer moments.

## 6. Full normalization and the separate E4 input

Assume the actual FULL normalizer `Z=E_Q W>=cZ r^2`, cZ>0. Divide (10) exactly once:

    Q^W(E_lambda) <= (C_depth/cZ)r^3.                      (11)

This neither adds a pin density nor normalizes on the good event. For
`E4={3k/10<rM4}`, retain the independent assumption

    E_Q[(W/r^2)M4^4] <= M4joint.

The pointwise fourth-moment estimate gives

    Q^W(E4) <= M4joint/[cZ(3k_floor/10)^4] r^4.             (12)

A raw unweighted fourth moment alone is not (12)'s premise. The cap-failure union and the implication on W>0 supplied by the deterministic source therefore give

    Q^W(G^c) <= (C_depth/cZ)r^3
                + M4joint/[cZ(3k_floor/10)^4]r^4.          (13)

The implication need only hold Q-a.e. on positive-weight support, not globally off typed support. The moment-nine refinement is for the depth numerator; it does not eliminate the separate weighted E4 moment assumption.

For a parameter family, C0,c,K,k_floor,M9,cZ,M4joint must have the stated common bounds. P supplies them only after restricting to its fixed L, fixed dimension and compact birth/positive-gap/frame sets and sufficiently small radius. No common probability-one statement across uncountably many conditioned laws is asserted.

## 7. The smaller formal task now exposed

Here is a concrete sufficient **unimplemented theorem signature**, rather than another hypothesis equal to the desired probability estimate. Use entry coordinates `V=(R x R) x R`, z=((a,b),d), and define

    frobSq(z)=a^2+2b^2+d^2,
    eig2(z)=((a+d)/2-sqrt(((a-d)/2)^2+b^2),
             (a+d)/2+sqrt(((a-d)/2)^2+b^2)).

The target is the measure inequality

```lean
-- Proposed signature only. No proof body, axiom, or kernel status is asserted.
theorem sym2_positive_spectral_domination
    (mu : Measure ((Real × Real) × Real))
    (C0 c : Real) (hC0 : 0 ≤ C0) (hc : 0 < c)
    (hdom : mu ≤ volume.withDensity
      (fun z => ENNReal.ofReal (C0 * Real.exp (-c * frobSq z)))) :
    Measure.map eig2 (mu.restrict {z | 0 < (eig2 z).1}) ≤
      volume.withDensity (fun e : Real × Real =>
        if 0 < e.1 ∧ e.1 < e.2 then
          ENNReal.ofReal (Real.pi * C0 * (e.2 - e.1) *
            Real.exp (-c * (e.1 ^ 2 + e.2 ^ 2)))
        else 0)
```

The displayed `frobSq` and `eig2` are definitions to be supplied, not imported existing names. Product Lebesgue volume is intended on both sides. The inequality permits equality of the eigenvalues on the left because (4) gives zero mass there. A separate proof must establish measurability and perform the two linear coordinate changes around the polar formula; it must not interpret a zero-totalized nonintegrable Bochner integral as a finite estimate.

**Available pinned interface, actually inspected:** mathlib commit `d13f23b723b8a846827a245b89c10fc7d3f11612`, `Mathlib/Analysis/SpecialFunctions/PolarCoord.lean`, blob `053dcbf1bcd84f42dcc8273dd4afb0d87a6755e6`, already contains `lintegral_comp_polarCoord_symm`, `det_fderivPolarCoordSymm`, and `polarCoord_source_ae_eq_univ`. Its polar target is `(0,infinity) x (-pi,pi)`, exactly the convention used above. Thus d=3 does not require formalizing a general-dimensional Weyl integration theorem or constructing a measurable eigenbasis just to prove (S2).

After (S2), the residual product law, pointwise inequality (8), nonnegative product integration and Gaussian moments (9)-(10) still need Lean implementation, together with concrete source-model instantiation. The existing original `MatrixDepthTransport` may alternatively be reached by replacing the retained hard factor in (8) with the coarser U^4 factor; its already-compiled consumer then applies. The ninth-moment refinement has a different envelope, so it is NOT falsely claimed as a new fact already proved by that consumer.

## 8. Verification, review boundary and references

`test_adapter.py` first ran with no `algebra.py`: all 14 methods failed with their named missing implementations. After implementation, all 14 pass in both standard-library normal/optimized modes, with byte-identical deterministic stdout. Checks cover the 3x3 derivative determinant at rational circle points, trace/determinant/Frobenius identities, angle/volume factors, both soft terms, hard-factor and ordered-domain bounds, moment/radius algebra, Gaussian-mean square identity, exact Gamma recurrences, full normalization, weighted support, a dependent-marginal counterexample, and small-hard-eigenvalue cases. Five named altered-formula copies are rejected by the replay protocol. These are finite algebra checks, not proofs of general change of variables, Gaussian regression, measurability, or the arbitrary-real inequalities.

No local Lean executable or full repository checkout is available; direct GitHub DNS in this container failed. The published packet uses only Python's standard library. No prior accepted source, formal seal, review body, scientific flag or coefficient output is changed.

Primary sources:
- P and its congruence erratum at the source cut above.
- Existing `CapI4.lean` at f4079f65, as identified in section 1.
- Exact pinned mathlib polar-coordinate source identified in section 7; current public documentation was used only for discovery, not to substitute a new library version.

Consensus was attempted in this pass and returned a rate-limit error. No Consensus paper was retrieved or credited. No literature novelty claim is made. A separate mathematical reader should check the measure convention, polar multiplicity, null strata, original-law independence, order of domain extension, moment-nine exponent, separate E4 requirement, and compact-family quantifiers before disposition.
