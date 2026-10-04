# Ordinary short bars: occurrence and field-first sampling

Object C52-ORDINARY-SHORT-BAR-OCCURRENCE-20261001-v1. Additive conditional mathematical candidate, OpenAI/Codex. Scientific-status effect NONE; C8 remains OPEN. The theorem consumes the exact analytic interfaces listed below; this packet does not reaccept those interfaces, formalize Gaussian persistence, or certify the whole program.

## 1. Frozen target and source contract

Fix L>0 and d=2. Let X be the centered, variance-one smooth Gaussian field on the fixed flat torus T_L^2 with covariance
$$
K_L(z)=\frac{\sum_{n\in\mathbb Z^2}e^{-|z+Ln|^2/2}}
 {\sum_{n\in\mathbb Z^2}e^{-|Ln|^2/2}}.
$$
Use ordinary SUPERLEVEL H0 persistence. A finite bar is born at a maximum M and dies at its actual global elder-selected merging saddle S; M is the dying component's maximum, not the older surviving maximum. Exclude the essential global-maximum class. Let K_tau be the total number of such bars of lifetime in (0,tau] in ONE field on the WHOLE torus. Its expectation is not divided by volume.

Sources P, CAP, E1, E2, REC, R and T are pinned by path, bytes, SHA256 and Git blob in SOURCES.json, all at Math- commit 7fe06b01489af8181e53f26d520810829f146094. P is the lifetime parent; CAP its deterministic predecessor; E1 corrects the congruence; E2 replaces P§9; REC supplies the mandatory reading rule/W1/embedding radius; R§2 supplies the regression construction; T§Proposition3 supplies the ordinary-bar marked intensity law. In particular:

- Interpret P through CAP/E1/E2/REC, with an embedded r_0<L/(4sqrt(2)).
- E2 identifies expected ACTUAL finite bars with the ordered maximum/saddle pair measure carrying the global elder indicator. It permits bounded Borel marks of the whole field, including tau-dependent marks.
- P§§3–5 give the six-pin law, endpoint determinant bounds, residual transverse density and compact-target moments.
- P(13.4) is the all-target UNNORMALIZED intensity majorant; P(14.1) bounds the fixed off-diagonal lifetime density.
- P Theorem C and its positive coefficient give E K_tau=L²(3/2)c_{2,L} tau^(2/3)+o(tau^(2/3)). No quantitative remainder from R(R1) is required for the new occurrence assertion.
- T(T4), used only for the explicit limiting mark distribution in §6, retains its own exact source premises. R is also read for its explicit coupling formula, not as an independence or genericity assertion.

**Theorem O (conditional on these interfaces).** As tau decreases to zero with L fixed,
$$
B_\tau:=E[K_\tau 1_{\{K_\tau\ge2\}}]=o(\tau^{2/3}). \tag{O1}
$$
Put m_tau=E K_tau, p_tau=P(K_tau>0), e_tau=m_tau-p_tau. Then
$$
0\le e_\tau=E[(K_\tau-1)_+]\le B_\tau=o(\tau^{2/3}),\qquad
p_\tau=L^2\frac32c_{2,L}\tau^{2/3}+o(\tau^{2/3}), \tag{O2}
$$
and
$$
\operatorname{TV}(\mathcal L(K_\tau\mid K_\tau>0),\delta_1)
=P(K_\tau\ge2)/p_\tau\longrightarrow0. \tag{O3}
$$
If a field is conditioned on K_tau>0 and one of its short bars is then chosen uniformly, the law of any common measurable mark differs in TV from the intensity-normalized short-bar mark law by at most e_tau/m_tau=o(1). This includes the explicit mark limit in §6.

These are small-lifetime, fixed-volume occurrence/mark statements. No speed for the little-o, factorial-moment asymptotic, Poisson process, independent-region construction, higher-dimensional extension or infinite-volume limit is asserted. K_tau counts actual persistence bars, not auxiliary window witnesses or the rejected-candidate replacement population of C50/C51. Those packets are not premises of this proof.

## 2. Whole-field isolation under one ordinary fold

Write q=(b,k,u), with b real, k>0 and u in S^1. Let r>0, M=-ru/2, S=ru/2, and condition on X(M)=b, X(S)=b-kr³ and both gradients zero. This is the exact six-observation continuous Gaussian regression law Q_{r,q}. Let
$$
W_r=|\det H_M\det H_S|1_{\{H_M<0,\operatorname{index}(H_S)=1\}},\quad
Z_r=E_Q W_r .
$$
There is no second determinant or adjacency factor in W_r. The exact scaled height gap is k=ell/r³, rather than a Taylor approximation.

The coauthored [fold isolation lemma](FOLD_ISOLATION.md) proves on the original full-field regression coupling, for each fixed q and y in (0,1] and r=(tau y/k)^(1/3),
$$
\frac{W_r}{r^2}1_{\{K_\tau(F_r)\ge2\}}\longrightarrow0
\quad\hbox{almost surely}. \tag{I}
$$
Its ingredients are stated here to make the new dependency visible:
1. The actual coupled F_r converge globally in C4 almost surely to the six-jet contact field F_0. This is derived from averaged-derivative observations on a smooth sample, not from an invalid upgrade of Lp convergence.
2. Residual finite-jet rank plus the overdetermined mesh argument show that off the contact, F_0 has Morse roots with pairwise distinct critical values, none equal to the contact value b.
3. If A=F_{0,zz}(0)<0, a fixed rectangle has a unique transverse ridge. The reduced derivative has strictly positive second derivative because the reduced third derivative at contact is12k>0. The two exact pinned roots exhaust ALL local critical points. Outside the rectangle, root stability and the positive minimum of the finitely many remaining critical-value gaps exclude every additional lifetime-small endpoint pair.
4. If A>0, the maximum-type weight vanishes for sufficiently small r. A=0 is null under the conditional nondegenerate scalar Gaussian law.

Thus the typed contact sector has at most one possible short bar eventually. This does not identify whether the pinned pair is itself the elder pair. The actual elder indicator is retained below. Random exclusion radii and critical-value gaps need not be uniform over q or sample paths. The argument uses per-fixed-law probability-one statements and then integration; it does not assert a common probability-one set for every uncountable parameter choice.

## 3. The bounded mark and exact weighted counting identity

Let H_tau(f)=1{K_tau(f)>=2}. On the Morse distinct-critical-value locus this is a bounded Borel function of the whole field: critical roots/values and their elder pairings are locally stable, and the finite counting function at a threshold is Borel; alternatively apply the countable path representation of E2 and thresholded point-count measures. Define the bar count and mark to be zero on the null complement for the unconditional field. For every r>0 the conditional kernels in E2 specify the same Borel mark; the isolation proof applies on their eventual generic locus.

Let J_eld(M,S;f) be the actual global elder indicator. Pathwise counting once per finite bar yields
$$
B_\tau=E\sum_{\substack{(M,S)\ \mathrm{actual}\ 0<\ell\le\tau}}
H_\tau(f). \tag{C}
$$
There is no extra factor K_tau inside the pair integral: summing the bounded mark already supplies it. Monotone exhaustion away from the diagonal and E2 extend this identity to all separations.

Use midpoint stationarity and oriented displacement S-M=ru. The endpoints have fixed, different types (maximum, saddle); they are ordered once. Reversing u exchanges spatial positions but is not an additional copy of the same ordered pair. For r<r_0, the full-pin determinant is12r^{-5}, height reparameterization contributes r³, planar polar measure contributes r, and W_r contributes r² after division. Thus the near marked pair intensity per unit area is
$$
r A_r^{H_\tau}(q)\,dr\,dq,\qquad
A_r^{H_\tau}(q)=12\pi_r(v_r)
 E_Q[(W_r/r²)J_{\mathrm{eld}}H_\tau],\qquad
0\le A_r^{H_\tau}\le A_r=12\pi_r(v_r)Z_r/r². \tag{C1}
$$
This is the same exact radial ledger r^{d-1}r³r^{-(d+3)}r²=r in d=2. Midpoint/displacement coordinates have absolute spatial Jacobian1. All q use the exact original six-pin target v_r=(b-kr³/2,-kr²,0,12k,0,0).

For ell=kr³ and y=ell/tau,
$$
r\,dr=\frac{\ell^{-1/3}}{3k^{2/3}}d\ell
=\tau^{2/3}\frac{y^{-1/3}}{3k^{2/3}}dy .
$$
Consequently
$$
\frac{B_\tau^{\rm near}}{L²\tau^{2/3}}
=\int_{0}^{1}\int_{\mathbb R\times(0,\infty)\times S^1}
1_{\{k\ge\tau y/r_0³\}}
\frac{y^{-1/3}}{3k^{2/3}}
A_{(\tau y/k)^{1/3}}^{H_\tau}(q)\,dq\,dy. \tag{C2}
$$
The indicator permits evaluating the integrand as zero when r exceeds r_0. The mark depends on tau and on the WHOLE coupled field, not only on the pinned jets.

## 4. All marks and all spatial separations

For each fixed q, endpoint determinant identities and conditional derivative moments P§§4–5 give uniformly bounded p-th moments of W_r/r² for some p>1 as r decreases. Together with (I), uniform integrability gives
$$
E_Q[(W_r/r²)H_\tau]\longrightarrow0 .
$$
Since 0<=J_eld<=1, the expectation in (C1) also tends to zero; continuity of pi_r(v_r) at fixed q proves A_r^{H_tau}(q)->0. No continuity of the global elder indicator along a degenerate contact field is needed.

At all birth heights and all positive k, P(13.4) gives
$$
0\le A_r^{H_\tau}(q)\le
H(b,k)=C(1+|b|+k)^4 e^{-c(b²+k²)},\quad0<r\le r_0.
$$
The dominating function in (C2) is y^{-1/3}H(b,k)/(3k^{2/3}). It is integrable: y^{-1/3} integrates to3/2 on(0,1]; k^{-2/3} is integrable at0; Gaussian tails control all remaining polynomial growth and birth integration; S1 has finite measure. This is an unnormalized bound. In particular no globally uniform floor for Z_r/r² or cap-failure constant over b,k is used.

Dominated convergence proves B_tau^near=o(L²tau^{2/3}). In the complementary FIXED off-diagonal region r>=r_0, H_tau and J_eld are bounded by1, so P(14.1) gives
$$
0\le B_\tau^{\rm far}/L²\le C\tau=o(\tau^{2/3}).
$$
No moving-cutoff RN assertion has been inferred from a fixed-cutoff bound. Near and far exhaust all ordered distinct endpoints (a spatial boundary has zero measure). This proves(O1).

Limit order: fix L and r_0, then fix q,y while tau decreases, use the coupled pathwise limit and conditional uniform integrability, then dominated convergence in(y,b,k,u). There is no L-limit, auxiliary-witness separation limit or interchange of a derivative with a cumulative asymptotic. Constants depend on the fixed field and source bounds; none is a numerical cutoff.

## 5. From weighted counts to field occurrence

Every field has finitely many critical points almost surely and hence finitely many finite bars. Integrability follows from the imported pair bounds. For every nonnegative integer K,
$$
K=1_{\{K>0\}}+(K-1)_+,\qquad
(K-1)_+\le K1_{\{K\ge2\}},\qquad
2P(K\ge2)\le E[K1_{\{K\ge2\}}].
$$
Apply these to K_tau and(O1). The positive leading mean supplied by P Theorem C gives(O2) and p_tau>0 for small tau. Dividing the last inequality by p_tau gives(O3). The excess and multi-count first moment are of the same little-o order, but neither statement controls K(K-1). Rare counts of growing size can invalidate such an inference; exact finite counterexamples are included with the controls.

## 6. Removing field-size bias from marks

Allow any common tau-dependent Borel bar mark in a standard Borel space. On a field with K_tau>0 let U_tau be its empirical probability measure assigning mass1/K_tau to each eligible bar. Define
$$
I_\tau=E[K_\tau U_\tau]/m_\tau,\qquad
F_\tau=E[1_{\{K_\tau>0\}}U_\tau]/p_\tau .
$$
I_tau is the intensity-normalized law; F_tau is obtained by first conditioning the FIELD on occurrence and then choosing a bar uniformly. When e_tau>0 put
D_tau=E[(K_tau-1)_+U_tau]/e_tau. The exact identity
$$
I_\tau=(p_\tau/m_\tau)F_\tau+(e_\tau/m_\tau)D_\tau
$$
proves, for TV=sup over measurable sets,
$$
\operatorname{TV}(F_\tau,I_\tau)\le e_\tau/m_\tau=o(1). \tag{O4}
$$
If e_tau=0 the laws agree. This bound is uniform over the choice of mark, but has no numerical convergence rate.

For T's cubic mark, retain y=ell/tau and q=(b,k,u) for pairs at r<r_0 and send far pairs to its cemetery mark. Set c=c_{2,L} and
$$
g(q)=\frac{A_0(q)}{3c k^{2/3}},\qquad\int g(q)dq=1.
$$
T(T4) and(O4) give the field-first law in TOTAL VARIATION:
$$
F_\tau\longrightarrow \tfrac23y^{-1/3}dy\,g(q)dq, \tag{O5}
$$
with zero cemetery mass. In particular the scaled actual endpoint displacement has the pushforward limit (y/k)^{1/3}u. The discrepancy with the true displacement on far pairs vanishes by the same mark TV bound and the vanishing intensity far mass. This gives no convergence of unbounded mark moments without a separate uniform-integrability argument.

The finite-torus coefficient is exactly P(15.2), with d=2:
$$
c_{2,L}=\frac{\Gamma(7/6)}{24^{1/3}\sqrt\pi}
\int_{S^1}p_G(0)p_{V_u}(0)\tau_u^{4/3}D_u\,d\sigma(u)>0.
$$
Here tau_u²=Var(partial_u³X|grad X=0), V_u=H_Xu, and
D_u=E[A_u²1_{A_u<0}|V_u=0]. The numerical factor24 is not L. No reference-space coefficient is substituted for the finite-torus coefficient.

## 7. Boundaries, review and falsifiers

The new obligation is ordinary-fold isolation and its use inside the bounded whole-field marked pair integral. The proof retains actual global elder identification and the positive leading mean as source interfaces. If those interfaces or the all-mark bound fail, the corresponding theorem here fails. The proof neither replaces their reviews nor grants them new acceptance.

The conclusion does not close the historical auxiliary shrinking-witness uniqueness problem: its random variable and normalization are different. Nor does it promote C8, RN/24-jet numerical gates, a covariance-class universality theorem, higher homology, higher dimensions, factorial moments or an increasing-volume cluster process. Mathematical completeness of this conditional theorem is separate from the project's other open nodes.

Review must inspect: conditional remote root AND critical-value genericity, complete local ridge rather than an O(r) window only, actual all-field coupling, A=0 null boundary, weight uniform integrability, exact tau/lifetime factors, all-target domination, field-first size-bias identity and the absence of an accidental factorial claim.

Exact rational programs check the finite identities and meaningful counterexamples. They do not prove continuum probability estimates, topological identification, dominated convergence, or analytic source acceptance. AI coauthors and fresh AI technical reviewers are named in the delivery; same-provider review earns organizational-independence credit0. Dylan Roy delegated AI work; personal reading PENDING.
