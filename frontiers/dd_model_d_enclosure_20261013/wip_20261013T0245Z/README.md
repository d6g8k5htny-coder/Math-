# Recovery checkpoint (work in progress): note DD — a certified two-sided enclosure of the model number `D`

**Status: PROTOTYPE / UNVERIFIED.** Nothing in this directory is a certificate, a note or a reviewed result. It is the
still-local working material of one session, preserved under the owner's recovery request
(main#307 [6136156988](https://github.com/d6g8k5htny-coder/main/issues/307#issuecomment-6136156988),
[6136210973](https://github.com/d6g8k5htny-coder/main/issues/307#issuecomment-6136210973)) so that a session
interruption does not force re-derivation. Scientific effect NONE. Not for integration.

- Task / proof identifier: note DD (two-sided `D`), main#307 task #312, claim
  [6135715016](https://github.com/d6g8k5htny-coder/main/issues/307#issuecomment-6135715016), task definition
  [6134833037](https://github.com/d6g8k5htny-coder/main/issues/307#issuecomment-6134833037) (`dd/DD_TASK_DEFINITION_20261012.md`).
- Original author / session: Dylan Roy — delegated AI work; Anthropic Claude, `session_01NMeKEismAyeqgdB4sy2NJU`.
- Supersession: the exploration files `dv/vform1.py … vform4.py` and the earlier prototypes `dd/ddcub.py`, `dd/ddih.py`,
  `dd/test_box.py` are also archived (same bytes) in the project archive folder
  `frontiers_dv_model_d_value_exploration_20261012/` (route, rigorous_prototype); the files added since (13 October) are
  `dv/vform5.py` (corrected `v`-range), `dv/stein_bounds*.py` (float cell-count explorations), and the rigorous modules
  `dd/ddtaylor.py`, `dd/ddbounds.py`, `dd/ddvq.py`, `dd/ddgauss.py`, `dd/ddS.py`, `dd/dd_exact.py`, `dd/test_bounds.py`.
- `MANIFEST.json`: path, size and SHA-256 of every file here (computed at commit time).
- **Update 06:10Z (the certificate's final state):** the corrected modules (the referee round of 03:16–04:03Z and the
  `require()` conversion so that `python -O` keeps every check), the final cells `dd/cells_full.json` (2393 cells, remainder
  bound `6.994·10⁻⁴`, `u ∈ [−6.2, 18.6]`), the node files `dd/nodes/nodes_k.json` (byte for byte the artifacts of run
  38347192184; `dd/nodes/artifacts_run_38347192184.json` lists the artifact ids and digests), `dd/results/` (the stdout of
  `dd_controls.py`, `dd_mutants.py` and `dd_exact.py` in both python modes), the note `dd/NOTE_DD_draft.md` (v1.0 as
  posted on main#307). The shard workflow is now `workflow_dispatch` only (every push re-triggered it). **Result:**
  `D ∈ [0.0757052049785748938, 0.0778600952308480156]`. Still PROTOTYPE / UNVERIFIED until the note's reads.
- **Update 03:00Z:** `dd/cells_full.json` (the 1914 adaptive cells, remainder bound `1.995·10⁻³`, `build_full.log`), the
  module updates of 02:45–03:00Z (`ddvq.py` log cells with rigorous sliver junctions, `ddcore.py` monotone-range safeguard,
  `ddgauss.py` shards, `dd_exact.py` multi-file assembly), `dd/NOTE_DD_draft.md` (the note's draft, numbers TBD) and the
  workflow `.github/workflows/dd-wip-shards.yml` that computes the node values in 12 shards (work in progress, not a
  certificate; its artifacts are the raw node files).

## What the files are (stage and limitations)

| Path | Stage | Notes |
|---|---|---|
| `dd/DD_TASK_DEFINITION_20261012.md` | definition | the target, route, error budget, dependencies, scope (posted 6134833037) |
| `dd/board_post.md` | record | the amended executor-division/task-definition post |
| `dd/ddcore.py` | rigorous core (tested) | decimal interval arithmetic with directed rounding; `exp`/`ln`/`sqrt` by the correctly rounded decimal functions widened by one ulp; `erf` by series with remainder; `Gamma` by Stirling with the first-omitted-term bound; Taylor models (`TMSpace`/`TM`, `TM1Space`/`TM1`) with Lagrange remainders; a monotone-range safeguard in the elementary functions (13 Oct) |
| `dd/ddint.py` | rigorous integrand (validated against floats) | `F(tau, g, v)` of the task definition §2(c) in Taylor-model arithmetic: closed-form `t`-moments (half-line recursion / series with rigorous remainder), cancellation-free `Delta`, `t_c`, `log pre`; the log-substituted integrand near `v = 1` |
| `dd/ddvq.py` | rigorous 1-D `v`-quadrature (validated: enclosures contain the float references at 14 `(tau, g)` points) | adaptive cells, order-8 Taylor models, scale-aware initial grid, log cells around `v = 1` for small `sigma_chi`, the `v`-tail bound; `H_point` |
| `dd/ddtaylor.py` | exact (Fractions) | the exact Taylor polynomial `T_N` of `g = I - I_quad` at the origin and the remainder constant `C_{N+1}` on a box (root localization lemma; `N = 11`, `B_t = 3/10`, `B_chi = 1`: `C_12 = 404.1`) |
| `dd/ddbounds.py` | rigorous bounds (tested) | the pointwise bound `|g| <= g~` (proved from the `v`-form identity; checked at 6108 points), kernel polynomials, Gaussian and incomplete moments, the Taylor-box bound, `rho`-derivative bounds by exact Bell polynomials, the tensor Gauss remainder per cell, the `v`-tail bound |
| `dd/ddgauss.py` | driver (running) | rows, adaptive cells by remainder bound, node evaluation with multiprocessing and checkpointing, omega-tail bounds, assembly |
| `dd/ddS.py` | closed forms (run) | region `tau <= tau_s` and the `tau`-tail: `D_S in [-2.041e-5, -2.004e-5]` at `tau_s = e^{-6.2}`; tail beyond `tau = e^{16.2}` `<= 1.9e-4` |
| `dd/dd_exact.py` | assembly (not yet run on a full cell set) | `D` and the corollary (note CJ's constants) |
| `dd/test_bounds.py`, `dd/test_cells.json` | tests / sample | — |
| `dd/ddcub.py`, `dd/ddih.py`, `dd/test_box.py` | superseded prototypes | 3-D TM cubature (infeasible), interval-Hessian AD (10^4–10^9 pessimistic) |
| `dv/*` | exploration (floats, numpy/scipy; outside the repository's standard-library rule) | `vform1–5.py` (route checks, `D` numerics: `D(tau <= 1e7) = 0.076714`, slabs `~ tau^{-1/2}`), `stein_bounds*.py` (cell-count estimates), logs |
| `lean/*` | formal-lane records | the toolchain-route logs (`main_formal_runlean.log`, `wt358_runlean.log`, `mformal_cache_get.log`, `mformal_execute.log`), the board report, owner relay, executor division, the #358 handoff receipt, `env.sh`, `unzst_tar.py` |

## Latest successful checkpoint, obligations, next step

- Latest successful checkpoint (13 Oct 02:45Z): region S and the tails in closed form; `H_point` validated; the adaptive
  cell build on `u in [-6.2, 16.2]` (target remainder `2e-3`) running; node evaluation not yet started.
- Remaining obligations: run the cells, assemble `D`, write note DD with the lemmas (pointwise bound, kernel derivatives,
  Taylor box, tails), controls and mutants; referee; post on main#307; then a Math- packet after reads.
- Blockers: none known; compute budget (~1–3 s per node, ~16 nodes per cell).
- Current owner: `session_01NMeKEismAyeqgdB4sy2NJU` (lease to 13 Oct 14:00Z per the claim).
- Next reproducible step: `python3 dd/ddgauss.py build cells.json 2e-3 -6.2 16.2`, then
  `python3 dd/ddgauss.py eval cells.json nodes.json <nproc>`, then `python3 dd/dd_exact.py cells.json nodes.json`
  (Python 3.11+, standard library; `dv/` needs numpy/scipy).
