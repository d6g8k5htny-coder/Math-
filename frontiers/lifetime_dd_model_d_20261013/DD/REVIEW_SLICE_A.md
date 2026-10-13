**PASS for Slice A of lifetime note DD.** §§0–2 and `ddcore.py`, `ddbounds.py`, and `ddtaylor.py` hold at the pinned bytes. This does not certify the numerical interval for `D` or Corollary DD1. Slice B was not read. Scientific effect NONE. This claim is released. Author claim 6135715016 stays open.

GitHub refused the record. `POST /repos/d6g8k5htny-coder/main/issues/307/comments`, `PATCH` of acknowledgement 6139419031, and a comment on Math-#446 all returned 403 `Resource not accessible by integration`, with `X-Accepted-GitHub-Permissions: issues=write; pull_requests=write`. The text below is the pickup and the verdict.

Dylan Roy — delegated AI review. Actual performer: xAI Grok 4.7, Cursor cloud agent `bc-f621b80c-36df-402e-a3af-31e6b2b86eb1`, model `grok-4.7-high-fast` (run record; serving model not attested). Not Anthropic and not OpenAI. Organizational-independence credit 0. No source edit, no pull request, no timer.

Served bodies were hashed before and after the read (`gh api … --jq .body`, one trailing newline removed). Both times: note 6139410118 is 23,330 B, SHA-256 `2331cd2763f98ccb057097559139e92b0a7fdf5393954fafb31f9c3faf808d0c`; controls 6139414648 are 9,110 B, SHA-256 `58fdb020f585f50cf2ce9e9a672830ba3d5d7e1c81c8fbbf251873c24bf5dc11`. Certificate commit `35ae8fbb431a49a3ea15e5bcee299b83360a6348`. The five Slice A files match the pinned sizes and hashes.

What was checked:

- **§1.1.** On Math- `07320089`, (2.5) is `|c′|δ² + δ³/3` and (2.7) is the second form. With `ρ = ψ_e − 2c′` and `v² = ψ_e + c′`, both expand to the `v`-form (1.1). Control C1 matches.
- **§1.2.** Against note DC §0 and Lemma 4. `c₀ = 1/(2400√π) = 24√π A₃`, the measure `dτ dg = τ g du dω` produces `τ^{−5/3} g^{11/3}`, and `σ_t = 12√2 τ`, `σ_χ = 576√6 τ² g`.
- **§1.3.** Jacobian `12(v² − 1 + t) ≥ 0` on the domain, `t` from `1 − v²/3` to `∞`, completed square `t_c = −λμ/Δ` with prefactor `e^{−aμ²/Δ}`, and the half-line recurrence. C3 passed.
- **Lemma 1.** The `I_quad − R²/48` identity, both exact forms of `Φ − R²/48`, `ρ ≤ ρ_R` and `v² ≤ ρ_R`, and the monomial majorant (`x^{2/3}` subadditive, power mean of order `4/3`). C5: 6140 points, max ratio 0.9935.
- **Lemma 2.** Kernel recursion, the four logarithmic derivatives, `Q_{a,b}`, and the absolute Gaussian moments. C6 passed. M2 dies at import on the exact `p₁`, `p₂` check.
- **Lemma 3.** An independent undetermined-coefficient jet, not the certificate Newton, reproduces the posted degree-3 and degree-4 coefficients and the vanishing through degree 2. Localization is the condition written in the note. C7 gives `C₁₂ = 404.065…`. The three `EgQ_box` pieces and the incomplete-gamma bounds are valid.
- **Lemma 4.** `K_n`, the tensor remainder, Leibniz, the Bell recurrence, the `φ` derivatives, the unimodal maxima, and the `2×2` sub-cells. C8 passed.
- **Lemma 5.** The `v`-tail split is correct. C9 passed.
- **Lemma 6.** The gamma integral, the exponent `e = a + 3b/2 − 9/2 < −1`, the lower tail `g_lo^{11/3}/(11/3)`, and the AM–GM step match `ddS.py` and `ddgauss.omega_tails`. `region_S` and the assembly were not run.
- **`ddcore.py`.** Directed rounding, one-ulp widening, sqrt checked by squaring. Machin `π` contains the 50-digit value. `erf(1)`, `Γ(1)`, `Γ(2)`, and `Γ(1/2)` meet the known values. Taylor-model multiplication, the Lagrange step, the monotone fallback, the `exp` cap, and `integrate` were read.

Python 3.12.3: `python3 -B -S dd_controls.py` exited 0 with the pinned C1–C9 stdout. `python3 -B -S dd_mutants.py` exited 0, all nine rejected, including M2, M3, M4, M5, M6, M7, and M9.

Not checked: Slice B (§§3–5, `ddvq.py`, the adaptive quadrature, `dd_exact.py`, node recomputation, and the printed rounding of `D` and the corollary). Theorem A’s hypotheses, Theorem V, note CJ, and #242 were not re-proved. No compiler.

One observation, not an amendment: Taylor-model multiplication adds an extra `r_a r_b` on top of a product that already includes it. On these centered models that extra interval contains 0, so the remainder only gets wider.



<div><a href="https://cursor.com/agents/bc-f621b80c-36df-402e-a3af-31e6b2b86eb1?cursor_ref=pr_footer&cursor_cta=open_in_web"><picture><source media="(prefers-color-scheme: dark)" srcset="https://cursor.com/assets/images/open-in-web-dark.png"><source media="(prefers-color-scheme: light)" srcset="https://cursor.com/assets/images/open-in-web-light.png"><img alt="Open in Web" width="114" height="28" src="https://cursor.com/assets/images/open-in-web-dark.png"></picture></a>&nbsp;<a href="https://cursor.com/background-agent?bcId=bc-f621b80c-36df-402e-a3af-31e6b2b86eb1&cursor_ref=pr_footer&cursor_cta=open_in_cursor"><picture><source media="(prefers-color-scheme: dark)" srcset="https://cursor.com/assets/images/open-in-cursor-dark.png"><source media="(prefers-color-scheme: light)" srcset="https://cursor.com/assets/images/open-in-cursor-light.png"><img alt="Open in Cursor" width="131" height="28" src="https://cursor.com/assets/images/open-in-cursor-dark.png"></picture></a>&nbsp;</div>

