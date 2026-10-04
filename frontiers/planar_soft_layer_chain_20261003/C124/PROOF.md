# A correlated saddle-level estimate and the planar endpoint rate

Object: C124-PLANAR-K1-CORRELATED-BAND-ENDPOINT-LOG-RATE-20261003-v1.
Author: OpenAI/Codex root01a0bbb5, delegated by Dylan Roy.
Author-side analytic/control contributor: OpenAI/Codex next_math_triage.
Source-custody executor: OpenAI/Codex next_ui_triage.
Exact model variant/build UNKNOWN; organizational independence 0.
This is AI-authored mathematics. A subsequent AI review is not human review.
Scientific effect of the author-side packet: NONE; source-bound review follows.
Claim33e06044-3ffa-4d61-81d8-937ad54e3fb4, Work Events733, pickup5974059664.

This additive argument improves the quantitative rate in C101/A4 at physical
gap k=1. It does not replace their field model, event identification, determinant
weight, full normalizer, or geometric hypotheses. The two new ingredients are
a saddle-level band estimate with the correlated field norm still inside the
weight, and an exponential-square bound for the precise endpoint residual.

## 1. Exact population, sources, and conclusion

Fix L>0 and a nonempty compact birth set B0. Work uniformly in b in B0 and
orthonormal planar frames. The centered variance-one Gaussian field on the
flat torus X=R^2/(L Z^2) has covariance

    K_L(z) = sum_(n in Z^2) exp(-|z+Ln|^2/2)
             / sum_(n in Z^2) exp(-|Ln|^2/2).

The continuous Gaussian regression Q_r has exact pins
M_r=(-r/2,0), S_r=(r/2,0), f(M_r)=b, f(S_r)=b-r^3, and zero gradients.
Thus physical k=1, not a variable cubic mark. Define

    W_r=|det H_M det H_S| 1{H_M<0, index H_S=1},
    Z_r=E_Qr W_r=r^2 z_r,        Q_r^W=(W_r/Z_r)Q_r.

The index counts negative eigenvalues. Singular endpoints have weight zero.
H_r is the event that the finite ordinary-superlevel H0 bar born at M_r dies
at S_r, with the global older-point maximin convention of C96. The essential
class is not such a finite bar. Define H_r false off the Morse/distinct-value
locus, F_r=H_r^c and p_r=Q_r^W(H_r). P8/C96 give the actual persistence
interpretation almost surely for each fixed parameter and r; no common
probability-one set over uncountably many laws is asserted here.

Write

    A=f_zz(0), lambda=-A/r,
    t=(gamma,B1,C3)=(f_xxz(0),f_xzz(0),f_zzz(0)), theta=(lambda,t),
    Pjet=1+|gamma|+|B1|+|C3|,
    N=1+max_(|alpha|<=4) sup_X |D^alpha f|,
    a_M=24lambda-gamma^2+12B1, a_S=24lambda+gamma^2-12B1,
    T={a_M>0,a_S>0}, w_lambda=(a_M a_S/16)1_T,
    D=gamma^2-12B1, J=8gamma^3-144B1 gamma+576C3.

On T and gamma!=0 put psi=24lambda/gamma^2, c=D/gamma^2, R=J/gamma^3.
The raw-to-sheared chart is u=X+gamma zeta/12, Z=gamma zeta and the cubic is

    P_QS(u,Z)=2u^3-3u/2-1/2-(psi+2cu)Z^2/48+RZ^3/3456.

Let mu be the highest P_QS(Y)+1 among its extra nondegenerate saddles, or
-infinity if none exists. Set E={T,gamma!=0,mu<0}, Rsec={T,gamma!=0,mu>0}.
All such definitions include C82/C98's absent, degree-drop and tangency cases.
The gamma=0 chart and neutral mu=0 locus are null under the nonsingular raw
jet laws. A neighborhood of the neutral locus is not treated as null.

Let rho_0(a,t) be the JOINT contact-conditioned density of (A,t), with
U_0=(f,f_x,f_xx,f_xxx,f_z,f_xz)(0)=(b,0,0,12,0,0), and let
z_0=36 E[A^2 1{A<0}|U_0]. Define finite failure measures on raw theta-space by

    nu_r^F(B)=r^(-3) Q_r^W(theta in B,F_r),
    dnu_0^F=z_0^(-1) rho_0(0,t) w_lambda 1_Rsec dtheta.       (1)

The variation norm is sup_(|phi|<=1)|integral phi d(nu-nu')|, without 1/2.
The source CUB/C101 identifies its mass as

    M_F=nu_0^F(R^4)=alpha_1+alpha_2,  0<M_*<=M_F<=M^*<infinity. (2)

These are the existing, parameter-dependent CUB G11 coefficients, not
numerically evaluated constants and not alpha_1+2alpha_2.

**Theorem ER.** There exist C<infinity and r_* >0, depending on the fixed
L and compact birth set, uniformly in births and frames, such that for
0<r<r_* with r_*<=exp(-1),

    ||nu_r^F-nu_0^F||_var <= C r^(2/3) log(1/r)^(8/3),
    1-p_r = r^3(alpha_1+alpha_2)
             + O(r^(11/3) log(1/r)^(8/3)).                 (3)

After normalizing these two finite measures to probability measures, the
same variation rate holds for the raw jets conditional on actual failure.
For each fixed soft cutoff Lambda>=1, a sharper local statement is

    Q_r^W(D_Lambda intersect (H_r symmetric_difference E))
                    <= C_Lambda r^(11/3),
    D_Lambda={|lambda|<=Lambda}.                           (4)

The constants and cutoff are analytically finite, not optimized numerical
error bars. No uniformity in L, a growing birth set, or physical k is asserted.
The result is not a once-counted replacement-bar measure, transported
real-height/location total variation, lifetime density theorem, or closure
of shrinking witness collision, small gaps, intermediate regions, higher
dimensions, or the complete persistence-asymptotic dependency graph.

### Source identities and the exact conclusions consumed

All source texts and full hashes are in SOURCE_IDENTITIES.json. These are
frozen inputs, not mutable names used as evidence:

- C82 LB, native5959920397 (proof prefix SHA256
  f390ad99b07ec4eda9160191d776cfc3a53ca628976165987d9a61ab79816827):
  the explicit polynomial saddle-level integral, including exceptional branches.
- C101, native5967063473, SHA256
  300d0d18abb74332e593e389485c817a3c0ea7c31345194e3cfdd4039ac3b5c4:
  Q5–Q19, Q24–Q35, together with its exact P/E1/E2/REC, C91–C98,
  ELDER and CUB interfaces. Its Q23 and polynomial tails are strengthened
  below; its original rejected endpoint estimate is replaced by A4.
- A4, native5972396791, SHA256
  acd172c5f8626aa3b7be5ac691786eefa6d6f243a32909502dfdbd79c8066a7c:
  Lemma LE, Corollary LE, Lemma B-prime and section3's error ledger.
  Full source-bound review5972610615 is a separate record.
- P4.2 is the CENTERED endpoint-matrix residual, with E1 congruence correction,
  E2 section9 replacement and REC. Its P7.5–7.7 and P8 remain hypotheses of
  the imported actual failure-tail and global event interfaces.

In particular, this packet does not independently reprove C95's geometric
theorem or C96's persistence identification. It proves the new analytic
estimates from the identified, scoped input theorems. The present result has
exactly their retained hypotheses; a defect in an input would propagate.

## 2. Retained cutoff-uniform estimates

Let Lambda>=1, H=1+Lambda. C101 constructs constants from the fixed covariance
and compact family, independently of Lambda, such that when r<=r_0 and rH<=1,
the actual conditional joint density satisfies

    rho_r(-r lambda,t)<=C exp(-c|t|^2) on D_Lambda.           (5)

Put D_r=W_r/r^4 and, for field-dependent Phi,

    mu_r(Phi)=r^(-5) E_Qr[W_r Phi 1_DLambda].

The dA=r d lambda change of variables gives

    mu_r(N^p 1_B)=integral_B rho_r(-r lambda,t)
                          E[D_r N^p|lambda,t] d lambda dt,
    Q_r^W(Phi 1_DLambda)=r^3 mu_r(Phi)/z_r.                 (6)

C101 Q7–Q12 prove, for every FIXED p,q>=0,

    E[D_r N^p|lambda,t]
      <=C_p w_lambda Pjet^p+C_p rH^3 Pjet^(p+4),
    mu_r(N^p Pjet^q)<=C_(p,q) H^3,
    mu_r(T^c)<=CrH^4,
    integral_DLambda |g_r/z_r-g_0/z_0|<=CrH^4,
    |z_r-z_0|<=Cr, z_*/2<=z_r<=2z^*, 0<z_*<=z_0<=z^*.    (7)

Here g_r=rho_r E[D_r|theta] and g_0=rho_0(0,t)w_lambda.
The first bound is obtained by multiplying the filtered-determinant error
by N^p BEFORE conditional expectation. It is not an independence assertion,
nor an unweighted density comparison multiplied by an unbounded norm.

## 3. New joint weighted saddle-level band

**Lemma JB.** For each fixed p>=0, uniformly under the conditions of section2
and for 0<delta<=1/2,

    mu_r(N^p; T, gamma!=0, |mu|<=delta)
                           <=C_p(delta+rH^4).             (8)

**Proof.** Insert (5),(7) into the exact integral (6). The determinant-error
term is bounded by

    C_p rH^3 integral_(-Lambda)^Lambda d lambda
             integral exp(-c|t|^2) Pjet^(p+4) dt <= C_p rH^4.

For the principal term first fix t with gamma!=0. The multiplier
exp(-c|t|^2)Pjet^p has no lambda dependence. On T,

    w_lambda d lambda=(gamma^6/384)(psi^2-c^2)d psi,
    psi>|c|.

Extend the nonnegative lambda integral from D_Lambda to the whole typed
half-line. C82 LB gives the actual highest-saddle band bound

    integral_(psi>|c|) (psi^2-c^2)1{|mu|<=delta}d psi
        <=delta[(1024/3)|c|^3+64R^2].

There is no substitution of a psi-dependent width. Multiplying by gamma^6
cancels the chart poles exactly:

    gamma^6 |c|^3=|D|^3,        gamma^6 R^2=J^2.

Thus the principal term is at most a fixed multiple of

    delta integral exp(-c|t|^2)Pjet^p (|D|^3+J^2) dt.

This is finite independently of Lambda, since D,J are polynomials in t.
Tonelli applies to these nonnegative integrands. Gamma=0 has measure zero
under the joint Gaussian density. The absent-saddle value -infinity never
belongs to this band. C82 already includes degree drops and tangencies.
Combining the two terms proves (8). No independent-reference Gaussian has
been substituted for rho_r. QED.

## 4. Fixed-order dyadic summation removes the epsilon loss

For the raw window W_w={|X|,|zeta|<=w}, let E0 be the sup norm of the
difference of the raw pinned field and its cubic. C91/C101 Q16 give

    E0<=K0 N e,       e=rw^4,       K0=167/192.             (9)

**Lemma DB.** For w>=1 in the embedded-window range, rH<=1, and sufficiently
small e, the actual weighted decision error satisfies

    mu_r(E union Rsec, E0>=|mu|/2)
                          <=C[e+rH^4+H^3e^2].             (10)

**Proof.** Put a=2K0e, b_r=rH^4 and assume 0<a<=1/4. A decision error with
finite mu implies |mu|<=aN. The no-extra-saddle case mu=-infinity cannot
contribute. The innermost band |mu|<=a costs C(a+b_r) by JB with p=0.

Choose the nonnegative integer m for which 2^m a belongs to [1/4,1/2).
For j=0,...,m-1, consider

    2^j a<|mu|<=2^(j+1)a,       |mu|<=aN.

This forces N>2^j. Apply JB with the SINGLE fixed p=2 and fixed band width
delta=2^(j+1)a, which is <=1/2. Its contribution is at most

    2^(-2j) mu_r(N^2;|mu|<=2^(j+1)a)
                        <=C[2a 2^(-j)+b_r 4^(-j)].

The finite sums are bounded by 4a+(4/3)b_r. The remaining region
|mu|>2^m a>=1/4 forces N>1/(4a). Its mass is at most

    16a^2 mu_r(N^2)<=C H^3 a^2

by (7). This also covers large negative values of mu. Combining all regions
proves (10). The moment order and constants do not grow with r or m. QED.

An unweighted band bound plus arbitrary fixed moments of N would not prove
this: on U uniform in (0,1), let N=ceil(log_2(1/U)). All moments are finite
and P(U<=delta)=delta, but for e_m=2^(-m)/m,
P(U<=e_m N)>=2^(-m)=m e_m. JB's correlated weighted assertion is essential.
Similarly the finite-r floor rH^4 survives the entire dyadic summation.

## 5. Exponential-square control of the precise endpoint residual

This section strengthens the tail decay in C101 Q32; it does not change its
rare endpoint-scalar integration. Distinguish the raw cubic variable J in
section1 from the random field norm J_r below.

Let A_M=f_zz(M_r), the entire transverse Hessian block in dimension2.
The centered residual from P4.2 is

    g_r=f-E_Qr f-B_r(A_M-E_Qr A_M),    J_r=1+||g_r||_C4.    (11)

It is jointly independent of A_M; its internal Fourier coefficients are
not asserted independent. The regression coefficient and mean have uniformly
bounded C4 norm as stated in P4.2. C101 Q30 uses exactly this residual.

**Lemma ES.** There are epsilon_0>0 and C<infinity, uniform over the fixed
parameter family and sufficiently small r, such that

    E exp(epsilon_0 J_r^2)<=2,
    E[J_r^10;J_r>A]<=C exp(-epsilon_0 A^2/2), A>=1.         (12)

**Proof.** Express the original centered field in a standardized real Fourier
Gaussian basis as sum_n xi_n phi_n. Gaussian spectral decay gives

    S=sum_n ||phi_n||_C4 < infinity,

uniformly in rotated coordinate norms: derivatives of order at most4 in a
unit direction are bounded by a fixed multiple of (1+|2pi n/L|)^4. The real
sine/cosine multiplicities are included in S. After joint conditioning on
U_r and A_M, set eta_n=xi_n-E[xi_n|U_r,A_M]. Each eta_n is centered Gaussian
of variance at most1. This is the orthogonal Gaussian projection defining
(11). Covariance between distinct eta_n is retained.

For every integer n>=1, Minkowski applied to finite Fourier partial sums,
followed by their L^(2n)(C4) limit, gives

    ||J_r||_(2n)<=1+S sqrt(2n)<=C_* sqrt(2n), C_*=1+S.

Indeed a centered Gaussian of variance <=1 has even moment at most
(2n-1)!!<=(2n)^n. The same summable Fourier majorant makes the residual
partial sums C4-convergent in each of these spaces, so this limit is the
actual Gaussian regression residual. None of these estimates uses independence
between its Fourier coefficients or moments with uncontrolled order constants.

Using n!>=(n/e)^n and monotone convergence for the exponential series, choose
epsilon_0=1/(12 C_*^2). Since the numerical exponential base e<3, we have

    E exp(epsilon_0 J_r^2)
       <=1+sum_(n>=1) epsilon_0^n C_*^(2n)(2n)^n/n!
       <=sum_(n>=0) (1/2)^n=2.

Finally x^10 exp(-epsilon_0 x^2/2)<=(10/(epsilon_0 e))^5 for x>=0.
On J_r>A split the exponential into two halves to obtain

    J_r^10 1{J_r>A}
      <=(10/(epsilon_0 e))^5 exp(epsilon_0 J_r^2)
                              exp(-epsilon_0 A^2/2).

Taking expectation proves (12). QED.

**Lemma FT.** For Lambda>=1 and all sufficiently small r,

    nu_r^F(D_Lambda^c)<=C exp(-c Lambda)+Cr,
    nu_0^F(D_Lambda^c)<=C exp(-c Lambda).                  (13)

**Proof for the actual measure.** C101 Q30–Q31 are the retained analytic
interfaces. Let l_end=-f_zz(M_r)>0 on the typed support. The cap-failure
decomposition from P7.5 has a near branch
0<l_end<=4Dcap rJ_r^2, a far branch l_end>1/(4Dcap r), and the fourth-
derivative exception. On near, |lambda|<=C_0 J_r^2, and

    W_r<=C r^2 J_r^4 l_end(l_end+C rJ_r^2).

Independence of the endpoint residual from this scalar and its bounded scalar
density give, keeping the SAME residual tail indicator within the integral,

    E_Qr[W_r;near,J_r>A]
      <=C r^2 E[J_r^4 1{J_r>A}
             integral_0^(4Dcap rJ_r^2) l(l+C rJ_r^2)dl]
      <=C r^5 E[J_r^10;J_r>A].                            (14)

F_r is bounded by cap failure, not declared independent of these variables.
If Lambda>=C_0, set A=(Lambda/C_0)^(1/2). On near and D_Lambda^c this
residual event holds. Lemma ES followed by the single full floor Z_r>=c r^2
and the r^(-3) scaling in (1) yields C exp(-c Lambda). If 1<=Lambda<C_0,
use (14) without an indicator and enlarge the constant by a finite factor.
P7.6–7.7 give Q_r^W mass O(r^4) for the far/derivative branches, hence scaled
mass O(r). This proves the first line, independently of rH<=1.

For the model, C101 Q33 gives on Rsec

    0<lambda<=C Pjet^2,
    integral w_lambda 1_Rsec d lambda<=C Pjet^6.

Its joint Gaussian slice has the uniform envelope C exp(-c|t|^2). Therefore
the tail integral is bounded by

    C integral Pjet^6 exp(-c|t|^2)1{Pjet^2>Lambda/C}dt
                                <=C' exp(-c' Lambda).

For large Lambda the indicated event implies |t|^2>=c_1 Lambda; absorb the
polynomial with half the Gaussian exponential. For bounded Lambda enlarge
C'. The full z_0 floor is retained. This exhausts only the failure-marked
measure; the unmarked soft measure has mass of order Lambda^3. QED.

## 6. The unchanged geometry and the new error ledger

Use C101's radius, elder value-margin, typing and Hessian estimates, and A4's
local endpoint certificate for the rejected chord. A4 LE retains both the
strict saddle clearance and the endpoint above the birth level. Its condition
eta_LE=2(115/48)rw^2 and B-prime give endpoint loss
C[H^3 rw^2+rH^4 sqrt(rw^2)]. These are actual weighted sufficient events.

C95/C96 identify the elder good event with actual H_r. C98's coverage puts
every typed nonneutral jet in E or Rsec. Finite-r T^c is not null and is
included with its entire CrH^4 loss. With the new decision Lemma DB replacing
C101 Q23/A4's unweighted-band split, the full scaled layer error is

    R_*(r,H,w) = w^(-8)+rH^3w^(-4)
       +H^4e+rH^5 sqrt(e)
       +H^3rw^2+rH^4 sqrt(rw^2)
       +e+rH^4+H^3e^2
       +H^5r^2w^4+H^7r^2w^2,         e=rw^4.              (15)

Specifically, these terms come respectively from C101 Q17 (radius), Q19
(elder value margin), A4 B-prime (rejected endpoint), JB/DB plus Q12
(decision level and typing), and Q25 (rescaled Hessian errors).

The event union and the normalized raw-jet density comparison in C101
Q28–Q29 now give

    r^(-3) Q_r^W(D_Lambda,H_r symmetric_difference E)<=C R_*,
    ||nu_r^F|D_Lambda-nu_0^F|D_Lambda||_var<=C R_*.         (16)

For the second inequality take any measurable |phi(theta)|<=1, replace the
actual failure indicator by 1_Rsec and pay the first bound, plus off-type
CrH^4. Then use (7) on that same fixed jet event. This also explains why
(16) applies to raw-jet/Boolean measures and does not assert anything about
moving real-valued marks.

The uniform constants hold when

    r<=r_0, Lambda>=1, rH<=1, w>=5, 2rw<=L/4,
    e<=1, 2K0e<=1/4, C_V H^2e<=1,
    C_eta rw^2<=1, eta_LE<=1.                              (17)

C_V and C_eta are the fixed constants of C101. The obsolete C_H H^3e
condition is not needed after A4, but would also hold for our choices below.
No growing-Lambda substitution into an unspecified fixed-cutoff constant
has been used.

## 7. Fixed-layer and full-measure rates

For fixed Lambda, take w=r^(-1/12). Then e=r^(2/3). Every term of (15)
is O_Lambda(r^(2/3)): their r-exponents in displayed order are

    2/3, 4/3, 2/3, 4/3, 5/6, 17/12,
    2/3, 1, 4/3, 5/3, 11/6.

All cutoffs (17) hold for sufficiently small r. Multiply the first bound
of (16) by r^3 to obtain (4). In particular both sector mismatches have
the exact endpoint exponent 11/3, with no epsilon loss on a fixed layer.

For full exhaustion choose D_*>0 large enough that both exponential tails
in (13), at Lambda=D_* log(1/r), are O(r). Increase D_* to at least1.
Set

    Lambda=D_* log(1/r), H=1+Lambda,
    w=(rH^4)^(-1/12)=r^(-1/12)H^(-1/3),
    e=r^(2/3)H^(-4/3).                                   (18)

For r small enough w>=5 and every condition (17) holds. In particular
rH->0, rw->0, e->0, H^2e->0 and rw^2->0. Powers of log do not defeat any
of these positive powers of r. Each term in (15) is as follows:

| term | after (18) |
|---|---|
| w^(-8) | r^(2/3)H^(8/3) |
| rH^3w^(-4) | r^(4/3)H^(13/3) |
| H^4e | r^(2/3)H^(8/3) |
| rH^5 sqrt(e) | r^(4/3)H^(13/3) |
| H^3rw^2 | r^(5/6)H^(7/3) |
| rH^4 sqrt(rw^2) | r^(17/12)H^(11/3) |
| e | r^(2/3)H^(-4/3) |
| rH^4 | rH^4 |
| H^3e^2 | r^(4/3)H^(1/3) |
| H^5r^2w^4 | r^(5/3)H^(11/3) |
| H^7r^2w^2 | r^(11/6)H^(19/3) |

All rows are O(r^(2/3)H^(8/3)); rows with a strictly larger r power have
ratio tending to zero, even when their H power is larger. For r<=exp(-1),
H<=(1+D_*)log(1/r). Splitting each finite measure into D_Lambda and its
complement, using (13),(16), proves the first assertion of (3).

Taking total masses gives |r^(-3)(1-p_r)-M_F| bounded by that variation
norm. Multiplication by r^3 gives the second assertion. Since M_F>=M_*>0,
the actual total mass is >=M_*/2 for small r. The elementary inequality

    ||nu/m-nu0/m0||_var
       <= ||nu-nu0||_var/m + |m-m0|/m
       <= 4 ||nu-nu0||_var/M_*

gives the stated rate for the conditional raw-jet laws. QED.

This argument supplies an endpoint power with an explicit logarithmic loss;
it does not prove an O(r^(2/3)) global rate or an optimality statement.
The logarithm comes from exhausting the failure measure while balancing
the radius tail w^(-8) against the elder value-margin term H^4rw^4.

## 8. Evidence boundaries and completion effect

The proof's new analytic obligations are JB, DB, ES and FT. Equations (15)–(18)
then compose them with the stated geometric and regression sources. The
separate controls.py checks exact exponent algebra, fixed-order summation,
normalization powers and countermodels. Passing those checks is not a proof
of Gaussian conditioning, global path topology or an unproved source lemma.

The change removes A4's arbitrarily small exponent loss for fixed-layer
sector errors, and replaces its family of beta<2/3 full-measure bounds by
the explicit endpoint logarithmic rate (3). It preserves the failure measure,
its alpha_1+alpha_2 coefficient, the full pair-Palm normalizer and the actual
finite-H0 selection event. It closes no other dependency merely by proximity.

In particular no mathematical-completion certificate with zero open nodes
is warranted by this packet. The distinction between a selected pair's
failure law and a once-counted small-persistence-bar intensity remains.
