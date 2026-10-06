# LM006: the common-regression rate input and its endpoint consequences

Dylan Roy — delegated AI mathematical work. Actual author: **OpenAI / GPT-6
Astra Pro**, `lm006-common-regression-rate-20261006`. Author-side additive
application; scientific effect **NONE**; organizational-independence credit **0**.
This does not revise a historical source, supply a Lean proof, or constitute
its own nonauthor review.

## 1. What is reused, and what is supplied here

The remote-window source [R], §§2–4, already constructs a common conditional-
field coupling with error O(r²), explicitly including the endpoint-only law,
and already obtains normalized-weight error O(r). Those methods and rates
are **not new here**. The general Gaussian prior-plus-regression update also
has extensive prior literature; [W] is external context, not a proof premise.

The precise interface supplied here is a common coupling of **all six LM006
scaled endpoint coordinates**, including both mixed derivatives, with
`e_r=(E||X_r-Y||²)^(1/2)=O(r)` and every finite Lp error O(r). We verify its
hypotheses in the exact fixed periodic field by the integral kernels of [E],
not by differentiating a singular target-covariance square root. We then
apply the already established inequalities of [N], [T], and [S]. In
particular [S]'s conditional `r e + e^4` bound becomes an actual-field
O(r²) bound for its **saddle-transverse sign event**, not for elder failure.
This is an application/interface result, not a new general coupling principle
or the first conditional r² sign estimate.

Fix d=2, L=24, birth b=6/5 and axial sites M=(-r/2,0), S=(r/2,0). Let f be the
centered, variance-one Gaussian field with the exact covariance of [P] §1,
not its nonperiodic approximation. The six physical observations are

    (f(M), f_x(M), f_y(M), f(S), f_x(S), f_y(S))
       = (b,0,0,b-r³/6,0,0).

Q_r denotes their canonical continuous Gaussian regression law. Work on
`0<r<=r_*`, where one sufficiently small **fixed** r_*>0 is chosen below,
with r_*<=1 and r_*<24. No compatible unequal-height pins are claimed at a
torus alias. All constants may depend on this fixed model, frame and pins;
no numerical radius or evaluated coefficient is provided.

**Application.** There is a common Gaussian coupling X_r,Y of the actual
six-coordinate endpoint law under Q_r and its contact law such that, for
every fixed finite p>=1,

    ||X_r-Y||_Lp <= C_p r,    sup_r E||X_r||^p < infinity.       (A)

Here `Y=(-1,1,-a/2,a/2,Q,Q)` has the conditional law from [E], not an arbitrary
vector on that plane. With the physical typed weight W_r, define
`Z_r=E_Qr W_r`, `z_r=Z_r/r²` and `z0=E[(Q_-)²]`. Then

    z0>0,    E|T_r(X_r)-T_0(Y)| <= C r,
    |z_r-z0| <= C r,    z_r >= z0/2,                           (B)
    d_BL(nu_r,nu0) <= C_BL r,
    nu_r{c_+>=0} <= C_sign r².                                (C)

The measures nu are the normalized determinant/type tilts of the endpoint
laws; d_BL uses |phi|<=1 and Lipschitz constant<=1 as in [T]. The sign event
is `f_yy(S)>=0`. It is not the maximum's already-excluded transverse sign,
and it is not identified with any full-field capture or persistence event.
These conclusions do not assert endpoint TV convergence; [D]'s TV=1 result
is compatible with them.

## 2. One unconditioned Hilbert-space model and the exact pins

Use H=L² of the original unconditioned probability space. Put
`F(x)=f(x,0)`, `H_y(x)=f_y(x,0)`, `Q(x)=f_yy(x,0)`.
A sufficient local regularity assumption is that F is H-valued C5, H_y is
H-valued C3, and Q is H-valued C1 on a neighborhood of [-h_*,h_*], h_*>0.
Restrict r_* further to r_*<=2h_* so every kernel evaluation stays there.
Assume joint Gaussianity and positive-definiteness of the contact pin Gram.
Section 5 verifies these assumptions for the actual field.

Use [E]'s exact equivalent pin frame P_r=(P0,...,P5), writing h=r/2:

    P0=(F(-h)+F(h))/2,       P1=(F'(-h)+F'(h))/2,
    P2=(H_y(-h)+H_y(h))/2,
    P3=(F'(h)-F'(-h))/r,     P4=(H_y(h)-H_y(-h))/r,
    P5=(12/r²)[P1-(F(h)-F(-h))/r].

Its inverse in [E] (2.2) recovers the six raw observations, so its exact
conditioning target is

    d_r=(b-r³/12,0,0,0,0,2),    d_0=(b,0,0,0,0,2).            (1)

The frame limit is J=(f,f_x,f_y,f_xx,f_xy,f_xxx)(0). In particular its last
pin is **2**. This frame is not confused with [R]'s different, equivalent
ordering and divided-difference row.

Before conditioning define the adjusted six-vector V_r by [E] (3.2):

    A_±=(F''(±h)-P3)/r,     B_±=(H_y'(±h)-P4)/r,
    C_±=Q(±h),             V_r=(A_-,A_+,B_-,B_+,C_-,C_+).

On the pin target P3=P4=0 these are exactly the four divided Hessian entries
and two unscaled transverse Hessian entries. Subtraction before taking the
unconditioned limit is essential. The exact kernels on I=[-1/2,1/2] are

    P3=integral_I F''(ru)du, P4=integral_I H_y'(ru)du,
    P5=6 integral_I (1/4-u²)F'''(ru)du,
    A_-=-integral_I(1/2-u)F'''(ru)du,
    A_+= integral_I(u+1/2)F'''(ru)du,
    B_-=-integral_I(1/2-u)H_y''(ru)du,
    B_+= integral_I(u+1/2)H_y''(ru)du.                        (2)

These are the Hilbert-space identities already proved in [E], not Taylor
formulas assumed under a varying conditional law. Their limit is

    V_0=(-F'''(0)/2,F'''(0)/2,-H_y''(0)/2,H_y''(0)/2,Q(0),Q(0)).

## 3. Quantitative pin and endpoint convergence

Let D_j=sup_x||F^(j)(x)||_H, E_j=sup_x||H_y^(j)(x)||_H and
J_1=sup_x||Q'(x)||_H on the fixed interval. These are finite by continuity.
Taylor's formula with its Hilbert-valued integral remainder and cancellation
of the odd term in each centered average give

| Coordinate | H-error from its contact value |
|---|---|
| P0 | D2 r²/8 |
| P1 | D3 r²/8 |
| P2 | E2 r²/8 |
| P3 | D4 r²/24 |
| P4 | E3 r²/24 |
| P5 | D5 r²/40 |

For P5, the kernel mass is 1 and its second moment is 1/20; the Taylor
factor 1/2 gives 1/40. The analogous constant for the uniform kernel is
1/24. Hence, with the Euclidean vector norm in L²,

    ||P_r-J||_L² <= C_P r²,
    C_P²=(D2/8)²+(D3/8)²+(E2/8)²
                  +(D4/24)²+(E3/24)²+(D5/40)².             (3)

The endpoint kernels need only first-order remainders. Both absolute first
moments are `integral_I(1/2-u)|u|du=1/8` (the plus kernel has the same value).
Thus each A error is <=D4 r/8, each B error <=E3 r/8, and each C error
<=J_1 r/2. Consequently

    ||V_r-V_0||_L² <= C_V r,
    C_V²=2(D4/8)²+2(E3/8)²+2(J_1/2)².                       (4)

The first-order endpoint displacement is not generally second order even
though the centered pin frame is. The finite model in §7 explicitly tests
that distinction.

## 4. The means and residuals in the same coupling

All unconditioned vectors are centered. Set

    G_r=Cov(P_r), C_r=Cov(V_r,P_r), K_r=C_r G_r^{-1},
    X_r=V_r+K_r(d_r-P_r),
    Y=V_0+K_0(d_0-J).                                      (5)

Only the **pin** covariance is inverted. No inverse, inverse square root, or
Lipschitz square-root map is assumed for the singular six-endpoint covariance.
The Gaussian residual V_r-K_r P_r is orthogonal to P_r, hence independent
of it. Its covariance is the Schur complement, and its mean after adding
K_r d_r is K_r d_r. Thus (5) realizes the canonical conditional marginal
for every prescribed finite pin value, not conditioning on a positive-
probability event. It is an artificial common coupling realizing the physical
marginals, not a claim that one physical field is simultaneously conditioned
to all the different pin events.

Here are explicit finite constants showing that the rate is not inferred
merely from continuity. Put p0=||J||_L², v0=||V_0||_L²,
pb=p0+C_P, vb=v0+C_V, and lambda=lambda_min(G_0)>0. For r<=1, covariance
Cauchy--Schwarz gives

    ||G_r-G_0||op <= alpha r²,  alpha=C_P(2p0+C_P),
    ||C_r-C_0||op <= beta r,    beta=C_V pb+v0 C_P.

Choose r_* small enough that alpha r_*²<=lambda/2 (no constraint is
needed from this inequality if alpha=0). Then

    ||G_r^{-1}||op<=2/lambda,
    ||G_r^{-1}-G_0^{-1}||op<=2 alpha r²/lambda²,
    ||K_r||op<=k_b:=2 vb pb/lambda,
    ||K_r-K_0||op<=k_d r,
    k_d=2 beta/lambda+2 v0 p0 alpha/lambda².                  (6)

The inverse difference follows from the exact resolvent identity; the bound
for K uses C_rG_r^{-1}-C_0G_0^{-1}. Define m_r=K_r d_r and
R_r=V_r-K_rP_r, with R_0=V_0-K_0J. Formula (1) gives

    ||m_r-m_0|| <= C_m r, C_m=k_d||d_0||+k_b/12,
    ||R_r-R_0||_L² <= C_R r,
    C_R=C_V+k_d p0+k_b C_P.                                (7)

In the second line split the difference into V_r-V_0,
-(K_r-K_0)J and -K_r(P_r-J). The last term is actually second order.
The first line retains the deterministic mean change; a covariance bound
alone would not imply it. Since R_r-R_0 is centered,

    e_r²=E||X_r-Y||²=||m_r-m_0||²+E||R_r-R_0||²
          <=(C_m²+C_R²)r²=:C_e² r².                        (8)

The difference is Gaussian, possibly singular. A Gaussian vector with mean
m and centered covariance A has an Lp norm bounded by
`||m||+c_(p,6) sqrt(tr A)` for every finite p>=1, by its PSD square-root
representation and the standard Gaussian norm moment. Applied to the
*difference law*, (8) proves (A). This use of a square root supplies a moment
bound; it does not estimate how square roots vary with r.

Uniform marginal means satisfy `||m_r||<=M:=k_b(||d_0||+1/12)`, including
r=0. Projection only reduces the covariance, so
`||Cov(X_r)||op<=vb²=:Lambda`. The same bounds hold for Y. All finite
moments are uniformly bounded. For any fixed r the jointly Gaussian pair
(X_r,Y) can, if desired, be represented with a common standard Gaussian of
at most twelve coordinates; that representation preserves (8). We do not
claim O(r) variation of the particular symmetric six-by-six covariance roots.

## 5. Verification in the actual periodized field

[P] §2 gives positive weights

    p_n=exp(-2pi²|n|²/24²)/sum_j exp(-2pi²|j|²/24²), n in Z².

They satisfy every polynomial spectral-moment condition. In particular
`sum_n p_n(1+|(2pi/24)n|^10)<infinity`. Differentiating the Fourier symbols
in weighted L², with dominated convergence, gives mean-square derivatives
through order five and continuity at that order. This supplies the H-valued
regularity of §2, all D_j/E_j/J_1 used above, and joint Gaussianity of the
derivatives and their integrals. No uniform pathwise derivative bound is
assumed in place of these mean-square facts.

The six contact derivative monomials in J are distinct. With every p_n>0,
a zero-variance linear combination would give a polynomial vanishing on
Z², hence identically zero. Thus G_0 is positive definite, supplying lambda.
Appending f_yy(0) gives seven distinct monomials, so its Schur complement
is strictly positive. Under J=d_0 the variable Q=f_yy(0) therefore has a
nondegenerate real Gaussian law. In particular `0<z0=E[(Q_-)²]<infinity`.
It is the actual conditional torus law, not an inserted N(-b,2) law.

Formula (5) at zero gives the stated contact vector with
`(a,Q)` distributed as `(f_xxy(0),f_yy(0))` conditional on `J=d_0`. Formula (2) and P3=P4=0 give the
actual positive-r physical endpoint vector. This checks both ends of the
same-coupling interface before applying any tilted-law inequality.

## 6. Consequences, with the previously proved inequalities credited

Use [N]'s exact `W_r=r² T_r(X_r)` and `T_0(Y)=(Q_-)²`. Its pointwise
polynomial-growth Lipschitz estimate, integrated as in [T] (10), yields

    Delta_r=E|T_r(X_r)-T_0(Y)| <= B e_r+D r <= C_D r,
    B=sqrt(2048(M^6+480Lambda³)), D=8(M^4+48Lambda²),
    C_D=B C_e+D.                                           (9)

This is an absolute L1 estimate, not cancellation of signed expectations.
It proves (B), after reducing r_* so C_D r_*<=z0/2. The physical lower
normalizer is then `(z0/2)r²`; the normalized one is z0/2. The qualitative
O(r) normalizer conclusion already exists in [R] (11); this is its explicit
six-coordinate compatibility and does not replace historical finite-band data.

For H=(E[(Q_-)^4])^(1/2), [T] (5) gives

    d_BL(nu_r,nu0) <= min(2,(2 C_D+H C_e)r/z0).              (10)

Its Gaussian moving-event tail also satisfies
`kappa(t)<=sqrt(3) H C_e² r²/(z0 t²)`. A same-set probability rate for a
general Borel set still needs its own limiting boundary margin. No arbitrary-
event or endpoint-total-variation conclusion follows from (10).

Finally [S] (8) is the separately proved direct typed-sign estimate. In its
notation K2<=M²+6Lambda=:C2 and K6<=32(M^6+480Lambda³)=:C6. Since the
coupling constructed here is Gaussian and has the exact contact identities,
its conclusion gives

    nu_r{c_+>=0}
       <= (2/z0)[sqrt(2 C6) C_e r²
                        +sqrt(105 C2) C_e^4 r^4/8].         (11)

This supplies the concrete-field e=O(r), moment, and positive normalized-
floor inputs that [S] deliberately retained. For r<=1 the right side is
O(r²), proving (C). No independence between error coordinates or endpoint
Hessians is introduced. No small-r exponent is claimed sharp. [S]'s earlier
negative-part predecessor and its other author-side consequences retain their
own attribution; the contribution here is verification of the actual coupling
input, not a repeated sign proof.

## 7. Exact finite diagnostics and audit exclusions

`regression_rate_check.py` represents the finite polynomial field
`sum_(i,j) Z_(i,j) x^i y^j/(i! j!)` with independent standard normal Z,
using horizontal degrees 0..5, 0..3, 0..1 for transverse degrees 0,1,2.
It is **not** the stationary periodic field. No sampling is used: means,
regression factors and covariances are exact Fraction matrices. Its ten-test
suite checks exact raw pins, physical/adjusted equality after conditioning,
residual orthogonality, the Schur identity, contact rank two, positive-radius
rank six, seven rational-radius pin/endpoint error bounds, and two controls
showing why mean and common-factor terms cannot be dropped. Its nonzero
linear endpoint error illustrates why pin O(r²) is not endpoint O(r²).

Run from this directory with Python's standard library only:

    python -B -S test_regression_rate.py -v
    python -B -O -S test_regression_rate.py -v
    python -B -S regression_rate_check.py
    python -B -O -S regression_rate_check.py

Named mutants `omit-mean`, `covariance-only`, `reverse-gap`, and
`quadratic-endpoints` must exit1 with their distinct `REGRESSION_RATE_FAIL`
messages; an unknown label must exit2. These finite controls support the
algebra and expose inadmissible shortcuts. The Hilbert and spectral arguments
in §§2–6, not the test grid, are the application proof. No local Lean, complete
repository replay, or automatic hosted execution of this standalone checker
is claimed. A future general CI success is not such an execution receipt.

No original proof, historical review, flags, scientific register, workflow,
formal package or sibling branch is changed. Full P0.2/Palm/elder-failure/
Cap/IBA2/global closure, all-mark or dimension uniformity, numerical constants,
and independent full-package formal alignment remain outside this note.
The four-file application requires its own nonauthor review before eligible
integration; parent reviews are not transferred to it.

## Sources (immutable interfaces; metadata is not a mathematical premise)

[P] `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md`,
Math- commit `5e027afcae8c7bd42a6df8ae2025f82105b3e586`, blob
`dfed3b8d318a3ab1950957f393307733a4bef3f2`, §§1–2: exact model and positive
spectrum/finite-jet independence. No broader parent theorem is imported.

[E] `reviews/lm006_endpoint_extension_20261005/NOTE.md`, commit
`e31b6ad8356e0760c8a7fb6e816ff640c45176c9`, blob
`551aa563562bc88a19e33d146259c03aa2d318f6`, §§1–4 and 6: exact pins,
adjusted coordinates, Hilbert kernels and contact identification.

[R] `frontiers/remote_window_20260924/PROOF.md`, commit
`f4c33a98a982d50aa490e49ce9327c755682527c`, blob
`b383bfcc88ec4ad497dff01fb6640e429ba24a84`, §§2–4, especially (5),(11):
existing common-regression rate and normalized-weight precedent. Its remote
mean-measure TV is not endpoint-law TV; its remote-count theorem is not used.

[N] `reviews/lm006_normalizer_stability_20261005/NOTE.md`, commit
`5e027afcae8c7bd42a6df8ae2025f82105b3e586`, blob
`5790aaa0332bd8e79b276be1577e4c5f3502eed6`, §§2–5: typed identity and moment
bounds. [T] `reviews/lm006_tilted_endpoint_law_20261005/NOTE.md`, commit
`ecafa5206c528b0c662ea0bcbb26938681251aa5`, blob
`6633cdf0bfee55e2fc2046176effbf44634454b3`, §§2–4: absolute-weight L1,
normalized-density, BL and moving-event inequalities.

[S] `reviews/lm006_typed_sign_suppression_20261005/NOTE.md`, commit
`1dfe801eb61a8335a2e42b886fca9b000fb3598c`, blob
`9015971fa03f44ae99d410facc6f3d8c26cdc945`, §§3–5, especially (8): the
reviewed conditional sign inequality. Its original PR #325 review does not
cover this new application. [D] `reviews/lm006_positive_radius_density_20261006/NOTE.md`,
commit `b154cd0074798850bfafe2c0f7e433707d93403f`, blob
`a6d5209a64d37b3ea28cb7dd64d92888a74acfe1`, cited only for the compatible TV
obstruction, not used to prove the rate.

[W] James Wilson et al., *Efficiently sampling functions from Gaussian process
posteriors*, PMLR 119, 10292–10302 (2020),
https://proceedings.mlr.press/v119/wilson20a.html . Primary publication metadata
and abstract were checked in this session. Its decomposition motivates
context only; no unread theorem is invoked and no new general method is
claimed. The proof of the regression marginal in §4 is self-contained.
