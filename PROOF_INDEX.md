# Proof availability index

This file indexes complete proof text, reviews, and explicitly incomplete proof obligations. Scientific status is unchanged by this index.

## Reviewed scoped results

- D5 all-height fixed annulus: proof `frontiers/rn_annulus_bridge_20260925/PROOF.md`; review `reviews/pr28_annulus_bridge_nonauthor_20260925/REVIEW.md`.
- D5 fixed-annulus height-window fallback: proof `frontiers/rn_thin_tube_20260925/FIXED_ANNULUS_CANDIDATE.md`; review `reviews/pr22_fixed_annulus_nonauthor_20260925/REVIEW.md`.
- D5 two-scale S6-S21: proof `frontiers/rn_thin_tube_20260925/TWO_SCALE_ADDENDUM.md`; review `reviews/replacement_20260925_pr19_pr21/TWO_SCALE_REVIEW.md`.
- D5 inner-belt gradient density: proof `frontiers/axial_density_20260925/PROOF.md`; review `reviews/replacement_20260925_pr19_pr21/REVIEW.md` accepts corollary (1) on `|z|<=W r^2`. That acceptance is the density bound only.
- D5 fixed-transverse chart: proof `reviews/downstream_boundary_20260925/TRANSVERSE_BOUND_CANDIDATE.md` (byte-for-byte import of commit `32b80ee085dc6a40113d1e46e333cda50d57ba21`, blob `024d927779f79fadaf932541ea6474f2995f8c50`); review `reviews/pr16_fixed_transverse_nonauthor_20260925/REVIEW.md`.
- Cumulative transfer correction: proof `reviews/collision_mechanism_20260925/CUMULATIVE_TRANSFER_CORRECTION.md`; review `reviews/d2_cumulative_correction_20260925/REVIEW.md` accepts this correction only.
- P15 demand-one extension: exact counterexample `frontiers/three_fronts_20260924/P15_PRICE_BOUNDARY.md`; review pointer in `claims/LANDING_CLAIMS.json` is [main #67](https://github.com/d6g8k5htny-coder/main/issues/67), disposition EXACT_COUNTEREXAMPLE.

## Open or conditional results with complete proof text in GitHub

- D1 parent lifetime theorem: `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md`; support `imports/lifetime_parent_20260925/MARKED_CYLINDER_CAP_PROOF.md`; main issue 63 reconciliation pending.
- D1 Section 9 Borel elder-mark repair: `reviews/d1_section9_borel_repair_20260925/REPAIR.md`. Author-side amendment; nonauthor re-review required. The parent mirror is unchanged.
- D2 lifetime remainder: `frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md`; main issue 67.
- D3 SIDE24 coefficient: `coefficients/side24_v1/PROOF.md`; main issue 65.
- D4 RN count interface: `frontiers/three_fronts_20260924/RN_COUNT_INTERFACE.md`.
- D4 fixed-remote RN theorem: `frontiers/remote_window_20260924/PROOF.md`; main issue 76.
- D5 thin-tube candidate: `frontiers/rn_thin_tube_20260925/PROOF.md`. Independent review is open. This file is distinct from the reviewed two-scale addendum and the reviewed fixed-annulus candidate.
- D5 contact-kernel tail note: `frontiers/contact_kernel_tail_20260925/NOTE.md`. Author-side. Distinct from `reviews/contact_kernel_tail_20260925/`.
- D6 P15 realized covers: `frontiers/three_fronts_20260924/P15_REALIZED_COVERS.md`.
- D6 P15 restricted price theorem: `frontiers/price_budget_20260924/PROOF.md`.
- D6 P15 full price theorem: `frontiers/full_price_20260924/PROOF.md`; main issue 74.
- Collision/transfer note: `reviews/collision_mechanism_20260925/NOTE.md`. Sections B–C: `reviews/pr25_contact_kernel_20260925/REVIEW.md` accepts R1–R4. `reviews/pr25_typed_transfer_nonauthor_20260925/REVIEW.md` accepts R1–R2 and marks R3 AMEND_REQUIRED; that cumulative amendment is the separate reviewed correction above. Section A is outside both acceptances.
- Contact-kernel work: `reviews/contact_kernel_tail_20260925/KERNEL_TAILS_AND_SMALL_GAP.md` and `reviews/contact_kernel_tail_20260925/ANNULUS_ASYMPTOTIC_BRIDGE.md`. The kernel note cites `TRANSVERSE_CONTACT_ASYMPTOTIC.md`. SOURCE NOT FOUND IN GIT / RECOVERY OPEN. The proof note is unchanged.

## Open obligations without a complete proof yet

- D5 pin neighborhoods: strongest current derivations are `reviews/d5_finite_r_hermite_repair_20260925/REPAIR.md` and `reviews/d5_finite_r_hermite_repair_20260925/C6_REMAINDERS.md`, with M1–M7 and S1–S4 accepted in `reviews/replacement_20260925_pr19_pr21/REVIEW.md`. NO COMPLETE PROOF YET: witness-at-pin desingularized chart, covariance/Jacobian ledger and count bound.
- D5 intermediate scale r << |x| << rho: bounded on opposite sides by `frontiers/remote_window_20260924/PROOF.md` and by the reviewed fixed-annulus proofs `frontiers/rn_annulus_bridge_20260925/PROOF.md` and `frontiers/rn_thin_tube_20260925/FIXED_ANNULUS_CANDIDATE.md`. NO COMPLETE PROOF YET: uniform growing-scaled-radius bridge.
- D5 shrinking multiple-witness collision: fixed-separation machinery is `frontiers/remote_window_20260924/PROOF.md` section 6, (15)–(16), at fixed `eta>0`. NO COMPLETE PROOF YET: shrinking-separation factorial-moment/collision estimate.
- D0 historical CH-LIFT/Piece-2/24-jet obligations outside reviewed regional bypasses: see `frontiers/downstream_gate_20260925/GRAPH.json`. NO COMPLETE PROOF YET where not explicitly superseded; absent historical carriers remain ABSENT.

## Repository rule

A reviewed/closed theorem or lemma must have its full proof or immutable byte-bound mirror in this repository plus the exact review/certificate. An open theorem with a complete candidate proof must link it here. An open item without a complete proof must link the strongest partial derivation and state the missing proof explicitly. Superseded/refuted work stays available. Tests and hashes are evidence, not substitutes for analytic proof. Update this index, `claims/LANDING_CLAIMS.json`, and the D0-D7 graph together when dispositions change.
