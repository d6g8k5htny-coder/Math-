**AMEND for Slice B of lifetime note DD.** The certificate's long interval holds. Eight short displays do not cover the values they name. Slice A was not read. Scientific effect NONE. This claim is released. Author claim 6135715016 stays open.

GitHub refused a new comment. `POST /repos/d6g8k5htny-coder/main/issues/307/comments` and `PATCH` of acknowledgement 6139664497 both returned 403 `Resource not accessible by integration`, with `X-Accepted-GitHub-Permissions: issues=write; pull_requests=write`. The text below is the pickup and the verdict.

Dylan Roy — delegated AI review. Actual performer: xAI Grok 4.7, Cursor cloud agent `bc-42c6fc88-4761-4fb2-8382-3cbfda022d1f`, model `grok-4.7-high-fast` (run record; serving model not attested). Not Anthropic and not OpenAI. Organizational-independence credit 0. No source edit, no pull request, no timer.

**Pickup.** Re-summons [6139663531](https://github.com/d6g8k5htny-coder/main/issues/307#issuecomment-6139663531). No earlier Slice B pickup. Slice A PASS [6139419031](https://github.com/d6g8k5htny-coder/main/issues/307#issuecomment-6139419031) is a different reader. Served bodies were hashed before and after (`gh api … --jq .body`, one trailing newline removed). Both times: note [6139410118](https://github.com/d6g8k5htny-coder/main/issues/307#issuecomment-6139410118) is 23,330 B, SHA-256 `2331cd2763f98ccb057097559139e92b0a7fdf5393954fafb31f9c3faf808d0c`; controls [6139414648](https://github.com/d6g8k5htny-coder/main/issues/307#issuecomment-6139414648) are 9,110 B, SHA-256 `58fdb020f585f50cf2ce9e9a672830ba3d5d7e1c81c8fbbf251873c24bf5dc11`. Commit `35ae8fbb431a49a3ea15e5bcee299b83360a6348`. Every file named in the controls table matches the pinned size and hash: the ten Python files, `cells_full.json`, and `nodes/nodes_0.json` through `nodes_11.json`.

**What holds.** Python 3.12.3.

- **§3.1** describes `ddcore.py`: precision 30, two directed contexts, one-ulp widening of `exp`/`ln`/`sqrt` with the square-root check, Machin `π`, the `erf` series for `x ≤ 7`, Stirling `Γ` at `x+40` with 7 terms, order-8 Taylor models, and the factor-of-four monotone fallback.
- **§3.2.** `u ∈ [−6.2, 18.6]`, 62 rows of width `0.4`, `g_hi_of`, `g_lo = 0.002 g_hi`, 8 initial cells, target `7·10⁻⁴`, 4-point nodes and weights, `ρ·H` at thin nodes, order-8 `v`-quadrature, the log substitution when `σ_χ/(12σ_t) < 0.1` and `σ_t > 0.1`, four slivers hulled with `0`, short-decimal geometry, relative tolerance `5·10⁻³`, and the `v`-tail added after `(24τ√π)⁻¹`. `F_core` matches (1.3): both branches of `Φ̃`, `χ = χ₀ + χ₁ t`, degree-4 `P`, `Δ`, `α`, `t_c`, `log pre = −aμ²/Δ`, and the half-line recurrence. The series remainder is the geometric tail of `e^{−αu²}`.
- **Lemma 6.** Exponents and directions match `ddS.region_S`, `ddS.tau_tail` and `ddgauss.omega_tails`: `p = b+11/3`, `e = a+3b/2−9/2 < −1`, `G_β(0) = 2^{p−1}Γ(p/2)`, `M_β = 2^{p+3}Γ(p/2+2)`, the factor `2^{(a+1)/2}` from `Γ(s,x) ≤ 2^s Γ(s) e^{−x/2}`, and the AM–GM step `2√(c/8) = √(c/2)`.
- **§3.3.** The 2393 cells tile the 62 rows and are disjoint. Decade counts match. All 2393 cell remainders were recomputed and equal the stored values (sum `0.000699415225762334605564277483154`). Four nodes, cells 0, 400, 1200 and 2200, recomputed with `eval_node` and matched `nodes_k.json` exactly. Fresh assembly reproduces the controls stdout digit for digit, including `D ∈ [0.0757052049785748938015641071813, 0.0778600952308480155728023482430]`. The printed long enclosure, `0.0757052 ≤ D ≤ 0.0778601`, `q ∈ [0.672471, 0.674627]`, the four 7-decimal coefficient bounds, and the `D_S`, `ω` and `τ` rows are outward. `J`, `−Ĩ_quad`, the four `η` pairs, `𝒮₂` and `𝒮₃` match note CJ, note DC, note V24's table and #242 Corollary 1′. #244's Theorem A scope in the header and §5 matches #244 §8. No claim for `d ≥ 4` or `L < 10`.
- **§3.4.** `dd_controls.py` exited 0 with the pinned C1–C9 stdout. `dd_mutants.py` exited 0, all nine rejected. M1 fails C8b and C8c. M8 fails C3a.

**Exact changes.**

1. Header: `D = 0.07678 ± 0.00108` to `D = 0.07678 ± 0.001081`. The certified upper end is `0.07786009523…`; `0.07678 + 0.00108 = 0.07786`.
2. Header: `0.06156 ± 0.00010` in `d = 2` to `0.06156 ± 0.000103`. The `L ≥ 24` upper end is `0.06166277849…`; `0.06156 + 0.00010 = 0.06166`. The `d = 3` statement `0.07746 ± 0.00013` does cover.
3. Header: `1.8572c` to `1.8573c`, with `c` defined by `1.8544c = 0.0774672`. Then `1.8572c = 0.07758417 < 0.077585976…`. `1.8513c` does cover for that `c`.
4. §3.2 and the §3.3 table: `≤ 6.994·10⁻⁴` to `≤ 6.995·10⁻⁴`. The recomputed sum is `6.994152…·10⁻⁴`.
5. §3.3 Gauss sum: `[0.07649608, 0.07710967]` to `[0.07649607, 0.07710968]`. Both printed ends lie inside `[0.07649607876…, 0.07710967484…]`.
6. §3.3 polynomial part: `[−2.0249, −2.0204]·10⁻⁵` to `[−2.0250, −2.0204]·10⁻⁵`. The recomputed part is `[−2.02491037…, −2.02042910…]·10⁻⁵`.
7. §3.3: `R_C = 3.0·10⁻¹⁰` to `R_C ≤ 3.027·10⁻¹⁰`; `R_t = 1.6·10⁻⁷` to `R_t ≤ 1.611·10⁻⁷`; `R_χ = 1.1·10⁻²⁵` to `R_χ ≤ 1.13·10⁻²⁵`. Recomputed: `3.0262…·10⁻¹⁰`, `1.6105…·10⁻⁷`, `1.1285…·10⁻²⁵`.
8. Remark 3: `6.99·10⁻⁴` to `7.00·10⁻⁴`, and `5.7·10⁻⁵` to `5.8·10⁻⁵`. The `1.40·10⁻³` two-sided figure already covers twice the remainder.

**Not an amendment.** For one narrow test point, an `sv` model interval stopped `1.5·10⁻³⁰` short of its right endpoint. There `|F(1)| ≈ 1.9·10³`, so the omitted integral is about `3·10⁻²⁷`, inside the node widths. `F_core` does not divide by `v−1`.

**Not checked.** The other 20 of `dd_exact.py`'s 24-node sample, and the 26–75 minute shard rerun. Theorem A, Theorem V, note CJ and #242 were not re-proved. `ddcore.py` was read only against §3.1. No compiler.



<div><a href="https://cursor.com/agents/bc-42c6fc88-4761-4fb2-8382-3cbfda022d1f?cursor_ref=pr_footer&cursor_cta=open_in_web"><picture><source media="(prefers-color-scheme: dark)" srcset="https://cursor.com/assets/images/open-in-web-dark.png"><source media="(prefers-color-scheme: light)" srcset="https://cursor.com/assets/images/open-in-web-light.png"><img alt="Open in Web" width="114" height="28" src="https://cursor.com/assets/images/open-in-web-dark.png"></picture></a>&nbsp;<a href="https://cursor.com/background-agent?bcId=bc-42c6fc88-4761-4fb2-8382-3cbfda022d1f&cursor_ref=pr_footer&cursor_cta=open_in_cursor"><picture><source media="(prefers-color-scheme: dark)" srcset="https://cursor.com/assets/images/open-in-cursor-dark.png"><source media="(prefers-color-scheme: light)" srcset="https://cursor.com/assets/images/open-in-cursor-light.png"><img alt="Open in Cursor" width="131" height="28" src="https://cursor.com/assets/images/open-in-cursor-dark.png"></picture></a>&nbsp;</div>

