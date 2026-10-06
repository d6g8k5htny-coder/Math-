# Orthogonal positivity and a dimension-free band for the cubic jet variance

Object: PERIODIC-TAU-POSITIVE-FLOOR-20261005-v1. Date: 2026-10-05.
Dylan Roy — delegated AI mathematical work. Actual author: OpenAI / GPT-6 Astra Pro,
ChatGPT session `github-closure-directional-tau-20261005`.
Scientific effect **NONE**; author-side mathematics, not scientific acceptance.

## 1. Relation to the existing work

Math-#298, authored by the separate OpenAI session `periodic-tau-envelope-20261005`,
proves the closed cumulant formula and exact sphere-extremum reduction. Its
REPORT.md is pinned at commit `9deebd17dd696f72c6246d11bafb9e8265fd8f68`, blob
`2166869f20eb4d50249920691b90415943c4b5ff`. Those results are not republished or
reviewed here. An initially overlapping local draft was not published after the
peer and coordinator identified the earlier claim (main#229, comments
6002156344, 6002166026; reconciliation 6002199013).

This disjoint supplement proves an orthogonal spectral-polynomial decomposition
and explicit positive variance bounds. It does not alter #297, #298, either
review, or their branches. The product spectral model comes from the actual
parent P §§1–2; #297 supplies the named computational interface. SOURCES.json
records the exact sources and the three new payloads.

The quantity is exclusively

    tau_u^2 = Var(partial_u^3 f(0) | grad f(0)=0),    |u|=1.

It conditions on the FULL gradient, and not additionally on field value, Hu,
two separated pins, a cap/elder event, or a selected-pair law. For jointly
Gaussian field derivatives, ordinary Gaussian regression defines this variance.
The auxiliary spectral-coordinate random variables below need not be Gaussian;
only their moments represent the field derivative covariance. Their residual
law is not identified with the field's conditional law.

## 2. Orthogonal decomposition

Let X_1,...,X_d be independent copies of a symmetric real random variable X
with finite sixth moment and m2=E X^2>0. Define

    m4=E X^4,    m6=E X^6,
    Delta=m6-m4^2/m2,    V2=m4-m2^2,    t_i=u_i^2.

Here m2,m4,m6 are RAW moments. The notation in #298 is cumulant-based:
its a=m2, b=m4-3m2^2, c=m6-15m2*m4+30m2^3. No birth mark is denoted by m4.

**Proposition P1.** For every unit direction in every finite dimension,

    tau_u^2 = Delta sum_i t_i^3
            + 9 m2 V2 sum_{i!=j} t_i^2 t_j
            + 36 m2^3 sum_{i<j<k} t_i t_j t_k.          (1)

**Proof.** Put Y=sum_i u_i X_i. In the product spectral representation,
Cov(grad f)=m2 I. Also Cov(partial_u^3 f,partial_i f)=-E(Y^3 X_i), with the
minus sign dictated by the stationary derivative convention. It disappears
on squaring in the Schur complement. Thus tau_u^2 equals the second moment
of the spectral polynomial residual

    R=Y^3-sum_i [E(Y^3 X_i)/m2]X_i.

Direct expansion gives E(Y^3 X_i)/m2=3m2 u_i+(m4/m2-3m2)u_i^3, and

    R = sum_i u_i^3 [X_i^3-(m4/m2)X_i]
      + 3 sum_{i!=j} u_i^2 u_j (X_i^2-m2)X_j
      + 6 sum_{i<j<k} u_i u_j u_k X_i X_j X_k.          (2)

All summands are centered and pairwise L2-orthogonal. This follows from
independence and symmetry, together with E[(X^3-(m4/m2)X)X]=0 and
E[(X^2-m2)X]=0. Their variances before the displayed coefficients are Delta,
m2 V2, and m2^3. Squaring the coefficients proves (1). The mixed sum is over
ORDERED distinct pairs; the triple sum is over UNORDERED triples. Empty sums
in d=1,2 are interpreted as zero. No inverse Hessian or isotropy assumption
is involved. QED.

This is an exact covariance statement for the product spectrum, not a claim
that spectral coordinates equal the field derivatives. The Schur projection
uses linear functions of the spectral coordinates only because their inner
products encode the Gaussian field's gradient covariance.

## 3. Positive bounds in every direction and dimension

**Corollary P2.** Let

    c_low = min{Delta, 3 m2 V2, 6 m2^3},
    c_high = max{Delta, 3 m2 V2, 6 m2^3}.

Then for EVERY finite d>=1 and every unit u,

    c_low <= tau_u^2 <= c_high,                         (3)
    tau_u^2 >= Delta/d^2.                               (4)

If Delta>0, then c_low>0. In particular the constants in (3) depend on the
ONE-COORDINATE spectral law, not on direction or dimension.

**Proof.** Delta=E[(X^3-(m4/m2)X)^2]>=0 and V2=Var(X^2)>=0. Since sum t_i=1,

    sum_i t_i^3 + 3 sum_{i!=j}t_i^2 t_j
      + 6 sum_{i<j<k}t_i t_j t_k = 1.

These three nonnegative monomial weights make (1) a convex combination of
Delta, 3m2 V2 and 6m2^3, proving (3). Convexity of x^3 gives sum t_i^3>=1/d^2;
keeping the first nonnegative term proves (4). If V2=0, then X^2=m2 almost
surely, so X^3=m2 X and Delta=0. Therefore Delta>0 implies V2>0, and m2>0
makes all three coefficients strictly positive. QED.

The band need not be sharp. #298 supplies sharp extrema when those are needed.
Do not use Delta alone as a dimension-free lower bound: for the symmetric
law with total mass 99/100 on {-1,1} and 1/100 on {-10,10}, the equal two-support
direction has variance strictly below its axis value Delta. This is a control,
not a claim that that discrete law is P's spectrum.

**Exact finite-period application.** For P's variance-one covariance at fixed
L>0, the one-coordinate spectral weights are proportional to
exp(-2*pi^2*n^2/L^2), at X=2*pi*n/L, with positive weight for every n in Z.
They have all moments finite. Hence m2>0 and Delta>0: the polynomial
X^3-(m4/m2)X cannot vanish at both distinct nonzero magnitudes 2*pi/L and
4*pi/L. This proves a symbolic strictly positive band (3) for the tau
invariant for every finite dimension at the same L. No numerical value of
c_low is certified here. There is no uniform-in-L assertion.

Dimension independence here is SPECIFIC to this scalar conditional variance
in a family with the same coordinate spectral law. It does not imply a
uniform full-jet covariance floor, a finite-r pinned-law bound, a selected
weight normalizer, a dimension-uniform lifetime coefficient, or parent-theorem
constants uniform in dimension. The full jet and numerical-integration
obligations retain their original scope.

## 4. Exact reproduction and limits

From the packet directory:

    python -B -S positive_tau.py
    python -B -O -S positive_tau.py
    python -B -S -m unittest test_positive_tau -v
    python -B -O -S -m unittest test_positive_tau -v

The standalone oracle expands E(Y^6) and E(Y^3 X_i) by multinomials, then
forms the full-gradient Schur complement. It is independent of (1)'s
coefficient implementation. Nonunit rational vectors are handled by exact
homogeneous division, avoiding irrational normalizations.

The nine unittest methods also check the ten polynomial summands on all
64 atoms of a three-coordinate {-2,-1,1,2} product law: zero means, all45
cross inner products zero, pointwise residual equality, and variance equality.
They exercise exact simplex weights, the two bounds, Gaussian reference,
zero-Delta degeneration, the invalid Delta-only floor, input validation, and
actual CLI behavior in both Python modes.

Each deliberately incorrect alternative must exit1 with POSITIVE_TAU_FAIL:
M1 omits gradient regression; M2 replaces9 by3 in the mixed coefficient;
M3 replaces36 by6 in the triple coefficient; M4 replaces the minimum lower
coefficient by Delta. An unknown mutant label exits2. Floating inputs and
booleans are refused; accepted rational/decimal strings mean their exact
encoded value, not a certified approximation to unspecified real moments.
The necessary moment inequalities checked by the utility do not by themselves
certify that supplied numbers are moments of a particular field.

Test-first: the narrowed suite failed because positive_tau.py did not yet
exist. After implementation all9 tests passed in normal and optimized Python.
CLI outputs are byte-identical. The standalone run checks60 direct Schur
identities,462 convex-weight identities,1848 dimension-free band inequalities,
1848 dimension-dependent floor inequalities, and1386 strict positive-law cases.
These finite checks are not proofs of the arbitrary-real and all-dimensional
statements; P1/P2 supply those proofs. No Lean execution is claimed. Existing
hosted repository workflows do not execute this standalone script.

A raw-source network download failed with DNS resolution in this environment.
No #297/#298 executable was downloaded or run locally. Their source was read
through the GitHub connector; this supplement imports no executable from
either. The abandoned extrema draft remains unpublished scratch and is not
part of this packet or its claimed test count. No audit, scientific status,
original source, author attribution, or existing review was changed.
