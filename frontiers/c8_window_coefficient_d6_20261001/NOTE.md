# The compact-window coefficient `c_{B,K}` in `d = 6`: reference value and transfer to the torus for every `L ≥ 10` and every frame

**Object** `CL-C8-WINDOW-COEFFICIENT-D6-20261001-v1` · **scientific effect NONE** · declarative record, `executed: false` ·
base `main 124c37d` · claim: Math-#213 comment 5930520277.

Companions (not on `main`):
- Math-#213: the `d = 5` record. Its `m = 4` layers become here one layer recursion for every `m ≤ 5`.
- Math-#209: the total-trace reduction and the Taylor quadrature.
- Math-#205: Lemma S.
- Math-#197: the interval toolkit, Owen's `T`, and the `d = 3` reference closed form.
- Math-#204: the certified `D_5`, `c_{6,ref}`, `Z_5`, the `d = 6` image-bound constant, and the cumulative layer for Owen-type terms.
- Math-#202 and #201: the closed forms of `D_4` and `D_3`.

Catalog entry C8 stays OPEN; no register, GRAPH, STATUS or catalog surface is touched. Same GitHub account as every lane: zero
organizational-independence credit. Claude reads of this record count for nothing. The author will not merge.

## 0. Statement

Let `f` be the unit-variance stationary Gaussian field on `R⁶/(LZ⁶)` with the parent kernel `K_L` of [LP] §1. Let `B = [b_−, b_+]`
be a birth window and `K = [k_−, k_+]` a gap window, compact and of positive length with a positive gap floor:
`−∞ < b_− < b_+ < ∞` and `0 < k_− < k_+ < ∞`. This is [LP] Theorem B's hypothesis (lines 16 and 37 of the pinned [LP]). Let
`c^(6)_{B,K}` be the leading coefficient of [LP] Theorem B for the pairs with birth in `B` and scaled gap in `K` ([LP] (11.3), §15;
both stated for every `d`). Windows outside that hypothesis are treated in §7.

**Proposition (d = 6 window coefficient).**
- **Reference kernel.** `c^(6)_{B,K} = c_{6,ref} F^(6)_B G_K`, with the birth factor `F^(6)_B` given by the one-dimensional integral
  (2.3) below.
- **Torus.** For every `L ≥ 10` and every frame, `c^(6)_{B,K}` lies in the interval computed by `window_coefficient_d6.py` from the
  entry box of radius `E^(6)_10 ≈ 4.610·10⁻⁹`.

On the C8 band `B = [0, 1]`, `K = [1/2, 2]`:

```
c^(6)_{B,K}(reference)                     = 0.000004147268276047706822538464047034235965965259540700346…,
c^(6)_{B,K}(torus, every L ≥ 10, every frame) ∈ [0.0000041472119578916668252, 0.0000041473245949635375804]   (relative half-width 1.36e-5),
c^(6)_{B,K}(torus, L = 24)                 = the reference digits to about 50 places (quadrature-limited).
```

The same holds on every window of §5, with relative half-width at most `1.6·10⁻⁵` at `L ≥ 10`. The full window returns
`c_{6,ref}`, Math-#204's value, and narrows its `D_5` enclosure from width `3.9·10⁻³⁷` to `8.8·10⁻⁵⁵`.

## 1. The object and the reference law

The setup is Math-#209 §1 with `|S⁵| = π³` and frame `(u, w_1, …, w_5)`:
- `G = ∇f ∈ R⁶`;
- `V = (f_uu, f_uw1, …, f_uw5)`;
- `A` is the `5×5` transverse Hessian;
- `t = f_uuu`.

```
c^(6)_{B,K} = 144 ∫_{S⁵} p_G(0) p_V(0) I_B(u) J_K(u) dσ(u),     I_B(u) = E[1{f ∈ B} det(A)² 1{A ≺ 0} | V = 0].            (1.1)
```

For the reference kernel, `Cov V = diag(3, 1, 1, 1, 1, 1)`, `Cov G = I` and `τ² = 6`. For the 16-vector `(f, A_11, A_12, …, A_55) | V = 0`:

```
C'_ref:  Var f = 2/3,  Cov(f, A_ii) = −2/3,  Var A_ii = 8/3,  Cov(A_ii, A_jj) = 2/3,  Var A_ij = 1 (i ≠ j),  all else 0;
A | f = b, V = 0  ~  −b I + Q,    Q the 5×5 GOE (diagonal variance 2, off-diagonal 1).                                  (1.2)
```

This is checked by rule `REFERENCE_EXACT`.

## 2. The reference birth integral

Math-#209 (2.1) in general `m` puts the window on the total trace `T = −Σ μ_i`. For `m = 5`, use the ordered sector `μ_5 = −a`,
`μ_4 = −a − p_1`, …, `μ_1 = −a − p_1 − … − p_4` and the coordinates

```
T = 5a + 4p_1 + 3p_2 + 2p_3 + p_4,   w′ = 4p_1 + 3p_2 + 2p_3 + p_4,   w = 3p_2 + 2p_3 + p_4,   s = 2p_3 + p_4,   q = p_4
(Jacobian 1/120, region T > w′ > w > s > q > 0).
```

The `5!` sectors cancel the Jacobian, and the exponent decouples exactly:
`|μ|²/4 − T²/32 = 3T²/160 + w′²/80 + w²/48 + s²/24 + q²/8`. The coefficients `1/8, 1/24, 1/48, 1/80` are `1/(8·(1, 3, 6, 10))`, as in
Math-#204. With Mehta's `Z_5 = 46080 π^{3/2}`:

```
I^ref_B = (√(3/8)/(46080 π^{3/2})) ∫_{T>w′>w>s>q>0} P e^{−3T²/160 − w′²/80 − w²/48 − s²/24 − q²/8} W_B(T) dq ds dw dw′ dT,
P = Π μ_i² · Π_{i<j} (μ_i − μ_j),     W_B(T) = Φ(2(b_+ − T/8)) − Φ(2(b_− − T/8)).                                    (2.1)
```

**Four layers in closed form.** The script integrates (2.1) layer by layer in exact rationals, by one recursion valid for every
`m ≤ 5` (at `m = 4` it reproduces Math-#213's stated `F_4` exactly). Each layer integrates `y^j e^{−c y²}` times a kind:
`1`, `e^{−γy²}`, `E_g(y) = ∫_0^y e^{−g s²} ds`, or `e^{−αy²} E_g(y)`. The last reduces by parts to the others plus the Owen-type
`K_{α,g}(T) = ∫_0^T e^{−αy²} E_g(y) dy`.
- **The `q`-layer.** The reflection `q ↦ −q` at fixed `(T, w′, w, s)` exchanges `μ_1` and `μ_2`, so `P` is odd in `q` and only the
  elementary odd `J_k` occur.
- **The `s`-layer** gives incomplete Gaussian moments; the constant kind it generates is zero.
- **The `w`-layer** (`c = 1/48`) is Math-#213's: the Owen-type kinds `K_{1/48,1/24}` and `K_{1/48,1/6}`, the constant and `E_{3/16}`
  are generated and **cancel identically again**.
- **The `w′`-layer** (`c = 1/80`) is new. The constant, `E_{1/5}` and `E_{3/40}` are generated and cancel. **Three Owen-type kinds
  survive:** `K_{1/80,1/16}` (from `E_{1/16}`) and `K_{1/30,1/24}`, `K_{1/30,1/6}` (from `e^{−w²/48} E_g`, since
  `1/80 + 1/48 = 1/30`).

What remains, with `R_10(T) = T¹⁰ − 700T⁸ + 176750T⁶ − 14962500T⁴ + 554203125T² + 7189875000`, is

```
F_5(T) = (192/5¹⁰) R_10(T) [3 K_{1/80,1/16}(T) + 4 K_{1/30,1/24}(T) + 8 K_{1/30,1/6}(T)]
         − (3T/500000000)(9372409T⁸ + 290979840T⁶ − 26148412800T⁴ + 4362224640000T² − 211803379200000) e^{−T²/80} E_{1/16}(T)
         + (256T/158203125)(729T⁸ − 521235T⁶ + 39341075T⁴ − 34608500625T² − 349281450000) e^{−T²/30} [E_{1/24}(T) + 2E_{1/6}(T)]
         + (256/10546875)(243T⁸ − 174960T⁶ + 7502375T⁴ − 13096721250T² − 131412150000) e^{−T²/5}
         − (1/337500000)(150240501T⁸ + 4666529880T⁶ − 113418584000T⁴ + 241731011520000T² − 1076528332800000) e^{−3T²/40},   (2.2)

I^ref_B = (√(3/8)/(46080 π^{3/2})) ∫_0^∞ e^{−3T²/160} F_5(T) W_B(T) dT,                                                 (2.3)
```

where `E_g(T) = ½√(π/g) erf(√g T)`. One polynomial `R_10` carries all three Owen-type kinds, and the pair `E_{1/24} + 2E_{1/6}` is
the same combination as in Math-#213's `F_4`.

**The Owen-type kinds are Owen's `T`.** Writing `E_g(y) = ∫_0^y e^{−gs²} ds`, substituting `s = yx` and then `x = ξ/a`,

```
K_{α,g}(T) = ∫_0^1 (1 − e^{−T²(α + g x²)}) / (2(α + g x²)) dx = (π/√(αg)) [arctan(a)/(2π) − T_Owen(√(2α) T, a)],   a = √(g/α),   (2.4)
```

with `a = √5` for `(1/80, 1/16)` and `(1/30, 1/6)`, and `a = √5/2` for `(1/30, 1/24)`. Since `a > 1`, the script evaluates
`T_Owen(h, a)` by the reflection `T(h, a) = ½[Φ(h) + Φ(ah)] − Φ(h)Φ(ah) − T(ah, 1/a)` and Math-#197's Owen series (1400 terms).

Rule `INNER_LAYERS` requires five things:
- (2.2) holds coefficient by coefficient;
- at each layer, the set of kinds that the derivation generates and that come out zero is exactly the one stated above. A missing kind
  fails the rule, so each cancellation is derived, not assumed;
- the outer exponent is `3/160`;
- the same recursion at `m = 4` reproduces Math-#213's stated `F_4` exactly;
- the interval value of (2.2) at `T = 3, 6, 10`, with (2.4) for the Owen-type kinds, agrees with a direct floating-point 4-D
  Gauss–Legendre integral of (2.1) (20 nodes per layer) to `10⁻¹⁰` relative; the observed agreement is about `10⁻¹³`.

**Controls.**
- **The cumulative layer against Owen's `T` (rule `OWEN_EXACT`).** The quadrature carries each `K_{α,g}` as a certified cumulative
  layer (§3). At the cell centres `T = 1/4` and `81/4`, and at the cut `T = 100`, its value meets (2.4), both to `10⁻⁵⁰`; for
  example `K_{1/80,1/16}(100) = 20.57651203962183075809061835089575319152259889923…`.
- **Full window (rule `D5_CERTIFIED`).** For `B = R`, (2.3) gives
  `D_5 = 44.13065187507413271036202489540263314878223806307704201…` (width `8.8·10⁻⁵⁵`). It meets Math-#204's certified interval,
  which has width `3.9·10⁻³⁷`.
- **Same code at `m = 2, 3, 4` (rule `CROSSCHECK_M2_M4`).** At `m = 2` it returns `29/6 − √6` and Math-#197's Owen-`T` closed form on
  three windows. At `m = 3` it returns Math-#201's `D_3` and Math-#209's band factor `F^(4)_{[0,1]}`. At `m = 4` it returns
  Math-#202's closed form of `D_4` and Math-#213's band factor `F^(5)_{[0,1]}`.
- **Independent outer quadrature (rule `FLOAT_CONTROL`).** The `T`-integral (2.3) by Gauss–Legendre (four panels of 48 nodes on
  `(0, 80)`), with `F_5` evaluated in floating point and `K_{α,g}` by Simpson's rule, is independent of the Taylor quadrature and of
  the cumulative layer. It agrees with (2.3) on `[0, 1]` and `[1, 2]` to `10⁻⁸` relative.

## 3. Certified quadrature

The quadrature is Math-#209 §3:

| parameter | value |
|---|---|
| Taylor order | `48` |
| cell width | `1/2` |
| range | `(0, 100)` |
| Cauchy radius | `6` |

The Owen-type kinds enter as a certified cumulative layer, the method of Math-#204 §3. At each cell centre `s_0`:
- the value of `K_{α,g}(s_0)` is the certified integral of `k = e^{−αw²} E_g(w)` over the earlier full cells, plus its integral over
  the left half of the current cell, plus a one-sided Cauchy remainder;
- the higher Taylor coefficients of `K` at `s_0` are those of `k` divided by `n`;
- the disc bound of `K` is `|K(s_0)| + ρ M_k`.

Beyond the cut, the integrand is bounded using `|K_{α,g}| ≤ π/(4√(αg))`. The Cauchy remainders sum to `6.2·10⁻⁵⁵` and the tail is
`5.4·10⁻⁶⁵`. Rule `QUAD_COARSE` runs the same quadrature at order `8` with cells of width `2`; its enclosure, remainder included, is
wide (`[7.95, 80.31]`) but must contain `D_5`.

## 4. The torus in `d = 6`

**Lemma S** (Math-#205 §2) applies verbatim to the 16-vector `(f, A)`, whose `det(A)²` has degree `10`. If
`(1 − ε)C'_ref ≤ C' ≤ (1 + ε)C'_ref`, then

```
(1 − ε)^13/(1 + ε)^8 · I^ref_{B/√(1−ε)}  ≤  I'_B  ≤  (1 + ε)^13/(1 − ε)^8 · I^ref_{B/√(1+ε)}.                             (4.1)
```

**Eigenvalue floor.** In general `m`, the eigenvalues of `C'_ref` are:
- `1` on the off-diagonal `A_ij`;
- `2` on the traceless diagonal;
- the two eigenvalues of `[[2/3, −(2/3)√m], [−(2/3)√m, (2m+6)/3]]` on `(f, tr A/√m)`. That block has determinant `4/3`.

For `m = 5` this gives `λ_min = (6 − √(92/3))/2 = 0.23113`. The `d = 5` floor `1/4` therefore fails. Rule `LAMBDA_FLOOR` checks, by
Sylvester's criterion in rationals, that `C'_ref − (23/100) I` and `C'_ref − 0.231 I` are positive definite and that
`C'_ref − 0.2312 I` and `C'_ref − I/4` are not. Hence `ε := (100/23)‖C' − C'_ref‖_F`.

**Image bound.** The shell `|n|_∞ = j` holds `(2j+1)⁶ − (2j−1)⁶ = 384j⁵ + 320j³ + 24j ≤ 728j⁵` points, with `|n|² ≤ 6j²`. So
`Σ_{n≠0}|n|⁶ e^{−L²|n|²/2} ≤ 157248 Σ_j j¹¹ e^{−L²j²/2} ≤ 314496 e^{−L²/2}` for `L ≥ 10` (successive terms have ratio at most
`2¹¹ e^{−3L²/2} < 1/2`); this is Math-#204's `E_6` constant. Every covariance entry of the 6-jet of `K_L`, in every frame, is within

```
E^(6)_L = 314496 (76 L⁶ + 15) e^{−L²/2}:    E^(6)_10 ≈ 4.6100e-9,   E^(6)_12 ≈ 3.8398e-18,   E^(6)_24 ≈ 3.8272e-110      (rule IMAGE_BOUND)
```

of its reference value. The contraction bound, `|D^q φ(0)| ≤ 15` and the normalization are dimension-free (Math-#197 §3).

**Interval evaluation.** `Space6(E)` widens by `±E` every entry of the 22-variable even block `(f, f_uu, f_uw1, …, f_uw5, A)` (253
entries; all but `Var f = 1`, which stays exact) and the 28 entries of the odd block `(f_u, f_w1, …, f_w5, t)`. Over that box it
evaluates the following by interval linear algebra (adjugate inverses, Laplace determinants):
- `p_G(0) = (2π)^{−3} det(Cov G)^{−1/2}`;
- `p_V(0) = (2π)^{−3} det(Cov V)^{−1/2}`;
- `τ²`;
- the `16×16` Schur complement `C'`.

Rule `EPSILON` checks the resulting values:

```
ε(L ≥ 10) ≤ 7.072e-7,   ε(L ≥ 12) ≤ 5.890e-16,   ε(L = 24) ≤ 3.4e-57 (arithmetic-limited),   ε(E = 0) ≤ 1.1e-58;
τ²(L ≥ 10) ∈ [5.999999511, 6.000000489],   p_G p_V (L ≥ 10) ∈ [0.000009383398295622, 0.000009383398785879]   (reference (2π)^{−6}/√3).
```

Then `c^(6)_{B,K} ∈ 144 · π³ · [p_G p_V] · (4.1)(I^ref, ε) · J_K(τ²)`.

**Exact tests of (4.1).**
- **Rule `SANDWICH_EXACT_SCALING`.** For `C' = (1 + η)C'_ref` with `η = ±1/50`, on `[0, 1]`, `[3, 7/2]` and `[−7/2, −3]`, the exact
  value `(1 + η)⁵ I^ref_{B/√(1+η)}` lies inside its own sandwich.
- **Rule `TILTED_EXACT`.** This is Math-#209's tilted pair `(v, μ, σ²) = (17/25, 33/34, 133/5100)`, which is non-scalar, with
  `ε = (100/23)·√14/150 = 0.1085`. Its exact value is evaluated through the same reduction. On `B = R` it equals `D_5`. On `[0, 1]`
  and `[1, 2]` it exceeds the reference by `29.9 %` and `7.0 %`, and lies inside (4.1).

## 5. Values (`RESULTS.json`)

`F^(6)_B = I^ref_B/D_5`, `G_K` is Math-#197's, and `c^(6,ref) = c_{6,ref} F^(6)_B G_K`, with
`c_{6,ref} = Γ(7/6) (3/2)^{1/3} D_5/(64√3 π^{7/2})` (Math-#204). Displayed intervals are rounded outward (lower endpoints down, upper
endpoints up) and contain the certified intervals of `RESULTS.json`. Every `…`-terminated digit string is a common prefix of a
certified interval's endpoints. Both properties were checked mechanically before publication.

| `B` | `K` | `F^(6)_B` | `c^(6)` reference | torus, every `L ≥ 10`, every frame |
|---|---|---|---|---|
| `[0,1]` | `[1/2,2]` | `0.00800194436361…` | `0.0000041472682760477068225384…` | `[0.0000041472119578916668252, 0.0000041473245949635375804]` |
| `[0,1]` | `(0,∞)` | `0.00800194436361…` | `0.0000615579867872192435333128…` | `[0.000061557165243731316444, 0.000061558808341600505797]` |
| `[−1,1]` | `[1/2,2]` | `0.00802638034698…` | `0.0000041599330202636062388615…` | `[0.0000041598765100768776358, 0.0000041599895312130049122]` |
| `[−2,2]` | `[1/2,2]` | `0.21153125452829…` | `0.0001096329618694244702024245…` | `[0.00010963146730285680056, 0.00010963445645615433875]` |
| `[0,∞)` | `[1/2,2]` | `0.99997555972228…` | `0.0005182699013148570581656579…` | `[0.00051826204265890159945, 0.00051827776008865107624]` |
| `(−∞,0]` | `[1/2,2]` | `0.00002444027771…` | `1.2666969903564286844701424489…·10⁻⁸` | `[1.2666777831135967712e-8, 1.2667161978872683484e-8]` |
| `R` | `[1/2,2]` | `1` | `0.0005182825682847606224525026…` | `[0.00051827470943673273541, 0.00051829042725062994893]` |
| `R` | `(0,∞)` | `1` | `0.0076928786292368482786666312…` (= `c_{6,ref}`) | `[0.0076927637782619387375, 0.0076929934819071653012]` |

`RESULTS.json` lists all twelve window pairs, and each `L ≥ 10` enclosure contains its reference value. At `L = 24` every enclosure
agrees with the reference to about 50 digits. The full window carries Math-#204's 40 certified digits of `c_{6,ref}`
(rule `C6_CONSISTENT`).

**How the band's share moves with dimension.**

| `d` | height-window share `F^(d)_{[0,1]}` (every `K`) | C8 band's share of `c_{d,ref}`, `F^(d)_{[0,1]} G_{[1/2,2]}` |
|---|---|---|
| 2 | `48.3 %` | `3.25 %` |
| 3 | `34.6 %` | `2.33 %` |
| 4 | `15.4 %` | `1.04 %` |
| 5 | `4.37 %` | `0.295 %` |
| 6 | **`0.800 %`** | **`0.0539 %`** |

The first column is the share of birth heights in `B = [0, 1]`; by the factorization `c_{B,K} = c_{d,ref} F_B G_K` it does
not depend on the gap window. The second is the C8 band's share of the whole coefficient, with the dimension-free gap factor
`G_{[1/2,2]} = 6.74 %`. Both are ratios of certified values from the separate packets, not a theorem about birth mass. The negative half-line carries `0.0024 %` of the birth heights in `d = 6`.

## 6. Rules, mutants, verification

`python3 -B -S window_coefficient_d6.py` (also `-B -O -S`; about two minutes) prints `RESULTS.json`. It exits `0` only if all
nineteen rules hold:

| rule | what it requires |
|---|---|
| `REFERENCE_EXACT` | the exact `C'_ref` and conditional law, including the tilted covariance at `(2/3, 1, 0)` |
| `LAMBDA_FLOOR` | the floor `23/100` certified; `0.2312` and `1/4` refused |
| `INNER_LAYERS` | (2.2) exact, the per-layer cancellations, `m = 4` against Math-#213, and the float 4-D integral |
| `OWEN_EXACT` | the cumulative layer meets Owen's `T` (2.4) at three points for each kind |
| `D5_CERTIFIED` | the full window meets Math-#204's `D_5`, width below `10⁻⁵⁰` |
| `QUAD_COARSE` | the coarse quadrature with its remainder contains `D_5` |
| `CROSSCHECK_M2_M4` | the `m = 2, 3, 4` runs reproduce the `d = 3, 4, 5` results |
| `FLOAT_CONTROL` | the independent outer float quadrature agrees with (2.3) |
| `IMAGE_BOUND` | the `d = 6` image-bound constant and values |
| `EPSILON` | the certified `ε` values |
| `SANDWICH_EXACT_SCALING` | exact scalar perturbations lie inside (4.1) |
| `TILTED_EXACT` | the tilted non-scalar perturbation lies inside (4.1) |
| `FACTORIZATION` | the pipeline at `E = 0` reproduces `c_{6,ref} F^(6)_B G_K` on the band and the full window |
| `C6_CONSISTENT` | agreement with Math-#204's `c_{6,ref}` |
| `NESTING` | `L ≥ 10` enclosures contain the reference; the band meets the `10³⁰`-times narrower `L = 24` enclosure |
| `WIDTHS` | relative half-width below `2·10⁻⁵` at `L ≥ 10` |
| `SANDWICH_ORDERED` | every bracket has lower ≤ upper |
| `LIBRARY_EXACT` | exp, sqrt and negation against exact rational brackets |
| `PINNED` | the pinned digits |

Fourteen mutants exit `1` in both interpreter modes:

| mutant | change | rejected by |
|---|---|---|
| `image-shells` | `384j⁵` shells (the leading term only) | `IMAGE_BOUND` |
| `d5-floor` | the `d = 5` floor `1/4` | `LAMBDA_FLOOR`, `TILTED_EXACT` |
| `sandwich-swap` | the two rescalings exchanged | `SANDWICH_EXACT_SCALING`, `SANDWICH_ORDERED` |
| `window-scale` | `B·s` for `B/s` | `SANDWICH_EXACT_SCALING`, `SANDWICH_ORDERED` |
| `trace-slope` | the window factor's centre at `T/(m+2)` instead of `T/(m+3)` | `CROSSCHECK_M2_M4`, `FLOAT_CONTROL`, `PINNED` |
| `moment-recurrence` | `j` for `j + 1` in the moment recurrence | the recursion itself (see below) |
| `remainder-dropped` | the Cauchy remainders omitted, in the quadrature and in the cumulative layer | `QUAD_COARSE` |
| `parts-sign` | the sign of the boundary term in the integration by parts | `INNER_LAYERS`, `D5_CERTIFIED`, `CROSSCHECK_M2_M4`, `QUAD_COARSE`, `FLOAT_CONTROL` and four more |
| `schur-sign` | the sign of the Schur complement | `REFERENCE_EXACT`, `LAMBDA_FLOOR`, `TILTED_EXACT` |
| `tau-cross` | `Cov(t, f_u)` dropped | `REFERENCE_EXACT`, `FACTORIZATION`, `C6_CONSISTENT`, `NESTING` |
| `sphere` | `8π²/3` (the `d = 5` sphere) for `π³` | `FACTORIZATION`, `C6_CONSISTENT`, `NESTING` |
| `tilt-gamma` | the `σ²` term dropped from the tilted exponent | `TILTED_EXACT` |
| `layer-dropped` | the zero `E_{3/16}` layer silently left out of the derivation | `INNER_LAYERS` |
| `cumulative-shift` | the cumulative layer's value at each centre without the left half cell | `OWEN_EXACT`, `D5_CERTIFIED`, `QUAD_COARSE`, `FLOAT_CONTROL` and four more |

`moment-recurrence` breaks the `w`-layer cancellation, so an Owen-type kind would enter the `w′`-layer; the recursion refuses that
case and the script exits `1` through the `ValueError`. `layer-dropped` changes no value, since the omitted layer is zero, and fails
`INNER_LAYERS` alone. `remainder-dropped` is the only mutant that `QUAD_COARSE` alone catches: without remainders the coarse
quadrature gives about `44.130659`, which misses `D_5 = 44.130651875…`.

The hosted workflow replays the manifest, the pins, both modes byte for byte, and the mutants.

## 7. What this does not do

- It encloses `c^(6)_{B,K}` for the reference kernel and the torus. It does not revalidate [LP] Theorem B and §15, which it consumes
  at their scope. It does not review Math-#197, #199, #201, #202, #204, #205, #209 or #213.
- It does not go to `d ≥ 7`. At `m = 6` one more layer (`c = 1/120`) follows the `w′`-layer, so the three Owen-type kinds of (2.2)
  would have to be integrated against a further Gaussian layer unless they cancel there; the recursion as written refuses that case.
  The floor also falls further (`0.2064` at `m = 6`).
- **Windows outside [LP] Theorem B's hypothesis.** Theorem B assumes compact windows of positive length with a positive gap floor:
  `−∞ < b_− < b_+ < ∞` and `0 < k_− < k_+ < ∞`. Three kinds of window fall outside it:
  - a gap window that touches `k = 0` or `∞`, such as the tabulated `K = (0,∞)`;
  - an unbounded `B`: `[0,∞)`, `(−∞,0]`, `R`;
  - a singleton window, `b_− = b_+` or `k_− = k_+`. There (1.1) is zero and does not inherit Theorem B's positive coefficient. No
    singleton window is tabulated.

  For these windows the values are the coefficient integrals (1.1) on those sets only. Theorem B's asymptotic statement is not
  extended to them.
- It does not address `C`, `r_*` or `z_*`. C8 stays OPEN; no register surface is touched; `executed: false`.
- The replay workflow follows the repository's per-packet convention. On the workflow question raised on Math-#202/#204, the
  xAI lane ruled keep (thread reply 4155307498, a process ruling only); this workflow is the same construction.

## 8. Provenance

**Pins on `main 124c37d` (workflow-checked; the same blobs as on `main 3e0a91b`, the base of the earlier packets):**
- [LP] `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md`, blob `dfed3b8d`.
- SIDE24 `coefficients/side24_v1/PROOF.md`, blob `44b66f04`.

**Companions, not on `main`:**
- **Math-#197** at `ebc93cd`: `window_coefficient.py` blob `43b4f51b`. The toolkit, including Owen's `T`, is reused verbatim through
  Math-#205's copy.
- **Math-#205** at `aebb4d4`: `window_coefficient_d3.py` blob `ba24b380`. Its toolkit section and `I3_ref` are reused verbatim;
  Lemma S is its §2.
- **Math-#199** at `617236d`: `cone_moment_d4.py` blob `4787d6bf`. The exact polynomial algebra is reused verbatim.
- **Math-#209** at `84a494a`: `window_coefficient_d4.py` blob `f77f7d2d`. The reduction and the quadrature; its band factor is a rule.
- **Math-#213** at `b22ff4b`: `window_coefficient_d5.py` blob `da68e6ec`. The `m = 4` layers, generalized here; its stated `F_4`
  and band factor are rules; the tilted pair and the exact tests.
- **Math-#204** at `5915af4`: `cone_moment_d6.py` blob `c5e56694` (the cumulative layer, `Z_5`, the `E_6` constant) and
  `RESULTS.json` blob `031c8bbe` (`D_5`, `c_{6,ref}`).
- **Math-#202** at `4512309`: `RESULTS.json` blob `52ce9b57` (the closed form of `D_4`, `Z_4 = 1536π`).
- **Math-#201** at `3abcc10`: `NOTE.md` blob `cbf35dea` (the closed form of `D_3`).

No external numerical library is used.

## 9. Current disposition

- **Head / owner:** see the PR's disposition block. Branch `claude/c8-window-d6-20261001` (base `main 124c37d`); author lane
  Anthropic / Claude (`session_017Mi3hxjaxV45x6zo6o1ee3`).
- **Claim:**
  - the `m = 5` total-trace reduction and its closed inner layers (2.2), including the recurring `w`-layer cancellation and the three
    surviving Owen-type kinds with their Owen-`T` form (2.4);
  - the certified reference values of `c^(6)_{B,K}` and the sharpened `D_5`;
  - Lemma S in `d = 6` with the floor `23/100`;
  - the `d = 6` image bound and the certified `ε`;
  - the torus enclosures for every `L ≥ 10` and every frame, and for `L = 24`, on the windows of §5.

  No theorem of [LP] or SIDE24 is proved or reviewed.
- **Completed review scopes:** see the PR's disposition block, which is the live record (none at opening). Requested nonauthor reads:
  - Slice A: §§1–3;
  - Slice B: §4;
  - Slice C: §§5–7.
- **Unresolved finding IDs:** none.
- **Validation:** 19/19 rules in both modes, byte-identical output; 14/14 mutants rejected in both modes; workflow replayed
  locally; hosted runs: see the PR's disposition block (pending at opening).
- **Next action:** nonauthor reads; amendments on this branch, recorded in `SOURCE_FILES.json`. The author will not merge.

## 10. Revisions

- **v1.1 (band-share wording; NOTE only).** Two caption checks on this PR, the xAI lane (Harper, comment 5932429158) and a
  scoped check (comment 5932380111; its lane is not stated), found that the table of §5, headed as the band's share of the
  birth mass, shows `F^(d)_{[0,1]}`, the share of birth heights in `B = [0, 1]` (the same for every `K`), while it read as the
  C8 band's share of the whole coefficient. §5 now labels that column as the height-window share and adds the C8 band's share
  of `c_{d,ref}`, `F^(d)_{[0,1]} G_{[1/2,2]}`. The script, `RESULTS.json`, the rules and the mutants are byte-unchanged; no
  certified value changes.
- **v1.2 (nonauthor read W3, Grok Bot agent 12, Math-#222 comment 5974639810, on `afd1c29`; NOTE §9 only).** §9 said
  "Completed review scopes: none yet" and "hosted run pending at opening", which contradicted §10 and the PR body. It now points
  to the PR's disposition block as the live record. The read found no mathematical defect. The script, `RESULTS.json`, the
  rules, the mutants and the workflow are byte-unchanged.
