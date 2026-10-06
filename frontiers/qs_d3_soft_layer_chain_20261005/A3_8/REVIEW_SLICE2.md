**BLOCK lifted → PASS** on QS addendum A3.8, Slice 2. A3.4 §0 sets `rλ̃/k` equal to the smaller eigenvalue of `−A`, so the larger-eigenvalue branch in [6007722459](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6007722459) lies outside the coordinate image. Lemma 5.1 step 3’s threshold stands as written. No estimate changes.

Dylan Roy — delegated AI review. Actual performer: xAI, Grok 4.7, Cursor cloud agent, run model `grok-4.7-high-fast`, session `bc-31f1aced-3b79-4e25-b3ef-6e8ff04b2644`. This is a fresh session; `bc-ea15a5c7…` wrote the BLOCK. Provider-distinct from the note’s author (Anthropic Claude, `session_01NMeKEismAyeqgdB4sy2NJU`). Same provider as that BLOCK. Organizational-independence credit 0. Personal reading PENDING. Scientific effect NONE.

GitHub rejected a new comment and an edit of pickup [6008104745](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6008104745) (HTTP 403, resource not accessible to the integration). No repository edit, pull request, timer, or loop.

## Bodies read

- Frozen note [6007704303](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6007704303): 45,818 bytes, SHA-256 `afd2271252aa66c7e99f8fd7cb5ad194d881a56dcddcb9c726438f879b2c6451`. Unchanged.
- Successor text [6008104016](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6008104016): 5,431 bytes, SHA-256 `8a14d2e23bc23e10d116f5cb5dcdfcc8ccc3ccf1c51a554d0d5da63437f61e30`. Three `ℝ¹¹` → `X` replacements, and one inserted sentence in Lemma 5.1 step 3. Additive; the note is not edited.
- A3.4 [5999129544](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5999129544) §0 and Lemma S. Its successor [5999301338](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5999301338) changes conditioning bookkeeping and one signed-determinant phrase; the sentence `λ₁ ≤ λ₂`, `λ̃ := kλ₁/r` is untouched.
- A3.6 [6002480647](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6002480647) §0, and Astra’s source check [6007893752](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6007893752).

## The coordinate

A3.4 §0 sets `A := D²_Θ f(0) ∈ Sym(2)`, `Θ = u^⊥`, and then says: let `λ₁ ≤ λ₂` be the eigenvalues of `−A` and `λ̃ := kλ₁/r`. Where `λ₁ < λ₂`, `θ` is the angle of the `λ₁`-eigenline. Lemma S’s chart is `{λ₂ > rλ̃/k} × [0, π)`, with `Ψ_r = −R_θ diag(rλ̃/k, λ₂) R_θᵀ`, and (J₃.18) carries `(λ₂ − rλ̃/k)₊`. (J₃.1) is evaluated on `{λ₁ < λ₂}`. Theorem J₃ records that `0 < λ₂ ≤ rλ̃/k` contributes nothing, because no matrix has `λ₂ < λ₁`.

A3.8 §0 imports these coordinates and defines `D_Λ := {|λ̃| ≤ Λ}` in them. A3.6 §0 imports the same `(λ̃, λ₂, θ, t)`. A3.6 (0.1) is the cubic `P_QS`, with `ψ := 24λ̃/γ²`.

On the image of this map, `rλ̃/k = λ₁ = λ_min(−D²_Θ f(0)) ≤ λ₂`. A3.8’s `D²_⊥ f(0)` in Lemma 5.1 is that transverse Hessian. At the schematic spectrum `{10^{−6}, 10^{−2}}` with `r = 10^{−6}` and `k = 1`, the defined `λ̃` is `1`, so with `Λ = 10³` the point lies in `D_Λ`.

## Weyl on the smaller eigenvalue

The Lipschitz bound already accepted in the BLOCK stays: `‖D²_⊥ f(0) − A_M‖_op ≤ (r/2) M₃`. Weyl’s inequality for the smallest eigenvalue gives

`λ₁^{mid} = λ_min(−D²_⊥ f(0)) ≤ λ_min(−A_M) + (r/2) M₃`.

On depth failure, [P] (7.1) at `m = 2` gives `λ_min(−A_M) ≤ (4/(3k)) r M₃²`. With `M₃ ≤ √2 K₀^{[P]} U` and `D = 8 K₀^{[P]²}/(3k₋)`, the relation `k ≥ k₋` yields `(4/(3k)) r M₃² ≤ D r U²`. Also `(r/2) M₃ ≤ r K₀^{[P]} U/√2`. Therefore

`λ̃ = k λ₁^{mid}/r ≤ k(D U² + K₀^{[P]} U/√2)`.

`J_r := 1 + ‖g_r‖_{C⁴}` gives `U = J_r + λ_max ≥ 1`, and `k ≤ k₊`, so `K₀^{[P]} U/√2 ≤ K₀^{[P]} U²`. Hence `λ̃ ≤ k₊(D + K₀^{[P]}) U² = C_U U²` with the note’s `C_U`. So `λ̃ > Λ` forces `U ≥ (Λ/C_U)^{1/2}`. The `λ̃ < −Λ` comparison remains the one the BLOCK already accepted.

The successor’s inserted sentence records this identification and leaves the constants unchanged. A3.8 §0 already imports the definition, so the lift is PASS.

Lemmas 3.1–3.2, 4.1–4.2, 5.2–5.3, ES₃, the model half of Lemma 5.4, and the controls remain the delivered content of [6007722459](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6007722459). This readback does not repeat them and does not re-execute `a38_exact.py`. §§1–2 and §6 stay outside this slice.



<div><a href="https://cursor.com/agents/bc-31f1aced-3b79-4e25-b3ef-6e8ff04b2644?cursor_ref=pr_footer&cursor_cta=open_in_web"><picture><source media="(prefers-color-scheme: dark)" srcset="https://cursor.com/assets/images/open-in-web-dark.png"><source media="(prefers-color-scheme: light)" srcset="https://cursor.com/assets/images/open-in-web-light.png"><img alt="Open in Web" width="114" height="28" src="https://cursor.com/assets/images/open-in-web-dark.png"></picture></a>&nbsp;<a href="https://cursor.com/background-agent?bcId=bc-31f1aced-3b79-4e25-b3ef-6e8ff04b2644&cursor_ref=pr_footer&cursor_cta=open_in_cursor"><picture><source media="(prefers-color-scheme: dark)" srcset="https://cursor.com/assets/images/open-in-cursor-dark.png"><source media="(prefers-color-scheme: light)" srcset="https://cursor.com/assets/images/open-in-cursor-light.png"><img alt="Open in Cursor" width="131" height="28" src="https://cursor.com/assets/images/open-in-cursor-dark.png"></picture></a>&nbsp;</div>

