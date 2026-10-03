# C107 source-bound nonauthor technical review

**Verdict: ACCEPT — conditional and scoped, for the exact analytic bytes below.**
No blocking mathematical defect or required amendment was found. This is an
OpenAI same-provider nonauthor technical review, not organizationally independent
review or human mathematical acceptance. Independence credit: **0**. Human
review: **NONE**. Scientific/register effect: **NONE**.

Reviewer: `/root/c107_nonauthor_review`. Authors: OpenAI Codex root and
`/root/c99_custody_audit`. The reviewer did not contribute proof design before
freeze, did not read the candidate before the root's freeze notice, and did not
read author controls until the independent design, implementation and normal / 
optimized execution record had been frozen. The reviewer read the six named
source interfaces and their historical review narratives before candidate
freeze. All parties share one workspace and provider; this is disclosed rather
than converted into independence credit.

## 1. Exact object and sources

The reviewed analytic object is `../PROOF.md`, **29,606 bytes**, SHA256
`d94f8f2f7e809da37465729d3eca5f9793bce5fc5410d9f83e61db259ddf73df`.
The reviewed source manifest is `../SOURCE_IDENTITIES.json`, **2,931 bytes**,
SHA256 `f03da4be8cae14588d7e6e1d215091293dbad199bc9a0013cccca995a4c05a8c`.
The source cut is Math- commit
`7e2344166e989ae94e5732e445f445598fc75c4c`.

Before freeze the reviewer independently used `git ls-tree` and `git show` at
that exact cut and compared all six source byte strings with the audit-tree
copies. After freeze the C107 source copies were separately checked against
the manifest, with all hashes and lengths equal. No conclusion relied on the
audit-tree checkout HEAD being equal to the source cut.

| Key | Original path at source cut | Git blob |
|---|---|---|
| P | `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md` | `dfed3b8d318a3ab1950957f393307733a4bef3f2` |
| E1 | `imports/lifetime_parent_20260925/ERRATUM_CONGRUENCE.md` | `213594d6ca6a86fb938110f4d166d9ce275a02d0` |
| E2 | `reviews/d1_section9_borel_repair_20260925/REPAIR.md` | `fe9b9ce4999908bb3814b500ee2d0ceb0c6f704a` |
| REC | `reviews/d1_chain_reconciliation_20260928/RECONCILIATION.md` | `75da2597971510f843f8d90c743950cb8c177342` |
| RM | `frontiers/remote_window_20260924/PROOF.md` | `b383bfcc88ec4ad497dff01fb6640e429ba24a84` |
| RC | `frontiers/remote_collision_20260928/PROOF.md` | `7b48a88e2af54e759e89a8c8219573bb450a65ea` |

This accepts the C107 implication conditional on its retained interfaces. It
does not newly accept the entire parent P. P §5 is consumed with E1's corrected
congruence and REC's convergence-in-law reading. The full normalizer is
`Z_r=E_Q W_r`; no pin density, adjacency event or restricted good-event
normalizer is substituted. RC's fixed-rho covariance floor is expressly not
used as a moving-rho estimate.

## 2. Analytic review of the new interpolation bound

**Observation blocks — ACCEPT.** Direct substitution into (13) gives the six
coordinates in (10), including the two r-squared corrections. In (16), the
quadratic term contributes `6 delta D` to the gradient difference, while the
cubic term contributes `-6 delta D`; the remainder in the trapezoid expression
is exactly `delta^3 D`. Thus both local right inverses are exact. Their
coefficients remain bounded through confluence. Integral representations of
the original observations, not bounds on their apparently singular finite
differences, justify covariance continuity and the uniform variance upper
bounds.

**Periodic separators — ACCEPT.** For each minimal coordinate displacement,
`1-cos(omega t)` is comparable to `t^2` over the compact fundamental interval.
Their sum is therefore comparable to torus squared distance. The first
derivative has one distance factor, and the second and third are bounded. The
reciprocal derivative formulas consequently give distance powers `-2-j` up to
order three. The apparent `d^-4` third-derivative term is bounded by a constant
times `d^-5` because torus distance is globally bounded. A product of m
reciprocals then costs at most `rho^(-2m-j)` by the product rule. These constants
depend on fixed L, not on pin or witness directions.

**Sine chart and Hermite cancellation — ACCEPT.** On the specified fixed box,
each cosine stays uniformly away from zero; the coordinatewise arcsine inverse
has bounded derivatives through order three. The endpoints lie in a ball of
radius rho/8, their sine images also do, and the inverse of their straight
chart segment stays in the ball of radius rho/4 using inverse Lipschitz
constant at most two. The slightly larger rho/3 neighborhood therefore lies
where the reciprocal bounds are valid. This is a local chart statement; it
does not presume global injectivity of sine.

For the Hermite coefficients, integration of the derivative difference gives
`a2 = [g'(h)-g'(0)]/(2h) - 3h a3/2`. Integrating the cubic Peano kernel gives
`a3 = h^-3 integral t(h-t)g'''(t)dt`. The kernel mass is `h^3/6`, so the cubic
coefficient is bounded independently of h; the quadratic and mixed
coefficients follow as in (25). This verifies the exact factor and sign of
the cancellations and their limits. An orthonormal chord basis preserves
derivative norm bounds even as its direction varies. The physical chord is
never incorrectly identified with the chart chord.

**Close-pair duals — ACCEPT.** The pin-surviving product has two factors and
is bounded below by a constant times rho^4 throughout its chart neighborhood.
Dividing the bounded-data local polynomial by that product costs rho^-7 in
C3. Matching both values and both first-gradient components in chart
coordinates and transforming by the chain rule matches the desired physical
jets exactly. Multiplication by the separator restores the target jets and
kills full first jets at both unwanted sites. The same construction works with
the roles of pin and witness clusters reversed. The distances displayed in
the proof are valid: `rho-r/2 >= 15 rho/16`, and subtracting rho/3 leaves
`29 rho/48`.

The resulting objects are genuine periodic trigonometric polynomials. A cubic
polynomial in two shifted sine coordinates has frequency norm at most three;
the two separator factors add at most two. Translation and orthogonal chord
changes have bounded coefficients. Thus their Fourier coefficient norm costs
rho^-7 in a fixed finite space. The use of the larger degree-seven space is
harmless; the close-pair construction in fact lies in degree five. No
nonperiodic monomial is treated as a Cameron-Martin element.

**Separated witnesses — ACCEPT.** For a singleton, each of the two pins and
the other witness is at least a fixed multiple of rho away. Three separator
factors cost rho^-6 and one reciprocal derivative costs one additional power.
An affine local sine-chart interpolant suffices for its value and full
gradient, giving rho^-7 again. The other witness can be near a torus cut locus
or share the same global sine image: only the surviving singleton's local
chart is inverted. The pin-surviving construction still requires only
separation of both witnesses from 0, not their mutual proximity.

**Simultaneous confluence — ACCEPT.** For each fixed positive rho, the dual
coefficient vectors lie in a fixed finite-dimensional space and are uniformly
bounded. Along any convergent parameter sequence, a coefficient subsequence
converges; continuity of the integral observation functionals preserves the
exact right-inverse identities. This is enough for every boundary
configuration without a globally continuous choice of frame or interpolant.
Repeated separator factors have a zero of order four and annihilate the
contact derivatives through order three. The constants were already uniform
in rho from the reciprocal/chain-rule estimates; compactness here is used to
pass to confluence, not to manufacture a rho-uniform lower bound.

## 3. Covariance and regression accounting

**Joint covariance — ACCEPT.** The finite Fourier support has strictly
positive fixed variances under the exact periodic Gaussian model. Norm
equivalence on this one fixed space gives a right inverse of norm at most
`C rho^-7`. If it maps a to a, evaluating the covariance representer of
`a dot L` against that dual gives `|a|^4 <= Var(a dot L f) C rho^-14 |a|^2`.
This establishes the stated joint floor `c rho^14 I` rather than merely
positive definiteness at every point. The integral derivative representations
give a uniform upper bound. All arguments are in physical coordinates and
uniform in frames; no rotational invariance of the torus is assumed.

**Conditional covariance and mean — ACCEPT.** Taking the infimum of the joint
quadratic form over the pin component proves the same lower floor for the
witness Schur complement. Conditioning cannot increase covariance. The mean
uses the stronger, rho-independent inverse covariance of the desingularized
pins from (12), together with bounded pin targets and cross-covariances.
Using the joint rho^14 floor to estimate this mean would create an avoidable
loss; the proof does not do that.

**Density and height-difference tail — ACCEPT.** Six conditional coordinates
give determinant lower bound `c rho^84`, hence density prefactor rho^-42.
The covariance upper bound gives a rho-independent Gaussian tail about the
mean. Since that mean and y are bounded, its restriction to the actual
height-difference coordinate t is bounded by `C rho^-42 exp(-c t^2)`.
This tail bound is not inferred from the lower covariance floor.

**Conditional global derivative moments — ACCEPT.** For an original
standardized real Fourier coefficient, its residual variance after either
conditioning is at most one. Conditional covariance positivity gives
`c_j S^-1 c_j^T <= 1`. Cauchy-Schwarz in this covariance inner product then
bounds the shift by the square root of target energy, at most
`C rho^-7(1+|v|)`. Summability of the deterministic Fourier C3 amplitudes and
Minkowski give the global C3 norm moment bound, with no independence
assumption on the residual coefficients. Finite partial sums converge in
Lp(C3) under this bound; canonical Gaussian regression supplies the version
at every target v. This justifies exponent `7p`, not `14p`. The eighth moment
therefore costs rho^-56, and density times moment costs rho^-98.

The exact stress model `U=G1`, `V=G1+rho^7 G2`, `Z=G2` independently verifies
why one cannot simply discard this regression loss: under U=0,V=t the mean
of Z is exactly `t rho^-7`. A covariance with both small and O(1)
eigenvalues also distinguishes the determinant prefactor from the tail scale.

## 4. Counting, determinants and integration

**Pathwise determinant bounds — ACCEPT.** The two gradient pins force a small
axial Hessian direction at each endpoint by subtracting its segment average.
In the plane, `|det H| <= |He| ||H||op` gives endpoint weight at most
`C r^2 K^4`. The same calculation at a critical witness pair gives two
small directions, hence product of witness determinants at most
`C delta^2 K^4`. These identities continue to hold under the additional
witness conditioning because the original pin constraints remain in the
conditional support. The resulting eighth moment is exactly the one used
in the density estimate; no independent weight bound is substituted.

**Weighted pair Kac-Rice — ACCEPT, conditional on the retained interface.**
Under Q the process is the four-dimensional pair of witness gradients, with
block diagonal derivative and one determinant per witness. On compact
subsets off the diagonal and away from pins the covariance is nonsingular,
and the Gaussian conditional field law is continuous. Smooth genericity can
be checked there from distinct-site jet nondegeneracy as in the retained
interface. Truncated endpoint weight and open height/type restrictions are
appropriate lower-semicontinuous marks. The Borel location identity and
whole-field conditioning are read with E2. Exhaustion and monotone convergence
give the extended nonnegative identity, after which the finite estimates
establish integrability. The endpoint weight and the full denominator each
appear once; the conditional formula carries no extra pin density or pin
coordinate Jacobian.

**Near-diagonal integration — ACCEPT.** In two dimensions the raw-to-V
Jacobian is delta^-5. Height disintegration gives delta^3 and polar area gives
delta. Together with both small Hessian determinants the remaining power is
`1-5+3+2=1`. The bounded integrable function
`(1+|t|)^8 exp(-c t^2)` has integral over any interval of length ell at most
`C min(1,ell)`, uniformly in its location. This is the necessary saturation
when the second window becomes wide in divided-difference coordinates.
After the first height window and endpoint/normalizer cancellation, the
integral is bounded by
`C rho^-98 |E| r^3 integral delta min(1,k r^3/delta^3) ddelta`.
Splitting at `(k r^3)^(1/3)` gives `3(k r^3)^(2/3)/2`, hence r^5.

The enlargement of the angular/radial domain is legitimate because the proof
first obtains its bound where both points are in the original pair domain,
and then integrates that nonnegative bound on a larger domain. It does not
apply the covariance assertion to a newly admitted point inside the pin ball.

**Separated branch and conclusions — ACCEPT.** Here both raw heights are in
bounded targets and supply r^6 in total. The same rho^-98 bound applies and
there is no need for polar coordinates. Since torus area is at most L^2,
`r^6 |E|^2 <= r_* L^2 r^5 |E|` also works for arbitrarily tiny E. Ordered
factorial counting and both integer inequalities in (8) are correct.
Substituting rho=r^alpha yields `2-98 alpha`, strictly positive exactly for
the stated interval `0<alpha<1/49`. The radius band eventually holds because
alpha<1, and `|E_r|<=L^2` gives the displayed convergence. Equality at the
threshold yields no little-o conclusion from this estimate.

## 5. Independent controls and later author-code exposure

`CONTROL_DESIGN.md` was frozen before implementing or opening author tests:
SHA256 `161b0c0dc3b18db32a7ba61a868a944d5767c8b780281901ccc5c9f1435f51bb`.
The independent implementation `independent_controls.py` has SHA256
`ae449870aa408a5437d5990b50d331a8af3d4eb063c8c7476f781677530ca873`.
`INDEPENDENT_RUNS.json`, SHA256
`3ca33cc27729378744721b0a3bcc988b733410d3394b5dda4f2ca6048c29a424`, records
normal and optimized PASS, **425 positive evaluations across 30 families**
and **46 rejected mutant evaluations across 13 families**. It also records
zero author-checker exposure at the time of that freeze and the source-copy
hash checks.

The strongest operational tests construct actual periodic duals with rational
sine/cosine coordinates, match complete physical jets, kill the unwanted
jets, vary shrinking cluster separations, and check the repeated-separator
contact derivatives. Broken inverse-chart differentiation, omitted separators
and simple-zero gradient killing are rejected by these evaluations. Other
controls independently cover cancellation, right inverses, covariance energy,
the exact Jacobian, a planar fold, radial saturation, and strict scope limits.
Some elementary exponent/integer controls are bookkeeping tests; none is
presented as a continuum proof.

Only after this independent run freeze did the reviewer open the author
design and implementation. Their observed identities are:

- `author_controls.py`: SHA256
  `9063ffb1c09c3ea62cc5dd7e0663ba4a9dada240ff7f9504a5bebfd7e92fec87`;
- `CONTROLS_DESIGN.md`: SHA256
  `963a797c28c5872097421187d3332e7e9041435d1eb31fca0a186e8dab4f6de7`;
- `AUTHOR_CONTROL_RUNS.json`: SHA256
  `ee15e53018b87d160a0824c684b0eac8b0b598bd24bd3bf49298a1d3edb79bfe`.

That later read is separate engineering scope. The code uses exact rational
Laurent-polynomial evaluation, retains the quotient and sine-chart derivative
corrections, and includes the distant equal-global-sine-image fixture.
`AUTHOR_CHECKER_REPLAY.json` records this reviewer's later execution, including
stdout and its actual runtime. Author tests support the finite construction;
they are not the basis for the analytic verdict. The author's recorded first
launch failed before running the script because of the executable basename;
the author record discloses it and distinguishes the later successful runs.

## 6. Findings and strict stopping boundary

There are **no required changes** to the frozen analytic object. The new
covariance floor, confluence argument, periodic realization and regression
exponent are justified at the stated scope. No finite numerical constant or
optimal exponent has been certified.

This review accepts only the conditional planar estimate for deterministic
Borel `E subset D_rho`, fixed L, compact B, positive compact K, all frames,
and `0<r<=min(r_*,rho/8)`, including its separated branch, integer
consequences and strict moving-rho exponent range. It does not supply an
inner-ball estimate, mixed inner/outer pair bound, outer conditional presence
given an inner witness, all-region collision estimate, first-moment
asymptotic at moving rho, elder identification, barcode identification,
dimension extension, unbounded-mark uniformity or uniformity at k=0.

Any dependent claim needing one of those interfaces must stop at that missing
interface. Neither this verdict, a green finite checker, a publication packet
nor a merge supplies it. No source file, claim register or proof was edited by
this reviewer; all reviewer writes are confined to this directory.
