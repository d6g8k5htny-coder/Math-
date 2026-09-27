# Public reading map — unmerged incoming mathematics

**Date:** 2026-09-26 (tables refreshed 2026-09-27)  
**Scientific effect:** NONE.  
This file is a visibility index. It does not accept theorems, flip `STATUS.md`, edit `claims/LANDING_CLAIMS.json`, or close lemmas.

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

Pinned source revision: branch `incoming/harper-cycle4-d5-sard-20260926` at commit `05c20b67ca49281601532f7a0224f871a8dae8d6`. Every artifact link below resolves that exact commit, so the stated identity and the bytes reached by the links are bound to each other. This revision includes the 2026-09-27 amendments (denominator order `-r^8/12` in `CLOSED_FORMS_FTS_FTT.md`, exact-series tests, ledger caveats, RI predicate repairs) requested in the PR #87 review threads; earlier revisions (`8657130`, `0fab9330`) are superseded by it and their dispositions are not carried over. The packet is candidate / author-side material with open substantive review threads; nothing listed here is accepted.

| Path | What it is | SHA256 at `05c20b67ca49` |
|---|---|---|
| [harper/README.md](https://github.com/d6g8k5htny-coder/Math-/blob/05c20b67ca49281601532f7a0224f871a8dae8d6/incoming/grok-cycle4-20260926/harper/README.md) | Packet inventory, firewall and amendment log | `db1a696a30be01de74c68634f41cc276dcd0c0885297b08d7c7eabb66220c29d` |
| [harper/CLOSED_FORMS_FTS_FTT.md](https://github.com/d6g8k5htny-coder/Math-/blob/05c20b67ca49281601532f7a0224f871a8dae8d6/incoming/grok-cycle4-20260926/harper/CLOSED_FORMS_FTS_FTT.md) | Exact `Var(f_ts\|{pins})` and `Var(f_tt\|{pins})` on planar Bargmann–Fock | `27cb967a0f54cc505be7e01eb0545da1cba1bf7f4bc77baf76346a408200daad` |
| [harper/D5_OBSTRUCTION_LEDGER.md](https://github.com/d6g8k5htny-coder/Math-/blob/05c20b67ca49281601532f7a0224f871a8dae8d6/incoming/grok-cycle4-20260926/harper/D5_OBSTRUCTION_LEDGER.md) | Coordinate Jacobian `O(r^3 q^2)` vs on-axis congruence product `O(k^3 r^5 q^2)`; heuristic, no count lemma | `ba0f5f2e48ea9704d9078fe26a042815b7228a261c7685010a28bd9e6c0ca57b` |
| [harper/SARD_G_A1_RELATIVE_INTERIOR_LEMMA.md](https://github.com/d6g8k5htny-coder/Math-/blob/05c20b67ca49281601532f7a0224f871a8dae8d6/incoming/grok-cycle4-20260926/harper/SARD_G_A1_RELATIVE_INTERIOR_LEMMA.md) | Standalone RI1–RI4 / OPEN lemmas; A1 remains AMEND | `37020f4d44084faf50ed3665a18593e9554b8bce38096a2c43d8ea5d1bf2da03` |
| [harper/test_closed_forms.py](https://github.com/d6g8k5htny-coder/Math-/blob/05c20b67ca49281601532f7a0224f871a8dae8d6/incoming/grok-cycle4-20260926/harper/test_closed_forms.py) | Stdlib float and exact rational-series checks of the closed forms | `163d68b560c7640a349369b2d3431dc62eb401474ca2536dadf2f48733575573` |
| [benjamin/ALPHA_4PIN_SERIES.md](https://github.com/d6g8k5htny-coder/Math-/blob/05c20b67ca49281601532f7a0224f871a8dae8d6/incoming/grok-cycle4-20260926/benjamin/ALPHA_4PIN_SERIES.md) | Axial 4-pin remainder series | `bb951caad911dec409bf89668c25d1d1f3261dca60de6eaefe200ae60f556948` |
| [benjamin/REDUCED_FRAME_4SLOT.md](https://github.com/d6g8k5htny-coder/Math-/blob/05c20b67ca49281601532f7a0224f871a8dae8d6/incoming/grok-cycle4-20260926/benjamin/REDUCED_FRAME_4SLOT.md) | Leftover 4-slot frame after six pins | `c3d5940336ee3945ab8d6497e5fd52f02a307bff6ab4f8c3d61b951eb64a7c13` |
| [lucas/SARD_G_A1_APPLIED_TO_SUCCESSOR.md](https://github.com/d6g8k5htny-coder/Math-/blob/05c20b67ca49281601532f7a0224f871a8dae8d6/incoming/grok-cycle4-20260926/lucas/SARD_G_A1_APPLIED_TO_SUCCESSOR.md) | P1–P6 applied to successor §3 | `7e1782566079c67ddf06e15bb83c050031703391b167f38a420917beb00b16a3` |

Pinned raw tree: https://github.com/d6g8k5htny-coder/Math-/tree/05c20b67ca49281601532f7a0224f871a8dae8d6/incoming/grok-cycle4-20260926

Latest working PR head (mutable; may move past the pinned revision): https://github.com/d6g8k5htny-coder/Math-/tree/incoming/harper-cycle4-d5-sard-20260926/incoming/grok-cycle4-20260926

Verify the digests from a clone: `git show 05c20b67ca49281601532f7a0224f871a8dae8d6:incoming/grok-cycle4-20260926/<path> | sha256sum`.

### Related math PRs on Math- (state as of 2026-09-27)

| PR | Title | State | Where to read |
|---|---|---|---|
| [#82](https://github.com/d6g8k5htny-coder/Math-/pull/82) | D5 microdisk frame — constrained `det H_M` vanishes; no `O(r^3)` lemma | merged to `main` (`e85de878`) | [reviews/d5_microdisk_20260926/](https://github.com/d6g8k5htny-coder/Math-/tree/main/reviews/d5_microdisk_20260926) |
| [#60](https://github.com/d6g8k5htny-coder/Math-/pull/60) | Pin microdisk: anisotropic gradient covariance and density envelope | merged to `main` (`46a2a596`) | [reviews/pin_micro_covariance_20260926/](https://github.com/d6g8k5htny-coder/Math-/tree/main/reviews/pin_micro_covariance_20260926) |
| [#90](https://github.com/d6g8k5htny-coder/Math-/pull/90) | Bounded D5 pin microdisk note and exact divided-difference algebra packet | merged to `main` (`5ee7cfea`) | [reviews/d5_pin_microdisk_20260927/](https://github.com/d6g8k5htny-coder/Math-/tree/main/reviews/d5_pin_microdisk_20260927) |
| [#69](https://github.com/d6g8k5htny-coder/Math-/pull/69) | D5 pin microdisk divided-difference | closed without merge; contradicted by #82 / #90 | branch `cursor/d5-pin-microdisk-c059` (historical) |
| [#81](https://github.com/d6g8k5htny-coder/Math-/pull/81) | Drive-hole ledger | open draft, AMEND | branch `grok/drive-hole-ledger-20260926` |
| [#80](https://github.com/d6g8k5htny-coder/Math-/pull/80) | Contact-kernel substitute | open draft, AMEND | branch `grok/contact-kernel-substitute-20260926` |
| [#53](https://github.com/d6g8k5htny-coder/Math-/pull/53) | Pin-neighborhood reconnaissance | open draft, AMEND | branch `cursor/pr16-transverse-r1r5-review-b00c` |

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
