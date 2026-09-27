# D0 custody audit — 2026-09-26

**Object:** D0-PROOF-CUSTODY-AUDIT-20260926  
**Scientific effect: NONE.** This file classifies named D0 objects from current source custody. It leaves `GRAPH.json`, `SELECTOR_REGION.json`, `SOURCE_FILES.json`, landing claims, `lemma_closed`, and every historical node classification unchanged.

Pickup of Math- issue 61 is acknowledged. One bounded audit; no theorem is constructed.

## Inspected tip

| Item | Identity |
|---|---|
| Repository | `d6g8k5htny-coder/Math-` |
| Commit | `703e94744a7205d438c2df690ca62d5688812480` |
| Subject | Map reviewed fixed-annulus D5 scope without global status transfer |
| `frontiers/downstream_gate_20260925/GRAPH.json` | blob `23a6759eb0e8aca9de1da9bb5410cdb0621542d8`, 15375 bytes, sha256 `065e6a756060097bcef35055cbf2aa099905f615e82b2942770b142cf4bf2f8f` |
| `frontiers/downstream_gate_20260925/SELECTOR_REGION.json` | blob `ebffdb0969c7d3484f8fd1f4352ea290346f0318` |

## One classification each

Historical graph classifications are copied from that `GRAPH.json` and are preserved. The audit class is the custody result for this issue.

| Object | Audit class | Preserved graph classification |
|---|---|---|
| `rnu_env.py` (`hist.rnu_env.py`) | **BLOCKED_ABSENT** | `BLOCKED_ABSENT` |
| `CL_ANTHROPIC_BUNDLE_2026-09-17_v5.zip` | **BLOCKED_ABSENT** | `BLOCKED_ABSENT` |
| `allcell_fdz_enclosures.json` | **BLOCKED_ABSENT** | `BLOCKED_ABSENT` |
| ENV-RESCOV | **STILL_OPEN** | `OPEN_HISTORICAL` |
| ALLCELL-FDZ-Q4 | **STILL_OPEN** | `OPEN_HISTORICAL` |
| LOGQ-TAIL | **STILL_OPEN** | `OPEN_HISTORICAL` |
| SYM-Fw-jet | **STILL_OPEN** | `OPEN_HISTORICAL` |
| CH-LIFT | **REGIONALLY_SUPERSEDED_NONBLOCKING** | `OPEN_ACTIVE` |
| Piece-2-annulus | **REGIONALLY_SUPERSEDED_NONBLOCKING** | `OPEN_ACTIVE` |
| OBL-H5-JETMOD | **REGIONALLY_SUPERSEDED_NONBLOCKING** | `OPEN_HISTORICAL` |

No listed object is `EXACT_PROOF_IN_GIT`.

## Absent carriers

`BLOCKED_ABSENT` means no byte carrier of that filename was found. Absence stays a blocker for the historical certificate. It supplies no substitute proof.

Search evidence:

- Math- `git rev-list --all --objects` after `git fetch origin main`: no object path named `rnu_env.py`, `allcell_fdz_enclosures.json`, or `CL_ANTHROPIC_BUNDLE_2026-09-17_v5.zip`.
- Math- `git log --all -S` finds those strings only as citations, from `2f4baff` (hard gate), `dac4793` (claim audit), and `bbf63d0` (reading maps).
- Math- `git fsck --unreachable --no-reflogs`: no dangling objects printed.
- Public HEAD trees, recursive and untruncated: `main` `01d4598f182c85a5c16d807472d1ef076f33b603` (36 paths), `trial` `385c6de2e665846b4e0b0c46d351d174a8618f34`, `governance-` `7476e29c65ce82d23e0b39e7f7d98741a875a8ff`, `meta-framework` `14f6836e7ccf6a463ef6da745602debfea4d15ee`, `query-` `a61656fc7cbe704f5b874e1cae08637fb914227f`, `google-drive` `ea55c6e76edb31c48da5ce5aa0c3761d3ee49146`. None contains those three filenames.
- Full clone of `d6g8k5htny-coder/main`: `git rev-list --all --objects` has historical `docs/math_status/STATUS_RN_UNIF.md` blobs and no carrier filename path. That status path is absent on main HEAD.
- GitHub code search `owner:d6g8k5htny-coder` for `rnu_env.py` and for `allcell_fdz_enclosures.json` returns only Math- citations inside the downstream-gate package.
- Connected Drive exact-title queries returned empty: `title contains 'rnu_env.py'`, `title contains 'allcell_fdz_enclosures'`, `title contains 'CL_ANTHROPIC_BUNDLE_2026-09-17_v5'`.
- Drive `fullText` hits that mention both `rnu_env.py` and `allcell_fdz_enclosures` are absence receipts, including `1tdyP-UxOlqUifivjfdvb2uVQM5_Dxck8Ts1DPPQdinE` titled `RN_SOT_PRESENT_SCAN_2026-09-25_0958CT — still ABSENT×3 — NONAUTHORITATIVE`. Those documents are scan notes. The three carrier filenames remain absent as Drive file titles.

The historical status text cited by `frontiers/three_fronts_20260924/RN_COUNT_INTERFACE.md` is `d6g8k5htny-coder/main` blob `ccd542fb174e5a242ee343fad213aa40b35b733d` at path `docs/math_status/STATUS_RN_UNIF.md` (present in object history, absent on main HEAD). That blob records the three objects as **ABSENT** and records D3-LEMMA-RN-UNIF as OPEN. A later side-branch blob `9bde5a7ecb1fe4c71d93eaab78163c47c878df40` on `cursor/rn-unif-walkdown-scope-fixes-848aea2a` (`5c7c051`) still records the same three objects as **ABSENT** and states that ENV-RESCOV is not cleared. That side branch is outside Math- `main` and is corroborating absence text, not a recovered carrier.

Required graph edges remain: ENV-RESCOV → `hist.rnu_env.py`, ALLCELL-FDZ-Q4 → `hist.allcell_fdz_enclosures.json`, and SYM-Fw-jet → the zip with `required: false`.

## Predicates that stay open

ENV-RESCOV, ALLCELL-FDZ-Q4, LOGQ-TAIL, and SYM-Fw-jet stay **STILL_OPEN**. Their preserved classifications are `OPEN_HISTORICAL`. Fingerprints on the inspected graph are `status-rn-unif-ordered-wall-1` through `status-rn-unif-ordered-wall-4`.

- ENV-RESCOV has graph note “OPEN for historical D3; qualitatively rederived on newer routes where proved.” The required carrier `rnu_env.py` is `BLOCKED_ABSENT`, so there is no historical certificate blob to classify as exact proof.
- ALLCELL-FDZ-Q4 has graph note “Not a dependency of the fixed-remote theorem.” `SELECTOR_REGION.json` marks it `NOT_REQUIRED` on fixed-remote and on the mesoscopic scaled annulus, and `OPEN_HISTORICAL` on pin-collision, intermediate-`r`-to-`rho`, and witness-collision. `NOT_REQUIRED` on a later route leaves the historical predicate open. Its cell carrier is `BLOCKED_ABSENT`.
- LOGQ-TAIL has graph note “Replaced only inside named successors.” No regional-bypass edge names it, and no exact historical proof path was found.
- SYM-Fw-jet has graph note “Analogous interface rederived; no historical certificate identity.” The bundle named by its edge is `BLOCKED_ABSENT`.

## Regional supersession, exact scope only

CH-LIFT, Piece-2-annulus, and OBL-H5-JETMOD are **REGIONALLY_SUPERSEDED_NONBLOCKING** because the inspected graph records a scoped bypass, and because that bypass has a reviewed fixed-annulus statement behind it. Their preserved node classifications stay `OPEN_ACTIVE`, `OPEN_ACTIVE`, and `OPEN_HISTORICAL`.

Graph node `regional.fixed-annulus.high-jet-route`:

- classification `SUPERSEDED_NONBLOCKING`
- fingerprint `regional-bypass-fixed-annulus-window-v1`
- scope `fixed d=2 scaled annulus; compact positive gaps; between-pin height window`
- note: for this scope only, the reviewed analytic route bypasses CH-LIFT / Piece-2 / OBL-H5-JETMOD, and the historical predicates remain OPEN/ABSENT in their original replay scopes

Edges with relation `regional_bypass_only` run from that node to `hist.CH-LIFT`, `hist.Piece-2-annulus`, and `hist.OBL-H5-JETMOD` only. ENV-RESCOV, ALLCELL-FDZ-Q4, LOGQ-TAIL, and SYM-Fw-jet are outside that edge set.

The reviewed statement behind the bypass:

| Field | Identity |
|---|---|
| Landing claim | `rn-fixed-annulus-window`, disposition `REVIEWED_SCOPED` |
| Statement | `frontiers/rn_thin_tube_20260925/FIXED_ANNULUS_CANDIDATE.md`, blob `081abc13c5e66342c13df2af2bd6b114f320486f` |
| Review | `reviews/pr22_fixed_annulus_nonauthor_20260925/REVIEW.md`, blob `1f153966dae48d10574db0d272f75d08ca3a8b23`, disposition `ACCEPT` |
| Claimed review scope | eight declared interfaces for the fixed-annulus between-pin-height-window theorem only |
| Claim source commit recorded in `LANDING_CLAIMS.json` | `760340e921ac4ceda296b8118da936f1133e956e` |
| Reviewed subject commit recorded in the review | `2804dc1db27ef3b1fdef6bb350b486162692cc4a` |

The same statement blob is still the blob on Math- `703e947`. Landing-claim reason text: the nonauthor technical review accepts the exact fixed-annulus scope, with no global D5/RN/JETMOD transfer. The review’s own scope line is one witness in the fixed scaled annulus `1<A0<B0<∞`, dimension two, full periodic covariance at fixed `L`, compact positive marks, and a height window of length `k r^3`.

`GRAPH.json` node `math.rn-fixed-annulus-window` remains `AUTHOR_SIDE_CANDIDATE`, with `review_disposition` `ACCEPT`, `scientific_status_unchanged` true, and the same scope sentence: `d=2; fixed L; fixed scaled annulus 1<A0<=|y|<=B0<infinity; compact positive gaps k_->0; all frames; between-pin height window`. This audit does not promote that node.

`SELECTOR_REGION.json` is a separate inventory and is left as written. It still records CH-LIFT as `BYPASSED_BY_FIXED_RHO` on fixed-remote, `REOPENED` on the mesoscopic scaled annulus, and `OPEN_ACTIVE` on pin-collision and intermediate scale; Piece-2-annulus as `PARTIAL_COVER_ONLY` / `PARTIAL_PR7_REDUCTION` / `OPEN_ACTIVE`; and OBL-H5-JETMOD as `NOT_DISCHARGED` on every listed region. The audit class above names the regional bypass edge. It does not rewrite those selector rows into a global discharge, and it does not supply an exact Git proof of the old CH-LIFT, Piece-2, or 24-jet predicates.

`hist.lemma_closed` remains `FALSE` (`lemma_closed=false`) on the inspected graph. This audit does not flip it.
