# Compact positive cubic gaps: actual capture and a joint Borel mark

OpenAI/Codex author-side conventional addendum, 26 October 2026. The binding
brief is `SOURCE_COMPACT_MARK_CAPTURE_RICE.md`, frozen at
`8d64490df8620b749ba2f224da535eeb6016c2d0`. The preceding canonical capture
application remains unchanged at `117534e809819d028ee1e7197d321d606acd86e9`.
Exact reused inputs and their evidence are recorded in `REUSED_SOURCES.json`.
This unit owns the deterministic and event join; the affine-target analytic
numerator is a separate author unit.

## 1. Statement on the original physical field

Fix the literal finite `L!=0`, put `ell=|L|`, and retain the original source
carrier `Ω=SmoothSample 2 L`, original Gaussian coefficient law and literal
field `F_ω=smoothSourceField 2 L ω`. Fix

    0<k0<=k1<infinity,
    D=max(1,1/(6k0)),
    K0=4096,
    epsilonStar=1/(1024·4096·5^5),
    Kcap=25600010,
    epsilon=epsilonStar/D^5,
    K=6k1 Kcap D^5.                                            (1)

Any larger fixed `K` also works. Define the original, unscaled source radius
and its conservative all-frame enlargement by

    R(ω)=1+sum_(j=0)^5 Γ_j(ω),       Rsharp(ω)=8R(ω),

where `Γ_j=sourceDerivativeMajorant L j`. These are the same sample
functionals used in the analytic numerator, before any local amplitude
operation. Let `z∈T_ell=R^2/(ell Z^2)`, `e∈S^1`,
`n=(-e_2,e_1)`, and let `Q_e=[e n]∈SO(2)`. For

    0<r<deltaDet=min(1,ell/8),   b∈R,   k∈[k0,k1],
    M=z-(r/2)e,                 S=z+(r/2)e,
    q(ω,z,e)=partial_n^2 F_ω(z),

take the actual raw six-pin target

    (F(M),F(S),F_e(M),F_e(S),F_n(M),F_n(S))
          =(b,b-k r^3,0,0,0,0).                               (2)

Directional and Cartesian gradient zero pins are equivalent. The actual
directional confluent transform of (2) is exactly

    p_(r,b,k)=(b-k r^3/2,0,0,0,0,12k).                          (3)

Here the first coordinate is the height average, the next two are gradient
averages, the next two gradient divided differences, and the last is
`12r^-2[(F_e(S)+F_e(M))/2-(F(S)-F(M))/r]`. Thus the last coordinate
in (3) follows literally from (2), with no target or covariance limit.

On the pin fiber, use the strict domain where `Hess F(M)` is negative
definite, `Hess F(S)` has one positive and one negative eigenvalue, and
`P_u(Hess F(S))d!=0`, with `d=-re` in the global flat tangent trivialization.
Orient the saddle's positive eigenline by

    u=(P_u(Hess F(S))d)/|P_u(Hess F(S))d|,
    u·d=|P_u(Hess F(S))d|>0.                                   (4)

Let `A(ω,z,e,r,b,k)` mean that the selected connected unstable branch of
the **original physical gradient-ascent flow on `T_ell`** converges to
`M`. Assign failure outside the pin fiber or this strict nonorthogonal
domain. This mark is jointly Borel in the original coefficient sample
and all the displayed finite parameters. It is a torus capture mark;
no convergence to a specified covering-plane lift is asserted here.

The deterministic implication is

    exact pins (2),   r(Rsharp)^5<=epsilon,
    q<=-K r(Rsharp)^5             ==> A.                        (5)

It is uniform in all midpoints, directions, heights and `k∈[k0,k1]`.
Consequently, on the exact pin fiber,

    A^c ⊆ {epsilon<r(Rsharp)^5}
                 ∪ {q>-K r(Rsharp)^5}
        ⊆ B={epsilon<r(Rsharp)^5} ∪ {q>=-K r(Rsharp)^5}.         (6)

These are original-field events. The potential normalization in the proof
is a deterministic operation on this same sample, not a replacement
Gaussian prior or a claim of rotational invariance.

## 2. Normalize the local cubic gap, with all constants

The chart

    (s,t) -> z+s e+t n

is used only locally on the physical torus. Its pullback to `R^2` is
well-defined without choosing a lift of `z`, by periodicity. Define

    h_(ω,z,e,k)(s,t)=F_ω(z+s e+t n)/(6k).                       (7)

The pullback is smooth on `R^2`. It need not be periodic in the two
coordinate axes of this local frame. No such periodicity is used.
The pins (2) give

    grad h(-r/2,0)=grad h(r/2,0)=0,
    h(r/2,0)-h(-r/2,0)=-r^3/6.                                (8)

This is the exact cubic normalization needed by the completed
pin-preserving comparison and LM004.

In the source Pi norm, `||Q_e||<=sqrt(2)`. Therefore, for `0<=j<=5`,

    ||D^j h||_Pi <= ((sqrt(2))^j/(6k)) Γ_j
                  <= (8/(6k)) Γ_j.

Use the nonnegative derivative majorants

    G_j=(8/(6k))Γ_j,
    Rh=1+sum_(j=0)^5 G_j=1+(8/(6k))(R-1).

Every Euclidean unit direction has Pi norm at most one, so these also
control the directional derivatives required in the completed scalar
Taylor estimates, with the same explicit component/operator bridges.
Since `D>=1`, `1/(6k)<=D` and `R>=1`,

    Rh<=1+8D(R-1)<=8DR=D Rsharp.                               (9)

The normalized midpoint curvature is exactly

    qh=h_tt(0)=q/(6k).                                        (10)

Thus the original good event in (5), with the fixed constants (1), gives

    r Rh^5 <=D^5 r(Rsharp)^5<=epsilonStar,                      (11)

and, since `0<k<=k1`,

    qh<=-(K/(6k))r(Rsharp)^5
       <=-Kcap D^5 r(Rsharp)^5
       <=-Kcap r Rh^5.                                       (12)

These calculations check both proposed factors: the regularity factor is
`D^5`, the curvature factor includes `6k1 D^5`, and the physical source
radius is `Rsharp=8R` throughout. Neither the value `12k` in the target
nor the factor `6k` in the normalization has been dropped.

## 3. Instantiate the completed comparison and reviewed robustness

The deterministic portion of the completed actual pin-preserving
comparison uses only smoothness, the derivative majorants and the exact
pins (8). Its scalar Peano/Taylor argument is therefore applicable to
the actual local pullback (7). This is not an invocation of a source-law
theorem for a new Gaussian model. To identify that deterministic content,
write

    U_h=(h_sst,h_stt,h_ttt,h_ssss,h_ssst,h_sstt,h_sttt,h_tttt)(0),
    R0=1+sum_i |(U_h)_i|,
    Fstar=1+|(U_h)_0|/8+r|(U_h)_4|/48,
    W=Fstar/(K0 R0^5),
    P_h=the literal LM001 pin-preserving polynomial
         with U=U_h and s=qh/r,
    V_(h,r)(X)=r^-2 grad h(rX).

The imported deterministic estimates, in their exact norms, are

    R0<=1+3G_3+5G_4<=5Rh,
    ||V_(h,r)-P_h||_(MAX C1, closed Euclidean ball2)
                                          <=3r^2 G_5.           (13)

The norm in (13) is the maximum of the supremum Euclidean value error
and the supremum induced Euclidean operator error. Its proof is exactly
the completed symmetric pin5 Peano cancellation, degree-three gradient
Taylor expansion, pin-forced low coefficients and explicit finite-dimensional
norm conversion. In particular the axial cubic of `h` is within
`G_5 r^2/40` of `2`; it is the normalized potential (7), rather than
the original cubic jet near `12k`, that supplies this coefficient.
The polynomial is the pin-preserving LM001 polynomial, not the ordinary
uncorrected Taylor polynomial.

Equations (11)–(13) imply the exact LM001 hypotheses

    r R0^5<=1/(1024K0),
    qh/r<=-(2K0 R0^5+2R0).                                    (14)

For the second, `2K0 R0^5+2R0<=Kcap Rh^5` uses `R0<=5Rh` and
`Rh>=1`, exactly as in the completed source comparison. For the adaptive
tolerance, `G_5<=Rh`, `r<=1` and (11) give

    12K0 R0^4 r^2 G_5
       <=12K0 5^4 r^2 Rh^5
       <=12K0 5^4 r epsilonStar
       =3r/1280<1.

Since `Fstar>=1`,

    3r^2G_5<=R0 W/4.                                         (15)

The field `V_(h,r)` is a smooth Euclidean gradient, namely the gradient
of `r^-3 h(rX)`, with symmetric derivative and exact zeros at
`M0=(-1/2,0)`, `S0=(1/2,0)`. The completed LM001 geometry has
`R0W<=1/2048`, `rho=8R0W<=1/256`, `sigma=4R0W`,
`kappa=1/(16R0)`. Its cone, strip, central rectangle, endpoint balls
and boundaries are inside the radius-two ball. The cone section is
the central rectangle's right section, and its left section lies inside
the maximum ball since `sqrt(sigma^2+W^2)<rho`.

Apply the exact reviewed LM004 v1.1 implication at frozen body SHA256
`d43179f3abfd7e93f988725f3b89a5826cc71e0fa04840f65c7f93f3359d0f87`.
The closed Q1–Q5 facts, (14), exact pins, gradient symmetry, common
chart and the precise adaptive MAX-C1 tolerance (15) discharge every
hypothesis. Its native different-family scoped review is
`Math514/6406504239`; it is reused, not replayed.

LM004 gives the local selected branch pointing into increasing
`xi=1/2-X_1`: cone exit, invariant strip entry, finite central transit,
entry into the contracting maximum ball, and exponential convergence to
`M0`. All of this branch's certified forward trajectory stays in the
radius-two scaled chart. Its maximum and saddle types are strict.

## 4. Physical flow and the precise selected sign

For the normalized local field,

    V_(h,r)(X)=(6k r^2)^-1 Q_e^T grad F_ω(z+rQ_eX).

If `dX/dtau=V_(h,r)(X)`, its physical image is

    x(t)=z+rQ_e X(6kr t),          dx/dt=grad F_ω(x(t)).         (16)

The positive time change is `tau=6kr t`, not `rt` after the new
amplitude normalization. Both the amplitude and the chart rotation
in (16) act on the original sample. Physical Hessians satisfy

    DV_(h,r)(S0)=(6kr)^-1 Q_e^T Hess F_ω(S) Q_e.

Its positive/negative eigenvalue signs are unchanged. The positive
spectral projectors obey

    P_u(DV_(h,r)(S0))=Q_e^T P_u(Hess F_ω(S)) Q_e.               (17)

The displacement `d=-re` is the image of `(-r,0)` under `Q_e`.
For the orthogonal projector of a symmetric saddle Hessian,

    (P_u d/|P_u d|)·d=|P_u d|>0.

There is exactly one unit vector on its positive eigenline with this
positive inner product. LM004 selects the vector with negative first
component, since it points into increasing `xi`. Its image under
`Q_e` has positive inner product with `-re`; by (17) it is exactly
(4). Thus the connected unstable branch, including its sign, agrees
with the branch used in the physical capture mark. Hyperbolicity or
the endpoint types alone would not establish this agreement.

Since `r<ell/8`, the image of the radius-two scaled chart lies in the
injective ball of physical radius `2r<ell/4` around `z`. ODE uniqueness
identifies its entire certified trajectory with the selected physical
torus branch. Its convergence to `M0` gives convergence to `M`.
This proves (5)–(6). No property of a globally rotated lattice or an
unproved far-field continuation is used.

## 5. Joint Borel mark with moving endpoints

Let `X=C^3(T_ell;R)` with its norm Borel structure and let

    P=T_ell × S^1 × (0,deltaDet) × R × [k0,k1],
    eta=(f,z,e,r,b,k)∈X×P.

This product is a separable metric space. The maps to `M(eta),S(eta)`
are continuous on the original torus, and `d(eta)=-re` is continuous
in its canonical flat tangent trivialization. Joint moving-point
evaluation of `f`, `grad f` and `Hess f` is continuous in the `C^3`
topology. Hence the exact pin set `H⊂X×P` specified in (2) is closed
relative to this parameter domain. Negative-definite maximum and
nondegenerate saddle are relatively open conditions. On the saddle
set the positive spectral projector is continuous, using

    P_u(H)=(H-lambda_s(H)I)/(lambda_u(H)-lambda_s(H)).

The nonzero-projection test is open, and formula (4) is continuous
on it. Denote the resulting relatively open subset of `H` by `O`.
Thus `O` is Borel and second countable. No uniform hyperbolicity
margin over all fields is required for this event construction.

**A local selector when the saddle moves.** Around any `eta0∈O`,
translate the local torus chart with the actual saddle:

    u -> S(eta)+u,             |u|<a<ell/4,
    V_eta(u)=grad f(S(eta)+u).

The addition is torus addition; it requires no global coordinate
section for `z` or `S`. The equilibrium is now the fixed point `u=0`
on `H`. The map `eta↦V_eta` is continuous into `C^1` on a fixed
small chart: uniform convergence of `grad f,Hess f`, together with
uniform continuity on the compact torus, controls both derivatives
as `S(eta)` moves. Its derivative is a symmetric Hessian; its saddle
linearization is hyperbolic, and the translated orientation (4) is
continuous near `eta0`.

These are precisely the hypotheses of the approved symmetric local
Lyapunov–Perron selector, LCR-DER-057 v1.1. Apply it to this continuous
parameter family with fixed recentered equilibrium. It supplies,
after shrinking a relative neighborhood `U` of `eta0`, a continuous
positive local unstable point in the fixed chart. Translate this
point back by `S(eta)` to obtain a continuous torus point
`beta_U(eta)` on the branch selected by (4). This is an application
with continuous finite parameters added to the field parameter,
not a new global rotation theorem.

Choose a countable such cover `(U_j)` of `O`, and disjoint Borel strata

    E_1=U_1,        E_j=U_j minus union_(i<j)U_i.

Setting `beta(eta)=beta_(U_j)(eta)` on `E_j` gives a jointly Borel
selected point. All allowed selectors choose points on the same
positive connected unstable branch. Those points lie on one flow
orbit and differ by a finite time shift, so convergence to the
specified maximum does not depend on this countable cover.

**Complete flow and moving target.** The original vector field
`grad f` is `C^1` on the compact original torus. Its flow
`Phi(f,t,x)` is complete and depends continuously on `(f,t,x)` for
finite time, in the `C^1` vector-field topology supplied by `C^3`
potentials. Therefore for each rational `q>=0`,

    eta -> dist(Phi(f,q,beta(eta)),M(eta))

is Borel on `O`. The exact countable characterization is

    A_X = O ∩ intersection_(m>=1) union_(N>=1)
              intersection_(q∈Q,q>=N)
       {eta : dist(Phi(f,q,beta(eta)),M(eta))<=1/m}.             (18)

Continuity in time extends each rational-time bound to every real
time beyond `N`. Conversely convergence implies these rational-time
bounds. Thus (18) is exactly convergence of the selected branch to
the moving maximum, and is Borel. Assigning failure outside `O`
gives a Borel mark on the entire product `X×P`. The countable
globalization and selector-independence mathematics are the reused
LCR-DER-061 v1.1 construction; its exact-hash external conversion
remains separate from its completed mathematical proof.

**Pull back the actual coefficient sample.** The preceding published
capture application already proved the actual norm-Borel map

    J_L: Ω -> C^3(T_ell),       omega -> F_omega.

Its proof used original finite Fourier sums, the carrier's all-order
absolute summability, norm convergence in `C^3`, and the actual
derivative-series identity. That completed result is reused unchanged.
The product map `(omega,parameters)↦(J_L(omega),parameters)` is
measurable into `X×P`; the latter's Borel structure equals its
product Borel structure because its factors are second countable.
Taking the preimage of (18) proves the asserted **joint** Borel
mark on `Ω×P`. The original `Rsharp` is measurable, and the moving
directional scalar `q=Hess F_omega(z)[n,n]` is jointly measurable
by the same field map and continuous evaluation. Thus the full
pin set, the good event in (5) and the obstruction `B` in (6) are
jointly Borel as well.

This proof does not rotate the source into an axis-periodic field
space, assume the source is rotationally invariant, or infer event
measurability from Polishness alone. It constructs the event on
the original torus and identifies every actual pullback hypothesis.

## 6. The geometric Rice mark and the analytic join

For a short ordered physical pair `(x,y)`, the unique short
displacement `v` from `x` to `y` varies continuously off the diagonal
when `0<|v|<deltaDet`. Write

    r=|v|,       e=v/r,       z=x+v/2.

For raw heights `(u,vh)` set `b=u`, `k=(u-vh)/r^3`, and restrict to
`k∈[k0,k1]`. These maps are continuous on that short-pair domain.
Composing with (18) proves that noncapture is an actual Borel
field/pair/height mark in the original geometric Campbell identity.
No choice of a global lifted midpoint is necessary. This step is
what allows a jointly parameterized Rice integrand rather than only
separately measurable fixed-parameter probabilities.

Let `Q_(z,e,r,b,k)` be the canonical full-carrier Gaussian posterior
for the unchanged source and raw target (2), equivalently confluent
target (3). Let `W_(z,e,r)` be its **original physical** strict
maximum/saddle product of Hessian determinants. The existing
all-frame source construction and its affine-target extension give
full support on (2), at every target, on a common covariance interval.
Consequently (6) gives

    E_Q[W 1_(A^c)] <= E_Q[W 1_B].                              (19)

This is an unnormalized inequality. The deterministic operation (7)
does not change `W`, the posterior, or the raw density in (19).
In particular no power of `6k` is inserted into the physical Rice
weight or its probability law by the normalization used for LM004.

The completed separate compact-mark affine-target numerator proof at
`/workspace/scratch/compact-mark-rice-numerator/PROOF.md`, supplied source
SHA256 `2dd31febe3db93390a4bd53e4ce0242359a26428faefe28b0c68d3c46c63f19d`,
proves the actual all-frame estimates for this same `Q`, `W`, `Rsharp`,
`q` and fixed constants (1). Take the minimum of its radius interval and
`deltaDet`; this common interval is independent of `z,e,b,k`. On it,

    E_Q[W 1_B]
       <=r^5[N17(1+|b|)^17+N19(1+|b|)^19],
    p_raw,6(z,e,r; b,b-kr^3,0,0,0,0)
       <=Cd r^-5 exp(-c b^2).                                (20)

Applying the proved (19) to these completed estimates yields the true noncapture
Rice density envelope

    p_raw,6 E_Q[W 1_(A^c)]
       <=Cd[N17(1+|b|)^17+N19(1+|b|)^19] exp(-c b^2).           (21)

The right side is integrable in `b`, uniformly in `z,e,k,r` on the
stated intervals. It is also integrable over the compact torus,
direction circle and compact `k` interval. Its constants are those
of the affine-target unit with the fixed `epsilon,K` in (1); they
need not equal the earlier axial constants. The actual canonical
Gaussian/Rice mark version is the one derived by the separate
geometric Campbell application, via its pointwise coefficient
posterior. No assertion about arbitrary null-parameter versions is
made.

The density in (21) is with respect to the original physical
`dx dy du dvh` parameter measure, evaluated at the displayed
parameters. Its raw-to-confluent density multiplier remains
`12/r^5`; the four gradient-row frame changes have determinant
of absolute value one. Neither the local amplitude operation nor
simply evaluating at a gap relation is a further density change.
If these variables are later actually changed, the separate
Jacobians are `dx dy= r dz dr dtheta` and, at fixed `r`,
`du dvh=r^3 db dk`. Their product is `r^4`, rather than an
extra factor in (19)–(21). No measure on a gap hypersurface is
created by evaluation alone.

In particular the actual pair Campbell measure restricted to selected
noncapture, `0<r<a`, `k∈[k0,k1]`, all birth heights and all midpoint/frame
parameters, has mass at most

    [vol(T_ell)·2pi·(k1-k0)/5]
       ·integral_R Cd[N17(1+|b|)^17+N19(1+|b|)^19]exp(-c b^2)db
       ·a^5                                                     (22)

for every `a` below this common radius. This uses the companion's
short-domain Campbell extension by actual finite original coefficient
minors and a countable cover, and the genuine `r^4` parameter Jacobian.
It is a local ordered critical-pair statement, with no unordered-pair
factor and no conversion from capture to elder or from pairs to bars.

## 7. Scope and evidence boundary

The new mathematical work in this unit is (5)–(6), its checked
amplitude/radius/curvature factors, the physical branch and time
identification (16)–(17), and the moving-endpoint joint Borel mark
(18) and its actual-source/Rice pullback. The compact-mark target
and analytic numerator in (20) are separately owned; their exact
artifact is identified in the companion manifest rather than
silently attributed to this unit. No normalizer floor uniform in
height was needed or claimed.

M-ward saddle-to-maximum capture is not identified with an elder
pairing event. This proof supplies neither an older component on
the other branch nor a global once-counting argument. The existing
elder-versus-capture gap remains separate. No parent/P0.2 closure,
Lean ODE theorem, formal Kac–Rice theorem, new independent-review
credit, or scientific-status change follows.

The original Fourier prior, earlier published application, Lean
sources and all shared metadata remain unchanged. Completed
applicable mathematical verification, exact dependency identities
and scoped reviews are reused under `/workspace/AGENTS.md`; no
old builds, kernel replays, axiom audits, controls, source hashes
or mathematical checks are rerun. This addendum's own scoped
review remains a separate process requirement.
