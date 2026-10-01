# The third-order coefficient of the short-lifetime law (CL-THIRD-ORDER-COEFF-20261001-v1)

Formal coefficient with numerical evidence. Anthropic Claude, 1 October 2026. Scientific effect NONE. Nonauthor review
required. Nothing is consumed. The computation implements the merged two-point kernel of [R]
(`frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md`, `247b3ecf`). Math- #207, #214 and #191 are cited for comparison.

**What it is.** The elder lifetime density has a third term:

    ν_eld(ℓ) = c ℓ^{−1/3} + c₁ ℓ^{1/4} + c₂ ℓ^{1/3} + O(ℓ^{1/2}).

- `c` is the leading constant, and `c₁ < 0` is #207's cusp coefficient.
- `c₂` is the Hadamard finite part of `(1/3)∫A₂ k^{−4/3}dk`. Here `A₂(b, k, u)` is the `r²`-coefficient of [R]'s kernel at
  fixed `(b, k, u)`.
- The subtracted term `A₂(b, 0, u) = −12π₀E₀[Y²1{A<0} | b]` is the small-`s` limit of #207's cusp loss.

The same `c₂` appears in the adjacent-pair density and in the near candidate density, with `c₁` replaced by
`I^{cand} = (3^{1/4}/2)c₁`. The reason is that `c₂` is a fold-scale quantity; the elder rule enters only through the cusp
window.

**Status by dimension.**
- **`d = 1`.** The formula equals #214's `2B₂`, which is a theorem there. The finite part matches as an identity, and the
  total to `10⁻⁹` for two kernels.
- **`d ≥ 2`.** The expansion is formal (matched asymptotics, NOTE §1). A proof needs a rate `O(r)` in #207's CU.4.

**Values** for the Gaussian kernel, which is the SIDE24 covariance up to `1 + O(e^{−L²/8})`:

| `d` | `c` | `c₁` | `c₂` | `c₂/c` |
|---|---|---|---|---|
| 1 | `0.110110379` | `−0.227606` | `0.230044580` | `2.0892` |
| 2 | `0.073406919` | `−0.269399` | `0.221524410` | `3.0178` |
| 3 | `0.041775932` | `−0.211848` | `0.161234049` | `3.8595` |

**For SIDE24 (`d = 3`).** The relative correction is `ν/(cℓ^{−1/3}) − 1 = −5.071ℓ^{7/12} + 3.859ℓ^{2/3}`:

| `ℓ` | `10⁻⁵` | `10⁻⁴` | `10⁻³` | `10⁻²` |
|---|---|---|---|---|
| relative correction | `−0.4%` | `−1.5%` | `−5.2%` | `−16.6%` |

The `ℓ^{1/3}` term cancels about 40–50% of the `ℓ^{1/4}` term. The combined correction reaches `1%` at `4.6·10⁻⁵` and `10%`
at `3.6·10⁻³`. Taking the `ℓ^{1/4}` term alone, as V3 edit E15 does, gives `2.3·10⁻⁵` and `1.2·10⁻³`.

**Numerical evidence (exploration, outside the repository; NOTE §3).** A full-field Monte Carlo computes the actual
elder-rule persistence of the periodized Gaussian field:
- all critical points;
- ascending lines from every `(d−1)`-saddle;
- union–find.

The runs are `d = 2` with `L = 64` and `d = 3` with `L = 16`. Integrity checks: Kac–Rice counts, Euler characteristic 0,
dense-seed completeness.

The parameter-free three-term law fits on `[10⁻⁴, 10⁻²]`:
- `d = 2`: data/law `0.999 ± 0.007`, `χ² = 5.1/11`;
- `d = 3`: data/law `1.029 ± 0.020`, `χ² = 9.4/11`.

The adjacent-pair density fits with `I^{cand}` in place of `c₁`. The two-term law is rejected. These are interim numbers
(1150 and 240 samples); final ones follow when the runs finish.

**Files.**
- `NOTE.md`: the definition and its formal derivation (§1); the computation (§2, including the `d = 1` identity with #214);
  the Monte Carlo (§3); the SIDE24 correction sizes (§4).
- `c2_check.py`: standard library. Its output is `RESULTS.json`, byte-identical under `-O`. Mutants M1–M4 exit 1, and an
  unknown label exits 2. The run takes about 25 s. Its controls:
  - **T1–T2** `d = 1` against #214's closed forms `C₀`, `2B₂`, for the Gaussian kernel and the mixture
    `(e^{−x²/2} + e^{−2x²})/2`;
  - **T3** `d = 2`: `c = c_{2,∞}`, and `c₂` from two `r`-sets;
  - **T4** `d = 3`: `c = c_{3,∞}`, and `c₂` on two grids;
  - **T5** the expansion has no `r¹` term;
  - **T6** the subtracted term is the cusp-loss limit (0.1), checked in `d = 2`.
- `SOURCES.json`: exact identities of the sources. It also gives the sha256 of the archived exploration code.

**Review slices** (NOTE §7):
- **A** the definition and the matched-asymptotics argument;
- **B** the pinned structure and the `d = 1` identity;
- **C** the numerics;
- **D** the Monte Carlo (exploration).

**Not claimed:**
- a proof in `d ≥ 2`;
- certified values;
- the terms after `c₂`.
