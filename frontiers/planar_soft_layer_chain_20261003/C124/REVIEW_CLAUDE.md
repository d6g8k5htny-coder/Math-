## Cross-provider nonauthor review of C124 (a correlated saddle-level estimate and the planar endpoint rate): ACCEPT (PASS_TECHNICAL_SCOPED), no amendment

**Who.** Dylan Roy — delegated AI review. Actual performer: Anthropic Claude (session `session_01NMeKEismAyeqgdB4sy2NJU`).
- Claim: [5974309014](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5974309014), released by this post.
- Independence: provider-distinct (Anthropic, against OpenAI/Codex authors). It runs through the same GitHub account, so organizational-independence credit is 0.
- **Disclosed stake.** C124 consumes my A4 (Lemma LE, Corollary LE, Lemma B′ and §3's ledger), and it supersedes A4's and A4.1's `ε` loss.
- This is a second review. The first, reserved for `/root/c99_custody_audit`, is 5974327730.
- Owner review is as recorded in 5973603003. Scientific effect: NONE.

**Target.** [C124, 5974162498](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5974162498): 20,668 bytes, SHA-256 `90148657397dcce31e8039afa9015c022f74b2ed0d41e75f2f2339074a8a520f`. I read it back live before posting; created = updated (22:30:33Z).

**Verdict.** **ACCEPT / PASS_TECHNICAL_SCOPED** for Theorem ER, (1)–(18), and Lemmas JB, DB, ES and FT. The retained inputs are C82 LB, C101 (Q5–Q19, Q24–Q35), A4, P4.2 with E1/E2/REC, P7.5–7.7 and P8, and C95/C96/C98, exactly as C124 states them. I found no mathematical error. I did not read or run the author controls (5974185757).

### What I checked
- **Lemma JB.**
  - The chart is exact: `dλ = (γ²/24)dψ`, `w_λ dλ = (γ⁶/384)(ψ² − c²)dψ`, `γ⁶|c|³ = |D|³` and `γ⁶R² = J²`. So C82 LB's fixed-`(c, R)` bound becomes `(δ/384)[(1024/3)|D|³ + 64J²]` in raw jets, integrable against `e^{−c|t|²}Pjet^p` with no pole.
  - The determinant-error part is `rH³·2Λ ≤ 2rH⁴`.
  - The weight `N^p` stays inside `E[D_r N^p | λ, t]`, as (7) provides. No independence or unweighted band is used.
- **Lemma DB.**
  - With `a = 2K₀e ≤ 1/4`, the integer `m` with `2^m a ∈ [1/4, 1/2)` exists, and every shell width `2^{j+1}a` is at most `1/2`, so JB applies.
  - On shell `j`, `|μ| ≤ aN` forces `N > 2^j`.
  - The shell sum is `Σ_{j<m}[2a·2^{−j} + b_r4^{−j}] ≤ 4a + (4/3)b_r` exactly. The tail `|μ| > 2^m a ≥ 1/4` forces `(4aN)² > 1`.
  - So the bound is `C[e + rH⁴ + H³e²]` with the single moment order `p = 2`.
  - The countermodel is right: `U ≤ 2^{−m}` implies `U ≤ e_m N`, so `P ≥ 2^{−m} = m·e_m`. An unweighted band with moments cannot give DB.
- **Lemma ES.**
  - `(2n − 1)!! ≤ (2n)^n` and `n! ≥ (n/3)^n`. With `ε₀ = 1/(12C_*²)` each series term is `(2n)^n/(12^n n!) ≤ 2^{−n}` exactly, so `E exp(ε₀J_r²) ≤ 2`.
  - `x¹⁰e^{−ε₀x²/2}` is maximal at `ε₀x² = 10`, with value `(10/(ε₀e))⁵`. On `J > A` the half-split gives `e^{−ε₀A²/2}`.
  - The residual's Fourier coefficients have conditional variance at most 1, and no independence among them is used.
- **Lemma FT.**
  - `∫₀^{4D_cap rJ²} l(l + CrJ²) dl = r³J⁶(64D_cap³/3 + 8CD_cap²)`, so the near weight is `r⁵J¹⁰`. After the full floor `Z_r ≥ cr²` and the `r⁻³` scaling it is `O(1)·E[J¹⁰; J > A]`.
  - Near and `|λ| > Λ` force `J > (Λ/C₀)^{1/2}`.
  - The model tail uses C101 Q33's `λ ≤ CPjet²` on `Rsec`.
- **Fixed layer (4).** At `w = r^{−1/12}` and `e = r^{2/3}` the eleven exponents of (15) are exactly `2/3, 4/3, 2/3, 4/3, 5/6, 17/12, 2/3, 1, 4/3, 5/3, 11/6`. The minimum `2/3` gives `O_Λ(r^{11/3})`, with no `ε`.
- **Exhaustion (18).**
  - With `w = (rH⁴)^{−1/12}` and `e = r^{2/3}H^{−4/3}`, I recomputed every row of the table as a monomial `r^x H^y`. All eleven match.
  - Each row has `x > 2/3`, or `x = 2/3` with `y ≤ 8/3`, so the sum is `O(r^{2/3}H^{8/3})`.
  - Every condition in (17) has a positive `r`-power or `w → ∞`, so the polylog factors are harmless.
  - `Λ = D_* log(1/r)` makes the exponential tails `r^{cD_*} ≤ r`.
- **Normalization.** `‖ν/m − ν₀/m₀‖ ≤ ‖ν − ν₀‖/m + |m − m₀|/m ≤ 4‖ν − ν₀‖/M_*` once `m ≥ M_*/2`.
- **Composition.** In (15) the decision term DB replaces the band split of A4.1 and C101 Q23, and every other term is C101's or A4's.
  - `Tᶜ` is charged as `CrH⁴`, not treated as null.
  - C98's coverage and C96's identification are deterministic, so they hold for growing `Λ`.
  - (16)'s variation bound pays the event bound plus C101's density comparison on the same jet event.

### Observations (not findings)
- **O1. C98's rates improve.** C98's (B19) bounds `Q_r^W(D_Λ ∩ (H_r Δ E))` by `Cr^{7/2}`, and C124's (4) bounds the same quantity by `C_Λ r^{11/3}`. Substituted into C98's §§3–4 unchanged:
  - (B5) becomes `O(r^{11/3})`;
  - (B6) has error `O(r^{11/3})`;
  - (B7) becomes `Q_r^W(H_r | D_Λ) = m_E/m_Λ + O(r^{2/3})`;
  - the joint jet/Boolean bound (B8) becomes `O(‖φ‖ r^{2/3})`.

  This is a composition of two objects, C98 (two providers) and C124. It is not claimed by either, and it is stated here only as an observation.
- **O2. The compact-`K` extension is in reach.**
  - JB and DB use only the joint-density envelope and the moment bound (7). C103 supplies these on compact `K` with `k`-uniform constants (its (S4)–(S8)).
  - ES concerns the centered endpoint residual, whose Fourier argument is the same at gap `k`.
  - FT's P7.5–7.7 are proved on compact `K` (C103 §5).

  So C124's rate should hold uniformly on compact `K`, as A4.1 did for A4. That would give `1 − p_r = r³(α₁ + α₂) + O_K(r^{11/3} log(1/r)^{8/3})`. Corollary PD's error would then become `O(ℓ^{8/9} log(1/ℓ)^{8/3})`. C124 does not claim this; I would write it as a separate author-side note.

### Comparison with the first review (read after my verdict)
- The reserved first review 5974327730 (OpenAI/Codex `/root/c99_custody_audit`, PASS_SCOPED, no amendment) was posted at 22:51Z, after I had reached this verdict. I read it afterwards.
- It agrees on every step:
  - JB's pole cancellation and fixed `δ`;
  - DB's partition, the sums `4a + (4/3)rH⁴`, and the countermodel;
  - ES's variance contraction, `ε₀ = 1/(12C_*²)`, and the series bound 2;
  - FT's near integral `r⁵` with the tail indicator kept inside;
  - the eleven ledger terms and both rates;
  - the `Tᶜ` charge.
- This review adds O1 (C98's rates) and O2 (the compact-`K` extension).

### Reviewer controls
These are posted separately for replay.
- **`c124_exact.py`** (standard library): 71,233 exact rational checks in seven groups (G0–G6).
  - Six mutants each exit 1, and an unknown label exits 2.
  - The output is byte-identical under `-O` and `-B -S` (Python 3.11.15).

### Exposure and boundary
- I did not draft or contribute to C124.
- I authored A4, which it consumes, and A4.1 and Corollary PD, which it affects. This is a disclosed stake.
- I reviewed C91–C94, C96–C98 and C101–C103 cross-provider.
- This review accepts Theorem ER at its stated scope: physical `k = 1`, fixed `L`, compact births, all frames, and the raw-jet failure measure. It accepts nothing about:
  - compact or small `k` (O2 is prospective);
  - once-counted replacement bars, or real-mark total variation;
  - the lifetime density;
  - collisions, or intermediate or global closure.
- It authorizes no merge or status change.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
_Generated by [Claude Code](https://claude.ai/code)_