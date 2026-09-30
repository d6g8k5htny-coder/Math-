# Register alignment — graph nodes for the accepted STATUS rows D2, D3, D4, D5-annulus and D6

**Object:** REGISTER-ALIGNMENT-20260930-v1.
**Reconciler:** Anthropic Claude, Claude Code session `session_017Mi3hxjaxV45x6zo6o1ee3`.
**Read at:** Math- `main` `aa288385af9392c509233c25a0f4012c9ba023e5` (30 September 2026); main `STATUS.md` at `7bbbdc9`.
Re-verified at `ec6db8c` (Math-#151 merged, 30 September 00:56Z): the ten inventoried sources and the eight live nodes of
§4 are unchanged; the live graph now also carries `math.d5-component.remote-window-proof` (`PROVED_REVIEWED`, fingerprint
`a332bae9…`, `review_basis` "STATUS D4 (main#76, external)") beside the still-`AUTHOR_SIDE_CANDIDATE`
`math.rn-fixed-remote-window`: the D4 dual-node inconsistency is now live, and the `D4_DUPLICATE` check binds it.
**Revision:** v1.1 records the two xAI reads of `670e4ae` and makes the Math-#151-first ordering of the D4 flips
explicit; transitions unchanged. v1.2 re-verifies at `ec6db8c` after Math-#151 merged, binds the now-live duplicate D4
node (`D4_DUPLICATE` check, `duplicate-drift` mutant) and records that the HOLD's Math-#151 precondition is met;
transitions unchanged. v1.3 answers the two OpenAI AMEND reviews (5360320845, 5360327058) and the five Codex threads
(4139807545–67): review records and consumed sources become fingerprinted component nodes with required edges, regions
gain `covered_by` edges, `apply()` carries scope exclusions and replacement notes, a nine-case `PROPAGATION` check replays
two-commit source mutations through the production reverse-impact rule, the interface's promoted scope is narrowed to
self-contained inequalities plus conditional implications with its consumed premises as edges, the interface evidence
labels separate exact from floating-point checks, and the external issue comments are preserved in `EXTERNAL_REVIEWS.md`
and labelled as mutable evidence; the eight classifications are unchanged.
**Effect:** register reconciliation, **declarative only**. This record introduces **no new mathematical claim**. It binds
five objects that the register already lists as accepted to their exact bytes, quotes the nonauthor verdicts that
accepted them, records that their live graph nodes still carry the pre-review classification, and proposes the node
transitions in machine-readable form (`PROPOSED_TRANSITIONS.json`, `"executed": false`). It carries one bounded
nonauthor review (`RN_COUNT_INTERFACE_REVIEW.md`) of the RN count-interface note, the only unreviewed required premise
in these chains. Execution of any `GRAPH.json` change is a separate act for a **non-Claude lane**. `lemma_closed`,
prizes and premises are untouched. Scientific effect: NONE.

## 0. Exposure, stated first

- Every lane shares one GitHub account; no organizational independence is claimed anywhere below.
- I authored none of the six sources inventoried in §2 (all six are OpenAI / ChatGPT notes). I authored
  `reviews/d1_chain_reconciliation_20260928/` (Math-#126), the record that moved the D1 parent node
  `math.uniform-matrix-cap-lifetime` to `PROVED_REVIEWED`; the D2 and D3 nodes require that node. I authored
  `reviews/d5_reconciliation_20260929/` (Math-#138), executed by Math-#151, which handles the mesoscopic, pin-collision
  and intermediate regions; none of those is re-proposed here.
- Reviews cited: D2, D4, the D5 fixed annulus and D6 each rest on **one** nonauthor provider, xAI / Grok 4.7 running in
  Cursor cloud sessions on 25–26 September. D3 has two providers (xAI; Anthropic, session `01NMeKE…`, in-repo record).
  The count-interface review in §3 is by this session. No Cursor agent is restarted or contacted (owner stop of
  27 September); only their published comments are cited, with the byte identities they state.
- **Precedent and caveat.** The D1 node moved to `PROVED_REVIEWED` on xAI plus Anthropic reads. Four of the five flips
  proposed here rest on a single provider. The executing lane may ask for a second read before flipping any of them;
  this record binds what exists and says so per row. STATUS already records all five as accepted at scope.

**Verdicts on this record.** xAI inventory read 5901912476 and xAI/Grok (Lucas) review 5360240245, both at `670e4ae`:
**ACCEPT as a declarative inventory of already-accepted STATUS scopes** (classification lag, not new mathematics; no
edge, node, controlling, prize or `lemma_closed` change; single-provider caveat correctly stated; the D3 row is the
two-provider one), with **HOLD on execution** until Math-#151 is on main so that the D4 dual-node inconsistency is
resolved in one direction, and with the single-provider rows recorded as such by the executing lane. Neither read
re-read the count-interface note: that flip rests on this packet's Anthropic review alone. Both say: do not touch
witness-collision here, do not enlarge any scope, do not treat this as a prize or Boolean fold. This record agrees
on every point; v1.1 makes the #151-first ordering explicit in §4 and `execution_order`. Math-#151 merged at `ec6db8c`
(30 September 00:56Z; main#207 closed at 00:57Z), so the first HOLD condition is met; the second, that the executing
lane record the single-provider rows as such, is already stated per row in §4 and in `PROPOSED_TRANSITIONS.json` and is
that lane's to carry out.

OpenAI source-custody / RN-interface review 5360320845 and OpenAI-Codex engineering review 5360327058 (both at `f2250bf`,
with Codex threads 4139807545/51/58/62/67 at `670e4ae`): **the historical classification lag and the logical-interface
inequalities are sound at their stated scopes; AMEND the executable proposal; HOLD execution.** Their findings: the
acceptance evidence lived only in `review_sources` metadata, which the production loss-only audit
(`git_transition_audit.read_snapshot`, `node.source` only) never sees; a covering-proof change did not reach the promoted
regions; the annulus's `TWO_SCALE_ADDENDUM.md`, D6's `P15_REALIZED_COVERS.md` and the interface's consumed cap / parent
items were not tracked; `apply()` dropped `explicit_limits` and kept stale notes; the (N4)/(N5) checks were floating
point while labelled exact; external issue-comment verdicts were quoted, not preserved. v1.3 answers each (§4, §6; the
eight classifications and scope exclusions unchanged). The region-reporting complaint (4139807545) is superseded on main
since `ec6db8c` (`hard_gate.d4_region_complement` has a `proved_reviewed_regions` bucket) and is not replayed. Neither
OpenAI read is a new mathematical acceptance of the six sources; both keep the single-provider caveat.

## 1. The lag

The main `STATUS.md` accepted-scope table (rows D1–D4, D6) and `PROOF_INDEX.md` "Reviewed scoped results" list these
objects as reviewed. The downstream graph does not:

| Object | STATUS / PROOF_INDEX | Live node | Live classification | Live fingerprint |
|---|---|---|---|---|
| D2 Theorem R | accepted, `O(1)` remainder scope | `math.lifetime-remainder` | `AUTHOR_SIDE_CANDIDATE` (in-node `review_disposition: ACCEPT`) | SHA256 `380b7d0a…` = current |
| D3 SIDE24 coefficient | accepted, `d = 2, 3` arithmetic | `math.side24-coefficient` | `AUTHOR_SIDE_CANDIDATE` (in-node `ACCEPT`) | SHA256 `c06daccc…` = current |
| D4 fixed-remote theorem | accepted, fixed `ρ`, `η` | `math.rn-fixed-remote-window` | `AUTHOR_SIDE_CANDIDATE`; region `math.rn-region.fixed-remote` `COVERED_BY_CANDIDATE` | SHA256 `a332bae9…` = current |
| D5 fixed-annulus window | PROOF_INDEX reviewed row | `math.rn-fixed-annulus-window` | `AUTHOR_SIDE_CANDIDATE` (in-node `ACCEPT`); region `math.rn-region.fixed-annulus-window` `COVERED_BY_CANDIDATE` | git blob `081abc13…` = current |
| D6 P15 full price | accepted, realized family | `math.p15-full-price` | `AUTHOR_SIDE_CANDIDATE`, note "review open" | label `full-price-20260924` |
| (premise) RN count interface | — | `math.rn-count-interface` | `AUTHOR_SIDE_CANDIDATE`, unreviewed | SHA256 `aa993f52…` = current |

Why it matters: the hard gate's rule is "Only `PROVED_REVIEWED` satisfies a still-required positive premise"
(`frontiers/downstream_gate_20260925/README.md`). As long as these nodes stay author-side, the fixed-remote region is
"covered by candidate" only, and D2, D3, D4 and D6 satisfy no downstream premise, although their STATUS rows are
accepted. The register is also internally inconsistent on D4: since `ec6db8c` the live graph carries
`math.d5-component.remote-window-proof` (Math-#151, executing the D5 proposal of Math-#138) for the same bytes as
`PROVED_REVIEWED`, with `review_basis` "STATUS D4 (main#76, external), nonauthor, ACCEPT, full", beside
`math.rn-fixed-remote-window` at `AUTHOR_SIDE_CANDIDATE`. The same review either suffices for those bytes or it does
not; this record proposes that it does, on the older live node, so that the two agree; collapsing the pair is a
separate one-edge follow-up for the executing lane (§7). The `D4_DUPLICATE` check binds the duplicate's classification,
fingerprint, source and review basis to the D4 transition.

## 2. Bindings: what each review bound, and what the bytes are now

All six sources, and the two consumed sources and the addendum's review added in v1.3, are unchanged since their landing
commits. Identities of all fifteen inventoried files (six sources, the D1 parent, four in-repo reviews, two consumed
sources, this packet's two review records) are checked by `alignment_check.py` (`IDENTITIES`); the quoted verdict lines
are checked as substrings where the review is in this repository (`VERDICTS`). The issue-comment reviews are preserved
as a transcribed read-back in `EXTERNAL_REVIEWS.md` (comment id, URL, posting account, timestamps, body) and are
labelled there as mutable external evidence that an offline check cannot re-authenticate; OpenAI 5360327058 reports
having directly authenticated the D2, D3 and D4 comments.

| Object | Source now | Review binding (quoted) | Verdict (quoted) |
|---|---|---|---|
| D2 | `frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md`, 17734 B, SHA256 `380b7d0abdb0fe2de5a6564565af9560d3f1b1ce22fd5538927db0c52f4f3a4a`, blob `247b3ecf80bfbe896948d5d489b2d5842a81c481` | main#67 5841270276: "blob `247b3ecf80bfbe896948d5d489b2d5842a81c481`, 17734 bytes, SHA256 `380b7d0a…`"; 5841782206 re-read "and hashed" the same blob | 5841270276: "R1 — ACCEPT … R2 — ACCEPT … R3 — ACCEPT … R4 — ACCEPT for (R12) … R5 — IMPORTED-OPEN … R6 — IMPORTED-OPEN"; 5841782206: "R5 and R6 are **ACCEPT**. Theorem R is accepted at its stated O(1) remainder scope." The imports are mapped to #63 comment 5841570965 (D1-A…E), the review that the D1 reconciliation binds. |
| D3 | `coefficients/side24_v1/PROOF.md`, 10272 B, SHA256 `c06daccc4ba4b9168522b9888b76a7d599934fc3b91bd753ee5d492262917769`, blob `44b66f04f89fcd87383b3603fa69f1feb64cdddd` | main#65 5841269490: "commit `e329fba1…`, directory `coefficients/side24_v1/`", "`PROOF.md` 10272 bytes, SHA256 `c06daccc…`" | "All six coefficient interfaces check out. The disposition is **COEFFICIENT-CALC-REVIEWED / PARENT-IMPORTED-OPEN**." Second provider: `reviews/side24_v1_coefficient_claude_20260929/REVIEW.md` (blob `665d1683f33a7180957923c3cb2abce8ade235d1`): "Overall: **ACCEPT at the arithmetic-enclosure scope**". Owner reconciliation 5841779222 closed the package. The parent import is now the live `PROVED_REVIEWED` D1 node. |
| D4 | `frontiers/remote_window_20260924/PROOF.md`, 18355 B, SHA256 `a332bae9bdc0106ce17047f7e0409cc3d94eb610a0c7b74ba5ba2d01a1620cb7`, blob `b383bfcc88ec4ad497dff01fb6640e429ba24a84` | main#76 5841783172: "at commit `191ea7d541a486736ba7bbddfd4eac25a6c4567b` … 18355 bytes, SHA256 `a332bae9…`" | "This accepts only the fixed-ρ and fixed-η interfaces below. It does not accept a full RN or 24-jet theorem." Items 1–7: conditional covariance ACCEPT; three determinant factors and `O(k r⁵)` numerator ACCEPT; original endpoint normalizer ACCEPT; contact kernel and `O(k r⁴ ‖E‖)` remainder ACCEPT; fixed-separation factorial moments ACCEPT; selector/window mapping ACCEPT for the §7 implication only; uncovered complement ACCEPT as stated. Owner 5841861362: "returns ACCEPT on all seven fixed-rho/fixed-eta interfaces … Closing #76 as the fixed-remote REVIEW work package only." |
| D5 annulus | `frontiers/rn_thin_tube_20260925/FIXED_ANNULUS_CANDIDATE.md`, 17646 B, SHA256 `1fd9fe7141e464fd1c09ebf0318d8a701729c9c61ea24f73f7e20a9cf10c552b`, blob `081abc13c5e66342c13df2af2bd6b114f320486f` | `reviews/pr22_fixed_annulus_nonauthor_20260925/REVIEW.md` (blob `1f153966dae48d10574db0d272f75d08ca3a8b23`): "Immutable commit `2804dc1d…`", "Blob `081abc13…`", "SHA256 `1fd9fe71…`" | rows "Covariance floor … **ACCEPT**", "Cutoff `r^{1/24}` **ACCEPT**", "Rare target in the full joint gradient/height density **ACCEPT**", "Conditioned `C^3` sixth moment **ACCEPT**", at the exact scoped theorem; PR28 and later blobs excluded. |
| D6 | `frontiers/full_price_20260924/PROOF.md`, 11352 B, SHA256 `87521901ca8e5405b4d1e47f1deb1cd0326affbd6f5967b53c4178590da993f9`, blob `582180e41dca0ad815ad0f18574df42040912149` | `reviews/p15_full_price_nonauthor_20260926/REVIEW.md` (blob `07db19f826763b8faa7414ba2e403d9c45bc0b6e`): "Blob `582180e4…`", "SHA256 `87521901…`" | six rows **ACCEPT** (hazard transform and separate concavity; odd-majority worst case; global hazard direction and independence; full-block cover; sharpness; demand-one boundary). Owner 5842112010: "D6 ANALYTIC REVIEW COMPLETE … Closing #74 as the D6 review work package". |
| premise | `frontiers/three_fronts_20260924/RN_COUNT_INTERFACE.md`, 8938 B, SHA256 `aa993f5217bd70e6d1060402d121ab659f6582a098e29042c67585a345a8e3ab`, blob `371fd6d17920f2eb3b1c5ec30297acf6daf1d385` | this packet, `RN_COUNT_INTERFACE_REVIEW.md` | ACCEPT at the logical-interface scope (§3); its consumed formulation was reconstructed inside the D4 review (items 2–3). |
| D1 parent (premise of D2, D3) | `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md`, 40261 B, SHA256 `9350ad6eaba6626b93c3dedeef9e2ff816e5cdf1c8318e85fb27499141c84bc7` | live node `math.uniform-matrix-cap-lifetime`, `PROVED_REVIEWED`, four required reading-rule components (Math-#126) | not re-reviewed; checked live (`BASELINE`). |
| consumed by D5 annulus | `frontiers/rn_thin_tube_20260925/TWO_SCALE_ADDENDUM.md`, 15902 B, SHA256 `079f9399aef401d58749b3684f3acbb7f49ffdcbcac9f501b79e06c28a7f4e7d`, blob `89cae3a9734f2ec7172cd0b6b0b3af3ddd355d73` | `reviews/replacement_20260925_pr19_pr21/TWO_SCALE_REVIEW.md` (10073 B, SHA256 `04cf4c98…`, blob `89882516`): "blob `89cae3a9…`, 15902 bytes, SHA256 `079f9399…`"; the pr22 review: "Read as the imported inner bound, not re-derived: `TWO_SCALE_ADDENDUM.md` blob `89cae3a9…`" | S6–S21 and (S3)–(S5) **ACCEPT** (xAI, Math- PR34); pr22 row "Inner two-scale stitching **ACCEPT**". Component nodes `…two-scale-addendum`, `…two-scale-review` (§4). |
| consumed by D6 | `frontiers/three_fronts_20260924/P15_REALIZED_COVERS.md`, 11467 B, SHA256 `c0dbb821fb57b685a20cc321e4074456f39a9697f3104afd1f728e4732179bb9`, blob `173881916ccd0e738bdb41279e835e78e520fcbc` | the p15 review: "Read as the cited setwise dependency, and checked for the local restriction and the full-block cover: … SHA256 `c0dbb821…`. That is the digest named in the proof. The check uses (P1), (P2), and Theorem P2 there. It does not accept that note's `c_v<=p_v` price theorem" | setwise interfaces only, at the D6 review's scope. Component node `…p15-realized-covers-setwise` (§4). |
| external comments (D2, D3, D4, D6) | `reviews/register_alignment_20260930/EXTERNAL_REVIEWS.md` (this packet) | seven comments with id, account, `created_at`, `updated_at`, body; the four `cursor[bot]` reviews and three owner reconciliations | preserved read-back; mutable external evidence, labelled. Component node `…external-issue-reviews` (§4). |

## 3. The count-interface note

`RN_COUNT_INTERFACE_REVIEW.md` reviews `RN-COUNT-INTERFACE-20260924-v1` at the scope the note itself states: the Hölder
implications (N1)–(N3), the two counterexamples of its §3 and the layer-cake bound (N5), the marked Kac–Rice formula
(N6)–(N7) as a formula, and the support statement of §5. Verdict: **ACCEPT at the logical-interface scope**; it is not
an expected-count rate and is not treated as one. The finite parts are checked in `INTERFACE` in two labelled parts: exact rational arithmetic (Hölder on finite rational
distributions for `p = 2, 3`; the exponent identity of (N2); the (N3) identity; the single-`p` sharp example at
`r = 2^(−pm)`, where `E N^p = 1` and `E N = r^(3−3/p)` exactly) and floating-point numerical corroborations of arguments
proved in the review (the (N4) example's moments and the located maximum of `(t+1)^p e^(−3t)`; the identity
`∫ min(q, A e^(−t/B)) dt = B q [1 + log(A/q)]` by Simpson quadrature; the uniform tail `P(N_r > t) ≤ e³ e^(−3t)` of the
(N4) example on a grid); OpenAI 5360320845 item 2 asked for exactly this separation. The note's consumed premises are the
parent's regression law and §9 Borel-mark convention (live node `math.uniform-matrix-cap-lifetime`, with its four
reading-rule components) and the cap support source of §5 (live node `math.d1-component.marked-cylinder-cap`, SHA256
`0bf922b9…`, the digest the note quotes); both are required edges of the proposal, and the promoted scope is narrowed to
(N1)–(N5) with the counterexamples as self-contained statements and (N6)–(N7), §5 as conditional implications at formula
level. A later rigorous statement of (N6) is Lemma 5.1 of `frontiers/c6_palm_route_20260929/PROOF.md` (Math-#145),
cited for the reader and not consumed.

## 4. Proposed transitions

Eight node transitions and, since v1.3, the evidence that carries them, represented in the graph itself: eight
fingerprinted review-record / consumed-source component nodes and sixteen required edges (`PROPOSED_TRANSITIONS.json`:
`transitions`, `proposed_graph_nodes`, `proposed_graph_edges`; `edges_unchanged: false`). The change of packaging answers
OpenAI 5360320845 item 1, OpenAI 5360327058 items 1–2 and Codex threads 4139807558/4139807562/4139807567: the production
loss-only audit (`git_transition_audit.read_snapshot`) reads `node.source` only, so acceptance evidence and consumed
sources that live only in `review_sources` metadata would never revalidate a promoted object when they change. The eight
classifications and every scope exclusion are unchanged from v1.0.

| Node | Current | Proposed | Scope (STATUS row) | Review sources | Required premises after |
|---|---|---|---|---|---|
| `math.rn-count-interface` | `AUTHOR_SIDE_CANDIDATE` | `PROVED_REVIEWED` | (N1)–(N5) and the §3 counterexamples as self-contained probability statements; (N6)–(N7) and §5 as formula-level implications conditional on the parent's regression law / §9 convention and on the cap support source | this packet (`RN_COUNT_INTERFACE_REVIEW.md`, a component node); main#76 items 2–3 | `math.uniform-matrix-cap-lifetime` and `math.d1-component.marked-cylinder-cap` (both live `PROVED_REVIEWED`; the note's consumed premises); `math.align-component.rn-interface-review` |
| `math.lifetime-remainder` | `AUTHOR_SIDE_CANDIDATE` | `PROVED_REVIEWED` | Theorem R, existential `O(1)` remainder | main#67 5841270276, 5841782206 | D1 (live `PROVED_REVIEWED`); `math.align-component.external-issue-reviews` |
| `math.side24-coefficient` | `AUTHOR_SIDE_CANDIDATE` | `PROVED_REVIEWED` | coefficient arithmetic, `d = 2, 3` | main#65 5841269490; in-repo Anthropic record | D1; `…external-issue-reviews`; `…side24-review-claude` |
| `math.rn-fixed-remote-window` | `AUTHOR_SIDE_CANDIDATE` | `PROVED_REVIEWED` | fixed `ρ`, `η`, between-pin window | main#76 5841783172, 5841861362 | `math.rn-count-interface`; `…external-issue-reviews` |
| `math.rn-region.fixed-remote` | `COVERED_BY_CANDIDATE` | `PROVED_REVIEWED` | the D4 region | as the covering node | `math.rn-fixed-remote-window` (new required `covered_by` edge) |
| `math.rn-fixed-annulus-window` | `AUTHOR_SIDE_CANDIDATE` (blob fingerprint) | `PROVED_REVIEWED` (SHA256 fingerprint) | `d = 2` fixed scaled annulus, window | `reviews/pr22_…/REVIEW.md` | `math.rn-count-interface`; `…pr22-annulus-review`; `…two-scale-addendum` (the S6–S21 stitching input, which itself requires `…two-scale-review`) |
| `math.rn-region.fixed-annulus-window` | `COVERED_BY_CANDIDATE` | `PROVED_REVIEWED` | the covering node's scope | as the covering node | `math.rn-fixed-annulus-window` (new required `covered_by` edge) |
| `math.p15-full-price` | `AUTHOR_SIDE_CANDIDATE` (label fingerprint) | `PROVED_REVIEWED` (SHA256 fingerprint) | realized family, `d_i ≥ 2` | `reviews/p15_…/REVIEW.md`; main#74 5842112010 | `…external-issue-reviews`; `…p15-review`; `…p15-realized-covers-setwise` ((P1), (P2), Theorem P2 setwise only, which itself requires `…p15-review`) |

Component nodes (`kind: reading_rule_component`, `PROVED_REVIEWED`, `controlling: false`, `fingerprint` = SHA256 of the
source; one node per byte identity; none duplicates a source the live graph already carries with a fingerprint):

| Node | Source | Role | Provider | Consumed by |
|---|---|---|---|---|
| `math.align-component.rn-interface-review` | `reviews/register_alignment_20260930/RN_COUNT_INTERFACE_REVIEW.md` (this packet) | review record | Anthropic (nonauthor) | `math.rn-count-interface` |
| `math.align-component.external-issue-reviews` | `reviews/register_alignment_20260930/EXTERNAL_REVIEWS.md` (this packet: seven issue comments transcribed with id, account, timestamps and body; mutable external evidence, labelled) | external review record | xAI/Grok via Cursor (posted by `cursor[bot]`) and owner; recorded by Anthropic | D2, D3, D4, D6 |
| `math.align-component.side24-review-claude` | `reviews/side24_v1_coefficient_claude_20260929/REVIEW.md` | review record | Anthropic (other session) | D3 |
| `math.align-component.pr22-annulus-review` | `reviews/pr22_fixed_annulus_nonauthor_20260925/REVIEW.md` | review record | xAI | annulus |
| `math.align-component.two-scale-addendum` | `frontiers/rn_thin_tube_20260925/TWO_SCALE_ADDENDUM.md` (`079f9399…`, blob `89cae3a9`) | consumed proof: the S6–S21 stitching input ((S4) on `A ≤ |u| ≤ B`) | OpenAI | annulus |
| `math.align-component.two-scale-review` | `reviews/replacement_20260925_pr19_pr21/TWO_SCALE_REVIEW.md` (`04cf4c98…`, blob `89882516`) | review record of the addendum (S6–S21 and (S3)–(S5) ACCEPT) | xAI | `…two-scale-addendum` |
| `math.align-component.p15-review` | `reviews/p15_full_price_nonauthor_20260926/REVIEW.md` | review record | xAI | D6, `…p15-realized-covers-setwise` |
| `math.align-component.p15-realized-covers-setwise` | `frontiers/three_fronts_20260924/P15_REALIZED_COVERS.md` (`c0dbb821…`, blob `17388191`) | consumed interface: (P1), (P2), Theorem P2 setwise at `K ≥ K_H(d)` only, as the D6 review checked them; the note's `c_v ≤ p_v` price theorem is not included | OpenAI | D6 |

These are exactly the support dependencies the canonical claim manifest records for the annulus (`two-scale-s6-s21`)
and for the full-price theorem (`p15-realized-covers:setwise-interfaces`). The interface's two consumed premises are
the live D1 node (regression law `Q`, §9 Borel-mark convention, read with its four reading-rule components) and the live
cap component (`0bf922b9…`, the SHA256 the note quotes for its §5 support statement); the (N6) cross-reference to the
C6 Palm route's Lemma 5.1 in the review is for the reader and is not consumed.

Every proposed node keeps `controlling: false`; each candidate node's `fingerprint` becomes the SHA256 of its source in
§2, and `apply()` carries `scope`, `explicit_limits`, a replacement `notes`, `review_disposition`, `review_sources` and a
structured `review_basis` onto the node, so no promoted node keeps a "review open" or "covered by candidate only" note
(Codex 4139807551; OpenAI 5360327058 item 3). Region nodes keep `coverage_source` and gain a required `covered_by` edge
to their covering node, so that a change to the covering proof reaches the region in `reverse_impact_between` (Codex
4139807558; OpenAI 5360327058 item 1). No `hist.*`, `eng.*` or `regional.*` node moves; no live node other than the
eight changes; no live edge is removed; every added edge leaves one of this record's objects. The order in
`execution_order` creates the component nodes and edges first, then the premise, then each region after its covering
node; the D4 theorem node and its region are executed only after Math-#151 is on main (satisfied at `ec6db8c`): the D4
bytes are now carried by two live nodes on the same review, and the flip aligns the older one with the newer one; the
executing lane may then collapse `math.d5-component.remote-window-proof` onto the live node or keep both (xAI
5901912476, 5360240245). STATUS, PROOF_INDEX, SELECTOR_REGION and the catalog need no edit for this record: they
already say what the graph is being aligned to.

`alignment_check.py` applies the proposal to a copy of the live graph and replays it through the hard gate's own
validators (`validate_graph_fail_closed`, `closure_report`, `reverse_impact_between`, imported from
`frontiers/downstream_gate_20260925/hard_gate.py`): the proposed graph is well formed, no node is controlling,
`gate_ok` holds, and the loss-only reverse-impact proposal names exactly the changed nodes and their dependents.
`PROPAGATION` then runs nine two-commit mutations through `reverse_impact_between` with source snapshots in the shape of
`git_transition_audit.read_snapshot` (proof edits reach their regions and consumers; a deleted review record and an
edited external-review record reach the accepted objects and their dependents; consumed-source edits reach their
consumers; an unrelated edit and a no-op reach none of the eight), the guarantee OpenAI 5360320845 asked to be tested
rather than inferred from old-versus-new GRAPH metadata.

## 5. What is not proposed

- The mesoscopic, pin-collision and intermediate regions: Math-#151. The witness-collision region and its residual:
  Math-#160. `math.rn-mesoscopic-reduction` (legacy PR7 route): unchanged, still `AUTHOR_SIDE_REDUCTION`.
- Any second-provider reads. Where a row rests on one provider the row says so; the lane executing the flip decides
  whether that is enough, as it was not for D1.
- Any controlling flag, promotion, `lemma_closed`, prize, STATUS, PROOF_INDEX, catalog or selector edit.

## 6. Checks

`alignment_check.py` (stdlib only, run from the repository root):
- **IDENTITIES.** All fifteen inventoried files (the six sources, the D1 parent, the four in-repo reviews, the two
  consumed sources, and this packet's two review records) exist as regular files, no symlink on their paths, stated
  SHA256 and blob.
- **VERDICTS.** The quoted verdict rows and binding lines of the in-repo reviews (pr22, p15, side24, two-scale), the
  object headers of the sources, the D4 sentence that consumes the interface, the interface note's (N1)/(N4)/(N5)
  displays, the five PROOF_INDEX rows, the interface review's overall verdict and evidence labels, and the seven comment
  ids with their verdict lines and the mutability label in `EXTERNAL_REVIEWS.md` are present as substrings.
- **BASELINE.** Each transition's live node exists with exactly the recorded current classification, fingerprint,
  kind and source; the D1 node is `PROVED_REVIEWED` with its four reading-rule components `PROVED_REVIEWED`.
- **TRANSITIONS.** `declarative` true, `executed` false, `edges_unchanged` false; every proposed classification is
  `PROVED_REVIEWED` with `controlling: false`, a non-empty scope, explicit limits, replacement notes and at least one
  review source; every candidate node's fingerprint equals the SHA256 of its inventoried source; every component node
  is a `reading_rule_component`, `PROVED_REVIEWED`, non-controlling, fingerprinted to its inventoried source, with a
  role, a provider, a review basis and a consumer, one node per byte identity and none for bytes the live graph already
  carries; every added edge is well formed, new, and leaves one of this record's objects; applied to a copy of the live
  graph, no live node other than the eight changes, no live edge is removed, every flipped node's required premises (the
  live D1 node and cap component, the interface, the component nodes) are `PROVED_REVIEWED`, every region requires its
  covering node, and every applied node carries its `explicit_limits`, its replacement `notes` and a `review_basis`.
- **GATE.** The proposed graph passes the hard gate's `validate_graph_fail_closed`; `closure_report` gives `gate_ok`
  with no illegal controlling node; `reverse_impact_between(live, proposed)` runs and its impacted set (the eight nodes,
  the eight component nodes and their dependents) is recorded.
- **PROPAGATION.** Nine two-commit cases on the proposed graph with source snapshots in the shape of
  `git_transition_audit.read_snapshot`: a D4 proof edit reaches the fixed-remote region and the mesoscopic consumer; an
  annulus proof edit reaches its region; deleting the interface review record reaches the interface, D4, the annulus and
  both regions; editing the external-review record reaches D2, D3, D4, D6 and the fixed-remote region; editing the
  two-scale addendum reaches the annulus and its region; editing the realized-covers source reaches D6; a D4 fingerprint
  edit reaches the region; an unrelated edit reaches none of the eight; a no-op impacts nothing.
- **INTERFACE.** The finite content of §3, in two labelled parts: exact rational checks (Hölder for `p = 2, 3` on
  finite spaces, the (N2) exponent identity, the (N3) identity, the sharp-`p` example at `r = 2^(−pm)`, the integer
  monotonicity in (N4)) and floating-point numerical corroborations (the (N4) grid maximum, the (N5) Simpson quadrature
  at three parameter points, the (N4) example's uniform tail on a grid). The analytic arguments are in the review; the
  numerical part corroborates, it does not prove.
- **NEGATIVES.** Real filesystem faults on a temporary copy of the inventory (delete, change one byte, symlink, symlink
  parent of the D4 proof) are rejected.
- **D4_DUPLICATE.** The live graph carries `math.d5-component.remote-window-proof` as `PROVED_REVIEWED`,
  non-controlling, with the same SHA256 fingerprint and source as the D4 transition and as the inventory, a `review_basis`
  citing main#76 with verdict ACCEPT, `component_of` `math.d5-pin-neighborhood-first-moment`; and the older live node
  `math.rn-fixed-remote-window` still carries that fingerprint at `AUTHOR_SIDE_CANDIDATE`, the lag this record aligns.

Twelve mutants must fail: `allow-symlink`, `no-hash`, `stale-fingerprint`, `drop-review-source`, `controlling-true`,
`executed-flag`, `skip-interface-premise`, `holder-reversed`, `baseline-drift`, `duplicate-drift`, `region-unlinked`
(the `covered_by` edges removed before the propagation replay: proof edits no longer reach the regions) and
`review-metadata-only` (the review-record nodes and their edges removed before the replay, leaving the citations as
metadata only: a deleted or edited review record no longer reaches its accepted object).

## 7. Relation to other lanes

- **Math-#151 (Codex, D5 fold; merged at `ec6db8c`, 30 September 00:56Z, final head `609e559`):** landed as proposed,
  so the live graph carries `math.d5-component.remote-window-proof` (`PROVED_REVIEWED`, `component_of`
  `math.d5-pin-neighborhood-first-moment`, `review_basis` main#76) for the D4 bytes beside `math.rn-fixed-remote-window`
  (`AUTHOR_SIDE_CANDIDATE`); the coordination note (comment 5901742635) was not taken up before the merge. This record's
  D4 flip aligns the two; collapsing the component node to a `required` edge onto the live node is a one-edge follow-up
  for the executing lane, not proposed here.
- **Math-#160 (this session, C6 reconciliation):** already references the live D4 node with supporting edges; nothing
  there changes.
- **OpenAI reviews 5360320845 and 5360327058; Codex review 5360253242 (threads 4139807545–67):** answered by v1.3 (§0,
  §4, §6); the region-reporting thread is superseded on main since `ec6db8c` and not replayed. The single-provider caveat
  and the HOLD on execution stand until the executing lane decides.
- **Math-#163 (navigation refresh):** availability index only; disjoint.
- **main#207 (closed 30 September 00:57Z, after Math-#151 merged):** the delivery note for this record is comment
  5901889845. The executing lane for this record remains non-Claude; any new coordination thread is that lane's to open.
