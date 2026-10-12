# D2: the sharp joint-mass Schur floor reduces to one scalar minimum

Object: D2-JOINT-MASS-SCHUR-20261006-r6.
Dylan Roy — delegated AI work. Actual author: OpenAI / GPT-6 Astra Pro,
`canonical-joint-mass-schur-20261006-r6`, pickup Math-#328/6016666735.
**NEW AUTHOR-SIDE MATHEMATICAL CANDIDATE; independent source review pending.**
Scientific effect NONE; organizational-independence credit 0. Prior sources and
reviews are exposed. No earlier source, review, status, premise or flag changes.

## 1. What is additional, and what is not

#326 is the primary source for the common moment floors under squared-radius
mass lower bounds. #328 gives the conservative upper-moment-free Schur bound.
Part B of #328 comment6008747995 gives a better bound from an independent lower
input pair; comment6016072968 reviews that exact observation, and separate PR371
is its source-publication route. None of those verdicts reviews this note.

The question left outside those scopes is the *joint* constraint: the smallest
second moment and smallest fourth-moment gap need not occur in one law. Here the
exact lower envelope of the feasible moment pairs is computed. This reduces the
optimal all-direction Schur constant over the full prescribed probability-law
class to a compact one-variable minimum and supplies an attaining law. A concrete
example has an exact algebraic minimizer and a rational outward certificate.

The residual square identity is elementary variance decomposition, not a claim
of inventing a general inequality. No global literature novelty is asserted.
This is not a consolidation of the earlier packets or a prerequisite for their
integration. It is not a Gaussian/Palm covariance identification or field result.

## 2. Probability class and exact scalar expressions

Fix real numbers p,q>0, P=p+q<=1, and distinct u,v>0. Let Y be a nonnegative
measurable random variable on a probability space satisfying

    Prob(Y=u)>=p, Prob(Y=v)>=q, E[Y^2]<infinity.          (2.1)

Equivalently one may take Y=X^2 with E[X^4]<infinity. A sixth moment is not needed
for this Schur-only statement. It is not a tau/Delta theorem with a dropped
sixth-moment premise. Set

    s=E[Y], g=E[Y^2]-s^2, a=pu+qv, c=a/P,
    w=1-P, g0=pq(u-v)^2/P.                              (2.2)

The original mass lower bounds, not necessarily actual atom masses, are p,q.
Since u!=v, the specified atom events are disjoint. We will prove s>=a>0,g>=g0>0.
For x=s^2 and t in the closed interval [0,1/4], define

    D0=x(g+x), D1=g(g+4x)/4, N=xg(g+2x),
    D(t)=(1-4t)D0+4tD1, S(t)=N/D(t),
    F0(x,g)=g(g+2x)/(g+x),
    F1(x,g)=4x(g+2x)/(g+4x).                             (2.3)

These are the exact existing D2Schur numerator/denominator expressions after
m2=s,m4=g+s^2. They are scalar expressions. Their identification with an actual
conditional covariance is not supplied by this note. All denominators below
are positive in the stated domain; no totalized division at zero is used.

## 3. Exact feasible lower variance curve

Suppose 0<P<1. Let mu be the law of Y and subtract the prescribed atom masses:

    rho=mu-p delta_u-q delta_v.

This is a nonnegative measure of total mass w, even when mu has larger masses
at u or v. Its first moment is s-a>=0 and its second moment is finite. Put
z=(s-a)/w. Expansion of the nonnegative square integral gives

    integral (y-z)^2 d rho
      = E[Y^2]-pu^2-qv^2-(s-a)^2/w >=0.                (3.1)

Consequently

    g >= h(s):=pu^2+qv^2+(s-a)^2/w-s^2
              =g0+(P/w)(s-c)^2,   s>=a.               (3.2)

For the last equality use pu^2+qv^2=g0+a^2/P and w=1-P.
Thus s>=a>0 and g>=g0>0 follow without using an earlier result as an assumption.

For EVERY finite s>=a equality in (3.2) is realized by the probability law

    mu_s=p delta_u+q delta_v+w delta_((s-a)/w).         (3.3)

The residual radius is nonnegative. Repeated atom locations simply combine
masses and still satisfy (2.1). Equality in (3.1) means rho is concentrated at z,
because a nonnegative integrable square has integral zero only when it vanishes
rho-almost everywhere. This is also a characterization of lower-envelope laws.
The construction has finite moments of every order.

At s=a, h(a)=g0+wa^2/P>g0; at s=c, h(c)=g0 but c>a. Thus when w>0 no law attains
both s=a and g=g0. This joint obstruction concerns s and g, not the already
separate g and Delta extremizers in #326/#328.

If P=1, rho has mass zero, mu=p delta_u+q delta_v, s=a=c and g=g0. Formula (3.2)
with division by w is NOT used. This case is retained separately throughout.

## 4. Exact sharp all-direction lower constant

Both endpoints D0,D1 and N are positive. Since D(t) is a convex interpolation,

    min_(0<=t<=1/4) S(t)
      =N/max(D0,D1)=min(F0(s^2,g),F1(s^2,g)).           (4.1)

The minimum is attained at t=0 when D0>=D1, and at t=1/4 when D1>=D0.
Equality of the denominators makes every t equivalent. Endpoint inclusion is
material; no bound is asserted outside [0,1/4].

Both Fi are STRICTLY increasing in each positive coordinate. For X>=x>0,
G>=g>0, the exact differences (including zero increments) are

    F0(X,g)-F0(x,g)=g^2(X-x)/((g+X)(g+x));
    F0(x,G)-F0(x,g)=(G-g)+x^2(G-g)/((G+x)(g+x));
    F1(X,g)-F1(x,g)=2(X-x)+2g^2(X-x)/((g+4X)(g+4x));
    F1(x,G)-F1(x,g)=8x^2(G-g)/((G+4x)(g+4x)).          (4.2)

These are the credited Part B identities, included explicitly. Every denominator
is positive and a strictly positive increment makes each displayed difference
strictly positive. Therefore (3.2) and (4.1) give, for each law with mean s,

    S(t)>=Phi(s):=min(F0(s^2,h(s)),F1(s^2,h(s))).        (4.3)

Every value Phi(s), s>=a, is attained by (3.3) and a suitable endpoint t. For
s>=c, both s^2 and h(s) are nondecreasing in s, so each endpoint value, hence
Phi(s), is nondecreasing. Phi is continuous on [a,c], a nonempty compact
interval. Its minimum is attained. It follows that

    C(p,q,u,v):=min_(a<=s<=c) Phi(s)                    (4.4)
      = inf over ALL laws (2.1) AND all t in [0,1/4] of S(t).

This is an EXACT SHARP constant for the declared class, not merely a lower
bound obtained by sampling s. An extremizer is mu_(s_star) from (3.3), with
s_star any minimizer in (4.4) and t its maximizing-denominator endpoint.

For X with specified individual nonzero atoms b1,b2, b1^2=u!=v=b2^2, the same
infimum holds: choose p delta_b1+q delta_b2+w delta_sqrt((s_star-a)/w).
No sign symmetry or independence is necessary. For the broader squared-radius
class any signs may be chosen without changing the scalar moments.

When P=1 the exact constant is min(F0(a^2,g0),F1(a^2,g0)); the preceding
one-variable interval collapses to a point, without division by w.

## 5. Strict improvement over independent lower inputs

For 0<P<1, let B=min(F0(a^2,g0),F1(a^2,g0)), the credited Part B lower-input
bound. Every s in [a,c] has s^2>=a^2 and h(s)>=g0, but these cannot both be
equalities: equality of s^2 requires s=a whereas equality of h requires s=c>a.
By (4.2), BOTH Fi(s^2,h(s))>Fi(a^2,g0). Each is therefore greater than B, so
Phi(s)>B everywhere on the compact interval. Taking its attained minimum gives

    C(p,q,u,v)>B>=min(g0,2a^2),   when 0<P<1.          (5.1)

The strict positive gain depends on the fixed inputs. No uniform gain is
claimed as w tends to zero, a mass vanishes, or the radii coalesce. At P=1,
C=B, consistently with simultaneous attainment. Scaling u,v by k>0 scales
s by k, g by k^2 and C by k^2, equivalently degree four under X->lambda X.

## 6. A fully certified sharp example

Take p=q=1/4,u=1,v=4. Then P=w=1/2, a=5/4,c=5/2,g0=9/8 and

    h(s)=9/8+(s-5/2)^2,     5/4<=s<=5/2.

Write f0(s)=F0(s^2,h(s)), f1(s)=F1(s^2,h(s)). Direct simplification gives

    f0=(8s^2-40s+59)(24s^2-40s+59)/(8(16s^2-40s+59)),
    f1=4s^2(24s^2-40s+59)/(40s^2-40s+59).

Their derivatives are

    f0'(s)=P5(s)/(16s^2-40s+59)^2,
    f1'(s)=8s R4(s)/(40s^2-40s+59)^2,
    P5=768s^5-5440s^4+18464s^3-36320s^2+37524s-17405,
    R4=960s^4-2240s^3+4432s^2-4720s+3481.             (6.1)

The denominators are positive because they are positive multiples of the
positive endpoint-ratio denominators in (2.3).

### 6.1 Exact sign certificate, not sampled derivatives

Put z=(s-5/4)/(5/4), so z in [0,1]. For a degree-n polynomial write
sum_(j=0..n) b_j binomial(n,j) z^j(1-z)^(n-j). The EXACT Bernstein coefficients
of P5 on this interval, from low index to high, are

    (-2125, -8351/4, -10127/4, -5639/2, -2626, 405).

All are negative except the last. For 0<z<=1 divide by z^5 and put r=(1-z)/z.
The result is 405 minus a polynomial in r with strictly positive coefficients
in every degree 1 through 5. It is strictly decreasing in r>=0, equals405 at
r=0 and tends to minus infinity. Since r decreases as z increases, P5 has
exactly ONE zero s_star in (5/4,5/2), is negative before it and positive after
it. This elementary sign proof does not assume P5 itself is increasing.

The exact degree-four Bernstein coefficients of R4 are

    (9899/4, 14099/4, 35311/6, 10806, 21881),

all strictly positive. The basis is nonnegative and sums to one, so R4>0 on the
whole interval. Hence f0 has its unique minimum at s_star and f1 is increasing.
Furthermore f0(5/2)<f1(5/4), an exact rational comparison. Consequently the
minimum of min(f0,f1) is f0(s_star), rather than the f1 endpoint minimum.
At s_star, f0<f1, so the attaining direction is t=0.

### 6.2 Rational outward enclosure

The checker derives the Bernstein coefficients by exact rational affine
substitution, verifies their signs, and performs80 rational bisections of P5.
This yields rational lo<s_star<hi inside(5/4,5/2), with P5(lo)<0<P5(hi).
On that interval h is decreasing and s^2 is increasing. Therefore (4.2) gives

    F0(lo^2,h(hi)) < f0(s_star) < F0(hi^2,h(lo)).        (6.2)

These are rational endpoint evaluations, not floating-point quadrature. Integer
floor/ceiling of the rational bounds at12 decimal places certifies

    2.464780131951 < s_star < 2.464780131952,
    2.076345574173 < C(1/4,1/4,1,4) < 2.076345574174.   (6.3)

The exact defining polynomial, rational brackets, Bernstein coefficients and
rounding directions are stored in RESULTS.json. The extremizing law is

    X ~ (1/4)delta_1 + (1/4)delta_2
          + (1/2)delta_sqrt(2s_star-5/2),   t=0.        (6.4)

This is a finite probability law, not the actual periodic spectral law. The
previous independent-lower-input bound is153/86; the conservative bound is9/8.
All remain correct; (6.3) is sharper because it retains joint feasibility.

## 7. Exact sources, verification and limits

Source correspondence, not inherited review or runtime dependencies:

- Math-#326, commit544499292f1cf09fe1bd030ce25d7cd0d80fc38c,
  `reviews/d2_two_mass_floors_20261006/NOTE.md`,
  blob b3e3b337697e4bf8c15bdab3666e49dc8833ca80, §§1-3/5.
- Math-#328, commit31f7a6b5a36045be7795a6461da067a8ada96343,
  `reviews/d2_two_atom_floors_20261006/NOTE.md`,
  blob cedbb44a237d1a158111dca81c30983f7efd37f1, §§2-6.
- Math- commit2f8b6f372be383d752e9dd30d38234faa977243c,
  `formal/ResearchFormalCoreR1/D2Schur.lean`,
  blob b95460c0d263a32ea274b347079cca6aaab3d2e9: definitions, cancellation,
  ratio and endpoint interpolation. Reading it is not new Lean execution.
- #328 comment6008747995 Part B, created/updated2026-10-06T03:29:55Z;
  its own technical comment review6016072968 and separate source PR371 retain
  their existing scope. This note neither replaces nor silently incorporates
  changes into either original packet.

Run from the repository root:

    python -B -S -m unittest discover -s tests -p test_d2_joint_mass_schur.py -v
    python -B -O -S -m unittest discover -s tests -p test_d2_joint_mass_schur.py -v
    python -B -S reviews/d2_joint_mass_schur_20261006/joint_mass.py

The twelve methods test exact square identities, attaining laws, endpoint
reduction, boundaries, finite strict-improvement examples, homogeneity, derivative
coefficient identities, Bernstein conversion, root/constant enclosure and source/
result identities. Grids are finite diagnostics; the continuum proofs are above.
The source inventory is an identity record, not an independent authenticity root.
The initial twelve missing-implementation assertions and later missing-inventory
assertion are retained in the author's evidence, not rewritten as successful runs.

The new root test is eligible for existing repository test discovery. No new
workflow, primary formal source, dependency pin, gate or acceptance flag is edited.
Actual hosted execution must be observed on the new candidate, not inferred from
older green checks. Author execution, source review, kernel checking, statement
alignment and scientific acceptance remain separate. Full exact-source review of
this new reduction, sharpness proof and certificate is required before integration.
No fixed-field rate, lifetime/elder/capture theorem, all-parameter uniform floor,
PSD matrix generalization or new Lean target is supplied.
