# Finite-radius additional-soft cluster bounds

Author-side mathematical candidate for IBA2-012. Scientific effect **NONE**.
Actual performer: OpenAI / GPT-6 Astra Pro, continuation `iba2-012-publication-audit-20261005-r3`, acting for Dylan Roy. This is the same author continuation as the preceding local proof, not an independent review.

For fixed dimension, torus side, observation radius and compact positive marks, PROOF.md proves the proposed bound

    E_{Q^W}[K^a; N_R>0, h_{q+1}<=eta] <= C r^3 (eta+r)^{q(q+7)/2}.

It also proves an unequal-scale refinement, with factors (eta_j+r)^{j+2}. The result is a finite-radius event/derivative-weight estimate. It does not establish a full cluster convergence rate, count-weighted factorial bound, all-mark statement, or general IBA2-012 closure. The separate small-k cusp proposal is not consumed.

## Reproduce

From this directory:

```sh
python -B -S test_finite_radius_cluster.py
python -B -O -S test_finite_radius_cluster.py
```

Each runs 12 test methods and prints an exact algebra ledger. Normal and optimized stdout must agree. The tests check finite polynomial integration, exponent accounting, domain-extension bounds, large-norm absorption algebra, the limiting-measure counterexample, and unequal-scale accounting. Degree-changing variants are tested within the suite. No Lean execution, random-field simulation or analytic proof acceptance follows from these tests.

SOURCES.json records the three other packet files by bytes, SHA-256 and Git blob, and the exact P/SC interfaces. Its own blob is recorded in the PR. Only these four files are introduced. No shared workflow, formal manifest, parent proof, status, scientific flag, review or prize is changed. Existing repository CI does not execute this standalone suite automatically.

## Review and integration

Pickup: main#259 comment6005046599. Credit for the limiting additional-hard slice remains with comments6003533425/6003547392. The preceding local archive has SHA-256 f2bf763ea204fc293d64fbae2b9eb68e7e37102e66ce438cc859d2465296d562.

Nonauthor review should cover SC(11) to endpoint localization, P's conditional moments/full normalizer, Vandermonde bounds before domain extension, norm-polynomial absorption before discarding Gaussian decay, the retained saddle r term, and the unequal-scale refinement. Preserve fixed d,L,R and k_->0 throughout. The author will not self-merge. Applicable exact-candidate checks, ownership reconciliation and a guarded integration remain required; a green check is not a theorem disposition.
