# LM006 coefficient: analytic dimension reduction and a certified one-dimensional enclosure

Dylan Roy — delegated AI mathematical/numerical work. Actual author OpenAI /
GPT-6 Astra Pro, `coefficient-dimension-reduction-20261006-1340-a62c`, claim
Math-362/6017509107. Scientific effect NONE; organizational-independence credit0.
This is a new additive numerical candidate requiring its own source review.
No historical proof, numerical result, review disposition or Lean target changes.

## 1. Exact object and relation to existing work

Consume #358's coefficient definition at commit
`64c0a203b94105f0fccbe6f8116a94e13431f84e`, NOTE blob
`ea914c1b8e0b8180b645f3f626e2081ab87700b9`, in
`reviews/lm006_wrong_sign_asymptotic_20261006/`. For the fixed original-axis
periodized field d=2,L=24,b=6/5 with its six pins and gap r^3/6, it states

 C = p0 Gamma/z0,   Gamma=E[J(D,B^2)],
 D~N(0,v), B~N(0,v/4) independently,
 Q~N(-m2*b,delta), z0=E(Q_-)^2, p0=density_Q(0),
 delta=m4-m2^2, v=m2*delta,
 J(d,u)=int_0^{d_+}(d-u-t)_+(u-t)_+ dt, u>=0.              (1)

These are UNTILTED Gaussian inputs defining a coefficient of the determinant-
tilted sign probability. Independence after tilting is not asserted. This note
neither re-proves #358's limit theorem nor turns C*r^3 into a finite-r bound.
There is no numerical asymptotic remainder, radius, arbitrary orientation/mark
extension, or capture/elder/persistence conclusion.

#362's original packet `coefficients/lm006_wrong_sign_20261006_r20/` at
`1f64b8f8ee450262e0f56e6bdf9dfb37931f48c6` supplies reviewed interval arithmetic,
the actual periodic-moment enclosure and p0,z0 parameter bounds. Its five files
are unchanged on its actual landing `4fe1d6762db8faa13859c4eeda0167b3c65ac069`.
We load only its exact7215-byte enclose.py, blob
`e680ddb7aa0abd4b6aab2cac6a54c1ff28efc782`, SHA256
`157e02ee22699b4fa2efdde1894824b92b962900dbb8da9bd65acee41ae91e88`.
The same bytes are authenticated then compiled, not checked and later reread.
The parent is trusted code, not made into a hostile-code sandbox by hashing.
Leaf symlinks/nonregular files reject; hostile ancestor resolution and external
future disk immutability are not claimed. The cached module retains the actual
verified in-memory code.

#372 already refines the parent's two-dimensional rectangle sum by exact zero-
cell pruning. It has a reviewed4096 result and separately owned8192 execution.
Neither that source nor its outputs are changed, imported or re-executed here.
The present contribution integrates D out analytically, proves a uniform fourth-
derivative bound for the remaining smooth integrand, and uses Simpson's rule
with an explicit error, not agreement between grids. Gaussian truncated moments
and Simpson integration are classical methods; no general novelty is claimed.

## 2. Analytic integration over D

Write s=sqrt(v), phi for the standard normal density and T=1-Phi. For u>=0,
Tonelli gives

 g_v(u):=E_D J(D,u)
       =int_0^u (u-t) E[(D-u-t)_+] dt
       =int_u^{2u}(2u-a)[s phi(a/s)-a T(a/s)] da.           (2)

The first equality uses that the original positive parts restrict t to[0,u]
and D>u+t. In particular no factor involving B's density has entered yet.
For a=u/s, explicit integration yields

 g_v(u)=s^3/6 * {
   (4a^2+2)[phi(2a)-phi(a)]
   +(6a+4a^3)T(a) -(6a+8a^3)T(2a) }.                     (3)

An independent derivation specifies every coefficient. On u<d<2u,
 J(d,u)=(-d^3+6u d^2-9u^2 d+4u^3)/6;
on d>=2u, J(d,u)=u^2 d/2-2u^3/3; elsewhere it is zero.
The truncated Gaussian moments at threshold t, x=t/s, are

 M0(t)=T(x), M1(t)=s phi(x),
 M2(t)=s^2[x phi(x)+T(x)],
 M3(t)=s^3[(x^2+2)phi(x)].

These follow by integration by parts from phi'=-x phi. Integrating the two
polynomials over[u,2u] and[2u,infinity) with these moments simplifies to(3).
At u=0 both expressions give0. Formula(3) extends analytically across u=0,
which supplies all right derivatives used below. The clipped polynomial J
itself need not have four continuous derivatives.

By symmetry of B, retain BOTH its variance v/4 and the folding factor2:

 Gamma=int_0^infinity F_v(b) db,
 F_v(b)=2 f_B(b) g_v(b^2),
 f_B(b)=c exp(-alpha b^2), c=2/(s sqrt(2pi)), alpha=2/v.    (4)

This is an exact one-dimensional integral, not an approximation of the other
Gaussian integral by a fitted curve.

## 3. A uniform fourth-derivative bound

The following estimates hold on the COARSE range 3/2<=v<=3 and u>=0.
They apply in particular to every actual parameter in the narrower parent box.
Denote derivatives of g_v with respect to u by g',...,g''''. Then

 |g|<=1/5, |g'|<=3/16, |g''|<=3/4,
 |g'''|<=9/4, |g''''|<=29/4.                              (5)

Here is a proof, not a sampled derivative maximum. For d>0, J as a function of
u has maximum d^3/24 at u=d/2. Its first derivative has absolute value at most
d^2/8. It is C1 across its clipping thresholds, and that first derivative is
Lipschitz with constant d, since each piece has |J''|<=d. These bounds justify
differentiating the Gaussian expectation through order2 by dominated difference
quotients (or absolute continuity plus domination). Therefore

 |g|<=s^3/(12 sqrt(2pi)), |g'|<=v/16,
 |g''|<=s/sqrt(2pi),

which give the first three estimates in(5) for v<=3. Direct differentiation of
(3), remembering a=u/s, gives

 g'''(u)=4T(a)-8T(2a)-a phi(a),
 g''''(u)=[16phi(2a)+(a^2-5)phi(a)]/s.                    (6)

Because 0<=T(2a)<=T(a)<=1/2, the first two terms of g''' lie in[-2,2].
Also max_{a>=0} a phi(a)=1/sqrt(2pi e)<1/4, using pi>3,e>8/3. For g'''',
max a^2 phi(a)=2phi(0)/e, and phi(0)/s<1/3 for v>=3/2. Thus its magnitude
is less than(21+3/4)/3=29/4. Degenerate clipping endpoints do not require
exceptional-point exclusions, since g has the analytic representation(3).

The exact product/chain differentiation of(4) is

 F_v''''(b)=2c exp(-alpha b^2) * [
  (16alpha^4 b^4-48alpha^3 b^2+12alpha^2) g
 +(144alpha^2 b^2-64alpha^3 b^4-24alpha) g'
 +(96alpha^2 b^4-144alpha b^2+12) g''
 +(-64alpha b^4+48b^2) g''' +16b^4 g'''' ],                (7)

with all g derivatives evaluated at b^2. The exact rational polynomial tests
independently differentiate both(3) and exp(-alpha b^2)g(b^2), verifying every
coefficient in(6),(7). For 2/3<=alpha<=4/3,

 sup b^2 exp(-alpha b^2)<=1/(2alpha),
 sup b^4 exp(-alpha b^2)<=1/alpha^2,   c<=2/3.

These use e>2. Taking absolute values separately in(7), the bracket multiplied
by its exponential is bounded by

 52alpha^2 G0 +160alpha G1+180G2+88G3/alpha+16G4/alpha^2,

where G_j are the five constants in(5). Consequently

 sup_{b>=0,3/2<=v<=3}|F_v''''(b)|
   <=(4/3)[832/45+40+135+297+261]<1002<1100.               (8)

The deliberately rounded constant1100 is uniform on the WHOLE stated variance
range, not only at v=2. Neither this bound nor the leading coefficient is claimed
optimal. The code uses1100 without attempting a numerical derivative maximum.

## 4. Compact quadrature and a smaller support-aware tail

On[0,3] use the classical composite Simpson rule with EVEN panel count n,
spacing h=3/n. NIST DLMF3.5.7–3.5.8 gives, for F in C4,
 absolute error <=(3/180)h^4 sup|F''''|.
The assumptions were proved above. Thus

       E_n=1485/n^4                                    (9)

is a valid uniform quadrature error for every permitted v. Every evaluated
node is enclosed by rational intervals. Simpson's coefficients are positive,
so the lower and upper weighted sums enclose the exact Simpson sum, without
assuming monotonicity in v. Subtract E_n from the lower endpoint and add it to
the upper endpoint. No agreement between resolutions enters this proof.

For the omitted part |B|>3, the support condition J(D,B^2)>0 forces D>B^2>9.
Since J<=D_+^3/24 and D,B are independent BEFORE tilting,

 Gamma_tail <= (1/24) E[D^3;D>9] P(|B|>3).                (10)

Gaussian integration by parts and the two-sided Mills bound give
 E[D^3;D>9]=(81v+2v^2)f_D(9),
 P(|B|>3)<= (v/6) f_B(3).

For a parameter interval [v_-,v_+], evaluate the polynomial factors at v_+ and
use valid upper density bounds from the parent. Their product is the tail tau.
This is not a bound obtained by dropping the D>B^2 support condition. The
rectangle D in[12,13], B in[3,13/4] also has strictly positive integrand and
positive density lower bounds, proving that the omitted integral is not zero.
The tests verify its explicit lower bound is below the proposed upper tail.
The tail is ADDED ONLY to the upper Gamma endpoint.

For this parameter box, the outward decimal upper tail is

                  tau <= 0.00000000000007444285.

A fixed b cutoff therefore imposes a tail floor on eventual accuracy; increasing
n alone would not establish an arbitrarily accurate enclosure.

## 5. Exact intervals and stable treatment of the normal tail

The parent proves for epsilon=10^-24 the actual image-corrected bounds
 m2 in[1-epsilon,1], m4 in[3,3+epsilon]. Its actual parameter code computes
 delta and v=m2 delta outward, together with positive p0,z0 intervals. We use
THOSE intervals, not the nonperiodic values m2=1,m4=3. In particular v's lower
endpoint is slightly below2; claiming v>=2 would be wrong. The interval lies
inside[199/100,3], a subset of the coarse derivative domain[3/2,3].

The parent Machin/pi, nonnegative exponential, density and square-root bounds
are hash-bound prerequisites already derived/reviewed there. This note does
not transfer its predecessor's verdict to new code. New interval add/subtract/
multiply/divide operations take all appropriate endpoint extrema and round
outward at scale10^36, using integer floor/ceiling. Denominators containing0
reject. Fraction operations have no binary64 conversion on the production path.

The parent normal CDF interface only handles arguments in[0,1]. It is NOT used
outside that domain. We introduce a normal upper-tail enclosure for 0<=x<=13.
Taylor's integral remainder for exp(-y), y>=0, shows that its odd partial
polynomial is below exp(-y) and its even partial polynomial is above it for
all y>=0. This fact does NOT require that the early alternating terms decrease.
Integrating at y=t^2/2 from0 to x gives

 I_331(x) <= I(x):=int_0^x exp(-t^2/2)dt <= I_330(x),
 I_N(x)=sum_{k=0}^N (-1)^k x^(2k+1)/(2^k k!(2k+1)).       (11)

The positive term magnitudes satisfy
 t0=x, t_k/t_{k-1}=x^2(2k-1)/[2k(2k+1)].
The implementation encloses each magnitude at internal scale10^100 and adds
with alternating signs and outward endpoints. All recurrence multipliers are
nonnegative, so induction bounds every term and signed partial sum. It retains
the LOWER endpoint of the final odd sum and the UPPER endpoint of the preceding
even sum. Known I>=0 permits clipping the lower side at0. From the parent
interval for c0=1/sqrt(2pi), form

 T(x) in[1/2-c0_upper*I_upper, 1/2-c0_lower*I_lower],

intersect with the known[0,1/2], then round outward. Evaluating T on an interval
uses its monotonicity with opposite endpoints. Formula(11) and tracked rounding,
not a floating erfc call or cancellation estimate, are the certificate. Large
intermediate terms can cancel without losing enclosure because integer/Fraction
arithmetic and directed bounds are used. Extremely small tails may have lower
endpoint0; this is legitimate and not replaced by a signed negative probability.

The implementation only requires u in[0,9] and v in[199/100,3], so the largest
argument 2u/s is below13. It enforces those domains. The formula for g is evaluated
with signed interval arithmetic; intersecting with the independently proved
0<=g<=1/5 is valid and improves cancellation at small values. A cache contains
only already computed exact argument enclosures. Parent authentication uses the
same byte buffer for hashing and compilation; it provides identity, not a general
source sandbox or a guarantee against mutable ancestor directories.

## 6. Result, test history and precise exclusions

For n=1024, the two completed author commands produce the inclusive enclosure

       0.001321995248726 <= C_(24,6/5) <= 0.001321995413271. (12)

The final assembly is
 Gamma in[max(0,S_lower-E_n), S_upper+E_n+tau],
 C in[Gamma_lower*p0_lower/z0_upper,
                         Gamma_upper*p0_upper/z0_lower].

The Gamma interval is[0.021702757242874,0.021702759944149]. The quadrature
error upper is0.00000000135059963214. These displayed decimals themselves
are rounded outward, not nearest. RESULTS.json retains independently_reviewed=false
as immutable author-execution history. It is not changed automatically by a
later technical review or CI pass.

There are1025 interval-valued node evaluations, each using analytic Gaussian
moments and bounded series, rather than millions of two-dimensional cells.
This is an algorithmic count, NOT a controlled wallclock benchmark against the
other implementations or hardware. Bounds nest within the prior2048/4096/8192
records as a corroboration; such nesting is not the proof of(12). No source or
execution of #372 is claimed by this packet.

Reproduction from this directory, with the unchanged parent at its repository path:

    python -B -S test_oned.py
    python -B -O -S test_oned.py
    python -B -S oned.py --panels 1024
    python -B -O -S oned.py --panels 1024

The initial12 methods produced12 intended missing-implementation assertions in
each mode and zero errors. After implementation those12 passed; additional
independent coefficient/assembly and truncated-moment controls make15 final
methods. Tests include independent unrounded335/334 integral-series enclosures,
exact symbolic third/fourth derivatives and all12 product-derivative coefficients,
exact rational Simpson identities, signed outward operations and B scaling,
the nonzero tail and opposite-normalizer attachment. A few math.erfc and midpoint
comparisons are explicitly binary64 SANITY checks in tests only, not premises of
the certificate. Tests neither numerically maximize the fourth derivative nor
replace the written proof by a grid.

Eight isolated source variants each fail the same complete15-method suite in
normal and optimized modes, with intended assertion sets and zero errors:
missing symmetry, wrong B variance, halved integrated kernel, wrong Simpson
weights, omitted upper tail, wrong normalizer endpoint, inward interval rounding,
and wrong lower-error sign. These check the implemented proof contract; an
omitted tiny tail can leave a decimal interval containing the answer by accident,
which would not make that proof-contract change sound. No result is learned from
the variant under test. The combined campaign's outer60-second tool deadline
occurred after15 completed records; its final optimized variant was completed
separately. Original streams and the interruption remain retained, not labeled
as an uninterrupted16-process run.

Existing general CI does NOT automatically run these standalone files. No new
workflow, Lean target, full local checkout, full historical-archive replay, or
formal independent alignment is claimed. Direct local GitHub access was unavailable;
the recovered parent was authenticated to native source identities. A new
nonauthor numerical/source read must check this reduction, bounds, signed series,
exact code, domains and actual executions. #362's source review does not cover
this successor. General publication CI, if successful, remains separate.

Classical references checked: NIST DLMF3.5(ii), equations3.5.7–3.5.8
(https://dlmf.nist.gov/3.5#ii) for composite Simpson and its C4 remainder;
DLMF7.6(i) (https://dlmf.nist.gov/7.6#i) for error-function power-series context.
The signed finite truncation directions needed here were proved directly above.
No new general quadrature/stability principle, complete literature review,
finite-r probability or numerical radius, non-axial product decomposition, or
full-field capture/elder/persistence theorem is asserted.
