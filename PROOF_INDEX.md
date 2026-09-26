# Proof availability index

This file indexes complete proof text, reviews, and explicitly incomplete proof obligations. Scientific status is unchanged by this index.

## Reviewed scoped results

- D5 all-height fixed annulus: proof `frontiers/rn_annulus_bridge_20260925/PROOF.md`; review `reviews/pr28_annulus_bridge_nonauthor_20260925/REVIEW.md`.
- D5 fixed-annulus height-window fallback: proof `frontiers/rn_thin_tube_20260925/FIXED_ANNULUS_CANDIDATE.md`; review `reviews/pr22_fixed_annulus_nonauthor_20260925/REVIEW.md`.
- D5 two-scale S6-S21: proof `frontiers/rn_thin_tube_20260925/TWO_SCALE_ADDENDUM.md`; review `reviews/replacement_20260925_pr19_pr21/TWO_SCALE_REVIEW.md`.
- D5 fixed-transverse chart: review `reviews/pr16_fixed_transverse_nonauthor_20260925/REVIEW.md`; source lineage identified in that review.
- P15 demand-one extension: exact counterexample `frontiers/three_fronts_20260924/P15_PRICE_BOUNDARY.md`.

## Open or conditional results with complete proof text in GitHub

- D1 parent lifetime theorem: `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md`; support `imports/lifetime_parent_20260925/MARKED_CYLINDER_CAP_PROOF.md`; main issue 63 reconciliation pending.
- D2 lifetime remainder: `frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md`; main issue 67.
- D3 SIDE24 coefficient: `coefficients/side24_v1/PROOF.md`; main issue 65.
- D4 RN count interface: `frontiers/three_fronts_20260924/RN_COUNT_INTERFACE.md`.
- D4 fixed-remote RN theorem: `frontiers/remote_window_20260924/PROOF.md`; main issue 76.
- D6 P15 realized covers: `frontiers/three_fronts_20260924/P15_REALIZED_COVERS.md`.
- D6 P15 restricted price theorem: `frontiers/price_budget_20260924/PROOF.md`.
- D6 P15 full price theorem: `frontiers/full_price_20260924/PROOF.md`; main issue 74.
- Collision/transfer work: `reviews/collision_mechanism_20260925/NOTE.md` and `reviews/collision_mechanism_20260925/CUMULATIVE_TRANSFER_CORRECTION.md`.
- Contact-kernel work: `reviews/contact_kernel_tail_20260925/KERNEL_TAILS_AND_SMALL_GAP.md` and `reviews/contact_kernel_tail_20260925/ANNULUS_ASYMPTOTIC_BRIDGE.md`.

## Open obligations without a complete proof yet

- D5 pin neighborhoods: strongest current derivations are `reviews/d5_finite_r_hermite_repair_20260925/REPAIR.md` and `C6_REMAINDERS.md`. NO COMPLETE PROOF YET: witness-at-pin desingularized chart, covariance/Jacobian ledger and count bound.
- D5 intermediate scale r << |x| << rho: bounded by the reviewed fixed-annulus and fixed-remote results on opposite sides. NO COMPLETE PROOF YET: uniform growing-scaled-radius bridge.
- D5 shrinking multiple-witness collision: fixed-separation machinery exists in the RN packages. NO COMPLETE PROOF YET: shrinking-separation factorial-moment/collision estimate.
- D0 historical CH-LIFT/Piece-2/24-jet obligations outside reviewed regional bypasses: see `frontiers/downstream_gate_20260925/GRAPH.json`. NO COMPLETE PROOF YET where not explicitly superseded; absent historical carriers remain ABSENT.

## Repository rule

A reviewed/closed theorem or lemma must have its full proof or immutable byte-bound mirror in this repository plus the exact review/certificate. An open theorem with a complete candidate proof must link it here. An open item without a complete proof must link the strongest partial derivation and state the missing proof explicitly. Superseded/refuted work stays available. Tests and hashes are evidence, not substitutes for analytic proof. Update this index, `claims/LANDING_CLAIMS.json`, and the D0-D7 graph together when dispositions change.
