# C6 / witness collision — source-bound reconciliation

**Object:** C6-WITNESS-COLLISION-RECONCILIATION-20260929-v1.
**Reconciler:** Anthropic Claude, Claude Code session `session_017Mi3hxjaxV45x6zo6o1ee3`.
**Read at:** Math- `main` `8e61fc4c055b56e526b5b3488104945e8e0e29cc` (29 September 2026); every inventoried byte
re-verified identical at the record's base `7a1cb09` (the merges of Math-#155 and Math-#156 in between touch no
inventoried path); re-verified again at `5c484bf` (Math-#161 merged), at `aa28838` (Math-#158 merged) and at
`bb429d3` (Math-#157 and #165 merged); no inventoried path changed at any of them.
**Revision:** v1.1 applies the scope corrections and the residual wording of OpenAI nonauthor review 5359701805
(at `6a0e3b9`) and pickup 5900929519; v1.2 merges Math- main `5c484bf` and updates the §5/§9 status of the
candidates after Math-#161 merged; v1.3 answers Codex review 5359693191 (the [LP] evidence reuses the live node
`math.uniform-matrix-cap-lifetime`; the selector proposal resolves all six cells per region and is checked; the
catalog is bound by the `OBLIGATION` check and the workflow paths; the residual is defined at scale `r`). §§1 and
3, the §4 statement and the 22-file inventory are unchanged; v1.3 removes one proposed node in favour of a live one.
v1.4 merges main `aa28838`, records xAI 5901345590 (ACCEPT as inventory; HOLD on execution until Math-#151 lands) and
makes the execution order explicit in §7. v1.5 merges main `bb429d3` and records Math-#166 as the third candidate
for the §5 residual, the one whose statement matches the residual's definition. v1.6 records xAI 5901915195.
**Effect:** register reconciliation, **declarative only**. This record introduces **no new mathematical claim**. It binds
the merged C6 chain to exact bytes, quotes the open obligation as the register recorded it, states which reviewed
theorem discharges that obligation and at what scope, states precisely what is *not* discharged, and proposes the
register transitions in machine-readable form (`PROPOSED_TRANSITIONS.json`, `"executed": false`). Execution of any
STATUS, PROOF_INDEX, GRAPH or catalog change is a separate act for a **non-Claude lane**. `lemma_closed`, prizes and
premises are untouched. Scientific effect: NONE.

## 0. Exposure, stated first

Every lane shares one GitHub account; no organizational independence is claimed anywhere below.

| Object | Author | Nonauthor verdict(s) | This reconciler's relation |
|---|---|---|---|
| [C6L] `frontiers/c6_factorial_moment_20260929/PROOF.md` (Math-#140) | Anthropic Claude, **this session** | OpenAI 5355120953 (§§4–6), 5355457002 (Lemma R, §§2/7/8), 5355682335 (rebind to v1.3); xAI bounded read 5894209739 | **author** |
| [PALM] `frontiers/c6_palm_route_20260929/PROOF.md` (Math-#145) | Anthropic Claude, session `015wNj8L…` | OpenAI 5356233690 (§4), 5357899713 (AMEND R3a), 5358116559 (ACCEPT §§5–7, Theorem Q, Corollaries Θ, P at `06bc0d6`); Codex integration review 5358643154 | none |
| [DL] `frontiers/d5_dimension_lift_20260929/PROOF.md` (Math-#141) | Anthropic Claude, session `015wNj8L…` | OpenAI 5357858391 (P_d, C_d), 5357882570 (I_d, G_d), source-exposed; xAI identities 5894274124, 5894406926; xAI planar P2 continuum 5894512272 | none |
| [EDL] `frontiers/elder_dimension_lift_20260928/PROOF.md` | OpenAI | Anthropic `reviews/elder_dimension_lift_claude_20260928/` ((A4) ACCEPT) | **reviewer** of (A4) |
| [LP] `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md` | OpenAI | D1 reconciliation (Math-#126); register row D1 | reviewer C1 and D1 reconciler |
| [P_η] `frontiers/remote_collision_20260928/PROOF.md` | Anthropic Claude, **this session** | xAI `reviews/d5_remote_collision_grok_20260928/`, `reviews/d5_offpin_second_moment_20260928/` | **author** |
| [FOU] `frontiers/c6_fourier_cutoff_20260929/PROOF.md` (Math-#148) | OpenAI | Anthropic review 5356335148 (session `01NMeKE…`), recorded in `reviews/c6_fourier_completion_20260929/READING_NOTE.md` | none |
| [BND] `frontiers/c6_count_cap_boundary_20260929/PROOF.md` (Math-#146) | OpenAI | Anthropic review 5355817385 (**this session**) | reviewer and integrator |
| [SHP] `frontiers/c6_sharpened_20260929/PROOF.md` (Math-#142) | Anthropic Claude, **this session** | OpenAI 5355652934 (source-exposed: the route was OpenAI's) | **author** |
| [CLU] `frontiers/c6_rare_cluster_laws_20260929/PROOF.md` (Math-#153) | OpenAI | Anthropic 5358565704 (session `01NMeKE…`), xAI 5358623521 | none |

The three load-bearing proofs of the discharge, [C6L], [DL] and [PALM], are all Claude-authored (two sessions). Their
nonauthor verdicts are OpenAI's, and OpenAI states its own source exposure in each (it authored the planar first-moment
sources that [DL] lifts and that [C6L]/[PALM] consume). xAI's verdicts cover [DL]'s identities, the planar P2 continuum
and a bounded read of [C6L]. **An integrating lane that wants a second provider on the discharge itself should ask xAI
for a bounded read of [PALM] §§4–6 before executing §7.** That is the same caveat the D5 record carried for P2.

**Verdicts on this record.** OpenAI nonauthor scope review 5359701805 (at `6a0e3b9`, `RECONCILIATION.md` blob
`66bb7cfd`): ACCEPT of §§1 and 4, the identification and the count-bound discharge of the original obligation, with
three scope corrections applied in v1.1 (§2 [P_η] row; §4 upper bounds only; §6 scope retention) and the §5 wording
"not supplied by the landed reviewed chain". That review explicitly does **not** accept the executable fold
(inventory, edges, selector transition, checker, hosted results); it defers that to a separate engineering review
after Math-#151 lands. No register transition occurs from it.

xAI bounded read 5901345590 (at `3e00f21`): **ACCEPT as inventory** (§1 quotes a count estimate; §3 byte-binds the
chain; `MONOTONE` is correct; the line-45 sentence is discharged at existential fixed-`d` compact-mark window scope)
and **HOLD on execution** for three reasons this record already states: `executed: false` and the dependence on
Math-#151; the residual node must exist before the old node moves (§7 ordering); and the xAI read of [PALM] §§4–6
asked for above is a separate slice, not that comment. The record may land declaratively; the
`OPEN_ACTIVE → PROVED_REVIEWED` step is a later non-Claude act.

xAI bounded discharge read 5901915195 (at `c641df1`): agrees that §1 quotes a count estimate and that [PALM]
Theorem Q with [EDL] (A4) discharges it at existential, fixed-`d ≥ 2`, compact-mark, window-`I_r` scope, with the
regional monotonicity an upper bound only; holds execution until Math-#151 is on main; requires the residual node
to exist before the old node moves (the §7 order); and states that it is not the second-provider read of [PALM]
§§4–6, which the xAI lane (Benjamin) is taking separately.

## 1. The obligation, as the register recorded it

Four places define the open item. They are quoted at the bytes of `8e61fc4`.

1. **`PROOF_INDEX.md`, line 45:**
   > D5 shrinking multiple-witness collision: fixed-separation machinery is `frontiers/remote_window_20260924/PROOF.md`
   > section 6, (15)–(16), at fixed `eta>0`. **NO COMPLETE PROOF YET: shrinking-separation factorial-moment/collision
   > estimate.**
2. **`frontiers/downstream_gate_20260925/GRAPH.json`, node `math.rn-region.witness-collision`:** layer D5, kind
   `region`, classification `OPEN_ACTIVE`, fingerprint **"eta->0 mutual witness separation"**, notes **"Fixed-eta
   factorial moments do not cover shrinking separation"**.
3. **`frontiers/remote_window_20260924/PROOF.md`** (D4, reviewed at main#76), after (15)–(16):
   > Witness tuples whose mutual separation tends to zero; (15) does not control that collision.
4. **`frontiers/remote_collision_20260928/PROOF.md`** ([P_η], xAI-reviewed), §1 and §8:
   > […] records that shrinking separation is uncontrolled. This is the open "witness-collision" region of the D5 graph
   > (`math.rn-region.witness-collision`, "eta->0 mutual witness separation"). […]
   > Not established: **A torus-wide second factorial moment, or `math.rn-region.witness-collision` in its full
   > torus-wide sense.** Pairs with either witness in the local, collar or intermediate regions are not estimated here.

The D5 reconciliation (`reviews/d5_reconciliation_20260929/RECONCILIATION.md` §5, landed via Math-#138) restated it:
> **D5-open (catalog C6): shrinking multiple-witness collision.** Target. A torus-wide second factorial moment
> `E_{Q_r^W} N(N−1)` for the window count, with pairs where at least one witness is within fixed `η` of a pin.
> […] **No upper bound.** The optimal order is open.

And catalog C6 (`reviews/candidates_pending_20260928/CANDIDATES.md`, read at blob `e3fc1a31`, unchanged through
`5c484bf`; bound by the `OBLIGATION` check and the workflow paths) asked for "a valid full-window factorial upper
bound with the pin-neighborhood collisions included".

**Reading.** In all five places the obligation is a **count estimate**: a factorial-moment (collision) bound for the
window count that covers (a) witness pairs at shrinking *mutual* separation, including coincidence limits, and (b)
witness pairs with a member at shrinking distance from a pin. The fixed-`η` results ([D4] (15)–(16); [P_η]) cover (a)
only when both witnesses stay in a fixed remote region; nothing covered (b). No source defines the node as a regional
decomposition of the leading-order mass, as a Palm or conditional statement, or as anything other than the count
estimate above. §5 returns to that point.

## 2. What is now proved and reviewed

All statements are for the exact pinned model of [LP] (period `T`, written `L` in [LP]/[PALM]): fixed `d ≥ 2`, fixed
torus, compact marks `b ∈ B`, `k ∈ K` with `k_− > 0`, all frames and indices, the original weight `W_r` and full
normalizer `Z_r`, the window `I_r = (b − k r³, b)`, and `N` = number of critical points of `f` in `X ∖ {M, S}` with
height in `I_r`. Constants are existential.

| Tag | Statement | Scope | Verdict on file |
|---|---|---|---|
| [C6L] Theorem C6-L | `E_{Q_r^W} N(N−1) ≤ C r³ log²(1/r)`; `(N)_q ≤ C_q r³ log^{2(q−1)}(1/r)` | `d = 2`; D5 reading rule | OpenAI complete acceptance (5355120953 + 5355457002, rebound 5355682335) |
| [SHP] S₂ / S_d | `r³[L/log L]²` planar; `r³[L/log L]^{d(q−1)}` given G_d | fixed `d` | OpenAI 5355652934 (source-exposed) |
| [FOU] Theorem F, W | count-tail `C e^{−c x^{2/d}}`; `E N(N−1) ≤ C r³ log(1/r)` planar; `(N)_p ≤ C_p r³ [log(1/r)]^{d(p−1)/2}` given G_d | fixed `d` | Anthropic 5356335148 |
| [BND] Theorems A, B, Prop. C | cap tail + first moment alone cannot give `O(r³)`; the missing input is a size-biased cap moment | abstract | Anthropic 5355817385 |
| [DL] Theorems P_d, C_d, I_d, **G_d** | first moments in every fixed `d`; `E_{Q_r^W} N ≤ C r³` | fixed `d` | OpenAI 5357858391, 5357882570 (source-exposed); xAI identities |
| [PALM] **Theorem Q** | `E_{Q_r^W}[(N)_q] ≤ C_q r³` for every fixed integer `q ≥ 2` | every fixed `d ≥ 2` | OpenAI 5358116559 (source-exposed) |
| [PALM] **Corollary Θ** | `c r³ ≤ E_{Q_r^W} N(N−1) ≤ C r³` and `c r³ ≤ Q_r^W{N ≥ 2} ≤ C r³` | every fixed `d ≥ 2` | same, with [EDL] (A4) |
| [EDL] (A4) | `Q_r^W(N_r ≥ 2) ≥ c r³`, `E[N_r(N_r−1)] ≥ c r³`, from two extra index-`(d−1)` points within `C_d r` of the midpoint | every fixed `d` | Anthropic `reviews/elder_dimension_lift_claude_20260928/` |
| [P_η] Corollary D | `E N_η(N_η−1) ≤ C_η r⁵`, both witnesses at distance `≥ η` from the pins, all mutual separations | fixed `η`, every fixed `d` (Theorem C / Corollary D constants depend on `d, L, ρ, η_0, B, K`; the planar / `G_d` condition of [P_η] concerns its Corollary F upper half only) | xAI |
| [CLU] | conditional consequences of (H1), (H2), (Hq): Poisson obstruction at scale `r³`, cluster-law compactness | abstract given the above | Anthropic + xAI |

[PALM] §1.4 records that at `d = 2` every regional input is the planar row it lifts, each with its own nonauthor
verdict, so the planar statement of Theorem Q depends on [PALM]'s own steps only; the every-`d` statement additionally
needs [DL]. [PALM] §2 pins [C6L] v1.3 and [DL] at the merged bytes, which are the bytes inventoried in §3 below.

## 3. Components, exact bytes and verdict rows

`reconciliation_check.py` binds every path below to its SHA256 and git blob, rejects symlinks anywhere on the path,
and checks the quoted verdict rows as exact substrings. The inventory is on `main` `8e61fc4`.

| Role | Path | SHA256 (prefix) | Blob (prefix) |
|---|---|---|---|
| **Discharge (required)** | | | |
| [PALM] proof | `frontiers/c6_palm_route_20260929/PROOF.md` | `aa37f160…` | `89eb8adf…` |
| [PALM] review record | `frontiers/c6_palm_route_20260929/README.md` | `56c0b94f…` | `1ebf8ede…` |
| [PALM] source map | `frontiers/c6_palm_route_20260929/SOURCE_MAP.json` | `c7cc195f…` | `b528fe10…` |
| [PALM] checker, results | `palm_exact_check.py`, `RESULTS.json` | `3bd19ec6…`, `7812de45…` | `6b0c73ba…`, `cd8003da…` |
| [C6L] proof v1.3 | `frontiers/c6_factorial_moment_20260929/PROOF.md` | `b1992756…` | `f5bd013b…` |
| [DL] proof | `frontiers/d5_dimension_lift_20260929/PROOF.md` | `6fb94b24…` | `9d82c707…` |
| [DL] crosswalk | `frontiers/d5_dimension_lift_20260929/CONTINUUM_CROSSWALK.md` | `bdb83c28…` | `45e4324f…` |
| [EDL] proof | `frontiers/elder_dimension_lift_20260928/PROOF.md` | `b529fe37…` | `7303bd79…` |
| [EDL] review | `reviews/elder_dimension_lift_claude_20260928/REVIEW.md` | `032bb4c7…` | `e2b9fcdc…` |
| [LP] parent | `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md` | `9350ad6e…` | `dfed3b8d…` |
| Planar reading rule | `reviews/d5_reconciliation_20260929/RECONCILIATION.md`, `PROPOSED_TRANSITIONS.json` | `14342b7e…`, `02f91870…` | `4062d76b…`, `d928969e…` |
| **Supporting (not required by the discharge)** | | | |
| [FOU] proof, reading note | `frontiers/c6_fourier_cutoff_20260929/PROOF.md`, `reviews/c6_fourier_completion_20260929/READING_NOTE.md` | `c1692379…`, `62f84b68…` | `1d9177a2…`, `682d7045…` |
| [BND] proof | `frontiers/c6_count_cap_boundary_20260929/PROOF.md` | `264a5e76…` | `3d4c28a4…` |
| [SHP] proof | `frontiers/c6_sharpened_20260929/PROOF.md` | `9f45274a…` | `70ba1972…` |
| [CLU] proof | `frontiers/c6_rare_cluster_laws_20260929/PROOF.md` | `c52a3cf1…` | `2ab625ce…` |
| [P_η] proof, xAI reviews | `frontiers/remote_collision_20260928/PROOF.md`, `reviews/d5_remote_collision_grok_20260928/REVIEW.md`, `reviews/d5_offpin_second_moment_20260928/REVIEW.md` | `b9b8b58f…`, `f8289546…`, `43beb4ef…` | `7b48a88e…`, `c18560f8…`, `62697c47…` |
| [D4] proof | `frontiers/remote_window_20260924/PROOF.md` | `a332bae9…` | `b383bfcc…` |

Full hashes are in `reconciliation_check.py` (`INVENTORY`). The GitHub review ids are bound where an on-disk record
carries them: [PALM] `README.md` (review table), [C6L] header (5355120953, 5355457002), [DL] `README.md` and
`CONTINUUM_CROSSWALK.md` (5357858391, 5357882570, 5894512272), [FOU] reading note (5356335148), [EDL] review ((A4)
row). Reviews 5355817385, 5358565704, 5358623521 and 5355652934 exist on GitHub only; the record cites them and
`SOURCE_FILES.json` does not claim otherwise.

## 4. Discharge

**Claim reconciled.** The obligation of §1 — a shrinking-separation factorial-moment/collision estimate for the window
count, torus-wide, pin neighbourhoods included — is discharged by [PALM] Theorem Q, with the matching lower bound
[EDL] (A4), at the following scope:

- **Statement.** `E_{Q_r^W}[(N)_q] ≤ C_q r³` for every fixed integer `q ≥ 2`, and `c r³ ≤ E_{Q_r^W} N(N−1) ≤ C r³`.
  The optimal order asked for by catalog C6 is `r³`.
- **Scope.** Every fixed `d ≥ 2`; fixed torus; compact marks with `k_− > 0`; all frames and indices; the height window
  `I_r`; the original `W_r` and full `Z_r`; existential constants. At `d = 2`, conditional on [PALM]'s own steps
  (§§3–7) only; for `d ≥ 3`, additionally on [DL] at its OpenAI acceptance.
- **Why it is the recorded obligation and not a different quantity.**
  1. `N` counts *every* window critical point other than the pins. `(N)_2` counts every ordered pair of distinct
     ones, at every mutual separation including the coincidence limit, and at every distance from the pins. [PALM]
     proves this through the pathwise cap `N(N−1) ≤ N Ψ` and the marked Kac–Rice formula over the same tiling as
     [DL] §7 (pin balls, collar, shells, remote region); the pin-neighbourhood pairs are the R1 regime of its §6.
  2. For any Borel region `A` of the torus, the count `N_A` of window critical points in `A` satisfies `N_A ≤ N`
     pathwise, hence `(N_A)_q ≤ (N)_q` for every `q`. Every *regional* factorial-moment bound of the recorded type is
     therefore implied by the torus-wide one. `reconciliation_check.py` records this reading exactly on integer count
     vectors (`MONOTONE`). There is no sense of "factorial-moment/collision estimate" under which a torus-wide bound
     leaves a regional bound of the same quantity open. This monotonicity supplies **upper bounds only**: the lower
     bound `c r³` is global, realised on the [EDL] (A4) event by pairs within `C_d r` of the midpoint, and is not
     claimed for an arbitrary subregion or shrinking selector. OpenAI review 5359701805 states the sharper pathwise
     form, adopted here with credit: for any Borel selector `0 ≤ χ_r ≤ 1` on ordered `q`-tuples of distinct window
     points (mutual-separation cutoffs tending to zero with `r`, positions relative to the pins and mixed
     local/remote subsets included), `T_χ := Σ χ_r ≤ (N)_q` pathwise, hence `E T_χ ≤ C_q r³` uniformly in the
     selector, with no separate regional constant. It gives no matching lower bound for a selected subregion, no
     pointwise Kac–Rice density bound, no leading coefficient and no `o(r³)` for mixed pairs; those are §5's
     residual.
  3. The lower bound is the one the D5 record already carried (`E N(N−1) ≥ 2 P(N ≥ 2) ≥ 2c r³`), now from [EDL] (A4)
     in every fixed `d`; the upper bound matches it in order. The pair `(A4, Theorem Q)` is exactly "the eventual
     disposition of C2" that catalog C6 said the answer must be compatible with.
- **Consistency across the chain.** [BND] shows that a cap tail plus the first moment cannot give `O(r³)`; [PALM]
  uses more (the size-biased cap moment under the witness-conditioned regression, its Lemma M′ and Lemma 5.1), which is
  precisely the input [BND] Proposition C names. [FOU]'s `r³ log(1/r)` and [SHP]'s `r³[L/log L]²` are upper bounds
  superseded in order by Theorem Q and remain correct. [P_η]'s `O(r⁵)` for both-remote pairs is compatible with a
  total of order `r³` whose lower bound (A4) is realised by pairs within `C_d r` of the midpoint.

## 5. What is not discharged, and the one residual worth naming

- **Numerical constants** (`C_q`, `c`, `r_*`): open, as in every source. Catalog C8.
- **All-height pairs:** [PALM] counts the window `I_r` only. The all-height statement is not part of the obligation
  (which is the window count) and is not claimed.
- **Positional and cluster laws:** [CLU] gives conditional consequences (a Poisson obstruction at scale `r³`,
  compactness of the conditional and size-biased laws) but, as it says, does not identify a unique limiting cluster
  law. Not part of the obligation.
- **Uniformity** in `T` (`L`), in `d`, as `k ↓ 0` or as marks grow: not claimed anywhere.
- **Elder selection:** separate (D1; `frontiers/elder_lower_all_d_20260929/` for the every-`d` lower bound).
- **Historical numerical certificates** (RN annulus partition, 24-jet / OBL-H5-JETMOD): not discharged and not
  claimed; see §6 for what the analytic route does to their *blocking role*.
- **The residual that the phrase "regional shrinking-witness mechanism" could legitimately mean.** Math-#151's draft
  catalog and proof-index text keep `math.rn-region.witness-collision` open on the ground that "the global `Θ(r³)`
  result is not a proof of that node". §1 shows the node was never defined as anything but the count estimate. If the
  integrating lanes nevertheless want the register to keep a *regional* question, it should be a new node with a
  definition, not the old node under a new meaning. The one genuinely open regional statement is the
  **localization of the leading-order mass at scale `r`**, defined (with `o` the midpoint) as
  `lim_{R→∞} limsup_{r→0} r⁻³ E_{Q_r^W} #{ordered pairs (X, X′) of distinct window points : not both |X − o| ≤ R r
  and |X′ − o| ≤ R r} = 0`. What the landed chain gives: (A4) shows pairs within `C_d r` of `o` carry `≥ c r³`, so
  the scale-`r` mass is of order `r³`, and local–local pairs between `C_d r` and `R r` belong to it, not to the
  residual; [P_η] shows pairs with both witnesses at distance `≥ s_0` from the pins carry `O(r⁵)`; [PALM] §6 R3, the
  marked shell bound with `q = 2` whose dyadic sum is `C r³(A_0⁻² + s_0²)`, shows that every pair with a witness in
  the shells `R r ≤ |X − o| ≤ s_0` carries at most `C r³(R⁻² + s_0²)`. What it does not give: an `o(r³)` bound for the
  **mixed pairs**, one witness within `R r` of `o` and the other at distance `≥ s_0`, where [PALM] §6 R4 gives `C r³`
  only. By the three facts above the residual is equivalent to `lim_{s_0→0} lim_{R→∞} limsup_{r→0} r⁻³ M(R, s_0) = 0`
  for that mixed count `M(R, s_0)`, and this bound is **not supplied by the landed reviewed chain**. This is a
  further theorem, not a gap in Theorem Q. Two author-side
  candidates for it exist and are recorded here as **candidates only**: Math-#161 (OpenAI, head `e7f8929`, merged
  to main at `5c484bf`; planar; its Lemma M gives joint probability `o(r³)` for the local and fixed-remote nonempty
  events, and its §§6–7 one/two law is conditional on Math-#158 Theorems C/G/F) and Math-#159 (Anthropic Claude,
  session `015wNj8L…`, v1.1 head `7188bfa`, every fixed `d`; its Lemma 5.2 claims a near–far cross term
  `O(r^{9/2})`). Status at `5c484bf`: Math-#161 carries an Anthropic analytic ACCEPT (5359733142, by the session
  that authored its consumed [PALM] and [DL], so source-exposed) and a Codex engineering ACCEPT (5359797442); the
  four review slices of Math-#158 carry verdicts (A xAI 5359488967; B Codex 5359738045; C Anthropic, this session,
  5359814083; D Codex 5359601495), and Math-#158 merged at `aa28838`; Math-#159 is unreviewed. Neither candidate
  is a premise of this record, neither is inventoried, and neither is consumed by any proposed node or edge. The
  residual stays `OPEN_ACTIVE` for every fixed `d`: the Math-#161 chain is planar and source-exposed, so an executing
  lane could at most record a planar sub-status from it, after its own fold; this record proposes none. A third
  candidate, Math-#166 (OpenAI, `frontiers/two_scale_cluster_geometry_20260929/TWO_SCALE_LAW.md`, blob `a32fd5f7`,
  math head `7c82252`), states the residual as defined here: `r⁻³ E[(N)_q − (N_in)_q] → 0` for every fixed `q ≥ 2`
  and any `δ_r → 0` with `δ_r / r → ∞`, retaining counted mass (its near/remote product is `o(r³)`), conditional on
  Math-#162; at `bb429d3` its Slices B and C carry Anthropic verdicts (5360178611, 5360216551, session `01NMeKE…`) and
  Slice A, the two-scale law itself, is under review. It is unmerged, not a premise, not inventoried, not consumed.
  When #162 and #166 are on main with their reviews, an additive successor record can bind the residual's closure
  in every fixed `d`; this record does not. `PROPOSED_TRANSITIONS.json` proposes the residual as an explicitly
  scoped `OPEN_ACTIVE` node, `math.rn-region.witness-collision.leading-mass-localization`, required by nothing, so that
  the question is recorded precisely and blocks nothing.

## 6. Historical predicates and the shrinking regions

The graph already contains the pattern for this situation: `regional.fixed-annulus.high-jet-route`
(`SUPERSEDED_NONBLOCKING`, kind `regional_supersession`) records that, for the reviewed fixed-annulus scope, the
analytic route bypasses `hist.CH-LIFT`, `hist.Piece-2-annulus` and `hist.OBL-H5-JETMOD`, while those predicates stay
`OPEN`/`ABSENT` in their original replay scopes. `SELECTOR_REGION.json` still lists `CH-LIFT` and `Piece-2-annulus` as
`OPEN_ACTIVE` for `pin-collision` and `intermediate-r-to-rho`, and `Piece-2-annulus` as `OPEN_ACTIVE` for
`witness-collision`, with the notes "scaled charts reopen CH-LIFT" and "active mathematical blocker outside
fixed-remote".

With the reviewed D5 chain (planar via `reviews/d5_reconciliation_20260929/`, every fixed `d` via [DL]) and Theorem Q,
the pin-collision, intermediate and witness-collision regions are covered by analytic proofs that use no shrinking
chart lift, no annulus piece and no 24-jet enclosure. This record therefore proposes a second supersession node,
`regional.shrinking-regions.analytic-route`, with the same three `regional_bypass_only` edges and the same discipline:
the historical predicates are **not** discharged, their classifications are **not** changed, and the bypass is scoped
to the reviewed regions and scopes only. The `SELECTOR_REGION.json` cells of those three regions are all resolved
under that node, so that `hard_gate.py::selector_region_report` shows no open cell for them: `CH-LIFT`,
`Piece-2-annulus`, `OBL-H5-JETMOD` and `H5-REMOTE-THRESHOLD` become `BYPASSED_BY_ANALYTIC_ROUTE`; `ALLCELL-FDZ-Q4`
becomes `NOT_REQUIRED` and `ENV-RESCOV` `REDERIVED_QUALITATIVELY`, the values the `fixed-remote` row already carries
for the same reason (the analytic route uses the positive Fourier spectrum and the joint floors of [PALM] Lemma 6.1 /
Lemma E_d, not the historical cell carrier or the historical covariance predicate). The three region ids then move
from `open_region_ids` to `covered_region_ids`; `mesoscopic-scaled-annulus` stays open. The `SELECTOR` check applies
the proposal to the live table and verifies exactly this. The file edit is for the executing lane; if it prefers the
node-only precedent of `regional.fixed-annulus.high-jet-route` (cells untouched), the lists stay unchanged and §7's
selector row does not apply.

**Scope retained by the bypass.** The bypass inherits every restriction of §2: the original weight `W_r` and the full
normalizer `Z_r`, compact marks with `k_− > 0`, fixed `d` and fixed torus, and the height window `I_r` wherever the
source is window-only. It grants no all-height collision bound, no numerical certificate (RN annulus partition,
24-jet / OBL-H5-JETMOD) and no discharge of any historical predicate outside that analytic scope (OpenAI 5359701805,
item 3).

## 7. Proposed register transitions (for a non-Claude lane)

| Surface | Current (`8e61fc4`) | Proposed |
|---|---|---|
| main `STATUS.md` C6 row | "C6 — Fourier count tail and planar factorial upper bound", `E N(N−1) ≤ C r³ log(1/r)` in `d = 2` | **"C6 — torus-wide factorial moments (witness collision): `Θ(r³)`"** with the §4 statement and scope; keep the Fourier row's count-tail sentence as a component; independence caveat of §0 in the notes column |
| `PROOF_INDEX.md` line 45 | "NO COMPLETE PROOF YET: shrinking-separation factorial-moment/collision estimate" | move to the reviewed section, citing [PALM] with reviews 5356233690/5358116559, [EDL] (A4), [DL], and this record; keep a separate open bullet for the §5 residual and for numerical constants |
| `reviews/candidates_pending_20260928/CANDIDATES.md` C6 | Math-#151's draft keeps "regional mechanism open" | "Resolved at existential scope: optimal order `r³` in every fixed `d ≥ 2` (upper: Palm route; lower: (A4)). Open: numerical constants; leading-mass localization (§5); a unique limiting cluster law." |
| `GRAPH.json` `math.rn-region.witness-collision` | `OPEN_ACTIVE` (also in Math-#151) | `PROVED_REVIEWED` at the §4 scope, realized by the aggregate node `math.c6-witness-collision-factorial-moment`, one component node per required file with `fingerprint` = SHA256 and `source` = path, and `required: true` edges from the region node and the aggregate to each; the [LP] evidence is the live reconciled node `math.uniform-matrix-cap-lifetime` (same SHA256, four required reading-rule edges), not a new node; plus a required edge to the planar reading-rule node `math.d5-pin-neighborhood-first-moment` (created by Math-#151) |
| `GRAPH.json` new node | — | `math.rn-region.witness-collision.leading-mass-localization`, `OPEN_ACTIVE`, required by nothing, defined as the scale-`r` localization of §5 with the mixed local/remote count as its open piece, with the §5 candidate note (Math-#161, Math-#159: not premises) |
| `GRAPH.json` new node | — | `regional.shrinking-regions.analytic-route`, `SUPERSEDED_NONBLOCKING`, non-required `regional_bypass_only` edges to `hist.CH-LIFT`, `hist.Piece-2-annulus`, `hist.OBL-H5-JETMOD` (§6) |
| `SELECTOR_REGION.json` | `Piece-2-annulus` / `CH-LIFT` `OPEN_ACTIVE`, `ENV-RESCOV` / `ALLCELL-FDZ-Q4` `OPEN_HISTORICAL` for the shrinking regions | all six cells resolved for `pin-collision`, `intermediate-r-to-rho`, `witness-collision` (§6: four `BYPASSED_BY_ANALYTIC_ROUTE`, `ALLCELL-FDZ-Q4` `NOT_REQUIRED`, `ENV-RESCOV` `REDERIVED_QUALITATIVELY`); the three region ids move to `covered_region_ids`; checked by `SELECTOR` |

**Ordering.** These transitions presuppose Math-#151's execution of the planar D5 fold (its 14 nodes and 30 edges);
the required edge to `math.d5-pin-neighborhood-first-moment` refers to that node. They can be executed in the same
lane, after it, or folded into #151's restack if that lane prefers; either way the executing lane, not this record,
decides. Within the execution the order is fixed (xAI 5901345590): first create the residual node
`math.rn-region.witness-collision.leading-mass-localization` (`OPEN_ACTIVE`) and the supersession node, then the
component nodes and edges, and only then move `math.rn-region.witness-collision` to `PROVED_REVIEWED`, so that the
register never loses the localization question under a renamed meaning; the xAI bounded read of [PALM] §§4–6 asked
for in §0 precedes that last step. Nothing here edits `GRAPH.json`, `PROOF_INDEX.md`, `STATUS.md` or the catalog (`"executed": false`, checked).

**Reverse-impact.** Every proposed component node carries the SHA256 of its source, so a later byte change to any of
them invalidates the fold through the existing reader; `coverage_source` metadata is not used.

## 8. Checks

`reconciliation_check.py` (stdlib only, run from the repository root):
- **IDENTITIES.** All 22 inventoried files exist as regular files, with no symlink anywhere on their paths, and with
  the stated SHA256 and git blob.
- **VERDICTS.** The exact verdict rows and statements quoted in §§1–2 are present as substrings.
- **OBLIGATION.** The live graph still carries `math.rn-region.witness-collision` as a `region` node, either
  `OPEN_ACTIVE` with the recorded fingerprint or already `PROVED_REVIEWED`; `SELECTOR_REGION.json` lists the region;
  `PROOF_INDEX.md` carries either the line-45 obligation sentence or a reference to this record;
  `reviews/candidates_pending_20260928/CANDIDATES.md` carries the C6 heading and the quoted open-task sentence, or a
  reference to this record.
- **NEGATIVES.** Real filesystem faults on a temporary copy of the inventory: delete [PALM]'s proof, change one byte
  of it (all quoted statements kept), replace it by a symlink to identical bytes, replace its directory by a symlink.
  Each is rejected.
- **TRANSITIONS.** `PROPOSED_TRANSITIONS.json` names only inventoried files or known node ids; every required file is
  a proposed node with matching fingerprint and source, reached by a required edge from each consuming node; the
  supporting files are reached by non-required edges; the residual node is `OPEN_ACTIVE` with no required edges; the
  supersession node has exactly the three `regional_bypass_only` edges and no historical predicate changes class; the
  cross-record node is one the D5 proposal defines; a source already carried by a live fingerprinted node ([LP],
  `math.uniform-matrix-cap-lifetime`) is referenced through that node, with equal SHA256 and its four required
  reading-rule edges present, and no proposed node duplicates a live source; every proposed node passes the hard
  gate's shape rules; `declarative` is true and `executed` is false.
- **SELECTOR.** The selector proposal names every selector of the live table for its three regions, assigns each a
  value the hard gate classifies as covered or bypassed, and, applied to the live table, moves exactly those three
  region ids from `open_region_ids` to `covered_region_ids`.
- **MONOTONE.** Exact enumeration: `(n_A)_q ≤ (n)_q` for every sub-count and `q ≤ 4`; `2·1{n≥2} ≤ n(n−1) ≤ nΨ`;
  the `Θ(r³)` bracket needs both the upper and the lower row.
- **OPEN_RESIDUAL.** §5's open items are recorded (numerical constants; the residual node with its scale-`r`
  definition; the mixed-pair bound
  "not supplied by the landed reviewed chain", with the candidates named as candidates only) and the residual node
  is proposed open.

Ten mutants must fail: `allow-symlink`, `no-hash`, `drop-edge`, `stale-fingerprint`, `executed-flag`,
`close-residual`, `drop-lower-bound`, `regional-strict`, `clone-live-node`, `open-cell-left`.

## 9. Relation to other lanes

- **Math-#151 (Codex; head `64a170f`; xAI wording hold lifted at 5900436844):** executes the planar D5 fold and
  keeps witness-collision open. This record does not conflict with its graph edits; it supersedes only its *catalog and proof-index wording* about C6, and only if the
  integrating lane accepts §§1 and 4. If that lane prefers to keep the old node open, §5 asks that the reason be
  written as the residual node's definition. One register point for that lane: the live graph already carries
  `math.rn-fixed-remote-window` (fingerprint = the remote_window bytes, classification `AUTHOR_SIDE_CANDIDATE` despite
  the main#76 review), and the D5 proposal creates `math.d5-component.remote-window-proof` for the same bytes; this
  record references the live node (supporting edges only) and leaves the collapse of the pair, and the classification
  repair, to the executing lane.
- **Math-#155 (OpenAI, C7):** unrelated to the count; not consumed.
- **Math-#161 (OpenAI, `e7f8929`, merged at `5c484bf`) and Math-#159 (Anthropic Claude, other session, `7188bfa`):**
  author-side candidates for the §5 residual; not premises, not inventoried, not consumed (§5, with their review
  status at `5c484bf`). Their appearance changes none of this record's status rows, nodes or edges; a planar
  sub-status of the residual would be a further transition by an executing lane, after its own fold.
- **Math-#166 (OpenAI, two-scale cluster geometry, math head `7c82252`, open):** the consumer whose `TWO_SCALE_LAW.md`
  states the §5 residual exactly, conditional on Math-#162; B and C accepted (other Claude session), A under review;
  not consumed here; the residual closes by a successor record after both land.
- **Math-#158 (OpenAI, planar cubic cluster law, `bfcc67dc`, merged at `aa28838`):** premise of Math-#161 §§6–7; this session
  reviewed its Slice C (5359814083); not consumed here.
- **main#207:** the pickup for this record is comment 5900687550. The register execution stays with a non-Claude lane.
