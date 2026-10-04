# Uniform compact-positive-gap comparison of the actual planar elder-failure measure

Object: C103-COMPACT-K-ACTUAL-FAILURE-COMPARISON-20261003-v1.
Actual author executor: OpenAI / Codex `/root` in this conversation, under
R17 claim b9eb31f0-1eee-4509-aafd-a821434f45b9 (WE656, heartbeat WE659).
The R17/native pickup uses the source-coordination label 01a0bbb5.
The originating root01a0bbb5 supplied author-side torus-transport,
endpoint-residual and optimized-checker findings; c93_edge_integral_audit
supplied author-side compact-K consumer reconstruction. Neither is a
nonauthor reviewer of this object. Dylan Roy — delegated AI work.
AUTHOR_SIDE / HOLD pending a fresh whole-object review.
Organizational independence 0; human review NONE; personal reading PENDING;
scientific effect NONE.

This is the full successor to the public step-1 lemma5967654152, not an edit
of it. Its full event proof is below. The old assert-based checker5967657529
is retained as historical, with its optimized-mode verification claim
withdrawn: a changed exponent failed normally but incorrectly printed PASS
under -O. The new controls use explicit raises and actual mutant reruns.
Controls do not prove the analytic theorem.

## 0. Exact population, inputs and theorem

Fix finite L>0, a nonempty compact set of births B0, and
K=[k_-,k_+] with 0<k_-<=k_+<infinity. Use all orthonormal planar frames
R=(u,e), of either orientation. The covariance is the original variance-one
periodized Bargmann-Fock covariance on X=R^2/(L Z^2):

    K_L(x)=sum_n exp(-|x+Ln|^2/2)/sum_n exp(-|Ln|^2/2).

No rotation invariance of the torus, amplitude rescaling of this random
field, or independence of its remainder from its jets is assumed.
Let Q_r=Q_{r,b,k,R} be continuous Gaussian regression at the physical pins

    M_r=x0-r u/2, S_r=x0+r u/2,
    f(M_r)=b, f(S_r)=b-k r^3, grad f(M_r)=grad f(S_r)=0.

Translation stationarity permits x0=0, but we retain it in path transport.
Let H_M,H_S be the actual physical Hessians and

    W_r=|det H_M det H_S| 1{H_M<0, index H_S=1},
    Z_r=E_Qr W_r=r^2 z_r, dQ_r^W=(W_r/Z_r)dQ_r.

The index counts strictly negative eigenvalues, and singular matrices
contribute zero. The normalizer is FULL, without a layer or event restriction.
Let H_r be the event that the finite ordinary-superlevel H0 class born at M_r
dies at S_r. It is defined false off the Borel Morse/distinct-value locus.
An essential maximum has no older endpoint and is a failure. Put
F_r=H_r^c and p_r=Q_r^W(H_r).

Physical midpoint jets and normalized raw jets are

    (A,a,beta,c3)=(f_zz,f_xxz,f_xzz,f_zzz)(0),
    y=(lambda,gamma,B,C)=(-kA/r,a,k beta,k^2 c3),
    t=(gamma,B,C), Pjet=1+|gamma|+|B|+|C|,
    N=1+max_{|alpha|<=4} sup_X |D_R^alpha f|.

The physical gap k varies in K. Only the deterministic normalized polynomial
has unit gap. This resolves the ambiguous “k=1” language in the original
pickup: no physical fixed-k assertion is being extended by notation alone.

Set a_M=24lambda-gamma^2+12B, a_S=24lambda+gamma^2-12B,
T={a_M>0,a_S>0}, and

    w(y)=(6lambda+3B-gamma^2/4)_+
          (6lambda-3B+gamma^2/4)_+.

Then w=a_M a_S/16 on T and zero elsewhere; 0<=w<=36(lambda_+)^2.
For gamma!=0 on T define

    D=gamma^2-12B, J=8gamma^3-144B gamma+576C,
    psi=24lambda/gamma^2, c=D/gamma^2, Rq=J/gamma^3,
    X=u-Z/12, zeta=Z/gamma,
    P_QS(u,Z)=2u^3-3u/2-1/2
                  -(psi+2cu)Z^2/48+Rq Z^3/3456.          (S1)

Let mu be the highest value P_QS(Y)+1 among extra nondegenerate saddles, and
-infinity when absent. C82/C98's finite guarded branches give a Borel mu
including degree drops, absent branches and tangencies. Write

    E={T,gamma!=0,mu<0}, Rsec={T,gamma!=0,mu>0}.

Let rho_{0,k} be the JOINT density of (A,a,beta,c3) at contact under
U0=(f,f_x,f_xx,f_xxx,f_z,f_xz)(0)=(b,0,0,12k,0,0).
Define, without dividing out its A marginal,

    g0(y)=k^-4 rho_{0,k}(0,gamma,B/k,C/k^2) w(y),
    z0=36k^2 E[A^2 1{A<0}|U0],
    nu_r^F(B)=r^-3 Q_r^W{y in B,F_r},
    nu_0^F(dy)=(g0(y)/z0)1_Rsec(y)dy.                  (S2)

Variation norm means sup_{|phi|<=1}|integral phi d(nu-nu')|, no factor1/2.

**Theorem.** There are C<infinity and r_*>0, uniform over b in B0,
k in K and all frames, such that

    ||nu_r^F-nu_0^F||_var<=C r^(1/4),
    1-p_r=r^3[alpha_1(b,k,R)+alpha_2(b,k,R)]
                                      +O_K(r^(13/4)).    (S3)

Here alpha_j are exactly CUB G11, not numerical coefficients or new count
moments. Their sum has a uniform positive lower and finite upper bound.
The conditional law of y given F_r consequently converges in variation at
this rate to nu_0^F/(alpha_1+alpha_2). No real height/location mark is added.

Exact controlling sources:
C101 proof5967063473,36333B,SHA256
300d0d18abb74332e593e389485c817a3c0ea7c31345194e3cfdd4039ac3b5c4,
review5967219096; C102 proof5967305153,28794B,SHA256
1a89b365bec20e353b84d5ac17b1acbe9179d48e4e4137e04d3c7e40ad207628,
review5967434317. C101's fixed-k event estimates are NOT themselves
assumed uniform in K: sections1–5 below reconstruct their consumers using
C102's uniform original-law inputs.

Retained mathematical interfaces:
C91's exact pinned C4 Taylor formula; C93's raw edge substitutions;
C94/C82's direct saddle-band integral; C95's corrected G, read as the ordered
pair (A2v1,three explicit repairs) and retaining its QS/CUB local premises;
C96's compact-manifold ordinary-global-elder identification; C97's chord
with TWO margins; C98's algebraic coverage/null polynomial; P's compact-K
endpoint residual/cap integration; CUB's classification and finite G11
integral. P is read with E1 inverse-square-root congruence, E2 Section9
replacement v1.1, REC wording W1 and strict chart embedding.
The immutable identities and consumed sections are in section9.
Original A2v1 remains AMEND. These interfaces are retained hypotheses, not
new acceptances of every assertion of the parent packets.

## 1. Uniform actual weighted laws, not a rescaled field law

Let Lambda>=1, H=1+Lambda, D_Lambda={|lambda|<=Lambda}.
Require r<=r0 and rH/k_-<=1, where r0 is C102's fixed compact-parameter
regression/normalizer cutoff. C102 Lemmas1–2 construct it from a positive
finite Fourier Gram floor uniform on O(2), summable covariance derivatives,
bounded contact targets and a compact-K minimum. They prove nonsingular
ten-observation regression, O(r^2) covariance/target errors, and

    rho_r(-r lambda/k,gamma,B/k,C/k^2)<=C exp(-c|t|^2),
    |rho_r(-r lambda/k,gamma,B/k,C/k^2)
                   -rho_{0,k}(0,gamma,B/k,C/k^2)|
                           <=CrH Pjet^2 exp(-c|t|^2),
    E[N^p|y]<=C_p Pjet^p, p>=0 fixed.                    (S4)

For p<1 use Jensen; p=0 is immediate. This is conditional regression on the
actual OWN ten observations, not a contact random-field coupling substituted
for the actual field. Compact K makes the physical/normalized jet norms
equivalent. No cutoff dependence is hidden in C_p.

Put D_r=W_r/r^4. With D_k=diag(1,k),

    F_r(X,zeta)=(f([x0+r R D_k(X,zeta)])-b)/(k r^3),
    Hess F_r=(k r)^-1 D_k R^T H R D_k.

In dimension2 the determinant factor is exactly one in
H/r=k D_k^-1(Hess F_r)D_k^-1, and inertia is preserved. Hence D_r is
the product of the two filtered determinants of Hess F_r, with no extra k^4.
C102(4.8), multiplying by N^p BEFORE conditioning, gives

    E[|D_r-w|N^p|y]<=C_p rH^3 Pjet^(p+4),
    E[D_r N^p|y]<=C_p w Pjet^p
                               +C_p rH^3 Pjet^(p+4).     (S5)

This follows by expanding rN(H+Pjet+rN)^3 and applying S4.
Filtered determinants, not their discontinuous index indicators separately,
are continuous across type boundaries.

The physical-jet Jacobian is r/k^4. Therefore for field-dependent Phi>=0,

    mu_r(Phi;D_Lambda)=r^-5 E_Qr[W_r Phi;D_Lambda],
    g_r(y)=k^-4 rho_r(-r lambda/k,gamma,B/k,C/k^2)
                                             E[D_r|y],
    r^-3 E_QrW[Phi;D_Lambda]=mu_r(Phi;D_Lambda)/z_r.   (S6)

Tonelli justifies the identities. C102 supplies the full floor and rate

    |z_r-z0|<=Cr, 0<z_*/2<=z_r, z_*<=z0<=z^*,
    E_Qr[(W_r/r^2)N^p]<=C_p.                             (S7)

Gaussian polynomial absorption, w<=36lambda^2 on T, and the lambda interval
length then give

    mu_r(N^p Pjet^q;D_Lambda)<=C_(p,q)H^3,
    integral_D Pjet^q|g_r/z_r-g0/z0|<=C_q rH^4,
    mu_r(D_Lambda intersect T^c)<=CrH^4.                 (S8)

All constants are independent of Lambda. The first bound also follows from
H^3+rH^4<=C_K H^3 under rH<=k_-.
The off-T statement is actual finite-r leakage, not a null-set claim.

## 2. N-weighted edge strips and truncated inverse integration

For either i=M or S change B to s=a_i:

    B=(s-24lambda+gamma^2)/12, i=M;
    B=(24lambda+gamma^2-s)/12, i=S.

The absolute Jacobian is 1/12 in both cases. On T,
0<lambda<=Lambda, 0<s<48lambda and w=s(48lambda-s)/16.
Using S4–S5 gives the joint N^pPjet^q weighted density majorant

    C exp(-c|t|^2)[w Pjet^(p+q)+rH^3 Pjet^(p+q+4)].

Bound the B-polynomial times its Gaussian uniformly in B while retaining
Gaussian decay in gamma,C. Integrating the lambda interval yields for every
nonnegative phi

    mu_r(N^pPjet^q;T phi(a_i))
        <=C_(p,q) integral_0^(48Lambda)
                            phi(s)[H^2 s+rH^4] ds.       (S9)

The model jet-only version (p=0) has no r term. No model field norm N is
defined, and no N-weighted bound is obtained by multiplying a jet-only TV
estimate. In particular for 0<delta<=1,

    mu_r(N^pPjet^q;T,min(a_M,a_S)<=delta)
                           <=C(H^2delta^2+rH^4delta).    (S10)

On a_i>delta inverse powers v=3,4,6 are bounded respectively by

    C[H^2/delta+rH^4/(2delta^2)],
    C[H^2/(2delta^2)+rH^4/(3delta^3)],
    C[H^2/(4delta^4)+rH^4/(5delta^5)].                  (S11)

These are the integrals of H^2 s^(1-v)+rH^4 s^-v.
Only truncated moments are used. The finite-r strip correction is retained.

## 3. Compact-K deterministic errors and their ACTUAL weighted probabilities

Put w0>=5, e=rw0^4, and require r(1+k_+)w0<=L/4.
C102(4.5), from C91's pin correction with all mixed derivatives, gives

    |F_r-G_y|_j<=K_j N r w0^(4-j), j=0,1,2,
    K0=9/(64k_-)+1/16+(1+k_+)^4/(24k_-),
    K1=33/(128k_-)+1/16+max(k_-^-1,1)(1+k_+)^3/6,
    K2=17/(48k_-)+1/24+max(k_-^-1,1,k_+)(1+k_+)^2/2.     (S12)

These finite constants depend only on K. At k_-=k_+=1 they are exactly
167/192,635/384,115/48. Let E0 be the value supremum, so E0<=K0 N e.

The normalized cubic G_y is IDENTICAL as a polynomial to C101's cubic.
Consequently all following algebra concerns G_y, regardless of k; its
probability and remainder bounds are obtained here under the ORIGINAL Q_r.

### 3.1 Radius and selected-sector value tolerance

C95's corrected G and C97 give raw-square-containing radius bounds

    Rbox=3/2+(5/2)(|gamma|+12)/sqrt(24lambda),
    Rch=5/2+3(|gamma|+12)/sqrt(24lambda).                  (S13)

They include the whole controlled axis and the two pin ellipses, not just a
trap component or saddle. If either exceeds w0, use
U=min(Lambda,C(|gamma|+12)^2/w0^2) in the two-variable edge integral.
Before its fixed Jacobian the exact elementary integrals are

    integral_0^U integral_0^(48lambda) w ds d lambda=288U^4,
    integral_0^U integral_0^(48lambda) 1 ds d lambda=24U^2.

S4–S5 and Gaussian polynomial integration give

    mu_r(N^pPjet^q;T,Rbox>w0 or Rch>w0)
                            <=C(w0^-8+rH^3w0^-4).       (S14)

On E, C98 coverage supplies C94's selected-sector inequalities even for
absent/exceptional branches. C94's local algebra, in the normalized cubic,
gives v=min(m_S,epsilon_M)>=c_*a_S^2, where

    c_*=3/[250(48Lambda)^2].

The selected G tolerance is eta=min(v,-mu)/2. If E0>=v/2, then
epsilon_V N/a_S^2>=1 with epsilon_V=2K0e/c_*<=C_V H^2e,
C_V=500K0*48^2/3. Split at a_S=sqrt(epsilon_V)<=1, use S10, and use
squared Markov with S11(v=4) away from it. This yields

    mu_r(E,E0>=v/2)<=C[H^4e+rH^5sqrt(e)].                 (S15)

No random-width strip was replaced by a deterministic variable-width
enclosure; N is multiplied into the weighted measure before integration.

### 3.2 Rejected endpoint tolerance: BOTH margins

For the Borel highest extra saddle Y in Rsec let h=-P_QS(Y)=1-mu.
Euler's identity at the critical displacement from M gives h=rho^2/3 and
h>=4/(27tau_M^2)>0. Therefore 0<mu<1. Exact pole cancellation gives

    tau_M=(1/sqrt(3))[2/3+2|D|/a_M+|J|/(6a_M^(3/2))],
    tau_M^2<=C_T H^3 Pjet^6/a_M^3,
    C_T=(4/9)48^3+676*48+728^2/36,
    h>=4a_M^3/(27C_T H^3 Pjet^6).                       (S16)

Here |D|<=13Pjet^2, |J|<=728Pjet^3 and a_M<=48Lambda.
C97's whole-chord formula is

    P_QS(M+t(Y-M))=h(2t^3-3t^2), 0<=t<=2.

Its minimum is -h=-1+mu, and its endpoint is 4h>0.
A sufficient actual-field condition is

    E0<(1/2)min(mu,4h).                                 (S17)

Both endpoint and intervening-path margins are essential. Split the bad event
E0>=2h at a_M=epsilon_H^(1/3), where
epsilon_H=27K0 C_T H^3 e/8. Squared Markov with N^2Pjet^12 and S11(v=6)
gives

    mu_r(Rsec,E0>=2h)
                    <=C[H^4e^(2/3)+rH^5e^(1/3)].        (S18)

No reference independence is needed; this is under mu_r itself.

### 3.3 Decision level near zero

For each fixed t, d lambda=(gamma^2/24)d psi and

    w d lambda=(gamma^6/384)(psi^2-c^2)d psi.

C82's direct finite-branch saddle-band integral, consumed by C94, gives
for 0<delta<=1/2 the bound
delta[(1024/3)|c|^3+64Rq^2]. Multiplication cancels the chart poles:
gamma^6|c|^3=|D|^3 and gamma^6 Rq^2=J^2.
C102's contact density has a UNIFORM compact-K Gaussian majorant in t;
therefore its actual joint reference slice, including k^-4, absorbs these
polynomials without any independence assumption. Extend the nonnegative
lambda integration beyond Lambda to obtain

    mu_0(T,|mu|<=delta)<=C delta,
    mu_r(T,|mu|<=delta)<=C(delta+rH^4).                  (S19)

The second estimate uses S8 before normalizing; z_r,z0 are bounded.
For 0<d<=1/4, squared Markov of E0<=K0Ne and S8 give

    mu_r(E or Rsec,E0>=|mu|/2)
                       <=C[d+rH^4+H^3(e/d)^2].          (S20)

For mu=-infinity the event is empty, so no undefined finite division is used.

### 3.4 Actual raw-to-QS Hessian transfer

Let T_gamma=[[1,-1/12],[0,1/gamma]], the derivative of
(X,zeta)=(u-Z/12,Z/gamma). Let J_i=diag(1/sqrt(3),1/sqrt(kappa_i)),
where kappa_M=a_M/(48gamma^2), kappa_S=a_S/(48gamma^2).
The Frobenius square, hence an upper bound for the operator square, is

    ||T_gamma J_i||_F^2
       =1/3+(gamma^2+144)/(3a_i)=L_i/3,
    L_i=1+(gamma^2+144)/a_i<=C H Pjet^2/a_i.             (S21)

Thus S12's bound on all second partial derivatives implies

    H_i^err:=||J_i D^2(F_r-G_y)_QS J_i||
                     <=(2K2/3)N r w0^2 L_i.             (S22)

There is no standalone gamma pole. The raw law includes gamma=0; this
chart estimate excludes it on a null set rather than assigning a value there.
At tolerances tau_M^tol=1,tau_S^tol=2/5 put
epsilon_i=(2K2/3)rw0^2/tau_i^tol. Require epsilon_i<=1.
Split at a_i=epsilon_i. On the complement use THIRD Markov with
N^3Pjet^6 and S11(v=3), retaining L_i<=C H Pjet^2/a_i:

    mu_r(T,H_i^err>=tau_i^tol)
                        <=C[H^5r^2w0^4+H^7r^2w0^2].     (S23)

Indeed the away term is bounded by
C H^3 epsilon_i^3[H^2/epsilon_i+rH^4/(2epsilon_i^2)];
the near term from S10 is smaller since H>=1.
A common sufficient smallness constant is C_eta=5K2/3.

The common admissibility list is

    r<=r0, Lambda>=1, rH/k_-<=1, w0>=5,
    r(1+k_+)w0<=L/4, e<=1, C_VH^2e<=1,
    (27K0C_T/8)H^3e<=1, C_eta rw0^2<=1, 0<d<=1/4.      (S24)

Every constant in it is fixed before Lambda,w0,d are chosen.

## 4. Actual torus event: exact transport, trap and TWO-margin rejection

The periodic lift F_r(y) in S6 is a function on R^2 whose lattice is

    L_r=(r R D_k)^-1(L Z^2).

The induced map R^2/L_r -> X, [y]->[x0+r R D_k y], is a diffeomorphism.
It is NOT in general a self-map of the original side-L square torus.
Positive affine height scaling and this diffeomorphism carry paths, their
minima, and the predicate “endpoint above birth” exactly. Alternatively,
each physical torus path has a unique lift from the chosen starting lift,
and every finite lifted path projects to the torus, winding allowed.
Consequently with F_r(M)=0,F_r(S)=-1,

    D_f(M_r)=b+k r^3 d_{F_r}(M),                         (S25)

where d uses all paths to a point of height>0 on the transformed compact
torus, equivalently their periodic lifts. If no higher endpoint exists,
both sides use the empty-family value -infinity. No compact-manifold
persistence theorem is applied to the noncompact lift.

On E and the simultaneous good event Rbox<=w0,
E0<eta=min(v,-mu)/2, H_M^err<1,H_S^err<2/5, the exact pins plus S12/S22
supply all hypotheses of C95's corrected geometric interface G.
That interface controls the entire compact trap and axis, not merely
values at the two endpoints. Applying its boundary barrier to the globally
continuous periodic lift proves d_{F_r}(M)<=-1: every path to a point
above birth first exits the trap, where its value is at most -1.
The controlled axis through S to its endpoint at X=3/2 supplies a path of
minimum -1 and an endpoint of positive height. Hence d_{F_r}(M)=-1 and
the path family is nonempty. The embedding inequality in S24 guarantees
the local control patch is embedded; it does not prohibit exterior winding.

On Rsec, choose the highest extra nondegenerate saddle by the finite C82
branches and a Borel lexicographic tie rule. With Rch<=w0 and S17, its
whole chord projects to an actual torus path of minimum STRICTLY above -1,
and its doubled endpoint is STRICTLY above birth. S25 therefore gives
D_f(M_r)>f(S_r), so the designated pair is not selected.

On the physical compact torus, P section8 supplies pinned Morse/distinct
critical values at each fixed parameter and r. Absolute continuity transfers
this locus to Q_r^W. C96's compact-manifold deterministic equivalence then
identifies D_f(M_r)=f(S_r) with the finite ordinary-superlevel H0 event H_r.
If M_r is essential, the absence of a higher endpoint makes H_r false;
the selected good event explicitly supplies one. No adjacency or
Morse-Smale premise is inserted. These statements need not hold on a single
common probability-one set for uncountably many parameter laws.

Measurability is retained, not guessed from tests. The maximin is Borel by
strict rational path tests on the physical compact torus, as in P/E2/C96.
Finite branch selection, its rational chord supremum, and the local norm
suprema are Borel. On T, C98 proves mu<0 implies the additional elder-sector
inequalities of G, including no-saddle/exceptional branches. The remaining
neutral boundary is contained in

    J^2-16(24lambda-2D)^2(24lambda+D)=0,                 (S26)

a nonzero polynomial in C with leading coefficient576^2.
It and gamma=0 are Lebesgue-null under both C102 joint densities.
No neighborhood estimate is inferred from nullity; S19–S20 supply it.

Collect S14,S15,S18,S20,S23 and the two null exclusions. Put

    Rerr=w0^-8+rH^3w0^-4
          +H^4e+rH^5sqrt(e)
          +H^4e^(2/3)+rH^5e^(1/3)
          +d+rH^4+H^3(e/d)^2
          +H^5r^2w0^4+H^7r^2w0^2.                      (S27)

On T the actual H_r indicator equals E except on those bounded bad events.
Off T the complements need not agree; add the ENTIRE actual leakage from S8.
Using the full normalizer floor exactly once gives

    r^-3 Q_r^W{D_Lambda,H_r symmetric_difference E}
                                                   <=C Rerr,
    ||nu_r^F|D_Lambda-nu_0^F|D_Lambda||_var
                                                   <=C Rerr. (S28)

For the second inequality replace 1_F_r by 1_Rsec on the typed domain,
add off-T leakage, and use S8's normalized joint-density comparison against
the same raw-jet indicator Rsec. Taking the supremum over |phi(y)|<=1
proves variation; no transported real-valued mark is substituted.

## 5. Uniform ACTUAL endpoint-residual failure tail

The endpoint transverse scalar ell_end=-f_zz(M_r)>0, not the midpoint A or
normalized lambda, is the scalar to which P section4's regression applies.
Under Q_r, before tilting, it gives an independent residual g_r; write
J_r=1+||g_r||_C4. P's compact-positive-K proof provides a bounded scalar
density and uniform moments of each fixed order of J_r, with

    ||f||_C4<=C_K(J_r+ell_end).

Its global good-cap implication gives F_r subset Gcap,r^c up to weighted null
sets; it includes the essential maximum convention. P(7.5) splits depth
failure into

    near:0<ell_end<=C_K r J_r^2,
    far:ell_end>c_K/r.

On near, P(6.2) and the derivative bound give

    W_r<=C_K r^2 J_r^4 ell_end(ell_end+C_K r J_r^2).

For A>=1 retain the SAME J_r>A indicator in the independent scalar integration:

    E_Qr[W_r;near,J_r>A]
      <=C_K r^2 E[J_r^4 1_{J_r>A}
            integral_0^(C_K r J_r^2) l(l+C_K r J_r^2)dl]
      <=C_K r^5 E[J_r^10;J_r>A].                       (S29)

The event and determinant need not be independent of either variable; only
the endpoint residual/scalar regression independence, before W tilt, is used.
The midpoint derivative inequality gives on near

    |lambda|=k|A|/r
       <=k[ell_end/r+(1/2)sup|f_xzz|]<=C_K J_r^2.       (S30)

Thus for every fixed integer m>=1, using the actual residual moment
J_r^(10+2m), S29 yields the scaled near tail C_m Lambda^-m.
When the threshold (Lambda/C_K)^(1/2)<1, enlarge the constant and use the
unrestricted near integral. P(7.6),(7.7), uniformly for k>=k_-, bound the
far and fourth-derivative exceptions in tilted probability by O(r^4).
Their r^-3-scaled contribution is O(r), not omitted. S7 gives

    nu_r^F(D_Lambda^c)<=C_m Lambda^-m+Cr.               (S31)

This does not use the local restriction rH/k_-<=1.
An unconditional C4 tail or midpoint residual cannot replace S29.

## 6. Model failure tail and positive coefficient

In CUB coordinates theta=(s,a,beta,c3), use
s=-lambda/k,a=gamma,beta=B/k,c3=C/k^2. Its shear variables are

    Bsh=(B-gamma^2/12)/k=-D/(12k),
    Dsh=(C-gamma B/4+gamma^3/72)/(2k^2)=J/(1152k^2).

CUB G13 on n>0, with x=-s=lambda/k, gives

    lambda<=2|B-gamma^2/12|+(48/1152^2)^(1/3)|J|^(2/3)
                                                     <=C Pjet^2. (S32)

This follows by multiplying
x<=2|Bsh|+(48kDsh^2)^(1/3) by k; all k powers in the second term cancel.
Also CUB's s-integrated marked weight is bounded by
384k^2|Bsh|^3+2304k^3Dsh^2, a fixed polynomial majorant in t uniform on K.
The measure g0(y)dy is exactly CUB's contact measure:
dtheta=k^-4dy and its endpoint determinant product is w(y).
There is neither a missing jet Jacobian nor an additional determinant k^4.

CUB classifies every extra critical point in (-k,0) as a nondegenerate saddle;
C101/C98's exact Euler height identity gives negative height at every finite
extra point. Hence its n>0 is Rsec off the named polynomial-null boundaries.
The transformed polynomial G_y has window (-1,0), as required here.
S32 forces Pjet^2>Lambda/C when lambda>Lambda. The compact-K Gaussian
majorant in S4 absorbs the fixed integrated weight polynomial, so

    nu_0^F(D_Lambda^c)<=C_m Lambda^-m.                  (S33)

This is a MARKED tail, not an attempted finite exhaustion of the unmarked
soft measure whose layer mass grows as Lambda^3.

CUB G11 therefore identifies

    M_F=nu_0^F(R^4)=alpha_1+alpha_2.                     (S34)

For a uniform lower bound, choose a fixed open ball strictly inside each of
the normalized polynomial's n=1 and n=2 sectors. Such balls exist by mapping
CUB's explicit interior examples at k=1 into normalized y. The G_y sectors
are independent of the parameter k, while the contact joint density has a
uniform positive lower bound on each smaller compact ball for compact b,k,R.
The weight is uniformly positive on the ball, and z0 has a uniform finite
upper bound. S32–S33 give the finite upper bound. Thus
0<M_*<=M_F<=M^*<infinity uniformly. Each event counts once, so the sum is
alpha_1+alpha_2, NOT alpha_1+2alpha_2. Finite-r birth independence is not
asserted.

## 7. Fixed beta1/4 balance, uniform cutoff and consumer

Choose, only now,

    Lambda=r^-1/12, H=1+Lambda<=2r^-1/12,
    w0=r^-1/32, d=r^1/4, e=r^7/8, m=3.                 (S35)

Every admissibility condition in S24 holds for all sufficiently small r
uniformly on the fixed compact parameters. Its vanishing powers are
rH/k_-:11/12; r(1+k_+)w0:31/32; e:7/8;
H^2e:17/24; H^3e:5/8; rw0^2:15/16; d:1/4.
Choose a cutoff below r0 and below the finitely many positive thresholds
given by these powers and their fixed constants, also ensuring w0>=5 and
d<=1/4. This is an existential uniform analytic cutoff, not a computed
accuracy window.

Every term of S27/S31/S33 has the following exact exponent:

| Term | r exponent |
|---|---:|
| w0^-8 | 1/4 |
| rH^3w0^-4 | 7/8 |
| H^4e | 13/24 |
| rH^5sqrt(e) | 49/48 |
| H^4e^(2/3) | 1/4 |
| rH^5e^(1/3) | 7/8 |
| d | 1/4 |
| rH^4 | 2/3 |
| H^3(e/d)^2 | 1 |
| H^5r^2w0^4 | 35/24 |
| H^7r^2w0^2 | 65/48 |
| Lambda^-3 | 1/4 |
| scaled far/derivative exceptions | 1 |

The actual tail uses fixed J_r^16 and the model tail a fixed degree12
Gaussian jet moment, with no moment order increasing with r.
Combine S28 and the two omitted nonnegative tail masses S31/S33 to prove
the first part of S3. Apply it to phi=1, use S34, and multiply by r^3
to prove the scalar consumer. Positivity gives for small r a uniform positive
failure mass after r^-3 scaling. The elementary positive-mass normalization
inequality then gives the conditional raw-jet conclusion with the same rate.
No full unmarked Boolean law on all jets is claimed: its scaled unmarked
mass diverges, whereas the failure-marked measure is finite.

## 8. Scope and evidence firewall

The genuinely new implication is that C101's quantitative actual event/tail
rate is now uniform over a fixed positive compact gap interval, using
C102's ORIGINAL compact-K Gaussian law, exact Jacobian/determinant ledger,
and the above deterministic consumers. It is not an extrapolation of C101
by rescaling random-field amplitude.

All constants and sufficiently small radii depend on finite L,B0,K.
There is no k->0, growing K or L, endpoint beta1/2, rate optimality, d>=3,
another covariance, whole-field TV, real-valued-mark TV, or all-bars theorem.
It does not turn rejected candidate pairs into once-counted replacement bars.
It does not identify every small finite bar with this pair population or
close shrinking multiple-witness, small-gap/intermediate/coarea, or
Conjecture7. The other owner's retained lane is untouched.
No repository application, commit, hosted CI, merge, deployment, human
reading or organizationally independent review is implied.

The original A2v1 literal false lines remain AMEND. We consume only C95's
additive corrected G with its exact local premises and C98 coverage.
P/E1/E2/REC and C96 supply fixed-law genericity, Borel mark and ordinary H0
identification; successful finite controls cannot supply those hypotheses.
The rational controls check finite formulas and reject explicit false
inferences. They do not substitute for this argument or its fresh review.

## 9. Source custody and actual exposure

All following full snapshots were freshly compared to their native bodies
or immutable Git blobs, not just to old headers. C96's 7913B native body
contains its 7657B mathematical suffix; the two identities are distinguished.

| Source | native ID / Git blob | UTF-8 bytes | SHA256 |
|---|---|---:|---|
| C91 | 5963566666 | 12433 | 74a9ee276c3647276deb544c6d83e3cf21f708f55f9009fa4db5cc49c9d0e9aa |
| C92 | 5963825788 | 19567 | 6fa4c3d6d1e8c3d8590c865802d5df061ad5b17652ddc7fd7bf5c5e8b8de084a |
| C93 | 5964167051 | 15545 | f25f86cc66ae335b4832ea53670646815567ec7854fa0386f8c57f6939e0af1c |
| C94 | 5964517708 | 15407 | 0fe4fa2028f8ddbbf5a79df3879bcbd3789f19409fb44ad739caeabedff1af3c |
| C95 | 5964938563 | 16185 | c0d9ee72352fafe91f96a8b6187c978f09ee3c187d5f4c7c2462c0187750d2e1 |
| C96 full native | 5965141133 | 7913 | 0758b5de8f4d9e4658ca3c6cf3e52c23d8e12f77999e9c3668ef0bedb15a05f5 |
| C97 | 5965421543 | 16098 | acf83958e6ea650d83bf811b2beacc03b553637dc4a3160012567c7f0a300a57 |
| C98 | 5965738339 | 15050 | 3ca1622197bf22cf71ab64f2938ecc0b022ed09487b691d50ae8d2ad1f46d198 |
| C101 | 5967063473 | 36333 | 300d0d18abb74332e593e389485c817a3c0ea7c31345194e3cfdd4039ac3b5c4 |
| C102 | 5967305153 | 28794 | 1a89b365bec20e353b84d5ac17b1acbe9179d48e4e4137e04d3c7e40ad207628 |
| P | dfed3b8d318a3ab1950957f393307733a4bef3f2 | 40261 | 9350ad6eaba6626b93c3dedeef9e2ff816e5cdf1c8318e85fb27499141c84bc7 |
| E1 | 213594d6ca6a86fb938110f4d166d9ce275a02d0 | 1782 | bad7ef609c4ad8c41ad6af562c1b6807921e19a9d556ed793ad1a0db6e202028 |
| E2 | fe9b9ce4999908bb3814b500ee2d0ceb0c6f704a | 9062 | 845abf9f9c99d672c2a10a887b5a2e7206a3d2de3d876f35f75ff6e2dc13e62f |
| REC | 75da2597971510f843f8d90c743950cb8c177342 | 23312 | 451b9d7ffee072a73fc904cab891b6693e3f233808b89df10cce1b57036b65da |
| CUB | bb446d08db8a944537a743ad550b88c1c2ad5758 | 19889 | 117e9299a71e6139270266889eb772ed97518e402d9af029bbdb67caf9d4a0f0 |
| ELDER | ef2aa57959ea9f721bbf2316ce94cf616c1c9113 | 39722 | f68038be79b46124b0f9b31205aa6e3682b34b6f5ef81f4a5697ae81f07cc46b |

Full native controlling inputs:
[C101](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5967063473),
[C102](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5967305153),
[corrected G/C95](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5964938563),
[C96](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5965141133),
[C97](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5965421543),
[C98](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5965738339).
The six immutable Math- objects are pinned at commit
044d42d5bd7f31df6f7e6b9034d6711e8fb7ee43, with exact paths in the
attached SOURCE_IDENTITIES.json. C82 mathematical prefix5959920397
(11253B SHA256f390ad99b07ec4eda9160191d776cfc3a53ca628976165987d9a61ab79816827)
and QS5961415030's local premises are retained through C94/C95/C97;
they are not missing invented carriers. A1 correction5962385282,
A2v1 and C90's three repairs remain explicit in C95.

Author executor had prior C91–C99 source/review and C101 authorship exposure.
The originating coordinator and c93_edge_integral_audit are author-side
contributors here. The fresh whole-object reviewer must exclude all these
contributors from acceptance credit. Same-provider review earns zero
organizational independence regardless of account or conversation.
