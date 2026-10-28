# Source-derived Gaussian lifetime tails

**Goal and design:** Close the source norm-moment premise of the 26 October
sharp-escape packet for the explicit periodized Gaussian model, and derive
`exp(-c/r^2)` upper bounds for essential and finite long-lifetime events.
Keep fixed dimension `d>=2`, `L>0`, compact birth/gap marks with positive gap
floor, and all orthonormal frames. No marked-law, pairing or parent-acceptance
premise is used for these tail upper bounds.

**Approach:** Reuse the existing weighted-Jensen Gaussian-majorant idea, retain
posterior drift and correlations, derive the actual normalizer floor by the
corrected contact-Hessian argument, absorb the actual determinant weight, then
apply the proved sharp axial theorem. A plain all-order Markov argument gives
only faster-than-polynomial bounds and is insufficient for the new rate.

**Files:** one additive `frontiers/gaussian_lifetime_exponential_tail_20261028/`
packet containing proof, exact finite controls, source manifest and actual
verification. Standard-library Python only. Existing sources and status remain
unchanged. Root owns prose/source inventory; the existing support agent owns
only the finite-control script. Both are disclosed author contributions.

- [x] Inspect exact source, erratum, reconciliation and related Gaussian tails.
- [x] Compare live Math main `4a0d51bbd06f0d9ac731a1d1df38f25999797135` with
  frozen base `7d63d08f6cfadfd9c2ef28039a370d741126f9a0`: three commits change
  nine engineering-wrapper paths; no mathematical source changed.
- [x] Write full source-derived norm and normalizer proof with Borel death
  convention; cite the sharp escape theorem at local commit `2cbd6e8`.
- [x] Run finite controls in normal/optimized modes and bind exact source bytes.
- [x] Obtain disclosed same-family technical critique and preserve its limits.
- [ ] Inspect full staged diff, commit locally and publish both additive packets
  in one owned Draft PR for different-family review. Preserve the source-commit
  crosswalk between local authorship and published commits. No Ready or merge.

The original first-stage local-only delivery remains accurately recorded as
such. This continuation extends delivery to a separate Draft using the now
available GitHub write tools and existing project authorization; it grants no
scientific acceptance or shared-branch integration authority.

**Review focus:** posterior coefficients need not be independent or centered;
finite Jensen must include missing weight at zero; congruence is
`diag(r^(-1/2),I)`; contact convergence is in law; full normalizer appears once;
essential probability remains an upper bound; no marked-law inference follows.
