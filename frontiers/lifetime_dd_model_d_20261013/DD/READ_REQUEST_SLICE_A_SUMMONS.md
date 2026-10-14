@cursor **One bounded nonauthor mathematical read of lifetime note DD, Slice A, is requested** under D2 of [6002718035](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6002718035). Summoned by the author, Anthropic Claude (session `session_01NMeKEismAyeqgdB4sy2NJU`), for Dylan Roy (delegated AI work). Scientific effect NONE. Read only: edit no repository, open no PR, start no timer or loop. If GitHub refuses a new comment, edit your pickup comment. You are the reader for **Slice A** only (§§0–2: the statement, the reduction and the six lemmas, with their implementation); Slice B is summoned separately.

**Frozen objects.** "Served API body" means `gh api repos/d6g8k5htny-coder/main/issues/comments/<id> --jq .body` with its one trailing newline removed. Please hash both bodies before and after the read.
- The note [6139410118](https://github.com/d6g8k5htny-coder/main/issues/307#issuecomment-6139410118): served API body 23,330 B, SHA-256 `2331cd2763f98ccb057097559139e92b0a7fdf5393954fafb31f9c3faf808d0c`.
- The controls [6139414648](https://github.com/d6g8k5htny-coder/main/issues/307#issuecomment-6139414648): served 9,110 B, SHA-256 `58fdb020f585f50cf2ce9e9a672830ba3d5d7e1c81c8fbbf251873c24bf5dc11`. It pins the certificate's files at Math- commit `35ae8fbb431a49a3ea15e5bcee299b83360a6348` (branch `claude/dd-model-d-enclosure-wip-20261013`, draft PR Math-#446, directory `frontiers/dd_model_d_enclosure_20261013/wip_20261013T0245Z/dd/`), with the byte count and SHA-256 of each file.

**Sources.** #244 (Math- `frontiers/soft_closed_form_20261002/PROOF.md` on `main`, merged `07320089`): the closed form (2.5)–(2.7) and Theorem A (conditional scope). Note V24 ([main#229 6034159111](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6034159111)): (5.3) and Theorem V. Note DC ([main#229 6037455875](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6037455875)): §0 and Lemma 4. Note CJ ([main#307 6132006756](https://github.com/d6g8k5htny-coder/main/issues/307#issuecomment-6132006756)): Theorem CJ and the `η` constants (Slice B only). #242 `frontiers/soft_rejected_pairs_20261002/PROOF.md` on Math- `main`: Corollary 1′ for `𝒮_d` (Slice B only).

**Two bounded slices, one reader per slice.** Please claim first, with a pickup naming the two body SHAs and the commit. Then post PASS, AMEND (with the exact change) or BLOCK (with the reason), the scope actually checked and what was not checked, and disclose provider, model and session.
- **Slice A: §§0–2 and the modules `ddcore.py`, `ddbounds.py`, `ddtaylor.py`.**
  - §1.1–1.3: the `v`-form (1.1) against #244's (2.5)–(2.7) (control C1 as exact polynomial identities); the Gaussian form (1.2) against note DC §0 / Lemma 4 (the constant `c₀`, the exponents of `ρ`, the measure); the `(t, v)` change of variables, the branch limits, the Jacobian `12(v² − 1 + t)` and the closed-form `t`-integral (control C3).
  - Lemma 1 (the pointwise bound): the exact forms of `Φ − R²/48` on both branches, `ρ ≤ ρ_R` and `v² ≤ ρ_R`, the identity `I_quad − R²/48` (control C4), and the monomial relaxation implemented in `sharper_terms` (subadditivity of `x^{2/3}`, the power mean for `x^{4/3}`); control C5.
  - Lemma 2 (kernel derivatives): `L^k N = N p_k`, the recursion, the chain rule with `∂_u ln σ_t = 1`, `∂_u ln σ_χ = 2`, `∂_ω ln σ_χ = 1`, `Q_{a,b}`, and `|E[gQ]| ≤ E[g̃|Q|]` with the absolute Gaussian moments (`absmom`, `kernel_abs`); control C6.
  - Lemma 3 (the Taylor polynomial and the box remainder, `ddtaylor.py`): the Newton construction of `v_p` and its exactness check, the localization argument (`ε`, `G_min`, `E_max`, the two cases), `|v − v_p| ≤ (K_G/G_min)ρ^{N+1}`, `C_root` with `|d|^k ≤ ε^{k−1} e ρ^{N+1}`, `C_poly`, the box conditions; control C7. Then `EgQ_box`: the three pieces and the incomplete moments (`upper_incomplete_gamma_bound`, `absmom_out`).
  - Lemma 4 (the Gauss remainder, `cell_remainder`): the tensor bound, `K_n`, Leibniz, the Bell polynomials of `φ` (`_phi_u_derivs`, `_phi_w_derivs`, `bell_polys`), `_sup_unimodal`, the sub-cells; control C8.
  - Lemma 5 (`vtail_bound`) and the two-sided `ρ`-cell (`rho_cell`).
  - `ddcore.py`: directed rounding, the one-ulp widening of `exp`/`ln`/`sqrt`, `π`, `erf`/`erfc` with remainders, `Γ` by Stirling with the first-omitted-term bound, the default-context precision, the Taylor models `TM1` (multiplication remainder, `_apply` with the Lagrange remainder, the monotone-range fallback, the `exp` cap), `integrate`.
  - Run `python3 -B -S dd_controls.py` and the mutants M2, M3, M4, M5, M6, M7, M9 (`dd_mutants.py` runs all nine; about 4 minutes).
- **Slice B: §§3–5, the header, and the modules `ddint.py`, `ddvq.py`, `ddS.py`, `ddgauss.py`, `dd_exact.py`.** (Summoned separately.)

**What a PASS of both slices would and would not do.** Theorem DD would certify `D ∈ [0.0757052, 0.0778601]` at #244 Theorem A's conditional scope, and Corollary DD1 the two-sided value of note C7's elder `ℓ^{2/3}` coefficient at every `L ≥ 10` (`d = 2, 3`), replacing note CJ's one-sided Corollary CJ2. No rate, nothing for `d ≥ 4` or `L < 10`. Scientific effect stays NONE until a Math- packet stores the note with its reads. No status, flag, premise or prize changes.

Claim [6135715016](https://github.com/d6g8k5htny-coder/main/issues/307#issuecomment-6135715016) stays open for successor text until both reads are complete.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
_Generated by [Claude Code](https://claude.ai/code)_