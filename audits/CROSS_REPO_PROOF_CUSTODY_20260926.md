# Cross-repository proof custody — 2026-09-26

Scientific effect: **NONE**. This manifest records where proof text lives. It does not accept a theorem, edit a proof, change `lemma_closed`, or update `claims/LANDING_CLAIMS.json`.

Pickup of the single cross-repo custody audit. Distinct from Math PR 54, which edits `PROOF_INDEX.md` on `chatgpt/proof-index-20260925-v2`. This file is the only added artifact. `PROOF_INDEX.md` is absent from Math default `1e1114f5eb8ef8cdbcde591bf74126274c250f88`.

Vault99 paths on `main` were not opened. Private `sandbox` contents were not read.

## Pins

| Repo | Default branch | Commit |
|---|---|---|
| `d6g8k5htny-coder/main` | `main` | `01d4598f182c85a5c16d807472d1ef076f33b603` |
| `d6g8k5htny-coder/Math-` | `main` | `1e1114f5eb8ef8cdbcde591bf74126274c250f88` |
| `d6g8k5htny-coder/meta-framework` | `main` | `14f6836e7ccf6a463ef6da745602debfea4d15ee` |
| `d6g8k5htny-coder/google-drive` | `main` | `ea55c6e76edb31c48da5ce5aa0c3761d3ee49146` |
| `d6g8k5htny-coder/governance-` | `main` | `7476e29c65ce82d23e0b39e7f7d98741a875a8ff` |
| `d6g8k5htny-coder/trial` | `main` | `c14dccdf03683444575832469328350d2bfb507f` |
| `d6g8k5htny-coder/query-` | `main` | `a61656fc7cbe704f5b874e1cae08637fb914227f` |
| `d6g8k5htny-coder/sandbox` | — | HTTP 404 to this token; registry marks it private |

Nondefault research tip used when default navigation points there: `main` branch `chatgpt/drive-github-hardening-20260919` at `ebedb7802024fa557e9071e4c9cec7cddc474b89`.

Classes: `AUTHORITATIVE_SOURCE`, `REVIEW_RECORD`, `EXPERIMENT_ONLY`, `SUPERSEDED`, `ABSENT/UNRESOLVED`.

`proof_index`: whether Math `PROOF_INDEX.md` needs a link or import once that index is on default. This audit does not add those links.

## Release blockers

Reviewed or self-labeled closed objects whose full proof text is absent from every default branch.

| ID | Class | Where the proof bytes are | Default-branch proof | Review path | `proof_index` |
|---|---|---|---|---|---|
| `fixed-transverse-count` | `AUTHORITATIVE_SOURCE` off default | Math commit `32b80ee085dc6a40113d1e46e333cda50d57ba21`, path `reviews/downstream_boundary_20260925/TRANSVERSE_BOUND_CANDIDATE.md`, blob `024d927779f79fadaf932541ea6474f2995f8c50`, 9902 bytes. Same blob is on unmerged `chatgpt/proof-index-20260925-v2`. Commit `32b80ee` is not an ancestor of Math `1e1114f`. | Absent (HTTP 404 at Math `main`) | Math `reviews/pr16_fixed_transverse_nonauthor_20260925/REVIEW.md`, blob `4003ff13cf696389b9530fd445ee46daf3b4c646`, on default. R1–R5 **ACCEPT** for the declared qualitative theorem. | **Yes. Import that exact blob onto Math default.** |
| `EC-014` | `AUTHORITATIVE_SOURCE` off default | `main` `ebedb780`, `drive/mirrors/.../02_CORE_LEMMAS/LEMMA_EC-014_v2.0 — Six-Pin Pair-Frame Jacobian/proof.md.export.txt`, blob `7189b4d1538866594c6d8c94f09e247a2cd65abe`, 11331 bytes. Status blob `38db98eb3199907ce8e795cb128d7f30a116fe3c` says `CLOSED — EXACT CORRECTED SIX-PIN PAIR-FRAME JACOBIAN AND CONTACT-POWER IDENTITY`. | Absent from `main` default and from Math default | `independent_review.json.export.txt` beside the proof; review id `1QzlaLR9OStGhOMVeECitanMt7ecxmDREjMOHOAOWSJ4` | **No Math import.** Custody gap is `main` default versus the hardening branch. |
| `EC-015` | `AUTHORITATIVE_SOURCE` off default | proof blob `7bcafa247f80297009f7450df28ece5cae58073c`, 7196 bytes; status blob `27462d2573d26fe7ff77bbde1d0331181e500c15`. Label: `CLOSED — EXACT NONEMPTY WITNESS-PARAMETERIZED DEGREE-FOUR PRCP EVENT`. | Absent from both defaults | review id `1Hp0Kg1XGCnulfeSm2qON0V26b-_HP-HEU2aNI7LHEkg` | **No Math import.** |
| `EC-021` | `AUTHORITATIVE_SOURCE` off default | proof blob `fce94e3b77a2851ce76fa05002ecb1fd6faea1e9`, 8269 bytes; status blob `33e99c515cc82d9f99881cf22cbe3358684c583b`. Label: `CLOSED — EXACT UNIFORM POSITIVE TYPED FINITE-Q4 PALM MASS`. | Absent from both defaults | review id `1Ed5R7jycID1OmXyDgzpQd8Apy_e8LHlMBrKsKOVJ31Q` | **No Math import.** |
| `P02-LM-001` | `AUTHORITATIVE_SOURCE` off default | proof blob `de9995e3e312894434fb747a689ee2c6df725d8b`, 17261 bytes; status blob `0256324facdf782744cc7223ab55aa1aacc38681`. Label: `CLOSED — CONDITIONAL EXACT DEGREE-FOUR DETERMINISTIC CAPTURE MAJORANT`. | Absent from both defaults | review id `1iEv2eMApYfugkePc2kIGlLalXqaAfN5fQwou6CyDFp8` | **No Math import.** |
| `P02-LM-002` | `AUTHORITATIVE_SOURCE` off default | proof blob `d1fd7eccd5947cb6c5bf8724a77b7ec1c380a29b`, 9748 bytes; status blob `80c0258f53e643df3fdae554314ed76a59907480`. Label: `CLOSED — EXACT UNIFORM r^4 DETERMINANT-WEIGHT SECOND-MOMENT INTERFACE`. | Absent from both defaults | review id `1JaNPnyxAHXJNy45e4Wvrgx2ltYJB4saCZTnWQv-cOaQ` | **No Math import.** |
| `P02-LM-005` | `AUTHORITATIVE_SOURCE` off default | proof blob `8fa134312a4fba7307b97e70498605a41b71ec82`, 15009 bytes; status blob `50418ee2b623a4efa8548aec475f3b934e98a9db`. Label: `CLOSED — EXACT UNIFORM NINE-JET GAUSSIAN DENSITY AND MOMENT INTERFACE`. Status text also says the legacy capsule lacked marker-delimited byte identity. | Absent from both defaults | review id `1LcMVKIBcg0RzZf60lcXaYLB8x0HcVqifI4TqV9Wn2nQ` | **No Math import.** |
| `P02-LM-007` | `AUTHORITATIVE_SOURCE` off default | proof blob `f895c56c1abfabb6da48e7fc1d8a67a24e2583e9`, 12936 bytes; status blob `d59f245e9e2c7271302973d9c57a2b53d6b14e62`. Label: `CLOSED — EXACT UNIFORM CONDITIONED FIFTH-DERIVATIVE SUPREMUM TAIL`. | Absent from both defaults | review id `1EGjAK3pAtF1CzPUrCW11jXhF4IP2T_Md6C886T13vhQ` | **No Math import.** |
| `P02-LM-008` | `AUTHORITATIVE_SOURCE` off default | proof blob `70112651948447cf95f94c620e17c0e2bbc4dd99`, 12160 bytes; status blob `d0e1db89dfbcb8439c95a6b05677f4c6bb24cafe`. Label: `CLOSED — EXACT DETERMINANT-WEIGHTED PALM-TAIL TRANSFER INTERFACE`. | Absent from both defaults | review id `1sbm4z64ro7mHyMtswaBz-IO7BLmrxj6xAjPBdMDYDD4` | **No Math import.** |
| `main#59` matroid palette specialization | Issue text is the only GitHub statement | `d6g8k5htny-coder/main` issue 59, closed 2026-09-25. Body is 4686 characters and cites Edmonds, J. Res. NBS 69B (1965), Theorem 1. No default-branch file carries this argument. | Absent as a file | Closing comment says the package is complete at author-side scope and points at later Math sources for the realized-family successor | **Yes, if the closed #59 argument is to have a default-branch file.** The successor family proofs below are already on Math default. |

Those eight lemma status records say parent-theorem effect is none. Their own labels still say closed, and the proof files are GitHub objects only on the nondefault branch. That is the default-branch release block.

## Open candidates whose full proof is off default

| ID | Class | Proof | Default-branch proof | Review | `proof_index` |
|---|---|---|---|---|---|
| `P15-B` palette-separated localization | `AUTHORITATIVE_SOURCE` off default; Drive copy has the same digest | `main` `ebedb780`, path `drive/mirrors/2026-09-16 — PRIZE PROBLEM RECONNAISSANCE — INDEPENDENT TRACK/06_TALAGRAND_DISCRETE — RESTRICTED_PROOF_CANDIDATES/P15-B_PALETTE_SEPARATED_LOCALIZATION.md`, blob `deab15ebd40e473374ec5943b0163a4a246081aa`, 6286 bytes, SHA256 `9b18b6e9abc90d18deef06ab12e3aa7794dad40e1618d99daa88e369c300e8c3`. Drive file `19D-eHQAIXMGGy2ThZUfZ0GGjIKWm5C2j` is the copy named from `main` `docs/RESEARCH_INDEX.md`. | Absent from `main` default and from Math default | `main` `ebedb780` `reviews/records/REV-P15-B.md` is a `REVIEW_RECORD`. It records HOLD, `prize_closed` false, and external review unresolved. | **Link the blob.** A Math import is optional because the bytes already exist on the hardening branch. Default `main` still does not contain the path. |
| `D3-LEMMA-RN-UNIF` | `ABSENT/UNRESOLVED` as a proof; status note is not the proof | `main` `ebedb780` `docs/math_status/STATUS_RN_UNIF.md` states `lemma_closed: false` and names three absent historical carriers (`rnu_env.py`, `CL_ANTHROPIC_BUNDLE_2026-09-17_v5.zip`, `allcell_fdz_enclosures.json`). | No proof file on either default | `main` `docs/RESEARCH_INDEX.md` points at this status file and at `docs/RESEARCH_EXECUTION.md` on the hardening branch | **No.** State: no complete proof on a default branch. |
| `OBL-H5-JETMOD` | `ABSENT/UNRESOLVED` | Named OPEN from `main` default `README.md` and from `docs/OPEN_PROBLEMS.md` on `ebedb780` | No complete 24-jet proof on either default | Open-problem note | **No.** |
| `TRANSVERSE_CONTACT_ASYMPTOTIC` | `ABSENT/UNRESOLVED` | Cited by Math default `reviews/contact_kernel_tail_20260925/KERNEL_TAILS_AND_SMALL_GAP.md` as an expanded exposition. No blob found on the seven public default trees. Math PR 59 records the source as unavailable. | Absent | The kernel-tail note itself is on Math default and says it is author-side, with separate review required | **No import** until a byte identity exists. The kernel-tail note is not a substitute for the missing exposition. |

## Navigated proofs present on Math default

`main` `docs/RESEARCH_INDEX.md` and Math `README.md` / `claims/LANDING_CLAIMS.json` point at these. Blobs are from Math `1e1114f`.

| ID | Class | Repo / path / blob | Completeness | Review | `proof_index` |
|---|---|---|---|---|---|
| `marked-cylinder-cap` | `AUTHORITATIVE_SOURCE` | Math `imports/lifetime_parent_20260925/MARKED_CYLINDER_CAP_PROOF.md`, blob `0633aca3c2a2`, 15160 bytes, SHA256 `0bf922b9203c29088b12388807aa0e2ecd020485eb0f6e919679841b5b2636fc`. Drive `1BnPods7Lf-ECdD34noQihZcEfcqpy7R5` is the pre-import original. | Full text on Math default. `main` `docs/RESEARCH_INDEX.md` still cites only the Drive URL. | `main` issue 63, **open** | **Yes, link the in-repo path.** Import already done. |
| `uniform-matrix-cap-lifetime` | `AUTHORITATIVE_SOURCE` | Math `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md`, blob `dfed3b8d318a`, 40261 bytes, SHA256 `9350ad6eaba6626b93c3dedeef9e2ff816e5cdf1c8318e85fb27499141c84bc7` (matches `meta-framework` `registry.json` `parent_source.sha256`). Drive `1foDgiDi4XIKOfbrZEE8dWKV_BkZU8LIb`. | Full text on Math default. Research index still cites only Drive. | `main` issue 63, **open** | **Yes, link.** |
| `side24-coefficient` | `AUTHORITATIVE_SOURCE` | Math `coefficients/side24_v1/PROOF.md`, blob `44b66f04f89fcd87383b3603fa69f1feb64cdddd`, 10272 bytes | Full enclosure proof on default. Parent interpretation stays conditional on issue 63. | `main` issue 65, **closed**. Issue text says the closure is the coefficient handoff and leaves the parent unreviewed. | Link already implied by README and `registry.json`. |
| `lifetime-remainder` | `AUTHORITATIVE_SOURCE` | Math `frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md`, blob `247b3ecf80bfbe896948d5d489b2d5842a81c481`, 17734 bytes | Theorem R text on default. Landing disposition `FAIL_CLOSED` because parent interfaces are external. | `main` issue 67, **open** | Already in `docs/NAVIGATION.json`. |
| `rn-count-interface` | `AUTHORITATIVE_SOURCE` for the interface and counterexamples | Math `frontiers/three_fronts_20260924/RN_COUNT_INTERFACE.md`, blob `371fd6d17920f2eb3b1c5ec30297acf6daf1d385`, 8938 bytes | The three-determinant integral is explicitly unevaluated. Global RN proof: **no complete proof.** | `main` issue 67, **open** | Already in `docs/NAVIGATION.json`. |
| `rn-fixed-remote-window` | `AUTHORITATIVE_SOURCE` | Math `frontiers/remote_window_20260924/PROOF.md`, blob `b383bfcc88ec4ad497dff01fb6640e429ba24a84`, 18355 bytes, SHA256 `a332bae9bdc0106ce17047f7e0409cc3d94eb610a0c7b74ba5ba2d01a1620cb7` | Full fixed-remote argument on default. | `main` issue 76, **closed**, with an ACCEPT comment for seven fixed-rho/fixed-eta interfaces. `docs/NAVIGATION.json` omits this path. | **Yes, link.** Registry key `rn-fixed-remote-window` already routes the proof. |
| `rn-fixed-annulus-window` | `AUTHORITATIVE_SOURCE` | Math `frontiers/rn_thin_tube_20260925/FIXED_ANNULUS_CANDIDATE.md`, blob `081abc13c5e66342c13df2af2bd6b114f320486f`, 17646 bytes. Research index cites commit `760340e921ac4ceda296b8118da936f1133e956e`; that blob is still the default-tip blob. | Scoped theorem text on default. | Math `reviews/pr22_fixed_annulus_nonauthor_20260925/REVIEW.md`, blob `1f153966dae48d10574db0d272f75d08ca3a8b23`, **ACCEPT** at the fixed d=2 annulus scope. | **Yes, link.** |
| `p15-realized-covers` | `AUTHORITATIVE_SOURCE` | Math `frontiers/three_fronts_20260924/P15_REALIZED_COVERS.md`, blob `173881916ccd0e738bdb41279e835e78e520fcbc`, 11467 bytes | Theorem P on the realized family. | `main` issue 67, **open** | Already in `docs/NAVIGATION.json`. |
| `p15-price-boundary` | `AUTHORITATIVE_SOURCE` | Math `frontiers/three_fronts_20260924/P15_PRICE_BOUNDARY.md`, blob `1d6946658e00e2446d68e8a4884425d4bcec62fb`, 2266 bytes | Exact counterexample text on default. | `main` issue 67, **open** | Already in `docs/NAVIGATION.json`. |
| `p15-price-budget` | `AUTHORITATIVE_SOURCE` | Math `frontiers/price_budget_20260924/PROOF.md`, blob `9b17d179d2408dae9ea497d3c6e5c6538d2c3b8b`, 7935 bytes | Theorem T1 on default, restricted domain. | `main` issue 67, **open** | Already in `docs/NAVIGATION.json`. |
| `p15-full-price` | `AUTHORITATIVE_SOURCE` | Math `frontiers/full_price_20260924/PROOF.md`, blob `582180e41dca0ad815ad0f18574df42040912149`, 11352 bytes | Theorem F on default. | Math `reviews/p15_full_price_nonauthor_20260926/REVIEW.md` on the same tip: **ACCEPT** Theorem F at the realized-family statement. `main` issue 74 remains **open**. Landing disposition is still `HOLD_WITH_DOMAIN`. | **Yes, link the new review.** Proof path is already in `docs/NAVIGATION.json`. |

## Other Math default proof files

These are on Math default and are not copied from `trial`. Several already have in-repo reviews. They are listed so a later index can see them. This audit does not promote them.

| Path | Blob | Bytes | Class | Review on default | `proof_index` |
|---|---|---:|---|---|---|
| `frontiers/axial_density_20260925/PROOF.md` | `a72418d78fd3` | 10858 | `AUTHORITATIVE_SOURCE` | `reviews/replacement_20260925_pr19_pr21/REVIEW.md` accepts the listed interfaces | Link |
| `frontiers/rn_annulus_bridge_20260925/PROOF.md` | `6f317515b3d4` | 16948 | `AUTHORITATIVE_SOURCE` | `reviews/pr28_annulus_bridge_nonauthor_20260925/REVIEW.md` R1–R7 **ACCEPT** | Link |
| `frontiers/rn_thin_tube_20260925/PROOF.md` | `338d92d1f6be` | 14743 | `AUTHORITATIVE_SOURCE` (tube candidate) | Separate from the fixed-annulus ACCEPT | Link as its own object |
| `frontiers/rn_thin_tube_20260925/TWO_SCALE_ADDENDUM.md` | `89cae3a9734f` | 15902 | `AUTHORITATIVE_SOURCE` | `reviews/replacement_20260925_pr19_pr21/TWO_SCALE_REVIEW.md` | Link |
| `reviews/collision_mechanism_20260925/NOTE.md` | `3ee3082911f4` | 16243 | `AUTHORITATIVE_SOURCE` | `reviews/pr25_contact_kernel_20260925/REVIEW.md` accepts Sections B–C interfaces | Link |
| `reviews/collision_mechanism_20260925/CUMULATIVE_TRANSFER_CORRECTION.md` | `044ac5fdaf403a38e33983e31f0ad69f8e76d6d5` | 3272 | `AUTHORITATIVE_SOURCE` | `reviews/d2_cumulative_correction_20260925/REVIEW.md` **ACCEPT** for the correction only | Link |
| `reviews/contact_kernel_tail_20260925/KERNEL_TAILS_AND_SMALL_GAP.md` | `26890787afe6` | 10695 | `AUTHORITATIVE_SOURCE` for the note’s own derivations | Author-side; separate review required in the file | Link |
| `reviews/contact_kernel_tail_20260925/ANNULUS_ASYMPTOTIC_BRIDGE.md` | `1ab830279a5e` | 7737 | `AUTHORITATIVE_SOURCE` conditional on named inputs | Author-side | Link |
| `frontiers/contact_kernel_tail_20260925/NOTE.md` | `8da0cc852310` | 13359 | `AUTHORITATIVE_SOURCE` conditional | Author-side | Link |
| `reviews/d1_section9_borel_repair_20260925/REPAIR.md` | `fe9b9ce49999` | 9062 | `AUTHORITATIVE_SOURCE` for the Section 9 replacement | Successor text; parent file unchanged | Link |
| `reviews/d5_finite_r_hermite_repair_20260925/C6_REMAINDERS.md` | `2f8dc9badeea` | 8054 | `AUTHORITATIVE_SOURCE` | Replacement review accepts M1–M7 and S1–S4 | Link |
| `frontiers/downstream_gate_20260925/README.md` | `7f07316b733a` | 3559 | Engineering control, not a mathematical proof | `main` issue 90, **closed** | No theorem import |

`claims/LANDING_CLAIMS.json` on this tip still records `audited_default_commit` `760340e921ac4ceda296b8118da936f1133e956e`. The statement blobs checked above still match that manifest. The new full-price review file is outside the manifest. This audit leaves the manifest unchanged.

## Other repositories

| Object | Class | Finding | `proof_index` |
|---|---|---|---|
| `meta-framework` `registry.json` | Routing record | Byte routes for the coefficient, three-fronts, price, and remote-window artifacts. It does not contain proof bodies. It omits the lifetime-parent imports, fixed annulus, annulus bridge, and axial density. `scientific_status_authority` is false. | Use as a route, not as a proof. |
| `google-drive` `replicas/side24-coefficient-v1/ENCLOSURE.json` | Output replica, blob `57af39a05e14` (same bytes as Math `ENCLOSURE.json`) | Numerical output only. The proof remains Math `coefficients/side24_v1/PROOF.md`. | No. |
| `governance-` `REVIEW_TOPOLOGY.md` | Working contract | Default tree is three files. No theorem proof. | No. |
| `governance-` `amendments/20260925-math16-transverse-review.md` at `a1fc2c1f5b1a90d08c4b3cd20b418eeecf8fca1a`, blob `a2495644c8ae08526903faf5a372b5c77e508695`, 4004 bytes | `REVIEW_RECORD` | Off `governance-` default. The Math PR16 review says this note was not used as analytic evidence. | No. The transverse proof import above is the custody gap. |
| `query-` `portable/*.json` and `research_query.py` | `EXPERIMENT_ONLY` | Lookup stubs and a read-only checker. No proof bodies. | No. |
| `trial` default tree | `EXPERIMENT_ONLY` | No path matching PROOF, THEOREM, or LEMMA at `c14dccdf`. Batch briefs and integration logs stay in `trial`. | No. |
| `sandbox` | `ABSENT/UNRESOLVED` for this scan | Named by `main` `docs/RESEARCH_INDEX.md` and by `registry.json` as the private experiment repo. This token cannot read it (HTTP 404). Nothing from it is copied here. | No. |
| `main` `audits/vault_99/2026-09-25/` | Unread | Present on `main` default. Contents not inspected. | No. |
| `main` `history/2025/body.original.txt` | Historical text on default | Landing manifest treats it as historical identity, not a current proof. | No. |
| Hardening `drive/mirrors/` bulk tree | Historical mirror on a nondefault branch | Contains many further notes, including Theorem B repair material and SIDE24 ratification copies. Default navigation points at the branch generally through `README.md`, `docs/RESEARCH_MAP.md`, and `docs/OPEN_PROBLEMS.md`. Those files are not current default-branch proofs. They were not imported. | No bulk import. |

## Machine-navigation gaps that are not missing proofs

`main` `docs/NAVIGATION.json` `public_targets` lists seven Math paths. It omits the remote-window proof, the fixed-annulus candidate, the lifetime-parent imports, and every later reviewed Math proof in the table above. The prose research index already links the remote window and the fixed annulus. The lifetime parents are linked there only as Drive URLs, while the byte mirrors are on Math default.
