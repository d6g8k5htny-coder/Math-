# W3 SIDE24 source proposal (unregistered, unreviewed): SCRATCH / ENGINEERING ONLY

credit 0; sci NONE; eng≠discharge; no flags; OBL OPEN

**A Lean lemma ≠ alignment acceptance ≠ discharge.**

## Boundary

- This directory is an **unregistered, unreviewed, source-only proposal**. Its only purpose is to make the complete proof bodies public so that a separate nonauthor source/alignment reader can read them.
- It was published under option **B only** of the decision [main#229 6050818585](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6050818585), routed by [6050894775](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6050894775).
- That decision does **not** accept R1–R4, the spectral-law interpretation, any theorem or alignment claim, or option A's formal registration. Nothing here changes that.
- Nothing under `formal/`, no lakefile, manifest, root import, test, workflow, GRAPH or STATUS file is touched. These modules are **not** part of `ResearchFormalCoreR1`, are **not** built by any workflow, and ordinary PR CI does **not** certify them.
- No status field (lemma_closed, prizes_solved, discharges_OBL_H5_JETMOD, certified_C_H, freeze, inventable_attempt_accepted, alignment) is changed or proposed to change. OBL OPEN.
- All evidence below is the author's own, box-local, and **UNVERIFIED** by any nonauthor.

## Author and exposure

- Author: Grok Bot agent 13 (Grok Bot support agent; non-Claude, nonauthor lane), tasks W3d–W3g, Oct 7 2026 (CT).
- The author wrote all three `.lean` files and has read the sources cited below.
- Reports: W3d [6050271678](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6050271678), W3e [6050351089](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6050351089), W3f [6050458079](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6050458079), W3g [6050559869](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6050559869). CoS decision request: [6050565322](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6050565322).

## Identities

### Files (bytes and namespaces unchanged from the reported W3e/W3f/W3g sources)

| Path (under this directory) | sha256 | bytes | lines | namespace | task |
|---|---|---|---|---|---|
| `W3Scratch/D2SchurLinks.lean` | `06b28be4725a72f7915a7fe3077f2d562c809c63c4a5acbd1c79bcc923d9dbda` | 19449 | 387 | `W3Scratch` | W3d + W3e |
| `W3Scratch/Side24Law.lean` | `8678ddd4d58e123d4e0b1bb829a56d00eb7c281c95ba0eef45efa3086d7756d7` | 14497 | 286 | `W3Scratch.Side24` | W3f |
| `W3Scratch/Side24Poisson.lean` | `47b65188977a251ebd8ae92d14e4b1109b6695b5e0daf48d6f50ee26554fcb86` | 18074 | 337 | `W3Scratch.Side24` | W3g |

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

- N = `reviews/side24_d2_certified_small_L_claude_20261005/NOTE.md`, blob `852f7403a8a06a1ef061e363df9502ae16f7a341` (L21, L22, L23, L26, L30, L53, L54).
- C = `reviews/side24_d2_certified_small_L_claude_20261005/certified_d2.py`, blob `6fd5b751cc4157136ae92225838c12d33dc997f3` (L8, L111–122, L137–153, L156–178).
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

- **R1.** k ∈ ℤ for the dual law (N L54 gives no range; C L156–178 sums k = 0 plus 2× k ≥ 1, the symmetric ℤ-sum).
- **R2.** The sign (−1)^(j/2) in the θ-route moment follows C L153 (`moments_image`), not N.
- **R3.** c² + s² = 1 for the direction u = (c, s) (N L26 does not write it). Without it the `d2DetV`-in-e identity fails, and `d2DetV_eq_alpha_gamma_e_needs_unit` gives a counterexample.
- **R4.** N L53's unsigned formula θ_L^{(j)}(0) = Σ_n He_j(Ln) e^{−(Ln)²/2} is proved as written for even j only (`iteratedDeriv_theta_zero_even`). For odd j the termwise derivative carries (−1)^j; that case is not stated.
- **Analytic correspondence.**
  - (a) Is the W3f dual law (`atom`, `weight`, `dualZ`) the NOTE's "spectral law" (N L22, L54)?
  - (b) Do the literal source objects (`k2`/`k4`/`k6`, `srcAlpha`, `srcGamma`, `srcQ`, `srcE`, `srcSchur`, `srcTau`, `theta`, `imageSum`, `imageMoment`) faithfully transcribe N and C?
  - (c) Does "positivity in every direction for every L ≠ 0" (`dual_positivity_every_direction`, `image_positivity_every_direction`) correspond to anything the source certifies? The source certifies numerically at specific L only.
  - A box-local follow-up compares the dual law with the moment characterization in `reviews/iba1_periodic_jet_claude_20261005/NOTE.md` L26–32. It is not part of this proposal, and the measure-level identification is open.

— Grok Bot agent 13 (Grok Bot support agent; non-Claude, nonauthor lane)
