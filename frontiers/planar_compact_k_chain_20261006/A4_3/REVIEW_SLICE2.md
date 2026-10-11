**PASS** on QS addendum A4.3, Slice 2 only (§§4–5: the exhaustion at compact `K` and the consequences; §§6 and 8 for overclaim; controls Z6–Z8).

Dylan Roy — delegated AI review. Actual performer: xAI Grok 4.7 (`grok-4.7-high-fast`), Cursor cloud agent, session `bc-896b2b0f-affe-489a-85c7-c476c8971007`. Summoned by Anthropic Claude, session `session_01NMeKEismAyeqgdB4sy2NJU`, under D2 of [6002718035](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6002718035), after the window in [6010712951](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6010712951) (no OpenAI pickup by 06:54Z). Nonauthor of the note. Organizational-independence credit 0. Scientific effect NONE. Personal reading PENDING. No repository edit, no pull request, no timer.

Creating a comment and editing the Cursor acknowledgement [6011056566](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6011056566) both returned HTTP 403 (`Resource not accessible by integration`). The pickup was attempted first, naming the two body hashes below. This reply is the pickup and the verdict together.

**Frozen bodies, hashed before and after the read (served API `body`, UTF-8).** Both unchanged (`updated_at` still `2026-10-06T06:12:42Z` and `06:12:45Z`).
- Note [6010510789](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6010510789): 30,114 bytes, SHA-256 `271fbb20f2aa09f9fb70248aab2a0a40d96baeb744961fb00705a18f65b45bd7`.
- Controls [6010511425](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6010511425): 13,947 bytes, SHA-256 `dc1fe98402bc2bb5d8c7522a21576ec7239f92c36831295c1dc61f5343c32178`.
- Extracted `a43_exact.py`: 9,853 bytes, SHA-256 `a69c67ae66b966049eb8975e13922d427f3cf52f4659b536ac0f12c2349e1e78`. Stdout: 145 bytes, SHA-256 `3352a3105b27f7054dd94e443f573906f22acf3c22a5ed1cae74eb06da08a1e8`.

**Scope checked.** (4.1) and its domination sentence; Proposition 4.1 against C103 (S28) and A4.2 Theorem ER_K step 1; Theorem QFE″_K (the schedule, the eight closed forms and their thresholds, the two side conditions, FT_K at `Λ = r^{−α}`) against A4.1 Theorem QFE′_K; Theorem ER′_K against A4.2 Theorem ER_K, including the logarithm power; Corollary PD_ER′ against A4.2 §3 and Corollary PD §2; Remark 4 against C103 (S12) and C124 Theorem ER (3)–(4); §§6 and 8; controls Z6–Z8.

**Unchecked.** §§0–3 and Z1–Z5, which stay at the Slice 1 PASS [6010522535](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6010522535). C103’s derivation of (S8), (S28) and (S34), A4.1’s certificate, A4.2’s Lemmas JB_K–FT_K, and PD’s identities (o) and steps 1–3 were used as frozen inputs and were not re-proved.

**(4.1).** For `H ≥ 1`, each monomial of (3.1) and (3.2) is at most one term of (4.1). The three comparisons named after (4.1) are `H³r ≤ rH⁴`, `r^{3/2} ≤ r^{3/2}H⁵` and `r^{3/2}H⁴ ≤ r^{3/2}H⁵`. The remaining monomials already appear in (4.1), including `H⁵r^{3/2} = r^{3/2}H⁵`. Z6’s fourth comparison is the same product written as `rH³ ≤ rH⁴`.

**Proposition 4.1.** C103 (S28) is the pair `r^{−3}Q_r^W(D_Λ ∩ (H_r Δ E)) ≤ C·Rerr` and `‖ν_r^F|_{D_Λ} − ν_0^F|_{D_Λ}‖_var ≤ C·Rerr`. A4.2 step 1 puts `R_*^K` in that slot. Here (3.1), (3.2) and (S8)’s `C_KrH⁴` are majorized by `C_KR_*^{K″}`, and `r³/z_r ≤ 2r³/z_*` turns the `μ_r` bounds into the first line of (4.2). The second line is (S28)’s own second sentence: replace `1_{F_r}` by `1_{Rsec}`, add the off-`T` leakage, and use (S8)’s normalized density comparison, which is again the `rH⁴` term.

**Theorem QFE″_K.** The schedule is `α = (1−β)/8`, `Λ = r^{−α}`, `H ≤ 2r^{−α}` for `r ≤ 1`. The eight exponents are exactly the table:

| term | exponent | ≥ β on |
|---|---|---|
| `rH⁴` | `(1+β)/2` | `β ≤ 1` |
| `H²r log(1/r)` | `(3+β)/4` | `β < 1` |
| `H⁵r^{5/4}` | `5/8+5β/8` | `β ≤ 5/3` |
| `r^{3/2}H⁵` | `7/8+5β/8` | `β ≤ 7/3` |
| `r^{3/2}H⁴ log(1/r)` | `1+β/2` | `β < 2` |
| `H⁷r^{13/8}` | `3/4+7β/8` | `β ≤ 6` |
| `r^{7/4}H³` | `11/8+3β/8` | `β ≤ 11/5` |
| `r²H³ log(1/r)` | `13/8+3β/8` | `β < 13/5` |

For `β ∈ (0,1)` every power is at least `β`, and the three logarithmic ones are strictly above `β`, so each logarithm is absorbed. The side conditions are `rH/k_- ≤ 2r^{(7+β)/8}/k_-` and `C_VH²r^{1/4} ≤ 4C_Vr^{β/4}`. FT_K gives `ν_r^F(D_Λ^c)+ν_0^F(D_Λ^c) ≤ C_Ke^{−c_KΛ}+C_Kr`, hence `O(r)` at `Λ = r^{−α}`. Adding that tail to (4.2) yields `O(r^β)`. The mass line is (S2) and (S34): `|r^{−3}(1−p_r)−(α₁+α₂)| ≤ ‖ν_r^F−ν_0^F‖`, so the error is `O(r^{3+β})`. The conditional factor `4/M_*` from A4.2 step 5 preserves the rate.

**Theorem ER′_K.** With `Λ = D_K log(1/r)` large enough that both FT_K tails are `O(r)`, and `H ≤ (1+D_K)log(1/r)` for `r ≤ e^{−1}`, the ledger contributes `rH⁴ ≤ C_Kr log(1/r)⁴` and `H²r log(1/r) ≤ C_Kr log(1/r)³`. Every other term is `r^{1+a}` times a power of `log(1/r)` with `a ≥ 1/4`, hence `O(r)`. The power `4` is the power of `H` on the leading `rH⁴` term. The mass and conditional lines are again A4.2 step 5, and they carry this rate to `O(r⁴ log(1/r)⁴)`.

**Corollary PD_ER′.** PD’s conversion gives `r ≤ k_-^{−1/3}ℓ^{1/3}` and, once `k ≤ k_+ ≤ 1/ℓ`, `log(1/r) ≤ (2/3)log(1/ℓ)`. Thus `r log(1/r)⁴ ≤ (16/81) k_-^{−1/3} ℓ^{1/3} log(1/ℓ)⁴`. The `(A_r−A_0)` piece is `O(ℓ^{1/3})` and is absorbed for `log(1/ℓ) ≥ 1`, which is (i). The error integral `∫₀¹ s^{q+1}(1+log(1/s))⁴ ds = Σ_{j=0}^{4} C(4,j) j!/(q+2)^{j+1}` converges exactly for `q > −2`. The stated range `q > −5/3` is the main-term threshold, and on it the sum is at most `Σ C(4,j) j! 3^{j+1} = 8139`. At `q = 0` the sum is `21/4 < 6`, which is (ii). PD step 6 gives the fraction error `O(ℓ^{4/3} log(1/ℓ)⁴)`. Step 7 with (4.3) gives (v), with denominator `q+(5+β)/3 > β/3`, so `1/(q+(5+β)/3) ≤ 3/β`.

**Remark 4.** C103 (S12) at `k_- = k_+ = 1` is `K₀ = 167/192` and `K₂ = 115/48`. Then `η_K = 2K₂ rw² = (115/24)rw²` and `C_η = 5K₂/3 = 575/144`. C124 (3)–(4) are `r^{2/3}log(1/r)^{8/3}`, `r^{11/3}log(1/r)^{8/3}` and `r^{11/3}`; (4.4) and (3.3) replace them by `r log(1/r)⁴`, `r⁴ log(1/r)⁴` and `r⁴ log(1/r)`.

**§§6 and 8.** The binding terms are the margin sum `H²r log(1/r)` and the layer comparison `rH⁴`. Any `w_max = r^{−ω}` with `1/8 ≤ ω < 1/4` keeps the fixed layer and the endpoint, and a smaller positive `α` keeps `C_VH²e(w_J) → 0` together with the exponent table. The note claims no `k_- → 0`, no logarithm removal, and no power above `1` in `r`. The new rates are strictly stronger than A4.1’s `β < 2/3`, A4.2’s `r^{11/3}log^{8/3}` and C124 (3)–(4), while those statements are left unchanged.

**Controls.** `python3 -B -S` and `python3 -B -O -S` both exited 0 with byte-identical stdout, equal to the posted JSON line (`checks` 1835). Mutants M6, M7, M9 and M10 exited 1 in both modes, with identical stderr naming `Z6_exponent_tables`, `Z7_pd_constants`, `Z7_pd_constants` and `Z8_k1_constants`. `--bogus`, `--mutant M11`, a bare `--mutant`, and a stray argument exited 2.

Slice 2 is PASS. No amendment.



<div><a href="https://cursor.com/agents/bc-896b2b0f-affe-489a-85c7-c476c8971007?cursor_ref=pr_footer&cursor_cta=open_in_web"><picture><source media="(prefers-color-scheme: dark)" srcset="https://cursor.com/assets/images/open-in-web-dark.png"><source media="(prefers-color-scheme: light)" srcset="https://cursor.com/assets/images/open-in-web-light.png"><img alt="Open in Web" width="114" height="28" src="https://cursor.com/assets/images/open-in-web-dark.png"></picture></a>&nbsp;<a href="https://cursor.com/background-agent?bcId=bc-896b2b0f-affe-489a-85c7-c476c8971007&cursor_ref=pr_footer&cursor_cta=open_in_cursor"><picture><source media="(prefers-color-scheme: dark)" srcset="https://cursor.com/assets/images/open-in-cursor-dark.png"><source media="(prefers-color-scheme: light)" srcset="https://cursor.com/assets/images/open-in-cursor-light.png"><img alt="Open in Cursor" width="131" height="28" src="https://cursor.com/assets/images/open-in-cursor-dark.png"></picture></a>&nbsp;</div>

