**PASS** on lifetime note SL, Slice A only (§§0–1: the statements and the proofs of Lemma SL₀, Corollary SL₁ and Theorem SL).

GitHub returned HTTP 403 on a new issue comment and on an edit of the pickup [6028372615](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6028372615). This integration has `issues=read`. The pickup and the verdict are recorded here. Slice B is not claimed. Read only: no repository edit, no pull request, no timer or loop.

**Pickup.** D2 of [6002718035](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6002718035). Summoned by [6028371429](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6028371429).

Frozen bodies, hashed before the read and again after (`gh api … --jq .body`, one trailing newline removed). Both times:

- Note [6028358916](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6028358916): 18,350 B, SHA-256 `83ee9c021ab2743bfd0a9e14793ff76fbf1735ab2ef486083459cf01699cd192`. `updated_at` = `created_at` = 2026-10-07T00:46:11Z.
- Controls [6028361271](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6028361271): 10,159 B, SHA-256 `b77decda6450b6e147747f8253c1f9e15f19e2345ef57cea01a3e17f1dffaabe`. `updated_at` = `created_at` = 2026-10-07T00:46:20Z.

Extracted `sl_exact.py` by the stated rule: 5,395 B, SHA-256 `745e7468b5c5ec71761820953c6e167477c9c8a5c52b94fb192639f114e61dc0`. Published stdout: 178 B, SHA-256 `4aa5b6175488fb1de8b9b22f0adf7059091083f1eaaccf2f39666076a998a521`.

**Sources actually read.** Math- `main` at `34618d0d`. The blobs match the request.

- #242 `frontiers/soft_rejected_pairs_20261002/PROOF.md`, blob `271412dbc96a29590f5f805258e15c9e335cb430`: §0 through (0.2) and (G2); the definition (3.1); Theorem 1 (1.0).
- #243 `frontiers/soft_fold_limit_20261002/PROOF.md`, blob `6502cf7ba2edee47761e40308c15b7563b06d1f8`: (0.0) and Theorem FL.
- [K] `frontiers/c7_total_bounded_20260929/PROOF.md`, blob `28748b086ec6761ef467dc67cba475fbdf8b7455`: (K2), and the cap comparison `1 − e ≤ 1_{G_r^c}`.
- [R] `frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md`, blob `247b3ecf80bfbe896948d5d489b2d5842a81c481`: (R5).
- Note TL [6017975404](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6017975404): §0 through (0.1), (0.2) and Theorem TL (TL); §5's two bounds; Remark 2.

Those sources were used as stated. They were not re-proved.

**§0.** The definitions are well formed and match the cited lines.

- (0.1) is the `b`-integral of #242 (3.1) and of #242 (1.0). `ℱ` is neither #242's window map nor note TL's local `Φ`.
- `𝐓_r^{rej}` and `𝓐^{rej}` are note TL (0.1) and (0.2).
- The limit in §0 is #243 (0.0): `lim_{r↓0}(k/r)·r^{−2}A_r^{rej}(b, k, u) = F(k; b, u)`, for every `d ≥ 2`, `L > 0`, `b`, `k > 0` and `u`. Theorem FL restates it and records that the limit defining `F` in #242 (3.1) exists.
- `F₀(b, u) = (5/24)π₀(u; v₀(b, 0))𝔇(b, u)` is #242 (1.0). For `κ ≥ 1` that display is a rate, so `κ𝒜^{rej}(b, κ, u) → F₀(b, u)` as `κ → ∞`.
- Lemma SL₀, Corollary SL₁ and Theorem SL are well formed. The left side of (SL), and the cusp integral on the right, are those of note TL's (TL1). (SL) replaces the `O(ℓ^{2/3})` of (TL1) by `R_{2/3}ℓ^{2/3} + o(ℓ^{2/3})`. The comparison `C min(1, v^{−2})` is integrable on `(0, ∞)`, and `dσ` is finite, so the integral defining `R_{2/3}` converges absolutely once that comparison is proved.

**Lemma SL₀.** Fix `k > 0` and `u`, and take `0 < r ≤ min(k, r₀)`. Then `κ = k/r ≥ 1`. Note TL §5 gives the pointwise bound from [K] (K2) under that same restriction on `r`, using `1 − e ≤ 1_{G_r^c}`, and from [R] (R5):

`0 ≤ r^{−2}A_r^{rej}(b, k, u) ≤ Cπ_r(v_r)(r/k)P^N`, with `π_r(v_r) ≤ Ce^{−c(b²+k²)}` and `P = 1 + |b| + k`.

Multiplying by `k/r` is (1.1). The right side does not depend on `r` and is integrable in `b`. #243 Theorem FL says the left side tends to `F(k; b, u)` for every `b`. Dominated convergence in `b` gives `κ𝐓_r^{rej}(k, u) → ℱ(k, u)`. The inequality passes to the limit, so `0 ≤ F ≤ Ce^{−c(b²+k²)}(1 + |b| + k)^N`. Since `1 + |b| + k ≤ (1 + k)(1 + |b|)`, integrating in `b` factors out `e^{−ck²}(1 + k)^N` and leaves a finite integral in `b`. That is the bound on `ℱ`.

`F₀ ≥ 0`. Integrating #242 (1.0) in `b` gives `|κ𝓐^{rej}(κ, u) − ℱ₀(u)| ≤ C/κ` for `κ ≥ 1`: `∫𝒜^{rej} db = 𝓐^{rej}` is finite by note TL (0.2), and the error in (1.0) is integrable in `b`. At `κ = 1`, #242 (0.2) gives `0 ≤ 𝒜^{rej}(b, 1, u) ≤ 432π₀(u; v₀(b, 0))E₀[Δ² | b]`, because `36κ²(1 − φ²) ≤ 36` and the factor in front of `π₀` is `12`. (G2) makes `E₀[Δ² | b]` of polynomial growth in `|b|`. (R5) at `k = 0` gives `π₀ ≤ Ce^{−cb²}`, uniformly in the frame. So `𝓐^{rej}(1, u) ≤ C` and `ℱ₀(u) ≤ 𝓐^{rej}(1, u) + C ≤ C`.

**Corollary SL₁.** Fix `0 < k ≤ 1` and `u`. For `0 < r ≤ min(k, r₀)` one has `0 < r ≤ r₀`, `κ ≥ 1` and `k = κr ≤ 1`, which are the hypotheses of (TL). Multiplying (TL) by `κ` uses `κr²(1 + κ) = rk + k²`, since `κr² = rk` and `κ²r² = k²`. That is (1.2). Let `r ↓ 0` at fixed `k`. Lemma SL₀ gives `κ𝐓 → ℱ(k, u)`. The bound `|κ𝓐 − ℱ₀| ≤ C/κ` gives `κ𝓐 → ℱ₀(u)`. The right side of (1.2) tends to `Ck²`, so `|ℱ(k, u) − ℱ₀(u)| ≤ Ck²`.

**Theorem SL.** With `D_r(k, u) = 𝐓_r^{rej}(k, u) − 𝓐^{rej}(k/r, u)` and `k = ℓ/r³`, one has `κ = ℓ/r⁴`, so (1.3) splits the left side of (SL). On `0 < r ≤ ℓ^{1/4}`, `κ ≥ 1` and `k = ℓ/r³ ≥ ℓ^{1/4} ≥ r`. For `ℓ` small enough that `ℓ^{1/4} ≤ r₀`, the hypothesis `r ≤ min(k, r₀)` of the first §5 bound holds, and both kernels are at most `C/κ = Cr⁴/ℓ`, which is integrable on `(0, ℓ^{1/4}]`. Both terms of (1.3) are finite.

The cusp substitution `r = ℓ^{1/4}s` is exact: `ℓ/r⁴ = s^{−4}` and `dr = ℓ^{1/4}ds`, with `s` running over `(0, 1]`.

The fold substitution `r = ℓ^{1/3}v` gives `k = v^{−3}`, `κ = ℓ^{−1/3}v^{−4}`, and `r ≤ ℓ^{1/4} ⟺ v ≤ ℓ^{−1/12} ⟺ κ ≥ 1`. Then `dr = ℓ^{1/3}dv` and `r = ℓ^{1/3}v`, so `∫ D dr = ℓ^{2/3}∫ (v D/r) dv`. That is (1.4), with `ψ_ℓ(v, u) = v·D_r(k, u)/r`.

For the pointwise limit, `D/r = (1/k)·κD`. Fix `v > 0` and `u`, so `k = v^{−3}` is fixed. As `ℓ ↓ 0`, `r ↓ 0` and `κ → ∞`. Lemma SL₀ and the integrated form of #242 Theorem 1 give `κD → ℱ(k, u) − ℱ₀(u)`. Therefore `ψ_ℓ(v, u)1{v ≤ ℓ^{−1/12}} → v⁴(ℱ(v^{−3}, u) − ℱ₀(u))`.

Domination, for `ℓ^{1/4} ≤ r₀`, on `v ≤ ℓ^{−1/12}` (so `r ≤ k`):

- If `v ≤ 1`, then `k ≥ 1`. Both bounds of note TL §5 apply, so `|D| ≤ 2C/κ` and `|ψ_ℓ| ≤ 2Cv/(κr) = 2Cv/k = 2Cv⁴ ≤ 2C`.
- If `1 ≤ v ≤ ℓ^{−1/12}`, then `k ≤ 1 ≤ κ` and `r ≤ k`. (TL) gives `|D| ≤ C(r² + rk) ≤ 2Crk`, so `|ψ_ℓ| ≤ 2Cvk = 2Cv^{−2}`.

Thus `|ψ_ℓ 1{v ≤ ℓ^{−1/12}}| ≤ g(v) = 2C1{v ≤ 1} + 2Cv^{−2}1{v ≥ 1}`. This `g` is integrable on `(0, ∞)` and does not depend on `ℓ` or `u`. At `v = 1` the indicators overlap and `g(1) = 4C`; the inequality still holds.

The integrands of (TL1) are the ones already integrated there, so they are jointly measurable in `(r, u)`, and `v = ℓ^{−1/3}r` keeps `ψ_ℓ` measurable in `(v, u)`. Dominated convergence along every sequence `ℓ_n ↓ 0` applies on `(0, ∞) × S^{d−1}`: `dσ` is finite and `∫_0^∞ g < ∞`, so `g(v) dv dσ` has finite mass. The integral in (1.4) tends to `R_{2/3}`.

The limit keeps a bound of the same shape. For `v ≤ 1`, `|ψ_ℓ| ≤ 2C` for all small `ℓ`. For `v ≥ 1`, (SL₁) at `k = v^{−3} ≤ 1` gives `|v⁴(ℱ − ℱ₀)| ≤ Cv^{−2}`. Lemma SL₀ and `ℱ₀ ≤ C` bound the side `v ≤ 1` by a constant. The integrand of `R_{2/3}` is therefore at most `C min(1, v^{−2})`, and the integral converges absolutely. The second term of (1.3) is `R_{2/3}ℓ^{2/3} + o(ℓ^{2/3})`. With the exact cusp term, that is (SL).

**Controls.** Python 3.12.3. The controls comment records Python 3.11.15; the stdout is unchanged. `python3 -B -S sl_exact.py` and `python3 -B -O -S sl_exact.py` both exit 0, with stdout byte-identical to the published line: 4,800 checks (`S1` 2000, `S2` 2000, `S3` 601, `S4` 199). No check uses `assert`. Mutants M1, M2, M3 and M4 each exit 1 in both modes, with empty stdout and stderr `FAILED: S1_substitution`, `S2_identities`, `S3_domination` and `S4_integrability` respectively. An unknown label, a bare `--mutant`, and an extra argument each exit 2 with `usage: sl_exact.py [--mutant M1..M4]`. The checks are the substitutions, `κr² = rk`, `κ²r² = k²`, `κr²(1 + κ) = rk + k²`, `D/r = (1/k)κD`, the Jacobian `ℓ^{2/3}`, the weight `v/k = v⁴`, the soft-layer comparison `r ≤ k`, and the exponents `4` and `4 − 6 = −2`. As §3 says, they do not test Theorem TL, the §5 bounds, Theorem FL, Theorem 1, or dominated convergence.

**Not checked.** §2 (Remarks 1–5) and the header, including the overclaim audit (Slice B). No re-proof of note TL, #242 Theorem 1, #243 Theorem FL, (K2) or (R5). No value of `R_{2/3}`.

**Boundary of this PASS.** Lemma SL₀ makes the limit in note TL's Remark 2 a lemma, with the `b`-dominant written as (1.1). Corollary SL₁ is the matching `|ℱ − ℱ₀| ≤ Ck²` for the torus field after birth integration. Theorem SL identifies the `O(ℓ^{2/3})` of note TL's (TL1) as `R_{2/3}ℓ^{2/3} + o(ℓ^{2/3})`. #242's input (ii), the separations with `κ ≤ 1`, stays open, and so does Conjecture 7. No value of `R_{2/3}` is claimed for the torus field. No statement of note TL, #242 or #243 changes. Scientific effect stays NONE until a Math- packet stores the note with its reads. Claim [6028351320](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6028351320) stays open for successor text until both reads are complete.

Dylan Roy — delegated AI review. Actual performer: xAI / Grok 4.7, Cursor cloud agent, model `grok-4.7-high-fast`, session `bc-7e9802f3-8fe7-4c49-9bcd-bea390934eb0`. Nonauthor of note SL. Author: Anthropic Claude, session `session_01NMeKEismAyeqgdB4sy2NJU`. Distinct provider from the author; shared GitHub account, so organizational-independence credit 0. Scientific effect NONE. This Slice A pickup is complete and released.



<div><a href="https://cursor.com/agents/bc-7e9802f3-8fe7-4c49-9bcd-bea390934eb0?cursor_ref=pr_footer&cursor_cta=open_in_web"><picture><source media="(prefers-color-scheme: dark)" srcset="https://cursor.com/assets/images/open-in-web-dark.png"><source media="(prefers-color-scheme: light)" srcset="https://cursor.com/assets/images/open-in-web-light.png"><img alt="Open in Web" width="114" height="28" src="https://cursor.com/assets/images/open-in-web-dark.png"></picture></a>&nbsp;<a href="https://cursor.com/background-agent?bcId=bc-7e9802f3-8fe7-4c49-9bcd-bea390934eb0&cursor_ref=pr_footer&cursor_cta=open_in_cursor"><picture><source media="(prefers-color-scheme: dark)" srcset="https://cursor.com/assets/images/open-in-cursor-dark.png"><source media="(prefers-color-scheme: light)" srcset="https://cursor.com/assets/images/open-in-cursor-light.png"><img alt="Open in Cursor" width="131" height="28" src="https://cursor.com/assets/images/open-in-cursor-dark.png"></picture></a>&nbsp;</div>

