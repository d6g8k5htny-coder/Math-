# LM006: tilted endpoint laws, event margins, and the singular-support obstruction

Dylan Roy — delegated AI mathematical work. Actual author OpenAI / GPT-6
Astra Pro, session `round13-endpoint-law-audit-20261005`. Scientific effect NONE.
This is an additive analytic companion, not a Lean formalization or a change
of any historical theorem, review, or scientific register.

## 1. Exact source and scope

The predecessor is Math-#315 at `5e027afcae8c7bd42a6df8ae2025f82105b3e586`,
`reviews/lm006_normalizer_stability_20261005/NOTE.md`, Git blob
`5790aaa0332bd8e79b276be1577e4c5f3502eed6`, SHA256
`2e63518026cef54bb91757ccbdba986a0765f8a8b640240417ba30c59e2f5fd4`.
It is a separately reviewed analytic source, not a new Lean theorem or a
statement that its PR is already merged. It explicitly excludes arbitrary
full-field event transfer. This companion proves conditional statements about
endpoint laws on R^6 and records exactly why total variation can fail there.

Use its endpoint function, with x_+=max(x,0) and x_-=max(-x,0):

 T_r(v)=[(a_-)_-(c_-)_- - r b_-^2]_+ [r b_+^2-a_+c_+]_+,
 v=(a_-,a_+,b_-,b_+,c_-,c_+),  0<=r<=1.                     (1)

For r>0 this is the normalized physical typed weight W_r/r^2. At
v0(u,q)=(-1,1,-u/2,u/2,q,q), T_0(v0)=(q_-)^2, including q=0.
The input inequality, predecessor (5), is

 |T_r(v)-T_s(w)| <= (||v||+||w||)^3 ||v-w||+|r-s| ||w||^4. (2)

General posterior/reweighted-measure stability and the distinction between
probability metrics have extensive prior literature; this note claims no new
general stability principle. Repository `formal/WeightPerturbation` (under
`formal/ResearchFormalCoreR1/`) already handles two weights under one law.
The present addition distinguishes a common latent law from TWO different
pushforward maps, provides explicit endpoint/margin constants, and exhibits
the singular-support obstruction for (1). The prior remote-window result also
already uses common regression couplings and filtered determinants.

## 2. A normalized-density lemma on the common probability space

Let (Omega,gamma) be a probability space. Let a,b be measurable, nonnegative,
integrable random variables, z=E_gamma a>0 and z0=E_gamma b>0. Write
Delta=E_gamma|a-b|. The tilted probability laws on Omega are gamma_a with
density a/z and gamma_b with density b/z0. Then

 E_gamma|a/z-b/z0| <= 2 Delta/z0.                           (3)

Indeed split a/z-b/z0=(a-b)/z0+a(1/z-1/z0), integrate absolute values, and
use |z-z0|<=Delta. No smallness assumption is needed once both normalizers
are positive. Delta<=z0/2 is a useful sufficient condition for z>=z0/2>0.

We use TV(mu,nu)=sup_A|mu(A)-nu(A)|, with range [0,1]. For probability
densities the signed difference integrates to zero; its positive and negative
parts have equal integral, each half the L1 norm. Thus

 TV(gamma_a,gamma_b) <= min(1,Delta/z0)=:theta,              (4)
 |E_gamma_a h-E_gamma_b h| <= theta         for 0<=h<=1,
 |E_gamma_a h-E_gamma_b h| <= 2 theta       for |h|<=1.

These are bounds for the SAME measurable function h on Omega. Replacing h
by two unrelated functions is not justified by (3) or (4).

## 3. Moving endpoint maps: bounded-Lipschitz and padded-event bounds

Let X,Y:Omega->R^6 be measurable maps. Set

 nu=X_#gamma_a,  nu0=Y_#gamma_b,  nu_tilde=X_#gamma_b,
 D=||X-Y||, H=(E_gamma b^2)^(1/2), e=(E_gamma D^2)^(1/2),

and assume H,e are finite. All three measures are well-defined probabilities;
countable additivity follows from that of integrals of nonnegative densities.
No independence between a,b,X,Y is required.

For real phi with |phi|<=1 and Lipschitz constant at most1,

 |nu(phi)-nu0(phi)| <= 2 theta + E_gamma[b D]/z0
                     <= 2 theta+H e/z0.                   (5)

Proof: compare nu with nu_tilde using (4) on phi(X), then compare nu_tilde
with nu0 using the actual coupling (X,Y) under gamma_b. Cauchy--Schwarz under
gamma proves the last inequality. Taking the supremum defines the bounded-
Lipschitz metric d_BL used here, which is also at most2. The density comparison
alone is insufficient: the movement term must remain. We make no W1 claim
for unbounded test functions by merely substituting TV into this proof.

For a Borel set A and t>0, let A^t={y:dist(y,A)<=t}; distance to an arbitrary
set means distance to its closure, and distance to the empty set is infinity.
These neighborhoods are Borel. Put kappa(t)=E_gamma[b 1_{D>t}]/z0. Then

 nu(A) <= nu0(A^t)+theta+kappa(t),
 nu0(A) <= nu(A^t)+theta+kappa(t).                         (6)

Proof: on {D<=t}, X in A implies Y in A^t, and conversely with X,Y reversed.
Take expectations under gamma_b and use (4) for the appropriate event of X.
Consequently kappa(t)<=H e/(z0 t), by Cauchy--Schwarz and Markov's inequality.
The probability in this tail is reweighted by b; substituting gamma(D>t)
without a bound on b would be an error.

In Euclidean space a line segment between points with different membership
in A meets the topological boundary of A. Hence if indicators differ and
D<=t, dist(Y,boundary A)<=t. This covers arbitrary Borel A, including points
on the boundary; for A empty or full the assertion is trivial. Therefore

 |nu(A)-nu0(A)| <= theta+beta_A(t)+kappa(t),                (7)
 beta_A(t)=nu0({y:dist(y,boundary A)<=t}).

A small marginal approximation error does NOT supply beta_A(t). For an event
whose boundary contains the limiting support, beta_A(t)=1 and (7) does not
assert convergence. This is the required safeguard for moving-band events.

## 4. Gaussian specialization and conditional event rates

Assume X=m_r+A_r Z and Y=m_0+A_0 Z with one standard Gaussian Z and finite
factors having the same number of columns. Singular covariances are allowed.
Then X-Y is Gaussian and

 e^2=||m_r-m_0||^2+||A_r-A_0||_F^2.

For a Gaussian vector U with mean m and covariance C, direct expansion gives

 E||U||^4=(||m||^2+tr C)^2+2 tr(C^2)+4 m^T C m
          <=3(||m||^2+tr C)^2.                             (8)

To verify the expansion, diagonalize C; centered coordinates are independent,
with E Z_i^2=1, E Z_i^4=3 and odd moments zero. Use tr(C^2)<=(tr C)^2 and
m^T C m<=||m||^2 tr C for the bound. No invertibility is needed. Applied to
U=X-Y, Cauchy--Schwarz plus fourth-moment Markov yields the alternative

 kappa(t) <= min(H e/(z0 t), sqrt(3) H e^2/(z0 t^2)).      (9)

For a=T_r(X), b=T_0(Y), Y=v0(u,Q), the predecessor's bound (2) gives the
STRONGER L1 estimate, not only cancellation of signed expectations:

 Delta=E|T_r(X)-T_0(Y)| <= B e+D0 r,                       (10)
 B=sqrt(2048(M^6+480 Lambda^3)),
 D0=8(M^4+48 Lambda^2),

provided the means have norm<=M and covariance operator norms<=Lambda as in
that predecessor. This follows by integrating the absolute pointwise bound;
it is not inferred from |E T_r-E T_0| alone. Here z0=E(Q_-)^2, and
H^2=E(Q_-)^4. A convenient coarse bound is

 H^2<=E||Y||^8<=128(M^8+5760 Lambda^4).

Suppose z0>0 and B e+D0 r<=z0/2. Equations (5)--(10) then control actual
tilted endpoint laws with all constants explicit in the supplied inputs.
For example

 d_BL(nu_r,nu0) <= min(2, [2(B e+D0 r)+H e]/z0).           (11)

If additionally beta_A(t)<=C_A t^alpha for 0<t<=t0, alpha>0, then for
0<e with e^(2/(alpha+2))<=t0, choose t=e^(2/(alpha+2)) in (7),(9):

 |nu_r(A)-nu0(A)| <= (B e+D0 r)/z0
        +(C_A+sqrt(3)H/z0)e^(2 alpha/(alpha+2)).           (12)

This is a conditional rate, not an optimized constant. At e=0, X=Y almost
surely and (4) gives the direct theta bound. No margin exponent, Gaussian
factor-error rate, uniform numerical normalizer, or radius is supplied by this
note. All such inputs must be verified under the intended law and fixed
parameter range before application. Full-field events are not automatically
functions of the six endpoint coordinates.

## 5. Exact obstruction: full endpoint total variation may remain one

Let

 S={v in R^6: a_-=-1, a_+=1, b_-+b_+=0, c_--c_+=0}.

This is an affine plane of dimension2 and Lebesgue measure zero. If Y is
supported on S, then so is nu0. If X_r has a Lebesgue density and its tilted
normalizer is finite and positive, nu_r also has a Lebesgue density. Hence

 nu0(S)=1, nu_r(S)=0, TV(nu_r,nu0)=1.                     (13)

This does not conflict with (11). The intermediate nu_tilde in §3 is also a
pushforward through X_r, whereas nu0 is pushed through Y. Even when the latent
tilts are close in TV, the two pushforward maps need not be the same.

Self-contained Gaussian example using exactly (1): take y=(-1,1,0,0,-1,-1),
Y=y, X_epsilon=y+epsilon Z_6, and r=epsilon in(0,1]. Then e=sqrt(6)epsilon,
z0=T_0(y)=1, and Delta tends to zero by (10) with M=2,Lambda=1. Since
T_r(y)=1 and T_r is continuous, E T_r(X_epsilon)>0 for every epsilon>0;
quartic growth gives integrability. X_epsilon and its tilt have a density,
while nu0 is the point mass at y. Therefore (13) holds for every epsilon,
although (11) tends to zero. This example is NOT a claimed six-pin Gaussian
field realization. In the actual LM006 application, (13) holds whenever the
finite-r endpoint vector has a density; establishing that property is the
separate positive pin/Hessian Gram argument, not a consequence of (11).

This is a scope obstruction, not an error finding against #315, whose text
already excludes full-field event transfer. It prohibits strengthening the
new endpoint conclusion to convergence in TV without a different coordinate
representation or additional argument.

## 6. Exact finite controls and review boundary

Run `python -B -S test_tilt.py` and the same with `-O`. The 12 methods verify
676 weight-pair TV comparisons,64 latent events,300 clipped-Lipschitz cases,
400 directed padded inequalities,150 threshold/margin inequalities,81 exact
Gaussian fourth-moment parameter cases, normalization/null-mass/input edges,
and the movement-vs-TV counterexample. These are one-dimensional finite
analogues of the inequalities, not a proof of the R^6 or Gaussian claims.
`tilt_check.py` has687 exact baseline controls. M1--M7 independently test:
omitted normalization, signed instead of absolute weight error, omitted map
movement, unweighted tail substitution, omitted event margin, wrong Gaussian
fourth-moment coefficient, and substituting BL for TV. Each must exit1 with
its exact named TILT_FAIL diagnostic; invalid arguments exit2. A crash is not
an accepted rejection. The predecessor's existing workflow is not represented
as an execution of these new tests, and no new Lean target is claimed.

## 7. Attribution and external context

The original normalizer and endpoint definitions remain unchanged. The
predecessor's source review is reused only for (1),(2),(10)'s stated inputs;
this new density/map argument needs its own nonauthor read. Other ongoing
moment-law, Cap I4, spectral and gate-hardening work is not a premise here.

As related context only, Latz, *On the well-posedness of Bayesian inverse
problems*, arXiv:1902.10257, and Sprungk, *On the local Lipschitz stability of
Bayesian inverse problems*, arXiv:1906.07120, distinguish stability metrics
and normalization-sensitive posterior bounds. Their abstract records were
consulted, not imported as proofs of (1)--(13); the elementary argument above
is complete on its explicit assumptions. No claim of literature novelty or
complete literature coverage is made. A requested Consensus search hit its
monthly limit, so no Consensus result supplies any premise.
