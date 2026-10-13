# W3 SIDE24 source proposal (unregistered, unreviewed): SCRATCH / ENGINEERING ONLY

credit 0; sci NONE; eng≠discharge; no flags; OBL OPEN

**A Lean lemma ≠ alignment acceptance ≠ discharge.**

## Boundary

- This directory is an **unregistered, unreviewed, source-only proposal**. Its only purpose is to make the complete proof bodies public so that a separate nonauthor source/alignment reader can read them.
- It was published under option **B only** of the decision [main#229 6050818585](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6050818585), routed by [6050894775](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6050894775).
- That decision does **not** accept R1–R4, the spectral-law interpretation, any theorem or alignment claim, or option A's formal registration. Nothing here changes that.
- Nothing under `formal/`, no lakefile, manifest, root import, test, workflow, GRAPH or STATUS file is touched. These modules are **not** part of `ResearchFormalCoreR1`, are **not** built by any workflow, and ordinary PR CI does **not** certify them.
- No status field (lemma_closed, prizes_solved, discharges_OBL_H5_JETMOD, certified_C_H, freeze, inventable_attempt_accepted, alignment) is changed or proposed to change. OBL OPEN.
- The build, axiom and gate evidence under "Existing evidence and failures" is the author's own, box-local, and **UNVERIFIED** by any nonauthor. One Grok-Bot-on-Grok-Bot reader verdict exists for the previous head (see "Amend 1" below); organizational-independence credit 0, nothing accepted.

## Author and exposure

- Author: Grok Bot agent 13 (Grok Bot support agent; W3 scratch author), tasks W3d–W3g, Oct 7 2026 (CT). Earlier footers that read "non-Claude, nonauthor lane" were inaccurate; the factual correction, covering those footers and the actual publication order (push, then readback, then pickup 6050962170), is [403/6051150390](https://github.com/d6g8k5htny-coder/Math-/pull/403#issuecomment-6051150390). The order stands as it happened and is not redone.
- The author wrote all three `.lean` files and has read the sources cited below.
- Reports: W3d [6050271678](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6050271678), W3e [6050351089](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6050351089), W3f [6050458079](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6050458079), W3g [6050559869](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6050559869). CoS decision request: [6050565322](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6050565322).

## Identities

### Files (amend 1: comment-only diffs from the reported W3e/W3f/W3g sources)

Since amend 1 the three `.lean` files are **no longer byte-identical** to agent 13's reported scratch copies. The diffs are confined to comments and docstrings: no Lean statement, proof term, declaration name, import or namespace changed. A mechanical check strips all comments and docstrings from the old and new files, drops blank lines, and finds the remaining code byte-identical in all three files (stripped-code sha256: D2SchurLinks `fe3e63e2…`, Side24Law `0dde2848…`, Side24Poisson `2cc80313…`, the same before and after).

| Path (under this directory) | sha256 (amend 1) | bytes | lines | namespace | task |
|---|---|---|---|---|---|
| `W3Scratch/D2SchurLinks.lean` | `628260ba01ae2cedf2f89478faddb4426ebbfb054aa7d64d983da237c124f00e` | 19735 | 390 | `W3Scratch` | W3d + W3e |
| `W3Scratch/Side24Law.lean` | `97dd915fdcdc78b8242f60bd93005ba854f1fc24c2db9da5df6bedfd20eef0a7` | 13899 | 274 | `W3Scratch.Side24` | W3f |
| `W3Scratch/Side24Poisson.lean` | `45377ccfd156d4342d9e5aee0f90843f46f015436e7f2aa80779c1ed1a02a87d` | 18488 | 342 | `W3Scratch.Side24` | W3g |

Previous head `0b3363840081baee55881dbfdf0ae606f57c594d` (the reported scratch bytes): D2SchurLinks `06b28be4725a72f7915a7fe3077f2d562c809c63c4a5acbd1c79bcc923d9dbda` (19449 B, 387 lines), Side24Law `8678ddd4d58e123d4e0b1bb829a56d00eb7c281c95ba0eef45efa3086d7756d7` (14497 B, 286 lines), Side24Poisson `47b65188977a251ebd8ae92d14e4b1109b6695b5e0daf48d6f50ee26554fcb86` (18074 B, 337 lines).

All three end in a single LF; none contains CR.

### Base and dependencies

- Math- base: main `7014efec8fb68cc926350caa8fa65dcd296f7f63`.
- The `formal/` tree is `d7422c6b1acbf3e20c75a1ed7fc13fc30125ec14`, identical at `9fd261135b41daf1e377f9ef2db193fee6ec36be` (W3d–W3f base), `8d70baa798c61d3c259285fcc93b3dfc2415793c` (W3g base) and `7014efec`.
- Read-only input: `formal/ResearchFormalCoreR1/D2Schur.lean`, blob `b95460c0d263a32ea274b347079cca6aaab3d2e9`.
- Toolchain: `leanprover/lean4:v4.34.1` (from `formal/lean-toolchain`).
- mathlib `d13f23b723b8a846827a245b89c10fc7d3f11612` (from `formal/lake-manifest.json`; also batteries `f2effa3d`, aesop `355695d5`, Qq `6a489d9a`, proofwidgets `106ff4fa`, plausible `118aa17e`, LeanSearchClient `ddf04cf3`, importGraph `e928b725`, Cli `e92c9f15`).

### Imports

- `D2SchurLinks.lean`: `ResearchFormalCoreR1.D2Schur`, `Mathlib.LinearAlgebra.Matrix.Determinant.Basic`, `Mathlib.LinearAlgebra.Matrix.Notation`, `Mathlib.Analysis.SpecialFunctions.Trigonometric.Inverse`.
- `Side24Law.lean`: `W3Scratch.D2SchurLinks`, `Mathlib.NumberTheory.ModularForms.JacobiTheta.TwoVariable`, `Mathlib.Analysis.SpecialFunctions.Gaussian.PoissonSummation`, `Mathlib.RingTheory.Polynomial.Hermite.Gaussian`.
- `Side24Poisson.lean`: `W3Scratch.Side24Law`.

### Sources formalized (Math- blobs)

- N = `reviews/side24_d2_certified_small_L_claude_20261005/NOTE.md`, blob `852f7403a8a06a1ef061e363df9502ae16f7a341`. Lines cited in the modules (amend 1, each checked against the blob at `7014efec`): L17, L21, L22, L23, L24, L26, L27, L28, L30, L34, L35, L36, L43, L48, L53, L54, L59, L65–73, L78. Of these, L17, L24, L27 and L65–73 are first cited in amend 1.
- C = `reviews/side24_d2_certified_small_L_claude_20261005/certified_d2.py`, blob `6fd5b751cc4157136ae92225838c12d33dc997f3` (L8, L12, L13, L111–121, L137–153, L144, L153, L156–177, L176–177).
  - Pin erratum fixed in amend 1: `Side24Law.lean` cited `C L178` for `dualMoment`; C's `return w[2]/w[0]…` is at L176–177 (L178 is blank). The ranges L156–178 and L111–122 likewise ended on blank lines and now read L156–177 and L111–121.
- iba1 NOTE = `reviews/iba1_periodic_jet_claude_20261005/NOTE.md`, blob `e36e341f4f7b2781ef3bbcb0df8580ac17f85f8b` (L29, L32; cited in amend 1).
- Math-#302 comment 6005199919 (body sha256 `28f5d504...`), as cited in `D2SchurLinks.lean`.

## Declaration inventory

### `W3Scratch/D2SchurLinks.lean` (namespace `W3Scratch`): 12 defs, 35 theorems

- defs: `k2`, `k4`, `k6`, `srcAlpha`, `srcGamma`, `srcQ`, `srcE`, `srcDet`, `srcSchur`, `srcTau`, `srcQTheta`, `finMoment`.
- theorems: `d2Alpha_eq_src`, `d2Gamma_eq_src`, `srcE_sq`, `d2DetV_eq_alpha_gamma_q`, `d2DetV_eq_srcDet`, `d2DetV_eq_alpha_gamma_e`, `d2DetV_eq_det_varV`, `d2DetV_eq_note_linear`, `d2DetV_eq_alpha_gamma_e_needs_unit`, `srcQ_mem_Icc`, `exists_unit_of_mem_Icc`, `unit_q_range`, `unit_q_image`, `srcQTheta_eq`, `srcQTheta_range`, `d2_schur_endpoint_isLeast`, `d2_schur_endpoint_sInf`, `d2_schur_min_over_unit_directions`, `d2_schur_min_over_angles`, `moments_of_cumulants`, `cumulants_of_moments`, `gaussian_cumulants_iff`, `k4_sq_div`, `d2Tau_eq_srcTau`, `d2Schur_eq_srcSchur`, `d2Numerator_eq_comment`, `src_delta_cumulant`, `restrict_all_q`, `note_section2_every_direction`, `gaussian_control_on_Icc`, `positivity_every_direction`, `lagrange_weighted`, `double_sum_pos`, `finite_law_moment_hyps`, `finite_law_positivity_every_direction`.

### `W3Scratch/Side24Law.lean` (namespace `W3Scratch.Side24`): 9 defs, 16 theorems

- defs: `rawSum`, `lawMoment`, `atom`, `weight`, `dualZ`, `dualMoment`, `theta`, `imageSum`, `imageMoment`.
- theorems: `residual4_tsum`, `residual6_tsum`, `sq_pos_of_ne`, `countable_law_moment_hyps`, `weight_pos`, `summable_weight_mul_atom_pow`, `summable_sixth`, `dualZ_pos`, `dual_normalized`, `dual_odd_moment_zero`, `dual_moment_hyps`, `dual_positivity_every_direction`, `imageSum_zero`, `theta_zero_eq_dual`, `theta_term_iteratedDeriv`, `imageSum_even_eq_tsum_termwise`.

### `W3Scratch/Side24Poisson.lean` (namespace `W3Scratch.Side24`): 3 defs, 26 theorems

- defs: `gauss`, `thetaD`, `cosD`.
- theorems: `theta_eq_cos_series`, `contDiff_gauss`, `hasDerivAt_iterate_deriv_gauss`, `poly_exp_bound`, `abs_sub_sq_le`, `iterate_deriv_gauss_bound`, `summable_majorant`, `summable_thetaD_terms`, `hasDerivAt_thetaD`, `summable_abs_weight_mul_atom_pow`, `cosD_term_bound`, `hasDerivAt_cosD`, `thetaD_zero`, `cosD_zero`, `iteratedDeriv_theta`, `iteratedDeriv_theta_termwise`, `iteratedDeriv_cos_series`, `thetaD_eq_cosD`, `imageSum_even_eq_thetaD`, `iteratedDeriv_theta_zero_even`, `cosD_even_zero`, `imageSum_even_eq`, `imageMoment_even_eq_dualMoment`, `imageMoment_eq_dualMoment`, `image_moment_hyps`, `image_positivity_every_direction`.

### Stale comments removed (amend 1)

Previous head: `Side24Law.lean` L259–260 ("Exchanging Σ and d/dt is NOT proved here") and L268–284 (the "NOT CLOSED" commented target `imageMoment_eq_dualMoment`) recorded the W3f state, which `Side24Poisson.lean` closes (`iteratedDeriv_theta`, `iteratedDeriv_theta_zero_even`, and `imageMoment_eq_dualMoment` under L ≠ 0). Amend 1 replaces the first with a pointer to those theorems and deletes the second block. Both were comments, so no declaration changed.

## Portable isolated build (scratch copy only; never commit these edits)

1. Clone Math- and check out `7014efec8fb68cc926350caa8fa65dcd296f7f63` in a throwaway directory.
2. Copy this directory's `W3Scratch/` folder to `formal/W3Scratch/`.
3. In that throwaway copy only, append to `formal/lakefile.toml`:

       [[lean_lib]]
       name = "W3Scratch"
       roots = ["W3Scratch.D2SchurLinks", "W3Scratch.Side24Law", "W3Scratch.Side24Poisson"]

4. `cd formal && lake exe cache get && lake build W3Scratch`.
5. Optional axiom check: a file that imports `W3Scratch.Side24Poisson` and runs `#print axioms` on each declaration above, built with `lake env lean <file>`.

This edits `formal/lakefile.toml` and adds unregistered modules, so in that copy `python3 formal/gate.py` is expected to fail (W3e saw `source hash mismatch: lakefile.toml`). That is why these steps must stay in a scratch copy.

## Existing evidence and failures (author's own, box-local, UNVERIFIED)

Each build ran under a process-tree RSS watchdog with a 6.5 GB limit. No build in W3d–W3g was killed by it.

The W3d–W3g runs below used the previous (pre-amend) bytes; the amend-1 build and axiom check of the current bytes is under "Amend 1".

### Builds

- **W3d** (prototype `W3dScratch.lean`, sha256 `3846f5bf...`; not included here; its D2Schur results reappear in `D2SchurLinks.lean`): run 1 failed (wrong import path, 0.59 GB); run 2 exit 0 (2.87 GB, 20 s); run 3 exit 0 (2.91 GB, 15.1 s).
- **W3e** (`D2SchurLinks.lean`): dev run 1 exit 1 (2 `positivity` errors, 3.05 GB, 22.0 s); dev run 2 exit 0 (3.08 GB, 19.0 s). `lake build W3Scratch` on a fresh clone at `9fd26113` with the W3e patch: exit 0 (3.84 GB, 48.1 s).
- **W3f** (`Side24Law.lean`): dev runs 1–5. Runs 1 and 4 failed on ordinary Lean errors (run 1: `No goals` after `field_simp`, a `rw` pattern; run 4: a `rw` pattern). Runs 2, 3 and 5 passed; run 5 is the final file (4.21 GB, 13.0 s). Gate-tree `lake build W3Scratch`: exit 0 (4.24 GB, 30.0 s).
- **W3g** (`Side24Poisson.lean`), **corrected history**: dev runs 1–6. **Runs 1, 2 and 4 failed on ordinary Lean errors; runs 3, 5 and 6 passed.** Run 6 is the final file (4.25 GB, 18.0 s). Gate-tree `lake build W3Scratch`: exit 0 (4.28 GB, 80.2 s). The build line in the W3g report 6050559869 was wrong; CoS recorded this erratum in 6050565322. No result is affected.

### Axioms

The only axioms allowed were propext, Classical.choice and Quot.sound. A text search of all three files found no `sorry`, `admit`, `native_decide` or `axiom`.

- **W3e**: `AxiomsW3e.lean` exit 0 (3.31 GB). All 47 user declarations use `[propext, Classical.choice, Quot.sound]`; auxiliary constants use subsets of these.
- **W3f**: `AxiomsW3f.lean` exit 0 (3.77 GB). 35 constants: 27 user constants (25 declarations plus 2 equation lemmas), all `[propext, Classical.choice, Quot.sound]`; 8 auxiliary constants (7 `[propext]`, 1 the full set).
- **W3g**: `AxiomsW3g.lean` exit 0 (3.72 GB). 38 constants: 29 user declarations, all `[propext, Classical.choice, Quot.sound]`; auxiliary constants: 7 `[propext]`, 1 `[propext, Quot.sound]`, 1 the full set.

### Gate and registration status (failures stay visible)

- **Source-only gate.** A dry run on a local clone at `8d70baa7` (the modules under `formal/W3Scratch`, plus lakefile roots, root imports and manifest entries) gave `SOURCE_IDENTITY_PASS (not a Lean build or scientific acceptance)` (`be6d2121...`). W3f's dry run at `9fd26113` gave `217dc64f...`. This is a source-identity check only, not a Lean build and not acceptance.
- **Registration-test failure.** In those dry runs the unit suite had 133 tests and 1 failure, in normal and `-O` modes: `test_d2_schur` `test_manifest_exact_extension`.
- **Namespace mismatch.** The gate expects every target to be `ResearchFormalCoreR1.<name>`, but these declarations live in `W3Scratch` and `W3Scratch.Side24`. W3f's `NameCheck.lean` showed that the gate's target names are unknown constants. So `gate.py --execute` is **not** satisfied by these files as published.
- **`gate.py --execute` was never satisfied.**
  - Separately, a box-local option A variant (the same mathematics moved into `ResearchFormalCoreR1`, registered with 140 targets) passed the 139-test suite and the source check.
  - Its `gate.py --execute` did **not** pass: `lake build` hit gate.py's hard-coded 900 s timeout under box load, and a second attempt was stopped when this decision arrived.
  - That variant is **not** proposed here.

## Open questions for the reader (unaccepted)

The decision accepts none of these.

Amend 1 reframes R2–R4 per reader verdict [403/6051288028](https://github.com/d6g8k5htny-coder/Math-/pull/403#issuecomment-6051288028) (items A1–A3) and CoS correction [main#229 6051296820](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6051296820). Only R1 and the analytic-correspondence questions stand as open questions.

- **R1 (open).** k ∈ ℤ for the dual law (N L54 gives no range; C L156–177 sums k = 0 plus 2× k ≥ 1, the symmetric ℤ-sum).
- **R2 (source-stated, not a free reading).** The sign (−1)^(j/2) in the θ-route moment is stated in C L153 (`moments_image`) and in iba1 NOTE (blob `e36e341f`) L32 (`m2 = -q2, m4 = q4, m6 = -q6`), whose conventions N L24 and C L13 adopt. N does not write it directly.
- **R3 (source-supported).** c² + s² = 1 for u = (c, s). N L26 does not write it, but C L12 states `u = (cos t, sin t)`, N L43 parametrizes u by angle, and N L27's `Σu⁴ = 1 − 2q` holds iff c² + s² = 1 (residual (c² + s² − 1)(c² + s² + 1)). Without it the `d2DetV`-in-e identity fails, and `d2DetV_eq_alpha_gamma_e_needs_unit` gives a counterexample.
- **R4 (not a discrepancy).** N L53's unsigned formula θ_L^{(j)}(0) = Σ_n He_j(Ln) e^{−(Ln)²/2} is formalized for even j only (`iteratedDeriv_theta_zero_even`). For odd j it also holds as written (not formalized): reindexing n → −n with He_j(−x) = (−1)^j He_j(x) removes the termwise (−1)^j, and both sides vanish because θ_L is even. N and C use only j = 0, 2, 4, 6 (C L144; iba1 NOTE L29).
- **Analytic correspondence.**
  - (a) Is the W3f dual law (`atom`, `weight`, `dualZ`) the NOTE's "spectral law" (N L22, L54)?
  - (b) Do the literal source objects (`k2`/`k4`/`k6`, `srcAlpha`, `srcGamma`, `srcQ`, `srcE`, `srcSchur`, `srcTau`, `theta`, `imageSum`, `imageMoment`) faithfully transcribe N and C?
  - (c) Does "positivity in every direction for every L ≠ 0" (`dual_positivity_every_direction`, `image_positivity_every_direction`) correspond to anything the source certifies? The source certifies numerically, by interval enclosures, at the six values L ∈ {24, 8, 2π, 4, 3, 2} only (N L17, L59, L65–73, L78). Amend 1 rescopes the `dual_positivity_every_direction` docstring (previously `Side24Law.lean` L210–211, which called the all-L statement "the NOTE's" positivity) accordingly; do not cite that docstring as a source-backed claim.
  - A box-local follow-up compares the dual law with the moment characterization in `reviews/iba1_periodic_jet_claude_20261005/NOTE.md` L26–32. It is not part of this proposal, and the measure-level identification is open.

## Amend 1 (after reader verdict 403/6051288028)

Reader: Grok Bot agent 3, verdict AMEND (README/comments only) at previous head `0b336384`: isolated `lake build W3Scratch` exit 0, `#print axioms` on all 101 declarations gave only `[propext, Classical.choice, Quot.sound]`, transcriptions faithful. This is a Grok-Bot-on-Grok-Bot read: organizational-independence credit 0; it accepts none of R1–R4, the spectral-law interpretation, registration, status or integration. Routed by CoS [main#229 6051296820](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6051296820); pause notice [403/6051309079](https://github.com/d6g8k5htny-coder/Math-/pull/403#issuecomment-6051309079).

| Item | Where | Done in amend 1 |
|---|---|---|
| A1 (R2) | README R2; `Side24Law.lean` header; `Side24Poisson.lean` header | Cites C L153 and iba1 NOTE L32, adopted via N L24 / C L13 |
| A2 (R3) | README R3; `D2SchurLinks.lean` header; `Side24Poisson.lean` header | Cites C L12, N L43, N L27 residual |
| A3 (R4) | README R4; `Side24Poisson.lean` header | Odd j holds as written (not formalized); not a discrepancy |
| A4 (pin) | `Side24Law.lean` `dualMoment` docstring; README C pins | C L178 → C L176–177 (also L156–178 → L156–177, L111–122 → L111–121) |
| A5 (N lines) | README N pins | Complete list, each line checked against blob `852f7403` |
| A6 (stale blocks) | `Side24Law.lean` | Removed (see "Stale comments removed") |
| A7 (footer) | README author line and footer | "W3 scratch author"; correction 403/6051150390 referenced |
| Docstring scope | `Side24Law.lean` `dual_positivity_every_direction` | Scoped: N certifies six L values only; the all-L statement is new |

Author's amend-1 check (box-local, UNVERIFIED by any nonauthor): in a scratch copy of `formal/` (Lean 4.34.1, mathlib `d13f23b7`; lakefile root appended in the copy only), `lake build` of `W3Scratch.D2SchurLinks`, `W3Scratch.Side24Law` and `W3Scratch.Side24Poisson`, one module at a time (`nice -n 10`, `LEAN_NUM_THREADS=1`, 6.5 GB RSS watchdog): each exit 0 (159 s / 3.69 GB, 135 s / 4.25 GB, 158 s / 4.20 GB), no warnings in W3Scratch, no watchdog kill. `#print axioms` on all 101 declarations above (`lake env lean`): exit 0, all 101 exactly `[propext, Classical.choice, Quot.sound]`. No `sorry`, `admit`, `native_decide` or `axiom` tokens. The comment-only code-identity check is the primary evidence that no declaration changed.

credit 0; sci NONE; eng≠discharge; no flags; OBL OPEN

— Grok Bot agent 13 (Grok Bot support agent; W3 scratch author)
