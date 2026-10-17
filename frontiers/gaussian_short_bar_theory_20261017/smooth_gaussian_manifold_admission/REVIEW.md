# Nonauthor review of the smooth dense-support Gaussian admission theorem

Review date: 17 October 2026. Reviewer: OpenAI/Codex task
`/root/reverse_localization_nonauthor_review_20261017`. This is a new mathematical
review of the frozen proposal, separate from this reviewer's earlier reverse
localization review and local formal-packet preparation authorship. The reviewer
did not author the universality proposal or its mechanism. Root and the proposal
author did author that mechanism. All participants are source-exposed and share
OpenAI as provider; organizational independence is zero. Preparation questions
were exchanged before the freeze. This is not blind or provider-independent
review, and no scientific promotion follows.

**Final integrated verdict: ACCEPT_SCOPED. There are no must-fix findings or
required source amendments for the exact frozen proof under the hypotheses and
classical imports stated below.** The separately assigned focused review has
been read in full and joined; its seal and the author freeze have been freshly
verified. No theorem verdict was issued on an unsealed draft.

## Exact object and scope of this review

The exact proposed source is `smooth-full-support-universality-author-20261017/PROOF.md`,
40231 UTF-8 bytes, 739 lines, SHA256
`8d992e194f0a898e563c4c3d05b8079cde292f9e87d7ff51030ad12ef5faf319`.
Its author freeze manifest is 2203 bytes, SHA256
`3f1338445bf20cf6d1300fbdf1ddbc687b4abb0ab318b777b7fb70bf77121c5e`,
binding 11 files with 150111 bytes in total. The reviewer read the full exact
739-line source after freezing, reconstructed the arguments below, and verified
all eleven bound files. Hashes identify the object; they are not mathematical
proof. The author source and its freeze remain unchanged.

The four actual imported ST/IG documents were also read completely, rather
than accepted from their review labels:

| Document | Bytes | SHA256 |
| --- | ---: | --- |
| ST structural proof | 43927 | `3d952a906553d578876456539a8f0dcd64aedd45099e8394cbe9db99866ec531` |
| ST source-bound review | 3701 | `81f4908c7f904079f416e7bc38f8ef936079ab6049e6b65cbbfcfcfc3104ae4e4b` |
| IG periodized Gaussian proof | 34629 | `c8bd489ca3fbb3760f7b2d53e7385131ac5336c51ba983e00e4d540fe2f00aaa` |
| IG source-bound review | 3700 | `e3bb8751fbdaf0db075342a31dd208c1300c6e93a1c3c8a7c3b255860442551b` |

The frozen author directory contains exact copies. Their original paths relative to the core workroot
are recorded in `PREPARATION_INPUT_IDENTITIES.json`; the explicit base is
clarified additively in `PATH_BASE_CORRECTION.json`. ST is a conditional theorem
with five named interfaces, not a prior proof of admission for every smooth
Gaussian field. IG supplies a previously developed finite-tail proof route for
one periodized law, not automatic rank or conditional genericity for this new
class. The new proposal proves the required admission separately. The old review
records preserve the intermediate half-Gaussian normalization error and its
later actual correction; the new proposal is assessed against the corrected
exact bodies, without rewriting those historical stages.

The admitted object is one fixed actual centered real Gaussian series

    F = sum_j a_j Z_j phi_j,
    Z_j independent N(0,1), a_j>0,
    span_R{phi_j} dense in C-infinity(X),
    sum_j a_j ||phi_j||_Cq < infinity for every integer q>=0.

Here X is a fixed nonempty connected compact smooth manifold without boundary,
g is a fixed smooth Riemannian metric, and d=dim X>=1. Write V=vol_g(X)>0.
Each law, geometry, and finite dimension is considered separately. The result
is the expected finite ordinary superlevel H0 elder-bar measure, with the one
essential class excluded. It has the particular finite Borel density version
specified by the exact Rice/height kernels, and

    nu(ell) ~ C_F,g ell^(-1/3),
    E N_bar((0,t])/V ~ (3/2) C_F,g t^(2/3),
    0<C_F,g<infinity.

It is not a theorem here that every abstract full-support smooth Gaussian
random element admits this particular representation with these summability
bounds. The theorem admits the explicitly specified nonempty series class.
It supplies no constants uniform over laws, degenerating spectra, metrics,
or dimension; no numerical onset scale; no point process or higher factorial
moment result; no Hk extension; no field sampler certification; no Lean theorem;
no coefficient enclosure or scientific adoption. These restrictions are
mathematical boundaries of the actual claim, not pending steps silently counted
as completed.

## What was genuinely new and was checked independently

Five risks had to be discharged beyond the conditional ST theorem: dense smooth
support had to yield the particular finite coefficient minors; the infinite
law needed canonical whole-field conditioning at literal zero-probability
targets; remote genericity had to survive the forced degenerate contact under
that conditional law; all-mark norm and Gaussian density bounds had to work
without finite-dimensional coefficient norm equivalence; and the coefficient
had to retain all joint jet correlations on a curved, nonstationary manifold.
The remaining sections address those points directly.

The conclusion cannot follow solely from smooth covariance, a dense-support
statement, unconditional Morse genericity, or a local candidate fold. In
particular a dense-support measure may charge a residual bad set, arbitrary
Borel marks need not be continuous on a conditioning fiber, and a global
Gaussian coefficient sequence does not lie in unweighted l2. None of those
invalid shortcuts is required by the frozen proof.

## Nonempty class, actual smooth law, moments, and support

The chart construction is valid on every X in scope. Refine a finite cover to
coordinate cubes, choose partition functions rho_i supported compactly inside
them, and choose chi_i=1 near supp rho_i. For each smooth f, rho_i f extended
by zero is a smooth periodic function in its cube. Integration by parts makes
its Fourier coefficients rapidly decreasing; finite Fourier sums therefore
converge with every derivative. Multiplication by chi_i preserves that
convergence. Their sum converges to sum rho_i f=f. Thus the countable list of
real cutoff sine/cosine functions has dense real span in the smooth topology.
The construction does not require an eigenfunction theorem, orientability,
a global frame, a flat chart transition, or stationarity.

For any such list, the proposed positive choice

    a_j=2^-j/(1+max_{0<=q<=j} ||phi_j||_Cq)

is sufficient: at any fixed q all j>=q summands of a_j||phi_j||_Cq are at most
2^-j, and finitely many earlier terms are finite. This proves nonemptiness
without appealing to a probabilistic existence theorem.

Let B_q=sum a_j|Z_j| ||phi_j||_Cq. Finite first expectation gives B_q<infinity
almost surely. The countable intersection over q has probability one. On that
event all derivative series converge absolutely and uniformly, giving an actual
smooth field and ||F||_Cq<=B_q. Minkowski gives ||B_q||_Lp<=A_q||Z||_Lp for
p>=1; smaller positive moments follow. Consequently every smooth norm has all
finite moments needed later. Covariance derivatives converge absolutely because
products of the relevant summable nonnegative sequences are summable. The
smooth field is a Borel random element obtained as a smooth-topology limit.
No Fernique theorem, infinite-dimensional standard Gaussian vector, or
unweighted coefficient l2 bound is used.

The full-support argument also works with the actual tails. Approximate h in a
Cq neighborhood by a finite prefix, enlarge that prefix until the expected Cq
norm of its independent tail is small, and use Markov on the tail. The finite
Gaussian prefix has positive probability to lie near any required finite
coefficient vector because all a_j are positive. Independence gives positive
probability for their intersection. Finite rational linear combinations give
a countable dense set in the smooth space, also useful for Borel generation.
This argument requires only neighborhoods involving finitely many seminorms,
which an increasing Cq norm controls.

## Named jet rank, finite original minors, and compact-domain floors

For linearly independent continuous linear functionals L_1,...,L_m on smooth
functions, a nonzero annihilator of every column (a_j L_i phi_j)_i would vanish
on the dense span, and then on every smooth function. This contradicts the
independence of the L_i. Hence the actual infinite column family spans R^m,
and a finite subset already spans it. The covariance sum is strictly positive.
This proves an actual finite original coefficient block; it is stronger than
merely observing positive covariance after a formal limit.

The relevant rows really are independent. At finitely many distinct sites,
disjoint bump functions times Taylor polynomials prescribe independent local
jets. The particular covariant derivative rows are triangular transforms of
those local Taylor data. Only independent symmetric jet entries are used; no
claim is needed that all ordered covariant third-derivative components are
independent on a curved manifold. The named rows are gradients; two first
jets O; the contact rows (F,F_u,F_uu,F_uuu,(F_vi,F_uvi)); the additional independent
transverse symmetric Hessian block; and contact rows joined to one or two
off-contact first jets. There are no duplicate axial-column entries in the
contact/transverse map.

Joint surjectivity of (U,J) implies surjectivity of J restricted to ker U:
lift each (0,y). This elementary fact is decisive under conditioning. It proves
both conditional transverse nondegeneracy and finite residual remote first-jet
freedom. It is not inferred merely from support on an affine fiber.

A chosen nonzero minor stays nonzero in a neighborhood. On a compact separated
domain finitely many such neighborhoods suffice, and the union of their finite
column sets supplies one block throughout that domain. Continuity plus
compactness gives covariance floors there. The compact orthonormal frame bundle
likewise gives a uniform contact floor. Local frame trivializations are enough;
there is no assumption that the perpendicular bundle is trivial. No minor or
floor uniform over collisions, or over different laws or metrics, is claimed.
Countably many annuli away from a contact and away from the pair diagonal are
the correct domains for the later conditional argument.

## Literal observations and global smooth Gaussian conditioning

For M=exp_x(-ru/2), S=exp_x(ru/2), parallel frames give the literal rows of
proposal (7), including the cubic row with coefficient 6/r^2. Their target for
heights b,b-kr^3 and zero gradients is

    v_r=(b-kr^3/2,-kr^2,0,12k,(0,0)_i),
    v_0=(b,0,0,12k,(0,0)_i).

Direct finite row operations give the absolute transform determinant
12 r^(-(d+3)). Integral divided-difference identities bound U_r by the C3 norm
and U_r-U_0 by Cr times the C4 norm. Bounding the separated summands in the
cubic row would have been invalid; bounded averaged derivatives are the
correct calculation. Curved geometry does not alter these one-dimensional
identities along a geodesic with parallel frames.

The smooth covariance then gives Sigma_r->Sigma_0 and c_r->c_0 globally in each
Cq norm, uniformly on compact frame charts. The proven positive contact floor
persists for one small common r_0. On one copy of the actual F, define

    F_r=F+c_r Sigma_r^-1(v_r-U_r F).

This has exact observations v_r. Its residual is Gaussian and uncorrelated
with U_r F. Independence holds for finite evaluation vectors and then the
whole smooth field because a countable evaluation family generates its Borel
sigma-field. Its law is therefore a specified Gaussian conditional version at
every literal target. Smooth parameter dependence of the formula supplies
joint Borel versions. It is not a conditional probability of a positive-mass
pinning event.

The residual projection H_r=I-c_r Sigma_r^-1 U_r is continuous in the smooth
topology, has range ker U_r, and restricts to the identity on that kernel.
The image of full smooth support therefore has support exactly ker U_r.
Translation gives the affine-fiber support. This true assertion is not used
as a substitute for the finite residual incidence proof.

For each fixed b,k and converging geometric parameters, the same underlying
field gives almost sure and all finite Lp global C4 convergence F_r->F_0.
Uniform covariance coefficient bounds and the integral-row bounds give

    ||F_r||_Cq <= ||F||_Cq+C_q||F||_C3+C_q(|b|+k).

This is the actual global coupling and moment estimate needed by the elder
lemma. Pointwise jet convergence alone would not control a remote elder
competitor. The proof uses the whole manifold norm and avoids any assertion
of norm equivalence for infinitely many raw coefficients.

## COUNT and all-Borel marks at the actual null targets

Fix a compact point or separated-pair domain and choose a finite block of the
original independent standard Gaussians with the proven observation ranks.
Split F=F_B+T with an independent smooth tail. Fix that smooth tail before
applying a deterministic finite-dimensional theorem. For an invertible
coefficient gradient minor B, solve the critical equations for those
coefficients as a(p,eta)=-B(p)^-1(grad T+D(p)eta). The smooth incidence projection
(p,eta)->(a(p,eta),eta) has a singular differential precisely when the Hessian
is singular. Smooth equal-dimensional Sard proves that degenerate critical
points occur on a coefficient null set. Integrating the independent tail,
using countable local covers, proves unconditional Morse behavior. Compactness
makes the critical set finite.

The pair version has incidence Jacobian
|det H_p det H_q|/|det B_pair|. Ordinary coefficient-fiber change of variables
and the Gaussian coefficient density cancel the minor denominator. Each
physical Hessian determinant appears exactly once. Coordinate metric factors
cancel against the corresponding Riemannian volumes. The weighted area identity
allows arbitrary nonnegative Borel functions of the entire smooth field,
including its actual nonlocal bar event. A disjoint Borel chart/minor partition,
compact exhaustion in coefficient space, Tonelli over tails, and countable
separated-domain exhaustion give the extended root-counting formula before
assuming total finiteness. The accompanying
`FINITE_SMOOTH_INCIDENCE_RECONSTRUCTION.md` derives the finite smooth weighted
area statement from equal-dimensional Sard, inverse maps, and ordinary change
of variables. Thus no abstract-only area/coarea reference is counted as proof
of an all-Borel Kac-Rice theorem.

The target-version issue requires an additional calculation. Let L be the
finite observation map, Y_B=L F_B, Y_T=L T, Sigma_B>0 and Sigma=Cov(LF)>0. For
any literal y, the correct tail distribution is

    p_B(y-Y_T)/p_Y(y) times its original distribution.

The normalizer is the actual positive Gaussian convolution density. Given
that tail, the finite block has its ordinary affine conditional Gaussian
law. This mixture is defined at every y. For any finite field evaluation
vector W, insert the finite Gaussian conditional characteristic function
of W_B given Y_B=y-Y_T and integrate the joint finite Gaussian vector
(Y_T,W_T). Completing the observation square gives exactly

    exp(i t^T Cov(W,Y) Sigma^-1 y
        - (1/2)t^T[Cov(W)-Cov(W,Y)Sigma^-1 Cov(Y,W)]t).

The calculation holds for every y, not merely almost every y. Hence this
mixture is the same regression kernel as the explicit whole-field formula.
A countable dense evaluation set generates the smooth Borel sigma-field:
derivatives are measurable limits of finite differences of values, Cq norms
are countable suprema of derivative values in finite charts, and rational
finite combinations form countably many dense ball centers. Equality of all
finite evaluation laws therefore identifies the whole-field laws. All Borel
marks transfer by equality of measures; no continuity of the mark on an
exceptional fiber is invoked. The same calculation for the complete first-jet
observation O specifies the height-disintegrated kernels used in the density.

First-jet rank makes the two-height law given both gradients nondegenerate.
On each separated compact domain conditional Hessian moments and covariance
floors give finite local integrals. A critical-height tie therefore has zero
expected count after ordinary Gaussian height disintegration. Countable
annuli give distinct critical values almost surely. The analogous one-point
formula and the compact gradient floor give finite expected total critical
count. No collision-uniform two-point estimate is needed for these assertions.

The actual elder indicator is Borel. Strict-superlevel connectivity can be
tested by finite chains of countably many geodesic basis balls whose closure
minima exceed a rational level. Membership of endpoints, dense-point values,
and closure minima are Borel in sites and the smooth field. Taking the
supremum of rational connection levels to a point with value above the birth
maximum gives the death level. The Morse/distinct-height restriction is Borel.
Classical Morse level/handle facts and H0 elder linear algebra imply that a
maximum creates one component and an index-(d-1) event either merges two or
does not change H0; at a merger the younger maximum dies. Distinct heights
make events unique. The global maximum represents the excluded essential
class. This proves once-counting of every finite ordinary bar. There is no
additional unordered-pair division by two.

Consequently proposal (19) is an actual expected-bar density representative,
with the same canonical full-field kernels used by the contact argument.
This proves COUNT, including the nonlocal mark, rather than merely a candidate
critical-pair identity.

## Forced-contact remote genericity under each fixed target

Unconditional Morse genericity cannot be applied to Q_0: the contact is forced
to be degenerate. The proposal supplies the required separate argument. For
each domain separated from x, choose a finite original block with joint
(U_0,J_remote) rank. Under the literal contact target v_0, its tail distribution
is the positive Bayes weighting p_(U_0F_B)(v_0-U_0T)/p_(U_0F)(v_0), not the
unconditional tail law. It is absolutely continuous with respect to the smooth
tail law and therefore still smooth almost surely. Given that tail, write

    xi_B=L_B^T(L_BL_B^T)^-1(v_0-U_0T)+P_B z,
    P_B=I-L_B^T(L_BL_B^T)^-1 L_B.

An orthonormal basis of ker L_B identifies the free coordinates as genuine
independent standard Gaussians. The mean is generally nonzero and retained.
The proven joint surjectivity makes all needed remote first jets surjective
in these free directions. Apply the finite incidence/Sard argument in those
coordinates. Residual first-jet ranks and Gaussian height disintegration
exclude other critical height b and off-contact critical-height ties. This
works on each compact separated domain with its own block and its own local
floors. Every conclusion is a property of the same already identified Q_0;
countably intersecting over domains is legitimate. There is no uncountable
intersection over all literal targets, and none is needed for pointwise
contact convergence followed by dominated integration.

Conditional transverse A_0 has a full Gaussian density on its independent
symmetric entries, by the local enlarged contact rank. Thus it is invertible
almost surely; for d=1 the empty block is automatically invertible. An
implicit transverse ridge isolates the forced contact: its reduced first and
second derivatives vanish and its third derivative is 12k>0, so its first
derivative is 6ks^2+o(s^2)>0 at all sufficiently small nonzero s. This isolation
uses invertibility of A_0, not its negative definiteness. Outside that
neighborhood a compact set contains only isolated Morse critical points;
otherwise a compact accumulation point would itself be critical and not
isolated. Thus there are finitely many, with positive gaps among heights and
from b. These are exactly the deterministic elder lemma's global premises.

## CONTACT: physical Hessians, weighted cone limit, and positivity

Exact zero endpoint gradients make the axial-column integral vanish along the
geodesic. The physical Hessians have blocks

    H_i=[r alpha_i, r beta_i^T; r beta_i, A_i],
    alpha_M->-6k, alpha_S->6k, A_i->A_0.

Fundamental calculus bounds alpha_i,beta_i by the C3 norm; global C4 coupling
justifies the stated limits. The determinant identity

    det H_i/r=alpha_i det A_i-r beta_i^T adj(A_i)beta_i

is polynomial and valid even for singular transverse blocks. The congruence
rescaling diag(r^-1/2,I) gives the correct inertia. Thus the maximum/index-(d-1)
weight divided by r^2 tends to

    V_0=36k^2(det A_0)^2 1{A_0<0}.

When the limiting A is nonsingular but not negative definite the maximum
condition fails. At singular A the determinant weight tends to zero. No
unjustified cone-boundary continuity or inverse curvature factor is required.
The weight is dominated by C(1+||F_r||_C3)^(2d). The all-norm moments give
uniform integrability and expectation convergence. Contact densities converge
by the actual uniformly nondegenerate Sigma_r. Conditional A has everywhere
positive Gaussian density, so its negative-definite cone has positive weighted
mass for every b,k>0. For d=1 det A=1, the cone condition is empty, and z_0=36k^2.
This proves finite positive CONTACT, for the exact required kernels.

## SELECT: deterministic elder identification under the global coupling

On V_0>0 the transverse Hessian is negative, the cubic coefficient is positive,
and the preceding fixed-target genericity holds. The full ST deterministic
vector-ridge lemma applies to the actual coupled global fields, not to an
unconditioned generic replacement. In a small fixed cylinder transverse strict
concavity gives a unique ridge. Its reduced derivative has strictly positive
second derivative. The exact two critical pins at +-r/2 are therefore its only
two nearby zeros; the left one is a maximum and the right one has index d-1.

The trapping boundary is asymmetric. The left and side faces are below the
death level, while the face through the right critical point is at most that
level by transverse concavity. The newborn component cannot escape before
that death level. Beyond the right point the positive cubic ridge reaches a
fixed point with height above b. This is an older component and a closed
level path through the right point meets it. Persisting other Morse branches
and the compact gradient floor ensure global Morse/distinct-height behavior
for small r. Hence the actual intrinsic elder selector is eventually one.
This identifies the ordinary bar, not only a nearby candidate pair. It also
works in d=1, with no transverse side face. It never invokes a false full
symmetric-fold boundary barrier; the positive cubic arm prevents that barrier.

On V_0=0, V_r(1-sigma)->0 regardless of the value of sigma. On V_0>0 it vanishes
eventually by the elder argument. The same polynomial moment domination yields
E[V_r(1-sigma)]->0 and E[V_r sigma]->z_0. No all-mark inverse normalizer, fixed
samplewise chart common to all marks, finite-r unconditional genericity, or
rate is required. This proves SELECT. The optional compact-mark qualitative
uniformity is not used in the density asymptotic.

## ENVELOPE, FAR, and cutoff order

The conditional norm estimate implies E[V_r]<=C(1+|b|+k)^(2d). The first and
fourth target coordinates b-kr^3/2 and 12k retain a uniformly invertible linear
map from (b,k) over the bounded r interval. The covariance floor and upper
bound give

    12 pi_r(v_r) E[V_r]
      <=C(1+|b|+k)^(2d) exp[-c(b^2+k^2)].

Multiplying by k^-2/3 is integrable near k=0; Gaussian tails control the other
mark boundaries; the unit sphere bundle has finite volume. This proves the
all-mark ENVELOPE with one law-dependent r_0. There is no inverse cone mass,
inverse curvature moment, or small-k uniform selector premise hidden here.

For dist(p,q)>=r_0, the actual full first-jet covariance has a positive compact
floor. Regression at (b,0,b-ell,0) gives C2 moments polynomial in 1+|b| on each
bounded lifetime band and Gaussian density decay in b. Integrating candidate
weight bounds the selected density by O(1), uniformly for 0<ell<=1. This is a
bound on the same density representative, which proves FAR. It is not obtained
by differentiating a cumulative bound or by conditioning on a failed local
fold event. The near density is finite for every ell>0 because k=ell/r^3 grows
without bound as r->0 and its Gaussian tail beats every radial power. These
arguments also give local boundedness on compact positive-lifetime bands.

For fixed ell, the near substitution r=(ell/k)^(1/3) leaves the indicator
k>=ell/r_0^3. One first takes ell->0 at each fixed positive k,b,x,u using
CONTACT/SELECT, and then uses the proven common k^-2/3 Gaussian-polynomial
envelope to integrate all marks. A hypothetical small-k collision floor or
quantitative all-mark elder radius would be unnecessary and generally
unavailable. FAR vanishes after multiplication by ell^(1/3). Positivity and
integrability give a finite positive coefficient. Integrating the resulting
density asymptotic gives the cumulative factor 3/2. These are first-moment
statements; no higher moment passage is asserted.

## Curved geometry, dimension one, and the coefficient normalization

The short-pair midpoint map (x,h)->(exp_x(-h/2),exp_x(h/2)) has Jacobian one at
h=0 and is smooth and even under h->-h. Therefore J(x,ru)=1+O(r^2), uniformly
on compact X, rather than identically one at positive r in curved geometry.
Polar h coordinates contribute r^(d-1) dr d sigma. The complete radial ledger
is

    (d-1) from space +3 from the height change
       -(d+3) from the literal observation density +2 from Hessians =1.

Thus r dr is the remaining measure in every fixed d>=1. Combining ell=kr^3
with that measure produces ell^-1/3 and k^-2/3. The exact local coefficient is

    C=(4/V) integral_SX integral_R integral_0^infinity
             k^-2/3 pi_0(b,0,0,12k,0,...) z_0(b,k,x,u) dk db dvol d sigma.

Every factor and the numerical 4 are preserved by the direct source equations
(24)-(25). Since z_0=36k^2 times the conditional transverse determinant-cone
moment, integrate the birth height with its actual joint Gaussian law and
set T=12k. The scalar is 144*12^(-7/3)=12^(-1/3). With G=grad F,
V_u=Hess F(u,.), T=nabla_u^3 F, and A=Hess F restricted to u-perp, this gives

    C=12^(-1/3)/V integral_SX p_(G,V_u)(0,0)
        E[(T_+)^(4/3)(det A)^2 1{A<0} | G=0,V_u=0] dvol d sigma.

The full Schur complement must be retained. General smooth Gaussian laws
need not have odd/even independence; neither p_G p_V nor an independent
T times transverse moment is available without an extra hypothesis. The
conditioned joint Gaussian is centered because the source is centered and
this pin is zero, not because the whole law is stationary.

Replacing u by -u changes T to -T and preserves A, with an absolute-determinant
one transformation of the zero-pinned G,V coordinates. Full sphere area is
invariant. Averaging the two oriented integrals therefore gives exactly

    C=1/(2*12^(1/3)*V) integral_SX p_(G,V_u)(0,0)
        E[|T|^(4/3)(det A)^2 1{A<0} | G=0,V_u=0] dvol d sigma.

This half comes from antipodal averaging, not a new division by unordered
pairs. The earlier ordered maximum/death count already counts every bar once.
No pointwise T/A factorization is needed for this identity.

For d=1 the transverse determinant and cone indicator both equal one and S^0
has ordinary area measure assigning mass one to each of its two directions.
The two-point incidence and the 12r^-4 transform still apply. The index-(d-1)
critical point is a minimum with positive Hessian determinant; a universal
negative-determinant saddle test would fail. The cylinder trap becomes an
interval with a right cut. No d>=2 argument is being silently substituted.

As checks of physical units, F->aF multiplies the pin density by a^-2d and
the fractional/determinant moment by a^(4/3+2(d-1)), so C->a^-2/3 C. Scaling
g->lambda^2 g makes G,V,T,A scale by lambda^-1,lambda^-2,lambda^-3,lambda^-2;
the local density-moment product scales by lambda^-d. The volume normalization
therefore has exactly the per-volume scaling required, while total expected
bar count remains metric-independent. These computations check normalization;
they are not substitutes for COUNT or SELECT.

## Independent bounded controls and preserved refusal cases

The main reviewer ran `independent_jet_normalization_controls.py` once with
Python's exact integer/Fraction arithmetic. Actual receipt
`CONTROL_EXECUTION.json` records execution at 22:01:20 UTC, exit 0, 1947 stdout
bytes and empty stderr. It passed 91 exact checks in four negative-control
families. The checks cover the cubic change-of-variable scalar, antipodal
positive-part to half-absolute averaging with deliberately correlated cone
weights, S^0 mass and empty transverse blocks, amplitude and metric units,
and the dimension-dependent Morse index criterion. They do not approximate
an infinite Gaussian field, Rice integral, root, eigenvalue, or asymptotic
limit. No old or author controls were rerun; no field realization or Lean
process was used.

A useful new nonparity example is F=gH on a flat two-torus, where H is a centered
stationary smooth full-support Gaussian member and g=1+a sin(x_1), 0<a<1.
Multiplication by positive smooth g is a smooth-space homeomorphism, so the
result remains a centered smooth full-support Gaussian series with summability.
At x=0, Cov(F,F_x1)=a Var(H) is nonzero. Gaussian full support therefore does
not imply the odd/even independence used by ST's special parity simplification.
A separate exact two-variable covariance calculation shows that the squared
joint/product zero-density ratio for correlation rho is 1/(1-rho^2), not one.
The proposal correctly uses the general joint-jet coefficient.

Other refusal controls retain the distinction between actual index d-1 and
negative determinant: the d=1 index-0 and d=3 index-2 cases both have positive
determinants. Extra unordered-pair halves and probability-normalized sphere
measures change nonzero exact examples and are rejected. The inherited
non-Gaussian amplitude-mixture falsifier remains a real boundary: covariance,
smooth moments, and Morse pairing alone do not give Gaussian admission or the
2/3 cumulative exponent. No covariance-only extension is adopted.

The focused reviewer performed a different finite Gaussian calculation on
conditional block/tail composition. Its actual report, exact controls, and
seal were read in full and are joined below; their result is not inferred from
this main reviewer's checks. The author reported 137 controls in five negative
families, but those are author evidence only and were not rerun or counted as
independent review checks.

## Classical imports and exact evidence limits

The result is conventional mathematics under the explicit classical imports in
proposal Section 12: compact smooth partitions/cutoffs and local differential
calculus; uniform short geodesics and parallel frames; finite-dimensional
smooth Sard; finite smooth weighted counting/area change of variables; Morse
local form, critical-free compact-band flow and isolated handle attachment;
H0 elder linear algebra; elementary finite Gaussian regression and uniqueness;
and Tonelli, Minkowski and dominated convergence. The proposal does not prove
all of differential topology, measure theory or Morse theory from axioms.
Those are precise accepted premises of this scoped review.

The finite smooth incidence appendix reduces the all-Borel area statement
needed here to Sard and ordinary change of variables, so a generic Kac-Rice
formula with unsuitable mark hypotheses is not being imported. The conditional
Gaussian kernel and remote genericity arguments are proved for the actual law;
they are not left as classical imports. Likewise full support, finite named
jet minors, residual ranks, global norm moments, and all five stochastic
interfaces are new derivations rather than outsourced assertions.

For a bounded primary statement check, the reviewer downloaded and retained
the UT differential-topology notes (636727 bytes, SHA256
`f1018cc3f838da11b3b98a5c39abc6498c0edb0eb615a3ab1f408b68e485e807`) and read the
Sard statement at Theorem 1.5.1, one-based PDF page 14, including its rendered
page and nearby definition of null sets. No full 60-page reading or complete
classical-book read is claimed. The stated smooth Sard theorem is sufficient
for the compact smooth incidence maps. The reviewer's independent appendix
also explains the equal-dimensional case directly. [UT course notes](https://web.ma.utexas.edu/users/abhishek/files/notes/Differential%20Topology.pdf)

The proposal's area/coarea abstract and Stanford handout index remain source
pointers, not proofs that discharge an unproved infinite-dimensional Rice
identity. An initial unused MIT probability PDF lookup returned HTTP 404 and
the web screenshot endpoint failed on the UT URL; both supplied no mathematical
evidence. The actual UT download was successfully rendered locally. The proof
does not use Fernique, which was the purpose of the abandoned lookup. These
access failures are retained as access history, not semantic proof failures.

No original experiment source, author freeze, earlier proof/review, formal
packet preparation file, source branch, native research page, or scientific
status register was changed. The new controls and documents are confined to
this review directory. Mathematical review is distinct from archive custody,
formal kernel execution, experimental observation, external uptake, and
scientific acceptance.

## Focused review join and final disposition

The fresh focused reviewer
`/root/reverse_localization_nonauthor_review_20261017/dense_support_rice_nonauthor`
returned ACCEPT_SCOPED with no must-fix or amendment in §§2–4 and §§6–7.
Its full report is 24252 bytes, SHA256
`a14f009f44a74ff25c9cac3aa779f17c8429865089d7ae656c7c6aeac0b6276b`;
its machine verdict is 2736 bytes, SHA256
`b82e9fcf4a0f7a30ffc8fec3288188c41c9cc8f6814b1ab6da73f5c278ce07f7`;
and its manifest is 3161 bytes, SHA256
`9da5ea841f20d8227aec89d2564a2c1a24865bbfd4358b224e3e994b8c49e469`.
The main reviewer read the full report, machine verdict, manifest and control
program, checked its argument against the frozen proof, and freshly verified
all 8 retained input and 9 output rows. That review independently reconstructs
all-target block/tail precision, normalization, conditional means and covariance,
whole-field Borel pushforward, finite residual genericity, and contact isolation.
It properly notes that an overcomplete/noninjective coefficient representation
is harmless: condition the augmented coefficient/tail law, then push forward
to the field. Neither coefficients nor tails must be recoverable from F.

Its new exact rational controls passed 168 identities and 18 negative instances
in three families, exit 0 with empty stderr. The negative families distinguish
unreweighted conditional tails, unwhitened kernel bases, and remote rank which
collapses after contact conditioning. These are separate from the main
reviewer's 91 checks and four negative families. Across the two programs there
are 259 passed exact checks (the main program includes refusal assertions),
seven distinct negative families, and the focused program's 18 separately
counted negative instances. Counts are engineering evidence supporting the
analytic review, not a proof score. No
old or author controls were rerun. The focused report is unchanged and is
retained under `dense-support-rice/`.

The integrated mathematical disposition is **ACCEPT_SCOPED** for this exact
source-bound actual-law admission theorem. COUNT, CONTACT, SELECT, ENVELOPE and
FAR are discharged for each fixed law in the stated explicit series class,
with its fixed compact connected boundaryless smooth Riemannian manifold and
fixed d>=1. The coefficient in equations (25), (27), and (28), including the
full joint conditional jet moment, the antipodal half, ordinary sphere area,
and empty transverse convention in d=1, is correct. There is no missing
conditional-genericity, full-support, or all-Borel-kernel hypothesis that must
be added to this source. No required proof amendment was found.

Acceptance retains the explicitly stated classical smooth/Morse/measure
imports. It also retains the narrower actual Gaussian-series hypothesis,
positive weights and dense smooth span, all smooth-norm summability, fixed-law
constants, actual intrinsic ordinary H0 observable, and exclusion of the
essential class. Extending to all abstract smooth full-support Gaussian laws,
non-Gaussian covariance classes, uniform degenerating families, quantitative
windows, Hk, factorial moments or Poisson limits would require new arguments.
No such extension is reviewed or inferred. In particular this review does not
close any unrelated formal holds such as C263/C264, does not promote a Lean
packet, and does not substitute for the Root's reading of the entire sealed
review before any adoption decision.

A first identity-checker attempt failed with FileNotFoundError because it used
the workspace instead of the core workroot as the base of four historical
relative ST/IG paths. The failed checker preimage and empty stdout are retained
under `attempts/`; `PATH_BASE_CORRECTION.json` records the explicit corrected
base. This was a local verifier path error, not a source hash mismatch or a
mathematical proof failure. The corrected read-only verifier exited zero and
matched all 35 source/original-input/focused-seal rows. It did not rerun any
control program.

The actual author freeze, original ST/IG inputs, focused review and all output
identities are recorded in the final manifest and readback receipt. The larger
project goal remains ACTIVE / UNMET. Scientific effect: NONE.
