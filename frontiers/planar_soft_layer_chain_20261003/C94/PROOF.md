# Actual weighted trap-window and random-margin transfer

Object: C94-PLANAR-WEIGHTED-TRAP-WINDOW-RANDOM-MARGIN-20261003-v1.
Author: OpenAI/Codex root01a0bbb5, acting for Dylan Roy — delegated AI work.
Disposition: AUTHOR-SIDE PROOF CANDIDATE; nonauthor technical review pending.
Personal reading PENDING; organizational independence 0; scientific effect NONE.

This supplies quantitative actual-law bounds for the radius, local value
tolerance and decision margin needed on a specified planar model-elder
sector. A simultaneous certificate fails with full weighted probability
O(r^(7/2)), whereas that sector has probability of order r^3. The analytic
statement is separate from the conditional geometric application in §6.
In particular the original A2 v1 remains AMEND; it is not relabeled PASS.

## 0. Fixed setting, exact sources and observables

Use C92's normalized periodized Gaussian field on the planar torus of fixed
side L>0, gap mark k=1, birth b in a fixed nonempty compact set B0 and all
orthonormal frames. Pins, Q_r, actual determinant weight W_r, FULL Z_r,
Q_r^W, raw field F_r, cubic G, error E_r and field norm N are exactly C92's.
No new pin law or normalization is introduced. In particular

    A=f_zz(0), lambda=-A/r, t=(gamma,B1,C3),
    Pjet=1+|gamma|+|B1|+|C3|,
    D_Lambda={|lambda|<=Lambda}, 0<Lambda<infinity fixed,
    a_M=24lambda-gamma^2+12B1,
    a_S=24lambda+gamma^2-12B1,
    T={a_M>0,a_S>0}, A_*=48Lambda,
    w_lambda=a_M a_S/16 on T,
    mu_r(E)=r^(-5) E_Q[W_r 1_E],
    dmu_0=rho_0(0,t) w_lambda d lambda dt on T,
    Q_r^W(E)=r^3 mu_r(E)/z_r, z_r=Z_r/r^2=z_0+O(r).       (C1)

Here mu_r is restricted to D_Lambda. C92 gives a uniformly positive floor
for z_r, a uniform Gaussian density envelope in t and weighted L1 error
O(r). C93 supplies the correlated moment-weighted edge estimate

    r^(-5) E_Q[W_r N^p Pjet^q 1_T phi(a_i)]
       <= C_(p,q) integral_0^A_* phi(s)(s+r) ds,           (C2)

for nonnegative measurable phi and fixed finite p,q. All constants below
are uniform in b and frame; they may depend on L,B0,Lambda and fixed moment
orders. They are finite analytic constants, not numerical enclosures.

Sources: C91 proof5963566666/review5963668996;
C92 proof5963825788/review5963946854;
C93 proof5964167051/review5964232937;
C82 proof5959920397/review5959988102;
QS5961415030; A1 proof5961913750/review5962025965/correction5962385282;
A2 original5963200491 and C90 combined review5963477339. All are in
main issue229. SOURCE_IDENTITIES.json pins retained source bytes. The
C82 mathematical body is11253B, SHA256
f390ad99b07ec4eda9160191d776cfc3a53ca628976165987d9a61ab79816827;
its native footer is separately retained. C92/C93's imported Gaussian
interfaces and their errata remain premises with exactly their scopes.

On T and gamma!=0 define the exact raw-to-cubic map

    D=gamma^2-12B1, J=8gamma^3-144B1 gamma+576C3,
    psi=24lambda/gamma^2, c=D/gamma^2, R=J/gamma^3,
    u=X+gamma zeta/12, Z=gamma zeta,
    P(u,Z)=2u^3-3u/2-1/2-(psi+2cu)Z^2/48+RZ^3/3456.
                                                               (C3)

Direct expansion gives G(X,zeta)=P(u,Z); here lambda is precisely the
tilde-lambda of QS at k=1. Thus a_S=gamma^2(psi+c),
a_M=gamma^2(psi-c), and raw values are already in P-units.

Let mu be the maximum of P(Y)+1 over extra NONDEGENERATE saddles Y of P,
with mu=-infinity if there is none. It is a Borel extended-real function:
C82 §2 represents these saddles by finitely many algebraic branches,
including degree drops and tangencies. Define the fixed jet sector

    E={D_Lambda, T, gamma!=0, psi>=2c,
       R^2<=16(psi-2c)^2(psi+c), mu<0}.                 (C4)

The two explicit inequalities in (C4) retain A1's elder-side hypotheses;
we do not need to infer them from an unrecorded classification theorem.
The finite-r sector uses these model jets, not an actual elder indicator.

Set a=2/(3sqrt(3)), kappa_S=(psi+c)/48, kappa_M=(psi-c)/48 and

    tau_i=a+|c|/(24sqrt(3) kappa_i)
                 +|R|/(3456 kappa_i^(3/2)),
    m_S=2/(125 tau_S^2), e_M=min(1/(8 tau_M^2),1),
    v=min(m_S,e_M), eta=(1/2)min(v,-mu),
    Rbox=3/2+(5/2)(|gamma|+12)/sqrt(24lambda).           (C5)

On E all these quantities except possibly -mu are finite and strictly
positive; min(v,+infinity)=v. The tolerance eta is random and depends on
the same jets as the determinant and the field norm. No independence is
assumed. The chart gamma=0 is null under both measures but is not extended
pointwise. Define E0(r,w)=sup_{|X|,|zeta|<=w}|E_r| and H_i(r,w) exactly as
C93 E13 (raw-window supremum of the rescaled Hessian norm).

## 1. Actual radius tail

For rho>0, fixed finite p,q>=0,

    r^(-5) E_Q[W_r N^p Pjet^q 1_T
                              1_{Rbox>3/2+rho}]
          <= C_(p,q)(rho^(-8)+r rho^(-4)).             (C6)

Only large rho is needed. No A2 trap theorem is used to prove this tail
of the explicitly defined function Rbox. Its geometric meaning is §6.

Proof. C93 E7–E8 gives the joint integrand envelope

    C exp(-c0|t|^2)[w_lambda Pjet^(p+q)
                                      +r Pjet^(p+q+4)].

Change B1 to s=a_S, with dB1=ds/12. On T, 0<lambda<=Lambda,
0<s<48lambda and w_lambda=s(48lambda-s)/16. Absorb the polynomial
into half the Gaussian and retain exp[-c1(gamma^2+C3^2)] after dropping
the remaining B1 decay. The radius event implies

    lambda<H(gamma)/rho^2,
    H(gamma)=(25/96)(|gamma|+12)^2.

For U=min(Lambda,H/rho^2), the two elementary integrals are

    integral_0^U integral_0^(48lambda)
                s(48lambda-s)/16 ds dlambda =288 U^4,
    integral_0^U integral_0^(48lambda) r ds dlambda=24r U^2. (C7)

The Jacobian1/12 is absorbed into C, not dropped from the identity. Bound
U^4 by H^4/rho^8 and U^2 by H^2/rho^4, and integrate the remaining
Gaussian polynomial. This proves (C6) with all correlations retained.
It is a bounded-lambda actual-law tail; it is not the fixed-(c,R), model
rho^-6 tail of A2, and neither calculation is a partition of the other.

## 2. A usable lower bound for the random local value tolerance

On E, A1 W1 (with its retained correction) gives

    tau_S<=a(2psi-c+3|c|)/(psi+c), tau_M<=4a.

Since |c|<psi and 0<lambda<=Lambda,

    tau_S<=6a psi/(psi+c)<=3a A_*/a_S,
    v>=c_* a_S^2, c_*=3/(250 A_*^2).                  (C8)

Indeed a^2=4/27 gives m_S>=3a_S^2/(250 A_*^2), whereas
e_M>=27/512>3/250 and a_S<=A_*. These inequalities also show the
deterministic threshold in (C8) never exceeds the available e_M bound.
Only W1 is used: no fixed-R equality/sharpness assertion from A1 is used.

Let K0=167/192, e=rw^4 and epsilon=2K0 e/c_*. For w>=1 with
2rw<=L/4 and sqrt(epsilon)<=min(1,A_*),

    mu_r(E intersect {E0(r,w)>=v/2})
             <= C(epsilon+r sqrt(epsilon))
             <= C(e+r sqrt(e)).                      (C9)

Proof. The exact C91/C92 bound is E0<=K0 N e. On a_S>=d, (C8) and
the pointwise squared Markov inequality give the bad-event bound
epsilon^2 N^2 a_S^(-4). On a_S<d use C93's strip estimate. By (C2),
the total is at most

    C[d^2+rd+epsilon^2(d^(-2)/2+r d^(-3)/3)].          (C10)

Here the last terms follow by integrating s^-3+r s^-4 from d to A_*
and dropping nonnegative upper-end subtractions. Choose d=sqrt(epsilon).
If d=A_* the away part is null and the strip suffices. This proves (C9).
It never multiplies an L1 error by an uncontrolled inverse random margin.

## 3. The model level band under the actual Gaussian jet measure

For 0<d<=1/2,

    mu_0(T intersect {|mu|<=d})<=Cd,
    mu_r(T intersect {|mu|<=d})<=C(d+r).               (C11)

This uses C82 Theorem LB, not its independent-Gaussian Corollary GLB.
The actual finite-torus jets need not be independent or have the reference
variances. At fixed t with gamma!=0, c and R are fixed and

    dlambda=(gamma^2/24)dpsi,
    w_lambda dlambda=(gamma^6/384)(psi^2-c^2)dpsi.     (C12)

Use the JOINT density bound rho_0(0,t)<=C exp(-c0|t|^2). Extend the
lambda integral to the full typed psi range, a valid enlargement of a
nonnegative integral. C82 LB bounds the inner integral by
d[(1024/3)|c|^3+64R^2]. Both apparent chart poles cancel:

    gamma^6|c|^3=|D|^3, gamma^6 R^2=J^2.              (C13)

The remaining integral of (|D|^3+J^2) against the joint Gaussian envelope
is finite uniformly in birth and frame. This proves the first assertion.
C92's L1 bound applies to the BOUNDED band indicator, proving the second.
The width d is deterministic, hence independent of the inner psi variable.
No clipping or substitution of a psi-dependent width is involved.

## 4. Actual control with the full random tolerance

For any fixed finite p>=1, 0<d<=1/4 and sufficiently small e=rw^4,

    mu_r(E intersect {E0(r,w)>=eta})
       <=C[e+r sqrt(e)+d+r+(e/d)^p].                 (C14)

To prove it, eta=(1/2)min(v,-mu). If E0>=eta, either E0>=v/2 or
E0>=(-mu)/2. Use (C9) on the first event. The second lies in the union
of {-2d<=mu<0} and {E0>=d}. The first costs C(d+r) by (C11), used
with width2d. No-extra-saddle points have mu=-infinity and are absent.
C92 J6 bounds the second event by C(K0 e/d)^p in mu_r units. This
uses E_Q[W_r N^p 1_D]=O(r^5), not an unweighted field-norm probability.
All these are union bounds; dependencies among the events are harmless.

## 5. A simultaneous analytic certificate at the rare-sector scale

Let Good(r,w) be the following event inside the explicitly defined E:

    Rbox<=w, E0(r,w)<eta, H_M(r,w)<1, H_S(r,w)<2/5.   (C15)

For deterministic w>=3 with 2rw<=L/4, sufficiently small rw^4 and
0<d<=1/4, (C6), (C14) and C93 E15 imply

    Q_r^W(E minus Good(r,w))
       <=C r^3[w^-8+r w^-4+rw^4+r sqrt(rw^4)
                         +d+r+(rw^4/d)^p+r^2 w^4].   (C16)

For (C6) use rho=w-3/2>=w/2. The two Hessian losses are at most
Cr^5w^4 by C93 at the fixed thresholds1 and2/5. Divide every mu_r
bound by the same full z_r and multiply by r^3. The outside-T error is
not silently discarded: E is DEFINED inside T; no assertion here covers
all finite-r soft-layer jets. C93 separately supplies its O(r^4) bound.

In particular take the fixed choices

    w=r^(-1/16), d=r^(1/2), p=2.                      (C17)

For sufficiently small r all window/cutoff conditions hold. The powers
inside the brackets in (C16), in order, are

    1/2, 5/4, 3/4, 11/8, 1/2, 1, 1/2, 7/4.

Consequently

    Q_r^W(E minus Good)<=C r^(7/2).                   (C18)

Write m_E(b,frame)=mu_0(E). C92's bounded-indicator L1 comparison and
normalizer estimate give

    Q_r^W(E)=r^3 m_E/z_0+O(r^4),
    Q_r^W(Good)=r^3 m_E/z_0+O(r^(7/2)).               (C19)

Moreover m_E has a uniform positive lower bound. Here is an explicit
interior witness rather than an assumption of positivity. At
lambda=Lambda/2, gamma=1, B1=(1+6Lambda)/12 choose C3 so J=0.
Then psi=12Lambda, c=-6Lambda, R=0. The extra-point discriminant factor
R^2+64c(psi^2-c^2) is strictly negative. Thus a small fixed neighborhood
has no extra critical point, mu=-infinity, strict T, psi>2c and R^2<q^2.
It is a compact positive-volume subset of E after shrinking. Its w_lambda
and joint Gaussian density have positive lower bounds, the latter uniform
over compact birth/frame parameters by C92's nondegeneracy and continuous
parameter dependence. A uniform upper bound follows from m_Lambda.
This proves

    Q_r^W(Good | E)=1-O(r^(1/2)).                     (C20)

This is a conditional probability under the full ACTUAL weighted law,
not a probability under a newly normalized reference jet distribution.
It is uniform in the declared fixed parameters. The constants/cutoffs may
depend on Lambda; letting Lambda grow with r is not permitted.

## 6. Exact geometric consumption boundary

The analytic theorem (C6)–(C20) uses only the displayed functions Rbox,
v, mu, the source polynomial estimates and C91–C93. It does not need the
topological assertions of A2. The following is a conditional application,
with the required corrected source explicitly identified.

**Geometric interface G.** For the same cubic, exact pins and (H), assume
the corrected QS-Eprime criterion: V'_eta, E_S and E_M lie in
[-5/4,3/2] times [-30/sqrt(psi),30/sqrt(psi)], and value error<eta on
V'_eta together with rescaled Hessian errors<1 at M and<=2/5 at S implies
the maximin death level d_g(M)=g(S)=-1. The axis through (3/2,0) is
included in V'_eta. The raw image of the box has Euclidean radius<=Rbox.

The proposed source is A2 Theorem QS-Eprime and Corollary9(a)(b), read
with these C90 repairs, not A2's literal v1:

1. In Lemma7(b), set a0=599/250,b0=277/250,k0=256/125,
   K=b0+k0*a0=187969/31250, omega0=a0/K=74875/187969.
   For 0<omega<=omega0 use b0/(1-k0*omega)<=K, whose denominator is
   positive there; for omega>=omega0 use a0/omega<=K. This preserves
   K<6.05 without using the invalid reciprocal on the second interval.
2. Lemma7(c)'s sharpness segment stops BEFORE the first level root
   t_eta in(0,1), (1+m)(3t_eta^2-2t_eta^3)=1+eta. The saddle itself
   is outside the trap. The limit t_eta->1 as eta increases to m retains
   supremal constant12. This sharpness statement is not used in G.
3. Corollary9(c)'s typed integral is zero for x<=|c|; otherwise it is
   x^3/3-c^2*x+2|c|^3/3. Its model rho^-6 tail is not used in C94.

These identify the prospective corrected consumer interface and preserve
the historical AMEND verdict. They do not impersonate an author-issued A2
successor, settle its publication custody, or constitute a new full review
of QS's topology. Exact-delta acceptance of a frozen corrected geometric
source remains separate from the unconditional analytic verdict here.

**Conditional corollary.** If G is supplied with its retained QS/CUB local
premises, Good implies its hypotheses at the actual field. Indeed
0<eta<min(-mu,m_S,e_M); Rbox<=w contains the raw images of every required
set; (C3) transfers value errors exactly; C93 transfers the Hessian norms;
the actual pins are exact. The axis endpoint has been retained. The small
raw patch embeds into the torus because 2rw<=L/4. A path to a higher point
must leave the compact trap through its boundary, while the axis gives a
path attaining the saddle level. Thus the same maximin argument works on
the torus. Conditional on G, the failure of that maximin conclusion on E
has full Q_r^W mass at most Cr^(7/2).

This is one model sector and one direction of a decision comparison. It
is not a bijection of all short persistence bars with local witnesses,
does not control the rejected-side chord, and does not close shrinking
multiple-witness collisions or intermediate/coarea obligations. No
all-mark, unbounded-lambda, infinite-volume or unrestricted density/
remainder statement follows. The observable is the stated maximin death
level; any translation to a persistence-module convention keeps its own
Morse/topology and event-identification hypotheses.

## 7. Verification meaning

The accompanying exact-rational controls check the raw polynomial identity,
the 1/12 and gamma^6/384 Jacobians, radius integration powers/constants,
local tolerance algebra, truncation exponents, chart-pole cancellations,
the positive sector witness and the complete exponent ledger. Negative
controls reject omitted finite-r terms, lost Jacobians, incorrect radius
powers, false independent-moment factorizations and conversion errors.
The continuous Gaussian estimates, topology and limiting conclusions are
proved or explicitly imported above; finite controls are not their proof.
