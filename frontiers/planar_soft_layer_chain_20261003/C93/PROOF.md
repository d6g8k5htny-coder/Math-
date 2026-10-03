# Actual weighted typing-edge control and planar Hessian transfer

Object: C93-PLANAR-TYPING-EDGE-HESSIAN-TRANSFER-20261003-v1.
Author: OpenAI/Codex root01a0bbb5, acting for Dylan Roy — delegated AI work.
Disposition: AUTHOR-SIDE PROOF CANDIDATE; nonauthor technical review pending.
Personal reading PENDING; organizational independence 0; scientific effect NONE.

This note bounds the actual finite-radius determinant-weighted mass near the
two cubic typing edges and controls the Hessian-transfer loss across their
complement. It retains the finite-r density term. The model edge suppression
has antecedents in the QS addendum; the new scope is its actual weighted
field/jet transfer, with field-norm factors and full normalization.

## 0. Inputs and exact setting

Use exactly the model, pins and notation of C92 Theorem J: planar normalized
periodized Gaussian covariance on a fixed torus of side L>0; gap mark k=1;
birth b in a fixed nonempty compact set B0; every orthonormal frame; exact
pins at M=(-r/2,0), S=(r/2,0), values b,b-r^3 and zero gradients.
Q_r is the continuous Gaussian regression law at these pins. W_r is the
actual product of absolute Hessian determinants with the maximum/saddle
typing indicator. Z_r is its FULL expectation, Q_r^W=(W_r/Z_r)Q_r.

Set

    A=f_zz(0), lambda=-A/r,
    t=(gamma,B1,C3)=(f_xxz(0),f_xzz(0),f_zzz(0)),
    P=1+|gamma|+|B1|+|C3|,
    N=1+max_{|alpha|<=4} sup_torus |D^alpha f|,
    D_Lambda={|lambda|<=Lambda}, 0<Lambda<infinity fixed,
    mu_r(E)=r^(-5) E_{Q_r}[W_r 1_E] for jet events in D_Lambda.

Write rho_r(a,t) for the JOINT density of (A,t) under Q_r and rho_0 for its
contact limit. Define the two cubic typing quantities

    a_M=24lambda-gamma^2+12B1,
    a_S=24lambda+gamma^2-12B1,
    T={a_M>0,a_S>0},  h=min(a_M,a_S),
    w_lambda=(a_M)_+(a_S)_+/16,
    dmu_0=rho_0(0,t) w_lambda d lambda dt on D_Lambda.       (E1)

Thus T implies lambda>0, a_M+a_S=48lambda, and mu_0 is supported in T
up to a null boundary. The finite-r mu_r need not be supported in T: it
uses the actual endpoint typing, not the cubic typing.

The complete C92 proof is main229 comment5963825788, 19567 bytes,
SHA256 6fa4c3d6d1e8c3d8590c865802d5df061ad5b17652ddc7fd7bf5c5e8b8de084a.
Full nonauthor review5963946854: 24984 bytes, SHA256
298bbf9ccd75b57fde9d131551b32b9b5b3a5a7910e7c9df7ce796cdf3334fac.
We use J4/J5 and the pointwise inputs J9/J10/J16/J18/J19, with their full
fixed-parameter scope. Its underlying P/R sources and errata remain part
of that imported Gaussian interface; they are not silently reclassified.

The deterministic C91 proof is main229 comment5963566666, 12433 bytes,
SHA256 74a9ee276c3647276deb544c6d83e3cf21f708f55f9009fa4db5cc49c9d0e9aa.
Full review5963668996: 17914 bytes, SHA256
0c472af06e13f564d44c1723b5492c6c60681000f1f00d653b2bbb5f2e992eda.
Only W4/W5 and W15/W16 are used. Neither the QS/A2 trap implication nor
its containment/margin assumptions are proved or assumed satisfied here.
SOURCE_IDENTITIES.json carries exact source/extraction records.

Historical antecedent: QS addendum A1, main229 comment5961913750, already
has a MODEL typing-edge suppression estimate. Read it with its nonauthor
review5962025965 and author correction5962385282: the fixed-R integrated
sharpness sentence is withdrawn, and the corrected W3 cubic coefficient is
576000. Those sources are retained byte-exact in this packet. C93 does not
claim novelty for the model mechanism or import the withdrawn sharpness.
Its actual finite-r, correlated field-norm and full-normalization estimates
below are derived from C91/C92. No QS geometric implication is a premise.

## 1. The actual moment-weighted edge integral

For fixed finite p,q>=0, interpret expectations with N^p P^q as moments
under the ACTUAL field law; they are not observables of the limiting jets.
All constants below are finite and uniform in b and frame for 0<r<=r0,
and may depend on L,B0,Lambda,p,q. Put A_*=48Lambda.

**Theorem E.** For i=M or S and every nonnegative measurable phi on (0,A_*),

    r^(-5) E_{Q_r}[W_r N^p P^q 1_{D_Lambda intersect T} phi(a_i)]
          <= C_{p,q} integral_0^{A_*} phi(s)(s+r) ds.      (E2)

The inequality is valid as a nonnegative extended-integral statement; its
useful finite cases do not presume any untruncated inverse moments. For the
model measure, for finite q>=0,

    integral_T P^q phi(a_i) dmu_0
          <= C_q integral_0^{A_*} phi(s) s ds.            (E3)

In particular, for 0<delta<=delta0=min(1,A_*),

    mu_0(T intersect {h<=delta}) <= C delta^2,
    r^(-5) E_{Q_r}[W_r N^p P^q 1_{D_Lambda intersect T}
                                           1_{h<=delta}]
          <= C_{p,q}(delta^2+r delta).                    (E4)

After full normalization the second expression in (E4) gives

    E_{Q_r^W}[N^p P^q 1_{D_Lambda intersect T}1_{h<=delta}]
          <= C_{p,q} r^3(delta^2+r delta).                (E5)

The retained r delta term is essential to the argument; model suppression
alone has not been substituted for the actual measure. C92 also gives

    Q_r^W(D_Lambda intersect T^c)<=Cr^4.                  (E6)

The last bound includes finite-r jets outside the model typing domain.

### Proof of (E2)–(E6)

Let D_r=W_r/r^4 and condition further on A=-r lambda,t under Q_r. In this
section conditional expectations are always taken in C92's continuous
Gaussian regression version. C92 J10 and J16 give

    E[N^p | A=-r lambda,t] <= C_p P^p,
    |D_r-w_lambda| <= CrN(1+Lambda+|t|+rN)^3.

For p=0 the first assertion is just1; for any positive p<1 it also follows
from its p=1 case by Jensen. Multiplying the second inequality by N^p,
expanding its four terms, and using moments through p+4 yields

    E[D_r N^p | A=-r lambda,t]
          <= C_p w_lambda P^p + C_p r P^(p+4).          (E7)

This is stronger for edge integration than the bound C P^(p+4) alone.
It follows from the pointwise determinant comparison before taking moments,
not from multiplying a total-variation error by an unbounded function.
No independence of N, t or endpoint Hessians is used.

The exact Jacobian dA=r d lambda and W_r=r^4D_r give, for nonnegative
jet observables F,

    r^(-5) E_{Q_r}[W_r N^p F(lambda,t)]
      =integral F(lambda,t) rho_r(-r lambda,t)
                         E[D_r N^p | A=-r lambda,t] d lambda dt. (E8)

C92 J9 gives rho_r(-r lambda,t)<=C exp(-c|t|^2) on D_Lambda. Apply (E7)
inside (E8). On T change variables from B1 to s=a_i, holding lambda,gamma,C3
fixed. For i=M,

    B1=(s-24lambda+gamma^2)/12,

and for i=S,

    B1=(24lambda+gamma^2-s)/12.

Both absolute Jacobians are 1/12. In both cases

    0<lambda<=Lambda, 0<s<48lambda,
    a_other=48lambda-s, w_lambda=s(48lambda-s)/16.      (E9)

For every fixed finite m, the bound

    P^m exp(-c|t|^2)
       <= C_m exp[-c'(gamma^2+C3^2)]

holds uniformly in B1, by absorbing the polynomial into half of the
Gaussian exponent and then dropping the remaining B1 decay. Consequently
the gamma,C3 integrals are finite uniformly in lambda and s. Keeping the
vanishing factors in w_lambda, (E8) is bounded by

    C integral_0^Lambda integral_0^{48lambda}
                  phi(s)[s(48lambda-s)+r] ds d lambda.

Since 48lambda-s<=A_* and the lambda range has length Lambda, this is at
most C integral_0^{A_*} phi(s)(s+r)ds, proving (E2). The identical
calculation with rho_0(0,t) and no field norm gives (E3). Tonelli justifies
these changes for nonnegative measurable phi, even if either side is
infinite. There is no assumption of bounded t or a positive lower lambda
cutoff.

Use phi=1_{s<=delta}; the elementary integral is delta^2/2+r delta, when
delta<=A_*. A union over i=M,S proves (E4). C92's full normalization is
Z_r=r^2 z_r, with a fixed positive floor on z_r. Multiplying by r^3/z_r
proves (E5). Finally, mu_0(T^c)=0 and C92 J3 gives mu_r(T^c)<=Cr; divide
by the same full z_r and multiply by r^3 to obtain (E6). QED.

## 2. The inverse-moment threshold and the need for truncation

For each i and each fixed parameter choice,

    integral_T a_i^(-v) dmu_0 < infinity if 0<=v<2,
    integral_T a_i^(-v) dmu_0 = infinity if v>=2.        (E10)

The upper assertion follows from (E3) and integral_0^{A_*}s^(1-v)ds.
To prove the lower assertion, restrict lambda to [Lambda/3,2Lambda/3],
gamma,C3 to a fixed small box around0, and 0<s<s0 with
0<s0<min(1,8Lambda). Then 48lambda-s>=8Lambda. B1 as given in (E9)
stays in a compact set, the joint Gaussian density has a positive lower
bound there, and w_lambda>=c s. Thus the integral dominates
c integral_0^{s0}s^(1-v)ds, which diverges exactly when v>=2.
The same reasoning is uniform over compact birth/frame parameters.

For the loss factor

    L_i=1+(gamma^2+144)/a_i on T,

the same threshold holds for integral_T L_i^v dmu_0: the lower bound uses
L_i>=144/a_i; the upper bound uses a_i<=A_* and
L_i<=(A_*+gamma^2+144)/a_i together with (E3) and a polynomial jet weight.

For the actual field, (E2) instead supplies the truncated inequality, for
every finite v>=0, p,q>=0 and 0<delta<A_*,

    r^(-5) E_{Q_r}[W_r N^p P^q 1_{D_Lambda intersect T}
                                      a_i^(-v)1_{a_i>=delta}]
      <= C_{p,q} integral_delta^{A_*}[s^(1-v)+r s^(-v)]ds. (E11)

In the case v=3 this is at most

    C_{p,q}[delta^(-1)+r/(2delta^2)].                  (E12)

No statement of an untruncated actual inverse moment is inferred. For a
simple obstruction to such an inference, on (0,1) take g_0(s)=s and
g_r(s)=s+r. Their L1 distance is r, the model first inverse moment is1,
but integral_0^1 g_r(s)/s ds is infinite for every r>0. This is an exact
measure-theoretic counterexample to the inference, not a claim that these
are the Gaussian densities of the present field.

## 3. Actual probability of a Hessian-transfer failure

Let w>=1 with 2rw<=L/4. Let F_r,G,E_r=F_r-G be the raw field, cubic and
error of C92, and W_w={|X|,|zeta|<=w}. On T and gamma!=0, set

    kappa_i=a_i/(48gamma^2),
    T_i=[[1/sqrt(3), -1/(12sqrt(kappa_i))],
         [0,          1/(gamma sqrt(kappa_i))]],
    H_i(r,w)=sup_{W_w} ||T_i^T D^2 E_r T_i||_op.       (E13)

The supremum here is over raw points in W_w. It bounds the corresponding
rescaled Hessian on any set whose raw image is contained in W_w. It does
not assert that a geometric trap or ellipse is contained there.
These are measurable events: on the smooth-field event each supremum on
the compact raw window equals its supremum on a countable dense subset;
the matrices are measurable functions of the jets on their stated chart.

For any fixed deterministic tau>0, put

    epsilon=(115/72) r w^2/tau.

Whenever epsilon<=delta0, the actual weighted failure probability satisfies

    Q_r^W(D_Lambda intersect T intersect {gamma!=0}
                                      intersect {H_i(r,w)>=tau})
          <= C r^3(epsilon^2+r epsilon).               (E14)

The constant in this form is independent of tau,w; their effect is inside
epsilon. With tau fixed, w>=1 and epsilon<=delta0, this implies

    Q_r^W(D_Lambda intersect T intersect {gamma!=0}
                                      intersect {H_i(r,w)>=tau})
          <= C_tau r^5 w^4.                            (E15)

### Proof

C91 W4/W5 bounds each raw Hessian entry by (115/48)Nrw^2. Its exact
matrix transfer W16 therefore gives

    H_i(r,w)<=(115/72)Nrw^2 L_i.                       (E16)

The apparent gamma inverse in the coordinate matrix has cancelled in
this bound; gamma=0 itself remains outside the chart. There is no positive
lower bound imposed on |gamma| or on either a_i.

Under mu_r, split the event in (E14) into a_i<delta and a_i>=delta.
The first part is bounded by C(delta^2+r delta) using (E4). On the second,
the pointwise Markov inequality and (E16) give

    1_{H_i>=tau} <= epsilon^3 N^3 L_i^3.

Because a_i<=A_* on T,

    L_i^3 <= C_Lambda P^6 a_i^(-3).

Apply (E12) with p=3,q=6 to get an unnormalized rescaled bound

    C[delta^2+r delta+
                    epsilon^3(delta^(-1)+r delta^(-2))]. (E17)

Choose delta=epsilon. If epsilon=delta0=A_* the away set is empty except
a null boundary, and the strip bound alone gives the same conclusion;
otherwise (E12) applies directly. Then (E17) is
C(epsilon^2+r epsilon). Division by the full z_r and multiplication by
r^3 proves (E14). For fixed tau and w>=1,
r/epsilon=tau/[(115/72)w^2] is bounded, proving (E15). Using a third
moment rather than the critical second moment avoids a logarithmic loss.
All field-norm/jet correlations remain inside (E7)–(E12).

Under Q_r^W restricted to D_Lambda the jet law has a Lebesgue density by
C92 J18/J5. Hence gamma=0 is a null set and its exclusion adds no mass.
It does not create a coordinate chart at gamma=0. QED.

## 4. Simultaneous analytic conditions at the r^3 rare-layer scale

Fix deterministic positive budgets tau0,tauM,tauS. Define G_{r,w} inside
D_Lambda by

    T, gamma!=0, |E_r|_0<tau0,
    H_M(r,w)<tauM, H_S(r,w)<tauS.                       (E18)

Here |E_r|_0 is the raw value-error supremum on W_w. This is an analytic
good event; no global topological or model-decision assertion is built into
its name. For every fixed finite p>=1, and sufficiently small epsilon_i
as in (E14),

    Q_r^W(D_Lambda minus G_{r,w})
       <= C[r^4+r^5 w^4+r^3(rw^4)^p].                 (E19)

Constants may additionally depend on the fixed budgets and p. To prove
this, use (E6) for the outside-T term, the null gamma slice, (E15) for
both Hessian terms, and C92's weighted Taylor Markov argument for the value
term. That argument also handles the non-strict bad event |E_r|_0>=tau0,
since its pointwise bound is (K0Nrw^4/tau0)^p, K0=167/192. The union bound
requires no independence among these events.

In particular let w=r^(-beta), 0<=beta<1/4, and choose any fixed finite
p>=max(1,1/(1-4beta)). For sufficiently small r the physical window and
epsilon_i restrictions hold. Then (E19), C92 J5 and the positive mass floor
give

    Q_r^W(D_Lambda minus G_{r,w})<=Cr^4,
    Q_r^W(G_{r,w})=r^3 m_Lambda/z_0+O(r^4),
    Q_r^W(G_{r,w} | D_Lambda)=1-O(r).                  (E20)

The Hessian term is r^(5-4beta), of order at least r^4, and the value term
is r^[3+p(1-4beta)] with exponent at least4. This calculation uses a fixed
p chosen after beta, never a radius-dependent moment order. The scale and
conditioning in (E20) are those of the FULL actual determinant-weighted law.

## 5. Retained geometric and global obligations

For the C91 sufficient Hessian thresholds, one may take tauM=1 and
tauS=2/5; the strict bounds in G_{r,w} imply the corresponding weak/strict
requirements. A geometric application ALSO needs a valid imported trap
certificate, its raw sets contained in W_w, and its value tolerance at
least tau0. None of those events is proved likely by (E20). In particular
a random model tolerance tending to zero cannot be replaced by fixed tau0.
Such tolerances, containment and any model-decision exclusions must be
estimated and combined separately.

No unbounded-lambda or all-mark conclusion is asserted. The actual outside-
model-typing estimate here is C92's O(r^4) bound, not a sharper unproved
crossing estimate. The construction does not resolve A2's literal-v1
amendments, shrinking witness collisions, intermediate/coarea composition,
elder versus branch-adjacency identification, or the final persistence
coefficient/remainder. Model edge integrability is not presented as a new
geometric mechanism. Exact rational controls check the coordinate,
integration and scaling algebra; they do not prove the Gaussian analytic
inputs, topology, or canonical scientific completion.
