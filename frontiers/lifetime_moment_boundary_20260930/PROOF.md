# Actual lifetime moments: axial escape, finite-death moments, and the essential class

30 September 2026. Additive local analytic proposal, not a parent source edit or acceptance decision. R17 claim `19650bdb-2c21-42b9-b4a9-d67cabb12d4c` / Work Event 319; exact public scope pickup on Math- #175 comment 5907574791. Root owns integration; no branch write is authorized before review.
Authors: the reader_first_independent_review OpenAI subagent and the root OpenAI agent. Root supplied the clipped-moment formulation and independently reconstructed the essential-class support argument; the subagent supplied the axial escape lemma and its finite-death uniform-integrability consequence. This is author-side technical work with zero organizational-independence credit. It does not repeat the completed exact-head reviews of the existing proofs.

## Source boundary and current ownership

At 08:44:53 UTC, fresh GitHub reads returned:

- Math- #175: open draft, head `9c6a73489c5ed2465a3cf65dcc950eeeae074b05`, base `8d48d02a6a580666a879d719a9e61f460baa5f40`. Its marks/lifetime slice already has same-provider review 5363612238. Its consumed `frontiers/concave_fibre_elder_20260930/PROOF.md` is SHA256 `5681896a6808f48fb7508914d0860ec508af7646e9e706fc260d935dd951c75e`.
- Math- #170: open draft, head `79f18f0cb318fceccd5bdf4e6dad29815165bc7d`, base `358f2562efbccc59f9549e5a79650e2e936395c3`. Its remaining rare-measure/marks/lifetime slice already has same-provider review 5363625339. Its consumed `frontiers/local_elder_geometry_20260930/PROOF.md` is SHA256 `f68038be79b46124b0f9b31205aa6e3682b34b6f5ef81f4a5697ae81f07cc46b`.
- Parent P: `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md`, commit `ab13a08f5e5b0adc7a7d80cf643d9b5a0618507f`, blob `dfed3b8d318a3ab1950957f393307733a4bef3f2`, SHA256 `9350ad6eaba6626b93c3dedeef9e2ff816e5cdf1c8318e85fb27499141c84bc7`.

Cached bytes were rehashed before this derivation. Exact consumed source bytes are retained under `sources/` beside this note; immutable URLs, commits, Git blob IDs, SHA256 values, byte counts, consumption roles, and every retained reading rule are in [SOURCES.json](SOURCES.json). Relevant source slices are #175 §§1,5–6; #170 §§8.1,8.7–8.8; P §§2,4–5,7–8. P §12 concerns integrated finite-bar intensity moments, which are a different estimand. The full parent identity set includes P, CAP, the congruence erratum ERR, Borel replacement BOREL, and reconciliation REC. Their reading rules remain in force; no new formal alignment or scientific acceptance is claimed here.

The bounded question is what the existing actual failure-mark weak law implies about moments of the actual lifetime fraction. Its intentional weak scope is not a defect. The conclusion below is stronger than a generic statement that weak convergence needs an extra uniform-integrability assumption: the original pin constraints and already available all-order global moments supply that assumption for the finite-death submeasure.

## Exact estimand

Fix the parameters and the original pinned Gaussian law of the relevant source, in dimension 2 for #170 or a fixed dimension at least 3 for #175. Retain the reconciliation embedding restriction r<L/(4 sqrt(2)); reduce r further whenever required by the parent normalizer floor. In an embedded axial chart let

    M=(-r/2,0), S=(r/2,0),
    f(M)=b, f(S)=b-k r^3, grad f(M)=grad f(S)=0, k>0.

Keep the original weight and full normalizer

    W_r=F_d(H_M) F_(d-1)(H_S), Z_r=E_Q W_r,
    Q_r^W=(W_r/Z_r)Q_r.

Let F_r be failure of S to be the ordinary elder partner, and let E_r be the essential event d_f(M)=-infinity. Under Q_r^W, M is a maximum; E_r is contained in F_r. Define the extended lifetime fraction

    X_r=(b-d_f(M))/(k r^3) in [0,infinity].

For finite deaths it is nonnegative because every path in the death definition includes M, so d_f(M)<=b. Define its clipped version C_r=min(X_r,1), setting C_r=1 on E_r. A location outside the local chart is not a reason to replace an available finite death height by a sentinel.

Assume the source's failure-mark conclusion: r^-3 Q_r^W(F_r)->a>0 and the finite marked measures converge weakly, with isolated sentinel mass o(r^3), to mu_fail and lifetime fraction lambda(theta)=-h_*(theta)/k in (0,1). Here a=a_fail in #175 and a=alpha_1+alpha_2 in #170. Put

    m_q=integral lambda(theta)^q dmu_fail(theta), q>0.

Thus 0<m_q<a. No replacement-bar counting intensity is introduced.

## 1. Bounded corollary from the stated weak law

For every fixed q>0,

    r^-3 E_QW[C_r^q;F_r] -> m_q,
    E_QW[C_r^q | F_r] -> m_q/a.                     (B1)

Proof: on finite death marks use the bounded continuous function

    t -> min(max(-t/k,0),1)^q

of D_r=(d_f(M)-b)/r^3, and assign value 1 at the isolated essential sentinel. Its limit is lambda^q because the limiting death lies in (-k,0). The exceptional position sentinel is irrelevant to this test. Divide by r^-3 Q_r^W(F_r)->a for the second formula. This is only a corollary of the stated weak law.

## 2. Deterministic axial escape lemma

Let g(x)=f(x,0) on [a,e]=[-r/2,3r/2] in the embedded chart; put c=r/2. Let H be the supremum of the absolute fourth directional derivative along that segment. If

    r H <= 3 k,                                         (A1)

there is a path from M to a point with field value greater than b whose minimum is exactly f(S). In particular

    d_f(M)>=f(S), E_r cannot occur, and 0<=X_r<=1.       (A2)

This assertion does not say S is the actual partner. Another path can give an earlier death at a higher level.

Proof: the exact cubic Hermite interpolant at a,c is

    p(x)=b+k r^3 [2(x/r)^3-(3/2)(x/r)-1/2].

It has p(a)=b, p(c)=b-kr^3, p'(a)=p'(c)=0 and p'''=12k. Since g-p has double zeros at a and c, repeated Rolle's theorem gives xi in (a,c) with g'''(xi)=12k. For every x in [a,e],

    g'''(x)>=12k-2rH>=6k>0.

Therefore g' is strictly convex, has its exact zeros at a,c, is negative on (a,c), and is positive on (c,e]. Consequently g has its minimum on [a,e] at c.

For clarity the endpoint exceeds b with a strict quantitative margin. The same repeated-Rolle argument for the fourth-order Hermite remainder gives, for some zeta in (a,e),

    g(e)-p(e)=g''''(zeta)(e-a)^2(e-c)^2/24.

Here p(e)=b+4kr^3 and (e-a)^2(e-c)^2=4r^4, so

    g(e)>=b+4kr^3-Hr^4/6>=b+(7/2)kr^3>b.

The axial path x from a to e is therefore one admissible older-endpoint path, with minimum g(c)=f(S), proving (A2). Generalized Rolle's theorem here is elementary: subtract the displayed multiple of (x-a)^2(x-c)^2 so that the difference also vanishes at e, and differentiate four times. No probabilistic estimate or hard-fibre geometry enters this lemma.

## 3. The current parent bounds supply finite-death uniform integrability

Take K=1+||f||_(C4) in a fixed global coordinate norm and a dimension constant C_d with H<=C_d K for every axial orientation. Define

    B_r={K>3k/(C_d r)}.

The lemma shows that E_r and {finite death, X_r>1} are contained in B_r. The parent supplies, uniformly for small r at fixed parameters,

    Z_r/r^2 >= z_*>0,
    sup_r E_Q[(W_r/r^2) K^s] < infinity for every finite s>=0.  (P1)

The second assertion follows from P(4.1), the all-order W_r/r^2 bound following P(5.3), and Holder's inequality. It retains the weight-field correlations. Its constants can also be taken common on the parent's compact b,k,R sets with k bounded away from zero.

For every N>0, direct weighted Markov gives

    Q_r^W(B_r)
      = E_Q[(W_r/r^2)1_B]/(Z_r/r^2)
      <= C_N r^N.                                     (U1)

For a finite death the torus is connected and an older endpoint exists. Its path minimum is at least min f, so

    0<=b-d_f(M)<=b-min f<=2||f||_infinity<=2K.

For q>0 and any N>0, using a Markov power p>N+3q+3 in (P1),

    r^-3 E_QW[X_r^q; finite death, X_r>1]
      <= C r^(-3q-3) E_Q[(W_r/r^2) K^q 1_B]
      <= C_p r^(p-3q-3)
      = O(r^N).                                       (U2)

Changing p slightly if necessary gives the stated exponent for any prescribed N. The same estimate with q+epsilon supplies the conventional sufficient criterion

    sup_(small r) r^-3 E_QW[X_r^(q+epsilon);F_r,finite death]<infinity,

because X_r<=1 off B_r and r^-3 Q_r^W(F_r) is bounded. Hence the family of finite-death failure measures is uniformly integrable for every positive power. No new tail assumption is needed beyond the current parent's all-order moment statements, the failure O(r^3) bound, and the elementary axial lemma.

In particular, since E_r is contained in B_r,

    Q_r^W(E_r)=O(r^N) for every N>0.                    (U3)

This is an upper bound only. It does not imply the essential event has zero probability at any fixed r.

Combining (B1), (U2) and (U3) gives the finite-death moment corollary:

    r^-3 E_QW[X_r^q;F_r,d_f(M)>-infinity] -> m_q,
    E_QW[X_r^q | F_r,d_f(M)>-infinity] -> m_q/a.         (MOM)

Indeed the difference between the first numerator and the clipped numerator consists of the finite part above 1, bounded by (U2), and the clipped contribution Q_r^W(E_r), bounded by (U3). Also Q_r^W(F_r,finite)/r^3->a. These statements hold for every fixed positive q. They do not assert inverse moments (q<0), convergence uniform in all unbounded parameters, or an intensity for uniquely counted replacement bars.

## 4. Essential-inclusive moments are nevertheless infinite in the actual model

For every fixed sufficiently small r>0 and fixed parameter choice, the original tilted law has

    Q_r^W(E_r)>0.                                      (S1)

Therefore, with the literal extended-value convention,

    E_QW[X_r^q;F_r]=infinity,
    E_QW[X_r^q | F_r]=infinity, q>0.                    (S2)

This is a model-realized obstruction, not an abstract rare-tail example. It is compatible with the faster-than-every-power upper bound (U3).

Proof of conditional support: P §2 gives strictly positive variance for every real Fourier mode and convergence of the Fourier expansion in C2 with its expected tail norm tending to zero. Every smooth trigonometric polynomial is in the C2 support: finitely many coefficients can fall in any prescribed neighborhood with positive probability, independently of a tail whose C2 norm is small with positive probability. Smooth trigonometric polynomials are dense in C2 on the torus (smooth approximation followed by Fourier approximation). Thus the unconditioned Gaussian field has full support in the Banach space B=C2(T^d).

Let L:B->R^(2(d+1)) be the original value/gradient pin map and Sigma its positive-definite covariance. Define the continuous regression right inverse

    A y = Cov(f,Lf) Sigma^-1 y, so L A=Id,
    T=Id-A L.

Then T is a continuous projection of B onto ker L, and Tf is a centered Gaussian field independent of Lf. For the prescribed pin vector y, Q_r is the law of Ay+Tf. Since f has full support in B, Tf has support the closure of T(B)=ker L. Therefore Q_r has full relative C2 support on {h:Lh=y}. This uses the original pin law, not a second conditioning or a restricted normalizer.

Proof of a stable essential typed configuration: write Delta=kr^3. Choose disjoint small embedded balls about M,S, a constant c0<b-2Delta, and smooth cutoffs chi_M,chi_S taking values in [0,1], equal to 1 on smaller balls and supported in those disjoint balls. On those balls set

    q_M(z)=b-|z-M|^2,
    q_S(z)=b-Delta+epsilon x_axial^2-epsilon|x_transverse|^2,

using coordinates centered at the appropriate pin. Choose the S ball and epsilon>0 so q_S<b-Delta/2 throughout its support. Extend

    h=c0+chi_M(q_M-c0)+chi_S(q_S-c0)

smoothly by the constant c0 outside the supports. This has exactly the required values and gradients at the pins. Its Hessian at M is negative definite; its Hessian at S has exactly d-1 negative eigenvalues and one positive eigenvalue. Its unique global maximum is M with value b: convex interpolation stays strictly below b at every other point.

There is a relative C2 neighborhood U of h inside the exact affine pin space on which these properties persist. On a small inner M ball the Hessian stays uniformly negative and the exact gradient pin forces a strict maximum at M. On the compact complement of that ball, h has a positive gap below b; a small C0 perturbation preserves it. A small C2 perturbation also preserves the strict S index and keeps both absolute determinants bounded below, so W_r>=w0>0 on U. Conditional full support gives Q_r(U)>0. Thus

    Q_r^W(E_r)>=E_Q[W_r;U]/Z_r>=w0 Q_r(U)/Z_r>0.

The prototype itself need not be globally Morse outside the pin balls: the source's almost-sure Morse distinct-value event has Q_r-measure one and intersects U with the same positive measure. There is no older endpoint on U, so d_f(M)=-infinity and E_r is indeed a failure event. No lower bound uniform in r or quantitative probability asymptotic is asserted.

## Assessment and retained boundaries

There is no defect in the existing weak mark claims. There is a useful author-side positive extension: the finite-death conditional law has convergence of every fixed positive moment, because an axial path and the parent's existing all-order moments already prove the needed uniform integrability. Clipped positive moments are an immediate bounded-test corollary. With the actual essential value retained as infinity, every positive moment is infinite at each r despite the vanishing essential mass. The finite-death convention must therefore be stated explicitly.

The source failure measure and cubic mark identification remain required hypotheses. This proposal supplies neither their acceptance nor a provider-distinct review. It changes no scientific status, evidence JSON, formal-required-check contract, or historical source. No repository source was edited, no external message or review was posted, and no Lean execution or full test suite was run. Root retains integration and external coordination ownership.
