# Cusp coefficient on the finite torus: birth-marginal covariance transfer

Object OA-CUSP-TORUS-TRANSFER-20261001-v1. OpenAI / GPT-6 Astra Pro.
Author-side mathematical candidate; new nonauthor review OPEN. Scientific effect NONE.
No source proof, status register, Boolean, prize or earlier verdict is changed.

## 1. Scope, credit and statement

This completes the interrupted pickup on Math-#219 (5930612079), recovered under
Dylan's new screenshot continuation. The peer subsequently published Lemma S in
#219 v1.1 (3ac897a), already treating d=2,3 and L>=24 by a full-jet density
sandwich. That overlap is credited, not represented as independent acceptance.
The present distinct improvement integrates out birth BEFORE the comparison,
proves a stronger reference floor, and supplies bounds for every L>=10 in
**d=1,2,3 and every orthonormal frame**. No expensive reference quadrature is rerun.

Let phi(x)=exp(-|x|^2/2), and use the normalized periodic covariance

 K_L(x)=sum_{n in Z^d} phi(x+Ln)/sum_{n in Z^d} phi(Ln).             (T1)

For an axial unit vector u with orthonormal transverse frame Theta, set m=d-1,
A=D_Theta^2 f, gamma=grad_Theta d_u^2 f, f4=d_u^4 f,
Delta=det A, Y=f4 Delta/12-gamma^T adj(A)gamma/4 and

 h(A,gamma,f4)=|Y|^(7/4)|Delta|^(1/4) 1{A<0}.                      (T2)

When d=1, det(empty)=1, the quadratic term is zero and h=|f4/12|^(7/4).
The object c1 is the explicit integral CU.2 in [CU]:

 c1[K]=-(192/7)2^(1/4) int_{S^(d-1)} int_R
        p_(f,Q)(b,0) E[h | f=b,Q=0] db d sigma(u),
 Q=(grad f,H_f u,d_u^3 f).                                       (T3)

It is defined here as a finite Gaussian integral. Its identification as the
ell^(1/4) term of an ACTUAL elder lifetime density is the distinct, conditional
claim of [CU], not proved or reviewed by this packet. For d=1 the same expression
is covered, without extending [P]'s d>=2 parent theorem by notation.

**Theorem T.** Write N_d=3d+1+d(d-1)/2, so N_1=4,N_2=8,N_3=13, and

 E_d(L)=3d 3^(d-1) (764 d^4 L^8+105) exp(-L^2/2),
 delta_d(L)=3N_d E_d(L),   eta_d(L)=13 delta_d(L).                 (T4)

For d=1,2,3 and every real L>=10, the integral (T3) is strictly negative and

 |c1[K_L]/c1[phi]-1| <= eta_d(L).                                 (T5)

The same relative comparison holds for the positive integrand after birth
integration at EACH frame. In particular, rigorously rounded upper bounds are

| dimension | all L>=10 | all L>=24 |
|---|---|---|
| 1 | 6.89628366587e-9 | 3.29775477012e-109 |
| 2 | 1.32408646215e-6 | 6.33168915861e-107 |
| 3 | 4.90170601596e-5 | 2.34396164673e-105 |

Thus both estimates in the interruption screenshot are achieved, conservatively:
**less than 5e-5 for L>=10 and less than 3e-105 for L>=24** in these dimensions.
These are covariance-transfer bounds for a specified coefficient integral,
NOT total errors of a finite-lifetime approximation and NOT 105-digit reference
coefficient evaluations. The original reference interval widths remain present.

## 2. Integrate birth, retain its correlations

Let Z consist of the independent upper-triangular entries of A, then gamma, then
f4; let X=(Q,Z) and C_{L,u}=Cov X. There are q=2d+1 zero-pin coordinates and
n=m(m+1)/2+m+1 free coordinates, with q+n=N_d. All are centered before conditioning.
Because h is nonnegative and independent of f itself, Tonelli and Gaussian
marginalization give the EXACT identity

 int_R p_(f,Q)(b,0) E[h | f=b,Q=0] db
                =int_{R^n} h(z) p_X(0,z) dz =: J(C_{L,u}).        (T6)

No old full-normalizer or pin-density factor is inserted a second time. This
step discards f as a coordinate of the covariance, not as a source of correlations.
For the reference kernel, conditioning on (f=b,Q=0) gives independent f4, gamma
and A with means -3b,0,-bI and variances24,2I and GOE variances2/1. But after birth
integration, the normalized b-mixture has b~N(0,2/3). Thus, for example,

 Var(f4 | Q=0)=30,
 Cov(f4,A_ii | Q=0)=2,
 Var(A_ii | Q=0)=8/3,
 Cov(A_ii,A_jj | Q=0)=2/3, i!=j.                         (T7)

Pretending that all these variables remain independent would change (T3).
The exact companion recomputes both Schur complements and their mixture identity.
At finite L no reference conditional independence or rotational invariance is
assumed: C_{L,u} retains every covariance entry.

The weight is homogeneous under simultaneous POSITIVE amplitude scaling:

 h(tA,t gamma,t f4)=t^p h(A,gamma,f4),
 p=2m+7/4=2d-1/4.                                            (T8)

Indeed Delta has degree m, each term in Y has degree m+1, and the cone A<0 is
preserved. Even at a singular A, the adjugate is a polynomial; there is no inverse
matrix in (T2). The weight is measurable, nonnegative and polynomially bounded.
For positive definite C, its Gaussian slice integral is finite and positive:
the negative cone and the set Y!=0 contain a nonempty open set with positive
density. These facts also cover d=1 directly.

Substituting z=sqrt(a)w into the density integral yields

                  J(aC)=a^((p-q)/2) J(C)=a^(-5/8)J(C).           (T9)

The zero-pin count is 2d+1, not 2d+2, because birth was INTEGRATED, not set to zero.
Neither h's lack of differentiability nor the cone boundary is differentiated.

## 3. An exact reference-covariance floor

For the reference kernel in any orthonormal frame,

 Cov(d^alpha f,d^beta f)=(-1)^|beta| d^(alpha+beta)phi(0).          (T10)

If a coordinate of alpha+beta is odd, the entry vanishes. Otherwise it is
(-1)^(|beta|+|alpha+beta|/2) product_i (alpha_i+beta_i-1)!!.
The sign can equivalently use |alpha|; all nonzero entries have even total order.

**Lemma F.** In the stated raw independent-entry coordinates, C_0>I/3.
In fact the proof holds for every fixed integer d>=1, though the quantitative
image bound and table of this packet are restricted to d<=3.

Proof. By coordinate parity and permutation, the odd block is the direct sum
of [[1,-3],[-3,15]] (f_u,f_uuu) and m copies of [[1,-1],[-1,3]]
(f_{theta_j},f_{uu theta_j}). After subtracting I/3 their leading pivots are2/3,
and the respective second pivots are7/6. Thus each block is positive definite.
All off-diagonal Hessian entries are independent variance-one scalar blocks.
The remaining even block comprises the d diagonal Hessian entries and f4:

 B=2I_d+11^T,     v=-3*1-12*e_1,     Var(f4)=105.

After subtracting I/3, B'=(5/3)I+11^T is positive definite and

 (B')^-1=(3/5)I-9/[5(3d+5)] 11^T.

Its last Schur pivot is exactly

 314/3-v^T(B')^-1 v = (417d+2018)/[15(3d+5)]>0.                   (T11)

This exhausts every covariance coordinate and proves the matrix inequality.
It is a dimension-valid algebraic identity, not an eigenvalue estimate from a
floating-point table. The code also performs a separate exact LDL^T elimination.

For example, its complete pivots for C_0-I/3 in d=3, in the ordered labels of
the script, are

 2/3,2/3,2/3,8/3,2/3,2/3,7/6,55/24,2/3,70/33,7/6,7/6,467/30.

The birth-INCLUDED covariance does not have this floor in d=3; its first valid
simple floor in the peer's proof is1/4. Marginalization improves this proof's
conditioning without changing the integral, and reduces N from14 to13. QED.

## 4. Order-eight derivative and lattice-tail control

A covariance involving f4 and f4 uses EIGHT derivatives. The old order-six
SIDE24 estimate cannot be used for this purpose.

For unit directions v_1,...,v_j, differentiation of exp(-|x|^2/2) gives a sum over
partial matchings of the directions: each singleton contributes x.v_i and each
paired pair contributes v_i.v_k, with signs. The number of terms is

 T_j=sum_{a=0}^{floor(j/2)} j!/[2^a a!(j-2a)!].

For0<=j<=8 this is at most T_8=764. Thus for |x|>=1,

 |D^j phi(x)[v_1,...,v_j]|<=764 |x|^8 phi(x),
 |D^j phi(0)[v_1,...,v_j]|<=105.                            (T12)

At zero only perfect matchings survive; the largest number is7!!=105. The
argument is for arbitrary unit directions, not only Cartesian derivatives.

For the infinity-norm shell |n|_infinity=a>=1, the number of lattice points is
(2a+1)^d-(2a-1)^d <=2d3^(d-1)a^(d-1), and |n|^8<=d^4 a^8.
At L>=10,d<=3, successive terms of a^s exp(-L^2a^2/2), for0<=s<=d+7, have ratio
at most2^10 exp(-150)<1/3. Already exp(150)>1+150+150^2/2=11401>3072
proves this last bound. Therefore

 sum_{a>=1} a^s exp(-L^2a^2/2) <= (3/2)exp(-L^2/2).              (T13)

Let S_L=sum_{n!=0}phi(Ln). Normalization in (T1) gives

 D^j K_L(0)-D^j phi(0)
 = [sum_{n!=0}D^j phi(Ln)-S_L D^j phi(0)]/(1+S_L).

Using (T12)-(T13) and 1+S_L>=1 proves that every entry of C_{L,u}-C_0 has
absolute value at most E_d(L) in (T4). This includes the denominator correction
105; it is not silently discarded. There is no extra rotation norm: every
contraction used in (T10) consists of unit frame directions covered by (T12).

For an N by N symmetric perturbation bounded entrywise by E, its operator norm
is at most NE (for instance by its Frobenius norm). Since C_0>I/3,

 (1-delta)C_0 <= C_{L,u} <= (1+delta)C_0,
                      delta=3NE_d(L).                           (T14)

The computed delta at d=3,L=10 is below3.771e-6, in particular below1e-4. The
function (a L^8+b)exp(-L^2/2) is decreasing for L>=10 when a,b>0, by differentiation.
Thus every bound at10 or24 remains valid for all larger REAL side lengths.
No lattice-axis alignment or isotropy of the finite torus is assumed.

## 5. Transfer of the entire nonsmooth cone integral

For positive definite C satisfying (T14), inverse and determinant inequalities
give pointwise on R^N

 [(1-delta)/(1+delta)]^(N/2) p_((1-delta)C0)
 <=p_C<=
 [(1+delta)/(1-delta)]^(N/2) p_((1+delta)C0).                      (T15)

Restrict to Q=0, multiply by the NONNEGATIVE h, and integrate. By (T9),

 L_N(delta) <= J(C)/J(C0) <= U_N(delta),
 L_N=(1-delta)^(N/2-5/8)/(1+delta)^(N/2),
 U_N=(1+delta)^(N/2-5/8)/(1-delta)^(N/2).                         (T16)

This is not a uniform relative expectation bound for arbitrary measurable tests:
h's specific nonnegative homogeneity is essential. In particular it avoids the
invalid strategy of perturbing the negative-cone boundary or differentiating a
fractional power through singular matrices.

For N<=13 and0<=delta<=1e-4, put a=N/2-5/8,b=N/2. Both a,b are positive. The
absolute logarithmic derivatives of L_N and U_N are bounded above by

 a+b/(1-delta) or a/(1-delta)+b <= (99/8)/(1-1e-4)<25/2.

Consequently L_N>=exp(-(25/2)delta)>=1-(25/2)delta, and
U_N<=exp((25/2)delta)<=1/[1-(25/2)delta]<=1+13delta on this interval.
The final inequality follows by multiplication of positive denominators. Thus

              1-13delta <= L_N <= U_N <=1+13delta.                (T17)

The reference J(C0) is the same in every frame, but the actual J(C_{L,u}) need
not be. Angular integration preserves the bounds since it integrates positive
quantities. Multiplying by the common NEGATIVE prefactor in (T3) preserves the
positive ratio c1[K_L]/c1[phi]. This proves (T5).

Normalization matters: if K_L^raw=(1+S_L)K_L, then exactly
c1[K_L^raw]=(1+S_L)^(-5/8)c1[K_L]. We state our theorem for normalized (T1),
not as equality of normalized and unnormalized coefficients.

## 6. Exact arithmetic and what the numerical table does establish

Only integer/Fraction arithmetic is used for the certificate. For x>=0 and an
integer n with x/(n+2)<1, write S_n=sum_{j=0}^n x^j/j! and t_{n+1}=x^(n+1)/(n+1)!.
All remaining successive term ratios are <=x/(n+2), so

 S_n <=exp(x)<=S_n+t_{n+1}/(1-x/(n+2)).

Reciprocals provide a rational interval for exp(-x). The code uses
n=2ceil(x)+64 and applies this to x=50 and288. No libm exponential is trusted.
Rational values are rounded upward for error bounds; negative absolute coefficient
intervals use a separate correct floor/ceiling rule. Fractional sandwich powers
are verified by raising both positive sides of (T16)-(T17) to the EIGHTH power,
which reduces each comparison to rational arithmetic.

The broad headline bounds are strictly below5e-5 and3e-105. The table in §1 keeps
12 significant digits rounded upward, not nearest rounding. An absolute interval
[alpha,beta] for c1[phi], alpha<beta<0, transports to

                 [alpha(1+eta), beta(1-eta)].                    (T18)

The `conditional_absolute_c1` entries in RESULTS.json apply (T18) to the OUTWARD
reference table in [NUM]. They are conditional consumers of that certificate:
we do not re-evaluate or independently accept its Mellin reduction, special
functions or quadrature. Tiny transfer errors are applied as rational numbers
before decimal rounding and are never rounded to zero. At L>=10,d=3 the resulting
interval is [-0.2118587311831697,-0.2118379618168794]. At SIDE24 the reference
certificate's much wider uncertainty dominates the negligible transfer allowance.

The bound on covariance replacement does not control the o(ell^(1/4)) term in
[CU], any finite-lifetime percentage forecast, c2, or parameter-uniform asymptotic
rates. The existence and value of the CU.2 integral are distinct from its
interpretation as a persistence asymptotic coefficient.

## 7. Recovery, review and verification boundaries

Sources in SOURCES.json bind [P] (model definition only), [CU] (expression CU.2
only), and [NUM] (reference interval transcription and peer overlap credit).
No independent proof status for these source theorems is manufactured. The older
R.1 reference-regression review5378866830 was recovered on GitHub: it was delivered
by this same conversation before interruption. It is NOT issued again or counted
as independent acceptance of this transfer. New exact matrix replay agrees with it.

New review requests:
A: (T6)-(T11), birth marginalization, retained mixture correlations, positive
homogeneity and dimension-valid reference floor.
B: (T12)-(T17), order-eight/all-frame image estimate, normalized denominator,
entrywise-to-operator conversion, two-sided Gaussian sandwich and linear bound.
C: numerical comparisons/rounding, conditional use of [NUM], and separation of
coefficient transfer from the parent asymptotic theorem. Tests do not replace
these analytic reviews. No self-merge, register change or new Lean formalization.

The finite controls rebuild all covariance matrices from derivative multi-indices,
verify independent Hermite recurrences, LDL reconstruction, full-birth regression
and marginal mixtures, homogeneous polynomial identities and signed interval
transport. Both modes and eight semantic mutations are replayed. The original
eight-method scaffold failed all eight tests before implementation. Code for
historical source verification is reused from the prior D1 audit with a small
per-source-commit entry adaptation and its real-Git tests retained.

The local raw-host network lookup failed DNS, so historical source objects were
not available locally. `--local-only` reports that fact. Actual project source
commit/path/blob authentication is a hosted requirement, not replaced by matching
local fixture data. The author's isolated mathematical checks are not a new
provider review. Final head-specific hosted observations belong in the PR receipt.

External background: DLMF §4.2(iii), equation4.2.19, supplies the familiar exponential
series, and DLMF §18.5 gives Hermite polynomial representations. The needed
remainder, matching-count and covariance calculations are derived above. These
primary web records were read at page/search depth, not as an exhaustive novelty
audit. The peer's #219 Lemma S already contains the overlapping density-sandwich
idea; this packet contributes the wider side range, marginal floor and bounds.
