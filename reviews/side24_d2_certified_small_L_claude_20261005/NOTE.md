# Certified `d = 2` coefficients `c_{2,L}` at small periods

**Object:** `CL-SIDE24-D2-CERTIFIED-SMALL-L-20261005-v1`.
**Author:** Anthropic Claude, Claude Code session `017Mi3hx…`, for Dylan Roy (delegated AI work).
Claim: [main#229 6002718035](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6002718035), item P1.
**Scientific effect NONE.** Additive packet only. No proof, status, register, catalog, PROOF_INDEX, GRAPH or `formal/` change.
Same GitHub account as every lane, so organizational-independence credit is 0.

## 1. What this supplies

The second independent audit lists, as remaining work item 4 ([main#259](https://github.com/d6g8k5htny-coder/main/issues/259)):

> For certified finite-period coefficients: supply interval quadrature and explicit Fourier/image tails with full angular covariance.

The first audit's item 3 ([main#252](https://github.com/d6g8k5htny-coder/main/issues/252)) asks for the finite-`L` coefficient with directional integration and error control. Before this packet, the small-`L` values in `d = 2` were diagnostics only: [Math-#297](https://github.com/d6g8k5htny-coder/Math-/pull/297), and [main#259 6002327092](https://github.com/d6g8k5htny-coder/main/issues/259#issuecomment-6002327092) for `L = 2`.

This packet gives **rigorous outward enclosures** of the coefficient (15.2) in `d = 2` for P's SIDE24 family at `L ∈ {24, 8, 2π, 4, 3, 2}`. It also certifies that, in every direction, τ², `det V` and `Σ_{A|V}` are positive. Formula (15.2) itself is imported from P, as in `side24_v1`; this packet does not review it.

## 2. Reduction to one variable

Write `K_L(z) = q_L(z_1) q_L(z_2)` with `q_L = θ_L/θ_L(0)` and `θ_L(t) = Σ_n e^{−(t+Ln)²/2}`.
- The spectral law has independent coordinates. One coordinate has raw moments `m2, m4, m6`.
- Its cumulants are `k2 = m2`, `k4 = m4 − 3m2²` and `k6 = m6 − 15 m4 m2 + 30 m2³`.
- Derivative covariances follow the sign rule of `reviews/iba1_periodic_jet_claude_20261005`. In particular, `Cov(f_ab, f_cd) = k2²(⟨a,b⟩⟨c,d⟩ + ⟨a,c⟩⟨b,d⟩ + ⟨a,d⟩⟨b,c⟩) + k4 Σ_i a_i b_i c_i d_i`.

Take `u = (c, s)` and `w = (−s, c)`, and put `q = c²s²` and `e = cs(c² − s²)`. Then:
- `Σu⁴ = Σw⁴ = 1 − 2q`, `Σu²w² = 2q`, `Σu⁶ = 1 − 3q`;
- `Σu³w = −e`, `Σuw³ = e`, and `e² = q(1 − 4q)`.

With `V = (f_uu, f_uw)` and `A = f_ww`, put `α = 3k2² + k4 − 2k4 q` and `γ = k2² + 2k4 q`:

```
Var V = [[α, −k4 e], [−k4 e, γ]],   Cov(A, V) = (γ, k4 e),   Var A = α,
det V  = αγ − k4² e² = k2²(3k2² + k4) + k4(4k2² + k4) q                    (linear in q),
Σ_{A|V} = α − (γ³ + (2γ + α) k4² q(1 − 4q)) / det V,
τ²     = 6k2³ + 9k2k4(1 − 2q) + (k6 − k4²/k2)(1 − 3q)                         (linear in q).
```

The τ² identity is the `d = 2` case of the formula proved in [Math-#298](https://github.com/d6g8k5htny-coder/Math-/pull/298) and checked against #297's code in main#229 6002226634. With `det G = k2²`:

```
Φ(q) = (τ²)^{2/3} Σ_{A|V} / (8π² k2 √det V),
c_{2,L} = Γ(7/6) / (24^{1/3} √π) · ∫_0^{2π} Φ(q(θ)) dθ,   q(θ) = (1 − cos 4θ)/8.
```

Substituting `φ = 4θ` gives `∫_0^{2π} Φ(q(θ)) dθ = ∫_0^{2π} Φ((1 − cos φ)/8) dφ`.

The Gaussian reference (`k2 = 1`, `k4 = k6 = 0`) gives `det V = 3`, `Σ_{A|V} = 8/3` and `τ² = 6`. This reproduces `side24_v1`'s closed form `Γ(7/6)(3/2)^{1/3}(4/3)/(2√3 π √π)`, which is check C1.

## 3. Certified ingredients

- **Arithmetic.** Every operation uses the outward-rounded rational interval class of `coefficients/side24_v1/coefficient.py` (OpenAI), together with its enclosures of π, log, exp, real roots and Γ(7/6) (analytic Stirling remainder). The checker imports that file only after its git blob matches the pin `c2d3ff33`.
- **Moments, route 1 (image sums).** `θ_L^{(j)}(0) = Σ_n He_j(Ln) e^{−(Ln)²/2}`, truncated at `|n| ≤ n₀` with `L(n₀+1) ≥ 22`. For `y ≥ 10`, `0 < He_j(y) ≤ y^6`. The ratio of consecutive tail terms is verified below 1/2 in interval arithmetic. So each two-sided tail is at most `4·(x^6 e^{−x²/2})`, with `x = L(n₀+1)`.
- **Moments, route 2 (Poisson-dual spectral sum).** By Poisson summation, `P(X = 2πk/L) ∝ e^{−(2πk/L)²/2}`. Truncating with the same tail lemma gives an independent enclosure. Check C3 requires the two routes to intersect for every `L`.
- **Quadrature.** Trefethen–Weideman, *SIAM Rev.* 56 (2014), Thm 3.2: if a `2π`-periodic `u` is analytic with `|u| ≤ M` on `|Im φ| < a`, the `N`-point trapezoid error is at most `4πM/(e^{aN} − 1)`. The strip maps under `q = (1 − cos φ)/8` onto the filled ellipse centred `1/8` with semi-axes `cosh(a)/8` and `sinh(a)/8`.
  - **Analyticity.** Φ is analytic there when `Re τ² > 0` and `Re det V > 0`, so that the principal powers and the quotient are analytic. Both are affine in `Re q`, so the two extreme values `(1 ± cosh a)/8` decide it exactly. The strip `a` is the largest admissible dyadic value, halved.
  - **Bound M.** `M` bounds `|Φ|` on the boundary ellipse by 128 complex interval boxes. Maximum modulus applies, and conjugate symmetry covers the lower half.
  - **Node count.** `N` is chosen so the bound is below `10⁻⁴⁰`. Nodes are `q_j = sin²(πj/N)/4`, enclosed by Taylor series with alternating remainders.
- **Positivity in every direction.** τ² and `det V` are linear in `q`, so their minima over `q ∈ [0, 1/4]` are at the endpoints. `Σ_{A|V}` is enclosed on 64 subintervals, refined until positive.

## 4. Results

From `RESULTS.json`, rounded outward to 30 decimals:

| `L` | `c_{2,L}` enclosure | `c_{2,L}/c_2` | `a`, `N` | min τ² over directions |
|---|---|---|---|---|
| ref | `0.073406919306034271030135962957 … 958` | 1 | 1, 128 | 6 |
| 24 | `0.073406919306034271030135962957 … 958` | `1 ± 1e-25` | 1, 128 | 6.0000000 |
| 8 | `0.073406919277779905473535403534 … 535` | `0.99999999961509942354605845` | 1, 128 | 6.0000000 |
| 2π | `0.073405684662965293708694735170 … 171` | `0.99998318083525845730400135` | 1, 128 | 5.9997420 |
| 4 | `0.067568657600538789457649064979 … 980` | `0.92046714722959966550359775` | 1, 128 | 4.5857514 |
| 3 | `0.049879432666614182044489927839 … 840` | `0.67949224866209501388496905` | 1/4, 512 | 0.76518610 |
| 2 | `0.012617593130692105902277303954 … 955` | `0.17188561037535465056755305` | 1/64, 8192 | 1.8255735e-4 |

- **The `L = 24` enclosure lies inside `side24_v1`'s published interval** `[…427103, …427104]` (check C2). It equals the reference to far below that width, consistent with the measured anisotropy of about `4e-118` (#297).
- **The `L ∈ {8, 2π, 4, 3}` enclosures contain #297's diagnostic values** to within half a unit in their last printed digit (check C6).
- **`L = 2`.** The certified value differs from the 4096-direction diagnostic trapezoid by `1.04e-25`. The branch point of `(τ²)^{2/3}` at `Im φ ≈ 0.0412` predicts that residual for that grid: successive differences there shrink by `e^{0.0412·N_φ}`.
- **Positivity.** τ², `det V` and `Σ_{A|V}` have certified positive minima at every `L`. At `L = 2` the minimum of τ² is `Δ = 1.8256e-4`, attained on the axes.
- **Gram floors** (Astra, main#229 6002455230): `V2 ≥ 9h⁴p₁p₂` and `Δ ≥ 36h⁸p₁p₂/m2` hold at every `L` (check C7). At `L = 2` the `Δ` floor is nearly attained, with a margin of `5.6e-14`.

## 5. Checks and falsification controls

`certified_d2.py` prints `RESULTS.json` and exits 0 only if every check passes.

| Check | Content |
|---|---|
| C1 | The Gaussian reference equals `side24_v1`'s closed-form `c_2`; width `< 1e-30` |
| C2 | `L = 24` lies inside `side24_v1`'s published `d = 2` interval (pinned `ENCLOSURE.json`) |
| C3 | Image-sum and Poisson-dual moment enclosures intersect, at every `L` |
| C4 | Strip analyticity verified and quadrature bound `< 1e-40`, at every `L` |
| C5 | τ², `det V` and `Σ_{A|V}` positive in every direction, at every `L` |
| C6 | Agreement with #297's merged diagnostic values (pinned `RESULTS.json`) at `L ∈ {8, 2π, 4, 3}` |
| C7 | Astra's Gram floors, at every `L` |
| C8 | Relative enclosure width `< 1e-25`, at every `L` |
| C9 | The enclosure from a 4× coarser rule, with its own error bound, intersects the main one |

Each mutant must fail a check (exit 1); an unknown label exits 2:

| Mutant | Change | Rejected by |
|---|---|---|
| M1 | strip half-width quadrupled beyond the verified one | C4 at `L = 4` |
| M2 | transverse block not conditioned on `V` | C1 |
| M3 | wrong `det V` slope `4k2²k4 + 2k4²` | C6 at `L = 4` |
| M4 | quadrature error term dropped | C9 at `L = 4` |

## 6. Limits

- `d = 2` only. The `d = 3, 4` coefficients need a cone integral over a sphere of directions and are not attempted here.
- Formula (15.2), its prefactor and the conditional-covariance conventions are imported from P and from `side24_v1` and #297. No lifetime theorem, persistence pairing or uniform-in-`L` statement is claimed.
- The rigor rests on the correctness of `side24_v1`'s interval library (an outward rational grid of `10⁻⁸⁰`, with analytic series remainders) and on Python integer arithmetic. No floating point enters any reported bound.
- The anisotropy measures and other invariants beyond those listed are not re-certified.

## 7. Reproduction

From the repository root, with Python 3.11 and no third-party packages:

```sh
python3 -B -S reviews/side24_d2_certified_small_L_claude_20261005/certified_d2.py      # about 90 s; prints RESULTS.json
python3 -B -O -S reviews/side24_d2_certified_small_L_claude_20261005/certified_d2.py   # byte-identical
python3 -B -S reviews/side24_d2_certified_small_L_claude_20261005/certified_d2.py --mutant M1   # exit 1; likewise M2–M4
```

The workflow `.github/workflows/side24-d2-certified.yml` verifies the manifest and the three pins on `main`, replays both modes byte for byte, and rejects the mutants.
