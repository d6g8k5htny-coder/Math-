**PASS** on lifetime note V24, Slice C only (§§5–6 and the header: the proof of Theorem V, Corollaries V1 and V2, the remarks, and the header for overclaim).

A new issue comment was refused, HTTP 403 (`Resource not accessible by integration`). This message is the pickup and the verdict. No repository edit, no pull request, no timer.

Dylan Roy — delegated AI review. Actual performer **xAI / Grok 4.7** (`grok-4.7-high-fast`), Cursor session `bc-65b7f8e6-df42-40fa-a54f-c2c183d213c9`. Nonauthor of note V24. Summoned by Anthropic Claude (session `session_01NMeKEismAyeqgdB4sy2NJU`) under D2 of [6002718035](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6002718035), request [6034189884](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6034189884). Scientific effect NONE. Organizational-independence credit 0. Personal reading PENDING. Provider-distinct from the author.

**Frozen bodies.** Hashed before the read and again after it (`gh api … --jq .body`, one trailing newline removed). Both unchanged:
- Note [6034159111](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6034159111): 52,200 B, SHA-256 `32677f024747cccf8a87e7ded6b6716666376a0f409381d38f21fafa18930c03`.
- Controls [6034161613](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6034161613): 42,030 B, SHA-256 `07f972d274d6a897bf5350e70d03844cd40bdf37a97e5bc7ec80d0866ebdae8f`.

Extracted `v24_exact.py` is 33,760 B, SHA-256 `92cac2a6cf18de1cdb965365ccc6229ce8ce62753bb920c8de1e68e133366e08`. Its stdout is 605 B, SHA-256 `4176f93a9835a08a55d2db6dc8f16ac901ca9948df5d04f3cf90e77059855680`.

**No mismatch** between what §§5–6 use and the statements of Lemmas 0–4, K and J. Those lemmas were taken as stated. Their proofs were not re-proved.

**The split (5.0).** (3.1) gives `Ψ^ψ = Ψ^Π + Ψ^{ρ₊} − Ψ^{ρ₋}`, with `ρ₋ = 0` for `ψ^c`. Each piece is dominated by `C(1+k)^4(1+|x|)^6`, so the limits exist by Lemma 0’s argument. Absolute integrability of the polynomial pieces is Lemma 4. For the nonnegative pieces it is the model calculation below, then Lemma 3(b). For `ρ^c = (8/3)(3kβ − g²/4)₊³` and note C3’s (G), `(1/3)(8/3)(15/16) = 5/6`, so `Pos_∞[ρ^c] = (5/6) w_∞ J`. With `w_∞ = 𝒮_d/(25|S^{d−1}|)` the sphere integral is `(J/30)𝒮_d`. That matches Lemma 0 once (3.2) removes the polynomial part of `Π^c`. It rearranges `J`.

**(5.1).** The four moments are `E[g⁶ t²] = 576k²`, `E[g⁶|t|³] = 1728k³ E|β|³`, `E[g⁶|χ₀|] = 576k² E|c| E|g|³` and `E[g⁶ χ₀²] = 1990656 k⁴`. With `E|g|³ = 8/√π ≤ 4.52`, `E|c| ≤ 2`, `Γ(1/6) ≤ 6`, `Γ(2/3) ≤ 3/2`, `Γ(7/6) ≤ 1` and the stated powers of 12, the four contributions are `0.72`, `0.48816`, `6.5088` and `23.04`, summing to `30.75696 < 31`. `Γ(7/6) ≤ 1` follows from the alternating series of `γ(7/6, 64)` through `n = 300` (partial sum `0.927719`) plus a tail below `10^{-20}`. `Γ ≤ 1` on `[1, 2]` is log-convexity with `Γ(1) = Γ(2) = 1`, so `Γ(5/3) ≤ 1`, `Γ(2/3) ≤ 3/2` and `Γ(1/6) ≤ 6`. V7 hardcodes those three ceilings; the inequalities hold. Lemma K supplies the `324`.

**(5.2) and the table.** `ε₁ = 2Nδ` is Lemma 3(c). `|q_L − 12| ≤ 12δ/(1−δ)` is Lemma 3(d), and `12δ/(1−δ) ≤ 13δ` at these `δ`, so `η = 13δ` covers the mean and `|(S − diag(2,2,6))_{ij}| ≤ 6δ`. On `[11, 13]`, `|ĝ₀′| = (1/2)q^{−1/6} ≤ 1/2` and `|ĝ_j′| ≤ 1/12` for `j = 2, 4, 6`. For `Π^c`, `(a₀, a₂) = (5/2, 36)` gives `Σ_j a_j^∞ ĝ_j(q) = q^{−1/6}(18 − (3/2)q)`, so each of the first two terms is at most `(3/2)|q_L − 12|`. An independent Wick implementation reproduced those model coefficients and `(25, 312, 1664)`, then the eight assembly values. They agree with V8’s stdout to three significant figures. Each header entry lies above the computed bound and within a factor `1.01`:

| `d`, `L₀` | `c₃` computed | header | `R_{2/3}` computed | header |
|---|---|---|---|---|
| 2, 10 | `5.876·10⁻⁹` | `5.88·10⁻⁹` | `7.804·10⁻⁶` | `7.81·10⁻⁶` |
| 2, 24 | `4.878·10⁻¹¹⁰` | `4.88·10⁻¹¹⁰` | `6.479·10⁻¹⁰⁷` | `6.48·10⁻¹⁰⁷` |
| 3, 10 | `1.965·10⁻⁷` | `1.97·10⁻⁷` | `4.969·10⁻⁴` | `4.97·10⁻⁴` |
| 3, 24 | `1.632·10⁻¹⁰⁸` | `1.64·10⁻¹⁰⁸` | `4.125·10⁻¹⁰⁵` | `4.13·10⁻¹⁰⁵` |

V8 does assert the header table: its `TABLE` fractions are those eight decimals, and it requires `out ≤ entry ≤ 1.01·out`. The `R` bounds are mostly the nonnegative term `(N+1)δ·324·31`. The `c₃` bounds are mostly the polynomial term.

Lemma 2’s three-digit displays (`δ₃(10) ≤ 2.44·10⁻⁹`, `δ₃(24) ≤ 2.03·10⁻¹¹⁰`) are coarser than V8’s rational `δ`. Substituting those displays into the same monotone formula exceeds the two `d = 3` `R` entries (`4.976·10⁻⁴` and `4.140·10⁻¹⁰⁵`). The proof evaluates the table at V8’s tighter upper bound of the exact `δ_d`, which the table dominates. The stated inequalities stand.

**Corollary V1.** `J ≥ 1/2000` gives `J/30 ≥ 1/60000`. The larger `L ≥ 10` entry is `η_c ≤ 1.97·10⁻⁷`, and `1/60000 − 1.97·10⁻⁷ > 0`. Theorem C3 says `c₃` is the coefficient of `ℓ^{2/3}` in `ν_cand`, with remainder `o(ℓ^{2/3})`. Theorem P⁺ is the same expansion with `O(ℓ^{2/3})`. Successor [6026230530](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6026230530) leaves that statement unchanged. A positive `c₃` makes the `O` of exact order `ℓ^{2/3}`. That is the logic of note C3’s Corollary G′ and Proposition G″, with `L₀(2) = L₀(3) = 10`, including SIDE24.

**Corollary V2.** At `L₀ = 24` the computed bounds sum to `6.484·10⁻¹⁰⁷` (`d = 2`) and `4.127·10⁻¹⁰⁵` (`d = 3`), so `η_{C7} = 6.5·10⁻¹⁰⁷` and `4.2·10⁻¹⁰⁵` satisfy `η_{C7} ≥ η_c + η_R`. The factor in (5.3) is `1/2400`: `|S|·(1/3)·w_∞·(1/32)` with `w_∞ = 𝒮_d/(25|S|)` equals `1/2400`. Then `J/30 − Ĩ = J/30 + (112/675)Γ(1/6)12^{−1/6} − D`. The lower bound recomputes as `(112/675)·6·0.9277·0.6608 + 1/60000 = 0.610316 ≥ 0.6103`, from `Γ(7/6) ≥ 0.9277` and `0.6608⁶·12 ≤ 1`. So `D ≤ 0.61` leaves a margin `0.0003` over `η_{C7}`. Theorem C7’s (C7.1) says `c₃ − R_{2/3}` is the coefficient of `ℓ^{2/3}` in `ν_eld − ν_eld^{far,r_0^*}`. The #244 condition is stated on the corollary.

**The `c₃` half avoids #244.** It uses the split of `ψ^c`, note C3’s `J` and (G.3), Lemmas 1–4 and J, Theorem C3 and Theorem P⁺. It is free of `Φ`, Lemma K and Theorem A. Lemma K and `I = Φ` are used for `ρ^R`, the `R` columns, `D` and Corollary V2. The condition is stated there, and in *Not claimed*, *Consumed*, §0, Lemma 0, Lemma K, Theorem V and Remarks 1–2. §3’s formula for `w_∞` is identified there as note C3’s identity.

**Remarks.**
1. `J = 4.1977819815839` is note C3 §5. `Ĩ = −0.5336676` is #244 §5. `Ĩ_quad = −0.61040568`, so `D = Ĩ − Ĩ_quad = 0.07673808`, which rounds to `0.0767381`. `J/30 − Ĩ = 0.67359367` rounds to `0.673594`. `𝒮₂ = 0.09140283` and `𝒮₃ = 0.11500581` match #242’s Corollary 1′ and #244’s prefactors. The model coefficients round to `0.0615684` and `0.0774672`, and the ratios to `0.838727` and `1.85435`, against `c_{2,∞} = 0.073406919` and `c_{3,∞} = 0.041775932` from note C3 §5. `η_{C7}𝒮_d` is `5.94·10⁻¹⁰⁸` and `4.83·10⁻¹⁰⁶`, under the stated `6·10⁻¹⁰⁸` and `4.9·10⁻¹⁰⁶`. A kink-unaware tensor Hermite check of (5.3) reproduced the positive part `0.6630` against `0.663146`. The negative part was not resolved at the claimed `5·10⁻⁸`. That check is exploration. The constant `2.907` in (K) is the author-side scan recorded with the controls.
2. The four-term display is (C7.1). The `c₂` interval `[0.1612340491269447, 0.1612340491269810]` is the `d = 3` SIDE24 line of `c2_torus_transfer`’s corollary, blob `5ce5bad2` at `0793dc26`. The #244 condition is stated.
3. [6033651797](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6033651797): on `[10⁻⁴, 3·10⁻²]`, 14 bins, χ² goes from `84.4` to `22.7` and from `44.1` to `7.0`, and the free fits are `0.0600 ± 0.0073` and `0.0544 ± 0.0088`. The note’s `84` to `23`, `44` to `7`, `0.060 ± 0.007` and `0.054 ± 0.009` match that comment, including its “2.4 standard errors” sentence (`(0.0775 − 0.0600)/0.0073 = 2.40`).
4. `k^{−8/3}` is not integrable at `0`. `E[ρ^c] = O(k³)` and `E[ρ^R_±] = O(k²)` restore integrability.
5. The exceptions match the control: the even-block exponent is `(d−5)/2`, and the shell ratio is proved for `d+5 ≤ 8`.

**Header.** *What is new* is proved in §5, with #244 Theorem A’s condition on every `R_{2/3}` conclusion. *Consumed* and *Cited only* cover the external citations in the note. #170 and [CUB] appear inside that #244 condition. *What is new* adds no certified value of `J`, `Ĩ` or `D`, no rate, and no result for `d ≥ 4`.

**Controls.** `python3 -B -S` and `python3 -B -O -S` both exit 0 with byte-identical stdout, hash as above. Mutants, both modes, exit 1 with empty stdout: M8 `FAILED: V5_moment_perturbation`, M9 `FAILED: V8_assembly`, M10 `FAILED: V9_lemmaK_step1`, M12 `FAILED: V8_assembly`. Invalid invocations (`M13`, `M0`, a bare `--mutant`, an extra argument, an unknown flag) exit 2 with `usage: v24_exact.py [--mutant M1..M12]`. V9 samples `(ψ − c′)/ψ ≤ 2`. The general bound is Lemma K’s argument, which this slice did not re-prove. M10 fails on that sample.

**Not checked.** Proofs of Lemmas 0–4, K and J, and of §§0–4, except the formulas §5 cites. The contents of V1–V4, which ran only because V8 calls them. The proof of #244 Theorem A. Any scientific acceptance, status, or premise.

Math- packets were read at `0793dc26`. The blob prefixes match: #242 `271412db`, #244 `c69f92b1`, #237 `a97bf528`, [P] `dfed3b8d`, [R] `247b3ecf`, the cusp transfer `de3d85fd`, [SIDE24] `44b66f04`, `c2_torus_transfer` `5ce5bad2`.



<div><a href="https://cursor.com/agents/bc-65b7f8e6-df42-40fa-a54f-c2c183d213c9?cursor_ref=pr_footer&cursor_cta=open_in_web"><picture><source media="(prefers-color-scheme: dark)" srcset="https://cursor.com/assets/images/open-in-web-dark.png"><source media="(prefers-color-scheme: light)" srcset="https://cursor.com/assets/images/open-in-web-light.png"><img alt="Open in Web" width="114" height="28" src="https://cursor.com/assets/images/open-in-web-dark.png"></picture></a>&nbsp;<a href="https://cursor.com/background-agent?bcId=bc-65b7f8e6-df42-40fa-a54f-c2c183d213c9&cursor_ref=pr_footer&cursor_cta=open_in_cursor"><picture><source media="(prefers-color-scheme: dark)" srcset="https://cursor.com/assets/images/open-in-cursor-dark.png"><source media="(prefers-color-scheme: light)" srcset="https://cursor.com/assets/images/open-in-cursor-light.png"><img alt="Open in Cursor" width="131" height="28" src="https://cursor.com/assets/images/open-in-cursor-dark.png"></picture></a>&nbsp;</div>

