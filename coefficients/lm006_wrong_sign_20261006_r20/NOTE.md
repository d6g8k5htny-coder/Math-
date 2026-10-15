# An outward enclosure of the actual LM006 cubic sign coefficient

Dylan Roy — delegated AI mathematical/numerical work. Actual author OpenAI /
GPT-6 Astra Pro, `r20-sign-coefficient-enclosure-20261006-1105`, pickup
Math-#358/6014879289. Scientific effect NONE; organizational-independence credit0.
This is an additive certificate candidate, not an independent review or Lean proof.

## 1. Exact coefficient and scope

Consume ONLY the coefficient formula (3)–(5),(18)–(20) of
`reviews/lm006_wrong_sign_asymptotic_20261006/NOTE.md` at immutable Math-
`64c0a203b94105f0fccbe6f8116a94e13431f84e`, Git blob
`ea914c1b8e0b8180b645f3f626e2081ab87700b9`, SHA256
`00d57d987c28ef5f2e3f6467c9e343fb60ffb3ad5806d004f245fe16914fbb61`.
Its theorem and source review are not reproved or broadened by this calculation.
The model is d=2, L=24, b=6/5, original coordinate axes, six canonical pins with
height gap r^3/6, and the FULL normalized determinant tilt. The coefficient is
for the saddle-transverse event f_yy(S)>=0, not capture, elder or persistence.

Write m2,m4 for the exact one-coordinate torus spectral moments,
delta=m4-m2^2, v=m2*delta. Under the UNTILTED Gaussian law take independent
D~N(0,v), B~N(0,v/4), Q~N(-m2*b,delta). Then

    C=p0*Gamma/z0,  Gamma=E J(D,B^2),  z0=E(Q_-)^2,
    p0=exp(-(m2*b)^2/(2delta))/sqrt(2*pi*delta),
    J(d,u)=int_0^(d_+) (d-u-t)_+ (u-t)_+ dt.             (1)

For u>=0, J=0 when u=0 or d<=u. Otherwise, with l=min(u,d-u),
M=max(u,d-u), J=l^2*(3M-l)/6. The denominator z0 is NOT conditioned on
the sign event. There is no extra pin density, six-variable Jacobian, or
factor from treating B as the full derivative rather than its half.

**Computed enclosure.** The algorithm proved below, evaluated at grid2048,
gives inclusive outward decimal bounds

    0.001305365507 <= C_(24,6/5) <= 0.001338803452.       (2)

In particular 0.00130<C_(24,6/5)<0.00134. Other retained intervals are

    0.021429752302 <= Gamma <= 0.021978691924,
    3.230978535287 <= z0 <= 3.230978535288,
    0.196810857928 <= p0 <= 0.196810857929.               (3)

These decimal endpoints are rounded OUTWARD from exact rational values. The
interval width is principally the rectangle discretization bound, not a
floating-point error estimate. RESULTS.json is the exact author-run output;
its independently_reviewed=false is a historical execution annotation, not a
substitute for a later source-bound review. The certificate requires the proof
and implementation to be read together. A passing script alone is not a proof.

This does not bound the o(r^3) remainder or supply a numerical radius. One
cannot assert nu_r(E)<=0.001338803452*r^3 for a specified positive r from (2).
No arbitrary-axis, nonproduct, other-period, birth/gap-mark or dimensional
extension is included. No claim of numerical-method novelty is made.

## 2. Exact periodic inputs, not planar substitution

The second consumed source is ONLY the covariance definition in P §1:
`imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md`,
blob `dfed3b8d318a3ab1950957f393307733a4bef3f2`, read at
`a952d25d11400561da10324dbb40e42c9da4ea6c`. Its one-coordinate image sum is

    k(t)=sum_n exp(-(t+24n)^2/2)/H,
    H=1+2 sum_(n>=1) exp(-288n^2).

Gaussian image tails permit termwise differentiation. Put
A2=2 sum_(n>=1)(24n)^2 exp(-288n^2),
A4=2 sum_(n>=1)(24n)^4 exp(-288n^2). Direct second/fourth derivatives give

    m2=1-A2/H,  m4=3+(A4-6A2)/H.                        (4)

For every n>=1, (24n)^4-6(24n)^2>0, so m4>=3. H>=1. The positive rational
Taylor sum sum_(k=0)^400 288^k/k! is greater than10^125, checked exactly by
image_bounds(). Hence exp(-288)<q=10^-125 and exp(-288n^2)<=q^n. Differentiating
the convergent geometric series gives

    sum n^2 q^n=q(1+q)/(1-q)^3,
    sum n^4 q^n=q(1+11q+11q^2+q^3)/(1-q)^5.

Consequently the code bounds 1-m2 by2*24^2 times the first expression and
m4-3 by2*24^4 times the second. Both are less than10^-118. For simpler
subsequent rational arithmetic we deliberately WIDEN to epsilon=10^-24:

    m2 in[1-epsilon,1],  m4 in[3,3+epsilon].             (5)

No equality with planar moments is used. Monotone positive interval operations
then enclose delta=m4-m2^2 and v=m2*delta. All resulting lower variances are
strictly positive. Actual infinite-periodic contributions are contained by
(4)–(5); there is no finite-frequency truncation presented as the whole field.

## 3. Elementary real-function enclosures

Every quantity used to form (2) is an integer or fractions.Fraction. There are
no float operations, decimal transcendental library calls, quadrature packages,
or random samples in enclose.py. The fixed-point denominator is S=10^36.

For rational x>=0, a=isqrt(floor(x*S^2)) gives a/S<=sqrt(x). If (a/S)^2=x,
the upper endpoint is a/S; otherwise it is(a+1)/S. Products and reciprocals
of positive interval endpoints are carried out exactly before outward rounding.

For exp(-x), divide x by2 until y<=1/8. The alternating Taylor polynomial of
degree23 is a lower bound, and degree22 is an upper bound. Terms decrease.
First round the lower down and upper up to units1/S, then square each interval
as many times as the initial divisions, rounding each squared lower down and
upper up. Monotonicity on nonnegative numbers preserves enclosure. Intersection
with[0,1] is valid because0<exp(-x)<=1. The case x=0 is exact.

For pi use Machin's identity pi=16atan(1/5)-4atan(1/239). To check it, the
angle theta=atan(1/5) has tan(2theta)=5/12 and tan(4theta)=120/119. The
subtraction formula gives tan(4theta-atan(1/239))=1. The angle lies in(0,pi/2):
theta<pi/8 because1/5<sqrt(2)-1, and atan(1/239)<theta. Thus it equals pi/4.
For each arctangent the81-term alternating sum ending positive is upper;
the80-term sum is lower. Subtracting endpoints in the correct directions
bounds pi. The two reciprocal square-root endpoints give1/sqrt(2pi).

For0<=z<=1,

    Phi(z)=1/2+(1/sqrt(2pi)) sum_(k>=0)
              (-1)^k z^(2k+1)/(2^k k! (2k+1)).           (6)

This follows by integrating the Gaussian exponential series on[0,z]. Its
terms decrease; k=0..33 gives a lower sum, k=0..32 an upper sum. The positive
normalizing factor is bounded by the previous pi/root construction. The
implementation explicitly rejects z outside[0,1]; the parameter intervals
in(5) put a/sqrt(delta) strictly inside this domain, with a=m2*b>0.
The DLMF7.6.1 power series was consulted as classical context; the alternating
remainder and all coefficients used here are stated explicitly, not imported
from a floating library or unread numerical table.

Finally

    z0=(a^2+delta) Phi(a/sqrt(delta))
                    +a sqrt(delta) phi(a/sqrt(delta)).  (7)

All factors are positive. Bound the argument by its a/delta endpoints, use
monotonicity of Phi and decreasing phi on nonnegative arguments, then combine
positive lower/upper products. p0=phi(a/sqrt(delta))/sqrt(delta) is treated
similarly. This encloses the means as well as covariances; it does not assume
normalizer invariance under a mean shift.

## 4. Rectangle extrema and Gaussian density bounds

By symmetry in B and since J=0 for D<=0,

    Gamma=2 int_0^infty int_0^infty J(d,beta^2)
                               p_D(d) p_B(beta) d beta dd. (8)

For fixed u, J(d,u) is nondecreasing in d by its original nonnegative integral.
For fixed d>=0 it is symmetric under u -> d-u on[0,d], zero outside that
interval, increasing up to d/2 and decreasing thereafter. For0<=u<=d/2,
J=d*u^2/2-2*u^3/3, whose u derivative is u(d-2u)>=0; symmetry proves the rest.
Thus on d in[d0,d1], u in[u0,u1], all nonnegative,

    J_lower=min(J(d0,u0),J(d0,u1)),
    J_upper=J(d1, clamp(d1/2,u0,u1)).                     (9)

This includes intervals crossing either zero-support threshold or the maximum.
It is not sufficient to sample only the two corners for the UPPER bound.
The global maximum is J(d,d/2)=d^3/24.

If a centered normal variance lies in[vlo,vhi] with vlo>0, its density at
x>=0 is bounded below by

    exp(-x^2/(2vlo))/sqrt(2pi*vhi)

and above by exp(-x^2/(2vhi))/sqrt(2pi*vlo). Each actual centered normal
density decreases in x>=0. Use the lower density at the right cell endpoint
and the upper at the left, and round the two density values outward to1/S.
For B the variance interval is[vlo/4,vhi/4], NOT[vlo,vhi].

Use[0,R]x[0,T], R=12,T=4, with n subdivisions in each variable. On a cell,
u0=beta0^2,u1=beta1^2. Multiply (9), the two density bounds, the exact area
(R/n)(T/n), and symmetry factor2. Summing nonnegative lower/upper cell bounds
gives a lower/upper integral over the rectangle without a derivative-error or
floating-quadrature hypothesis.

The optimized implementation uses common coordinate denominator qcoord=2n^2:
d_i=2Rin/qcoord, u_k=2T^2 k^2/qcoord. The extra2 includes d/2 exactly.
_jnum returns l^2(3M-l) in these integer units. Multiplication by
2RT/[n^2*6*qcoord^3*S^2] restores the integration area, J denominator, and two
densities. test_full_rectangle_sum_against_fraction_reference independently
uses actual Fraction coordinates and the explicit cell formula, not those units.

## 5. Explicit omitted-domain tails

Since J(d,u)<=d_+^3/24, the union of D>R and |B|>T bounds the omitted region.
Double-counting their overlap only enlarges the upper bound. Integration by
parts in the centered Gaussian density of variance v gives

    E[D^3;D>R]=(v R^2+2v^2)p_D(R),
    E[D_+^3]=2v^2 p_D(0).

Also for T>0, x/T>=1 on x>=T and integration of x*p_B(x) gives

    P(|B|>T)<=2(v/4)p_B(T)/T=v*p_B(T)/(2T).

Independence of B,D under the UNTILTED law in (1) therefore bounds the tail by

    tail <= (vR^2+2v^2)p_D(R)/24
            +[2v^2 p_D(0)/24]*[v p_B(T)/(2T)].           (10)

Use vhi in the polynomial prefactors and the uniform density upper bounds
from section4. This bounds all parameters in(5), not just v=2. The computed
upper tail of Gamma is less than0.000000001492544918. Lower Gamma omits
the tail; upper Gamma ADDS it. Removing it from the upper sum is not certified.
Divide only after multiplying Gamma by the positive p0 interval, using the
opposite z0 endpoint for each quotient. This produces(2).

## 6. Execution, sensitivity, and review boundary

Reproduce with Python standard library only:

    python -B -S test_enclosure.py
    python -B -O -S test_enclosure.py
    python -B -S enclose.py --grid 2048
    python -B -O -S enclose.py --grid 2048

The first12 methods failed for the missing implementation, with no import/harness
errors. The final15 methods pass in both modes; three later checks add independent
unrounded exponential sums,221 root-split exact J integrations, and an independent
64-cell Fraction-coordinate sum. Other coverage includes sqrt/outward rounding,
Gaussian density parameter variation, image tails, boundary/rectangle cases,
normalizer positivity, grid nesting and CLI/input guards. A few loose binary64
math.exp/math.erf comparisons occur ONLY in the test file as sanity screens;
no certified endpoint depends on them or on its printed decimal pi sanity check.

Eight isolated wrong-source variants were actually run through all15 tests in
both modes and rejected by intended assertions, zero errors: doubled J; omitted
B variance/4; omitted symmetry2; omitted upper tail; omitted normalizer; inward
sqrt; inward exponential upper rounding; and a weakened image-exponential bound.
Those variants and raw test-first/failure streams are retained in the owner
execution delivery, not substituted into this production checker. Grids512,1024,
2048 are nested enclosure diagnostics. Agreement/convergence of grid outputs
alone is NOT the certification argument; the extrema and tails above are.

On the frozen source, normal and optimized grid2048 stdout is byte-identical to
RESULTS.json. No hosted workflow is added here; existing general CI does not
run this standalone checker or formalize this numerical proof in Lean. A new
nonauthor read must inspect the interval directions, cells, infinite tails,
periodic inputs, source mapping and actual execution before accepting this
candidate. The prior #358 theorem review does not cover these new files.

No original mathematical/Lean/gate/workflow/status files are changed. #358's
separate integration is not held by this follow-through. Existing source-admission,
provenance and full-field scientific obligations remain governed separately.
