# The one-dimensional lifetime and crest-to-trough laws to third order (CL-D1-THIRD-ORDER-20261001-v1)

Author-side proof candidate, Anthropic Claude, 1 October 2026. Scientific effect NONE. Nonauthor review required.
**No dependencies:** self-contained (Gaussian conditioning, the two-point Kac–Rice formula, Taylor, Markov and Landau
inequalities). Math- #207 (Theorem CU, `d ≥ 2`) and #210 (the `d = 1` literature remark) are cited for comparison only.

**Statement (Theorem D1).** Let `f` be a stationary Gaussian process on the circle `R/LZ` whose covariance `ρ` is `C^∞`
with all Fourier coefficients positive (e.g. the periodized `e^{−x²/2}`, the one-dimensional SIDE24 field). Let `ν₊(h)` be
the density per unit length of crest-to-trough amplitudes (maximum to the next minimum) and `ν(ℓ)` that of persistence
lifetimes (superlevel `H₀`, elder rule), both in their canonical Kac–Rice versions. Then

    ν₊(h) = (C₀/2)h^{−1/3} + (I/2)h^{1/4} + B₂h^{1/3} + O(h^{1/2}),
    ν(ℓ)  =  C₀ℓ^{−1/3}  +  C₁ℓ^{1/4} + 2B₂ℓ^{1/3} + O(ℓ^{1/2}),

with explicit constants in the spectral moments: `C₀ = 2·72^{−1/6}Γ(7/6)(2π)^{−1/2}p₁₂σ₃^{4/3}`,
`C₁ = −(8/21)24^{1/4}μ_{7/4}(2π)^{−1/2}p₁₂σ₄^{7/4}/σ₃ < 0`, `I = (3^{1/4}/2)C₁`, and
`B₂ = 2^{1/2}3^{1/3}Γ(5/6)(2π)^{−1/2}p₁₂σ₃^{2/3}𝒬/(120λ₂λ₄D) > 0`, where
`𝒬 = 4λ₂²λ₄λ₈ + 26λ₂λ₄²λ₆ − 5λ₂²λ₆² − 25λ₄⁴`.

Here `σ₃² = Var(f''' | f')`, `σ₄² = Var(f'''' | f'')`, `p₁₂` is the density of `(f', f'')` at `0`, and
`μ_{7/4} = E|Z|^{7/4}`.

For `e^{−x²/2}` the constants are `C₀ = 0.11011038`, `C₁ = −0.22760636`, `I = −0.14977341` and `B₂ = 0.11502229`. The
leading crest-to-trough constant per crest is `0.19971814`, #210's constant, so its remark becomes a theorem on the
circle. Adjacent max/min pairs that are not elder pairs have density `(I − C₁)ℓ^{1/4} + O(ℓ^{1/2})`.

**Mechanism.**
- *Leading term.* The leading term is the fold law: a maximum and the adjacent minimum at separation `t`, gap
  `≈ f'''t³/12`, at scale `t ≍ ℓ^{1/3}`.
- *The `ℓ^{1/4}` terms.* These come from the cusp scale `t ≍ ℓ^{1/4}`. There the pair sees #207's quartic ridge with no
  transverse fiber: it is adjacent iff `|φ| < 1` and an elder pair iff `|φ| < 1/3`, where `φ = f''''t⁴/(72ℓ)`. The fold law
  overcounts on this scale, and the deficit is a Mellin integral `k_θμ_{7/4}`, with `k₁ = 32/7` and `k_{1/3} = (64/7)3^{−1/4}`.
- *The `ℓ^{1/3}` term.* This collects the `τ²`-corrections of the pinned Gaussian law at the fold scale, plus the finite
  part of the cusp integrand.

**Structure of the proof.**
1. Under the pinned law, the pair kernel is an explicit Gaussian integral `(12/t⁴)p_t(α)E((m + E₂)² − E₁²)⁺`. This is exact,
   by a reflection symmetry that makes `E₁ ⊥ E₂`.
2. Its asymptotics give the three terms (Proposition 2.2).
3. On a fixed window `[−2, 2]` the elder rule is decided by the quartic model, with explicit margins (Lemma 3.3).
4. Thin and far pairs are negligible by a band lemma (Markov's inequality) and a flat-band (Landau) bound.

**Relation to #207.**
- (CU.2) at `d = 1` equals `C₁` exactly.
- `I/C₁ = 3^{1/4}/2` is (CU′.1)'s ratio.
- The proofs are independent, so this is a one-dimensional check of #207's normalization `(192/7)2^{1/4}` and of its elder
  window. It is not a proof of any part of #207.

**Numerical evidence (exploration).**
- *Deterministic two-point Rice integral (stdlib; control C6).* For `e^{−x²/2}` it fits the `h^{1/4}` coefficient
  `−1.3602117` (prediction `I/C₀ = −1.3602115`) and the `h^{1/3}` coefficient `2.0892177` (prediction `B₂/(C₀/2) = 2.0892180`).
  For the mixture `(e^{−x²/2} + e^{−2x²})/2` the fits are `−1.4697391` and `2.1373811`, against `−1.4697376` and `2.1373703`.
- *Monte Carlo (numpy, outside the repository).* Total length `8.4·10⁷`. Persistence lifetimes match the three-term law to
  `1.000 ± 0.003` on `[10⁻⁵, 10⁻²]`, and the rejected-adjacent-pair coefficient is `0.07779 ± 0.00080` against
  `I − C₁ = 0.0778330`.
- *Why plain histograms look flat.* The second and third terms nearly cancel on `10⁻⁴ ≤ ℓ ≤ 10⁻²`.

**Not claimed:** anything on the line `R` (needs a decorrelation hypothesis, §6.4); uniformity in the covariance; constants in
the `O(·)`; sharpness of `O(h^{1/2})`.

**Files.**
- `PROOF.md`.
- `d1_check.py`: standard library. Its output is `RESULTS.json`, byte-identical under `-O`. Mutants M1–M5 exit 1, and an
  unknown label exits 2. Run time is about three seconds. Its controls:
  - **C1** the constants, by exponent bookkeeping: (CU.2) at `d = 1`, the printed forms, `C₀`, `I/C₁`, and the `B₂`
    prefactors.
  - **C2** the Mellin integrals `k_θ`.
  - **C3** the model identities (3.1), the margins of Lemma 3.3, and the decision by exact persistence for 117 rational `φ`.
  - **C4** the pinned-law expansions, as exact Laurent series from the covariance, for two kernels.
  - **C5** the `B₂` polynomial identities.
  - **C6** the two-point Rice integral, a numerical check with tolerance.
- `SOURCES.json` (exact identities of the cited sources).

**Referee record before any nonauthor review (same author family; not acceptance).** Two clean-context Claude referee passes
read v1 before the PR.

*Slices A/B (§§1–2): no false claim.*
- Independent sympy verification of every coefficient in Lemma 1.3 for a general covariance.
- An independent high-precision Rice computation down to `h = 10⁻⁴⁰`. It confirms `I/2`, `C₁/2` and `B₂` to `10⁻⁹`–`10⁻¹¹`,
  and shows that the next term of the sign kernels is `O(h^{3/4})`.
- One gap: Proposition 2.2(a), where the straddle term's kernel is `αt`, not `αt³`. Repaired with its Gaussian factor; the
  bound is now `≤ Ct²`.
- Minor points, all applied.

*Slices C/D (§§3–5).*
- Lemma 3.3's case analysis was confirmed (sympy), as were Lemmas 3.1, 3.2, 4.1 and 4.2 (including the `τ^{N(N+5)}` scaling,
  and that the invertibility condition is necessary), the bookkeeping of ν, and an independent Monte Carlo
  (`2.6·10⁷`, three-term law `0.996 ± 0.003`).
- It found two errors, both repaired:
  - Corollary 3.4's misclassification window omitted the deterministic `τ²` shift between `φ_G` and `φ`;
  - "elder pairs are banded" holds only on the arc of the death point. The co-banded case is now bounded separately.
- It found one gap: a `√log` loss in the misclassification sum. This is removed by the parity split (Remark 1.4: the odd
  part of the field, which carries the first-order window error, is independent of `E₁`).
- Minor points, all applied.

**What the controls do not test:** Lemma 1.1, the Kac–Rice representation, the error bounds of Proposition 2.2, Lemmas
3.2–4.3 and the assembly (§5) are proved in prose only. Review slices (PROOF.md §9):
- **A** the pinned law;
- **B** the explicit asymptotics;
- **C** the window decision;
- **D** thin and far pairs, and the assembly;
- **E** the comparison with #207 and the numerics.
