# The compact-window coefficient `c_{B,K}` in `d = 5`: reference value and transfer to the torus for every `L ≥ 10` and every frame

**Object** `CL-C8-WINDOW-COEFFICIENT-D5-20261001-v1` · **scientific effect NONE** · declarative record, `executed: false` ·
base `main 3e0a91b` · claim: Math-#209 comment 5923710923.

Companions (not on `main`):
- Math-#209: the `d = 4` record, whose total-trace reduction and Taylor quadrature this record extends to `m = 4`.
- Math-#205: Lemma S.
- Math-#197: the interval toolkit and the `d = 3` reference closed form.
- Math-#200: `c_{5,ref}` and the `d = 5` image-bound constant.
- Math-#202: the closed form of `D_4`.

Catalog entry C8 stays OPEN; no register, GRAPH, STATUS or catalog surface is touched. Same GitHub account as every lane: zero
organizational-independence credit. Claude reads of this record count for nothing. The author will not merge.

## 0. Statement

Let `f` be the unit-variance stationary Gaussian field on `R⁵/(LZ⁵)` with the parent kernel `K_L` of [LP] §1. Let `B = [b_−, b_+]`
be a birth window and `K = [k_−, k_+]` a gap window, compact and of positive length with a positive gap floor:
`−∞ < b_− < b_+ < ∞` and `0 < k_− < k_+ < ∞`. This is [LP] Theorem B's hypothesis (lines 16 and 37 of the pinned [LP]). Let
`c^(5)_{B,K}` be the leading coefficient of [LP] Theorem B for the pairs with birth in `B` and scaled gap in `K` ([LP] (11.3), §15;
both stated for every `d`). Windows outside that hypothesis are treated in §7.

**Proposition (d = 5 window coefficient).**
- **Reference kernel.** `c^(5)_{B,K} = c_{5,ref} F^(5)_B G_K`, with the birth factor `F^(5)_B` given by the one-dimensional integral
  (2.4) below.
- **Torus.** For every `L ≥ 10` and every frame, `c^(5)_{B,K}` lies in the interval computed by `window_coefficient_d5.py` from the
  entry box of radius `E^(5)_10 ≈ 8.868·10⁻¹⁰`.

On the C8 band `B = [0, 1]`, `K = [1/2, 2]`:

```
c^(5)_{B,K}(reference)                     = 0.0000389351131406652779000208375489243154126558…,
c^(5)_{B,K}(torus, every L ≥ 10, every frame) ∈ [0.0000389350650058931493, 0.0000389351612754962131]   (relative half-width 1.24e-6),
c^(5)_{B,K}(torus, L = 24)                 = the reference digits to about 50 places (quadrature-limited).
```

The same holds on every window of §5, with relative half-width at most `1.4·10⁻⁶` at `L ≥ 10`. The full window returns
`c_{5,ref}`: Math-#200's value, from Math-#202's closed form of `D_4`.

## 1. The object and the reference law

The setup is Math-#209 §1 with `|S⁴| = 8π²/3` and frame `(u, w_1, …, w_4)`:
- `G = ∇f ∈ R⁵`;
- `V = (f_uu, f_uw1, …, f_uw4)`;
- `A` is the `4×4` transverse Hessian;
- `t = f_uuu`.

```
c^(5)_{B,K} = 144 ∫_{S⁴} p_G(0) p_V(0) I_B(u) J_K(u) dσ(u),     I_B(u) = E[1{f ∈ B} det(A)² 1{A ≺ 0} | V = 0].            (1.1)
```

For the reference kernel, `Cov V = diag(3, 1, 1, 1, 1)`, `Cov G = I` and `τ² = 6`. For the 11-vector `(f, A_11, A_12, …, A_44) | V = 0`:

```
C'_ref:  Var f = 2/3,  Cov(f, A_ii) = −2/3,  Var A_ii = 8/3,  Cov(A_ii, A_jj) = 2/3,  Var A_ij = 1 (i ≠ j),  all else 0;
A | f = b, V = 0  ~  −b I + Q,    Q the 4×4 GOE (diagonal variance 2, off-diagonal 1).                                  (1.2)
```

This is checked by rule `REFERENCE_EXACT`.

## 2. The reference birth integral

Math-#209 (2.1) in general `m` puts the window on the total trace `T = −Σ μ_i`, with factor
`√(3/(m+3)) e^{T²/(4(m+3))} [Φ(√((m+3)/2)(b_± − T/(m+3)))]`. For `m = 4`, use the ordered sector `μ_4 = −a`, `μ_3 = −a − p_1`,
`μ_2 = −a − p_1 − p_2`, `μ_1 = −a − p_1 − p_2 − p_3` and the coordinates

```
T = 4a + 3p_1 + 2p_2 + p_3,   w = 3p_1 + 2p_2 + p_3,   s = 2p_2 + p_3,   q = p_3      (Jacobian 1/24, region T > w > s > q > 0).
```

The `4!` sectors cancel the Jacobian, and the exponent decouples exactly (checked symbolically):
`|μ|²/4 − T²/28 = 3T²/112 + w²/48 + s²/24 + q²/8`. With `Z_4 = 1536π`:

```
I^ref_B = (√(3/7)/(1536π)) ∫_{T>w>s>q>0} P e^{−3T²/112 − w²/48 − s²/24 − q²/8} W_B(T) dq ds dw dT,
P = Π μ_i² · Π_{i<j} (μ_i − μ_j),     W_B(T) = Φ(√(7/2)(b_+ − T/7)) − Φ(√(7/2)(b_− − T/7)).                       (2.1)
```

**Three layers in closed form.**
- **The `q`-layer.** The reflection `q ↦ −q` at fixed `(T, w, s)` exchanges `μ_1` and `μ_2`, so `P` is odd in `q`. The `q`-layer
  therefore involves only the elementary odd `J_k` (209 terms).
- **The `s`-layer** gives incomplete Gaussian moments, as in Math-#209.
- **The `w`-layer.** Here `∫_0^T w^j e^{−w²/48} E_g(w) dw`, with `E_g(w) = ½√(π/g) erf(√g w)`, reduces by parts to elementary terms
  plus the Owen-type `L_0 = ∫_0^T e^{−w²/48} E_g(w) dw` (`g = 1/24, 1/6`). **Both Owen-type terms cancel identically.** So do the
  constant and `E_{3/16}` terms. The script derives the cancellation in exact rationals, and rule `INNER_LAYERS` requires it.

What remains is

```
F_4(T) = −(T/31104)(991830528 − 18489408T² + 346856T⁴ − 729T⁶) e^{−T²/16}
         + (3/1024)(T⁸ − 288T⁶ + 28800T⁴ − 522240T² + 11243520) · 2√π erf(T/4)
         − (256/729)(T⁶ + 45T⁴ + 405T² + 405) e^{−T²/48} · √(6π)[erf(T/(2√6)) + erf(T/√6)]
         − (512/243) T (T⁴ + 42T² + 297) e^{−3T²/16},                                                            (2.2)

I^ref_B = (√(3/7)/(1536π)) ∫_0^∞ e^{−3T²/112} F_4(T) W_B(T) dT.                                                    (2.3)
```

The bracket `√(6π)[erf(T/(2√6)) + erf(T/√6)]` is the same combination that carries Math-#209's `F_3`. Rule `INNER_LAYERS` requires
three things. First, (2.2) holds coefficient by coefficient. Second, the set of kinds that the derivation generates and that come
out zero is exactly the four stated: the two Owen-type kinds (`g = 1/24, 1/6`), the constant, and `E_{3/16}`. A missing kind fails
the rule, so the cancellation is derived, not assumed. Third, (2.2) agrees with a direct float triple integral of (2.1) at `T = 3, 6`
to `10⁻⁶`.

**Controls.**
- **Full window (rule `D4_EXACT`).** For `B = R`, (2.3) encloses Math-#202's closed form
  `D_4 = 6695/54 − (405/32)√6 − (1/π)[(1375/72)√21 + (6695/27) arctan(√21/7) + (405/16)√6 arctan(√14/14)] = 14.2187634589773576…`
  to `10⁻⁴⁵`.
- **Same code at `m = 2` and `m = 3` (rule `CROSSCHECK_M2_M3`).** At `m = 2` it returns `29/6 − √6` and Math-#197's Owen-`T` closed
  form on three windows. At `m = 3` it returns Math-#201's `D_3` and Math-#209's band factor `F^(4)_{[0,1]}`.
- **Independent float quadrature (rule `FLOAT_CONTROL`).** `M_4(b) = E[det(bI − Q)² 1{Q ≺ bI}]` is evaluated by Gauss–Legendre
  quadrature (28 nodes per eigenvalue gap) with Mehta's density at the shift `b`, then integrated in `b`. It agrees with (2.3) on
  `[0, 1]` and `[1, 2]` to `10⁻⁸` relative; the observed agreement is about `10⁻¹⁰`.

## 3. Certified quadrature

The quadrature is Math-#209 §3 unchanged in method:

| parameter | value |
|---|---|
| Taylor order | `48` |
| cell width | `1/2` |
| range | `(0, 80)` |
| Cauchy radius | `6` |

The outer Gaussian `e^{−3T²/112}` is wider than in `d = 4`, hence the longer range. Two rigorous fast paths are added:
- For `|x| ≥ 12`, `erf(x)` is enclosed by `[1 − e^{−x²}/(x√π), 1]`, since `0 < erfc(x) < e^{−x²}/(x√π)`. The same bound encloses
  `Φ` at large arguments.
- The Taylor coefficients of the Gaussian and `erf` factors are cached per cell.

Rule `QUAD_COARSE` runs the same quadrature at order `8` with cells of width `2`. It requires the enclosure, remainder included, to
contain `D_4`.

## 4. The torus in `d = 5`

**Lemma S** (Math-#205 §2) applies verbatim to the 11-vector `(f, A)`, whose `det(A)²` has degree `8`. If
`(1 − ε)C'_ref ≤ C' ≤ (1 + ε)C'_ref`, then

```
(1 − ε)^{19/2}/(1 + ε)^{11/2} · I^ref_{B/√(1−ε)}  ≤  I'_B  ≤  (1 + ε)^{19/2}/(1 − ε)^{11/2} · I^ref_{B/√(1+ε)}.           (4.1)
```

**Eigenvalue floor.** In general `m`, the eigenvalues of `C'_ref` are:
- `1` on the off-diagonal `A_ij`;
- `2` on the traceless diagonal;
- the two eigenvalues of `[[2/3, −(2/3)√m], [−(2/3)√m, (2m+6)/3]]` on `(f, tr A/√m)`. That block has determinant `4/3`.

For `m = 4` this gives `λ_min = (8 − 2√13)/3 = 0.2630`. The `d = 4` floor `3/10` therefore fails. Rule `LAMBDA_FLOOR` checks, by
Sylvester's criterion in rationals, that `C'_ref − I/4` and `C'_ref − 0.262 I` are positive definite and that `C'_ref − 0.263 I` and
`C'_ref − (3/10) I` are not. Hence `ε := 4‖C' − C'_ref‖_F`.

**Image bound.** The shell `|n|_∞ = j` holds `(2j+1)⁵ − (2j−1)⁵ = 160j⁴ + 80j² + 2 ≤ 242j⁴` points, with `|n|² ≤ 5j²`. So
`Σ_{n≠0}|n|⁶ e^{−L²|n|²/2} ≤ 30250 Σ_j j¹⁰ e^{−L²j²/2} ≤ 60500 e^{−L²/2}` for `L ≥ 10`; this is Math-#200's `E_5` constant. Every
covariance entry of the 5-jet of `K_L`, in every frame, is within

```
E^(5)_L = 60500 (76 L⁶ + 15) e^{−L²/2}:    E^(5)_10 ≈ 8.8684e-10,   E^(5)_12 ≈ 7.3868e-19,   E^(5)_24 ≈ 7.3625e-111      (rule IMAGE_BOUND)
```

of its reference value. The contraction bound, `|D^q φ(0)| ≤ 15` and the normalization are dimension-free (Math-#197 §3).

**Interval evaluation.** `Space5(E)` widens every entry of the 16-variable even block (136 entries; all but `Var f = 1`, which stays exact) and the 21 entries of
the odd block `(f_u, f_w1, …, f_w4, t)` by `±E`. Over that box it evaluates the following by interval linear algebra (adjugate
inverses, Laplace determinants):
- `p_G(0) = (2π)^{−5/2} det(Cov G)^{−1/2}`;
- `p_V(0)`;
- `τ²`;
- the `11×11` Schur complement `C'`.

Rule `EPSILON` checks the resulting values:

```
ε(L ≥ 10) ≤ 8.894e-8,   ε(L ≥ 12) ≤ 7.409e-17,   ε(L = 24) ≤ 1.9e-57 (arithmetic-limited),   ε(E = 0) ≤ 8.3e-59;
τ²(L ≥ 10) ∈ [5.999999921, 6.000000079],   p_G p_V (L ≥ 10) ∈ [0.00005895763159865, 0.00005895763208666]   (reference (2π)^{−5}/√3).
```

Then `c^(5)_{B,K} ∈ 144 · (8π²/3) · [p_G p_V] · (4.1)(I^ref, ε) · J_K(τ²)`.

**Exact tests of (4.1).**
- **Rule `SANDWICH_EXACT_SCALING`.** For `C' = (1 + η)C'_ref` with `η = ±1/50`, on `[0, 1]`, `[3, 7/2]` and `[−7/2, −3]`, the exact
  value `(1 + η)⁴ I^ref_{B/√(1+η)}` lies inside its own sandwich.
- **Rule `TILTED_EXACT`.** This is Math-#209's tilted pair `(v, μ, σ²) = (17/25, 33/34, 133/5100)`, which is non-scalar, with
  `ε = 4·√12/150 = 0.0924`. Its exact value is evaluated through the same reduction. On `B = R` it equals `D_4`. On `[0, 1]` and
  `[1, 2]` it exceeds the reference by `14.8 %` and `1.7 %`, and lies inside (4.1).

## 5. Values (`RESULTS.json`)

`F^(5)_B = I^ref_B/D_4`, `G_K` is Math-#197's, and `c^(5,ref) = c_{5,ref} F^(5)_B G_K`. Displayed intervals are rounded outward
(lower endpoints down, upper endpoints up) and contain the certified intervals of `RESULTS.json`. Every `…`-terminated digit string is
a common prefix of a certified interval's endpoints. Both properties were checked mechanically before publication.

| `B` | `K` | `F^(5)_B` | `c^(5)` reference | torus, every `L ≥ 10`, every frame |
|---|---|---|---|---|
| `[0,1]` | `[1/2,2]` | `0.04371743008362…` | `0.000038935113140665277900…` | `[0.0000389350650058931493, 0.0000389351612754962131]` |
| `[0,1]` | `(0,∞)` | `0.04371743008362…` | `0.000577914670751911841956…` | `[0.0005779139778591554955, 0.0005779153636454892771]` |
| `[−1,1]` | `[1/2,2]` | `0.04423769053347…` | `0.000039398461499405042485…` | `[0.0000393984127234172462, 0.0000393985102754525173]` |
| `[−2,2]` | `[1/2,2]` | `0.43304657819668…` | `0.000385674946697821276574…` | `[0.0003856744599965191507, 0.0003856754333997262939]` |
| `[0,∞)` | `[1/2,2]` | `0.99947924031769…` | `0.000890144668364114888224…` | `[0.0008901434362015235515, 0.0008901459005283823282]` |
| `(−∞,0]` | `[1/2,2]` | `0.00052075968230…` | `4.6379297938824046354106…·10⁻⁷` | `[4.637923373933157e-7, 4.637936213840385e-7]` |
| `R` | `[1/2,2]` | `1` | `0.000890608461343503128688…` | `[0.0008906072285389168673, 0.0008906096941497663666]` |
| `R` | `(0,∞)` | `1` | `0.013219319380084968076033…` (= `c_{5,ref}`) | `[0.0132193015749977590372, 0.0132193371851957381063]` |

`RESULTS.json` lists all twelve window pairs, and each `L ≥ 10` enclosure contains its reference value. At `L = 24` every enclosure
agrees with the reference to about 50 digits. The full window contains Math-#200's `c_{5,ref}` (rule `C5_CONSISTENT`).

**How the birth mass moves with dimension.** The share carried by the C8 band `B = [0, 1]`:

| `d` | band share |
|---|---|
| 2 | `48.3 %` |
| 3 | `34.6 %` |
| 4 | `15.4 %` |
| 5 | **`4.37 %`** |

The negative half-line carries `0.052 %` in `d = 5`. With the dimension-free gap factor (`6.74 %`), the band carries `0.29 %` of
`c_{5,ref}`.

## 6. Rules, mutants, verification

`python3 -B -S window_coefficient_d5.py` (also `-B -O -S`; about eighty seconds) prints `RESULTS.json`. It exits `0` only if all
eighteen rules hold:

| rule | what it requires |
|---|---|
| `REFERENCE_EXACT` | the exact `C'_ref` and conditional law, including the tilted covariance at `(2/3, 1, 0)` |
| `LAMBDA_FLOOR` | the floor `1/4` certified; `3/10` refused |
| `INNER_LAYERS` | (2.2) exact, the cancellations, and the float triple integral |
| `D4_EXACT` | the full window encloses Math-#202's `D_4` |
| `QUAD_COARSE` | the coarse quadrature with its remainder contains `D_4` |
| `CROSSCHECK_M2_M3` | the `m = 2` and `m = 3` runs reproduce the `d = 3` and `d = 4` results |
| `FLOAT_CONTROL` | the eigenvalue float quadrature agrees with (2.3) |
| `IMAGE_BOUND` | the `d = 5` image-bound constant and values |
| `EPSILON` | the certified `ε` values |
| `SANDWICH_EXACT_SCALING` | exact scalar perturbations lie inside (4.1) |
| `TILTED_EXACT` | the tilted non-scalar perturbation lies inside (4.1) |
| `FACTORIZATION` | the pipeline at `E = 0` reproduces `c_{5,ref} F^(5)_B G_K` on the band and the full window |
| `C5_CONSISTENT` | agreement with Math-#200's `c_{5,ref}` |
| `NESTING` | `L ≥ 10` enclosures contain the reference; the band meets the `10³⁰`-times narrower `L = 24` enclosure |
| `WIDTHS` | relative half-width below `2·10⁻⁶` at `L ≥ 10` |
| `SANDWICH_ORDERED` | every bracket has lower ≤ upper |
| `LIBRARY_EXACT` | exp, sqrt and negation against exact rational brackets |
| `PINNED` | the pinned digits |

Thirteen mutants exit `1` in both interpreter modes:

| mutant | change |
|---|---|
| `image-shells` | `160j⁴` shells |
| `d4-floor` | the `d = 4` floor `3/10` |
| `sandwich-swap` | the two rescalings exchanged |
| `window-scale` | `B·s` for `B/s` |
| `trace-slope` | the window factor's centre at `T/6` instead of `T/7` |
| `moment-recurrence` | `j` for `j + 1` in the moment recurrence |
| `remainder-dropped` | the Cauchy remainder omitted |
| `parts-sign` | the sign of the boundary term in the `w`-layer integration by parts |
| `schur-sign` | the sign of the Schur complement |
| `tau-cross` | `Cov(t, f_u)` dropped |
| `sphere` | `2π²` for `8π²/3` |
| `tilt-gamma` | the `σ²` term dropped from the tilted exponent |
| `layer-dropped` | the `E_{3/16}` layer silently left out of the derivation (v1.1) |

`moment-recurrence` breaks the Owen-term cancellation. The script then refuses to evaluate anything with a surviving Owen-type term,
and exits `1` through that `ValueError`. Every other mutant fails named rules; `parts-sign`, for instance, fails `INNER_LAYERS` and
`D4_EXACT`. `layer-dropped` changes no value, since the omitted layer is zero, and fails `INNER_LAYERS` alone. The hosted workflow
replays the manifest, the pins, both modes byte for byte, and the mutants.

## 7. What this does not do

- It encloses `c^(5)_{B,K}` for the reference kernel and the torus. It does not revalidate [LP] Theorem B and §15, which it consumes
  at their scope. It does not review Math-#197, #200, #202, #205 or #209.
- It does not go to `d ≥ 6`. The `m = 5` analogue would need one more layer, and the floor falls further (`0.2311` at `m = 5`).
- **Windows outside [LP] Theorem B's hypothesis.** Theorem B assumes compact windows of positive length with a positive gap floor:
  `−∞ < b_− < b_+ < ∞` and `0 < k_− < k_+ < ∞`. Three kinds of window fall outside it:
  - a gap window that touches `k = 0` or `∞`, such as the tabulated `K = (0,∞)`;
  - an unbounded `B`: `[0,∞)`, `(−∞,0]`, `R`;
  - a singleton window, `b_− = b_+` or `k_− = k_+`. There (1.1) is zero and does not inherit Theorem B's positive coefficient. No
    singleton window is tabulated.

  For these windows the values are the coefficient integrals (1.1) on those sets only. Theorem B's asymptotic statement is not
  extended to them.
- It does not address `C`, `r_*` or `z_*`. C8 stays OPEN; no register surface is touched; `executed: false`.
- The replay workflow follows the repository's per-packet convention. The owner's open decision on such workflows (Math-#202/#204)
  applies here too.

## 8. Provenance

**Pins on `main 3e0a91b` (workflow-checked):**
- [LP] `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md`, blob `dfed3b8d`.
- SIDE24 `coefficients/side24_v1/PROOF.md`, blob `44b66f04`.

**Companions, not on `main`:**
- **Math-#197** at `3dcf612`: `window_coefficient.py` blob `43b4f51b`. The toolkit is reused verbatim through Math-#205's copy.
- **Math-#205** at `01d09e9`: `window_coefficient_d3.py` blob `ba24b380`. Its toolkit section and `I3_ref` are reused verbatim; Lemma S
  is its §2.
- **Math-#199** at `617236d`: `cone_moment_d4.py` blob `4787d6bf`. The exact polynomial algebra is reused verbatim.
- **Math-#209** at `ea3a415`: `window_coefficient_d4.py`. The reduction, quadrature and controls are extended here; its band factor is
  a rule.
- **Math-#200** at `aa1d51e`: `RESULTS.json` blob `b67c00f4`, giving `c_{5,ref}`. Its `E_5 = 60500(76·24⁶ + 15)e^{−288}` gives the
  constant.
- **Math-#202** at `4512309`: `NOTE.md` blob `dfefe291` and `RESULTS.json` blob `52ce9b57`. These give the closed form of `D_4` and
  `Z_4 = 1536π`.

No external numerical library is used.

## 9. Current disposition

- **Head / owner:** see the PR's disposition block. Branch `claude/c8-window-d5-20261001` (base `main 3e0a91b`); author lane
  Anthropic / Claude (`session_017Mi3hxjaxV45x6zo6o1ee3`).
- **Claim:**
  - the `m = 4` total-trace reduction and its closed inner layers (2.2), including the cancellation of the Owen-type terms;
  - the certified reference values of `c^(5)_{B,K}`;
  - Lemma S in `d = 5` with the floor `1/4`;
  - the `d = 5` image bound and the certified `ε`;
  - the torus enclosures for every `L ≥ 10` and every frame, and for `L = 24`, on the windows of §5.

  No theorem of [LP] or SIDE24 is proved or reviewed.
- **Completed review scopes:** Codex code review at `7ab39d2`: three P2 findings, all fixed in v1.1 (§10). Requested nonauthor
  reads:
  - Slice A: §§1–3;
  - Slice B: §4;
  - Slice C: §§5–7.
- **Unresolved finding IDs:** none.
- **Validation:** 18/18 rules in both modes, byte-identical output; 13/13 mutants rejected in both modes; workflow replayed
  locally; hosted run pending at opening.
- **Next action:** nonauthor reads; amendments on this branch, recorded in `SOURCE_FILES.json`. The author will not merge.

## 10. Revisions

- **v1.1 (Codex code review at `7ab39d2`, three P2 findings).**
  - **Thread 4151593189 (cancelled layers).** `INNER_LAYERS` compared only the nonzero kinds with (2.2) and required one Owen-type
    kind to be present. A derivation that silently omitted a cancelled layer would still have passed. The rule now also requires the
    set of generated kinds that come out zero to equal exactly the four stated: the two Owen-type kinds, the constant, and
    `E_{3/16}` (§2).
  - **Thread 4151593177 (gap window).** §0 said `k_− ≥ 0`. [LP] Theorem B assumes `0 < k_− ≤ k_+ < ∞`, and §0 now states that
    hypothesis. §7 says that windows outside it, including the tabulated `K = (0,∞)` and the unbounded `B`, are coefficient integrals
    only.
  - **Thread 4151593183 (module documentation).** The script's docstring had been carried over from the `d = 4` script. It now
    describes the `d = 5` calculation: the 4×4 GOE, the coordinates `(T, w, s, q)`, the order-48 quadrature, the cancellation, Lemma S
    with `n = 11` and degree `8`, the floor `1/4`, `E^(5)_L`, and the window hypothesis.
  - A thirteenth mutant, `layer-dropped`, leaves the `E_{3/16}` layer out of the derivation. It changes no value, so before v1.1 it
    would have passed; it now fails `INNER_LAYERS`. The workflow's mutant list includes it.
  - The values, the eighteen rules and the twelve earlier mutants are unchanged, and `RESULTS.json` is byte-identical.
- **v1.2 (positive-length windows; NOTE only).** C43 found on Math-#205 (review 5377957341, finding C43-205-H-01) that
  [LP] Theorem B also requires `B` and `K` to have positive length (line 37 of the pinned [LP]). The statement here allowed
  singleton windows such as `K = [1, 1]`, where (1.1) is zero. §0 now states `−∞ < b_− < b_+ < ∞` and `0 < k_− < k_+ < ∞`, and
  §7 classes singleton windows with the other windows outside the hypothesis. Every tabulated window has positive length, so no
  value changes. The script's docstring states the same hypothesis; the values, the rules, the thirteen mutants and
  `RESULTS.json` are unchanged.
