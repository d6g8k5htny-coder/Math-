# The cone moment `D_6`, `c_{7,ref}` and the compact-window coefficient `c_{B,K}` in `d = 7`, with the transfer to the torus for every `L ≥ 10` and every frame

**Object** `CL-C8-WINDOW-COEFFICIENT-D7-20261001-v1` · **scientific effect NONE** · declarative record, `executed: false` ·
base `main c2f1270` · claim: Math-#222 comment 5931809506.

Companions (not on `main`):
- Math-#222: the `d = 6` record. Its layer recursion, cumulative layer and Owen's-`T` rule are extended here to `m = 6`.
- Math-#213 and #209: the `d = 5` and `d = 4` records (the reduction, the quadrature, the stated `F_4`, the band factors).
- Math-#205: Lemma S.
- Math-#197: the interval toolkit, Owen's `T`, and the `d = 3` reference closed form.
- Math-#204: the cumulative layer for Owen-type terms and the certified `D_5`.
- Math-#202 and #201: the closed forms of `D_4` and `D_3`.

Catalog entry C8 stays OPEN; no register, GRAPH, STATUS or catalog surface is touched. Same GitHub account as every lane: zero
organizational-independence credit. Claude reads of this record count for nothing. The author will not merge.

## 0. Statement

Let `f` be the unit-variance stationary Gaussian field on `R⁷/(LZ⁷)` with the parent kernel `K_L` of [LP] §1. Let `B = [b_−, b_+]`
be a birth window and `K = [k_−, k_+]` a gap window, compact and of positive length with a positive gap floor:
`−∞ < b_− < b_+ < ∞` and `0 < k_− < k_+ < ∞`. This is [LP] Theorem B's hypothesis (lines 16 and 37 of the pinned [LP]). Let
`c^(7)_{B,K}` be the leading coefficient of [LP] Theorem B for the pairs with birth in `B` and scaled gap in `K` ([LP] (11.3), §15;
both stated for every `d`). Windows outside that hypothesis are treated in §7.

**Proposition (d = 7).**
- **Cone moment.** `D_6 = E[det(A)² 1{A ≺ 0}]` for the `6×6` reference law `A = Q + √(2/3) Z I` is
  `D_6 = 155.863910787997676497686120415688971584094975568794349…` (width `7.9·10⁻⁵⁴`), and
  `c_{7,ref} = Γ(7/6)(3/2)^{1/3} D_6/(120√3 π^{9/2}) = 0.00461256991604821842117208474152043651029078658329251280…`.
  No earlier record has `D_6` or `c_{7,ref}`.
- **Reference kernel.** `c^(7)_{B,K} = c_{7,ref} F^(7)_B G_K`, with the birth factor `F^(7)_B` given by the one-dimensional
  integral (2.3) below.
- **Torus.** For every `L ≥ 10` and every frame, `c^(7)_{B,K}` lies in the interval computed by `window_coefficient_d7.py` from the
  entry box of radius `E^(7)_10 ≈ 2.198·10⁻⁸`.

On the C8 band `B = [0, 1]`, `K = [1/2, 2]`:

```
c^(7)_{B,K}(reference)                     = 2.9255026593895807106390826889043357133378490317925574…·10⁻⁷,
c^(7)_{B,K}(torus, every L ≥ 10, every frame) ∈ [2.9251167313955031078e-7, 2.9258886381073425720e-7]   (relative half-width 1.32e-4),
c^(7)_{B,K}(torus, L = 24)                 = the reference digits to about 50 places (quadrature-limited).
```

The same holds on every window of §5, with relative half-width at most `1.5·10⁻⁴` at `L ≥ 10`. The full window returns `c_{7,ref}`,
and at `L = 24` it gives `c_{7,24}` to about 50 digits.

## 1. The object and the reference law

The setup is Math-#209 §1 with `|S⁶| = 16π³/15` and frame `(u, w_1, …, w_6)`:
- `G = ∇f ∈ R⁷`;
- `V = (f_uu, f_uw1, …, f_uw6)`;
- `A` is the `6×6` transverse Hessian;
- `t = f_uuu`.

```
c^(7)_{B,K} = 144 ∫_{S⁶} p_G(0) p_V(0) I_B(u) J_K(u) dσ(u),     I_B(u) = E[1{f ∈ B} det(A)² 1{A ≺ 0} | V = 0].            (1.1)
```

For the reference kernel, `Cov V = diag(3, 1, 1, 1, 1, 1, 1)`, `Cov G = I` and `τ² = 6`. For the 22-vector
`(f, A_11, A_12, …, A_66) | V = 0`:

```
C'_ref:  Var f = 2/3,  Cov(f, A_ii) = −2/3,  Var A_ii = 8/3,  Cov(A_ii, A_jj) = 2/3,  Var A_ij = 1 (i ≠ j),  all else 0;
A | f = b, V = 0  ~  −b I + Q,    Q the 6×6 GOE (diagonal variance 2, off-diagonal 1).                                  (1.2)
```

This is checked by rule `REFERENCE_EXACT`.

## 2. The reference birth integral

Math-#209 (2.1) in general `m` puts the window on the total trace `T = −Σ μ_i`. For `m = 6`, use the ordered sector
`μ_6 = −a`, `μ_5 = −a − p_1`, …, `μ_1 = −a − p_1 − … − p_5` and the nested coordinates

```
T = 6a + 5p_1 + 4p_2 + 3p_3 + 2p_4 + p_5,   w″ = 5p_1 + … + p_5,   w′ = 4p_2 + … + p_5,   w = 3p_3 + 2p_4 + p_5,   s = 2p_4 + p_5,   q = p_5
(Jacobian 1/720, region T > w″ > w′ > w > s > q > 0).
```

The `6!` sectors cancel the Jacobian, and the exponent decouples exactly:
`|μ|²/4 − T²/36 = T²/72 + w″²/120 + w′²/80 + w²/48 + s²/24 + q²/8`; the coefficients of the inner variables are `1/(8·(1, 3, 6, 10, 15))`.
With Mehta's `Z_6` (2.5):

```
I^ref_B = (1/(√3 Z_6)) ∫_{T>w″>w′>w>s>q>0} P e^{−T²/72 − w″²/120 − w′²/80 − w²/48 − s²/24 − q²/8} W_B(T) dq ds dw dw′ dw″ dT,
P = Π μ_i² · Π_{i<j} (μ_j − μ_i),     W_B(T) = Φ((3/√2)(b_+ − T/9)) − Φ((3/√2)(b_− − T/9)).                          (2.1)
```

**Five layers in closed form.** The script integrates (2.1) layer by layer in exact rationals, by Math-#222's recursion extended to
`m = 6` (at `m = 4` and `m = 5` it reproduces Math-#213's and #222's stated `F_4` and `F_5` exactly). Each layer integrates
`y^j e^{−c y²}` times a kind: `1`, `e^{−γy²}`, `E_g(y) = ∫_0^y e^{−g s²} ds`, `e^{−αy²} E_g(y)`, or the Owen-type
`K_{α,g}(y) = ∫_0^y e^{−αx²} E_g(x) dx`.
- **The `q`-, `s`-, `w`- and `w′`-layers** generate and cancel exactly the kinds they do at `m = 5` (Math-#222 §2): the `w`-layer
  cancellation of Math-#213 occurs a third time, and the `w′`-layer leaves `K_{1/80,1/16}`, `K_{1/30,1/24}` and `K_{1/30,1/6}`.
- **The `w″`-layer** (`c = 1/120`) is new. It integrates the Owen-type kinds by parts, with `K′ = e^{−αy²} E_g`:

  ```
  ∫_0^T y^j e^{−cy²} K(y) dy = −(1/(2c)) T^{j−1} e^{−cT²} K(T) + ((j−1)/(2c)) ∫_0^T y^{j−2} e^{−cy²} K + (1/(2c)) ∫_0^T y^{j−1} e^{−(c+α)y²} E_g,
  ```

  which leaves, for even `j`, the nested kind `KK = ∫_0^T e^{−cy²} K_{α,g}(y) dy`, an integral of trivariate-orthant type. **All three
  nested kinds cancel identically**, and so do `K_{1/24,1/24}`, `K_{1/24,1/6}` (from `1/120 + 1/30 = 1/24`), `E_{1/12}`, `E_{5/24}` and
  the constant. One new Owen-type kind survives, `K_{1/48,1/16}` (from `1/120 + 1/80 = 1/48`), with the three products
  `eK = e^{−T²/120} K_{α,g}(T)`.

What remains, with

```
R_12(T) = T¹² − 1440T¹⁰ + 777600T⁸ − 174182400T⁶ + 17244057600T⁴ − 361184624640T² + 17156269670400,
S_12(T) = T¹² − 210T¹⁰ + 49125T⁸ − 7822500T⁶ + 898734375T⁴ − 66431531250T² + 2392508671875,
```

is

```
F_6(T) = (5/39366) R_12(T) K_{1/48,1/16}(T)
         − (18432/5¹²) S_12(T) e^{−T²/120} [3 K_{1/80,1/16}(T) + 4 K_{1/30,1/24}(T) + 8 K_{1/30,1/6}(T)]
         − (T/20503125000000)(123252092672T¹⁰ + 261305873316375T⁸ + 54126362457032400T⁶ + 26977353149594304000T⁴
                              − 451869635195452800000T² + 30469360222513728000000) e^{−T²/48} E_{1/16}(T)
         − (8192T/5¹¹)(27T¹⁰ − 6075T⁸ + 1429650T⁶ − 236297250T⁴ + 23876996875T² − 4306515046875) e^{−T²/24} [E_{1/24}(T) + 2E_{1/6}(T)]
         − (1/170859375000)(12354341056T¹⁰ + 15081527796345T⁸ + 4490688495364200T⁶ + 1543288909140360000T⁴
                              − 19424726020382400000T² + 696502101362688000000) e^{−T²/12}
         − (24576/5¹⁰)(9T¹⁰ − 2070T⁸ + 487800T⁶ − 81472500T⁴ + 8110196875T² − 1619841281250) e^{−5T²/24},             (2.2)

I^ref_B = (1/(√3 Z_6)) ∫_0^∞ e^{−T²/72} F_6(T) W_B(T) dT,                                                              (2.3)
```

where `E_g(T) = ½√(π/g) erf(√g T)`. The combination `3K_{1/80,1/16} + 4K_{1/30,1/24} + 8K_{1/30,1/6}` is exactly the one that carries
`F_5` in Math-#222, now multiplied by `e^{−T²/120}` and one polynomial `S_12`; the pair `E_{1/24} + 2E_{1/6}` recurs as well.

**The Owen-type kinds are Owen's `T`.** As in Math-#222 (2.4),

```
K_{α,g}(T) = (π/√(αg)) [arctan(a)/(2π) − T_Owen(√(2α) T, a)],   a = √(g/α),                                                 (2.4)
```

with `a = √3` for the new kind `(1/48, 1/16)`, `a = √5` for `(1/80, 1/16)` and `(1/30, 1/6)`, and `a = √5/2` for `(1/30, 1/24)`.

**Mehta's integral through the same layers.** With the Vandermonde alone in place of `P`, the same five layers leave, as
`T → ∞`, only `276480 K_{1/48,1/16}(T)`; every other surviving kind carries a Gaussian factor. Since
`K_{1/48,1/16}(∞) = arctan(√3)/(2√(1/768)) = 8√3π/3`,

```
Z_6 = ∫_{R⁶} |Δ(μ)| e^{−|μ|²/4} dμ = √(24π) · 276480 · 8√3π/3 = 4423680 √2 π^{3/2},                                         (2.5)
```

Mehta's closed form `2^{m/2 + m(m−1)/4} (2π)^{m/2} Π_{j ≤ m} Γ(1 + j/2)/Γ(3/2)` at `m = 6`. Rule `MEHTA_Z6` requires the surviving
kind and its constant exactly, and the interval value of `√(24π) · 276480 · K_{1/48,1/16}(∞)` to meet the closed form.

Rule `INNER_LAYERS` requires five things:
- (2.2) holds coefficient by coefficient;
- at each of the four layers, the set of kinds that the derivation generates and that come out zero is exactly the one stated above,
  including the three nested kinds. A missing kind fails the rule, so each cancellation is derived, not assumed;
- the outer exponent is `1/72`;
- the same recursion at `m = 4` and `m = 5` reproduces Math-#213's `F_4` and Math-#222's `F_5` exactly;
- the interval value of (2.2) at `T = 3, 6, 10`, with (2.4) for the Owen-type kinds, agrees with a direct floating-point 5-D
  Gauss–Legendre integral of (2.1) (16 nodes per layer) to `10⁻¹⁰` relative; the observed agreement is about `10⁻¹³`.

**Controls.**
- **The cumulative layer against Owen's `T` (rule `OWEN_EXACT`).** For each of the four Owen-type kinds, the certified cumulative
  layer (§3) meets (2.4) at the cell centres `T = 1/4` and `81/4` and at the cut `T = 120`, both to `10⁻⁵⁰`; for example
  `K_{1/48,1/16}(120) = 14.5103949138737428047526260611372458582…`, against `K_{1/48,1/16}(∞) = 8√3π/3 = 14.51039491…`.
- **`D_6` (rule `D6_CERTIFIED`).** For `B = R`, (2.3) gives `D_6` to width `7.9·10⁻⁵⁴`. The Cauchy remainders of the integral in
  (2.3), which is about `9.4·10⁹` before the prefactor, sum to `3.4·10⁻⁵²`, and its tail beyond `T = 120` is below `1.2·10⁻⁶⁵`.
- **Same code at `m = 2, …, 5` (rule `CROSSCHECK_M2_M5`).**
  - At `m = 2` it returns `29/6 − √6` and Math-#197's Owen-`T` closed form on three windows.
  - At `m = 3` it returns Math-#201's `D_3` and Math-#209's band factor `F^(4)_{[0,1]}`.
  - At `m = 4` it returns Math-#202's closed form of `D_4` and Math-#213's band factor `F^(5)_{[0,1]}`.
  - At `m = 5` it returns Math-#204's and Math-#222's `D_5` and Math-#222's band factor `F^(6)_{[0,1]}`.
- **Independent outer quadrature (rule `FLOAT_CONTROL`).** The `T`-integral (2.3) by Gauss–Legendre (four panels of 48 nodes on
  `(0, 96)`), with `F_6` evaluated in floating point and `K_{α,g}` by Simpson's rule, is independent of the Taylor quadrature and of
  the cumulative layer. It agrees with (2.3) on `R`, `[0, 1]` and `[1, 2]` to `10⁻⁹` relative.

## 3. Certified quadrature

The quadrature is Math-#222 §3, with the cut moved out for the wider outer Gaussian `e^{−T²/72}`:

| parameter | value |
|---|---|
| Taylor order | `48` |
| cell width | `1/2` |
| range | `(0, 120)` |
| Cauchy radius | `6` |

The four Owen-type kinds enter as certified cumulative layers (Math-#204 §3, Math-#222 §3); an `eK` term is the product of the
Gaussian `e^{−T²/120}` and the cumulative `K`. Beyond the cut the integrand is bounded using `|K_{α,g}| ≤ π/(4√(αg))`. Rule
`QUAD_COARSE` runs the same quadrature at order `8` with cells of width `2` on `(0, 96)`; its enclosure, remainder included, is wide
(`[21.47, 290.25]`) but must contain `D_6`.

## 4. The torus in `d = 7`

**Lemma S** (Math-#205 §2) applies verbatim to the 22-vector `(f, A)`, whose `det(A)²` has degree `12`. If
`(1 − ε)C'_ref ≤ C' ≤ (1 + ε)C'_ref`, then

```
(1 − ε)^17/(1 + ε)^11 · I^ref_{B/√(1−ε)}  ≤  I'_B  ≤  (1 + ε)^17/(1 − ε)^11 · I^ref_{B/√(1+ε)}.                            (4.1)
```

**Eigenvalue floor.** In general `m` the eigenvalues of `C'_ref` are `1` (off-diagonal `A_ij`), `2` (traceless diagonal) and the two
eigenvalues of `[[2/3, −(2/3)√m], [−(2/3)√m, (2m+6)/3]]` (determinant `4/3`). For `m = 6`, `λ_min = (10 − 2√22)/3 = 0.20639`, so
the `d = 6` floor `23/100` fails. Rule `LAMBDA_FLOOR` checks, by Sylvester's criterion in rationals, that `C'_ref − I/5` and
`C'_ref − 0.2063 I` are positive definite and that `C'_ref − 0.2064 I` and `C'_ref − (23/100) I` are not. Hence
`ε := 5‖C' − C'_ref‖_F`.

**Image bound.** The shell `|n|_∞ = j` holds `(2j+1)⁷ − (2j−1)⁷ = 896j⁶ + 1120j⁴ + 168j² + 2 ≤ 2186j⁶` points, with `|n|² ≤ 7j²`. So
`Σ_{n≠0}|n|⁶ e^{−L²|n|²/2} ≤ 749798 Σ_j j¹² e^{−L²j²/2} ≤ 1499596 e^{−L²/2}` for `L ≥ 10` (successive terms have ratio at most
`2¹² e^{−3L²/2} < 1/2`). Every covariance entry of the 7-jet of `K_L`, in every frame, is within

```
E^(7)_L = 1499596 (76 L⁶ + 15) e^{−L²/2}:   E^(7)_10 ≈ 2.1982e-8,   E^(7)_12 ≈ 1.8309e-17,   E^(7)_24 ≈ 1.8249e-109      (rule IMAGE_BOUND)
```

of its reference value. The contraction bound, `|D^q φ(0)| ≤ 15` and the normalization are dimension-free (Math-#197 §3).

**Interval evaluation.** `Space7(E)` widens by `±E` every entry of the 29-variable even block `(f, f_uu, f_uw1, …, f_uw6, A)` (435
entries; all but `Var f = 1`, which stays exact) and the 36 entries of the odd block `(f_u, f_w1, …, f_w6, t)`. Over that box it
evaluates, by interval linear algebra (adjugate inverses, Laplace determinants):
- `p_G(0) = (2π)^{−7/2} det(Cov G)^{−1/2}`;
- `p_V(0) = (2π)^{−7/2} det(Cov V)^{−1/2}`;
- `τ²`;
- the `22×22` Schur complement `C'`.

Rule `EPSILON` checks the resulting values:

```
ε(L ≥ 10) ≤ 5.183e-6,   ε(L ≥ 12) ≤ 4.317e-15,   ε(L = 24) ≤ 5.9e-57 (arithmetic-limited),   ε(E = 0) ≤ 1.3e-58;
τ²(L ≥ 10) ∈ [5.999997274, 6.000002726],   p_G p_V (L ≥ 10) ∈ [0.000001493414041908, 0.000001493414479615]   (reference (2π)^{−7}/√3).
```

Then `c^(7)_{B,K} ∈ 144 · (16π³/15) · [p_G p_V] · (4.1)(I^ref, ε) · J_K(τ²)`.

**Exact tests of (4.1).**
- **Rule `SANDWICH_EXACT_SCALING`.** For `C' = (1 + η)C'_ref` with `η = ±1/50`, on `[0, 1]`, `[3, 7/2]` and `[−7/2, −3]`, the exact
  value `(1 + η)⁶ I^ref_{B/√(1+η)}` lies inside its own sandwich.
- **Rule `TILTED_EXACT`.** Math-#209's tilted pair `(v, μ, σ²) = (17/25, 33/34, 133/5100)`, non-scalar, has `ε = 5·4/150 = 2/15`.
  Its exact value through the same reduction equals `D_6` on `B = R`, exceeds the reference by `54.4 %` on `[0, 1]` and `15.7 %` on
  `[1, 2]`, and lies inside (4.1).

## 5. Values (`RESULTS.json`)

`F^(7)_B = I^ref_B/D_6`, `G_K` is Math-#197's, and `c^(7,ref) = c_{7,ref} F^(7)_B G_K`. Displayed intervals are rounded outward and
contain the certified intervals of `RESULTS.json`; every `…`-terminated digit string is a common prefix of a certified interval's
endpoints. Both properties were checked mechanically before publication.

| `B` | `K` | `F^(7)_B` | `c^(7)` reference | torus, every `L ≥ 10`, every frame |
|---|---|---|---|---|
| `[0,1]` | `[1/2,2]` | `0.00094141218133…` | `2.9255026593895807106390826889…·10⁻⁷` | `[2.9251167313955031078e-7, 2.9258886381073425720e-7]` |
| `[0,1]` | `(0,∞)` | `0.00094141218133…` | `0.0000043423295062141521557836…` | `[0.0000043417623331335235628, 0.0000043428967531045859824]` |
| `[−1,1]` | `[1/2,2]` | `0.00094207529818…` | `2.9275633403153342751979067858…·10⁻⁷` | `[2.9271771096958928198e-7, 2.9279496217025732129e-7]` |
| `[−2,2]` | `[1/2,2]` | `0.07614120491129…` | `0.0000236613995308533540726986…` | `[0.000023658304977195847424, 0.000023664494486858627135]` |
| `[0,∞)` | `[1/2,2]` | `0.99999933686394…` | `0.0003107566247170773563595304…` | `[0.00031071098765697489980, 0.00031080226842967069477]` |
| `(−∞,0]` | `[1/2,2]` | `6.63136050961252…·10⁻⁷` | `2.0607405758006723979953119923…·10⁻¹⁰` | `[2.0604379398018453133e-10, 2.0610432559145940615e-10]` |
| `R` | `[1/2,2]` | `1` | `0.0003107568307911349364267702…` | `[0.00031071119370076887999, 0.00031080247453399628623]` |
| `R` | `(0,∞)` | `1` | `0.0046125699160482184211720847…` (= `c_{7,ref}`) | `[0.0046118985366076675777, 0.0046132413924806509402]` |

`RESULTS.json` lists all twelve window pairs, and each `L ≥ 10` enclosure contains its reference value. At `L = 24` every enclosure
agrees with the reference to about 50 digits. The general formula `Γ(7/6)(3/2)^{1/3}|S⁶|D_6/(√3√π(2π)⁷)` and the simplified one agree
(rule `C7_CONSISTENT`).

**The coefficient sequence.** With SIDE24 (`d = 2, 3`) and Math-#199, #200, #204:

| `d` | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|
| `c_{d,ref}` | `0.07341` | `0.04178` | `0.02332` | `0.01322` | `0.00769` | **`0.00461`** |
| height-window share `F^(d)_{[0,1]}` (every `K`) | `48.3 %` | `34.6 %` | `15.4 %` | `4.37 %` | `0.800 %` | **`0.0941 %`** |
| C8 band's share of `c_{d,ref}`, `F^(d)_{[0,1]} G_{[1/2,2]}` | `3.25 %` | `2.33 %` | `1.04 %` | `0.295 %` | `0.0539 %` | **`0.00634 %`** |

The second row is the share of birth heights in `B = [0, 1]`; by the factorization `c_{B,K} = c_{d,ref} F_B G_K` it does not
depend on the gap window. The third row is the C8 band's share of the whole coefficient, with the dimension-free gap factor
`G_{[1/2,2]} = 6.74 %`. Both are ratios of certified values from the separate packets, not a theorem about birth mass. The
negative half-line carries `0.000066 %` of the birth heights in `d = 7`.

## 6. Rules, mutants, verification

`python3 -B -S window_coefficient_d7.py` (also `-B -O -S`; about four minutes) prints `RESULTS.json`. It exits `0` only if all twenty
rules hold:

| rule | what it requires |
|---|---|
| `REFERENCE_EXACT` | the exact `C'_ref` and conditional law, including the tilted covariance at `(2/3, 1, 0)` |
| `LAMBDA_FLOOR` | the floor `1/5` certified; `0.2064` and `23/100` refused |
| `INNER_LAYERS` | (2.2) exact, the per-layer cancellations, `m = 4, 5` against Math-#213 and #222, and the float 5-D integral |
| `MEHTA_Z6` | (2.5): the one surviving kind, its constant, and the value against Mehta's closed form |
| `OWEN_EXACT` | the cumulative layer meets Owen's `T` (2.4) at three points for each of the four kinds |
| `D6_CERTIFIED` | `D_6` to width below `10⁻⁵⁰`, with the remainder and tail bounds |
| `QUAD_COARSE` | the coarse quadrature with its remainder contains `D_6` |
| `CROSSCHECK_M2_M5` | the `m = 2, …, 5` runs reproduce the `d = 3, …, 6` results |
| `FLOAT_CONTROL` | the independent outer float quadrature agrees with (2.3) |
| `IMAGE_BOUND` | the `d = 7` image-bound constant and values |
| `EPSILON` | the certified `ε` values |
| `SANDWICH_EXACT_SCALING` | exact scalar perturbations lie inside (4.1) |
| `TILTED_EXACT` | the tilted non-scalar perturbation lies inside (4.1) |
| `FACTORIZATION` | the pipeline at `E = 0` reproduces `c_{7,ref} F^(7)_B G_K` on the band and the full window |
| `C7_CONSISTENT` | the two forms of `c_{7,ref}` agree, and the `L ≥ 10` and `L = 24` full windows contain it |
| `NESTING` | `L ≥ 10` enclosures contain the reference; the band meets the `10³⁰`-times narrower `L = 24` enclosure |
| `WIDTHS` | relative half-width below `2·10⁻⁴` at `L ≥ 10` |
| `SANDWICH_ORDERED` | every bracket has lower ≤ upper |
| `LIBRARY_EXACT` | exp, sqrt and negation against exact rational brackets |
| `PINNED` | the pinned digits |

Sixteen mutants exit `1` in both interpreter modes:

| mutant | change | rejected by |
|---|---|---|
| `image-shells` | `896j⁶` shells (the leading term only) | `IMAGE_BOUND` |
| `d6-floor` | the `d = 6` floor `23/100` | `LAMBDA_FLOOR`, `TILTED_EXACT` |
| `sandwich-swap` | the two rescalings exchanged | `SANDWICH_EXACT_SCALING`, `SANDWICH_ORDERED` |
| `window-scale` | `B·s` for `B/s` | `SANDWICH_EXACT_SCALING`, `SANDWICH_ORDERED` |
| `trace-slope` | the window factor's centre at `T/(m+2)` instead of `T/(m+3)` | `CROSSCHECK_M2_M5`, `FLOAT_CONTROL`, `PINNED` |
| `moment-recurrence` | `j` for `j + 1` in the moment recurrence | the recursion itself (see below) |
| `remainder-dropped` | the Cauchy remainders omitted, in the quadrature and in the cumulative layers | `QUAD_COARSE` |
| `parts-sign` | the sign of the boundary term in the integration by parts of `e^{−αy²}E_g` | `INNER_LAYERS`, `MEHTA_Z6`, `D6_CERTIFIED`, `CROSSCHECK_M2_M5`, `FLOAT_CONTROL` and three more |
| `schur-sign` | the sign of the Schur complement | `REFERENCE_EXACT`, `LAMBDA_FLOOR`, `TILTED_EXACT` |
| `tau-cross` | `Cov(t, f_u)` dropped | `REFERENCE_EXACT`, `FACTORIZATION`, `C7_CONSISTENT`, `NESTING` |
| `sphere` | `π³` (the `d = 6` sphere) for `16π³/15` | `FACTORIZATION`, `C7_CONSISTENT`, `NESTING` |
| `tilt-gamma` | the `σ²` term dropped from the tilted exponent | `TILTED_EXACT` |
| `layer-dropped` | the zero `E_{3/16}` layer silently left out of the derivation | `INNER_LAYERS` |
| `cumulative-shift` | the cumulative layers' value at each centre without the left half cell | `OWEN_EXACT`, `QUAD_COARSE`, `CROSSCHECK_M2_M5`, `FLOAT_CONTROL` and three more |
| `owen-parts` | `j` for `j − 1` in the by-parts recursion for Owen-type kinds | the recursion itself (see below) |
| `mehta` | `Z_6` without its factor `√2` | `MEHTA_Z6`, `PINNED` |

Two mutants are refused by the recursion itself, and the script exits `1` through a `ValueError`:
- `moment-recurrence` breaks the `w`-layer cancellation. An Owen-type kind then enters the `w′`-layer, and its by-parts product
  `e^{−T²/80}K` enters the `w″`-layer, which the recursion refuses.
- `owen-parts` breaks the cancellation of the nested kinds, and the surviving nested kind is refused.

`layer-dropped` changes no value, since the omitted layer is zero, and fails `INNER_LAYERS` alone. `remainder-dropped` is caught by
`QUAD_COARSE` alone. `mehta` rescales `D_6` and every value by `√2` and fails `MEHTA_Z6` and `PINNED`.

The hosted workflow replays the manifest, the pins, both modes byte for byte, and the mutants.

## 7. What this does not do

- It encloses `D_6`, `c_{7,ref}` and `c^(7)_{B,K}` for the reference kernel and the torus. It does not revalidate [LP] Theorem B and
  §15, or SIDE24's (15.2) route to `c_{d,ref}`, which it consumes at their scope. It does not review Math-#197, #199, #201, #202,
  #204, #205, #209, #213 or #222.
- It does not go to `d ≥ 8`. At `m = 7` a further layer (`c = 1/168`) follows the `w″`-layer, so the Owen-type kinds of (2.2),
  including the products `e^{−T²/120}K`, would enter one more Gaussian layer; the recursion as written refuses a product kind
  entering a layer. The floor also falls further.
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

**Pins on `main c2f1270` (workflow-checked):**
- [LP] `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md`, blob `dfed3b8d`.
- SIDE24 `coefficients/side24_v1/PROOF.md`, blob `44b66f04`.

**Companions, not on `main`:**
- **Math-#222** at `0c88a56`: `window_coefficient_d6.py` blob `d38527e6` (the recursion, the cumulative layer, Owen's-`T` rule and
  the `d = 6` transfer, extended here) and `RESULTS.json` blob `df361c43` (`D_5`, `F^(6)_{[0,1]}`).
- **Math-#197** at `ebc93cd`: `window_coefficient.py` blob `43b4f51b`. The toolkit, including Owen's `T`, is reused verbatim through
  Math-#205's copy.
- **Math-#205** at `aebb4d4`: `window_coefficient_d3.py` blob `ba24b380`. Its toolkit section and `I3_ref` are reused verbatim;
  Lemma S is its §2.
- **Math-#199** at `617236d`: `cone_moment_d4.py` blob `4787d6bf`. The exact polynomial algebra is reused verbatim.
- **Math-#209** at `84a494a` and **Math-#213** at `b22ff4b`: blobs `f77f7d2d` and `da68e6ec` (the reduction, the quadrature, the
  stated `F_4`, the band factors).
- **Math-#204** at `5915af4`: `cone_moment_d6.py` blob `c5e56694` (the cumulative layer) and `RESULTS.json` blob `031c8bbe` (`D_5`).
- **Math-#202** at `4512309` (`D_4`) and **Math-#201** at `3abcc10` (`D_3`).

No external numerical library is used.

## 9. Current disposition

- **Head / owner:** see the PR's disposition block. Branch `claude/c8-window-d7-20261001` (base `main c2f1270`); author lane
  Anthropic / Claude (`session_017Mi3hxjaxV45x6zo6o1ee3`).
- **Claim:**
  - the `m = 6` total-trace reduction and its closed inner layers (2.2), including the by-parts rule for Owen-type kinds and the
    cancellation of the three nested kinds;
  - Mehta's `Z_6` through the same layers (2.5);
  - the certified `D_6`, `c_{7,ref}` and reference values of `c^(7)_{B,K}`;
  - Lemma S in `d = 7` with the floor `1/5`;
  - the `d = 7` image bound and the certified `ε`;
  - the torus enclosures for every `L ≥ 10` and every frame, and for `L = 24`, on the windows of §5.

  No theorem of [LP] or SIDE24 is proved or reviewed.
- **Completed review scopes:** none yet. Requested nonauthor reads:
  - Slice A: §§1–3;
  - Slice B: §4;
  - Slice C: §§5–7.
- **Unresolved finding IDs:** none.
- **Validation:** 20/20 rules in both modes, byte-identical output; 16/16 mutants rejected in both modes; workflow replayed
  locally; hosted run pending at opening.
- **Next action:** nonauthor reads; amendments on this branch, recorded in `SOURCE_FILES.json`. The author will not merge.

## 10. Revisions

- **v1.1 (band-share wording; NOTE only).** The xAI lane (Harper, Math-#222 comment 5932429158) found that the series' row
  headed as the band's share of the birth mass shows `F^(d)_{[0,1]}`, the share of birth heights in `B = [0, 1]` (the same for
  every `K`), while it read as the C8 band's share of the whole coefficient. §5 now labels that row as the height-window share
  and adds a row with the C8 band's share of `c_{d,ref}`, `F^(d)_{[0,1]} G_{[1/2,2]}`. The script, `RESULTS.json`, the rules
  and the mutants are byte-unchanged; no certified value changes.
- **v1.2 (nonauthor read W4, Grok Bot agent 8, Math-#226 comment 5974704137, on `e6ba833`; NOTE only).** With the ordering
  `μ_1 < … < μ_6` of §2, every factor `μ_i − μ_j` with `i < j` is negative, and at `m = 6` there are 15 of them, so the product
  displayed in (2.1) was `−|Δ(μ)|`. (2.1) now reads `Π_{i<j} (μ_j − μ_i) = |Δ(μ)|`, which is what the script, (2.2) and every
  certified value use. At `m = 4` and `m = 5` (6 and 10 pairs) the inherited form had the right sign. The script,
  `RESULTS.json`, the rules and the mutants are byte-unchanged; no certified value changes.
