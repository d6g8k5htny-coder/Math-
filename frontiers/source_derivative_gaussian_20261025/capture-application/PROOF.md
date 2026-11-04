# Actual canonical weighted capture defect at fixed finite period

OpenAI/Codex author-side conventional application, 26 October 2026. The
binding scope is `SOURCE_ACTUAL_CANONICAL_CAPTURE_APPLICATION.md`, frozen in
commit `9cbc87f`. This is a new application of completed results, not a new
Lean ODE proof or a scientific-status change. Exact source identities and
the evidence being reused are in `REUSED_SOURCES.json`.

## 1. The theorem and the specified law

Fix a literal finite real `L != 0`, a real height `b`, and write

    Ω = SmoothSample 2 L,
    f_ω = smoothSourceField 2 L ω,
    Q_(r,b) = sourceSmoothLaw hL r b,
    P_(r,b) = sourceSmoothWeightedLaw hL r b.

The physical period is `ell=|L|`. A negative `L` causes no change to the
period lattice: every literal sine/cosine mode is `ell`-periodic. No
replacement source law, truncation, zero-mode removal, or amplitude
renormalization is made. The endpoints, in a physical chart, are

    M_r=(-r/2,0),             S_r=(r/2,0),
    t_(r,b)=(b,b-r^3/6,0,0,0,0).

The raw order in `t_(r,b)` is `(fM,fS,fxM,fxS,fyM,fyS)`. Let

    H_(r,b)={ω : rawPins L r ω=t_(r,b)},
    W_r(ω)=|det Hess f_ω(M_r) det Hess f_ω(S_r)|
       ·1{Hess f_ω(M_r) negative definite}
       ·1{det Hess f_ω(S_r)<0}.

Thus `P_(r,b)` is the literal normalized `W_r` density over the specified
canonical Gaussian `Q_(r,b)`, on its positive-normalizer interval.

On the full raw pin fiber, require the two strict Hessian types and a
nonzero projection of `d_r=M_r-S_r` onto the positive eigenspace of the
saddle Hessian. Orient that eigenspace by

    e_u = P_u(Hess f(S_r)) d_r / |P_u(Hess f(S_r)) d_r|,
    e_u · d_r > 0.                                             (1)

Let `A_r` be the event that this selected unstable branch of the exact
physical gradient-ascent flow on `R^2/(ell Z^2)` converges to `M_r`.
Assign failure outside the full pin fiber or this strict, nonorthogonal
domain. This is exactly the fail-closed selected-branch convention in
GP-DER-197. It does not choose the opposite branch or insert capture into
the weighting law.

There exist `C>=0` and

    0<δ<=min(1,ell/8)

depending on the fixed `L,b`, such that for every `0<r<δ`, `P_(r,b)` is a
probability, `A_r` is a Borel event on the actual coefficient carrier, and

    P_(r,b)(A_r^c) <= C r^3,
    P_(r,b)(A_r)   >= 1-C r^3.                                  (2)

There is also a stronger measurable event `A_r^lift`: the same local
unstable branch, lifted from the specified saddle `S_r` to `R^2`, converges
to the literal lift `M_r`, rather than a translated lift. The same bound
holds for `(A_r^lift)^c`. Globally `A_r^lift ⊆ A_r`; equality of these
events is not needed or asserted. On the sufficient event below the
entire certified trajectory stays in a single physical chart and both
capture statements hold.

With the separate conventional geometric Campbell/Palm application
specified in §7, (2) applies to its named canonical Gaussian/Rice mark
version at this prescribed position/height pin. It is not an assertion
about every modification of a Palm kernel on intensity-null parameters.

## 2. Completed actual-source inputs and the radius interval

Put

    Γ_k(ω)=sourceDerivativeMajorant L k ω,
    R(ω)=sourceGammaRadius L ω=1+sum_(k=0)^5 Γ_k(ω),
    q(ω)=sourceQ L ω=f_yy(0),
    K0=4096,
    ε0=1/(1024 K0),
    ε*=ε0/5^5=1/(1024·4096·5^5),
    Kcap=2 K0 5^5+10=25600010.

The completed `I4SourceWeightedCurvature.sourceWeightedCurvature_bound`
has only the actual inputs `hL`, fixed `b`, `K>=0` and `ε>0`. Apply it
with `K=Kcap`, `ε=ε*`. It supplies `C>=0` and `δ_curv>0`, with
`δ_curv<=1`, such that for `0<r<δ_curv`, `P_(r,b)` is a probability and

    P_(r,b)(B_r) <= C r^3,
    B_r={ε*<r R^5} ∪ {q>=-Kcap r R^5}.                         (3)

Both sets in (3) are Borel by the proved actual measurability of `R,q`.
There is no scalar-density, moment, source decomposition, normalizer, or
desired event-bound premise left to postulate here.

The completed `sourceEndpoint_parameter_limits` gives a positive
`δ_pin` on which the actual confluent pin covariance is invertible.
The every-target identities `rawPinKernel_prescribed` and
`rawPinKernel_pin_fiber` then give

    Q_(r,b)(H_(r,b))=1.                                         (4)

This retains the exact nonzero height and the exact cubic gap. Since
`P_(r,b)<<Q_(r,b)` by its literal density, it also gives
`P_(r,b)(H_(r,b))=1`. The event `H_(r,b)` is Borel, by
`rawPins_measurable`. These assertions are made on the derived interval,
not at every positive radius. Also reuse
`sourceSmoothPalm_estimates hL b`: on a positive interval `δ_Palm`,
the literal normalizer is finite and bounded below by `c0 r^2` for
some `c0>0`. Choose

    δ=min(δ_curv,δ_pin,δ_Palm,1,ell/8).                          (5)

Every entry of this finite minimum is positive. This also provides
the positive-normalizer interval used by the separate canonical
geometric mark application in §7.

## 3. Discharge of the deterministic LM004 hypotheses

Fix `0<r<δ` and a deterministic sample `ω∈H_(r,b)` satisfying

    r R^5<=ε*,              q<=-Kcap r R^5.                     (6)

Set

    U=(f_xxy,f_xyy,f_yyy,f_xxxx,f_xxxy,f_xxyy,f_xyyy,f_yyyy)(0),
    R0=1+sum_i |U_i|,
    F*=1+|U_0|/8+r|U_4|/48,
    W=F*/(K0 R0^5),
    σ=4R0W,       ρ=8R0W,       κ=1/(16R0).

The midpoint curvature `q` is excluded from `U,R0`. The actual completed
source comparison proves `1<=R0<=5R`. Hence (6) gives

    r R0^5<=ε0,
    q/r<=-(2K0 R0^5+2R0).                                     (7)

For the second implication, use `r>0`, `R>=1`, and

    2K0 R0^5+2R0 <= (2K0 5^5+10)R^5.

These are precisely the LM001 regularity and curvature hypotheses;
they are also the completed `sourceQuartic_cutoff_tolerance` and
`sourceQuartic_curvature_threshold` applications.

The actual field to which LM004 is applied is

    F_r(X)=r^(-2) grad f_ω(rX)
          =grad_X [r^(-3) f_ω(rX)].                              (8)

It is smooth on all of `R^2`, is a gradient field in the Euclidean
metric, and therefore has symmetric Jacobian. The exact raw pins give
`F_r(S)=F_r(M)=0` at `S=(1/2,0)`, `M=(-1/2,0)`. Let `P_r` denote the
literal LM001 polynomial `sourceQuartic L r ω`, with the raw `U` above
and `s=q/r`. The completed source result is

    max(sup_(|X|<=2)|F_r(X)-P_r(X)|_2,
        sup_(|X|<=2)|DF_r(X)-DP_r(X)|_op) <=3r^2 Γ_5.             (9)

The norm in (9) is the MAX convention, with Euclidean value norm and
induced Euclidean operator norm. The Lean pointwise uniform maximum
bound yields (9) by taking the two suprema. The Pi-norm coordinates in
the source do not replace either of these norms; the completed theorem
has already supplied the explicit finite-dimensional bridges.

The same cutoff in (6) yields the required adaptive bound, with no
additional fifth-derivative event:

    12K0 R0^4 r^2 Γ_5
       <=12K0 5^4 r^2 R^5
       <=12K0 5^4 r ε*
       =3r/1280 <1.

Since `F*>=1`, this implies

    3r^2 Γ_5 <= R0 W/4.                                       (10)

The exact certificate chart can be chosen as the closed Euclidean
ball of radius two. The completed size estimate gives
`R0W<=1/2048`, so `ρ<=1/256` and `W<=1/2048`. The cone segment up to
`ξ=σ` lies in the saddle ball because
`σ sqrt(1+κ^2)<2σ=ρ`. The strip, central rectangle, both endpoint
balls and all their boundaries therefore lie in this chart. The cone
exit section is exactly the right central section
`X=1/2-σ`. The left central section lies strictly in the maximum ball:

    sqrt(σ^2+W^2)=W sqrt(16R0^2+1)<8R0W=ρ.

These geometric joins are unchanged LM001 facts, also explicitly
checked in the scoped LM004 review. The open neighborhood required by
LM004 is available because (8) is defined smoothly on the whole plane.

Apply the exact LM004 v1.1 robustness implication, frozen body SHA256
`d43179f3abfd7e93f988725f3b89a5826cc71e0fa04840f65c7f93f3359d0f87`.
Its LM001 Q1–Q5 inputs are completed dependency facts. The implication
has the native different-family Claude `PASS_SCOPED` at
`Math514/6406504239`. All its actual application hypotheses have now
been discharged in (7)–(10), rather than added to the final theorem.

Consequently `S` is a nondegenerate saddle, `M` is a strict maximum of
the potential in (8), and the selected unstable direction points into
`ξ=1/2-X>0`. Its projection toward `M-S=(-1,0)` is strictly positive.
The branch exits the invariant cone through `ξ=σ`, enters the strip
with `|Y|<=W/4`, crosses the central rectangle in finite forward time,
enters `B(M,ρ)`, and converges exponentially to `M`.

For clarity, the retained actual margins are strip flux
`F_Y(X,W)<=-1+R0W/4<0` and
`F_Y(X,-W)>=1-R0W/4>0`, central drift
`F_X<=-(11/4)R0W<0`, and contraction
`lambda_min(-DF_r)>0.44` in `B(M,ρ)`. These follow from reviewed
LM004; `SourceQuarticCaptureAlgebra` separately proves the actual
strip and central gates. Gates alone are not being used as an ODE
or saddle-to-sink theorem.

## 4. Exact physical orientation, space and time

If `X(τ)` solves `dX/dτ=F_r(X)`, then

    x(t)=r X(rt),              dx/dt=grad f_ω(x(t)).              (11)

Thus the time change is `τ=rt`, with positive multiplier, and the
space change is `x=rX`. Equivalently the equation for `X` in physical
time is `dX/dt=rF_r(X)`. Also

    DF_r(S)=r^(-1) Hess f_ω(S_r).

Positive scalar multiplication preserves Hessian signs, eigenspaces
and forward-time orientation. A vector pointing into increasing `ξ`
has negative first component, so its inner product with both `M-S`
and `M_r-S_r` is positive. More explicitly, for the orthogonal positive
spectral projector of a symmetric saddle Hessian,

    [P_u d/|P_u d|] · d = |P_u d|^2/|P_u d| = |P_u d|>0.

There is exactly one unit vector on that one-dimensional eigenspace
with positive inner product with `d`. LM004's cone direction has
`e_X<0`, hence has that positive inner product for `d=(-1,0)`.
Its image under (11) therefore equals the projector-oriented unit
direction (1), rather than merely some direction at the same saddle.
The connected unstable branch selected by the two rules is the same.
Hyperbolicity or the endpoint types alone would not select this sign.

Every certified point lies in `|X|<=2`; by (5), its physical lift
lies in `|x|<=2r<ell/4`. This ball injects into the physical torus.
Uniqueness of the local unstable manifold and of ODE solutions
identifies the branch in (11) with the selected physical branch,
first locally and then for its full certified forward trajectory.
It converges to the literal `M_r` in the covering plane, and hence
also on the torus. No continuation outside the certificate chart
or identification with a different saddle branch is needed.

We have proved the pointwise deterministic statement

    H_(r,b) ∩ {rR^5<=ε*, q<=-Kcap rR^5}
            ⊆ A_r^lift ⊆ A_r.                                 (12)

In particular the strict complement gives

    H_(r,b) ∩ A_r^c
       ⊆ {ε*<rR^5} ∪ {q>-Kcap rR^5} ⊆ B_r,                    (13)

and the same is true with `(A_r^lift)^c`. The larger closed one-sided
curvature event in (3) therefore covers the required failure. No
necessity claim is made for the sufficient conditions (6).

## 5. Actual Borel pullback, including the period change

Here is the missing conventional event application. Merely knowing
that the weighted `ell1` parameter space in `SourceSmoothParameterSpace`
is Polish would not prove any of the following event statements.

**Actual norm-Borel field map.** For the physical torus
`T_ell=R^2/(ell Z^2)`, use the usual `C^3` Banach norm, for example
the maximum of the suprema of the partial derivatives of order at
most three. For a finite exhaustion `I_n` of the actual countable
mode set, put

    J_(L,n)(ω)=sum_(m∈I_n) ω_m modeCoefficient(2,L,m).

This is a Borel `C^3(T_ell)`-valued function of the original carrier
coordinates: it is a finite sum of measurable real coordinates
times fixed smooth torus functions. Each mode is `ell`-periodic,
including when `L<0`. For every actual carrier sample,

    sum_m |ω_m| sum_(k=0)^3 orderModeBound(k,2,L,m) < infinity.    (14)

This is the defining all-order carrier property, using only four
of its already proved summability conditions. Each partial derivative
is an evaluation of its multilinear derivative on coordinate unit
vectors, so these same majorants dominate the stated `C^3` norm
(an equivalent Euclidean derivative norm only adds a fixed constant).
Thus `J_(L,n)(ω)` converges in the **norm** of `C^3(T_ell)` for
every `ω∈Ω`. Its limit is the literal `f_ω`, by the completed actual
derivative-series identities. A pointwise norm limit of these Borel
maps into this metric Banach space is Borel. Therefore

    J_L: Ω -> C^3(T_ell),       ω -> f_ω                       (15)

is Borel in the norm Borel structure. This is a conventional
application of the completed all-order series and norm convergence,
consistent with the reviewed finite-L `C^infinity` law admission and
the reviewed `SourceSmoothTopology` norm-Borel derivative fields.
It neither infers norm Borel measurability from finite evaluations
alone nor silently uses the product sigma algebra of a jet tuple.
The same measurable map (15) can be pushed forward under the literal
`Q_(r,b)` and `P_(r,b)`; it is not restricted to the unconditioned law.

**Reduce to the exact side-24 event space.** Put

    c=ell/24>0,       r24=r/c,       b24=b/c^3,
    (T_c f)(y)=c^(-3) f(cy),      y∈T_24.                       (16)

This is a continuous linear map `C^3(T_ell)->C^3(T_24)`.
For `|α|<=3`, its derivative is
`∂^α(T_cf)(y)=c^(|α|-3)(∂^αf)(cy)`; hence continuity follows with
finite constant `max_(0<=j<=3)c^(j-3)`. The torus map `y↦cy` is
a diffeomorphism. The exact pins transform to

    (T_cf)(M_(r24))=b24,
    (T_cf)(S_(r24))=b24-r24^3/6,
    grad(T_cf)(M_(r24))=grad(T_cf)(S_(r24))=0.                  (17)

Also `Hess(T_cf)=c^(-1) Hess f` at corresponding points and
`d_(r24)=c^(-1)d_r`. Thus the strict type and nonorthogonal
projection tests, the normalized direction (1), and its positive
orientation are exactly preserved. If `x(t)` is the physical flow,

    y(s)=c^(-1)x(s/c),       dy/ds=grad(T_cf)(y(s)).              (18)

Consequently forward convergence of the selected torus branch is
preserved, with the positive time change `s=ct`. The amplitude
factor `c^(-3)` in (16) is necessary for the cubic pin gap (17).
We do **not** claim that `(T_c∘J_L)_#Q_(r,b)` is the side-24
normalized Gaussian model. The event theorem is a Borel construction
on the entire `C^3(T_24)` pin fiber and does not require that law
identity. Our law on that space is the actual pushforward just proved
Borel. The source-to-event pullback is explicitly

    A_r=(T_c∘J_L)^(-1)(A_(r24,b24) on T_24).                    (19)

**LP, flow and convergence hypotheses.** The field-to-vector-field
map `g↦grad g` is continuous `C^3->C^2`, hence into `C^1`. The exact
pin fiber in (17) is closed, and keeps the saddle an equilibrium.
Endpoint Hessian evaluations are continuous; strict saddle and
negative-definite maximum are open conditions. For a symmetric
saddle matrix `H`,

    P_u(H)=(H-lambda_s(H)I)/(lambda_u(H)-lambda_s(H))

is continuous, so the nonzero-projection condition is relatively
open and (1) is continuous there. These are exactly the symmetry,
hyperbolicity, equilibrium and orientation hypotheses of the approved
local Lyapunov–Perron selector LCR-DER-057 v1.1. Its local continuous
positive-branch points cover this strict domain. The domain is second
countable, so take a countable cover and use the first applicable
chart to obtain a Borel branch point. Different such points on the
selected branch differ by a finite flow-time shift.

Compactness of `T_24` gives complete flow for each `C^1` field.
Finite-time parameter dependence makes
`g↦Phi(g,q,b(g))` Borel for each rational `q>=0`. The set of paths
converging to the fixed maximum is Borel, using the exact countable
test

    intersection_(k>=1) union_(N>=1)
       intersection_(q∈Q,q>=N)
          {g : dist(Phi(g,q,b(g)),M_(r24))<=1/k}.                (20)

Continuity in time extends the rational inequalities to all real
times; (20) is equivalent to convergence. The selector-independent
globalization is the preserved LCR-DER-061 v1.1 mathematical result.
Its exact-hash external-review conversion remains a separate process
item and does not undo this completed mathematical argument.

One can equivalently use hitting: around each strict maximum field,
choose a fixed sufficiently small ball on which its Hessian is
uniformly negative; this property persists on a field neighborhood.
The ball is invariant and contracting for every pinned field in that
neighborhood. A countable cover supplies such neighborhoods/balls.
On each neighborhood, capture is equivalent to entry into that ball
at some nonnegative rational time, a countable union of Borel flow
evaluation tests. This is the same event as (20).

Assigning failure outside the closed pin fiber and the relatively
open strict domain gives a Borel subset of the whole `C^3(T_24)`
space. Equations (15)–(19) prove that the actual `A_r` is Borel.
All pullback hypotheses have been discharged conventionally; there
is no residual source-field or period-scaling measurability premise
in (2).

**The literal-lift refinement.** The local LP points may, after
shrinking each field neighborhood, all be chosen in a fixed injective
coordinate ball around `S_(r24)` and lifted there from the specified
saddle lift. These lifts are Borel on the same countable strata and
lie on the same selected unstable branch in `R^2`. For a `C^3`
periodic potential, its lifted gradient and its first derivative are
globally bounded, so the lifted vector field is globally Lipschitz
and has complete flow. Finite-time dependence in the periodic
`C^1` norm follows from the same ODE theorem (or Gronwall). Apply
(20) with Euclidean distance and the literal lift `M_(r24)`.
Explicitly, writing `tilde_b(g)` for the stratum-wise lifted LP
point, `Psi(g,t,x)` for the lifted Euclidean flow, and `O24` for
the strict pin/type/nonorthogonal domain, the lifted event is

    O24 ∩ intersection_(k>=1) union_(N>=1)
       intersection_(q∈Q,q>=N)
       {g : |Psi(g,q,tilde_b(g))-(-r24/2,0)|_2<=1/k}.            (21)

Every fixed-rational flow evaluation in (21) is Borel, and its
closed Euclidean distance test is Borel. Time continuity makes
(21) equivalent to convergence to this literal maximum lift.
This makes convergence of the lifted selected branch Borel and
selector-independent, since points on this lifted branch differ
by a finite time shift. Apply (16)–(18) on the cover to obtain the
claimed Borel `A_r^lift` on the actual carrier. This refinement is
not inferred merely from torus convergence.

## 6. Outer measure first, then measurable probability

The deterministic part already supplies a separate conclusion that
does not use event Borel measurability. Let `N_r` be the actual set
of failures of either selected capture interpretation. Equation
(12) says, as an ordinary inclusion of sets,

    N_r ⊆ H_(r,b)^c ∪ B_r.

The right side is a Borel cover with `P_(r,b)` measure at most
`C r^3`, by (3)–(4). Thus the associated outer measure satisfies

    P_(r,b)^*(N_r) <= C r^3.                                   (22)

No measurability of `N_r` is used in (22). In §5 it was separately
proved that both failure sets are Borel, so their outer measures
equal their probabilities. This proves (2) and the stronger
literal-lift bound. In particular this note is claiming a measurable
probability theorem, rather than relabeling (22) as one without a
pullback proof.

## 7. The named geometric mark and the remaining boundaries

The separate actual geometric application
`geometric-palm-evidence/application/APPLICATION_PROOF.md`, SHA256
`bbf61e080cfcbaaeb78b160921943d8500fd8f1878a0109c3148ddfb446c54d2`,
derives the ordered physical maximum/saddle Campbell identity from
the already reviewed finite-original-block incidence/area theorem
and actual finite-L Gaussian admission. It derives, rather than
postulates, the canonical Gaussian/Rice probability mark kernel,
with a separate Dirac branch when its normalizer is zero. Its
pointwise raw/confluent coefficient-lift calculation identifies

    P_mark(z_r,b,b-r^3/6)=sourceSmoothWeightedLaw hL r b

at the prescribed null pin on the positive-normalizer interval.
The equality is pointwise in the target, not a use of almost-everywhere
uniqueness of regular conditional distributions. It retains the
same original coefficient sample, actual Hessian weight and exact
noncentered target; no extra pin density or power of `r` appears in
the normalized mark. Our Borel capture marks are now legitimate
coefficient-carrier integrands for that application. Hence (2)
holds for this named actual canonical geometric mark version too.

The new work here is the conventional application (12)–(22),
including the actual source-to-`C^3` pullback and the fixed-period
transport. Completed LM001, LM004, analytic-comparison, kernel,
axiom and control evidence is reused. No Lean builds, old proof
audits, kernel replays, source-hash recalculations, numerical
experiments or old tests were run. The new proof has OpenAI authorship
and still needs any required different-family source review of its
own exact bytes; that process item is distinct from the mathematics
proved above and from the already completed reviews of dependencies.

This is not a Lean selected-branch/flow theorem, a formal Kac–Rice
implementation, a global elder-pairing or once-counting result, or a
P0.2 closure. The constants are existential for each fixed `L,b`;
no uniformity in period or height and no effective accessible-radius
guarantee is asserted. No status registers or scientific labels are
changed by this note.
