# Uniform small-lifetime tails and inverse moments of the actual failure law

29 October 2026. Author-support derivation by OpenAI / Codex, delegated agent
`/root/inverse_uniform_route`, with the root OpenAI agent contributing the
proof-route check and exposition requirements. This is new author-side
mathematics, with zero qualifying nonauthor or organizational-independence
review credit. Scientific effect NONE. No predecessor proof, source verdict,
register, Boolean, prize, premise, or acceptance disposition is changed.

## 1. Sources, scope, and result

The model is the original variance-one periodized Gaussian field in [P] §1,
with fixed dimension d>=2 and fixed torus side L>0. Constants below are common
for births b in a fixed compact interval, gap marks k in a fixed compact
interval [k_-,k_+] contained in (0,infinity), and all orthonormal axial frames.
The radius is sufficiently small, including r<L/(4 sqrt(2)). No uniformity in
dimension, volume, a varying spectrum, or gaps approaching zero is asserted.

Consumed source interfaces are:

* [P] `../../imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md`,
  SHA256 `9350ad6eaba6626b93c3dedeef9e2ff816e5cdf1c8318e85fb27499141c84bc7`:
  §§1-4 for the original law, positive Fourier spectrum and desingularized
  pins; §5 (5.1)-(5.5) for endpoint identities and the full normalizer;
  §6 for its INDIVIDUAL saddle determinant bound; §§7-8 for the cap implication
  and the ordinary global elder interpretation. Its original bytes are read
  with `../../imports/lifetime_parent_20260925/ERRATUM_CONGRUENCE.md`,
  `../../reviews/d1_section9_borel_repair_20260925/REPAIR.md`, and
  `../../reviews/d1_chain_reconciliation_20260928/RECONCILIATION.md`, including
  the latter's convergence-in-law wording and embedding rule. The cap premise
  is `../../imports/lifetime_parent_20260925/MARKED_CYLINDER_CAP_PROOF.md`
  §§1-5, consumed through the exact implication restated in §4 below.
* [FIX] `../fixed_r_inverse_lifetime_20260930/PROOF.md`, SHA256
  `5adef725c1c696adae9bc73a525efe0bfe09d5c07e95ee3f067db9e877283630`:
  §§3-4 for the deterministic local barrier and weighted spectral reduction;
  §§5-6 for the fixed-positive-r lower tail and sharp inverse boundary.
  The barrier and required spectral integral are also reconstructed here.
* [LOCAL] `../local_elder_geometry_20260930/PROOF.md`, SHA256
  `f68038be79b46124b0f9b31205aa6e3682b34b6f5ef81f4a5697ae81f07cc46b`,
  §8, and [FIBRE] `../concave_fibre_elder_20260930/PROOF.md`, SHA256
  `5681896a6808f48fb7508914d0860ec508af7646e9e706fc260d935dd951c75e`,
  §§5-6, supply the already proved actual failure and marked lifetime laws,
  respectively in dimension 2 and fixed dimension at least 3. They are used
  only for the moment-convergence corollary, not to prove the tail theorem.
  Their complete source identities and retained reading rules are in their
  own `SOURCES.json` files. This consumer neither reproves their marked laws
  nor changes any existing review disposition.

Put M=-(r/2)u and S=(r/2)u. Let Q_r be continuous Gaussian regression at

    f(M)=b, f(S)=b-kr^3, grad f(M)=grad f(S)=0.

Keep exactly the original weight and FULL normalizer:

    W_r=|det H_M det H_S| 1{H_M<0,index(H_S)=d-1},
    Z_r=E_Q W_r,                 dP_r=(W_r/Z_r)dQ_r.       (1.1)

There is no added pin density, adjacency restriction, or restricted normalizer.
Let d_f(M) be the ordinary superlevel maximin death, F_r the event that S is
not the actual elder partner, ell_r=b-d_f(M), and X_r=ell_r/(kr^3). On the
essential class ell_r=X_r=+infinity. The local barrier below proves ell_r>0
whenever it is finite on typed support.

**Theorem U.** There are C<infinity and r_*>0, uniform on the stated parameter
family, such that

    P_r(F_r,0<X_r<=t) <= C r^3 t^(2/3)
                         (0<r<=r_*, 0<t<=1).             (1.2)

The event in (1.2) necessarily has finite death. It is also contained in F_r
when t<1, but keeping F_r explicitly is useful in the proof. At t=1 it is
important to retain F_r: pairing success has X_r=1 and probability near one.

**Corollary M.** At each fixed admissible birth, gap and frame, let mu_fail be
the actual failure measure from [LOCAL] or [FIBRE], let

    a_fail=mu_fail(total)>0,
    lambda(theta)=-h_*(theta)/k in (0,1).                 (1.3)

Then for every 0<p<2/3,

    r^-3 E_Pr[X_r^(-p);F_r,ell_r finite]
                  -> integral lambda^(-p) dmu_fail < infinity,  (1.4)
    E_Pr[X_r^(-p) | F_r,ell_r finite]
                  -> a_fail^-1 integral lambda^(-p) dmu_fail.   (1.5)

These moment limits are pointwise in the fixed parameters, as are the cited
actual marked laws. The tail theorem (1.2) itself has the stated compact
parameter uniformity. At each fixed positive r, the same conditional inverse
moment is infinite for p>=2/3 by [FIX]; consequently no finite-moment extension
of (1.4)-(1.5) to those orders is possible.

## 2. An enlarged nonsingular endpoint regression

Write m=d-1 and use the axial coordinate x and transverse coordinates y_j.
For a test field define g(t)=f(M+tu), 0<=t<=r, and
h_j(t)=f_{y_j}(M+tu). Use [P] §3's exact observation rows

    U_2=(g'(r)-g'(0))/r,
    U_3=(6/r^2)[g'(0)+g'(r)-2(g(r)-g(0))/r],
    V_j1=(h_j(r)-h_j(0))/r.

Append to its entire observation vector U_r the following linear rows:

    A_r=[g''(0)-U_2+(r/2)U_3]/r^2,
    v_r,j=[h'_j(0)-V_j1]/r,
    B_r=-D_y^2 f(M).                                    (2.1)

Symmetric entries of B_r are listed once. The apparent negative powers of r
in (2.1) cancel EXACTLY. Taylor's formula with integral remainder gives

    A_r=integral_0^1 theta(1-theta)^2
                            f_uuuu(M+r theta u) dtheta,
    v_r,j=-integral_0^1 (1-theta)
                            f_uuy_j(M+r theta u) dtheta. (2.2)

For the first identity, after multiplying (2.1) by r^2, the coefficient of
g''''(s) is s(r-s)^2/r^2 before the final division by r^2; all terms of degree
at most three cancel. For the second, subtract h'_j(0) from the average of
h'_j and integrate once. Thus (2.2) holds for every C4 test field, not merely
as a Gaussian asymptotic. Also

    U_2=integral_0^1 f_uu(M+r theta u)dtheta,
    U_3=integral_0^1 6 theta(1-theta)
                            f_uuu(M+r theta u)dtheta.   (2.3)

All appended and original rows are uniformly bounded functionals on C4.
Their joint contact limits include the original contact list

    (f,f_u,f_uu,f_uuu,f_y1,f_uy1,...,f_ym,f_uym)

and the additional, distinct coordinates

    A_0=f_uuuu/12,  v_0,j=-f_uuy_j/2,  B_0=-D_y^2f.     (2.4)

The factors in (2.4) are the integrals of the kernels in (2.2). The original
strictly positive Fourier weights prove nondegeneracy for this finite jet
list: a zero-variance combination would annihilate every Fourier mode and
therefore be the zero finite-order distribution. Arbitrary local jets force
each coefficient to vanish. The kernel identities, or the rapidly summable
Fourier series, show joint covariance convergence uniformly in frames.
Continuity in the compact orthogonal group gives a common strictly positive
covariance gap at contact and for sufficiently small r.

Under the prescribed pins U_2=0, U_3=12k and V_j1=0. Write A,v,B for the
resulting variables. Then the following is an EXACT identity:

    H_M=[[-6kr+r^2 A, r v^T], [r v,-B]].                (2.5)

The Gaussian vector V=(A,v,B), conditional on the original pins only, has a
uniformly bounded mean and covariance bounded above and below. In its
independent symmetric-matrix coordinates its density satisfies

    rho_r(V)<=C exp(-c |V|^2).                          (2.6)

The full-field conditional regression can be realized as

    f=mu_r+L_r(V-E_Q V)+g_r,
    g_r independent of V.                              (2.7)

The C4 norms of mu_r and all columns of L_r are uniformly bounded. Indeed
the enlarged covariance inverse is uniformly bounded, while differentiating
the field location through order four in its cross-covariance with (2.2)
uses only bounded covariance derivatives through order eight. The original
Fourier decay gives those bounds and their uniform convergence. Subtracting
this finite Gaussian regression from the original field, or the marginal
Fourier-coefficient contraction argument in [P] §4, shows

    sup E J^s<infinity for every finite s>=0,
    J=1+||g_r||_C4,   J independent of V.                (2.8)

Independence is of the complete residual field and the complete vector V;
it follows first for a countable dense collection of derivative evaluations
from Gaussian orthogonality and then for the C4-valued field by continuity.
No independence of derivative suprema and Hessians is asserted. With

    K=1+||f||_C4,  P=1+|A|+|v|+||B||_F+J,

we have, uniformly,

    K<=C P,  M3<=C K,  M4<=C K.                         (2.9)

Here M3,M4 are the derivative bounds in [P]'s cap theorem; finite dimensional
norm-equivalence constants are included in C. Enlarge K by one fixed factor
if needed so that it also dominates the global Hessian and third-derivative
operator norms used below.

## 3. A tail-retaining estimate for large regression coordinates

Let lambda=lambda_min(-H_M)>0 on typed maximum support. The elementary local
barrier in [FIX] §3 gives

    ell_r>=c_L lambda^3/K^2.                            (3.1)

For clarity, take an embedded ball of radius a_L lambda/K about M, where
a_L=min(1,L/4). Taylor's upper bound on that ball is
f(M+tv)<=b-lambda t^2/3. No point above b is inside; every older-reaching
path crosses the boundary, giving (3.1), also for ell_r=+infinity.

The exact endpoint gradient pins in [P] (5.1) imply that the first column of
H_S has norm <=CrK. Its other columns have norms <=CK. Hence Hadamard gives

    |det H_S|<=CrK^d.                                  (3.2)

For 0<epsilon<=1 put psi_epsilon(lambda)=min(1,epsilon/lambda^3). Equation
(3.1) implies

    1{0<ell_r<=epsilon}<=C K^2 psi_epsilon(lambda).       (3.3)

Fix c0>0, to be made smaller in §4. On P>c0/r, insert the pointwise bound
1<=(rP/c0)^N, where N is any chosen positive integer. Using (3.2)-(3.3),
and dropping the saddle type restriction for an upper bound, gives

    E_Q[W_r;0<ell_r<=epsilon,P>c0/r]
      <=C_N r^(N+1) E_Q[|det H_M| 1{H_M<0}
                            P^(N+d+2) psi_epsilon(lambda)].    (3.4)

Now integrate the independent residual J using (2.8), retaining the entire
V density. Its polynomial moments are bounded by a polynomial in 1+|V|.
Absorb that polynomial into half the Gaussian envelope in (2.6) BEFORE
changing coordinates. The affine transformation (2.5) has Jacobian

    dH_M=r^(m+2)dV=r^(d+1)dV.                           (3.5)

The axial coordinate contributes r^2, the m mixed entries contribute r^m,
and the transverse entries contribute one. Moreover
||H_M||_F<=C(1+|V|) for r<=1, including the bounded shift -6kr. Therefore

    (3.4)<=C_N r^(N-d) integral_{H<0} |det H|
                  psi_epsilon(lambda_min(-H)) exp(-c' ||H||_F^2)dH.
                                                                    (3.6)

The power of r in (3.5) is independent of N. There is no additional r^-N
loss: the Gaussian polynomial was absorbed while V was still the variable.

To bound the remaining integral, diagonalize -H with ordered positive
eigenvalues lambda=lambda_1<=...<=lambda_d. The matrix Lebesgue Jacobian is
a fixed constant times the Vandermonde product and compact angular measure.
The determinant contributes the exact factor lambda. Bounding all hard
eigenvalue factors polynomially and integrating their Gaussian tails gives

    integral_{H<0} ... <= C integral_0^infinity
      lambda min(1,epsilon/lambda^3)(1+lambda)^M
                                      exp(-c''lambda^2)d lambda
                         <=C epsilon^(2/3).             (3.7)

For epsilon=s^3<=1, the part below one uses exactly
integral_0^1 lambda min(1,s^3/lambda^3)d lambda=(3/2)s^2-s^3;
the remaining Gaussian tail is O(epsilon). This argument uses only an
isotropic upper envelope, not an isotropic law for H.

Take epsilon=kr^3t, reduce r_* so epsilon<=1 for t<=1, and set N=d+3.
Equations (3.6)-(3.7) prove

    E_Q[W_r;0<X_r<=t,P>c0/r]<=C r^5 t^(2/3).            (3.8)

This estimates even the nonfailure part and includes the rare axial-pivot,
large-derivative and scalar-far sectors. Only polynomial moments are needed.

## 4. Exact Schur-edge integration on the moderate sector

Work on W_r>0 and P<=c0/r. Choose c0 small enough, uniformly for k>=k_-,
that (2.9) implies

    q=6k-rA>=3k_->0,           rM4<=3k_-/10.             (4.1)

Use the actual positive Schur matrix

    C=B-(r/q)vv^T>0,
    x=lambda_min(C),
    |det H_M|=rq det C.                                 (4.2)

The variable C in this section is a matrix, whereas an unspecified constant
is written C_* where a distinction is needed. For fixed A,v the change
B=C+(r/q)vv^T has Lebesgue Jacobian one. Its shift is positive semidefinite;
therefore on C>0

    ||B||_F^2>=||C||_F^2.                               (4.3)

This retains a Gaussian envelope in C without a positive exponential in
|v|^4. In particular (2.6) is bounded by
C_* exp[-c_*(A^2+|v|^2+||C||_F^2)] in these coordinates.

The original global cap implication [P] §7, completed in §8 using CAP, is

    F_r subset G_r^c,
    G_r={lambda_min(B)>[4/(3k)]rM3^2, rM4<=3k/10}.       (4.4)

It applies to the ACTUAL global elder event, rather than a count of window
witnesses. Thus (4.1) forces, on F_r in the present sector,

    lambda_min(B)<=C_*rK^2,   x<=lambda_min(B)<=C_*rK^2.  (4.5)

The comparison x<=lambda_min(B) follows from C<=B as quadratic forms.
For ordered eigenvalues lambda_j of B, the individual bound displayed in
[P] §6 immediately before (6.2) is

    |det H_S|<=r(M3/2)[lambda_1+(3/2)rM3]
                              product_{j=2}^m(lambda_j+rM3).  (4.6)

It retains the saddle mixed-square term; it follows from [P] (5.3) and the
singular-value and adjugate bounds there. Since lambda_j<=||B||<=C_*K,
(4.5)-(4.6) imply, with the empty product understood when m=1,

    |det H_S|<=C_*r^2 K^(m+2),
    W_r<=C_*r^3 q (det C) K^(m+2).                     (4.7)

### 4.1. At least two transverse directions

Suppose m>=2. Write the ordered eigenvalues of C as

    0<x<=h2<=...<=hm,
    T=1+J+|A|+|v|^2+hm.

On this ORIGINAL ordered domain T is independent of the inner variable x.
Since q is bounded below, (4.2) gives

    P<=C_*T,   K<=C_*T,   q<=C_*T,
    x<=C_*rT^2 on F_r.                                 (4.8)

Indeed ||B||<=||C||+C_*r|v|^2<=C_*T. The last inequality is (4.5).
The exact quadratic-form completion is

    -H_M=L diag(rq,C)L^T,
    L=[[1,0],[-v/q,I]].

Since ||L^-1||^2<=C_*(1+|v|^2)<=C_*T^2, it yields

    lambda_min(-H_M)>=c_*min(r,x)/T^2,
    X_r>=c_*T^-8 min(1,(x/r)^3).                       (4.9)

The second line follows from (3.1), K<=C_*T, and k<=k_+.
If X_r<=t and x<=r, (4.9) gives x<=C_*rt^(1/3)T^(8/3).
If x>r, it gives 1<=C_*tT^8; use this together with x<=C_*rT^2 from
(4.8). Both cases imply, on the original domain,

    x<=C_* r t^(1/3) T^(14/3).                         (4.10)

Diagonalize C in its actual matrix Lebesgue integral. The angular space is
compact; the Vandermonde, det C=x product h_j, q, and all remaining weight
factors in (4.7) are bounded by x times a fixed polynomial in T. This uses
0<x<=hm on the ORIGINAL ordered domain. Drop the nonnegative Gaussian
factor exp(-c_*x^2). Only AFTER these bounds and (4.10) have been obtained,
extend the inner interval from its true ordered restricted set to

    0<x<C_*r t^(1/3)T^(14/3).

T in this extended positive majorant remains the function of the retained
variables defined above; no bound on the original field is claimed at the
artificial added points. The inner numerator is bounded by

    C_* r^3 T^M integral_0^{C_*rt^(1/3)T^(14/3)} x dx
       <=C_* r^5 t^(2/3) T^(M+28/3).                  (4.11)

Its remaining majorant is exp[-c_*(A^2+|v|^2+sum h_j^2)] times the independent
J law. Integrating gives a finite constant by (2.8). Hard eigenvalues may
approach zero or coincide; their Vandermonde contributes no negative powers.
Thus all higher-corank regions are included in (4.11).

### 4.2. One transverse direction

For m=1 the largest eigenvalue is x itself. Define instead

    T=1+J+|A|+|v|^2,
    P<=C_*(T+x).

Equation (4.5) implies x<=D r(T+x)^2 for a fixed D. Since
(T+x)^2<=2T^2+2x^2, either

    x<=4DrT^2,                 or x>1/(4Dr).            (4.12)

The far alternative is retained at this stage. But B=x+(r/q)|v|^2>=x,
so P>=x. After reducing c0 so c0<1/(4D), it contradicts P<=c0/r.
It is already covered by the large-P bound (3.8), rather than discarded.
On the remaining near branch,

    P,K<=C_*T^2,
    lambda_min(-H_M)>=c_*min(r,x)/T^2,
    X_r>=c_*T^-10 min(1,(x/r)^3).                      (4.13)

The same two cases used for (4.10), now with x<=4DrT^2, give

    x<=C_*rt^(1/3)T^(16/3).                            (4.14)

Here det C=x and there is no spectral Vandermonde. Equations (4.3),(4.7)
give a numerator majorant C_*r^3 xT^M exp[-c_*(A^2+|v|^2+x^2)]. Drop the
x Gaussian only after obtaining (4.14), extend the nonnegative inner
integral to that upper endpoint, and integrate x. Its bound is
C_*r^5t^(2/3)T^(M+32/3). The remaining A,v Gaussian integrals and J moments
are finite uniformly, as required.

Both cases prove

    E_Q[W_r;F_r,0<X_r<=t,P<=c0/r]<=C_*r^5t^(2/3).       (4.15)

Combine (3.8),(4.15) and divide ONCE by the full lower normalizer
Z_r>=z_*r^2 from [P] (5.5), with its retained reading rules. This proves
Theorem U, including the original determinant correlations and all frames.

## 5. Actual marked inverse-moment convergence

This section now consumes the existing actual marked laws: [LOCAL] §8 and
[FIBRE] §§5-6. They prove

    r^-3 P_r(F_r)->a_fail>0,
    r^-3 P_r((Theta_r,T_r,D_r) in dot,F_r)
      converges weakly to the actual pushforward of mu_fail,
    D_r=(d_f(M)-b)/r^3 -> h_*(theta),
    lambda(theta)=-h_*(theta)/k in (0,1).                (5.1)

The position/death sentinels, including essentiality, have o(r^3) mass.
In particular P_r(F_r,ell_r finite)/r^3->a_fail. These are consequences of
those complete source proofs, not new claims established by Theorem U.

Let 0<p<2/3 and 0<delta<=1. Integration by parts for the finite measure
H_r(t)=P_r(F_r,0<X_r<=t), or its elementary Tonelli equivalent, gives

    E_Pr[X_r^-p;F_r,0<X_r<=delta]
      <=delta^-p H_r(delta)
                       +p integral_0^delta t^(-p-1)H_r(t)dt
      <=C r^3 [(2/3)/(2/3-p)] delta^(2/3-p).             (5.2)

The boundary term at zero vanishes by (1.2). This is the required uniform
integrability estimate under the failure-scaled finite measures. In
particular it controls the scales t much smaller than any function of r;
an additive error independent of t would not suffice.

For A>0, apply (5.1) to the bounded continuous function of a finite death
mark obtained from min(x^-p,A), assigning its continuous value A at x=0,
and value zero at the isolated essential sentinel. One can use
x=max(-D_r/k,0); actual finite deaths have D_r<=0. On actual essentiality
the inverse is set to zero solely for this finite-death expectation. The
limit is min(lambda^-p,A). Equation (5.2), with delta=A^(-1/p), makes the
truncation remainder tend uniformly to zero as A tends to infinity.
The limiting inverse integral is finite by the same bound and monotone
convergence. Thus (1.4) follows, and division by the positive limiting mass
proves (1.5). The p=0 formula is simply the finite-failure mass convergence.

If instead one conditions on F_r alone and defines X_r^-p=0 on essentiality,
the same limit holds, since its denominator also has limit a_fail r^3.
Nothing here changes the literal extended-lifetime convention for positive
powers: its essential-inclusive positive moments remain a separate issue.

## 6. Sharp boundaries and the distinct distant-partner law

[FIX] proves, for EACH fixed r>0, a positive small-lifetime lower bound of
order epsilon^(2/3) for finite failures under the original full tilt.
Therefore its finite-failure inverse moments are infinite for every p>=2/3.
No matter how small the lower-bound constant becomes as r decreases, those
finite-r infinite expectations cannot converge as finite numbers to an
integrable limiting observable. Theorem U supplies the previously missing
uniform bound on the entire admissible range 0<p<2/3.

The exponent 4 in `../elder_partner_extremes_20260930/PROOF.md` Section5 belongs to
its further, sequential distant-partner conditioning after the contact
limit. It is a different law with different limiting operations. It is
compatible with both [FIX] and Theorem U; no correction of that source is
implied. This note does not need or assert a new sharp lower-tail theorem
for mu_fail itself.

The new analytic obligations exposed here are the enlarged exact endpoint
regression in §2, the tail-retaining large-P integral in §3, and the exact
Schur-edge integral in §4. Their proofs above introduce no unproved
inverse-hard-eigenvalue estimate, hidden conditioning, r-dependent moment
order, or proxy replacement for the actual lifetime. Existing marked-law,
cap, and ordinary-elder source conclusions remain consumed with their
original scope and dispositions. No formal verification or different-family
scientific review of this new consumer is claimed.
