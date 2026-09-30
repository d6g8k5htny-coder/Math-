# C6 / witness collision — closure of the leading-mass-localization residual

**Object:** C6-RESIDUAL-CLOSURE-20260930-v1.
**Reconciler:** Anthropic Claude, Claude Code session `session_017Mi3hxjaxV45x6zo6o1ee3`.
**Read at:** Math- `main` `358f2562efbccc59f9549e5a79650e2e936395c3` (30 September 2026, after Math-#159 `98fdb54`, Math-#164
`7d0c89a` and Math-#162 `358f256` merged; `GRAPH.json`, `PROOF_INDEX.md`, `SELECTOR_REGION.json` and the catalog are
unchanged since `ec6db8c`); re-verified at `fa1cf7b` (Math-#166 merged at `ab13a08f`, Math-#167 merged at `fa1cf7b`; the
same surfaces unchanged) and at `fe2c3ff` (Math-#172: custody repair of the two-scale packet; `TWO_SCALE_LAW.md` unchanged,
`REVIEW_RECORD.md` extended and `REVIEW_RECORD.json` added; register surfaces unchanged).
**Revision:** v1.0 at `358f256`; v1.1 at `fa1cf7b` binds Math-#166's `TWO_SCALE_LAW.md` and its review record as the
direct statement (execution step 0 satisfied), adds Route C (the pair-count corollary of Math-#160 comment 5901994240,
checked in 5902616692) with its exact checks, and makes this record's own node supporting; v1.2 at `fe2c3ff` rebinds the
two-scale review record to its Math-#172 bytes and binds `REVIEW_RECORD.json`, which pins the native body digest of
review 5360227991. Pickup: Math-#160 comment 5902470285; delivery 5902585446.
**Effect:** register reconciliation, **declarative only** (`PROPOSED_TRANSITIONS.json`, `"executed": false`). It binds the
residual question that Math-#160 §5 named (`math.rn-region.witness-collision.leading-mass-localization`) to the exact
merged bytes of two independently authored and cross-provider-reviewed proofs, writes the four-line corollary that turns
their reviewed statements into the residual, and proposes the residual node `PROVED_REVIEWED` at existential fixed-`d`
compact-mark window scope. The corollary is elementary bookkeeping, not new mathematics; §3 says exactly what it uses.
Execution of any `GRAPH.json`, `STATUS`, `PROOF_INDEX` or catalog change is a separate act for a **non-Claude lane**.
`lemma_closed`, prizes and premises are untouched. Scientific effect: NONE.

## 0. Exposure, stated first

- Every lane shares one GitHub account; no organizational independence is claimed anywhere below.
- I authored Math-#160, whose §5 defines the residual closed here; this record binds that definition to others' proofs,
  it does not review them. I authored none of the three sources of §2 and reviewed none of them.
- Both routes of §3 consume `frontiers/remote_collision_20260928/PROOF.md` ([RC], Math-#110) for the far region (its
  Corollaries D and E); that packet is Claude-authored, by this session per Math-#160 §0, with OpenAI (5342280263) and
  xAI (5342481786, frozen in `reviews/d5_remote_collision_grok_20260928`) nonauthor records. I am therefore
  source-exposed to both routes through one imported input; the routes' own reviewers are named per route below.
- Route A (Math-#162) is OpenAI-authored; its Slice A reviewer (Anthropic Claude 5359968447) declares no authorship of
  the consumed sources; its Slice B reviewer (Anthropic Claude 5359845136) authored the consumed [C6], [DL], [RC] and the
  competing Math-#159 (source-exposed); its Slice C reviewer (OpenAI/Codex 5359879627) is the author's provider. Route B
  (Math-#159) is Anthropic-authored (the Slice B reviewer's session) and accepted by OpenAI (5360192822), source-exposed
  as author of imported inputs and of Math-#161. Neither route carries an organizationally independent read; taken
  together they are the first item in this chain with a proof from each provider, each read by the other.
- The third source (Math-#166, OpenAI; merged at `ab13a08f`) carries one Anthropic read per slice (5360227991, 5360178611,
  5360216551; another session) and, per Math-#160 comments 5902410407 and 5902466075, an xAI bounded read of Theorem L
  (5901945424) not re-read here; I reviewed none of it. Route C was posted by an OpenAI lane (Math-#160 comment
  5901994240) and checked by this session (5902616692): a provider-distinct nonauthor read of a consumer of
  Math-#159 / [DL] / [C6], source-exposed on [RC].
- No Cursor agent is restarted or contacted (owner stop, 27 September 2026); only published records are cited.

## 1. The residual, as defined, and the register as it stands

**Definition (Math-#160 `RECONCILIATION.md` §5, v1.3–v1.7, unchanged; head `eba6045`).** With `o` the midpoint of the pins
and `N` the window count of critical points other than the pins,

    lim_{R -> oo} limsup_{r -> 0} r^-3 E_{Q_r^W} #{ ordered pairs (X, X') of distinct window points :
                                                     not both |X - o| <= R r and |X' - o| <= R r } = 0.       (Res)

Math-#160 §5 records what the landed chain gave: pairs within `C_d r` of `o` carry `>= c r^3` ([EDL] (A4)); both-remote
pairs carry `O(r^5)` ([RC]); pairs with a witness in the shells `R r <= |X - o| <= s_0` carry `<= C r^3 (R^-2 + s_0^2)`
([PALM] §6 R3); and the open piece was the mixed count `M(R, s_0)` of pairs with one witness within `R r` of `o` and the
other at distance `>= s_0`, where [PALM] R4 gives `C r^3` only. (Res) is equivalent to `lim_{s_0} lim_R limsup_r r^-3
M(R, s_0) = 0`.

**Register at `358f256`.** `GRAPH.json` does not carry the residual node (Math-#160 proposes it, `OPEN_ACTIVE`, required
by nothing); `math.rn-region.witness-collision` is `OPEN_ACTIVE`, fingerprint "eta->0 mutual witness separation", notes
"… the regional shrinking pin/witness-collision mechanism and its source-bound graph fold remain open" (Math-#151);
`PROOF_INDEX.md` reads "NO COMPLETE REGIONAL PROOF YET: `math.rn-region.witness-collision` remains `OPEN_ACTIVE`; the
global `Theta(r^3)` result is not a proof of that node"; catalog C6 asks to "prove or refute the shrinking-separation
witness-collision mechanism encoded by the open graph node". Math-#160 §1a records that no surface defines that
mechanism other than by (Res). Both Math-#159 (§9) and Math-#162 (README) state that they move no register node.

## 2. Sources bound (exact bytes on `main` `358f256`)

| Tag | File | Bytes · SHA256 · blob | Author | Nonauthor record | What is used (§3) |
|---|---|---|---|---|---|
| [SC] | `frontiers/spectral_cluster_closure_20260929/PROOF.md` (Math-#162, merged `358f256`) | 25006 · `e971b2cbe50a8a06b47c1219191201e0d1037c9adac23e5e3b7d2051bb70c2eb` · `16c56821b52fd76b0be791622b9c3809eafde75a` | OpenAI | in-repo `REVIEW_RECORD.md` (5629 · `6031d366…` · `9bcae183`): A Claude 5359968447 (§§2–3), B Claude 5359845136 (§§4–6), C OpenAI/Codex 5359879627 (§§7–8), all ACCEPT at the conditional scope | Theorem (3); (18) near limit; (20) exhaustion; (24) mixed event; (26) factorial-moment limits |
| [SC-R] | `frontiers/spectral_cluster_closure_20260929/README.md` | 5084 · `b1e2a072…` · `895dded8` | OpenAI | — | scope statement |
| [CL] | `frontiers/c6_cluster_law_20260929/PROOF.md` (Math-#159 v1.2, merged `98fdb54`) | 70131 · `96b8e2d59defee6059bf151a896b7fc7c91fc529b385a3db8a87574901197b38` · `ba492c8e62e58bfc055fc8254c790e893d346ba5` | Anthropic (other session) | OpenAI review 5360192822 at `f7c3395`, same blob: ACCEPT Theorem N, Corollaries Λ/S, Corollary X (preserved in `EXTERNAL_REVIEWS.md`); in-repo pointer `SOURCE_MAP.json` (`nonauthor_acceptance: true`, revision note naming 5360192822) | Corollary Λ (1.6); Proposition 4.4 (4.4) with its `A -> oo` step; Lemma 5.2 (5.4) |
| [CL-R] | `frontiers/c6_cluster_law_20260929/README.md`, `SOURCE_MAP.json` | 7560 · `e4b35f2b…` · `1166376f`; 12566 · `0584c380…` · `ef51c582` | Anthropic | — | object identity; acceptance pointer |
| [PALM] | `frontiers/c6_palm_route_20260929/PROOF.md` (Math-#145, merged `820d443`) | 53364 · `aa37f16040ab9e05bb2e4e3f1d678367497e8dc2cf43eef197a4d6592c2f129b` · `89eb8adf08fe7afc2cab9662d3a9875c05ae5cc5` | Anthropic (other session) | OpenAI 5356233690 (§4), 5358116559 (§§5–7, Theorem Q) | Theorem Q, `q = 3` and `q = 4`, for the uniform-integrability tails |
| this packet | `reviews/c6_residual_closure_20260930/EXTERNAL_REVIEWS.md` | see `SOURCE_FILES.json` | transcribed by Anthropic | mutable external evidence, labelled | the preserved 5360192822 |
| [TSL] | `frontiers/two_scale_cluster_geometry_20260929/TWO_SCALE_LAW.md` (Math-#166, merged `ab13a08f`) | 17139 · `e81d7fe09d25c3266eb8e62922756f54761d7f74d692fb35d9a8071fffd73769` · `a32fd5f7d941bbe1fe943df045b1e0fbec8d691c` | OpenAI | in-repo `REVIEW_RECORD.md` (6732 · `af1540308f37220e6592b700bf42181205b1d4588a040a5c151bf0a6f861e728` · `31896de23fc56822c184375d0dc2b1c7e27fcae4`, extended by Math-#172 at `fe2c3ff`) and `REVIEW_RECORD.json` (4226 · `958d2e1ae8ea5d034d0d87efce6cde9be57ebb9d7c0b671e69d3d6598a6675ca` · `a4b0fb99c24e2edf41973ea2a5e5176584602855`: native review 5360227991, reviewed commit `7c82252`, proof `TWO_SCALE_LAW.md`, body SHA256 `c63efc29…`): Claude 5360227991 ACCEPT of Theorem T, Theorem L, (L3), (V1) at the conditional scope; xAI bounded read 5901945424 reported in Math-#160 5902466075 | Theorem L (L1), (L2): the direct statement |

Identities are checked by `residual_check.py` (`IDENTITIES`, `NEGATIVES`); the quoted statements are checked as
substrings (`VERDICTS`). [SC] and [CL] are conditional on their own pinned inputs at those inputs' reviewed scopes
([SC] `SOURCES.json`: P, D5, C6, RM, RC, LM, CUB, RCL; [CL] `SOURCE_MAP.json`: LP, DL, C6, RM, RC, EDL, LM, RCL; [TSL]
`SOURCES.json`: SC, CUB, RM, C6, P, D5); this record inherits exactly those conditions and adds none.

## 3. The corollary: (Res) from the reviewed statements

Write `N_R` for the window count in the Euclidean ball of radius `R r` about `o` ([SC]'s `N_R`; [CL]'s `N^A` with
`A = R`), `N_out = N - N_R`, and `(n)_2 = n(n - 1)`. The quantity in (Res) is exactly

    M_R := E_{Q_r^W} #{ordered pairs of distinct window points not both within R r of o} = E[(N)_2] - E[(N_R)_2],   (D1)

since for every configuration `(N)_2 - (N_R)_2 = 2 N_R N_out + (N_out)_2 >= 2 N_R N_out >= 0` (exact identity, checked
in `DEDUCTION`). So (Res) says `lim_R limsup_r r^-3 (E[(N)_2] - E[(N_R)_2]) = 0`, and the mixed count of Math-#160 §5 is
`M(R, s_0) <= E[N_R N_out] <= M_R / 2`.

**Route A ([SC], Math-#162).**
1. *Full second factorial moment.* [SC] (26): `E (N)_2 / r^3 -> 2 nu2 = 2 a_2`, a stated consequence of Theorem (3)
   with `q = 2` (§8, Slice C).
2. *Near second factorial moment.* [SC] (18): `r^-3 Q_W(N_R = j) -> a_j^R` for `j = 1, 2` and `r^-3 Q_W(N_R >= 3) -> 0`
   (§5, Slice B). Tail: `(N_R)_2 <= (N)_2`, and for integers `n > M >= 3`, `n(n-1) <= n(n-1)(n-2)/(M-1)` (exact, `DEDUCTION`),
   so `E[(N_R)_2; N_R > M] <= E[(N)_3]/(M-1) <= C_3 r^3/(M-1)` by [PALM] Theorem Q with `q = 3`. Hence
   `limsup_r | r^-3 E[(N_R)_2] - 2 a_2^R | <= C_3/(M-1)` for every `M`, i.e. `r^-3 E[(N_R)_2] -> 2 a_2^R` (the finite sum
   over `n <= M` converges by (18), its `n >= 3` terms to zero). This is the same tail argument [SC] §8 uses for (3).
3. *Exhaustion.* [SC] (20): `a_2^R -> a_2` as `R -> oo` (dominated convergence with the integrable majorant (19), §6,
   Slice B).

Therefore `limsup_r r^-3 M_R = 2 a_2 - 2 a_2^R` (a full limit, by 1 and 2), which tends to `0` as `R -> oo` by 3. That is
(Res). ∎

**Route B ([CL], Math-#159).** Corollary Λ (1.6): `r^-3 E[(N)_2] -> Λ_2 = 2 nu(2) = 2 nu_near(2)`; Proposition 4.4:
`r^-3 Q{N^A = n} -> nu_near^A(n)` for `n = 1, 2`, `r^-3 Q{N^A >= 3} -> 0`, and `nu_near^A(n) -> nu_near(n)` as `A -> oo`;
the tail of step 2 is the one [CL] §6.3 uses ([PALM] Theorem Q). The same three lines give (Res). Directly, without the
factorial-moment limit: Lemma 5.2 (5.4), `E[N^A 1{N_far^rho >= 1}] <= C(A, rho) r^(9/2)`, together with
`E[N^A (N_far^rho - 1)_+] <= (E (N^A)^2)^(1/2) (E N_far^4)^(1/4) Q{N_far^rho >= 2}^(1/4) <= C r^(3/2) r^(3/4) r^(5/4) = C r^(7/2)`
([PALM] Theorem Q for the second and fourth moments through Stirling's identity `n^4 = (n)_4 + 6(n)_3 + 7(n)_2 + (n)_1`,
[RC] Corollary D for `Q{N_far^rho >= 2} <= E (N_far^rho)_2 / 2 = O(r^5)`), gives `E[N^A N_far^rho] = O(r^(7/2)) = o(r^3)`
at fixed `(A, rho)`, which is the mixed count of Math-#160 §5 with `s_0 = rho` (the far region `D_rho` is measured from
`o`; a point at distance `>= s_0` from both pins lies in `D_{s_0/2}` for `r < s_0`). Exponent ledgers checked exactly.

**Route C (pair-count corollary; Math-#160 comment 5901994240, checked in 5902616692).** With `A`, `B`, `C` the window
counts in `|X| <= R r`, `R r < |X| < rho`, `|X| >= rho` (from `o`; `N = A + B + C`), pathwise

    0 <= (N)_2 - (A)_2 <= N^2 [ 1{B > 0} + 1{A > 0, C > 0} + 1{C >= 2} ],                                       (D2)

exact: the right side vanishes only when `B = 0` and either `C = 0` or `A = 0, C <= 1`, and then the left side
`2A(B + C) + (B + C)(B + C - 1)` vanishes too (checked in `DEDUCTION`). Cauchy–Schwarz with `E N^4 <= C r^3` ([PALM]
Theorem Q through Stirling) and [CL] (5.1) (`E B <= C r^3 (R^-2 + rho^2)`, [DL] Theorem I_d, constant uniform in `R >= 4`,
`rho <= s_0`), the left inequality of [CL] (5.4) (`Q{A >= 1, C >= 1} <= C(A, rho) r^(9/2)`) and [RC] Corollary D
(`Q{C >= 2} <= E (C)_2 / 2 = O_rho(r^5)`) give

    r^-3 E[(N)_2 - (A)_2] <= C (R^-2 + rho^2)^(1/2) + C_(R,rho) r^(3/4) + C_rho r ;

`r -> 0` first, then `rho -> 0`, then `R -> oo` gives (Res). This route uses no count-law limit: only the shell bound,
the cross-term bound, the far second factorial moment and Theorem Q (exponent ledgers `3/2 + 9/4 - 3 = 3/4` and
`3/2 + 5/2 - 3 = 1`, checked exactly).

**Direct statement ([TSL], merged at `ab13a08f`).** Math-#166 Theorem L (L1): `r^-3 E_r[(N_r)_q - (N_in)_q] -> 0` for every
fixed `q >= 2` and every deterministic `delta_r -> 0` with `delta_r / r -> oo`, `N_in` the count within `delta_r` of `o`;
and (L2): `E_r[N_R N_far^rho] = o_(R,rho)(r^3)`, the mixed count itself. With `delta_r = R r` and `R -> oo` after `r -> 0`,
(L1) at `q = 2` is (Res); it is stronger (moving cutoff, all `q`) and is conditional on [SC]. It is bound in §2 and is a
required component in §5, so execution step 0 is satisfied by a reviewed merged source rather than by a read of this
record.

**What the corollary uses and nothing else.** Two reviewed limit statements about one law (the full and the near
second factorial moments), one reviewed exhaustion statement, and one reviewed moment bound for the tail. No
regression, no Kac–Rice step, no new estimate. Since v1.1 the direct statement [TSL] carries the flip and this record's
own node is supporting; a non-Claude read of this section remains welcome (the reconciler is source-exposed, §0) but
is not gating.

## 4. Scope, and what is not established

**Scope of the proposed `PROVED_REVIEWED`.** Every fixed `d >= 2`, fixed torus `L`, fixed frame, compact birth and
positive-gap marks (`k_- > 0`), the height window `I_r = (b - k r^3, b)`, the original endpoint weight `W_r` and the full
normalizer `Z_r`; existential constants; conditional on the pinned inputs of [SC] and [CL] at their reviewed scopes
(§2). Under this scope the register's chain for the witness-collision region reads: torus-wide `c r^3 <= E N(N-1) <= C r^3`
([PALM] + [EDL] (A4), Math-#160 §4); the leading `r^3` mass of `E N(N-1)` is carried, in the iterated limit, by pairs both
within `R r` of the midpoint ((Res), this record); the coefficient is `2 a_2` ([SC] (26) / [CL] (1.6)); the count law is
`nu(1) delta_1 + nu(2) delta_2` ([SC] Theorem (3) / [CL] Theorem N).

**Not established by this record.** No rate of convergence; no numerical value of `a_2`, `nu(1)`, `nu(2)`, `C_3` or of
the localization scale; no uniformity as `k -> 0`, in `L` or in `d`; no all-height statement (the window is
load-bearing in both sources); no statement about the elder selection of the extra points; no joint law of clusters
of distinct pin pairs; no configuration law beyond what [SC]/[CL] state (Math-#166 Theorem T supplies the configuration
form; not consumed); no `d_TV` statement (Math-#166 (V1); not consumed); the moving-cutoff form is [TSL] (L1) at its own
scope; no historical numerical certificate (RN annulus partition,
24-jet / OBL-H5-JETMOD) and no discharge of any historical predicate outside the analytic scope (Math-#160 §6). Neither
[SC] nor [CL] is re-reviewed here; their reviews stand at the scopes their records state.

## 5. Proposed register transitions (for a non-Claude lane)

| Node | Current (`358f256`) | Proposed |
|---|---|---|
| `math.rn-region.witness-collision.leading-mass-localization` | absent (Math-#160 proposes it `OPEN_ACTIVE`) | `PROVED_REVIEWED` at the §4 scope, with `fingerprint` unchanged from Math-#160's proposal, `scope`, `explicit_limits`, `review_disposition`, `review_basis`, and `required` edges to the component nodes below; created directly if Math-#160's step 1 has not run, moved if it has |
| `math.rn-region.witness-collision` | `OPEN_ACTIVE` (Math-#151 wording) | `PROVED_REVIEWED`, **conditional and deferred**: presupposes Math-#160's aggregate node `math.c6-witness-collision-factorial-moment` (count discharge) and this record's residual node (localization); executes only after both exist, with `required` edges to both. Under Math-#160's keep-open execution (§1a (iii) there), the residual's definition sits on the old node and this record moves the old node itself. If the executing lane holds that the node means something other than the count estimate and (Res), it must write that meaning down; no source defines one (Math-#160 §1a) |
| `SELECTOR_REGION.json`, `PROOF_INDEX.md`, catalog C6, `STATUS.md` C6 row | as at `358f256` | as Math-#160 §7 proposes, with the residual bullet closed: "leading-mass localization: resolved at existential scope by Math-#162 (26)/(18)/(20) and Math-#159 Corollary Λ / Proposition 4.4; direct statement Math-#166 Theorem L when merged; open: rate, constants" |

**Component nodes** (`kind: reading_rule_component`, `PROVED_REVIEWED`, `controlling: false`, `fingerprint` = SHA256 of the
source; one node per byte identity; none duplicates a source the live graph carries with a fingerprint):

| Node | Source | Role | Provider | Review basis |
|---|---|---|---|---|
| `math.c6r-component.spectral-closure-proof` | [SC] | proof: Theorem (3), (18), (20), (26) | OpenAI | A 5359968447, B 5359845136, C 5359879627 (in-repo `REVIEW_RECORD.md`) |
| `math.c6r-component.spectral-closure-review-record` | `frontiers/spectral_cluster_closure_20260929/REVIEW_RECORD.md` | review record | OpenAI-authored record of the Claude/Codex reviews | itself |
| `math.c6r-component.cluster-law-proof` | [CL] | proof: Corollary Λ, Proposition 4.4, Lemma 5.2 | Anthropic (other session) | OpenAI 5360192822 |
| `math.c6r-component.cluster-law-acceptance` | this packet's `EXTERNAL_REVIEWS.md` | external review record (5360192822, transcribed; mutable, labelled) | OpenAI review, transcribed by Anthropic | itself |
| `math.c6r-component.cluster-law-source-map` | `frontiers/c6_cluster_law_20260929/SOURCE_MAP.json` | in-repo acceptance pointer and consumed-input map | Anthropic | records 5360192822 |
| `math.c6-component.palm-proof` | [PALM] | proof: Theorem Q (`q = 3, 4`) | Anthropic (other session) | OpenAI 5358116559; **defined by Math-#160** (same id, source, fingerprint); created here only if absent |
| `math.c6r-component.two-scale-law-proof` | [TSL] | proof: Theorem L (L1), (L2), the direct statement | OpenAI | Claude 5360227991 (in-repo `REVIEW_RECORD.md`); xAI bounded read 5901945424 as reported |
| `math.c6r-component.two-scale-review-record` | `frontiers/two_scale_cluster_geometry_20260929/REVIEW_RECORD.md` (Math-#172 bytes) | review record | OpenAI-authored record of the Claude reviews | itself |
| `math.c6r-component.two-scale-review-binding` | `frontiers/two_scale_cluster_geometry_20260929/REVIEW_RECORD.json` | machine-readable review binding: native id 5360227991, reviewed commit `7c82252`, proof path and blob `a32fd5f7`, body SHA256 `c63efc29…` | OpenAI-authored record (Math-#172) | itself |
| `math.c6r-component.residual-closure-record` | this packet's `RECONCILIATION.md` | reading-rule record: the §3 corollary and Route C | Anthropic (this session; source-exposed) | `AUTHOR_SIDE_CANDIDATE` (the reconciler's own text; a non-Claude read is welcome); **supporting only** since v1.1, because [TSL] Theorem L is the direct statement |

Edges: from the residual node to each component, `required: true` (`requires_evidence`), except the record node, which
is supporting (`required: false`) since [TSL] is bound. From the old node (deferred transition): `required` edges to the
residual node and to Math-#160's aggregate node.

**Execution order** (`PROPOSED_TRANSITIONS.json` `execution_order`): (0) satisfied at `ab13a08f`: Math-#166 is on main and its
Theorem L is a required component node; a non-Claude read of §3 remains welcome but is not gating; (1) the component nodes and their edges; (2) the residual node
(created `PROVED_REVIEWED`, or moved from `OPEN_ACTIVE`); (3) only after Math-#160 step 3: the old node; (4) the
register rows. Nothing here edits `GRAPH.json`, `PROOF_INDEX.md`, `STATUS.md`, `SELECTOR_REGION.json` or the catalog
(`"executed": false`, checked).

**Reverse-impact.** Every component node carries the SHA256 of its source; a later change to [SC], [CL], [PALM], the
review record, the source map or the preserved acceptance reaches the residual node (and, once executed, the old
node) through `reverse_impact_between` (`GATE` replays it in both executions).

## 6. Checks

`residual_check.py` (stdlib only, run from the repository root):
- **IDENTITIES.** All twelve inventoried files exist as regular files, no symlink on their paths, stated SHA256 and blob.
- **VERDICTS.** The quoted statements are present as substrings: [SC] Theorem (3), (18), (20), (24), (26) and the
  Slice A/B/C lines of its review record with the core blob; [CL] Corollary Λ with `Λ_2 = 2 nu(2)`, Proposition 4.4's
  `A -> oo` sentence, Lemma 5.2 with `r^(9/2)`, the object header, the source map's `nonauthor_acceptance` and its note
  naming 5360192822; [PALM] object header and Theorem Q; [TSL] Theorem L with (L1) and (L2), its review record's
  5360227991 line at blob `a32fd5f7`, and the JSON binding's native id, proof path and body digest; the review id, verdict line and mutability label in `EXTERNAL_REVIEWS.md`.
- **LIVE.** `math.rn-region.witness-collision` is a live `OPEN_ACTIVE` region with its recorded fingerprint (or
  `PROVED_REVIEWED` after execution); the residual node is absent or `OPEN_ACTIVE` with Math-#160's fingerprint (or
  `PROVED_REVIEWED` after execution); the selector lists the region; no live fingerprinted node carries a component
  source of §5 other than `math.c6-component.palm-proof` if Math-#160 has been executed.
- **DEDUCTION.** Exact finite content of §3: the pair identity (D1) for all `0 <= N_R, N_out <= 12`; the Route C
  pathwise inequality (D2) for all `0 <= A, B, C <= 8` with its two exponent ledgers; the tail
  inequality `n(n-1)(M-1) <= n(n-1)(n-2)` for `n > M >= 3`; the Stirling identity for `n^4`; the exponent ledgers
  `3 + 3/2 = 9/2 > 3` and `3/2 + 3/4 + 5/4 = 7/2 > 3`; the truncation error of a finite distribution against
  `E(N)_3/(M-1)`; and an exact rational instance of the iterated limit `2 a_2 - 2 a_2^R -> 0`.
- **TRANSITIONS.** `declarative` true, `executed` false; the residual node `PROVED_REVIEWED`, non-controlling, with
  scope, explicit limits, review basis, Math-#160's fingerprint and a required edge to every component; every
  component node fingerprinted to the inventory with role, provider and review basis, one per byte identity; the
  record node `AUTHOR_SIDE_CANDIDATE` and reached by a supporting edge only; every required premise of the residual node
  `PROVED_REVIEWED`; the old-node transition marked deferred with its two presuppositions; the palm node marked
  cross-record with Math-#160's id.
- **GATE.** In both executions (residual node created directly; residual node pre-existing `OPEN_ACTIVE` as
  Math-#160 proposes), the proposed graph passes `validate_graph_fail_closed`, `closure_report` gives `gate_ok` with no
  illegal controlling node, and `reverse_impact_between` names the residual node and the components as changed and
  impacted; the deferred old-node transition is not applied (its presupposition is absent live) and is reported.
- **NEGATIVES.** Delete, one-byte change, symlink and symlinked parent on a temporary copy of the inventory are rejected.

Ten mutants must fail: `allow-symlink`, `no-hash`, `stale-fingerprint`, `drop-required-edge`, `executed-flag`,
`controlling-true`, `tail-reversed`, `pair-identity-broken`, `route-c-broken`, `drop-review-needle`.

## 7. Relation to other lanes

- **Math-#160 (this session):** defines (Res) and proposes the residual node `OPEN_ACTIVE`; this record is its successor
  and composes with either execution of its §7. Math-#160 is not changed.
- **Math-#162 (OpenAI; merged `358f256`, integrated by OpenAI Sol):** Route A. Not re-reviewed; its review record is
  bound in-repo.
- **Math-#159 (Anthropic, other session; merged `98fdb54`, integrated by the OpenAI engineering lane):** Route B. Not
  re-reviewed; its acceptance is preserved as external evidence.
- **Math-#166 (OpenAI; merged at `ab13a08f`, integrated by OpenAI Sol / C25):** the direct statement, bound in v1.1; not
  re-reviewed.
- **Math-#167 (this session; merged at `fa1cf7b` by OpenAI Sol after review 5360524053):** disjoint (D2/D3/D4/D5-annulus/D6
  alignment); its execution is a separate non-Claude act.
- **Math-#172 (merged at `fe2c3ff`):** custody repair of the two-scale packet, binding its reviews to exact proof bytes;
  the review record and its JSON binding are bound here at those bytes (v1.2); the proof bytes did not change.
- **Math-#151 (merged `ec6db8c`):** kept the old node open under the wording quoted in §1; this record supplies the
  discharge of the only defined residual meaning.
