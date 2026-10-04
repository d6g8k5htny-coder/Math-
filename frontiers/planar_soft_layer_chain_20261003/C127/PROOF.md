# A quantitative mixed inner/remote window-witness estimate

Object: OA-C127-MIXED-INNER-REMOTE-20261004-v1.
Authors: OpenAI / Codex, root session
01a0bbb5-2fcb-77f0-b78b-4d220ddd7ab2 and /root/next_math_triage.
Disposition: author-side proof candidate until separately identified review.
Shared account attribution is not organizational independence.
Scientific-status effect: NONE. All retained hypotheses remain retained.

## 1. Statement and exact scope

Fix L>0, a compact birth interval B, and the centered variance-one Gaussian
field on X=R^2/(L Z^2) with covariance

    K_L(z)=sum_(n in Z^2) exp(-|z+Ln|^2/2)
           /sum_(n in Z^2) exp(-|Ln|^2/2).

For any orthonormal frame (u,v), fix physical k=1 and actual observations

    M=-ru/2, S=ru/2,
    f(M)=b, f(S)=b-r^3, grad f(M)=grad f(S)=0, b in B.     (1)

Q_r is their canonical Gaussian regression law. Let F_j(H)=|det H| on
nonsingular Hessians with j negative eigenvalues, and zero otherwise. Set

    W_r=F_2(H_M)F_1(H_S), Z_r=E_(Q_r)W_r,
    dQ_r^W=(W_r/Z_r)dQ_r.                                (2)

This is the FULL normalizer, never restricted to a norm or spatial cutoff.
N counts all additional critical points of every Morse index with height
in I_r=(b-r^3,b), excluding M,S. For fixed R>=4, N_R counts those in
dist_X(x,0)<Rr; N_far^rho counts those in D_rho={dist_X(x,0)>=rho}.
Take r small enough for the local cylinder to be embedded and Rr<rho/2.
These regions are disjoint. Volume is physical torus area.

**Theorem C127, conditional on the retained interfaces in §2.**
For each fixed R>=4 and integer p>=0 there are finite C_(R,p),r_(R,p)>0,
uniform in b in B and all frames, such that for 0<r<=r_(R,p) and
rho=r^(1/100),

    E_(Q_r^W)[N^p N_R N_far^rho] <= C_(R,p)r^(427/100).    (3)

In particular it is O_(R,p)(r^4). In the original pinned law,

    E_(Q_r)[W_r N^p N_R N_far^rho]
                     <= C_(R,p)r^(627/100)=O_(R,p)(r^6).  (4)

Use N^0=1 including N=0. These exponents are nonoptimal. Constants depend
on L,B,R,p and retained interfaces, not r,b or frame. No R-growth, varying
volume or small-k uniformity is asserted. This regional critical-point
count is not elder selection, branch adjacency, barcode identification or
a lifetime-density theorem. The entire shrinking-witness node stays open.

## 2. Retained interfaces and dependency boundary

SOURCES.json binds source bytes at Math main
bbe85e270f2c8b747f2d5d9477c86e86e323fe15. Consume only:

* P, imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md
  §§2–5: positive Fourier spectrum; stable actual contact frame; uniform
  moments of every fixed order of a C^4 norm under Q_r; and
  0<z_*r^2<=Z_r<=z^*r^2. Read with E1 congruence repair and REC
  reconciliation, retaining CAP as part of that reconciled identity set. Keep actual weight, conditioning and restrictions.
* DL, frontiers/d5_dimension_lift_20260929/PROOF.md, Theorem G_d at d=2:
  E_(Q_r^W)N<=Cr^3, retaining its planar regional hypotheses.
* C6, frontiers/c6_palm_route_20260929/PROOF.md, Theorem Q at d=2:
  E_(Q_r^W)(N)_q<=C_qr^3 for every fixed integer q>=2.
  DL and the exact Stirling identity
  N^q=sum_(j=1)^q S(q,j)(N)_j imply

        E_(Q_r^W)N^q<=C_qr^3, q>=1.                     (5)

  C6 Lemma5.1 supplies whole-field Borel marked one-point Kac–Rice with
  canonical Gaussian regression at every target. Read with E2,
  reviews/d1_section9_borel_repair_20260925/REPAIR.md, in C^4 field space,
  and its pinned genericity interface. No arbitrary a.e. conditional
  expectation is evaluated at gradient zero.
* C107, frontiers/moving_remote_collision_20261003/PROOF.md §§2–4:
  actual U_r identities, sine charts, periodic separators, stable two-node
  Hermite interpolation and covariance duality. The NEW ten-functional
  interpolation is proved in FINITE_R_INTERPOLATION.md, not inferred
  from C107's two-outer-witness theorem.
* SC, frontiers/spectral_cluster_closure_20260929/PROOF.md §3:
  deterministic exclusion, reproduced in planar form below. Neither its
  cluster-law conclusion nor a quantitative reinterpretation of its
  fixed-cutoff §7 is a premise.

A defect in a retained interface blocks that arrow. No acceptance flag is
changed. The new arrows are finite-r conditional density (§4), correlated
weighted event bound (§5), and moving-cutoff composition (§6).
Global moments (5) alone do not imply the regional conclusion (3).

## 3. Deterministic near-event slab and determinant gains

Choose fixed C_L so K=C_L(1+||f||_(C^4(X)))>=1 bounds all physical operator
derivatives through four in every frame. Use y=tu+zv and A=f_vv(0).

The two gradient pins give integral H(tu)u dt=0 over -r/2<=t<=r/2.
Hessian Lipschitz continuity therefore gives

    H(M)u=(1/r)integral[H(M)-H(tu)]u dt,
    |H(M)u|<=rK/2, |H(S)u|<=rK/2.                       (6)

Other columns are at most K. Hadamard gives, without a near-event condition,

    W_r<=Cr^2K^4.                                       (7)

On W_r>0, H(M) is negative definite, hence A<rK/2.

**Planar exclusion.** If R>=1 and

    rK<=1/(4R), lambda=-A>(8RK+56RK^2)r,                 (8)

the cylinder |t|<=Rr, |z|<=Rr has only the pinned critical points.

Proof. Throughout it f_zz<=-lambda/2, by a variation bound 2RKr.
For g(t)=f_z(t,0), two pinned zeros and |g''|<=K give
|g(t)|<=KR^2r^2 by the two-node remainder, also outside the pin interval.
The zero integral of g' gives |g'(t)|<=K(R+1/2)r.
At a=4R^2Kr^2/lambda<Rr/2, f_z(t,-a)>0 and f_z(t,a)<0.
Strict transverse concavity gives a unique zero zeta(t) in the entire
cylinder, C^3 by the implicit-function theorem. On its graph,
|f_tz|<=2RKr and |zeta'|<=4RKr/lambda<1/2. Put psi(t)=f(t,zeta(t)).
Differentiating f_z=0 cancels zeta'' terms and yields

    psi'''=f_ttt+3f_ttz zeta'+3f_tzz(zeta')^2+f_zzz(zeta')^3.

Thus |psi'''-f_ttt|<=28RK^2r/lambda<1/2.
The two heights and two axial-gradient pins imply f_ttt(eta,0)=12
at some eta between pins by cubic Hermite interpolation/generalized Rolle.
The fourth derivative bound gives |f_ttt(t,zeta)-12|<=2RKr<=1/2.
Consequently psi'''>=11. Strict convexity of psi' and its two pinned zeros
exclude a third. Every cylinder critical point is on this graph. QED.

Fix T>=1 with rT<=1/(4R). On W_r>0,N_R>0,K<=T, (8) and A<rK/2 imply

    -64RrT^2<=A<rT/2, so |A|<=C_RrT^2.                 (9)

At either pin the axial column is <=CrT, including the off-diagonal
entry. The remaining transverse entry differs from A by <=rK/2, so the
whole transverse column is <=C_RrT^2. Hadamard in the orthonormal frame gives

    W_r 1{N_R>0,K<=T}
      <=C_Rr^4T^6 1{|A|<=C_RrT^2,K<=T}.                (10)

The remote Hessian determinant is <=CT^2 on K<=T. No determinant has
been replaced by an independent or unweighted mean.

## 4. Actual finite-r conditional density

For rho_0<=min(1,L/32), 0<rho<=rho_0, r<=rho/8 and x in D_rho,
the companion appendix constructs exact real periodic Fourier duals for

    (U_rf,A(f),f(x),grad f(x)) in R^10,                  (11)

in fixed frequencies |n|_1<=5, at Cameron–Martin cost C_Lrho^-9 per unit
target. U_r is an invertible transform of the six ACTUAL observations (1);
its target is (b-r^3/2,-r^2,0,12,0,0).
A quadratic separator correction kills both pin first jets and the remote
first jet, while its A-response is >=c_Lrho^2 at finite r.
No limiting-rank argument or nonperiodic RKHS polynomial is used.
The appendix proves

    c_Lrho^18 I_10<=Cov(U_r,A,f(x),grad f(x))<=C_L I_10.   (12)

Under Q_r the covariance Sigma of V_x=(A,f(x),grad f(x)) is the Schur
complement. For w in R^4,

    w^T Sigma w=min_(a in R^6)Var(a.U_r+w.V_x)
                       >=c_Lrho^18 |w|^2,

and Sigma<=C_L I_4. Its canonical Gaussian density satisfies at every target

    p_(A,f(x),grad f(x)|pins)(a,h,g)<=C_Lrho^-36.         (13)

The power is (18)(4)/2, from the conditional FOUR-dimensional determinant.
The maximum Gaussian density bound is independent of the mean.
All bounds are uniform over x in D_rho and frames. The torus covariance
has not been assumed rotationally invariant.

## 5. Marked event bound with one full normalizer

Let E={N_R>0,N_far^rho>0}. Since N_far^rho>=1 on E,

    Q_r^W(E;K<=T)
      <=Z_r^-1 E_(Q_r)[W_r 1{N_R>0,K<=T}N_far^rho].      (14)

For fixed r,rho the remote domain is compact and separated from both pins.
Apply C6 Lemma5.1 summed over all indices to the field mark
Xi=W_r1{N_R>0,K<=T}. In separable C^4(X), K is continuous, and the count
and mark are Borel by retained pinned genericity/exhaustion.
E2's finite-measure extension supplies the whole-field Borel formula.
The two endpoints are excluded and lie outside the open height window.

The marked canonical conditioned fields still satisfy the pin equalities,
so the deterministic inequality (10) holds under their kernels.
Use (10) and the remote determinant bound CT^2, retaining K<=T until that
bound is applied. Disintegrate A using the canonical joint Gaussian kernel
of §4. Successive Gaussian regression agrees with direct regression at
EVERY target by the Schur identities for means/covariances. These give
identical Gaussian measures on C^4 and hence identical Borel-mark
integrals. No a.e. conditional version is evaluated at g=0.

With h in I_r this yields the explicit finite estimate

    Q_r^W(E;K<=T)
      <=(C_Rr^4T^6/Z_r)
        integral_(D_rho) integral_(I_r)
        integral_(|a|<=C_RrT^2)
             T^2 p_(A,f(x),grad f(x)|pins)(a,h,0) da dh dx
      <=C_Rr^6T^10rho^-36.                              (15)

The factors are r^4T^6 for endpoints, T^2 for remote determinant,
rT^2 for the A slab, r^3 for height, area <=L^2, density rho^-36,
and exactly one division by Z_r>=z_*r^2.
We neither pin a near witness nor multiply witness probabilities.
Uniform moments under extra remote conditioning are not needed.

For every fixed m>0, the untruncated tail is estimated in ORIGINAL Q_r:
by (7), the full normalizer floor and P's uniform moments,

    Q_r^W(K>T)<=C E_(Q_r)[K^4;K>T]
               <=C T^-m E_(Q_r)K^(m+4)<=C_mT^-m.         (16)

Thus, whenever rT<=1/(4R),

    Q_r^W(E)<=C_Rr^6T^10rho^-36+C_mT^-m.                (17)

All integrals in (15) are finite by the displayed compact-window/area
bounds; (16) handles the tails. Estimate (17) holds pointwise for every
admissible r,rho,T. No interchange of limits over a moving domain occurs.

## 6. Counted moment and explicit cutoffs

Pathwise N^pN_RN_far^rho<=N^(p+2)1_E. Cauchy–Schwarz under the single
law Q_r^W, then (5) at q=2p+4 and (17), gives

    E_(Q_r^W)[N^pN_RN_far^rho]
      <=C_(R,p,m)[r^(9/2)T^5rho^-18+r^(3/2)T^(-m/2)].   (18)

Set rho=r^(1/100), T=r^(-1/100), m=600.
Take r sufficiently small that rho<=rho_0, r<=rho/8, Rr<rho/2,
rT<=1/(4R), Rr<L/32 and r<=1, together with retained small-r thresholds.
For example impose r<=rho_0^100, r^(99/100)<=1/8,
r^(99/100)<1/(2R), r^(99/100)<=1/(4R), and r<L/(32R).
A smaller positive threshold enforces strict inequalities.

| Quantity | Exact power of r |
|---|---:|
| Truncated event r^6T^10rho^-36 | 277/50 |
| Tail event T^-600 | 6 |
| Counted term r^(9/2)T^5rho^-18 | 427/100 |
| Counted tail r^(3/2)T^-300 | 9/2 |
| Original weighted numerator | 627/100 |

For r<=1 the tail term is bounded by the first. This proves (3).
Multiplying by the same FULL Z_r<=z^*r^2 proves (4).
The mixed count is o(r^3), quantitatively r^(127/100) smaller than the
r^3 rare-count scale. Its raw weighted numerator is o(r^2), but this is
only this event, not every configuration required for persistence.

## 7. Closure boundary and falsifier

SC §7 gives fixed-R,fixed-rho qualitative mixed suppression via a fixed
compact-jet box and exhaustion; C107 treats two remote witnesses.
The new interface is (3): fixed R, moving rho and any fixed multiplier N^p,
retaining the full correlated weight.

Both-inner collisions, growing normalized annuli, shrinking gap marks,
all-pairs-to-bar identification, reverse persistence-to-witness coverage,
coarea/density conversion and global completion remain outside this result.
No human or organizational independence is claimed.

A logical falsifier explains why (5) is insufficient: let N=2 with
probability r^3 and zero otherwise, and N_R=N_far=1 on the rare event.
Every fixed factorial moment is O(r^3), but E[N_RN_far]=r^3 is not O(r^4).
Its two events are fully correlated, not independent.

Exact rational controls accompany the proof only for finite identities,
exponents and explicit falsifiers. They do not establish the analytic
interpolation, Gaussian conditioning, Borel Kac–Rice or retained sources.
Those remain the written proof and nonauthor review obligations.
