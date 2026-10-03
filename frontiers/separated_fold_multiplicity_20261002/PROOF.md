# Separated folds force multiple ordinary short bars

Object: OA-SEPARATED-FOLD-MULTIPLICITY-20261002-v1.  
Actual author: OpenAI / GPT-6 Astra Pro.  
Program: Universal Law, initiated, directed and supported by Dylan Roy.  
Disposition: new author-side proof candidate; nonauthor review pending. Scientific-status effect NONE.

This is a successor to the two-bar question in Math-#235 comments 5942428034,
5942496197 and 5942555223, not an amendment of C52 or of a reviewed parent.
Pickup: #235/5943116501. The construction concerns the **original unconditioned
field**, not a pair-Palm law, replacement-bar population or independent-region
model. The proof below does not use the D1 density asymptotic, a Kac–Rice count
expansion, the finite-part coefficient, or independence of spatial regions.
Only the optional consequences in Section 7 consume those separate interfaces.

## 1. Statement and exact scope

Fix d >= 2 and L > 0. On the flat torus X = R^d/(L Z^d), let F be the centered
variance-one Gaussian field with covariance

    K_L(z) = sum_{j in Z^d} exp(-|z+Lj|^2/2)
               / sum_{j in Z^d} exp(-|Lj|^2/2).

Use ordinary **superlevel H0 persistence**, with a bar born at the maximum of
the younger component and dying at its actual global elder merging saddle.
Exclude the essential global-maximum class. K_t counts all finite bars with
lifetime in (0,t] in one field on the whole torus; it is not divided by volume.

**Theorem SF.** Let n >= 1 be a fixed integer, and let U_1,...,U_n be prescribed
pairwise disjoint nonempty open subsets of X. There are constants c_n > 0 and
t_n > 0 such that, for every 0 < t <= t_n,

    P(there is an actual finite elder bar (M_i,S_i) in each U_i,
      with t/8 <= F(M_i)-F(S_i) <= t, for i=1,...,n)
        >= c_n t^(2n/3).                                      (SF)

In particular P(K_t >= n) >= c_n t^(2n/3). The endpoints and the separating cap
of each constructed bar lie in its own U_i. The bars are distinct. Constants
depend on d,L,n and the chosen regions; no useful numerical value or parameter-
uniform bound is asserted. The n=2 construction establishes a genuine lower
bound for the original field, rather than only the abstract Bernoulli example.

No assertion is made that this is the sharp order, that K_t equals n, or that
separated folds exhaust multiple-bar configurations. There is no Poisson law,
region independence, factorial-moment asymptotic, increasing-volume limit or
asymptotic two-bar mark measure in this statement. Higher-corank/clustered events
may produce additional mass.

## 2. Smoothness, nondegeneracy and the Gaussian coordinates actually used

Poisson summation, with frequencies 2pi k/L, gives

    K_L(z) = sum_k a_k exp(2pi i k.z/L),
    a_k = exp(-2pi^2 |k|^2/L^2) / sum_j exp(-2pi^2 |j|^2/L^2) > 0.       (2.1)

This is the exact model in [P] Sections 1–2. In a real sine/cosine basis all
coordinate variances are positive and distinct coordinates are independent.
The positive constants attached to sine/cosine normalization are immaterial
below. For every integer q >= 0,

    sum_k sqrt(a_k) (1+|k|)^q < infinity.                       (2.2)

The expected sum of the C^q norms of the Gaussian Fourier summands is finite.
It follows that the series converges absolutely in C^q almost surely, and its
high-frequency remainder R_N satisfies

    E ||R_N||_{C^4} -> 0.                                    (2.3)

It is independent of the finitely many Fourier coordinates of P_N = F-R_N.
In particular, for each epsilon > 0, a sufficiently large **fixed** N gives

    P(||R_N||_{C^4} < epsilon/2) >= 1/2.                      (2.4)

All finite coordinate changes within the low-frequency space produce a
nondegenerate finite-dimensional Gaussian vector; their coordinates need NOT
remain independent. We use a conditional density, not such an independence
claim, in Section 6.

For completeness, this field is almost surely Morse with pairwise distinct
critical values. Every finite set of independent point-derivative functionals
has a positive Gram matrix: a zero-variance linear combination would annihilate
all Fourier modes, hence would be the zero distribution. Disjoint bump tests
and arbitrary prescribed finite jets force its coefficients to vanish. At one
site the same conclusion follows from independence of the derivative polynomials.

Apply this to (grad F(x), H_F(x)v), with |v|=1. Its range dimension is 2d and
its parameter dimension is 2d-1; H -> Hv is surjective on symmetric matrices.
For distinct x,y, use (grad F(x), grad F(y), F(x)-F(y)), whose dimensions are
2d+1 and 2d. On compact domains separated from x=y, covariance continuity gives
bounded densities. A C^1 random map from q parameters to p>q coordinates with
bounded point densities has no zero: on the event its derivative norm is <=M,
a zero requires a mesh value to lie in a ball of radius O(M epsilon). The
union probability is O(M^p epsilon^(p-q)). First send epsilon to zero, then
M to infinity; countable domain exhaustion handles all sites and directions.
This is the elementary genericity argument of [P] Section 8 without its pins.
Compactness and nondegenerate critical roots then give finitely many roots.

We work on this single unconditional full-probability locus. Removing its null
complement from the constructive event below does not change the probability.
No genericity is demanded separately for every residual sample or for every
uncountable parameter value.

## 3. A uniform local deterministic family

Choose a common small a in (0,1/8], with disjoint embedded coordinate cylinders

    D_i = [-a,a] x closed B_{d-1}(0,a) subset U_i,

and slightly larger disjoint coordinate neighborhoods. Such a is available for
any fixed finite collection of the stated open sets. The coordinates are local
Euclidean coordinates of the flat torus. Choose a smooth periodic template f_*
and smooth periodic parameter directions h_i^* with, on those larger neighborhoods,

    f_*(x,y) = b_i - x^3/3 - |y|^2/2,
    h_i^*(x,y) = x,        h_j^*(x,y) = 0 for j != i.          (3.1)

One obtains these by bump functions with disjoint supports; their behavior
outside the neighborhoods is unrestricted. The constants b_i may be chosen
arbitrarily and fixed. Put

    delta = a^2/100,      eta = a^3/100,
    D = [-delta,delta]^n.

Consider a family

    f_{s,e} = f_0 + sum_j s_j h_j + e,    s in D,              (3.2)

where f_0,h_j approximate f_*,h_j^* in C^4 and e is a C^4 error. There is a
single sufficiently small bound on these errors such that the conclusions
below hold for every s in D and every allowed e. The bound is independent of
t and of the specific error sample. Dimension-dependent coordinate norm factors
are included by choosing that bound small enough.

### 3.1 Transverse ridge and fold discriminant

The transverse Hessian is <= -I/2 on each D_i. Uniformly small transverse
linear perturbations give a unique maximizer y=h_i(x;s,e) in each closed fibre,
with |h_i| <= a/4. For example, Taylor from y=0 gives strictly negative outward
radial derivative on |y|=a/4 when |grad_y f(x,0)|<a/8; strict concavity rules
out other maximizers. The implicit function theorem gives a C^3 ridge.

Let g_i(x;s,e)=f_{s,e}(x,h_i(x;s,e)). On the compact parameter cube and axial
interval these functions are uniformly C^3-close to b_i+s_i x-x^3/3. Therefore,
after reducing the fixed approximation/error bounds, we have

    -3 <= g_i''' <= -1,
    g_i''(-a/4)>0,   g_i''(a/4)<0.                           (3.3)

There is one inflection z_i in (-a/4,a/4). Define its unfolding coordinate

    mu_i(s,e) = g_i'(z_i(s,e);s,e).                          (3.4)

In the ideal family mu_i=s_i. For the perturbed family we can ensure

    ||mu(0,e)||_infinity <= delta/4,
    sup_{s in D} ||D_s mu(s,e)-I||_{infinity->infinity} <= 1/4.   (3.5)

Here is the derivative that justifies the second assertion. Stationarity in y
implies partial_{s_j}g_i=h_j(x,h_i), and differentiating in x gives

    partial_{s_j}mu_i = (h_j)_x + (h_j)_y . partial_x h_i,
                         evaluated at x=z_i.               (3.6)

The additional term g_i''(z_i) partial_{s_j}z_i vanishes. At the ideal family
the right side is exactly the identity matrix. Its continuous dependence on
the fixed C^4 neighborhood, uniformly on the compact sets, proves (3.5).
This is a simultaneous n-parameter statement: no neglect of cross-region
parameter effects in the actual approximating functions is permitted.

The value comparison needed for the outer faces is also uniform:

    |g_i(x;s,e) - (b_i+s_i x-x^3/3)| <= eta.                 (3.7)

Indeed f differs from the ideal function by <=eta on the whole cylinder.
Taking the maximum over y preserves that bound, because the ideal transverse
maximum is at y=0. Choose the C^4 neighborhood to include this C^0 bound.

### 3.2 Two roots and the true gap

If 0<mu_i<=delta/2, Taylor's integral formula at z_i gives, writing v=x-z_i,

    mu_i - (3/2)v^2 <= g_i'(z_i+v) <= mu_i - (1/2)v^2.       (3.8)

Since g_i'' is strictly decreasing through zero, g_i' increases on the left
and decreases on the right. There are exactly two roots x_-<z_i<x_+, whose
distances to z_i lie between sqrt(2mu_i/3) and sqrt(2mu_i). Both lie in
(-a/2,a/2): sqrt(2mu_i)<=sqrt(delta)=a/10 and |z_i|<a/4.
The full critical points S_i=(x_-,h_i(x_-)) and M_i=(x_+,h_i(x_+)) have
indices d-1 and d, respectively. This follows from the negative transverse
block and its Schur complement g_i''; the sign is positive at x_- and negative
at x_+. The full Hessians are nondegenerate.

Their height gap is the integral of g_i' between the roots. The symmetric
inner interval |v|<=sqrt(2mu_i/3) is contained between them; integration of the
lower parabola on that interval supplies the lower bound. Integrating the
upper parabola on |v|<=sqrt(2mu_i) supplies the upper bound. Thus

    (4/3)sqrt(2/3) mu_i^(3/2) <= gap_i
             <= (4/3)sqrt(2) mu_i^(3/2),
    mu_i^(3/2) < gap_i < 2 mu_i^(3/2).                      (3.9)

For a fixed t, require each unfolding coordinate to lie in

    Q_t = [t^(2/3)/4, t^(2/3)/2]^n.                         (3.10)

Then each gap belongs to [t/8,t], since its upper bound is t/sqrt(2)<t.
Restrict t once and for all so that t^(2/3)<=delta/2 and t<=a^2/16.

## 4. Each constructed pair is a GLOBAL ordinary elder pair

This is the load-bearing deterministic step. Identifying the two critical
points and their height difference alone is insufficient.

Write birth_i=g_i(x_+) and death_i=g_i(x_-). From (3.7), |s_i|<=delta and
|x_+|,|x_-|<=a/2, the two axial margins satisfy

    g_i(-a)-birth_i >= (7/24)a^3 - (3/2)delta*a - 2eta
                    = (77/300)a^3 > a^3/4,
    death_i-g_i(a)  >= (77/300)a^3 > a^3/4.                 (4.1)

The first cubic margin uses a^3/3+x_+^3/3 >= 7a^3/24; the second is analogous.
Both parameter and approximation errors are subtracted, not omitted.

Define the closed cap

    C_i = [x_-,a] x closed B_{d-1}(0,a).

The derivative sign pattern makes g_i(x)<=birth_i throughout [x_-,a]. Thus
f<=birth_i on C_i. On its left face, transverse maximality gives f<=death_i,
with equality only at S_i. Its right face is strictly below death_i by (4.1).
On the lateral face, strong transverse concavity and |h_i|<=a/4 give

    f(x,y) <= g_i(x) - (1/4)|y-h_i(x)|^2
            <= birth_i - 9a^2/64 < death_i,                (4.2)

because gap_i<=t<=a^2/16. These inequalities cover intersections of faces as
well. M_i is interior. There is no point older than M_i inside C_i.

On the ridge path from M_i leftwards to (-a,h_i(-a)), the smallest value is
exactly death_i: the ridge decreases to S_i and then increases. The endpoint
is strictly older than M_i by (4.1). Hence the global maximin connection level

    d_f(M_i) = sup_{paths from M_i to {f>birth_i}} min f

is at least death_i. Conversely, every such path has its endpoint outside C_i
and must first exit through the complete boundary, where f<=death_i. Its
minimum is at most death_i, even if the path subsequently wanders or reenters.
Therefore d_f(M_i)=death_i.

On the Morse distinct-critical-value locus this is exactly ordinary superlevel
H0 death of the component born at M_i at S_i. To see why, a connection to an
older component above death_i would violate the upper maximin bound; below
that level the explicit path connects to a point above birth_i. Compactness
and distinct critical values identify the unique death critical point. The
older-reaching endpoint excludes an essential class. No unstable-manifold,
Morse–Smale or remote-independence assertion is used.

The caps are in disjoint U_i, so the maxima, death saddles and bars are distinct.
Among Morse distinct-value extensions, arbitrary changes outside the protected
cylinders preserve these conclusions.

## 5. The volume of simultaneous near-fold parameters

For each fixed allowed e, (3.5) implies that mu(s,e)-s is 1/4-Lipschitz in the
infinity norm. If ||v||_infinity<=delta/4, the map

    s -> s + v - mu(s,e)

is a contraction of D into itself: its norm is at most
(delta/4)+(delta/4)+(delta/4)=3delta/4. There is a unique solution mu(s,e)=v,
and this solution is interior. The same Lipschitz estimate proves that mu is
injective on D. The derivative is nonsingular, since ||Dmu-I||<1, and the
inverse is C^1 on this target cube.

By the selected t restriction, Q_t is contained in that target cube. Hadamard's
inequality and the row-sum bound in (3.5) give

    |det D_s mu| <= (5/4)^n.

The usual finite-dimensional change of variables therefore yields

    Leb{s in D: mu(s,e) in Q_t}
       >= (4/5)^n Leb(Q_t)
       = 5^(-n) t^(2n/3).                                (5.1)

A matrix's row **sums**, not just its diagonal entries, control this conclusion.
The map need not be diagonal, its coordinates need not be independent, and
its centre may depend on the residual field. The construction specifically
retunes the finite parameters to that residual-dependent centre. It does NOT
require the residual field to be within O(t) of the template.

## 6. Positive probability for the original Gaussian field

Here we realize the deterministic family using the actual Fourier series.
Smooth periodic functions can be approximated in C^4 by real trigonometric
polynomials: repeated integration by parts makes the Fourier coefficients of
the templates absolutely summable with the required derivative weights.
Choose fixed trigonometric polynomials f_0,h_1,...,h_n approximating (3.1) as
accurately as needed in Section 3. The h_i are linearly independent, since
the matrix of their axial derivatives at the n centres is close to the identity.

Put them in a finite symmetric Fourier space V_N. Enlarge N, if necessary, so
that the tail event (2.4) has probability at least 1/2 for the fixed error
tolerance used in Section 3. The approximants remain fixed elements of the
enlarged space. Complete h_1,...,h_n to a real basis by e_1,...,e_m. Write

    P_N = sum_i A_i h_i + sum_j B_j e_j,
    f_0 = sum_i a_i^* h_i + sum_j b_j^* e_j.                (6.1)

The vector (A,B) has a positive definite Gaussian covariance by (2.1). In
particular A|B=b has a positive definite covariance independent of b and an
affine conditional mean. Choose a small compact box B_0 about b^* whose
probability is positive and for which

    ||sum_j (b_j-b_j^*)e_j||_{C^4} < epsilon/2.

The m=0 case simply omits this factor. The high-frequency field R_N is
independent of (A,B). On B in B_0 and ||R_N||_{C^4}<epsilon/2, let

    s=A-a^*,   e=sum_j(B_j-b_j^*)e_j+R_N.

Then F is exactly (3.2), not an approximate Gaussian replacement. All the
uniform deterministic conditions apply whenever s in D. The conditional
Gaussian density has the strictly positive compact-set floor

    g_* = inf_{s in D, b in B_0} p_{A|B=b}(a^*+s) > 0.       (6.2)

This does not assert that the A_i or the regions are independent. Combining
(5.1) with (6.2), for each allowed b and residual sample the conditional
probability of the fold-parameter event is at least

    g_* 5^(-n) t^(2n/3).

The ridge, inflection and parameter inverse depend continuously on the field
in the fixed C^4 neighborhood, so these events are Borel. Conditional Fubini
and independence of the high Fourier tail from (A,B) now give

    P(event in SF) >= [P(B in B_0) g_*/(2*5^n)] t^(2n/3).    (6.3)

The global nongeneric null event from Section 2 may be removed. Define c_n
by the bracket, reduce t_n to the finitely many restrictions in Sections 3–4,
and Theorem SF follows. Every approximation, Fourier cutoff, box and density
floor was fixed before t tended to zero. The probability cost of the residual
neighborhood is a fixed positive constant, not a hidden small-ball rate.

## 7. Consequences and the precise sampling obstruction

### 7.1 A lower bound for the missing count correction

Take n=2 and abbreviate its positive constant by c_*. Define

    m(t)=E K_t,  p(t)=P(K_t>0),
    D(t)=E[K_t 1{K_t>=2}],  delta(t)=E[(K_t-1)_+].

When m(t) is finite, delta(t)=m(t)-p(t); the nonnegative expectations also
make sense without that assumption. Pointwise count inequalities and (SF) give

    D(t) >= 2c_* t^(4/3),
    delta(t) >= c_* t^(4/3).                               (7.1)

Since 4/3-10/7=-2/21, neither quantity is O(t^(10/7)). This is now an
actual-field obstruction. The previous independent-Bernoulli example only
refuted a general logical inference; (SF) establishes the lower order here.
It is consistent with C52's planar D(t)=o(t^(2/3)). It neither proves nor
refutes preservation of the first correction at order t^(5/4).

### 7.2 The three-term expected count cannot simply become the occurrence law

Conditionally on the exact pointwise density interface E3+ in [RATE],

    nu_eld(l) = c l^(-1/3)+c1 l^(1/4)+c2 l^(1/3)+O(l^(3/7)),

integration gives for the WHOLE torus

    m(t)=a0 t^(2/3)+a1 t^(5/4)+a2 t^(4/3)+O(t^(10/7)),
    (a0,a1,a2)=L^d ((3/2)c,(4/5)c1,(3/4)c2).               (7.2)

If p(t) had all three identical coefficients and remainder O(t^(10/7)), its
difference from (7.2) would contradict (7.1). Thus that proposed transfer is
false. If a three-term p expansion exists with the first two coefficients
unchanged and third coefficient b2, then a2-b2>=c_*. We do not prove existence
of that expansion or compute b2.

The needed next object is the actual multi-bar excess, not merely another
single-bar coefficient. The exact identity

    p(t)=m(t)-P(K_t=2)-E[(K_t-1)1{K_t>=3}]

shows why a two-bar asymptotic and a >=3 control would help. (SF) alone does
not supply either upper estimate and does not identify a two-bar limit law.

### 7.3 Marked laws: no unjustified lower bound for a particular mark

For any common measurable bar mark X_i and integrable K_t, define the finite
measures I=E sum_i delta_{X_i} and J=E[1{K_t>0}(1/K_t)sum_i delta_{X_i}].
Then R=I-J is positive, its mass is delta=m-p, and, when delta>0,

    I/m = (p/m)(J/p) + (delta/m)(R/delta),
    TV(I/m,J/p) = (delta/m) TV(R/delta,J/p) <= delta/m.      (7.3)

TV here is the supremum over measurable sets. If every mark is the same,
the TV distance is zero even when delta>0. Therefore (7.1) does NOT give a
lower bound for the lifetime-only or endpoint-only mark discrepancy.

There is an optional **field-aware count-mark** consequence in d=2. On the
additional [O] premises m(t)~a0 t^(2/3) and P(K_t=1|K_t>0)->1, use the mark
X_i=K_t on every bar. The event X_i=1 has probability p1/m under intensity
selection and p1/p under field-first selection. Its discrepancy is exactly

    p1*delta/(m*p) = (p1/p)(delta/m) >= c' t^(2/3)          (7.4)

for sufficiently small t. Thus a bound O(t^(16/21)) uniformly over ALL
field-aware marks is impossible on these premises. This does not extend [O]
to higher dimensions, prove a rate for its leading convergence, or prevent
cancellation for a specific mark.

## 8. Sources, controls and review obligations

[P] is pinned for the exact Fourier model, finite-jet rank and ordinary
maximin interpretation. Sections 2–6 reconstruct the support, genericity,
parameter-volume and global-cap argument explicitly. No P theorem A/B/C or
weighted Kac–Rice estimate is consumed in SF. [RATE] is used only by (7.2),
and [O] only by (7.4) and the stated compatibility comparison. Their original
conditional scopes and review limitations remain. SOURCE_BINDINGS.json names
these exact interfaces; their surrounding proof bodies are not reaccepted.

The finite controls verify cubic-gap algebra, both cap-face margins, Hessian
inertia under a nontrivial shear, matrix row/Jacobian bounds, correlated linear
unfoldings, exponent arithmetic, count and marked-measure identities, and
falsifiers for missing Jacobians, false exponents and sampling bias. They do
not establish C^4 approximation, the implicit function theorem, a Gaussian
small-ball event, global continuum topology or the positive probability in SF.
Those are the written analytic proof, not a test-grid inference.

Requested nonauthor scopes:
- A: uniform deterministic family, discriminant derivative, exact roots/gap,
  all cap faces and the actual global elder implication (Sections 3–4).
- B: Fourier construction, fixed residual neighborhood, conditional density,
  simultaneous inverse map, Jacobian, measurability and probability (2,5,6).
- C: count obstruction, volume factors, optional imported rate and mark-law
  hypotheses, especially what does NOT follow (Sections 1,7).

No self-merge, scientific register change, institutional validation, calibrated
constant, full formalization or priority-over-literature claim is made.
