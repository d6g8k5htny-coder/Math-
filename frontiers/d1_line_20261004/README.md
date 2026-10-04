# Theorems 1D and 1D⁺ on the line

**Author-side proof candidate (Anthropic Claude). Scientific effect: NONE. Nonauthor review required.**

Object `CL-D1-LINE-20261004-v1.1`. Full text: [`PROOF.md`](PROOF.md). Dylan Roy — delegated AI work.

**v1.1** was made before any nonauthor pickup; v1 was `f34ffd7`. It drops v1's decay hypothesis on `ρ, ρ', ρ''`, so
(H_ℝ) is now purely spectral. Lemma 4.3_ℝ now uses interlacing: conditioning on the three pin observations lowers at
most three eigenvalues of the samples' covariance, whatever the cross-covariances. The theorem and its rates are
unchanged.

## Result

Let `f` be a centered stationary Gaussian process on `ℝ` whose spectral measure has a density `s`. Assume (H_ℝ):
- (R1) all moments `∫|ω|^n s` are finite;
- (R2) `s ≥ s₀ > 0` on some interval `[ω₁, ω₂]` with `ω₁ > 0`;
- (R3) `(1 + ω⁶)s(ω)` is bounded.

No decay rate of the covariance is assumed. `ρ, ρ', ρ'' → 0` follows from (R1) by the Riemann–Lebesgue lemma.

Then, per unit length, as `h ↓ 0` and `ℓ ↓ 0`:

    ν₊(h) = (C₀/2) h^{−1/3} + (I/2) h^{1/4} + B₂ h^{1/3} + O(h^{3/4})           (1D_ℝ.1)
    ν(ℓ)  =  C₀ ℓ^{−1/3}   +  C₁ ℓ^{1/4}  + 2B₂ ℓ^{1/3} + O(ℓ^{3/4})           (1D_ℝ.2)

Here `ν₊` is the density of crest-to-trough amplitudes and `ν` that of persistence lifetimes. The constants are those of
Math- #214 §0, functions of `λ₂, λ₄, λ₆, λ₈` only. On the circle these laws are Math- #214 (Theorem 1D, remainder
`O(h^{1/2})`) and Math- #238 (Theorem 1D⁺, `O(h^{3/4})`), both merged.

For the covariance `e^{−x²/2}`, the classical setting of Rice, Cartwright–Longuet-Higgins and Lindgren, the
crest-to-trough density per crest is

    f_H(h) = 0.19971814 h^{−1/3} − 0.27165891 h^{1/4} + 0.41725471 h^{1/3} + O(h^{3/4}).

Its leading constant is the one of Math- #210.

## What is new

On the circle, compactness bounds the far part of the kernel. On the line a banded pair can be arbitrarily long, so
the number of sample points has to grow with the length of the band.

| Step | Statement | Tool |
|---|---|---|
| §1 | Nondegeneracy (Lemma 1.1_ℝ); `f` unbounded on half-lines (Lemma 1.5_ℝ), also under the pinned law; the marked two-point Kac–Rice formula on `ℝ` | entire functions; Maruyama + Birkhoff; Gaussian regression; monotone limits of compact-window marks |
| §2 | The parts of #214 and #238 that are local transfer verbatim | review of each step for global objects |
| Lemma 3.1_ℝ | `∫_{t₀}^{T₀}K^{band} = O(h²log(1/h))` | #214 Lemma 4.3's far argument on a compact range |
| Lemma 4.1_ℝ | the pin covariance is uniformly nondegenerate for `t ≥ T₁` | Riemann–Lebesgue + Gershgorin |
| Lemma 4.2_ℝ | `\|g'(y)\| ≤ (osc·S)^{1/2} + 2osc/\|Δ\|` at the midpoint `y` of an interval `Δ` | Landau |
| Lemma 4.3_ℝ | `P_Q(\|f'(y_i)\| ≤ ε, i ∈ G) ≤ (ε(2e/λ_*)^{1/2})^{\|G\|−3}` for `w`-separated samples, `\|G\| ≥ 6` | Ingham's inequality + interlacing (at most three eigenvalues drop) |
| Lemma 4.4_ℝ | `P_Q(at least N/2 of N cells have sup\|f''\| > R) ≤ exp(−NR²/(8σ_F²))` | Gaussian concentration along the Cameron–Martin space |
| Lemma F_ℝ | `∫_{T₀}^∞K^{band} = O(h^{17/8}(log(1/h))^{17/16}) = O(h²)` | Lemmas 4.1_ℝ–4.4_ℝ, with at least `23` cells |

## Dependencies

**Consumed (merged; bytes bound in `SOURCES.json`).**
- Math- #214, `frontiers/d1_third_order_law_20261001/PROOF.md`, blob `1591ecee`, merged at `e4ca2b3` ([1D]).
- Math- #238, `frontiers/d1_sharp_remainder_20261001/PROOF.md`, blob `8dc558a7`, merged at `8404169` ([1D⁺]).

**Cited.** `[P]` (`UNIFORM_MATRIX_CAP_AND_LIFETIME.md`, blob `dfed3b8d`) and `[E2]` (`REPAIR.md`, blob `fe9b9ce4`), the
marked Kac–Rice convention, through [1D] §1. Math- #210 (open; head `213dd9e`, addendum blob `b289c7cd`) is cited for
comparison only and is bound through the repository API.

## Controls

`line_check.py` uses only the standard library. It uses exact rationals, except that C3 evaluates the closed-form
constants in floating point. Its output is `RESULTS.json`, byte-identical with and without `-O` on CPython 3.10–3.14.

| Control | What it checks |
|---|---|
| C1 | Landau's inequality on 300 polynomials and the Taylor step, exactly. A nearly affine family shows that the term `2osc/\|Δ\|` is needed, and S-shaped cubics (with `osc` bounded above) that `(osc·S)^{1/2}` is |
| C2 | For the Gaussian kernel, the `f'`-sample covariance at spacing `w ≥ 2` is diagonally dominant with `λ_min ≥ 1/6`, using rigorous rational bounds for `e^{−x}` |
| C3 | `C₀, C₁, I, B₂` and the per-crest coefficients against the printed values; `𝒬 = 1620` and `𝒬/(120λ₂λ₄D) = 3/4` exactly |
| C4 | The cell Sobolev bound with constant `2`, on 155 polynomials; the witness `1 + (s/w)²/2` shows that the constant `1` is false |
| C5 | The geometric steps and exponent bookkeeping of Lemma F_ℝ (at least `23` cells), at sample values |
| C6 | Interlacing by exact inertia counts (`LDLᵀ`, Sylvester), with a family attaining the bound; Stirling's lower bound for the ball volume; the threshold `R₀ = 5(M₂^{1/2} + 1)` of Lemma 4.4_ℝ |

Replay:

    python3 -B -S line_check.py                 # exit 0; stdout = RESULTS.json
    python3 -B -S line_check.py --mutant M1     # M1–M7 exit 1, each in its own control
    python3 -B -S line_check.py --mutant XX     # exit 2

The workflow `.github/workflows/d1-line.yml` checks the packet tree and file identities, the consumed and cited sources,
both replay modes, the mutants and the bad arguments.

## Review

Before submission, two clean-context same-family referees (Anthropic Claude subagents) read the draft. Both returned
ACCEPT WITH MINOR FIXES on their slices, with no major finding. Their fixes are applied, and a delta check of the
revision found them fixed; `SOURCES.json` (`referee`) lists what they found and what changed. v1.1's new material
(Lemma 4.1_ℝ, the interlacing Lemma 4.3_ℝ, and Lemma F_ℝ with `23` cells) came after that pass. A second delta check
returned ACCEPT on slices B and C, and ACCEPT WITH MINOR FIXES on slices A and D, for one sentence of §0 and the
packaging; both are applied. One author-side
correction, made before the referee pass, changed a constant: the threshold of Lemma 4.4_ℝ is `R₀ = 5(M₂^{1/2} + 1)`,
because the factor `4` does not give `R/√2 − R/4 ≥ R/2`. These referees share a provider with the author and give no
independence credit.

**Requested:** a nonauthor review, by slices (PROOF §9):
- **A** §§0–1: the objects on `ℝ`, Lemmas 1.1_ℝ and 1.5_ℝ, the process under `Q`, and the Kac–Rice representation;
- **B** §2: that the listed parts of #214 and #238 are local;
- **C** §§3–4: Lemma 3.1_ℝ, Lemmas 4.1_ℝ–4.4_ℝ and Lemma F_ℝ;
- **D** §5 and the controls.

## Not claimed

- No uniformity in the covariance, and no explicit constant in any `O(·)`.
- No sharpness of the remainder `3/4`.
- Nothing without (R2) (for instance, spectra on finitely many points), or for spectral densities with `(1 + ω⁶)s`
  unbounded ((R3)), such as a spectral pole at `0` (long-range dependence) or spiky high-frequency tails.
