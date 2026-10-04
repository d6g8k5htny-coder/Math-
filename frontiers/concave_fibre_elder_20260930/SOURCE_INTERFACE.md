# Source-interface audit for a higher-dimensional elder bridge

Read-only source audit, 30 September 2026. Same-provider OpenAI contributor; zero organizational-independence credit. No mathematical acceptance, scientific-status transition, existing-proof modification, PR action, or count-law promotion is asserted. The analytic lemmas reconstructed below are new author-side consumer steps requiring source-bound review.

## 1. Exact public source cut

Public `Math-/main` readback was `ab13a08f5e5b0adc7a7d80cf643d9b5a0618507f`. Public PR170 is an open draft at head `79f18f0cb318fceccd5bdf4e6dad29815165bc7d`, branch `codex/local-planar-elder-f68038be`. All listed files were fetched in full from the exact public commit. The scratch copies in `sources/` have been checked against the public Git blob identities, including UTF-8 byte lengths. Existing mutable source maps were not changed.

| Tag | Exact path | Git blob | Bytes | Interface consumed |
|---|---|---|---:|---|
| SC | `frontiers/spectral_cluster_closure_20260929/PROOF.md` | `16c56821b52fd76b0be791622b9c3809eafde75a` | 25006 | §§2,5,6: raw midpoint regression, orthogonal spectral chart, physical anisotropic normal form, hard slaving, full weight, local spectral kernel and its integrability. Its count exhaustions are not premises. |
| CUB | `frontiers/planar_cubic_cluster_20260929/PROOF.md` | `bb446d08db8a944537a743ad550b88c1c2ad5758` | 19889 | C1–C15, Theorem C and Lemma S: original-coordinate cubic, classifier, stable roots, shear only for algebra. |
| EDL | `frontiers/elder_dimension_lift_20260928/PROOF.md` | `7303bd791a68a1139251f0f6e403a9f7cc89b006` | 23971 | Explanatory context only: A7–A28 compare physical jets, bounded shear charts and actual root/index constructions. SC supplies the orthogonal graph interface used here; no EDL count or pairing conclusion is a premise. |
| ELDERD | `frontiers/elder_lower_all_d_20260929/PROOF.md` | `7f41c9e315be0a7985d4c770a11a2cdf717bd46a` | 16485 | Context only: soft eigenplane path gives an elder-failure lower event, without an upper barrier or actual replacement partner. |
| DL | `frontiers/d5_dimension_lift_20260929/PROOF.md` | `9d82c707fdb17d3072a8930f26dabedf59e456fc` | 53727 | Scope audit only: §1.3 expressly excludes elder selection. No count/first-moment conclusion is consumed. |
| P | `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md` | `dfed3b8d318a3ab1950957f393307733a4bef3f2` | 40261 | §§3–8: endpoint matrix density, independent full-field residual, original weight and full normalizer, cap-failure inclusion, genericity and maximin; §§10–12: exact compact radial/lifetime ledger and its domination interfaces. |
| CAP | `imports/lifetime_parent_20260925/MARKED_CYLINDER_CAP_PROOF.md` | `0633aca3c2a2882b0de4399da0a75d64c2e6b2e1` | 15160 | §§1–5: deterministic all-dimensional good-cap implication. |
| ERR | `imports/lifetime_parent_20260925/ERRATUM_CONGRUENCE.md` | `213594d6ca6a86fb938110f4d166d9ce275a02d0` | 1782 | Corrected endpoint congruence in P §5. |
| BOREL | `reviews/d1_section9_borel_repair_20260925/REPAIR.md` | `fe9b9ce4999908bb3814b500ee2d0ceb0c6f704a` | 9062 | Required whole-field Borel marked Kac–Rice replacement for P §9. |
| REC | `reviews/d1_chain_reconciliation_20260928/RECONCILIATION.md` | `75da2597971510f843f8d90c743950cb8c177342` | 23312 | §1 reading rule; §5 W1 convergence-in-law clarification and embedding radius. |
| LOCAL | `frontiers/local_elder_geometry_20260930/PROOF.md` at PR170 head | `ef2aa57959ea9f721bbf2316ce94cf616c1c9113` | 39722 | Theorem E, §§3–6: planar compact collar and exact highest continued partner; §8 scalar failure exhaustion. SHA256 `f68038be79b46124b0f9b31205aa6e3682b34b6f5ef81f4a5697ae81f07cc46b`. |

For the first ten rows the immutable URL is `https://github.com/d6g8k5htny-coder/Math-/blob/ab13a08f5e5b0adc7a7d80cf643d9b5a0618507f/` followed by the path. For LOCAL replace the commit with `79f18f0cb318fceccd5bdf4e6dad29815165bc7d`. `SOURCES.json` gives complete URLs and SHA256 values.

## 2. The supplied analytic graph interface

Fix d≥3, m=d−1, one original axial frame, b∈R, k>0, and a midpoint spectral target. In SC's orthogonal coordinates

    A_mid = O diag(rs,−h2,…,−hm) Oᵀ,
    0<h2<…<hm,
    (x,z,w)=(rX,rZ,r²V),  w∈R^(d−2).

The field is still regression on the original `2(d+1)` observations; the rotation acts on the complete cubic tensor. SC (5) is the actual full-field extra-conditioned coupling. SC (6) supplies its pathwise C4 bound, and SC §5 supplies, on every fixed soft disk:

    (f(rX,rZ,0)−b)/r³ → P(X,Z) in C²,
    r^(−2) f_w(rX,rZ,r²V) → −diag(h)V+Q(X,Z) in C¹.

The original-coordinate P is exactly CUB (C1), with `(a,beta,c)=(tau_xxz,tau_xzz,tau_zzz)`. The hard quadratic forcing can be written, consistently with EDL (A28), as

    Q_j=(tau_xxwj/2)(X²−1/4)+tau_xzwj XZ+(tau_zzwj/2)Z².

The constant term `−tau_xxwj/8` retains the hard-gradient endpoint pins. Omitting it would move the hard graph at M and S and destroy exact pinning.

SC §5 expressly supplies a unique smooth hard graph, `w=zeta_r(x,z)=O(r²)`, and states that substituting it into f/r³ changes the planar potential by O(r) in C² on fixed sets. This is an analytic source interface, not a consequence of its count tests. The following estimates make the statement transparent. On `|t|≤Rr`, `|w|≤cr`, with `t=(x,z)`, fixed h_min>0 and fixed coupling C4 bound K, Taylor gives

    f_ww ≤ −h_min I/2,
    |f_w(t,0)| ≤ C r²,
    |f_tw(t,w)| ≤ C r.

The graph follows from strict concavity and the inward hard radial derivative. Implicit differentiation gives `|zeta_r|≤Cr²`, `|D_t zeta_r|≤Cr`, and `|D_t² zeta_r|≤C`. For `psi_r(t)=f(t,zeta_r(t))`, define `delta_r=psi_r(t)−f(t,0)`. Then

    |delta_r|≤Cr⁴,
    |D_t delta_r|≤Cr³,
    |D_t² delta_r|≤Cr².

The Hessian identity used in the last bound is

    D_t² psi_r = f_tt−f_tw f_ww^(−1) f_wt

evaluated on the graph. Each rescaled soft derivative contributes one factor r. Hence `(psi_r(rX,rZ)−b)/r³−(f(rX,rZ,0)−b)/r³=O(r)` in C². Inverse-hard constants are allowed at a fixed positive hard target; they must not be placed in the failure-tail majorant below.

Since the original hard gradients vanish at each pin and the hard graph is unique, `zeta_r(M)=zeta_r(S)=0`. The reduced potential retains the exact critical pins and values 0,−k. Nondegenerate reduced critical points are actual full roots on the graph. Block congruence gives

    index(H_full)=(d−2)+index(H_reduced).

Thus CUB's window saddles lift to actual index-(d−1) roots, and their hard coordinates are r² times `diag(h)^(−1)Q+o(1)`. Their physical coordinates divided by r tend to `(X,O(Z,0))` in the original axial/transverse frame.

EDL's distinct construction uses the bounded determinant-one shear `y=(z,w−qz)` with q=D^(−1)v. Its original physical r-scaled location is `(X,Z,−qZ)` after the axial frame, not `(X,Z,0)`. In that chart sigma, not the raw a entry of A, is the soft curvature. Both SC's orthogonal chart and EDL's determinant-one shear preserve criticality, inertia and Hessian determinants; a general invertible linear change would introduce its squared determinant factor. SC's orthogonal chart is the appropriate global norm-controlled chart here. CUB's separate planar shear `u=X+aZ/(12k)` is only an algebraic change; reported physical X must be recovered as `u−aZ/(12k)`.

## 3. Exact missing topological consumer step

LOCAL Theorem E is stated on surfaces. It cannot simply be cited as a theorem about the full d-dimensional field. The new consumer needs to thicken its compact planar collar and control every hard boundary exit.

The graph profile alone on an r²V box is insufficient. Hard side boundaries at that scale have a height drop of order r⁴, smaller than the r³ death window. A correct thickening uses a larger hard radius, for example `rho_r=A r^(3/2)` centered on zeta_r. Strict hard concavity yields

    f(t,w) ≤ psi_r(t)−(h_min/4)|w−zeta_r(t)|².

Choose A with `h_min A²/4>k`. For every planar collar disk K_(r,h) supplied by the LOCAL §§4–6 construction for the actual reduced profile, psi_r≤b inside and psi_r=b+r³h on its boundary. The graph-centered hard tube over K_(r,h), of radius rho_r, is contained in the local chart for small r. Its soft boundary has height ≤b+r³h and its hard side boundary has height <b−kr³. Its interior has no point above b. Every full global path to an older point must exit this compact tube, so it meets height ≤b+r³h. The same fixed radius works for every h between the highest actual continued saddle height and zero, since those h are ≥−k.

The lower paths from LOCAL §6 lift along the hard graph. Exact reduced criticality preserves the derivative zeros on each moving critical chord; C² convergence preserves its monotonicity and positive doubled endpoint. Hence the lifted path has exact minimum at that actual continued full critical root.

Combining those two steps would identify the global death with the highest actual continued local saddle for every sufficiently small r on the Morse distinct-value locus, including the exact empty-sector selection of S. This is the required new deterministic theorem. EDL §9 and SC §9 explicitly do not supply it; neither an extra-root count nor a planar restriction alone identifies the full elder partner.

## 4. Full failure exhaustion from the endpoint matrix, without counts

The following new retained-indicator version of P's existing matrix integral supplies the analytic exhaustion required after the deterministic bridge. It does not rely on `N_R>0`, a witness event, or any remote-count estimate.

Let `F_r={actual global ordinary partner of M is not S}` and let `B=−D_y²f(M)>0` on typed support. Order its eigenvalues

    0<lambda1≤lambda2≤…≤lambdam=Lambda,
    m=d−1≥2,  v=m(m−1)/2.

P §3 defines its matrix A_r at the endpoint M. P (4.2)–(4.3) regress the full field on that entire endpoint matrix and give an independent residual field g_r. Put `J=1+||g_r||_C4`, and `U=J+Lambda≥1`. J is independent of the whole matrix, not of its entries separately; all its fixed moments are uniformly bounded. Bounded coefficients and means give

    K:=1+||f||_C4 ≤ C(J+||B||_F) ≤ C U

on typed support. The final inequality is dimension dependent and uses lambda1≤Lambda. For m≥2 Lambda is one of the retained hard eigenvalues; this is why the scalar case needs a separate split.

P §8 and CAP imply `F_r⊂G_r^c` almost surely, with

    G_r={lambda1>[4/(3k)]r M3²,  r M4≤3k/10}.

The fourth-derivative exception has tilted mass O(r⁴) by P (7.7) and the full floor (5.5), hence has zero r^(−3) limit. On the remaining depth branch,

    lambda1≤D rU².

P (6.2), with its second soft factor retained, gives

    W_r ≤ C r² U^(2m) lambda1(lambda1+C rU).

The endpoint matrix density has the Gaussian bound P (3.5). Its spectral Jacobian is bounded by `C Lambda^v`; the hard angular volume is finite. For fixed J and lambda2,…,lambdam, U is independent of lambda1. Thus for any retained event E depending only on J and the hard eigenvalues,

    E_Q[W_r;depth,E]
      ≤ C r² E_J ∫ e^(−c sum_hard lambda_j²) Lambda^v U^(2m)
                  1_E ∫_0^(DrU²) lambda1(lambda1+C rU) d lambda1 d lambda_hard
      ≤ C r⁵ E_J ∫ e^(−c sum_hard lambda_j²)
                  Lambda^v U^(2m+6) 1_E d lambda_hard.       (T1)

The positive majorant permits extension of the lambda1 domain beyond its actual ordered interval; the Gaussian lambda1 factor can be dropped. The integral is exactly the r³ soft integral before the outer r² weight. Divide by the original full `Z_r≥z_*r²` once.

With `E={U>A}`, every higher J moment and Gaussian polynomial integrability give, for every fixed p>0,

    limsup_(r→0) r^(−3) Q_r^W(F_r,U>A) ≤ C_p A^(−p).    (T2)

This follows directly from `U^q 1{U>A}≤A^(−p)U^(q+p)`, q=2m+6. It requires no common residual law for every r; the uniform moment bounds suffice.

With `E={lambda2≤eta}`, averaging J's moments leaves an ordinary integrable Gaussian polynomial over the ordered positive hard eigenvalues. Its mass on the lambda2 strip tends to zero (a bound C eta for eta≤1 suffices). Consequently,

    lim_(eta→0) limsup_(r→0)
      r^(−3) Q_r^W(F_r,lambda2≤eta)=0.                    (T3)

This handles all higher-corank intersections in measure and never divides by a hard eigenvalue. It is a failure-measure statement, stronger for this purpose than SC §4's near-occurrence tail.

## 5. Endpoint-to-midpoint conversion

Let `mu1≤…≤mum` be the signed eigenvalues of `−D_y²f(0)`. Hessian Lipschitz control and Weyl's inequality give

    |muj−lambdaj|≤r M3/2≤C rU.

With SC's midpoint variables `s=−mu1/r`, `h_j=mu_j` for j≥2 and rotated complete tensor tau, the depth branch satisfies

    |s|≤D U²+C U,
    |h|+|tau|+K≤C U.                                    (T4)

T2 therefore implies full failure tightness in the actual midpoint spectral jets and in K. No replacement of the endpoint density by a midpoint density occurred in this tail argument.

On U≤A, midpoint `h2≤eta` implies endpoint `lambda2≤2eta` for all sufficiently small r at each fixed eta,A. T3 then gives

    lim_(eta→0) limsup_(r→0)
      r^(−3) Q_r^W(F_r,h2≤eta)=0.                        (T5)

The error from U>A is sent to zero by T2 and the M4 exception is o(r³). In particular midpoint hard eigenvalues that are negative can carry no unidentified leading failure mass. Repeated hard eigenvalues need no inverse-gap estimates: the spectral chart boundary is null; on each compact sector its Jacobian is bounded and vanishes at a collision. Positive hard lower bounds are used only for pointwise graph convergence and removed using T5.

For d=2/m=1, retain LOCAL §8's existing scalar near/far split and tail proof; T1 cannot be used with Lambda fixed because Lambda=lambda1.

## 6. Exact resulting marked-law interface, conditional on the new geometry

SC §2 disintegrates the raw physical midpoint (A,T) law, with density h_r→h_0. Its ordered orthogonal spectral transformation contributes `r c_m J_r`, where

    J_r=prod_(j≥2)(h_j+rs) prod_(2≤i<j≤m)(h_j−h_i).

The extra-conditioned coupling is the same actual field. On a compact sector with h2>0 the original typed weight has

    W_r/r⁴ → prod_(j≥2)h_j² w_+(s,a,beta),
    w_+=9k²[B−2s]_+[−B−2s]_+,  B=beta−a²/(12k).

The continuous determinant-weight limit is zero outside the typed domain and on its boundary; no selector convergence is needed there. The full normalizer is P (5.4), with ERR and REC's W1 reading rule. For any bounded failure multiplier the exact scaled disintegration is

    (c_m r²/Z_r) J_r h_r(O diag(rs,−h)Oᵀ,Rot_O tau)
                      E[(W_r/r⁴) multiplier].            (T6)

There is one raw soft-coordinate Jacobian r, one original W_r, and one full Z_r. On compact jets SC (6) and the two short-column determinant bound SC (15) provide an integrable coupling envelope without using a count event. Conditional on the deterministic fibre bridge, pointwise failure convergence is `1_F→1{n>0}` off LOCAL's polynomial null sets. The actual death and location converge to h_* and the winning physical root. Dominated convergence proves the compact marked failure law. T2–T5 exhaust the actual failure measure, so no near-occurrence exhaustion is substituted.

The candidate finite limiting failure measure is

    dmu_fail = 1{n(s,a,beta,c)>0} (c_m/z0)
       h_0(O diag(0,−h)Oᵀ,Rot_O tau)
       prod_(j≥2)h_j³ prod_(2≤i<j≤m)(h_j−h_i)
       w_+(s,a,beta) ds dh dO d tau.                       (T7)

This is exactly the nonempty restriction of SC (17). Its finiteness follows from the deterministic integral bound SC (19); positivity follows from its displayed open nonempty cubic sectors. Its total mass is `a1+a2` in SC (20). The count law's remote singleton coefficient beta_far is not an elder-failure coefficient and is absent here.

The jet/failure measure can converge in total variation. The normalized actual death, physical location and lifetime marks converge weakly; neither Gaussian source gives TV for those real-valued marks. On each regular coupled sector the finite-r normalized lifetime is `−D_r=−h_r` for all sufficiently small r. Its limiting conditional-on-failure mark is `−h_*∈(0,k)`, with limiting candidate-lifetime fraction `−h_*/k∈(0,1)`. Essential/sentinel mass vanishes at r³ scale by compact pointwise older paths and full failure exhaustion.

SC retains full normalized Haar O, including sign gauges. A law on spectral variables should be defined with that extended spectral disintegration, or on the gauge quotient. A deterministically selected eigenbasis generally lives in a fundamental domain and cannot be silently assigned the full Haar law. The physical location `(X,O(Z,0))` is gauge invariant.

## 7. Audit disposition and boundaries

Usable analytic interface: **supplied** for actual fibre-maximized fixed-disk C² convergence, exact pins, full roots, indices and W/Z; **newly reconstructed** for full elder-failure exhaustion T1–T5. Necessary new deterministic consumer: the thickened compact collar and exact graph-lifted critical chords in §3. Once that consumer is proved, T6–T7 provide the precise higher-dimensional actual-pair marked law without a count packet.

No full-field theorem follows from a CUB/EDL finite checker. No assertion uniform in varying d, vanishing k, growing marks, or growing volume is made. The parent supplies compact-mark domination for a subsequent lifetime-density composition, but this audit does not claim a separate elder-density second-order expansion, replacement-bar intensity obtained by counting rejected candidates, or an unrestricted refined lifetime law. Root/location marks remain in original physical coordinates. No existing proof/status/map/PR was modified.
