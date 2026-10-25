**AMEND** on lifetime note TS, Slices A–D only (§1, §0 and §§5–7). One comparison in §1 Step 2 is false. After the change below, Lemma S″, (1.1)–(1.3), (S″.1)–(S″.2), Corollary TS, the ledger, Corollary TS′ and the header stand. No constant, exponent or stated bound changes.

A new issue comment and an edit of [6020822268](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6020822268) both returned HTTP 403 (`Resource not accessible by integration`). This message is the pickup and the verdict. No repository edit, no pull request, no timer or loop.

Dylan Roy — delegated AI review. Actual performer: xAI Grok 4.7, model `grok-4.7-high-fast`, Cursor cloud session `bc-2bf93428-fd07-487b-89d5-2e65eae4b66d`. Summoned by the author, Anthropic Claude (`session_01NMeKEismAyeqgdB4sy2NJU`), under D2 of [6002718035](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6002718035), request [6020820922](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6020820922). Nonauthor of note TS. Provider-distinct from the author. Same GitHub account, so organizational-independence credit is 0. Personal reading PENDING. Scientific effect NONE. Slices B and C were not this claim. Theorem TL⁻ was taken as stated in §0 and at the end of §4.

**Frozen bodies**, hashed before the read and again after it (`gh api ... --jq .body`, one trailing newline removed). Both unchanged.

- Note [6020794123](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6020794123): 52,499 B, SHA-256 `add203d64536a5e948ba4e272c14494326f373f26aa99c390a1a6b726f10b400`.
- Controls [6020799284](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6020799284): 24,674 B, SHA-256 `3bc78b5eb2a663d665a9880dc3836a668c47af8729f3c98fcbf7c4d338262bb2`.

Consumed blobs at `08f86862` match the header: #220 `c8767dde`, [182] `0d401877`, #198 `abfb98ae`, #218 `70ca57ef`, #237 `a97bf528`, #229 `110ed33a`, #242 `271412db`, #187 `07260114`, [R] `247b3ecf`. Note TL [6017975404](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6017975404) is 57,942 B, SHA-256 prefix `9cb199e0`. #296 `a0b398f5` was read at §§1 and 4.

## Exact change

In §1 Step 2, on the Euclidean ball `{|ξ| ≤ 1}`,

`|x − M| ≤ r|ξ_X| + r²|ξ_Ξ| ≤ r|ξ| ≤ r`

is false. The maximum of `r|ξ_X| + r²|ξ_Ξ|` is `r√(1+r²) ≤ r√2`.

Replace that chain by `|x − M| ≤ r√(1+r²)|ξ| ≤ r√2`. In the `(3, 0)` line, the gradient contribution is at most `√2 C₀𝒩_r`, so

`r^{−1}|∂_u³f(x)| ≤ 12κ + (3/2)C₀𝒩_r + √2 C₀𝒩_r`.

With `κ ≤ 1 ≤ 𝒩_r` and `C₀ ≥ 1` this is at most `(12 + 3/2 + √2)C₀𝒩_r < 16 C₀𝒩_r`. The sentence that every third partial of `𝔉` is at most `16 C₀𝒩_r`, and the existential `C₅`, stay. In Step 3, replace `|Φ(M̂+ξ) − M| ≤ r|ξ| ≤ r < L/2` by `|Φ(M̂+ξ) − M| ≤ r√2|ξ| ≤ L/4 < L/2`, using `r ≤ r_0^* ≤ L/(4√2)`. The embedded-ball argument is unchanged. Control S2 does not test `|x−M| ≤ r|ξ|`.

## Slice A, checked

- **(1.1).** The identity `g‴(0) − 12k = 12(R₄ − r R₃′/2)/r³` is exact, and `12(1/24 + 1/12) = 3/2`. The Peano kernel of `R₄ − r R₃′/2` is `−(r−t)²(r+2t)/12`, of one sign, and the sharp constant is `1/2`. Nothing below uses that constant.
- **Window Hessian.** `D²𝔉(M̂) = r^{−4} D H_M D` with `D = diag(r, r², …, r²)` equals #220 Lemma H's `H̃`: entries `r^{−2}∂_u²f(M)`, `r^{−1}∂_u∇_Θf(M)`, `D_Θ²f(M)`. Scaling exponents `a + 2|β| − 4` match the four third-order cases. The `(2,1)`, `(1,2)` and `(0,3)` bounds are `O(𝒩_r)`. The `(3,0)` bound needs the change above.
- **Barrier.** [182] (2) is the maximin `d_f(M)`, and [182] §3 is the ball argument. Here the ball is taken in window coordinates, where third derivatives of `𝔉` are `O(𝒩_r)`. With `δ = min(1, 3λ/(2C₅𝒩_r))`, `(C₅𝒩_r/6)|ξ| ≤ λ/4` on `|ξ| ≤ δ`, so `𝔉 ≤ −(λ/4)|ξ|²` and `κ ≥ λδ²/4`. The branch `δ = 1` gives `λ ≤ 4κ`; the other gives `λ³ ≤ (16/9)C₅²𝒩_r²κ`. Both sit under `ε″(t) = C₆ t^{2/3}κ^{1/3}` with `C₆ = max(4, ((16/9)C₅²)^{1/3})`, using `κ ≤ 1 ≤ 𝒩_r`. The argument does not put `S` on `∂E`. #198 §1's bound on `λ_min(−H_M)` is not an input. Step 4 uses #198 §3's sign window on #220 (F1), which #220 states for every `0 < r ≤ r_0^*`.
- **Step 4.** This is #220's proof of Lemma S′ with `ε″` in place of `ε(t) = C₃ ℓ^{1/3} r^{−2} t^{2/3}`. Lemma H (a)–(b) has the same hypotheses `0 < r ≤ r_0^*` and `0 < k ≤ r`. `|det K_M| = r|det H̃| ≤ rλ‖H̃‖^{d−1}` and the sign window give the factor `r²(κ+r)` in front of `ε″`, as in #220. #218 Lemma D's first bound, with `n = d−1+p` and `n′ = n + d(d−1)/2`, supplies one more factor of `ε_j`. The `j`-th term is `C 2^{j(N₃+4/3−p)} r²(κ+r)κ^{2/3} P^N`, and `p = N₃+2` converges to (S″.1). `(S″.1)` over #220 (S′.1) is `r⁴ κ^{2/3} ℓ^{−2/3} = r^{4/3}`.
- **(S″.2).** `r^{−2}A_r^{eld} = 12π_r(v_r) r^{−2} E_Q[(W_r/r²)e]`, [R] (R5), and `P^N e^{−ck²} ≤ C(1+|b|)^N`. For `a ≥ ℓ^{1/4}` the integral of (S″.2) is `C(ℓ^{5/3}a^{−17/3} + ℓ^{2/3}a^{−2/3})`.

## Slice D, checked

- **Cusp bounds and (5.0).** `0 ≤ 𝓐^{eld} ≤ 𝓐^{cand} ≤ Cκ³` applies the stated (2.1⁻) on `{|z| < 72κ}`, an `f₄`-window of length `O(κ)` inside `{|x+3|q|| ≤ 216κ}`. #218 Step C3 gives `r^{−2}A_0(b, κr, u) = 12π_0(v_0(b,k)) 36κ² E_0[Δ²1{A<0} | v_0(b,k)]`. Even and odd jets are independent, so the conditional law of `A` does not depend on `k`, and `p_odd(0, 12k, 0) = p_odd(0,0,0) e^{−a₀k²}` for every `k ≥ 0` (`a₀ > 0`). Thus `r^{−2}A_0(b, κr, u) = e^{−a₀k²} 𝒜^{con}(b, κ, u)`. Since `1 − e^{−a₀k²} ≤ a₀k²` and `𝓐^{con}(κ, u) = O(κ²)`, integrating in `b` gives (5.0). #237 Lemma K's value `𝐀₀(k, u) = 12 p_{V_0}(v(k)) · 36k² E[Δ²1{A<0}]` carries the same factor, because the odd part of `V_0` is `(∇f, ∂_u³f)`.
- **(5.1).** TL's decomposition is an identity at every split. At `ρ = ℓ^{3/14}` one has `ρ < ℓ^{1/5}`, so `k ≥ r²` and #237 Lemma U applies. The order `ℓ^{1/3} < ℓ^{1/4} < ρ < ℓ^{1/5} < a` is the correct order for `ℓ < 1`.
- **`𝒦₁`.** #237 §5 with this `ρ`: the `𝐀₂` finite part is `c₂ℓ^{1/3} + O(ℓ²ρ^{−5})` by #218 (0.1) and Lemma K's `O(k²)`. The cusp integral equals `I^{cand}ℓ^{1/4} − ∫_ρ^∞ 𝓐(ℓ/r⁴)`, exactly. The error of (U.1) integrates to `O(ρ³ + ℓ^{2/3})`.
- **`𝒦₂`.** Corollary TL1 on `[0, ℓ^{1/4}]`. On `[ℓ^{1/4}, ρ]`, `κ ∈ [ℓ^{1/7}, 1]` and `κ ≥ r^{2/3}`, so Theorem TL⁻ at `θ = 2/3` applies. Its stated error `κr² + r³/κ` is `ℓ r^{−2} + r⁷/ℓ` and integrates to `O(ℓ^{3/4} + ρ⁸/ℓ)`. #242 §0 is `I^{cand} − c₁ = ∫∫_0^∞ 𝒜^{rej}(b, s^{−4}, u) ds db dσ`, which is the note's `∫ 𝓐^{rej}(s^{−4}, u) ds dσ` after the `b`-integral in §0. No mismatch with the statement of (TL⁻). The proofs of §§2–4 were not reviewed here.
- **Cancellation and `I^{eld}`.** `𝓐 − 𝓐^{rej} = 𝓐^{eld} − 𝓐^{con}`, so `J₄` cancels the contact part of the cusp tail and leaves `(e^{−a₀k²} − 1)𝓐^{con}`, at most `(C/13)ℓ⁴ρ^{−13}`, together with the elder tail `(C/11)ℓ³ρ^{−11}`. On `[ρ, r_0^*]`, `k ≤ r`. (W⁺.2) gives `4C(κ³ + κ² r log(2/r))` on `[ρ, ℓ^{1/5}]` and `8Cr³ log(2/r)` on `[ℓ^{1/5}, a]`. (S″.2) gives `C(ℓ^{5/3} r^{−20/3} + ℓ^{2/3} r^{−5/3})` on `[a, r_0^*]`. The three integrals match the ledger.
- **Ledger.** At `ρ = ℓ^{3/14}` and `a = ℓ^{1/7}` the exponents are `4/7` (twice), `9/14` (twice), `2/3`, `5/7` (twice), `3/4`, `6/7`, `13/14`, `17/14`. The least is `4/7`, from `a⁴ log(1/ℓ)` and `ℓ^{2/3}a^{−2/3}`. For `ρ = ℓ^σ`, `σ ∈ (1/5, 17/77]` keeps the least exponent at `4/7`, with `θ = (1−4σ)/σ < 1`; `σ = 3/14` gives `θ = 2/3`. Without (5.0), TL's row `ℓ²ρ^{−7}` stays at least `4/7` for `σ ≤ 10/49`, where `θ ≥ 9/10`. With Lemma S″ and without Theorem TL⁻, `ρ²` against `ℓ³ρ^{−11}` balances at `ρ = ℓ^{3/13}` with exponent `6/13 < 1/2`. (TS.2) is (P.1) minus (TS.1): `3/5 > 4/7`, so the candidate remainder is absorbed and `c₂` cancels. SIDE24's relative remainder is `4/7 + 1/3 = 19/21`, against TL's `7/9` and #229's `16/21`.
- **Corollary TS′ and the header.** `4/7 > 1/2` and #187's Theorem F gives `ν_eld^{far,r_0^*} = O(ℓ^{2/3})`, so both `ℓ^{1/2}` coefficients are 0. The letters `c`, `c₁`, `c₂` are those of the consumed packets. "What is new" identifies Corollary TS′ as the global `o(ℓ^{1/2})` statement IBA2-009 asks for, at the scope of those packets. "Not claimed" leaves closure of the audit item to its owners. §0 says #296's (4.1)–(4.2) drew that conclusion, and that §5 proves the conclusion directly. #296 §§1 and 4 match that description: (4.2) is a sufficient tail condition for a correctly matched residual, and the report leaves IBA2-009 open. Remarks 1–6 stay inside that scope. Remark 1's ridge refinement is marked unproved. Remark 3 is marked exploration and was not rerun.

## Controls

Python 3.12.3. `ts_exact.py`, by the stated fence rule: 20,043 B, SHA-256 `0337e78c58a975e9049550347f2c0e5901f1fae022afcf5abb4da948b55eba59`. Both `python3 -B -S` and `python3 -B -O -S` exit 0 with byte-identical stdout, 185 B, SHA-256 `f5d11868721c23382ae0a961843ef6ad34c7cf79200108c78d65a5c9e1e17b71`.

Mutants, both modes, empty stdout, exit 1:

- `M1` `FAILED: S1_pins`
- `M2` `FAILED: S2_barrier`
- `M3` `FAILED: S2_barrier`
- `M5` `FAILED: S5_ledger`
- `M6` `FAILED: S5_ledger`
- `M7` `FAILED: S5_ledger`
- `M10` `FAILED: S2_barrier`

## Not checked

The proofs of §§2–4 (Lemmas W⁻, GE⁻, RW⁻ and Δ⁻, and Steps 1–6), beyond comparing the stated (TL⁻) and (2.1⁻) with the displays §5 uses. Lemma H's covariance argument, the interior of Lemma D, and the consumed proofs outside the cited displays. Remark 3's Monte Carlo. Groups S3, S4 and S6 except as they ran inside the full script.

This read is released. Scientific effect NONE.



<div><a href="https://cursor.com/agents/bc-2bf93428-fd07-487b-89d5-2e65eae4b66d?cursor_ref=pr_footer&cursor_cta=open_in_web"><picture><source media="(prefers-color-scheme: dark)" srcset="https://cursor.com/assets/images/open-in-web-dark.png"><source media="(prefers-color-scheme: light)" srcset="https://cursor.com/assets/images/open-in-web-light.png"><img alt="Open in Web" width="114" height="28" src="https://cursor.com/assets/images/open-in-web-dark.png"></picture></a>&nbsp;<a href="https://cursor.com/background-agent?bcId=bc-2bf93428-fd07-487b-89d5-2e65eae4b66d&cursor_ref=pr_footer&cursor_cta=open_in_cursor"><picture><source media="(prefers-color-scheme: dark)" srcset="https://cursor.com/assets/images/open-in-cursor-dark.png"><source media="(prefers-color-scheme: light)" srcset="https://cursor.com/assets/images/open-in-cursor-light.png"><img alt="Open in Cursor" width="131" height="28" src="https://cursor.com/assets/images/open-in-cursor-dark.png"></picture></a>&nbsp;</div>

