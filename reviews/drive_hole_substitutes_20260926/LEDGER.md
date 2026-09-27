# Drive-waiting hole ledger — substitutes vs fail-closed

**Object:** OA-DRIVE-HOLE-LEDGER-20260926-v3 (v1 amended 2026-09-27 after the nonauthor review on Math- #81; v3 records the same-day recovery of `TRANSVERSE_CONTACT_ASYMPTOTIC.md` by merged Math- #94; changes are listed in Section 5).
**Scientific effect:** NONE. Does not flip `lemma_closed`, prizes, GRAPH classifications, or Math #58/#61 dispositions.
**Rule:** emit a verification-grade substitute only when live Git identities + CAS or an existing ACCEPT review already close the claim. Do not mint missing historical filenames — and do not mint predicate filenames either.

Source identities in this ledger are given as `repository/path @ commit` with the Git blob id of the bytes classified. Math- `main` is read at `db6a8d5a099b13cec4364edb544cdf0e34ea720c`. Anything on an unmerged branch is labeled as such; a branch head is not a review record.

Related audit already on `main`: `reviews/d0_custody_audit_20260926/AUDIT.md` (blob `32c874c5b3e30743e624f3382bb63b1643379d40`, merged Math- #65) classifies the same D0 carriers and the regional bypass node with blob identities and search surfaces. This ledger does not restate that audit; Section 2 cites it and keeps only the decision that is new here — substitute versus fail-closed for each hole.

## 1. Formerly missing exposition: original recovered; reconstruction demoted to cross-check

| Name | Carrier (identity) | Status | Scope |
|---|---|---|---|
| `TRANSVERSE_CONTACT_ASYMPTOTIC.md` | **main** `imports/transverse_contact_library_20260927/TRANSVERSE_CONTACT_ASYMPTOTIC.md`, blob `c2499674d29ad4312e872903d8f5999adc1c51db`, SHA256 `e3ad42b85de72f961978fe9a33d927b54ef8bd09abbd602458e3fb640caa6a73`, 12,049 bytes; companion `GEOMETRY_AND_CUBIC_INDEX.md`, blob `58fbeb8f5180104361938253203b9dfb576af2d9`, SHA256 `4d99cfac30d7d39b69c1a8813c607109328ae310695f1bd609cbc64d5056a6d7`; provenance in `SOURCE_BINDING.json` (blob `c2d30ea8238eb243fad25acc6d8bb5ab89fb8621`); merged Math- #94 at `db6a8d5a…` | **Recovered original bytes (source availability only).** Author-side candidate disposition unchanged; the import README requests a nonauthor source-custody review and states that reviews of the consolidated PR25 note do not transfer to this exposition. Nothing is accepted by the recovery. | Fixed-chart ($\|v\|\ge\eta$) six-pin contact kernel with proposed refined theorem (2.1)–(2.3); excludes $\eta\to0$, shrinking cutoffs and global selection. This hole is **closed as a Drive hole** (bytes exist on `main`) and **open as mathematics** (unreviewed). |
| Reconstruction (Math- PR80) | `reviews/contact_kernel_substitute_20260926/SUBSTITUTE.md` + `verify_substitute.py`, head `a88d569ee85f741870ba6e7bc1d368f56fc9e3cd` (unmerged, no review file) | **Cross-check only.** Its §7 tabulates which finite identities of the recovered originals ((4.1)–(4.3), (5.1) of the companion; (5.2), (6.1), (6.2) of the exposition) its exact rational script re-derives; the type-mass constants come from NOTE §C / KERNEL_TAILS §4, not from the original. Its own nonauthor review is AMEND-addressed, unmerged. | Not a substitute, not a review of the recovered original, no credit transfer in either direction. |

The v1 heading "Substitute emitted" and the phrase "verification-grade substitute" are withdrawn. Merged Math- #59 disposed of the TRANSVERSE filename as unavailable; after #59 no file on `main` cites it as attached, so there is no consumer for a stand-in.

## 2. Cannot substitute — exact historical bytes still ABSENT

GRAPH.json (`frontiers/downstream_gate_20260925/GRAPH.json`, blob `23a6759eb0e8aca9de1da9bb5410cdb0621542d8`) records these D0 carriers as `BLOCKED_ABSENT` with fingerprint `ABSENT`, and the historical predicate below as `OPEN_HISTORICAL`. Regional bypass on the reviewed fixed annulus does **not** restore any of them. Blob-level classification and search surfaces: PR65 audit above.

| Carrier / predicate (GRAPH node) | Predicate | Why no substitute |
|---|---|---|
| `hist.rnu_env.py` | ENV-RESCOV | Missing source file. Successors do not claim byte identity. |
| `hist.allcell_fdz_enclosures.json` | ALLCELL-FDZ-Q4 | Missing cell enclosure dump. |
| `hist.CL_ANTHROPIC_BUNDLE_2026-09-17_v5.zip` | SYM-Fw-jet receipts | Missing archive. |
| `hist.OBL-H5-JETMOD` (fingerprint `status-rn-unif-jetmod`) | certified 24-jet band enclosure | OPEN_HISTORICAL. main `audits/vault_99/2026-09-25/EXTRACTED_FACTS_BATCH1.md` (main `40493865b323f0376f09d553d78f705fe613492c`, blob `4557982e18c84d91c61105994318a7c3d5df6a38`, line 18): "displayed modulus and individual RUNG2/RUNG3 checks did not discharge the full certified 24-jet band enclosure." Inventing intervals would be a fake certificate. |

v1 named a predicate file `CHART_SIDE_JETMOD_PLAN.md` and a "G12-band"; neither string exists on Math- `main` or on `d6g8k5htny-coder/main`, so both are removed. The GRAPH node id and the extracted-facts line are the sources.

Regional note already in GRAPH: `regional.fixed-annulus.high-jet-route` is `SUPERSEDED_NONBLOCKING` **only** for fixed $d=2$, fixed $L$, fixed scaled annulus, compact positive gaps, between-pin height window. CH-LIFT / Piece-2 / JETMOD remain OPEN in their original replay scopes.

## 3. Not Drive-absent — already on GitHub, still open mathematically

Rows marked **main** are bytes on Math- `main` at the commit above; rows marked **draft** are unmerged branch heads with no review file and carry no disposition.

| Hole | Carrier (identity) | Status |
|---|---|---|
| D1 A3 congruence erratum | **main** `imports/lifetime_parent_20260925/ERRATUM_CONGRUENCE.md`, blob `213594d6ca6a86fb938110f4d166d9ce275a02d0` (via PR64) | In Git. A1–A7 review still open (`PROOF_INDEX.md` line 32). |
| D1 parent §8–15 | **main** `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md`, blob `dfed3b8d318a3ab1950957f393307733a4bef3f2` | D1-A–E ACCEPT on §8–15; §2–7 selection awaits A1–A7. |
| D5 Hermite finite-r rows | **main** `reviews/d5_finite_r_hermite_repair_20260925/REPAIR.md` blob `40c7ff79a1ca45f8b5663453c3c0fed1991b2e06`, `C6_REMAINDERS.md` blob `2f8dc9badeea1bb9ded53708e90b6dc105ebbd13` | M1–M7 / S1–S4 ACCEPT in `reviews/replacement_20260925_pr19_pr21/REVIEW.md` (blob `f1868bd92b600d92901146af1caf7baf960dba9c`). |
| D5 pin outer chart (transverse cone, steep strips) | **draft** Math- PR53 `reviews/pin_neighborhood_recon_20260926/NOTE.md`, head `b77aad681f449f743d040ba8b5cb4562dd176504` (unmerged; earlier reviewed head `9a6f8a66`) | Author-side reconnaissance, AMEND. After the OpenAI/Claude comments the cone ledger was corrected to $O(r^3)$ (no logarithm) on $\kappa r\le\|s\|\le1/4$; the earlier $O(r^2\log(1/r))$ punctured-disk statement is withdrawn. Not a proof. |
| D5 inner microdisk $\|s\|\le\kappa r$ | **main** `reviews/d5_microdisk_20260926/NOTE.md` blob `19efd64e6353f083deaad58366616dff8dd5ef0a` (merged #82: constrained $\det H_M$ vanishes, no $O(r^3)$ lemma); **main** `reviews/d5_pin_microdisk_20260927/NOTE.md` blob `ac09361caac76d07f878c51ebddf6d2bea3f565f` (merged #90: bounded microdisk note, exact divided-difference algebra); closed drafts Math- PR69 head `ae45d35192c2b601c7962e0b16b282ad9e98a400` (author-side $C r^3$ candidate) and PR74 head `eb8bf7a58ec89d63868d8e281e709844b0ded47b` (same-provider xAI review with six ACCEPTs; its own text: "organizational independence is not awarded"); PR69 closed as contradicted by #82/#90 | Missing proof, not a missing Drive file. Math #58 stays open; the merged notes bound the frame, they do not close the count. |
| D5 intermediate $r\ll\|x\|\ll\rho$ | bounded by D4 remote + D5 annulus | NO COMPLETE PROOF (`SELECTOR_REGION.json` open region `intermediate-r-to-rho`). |
| D5 shrinking witness collision | D4 §6 at fixed $\eta$ | NO COMPLETE PROOF for $\eta\to0$ (`SELECTOR_REGION.json` open regions `pin-collision`, `witness-collision`). |
| Kernel tails | **main** `reviews/contact_kernel_tail_20260925/KERNEL_TAILS_AND_SMALL_GAP.md`, blob `4d03f110ac82a4d876f97d1910fe997b128c6ca9` | Author-side; kernel tails excluded from the PR25 R1–R4 acceptance (`reviews/pr25_contact_kernel_20260925/REVIEW.md`, blob `ddf6859994d1b5cee855748520f8484b99a3a921`). |
| Annulus bridge (two objects, distinct) | (a) **main** `reviews/contact_kernel_tail_20260925/ANNULUS_ASYMPTOTIC_BRIDGE.md`, blob `1ab830279a5eb3d012737a1fa4f669cbab163874`; (b) **main** `frontiers/rn_annulus_bridge_20260925/PROOF.md`, blob `6f317515b3d417661f86e2fed09bc7d950899c2b` (PR28) | (a) author-side, conditional, tails not accepted; (b) nonauthor R1–R7 ACCEPT in `reviews/pr28_annulus_bridge_nonauthor_20260925/REVIEW.md` (blob `559d72242fdb7e4e3ac4a10d10641ae1da84f40e`) at its fixed-annulus scope only. v1 wrote "ANNULUS_BRIDGE" without distinguishing them. |

## 4. What will not be written

No files named `rnu_env.py`, `allcell_fdz_enclosures.json`, or `CL_ANTHROPIC_BUNDLE_2026-09-17_v5.zip`. (`TRANSVERSE_CONTACT_ASYMPTOTIC.md` was not written by anyone in this lane; the original bytes were imported by #94 with archive-manifest provenance, see Section 1.)
No invented 24-jet interval table, and no invented predicate filename for it.
No `lemma_closed=true`.

Next useful math (not Drive recovery): the #58 microdisk count on top of merged #82/#90, or an independent (non-xAI, non-OpenAI) review of the recovered `TRANSVERSE_CONTACT_ASYMPTOTIC.md` exposition and of PR53's corrected cone ledger.

## 5. Amendments from v1 (2026-09-27)

1. Section 2: `CHART_SIDE_JETMOD_PLAN.md` and "G12-band" removed (no such strings in either repository); replaced by the GRAPH node `hist.OBL-H5-JETMOD` and the main `EXTRACTED_FACTS_BATCH1.md` line 18 source.
2. Sections 1 and 3: PR80 and PR53 relabeled as unmerged draft heads with explicit commits and no review file; "Substitute emitted" / "verification-grade" withdrawn. The D5 inner-microdisk row now cites merged #82 and #90 on `main` and the closed PR69/PR74 drafts with PR74's independence disclaimer.
3. Section 2 no longer restates PR65's carrier classification; it cites the merged audit and keeps only the substitute-versus-fail-closed decision.
4. Minor: `UNIFORM_MATRIX_CAP_AND_LIFETIME.md` given its path; the two annulus-bridge objects distinguished; the v1 header's count of main #56 as an open disposition removed (#56 closed via merged Math- #59).
5. (v3) Section 1 rewritten after merged Math- #94 imported the original `TRANSVERSE_CONTACT_ASYMPTOTIC.md` bytes: the hole is closed as a Drive hole and open as mathematics; the PR80 reconstruction is demoted from "pending candidate" to a finite-identity cross-check and cited at its current head; Section 4 no longer lists the filename as one that will not be written; `main` re-read at `db6a8d5a…`. The nine-row historical R2 remainder is unchanged by #94 (its README says so explicitly) and is unchanged here.
