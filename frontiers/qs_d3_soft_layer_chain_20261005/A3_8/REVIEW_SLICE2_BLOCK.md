**BLOCK** on QS addendum A3.8, Slice 2 (§§3–5). The frozen note [6007704303](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6007704303) (45,818 bytes, SHA-256 `afd2271252aa66c7e99f8fd7cb5ad194d881a56dcddcb9c726438f879b2c6451`) and controls [6007706590](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6007706590) (32,933 bytes, SHA-256 `c12bbbc241648bcf61850c3f134bddc5e02557f4f786ddc1433f358047fce88a`) match the summons. Lemmas 3.1–3.2, 4.1–4.2, 5.2–5.3, the series ES₃, and the model half of Lemma 5.4 check out. Lemma 5.1 does not: on depth failure, `λ̃ > Λ` is not forced into `{U ≥ (Λ/C_U)^{1/2}}`. The actual half of Lemma 5.4 uses that same threshold, so it falls with Lemma 5.1.

Dylan Roy — delegated AI review. Actual performer: xAI, Grok 4.7, Cursor cloud agent, run model `grok-4.7-high-fast`, session `bc-ea15a5c7-4714-4f97-9e0e-8a2ed0e4285f`. Provider-distinct from the author (Anthropic). Organizational-independence credit 0. Personal reading PENDING. Scientific effect NONE.

GitHub rejected the pickup and this verdict (HTTP 403, resource not accessible to the integration). No repository edit, pull request, timer, or loop was started. The author work claim [6005773306](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6005773306) stays released by the note.

## Why Lemma 5.1 is blocked

[P] is `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md`, blob `dfed3b8d318a3ab1950957f393307733a4bef3f2`. For `m = d − 1 = 2`, (4.3) gives `M₃ ≤ K₀(J_r + ‖A_M‖_F)` and `‖A_M‖_F ≤ √2 λ_max` on a definite 2×2 matrix, so the `K` in (7.1) is `√2 K₀^{[P]}`. Then

`D = 4K²/(3k₋) = 8 K₀^{[P]²}/(3k₋)`.

That constant, the containment `0 < λ₁ ≤ D r U²`, the powers in (7.2)–(7.4) (`r⁵ U^{10}` and the Vandermonde factor `λ_max` at `m = 2`), and (7.7) (`E[W_r 1{r M₄ > 3k/10}] ≤ C r⁶`, hence scaled mass `Cr` after `Z_r ≥ z_* r²/2` and `r^{-3}`) all match the note. `U = J_r + λ_max` is a function of the conditioned variables in (7.4) (`J_r` and `λ₂, …, λ_m`), so `{U ≥ A}` does pass through the `λ₁`-integration. The Markov exponent `2m` is the right one for `A = (Λ/C_U)^{1/2}`.

The step that fails is the passage from that pin bound to `λ̃`. The pins are `M = −(r/2)u` and `S = (r/2)u`, so the midpoint-to-pin distance `r/2` is right, and `‖D²_⊥f(0) − A_M‖_op ≤ (r/2) M₃` is the right Lipschitz bound. Weyl then controls **ordered** eigenvalues. The coordinate in A3.6 (0.1) is different: `Ψ` is diagonal in the eigenframe as `diag(r λ̃/k, λ₂)`, so `r λ̃/k` is one distinguished eigenvalue, and it may be the larger one.

- If `r λ̃/k` is the smaller midpoint eigenvalue, then `λ̃ ≤ k(D U² + K₀ U/√2) ≤ C_U U²` with `C_U = k₊(D + K₀)`, and `λ̃ > Λ` forces `U ≥ (Λ/C_U)^{1/2}`.
- If `r λ̃/k > λ₂`, the same Weyl bound only caps the smaller eigenvalue. The distinguished one satisfies `r λ̃/k ≤ λ_max(−A_M) + (r/2) M₃ = O(U)`, hence `λ̃ = O(U/r)`. Depth failure with `U` of order 1 is compatible with `λ̃ > Λ` whenever `rΛ` is small. A schematic point is `r = 10^{-6}`, `Λ = 10^3`, `U = 2`, midpoint eigenvalues `10^{-6}` and `10^{-2}`: then `λ̃ = 10^4 > Λ` while `U < (Λ/C_U)^{1/2}`.

The branch `λ̃ < −Λ` is fine. There `r λ̃/k < 0 ≤ λ_min(−A_M)` on the typed support of `W_r`, so the operator-norm gap really does give `M₃ > 2Λ/k` and `U > √2 Λ/(k₊ K₀)`. The comparison `√2 Λ/(k₊ K₀) ≥ (Λ/C_U)^{1/2}` for `Λ > C_U`, using `C_U ≥ k₊ K₀` and `k₊² K₀²/(2 C_U) ≤ C_U/2`, checks. For `Λ ≤ C_U` the bound is the trivial `U ≥ 1`. Z6 tests this arithmetic after granting `λ₁^{mid} = λ_min + (r/2) M₃`. It does not test the larger-eigenvalue branch.

Lemma 5.4’s actual tail replaces Markov by the exponential split at this same `A`. That half is unproved until `{λ̃ > Λ}` is put inside `{U ≥ A}` or bounded another way. I do not have a local replacement that restores `Λ^{-m}`.

## What did check

**Lemmas 3.1–3.2.** C82 Theorem LB (comment 5959920397, (3)) is the width-`≤ 1/2` bound `J_δ ≤ δ[(1024/3)|c|³ + 64 R²]`. A3.6 (1.1) and M₃(c) convert it to `x Ł₀` with `Ł₀ = (1/384)[(1024/3)|D|³ + 64 J²]`, and C82 §5 forbids swapping a wider band for `1/2`. Lemma 3.1(a) stays inside `δ ≤ 1/2`. Lemma 3.1(b) uses `λ₂ ≥ 2δ`, so the fibre width `δ/λ₂` is at most `1/2`. The `δ`-coefficient is `Ł₀`, free of `Λ`. The remainder `CrH⁶ · 2Λ` is at most `C r H⁷` because `2Λ ≤ 2H`.

Lemma 3.2 cuts the dyadic sum where C124’s DB does. For `δ < 1/4`, `j₀` is the last index with `2^{j₀+1} δ ≤ 1/2`, every shell fed to Lemma 3.1 has width at most `1/2`, and the tail `N > 2^{j₀+1} > 1/(4δ)` costs `16 δ² μ_r(N²) ≤ C H³ δ²`. For `δ ≥ 1/4`, `16 δ² ≥ 1` and (1.3) give the same `H³ δ²` term. For (3.2), shells with `λ₂ ≥ 2 · 4^{j+1} δ` again have fibre width at most `1/2`, and the complementary shells sit in `{λ₂ ≤ 8 δ N²}` because `2 · 4^{j+1} δ = 8 δ · 4^j` and `N² > 4^j` on that shell. Lemma 2.3 at width `8δ` supplies `H⁴ δ⁴ + r H⁸ δ²`. The series totals are `5`, `7/3`, `19/3`, and `31/15`.

**Lemmas 4.1–4.2.** A3.6 (1.2) is `c_* = 3/(250 A_*²) = 1/(12000 Λ²)` with `A_* = 12Λ`. Then `4K₀ e/c_* = 48000 K₀ Λ² e ≤ C_V H² e` with `C_V = 48000 max(K₀, C_e k₊)`, and the same for `ε′_V`. The splits at `d₁ = √ε` reproduce A3.6 steps 5 and 6 with `(H² s + r H⁷)` in place of `(s + r)`. The exact strip-plus-away totals are `H² ε + (4/3) r H⁷ √ε` and `(17/24) H² ε + (23/18) r H⁷ √ε`; the proof’s coarser `H² d₁²` versions are `(3/2)` and `(29/24)` and still give `C(H⁴ e + r H⁸ √e)`. Lemma 4.2 matches A3.7’s B₃: the strip is at most `H² η/2 + r H⁷ √η`, and `H ≥ 1` absorbs `H² η` into `H³ η`. Off the strip, `N(γ² + 72) > 4 η^{-1/2}` and `γ² + 72 ≤ 73 P²` give the factor `73² η/16` in front of `μ_r(N² P⁴) ≤ C H³`.

**Lemma 5.2.** The conic identity before C82 (15), `σ² − 1 = 4 ρ x`, comes from C82 (5) and does not use `|v| ≤ 1/2`. On `Rsec^{(∞)}`, `h_Y ∈ (0, 1)`, so `(σ − 1)² < 4 h_Y`, `|σ − 1| < 2√h_Y < 2`, and `x = h_Y + (σ − 1)/2 < 2`. For `ψ ≥ 4|c|`, `|1 − ρ σ| > 1/4`, and C82’s line equation `R² = 16 ψ³ (1 − ρ σ)²/x` gives `ψ³ < 2 R²`. Otherwise `ψ³ < 64 |c|³`. The fibre bound uses A3.6 (1.1): `(γ⁶/384) · (ψ_max³)/3 = (64 |D|³ + 2 J²)/1152`, since `384 · 3 = 1152`, `γ⁶ |c|³ = |D|³` and `γ⁶ R² = J²`. Then `λ̃ = γ² ψ/24 ≤ (4|D| + 2^{1/3}|J|^{2/3})/24`, and `2^{1/3} ≤ 13/10 < 4` gives `λ̃ ≤ (|D| + |J|^{2/3})/6`.

**Lemma 5.3 and the model half of 5.4.** `∫ 1_{Rsec^{(∞)}} w_λ dλ̃ ≤ C P⁶` from the fibre bound and A3.6’s proof of M₃(e) (`|D| ≤ (1 + 24 k₊) P²`, `|J| ≤ (8 + 288 k₊ + 1152 k₊²) P³`), which does not use the layer cut. So `λ̃ > Λ` forces `P² ≥ Λ/C`, and Gaussian moments of `P` give `Λ^{-m}`. The coefficient lives on `Rsec^{(∞)}`, not on the `Λ`-cut `Rsec`. The lower bound is A3.6 BL₃(a) at `Λ = 1`: the rejected witness has `λ̃ = 1/2` and `μ = 1/2`, so `m_R^{(∞)} ≥ m_R(1) > 0`, and `z₀ ≤ z^*` gives `α^{(3)}` bounded above and below. The model exponential tail is the same integral with the Gaussian envelope. I did not re-prove that envelope (A3.4).

**ES₃.** [P] §2 and §4 give conditional Fourier variances at most 1 and `S = Σ √a_n ‖φ_n‖_{C⁴} < ∞` for `q = 4`. `‖Z‖_{L^{2n}} ≤ √(2n)` because `E Z^{2n} = (2n−1)!! ≤ (2n)^n`. Then `(2n)^n/n! ≤ (2e)^n` and `ε₀ = 1/(12(1+S)²)` make the ratio `e/6 < 1/2`, so the exponential series is at most 2. Z6 checks the factorial bound through `n = 60` with `e` bracketed by `27182/10000` and `27183/10000`; the same Stirling comparison covers every `n`.

## Controls

Script `a38_exact.py`, 28,557 bytes, SHA-256 `f5b32f603bbb4a0847d8299d02a0a49a6e7930b5eb93b4dc02761666e24d4faf`, extracted as the first Python fence. `python3 -B -S` and `python3 -B -O -S` both exited 0 with byte-identical stdout, 525 bytes, SHA-256 `11f3b6a37d0dd2cb7a1f741f9cd2091066cb4fa01454a864551a95b45ca22c6a`. Z3 branch counts: inner band 994, shell 504, wide tail 715, trivial range 400, outside 787; (3.2) first band 211, band shells 1483, strip 502, outside 804. In both modes, M4 and M5 exit 1 naming `Z3_MB3_coverings`, M8 and M9 naming `Z5_PQS_facts`, and M10, M11, and M13 naming `Z6_tails_algebra`, with byte-identical stderr. `--bogus`, `--mutant M14`, and a bare `--mutant` exit 2. Z6’s pass does not cover the blocked eigenvalue identification.

## Not checked

§§1–2 and §6, including the ledger, Proposition 6.1, Theorems QFE₃ and ER₃, and the mathematics of Z1, Z2, Z4, and Z7. Those groups ran inside the same executable and reported full pass counts; that is not a read of them. A3.4’s Gaussian envelope, A3.7’s open band and theorem slices, and C82’s coarea proof beyond the identities cited above were used as stated inputs. Same-session referee passes in the note’s §8 were not treated as review evidence.



<div><a href="https://cursor.com/agents/bc-ea15a5c7-4714-4f97-9e0e-8a2ed0e4285f?cursor_ref=pr_footer&cursor_cta=open_in_web"><picture><source media="(prefers-color-scheme: dark)" srcset="https://cursor.com/assets/images/open-in-web-dark.png"><source media="(prefers-color-scheme: light)" srcset="https://cursor.com/assets/images/open-in-web-light.png"><img alt="Open in Web" width="114" height="28" src="https://cursor.com/assets/images/open-in-web-dark.png"></picture></a>&nbsp;<a href="https://cursor.com/background-agent?bcId=bc-ea15a5c7-4714-4f97-9e0e-8a2ed0e4285f&cursor_ref=pr_footer&cursor_cta=open_in_cursor"><picture><source media="(prefers-color-scheme: dark)" srcset="https://cursor.com/assets/images/open-in-cursor-dark.png"><source media="(prefers-color-scheme: light)" srcset="https://cursor.com/assets/images/open-in-cursor-light.png"><img alt="Open in Cursor" width="131" height="28" src="https://cursor.com/assets/images/open-in-cursor-dark.png"></picture></a>&nbsp;</div>

