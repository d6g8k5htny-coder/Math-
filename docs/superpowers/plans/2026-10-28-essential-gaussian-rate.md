# Matching essential-event Gaussian scale

**Goal/design:** Prove a matching `exp(-C/r^2)` lower bound for the actual
typed essential-event probability, supplementing PR522's upper bound. Restrict
the axial direction to a coordinate axis of the periodic cube; retain fixed
`d>=2,L>0` and compact birth/gap ranges with a positive gap floor.

**Approach:** Construct a literal degree-two periodic template with exact pins,
unique global maximum and Cameron-Martin norm `O(1/r)`. Prove stability under
a fixed C4 ball of zero-pin perturbations. Centered conditional variance
contraction gives that ball probability at least 1/2; symmetric Cameron-Martin
translation controls its actual cost. Retain the typed determinant weight
and full normalizer. No shrinking small-ball assumption or rotated off-lattice
Fourier mode is allowed.

**Reuse check:** Existing fixed-r positivity and inverse-moment theorems are
not recreated. Failure-mark source proofs already exist; pending review is
not described as an unproved stochastic hypothesis. Existing conditional
Cameron-Martin and Fourier machinery is reused at its exact scope.

- [x] Reconcile current PR522 head/state and inspect existing source overlap.
- [x] Derive the exact periodic template, global stability and Gaussian cost.
- [x] Write the full proof and source inventory in
  `frontiers/essential_gaussian_rate_20261028/`.
- [x] Verify finite template identities, rational trigonometric enclosures,
  norm coefficients and source bytes in normal/optimized Python modes.
- [x] Obtain a disclosed same-family technical critique and resolve its
  lattice-completion clarity finding at the final proof hash.
- [ ] Commit locally and publish a separate Draft stacked on PR522.

**Roles:** root writes proof/docs and integrates. `essential_template` supplies
template reasoning and the finite-control script; `essential_gaussian_cost`
supplies the translation/stability route; `next_marked_hypothesis` supplies
reuse-first source corrections. These are author contributions, not qualifying
different-family review. No scientific status, workflow or foreign branch changes.

**Review focus:** exact pins on the actual torus; global rather than local
maximum; fixed-radius residual event; Hessian types and `r^2` weight floor;
conditional RKHS projection; correct translation direction; no arbitrary-frame
or optimal-rate-coefficient inference.
