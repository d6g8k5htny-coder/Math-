# Intermediate height-window bridge: a summable single-witness estimate

Object: OA-D5-INTERMEDIATE-WINDOW-20260928-v1.
Author: OpenAI / ChatGPT, foreground continuation.
Disposition: AUTHOR-SIDE ANALYTIC CANDIDATE; NONAUTHOR REVIEW REQUIRED.
Scientific effect: NONE. No controlling claim, graph, proof-index verdict, prize, or seal is changed.

## 1. Purpose and exact statement

The fixed-scaled-ball result does not permit substituting R=R(r) tending to infinity. This note treats the intermediate region with a second physical scale s, explicitly restricts the witness height to the original between-pin window, and obtains a bound summable over dyadic shells. It does not assert an all-height intermediate O(r^3) estimate.

Fix T>0 and the variance-one centered planar Gaussian field with covariance

    K_T(h)=sum_(n in Z^2) exp(-|h+Tn|^2/2)
            / sum_(n in Z^2) exp(-|Tn|^2/2).

Fix a compact birth interval and 0<k_-<=k<=k_+<infinity. Locations and frames range over the torus and O(2). Use an embedded frame chart with midpoint zero,

    M=(-r/2,0), S=(r/2,0),
    f(M)=b, f(S)=b-k r^3, grad f(M)=grad f(S)=0.        (I1)

Q_r is continuous Gaussian regression on exactly these six observations. It is not an adjacency law. As usual F_j(H)=|det H| on nonsingular symmetric Hessians with negative index j, zero otherwise. Retain

    W_r=F_2(H_M)F_1(H_S), Z_r=E_Qr W_r,
    dQ_r^W=(W_r/Z_r)dQ_r,
    I_r=(b-k r^3,b), b_bar=b-k r^3/2.                 (I2)

Let N_(r,j)(B) count index-j critical points in B with height in I_r. All spatial distances in the statement are physical distances in the local chart, except in the explicitly scaled annulus A={w:1<=|w|<=2}.

**Shell candidate.** There are C,s_0>0 such that for 0<r<=s/4 and 0<s<=s_0,

    E_(Q_r^W) N_(r,j)({s<=|X|<=2s})
       <= C r^3 [(r/s)^2+s^2].                        (I3)

Constants are uniform in s,r, the stated marks, frames, and j. They depend on T and the compact mark ranges. Choose s_0 small enough for every segment to embed and for the uniform estimates below. There is no numerical value of C or s_0.

**Intermediate candidate.** Uniformly for A_0>=4 and A_0 r<rho<=s_0,

    E_(Q_r^W) N_(r,j)({A_0 r<=|X|<=rho})
       <= C r^3 (A_0^-2+rho^2).                       (I4)

A_0 is a cutoff, not a Gaussian jet. The same bound holds for any Borel subset of the indicated region. The constants do not grow with the number of dyadic shells. The empty-region case is zero.

Combining (I4) with the reviewed fixed-scaled-ball bound and the fixed-remote height-window bound gives, in this exact planar model and these fixed mark ranges,

    E_(Q_r^W) N_(r,j)(torus minus {M,S}) <= C r^3.      (I5)

The count in (I5) STILL HAS THE HEIGHT RESTRICTION I_r. The prescribed pins are removed. Markov then bounds the probability of at least one additional critical point in that window by Cr^3. This is not an elder-selection theorem and gives no second factorial moment or shrinking multiple-witness collision estimate.

## 2. Exact dependencies and a distinction from the previous proof

All source paths are in d6g8k5htny-coder/Math- at
`aeed37683702e987f8a3cf081acb407bb942f107`:

- `reviews/d5_local_collar_20260928/PUNCTURED_PIN_PROOF.md`, SHA256
  `f972e50bc07674ebce9d971d1a1bd4dba2f8036dde37ecb57d8a44a35650f76a`:
  uniform endpoint regression, all fixed derivative-supremum moments, original positive-k normalizer, and punctured endpoint disks.
- `reviews/d5_local_collar_20260928/COLLAR_PROOF.md`, SHA256
  `794babe0fd039c3a93c401c0b8978316331af009fad45f953e63fbe7e1e31aab`:
  degree-five interpolation and the fixed-scaled-ball synthesis, not a growing-radius result.
- `frontiers/remote_window_20260924/PROOF.md`, Git blob
  `b383bfcc88ec4ad497dff01fb6640e429ba24a84`: fixed-remote height-window result; its spatial exclusion radius is fixed.
- `frontiers/three_fronts_20260924/RN_COUNT_INTERFACE.md`, Git blob
  `371fd6d17920f2eb3b1c5ec30297acf6daf1d385`: original-weight count identity and why event probabilities or unconditioned finite moments do not imply the required count estimate.

Math-#105 review comment5872932723 and replay5872950920 concern its exact prior source head. Their confirmation is not a review of THIS note. Both previous proofs remain unchanged.

Here the witness value is ACTUALLY conditioned during height disintegration, and the resulting density is then integrated over I_r. There are six-plus-three Gaussian observations. This differs deliberately from the earlier all-height pin/collar argument, whose actual conditioning had six-plus-two observations. The extra height factor is derived from a joint density, not inserted into an all-height estimate.

We consume the exact endpoint-law bounds

    E_Qr (1+||f||_(C^m))^p <= C_(m,p),
    Z_r >= c_Z r^2,                                   (I6)

for every fixed finite m,p and all sufficiently small r. The norms cover the torus and hence every Taylor segment. The sources prove these using a bounded-target Hermite frame, strictly positive Gaussian-decaying Fourier weights on the full lattice, uniform finite-jet covariance, and a positive-probability signed-curvature event with controlled remainders. No witness-conditioned quantity replaces Z_r. A failure of (I6) blocks this note's application.

## 3. A nine-row covariance floor uniform through endpoint confluence

Write epsilon=r/s in (0,1/4]. We first prove a coarse observation floor that has NO adverse epsilon or r/s factor.

Let H_r be the cubic interpolant of f(x,0) and f_x(x,0) at +/-r/2, and L_r the affine interpolant of f_z(x,0) there. The unconditional linear frame is

    U_r=(H_r(0), H'_r(0), H''_r(0), H'''_r(0),
         L_r(0), L'_r(0)).

It is invertibly equivalent to the six raw endpoint observations. Its exact target is

    (b_bar, -3k r^2/2, 0, 12k, 0, 0).                 (I7)

Its contact limit is U_0=(f,f_x,f_xx,f_xxx,f_z,f_xz) at zero. Define

    S_s=diag(1,s,s^2,s^3,s,s^2),
    V_(r,s,w)=(S_s U_r, f(sw), s f_x(sw), s f_z(sw)),
    w=(u,v) in A={1<=|w|<=2}.                          (I8)

There are nine coordinates. In dimensionless variables Y=X/s, S_s U_r is exactly the epsilon-Hermite frame applied to f(sY).

### 3.1 Polynomial row rank, including epsilon=0

For scalar polynomials P of total degree at most five, define B_(epsilon,w) to apply the six epsilon-Hermite functionals followed by value and the two derivatives at w. At epsilon=0 use the six contact jets instead. Use the fixed monomial basis (21 monomials).

For epsilon>0 the Hermite transform is invertible, and the three distinct sites (-epsilon/2,0),(epsilon/2,0),w admit arbitrary values and gradients from degree-five polynomials. One explicit proof chooses a direction with three distinct projections t_i, uses the degree-two Lagrange polynomials L_i, and the degree-at-most-five cardinals

    [1-2 L_i'(t_i)(t-t_i)] L_i(t)^2,
    (t-t_i)L_i(t)^2,
    (z-z_i)L_i(t)^2.

Their value, longitudinal-derivative and transverse-derivative responses at the three sites are independently prescribed. This is the elementary interpolation argument in the collar source; no quantitative projection separation is asserted as epsilon approaches zero.

At epsilon=0 the six contact rows are independent. To control the remaining three rows using polynomials that vanish on all six contact functionals:

- if v!=0, use z^2,z^3,x z^2; their value/gradient determinant at w is -v^6;
- if v=0, then |u|>=1, and x^4,x^5,x^2 z have value/gradient determinant u^10.

Thus B_(epsilon,w) has full row rank also at confluence. Its entries, obtained by exact polynomial Hermite interpolation, are continuous at epsilon=0. Compactness of [0,1/4] x A supplies a UNIFORM positive smallest row singular value. This is not obtained by taking the distinct-site constant and assuming it survives collision.

Degree four would fail on the collinear contact configuration: four longitudinal contact jets and the witness value/slope impose six conditions on a univariate polynomial with only five coefficients. The degree-five coordinate is load-bearing.

### 3.2 Taylor remainder through the divided differences

Let J_5 be the 21 midpoint Taylor coefficients D^alpha f(0)/alpha!, and D_s the diagonal matrix with entries s^|alpha|. Then

    V_(r,s,w)=B_(epsilon,w) D_s J_5+R,
    ||R||_(L^p)<=C_p s^6.                             (I9)

The last three coordinates follow from Taylor's formula for value and s times gradient. The six Hermite coordinates require care because their formulas contain divided differences in epsilon.

For the dimensionless Taylor remainder R_s(Y), every derivative of order j<=3 on the bounded interpolation domain is O(s^6 K_6). The cubic Hermite coefficient functionals at +/-epsilon/2 have operator norms uniformly bounded on C^3 for 0<=epsilon<=1/4. Here is an explicit verification. Put a=epsilon/2 and, for a scalar g, write

    s0=[g(-a)+g(a)]/2, d0=[g(a)-g(-a)]/(2a),
    s1=[g'(-a)+g'(a)]/2, d1=[g'(a)-g'(-a)]/(2a).

Its cubic interpolant H satisfies

    H(0)=s0-a^2 d1/2, H'(0)=(3d0-s1)/2,
    H''(0)=d1,
    H'''(0)=3(s1-d0)/a^2
           =[3/(4a^3)] integral_(-a)^a (a^2-t^2) g'''(t) dt.

The last kernel is nonnegative and integrates to one; the identity follows by two integrations by parts. The first divided differences are averages of g' or g'', so all four bounds are uniform. At a=0 take the corresponding derivative limits. The affine transverse interpolant likewise uses the average endpoint values and the average of its derivative, hence has a uniform C^1 bound. Applied to the restriction of R_s and its transverse derivative, these estimates give O(s^6 K_6) for every scaled endpoint coordinate, without a negative power of epsilon. By (I6) the same bound holds in each finite L^p. In this unconditional step the original field has the same finite derivative moments, so (I9) holds before endpoint regression as well.

The covariance of J_5 is uniformly positive definite, by the positive full Fourier lattice and distinct one-site derivative monomials, uniformly over frames. For a unit row a, with 0<s<=1,

    std(a B D_s J_5) >= c ||a B D_s||
                     >= c s^5 ||a B|| >= c' s^5.

Centering the remainder only changes its constant. Subtract its L^2 norm from this standard deviation and reduce s_0. Therefore

    Cov(V_(r,s,w)) >= c s^10 I_9.                      (I10)

Unscale all endpoint coordinates and witness gradients. Every inverse scale is at least one for s<=1, so the lower bound persists. Take the Schur complement of the six endpoint coordinates, equivalently conditioning on the original pins. For Y_X=(f_x(X),f_z(X),f(X)),

    Sigma_X=Cov_Qr(Y_X) >= c s^10 I_3.                 (I11)

The Schur variational identity justifies this: inf_b Var(a Y_X+b U_r) >= c s^10 ||a||^2. No observation-density Jacobian from the endpoint transform enters the conditional count formula.

## 4. Midpoint expansions and the actual height coordinate

Let T_3=f_xxz(0), C_3=f_xzz(0), D_3=f_zzz(0), S_0=f_zz(0), actual midpoint jets under Q_r. They are distinct from U_0. Their joint conditional covariance given U_r is bounded above and below, their means are bounded, and all their fixed moments are bounded by (I6).

The exact endpoint constraints and symmetric Taylor formulas give, pathwise with K a fixed multiple of 1+||f||_(C^6),

    |f(0)-b_bar| <= C r^4 K,
    f_x(0)=-3k r^2/2+O(r^4 K),
    f_z(0)=-r^2 T_3/8+O(r^4 K),
    |f_xx(0)|+|f_xz(0)| <= C r^2 K,
    f_xxx(0)=12k+O(r^2 K).                             (I12)

For example the average endpoint slopes and endpoint height difference determine f_x(0),f_xxx(0); the endpoint slope difference determines f_xx(0). The same two transverse-gradient equations determine f_z(0),f_xz(0). These are deterministic consequences of the original six pins, with derivative-controlled remainders, not replacements of random jets by their means.

Put d_e=u^2-epsilon^2/4. At X=s(u,v), uniformly in epsilon in [0,1/4] and w in A,

    f_x(X)/s^2 = 6k d_e+uv T_3+(v^2/2)C_3+O(s K),
    f_z(X)/s   = v S_0+(s/2)d_e T_3+suv C_3
                      +(s v^2/2)D_3+O(s^2 K),
    [f(X)-b_bar]/s^3
               = k(2u^3-3epsilon^2 u/2)+v^2 S_0/(2s)
                 +(v d_e/2)T_3+(uv^2/2)C_3
                 +(v^3/6)D_3+O(s K).                  (I13)

The apparently large S_0/s term is removed by an exact row operation. Define

    Z=( f_x(X)/s^2,
        f_z(X)/s,
        [f(X)-b_bar-(s v/2)f_z(X)]/s^3 ).              (I14)

For J=(T_3,C_3,D_3,S_0),

    Z=(6k d_e,0,k(2u^3-3epsilon^2u/2))+B J+O_(L^p)(s),
    B=[uv, v^2/2, 0, 0;
       0,  0,     0, v;
       v d_e/4,0,-v^3/12,0].                          (I15)

The C_3 term and the S_0 term both cancel from the third row; the D_3 coefficient is -v^3/12. The physical map from Z to (f_x,f_z,f-b_bar) has determinant s^6. At height y in I_r and zero gradient its exact target is

    tau=(0,0,(y-b_bar)/s^3),
    |tau_3| <= (k_+/2)epsilon^3.                      (I16)

This target is bounded uniformly, including epsilon tending to zero. It is not set to zero in the proof.

## 5. A critical-height Euler identity suppresses endpoint curvature

This is the extra factor that prevents a logarithmic loss from shell summation.

Suppose the original pins hold, grad f(X)=0 and f(X)=y in I_r. Taylor expansion about zero through degree three and Euler's identity for homogeneous polynomials give

    3[f(X)-f(0)]-X dot grad f(X)
       =2 grad f(0) dot X+(1/2)X^T H_0 X+O(s^4 K).     (I17)

Cubic terms cancel because their Euler degree is three. By (I12), the height bound |y-b_bar|<=k_+r^3/2, and r<=s/4<=1, the only potentially leading quadratic term is S_0 s^2 v^2/2. All the other terms are bounded by C K(r^2 s+s^4): in particular r^3<=r^2s and r^2s^2<=r^2s. Thus, for v!=0,

    |S_0| <= C K (r^2/s+s^2)/v^2.                    (I18)

This is a bound after the ACTUAL witness height and gradient constraints. It is false as a general all-height substitute. The s^2 contribution arises from fourth-order field terms and cannot be omitted.

The endpoint critical-segment identity gives ||H_M e_x||,||H_S e_x||<=Lr/2, where L<=K bounds Hessian variation. Also f_zz(M),f_zz(S)=S_0+O(rK). Expanding each determinant by entries therefore yields

    |det H_M|,|det H_S| <= C r K(|S_0|+rK).             (I19)

For v!=0, the M-to-S and M-to-X critical-segment identities, followed by Hessian transport, give

    ||H_X|| <= C s K/|v|,
    |det H_X| <= C s^2 K^2/v^2.                       (I20)

For clarity, multiply H_M by (su+r/2,sv). The critical-segment estimate bounds this by C K s^2. Subtract the controlled e_x column and divide by sv. Since |u|,|v|<=2 and r<=s/4, transport to X preserves the C s K/|v| bound.

Combining (I18)-(I20), dropping type indicators, dividing ONCE by Z_r in (I6), and using r^2/s<=r,

    W_r |det H_X| / Z_r
       <= C K^6 s^2 (r+s^2)^2 |v|^-6.                 (I21)

Constants absorb the bounded range |v|<=2. This is pathwise under all nine actual observations. The conditional K^6 moment still must be controlled and is not dropped.

At the axis, instead retain only the two endpoint short-column factors:

    W_r |det H_X| <= C r^2 K^6.                        (I22)

This cancels the original r^2 normalizer without requiring a division by v. Replacing the entire product by K^6 before normalizing would lose this essential uniformity in epsilon.

## 6. Small axial strip: coarse covariance with a Gaussian penalty

Choose a small fixed v_0>0. On A and |v|<=v_0, |u| stays bounded away from zero; epsilon<=1/4 implies d_e is bounded below by a positive constant. The first expansion in (I13), bounded jet means, and (I6) imply

    |E_Qr[f_x(X)/s^2]| >= c_0>0,
    Var_Qr[f_x(X)/s^2] <= C(v^2+s^2),                 (I23)

after choosing v_0 and s_0 small enough, uniformly over marks. The deterministic drift is positive here. This step does not use an isotropic Euclidean replacement for the torus field.

For a positive Gaussian covariance Sigma and target a,

    (a-m)^T Sigma^-1 (a-m) >= (a_1-m_1)^2/Sigma_11.

Use a_1=0 for the first physical gradient component. This lower bound on the FULL Mahalanobis exponent holds regardless of the chosen witness height in I_r.

Split at |v|=s^(1/8). On |v|<=s^(1/8), (I11), (I23) give the joint value-gradient density

    p_(grad f(X),f(X) | pins)(0,y)
       <= C s^-15 exp[-c s^-1/4].                     (I24)

The determinant prefactor is three-dimensional: a covariance floor s^10 gives s^-15, not the two-dimensional prefactor from an all-height calculation.

Under Q_r, the whole field has bounded C^6 moments by (I6). Regress it on Y_X=(grad f(X),f(X)). Cross-covariance derivatives through degree six are bounded; the inverse covariance is O(s^-10); the target (0,y) and conditional mean are bounded. Subtract the regression to obtain a centered Gaussian residual independent of Y_X. The triangle inequality gives

    E_Qr[K^6 | grad f(X)=0,f(X)=y] <= C s^-60.          (I25)

This is intentionally loose, but uniform in epsilon and y. It is a whole-field supremum moment after the additional constraints, not a statement of Hessian independence.

Let Lambda_(r,j)(X,y) be the weighted critical-point intensity per unit physical area and unit height, defined in Section 9. Combining (I6), (I22), (I24)-(I25),

    Lambda_(r,j)(X,y) <= C s^-75 exp[-c s^-1/4] <= C.   (I26)

The 300th positive term of exp(c s^-1/4) gives exp[-c s^-1/4]<=300! c^-300 s^75. Hence this strip contributes at most C r^3 s^2 to the shell count, by the actual window length k r^3 and shell physical area O(s^2). The large integer is just a qualitative absorption device, not an optimized constant or certificate.

## 7. Transverse region: rank, relative error, and conditional moment

For s^(1/8)<=|v|<=2, matrix B in (I15) has coefficient norm O(|v|). The minor from columns (C_3,D_3,S_0) has absolute value |v|^6/24. Consequently

    det(BB^T) >= v^12/576,
    sigma_min(B) >= c |v|^4.                          (I27)

The latter follows by bounding the product of the other two singular values by C v^2. The full four-jet conditional covariance is uniformly positive by (I6) and the contact Schur argument. For any row a, its leading standard deviation is at least c||aB||. The centered O(s) error in (I15) is bounded by C s||a||. Because

    s/|v|^4 <= s^(1/2),

the error is at most half the leading standard deviation for sufficiently small s. This yields a RELATIVE covariance lower bound

    Cov_Qr(Z) >= c BB^T,
    det Cov_Qr(Z) >= c |v|^12,
    ||Cov_Qr(Z)^-1|| <= C |v|^-8,
    Cov_Qr(Z) <= C v^2 I.                             (I28)

No independence between the remainder and the leading jets is used; this is the centered L^2 triangle inequality. Keeping the relative matrix bound avoids replacing det Cov by an unnecessarily worse power.

For |v|<=v_0, (I23) supplies exp(-c/v^2) in the joint density at tau. For |v|>=v_0, a larger constant supplies the same displayed bound since exp(-c/v^2) is then bounded away from zero. The map in (I14) has determinant s^6, so for all the transverse region and y in I_r,

    p_(grad f(X),f(X)|pins)(0,y)
       <= C s^-6 |v|^-6 exp(-c/v^2).                  (I29)

The target tau remains bounded by (I16). Regress the entire field on Z, use the inverse bound in (I28), bounded derivative cross-covariances and endpoint-law moments, and again use the independent residual construction. For the same full-domain K,

    E_Qr[K^6 | grad f(X)=0,f(X)=y] <= C |v|^-48.        (I30)

This coarse exponent suffices. Norms through degree six are used so (I18), (I19), (I20) and all their Taylor remainders are controlled by that SAME K under the extra conditioning.

## 8. The summable gain and the exact shell ledger

Insert the pathwise estimate (I21) into the conditional expectation in the weighted density formula and apply (I29)-(I30):

    Lambda_(r,j)(X,y)
       <= C s^-4 (r+s^2)^2 |v|^-60 exp(-c/v^2)
       <= C' s^-4 (r+s^2)^2.                          (I31)

Every inverse power of |v| is absorbed by its Gaussian factor, uniformly down to the moving lower endpoint s^(1/8). For example the 30th positive term of exp(c/v^2) supplies the |v|^60 power.

Integrate over the physical shell and the actual height interval:

    E N_(r,j)(shell, transverse)
       <= C r^3 (r+s^2)^2/s^2
       <= 2C r^3 [(r/s)^2+s^2].                       (I32)

The final inequality is (a+b)^2<=2a^2+2b^2. It avoids any r times number-of-shells term. Add the axial contribution from (I26) to prove (I3).

The decisive difference from a mere uniform joint-density estimate is (I18). Without its critical-height suppression one can lose the summable [(r/s)^2+s^2] factor and obtain only O(r^3) per shell, leaving a logarithmic loss after summation. No logarithmic loss is discarded here by notation.

## 9. Weighted Kac-Rice and height disintegration

For each r,s>0, the closed shell is separated from the prescribed pins. The observation floor in (I11) gives nondegeneracy of the joint value and gradient; the exact Fourier series gives smooth paths, finite derivative moments and continuous Gaussian regression. Under the Gaussian law Q_r, apply the marked critical-point formula to grad f with the endpoint weight and the witness type/height mark. Disintegrate the auxiliary witness value using the nondegenerate joint density. Thus

    E_(Q_r^W) N_(r,j)(B)
      = integral_B integral_(I_r) Lambda_(r,j)(X,y) dy dX,

    Lambda_(r,j)(X,y)
      = Z_r^-1 p_(grad f(X),f(X)|pins)(0,y)
        E_Qr[W_r F_j(H_X) | grad f(X)=0,f(X)=y].        (I33)

The endpoint Hessians, witness Hessian and value are not independent. The tilted law Q_r^W is not declared Gaussian. The witness determinant occurs exactly once, in F_j.

One precise framework is Armentano--Azais--Leon, arXiv:2304.07424v3, Theorems 2.2 and 7.1 with Remark 8. Start with truncated nonnegative marks and open height intervals. The endpoint filtered determinants are continuous through singular Hessians, the nonsingular index set is open, and the Gaussian conditional laws vary continuously on any fixed compact shell. Truncation and monotone convergence remove growth restrictions. The joint height density, locally bounded for fixed r,s, shows that single boundary heights have zero expected off-pin count. Closed or open I_r therefore give the same result. A general Borel spatial subset follows by equality of the resulting finite measures, or by monotone approximation on these compact domains.

This is a first-moment formula. No factorial-moment collision theorem is used or concluded.

## 10. Dyadic summation and the global single-witness corollary

Take s_j=2^j A_0 r while s_j<rho, and truncate the last shell at rho. The shells cover [A_0 r,rho], up to boundaries which can be assigned once. Since A_0>=4, all satisfy r<=s_j/4. Then

    sum_j (r/s_j)^2 <= 4/(3 A_0^2),
    sum_j s_j^2 <= (4/3)rho^2.                        (I34)

The constants in (I3) are independent of epsilon and j. Summing gives (I4), including parameter families with a growing number of shells. This is the explicit uniform growing-scaled-radius bridge that a fixed-R estimate alone did not supply.

For (I5), fix A_0=4 and any sufficiently small fixed rho. The local region |X|<=4r, with M,S removed, is bounded by the prior fixed-scaled-ball ALL-HEIGHT theorem, hence also by its height-window subset. The intermediate region is bounded by (I4). The fixed remote complement is covered by the source's Theorem A, in d=2 with the SAME original pins and weight, and its fixed rho.

For the upper bound only, the remote interface can also be checked directly: the contact endpoint jets and (grad f(X),f(X)) at a point a fixed distance away are independent derivative distributions on distinct supports. Fourier uniqueness and compactness give a fixed positive covariance floor. Endpoint-conditioned field moments and all witness-conditioned C^3 sixth moments are uniformly bounded. The endpoint critical-segment identity retains W_r<=C r^2 K^4, canceling Z_r>=c_Zr^2; the joint height-gradient density and remaining determinant moments are bounded. Integrating the window of length k r^3 over finite torus area gives O(r^3). No remote lower bound or second-moment statement is needed for this corollary.

All three regions share one exact Q_r, W_r and Z_r. No regional normalizers are multiplied, and no separate pin-density Jacobian is inserted. Take the minimum of the fixed positive radius cutoffs. This establishes (I5) at author-side level, assuming the precisely named source dependencies where consumed.

## 11. Completion boundary and non-claims

This note addresses the intermediate first-moment contribution for witnesses in the BETWEEN-PIN HEIGHT WINDOW. Its synthesis gives an O(r^3) global additional-critical-point first moment for the stated fixed planar Gaussian model and positive compact gap marks. It is a new candidate, not automatically a canonical scientific-status transition.

It does not establish:

- an all-height intermediate or global O(r^3) count;
- a second or higher factorial moment at shrinking witness separation;
- elder-rule pairing, a global RN numerical enclosure, the parent quantitative selector, or a new lifetime asymptotic;
- uniformity as k approaches zero, marks grow, T changes, dimension increases, or field covariance degenerates;
- an explicit numerical C, r_*, or all-cell/24-jet certificate;
- recovery of missing historical drivers or carriers.

The one-witness bridge may remove the need for certain collision machinery in a FIRST-MOMENT-only downstream argument, but it does not discharge any existing factorial-moment obligation without an explicit dependency/scope review. A failing inference must not be hidden by closing a GitHub issue.

## 12. Finite controls, review requests, and reconnaissance

The finite standard-library controls test the Hermite frame through epsilon=0; full degree-five versus failed degree-four contact rank; exact cubic value-gradient row operations and their v^6 minor; the homogeneous Euler cancellation; fixed-height polynomial fixtures retaining both r^2/s and s^2 terms; exact crossover, observation count, power and dyadic ledgers. They deliberately do not certify Gaussian supremum moments, Fourier series, uniform continuum compactness, or Kac-Rice applicability.

A nonauthor reviewer should independently check the nine-row confluent rank and uniform divided-difference remainder; full conditioning versus endpoint-only moments; the actual height target (I16); the pathwise Euler implication (I18); retained endpoint r factors; the relative covariance determinant in (I28); the summable shell factor; and compatibility of the global single-witness synthesis with the exact local and remote source scopes. Source exposure and provider/account independence must be disclosed separately.

Primary framework inspected: Diego Armentano, Jean-Marc Azais, Jose Rafael Leon, *On a general Kac-Rice formula for the measure of a level set*, arXiv:2304.07424v3, https://arxiv.org/html/2304.07424v3 .

Consensus and primary-record reconnaissance: Stephen Muirhead, *A second moment bound for critical points of planar Gaussian fields in shrinking height windows*, arXiv:1901.11336; Statistics & Probability Letters 160 (2020), 108698, DOI10.1016/j.spl.2020.108698. Only the abstract/bibliographic record was used. Its unconditioned large-domain second-moment theorem is NOT substituted for this multiply conditioned two-scale estimate.

The interpolation, Gaussian regression, Euler homogeneous identity, and Gaussian absorption are standard methods or already present in the local sources. The claimed contribution here is this explicit summable height-window application. No comprehensive novelty audit or worldwide-priority claim is made.
