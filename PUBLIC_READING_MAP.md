# Public reading map — unmerged incoming mathematics

**Date:** 2026-09-26 (tables refreshed 2026-09-27; cycle-4 pins split 2026-09-27)  
**Scientific effect:** NONE.  
This file is a visibility index. It does not accept theorems, flip `STATUS.md`, edit `claims/LANDING_CLAIMS.json`, or close lemmas.

> **Later state — pointer added 7 October 2026, read at Math- `7d2f6250`.** Everything below is the 26–27 September reading cut and is kept unchanged. Since then, [#87](https://github.com/d6g8k5htny-coder/Math-/pull/87) merged on 27 September at 23:41 UTC (merge `8c00f195`). The cycle-4 packet is now on the default branch at [`incoming/grok-cycle4-20260926/`](incoming/grok-cycle4-20260926/), and every file there matches a revised-candidate SHA-256 digest listed below. Its working branch was deleted, so the "Latest working PR head" link no longer resolves. [#80](https://github.com/d6g8k5htny-coder/Math-/pull/80), [#81](https://github.com/d6g8k5htny-coder/Math-/pull/81) and [#53](https://github.com/d6g8k5htny-coder/Math-/pull/53) merged between 23:25 and 23:38 UTC the same day, into [`reviews/contact_kernel_substitute_20260926/`](reviews/contact_kernel_substitute_20260926/), [`reviews/drive_hole_substitutes_20260926/`](reviews/drive_hole_substitutes_20260926/) and [`reviews/pin_neighborhood_recon_20260926/`](reviews/pin_neighborhood_recon_20260926/). The Firewall's AMEND line records 27 September. The linked [STATUS snapshot](https://github.com/d6g8k5htny-coder/main/blob/main/STATUS.md), last changed on 29 September, now lists D1 (Theorems A, B, C) and the planar D5 pin-neighborhood and window first moments as ACCEPT — scoped, with their stated limits. It keeps the remaining D5 quantitative obligations and the original SARD-G A1/A6 formulation as AMEND. A merge publishes bytes; it is not acceptance. For proof availability, use [PROOF_INDEX.md](PROOF_INDEX.md) and the [proof-reachability record](docs/integration/2026-10-02-proof-reachability.md); both are dated indexes, and packets merged after 3 October 2026 are not yet listed in either.

All repositories under `d6g8k5htny-coder` that hold this program are already **public**. Draft pull requests on a public repository are world-readable; they are only hidden from GitHub’s default “Ready” filter. The remaining gap is discoverability: cycle packets live on unmerged branches, not on `Math-` default.

## Default-branch reading (already public)

| Surface | URL |
|---|---|
| Research front door | https://github.com/d6g8k5htny-coder/main |
| Proof vault | https://github.com/d6g8k5htny-coder/Math- |
| Proof availability index | https://github.com/d6g8k5htny-coder/Math-/blob/main/PROOF_INDEX.md |
| Scientific status snapshot | https://github.com/d6g8k5htny-coder/main/blob/main/STATUS.md |
| Research guide | https://github.com/d6g8k5htny-coder/main/blob/main/docs/RESEARCH_INDEX.md |
| Public mathematics catalog | https://github.com/d6g8k5htny-coder/main/blob/main/docs/PUBLIC_MATHEMATICS.md |
| Claim manifest | https://github.com/d6g8k5htny-coder/Math-/blob/main/claims/LANDING_CLAIMS.json |
| Pages (main) | https://d6g8k5htny-coder.github.io/main/site/ |

## Incoming packets not on `Math-` default

These bytes are public on the cited branch and pull request. They are **review intake**, not accepted mathematics.

### Cycle-4 six-pin / D5 / SARD-G packet — Math- PR [#87](https://github.com/d6g8k5htny-coder/Math-/pull/87)

Two exact revisions are pinned. They are different candidates. Review [`5332391136`](https://github.com/d6g8k5htny-coder/Math-/pull/87#pullrequestreview-5332391136) binds only to the predecessor commit below and is not carried to the revised candidate. Scientific effect NONE. Nothing listed here is accepted. D5, SARD-G A1, and A6 remain AMEND.

#### Preserved predecessor — commit `05c20b67ca49281601532f7a0224f871a8dae8d6`

Pinned source revision: branch `incoming/harper-cycle4-d5-sard-20260926` at commit `05c20b67ca49281601532f7a0224f871a8dae8d6`. Every artifact link in this subsection resolves that exact commit. This revision includes the 2026-09-27 denominator repair (order `-r^8/12` in `CLOSED_FORMS_FTS_FTT.md`, exact-series tests) together with the earlier ledger and RI caveats. Earlier revisions (`8657130`, `0fab9330`) stay superseded for that repair; their dispositions are not carried. Review `5332391136` on this exact head accepts that denominator repair and records two defects in `D5_OBSTRUCTION_LEDGER.md` at SHA256 `ba0f5f2e48ea9704d9078fe26a042815b7228a261c7685010a28bd9e6c0ca57b`: the display `f_tt = ∓6 k r + O(r^3)`, and the claim that a marginal `f_ss(S) = O_p(1)` shows `O(r^6 q^2)` over-counts one power of `r`. The finite 8-pin grid in that review is diagnostic only. Those two assertions are withdrawn in the revised candidate; the predecessor bytes are preserved here.

| Path | What it is | SHA256 at `05c20b67ca49` |
|---|---|---|
| [harper/README.md](https://github.com/d6g8k5htny-coder/Math-/blob/05c20b67ca49281601532f7a0224f871a8dae8d6/incoming/grok-cycle4-20260926/harper/README.md) | Packet inventory, firewall and amendment log | `db1a696a30be01de74c68634f41cc276dcd0c0885297b08d7c7eabb66220c29d` |
| [harper/CLOSED_FORMS_FTS_FTT.md](https://github.com/d6g8k5htny-coder/Math-/blob/05c20b67ca49281601532f7a0224f871a8dae8d6/incoming/grok-cycle4-20260926/harper/CLOSED_FORMS_FTS_FTT.md) | Exact `Var(f_ts\|{pins})` and `Var(f_tt\|{pins})` on planar Bargmann–Fock | `27cb967a0f54cc505be7e01eb0545da1cba1bf7f4bc77baf76346a408200daad` |
| [harper/D5_OBSTRUCTION_LEDGER.md](https://github.com/d6g8k5htny-coder/Math-/blob/05c20b67ca49281601532f7a0224f871a8dae8d6/incoming/grok-cycle4-20260926/harper/D5_OBSTRUCTION_LEDGER.md) | Predecessor ledger. Contains the two assertions named in review 5332391136; those assertions are withdrawn in the revised candidate | `ba0f5f2e48ea9704d9078fe26a042815b7228a261c7685010a28bd9e6c0ca57b` |
| [harper/SARD_G_A1_RELATIVE_INTERIOR_LEMMA.md](https://github.com/d6g8k5htny-coder/Math-/blob/05c20b67ca49281601532f7a0224f871a8dae8d6/incoming/grok-cycle4-20260926/harper/SARD_G_A1_RELATIVE_INTERIOR_LEMMA.md) | Standalone RI1–RI4 / OPEN lemmas; A1 remains AMEND | `37020f4d44084faf50ed3665a18593e9554b8bce38096a2c43d8ea5d1bf2da03` |
| [harper/test_closed_forms.py](https://github.com/d6g8k5htny-coder/Math-/blob/05c20b67ca49281601532f7a0224f871a8dae8d6/incoming/grok-cycle4-20260926/harper/test_closed_forms.py) | Stdlib float and exact rational-series checks of the closed forms | `163d68b560c7640a349369b2d3431dc62eb401474ca2536dadf2f48733575573` |
| [benjamin/ALPHA_4PIN_SERIES.md](https://github.com/d6g8k5htny-coder/Math-/blob/05c20b67ca49281601532f7a0224f871a8dae8d6/incoming/grok-cycle4-20260926/benjamin/ALPHA_4PIN_SERIES.md) | Axial 4-pin remainder series | `bb951caad911dec409bf89668c25d1d1f3261dca60de6eaefe200ae60f556948` |
| [benjamin/REDUCED_FRAME_4SLOT.md](https://github.com/d6g8k5htny-coder/Math-/blob/05c20b67ca49281601532f7a0224f871a8dae8d6/incoming/grok-cycle4-20260926/benjamin/REDUCED_FRAME_4SLOT.md) | Leftover 4-slot frame after six pins | `c3d5940336ee3945ab8d6497e5fd52f02a307bff6ab4f8c3d61b951eb64a7c13` |
| [lucas/SARD_G_A1_APPLIED_TO_SUCCESSOR.md](https://github.com/d6g8k5htny-coder/Math-/blob/05c20b67ca49281601532f7a0224f871a8dae8d6/incoming/grok-cycle4-20260926/lucas/SARD_G_A1_APPLIED_TO_SUCCESSOR.md) | P1–P6 applied to successor §3 | `7e1782566079c67ddf06e15bb83c050031703391b167f38a420917beb00b16a3` |

Pinned raw tree: https://github.com/d6g8k5htny-coder/Math-/tree/05c20b67ca49281601532f7a0224f871a8dae8d6/incoming/grok-cycle4-20260926

Verify the predecessor digests from a clone: `git show 05c20b67ca49281601532f7a0224f871a8dae8d6:incoming/grok-cycle4-20260926/<path> | sha256sum`.

#### Revised candidate — commit `52c953c679dad79eec8d1f8032efc984b8f72cf2`

Intermediate revision `bc85130c12585f641ebb9b9ac3bee0ddd224cbf3` (ledger SHA256 `b2af7a0f980523d785464f4111701cfc93a0e42c2c3a11c8a7c11daff2152538`) is superseded by this commit, which adds ledger §8 (same-law transport identity and the finite 80-digit `schur_diagnostic.py`, plus `test_schur_diagnostic.py`) and merges `main` at `a650f66`. This commit does not inherit review `5332391136`. Fresh review is required. It keeps the denominator repair byte-for-byte (`CLOSED_FORMS_FTS_FTT.md` and `test_closed_forms.py` hashes match the predecessor). It replaces the two D5 assertions: `f_tt` is stated as a conditional mean plus a centered Gaussian of variance `~ r^4/6`, and the comparison of `O(r^6 q^2)` with a marginal `f_ss(S) = O_p(1)` is an open same-law transport obligation. No uniform estimate is added. The finite 8-pin grid is not used as a theorem. D5, SARD-G A1, and A6 remain AMEND.

| Path | What it is | SHA256 at `52c953c679da` |
|---|---|---|
| [harper/README.md](https://github.com/d6g8k5htny-coder/Math-/blob/52c953c679dad79eec8d1f8032efc984b8f72cf2/incoming/grok-cycle4-20260926/harper/README.md) | Packet inventory and follow-through log (second revision noted) | `2d49a4296be9401d952802bf96c0bf9f207a82347df2eebaeb50cbfff17cb57d` |
| [harper/CLOSED_FORMS_FTS_FTT.md](https://github.com/d6g8k5htny-coder/Math-/blob/52c953c679dad79eec8d1f8032efc984b8f72cf2/incoming/grok-cycle4-20260926/harper/CLOSED_FORMS_FTS_FTT.md) | Unchanged denominator repair | `27cb967a0f54cc505be7e01eb0545da1cba1bf7f4bc77baf76346a408200daad` |
| [harper/D5_OBSTRUCTION_LEDGER.md](https://github.com/d6g8k5htny-coder/Math-/blob/52c953c679dad79eec8d1f8032efc984b8f72cf2/incoming/grok-cycle4-20260926/harper/D5_OBSTRUCTION_LEDGER.md) | Revised ledger: conditional mean/variance of `f_tt`; §5 transport obligation open; §8 same-law transport identity + finite diagnostic (not a uniform estimate) | `a06ab0849894ed89770b6eb8639bf9f5b3ff9018b3588b8555d76e4598e5cf07` |
| [harper/SARD_G_A1_RELATIVE_INTERIOR_LEMMA.md](https://github.com/d6g8k5htny-coder/Math-/blob/52c953c679dad79eec8d1f8032efc984b8f72cf2/incoming/grok-cycle4-20260926/harper/SARD_G_A1_RELATIVE_INTERIOR_LEMMA.md) | Unchanged; A1 remains AMEND | `37020f4d44084faf50ed3665a18593e9554b8bce38096a2c43d8ea5d1bf2da03` |
| [harper/test_closed_forms.py](https://github.com/d6g8k5htny-coder/Math-/blob/52c953c679dad79eec8d1f8032efc984b8f72cf2/incoming/grok-cycle4-20260926/harper/test_closed_forms.py) | Unchanged exact-series checks of the denominator repair | `163d68b560c7640a349369b2d3431dc62eb401474ca2536dadf2f48733575573` |
| [harper/test_ftt_conditional_mean.py](https://github.com/d6g8k5htny-coder/Math-/blob/52c953c679dad79eec8d1f8032efc984b8f72cf2/incoming/grok-cycle4-20260926/harper/test_ftt_conditional_mean.py) | Exact series for `E[f_tt\|pins]` at `M` and `S`, second moment through `r^5`, identity-TT variance | `981eb395c3fa6f66d7b4fe0e216a72a7c3f7a1513b47785770f5e0e197da6cc5` |
| [harper/schur_diagnostic.py](https://github.com/d6g8k5htny-coder/Math-/blob/52c953c679dad79eec8d1f8032efc984b8f72cf2/incoming/grok-cycle4-20260926/harper/schur_diagnostic.py) | 80-digit direct Schur diagnostic (six- and eight-pin laws); reproduces the review 5332391136 grids; cross-checks identities TS/TT and the `E[f_tt]` series; `--mutate` control | `eaa5c23bdafa7717ee5d6d1cafa8c1fb07406e111ef85396ba268f67c488a54a` |
| [harper/test_schur_diagnostic.py](https://github.com/d6g8k5htny-coder/Math-/blob/52c953c679dad79eec8d1f8032efc984b8f72cf2/incoming/grok-cycle4-20260926/harper/test_schur_diagnostic.py) | Unit tests for the Schur diagnostic | `5d5b2921b66f5324494f5a4075c6ded52e0ffd482f6d17c8c401eb126b9439ee` |
| [benjamin/ALPHA_4PIN_SERIES.md](https://github.com/d6g8k5htny-coder/Math-/blob/52c953c679dad79eec8d1f8032efc984b8f72cf2/incoming/grok-cycle4-20260926/benjamin/ALPHA_4PIN_SERIES.md) | Unchanged axial 4-pin remainder series | `bb951caad911dec409bf89668c25d1d1f3261dca60de6eaefe200ae60f556948` |
| [benjamin/REDUCED_FRAME_4SLOT.md](https://github.com/d6g8k5htny-coder/Math-/blob/52c953c679dad79eec8d1f8032efc984b8f72cf2/incoming/grok-cycle4-20260926/benjamin/REDUCED_FRAME_4SLOT.md) | Unchanged leftover 4-slot frame | `c3d5940336ee3945ab8d6497e5fd52f02a307bff6ab4f8c3d61b951eb64a7c13` |
| [lucas/SARD_G_A1_APPLIED_TO_SUCCESSOR.md](https://github.com/d6g8k5htny-coder/Math-/blob/52c953c679dad79eec8d1f8032efc984b8f72cf2/incoming/grok-cycle4-20260926/lucas/SARD_G_A1_APPLIED_TO_SUCCESSOR.md) | Unchanged; A1 remains AMEND | `7e1782566079c67ddf06e15bb83c050031703391b167f38a420917beb00b16a3` |
| [PUBLIC_READING_MAP.md](https://github.com/d6g8k5htny-coder/Math-/blob/52c953c679dad79eec8d1f8032efc984b8f72cf2/incoming/grok-cycle4-20260926/PUBLIC_READING_MAP.md) | In-packet pointer to the predecessor hash and to this index | `e608d427d2c1b50530dfc9ef454d2c0651b745ac4092a0462c8aa33d4657622f` |

Pinned raw tree: https://github.com/d6g8k5htny-coder/Math-/tree/52c953c679dad79eec8d1f8032efc984b8f72cf2/incoming/grok-cycle4-20260926

Latest working PR head (mutable; may move past either pinned revision): https://github.com/d6g8k5htny-coder/Math-/tree/incoming/harper-cycle4-d5-sard-20260926/incoming/grok-cycle4-20260926

Verify the revised digests from a clone: `git show 52c953c679dad79eec8d1f8032efc984b8f72cf2:incoming/grok-cycle4-20260926/<path> | sha256sum`.

### Related math PRs on Math- (state as of 2026-09-27)

| PR | Title | State | Where to read |
|---|---|---|---|
| [#82](https://github.com/d6g8k5htny-coder/Math-/pull/82) | D5 microdisk frame — constrained `det H_M` vanishes; no `O(r^3)` lemma | merged to `main` (`e85de878`) | [reviews/d5_microdisk_20260926/](https://github.com/d6g8k5htny-coder/Math-/tree/main/reviews/d5_microdisk_20260926) |
| [#60](https://github.com/d6g8k5htny-coder/Math-/pull/60) | Pin microdisk: anisotropic gradient covariance and density envelope | merged to `main` (`46a2a596`) | [reviews/pin_micro_covariance_20260926/](https://github.com/d6g8k5htny-coder/Math-/tree/main/reviews/pin_micro_covariance_20260926) |
| [#90](https://github.com/d6g8k5htny-coder/Math-/pull/90) | Bounded D5 pin microdisk note and exact divided-difference algebra packet | merged to `main` (`5ee7cfea`) | [reviews/d5_pin_microdisk_20260927/](https://github.com/d6g8k5htny-coder/Math-/tree/main/reviews/d5_pin_microdisk_20260927) |
| [#69](https://github.com/d6g8k5htny-coder/Math-/pull/69) | D5 pin microdisk divided-difference | closed without merge; contradicted by #82 / #90 | branch `cursor/d5-pin-microdisk-c059` (historical) |
| [#94](https://github.com/d6g8k5htny-coder/Math-/pull/94) | Recovered original `TRANSVERSE_CONTACT_ASYMPTOTIC.md` + geometry companion (byte-preserving import; source availability only) | merged to `main` (`db6a8d5a`) | [imports/transverse_contact_library_20260927/](https://github.com/d6g8k5htny-coder/Math-/tree/main/imports/transverse_contact_library_20260927) |
| [#81](https://github.com/d6g8k5htny-coder/Math-/pull/81) | Drive-hole ledger (v3: transverse hole closed as a Drive hole, open as mathematics) | open, review amendments applied, ready for owner review | branch `grok/drive-hole-ledger-20260926` |
| [#80](https://github.com/d6g8k5htny-coder/Math-/pull/80) | Contact-kernel reconstruction note (cross-check against the recovered original, §7) | open, review amendments applied, ready for owner review | branch `grok/contact-kernel-substitute-20260926` |
| [#53](https://github.com/d6g8k5htny-coder/Math-/pull/53) | Pin-neighborhood reconnaissance (cone `O(r^3)`; inner disk open) | open, review amendments applied, ready for owner review | branch `cursor/pr16-transverse-r1r5-review-b00c` |

Merged rows are reachable on `main` at the cited paths; the merge commit is given for identity, and a merge is not acceptance beyond the scope recorded in each note.

### Related math PRs on main (state as of 2026-09-27)

| PR | Title | State |
|---|---|---|
| [#163](https://github.com/d6g8k5htny-coder/main/pull/163) | Incoming session ledger (scientific effect NONE) | merged |
| [#128](https://github.com/d6g8k5htny-coder/main/pull/128) | D5 intermediate-scale envelope | closed without merge |
| [#125](https://github.com/d6g8k5htny-coder/main/pull/125) | D5 shrinking witness pairs | merged |
| [#122](https://github.com/d6g8k5htny-coder/main/pull/122) | SARD-G execution repair | merged |

## Firewall

- Listing a file here does not accept it.
- D1 parent Theorem A, D5 pin neighborhoods, and SARD-G A1/A6 remain AMEND as recorded in [STATUS.md](https://github.com/d6g8k5htny-coder/main/blob/main/STATUS.md).
- D2/D3/D4/D6 stay at their existing scoped ACCEPT on default.
- Merge of this map is publication of pointers only.
