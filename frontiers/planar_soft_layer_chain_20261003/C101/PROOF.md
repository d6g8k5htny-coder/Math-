# Quantitative exhaustion of the actual planar elder-failure measure

Object: C101-PLANAR-K1-QUANTITATIVE-FAILURE-EXHAUSTION-20261003-v1.
Author/executor: OpenAI / Codex root01a0adb2, for Dylan Roy under delegation.
Author-side analytic contributor: OpenAI / Codex /root/c93_edge_integral_audit.
It checked the cutoff-uniform Gaussian, determinant, strip and tail estimates
below, with earlier C93/C99 exposure. It is not a nonauthor reviewer.
Root01a0bbb5 coordinates custody under R17 claim
5c1dc0ee-7ca9-4a65-8016-d41b59d8f6b2, native pickup5966810414.
Both authors are excluded from a subsequent nonauthor acceptance vote.
Exact model variant/build UNKNOWN. Personal reading PENDING; human review
NONE; organizational independence 0; scientific effect NONE.
Disposition: AUTHOR-SIDE FROZEN CANDIDATE; fresh full review requested.

This is a quantitative extension of ELDER's actual failure-measure exhaustion,
not a new count theorem. The parameter k is exactly 1. The proof tracks growing
soft-coordinate cutoffs from Gaussian and deterministic formulas rather than
substituting a growing cutoff into C92–C98's fixed-cutoff theorems.

## 0. Population, imported interfaces, and statement

Fix L>0, a nonempty compact birth set B0, and all orthonormal planar frames.
The field is centered with variance one on X=R^2/(L Z^2), with covariance

    K_L(z)=sum_{n in Z^2} exp(-|z+Ln|^2/2)
           / sum_{n in Z^2} exp(-|Ln|^2/2).

Use continuous Gaussian regression Q_r at the exact pins
M_r=(-r/2,0), S_r=(r/2,0), f(M_r)=b, f(S_r)=b-r^3, and zero gradients.
Coordinates and derivatives are in the chosen frame. Set

    W_r=|det H_M det H_S| 1{H_M<0, index H_S=1},
    Z_r=E_Qr W_r, Q_r^W=(W_r/Z_r)Q_r,
    z_r=Z_r/r^2, z_0=36 E[A^2 1{A<0}|U_0=v_0],
    A=f_zz(0), lambda=-A/r,
    t=(gamma,B1,C3)=(f_xxz(0),f_xzz(0),f_zzz(0)),
    theta=(lambda,t), Pjet=1+|gamma|+|B1|+|C3|,
    N=1+max_{|alpha|<=4} sup_X |D^alpha f|.

The index counts strictly negative eigenvalues. W_r vanishes on singular
endpoints. Let H_r be the Borel event that the finite ordinary-superlevel H0
bar born at M_r dies at S_r, using C96's closed-manifold, global older-point
maximin convention. Define it false off the Morse/distinct-value locus.
The essential class is NOT a finite selected bar and thus is a failure.
Let F_r=H_r^c and p_r=Q_r^W(H_r). Source P §8 and C96 identify this event,
not a local adjacency proxy, Q_r^W-almost surely for each parameter and r.

Write

    a_M=24lambda-gamma^2+12B1, a_S=24lambda+gamma^2-12B1,
    T={a_M>0,a_S>0},
    w_lambda=(6lambda+3B1-gamma^2/4)_+
              (6lambda-3B1+gamma^2/4)_+.

Thus w_lambda=a_M a_S/16 on T and zero elsewhere. Let rho_0(a,t) be the JOINT
density of (A,t) under the contact conditioning
U_0=(f,f_x,f_xx,f_xxx,f_z,f_xz)(0)=v_0=(b,0,0,12,0,0).
It includes the A-marginal density at zero.

On T with gamma!=0 define

    D=gamma^2-12B1, J=8gamma^3-144B1 gamma+576C3,
    psi=24lambda/gamma^2, c=D/gamma^2, R=J/gamma^3,
    u=X+gamma zeta/12, Z=gamma zeta,
    P_QS(u,Z)=2u^3-3u/2-1/2-(psi+2cu)Z^2/48+RZ^3/3456.       (Q1)

Let mu be the highest value P_QS(Y)+1 of its extra nondegenerate saddles,
or -infinity if there is none. C82/C98 give finite algebraic branches and
a Borel definition, including absent, degree-drop and tangency cases.
Put E={T,gamma!=0,mu<0}, Rsec={T,gamma!=0,mu>0}. Extend the model failure
density by zero off Rsec:

    dnu_0^F(theta)=z_0^(-1) rho_0(0,t) w_lambda 1_Rsec dtheta,
    nu_r^F(B)=r^(-3) Q_r^W(theta in B,F_r).                    (Q2)

For finite signed measures use the variation norm
sup_{|phi|<=1}|integral phi d(nu-nu')|, without a factor 1/2.

The retained inputs are P with congruence erratum E1, Section9 replacement E2
v1.1, wording reconciliation REC, and the embedded-chart restriction
r<L/(4 sqrt(2)); C91's pinned C4 Taylor formulas; C92's nonsingular actual
ten-observation regression, filtered determinants and FULL normalizer; C93's
typing-edge substitutions and raw-to-rescaled Hessian formula; C94's actual
weighted saddle-level estimate using C82; corrected geometric G in C95;
C96's maximin/H0 interface; C97's TWO-margin rejected chord; C98's sector
coverage/null polynomial; ELDER's actual good-cap implication and endpoint
residual integration; and CUB's nonempty coefficient integral. Their source
hypotheses remain in force. Exact identities and consumed sections are in §9.

**Theorem QFE.** Uniformly over the fixed b/frame parameters, for all
sufficiently small r,

    ||nu_r^F-nu_0^F||_var <= C r^(1/4),
    1-p_r=r^3(alpha_1+alpha_2)+O(r^(13/4)).                   (Q3)

More generally, for each fixed beta with 0<beta<1/2 there are C_beta<infinity
and r_beta>0, uniform over those same parameters, such that

    ||nu_r^F-nu_0^F||_var <= C_beta r^beta,
    1-p_r=r^3(alpha_1+alpha_2)+O_beta(r^(3+beta)).             (Q4)

Here alpha_j are exactly CUB G11 at k=1, NOT new or numerically evaluated
coefficients. Their sum is uniformly positive and finite on the fixed
parameter family. No uniformity in beta,L or a growing birth/gap set is claimed.
The cutoff r_beta and constants are analytic/existential, not error bars.
This theorem does not include beta=1/2.

The conclusion concerns the actual selector-failure measure under the original
pair-Palm weight W_r/Z_r, and its raw midpoint jets. It does not count
replacement bars once, give total variation for real height/location marks,
or refine an all-bars lifetime density. The intermediate/small-gap,
shrinking multiple-witness and Conjecture7 lanes are not consumed or discharged.

## 1. Uniform base constants, independent of the soft cutoff

Let Lambda>=1, H=1+Lambda, D_Lambda={|lambda|<=Lambda}. Throughout §§1–5 impose

    0<r<=r_0, rH<=1.                                         (Q5)

The common r_0 is chosen from the fixed field/parameter family, before Lambda.
We explain its construction rather than assuming polynomial dependence of
unspecified C_Lambda constants.

Use the centered observations in C92:

    U_r=((f(M)+f(S))/2, (f(S)-f(M))/r,
         (f_x(S)-f_x(M))/r,
         (6/r^2)[f_x(M)+f_x(S)-2(f(S)-f(M))/r],
         (f_z(M)+f_z(S))/2, (f_z(S)-f_z(M))/r),

whose target is v_r=(b-r^3/2,-r^2,0,12,0,0). Append A,t to obtain V_r.
At contact the ten entries are the ten distinct derivatives through order3.
The positive Fourier coefficients are
a_n=exp(-2 pi^2|n|^2/L^2)/sum_k exp(-2 pi^2|k|^2/L^2).
A nonzero combination of these jets has a nonzero polynomial Fourier
multiplier of degree<=3. It cannot vanish on all lattice points. In fact the
finite cube |n|_infinity<=3 suffices: repeated one-variable polynomial
uniqueness on its seven coordinate values proves the multiplier is zero only
when every coefficient is zero. Frame rotations are invertible on these
polynomials. The finite weighted Gram matrix therefore has positive minimum
eigenvalue in each frame. By continuity on compact O(2), its minimum
epsilon_0>0 is uniform. This constructs a finite positive lower bound without
sampling covariances.

For finite j let S_j=sum_n sqrt(a_n)(1+|2 pi n/L|)^j.
These sums are finite. They bound all covariance derivatives and regression
coefficient functions needed below. For a concrete constant construction set
rbar=min(1,L/(8 sqrt(2))) and
C_G=5 max_{i,j,frame,|s|<=rbar}|d^2 Gamma_s(i,j)/ds^2|.
The centered observation functions are even in s, with their integral Taylor
extensions at0. Differentiated covariance series (for example the finite
S_12 majorant) make this maximum finite. Taylor's integral formula and the
dimension10 matrix norm bound give ||Gamma_r-Gamma_0||<=C_G r^2.
Choose r_0<=min(rbar,sqrt(epsilon_0/(2C_G+1))) and include the source
normalizer/cap/chart cutoffs in its minimum.
The full covariance eigenvalues are then between epsilon_0/2 and a fixed M_0.
Schur-complement minimization supplies the same positive lower bound for
the conditional (A,t) covariance. Covariance inverses, means and their
r^2 differences are uniformly bounded. This is a concrete construction of
base constants from a finite Gram minimum, spectral sums and a compact
parameter maximum, not a claim that their values have been computed.

Let rho_r(a,t) be the actual joint density conditional on U_r=v_r.
On (Q5), a=-r lambda belongs to [-1,1]. Differentiating a Gaussian density
along the mean/covariance interpolation, and then in a, gives constants c,C>0
independent of Lambda such that

    rho_r(-r lambda,t)<=C exp(-c|t|^2),
    |rho_r(-r lambda,t)-rho_0(0,t)|
       <=Cr(1+|lambda|) Pjet^2 exp(-c|t|^2).                (Q6)

Indeed the mean/covariance changes give Cr^2 Pjet^2 exp(-c|t|^2); the a shift
gives Cr|lambda| Pjet exp(-c|t|^2), with intermediate a in [-1,1].
Shrinking c absorbs fixed polynomial changes in the exponent.
More explicitly set sigma_*=epsilon_0/2 and let mu_* bound the conditional
four-vector mean, constructed from M_0, 2/epsilon_0 and sup|v_r|. One valid
Gaussian envelope is c=1/(4M_0) with prefactor
(2pi sigma_*)^(-2) exp(mu_*^2/(2M_0)). Along the covariance interpolation,
the log-density derivative is bounded by the inverse-covariance norm times
the mean derivative and by its square times the covariance derivative,
multiplied by 1+|(a,t)|^2. Along the scalar shift its derivative is bounded
by sigma_*^(-1)(|(a,t)|+mu_*). These formulas construct the constant in (Q6)
from the fixed base bounds; no dependence on H is hidden in it.

Conditional on the actual V_r target, the field's regression mean has C4 norm
at most C(1+r|lambda|+|t|)<=CPjet. For each standardized real Fourier
coefficient, its conditional residual variance is at most one. Minkowski
and S_4 bound its residual C4 norm in every fixed L^p, p>=1, uniformly in r,
frame and target. Residual coefficients need not be independent of each
other. The summable Fourier majorant also justifies the conditional infinite
sum. Hence, including p<1 by Jensen,

    E[N^p|lambda,t]<=C_p Pjet^p, p>=0 fixed.                (Q7)

No unconditional moment is substituted for this conditional statement.
No field/remainder independence from t is asserted.

C92 J4 and its section4 full-normalizer argument, consuming the full P
normalizer rather than a soft-layer
normalizer, gives

    |z_r-z_0|<=Cr, z_*/2<=z_r<=2z^*, 0<z_*<=z_0<=z^*.      (Q8)

These constants have no Lambda dependence. The fixed compact parameter
family and continuous contact regression give the stated uniform floor.
The O(r) bound is the filtered determinant expansion under the full
conditioning; a growing soft cutoff is not used in that expansion.

## 2. Determinants, actual weighted moments and jet comparison

Write D_r=W_r/r^4. The raw cubic in C91/C92 is

    G=2X^3-3X/2-1/2+(gamma/2)(X^2-1/4)zeta
        -(lambda/2)zeta^2+(B1/2)X zeta^2+(C3/6)zeta^3.

Its endpoint Hessians are

    L_M=[[-6,-gamma/2],[-gamma/2,-lambda-B1/2]],
    L_S=[[ 6, gamma/2],[ gamma/2,-lambda+B1/2]].

C91's mixed-derivative bound at w=1 gives
||H_i/r-L_i||_op <=(115/24)rN.
For a symmetric matrix put F_j(B)=|det B|1{index B=j}.
These filtered determinants are continuous across every typing boundary and
satisfy |F_j(B)-F_j(C)|<=2 max(||B||,||C||)||B-C|| in dimension2:
within one index chamber use determinant differentiation; a segment changing
index meets a singular matrix, where the determinant is zero.
The product comparison therefore gives

    |D_r-w_lambda|<=CrN(H+Pjet+rN)^3.                       (Q9)

Multiply by N^p BEFORE conditional expectation. Expanding the cube and using
(Q7), r<=1, H>=1, yields

    E[|D_r-w_lambda| N^p|theta]<=C_p rH^3 Pjet^(p+4),
    E[D_r N^p|theta]<=C_p w_lambda Pjet^p
                         +C_p rH^3 Pjet^(p+4).            (Q10)

This argument retains dependence of the determinant and N.
The exact jet density of the measure
mu_r(Phi)=r^(-5)E_Qr[W_r Phi 1_DLambda] is

    g_r(theta)=rho_r(-r lambda,t) E[D_r|theta].             (Q11)

The one factor r here is dA=r d lambda and W_r=r^4D_r. Thus
Q_r^W(Phi 1_DLambda)=r^3 mu_r(Phi)/z_r, for field-dependent Phi as well.
There is no omitted pin-density factor, factor12, or second area normalization.

The two unclipped affine factors defining w_lambda sum to 12lambda. If the
positive-part product is nonzero, both factors are positive; their sum is then
12lambda. This is impossible when lambda<=0, and AM–GM bounds the product by
36lambda^2 when lambda>0.
Integrating (Q10),(Q6) over a lambda interval of length2Lambda gives, for fixed p,q,

    mu_r(N^p Pjet^q)<=C_(p,q)(H^3+rH^4)<=C_(p,q)H^3,
    integral_DLambda Pjet^q |g_r-g_0|<=C_q rH^4,
    integral_DLambda Pjet^q |g_r/z_r-g_0/z_0|<=C_q rH^4,
    mu_r(D_Lambda intersect T^c)<=CrH^4.                   (Q12)

Here g_0=rho_0(0,t)w_lambda. The determinant error contributes
CrH^3(2Lambda); the density error contributes
Cr integral_0^Lambda (1+lambda)lambda^2 d lambda.
The last normalized comparison also uses
|1/z_r-1/z_0|<=Cr and integral Pjet^q g_0<=C_qH^3.
The last line concerns finite-r typing leakage, not a null boundary.
Unmarked mu_0 has mass of order Lambda^3 and cannot be exhausted globally
as a finite measure. Only the failure-marked measures in (Q2) will be exhausted.

## 3. Uniform strip and truncated inverse formulas

For i=M or S change B1 to s=a_i. Respectively

    B1=(s-24lambda+gamma^2)/12,
    B1=(24lambda+gamma^2-s)/12.

In both cases |dB1/ds|=1/12, T means 0<lambda<=Lambda, 0<s<48lambda,
and w_lambda=s(48lambda-s)/16. After multiplying by N^pPjet^q, (Q10)
and polynomial Gaussian absorption bound the joint integrand by

    C exp(-c|t|^2)[w_lambda Pjet^(p+q)
                                  +rH^3 Pjet^(p+q+4)].

To integrate s, bound the B1 polynomial times its Gaussian uniformly in B1,
while retaining Gaussian decay in gamma,C3. Then integrate lambda over length
at most Lambda. For every nonnegative measurable phi,

    mu_r(N^pPjet^q 1_T phi(a_i))
       <=C_(p,q) integral_0^(48Lambda)
                        phi(s)[H^2 s+rH^4] ds.             (Q13)

For p=0 the jet-only model version omits the r term; no model field norm N
is defined or compared. This proves, for 0<delta<=1, either edge
(and their union by addition),

    mu_r(N^pPjet^q;T,min(a_M,a_S)<=delta)
                    <=C_(p,q)(H^2 delta^2+rH^4 delta).     (Q14)

For powers v>0 the away integral is exactly bounded by

    C_(p,q) integral_delta^(48Lambda)
                           [H^2 s^(1-v)+rH^4 s^(-v)] ds. (Q15)

For v=3 it is at most C[H^2/delta+rH^4/(2delta^2)];
for v=4 at most C[H^2/(2delta^2)+rH^4/(3delta^3)];
for v=6 at most C[H^2/(4delta^4)+rH^4/(5delta^5)].
Dropping the positive upper-end terms only enlarges these bounds.
There is no untruncated inverse moment of order>=2 in the model estimate.
The rH^4 delta strip correction cannot be discarded at finite r.

## 4. Local geometry errors with explicit H dependence

Let w>=5, 2rw<=L/4 and e=rw^4. C91 gives, with every mixed derivative included,

    E0=sup_{|X|,|zeta|<=w}|(f(rX,r zeta)-b)/r^3-G|
                               <=K0 N e, K0=167/192.      (Q16)

The gradient and Hessian raw constants are K1=635/384, K2=115/48.
We now rederive the H dependence of each consumer of this estimate.

### 4.1. Selected-box and rejected-chord radii

The explicit raw radius bounds from C94/C95 and C97 are

    Rbox=3/2+(5/2)(|gamma|+12)/sqrt(24lambda),
    Rch=5/2+3(|gamma|+12)/sqrt(24lambda).

If either exceeds its constant offset plus rho, then
lambda<Hgamma/rho^2, Hgamma=(3/8)(|gamma|+12)^2.
In (Q13)'s underlying two-variable integral set
U=min(Lambda,Hgamma/rho^2). Before the Jacobian1/12, direct integration gives

    integral_0^U integral_0^(48lambda) w_lambda ds d lambda=288 U^4,
    integral_0^U integral_0^(48lambda) 1 ds d lambda=24 U^2.

Retain Gaussian decay in gamma,C3 and integrate its polynomial Hgamma powers.
For fixed p,q,

    mu_r(N^pPjet^q;T,Rbox>w or Rch>w)
                         <=C_(p,q)(w^-8+rH^3 w^-4).       (Q17)

We used w-5/2>=w/2. The finite-r term is rH^3 w^-4, not merely r w^-4.

### 4.2. Selected local value margin

On E, C98's coverage supplies the extra inequalities of C94's elder sector.
Its retained local constants are
tau_i=2/(3sqrt(3))+|c|/(24sqrt(3)kappa_i)+|R|/(3456 kappa_i^(3/2)),
kappa_M=(psi-c)/48, kappa_S=(psi+c)/48,
m_S=2/(125tau_S^2), e_M=min(1/(8tau_M^2),1),
v=min(m_S,e_M), eta=(1/2)min(v,-mu).
The C94/A1 calculation gives

    v>=c_* a_S^2, c_*=3/[250(48Lambda)^2].                 (Q18)

There is no assertion of this inequality off that elder sector.
If E0>=v/2, then epsilon_V N/a_S^2>=1 with
epsilon_V=2K0e/c_* <=C_V H^2 e,
C_V=500K0*48^2/3.
Split at delta=sqrt(epsilon_V)<=1 and use squared Markov and (Q15), v=4.
Together with the near strip,

    mu_r(E,E0>=v/2)<=C[H^2 epsilon_V+rH^4 sqrt(epsilon_V)]
                         <=C[H^4e+rH^5 sqrt(e)].          (Q19)

### 4.3. Rejected endpoint margin, distinct from the saddle clearance

For the highest extra saddle Y in Rsec, put h=-P_QS(Y)=1-mu.
The cubic expansion at M gives
P_QS(M+v)=-rho^2+T3(v), |T3(v)|<=tau_M rho^3.
Euler's identity at a critical Y!=M gives T3(v)=2rho^2/3, hence

    h=rho^2/3>0, rho>=2/(3tau_M), h>=4/(27tau_M^2).

Thus 0<mu<1. In raw jets C97's exact pole cancellation is

    tau_M=(1/sqrt(3))[2/3+2|D|/a_M+|J|/(6 a_M^(3/2))].
    tau_M^2 <=Ctau Pjet^6/a_M^3,
    Ctau=(4/9)(48Lambda)^3+676(48Lambda)+728^2/36,
    h>=c_h a_M^3/Pjet^6, c_h=4/(27Ctau).                    (Q20)

Here |D|<=13Pjet^2, |J|<=728Pjet^3. Define
C_T=(4/9)48^3+676*48+728^2/36, so Ctau<=C_T H^3.
The chord K=[M,2Y-M] has
P_QS(M+t(Y-M))=h(2t^3-3t^2), 0<=t<=2:
its minimum is -h and its endpoint value is 4h.
Both margins mu and 4h are required.

For E0>=2h, epsilon_H N Pjet^6/a_M^3>=1, where
epsilon_H=K0e/(2c_h)<=C_H H^3e, C_H=27K0 C_T/8.
Split at delta=epsilon_H^(1/3)<=1, square the Markov bound,
and use (Q15), v=6, with p=2,q=12. This yields

    mu_r(Rsec,E0>=2h)<=C[H^2 epsilon_H^(2/3)+rH^4 epsilon_H^(1/3)]
                             <=C[H^4 e^(2/3)+rH^5 e^(1/3)]. (Q21)

All random tolerances are handled under the joint actual weighted measure.
An endpoint-only criterion or a variable-width enclosure is not being used.

### 4.4. The decision level mu near zero

C82's direct saddle-level integral, consumed in C94 C11, has a constant
independent of Lambda. At fixed t, d lambda=(gamma^2/24)d psi, and

    w_lambda d lambda=(gamma^6/384)(psi^2-c^2)d psi.

For 0<delta<=1/2, C82 LB bounds the inner saddle band by
delta[(1024/3)|c|^3+64R^2], including the finite-branch factor.
Multiplication cancels the chart poles:
gamma^6|c|^3=|D|^3 and gamma^6R^2=J^2.
Extending the nonnegative lambda integral beyond Lambda is legitimate.
The contact Gaussian slice absorbs these polynomials without reference
independence. Thus

    mu_0(T,|mu|<=delta)<=C delta,
    mu_r(T,|mu|<=delta)<=C(delta+rH^4).                      (Q22)

The second line uses the actual joint-density error (Q12), not an independent
model Gaussian. The no-saddle value -infinity is not in this band.
For 0<d<=1/4, the union of {|mu|<=2d} and {E0>=d} gives, by (Q12),(Q16),

    mu_r(E or Rsec,E0>=|mu|/2)
                       <=C[d+rH^4+H^3(e/d)^2].             (Q23)

The exponent 2 is fixed; it does not grow with r.

### 4.5. Actual raw-to-rescaled Hessian losses

Use the rescaled QS Hessian norm in C93 E13, and tau_M^(tol)=1,
tau_S^(tol)=2/5, distinguished from the local cubic tau_i above.
The coordinate-change estimate is

    H_i(r,w) <=(115/72)Nrw^2 L_i,
    L_i=1+(gamma^2+144)/a_i <=C H Pjet^2/a_i on T.          (Q24)

There is no standalone gamma pole. Let
epsilon_i=(115/72)rw^2/tau_i^(tol), so epsilon_i<=C_eta rw^2,
C_eta=575/144. Split at a_i=epsilon_i<=1. On its complement use
third Markov with (Q24), then (Q15), v=3, p=3,q=6.
The strip and away terms give

    mu_r(T,H_i>=tau_i^(tol))
                <=C[H^5 epsilon_i^2+rH^7 epsilon_i]
                <=C[H^5 r^2w^4+H^7 r^2w^2].               (Q25)

All norms and N moments were multiplied before conditioning.
The gamma=0 chart is excluded a.e., not assigned a pointwise transfer formula.

The common admissibility conditions for these calculations are

    r<=r_0, Lambda>=1, rH<=1, w>=5, 2rw<=L/4, e<=1,
    C_V H^2 e<=1, C_H H^3 e<=1, C_eta rw^2<=1, 0<d<=1/4.   (Q26)

Their constants are independent of Lambda: C_V,C_H,C_eta are displayed
numbers; r_0 is the fixed base cutoff of §1. No unknown compact-sector
constant is being presumed polynomial.

## 5. Actual event comparison on the growing layer

C98 proves on T that mu<0 supplies C94's selected-sector inequalities,
including the absent-saddle and exceptional branches. The remaining neutral
boundary is contained in the raw polynomial

    J^2-16(24lambda-2D)^2(24lambda+D)=0,

which is nonzero as a polynomial in C3 (leading coefficient 576^2).
It and gamma=0 are Lebesgue-null in raw jets. The nonsingular actual jet
density and model Gaussian density give them zero weight for each r.
This is not an estimate for neighborhoods of the boundary; (Q22) supplies that.

On E, when Rbox<=w, E0<eta, H_M(r,w)<1, H_S(r,w)<2/5,
the corrected geometric G consumed by C95 gives the actual global maximin
level f(S_r). Its premises include the QS/CUB local polynomial hypotheses,
the corrected vertical-cut/Box geometry, fixed exact pins and an embedded
controlled patch. C95 lifts every torus path from the fixed starting lift
to the globally continuous periodic field in the plane. The compact trap's
first exit forces the upper maximin bound, even for winding paths. The
controlled axial segment supplies the reverse bound and an older endpoint.
No global C2 closeness or additional stable-cut Proposition8 is consumed.
C96 then identifies
the finite ordinary-superlevel H0 event H_r. We retain that deterministic
interface with its exact premises; neither genericity nor path connectivity
is inferred from Gaussian tests.

On Rsec, the Borel highest extra saddle gives a chord with Rch<=w.
If E0<(1/2)min(mu,4h), it is a path strictly above f(S_r) to a point
strictly above b; therefore the actual maximin is larger than f(S_r)
and H_r fails. The estimates (Q20)–(Q23) retain BOTH margins.
These are sufficient events, not an assertion that every rejected pair
has the same local continued saddle at finite r.

Take the union of the complementary bad events. The entire fixed layer
is exhausted by E, Rsec, the two null sets and finite-r T^c leakage. Define

    Rerr(r,H,w,d)=
      w^-8+rH^3w^-4
      +H^4e+rH^5sqrt(e)
      +H^4e^(2/3)+rH^5e^(1/3)
      +d+rH^4+H^3(e/d)^2
      +H^5r^2w^4+H^7r^2w^2, e=rw^4.                       (Q27)

Equations (Q12),(Q17),(Q19),(Q21),(Q23),(Q25) imply

    r^-3 Q_r^W(D_Lambda, H_r symmetric_difference E)
                                  <=C Rerr(r,H,w,d).       (Q28)

The constant is independent of Lambda,w,d,r on (Q26). Full normalization
uses (Q8), once. The definitions on null/non-typed sets are those in §0.

For |phi(theta)|<=1, replace 1_F_r by 1_Rsec on D_Lambda. On T outside the
null sets, F_r symmetric_difference Rsec equals H_r symmetric_difference E.
Off T these complements need not agree, so also add the entire actual T^c
leakage from (Q12). The replacement error is therefore at most the left side
of (Q28) plus CrH^4, already covered by Rerr.
Then use the normalized joint-density comparison
(Q12) on that same fixed raw-jet event Rsec. Uniformity in phi gives

    ||nu_r^F|D_Lambda-nu_0^F|D_Lambda||_var <=C Rerr.        (Q29)

This is a raw-jet/Boolean comparison. A transported real-valued death or
location mark is not silently substituted for phi(theta).

## 6. Quantitative ACTUAL and model failure tails

### 6.1. Actual failure, retaining the endpoint scalar and full W_r

The endpoint depth l_end=-f_zz(M_r)>0 on typed support is NOT lambda.
Source P §4.2 regresses the whole field on this scalar and gives
an independent residual g_r. Write J_r=1+||g_r||_C4.
All its fixed finite moments are bounded uniformly; the endpoint scalar has
a bounded density. Its bounded regression mean/coefficient gives

    ||f||_C4<=C(J_r+l_end).

ELDER S4, consuming P §8's global older-path implication, gives
F_r subset G_cap,r^c up to Q_r^W-null sets, including essential maxima.
P §7.5 splits depth failure into
near: 0<l_end<=4Dcap rJ_r^2, and far: l_end>1/(4Dcap r).
Together with the fourth-derivative exception these cover cap failure.
On near, N and the third-derivative bound are at most C J_r^2, and

    W_r<=Cr^2J_r^4 l_end(l_end+CrJ_r^2).

For any A>=1 keep the indicator J_r>A inside this SAME scalar integration:

    E_Qr[W_r;near,J_r>A]
      <=Cr^2 E[J_r^4 1_{J_r>A}
          integral_0^(4Dcap rJ_r^2)
                    l(l+CrJ_r^2) dl]
      <=Cr^5 E[J_r^10;J_r>A].                              (Q30)

Only the proved independence of this endpoint residual and its scalar is used.
F_r need not be independent of either. We bounded it by cap failure, not by
an unconditional field-tail probability.

On near the mean-value derivative bound between M_r and 0 gives

    |lambda|<=l_end/r+(1/2)sup|f_xzz|<=CJ_r^2,
    |t|<=CJ_r^2.                                           (Q31)

Thus |lambda|>Lambda implies J_r>(Lambda/C)^(1/2).
For each fixed integer m>=1, (Q30), the full floor Z_r>=c r^2, and
E[J_r^(10+2m)]<C_m give a near scaled tail <=C_m Lambda^-m.
If Lambda is below the fixed constant C in (Q31), enlarge C_m and use the
unrestricted near-branch bound from (Q30); the threshold A>=1 is then not
silently assumed. This covers every Lambda>=1.
P §7.6 and §7.7 give tilted mass O(r^4) for the far and derivative branches;
their SCALED mass is O(r), not zero. Therefore

    nu_r^F(D_Lambda^c)<=C_m Lambda^-m+Cr.                   (Q32)

This holds independently of the local condition rH<=1.
The rare scalar integration supplies r^5 BEFORE the single full normalization.
A Cauchy–Schwarz bound on an unconditional C4 tail would not prove (Q32).

### 6.2. Model failure, not the divergent unmarked measure

Under CUB's exact shear use s=-lambda, a=gamma, beta=B1, c3=C3, and

    Bsh=B1-gamma^2/12=-D/12,
    Dsh=(C3-gamma B1/4+gamma^3/72)/2=J/1152.

Its physical typed domain is exactly T and its weight is
9(4s^2-Bsh^2)=a_Ma_S/16.
Every extra nondegenerate critical point has negative height:
the local quadratic/Euler argument in (Q20) applies to any critical Y!=M.
CUB Theorem C also proves that every extra point in the open window (-1,0)
is a nondegenerate saddle. Thus CUB's n>0 is exactly Rsec apart from the
named null exclusions; absent or degenerate branches are not invented.
From CUB G13, on n>0,

    0<lambda<=2|Bsh|+(48Dsh^2)^(1/3)<=C Pjet^2,
    integral w_lambda 1_{n>0} d lambda
                   <=384|Bsh|^3+2304Dsh^2<=C Pjet^6.      (Q33)

For lambda>Lambda this forces Pjet^2>Lambda/C.
The contact joint slice has uniform Gaussian decay. Consequently

    nu_0^F(D_Lambda^c)<=C_m Lambda^-m                       (Q34)

using the fixed Gaussian moment of Pjet^(6+2m).
No unmarked n=0 mass is included in this calculation.

CUB G11 now gives exactly

    M_F=nu_0^F(R^4)=alpha_1+alpha_2, 0<M_*<=M_F<=M^*<infinity. (Q35)

For uniform positivity take the fixed open neighborhoods of CUB's n=1 and
n=2 examples. Their typed weights are positive; the compact b/frame family's
Gaussian slice has a uniform positive lower bound on a smaller compact
neighborhood, and z_0 is uniformly bounded above.
This is once per FAILURE event, not the count moment alpha_1+2alpha_2.
The result still concerns candidate-pair Palm selection, not once-counted bars.

## 7. Complete cutoff balance and rates

For a fixed integer m>=1 define

    alpha=1/[2(m+3)], beta_m=m/[2(m+3)],
    Lambda=r^-alpha, w=r^(-beta_m/8), d=r^beta_m.           (Q36)

Then H<=2r^-alpha for r<=1 and e=rw^4=r^(1-beta_m/2).
Every admissibility inequality (Q26) holds for sufficiently small r
uniformly in the fixed parameter family. Indeed their vanishing powers are

    rH: 1-alpha;
    rw: 1-beta_m/8;
    e: 1-beta_m/2;
    H^2e: 1-beta_m/2-2alpha;
    H^3e: 1/2+beta_m/2;
    rw^2: 1-beta_m/4;
    d: beta_m.

All are strictly positive. Choose a cutoff small enough for their displayed
fixed prefactors as well as r_0, w>=5 and d<=1/4. This constructs a valid
uniform r_m without assuming compact-gap uniformity or a numerical lifetime
window.

For completeness the power of r in EVERY term of (Q27),(Q32),(Q34) is:

| Term | Exponent, writing beta=beta_m |
|---|---|
| w^-8 | beta |
| rH^3w^-4 | 1/2+3beta/2 |
| H^4e | 1/3+5beta/6 |
| rH^5sqrt(e) | 2/3+17beta/12 |
| H^4e^(2/3) | beta |
| rH^5e^(1/3) | 1/2+3beta/2 |
| d | beta |
| rH^4, including typing leakage and density error | 1/3+4beta/3 |
| H^3(e/d)^2 | 3/2-2beta |
| H^5r^2w^4 | 7/6+7beta/6 |
| H^7r^2w^2 | 5/6+25beta/12 |
| Lambda^-m, either failure tail | beta |
| scaled far/derivative exceptions | 1 |

Because 0<beta_m<1/2, every exponent is at least beta_m.
In particular the Taylor-Markov term requires precisely 3/2-2beta>=beta,
and is strictly better for each beta<1/2.
Combine (Q29) with the two nonnegative omitted masses (Q32),(Q34):

    ||nu_r^F-nu_0^F||_var<=C_m r^beta_m.                    (Q37)

For m=3 this uses
Lambda=r^(-1/12), w=r^(-1/32), d=r^(1/4), e=r^(7/8),
the fixed actual residual moment J_r^16 and model jet moment Pjet^12.
It proves the first rate in (Q3). No moment order grows with r.

For any requested fixed 0<beta<1/2 choose an integer
m>=max(1,ceil(6beta/(1-2beta))). Then beta_m>=beta, and (Q37)
implies C_m r^beta for r<=1. This proves the full family (Q4).
No m tends to infinity as r tends to zero. The construction approaches but
does not attain exponent1/2; it does not prove optimality.

## 8. Consumer, scope and negative-inference boundary

Apply (Q37) to phi=1. By the exact event and measure definitions,

    r^-3(1-p_r)=alpha_1+alpha_2+O_m(r^beta_m).               (Q38)

Multiplication by r^3 gives (Q3),(Q4). This is the promised genuinely new
quantitative consumer of the already-known leading failure coefficient.
The positive mass also permits normalization of the raw-jet measure given
F_r with the same rate, by the elementary positive-mass normalization
inequality. No real-valued mark is added by that observation.

Retained exclusions:
- k=1 is fixed. No constants were tracked uniformly over compact positive
  gap sets, let alone small gaps; that extrapolation is not made.
- The fixed field, finite L, compact births and all frames are set BEFORE
  r tends to zero. No infinite-volume, other-covariance or d>=3 theorem.
- Original A2v1 remains AMEND. We consume only C95's explicitly corrected G
  with its retained local premises; this does not impersonate an author v2.
- C96/P §8 supply the ordinary-global-elder event. Tests do not prove that
  interface, Gaussian genericity, or a new global persistence correspondence.
- Variation in (Q37) is on fixed raw jets of the actual FAILURE population.
  Weak or smoothed height convergence is not unsmoothed height-density TV.
- This does not sum rejected pairs into replacement-bar intensity, identify
  all finite bars, discharge regional multiple-witness collisions or the
  intermediate/small-gap lane, prove the unrestricted refined lifetime
  remainder, or change Conjecture7/status.
- Finite rational controls verify formulas, cutoff exponents and rejection
  of explicit false shortcuts. The uniform analytic proof is §§1–7, with
  the exact imported interfaces; successful scripts do not accept a theorem.

## 9. Exact source custody and exposure

All native mathematical inputs were fetched/read at their full exact bodies.
The six repository inputs were freshly fetched at Math-
044d42d5bd7f31df6f7e6b9034d6711e8fb7ee43. Copies are byte-identical
reading copies, not new source revisions. Parent P is read with E1,E2,REC.
C91–C98 remain fixed-parameter/fixed-layer source statements; the growing
cutoff estimates are derived here, not attributed to their theorem headers.
Reviews identify scoped exposure/history, not mathematical axioms.

Native objects, all in https://github.com/d6g8k5htny-coder/main/issues/229 :
- C91 proof5963566666: 12433B, SHA256
  74a9ee276c3647276deb544c6d83e3cf21f708f55f9009fa4db5cc49c9d0e9aa;
  review5963668996. Consumed: pinned raw C4 constants and Hessian transfer.
- C92 proof5963825788: 19567B, SHA256
  6fa4c3d6d1e8c3d8590c865802d5df061ad5b17652ddc7fd7bf5c5e8b8de084a;
  review5963946854. Consumed: J4/J8–J18 and actual ten-observation density.
- C93 proof5964167051: 15545B, SHA256
  f25f86cc66ae335b4832ea53670646815567ec7854fa0386f8c57f6939e0af1c;
  review5964232937. Consumed: E7–E13, strip substitutions and genuine a_i poles.
- C94 proof5964517708: 15407B, SHA256
  0fe4fa2028f8ddbbf5a79df3879bcbd3789f19409fb44ad739caeabedff1af3c;
  review5964735560. Consumed: C5/C11/C12/C15 and local value bound.
- C95 proof5964938563: 16185B, SHA256
  c0d9ee72352fafe91f96a8b6187c978f09ee3c187d5f4c7c2462c0187750d2e1;
  review5965062739. Consumed: corrected G and actual torus maximin sufficient
  event, preserving QS/CUB local premises and original A2 AMEND.
- C96 FULL native proof5965141133: 7913B, SHA256
  0758b5de8f4d9e4658ca3c6cf3e52c23d8e12f77999e9c3668ef0bedb15a05f5;
  mathematical suffix7657B SHA256
  7198ff636e330749428ded6938776dad612f6bdb51ad62359b445f016df13a7a;
  review5965199940/completion5965212531. Consumed: Borel fixed-pin maximin/H0.
- C97 proof5965421543: 16098B, SHA256
  acf83958e6ea650d83bf811b2beacc03b553637dc4a3160012567c7f0a300a57;
  review5965531981. Consumed: finite branches, Euler margin, raw chord,
  R9–R20 and both mu/4(1-mu) tolerances.
- C98 proof5965738339: 15050B, SHA256
  3ca1622197bf22cf71ab64f2938ecc0b022ed09487b691d50ae8d2ad1f46d198.
  Consumed: B1–B13 coverage including no-saddle/exceptional cases, raw neutral
  polynomial and actual/model null sets. Its fixed-Lambda rate is not imported.

Repository source identities at the stated immutable Math cut:
- P: imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md,
  blob dfed3b8d318a3ab1950957f393307733a4bef3f2, 40261B, SHA256
  9350ad6eaba6626b93c3dedeef9e2ff816e5cdf1c8318e85fb27499141c84bc7.
  Consumed: §§3–8, full normalizer, endpoint-independent residual, cap split,
  fixed-pin genericity and global older-point interface.
- E1: imports/lifetime_parent_20260925/ERRATUM_CONGRUENCE.md,
  blob213594d6ca6a86fb938110f4d166d9ce275a02d0, 1782B, SHA256
  bad7ef609c4ad8c41ad6af562c1b6807921e19a9d556ed793ad1a0db6e202028.
- E2: reviews/d1_section9_borel_repair_20260925/REPAIR.md,
  blobfe9b9ce4999908bb3814b500ee2d0ceb0c6f704a, 9062B, SHA256
  845abf9f9c99d672c2a10a887b5a2e7206a3d2de3d876f35f75ff6e2dc13e62f.
- REC: reviews/d1_chain_reconciliation_20260928/RECONCILIATION.md,
  blob75da2597971510f843f8d90c743950cb8c177342, 23312B, SHA256
  451b9d7ffee072a73fc904cab891b6693e3f233808b89df10cce1b57036b65da.
  Consumed: W1 wording, embedded chart and scoped parent consumption.
- CUB: frontiers/planar_cubic_cluster_20260929/PROOF.md,
  blobbb446d08db8a944537a743ad550b88c1c2ad5758, 19889B, SHA256
  117e9299a71e6139270266889eb772ed97518e402d9af029bbdb67caf9d4a0f0.
  Consumed: shear/typing classification and G11–G13; not global count exhaustion.
- ELDER: frontiers/local_elder_geometry_20260930/PROOF.md,
  blobef2aa57959ea9f721bbf2316ce94cf616c1c9113, 39722B, SHA256
  f68038be79b46124b0f9b31205aa6e3682b34b6f5ef81f4a5697ae81f07cc46b.
  Consumed: S4–S8/S13–S14, actual failure population and cap-tail integration.
  The pre-existing qualitative full failure limit is retained, not reinvented.

C82 proof5959920397, mathematical prefix11253B SHA256
f390ad99b07ec4eda9160191d776cfc3a53ca628976165987d9a61ab79816827,
review5959988102, is consumed through C94/C97's pinned full interfaces.
A1 correction5962385282 and QS5961415030 remain local geometric antecedents
as specified by C94/C95/C97. No new source-wide acceptance is claimed.

Author exposure: root01a0adb2 previously reviewed C91–C94, coordinated C95/C97/C98,
authored C96, and contributed C99. Root01a0bbb5 authored the imported C92–C95,
C97/C98 composition sources and supplies current custody, not C101 nonauthor
review. Earlier source/intake/feasibility exposure is disclosed. A fresh
reviewer must reconstruct the WHOLE new growing-cutoff proof, especially
(Q6),(Q10),(Q13),(Q19)–(Q25),(Q30)–(Q37), not merely accept its ledger.
No repository branch, commit, CI, integration, scientific register or Drive
delivery is changed by this native author publication.
