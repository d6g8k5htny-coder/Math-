# Actual weighted rejection from a finite cubic chord

Object: C97-ACTUAL-WEIGHTED-REJECTED-CHORD-20261003-v1.
Author: OpenAI/Codex root01a0bbb5, for Dylan Roy — delegated AI work.
Disposition: AUTHOR-SIDE CANDIDATE; fresh nonauthor review pending.
Deterministic feasibility support: OpenAI/Codex /root/clipped_surrogate_review,
dispatched by coordinating root01a0adb2. It reconstructed the margin/radius
bounds from QS/C82, with prior source/program exposure and no C97 checker
exposure. This is coauthor-side support, not a nonauthor acceptance. Personal reading PENDING; human review NONE;
organizational independence 0; scientific effect NONE.

This proves the rejected-side companion to C95/C96 on a fixed bounded
soft-Hessian layer. A finite chord certifies a path to a higher point above
the designated saddle. BOTH its saddle clearance and its endpoint height
are integrated under the actual weighted law. No branch-adjacency event
is substituted for elder pairing.

## 0. Exact setting, retained inputs and theorem

Use C92's planar normalized periodized Gaussian field on the torus of fixed
side L>0, gap mark k=1, birth b in a fixed nonempty compact set B0 and all
orthonormal frames. In frame coordinates the exact pins are
M_r=(-r/2,0), S_r=(r/2,0), f(M_r)=b, f(S_r)=b-r^3 and zero gradients.
Q_r is the continuous Gaussian regression law at these pins,

    W_r=|det H_M det H_S| 1{H_M<0, index(H_S)=1},
    Z_r=E_Q[W_r], Q_r^W=(W_r/Z_r)Q_r,
    A=f_zz(0), lambda=-A/r,
    t=(gamma,B1,C3)=(f_xxz(0),f_xzz(0),f_zzz(0)),
    Pjet=1+|gamma|+|B1|+|C3|,
    N=1+max_{|alpha|<=4} sup_torus |D^alpha f|,
    D_Lambda={|lambda|<=Lambda}, 0<Lambda<infinity fixed.

Write a_M=24lambda-gamma^2+12B1, a_S=24lambda+gamma^2-12B1,
T={a_M>0,a_S>0}, A_*=48Lambda and w_lambda=a_M a_S/16 on T.
The rescaled finite measure is mu_r(B)=r^(-5)E_Q[W_r 1_B] on D_Lambda;
for events depending on the whole field the same notation denotes this
expectation, not a fictitious jet-only conditional law. The model measure
is dmu_0=rho_0(0,t)w_lambda d lambda dt on T, where rho_0 is the JOINT
contact Gaussian density retained by C92. Its A-marginal density is not
divided out. Full normalization is

    Q_r^W(B)=r^3 mu_r(B)/z_r, z_r=Z_r/r^2=z_0+O(r), z_r>=z_*/2>0. (R1)

On T, gamma!=0, define

    D=gamma^2-12B1, J=8gamma^3-144B1 gamma+576C3,
    psi=24lambda/gamma^2, c=D/gamma^2, R=J/gamma^3,
    u=X+gamma zeta/12, Z=gamma zeta,
    P(u,Z)=2u^3-3u/2-1/2-(psi+2cu)Z^2/48+RZ^3/3456.              (R2)

Here P denotes the cubic, distinct from Pjet. Its pins M=(-1/2,0),
S=(1/2,0) have values0,-1. Typing is psi>|c|. C91/C92 give the exact
raw cubic identity G(X,zeta)=P(u,Z). If
F_r(X,zeta)=[f(rX,r zeta)-b]/r^3 and E_r=F_r-G, then for w>=1,

    E0(r,w):=sup_{|X|,|zeta|<=w}|E_r| <= K0 N r w^4,
    K0=167/192, provided 2rw<=L/4.                               (R3)

Let mu=max{P(Y)+1:Y is an extra nondegenerate saddle}, or -infinity if
there is no such point. Define the rejected sector

    Rsec={D_Lambda, T, gamma!=0, mu>0}.                            (R4)

The symbol Rsec is not the coefficient R in (R2). No A1 elder-sector
inequality is imposed here. Let H_r be C96's designated finite ordinary-
superlevel H0 pairing event, defined false off the Borel Morse/distinct-
value typed-pin locus. Let A_r={D_f(M_r)=f(S_r)} in C95/C96's path convention.

**Theorem R.** Uniformly over the stated fixed birth/frame parameters,
for sufficiently small r, writing m_R=mu_0(Rsec),

    0<m_*<=m_R<=m^*<infinity,
    Q_r^W(Rsec intersect {D_f(M_r)<=f(S_r)}) <= C r^(7/2),
    Q_r^W(Rsec intersect H_r) <= C r^(7/2),
    Q_r^W(Rsec minus H_r)=r^3 m_R/z_0+O(r^(7/2)),
    Q_r^W(H_r | Rsec)=O(sqrt(r)).                                 (R5)

No assertion here exhausts all ordinary short bars, all soft jets or all
marks. Lambda is fixed, not growing with r. The theorem uses the following
exact reviewed interfaces, with their source-bound errata and limitations:

- C92 proof5963825788, SHA256
  6fa4c3d6d1e8c3d8590c865802d5df061ad5b17652ddc7fd7bf5c5e8b8de084a:
  actual weighted L1 comparison, full normalizer and correlated moments.
- C93 proof5964167051, SHA256
  f25f86cc66ae335b4832ea53670646815567ec7854fa0386f8c57f6939e0af1c:
  E2/E7/E8, retaining the finite-r edge term.
- C94 proof5964517708, SHA256
  0fe4fa2028f8ddbbf5a79df3879bcbd3789f19409fb44ad739caeabedff1af3c:
  C11's actual saddle-level band. Its proof uses C82 LB, not independent
  reference Gaussian jets. No conditional A2 geometric conclusion is used.
- C82 proof5959920397, 11253-byte proof prefix SHA256
  f390ad99b07ec4eda9160191d776cfc3a53ca628976165987d9a61ab79816827:
  all finite extra-critical-point branches and their exact identities.
- C96 proof5965141133, 7657-byte suffix SHA256
  7198ff636e330749428ded6938776dad612f6bdb51ad62359b445f016df13a7a,
  full review5965199940 and author completion5965212531: A_r=H_r Q_r^W-a.s.

QS5961415030 (SHA25612ffa126e45253fea5eec47f50ffa842a61165a2cbc0f5917e3543e81c09c1f2)
is the historical source of the corrected two-margin chord criterion.
We reconstruct that elementary criterion below; no unreviewed QS elder
trap or source-wide disposition is imported. SOURCE_IDENTITIES.json retains
the exact proof/review bodies and extraction rules. Parent P/E1/E2 and
reconciliation remain the imported analytic premises of C92 and C96.

## 1. Finite saddles, measurable choice and chord geometry

C82 section2 covers all extra nondegenerate saddles by at most two algebraic
branches, including the c=0 case, the R^2=64c^3 degree drop and the tangency
endpoint (the degenerate point is not counted). Thus mu is Borel, is a
finite maximum on Rsec, and is attained. Order the finitely many saddle
points lexicographically by (u,Z) to break a highest-value tie. This gives
a Borel selection Y on Rsec. No assertion of a saddle at infinity is made.

At M, for v=(a,z), the exact local expression is

    P(M+v)=-rho^2+T3(v), rho^2=3a^2+kappa_M z^2,
    kappa_M=(psi-c)/48>0,
    T3(v)=2a^3-(c/24)az^2+(R/3456)z^3,
    |T3(v)|<=tau_M rho^3,
    tau_M=2/(3sqrt(3))+|c|/(24sqrt(3)kappa_M)
                              +|R|/(3456 kappa_M^(3/2)).          (R6)

At any critical Y!=M, the derivative along v=Y-M is zero. Euler's
identity for the homogeneous terms gives -2rho^2+3T3(v)=0. Consequently

    h:=-P(Y)=rho^2/3>0,
    rho>=2/(3tau_M), h>=4/(27tau_M^2).                           (R7)

The first inequality uses rho>0, so division by rho^2 is valid. For the
selected saddle on Rsec, h=1-mu and therefore 0<mu<1. This derives the
needed upper bound on mu without relying on a global cubic classification.

For sigma=-2u(Y), x=psi Z(Y)^2/144 and q=c/psi in(-1,1), C82's exact
critical identities give

    sigma^2-1=4q x, h=x-(sigma-1)/2,
    (sigma-1)^2<4h.                                             (R8)

Indeed x>0 and q<1, so sigma^2-1<4x=4h+2(sigma-1).
Since h<1, -1<sigma<3 and 0<x<h+sqrt(h)<2. Thus
|u(Y)|<3/2 and |Z(Y)|<sqrt(288)/sqrt(psi). The extended chord
K=[M,2Y-M] satisfies |u|<=5/2, |Z|<34/sqrt(psi). The inverse raw map is
X=u-Z/12, zeta=Z/gamma, and its Euclidean norm is bounded by

    |u|+|Z|sqrt(1/144+1/gamma^2)
      <=5/2+(17/6)(|gamma|+12)/sqrt(24lambda)
      <=Rch:=5/2+3(|gamma|+12)/sqrt(24lambda).                    (R9)

This is a bound for the whole finite chord, valid for either sign of gamma.
Gamma=0 remains outside the chart and is a null jet slice under both
weighted measures. No positive lower bound on |gamma| or lambda is imposed.

The restriction along the chord is exactly

    P(M+t(Y-M))=h(2t^3-3t^2), 0<=t<=2.                         (R10)

The polynomial has value0 at0, derivatives zero at0 and1, and value-h at1;
these four data determine the cubic, or (R7) gives it directly. Its minimum
is -h at1 and its value at2 is4h. Therefore if a continuous perturbation
g=P+e has exact values g(M)=0,g(S)=-1 and

    sup_K |e| < min(mu,4h),                                    (R11)

then g>-1 along K and g(2Y-M)>0. Hence d_g(M)>-1.
The second margin4h cannot be replaced by mu when mu approaches1.
No Hessian or gradient-path hypothesis is needed for this sufficient path.

## 2. Endpoint margin in raw jets

Put s=a_M in(0,A_*). Substitution in (R6) cancels the gamma chart poles:

    tau_M=(1/sqrt(3))[2/3+2|D|/s+|J|/(6s^(3/2))].              (R12)

The three-term square inequality gives

    tau_M^2 <= [4s^3/9+4D^2 s+J^2/36]/s^3.

Since |D|<=13 Pjet^2, |J|<=728 Pjet^3 and Pjet>=1, set

    Ctau=(4/9)A_*^3+676 A_*+728^2/36,
    c_h=4/(27 Ctau)>0.

Equations (R7) and (R12) imply the uniform pointwise bound

    h>=c_h a_M^3/Pjet^6.                                      (R13)

All constants are explicit functions of the fixed Lambda. They need not
be optimized. The power3 is retained; no false positive uniform margin or
finite untruncated inverse third moment is claimed.

## 3. Actual weighted radius and endpoint-error integrals

For any fixed finite p,q>=0, C93 E7/E8 supplies the joint integrand bound

    C exp(-c0|t|^2)[w_lambda Pjet^(p+q)+r Pjet^(p+q+4)]         (R14)

for mu_r with factor N^p Pjet^q. This came from conditional Gaussian
moments before integration; it preserves dependence of N on the jets.

For rho>0, the event Rch>5/2+rho implies
lambda<H(gamma)/rho^2, H=(3/8)(|gamma|+12)^2. Change B1 to s=a_S,
dB1=ds/12, so 0<s<48lambda and w_lambda=s(48lambda-s)/16.
Absorb polynomial factors into half the Gaussian, retain Gaussian decay
in gamma,C3, and set U=min(Lambda,H/rho^2). The elementary integrals are

    integral_0^U integral_0^(48lambda) w_lambda ds d lambda=288U^4,
    integral_0^U integral_0^(48lambda) r ds d lambda=24rU^2.

The Jacobian1/12 is absorbed into the constant, not omitted from the
transformation. Integrating H^4 and H^2 against the remaining Gaussian gives

    mu_r(T intersect {Rch>5/2+rho}; N^p Pjet^q)
                     <=C_(p,q)(rho^-8+r rho^-4).                (R15)

Next put e=rw^4, epsilon=K0 e/(2c_h). The endpoint-failure event
E0(r,w)>=2h on Rsec implies epsilon N Pjet^6 a_M^-3>=1 by (R3)/(R13).
For 0<d<A_*, split at a_M=d and apply C93 E2 with p=2,q=12 to the
squared pointwise Markov bound. It yields

    mu_r(Rsec intersect {E0>=2h})
      <=C[d^2+rd+epsilon^2(d^-4/4+r d^-5/5)].                   (R16)

The away integrals are integral_d^A_* (s^-5+r s^-6)ds, bounded by the
displayed inverse powers. Taking d=epsilon^(1/3)<=min(1,A_*) gives

    mu_r(Rsec intersect {E0>=2h})
                         <=C(e^(2/3)+r e^(1/3)).               (R17)

If d=A_* the away set is null and the strip alone suffices. This truncation
never applies an unbounded inverse margin to an L1 error. The finite-r term
r e^(1/3) is essential to the available bound and is kept.

For the other margin, C94 C11 gives the actual deterministic-width band
mu_r(T intersect {|mu|<=delta})<=C(delta+r), 0<delta<=1/2.
For 0<d<=1/4, a union of {0<mu<=2d} and {E0>=d}, together with C92's
weighted moment estimate and (R3), gives for each fixed p>=1

    mu_r(Rsec intersect {E0>=mu/2})<=C[d+r+(e/d)^p].             (R18)

The band width2d is deterministic, not a function of the inner psi variable.
The Taylor estimate uses E_Q[W_r N^p 1_D]=O(r^5). An unweighted field-norm
probability is not substituted for that correlated weighted estimate.

## 4. Rejection with an actual-field error rate

Define a measurable event inside Rsec by

    Good_R(r,w)={Rch<=w, E0(r,w)<(1/2)min(mu,4(1-mu))}.         (R19)

The sup defining E0 is over a compact raw window and equals the supremum
over a fixed countable dense subset for continuous fields. All jet functions
are Borel by the finite-branch construction. Thus Good_R is measurable,
even without selecting a continuous highest-saddle branch.

For w>=5 with 2rw<=L/4, e sufficiently small, and 0<d<=1/4, (R15)–(R18)
and full normalization (R1) give

    Q_r^W(Rsec minus Good_R)
      <=Cr^3[w^-8+r w^-4+e^(2/3)+r e^(1/3)+d+r+(e/d)^p].       (R20)

Here rho=w-5/2>=w/2 in (R15). If E0 reaches the half-minimum in (R19),
it reaches either mu/2 or2h, so both bad events are included. There is no
independence assumption in this union bound. Choose the fixed exponents

    w=r^-1/16, d=r^1/2, p=2, e=r^3/4.                         (R21)

For sufficiently small r, all cutoff and physical-window restrictions hold.
The bracket exponents in (R20), in order, are

    1/2, 5/4, 1/2, 5/4, 1/2, 1, 1/2.

Consequently

    Q_r^W(Rsec minus Good_R)<=Cr^(7/2).                         (R22)

On Good_R, (R9) places K in the raw window. The exact pins and (R19)
imply (R11), so its physical image is a path from M_r to a point higher
than b whose values stay strictly above b-r^3. The patch embeds into the
torus for the stated small-window condition, in every orthonormal frame.
The strict inequality on the compact chord supplies a positive clearance;
therefore D_f(M_r)>f(S_r), not merely a weak inequality.

It follows that {D_f<=f(S_r)} intersect Rsec is contained in Rsec minus
Good_R. C96 identifies H_r=A_r Q_r^W-a.s., at each fixed parameter/r,
using the retained parent Morse/distinct-value result and absolute
continuity under the actual determinant weight. No common probability-one
set over an uncountable family is required. Thus Rsec intersect H_r is
also bounded by (R22). This proves the two error assertions in (R5).

## 5. Positive rejected-sector mass and normalized conclusion

An explicit interior witness proves positivity. Set lambda=Lambda/2,
gamma=1, B1=1/12, hence c=0 and psi=12Lambda>0. Choose

    R=sqrt(32 psi^3), C3=(R+4)/576.

The extra saddle has sigma=1 and Z=48psi/R, so
P(Y)=-16psi^3/R^2=-1/2 and mu=1/2. It is nondegenerate, since
det Hess P=-psi/4<0, and T is strict. Its continuation to a small open
jet neighborhood still has P(Y)+1>0, giving a positive-volume subset of
Rsec inside D_Lambda; other saddles do not remove that property.
The determinant factor and joint Gaussian density have a positive lower
bound on a smaller compact box, uniformly in the compact birth/frame
parameters by C92. Therefore 0<m_*<=m_R; finiteness and a uniform upper
bound follow by Rsec subset D_Lambda and C92.

The set Rsec is fixed in (lambda,t), not radius-dependent. C92's bounded-
indicator L1 comparison and normalizer expansion imply

    Q_r^W(Rsec)=r^3 m_R/z_0+O(r^4).                             (R23)

Subtracting Q_r^W(Rsec intersect H_r)<=Cr^(7/2) proves the mass assertion
of (R5). Dividing by the positive order-r^3 mass in (R23) gives its
conditional probability O(sqrt(r)). The same leading mass holds for
Rsec intersect {D_f>f(S_r)} because its complement costs (R22).

Combining, without enlarging either domain, with C95/C96 on their E gives

    Q_r^W((E union Rsec) intersect (H_r symmetric_difference E))
                                                   <=C r^(7/2). (R24)

Here E and Rsec are disjoint because their mu signs differ. The specific
extra inequalities defining E are retained. We do NOT assert that their
union exhausts T or all actual weighted soft jets.

## 6. Boundaries and verification role

This is actual-field rejected-sector control for one designated pair with
the full normalizer. The finite chord criterion is a sufficient geometric
certificate, not a statement about gradient trajectories. The old condition
|e|<mu alone remains refuted; the retained exact mu=15/16 example is not
superseded by a new numerical experiment.

No all-small-bar/local-witness converse, regional multiple-witness estimate,
intermediate/coarea closure, unbounded-Lambda/all-mark limit, other dimension,
infinite-volume limit or new global density/remainder theorem follows.
Existing scoped D1/D2 acceptance and historical source dispositions stay
unchanged. This statement does not eliminate a final-theorem dependency
without an explicit downstream argument.

Exact rational controls check local/chord identities, radius implications,
edge-integral powers, chart-pole cancellation, endpoint obstructions and the
error ledger. Their role is algebraic falsification and reproducibility.
Finite tests do not prove the imported Gaussian estimates, the continuous
path argument or the persistence identification.
