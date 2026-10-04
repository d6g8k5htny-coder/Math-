# Quantitative separated jets and a shrinking far-elder region

Object: OA-QSF-20261002-C89-v1. Author: OpenAI / Codex, root01a0bbb5.
Dylan Roy — delegated AI work. Personal reading PENDING; organizational
independence 0; scientific effect NONE. This is an additive analytic candidate,
not a change to a scientific status register. Review disposition belongs in
REVIEW.md, separately from this author statement.

## 0. Exact interface and result

Fix d >= 2 and L > 0. Use the centered, variance-one periodized Gaussian field
on X = R^d/(L Z^d) of [P] §1, with Fourier weights

    a_n = exp(-2 pi^2 |n|^2/L^2) / sum_k exp(-2 pi^2 |k|^2/L^2) > 0.

[P] is `source/P.md`, SHA256
9350ad6eaba6626b93c3dedeef9e2ff816e5cdf1c8318e85fb27499141c84bc7,
40261 bytes. [G] is `source/G.md`, Math- PR188 head
5e0b31c8304e3a6ef96a5ee28c8faab5f9fdf799, blob
0b089b894960b0ee53fc2885e054d73ab73472bd, SHA256
967148439e32e8e5d6c06a12df5cc7c1eb2475fe6828e4aeb3748c48817a4cba,
29110 bytes. Its complete source interface is preserved in
`source/G_SOURCES.json`. We consume [P] §§1–2 and [G]'s canonical marked
Kac–Rice definition (0.1), deterministic Lemmas 1–3, and conditional genericity
§2(d). We do not consume Remark 6 or the OA-FD/OA-MT consequences, the SIDE24
coefficient, a finite-radius RN certificate, or a near-pair asymptotic.
The marked-measure construction retains [G]'s E2 repair and REC interpretation;
this note is not a new proof of those imported interfaces.

Write O_y=(f(0),grad f(0),f(y),grad f(y)), v=(b,0,b-ell,0), Q for Gaussian
regression on O_y=v, H_0,H_y for the two Hessians, and

    W = |det H_0 det H_y| 1{H_0 negative definite, index H_y=d-1}.

Let e_y be the ordinary global superlevel H_0 elder mark, not a branch-adjacency
mark. With p_y the density of O_y, define the canonical per-unit-spatial-volume
far-elder lifetime density

    F(ell,rho) = integral_{dist(0,y)>=rho} integral_R
                 p_y(v) E_Q[W e_y] db dy.                         (0.1)

Let J=(d+1)(d+2)/2, the number of independent derivatives of orders 0,1,2 at
one site; a symmetric Hessian has d(d+1)/2 coordinates, not d^2. Put

    rho_* = min(1,L/4),
    A_N = 24J + 12dN + 12N(N+1)(d+1).

**Theorem QSF.** For every integer q>=1 set N=2(q+1). There is a finite constant
C_q=C(d,L,q), independent of ell,rho, such that

    F(ell,rho) <= C_q rho^(-A_N) ell^(q+1),                       (0.2)

whenever 0<rho<=rho_* and 0<ell<=rho^2/(64N^2). In particular:

(a) For any fixed 0<beta<=1/A_N, F(ell,ell^beta)=O(ell^q) as ell decreases
to zero. Constants and the sufficiently small cutoff may depend on d,L,q,beta.

(b) For any fixed a>0, c>0, rho(ell)=c[log(e/ell)]^(-a), and every fixed
integer q>=1, F(ell,rho(ell))=O(ell^q) as ell decreases to zero.

These are bounds on an actual elder-marked far population with a specified
moving spatial cutoff. They are not uniform in arbitrary shrinking cutoffs,
in L, d or q. They do not establish the contact-scale region, witness uniqueness,
the intermediate region inside rho(ell), or either direction of the full
canonical-witness/persistence correspondence. There is no weighted-Palm
normalizer Z_r in (0.1); dividing by one would change the statement.

## 1. Constructive quantitative finite-jet rank

**Lemma QJ.** Fix s>=1 distinct sites x_1,...,x_s with pairwise torus distance
at least delta, where 0<delta<=1. Let T be the vector of all independent
coordinate derivatives through order two at these sites. Then

    lambda_min Cov(T) >= c(d,L,s) delta^[24(s-1)].                (1.1)

The constant is strictly positive and finite. It can be constructed from
finitely many positive Fourier weights; no sampled-covariance inference occurs.

Proof. Put omega=2pi/L and

    B_j(x)=sum_{k=1}^d [1-cos(omega(x_k-x_{j,k}))].

Choose coordinate differences in [-L/2,L/2]. The elementary inequality
sin t >= 2t/pi for 0<=t<=pi/2 gives

    B_j(x_i) >= 8 dist(x_i,x_j)^2/L^2 >= 8delta^2/L^2.

The sum of absolute Fourier coefficients of B_j is at most 2d. For each i set

    Q_i(x)=product_{j!=i} [B_j(x)/B_j(x_i)]^2.

It has value 1 at x_i, vanishes to order at least four at every other site,
has Fourier support |n|_infinity<=2(s-1), and has Fourier coefficient l1 norm
at most C delta^[-4(s-1)]. All its derivatives through order two at x_i have
the same bound, with a different C depending only on d,L,s. Here and below
C denotes a defined finite bound from the finite coefficient sum and its
frequency multipliers, never a constant allowed to depend on delta or the sites.

For a multiindex alpha with |alpha|<=2 let R_{i,alpha}(h) be the Taylor polynomial
through total degree two of

    h^alpha / (alpha! Q_i(x_i+h)).

The reciprocal is legitimate since Q_i(x_i)=1. If Q_i(x_i+h)=1+U_1(h)+U_2(h)
+O(|h|^3), its reciprocal through degree two is 1-U_1+U_1^2-U_2. Thus every
coefficient of R_{i,alpha} is bounded by C delta^[-8(s-1)]. Define the periodic
local coordinates z_k(x)=sin(omega(x_k-x_{i,k}))/omega and the trigonometric
polynomial

    P_{i,alpha}(x)=Q_i(x) R_{i,alpha}(z(x)).

Since z(x_i+h)=h+O(|h|^3), its jets satisfy

    partial^gamma P_{i,alpha}(x_j) = 1{i=j,alpha=gamma}, |gamma|<=2. (1.2)

At other sites the fourth-order zero of Q_i kills every derivative in question.
The Fourier support is |n|_infinity<=2s, and its coefficient l1 norm is bounded
by C_* delta^[-12(s-1)], uniformly over i,alpha and all separated configurations.
One may choose C_* as the maximum of the above finite-sum bounds for Q_i,
its first two derivatives, the displayed reciprocal polynomial, and the finitely
many monomials in sin/omega. This supplies an explicit finite construction of C_*.

Let a_* = min_{|n|_infinity<=2s} a_n >0. For real coefficients t_{i,alpha} set
L_t=sum t_{i,alpha} partial^alpha|_{x_i}. Fourier expansion gives

    V_t=Var(L_t f)=sum_n a_n |L_t exp(i omega n.x)|^2.

Writing P_{i,alpha}=sum p_n exp(i omega n.x), weighted Cauchy–Schwarz and (1.2)
give

    |t_{i,alpha}|^2 <= V_t sum |p_n|^2/a_n
                     <= V_t a_*^(-1) C_*^2 delta^[-24(s-1)].

Summing over sJ coordinates proves (1.1), with c=a_*/(sJ C_*^2). For s=1
the empty product Q_i=1 supplies the same argument with exponent zero.
Every subvector has at least this covariance lower bound. If a subvector is
split into V,Z, its conditional covariance also has this lower bound: for z,
the Schur-complement variational formula minimizes Var(z.Z-a.V) over a, and
(1.1) bounds every such variance below by c delta^[24(s-1)] |z|^2. QED.

This is deliberately conservative; it is a usable uniform power, not a sharp
collision exponent. The positivity of only the indicated finite cube suffices
for this rank estimate. The smooth field and moment arguments below additionally
use the summability of all Fourier modes of the stated Gaussian covariance.

## 2. Two-pin weighted moments, with the separation tracked

Let V_y=(O_y,H_0,H_y), with distinct symmetric Hessian coordinates. Its dimension
is 2J. Uniformly for dist(0,y)>=rho and 0<rho<=rho_*, Lemma QJ with s=2 implies

    lambda_min Sigma_y >= c rho^24,
    lambda_max Sigma_y <= C.                                      (2.1)

The upper bound follows from the fixed finite derivative variances. Thus at
the slice v=(b,0,b-ell,0,H_0,H_y), 0<ell<=1, the full Gaussian density satisfies

    p_{V_y}(v) <= C rho^(-24J)
                    exp[-c(b^2+|H_0|^2+|H_y|^2)].                 (2.2)

The determinant prefactor uses dimension 2J; the exponent uses the uniform
upper eigenvalue bound, not the deteriorating lower bound. The slice retains
the b coordinate and all independent Hessian coordinates, so its Euclidean norm
dominates b^2+|H_0|^2+|H_y|^2 up to fixed coordinate-norm constants.

Put K=1+sup_X ||D^2 f||_op. For every finite p>=1, Gaussian regression gives

    E[K^p | V_y=v] <= C_p rho^(-12p) (1+|v|)^p.                  (2.3)

Here is a direct uniform justification. Expand the real field into independent
standard-normal sine/cosine coefficients, with summable square-root spectral
amplitudes times (1+|n|)^2. For each standardized coefficient xi, its conditional
mean has absolute value at most sqrt(v^T Sigma_y^(-1)v), by covariance
Cauchy–Schwarz; its conditional centered variance is at most 1. Minkowski's
inequality, the spectral sum, and (2.1) bound the conditional L^p norm of K by
C_p(1+rho^(-12)|v|). The residual coefficients need not be independent of one
another. Infinite sums converge in conditional L^p(C^2) by the same summable
majorant. Gaussian regression, not conditioning on a positive-probability pin
event, defines these laws at every target v.

Consequently, for p>=1 (and with the evident p=0 version),

    M_p(ell,rho) := integral_{dist(0,y)>=rho} integral_R
                    p_y(v) E_Q[W K^p] db dy
                 <= C_p rho^[-(24J+12p)].                         (2.4)

Indeed, disintegrate further onto the Hessians: p_y(v) times the conditional
Hessian density is exactly p_{V_y}(v,H_0,H_y). W is V_y-measurable and at most
|det H_0 det H_y|, a polynomially bounded function of degree 2d. Apply (2.2)
and (2.3), integrate the polynomial times the Gaussian in b,H_0,H_y, and bound
the y volume by L^d. This preserves the full determinant weight and integrates
over all birth heights. No unweighted-to-weighted probability substitution or
inverse random Hessian moment is used.

## 3. N-site bound, retaining the weighted event

Use exactly [G] §3's shells

    S_j={x: |dist(0,x)-j rho/(2N)|<rho/(8N)}, j=1,...,N.

Every tuple (0,y,q_1,...,q_N), q_j in S_j, dist(0,y)>=rho, is separated by at
least delta=rho/(4N). Apply Lemma QJ with s=N+2 to the full two-jets, then take
the subvector (V_y,Z), where Z=(f(q_j),grad f(q_j))_{j=1}^N has m=N(d+1)
coordinates. Its conditional density given V_y, uniformly over all values, is
bounded by

    C_N rho^[-12N(N+1)(d+1)].                                    (3.1)

Therefore the conditional probability of |f(q_j)-b|<=3ell and
|grad f(q_j)|<=3sqrt(K_0 ell) at all N sites is at most

    C_N rho^[-12N(N+1)(d+1)] K_0^(dN/2) ell^[N(1+d/2)].          (3.2)

For 0<ell<=rho^2/(64N^2) and K_0>=2, [G] Lemmas 1–3 force on the elder event
with K<=K_0 a near-critical ball of volume omega_d(ell/K_0)^(d/2) in every
shell. The pathwise product-volume bound [G](3.1), Tonelli, and (3.2) yield

    integral integral p_y E_Q[W e_y 1{K<=K_0}]
      <= C_N rho^[-12N(N+1)(d+1)] K_0^(dN) ell^N M_0
      <= C_N rho^[-24J-12N(N+1)(d+1)] K_0^(dN) ell^N.            (3.3)

The shell product volume is at most L^(dN); this bound is independent of rho.
The tower step is valid because W is V_y-measurable, while (3.2) is uniform
in the conditioning values. No measurable choice of a point on each sphere
is needed: the forced lower volume is pathwise, and only measurable shell
integrals enter Tonelli. The conditional generic locus and the actual elder
topology are those explicitly imported from [G]; no claim that a local saddle
must be the elder saddle is introduced.

For the complement, Markov's inequality and (2.4) give

    integral integral p_y E_Q[W e_y 1{K>K_0}]
      <= K_0^(-p) M_p
      <= C_p K_0^(-p) rho^[-24J-12p].                            (3.4)

This is Markov applied inside the determinant-weighted integral, not an
unweighted tail probability subsequently divided by a normalizer.

## 4. Threshold, moving cutoff, and error order

Take K_0=2 rho^(-12) ell^[-1/(2d)]. It is at least 2. Equations (3.3)–(3.4)
become, for any integers N>=1 and p>=1,

    F(ell,rho) <= C_N rho^(-A_N) ell^(N/2)
                  + C_p rho^(-24J) ell^[p/(2d)].                (4.1)

Choose N=2(q+1), p=2d(q+1). Since rho<=1 and A_N>=24J, (0.2) follows.
This explicit loss of half the small-box exponent avoids any need for uniform
Borell constants in this extension.

For rho=ell^beta, (0.2) is C_q ell^[q+1-beta A_N], at most C_q ell^q when
beta A_N<=1. Since A_N>2, beta<1/2, so ell^(1-2beta)<=1/(64N^2) eventually;
rho<=rho_* also eventually. Thus the domain restriction is satisfied, rather
than silently discarded. More generally rho=c ell^beta with fixed c>0 works,
changing constants and the small cutoff.

For rho=c[log(e/ell)]^(-a), (0.2) is

    C_q c^(-A_N) ell^(q+1) [log(e/ell)]^(a A_N).

The elementary bound ell[log(e/ell)]^B=O(1) for each fixed B, and
ell[log(e/ell)]^(2a)->0, prove both the asserted order and the domain condition.
q is chosen before the limit; no uniformity over q is claimed.

For example d=2,q=1 gives J=6,N=4,A_N=960, and the conservative valid choice
rho=ell^(1/960) yields F=O(ell). This is much farther out than the contact
scale ell^(1/3), and is not a closure of that region.

For any one fixed moving-cutoff function in (a) or (b), the expected number per
unit volume of bars with 0<ell<=t and endpoint separation at least rho(ell)
is the integral of F(ell,rho(ell)) and is O(t^(q+1)). This counts a lifetime-
dependent selection. It does not differentiate the cutoff or identify that
count with the different observable using the common cutoff rho(t).

## 5. Limits, negative controls, and remaining obligations

All bounds hold for the fixed finite torus and stated covariance. The finite
Fourier construction is quantitative even as sites approach, but its constants
depend on the fixed number of sites. The proof makes no interchange of L with
ell, no diagonal choice of N, and no claim of sharp constants. Nonnegative
integrands justify Tonelli; (2.4) supplies the needed finite dominating weighted
moments in every displayed integral.

The accompanying exact rational Fourier controls check cardinal second jets
on finite configurations, the need for the square in Q_i, the need for the
reciprocal Taylor correction, repeated-site degeneracy, and the exponent
ledger. They do not prove the uniform analytic statements: those are proved
above. A finite spectral lower bound is used because it analytically constructs
a dual for every configuration, not because a finite sample happened to be
nonsingular.

Explicit non-promotions:
- Fixed-rho [G] alone did not imply this result; (1.1), (2.4), and (3.1) are
  the new quantitative bridges.
- A bound on the far elder subset does not control rejected candidates or
  identify the full persistence coefficient.
- The positive-power cutoff allowed for a given q is restricted by A_N. It
  cannot be set equal to the contact scale, and the same beta is not claimed
  to give every power q simultaneously.
- The logarithmic cutoff permits each fixed order separately; it leaves a
  large inner/intermediate region unresolved.
- Shrinking multiple-witness collision, actual field confinement for the
  QSA1 window, the complete two-sided persistence bridge, and imported parent
  hypotheses retain their own statuses. No dependency is erased by this note.
