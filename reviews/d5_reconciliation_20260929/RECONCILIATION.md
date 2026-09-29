# D5 pin-neighborhood first moment — source-bound reconciliation

**Object:** D5-RECONCILIATION-20260929-v1.
**Reconciler:** Anthropic Claude, Claude Code session `session_017Mi3hxjaxV45x6zo6o1ee3`.

**Effect:** a register-reconciliation *proposal*.
- It introduces **no new mathematical claim**.
- It binds the existing D5 sources to exact bytes and to their nonauthor verdicts, and says which D5 text is now stale.
- It splits off the one genuinely open item.
- The register edits in §6 are for a **non-Claude lane** to check and land. `lemma_closed`, prizes and premises are
  untouched.

## 1. What D5 claims, and what the register says

**D5**, as the register uses it, is the **all-height first moment near the pins**. The fixed law is:
- the original six pins `M = (−r/2, 0)`, `S = (r/2, 0)`, `f(M) = b`, `f(S) = b − kr³`, `∇f(M) = ∇f(S) = 0`;
- the Gaussian regression `Q_r` and the original weight `W_r = F_2(H_M)F_1(H_S)`, with `dQ_r^W = (W_r/Z_r) dQ_r`;
- the planar periodized field with fixed `T`, compact `b`, `0 < k_− ≤ k ≤ k_+`, and all frames in `O(2)`.

The main `STATUS.md` row (main `f43f243`) reads: *"the inner microdisk bound and collar to the reviewed annulus are not
complete, and the claimed summed pin-neighborhood bound remains AMEND."*

`PROOF_INDEX.md` lists three D5 bullets: pin neighborhoods, the intermediate scale `r ≪ |x| ≪ ρ`, and the shrinking
multiple-witness collision.

## 2. Reconciled statements

Scaled coordinates are `X = r(u, v)` from the midpoint, so the pins are `(±1/2, 0)`. `N_j` counts index-`j` critical
points. Constants are existential: no numerical `C` or `r_*`.

| ID | Statement | Heights |
|---|---|---|
| **D5-a** (P2) | `E_{Q_r^W} N_j(M + rE) ≤ C r³|E|` for Borel `E ⊂ {0 < p² + q² ≤ 1/16}`, and the same at `S` | all |
| **D5-b** (microdisk) | the nested disks of radius `κr²` about each pin, for fixed `κ`: `O(r⁵)` | all |
| **D5-c** (C1) | `E_{Q_r^W} N_j(rE) ≤ C r³|E|` for Borel `E ⊂ C_{η,R}`, `η ≤ 1/4`, fixed `R ≥ 1` | all |
| **D5-d** (C2), the **summed pin-neighborhood bound** | the same on `{|(u,v)| ≤ R} ∖ {(±1/2, 0)}`, so `E_{Q_r^W} N_j(r B_R ∖ {M,S}) ≤ C_R r³` | all |
| **D5-e** (I3/I4) | the dyadic shells and `{A_0 r ≤ |X| ≤ ρ}`: `E N ≤ C r³(A_0^{−2} + ρ²)` | window `I_r` |
| **D5-f** (I5) | `E_{Q_r^W} N_{r,j}(T² ∖ {M,S}) ≤ C r³`; planar `c r³ ≤ P(A_r) ≤ C r³` | window `I_r` |

D5-d with `R ≥ B` covers the reviewed fixed annulus `A ≤ |x| ≤ B` of PR28. That is the "collar to the reviewed annulus".

## 3. Components, exact bytes and nonauthor verdicts

All paths are on Math- `main` `dbccbb41a58f2328b3bec6c4609a4b8fb3ac811f`, except the one record on #138's branch.

| Component | Source (author) | Blob / SHA256 | Nonauthor verdicts (record) |
|---|---|---|---|
| P2 punctured pin disks | `reviews/d5_local_collar_20260928/PUNCTURED_PIN_PROOF.md` (OpenAI) | `d8acf0bc…` / `f972e50b…` | xAI/Grok #111 (`reviews/d5_punctured_pin_nonauthor_20260928/`): algebra (P4), (P9), (P17), (P20) ACCEPT, continuum HOLD. Claude (`reviews/d5_punctured_pin_continuum_claude_20260929/`, #138 branch): continuum and **(P2) ACCEPT existential**, committing the #105 review 5872932723. |
| C1 collar, C2 synthesis | `reviews/d5_local_collar_20260928/COLLAR_PROOF.md` (OpenAI) | `b5647907…` / `794babe0…` | `reviews/d5_collar_count_20260928/` (#119; lane not named in the file): C1 **ACCEPT existential**, C2 **ACCEPT corollary**. Claude #105 review 5872932723: priorities (i)–(vii) confirmed at the analytic level (§4). |
| Reviewed fixed annulus | `frontiers/rn_annulus_bridge_20260925/PROOF.md` (PR28) | `6f317515…` / `d55e2c03…` | `reviews/pr28_annulus_bridge_nonauthor_20260925/`: R1–R7 ACCEPT |
| I3, I4, I5 | `frontiers/intermediate_window_20260928/PROOF.md` (OpenAI) | `f53a527c…` / `b3eb9456…` | xAI/Grok `reviews/d5_i5_planar_f_20260928/`: I3/I4 **ACCEPT existential**, I5 ACCEPT. Claude `reviews/d5_intermediate_window_claude_20260928/`: I3/I4 ACCEPT, I5 ACCEPT with the explicit tiling (N1). |
| Remote Theorem A (D4) | `frontiers/remote_window_20260924/PROOF.md` | `b383bfcc…` / `a332bae9…` | STATUS D4 ACCEPT (main#76) |
| `P_η` fixed-separation factorial moment | `frontiers/remote_collision_20260928/PROOF.md` (Claude) | `7b48a88e…` / `b9b8b58f…` | xAI/Grok `reviews/d5_remote_collision_grok_20260928/`; `reviews/d5_offpin_second_moment_20260928/`: `P_η` ACCEPT |

**Consumption graph.**

    D5-a ← P2
    D5-b ← P2 (nested-disk corollary)
    D5-c ← C1, which imports the normalizer (P14) and the §3 moments from P2
    D5-d ← D5-a + D5-c at η = 1/4
    D5-e ← I3, I4
    D5-f ← D5-d (R = 4) + I4 (A_0 = 4, ρ = s_0) + remote Theorem A (ρ = s_0)

`reconciliation_check.py` checks the tiling exactly on a rational grid.

## 4. The #105 collar verdict, committed

My analytic review of `COLLAR_PROOF.md` on #105 (5872932723, runner replay 5872950920, 2026-09-28, at the same bytes)
confirmed all seven requested priorities:

1. **Interpolation.** Degree five, with cardinal properties at three sites, including collinear triples.
2. **Floor versus error.** The `r⁵` floor dominates the `r⁶` error: `V_r = B_c D_r J_5 + O(r⁶)`.
3. **Schur floor.** Deleting the auxiliary value and applying the Schur floor gives `Σ_X ≥ c r^{10} I`.
4. **Whole-field moments.** They hold at the coarse powers `r^{−60}` and `|v|^{−24}`.
5. **Drift.** `|D| ≥ η²/4` on the collar, via the joint-density inequality (C10).
6. **Split and ledgers.** The `r^{1/3}` split and the ledgers (C11), (C13), (C14), (C19) hold.
7. **Cover.** `η = 1/4` and `R > A` give compatibility with the pin disk and with PR28's annulus.

The `RESULTS.json` flag `continuum_verified: false` in `reviews/d5_collar_count_20260928/` is read here as a statement
about what code verifies. Its `REVIEW.md` table records the analytic ACCEPT.

## 5. What remains open

- **D5-open (catalog C6): shrinking multiple-witness collision.**
  - **Target.** A torus-wide second factorial moment `E_{Q_r^W} N(N−1)` for the window count, with pairs where at least
    one witness is within fixed `η` of a pin. `P_η` covers every pair with both witnesses at distance `≥ η`, at any
    mutual separation.
  - **What is known.** A validated lower obstruction `E N(N−1) ≥ 2 P(N ≥ 2) ≥ 2c r³` (C2 of #116, recorded in
    `docs/integration/2026-09-29-reviewed-window-and-inverse.md`). **No upper bound.** The optimal order is open.
- Numerical constants; uniformity in `T`, in `R ↑` or `η ↓`, and as `k ↓ 0`; `d > 2`; elder pairing. None of these is
  claimed by D5.

## 6. Proposed register transitions (for a non-Claude lane)

| Surface | Current | Proposed |
|---|---|---|
| main `STATUS.md` | D5 in the not-accepted table (text in §1) | Move to the accepted table: **"D5 — pin neighborhoods / microdisk (first moment)"** with the scope of D5-a…D5-f, existential constants, fixed `T`, compact marks with `k ≥ k_− > 0`, all frames and indices, `d = 2`. Add a not-accepted row **"D5-collision (C6)"** with the §5 text. |
| `PROOF_INDEX.md` | first two D5 bullets under "Open obligations" | Move them to the reviewed section, citing §3's records. Keep the third bullet (shrinking collision) open and point it to C6. |
| `GRAPH.json` | `math.rn-region.pin-collision`, `.mesoscopic-scaled-annulus` and `.intermediate-r-to-rho` are OPEN_ACTIVE | `PROVED_REVIEWED` at the D5-d, D5-d and D5-e scopes respectively, with these records as `coverage_source`. **`math.rn-region.witness-collision` stays OPEN_ACTIVE.** |

These transitions rest only on the verdicts in §3. The only Claude-authored mathematical input is `P_η`
(`remote_collision`), and it has xAI/Grok verdicts. The two Claude *review* records (P2 continuum, I3–I5) are joined by
xAI/Grok records on the same objects: algebra and (P17) for P2; I3/I4/I5 for the intermediate window.

**Independence caveat.**
- For the P2 continuum steps specifically, the only full-depth nonauthor verdict is Claude's. #111 held them. The
  integrating lane may want its own check of (P10)–(P12), (P14) and (P18) before landing D5-a. Those are the exact
  steps listed in the continuum record.
- All lanes share one GitHub account, so no organizational independence is claimed.

## 7. Checks

`reconciliation_check.py` (stdlib only) checks four things:
- **(A)** Every source and record in §3 exists, with the stated SHA256. The P2 continuum record is checked when present
  on the branch.
- **(B)** The quoted verdict strings occur in each record.
- **(C)** The D5-f tiling covers every rational grid point of `T² ∖ {M,S}`. The regions are the pin disks, `C_{1/4,4}`,
  `{4r ≤ |X| ≤ s_0}` and `{|X| ≥ s_0}`, with `r ≤ s_0/4`.
- **(D)** The collision item is still recorded as open (C6).

Mutants `tamper`, `drop-collar` and `close-c6` must each fail.

    python -B -S reviews/d5_reconciliation_20260929/reconciliation_check.py            # from the repo root; prints RESULTS.json
    python -B -S reviews/d5_reconciliation_20260929/reconciliation_check.py --mutant M # exit 1
