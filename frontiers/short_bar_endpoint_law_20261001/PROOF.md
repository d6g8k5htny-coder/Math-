# Actual short-bar intensity: a marked transfer and shrinking-distance consequence

Object OA-DIRECTIVE-ELDER-MEASURE-20261001-v1. OpenAI author/source-exposed derivation. CONDITIONAL COROLLARY of the exact stated D1/D2 interfaces, not a new acceptance of those proofs or a whole-program completion certificate. No cluster law or auxiliary-witness uniqueness is assumed.

## Sources and scope

All GitHub sources below are read at Math- commit 124c37d9218120245098df453cf88d3e54b8c9ca. Public full texts: [P](https://github.com/d6g8k5htny-coder/Math-/blob/124c37d9218120245098df453cf88d3e54b8c9ca/imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md), [R](https://github.com/d6g8k5htny-coder/Math-/blob/124c37d9218120245098df453cf88d3e54b8c9ca/frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md), and [required reading rule](https://github.com/d6g8k5htny-coder/Math-/blob/124c37d9218120245098df453cf88d3e54b8c9ca/reviews/d1_chain_reconciliation_20260928/RECONCILIATION.md).

- P: imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md, blob dfed3b8d318a3ab1950957f393307733a4bef3f2, 40261 B, SHA256 9350ad6eaba6626b93c3dedeef9e2ff816e5cdf1c8318e85fb27499141c84bc7.
- Required reading set: CAP blob0633aca3c2a2882b0de4399da0a75d64c2e6b2e1; E1 blob213594d6ca6a86fb938110f4d166d9ce275a02d0; E2 blobfe9b9ce4999908bb3814b500ee2d0ceb0c6f704a; REC blob75da2597971510f843f8d90c743950cb8c177342. REC §1 supplies W1 and r<L/(4sqrt(2)); E2 replaces P §9.
- R: frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md, blob247b3ecf80bfbe896948d5d489b2d5842a81c481; (R1)'s bounded nonselected density is used in T1. Its candidate and elder O(1) remainders additionally justify the displayed O(t) cumulative remainders. No new geometric assertion is imported from R.
- The authorized Drive parent 1foDgiDi4XIKOfbrZEE8dWKV_BkZU8LIb was fetched and its complete text equals P exactly. Its older author-side header is not a current review verdict.

Fix d>=2 and L>0; keep L fixed as t decreases. The field is centered, variance-one with the exact covariance of P §1 on the flat torus. Consider finite ordinary SUPERLEVEL H0 bars, excluding the essential global-maximum class. Measures are expected counts PER UNIT VOLUME; no samplewise asymptotic is asserted. A maximum M births a component which dies when it merges with an older component; S denotes its actual killing saddle of index d-1. This does not mean M is the older surviving maximum.

Inputs used, stated mathematically rather than by acceptance labels:
1. E2's full-field Borel marked Kac-Rice identity and P §8's Morse/distinct-value elder convention. Every finite bar corresponds to exactly one globally selected maximum/saddle pair.
2. P(10.2),(13.4): near candidate intensity is r A_r(b,k,u) dr db dk d sigma(u), with 0<=A_r<=H(b,k)=C(1+|b|+k)^(2d) exp[-c(b^2+k^2)]. Selected intensity has the extra factor p_r in [0,1].
3. For fixed b, k>0 and u, A_r->A_0 and p_r->1. The latter follows from the cap/global-selection theorem, not from a count estimate.
4. P(14.1): candidate density at separations >=r_0 is bounded by C. R(R1): the FULL density of candidate pairs which are not actual elder pairs is bounded by C; also each full density differs from c ell^(-1/3) by O(1). T1-T4 need only the nonselected bound and P's leading asymptotic; the additional remainder justifies the stronger cumulative displays.
All constants below are finite and may depend on d,L and these source bounds; none is numerical or uniform in L,d.

## Proposition 1: marked measure transfer is stronger than count transfer

For 0<t<=t_*, let C_t and E_t be the finite expected candidate and actual-elder measures of lifetimes 0<ell<=t. Attach ANY common Borel mark to each pair, and optionally let the mark depend measurably on t. The mark may include locations, Hessians, birth, or rescaled lifetime and separation. Count candidates and selected pairs with the SAME mark map. Then E_t<=C_t as measures and
D_t:=C_t-E_t is positive, with D_t(total)<=Ct.

Proof. Apply E2 to the candidate indicator and its product with the actual global elder indicator. Their difference is exactly the nonselected indicator, so D_t is positive even for field-dependent marks. Integrate the nonselected density bound R(R1) over (0,t]. A pushforward preserves positivity and total mass. No inference from an unweighted Palm probability has been made.

Put n_t=C_t(total), e_t=E_t(total), and normalize the measures to probability laws. P's positive coefficient and R(R1) give
n_t=(3/2)c_{d,L} t^(2/3)+O(t), e_t=(3/2)c_{d,L} t^(2/3)+O(t).
Consequently, for small enough t, e_t,n_t>0, and with total variation defined as sup over Borel sets,
TV(C_t/n_t,E_t/e_t)<=D_t(total)/n_t=O(t^(1/3)).    (T1)

Indeed C_t/n_t=(e_t/n_t)(E_t/e_t)+(D_t(total)/n_t)(D_t/D_t(total)); if D_t(total)=0 the laws coincide. This proves (T1) for all marks simultaneously, including t-dependent spatial tests. The bound does not convert a cumulative little-o estimate into a density bound: R supplies the density bound before integration.

These are INTENSITY-NORMALIZED laws. They equal E[sum of mark indicators]/E[number]. They need not equal the law obtained by conditioning a field sample on having at least one short bar and then choosing a bar uniformly in that sample; that law has a random 1/N factor. Identifying the latter may require cluster information. The mean persistence theorem and (T1) do not.

## Proposition 2: actual endpoints localize on explicit shrinking scales

For 0<rho<=r_0 and 0<t<=rho^3, the expected per-volume number of ACTUAL bars with ell<=t and torus endpoint distance r>rho is at most
C t/rho.                                                (T2)

Proof. Split rho<r<r_0 and r>=r_0. For a fixed lifetime ell<=t, the first range corresponds EXACTLY to
ell/r_0^3 < k < ell/rho^3.
P(11.1) and p_r<=1 give its density at most
ell^(-1/3)/3 * integral_(b,u) integral_0^(ell/rho^3)
                             H(b,k) k^(-2/3) dk db d sigma.
Since ell/rho^3<=1, the b-integral and finite sphere measure are bounded uniformly for k in [0,1]. The remaining integral is 3(ell/rho^3)^(1/3). Thus the density is <=C/rho. The far range has density <=C by P(14.1). Absorb its bound into C/rho using rho<=r_0, then integrate ell over (0,t]. This proves (T2) without applying a fixed-remote RN theorem at a moving cutoff.

Dividing by e_t>=c_*t^(2/3) gives
(E_t/e_t){r>rho}<=C t^(1/3)/rho.                         (T3)
For example rho=t^beta with any fixed 0<beta<1/3 yields O(t^(1/3-beta))->0. More generally any rho(t)->0 with t^(1/3)/rho(t)->0 gives localization. Constants are unchanged along this diagonal. This is a bound on actual birth/death ENDPOINTS, not on every auxiliary window critical point or on the full ascent path.

## Proposition 3: cubic-scale marked lifetime law in total variation

Let q=(b,k,u) in R x (0,infinity) x S^(d-1). Near the diagonal, k is the EXACT pair mark ell/r^3; no Taylor inversion is used. Take y=ell/t in (0,1]. Assign all pairs with r>=r_0 a cemetery mark dagger, retaining y. For near pairs retain (y,q). Define
c=c_{d,L}=integral A_0(q)/(3k^(2/3)) dq,
g(q)=A_0(q)/(3c k^(2/3)).
Then g is a probability density, and both the normalized candidate and actual-elder short-bar intensity laws converge in total variation to
(2/3)y^(-1/3) dy * g(q) dq,                             (T4)
with zero cemetery mass. There is no quantitative convergence rate for g asserted here.

Proof. The near candidate measure, after dividing by t^(2/3) and making ell=ty, has density
f_t(y,q)=1{k>=ty/r_0^3} y^(-1/3)
                     A_((ty/k)^(1/3))(q)/(3k^(2/3)).
The elder version replaces A_r by A_r p_r. For every y>0,k>0, both densities converge to
f_0(y,q)=y^(-1/3) A_0(q)/(3k^(2/3)).
They are dominated by y^(-1/3) H(b,k)/(3k^(2/3)). This is integrable: integral_0^1 y^(-1/3)dy=3/2; k^(-2/3) is integrable at zero; the unbounded b,k tails have Gaussian domination. Dominated convergence applied to |f_t-f_0| gives L1 convergence. The off-diagonal scaled total mass is O(t^(1/3)) by P(14.1). The limiting mass is (3/2)c>0, so dividing by the actual total mass proves (T4). Proposition 1 additionally compares the two normalized laws at rate O(t^(1/3)), without assigning that rate to their separate convergence to (T4).

The joint law of (y,b,k,u) determines the exact cubic-scale separation:
r/t^(1/3)=(y/k)^(1/3).
Extend this map arbitrarily on the cemetery mark. Pushforward contracts total variation. The true scaled separation agrees with the resulting map on near pairs; its law differs by at most the normalized far mass O(t^(1/3)). Thus the actual endpoint separation has the limiting distribution obtained from (T4), and is tight at scale t^(1/3). This is a spatial statement about actual finite bars, rather than a moment bound on extra window witnesses. It implies no bijection between an auxiliary witness population and bars.

## Proposition 4: the actual endpoint law has a seventh-power tail

This concerns the limiting ACTUAL-BAR endpoint law of T4, not an auxiliary microscopic-window witness law, whose radius-tail exponent can be different. Take t->0 first. In the limiting law let V=r/t^(1/3). Then
P{V>a}=C_endpoint a^(-7)+O(a^(-13)), a->infinity,         (T5)
where
C_endpoint=(96/(7c)) integral_(S^(d-1))
                 p_G(0) p_Vu(0) D_u phi_tau_u(0) d sigma(u)>0.
Here G,V_u,D_u,tau_u are exactly P(15.1); phi_tau is the centered scalar Gaussian density of standard deviation tau. Constants are at fixed d,L. This supplies no finite-t uniform rate or interchangeable two-parameter limit.

Proof. P(15.1)'s odd/even Gaussian factorization and birth disintegration give
integral_R A_0(b,k,u) db
      =432 k^2 p_G(0) p_Vu(0) D_u phi_tau_u(12k).
Thus the (k,u) marginal of g in T4 is
(144/c) k^(4/3) p_G(0) p_Vu(0) D_u phi_tau_u(12k).
Since V=(y/k)^(1/3) and y is independent with density (2/3)y^(-1/3),
P{V>a}=(96/c) integral_(u) p_G(0)p_Vu(0)D_u
            integral_0^1 y^(-1/3)
            integral_0^(y/a^3) k^(4/3) phi_tau_u(12k) dk dy.
By finite-jet rank and compactness of the sphere, tau_u is bounded above and away from zero, and all angular weights are bounded. Uniformly for 0<=k<=a^(-3),
phi_tau_u(12k)=phi_tau_u(0)+O(k^2).
The main inner integral is (3/7)phi_tau_u(0)(y/a^3)^(7/3); then integral_0^1 y^2 dy=1/3. This gives 96/(7c), with a^(-7). The error inner integral is O((y/a^3)^(13/3)); its y integral is finite, giving O(a^(-13)). Positivity and finiteness follow from P(15.1), c>0, and finite spherical measure. This proves T5.

As a consequence the limiting endpoint law has finite positive p-th radius moment exactly for 0<p<7, with logarithmic divergence at p=7. This follows from the nonnegative tail identity E[V^p]=p integral_0^infinity a^(p-1)P{V>a} da: the interval (0,1) is harmless and the positive tail in T5 gives both directions. This moment statement is about the limiting intensity law; it is NOT uniform integrability or convergence of the finite-t p-th moments.

## What to incorporate from the completion directive

Retain its demand for a precise observable, the global elder mark, full determinant weighting, legitimate pushforward, finite-volume normalization and legal limits. The leading fixed-torus target already supplied by P+R is
nu_eld(ell)=c_{d,L} ell^(-1/3)+O(1),
E N_eld(0,t]/Vol=(3/2)c_{d,L}t^(2/3)+O(t).
Use P(15.2) for the exact finite-torus coefficient. Reference-space coefficients and finite-torus corrections are separate quantities.

The proposed obligatory shrinking-witness uniqueness theorem is not a premise of this route. The required exact equality is instead:
actual finite-bar measure = candidate pair measure marked by GLOBAL elder death.
Every finite bar supplies its actual maximum/saddle endpoints directly, and the cap bound controls omitted candidates. Propositions 1–3 show explicitly how this route yields both persistence and endpoint geometry without assuming that a C6 auxiliary-witness count degenerates to one.

Likewise the directive's ell=k r^3 normal-form inversion problem is not required here: k is an exact height-gap coordinate, and P retains its Jacobian. A lower bound for k is needed for the compact quantitative selection probability, but unrestricted integration uses the UNNORMALIZED majorant, not a false global normalizer floor.

Historical RN/24-jet claims, auxiliary-witness regional estimates, occurrence-conditioned cluster laws, broader covariance universality, numerical finite-band error constants, and sharper third-order elder asymptotics remain separate unless a specific theorem actually consumes them. This does not supersede their own mathematical statements or rewrite their status.

No MATHEMATICAL_COMPLETION_CERTIFICATE with zero open nodes is issued. Logical proof completeness, independent review provenance, and formal/empirical validation are distinct. The blanket directive is useful only after its dependencies are matched to the actual target theorem.

## Falsifiers and review interface

A defect in the Borel marked identity, the full weight/normalizer, cap-to-global-elder implication, the unnormalized H bound, or R(R1)'s nonselected-density bound invalidates the corresponding conclusion. A cumulative bound alone is insufficient for R(R1). The shrinking cutoff proof must retain t<=rho^3; the cubic marked limit must retain k>0 and its integrable k^(-2/3) domination.

Requested scoped nonauthor review: (T1) for arbitrary common Borel marks and normalization, (T2)–(T3) moving cutoff, (T4) L1 convergence and actual-bar interpretation, (T5) the birth-integrated factor and seventh-power endpoint tail, and whether the dependency exclusion is justified. Source reacceptance, a cluster law and whole-program closure are excluded. Same-provider review earns zero organizational-independence credit.
