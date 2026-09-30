# Two-scale marked clusters and localization of all leading pair mass

Object: OA-TWO-SCALE-CLUSTER-GEOMETRY-20260929-v1.
Author: OpenAI / GPT-6 Astra Pro, foreground recovery, 29 September 2026 (Central).
Disposition: AUTHOR-SIDE CONDITIONAL PROOF; NONAUTHOR REVIEW REQUIRED.
Scientific effect NONE. No source proof, prior verdict, global register, Boolean,
prize or integration disposition is changed. A shared GitHub account is not
organizational independence.

## 1. Exact interface, not a silent revalidation

Fix d>=2, L>0, k>0, b in R, and one orthonormal axial/transverse frame. Use the
original periodized Gaussian field, pins M=(-r/2,0), S=(r/2,0), values b,b-kr^3,
zero gradients, determinant weight W_r and FULL normalizer Z_r of [SC]. Write
P_r=Q_r^W. N_r counts all additional critical points in the open height window,
excluding M,S. No observation set or normalizer is replaced.

All source identities are in SOURCES.json. This paper is a new conditional
consumer of [SC], not a review of it. In particular:

[SC] frontiers/spectral_cluster_closure_20260929/PROOF.md, exact commit
7a44130b41b827577424a73c4feac4cde20b5568, blob
16c56821b52fd76b0be791622b9c3809eafde75a.

[CUB] frontiers/planar_cubic_cluster_20260929/PROOF.md, exact commit
bfcc67dc8957b3ed1fbb789e5a0305e98d7359c8, blob
bb446d08db8a944537a743ad550b88c1c2ad5758. Only its deterministic cubic classifier
is consumed; not its separate Gaussian compact-sector theorem.

[RM] frontiers/remote_window_20260924/PROOF.md, Sections 2-5: the complete
height-disintegrated integrand in (12) is Lambda_j(x)+O_rho(r), uniformly at
fixed remote separation rho and throughout the window.

[C6] frontiers/c6_palm_route_20260929/PROOF.md, Theorem Q, together with [SC]'s
first moment: every fixed ordinary count moment is O(r^3).

[P] imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md,
Section 2: full distinct-site jet rank. Used only for the finite-r spatial
absolute-continuity statement in Section 6.

RM, C6 and P are pinned at source cut 7a1cb09a9d58d179393e6d29146252f714b9c9bf.
A defect or unfulfilled condition in an imported result blocks the corresponding
application here. Publication, tests and a status string do not remove that
condition. No theorem from the competing #159 proof or the #157 Fourier packet
is imported.

The following exact portions of SC are needed, not just its final count law:

* (14)-(18): the integrable full-field/spectral near-occurrence majorant,
  negligible exceptional branch, and pointwise convergence of the individual
  roots, heights and indices in each fixed rescaled ball.
* (19)-(20): a finite spectral measure on nonempty cubic configurations, with
  positive masses a1,a2 for one and two points.
* (21)-(25): beta_far=k integral Lambda is finite and positive, remote multiple
  probability O_rho(r^5), mixed near/remote probability o_(R,rho)(r^3), and
  middle-window mean <=C r^3(R^-2+rho^2), with the last constant independent
  of R>=4 and small rho.
* (3), or its C6 tail argument: polynomially weighted count convergence and
  E_r N_r^p=O_p(r^3) for every fixed positive integer p.

Let m=d-1. In SC's coordinates theta=(s,h,O,tau), ordered hard eigenvalues are
0<h2<...<hm, dO is NORMALIZED Haar on O(m), and tau is the full third-derivative
tensor except f_xxx, rotated with the same orthogonal frame. Denote its soft
entries by a=tau_xxz, beta=tau_xzz, c=tau_zzz. Set

    A0=O diag(0,-h2,...,-hm) O^t,
    H(h)=product_(j=2..m) h_j^3 product_(2<=i<j<=m)(h_j-h_i).

With c_m fixed by SC (8), z0 the full normalizer limit, and h0 the RAW contact
jet density, retain the measure

    dM(theta)=(c_m/z0) h0(A0,Rot_O(tau)) H(h)
                     w(s,a,beta) ds dh dO dtau.                 (M1)

It is extended by zero off the typed domain s<-|B|/2, where
B=beta-a^2/(12k) and w=9k^2(4s^2-B^2). Empty hard products are one for d=2.
The measure M on the whole typed domain need not be finite. Its restriction
to NONEMPTY cubic configurations is finite; that is the measure used below.

The original, unsheared planar cubic is

    P_theta(X,Z)=2kX^3-3kX/2-k/2+sZ^2/2
       +(a/2)(X^2-1/4)Z+(beta/2)XZ^2+(c/6)Z^3.                (M2)

Its additional window roots form C(theta), with n(theta) in {0,1,2}. Each has
index d-1 in the full field limit. In the fixed original frame its limiting
position is X e_axis + Z e_soft(O), not the sheared coordinate u. This distinction
is essential for the radius calculation in RADIAL_TAIL.md.

## 2. A configuration space that retains both spatial scales

Choose ANY deterministic positive cutoff delta_r satisfying

    delta_r -> 0,           delta_r/r -> infinity.              (T1)

For sufficiently small r the delta_r ball is embedded. For each additional
window critical point x put eta=(b-f(x))/(k r^3) in (0,1), and retain its index j.
Use the following two tags:

    micro:  dist(x,0)<delta_r, with mark (x/r,eta,j);
    remote: dist(x,0)>=delta_r, with mark (x,eta,j).             (T2)

The micro position uses the unique local lift, expressed in the fixed original
frame. Remote positions remain actual torus points; they are not divided by r.
The state space Y is the disjoint topological union

    Y_micro=R^d x (0,1) x {0,...,d},
    Y_remote=(X minus {0}) x (0,1) x {0,...,d}.

Let Conf_+(Y) be the disjoint union over n>=1 of the finite symmetric products
Y^n/S_n, with the quotient product topology. Multiplicities are allowed in this
ambient space; the particular laws below are simple almost surely. Cardinality
is a continuous, discrete-valued function. This space retains configurations,
not merely their one-point intensity.

Let Xi_r be the tagged configuration (T2). Define the finite nonempty measure

    L_r(G)=r^-3 E_r[G(Xi_r);N_r>0].                           (T3)

For a spectral jet theta, define the micro-only configuration

    C_micro(theta)=sum_(X,Z in C(theta))
        delta_(micro, X e_axis+Z e_soft(O), -P_theta(X,Z)/k,d-1).

Let L_micro be the pushforward of 1{n>=1}dM under this map. Let L_remote be the
singleton-configuration measure induced by

    k sum_(j=0..d) Lambda_j(x) dx d eta,
         x in X minus {0},   0<eta<1.                       (T4)

Lambda_j are RM's normalized contact kernels, and beta_far is the mass of T4.
There is no product factorization of the Gaussian endpoint and remote Hessians
inside Lambda_j.

**Theorem T (two-scale marked law).** Conditional on the exact inputs above,
for every cutoff satisfying (T1),

    L_r -> L=L_micro+L_remote weakly as finite measures       (T5)

on Conf_+(Y). The convergence also holds when testing G times any fixed
nonnegative integer power of the total count, for bounded continuous G.
The mass of L is a1+a2+beta_far=nu1+nu2. In particular, the probability law
of Xi_r conditioned on N_r>0 converges weakly to L/(nu1+nu2).

This is weak convergence of spatially marked configurations. It is not stated
as spatial total-variation convergence; Section 6 shows that such a statement
would be false in general. Count and tag-count marginals, which have a discrete
state space, do converge in total variation.

### Proof: fixed-radius limits, then the regional sandwich

Fix R>=4 and a sufficiently small rho>0. For small r, Rr<delta_r<rho.
Write N=N_R+N_mid+N_far using a disjoint near ball Rr, middle annulus and remote
complement of rho. Boundary spheres have zero expected count for each fixed r
by the spatial Kac-Rice formula, so choices of open/closed boundaries do not
matter. Form the bad event

    E_bad={N_mid>0} union {N_R>0,N_far>0}
                    union {N_far>=2} union {N_R>=3}.

SC's exact bounds imply

    limsup_(r->0) r^-3 P_r(E_bad) <= C(R^-2+rho^2).         (T6)

Only the middle term survives this limsup. The mixed bound here is the full
o(r^3) result, not a uniform extension of the compact-jet O(r^(9/2)) estimate.

For fixed R, SC's pointwise hard-direction slaving gives convergence of the
individual micro roots, their normalized heights and their indices for almost
every spectral jet and field coupling realization. Height and observation-circle
exceptional sets are null. Its integrable near-occurrence majorant (16), with the
exceptional branch handled by (14), therefore proves convergence of the entire
bounded continuous CONFIGURATION functional G, not only sums of one-point
functions, to the pushforward of 1{n_R>=1}dM. Here n_R counts cubic roots in the
R ball. All angular variables remain under the integral. No independent root
labelling is needed: local labellings from root stability induce convergence in
the symmetric-product topology.

For the remote component, change height variable t to eta=(b-t)/(kr^3) in
RM (12). Its complete integrand differs uniformly from Lambda_j(x) by O_rho(r).
The rescaled first-moment measure on D_rho x (0,1) x indices thus converges in
full variation to k Lambda_j(x) dx d eta. On N_far>=2, the mean number of remote
points is at most E_r(N_far)_2=O_rho(r^5). Subtracting this multiple-point
intensity shows that the SINGLETON-configuration measure has the same limit.
This proves T4 first on D_rho. In particular the limiting eta is uniform on
(0,1), independent of the remote location and index under the normalized remote
component; this is a marked consequence of the uniform height disintegration,
not a field-independence assertion.

On the complement of E_bad the global configuration is precisely either the
near configuration or a remote singleton, but never both. Testing a bounded G
and comparing these three finite measures gives an error bounded by a fixed
multiple of ||G||_infinity P_r(E_bad). Hence T6 bounds the scaled error.

For almost every fixed theta, every cubic root is finite and n_R=n eventually
as R->infinity. The measure 1{n>=1}M is finite by SC (19), so dominated convergence
of bounded configuration functionals gives the full micro pushforward. Meanwhile
SC (21) bounds the missing remote mass by C rho^2. Let r->0 first at fixed R,rho,
then R->infinity and rho->0. These steps prove T5 for every bounded continuous G,
including G=1. They apply to any delta_r obeying T1 because only the inequalities
Rr<delta_r<rho were used.

For a count power q, first truncate to N<=M. The truncation is a continuous
function on the disjoint-cardinality space. C6 and the first moment give

    r^-3 E_r[N^q;N>M] <= C_q/M,                            (T7)

using the (q+1)-st ordinary moment, including q=0. The limiting count is at most
two. Let M increase after the finite truncation limit. This proves the weighted
claim. Total mass tends to the positive value nu1+nu2, so normalization is valid.
Discrete tag-count convergence follows from the coordinate probabilities and
the vanishing scaled mass outside the three possible limit sectors. QED.

## 3. What singleton and double-cluster sampling mean

Conditional on N_r=1, Theorem T gives a mixture of a micro singleton, with weight

    a1/(a1+beta_far),

and a remote singleton, with weight beta_far/(a1+beta_far). The first is the
pushforward of 1{n=1}dM/a1; the second has density T4/beta_far. Conditional on
N_r=2, it gives the micro pair pushforward of 1{n=2}dM/a2, and both points have
index d-1. Positivity of a1,a2,beta_far was established by SC and remains an input.

A law obtained by sampling a nonempty configuration is not the same as a law
obtained by selecting one point from the intensity measure. The latter weights
clusters by their sizes. RADIAL_TAIL.md uses explicitly the second convention.
Likewise a first-moment formula of the form E sum phi(point) does not, by itself,
identify the full configuration law; T5 uses bounded continuous functionals of
ALL points in each configuration.

Plainly scaling ALL global positions by 1/r and seeking a finite Euclidean
configuration limit would lose a positive component. For fixed rho>0, the
remote singleton event has scaled probability tending to k integral_Drho Lambda,
while its rescaled distance is at least rho/r. Dividing by P_r(N>0)~(nu1+nu2)r^3
shows that a fixed positive fraction of the conditional mass escapes every
compact spatial set. The appropriate remedy is the two-scale space T2, not
silently deleting the remote contribution.

## 4. All leading ordered pair mass is microscopic

Let N_in count the points in the delta_r ball, with any cutoff T1. For q>=2,
(N)_q-(N_in)_q counts ordered distinct q-tuples not wholly inside that ball.

**Theorem L (factorial localization).** For every fixed integer q>=2,

    r^-3 E_r[(N_r)_q-(N_in)_q] -> 0.                     (L1)

In particular all order-r^3 second-factorial mass is microscopic and its limiting
coefficient is 2a2. The assertion does not hold for q=1, whose omitted coefficient
is beta_far>0.

**Proof.** On the good event used in T6, either all points belong to the near ball
and hence to the delta_r ball, or the only point is a remote singleton. For q>=2
the difference in L1 is zero in both cases. Everywhere it is between zero and
N_r^q 1_Ebad. By Cauchy-Schwarz and C6,

    r^-3 E_r[N_r^q 1_Ebad]
       <= (r^-3 E_r N_r^(2q))^(1/2)
                                 (r^-3 P_r(E_bad))^(1/2).

Take the small-r limsup, then R->infinity and rho->0 using T6. This proves L1.
The coefficient 2a2 follows from SC's count law and polynomial moment convergence.
The identical argument for fixed R,rho and their mixed event gives

    E_r[N_R N_far^rho]=o_(R,rho)(r^3),                    (L2)

using N_R N_far<=N^2 and E N^4=O(r^3). Thus the probability localization also
controls the COUNTED mixed pair mass; an event bound alone without uniform
integrability would not have supplied that conclusion. QED.

For a bounded continuous function of an ordered pair of micro position/height/
index marks, the scaled ordered-pair measure converges weakly to

    integral_(n=2) [delta_(z1(theta),z2(theta))
                     +delta_(z2(theta),z1(theta))] dM(theta).  (L3)

This is T5 with a count-quadratic functional and T7, followed by L1 to remove
nonmicroscopic pairs. No arbitrary root ordering enters L3. It gives a precise
conditional answer to localization of the leading pair mass, without changing
any existing scientific register or accepting a different proof of that problem.

## 5. The order of limits remains a real restriction

T5 concerns a two-scale weak limit as r->0. The sharp radius tail in the companion
paper concerns the tail of the already formed MICROSCOPIC limiting measure.
Neither result asserts a convergence rate or an interchange with a radius that
grows arbitrarily quickly at finite r. Count-polynomial uniform integrability
T7 is not spatial-moment uniform integrability. In particular an eleventh radial
moment conclusion for the limiting local law must not be advertised as an
asymptotic for the finite-r global eleventh moment, which also has remote points.

## 6. A rigorous obstruction to spatial total-variation convergence in d>=3

In the micro double-cluster limit, both transverse displacement vectors are
multiples of the same soft eigenvector. Let E_col be the event that a two-point
configuration has both tags micro and linearly dependent transverse vectors.
The limiting probability conditional on N=2 is one.

For any fixed r>0, the factorial spatial measure of two distinct additional
critical points under P_r is absolutely continuous away from the pins and the
coincidence diagonal. To see this, exhaust that domain by compact separated
sets; [P]'s distinct-site jet rank gives a nonsingular two-gradient covariance.
The Gaussian two-point Kac-Rice formula with the single endpoint weight W_r and
single Z_r gives a Lebesgue density there. Polynomial Gaussian moments make it
finite on each compact piece. A spatially null set therefore has zero factorial
measure. The conditional law on N=2 is dominated, as a null-set statement, by
this nonnegative factorial measure. No unproved uniform near-diagonal density
bound is needed for this absolute-continuity assertion.

When d>=3, the transverse dimension m>=2. Linear dependence of two transverse
vectors is a Lebesgue-null algebraic condition: for example the zero set of the
sum of squares of their 2-by-2 minors, a nonzero polynomial. Hence P_r(E_col|N=2)=0
whenever that conditioning is defined. SC implies it is defined for all small r
because P_r(N=2)~a2 r^3 and a2>0. The probability total-variation distance is thus

    dTV(Law(Xi_r|N_r=2), L_micro restricted to n=2 / a2)=1. (V1)

Weak convergence is fully compatible with V1. Latent-jet/count total variation
from SC must not be pushed through an r-dependent spatial map as if the map were
fixed. No V1 claim is made in d=2.

## 7. Review scope

New obligations: the marked configuration-space sandwich (not merely intensity),
remote height disintegration, arbitrary-cutoff localization with counted tails,
and the finite-r versus limiting-support argument V1. The cubic, SC domination
and imported Gaussian estimates keep their own review obligations. Exact finite
controls verify exponent ledgers and count inequalities; they do not certify
these measure-theoretic or Gaussian steps. The radius/height calculation is
separate in RADIAL_TAIL.md and has its own nonauthor review request.
