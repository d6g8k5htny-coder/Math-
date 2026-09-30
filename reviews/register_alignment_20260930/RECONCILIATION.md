# Register alignment — graph nodes for the accepted STATUS rows D2, D3, D4, D5-annulus and D6

**Object:** REGISTER-ALIGNMENT-20260930-v1.
**Reconciler:** Anthropic Claude, Claude Code session `session_017Mi3hxjaxV45x6zo6o1ee3`.
**Read at:** Math- `main` `aa288385af9392c509233c25a0f4012c9ba023e5` (30 September 2026); main `STATUS.md` at `7bbbdc9`.
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
accepted. The register is also internally inconsistent on D4: the D5 proposal (Math-#138, executed by Math-#151)
creates `math.d5-component.remote-window-proof` for the same bytes as `PROVED_REVIEWED`, with `review_basis`
"STATUS D4 (main#76, external), nonauthor, ACCEPT, full". The same review either suffices for those bytes or it does
not; this record proposes that it does, on the live node, and asks the executing lane to collapse the duplicate (§7).

## 2. Bindings: what each review bound, and what the bytes are now

All six sources are unchanged since their landing commits (`git log` on each path shows one commit). Identities are
checked by `alignment_check.py` (`IDENTITIES`); the quoted verdict lines are checked as substrings where the review is
in this repository (`VERDICTS`).

| Object | Source now | Review binding (quoted) | Verdict (quoted) |
|---|---|---|---|
| D2 | `frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md`, 17734 B, SHA256 `380b7d0abdb0fe2de5a6564565af9560d3f1b1ce22fd5538927db0c52f4f3a4a`, blob `247b3ecf80bfbe896948d5d489b2d5842a81c481` | main#67 5841270276: "blob `247b3ecf80bfbe896948d5d489b2d5842a81c481`, 17734 bytes, SHA256 `380b7d0a…`"; 5841782206 re-read "and hashed" the same blob | 5841270276: "R1 — ACCEPT … R2 — ACCEPT … R3 — ACCEPT … R4 — ACCEPT for (R12) … R5 — IMPORTED-OPEN … R6 — IMPORTED-OPEN"; 5841782206: "R5 and R6 are **ACCEPT**. Theorem R is accepted at its stated O(1) remainder scope." The imports are mapped to #63 comment 5841570965 (D1-A…E), the review that the D1 reconciliation binds. |
| D3 | `coefficients/side24_v1/PROOF.md`, 10272 B, SHA256 `c06daccc4ba4b9168522b9888b76a7d599934fc3b91bd753ee5d492262917769`, blob `44b66f04f89fcd87383b3603fa69f1feb64cdddd` | main#65 5841269490: "commit `e329fba1…`, directory `coefficients/side24_v1/`", "`PROOF.md` 10272 bytes, SHA256 `c06daccc…`" | "All six coefficient interfaces check out. The disposition is **COEFFICIENT-CALC-REVIEWED / PARENT-IMPORTED-OPEN**." Second provider: `reviews/side24_v1_coefficient_claude_20260929/REVIEW.md` (blob `665d1683f33a7180957923c3cb2abce8ade235d1`): "Overall: **ACCEPT at the arithmetic-enclosure scope**". Owner reconciliation 5841779222 closed the package. The parent import is now the live `PROVED_REVIEWED` D1 node. |
| D4 | `frontiers/remote_window_20260924/PROOF.md`, 18355 B, SHA256 `a332bae9bdc0106ce17047f7e0409cc3d94eb610a0c7b74ba5ba2d01a1620cb7`, blob `b383bfcc88ec4ad497dff01fb6640e429ba24a84` | main#76 5841783172: "at commit `191ea7d541a486736ba7bbddfd4eac25a6c4567b` … 18355 bytes, SHA256 `a332bae9…`" | "This accepts only the fixed-ρ and fixed-η interfaces below. It does not accept a full RN or 24-jet theorem." Items 1–7: conditional covariance ACCEPT; three determinant factors and `O(k r⁵)` numerator ACCEPT; original endpoint normalizer ACCEPT; contact kernel and `O(k r⁴ ‖E‖)` remainder ACCEPT; fixed-separation factorial moments ACCEPT; selector/window mapping ACCEPT for the §7 implication only; uncovered complement ACCEPT as stated. Owner 5841861362: "returns ACCEPT on all seven fixed-rho/fixed-eta interfaces … Closing #76 as the fixed-remote REVIEW work package only." |
| D5 annulus | `frontiers/rn_thin_tube_20260925/FIXED_ANNULUS_CANDIDATE.md`, 17646 B, SHA256 `1fd9fe7141e464fd1c09ebf0318d8a701729c9c61ea24f73f7e20a9cf10c552b`, blob `081abc13c5e66342c13df2af2bd6b114f320486f` | `reviews/pr22_fixed_annulus_nonauthor_20260925/REVIEW.md` (blob `1f153966dae48d10574db0d272f75d08ca3a8b23`): "Immutable commit `2804dc1d…`", "Blob `081abc13…`", "SHA256 `1fd9fe71…`" | rows "Covariance floor … **ACCEPT**", "Cutoff `r^{1/24}` **ACCEPT**", "Rare target in the full joint gradient/height density **ACCEPT**", "Conditioned `C^3` sixth moment **ACCEPT**", at the exact scoped theorem; PR28 and later blobs excluded. |
| D6 | `frontiers/full_price_20260924/PROOF.md`, 11352 B, SHA256 `87521901ca8e5405b4d1e47f1deb1cd0326affbd6f5967b53c4178590da993f9`, blob `582180e41dca0ad815ad0f18574df42040912149` | `reviews/p15_full_price_nonauthor_20260926/REVIEW.md` (blob `07db19f826763b8faa7414ba2e403d9c45bc0b6e`): "Blob `582180e4…`", "SHA256 `87521901…`" | six rows **ACCEPT** (hazard transform and separate concavity; odd-majority worst case; global hazard direction and independence; full-block cover; sharpness; demand-one boundary). Owner 5842112010: "D6 ANALYTIC REVIEW COMPLETE … Closing #74 as the D6 review work package". |
| premise | `frontiers/three_fronts_20260924/RN_COUNT_INTERFACE.md`, 8938 B, SHA256 `aa993f5217bd70e6d1060402d121ab659f6582a098e29042c67585a345a8e3ab`, blob `371fd6d17920f2eb3b1c5ec30297acf6daf1d385` | this packet, `RN_COUNT_INTERFACE_REVIEW.md` | ACCEPT at the logical-interface scope (§3); its consumed formulation was reconstructed inside the D4 review (items 2–3). |
| D1 parent (premise of D2, D3) | `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md`, 40261 B, SHA256 `9350ad6eaba6626b93c3dedeef9e2ff816e5cdf1c8318e85fb27499141c84bc7` | live node `math.uniform-matrix-cap-lifetime`, `PROVED_REVIEWED`, four required reading-rule components (Math-#126) | not re-reviewed; checked live (`BASELINE`). |

## 3. The count-interface note

`RN_COUNT_INTERFACE_REVIEW.md` reviews `RN-COUNT-INTERFACE-20260924-v1` at the scope the note itself states: the Hölder
implications (N1)–(N3), the two counterexamples of its §3 and the layer-cake bound (N5), the marked Kac–Rice formula
(N6)–(N7) as a formula, and the support statement of §5. Verdict: **ACCEPT at the logical-interface scope**; it is not
an expected-count rate and is not treated as one. The finite parts are checked exactly (`INTERFACE`): Hölder on finite
rational distributions for `p = 2, 3`; the exponent identity of (N2); the (N4) example's moments and the finiteness of
`sup_(t≥1) (t+1)^p e^(−3t)`; the single-`p` sharp example at `r = 2^(−pm)`, where `E N^p = 1` and `E N = r^(3−3/p)`
exactly; the identity `∫ min(q, A e^(−t/B)) dt = B q [1 + log(A/q)]`; and the uniform tail `P(N_r > t) ≤ e³ e^(−3t)` of
the (N4) example. The rigorous version of (N6) is Lemma 5.1 of `frontiers/c6_palm_route_20260929/PROOF.md` (Math-#145,
reviewed), whose fixed-remote instance is the D4 formula (12)–(14).

## 4. Proposed transitions

Eight node transitions, no edge change, no new node (`PROPOSED_TRANSITIONS.json`):

| Node | Current | Proposed | Scope (STATUS row) | Review sources | Required premises after |
|---|---|---|---|---|---|
| `math.rn-count-interface` | `AUTHOR_SIDE_CANDIDATE` | `PROVED_REVIEWED` | logical interface (N1)–(N7), §5 | this packet; main#76 items 2–3 | none |
| `math.lifetime-remainder` | `AUTHOR_SIDE_CANDIDATE` | `PROVED_REVIEWED` | Theorem R, existential `O(1)` remainder | main#67 5841270276, 5841782206 | D1 (live `PROVED_REVIEWED`) |
| `math.side24-coefficient` | `AUTHOR_SIDE_CANDIDATE` | `PROVED_REVIEWED` | coefficient arithmetic, `d = 2, 3` | main#65 5841269490; in-repo Anthropic record | D1 |
| `math.rn-fixed-remote-window` | `AUTHOR_SIDE_CANDIDATE` | `PROVED_REVIEWED` | fixed `ρ`, `η`, between-pin window | main#76 5841783172, 5841861362 | `math.rn-count-interface` |
| `math.rn-region.fixed-remote` | `COVERED_BY_CANDIDATE` | `PROVED_REVIEWED` | the D4 region | as the covering node | covering node |
| `math.rn-fixed-annulus-window` | `AUTHOR_SIDE_CANDIDATE` (blob fingerprint) | `PROVED_REVIEWED` (SHA256 fingerprint) | `d = 2` fixed scaled annulus, window | `reviews/pr22_…/REVIEW.md` | `math.rn-count-interface` |
| `math.rn-region.fixed-annulus-window` | `COVERED_BY_CANDIDATE` | `PROVED_REVIEWED` | the covering node's scope | as the covering node | covering node |
| `math.p15-full-price` | `AUTHOR_SIDE_CANDIDATE` (label fingerprint) | `PROVED_REVIEWED` (SHA256 fingerprint) | realized family, `d_i ≥ 2` | `reviews/p15_…/REVIEW.md`; main#74 5842112010 | none |

Every proposed node keeps `controlling: false`; each candidate node's `fingerprint` becomes the SHA256 of its source
in §2, and each gains `review_disposition`, `review_sources` and `scope` fields in the form the D1 node already has.
Region nodes keep their `coverage_source`. No `hist.*`, `eng.*` or `regional.*` node moves; no edge is added or removed.
The order in `execution_order` puts the premise first and each region after its covering node. STATUS, PROOF_INDEX,
SELECTOR_REGION and the catalog need no edit for this record: they already say what the graph is being aligned to.

`alignment_check.py` applies the proposal to a copy of the live graph and replays it through the hard gate's own
validators (`validate_graph_fail_closed`, `closure_report`, `reverse_impact_between`, imported from
`frontiers/downstream_gate_20260925/hard_gate.py`): the proposed graph is well formed, no node is controlling,
`gate_ok` holds, and the loss-only reverse-impact proposal names exactly the changed nodes and their dependents,
which the executing lane revalidates as part of the fold (as Math-#151 did).

## 5. What is not proposed

- The mesoscopic, pin-collision and intermediate regions: Math-#151. The witness-collision region and its residual:
  Math-#160. `math.rn-mesoscopic-reduction` (legacy PR7 route): unchanged, still `AUTHOR_SIDE_REDUCTION`.
- Any second-provider reads. Where a row rests on one provider the row says so; the lane executing the flip decides
  whether that is enough, as it was not for D1.
- Any controlling flag, promotion, `lemma_closed`, prize, STATUS, PROOF_INDEX, catalog or selector edit.

## 6. Checks

`alignment_check.py` (stdlib only, run from the repository root):
- **IDENTITIES.** All ten inventoried files exist as regular files, no symlink on their paths, stated SHA256 and blob.
- **VERDICTS.** The quoted verdict rows and binding lines of the three in-repo reviews, the object headers of the six
  sources, the D4 sentence that consumes the interface, the interface note's (N1)/(N4)/(N5) displays, and the five
  PROOF_INDEX rows are present as substrings.
- **BASELINE.** Each transition's live node exists with exactly the recorded current classification, fingerprint,
  kind and source; the D1 node is `PROVED_REVIEWED` with its four reading-rule components `PROVED_REVIEWED`.
- **TRANSITIONS.** `declarative` true, `executed` false; every proposed classification is `PROVED_REVIEWED` with
  `controlling: false`; every candidate node's fingerprint equals the SHA256 of its inventoried source; every node has
  a non-empty scope and at least one review source; applied to a copy of the live graph, every flipped candidate's
  required premises are `PROVED_REVIEWED` and every flipped region's `coverage_source` is `PROVED_REVIEWED`; edges
  and `hist.*` nodes unchanged.
- **GATE.** The proposed graph passes the hard gate's `validate_graph_fail_closed`; `closure_report` gives `gate_ok`
  with no illegal controlling node; `reverse_impact_between(live, proposed)` runs and its impacted set is recorded.
- **INTERFACE.** The exact checks of §3.
- **NEGATIVES.** Real filesystem faults on a temporary copy of the inventory (delete, change one byte, symlink, symlink
  parent of the D4 proof) are rejected.

Nine mutants must fail: `allow-symlink`, `no-hash`, `stale-fingerprint`, `drop-review-source`, `controlling-true`,
`executed-flag`, `skip-interface-premise`, `holder-reversed`, `baseline-drift`.

## 7. Relation to other lanes

- **Math-#151 (Codex, D5 fold):** its proposal creates `math.d5-component.remote-window-proof` for the D4 bytes. If
  this record is executed, that node should be collapsed to a `required` edge onto the live
  `math.rn-fixed-remote-window` (coordination note posted on #151, comment 5901742635); if #151 lands first, the
  collapse is a one-edge follow-up.
- **Math-#160 (this session, C6 reconciliation):** already references the live D4 node with supporting edges; nothing
  there changes.
- **Math-#163 (navigation refresh):** availability index only; disjoint.
- **main#207:** register coordination issue; this record is a separate, additive proposal for the same non-Claude lane.
