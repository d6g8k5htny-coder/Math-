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
