# The compact-window coefficient `c_{B,K}` in `d = 4`: reference value and transfer to the torus for every `L ≥ 10` and every frame

**Object** `CL-C8-WINDOW-COEFFICIENT-D4-20261001-v1` · **scientific effect NONE** · declarative record, `executed: false` ·
base `main 3e0a91b` · claim: Math-#205 comment 5922418823 · companions (not on `main`): Math-#205 (Lemma S and the `d = 3` transfer,
whose §7 leaves `d ≥ 4` open), Math-#197 (the interval toolkit and the `d = 3` reference closed form), Math-#199 (the `D_3`
reduction, the Taylor quadrature, `c_{4,ref}`), Math-#201 (the closed form of `D_3`). Catalog entry C8 stays OPEN; no register,
GRAPH, STATUS or catalog surface is touched. Same GitHub account as every lane: zero organizational-independence credit. Claude
reads of this record count for nothing. The author will not merge.

## 0. Statement

Let `f` be the unit-variance stationary Gaussian field on `R⁴/(LZ⁴)` with the parent kernel `K_L` of [LP] §1, `B = [b_−, b_+]` a
birth window and `K = [k_−, k_+]` a gap window, compact and of positive length with a positive gap floor: `−∞ < b_− < b_+ < ∞` and
`0 < k_− < k_+ < ∞`. This is [LP] Theorem B's hypothesis (lines 16 and 37 of the pinned [LP]). Let `c^(4)_{B,K}` be the leading
coefficient of [LP] Theorem B for the pairs with birth in `B` and scaled gap in `K` ([LP] (11.3), §15; both stated for every `d`).
Windows outside that hypothesis are treated in §7.

**Proposition (d = 4 window coefficient).** For the reference kernel `e^{−|z|²/2}`, `c^(4)_{B,K} = c_{4,ref} F^(4)_B G_K` with the
birth factor `F^(4)_B` the one-dimensional integral (2.4) below. For the torus, for every `L ≥ 10` and every frame,
`c^(4)_{B,K}` lies in the interval computed by `window_coefficient_d4.py` from the entry box of radius `E^(4)_10 ≈ 1.501·10⁻¹⁰`.
On the C8 band `B = [0, 1]`, `K = [1/2, 2]`,

```
c^(4)_{B,K}(reference)                     = 0.000241816107038247274210322215843921349422155120948…,
c^(4)_{B,K}(torus, every L ≥ 10, every frame) ∈ [0.00024181608774072626, 0.00024181612633576979]     (relative half-width 8.0e-8),
c^(4)_{B,K}(torus, L = 24)                 = the reference digits to about 48 places (quadrature-limited).
```

The same holds on every window of §5, with relative half-width at most `9.0·10⁻⁸` at `L ≥ 10`. The full window returns `c_{4,ref}`
(Math-#199, from Math-#201's closed form of `D_3`).

## 1. The object and the reference law

As in Math-#205 §1, with `|S³| = 2π²`, frame `(u, w_1, w_2, w_3)`, `G = ∇f ∈ R⁴`, `V = (f_uu, f_uw1, f_uw2, f_uw3)`,
`A = (f_{w_i w_j})` the `3×3` transverse Hessian, `t = f_uuu`, `τ² = Var(t | G = 0)`:

```
c^(4)_{B,K} = 144 ∫_{S³} p_G(0) p_V(0) I_B(u) J_K(u) dσ(u),     I_B(u) = E[1{f ∈ B} det(A)² 1{A ≺ 0} | V = 0],
J_K(u) = ∫_K k^{4/3} φ_τ(12k) dk.                                                                          (1.1)
```

Odd and even derivatives are independent for an even kernel, so `(G, t)` is independent of `(f, V, A)`. For the reference kernel,
`Cov(∂^a f, ∂^b f) = (−1)^{|a|} ∂^{a+b} e^{−|z|²/2}|_0` in exact rationals gives `Cov V = diag(3, 1, 1, 1)`, `Cov G = I`,
`τ² = 15 − 9 = 6`, and for `(f, A_11, A_12, A_13, A_22, A_23, A_33) | V = 0`

```
C'_ref:  Var f = 2/3,  Cov(f, A_ii) = −2/3,  Var A_ii = 8/3,  Cov(A_ii, A_jj) = 2/3,  Var A_ij = 1 (i ≠ j),  all else 0;
A | f = b, V = 0  ~  −b I + Q,    Q the 3×3 GOE (diagonal variance 2, off-diagonal 1),                      (1.2)
```

that is, `f ~ N(0, 2/3)` and `A = Q − f I` with `Q` independent of `f` (rule `REFERENCE_EXACT`). This is SIDE24's reference law
`A = Q + √(2/3) Z I` (Math-#199 §0) with the scalar part identified as `−f`. The full-window value is
`I_R = D_3 = (50π + 200 arctan 2 − 228)/(9π) = 5.32318026888989689492…` (Math-#201), and
`c_{4,ref} = Γ(7/6)(3/2)^{1/3} D_3 / (8√3 π^{5/2}) = 0.0233216660029528350945…` (Math-#199). Hence
`c^(4,ref)_{B,K} = c_{4,ref} F^(4)_B G_K` with `F^(4)_B = I^ref_B / D_3` and Math-#197's gap factor
`G_K = P(7/6, 12k_+²) − P(7/6, 12k_−²)` (dimension-free).

## 2. The reference birth integral as a one-dimensional integral

Let `λ_1, λ_2, λ_3` be the eigenvalues of `Q`, with Mehta's density `|Δ(λ)| e^{−|λ|²/4} / Z_3`, `Z_3 = 48√2 π` (Math-#199 §1). By
(1.2), `I^ref_B = ∫_B φ_{2/3}(b) E[Π_i (b − λ_i)² 1{λ_max < b}] db`. Put `μ_i = λ_i − b < 0` and `T = −Σ μ_i > 0`. Then
`|λ|² = |μ|² − 2bT + 3b²`, and the `b`-dependence is the Gaussian factor `exp(−3b²/4 − 3b²/4 + bT/2)`. Its integral over `B` is exact:

```
∫_B √(3/4π) e^{−3b²/4} e^{bT/2 − 3b²/4} db = √(1/2) e^{T²/24} W_B(T),
W_B(T) = Φ(√3 (b_+ − T/6)) − Φ(√3 (b_− − T/6)).                                                           (2.1)
```

(In general `m`: `√(3/(m+3)) e^{T²/(4(m+3))} [Φ(√((m+3)/2)(b_± − T/(m+3)))]`.) **The window enters only through the total trace.** For
`B = R` this is Math-#199 (1.1). On the ordered sector `μ_3 = −a`, `μ_2 = −a − p`, `μ_1 = −a − p − q`, take `T = 3a + 2p + q`,
`s = 2p + q` and `q` as coordinates. The Jacobian is `1/6`, the region `T > s > q > 0`, and the `3!` sectors cancel it. The traceless
part gives `|μ|²/4 − T²/24 = T²/24 + s²/24 + q²/8`, so

```
I^ref_B = (1/(96π)) ∫_{T>s>q>0} P(T, s, q) e^{−T²/24 − s²/24 − q²/8} W_B(T) dq ds dT,
P = a²(a+p)²(a+p+q)² · pq(p+q) = ((T−s)/3)² · ((2T+s)² − 9q²)²/1296 · q(s² − q²)/4.                           (2.2)
```

**`P` is odd in `q`.** So the `q`-integral involves only the odd `J_k(s) = ∫_0^s q^k e^{−q²/8} dq`, which are elementary:
`J_1 = 4 − 4e^{−s²/8}` and `J_{k+2} = −4s^{k+1}e^{−s²/8} + 4(k+1)J_k`, with no `erf`. The `s`-integral then consists of incomplete Gaussian
moments `∫_0^T s^j e^{−γ s²} ds` with `γ ∈ {1/24, 1/6}`. Both layers are exact (rational polynomial algebra), and

```
F_3(T) = (4√(6π)/729) (T⁶ − 90T⁴ + 2835T² + 11340) [erf(T/(2√6)) + erf(T/√6)]
         − (8T/243)(8802 + 933T² − 2T⁴) e^{−T²/24} + (8T/243)(T⁴ − 93T² + 3132) e^{−T²/6},                   (2.3)

I^ref_B = (1/(96π)) ∫_0^∞ e^{−T²/24} F_3(T) W_B(T) dT.                                                      (2.4)
```

The script derives (2.3) and requires it to equal the displayed form coefficient by coefficient. It also checks (2.3) against a
direct float double integral of (2.2) at `T = 2, 4, 6`, to `10⁻⁶` (rule `INNER_LAYERS`).

Three controls test (2.1)–(2.4):

- **Full window (rule `D3_EXACT`).** For `B = R`, (2.4) encloses Math-#201's closed form of `D_3` to `10⁻⁴⁵`. Every factor of
  (2.3) is tested this way.
- **Same code at `m = 2` (rule `M2_CROSSCHECK`).** Here `T = 2a + p`, the exponent is `3T²/40 + p²/8`, the prefactor
  `√(3/5)/(8√(2π))`, `P = (T² − p²)² p/16`, and `W` has slope `√(5/2)(b − T/5)`. The code returns `29/6 − √6`, and on `[0,1]`,
  `[−1,1]`, `[3, 7/2]`, `[0, ∞)` and `(−∞, 0]` it returns Math-#197's `d = 3` closed form (through Owen's `T`) to `10⁻⁴⁵`. This
  tests the window factor (2.1) and its slope.
- **Independent float quadrature (rule `FLOAT_CONTROL`).** `M_3(b) = E[det(bI − Q)² 1{Q ≺ bI}]` is evaluated by Gauss–Legendre
  quadrature over the ordered eigenvalues, with Mehta's density at the shift `b`, then integrated in `b`. It agrees with (2.4) on
  `[0, 1]` and `[1, 2]` to `7·10⁻¹¹` relative. The control does not use the coordinates `(T, s, q)`, (2.3) or the window factor.

## 3. Certified quadrature

(2.4) is `Λ(b_+) − Λ(b_−)` over `96π` with `Λ(b) = ∫_0^∞ g(T) Φ(√3 b − T/(2√3)) dT`, `g = e^{−T²/24} F_3 ≥ 0`, `Λ(−∞) = 0`, and
`Λ(+∞) = 96π D_3`. The method is Math-#199 §3:

- **Cells.** On each cell of width `1/2` in `(0, 60)`, the point Taylor coefficients of `g` to order `40` at the centre are formed
  once from those of its factors (polynomials, `e^{−γT²}`, `erf(κT)`) and contracted with the cell moments.
- **The window factor.** For given `b` (or a whole interval of `b`), one evaluation multiplies these coefficients by those of
  `Φ(α − βT)`: `Φ(w_0)`, then `−(β/√(2π)) y_n/(n+1)` with `(n+1) y_{n+1} = β w_0 y_n − β² y_{n−1}`.
- **Remainder.** The order-40 remainder of the product is bounded by Cauchy's estimate at the centre on the disc of radius `6`. On
  that disc, `|Φ(α − βz)| ≤ 1 + βρ e^{β²ρ²/2}/√(2π)`, because the segment from the real point `w_0` stays within `|Im| ≤ βρ`. The
  other factor bounds are Math-#199's.
- **Tail.** Beyond `T = 60`, `0 ≤ Φ ≤ 1` and incomplete-gamma bounds apply.

Rule `QUAD_COARSE` runs the same quadrature at order `8` with cells of width `2`, where the truncation error is visible. It requires
the enclosure, remainder included, to contain `D_3`.

Each evaluation of `Λ` at an interval argument encloses `Λ` over that interval. The rescaled endpoints `b/√(1 ± ε)` of §4 are
therefore evaluated directly, with no Lipschitz bound.

## 4. The torus: Lemma S in `d = 4`, the eigenvalue floor, the image bound

**Lemma S** (Math-#205 §2) is stated there for the 4-vector `(f, A)` of `d = 3`. Its proof uses only the density comparison and
homogeneity, so it applies verbatim to the 7-vector `(f, A)` of `d = 4`, whose `det(A)²` has degree `6`. If
`(1 − ε)C'_ref ≤ C' ≤ (1 + ε)C'_ref`, then:

- The density comparison gives `p_{C'}(x) ≤ ((1+ε)/(1−ε))^{7/2} p_{(1+ε)C'_ref}(x)`.
- Homogeneity gives `E_{sC}[g] = s³ I^C_{B/√s}`.

Together:

```
(1 − ε)^{13/2}/(1 + ε)^{7/2} · I^ref_{B/√(1−ε)}  ≤  I'_B  ≤  (1 + ε)^{13/2}/(1 − ε)^{7/2} · I^ref_{B/√(1+ε)}.          (4.1)
```

**Eigenvalue floor.** The eigenvalues of `C'_ref` are:

- `1` on the three `A_ij` with `i ≠ j`;
- `2` on the traceless diagonal, twice;
- `(7 ± √37)/3` on `(f, tr A/√3)`, whose `2×2` block is `[[2/3, −2/√3], [−2/√3, 4]]`.

So `λ_min = (7 − √37)/3 = 0.3057`. This is **below `1/3`**, so SIDE24's floor and Math-#205's `ε = 3‖·‖_F` do not carry over to
`d = 4`. The script checks, by Sylvester's criterion in exact rationals, that `C'_ref − (3/10)I` and `C'_ref − 0.305 I` are positive
definite while `C'_ref − 0.306 I` and `C'_ref − I/3` are not (rule `LAMBDA_FLOOR`). Hence `ε := (10/3)‖C' − C'_ref‖_F` satisfies the
hypothesis of (4.1).

**Image bound in `d = 4`.** This is Math-#197 §3 and Math-#205 §4 with the `d = 4` shell count. The contraction bound
`|D^q φ(x)| ≤ 76|x|⁶φ(x)` (`q ≤ 6`, `|x| ≥ 1`), `|D^q φ(0)| ≤ 15` and the normalization `S ≥ 1` are dimension-free. The shell
`|n|_∞ = j` holds `(2j+1)⁴ − (2j−1)⁴ = 64j³ + 16j ≤ 80j³` points with `|n|² ≤ 4j²`, so
`Σ_{n≠0} |n|⁶ e^{−L²|n|²/2} ≤ 5120 Σ_j j⁹ e^{−L²j²/2} ≤ 10240 e^{−L²/2}`. The ratio of successive terms is at most
`2⁹ e^{−3L²/2} < 1/2` for `L ≥ 10`. Every covariance entry of the 4-jet of `K_L` (derivatives of order `≤ 6`), in every frame, is
within

```
E^(4)_L = 10240 (76 L⁶ + 15) e^{−L²/2}:    E^(4)_10 ≈ 1.5010e-10,   E^(4)_12 ≈ 1.2503e-19,   E^(4)_24 ≈ 1.2461e-111      (rule IMAGE_BOUND)
```

of its reference value; `E^(4)_L` decreases in `L`.

**Interval evaluation.** The class `Space4(E)` widens the 66 entries of the even block
`(f, f_uu, f_uw1, f_uw2, f_uw3, A_11, …, A_33)` (all but `Var f = 1`) and the 15 entries of the odd block `(f_u, f_w1, f_w2, f_w3, t)`
by `±E`. Over that box it evaluates `p_G(0) = (2π)^{−2} det(Cov G)^{−1/2}`, `p_V(0)`, `τ²` and the `7×7` Schur complement `C'` by
interval linear algebra (adjugate inverses, Laplace determinants), and `ε` with each entry's deviation the supremum over its
interval. One box bounds the integrand of (1.1) for every `u` (rule `EPSILON`):

```
ε(L ≥ 10) ≤ 8.274e-9,   ε(L ≥ 12) ≤ 6.892e-18,   ε(L = 24) ≤ 8.6e-58 (arithmetic-limited),   ε(E = 0) ≤ 5.9e-59;
τ²(L ≥ 10) ∈ [5.9999999894, 6.0000000106],   p_G p_V (L ≥ 10) ∈ [0.0003704417259359, 0.0003704417263438]   (reference (2π)^{−4}/√3).
```

Then `c^(4)_{B,K} ∈ 144 · 2π² · [p_G p_V] · (4.1)(I^ref, ε) · J_K(τ²)`, with `J_K` by Math-#197 (2.2) at the interval `τ²`.

**Two exact tests of (4.1) as implemented.**

1. *Scalar perturbation (rule `SANDWICH_EXACT_SCALING`).* For `C' = (1 + η)C'_ref`, the exact value
   `(1 + η)³ I^ref_{B/√(1+η)}` lies inside the bracket for `ε = |η|`. This is checked for `η = ±1/50` on `[0, 1]`, `[3, 7/2]` and
   `[−7/2, −3]`; on the last two the rescaling dominates.
2. *Non-scalar, tilted perturbation (rule `TILTED_EXACT`).*
   - **Model.** Take `A = Q − gI` with `g = μf + σZ`, where `f ~ N(0, v)` and `Z` is an independent standard normal. Choose
     `(v, μ, σ²) = (17/25, 33/34, 133/5100)`, so that `μ²v + σ² = 2/3`. This moves `Var f` and `Cov(f, A_ii)` but not the law of `A`,
     so `C'` is not a multiple of `C'_ref`, and `ε = (10/3)·√10/150 = 0.0703`.
   - **Exact value.** `I'_B` follows from the same reduction. Conditioning on `f = b` and integrating `g` exactly changes only the
     prefactor `(2vAD)^{−1/2}`, the slope `√(2A)` and the centre `c'T` of the window factor. Here `D = 1 + 3σ²/2`,
     `A = 1/(2v) + 3μ²/(4D)` and `c' = μ/(4AD) = 33/200`. The outer Gaussian `e^{−T²/24}` is unchanged.
   - **Checks.** On `B = R` the tilted value equals `D_3`, as it must, since the law of `g` is that of the reference shift. On `[0, 1]`
     and `[1, 2]` it differs from the reference by `5.9 %` and `1.0 %` and lies inside its bracket (4.1).

## 5. Values (`RESULTS.json`)

`F^(4)_B = I^ref_B/D_3`, `G_K` is Math-#197's, and `c^(4,ref) = c_{4,ref} F^(4)_B G_K`. Displayed intervals are rounded outward (lower
endpoints down, upper endpoints up) and contain the certified intervals of `RESULTS.json`; every `…`-terminated digit string is a common
prefix of a certified interval's endpoints (both checked mechanically before publication).

| `B` | `K` | `F^(4)_B` | `c^(4)` reference | torus, every `L ≥ 10`, every frame |
|---|---|---|---|---|
| `[0,1]` | `[1/2,2]` | `0.15390330006768…` | `0.0002418161070382472742…` | `[0.00024181608774072626, 0.00024181612633576979]` |
| `[0,1]` | `(0,∞)` | `0.15390330006768…` | `0.0035892813609306973172…` | `[0.00358928109253599678, 0.00358928162932541748]` |
| `[−1,1]` | `[1/2,2]` | `0.16030200166098…` | `0.0002518698817702562001…` | `[0.00025186986157436282, 0.00025186990196615116]` |
| `[−2,2]` | `[1/2,2]` | `0.68011507457563…` | `0.0010686111317923825650…` | `[0.00106861104288191615, 0.00106861122070285613]` |
| `[0,∞)` | `[1/2,2]` | `0.99357136828676…` | `0.0015611202634258783862…` | `[0.00156112012373210018, 0.00156112040311966873]` |
| `(−∞,0]` | `[1/2,2]` | `0.00642863171323…` | `0.0000101008015669100341…` | `[0.00001010080066305966, 0.00001010080247076049]` |
| `R` | `[1/2,2]` | `1` | `0.0015712210649927884204…` | `[0.00157122092439515984, 0.00157122120559042922]` |
| `R` | `(0,∞)` | `1` | `0.0233216660029528350945…` (= `c_{4,ref}`) | `[0.02332166403326801449, 0.02332166797263781719]` |

`RESULTS.json` lists all twelve window pairs; each `L ≥ 10` enclosure contains its reference value. At `L = 24` every enclosure
agrees with the reference to about 48 digits, and the full window contains Math-#199's `c_{4,ref}`, whose `c_{4,24}` equals it to
`1.6e-108` (rule `C4_CONSISTENT`).

**How the birth mass moves with dimension.** The C8 band `B = [0, 1]` carries:

| `d` | share of the birth mass |
|---|---|
| 2 | `48.3 %` |
| 3 | `34.6 %` |
| 4 | **`15.4 %`** |

The negative half-line carries `0.64 %` in `d = 4`, against `4.6 %` in `d = 3`. The reason is that `f` must exceed the largest
eigenvalue of a larger GOE matrix. The gap factor is dimension-free (`6.74 %`). On the band, `c^(4)_{B,K}/c_{4,ref} = 1.04 %`.

## 6. Rules, mutants, verification

`python3 -B -S window_coefficient_d4.py` (also `-B -O -S`; about a minute) prints `RESULTS.json`. It exits `0` only if all eighteen
rules hold:

| rule | what it requires |
|---|---|
| `REFERENCE_EXACT` | the reference law (1.2), and that the tilted covariance at `(2/3, 1, 0)` is `C'_ref` |
| `LAMBDA_FLOOR` | the eigenvalue floor of §4 |
| `INNER_LAYERS` | (2.3) exact and against the float double integral |
| `D3_EXACT` | the full window encloses Math-#201's `D_3` |
| `QUAD_COARSE` | the coarse quadrature with its remainder contains `D_3` |
| `M2_CROSSCHECK` | the `m = 2` run reproduces `29/6 − √6` and Math-#197's windows |
| `FLOAT_CONTROL` | the eigenvalue float quadrature agrees with (2.4) |
| `IMAGE_BOUND` | the values of `E^(4)_L` |
| `EPSILON` | the values of `ε` |
| `SANDWICH_EXACT_SCALING` | exact scalar perturbations lie inside (4.1) |
| `TILTED_EXACT` | the tilted perturbation lies inside (4.1) |
| `FACTORIZATION` | the pipeline at `E = 0` reproduces `c_{4,ref} F^(4)_B G_K` on the band and on the full window |
| `C4_CONSISTENT` | agreement with Math-#199's `c_{4,ref}` |
| `NESTING` | every `L ≥ 10` enclosure contains the reference, and the band's meets the `10³⁰`-times narrower `L = 24` one |
| `WIDTHS` | relative half-width below `10⁻⁷` at `L ≥ 10` |
| `SANDWICH_ORDERED` | every bracket comes out in order |
| `LIBRARY_EXACT` | exp, sqrt and negation against exact rational brackets |
| `PINNED` | the quoted digits |

Eleven mutants exit `1` in both interpreter modes:

| mutant | change |
|---|---|
| `image-shells` | `64j³` shells |
| `d3-floor` | the `d = 3` floor `1/3` |
| `sandwich-swap` | the two rescalings exchanged |
| `window-scale` | `B·s` for `B/s` |
| `trace-slope` | the window factor's centre `T/5` for `T/6` |
| `moment-recurrence` | `j` for `j + 1` in the moment recurrence |
| `remainder-dropped` | the Cauchy remainder omitted |
| `schur-sign` | the sign of the Schur complement flipped |
| `tau-cross` | `Cov(t, f_u)` dropped |
| `sphere` | `4π` for `2π²` |
| `tilt-gamma` | the `σ²` term dropped from the tilted exponent |

The hosted workflow replays the manifest, the pins, both modes byte for byte, and the mutants.

## 7. What this does not do

- It encloses `c^(4)_{B,K}` for the reference kernel and the torus. It does not revalidate [LP] Theorem B and §15, which it
  consumes at their scope, and it does not review Math-#197, #199, #201 or #205.
- It does not cover `d ≥ 5`. Lemma S holds in every `d` (`n = 1 + m(m+1)/2` coordinates, degree `2m`), and (2.1) puts the window on
  the total trace in every `d`. In `d = 5`, however, the inner integrals over the differences have one more layer, and Math-#202's
  closed form of `D_4` integrates in a different order, so that layer is not supplied here. The floor must also be re-derived:
  `λ_min = ((2m+8)/3 − √(((2m+8)/3)² − 16/3))/2`, which is `0.2630` at `m = 4`.
- **Windows outside [LP] Theorem B's hypothesis.** Theorem B assumes compact windows of positive length with a positive gap floor:
  `−∞ < b_− < b_+ < ∞` and `0 < k_− < k_+ < ∞`. Three kinds of window fall outside it:
  - a gap window that touches `k = 0` or `∞`, such as the tabulated `K = (0,∞)`;
  - an unbounded `B`: `[0,∞)`, `(−∞,0]`, `R`;
  - a singleton window, `b_− = b_+` or `k_− = k_+`. There (1.1) is zero and does not inherit Theorem B's positive coefficient. No
    singleton window is tabulated.

  For these windows the values are the coefficient integrals (1.1) on those sets only. Theorem B's asymptotic statement is not
  extended to them; the full window is [LP] (15.2)'s `c_{4,L}`.
- It does not address `C`, `r_*` or `z_*`. C8 stays OPEN; no register surface is touched; `executed: false`. The replay workflow
  follows the repository's per-packet convention; the owner's open decision on such workflows (Math-#202/#204) applies here too.

## 8. Provenance

**Pins on `main 3e0a91b` (workflow-checked):**

- [LP] `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md`, blob `dfed3b8d`: (11.3) and §15.
- SIDE24 `coefficients/side24_v1/PROOF.md`, blob `44b66f04`: §§2–4, the image-bound pattern and the scaling argument.

**Companions, not on `main`:**

- **Math-#197** at `63e123f`, `window_coefficient.py` blob `43b4f51b`. The interval class, special functions, Owen primitives,
  incomplete gamma and `library_exact` are reused verbatim, through Math-#205's copy.
- **Math-#205** at `b875a46`, `window_coefficient_d3.py` blob `ba24b380`. The toolkit section and `I3_ref` (the `d = 3` reference
  window integral, for `M2_CROSSCHECK`) are reused verbatim; Lemma S is its §2.
- **Math-#199** at `617236d`:
  - `cone_moment_d4.py`, blob `4787d6bf`: the exact polynomial algebra, reused verbatim; the quadrature method of its §3, adapted;
    `Z_3`.
  - `RESULTS.json`, blob `187552f5`: `c_{4,ref}`.
- **Math-#201** at `3abcc10`, `closed_form_d3.py` blob `a0c91692` and `NOTE.md` blob `cbf35dea`: the closed form of `D_3`.

No external numerical library is used.

## 9. Current disposition

- **Head / owner:** see the PR's disposition block. Branch `claude/c8-window-d4-20261001` (base `main 3e0a91b`); author lane
  Anthropic / Claude (`session_017Mi3hxjaxV45x6zo6o1ee3`).
- **Claim:** the reduction (2.1)–(2.4) and its closed inner layers (2.3); the certified reference values of `c^(4)_{B,K}`; Lemma S
  in `d = 4` with the floor `3/10`; the `d = 4` image bound; the certified `ε`; the torus enclosures for every `L ≥ 10` and every
  frame, and for `L = 24`, on the windows of §5. No theorem of [LP] or SIDE24 is proved or reviewed.
- **Completed review scopes:** Codex code review at `ea3a415`, no findings. Requested nonauthor reads:

  | slice | scope |
  |---|---|
  | A | §§1–3: the reference law, (2.1)–(2.4), the quadrature |
  | B | §4: Lemma S in `d = 4`, the floor, the image bound, the entry box and `ε`, the exact tests |
  | C | §§5–7: values, rules, mutants, non-claims |

- **Unresolved finding IDs:** none.
- **Validation:** 18/18 rules in both modes, byte-identical output; 11/11 mutants rejected in both modes; workflow replayed
  locally; hosted run 4/4 green at `ea3a415`.
- **Next action:** nonauthor reads; amendments on this branch, recorded in `SOURCE_FILES.json`. Author will not merge.

## 10. Revisions

- **v1.1 (gap-window hypothesis; NOTE only).** §0 said `k_− ≥ 0`, which admits a gap window touching `k = 0`. [LP] Theorem B
  assumes `0 < k_− ≤ k_+ < ∞`, and §0 now states that hypothesis. §7 says that windows outside it, including the tabulated
  `K = (0,∞)` and the unbounded `B`, are coefficient integrals only. Codex found the same defect on Math-#213 (thread 4151593177),
  and it is repaired in every packet of the series. §9 records the Codex review. The script, `RESULTS.json`, the rules and the
  mutants are byte-unchanged.
- **v1.2 (positive-length windows; NOTE only).** C43 found on Math-#205 (review 5377957341, finding C43-205-H-01) that
  [LP] Theorem B also requires `B` and `K` to have positive length (line 37 of the pinned [LP]). The statement here allowed
  singleton windows such as `K = [1, 1]`, where (1.1) is zero. §0 now states `−∞ < b_− < b_+ < ∞` and `0 < k_− < k_+ < ∞`, and
  §7 classes singleton windows with the other windows outside the hypothesis. Every tabulated window has positive length, so no
  value changes. The script, `RESULTS.json`, the rules and the mutants are byte-unchanged.
