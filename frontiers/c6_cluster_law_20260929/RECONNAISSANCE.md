# Limited external reconnaissance — 29 September 2026

Scope: whether a scaling limit for the number of critical points of a Gaussian field near a pinned degenerate
configuration (a "cluster law" for window critical points at the scale of the pins) is already in the literature. Not a
novelty, priority or exhaustiveness claim.

## What was attempted

The Consensus connector returned its monthly quota error on every call made from this account today ("You've used all
30 searches this month; resets on October 1st"), as recorded in `frontiers/c6_palm_route_20260929/RECONNAISSANCE.md`
and `frontiers/d5_dimension_lift_20260929/RECONNAISSANCE.md`. One further call was made on 29 September 2026 at about
22:35 UTC with the query "critical points Gaussian random field near degenerate critical point scaling limit cluster
count cubic normal form fold bifurcation persistence pairs"; it returned the same quota error. No result was invented,
and no web search was performed.

## Records already cited by the consumed sources

Read from the reconnaissance sections of the consumed sources, not re-inspected here; none is imported as a theorem:

- D. Armentano, J.-M. Azaïs, J. R. León, *On a general Kac-Rice formula for the measure of a level set*,
  arXiv:2304.07424v3 — the marked Kac–Rice framework used by [C6] Lemma 5.1 and by [RM].
- L. Gass, M. Stecconi, *The number of critical points of a Gaussian field: finiteness of moments*, arXiv:2305.17586 —
  finiteness of moments for a fixed nondegenerate field; not uniform in the pinned family; not consumed.
- L. H. Y. Chen, A. Xia, *Stein's method, Palm theory and Poisson process approximation*, Ann. Probab. 32 (2004) —
  cited by [RCL]; not consumed.

## Classical facts used with a citation in the text

Bézout's theorem for two plane conics (at most four isolated common zeros); the Sylvester resultant of two quadratics;
the inverse function theorem and `C^1` stability of nondegenerate zeros; dominated convergence; Gaussian regression and
the Schur complement; the fold and cusp normal forms of a planar cubic (V. I. Arnold, *Catastrophe Theory*, 3rd ed.,
Springer 1992), cited only for the classical algebra of the unfolding, not as a probabilistic input.

## Assessment

The consumed candidates [EDL] and [LM] contain the rare-set construction and the cubic normal form as a lower-bound
device; [RCL] states the cluster law as unknown. The contribution here is to run the same construction as a
dominated-convergence limit over the whole configuration set, together with the exclusion of large soft curvature and
the separation of the near and remote regions. No claim of first discovery is made for any component.

## Addendum, 30 September 2026 (00:35Z): external check completed through web search

The Consensus connector still returned the exhausted-monthly-quota error at 00:33Z–00:35Z on 30 September (four
attempts; one returned a transient rate-limit message instead), after the owner reported that the quota had been
increased. The check was therefore made through general web search (three extended queries) and direct reads of the
arXiv abstract pages listed below. No full texts were read; no citation below is used as a source of any step of
PROOF.md, and none is invented.

| Record | What it establishes | Relation to this packet |
|---|---|---|
| D. Beliaev, V. Cammarota, I. Wigman, *Two point function for critical points of a random plane wave*, IMRN 2019(9), 2661–2689; arXiv:1704.04943 | Short-range asymptotics of the two-point function of critical points of the random plane wave: the second factorial moment of the count in a small disc of radius `rho` scales as `rho^4`; separate treatment of extrema and saddles. | Unconditioned pair statistics at short range. This packet's object is the law of the count *conditioned on a pinned birth–death pair* at separation `r` and gap `k r^3`, where the conditional second factorial moment is `Theta(r^3)` ([C6], [EDL]); different normalization and question. No cluster law there. |
| J.-M. Azaïs, C. Delmas, *Mean number and correlation function of critical points of isotropic Gaussian fields and some results on GOE random matrices*, arXiv:1911.02300 | Correlation function of critical points of isotropic fields: attraction in dimension `> 2`, neutrality in dimension `2`, repulsion in dimension `1`; the attraction comes from critical points of adjacent indices; exact GOE eigenvalue densities. | Qualitatively consistent with §6.5 and Lemma 3.6 here (the extra near points are saddles of index `d - 1`, adjacent to the pin indices `d` and `d - 1`). Unconditioned; no pinned-pair conditioning; no count law. |
| L. Gass, M. Stecconi, *The number of critical points of a Gaussian field: finiteness of moments*, arXiv:2305.17586 | All moments of the critical-point count are finite as soon as the Taylor polynomial of the relevant order is nondegenerate at every point; general method, not specific to critical points. | Background for moment methods; not the pinned conditional regime, not a small-scale rare-cluster statement. |
| M. Ancona, L. Gass, T. Letendre, M. Stecconi, *Zeros and critical points of Gaussian fields: cumulants asymptotics and limit theorems*, arXiv:2501.10226 | Cumulant asymptotics, strong law and CLT for nodal volumes and critical-point counts in the large-volume regime for stationary fields with decaying covariance. | Large-volume Gaussian fluctuation regime; no rare-event compound-Poisson or conditional cluster statement. |
| P. Pranav, *Topology and geometry of Gaussian random fields II: on critical points, excursion sets, and persistent homology*, arXiv:2109.08721 | Persistence diagrams of 3D Gaussian fields from simulations; intensity and difference maps; dependence on the power spectrum. | Numerical; no rigorous short-lifetime law for birth–death pairs. |

Conclusion of the check: no located source states or proves the conditional law of the number of additional critical
points in the height window of a pinned birth–death pair (Theorem N), its support on `{1, 2}`, or the explicit
near coefficients; the closest published relatives are the short-range two-point analyses above, which are
unconditioned. The classical pieces used in §§3.4 and 3.8 (a planar cubic normal form, Bézout, Hadamard's inequality,
Weyl's integration formula) are not claimed as new. Novelty is asserted only relative to this search; a full-text
survey was not performed.
