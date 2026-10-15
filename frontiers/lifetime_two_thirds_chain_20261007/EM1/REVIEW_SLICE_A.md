**PASS** on Slice A of lifetime addendum EM.1 (§§0–1 and §2 (a)–(c)). GitHub refused both a new comment and an edit of the pickup [6024106995](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6024106995) with HTTP 403, so the pickup and the verdict are recorded here.

**Pickup.** D2 of [6002718035](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6002718035). One nonauthor read of Slice A only, summoned by [6024105685](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6024105685). Slice B is not claimed. Read only. Frozen bodies, hashed before the read (`gh api … --jq .body`, one trailing newline removed):

- Addendum [6024077582](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6024077582): 20,844 B, SHA-256 `e2b73535aec78c812b22548115e5e52032ebf4725af7a6d6c8dd16925bc11c91`.
- Controls [6024090900](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6024090900): 18,607 B, SHA-256 `7d535deecb1f67d9c5a7cc513ea577b59bd028b1bff1e47e112d255217a0bda6`.

**After the read,** the same API calls return the same lengths and both SHA-256 values. `updated_at` equals `created_at` on both comments.

**Lemma V′.** In note EM §3, `Y < 0` if and only if `K > 0` and `a > yᵀK⁻¹y`, so `{K > 0, s_Y > 0} = {Y < 0}`. On `B_R` the event sits in one shell, and (L1) gives `β_i² < R μ_i`. The `K`-measure is at most `CR^N x` by (L0). Only `β₁` is cut down, to length `2(2Rx)^{1/2}`, so the `y`-measure is at most `2(2Rx)^{1/2}(2R)^{m−1}`. Given `(y, K)`, `{0 < s_Y < ε}` is an `a`-interval of length `ε`. The weight contributes another `ε · 2x`. The product is `CR^{N′} ε² x^{5/2}`: the `x`-powers are `1 + 1/2 + 1`. EM §3’s Gaussian transfer applies with `ε` and `x` independent of the annulus, and gives (V.4).

**(2.1).** On a typed pair, `H̃ < 0`, so `D < 0` and `s > 0`. Then `τ = (−D)⁻¹β̃` and `|τ|² = β̃ᵀ(−D)⁻²β̃`. For each eigenvalue `λ ≥ μ`, `1/λ² ≤ 1/(μλ)`, so `|τ|² ≤ q_D/μ`. From `s = −ã − q_D > 0`, `q_D < −ã`, hence `|τ|² ≤ q_D/μ < −ã/μ`. #220 Lemma H at `665f744a` (blob `c8767dde…`) gives `ã = −6κ + ∫₀¹ s(1−s)² ∂_u⁴f(M+rsu) ds`, and `∫ s(1−s)² ds = 1/12`, so `|ã| ≤ 6κ + 𝒩̄/12`. With `κ ≤ 1 ≤ 𝒩̄` this is at most `7𝒩̄`, and `|τ|² < 7𝒩̄/μ`. Thus `r|τ| ≤ 1` once `μ ≥ 7𝒩̄ r²`. The addendum’s range `k ≤ r²` and `r ≤ r_* ≤ r_Q ≤ 1/10` sits inside Lemma H’s `k ≤ r`.

**(2.2).** The chain rule in EM §0 splits `α = D³𝔉(M̂)[(1, τ)^{⊗3}]` into `r⁻¹∂_u³f(M)`, `3∂_u²∇_Θf(M)·τ`, `3r ∂_u D_Θ²f(M)[τ,τ]` and `r² D_Θ³f(M)[τ^{⊗3}]`. (P.2) gives `|r⁻¹∂_u³f(M)| ≤ 12κ + |f₄|/2 + (13/80)𝒩̄ r`. With `κ ≤ 1`, `|f₄| ≤ 𝒩̄` and `r ≤ 1`, the sum is `(1013/80)𝒩̄ ≤ 13𝒩̄`. The other three terms are at most `3𝒩̄|τ|`, `3𝒩̄ r|τ|²` and `𝒩̄ r²|τ|³`, by the order-3 directional bound and the gradient bound on derivatives of order at most 8. On `{μ ≥ 7𝒩̄ r²}`, `r|τ| ≤ 1`, so the parenthesis is at most 7, and `|α| ≤ 13𝒩̄ + 7𝒩̄(7𝒩̄/μ)^{1/2}`. Since `7√7 < 19` (`343 < 361`) and `13𝒩̄ ≤ 19𝒩̄^{3/2}` for `𝒩̄ ≥ 1`, this is at most `T = 19𝒩̄^{3/2}(1 + μ⁻¹/²)`.

**§2 (c).** On `ℬ₁`, `μ ≥ μ₀(𝒩)` supplies both `μ ≥ 7𝒩̄ r²` and `μ ≥ 4𝒩̄ r^{4/3}κ^{1/3}`.

- `r|τ| ≤ 1` by (2.1).
- `κ/μ ≤ 1/(7r)`, so `2r²(κ/μ)^{1/2} ≤ (2/√7) r^{3/2} ≤ r^{3/2}`. The choice of `r_*` gives `r + r^{3/2} ≤ L/4`.
- `μ³ ≥ 64𝒩̄³ r⁴κ`, and `64𝒩̄ ≥ 256/9` once `𝒩̄ ≥ 1`, so `μ³ ≥ (256/9)𝒩̄² r⁴κ`.
- `μ² ≥ 49𝒩̄² r⁴`, and `49𝒩̄ ≥ (64/3)κ` once `κ ≤ 1 ≤ 𝒩̄`, so `μ² ≥ (64/3)𝒩̄ r⁴κ`.

Lemma X’s setting (critical `M̂`, value 0, gap `κ`, `H̃ < 0`) is the pinned typed pair. Each of (X.0)’s five terms is at most `1024𝒩̄² ε_ℬ`: the cubic term is at most `22𝒩̄ κ^{1/3}(1+μ⁻¹/³)` because `(256/9)·19² = 92416/9 ≤ 22³` and `(1+y)^{2/3} ≤ 1+y^{2/3}`; `((1024/3)𝒩̄ κ)^{1/2} ≤ 18.5 𝒩̄ (κ/μ)^{1/2}` because `1024/3 ≤ (37/2)²` and `μ ≤ ‖D‖ ≤ 𝒩̄`; then `64𝒩̄(κ/μ)^{1/2}`, `1024𝒩̄² r²κ/μ²` and `16κ`. So on `ℬ₁ ∩ {e = 1}` one has `0 < s < 1024𝒩̄² ε_ℬ`. For the weight, #220 §0 states `W_r/r² = F_d(K_M)F_{d−1}(K_S)`; EM §4.1 (e) identifies that product on typed pairs with `|det K_M||det K_S|` and gives `|det K_M| = rs|det D| ≤ rsμ 𝒩̄^{m−1}`. Note TS §1 Step 4, unchanged by [6021299833](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6021299833), gives `|det K_S| ≤ Cr(κ+r)𝒩^{N₃}`. The product is (2.4). EM’s successor [6023434026](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6023434026) changes only the clause after (4.4); this slice uses (P.2), not that clause.

**Controls.** Extracted `em1_exact.py` is 12,720 B, SHA-256 `80d3f0452732ab6eceb48ce63baaed35f6cc6336417719bb55d1820aaa55e8bb`. Python 3.12.3, `python3 -B -S` and `python3 -B -O -S`: exit 0, stdout 162 B, SHA-256 `50001f8a77a3babe1d3b93f311f111b715eafcdbe0b2ec5d42ea322faa3bffa8`, byte-identical (`B1_tau` 4446, `B2_cubic` 4909, `B3_threshold` 4304, total 13691). Mutants M1, M2, M7 and M8, both modes: exit 1, empty stdout, stderr `FAILED: B1_tau`, `FAILED: B2_cubic`, `FAILED: B1_tau` and `FAILED: B3_threshold`.

**Not checked.** §2 (d)–(e), §§3–4, the header, and the mathematics of B4–B5 and M3–M6. The full script was executed so the stdout hash could be compared; that is not a review of those groups. Lemma X, (L0)–(L1) and [R] §4 were used as stated in the consumed notes, not re-proved. No statement of note EM or note TS is changed. Scientific effect NONE.

**Disclosure.** Cursor cloud agent `bc-2a80b870-60c0-47e3-bddf-0658818fdd1e`, xAI Grok 4.7 (`grok-4.7-high-fast`), for Dylan Roy (delegated AI review). Author: Anthropic Claude, session `session_01NMeKEismAyeqgdB4sy2NJU`. Shared GitHub account; organizational-independence credit 0. Dylan’s personal reading is pending.



<div><a href="https://cursor.com/agents/bc-2a80b870-60c0-47e3-bddf-0658818fdd1e?cursor_ref=pr_footer&cursor_cta=open_in_web"><picture><source media="(prefers-color-scheme: dark)" srcset="https://cursor.com/assets/images/open-in-web-dark.png"><source media="(prefers-color-scheme: light)" srcset="https://cursor.com/assets/images/open-in-web-light.png"><img alt="Open in Web" width="114" height="28" src="https://cursor.com/assets/images/open-in-web-dark.png"></picture></a>&nbsp;<a href="https://cursor.com/background-agent?bcId=bc-2a80b870-60c0-47e3-bddf-0658818fdd1e&cursor_ref=pr_footer&cursor_cta=open_in_cursor"><picture><source media="(prefers-color-scheme: dark)" srcset="https://cursor.com/assets/images/open-in-cursor-dark.png"><source media="(prefers-color-scheme: light)" srcset="https://cursor.com/assets/images/open-in-cursor-light.png"><img alt="Open in Cursor" width="131" height="28" src="https://cursor.com/assets/images/open-in-cursor-dark.png"></picture></a>&nbsp;</div>

