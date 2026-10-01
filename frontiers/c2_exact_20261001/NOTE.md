# The third-order coefficient `c2` in closed form: Gaussian kernel, `d = 1, 2, 3`

**Object:** CL-C2-EXACT-20261001-v1.
**Author:** Anthropic Claude (Claude Code session `session_015wNj8LPTKXsaT68G3DgPPh`), 1 October 2026.
**Disposition:** exact closed forms, by an exact rational derivation replayed with the standard library, and certified
interval enclosures of the coefficient `c2` that Math-#216 defines and Math-#218 (0.1) and Math-#220 use, together with
the leading coefficient `c` from the same pipeline. Author-side; no review yet. Scope claim: Math-#216 comment 5931466669.
**Scientific effect:** NONE. No `STATUS`, `PROOF_INDEX`, `GRAPH`, claim, catalog, prize or source-body change. Same GitHub
account as every lane; zero organizational-independence credit. Nothing in Math-#214, #216, #218 or #220 is touched.

## 0. Statement

Math-#216 ([D], head `4f0927f`) defines, from the two-point kernel `A_r(b, k, u)` of [R] and its fold expansion
`A_r = A_0 + r^2 A_2 + O(r^3)`,

    c  = (1/3) |S^(d-1)| integral_R db integral_0^oo A_0(b, k) k^(-2/3) dk,
    c2 = (1/3) |S^(d-1)| integral_R db  f.p. integral_0^oo A_2(b, k) k^(-4/3) dk
       = (1/3) |S^(d-1)| integral_R db integral_0^oo [A_2(b, k) - A_2(b, 0)] k^(-4/3) dk.

`c` is the leading coefficient of the short-lifetime law. `c2` is the coefficient of `ell^(1/3)`:
- Math-#218 (Theorem T, candidate status) proves it for the candidate density;
- Math-#220 (Theorem E3) proves it for the elder density, conditional on Math-#187;
- [D] derives it formally and by Monte Carlo, and lists a certified value as not claimed.

**Theorem (closed forms).** For the Gaussian kernel `K(z) = exp(-|z|^2/2)` on `R^d`:

| `d` | `c` | `c2` |
|---|---|---|
| `1` | `Gamma(1/6) 12^(-1/6) / (6 pi^(3/2))` | `(3/4) 12^(1/6) Gamma(5/6) / pi^(3/2)` |
| `2` | `Gamma(1/6) 12^(-1/6) / (9 pi^(3/2))` | `(13/18) 12^(1/6) Gamma(5/6) / pi^(3/2)` |
| `3` | `(29/72 - sqrt6/12) Gamma(1/6) 12^(-1/6) / pi^(5/2)` | `(5/48)(33 - 7 sqrt6) 12^(1/6) Gamma(5/6) / pi^(5/2)` |

In every dimension the ratio is an algebraic multiple of one transcendental factor:

    c2/c = kappa_d Gamma(5/6) / (12^(2/3) Gamma(1/6)),     kappa_1 = 54,   kappa_2 = 78,   kappa_3 = 18 (141 - sqrt6)/25.

Here `12^(1/6) = 2^(1/3) 3^(1/6)`. The certified values (interval arithmetic, outward to 16 digits, `RESULTS.json`) are:

| `d` | `c` | `c2` | `c2 / c` |
|---|---|---|---|
| `1` | `[0.1101103789590410, 0.1101103789590625]` | `[0.2300445802661503, 0.2300445802661998]` | `[2.089217950577392, 2.089217950578207]` |
| `2` | `[0.07340691930602738, 0.07340691930604167]` | `[0.2215244106266632, 0.2215244106267110]` | `[3.017759261945122, 3.017759261946299]` |
| `3` | `[0.04177593184059426, 0.04177593184060272]` | `[0.1612340491269447, 0.1612340491269810]` | `[3.859496174547095, 3.859496174548665]` |

At 30 digits (mpmath, a control only): `c2 = 0.230044580266174952088473542454`, `0.221524410626686990900011559`,
`0.161234049126962737547589515632`.

**Consequences.**
- **[D]'s eight digits are confirmed and made exact.** [D] gives `c2 = 0.23004458`, `0.22152441`, `0.16123405` and
  `c2/c = 2.089218`, `3.017759`, `3.859496` from an `r`-fit. Each is the correct rounding of the closed form (§7).
- **The leading coefficient comes out exactly.** In `d = 2, 3` it equals the closed form `c_(d,ref)` of
  `coefficients/side24_v1` (1). In `d = 1` it equals Math-#214's `C_0`, and `c2` equals #214's `2 B_2`. These are
  identities of exact numbers, checked by the certificate (§4).
- **The three-term law in closed form.** With [CU]'s `c1`, the relative correction is
  `nu/(c ell^(-1/3)) - 1 = (c1/c) ell^(7/12) + (c2/c) ell^(2/3) + ...`. In `d = 3` it is
  `-5.071062... ell^(7/12) + 3.859496174548... ell^(2/3)`, where `c1/c` is certified in Math-#219 and `c2/c` here.

## 1. What is evaluated

The kernel is that of [R] §§2–4 and [D] §0. Pins sit at `M = -r e1/2` and `S = r e1/2` with zero gradients and heights
`b`, `b - k r^3`. The symmetric pin vector `U_r` has target `v_r = (b - k r^3/2, -k r^2, 0, 12k, 0, ..., 0)`, with rows
as in [D]'s `c2_check.py` (`pseries.pin_rows`), and

    A_r(b, k) = 12 pi_r(v_r) E[ |det H_M| |det H_S| 1{typed} | U_r = v_r ] / r^2,     u = e1 (isotropy).

As in [D] §2.2, the typed indicator is:
- nothing in `d = 1`, where the typed event has probability `1 - O(e^(-c k^2/r^2))`;
- `1{f_yy(0) < 0}` in `d = 2`;
- `1{D_y^2 f(0) < 0}` in `d = 3`.

Each replacement changes `A_r` by `O(r^3)` at fixed `k`. [T] Lemma F proves the fold expansion and identifies
`A_2(b, 0) = -12 pi_0 E_0[Y^2 1{A < 0} | b]`, which is (0.1). Both are consumed, not reviewed. On the typed set,
`|det H_M| |det H_S| = -det H_M det H_S`.

## 2. Exact derivation (`pseries.py`, `exact.py`)

**2.1 Series.**
- Every quantity is a linear form in the jets at 0 with coefficients in `Q[[r]]`:
  `d^beta f(x e1) = sum_j x^j/j! d^(beta + j e1) f(0)`, with `x = -+r/2`.
- Jet covariances are the integers `(-1)^|b| d^(a+b) K(0)`.
- The pin rows divide by `r`, `r` and `r^3`. Each division is exact, because the low coefficients vanish identically;
  the code asserts this.
- Keeping `r^0 .. r^10`, every derived series is exact through `r^7`. The integrand needs `r^6`.

**2.2 Conditioning.**
- The `r^0` pin covariance is invertible (`det = 12` in `d = 1, 2`), so the conditional means `G v_r` and covariances
  are computed exactly in `Q[[r]]`.
- In `d >= 2` the Hessian entries are conditioned further on the transverse block `T = D_y^2 f(0)`: on `a = x1` in
  `d = 2`, and on `T = diag(x1, x2)` in `d = 3`.
- `d = 3` uses transverse rotation invariance. The pins lie on `e1`, and transverse rotations preserve the law and
  `det H_M det H_S`. With the Jacobian of the symmetric `2 x 2` eigenvalue map,
  `integral_(T<0) g(T) p(T) dT = pi integral_(x2<x1<0) g p (x1 - x2) dx`.

**2.3 The integrand.** `F = E[det H_M det H_S | T, U_r = v_r]` comes from Isserlis' theorem as an exact polynomial in
`(r, b, k, x1, x2)`. Then

    A_r(b, k) = const . integral_cone exp(-(q + Q)/2) F w / r^2,    q = v_r^T S_r^-1 v_r,   Q = z^T C_TT^-1 z,

where:
- `const = -12 (2 pi)^(-(p + n_T)/2) (det S_0 det T_0)^(-1/2)`, times `pi` in `d = 3`;
- `z = T - E[T | U_r]`;
- `w = 1`, `da`, or `(x1 - x2) dx`.

Writing `q = q_0 + dq` and `Q = Q_0 + dQ`, the factor `(det ratio)^(-1/2) exp(-(dq + dQ)/2) F` is expanded exactly in `r`.
`A_r` is real-analytic in `r` near 0, with Gaussian domination uniform in small `r` because the `r = 0` covariances are
nondegenerate. Its Taylor coefficients are therefore the cone integrals of those of the integrand.

**2.4 Exact structural facts.** The certificate verifies each of these.
- The integrand vanishes to order `r^2`.
- The `r^3` coefficient vanishes, so `A_r` has no `r^1` term ([D] T5).
- `q_0 = 3b^2/2 + 24 k^2`, with no `b k` term.
- `Q_0` has no `k`: the transverse block does not see `k`, by parity.
- `A_0` and `A_2` contain only even powers of `k`.

## 3. Integration

**3.1 `k`, by Gamma finite parts.** `A_j(b, k) = exp(-12 k^2) sum_(even l) a_l(b, x) k^l`. For `-2 < s < 0`,
`integral_0^oo (k^l e^(-12k^2) - [l = 0]) k^(s-1) dk = Gamma((l + s)/2) 12^(-(l+s)/2)/2`. With `s = 1/3` for `c` and
`s = -1/3` for `c2`, every term is a rational multiple of `Gamma(1/6) 12^(-1/6)` or of `Gamma(5/6) 12^(-5/6)`. The
`l = 0` finite part uses `Gamma(-1/6) = -6 Gamma(5/6)`.

**3.2 `b`, by completing the square.** The `k`-free exponent is `a_b b^2 + b L(x) + R(x)`. The substitution
`b -> b - L/(2 a_b)` leaves Gaussian moments `integral b^n e^(-a_b b^2) db` and the cone exponent `R - L^2/(4 a_b)`.

**3.3 The cone.**
- **`d = 2`:** half-line moments `integral_(-oo)^0 a^n e^(-g a^2) da`, with `g = 3/16`.
- **`d = 3`:** with `x1 = -s` and `x2 = -s - t`, the exponent is `(3/10) s^2 + (3/10) s t + (1/5) t^2` and
  `D = 4 al ga - be^2 = 3/20`. The quadrant moments `M(i, j)` follow from two integration-by-parts identities, in `s`
  and in `t`. These form a `2 x 2` system with determinant `D`, starting from
  `M(0, 0) = theta = (pi/2 - arctan(be/sqrt D))/sqrt D`.
- Every `M(i+1, j)` with `j >= 1` is reached twice, and the two values agree exactly (asserted).
- **The angle `theta` cancels exactly in both `c` and `c2`.** The results lie in `Q(sqrt6)` times powers of `pi`.

Numbers are carried as `sum q pi^(h/2) sqrt(m) theta^e`, with `q` rational and `m` squarefree.

## 4. Exact checks (`certificate.py`)

1. **`theta` does not occur** in any result.
2. **`d = 2, 3`, `c` equals `coefficients/side24_v1` (1).** Since `Gamma(7/6) = Gamma(1/6)/6` and
   `(3/2)^(1/3) = sqrt3 12^(-1/6)`, the closed form `Gamma(7/6)(3/2)^(1/3) D_(d-1)/(2 sqrt3 pi^(d-1) sqrt pi)` equals
   `Gamma(1/6) 12^(-1/6) D_(d-1)/(12 pi^(d-1/2))`, with `D_1 = 4/3` and `D_2 = 29/6 - sqrt6`. Equality is exact.
3. **`d = 1`, `c = C_0` and `c2 = 2 B_2` of Math-#214 (D1.2).** For the Gaussian spectral moments `1, 3, 15, 105`:
   - `D = 6`, `sigma_3 = sqrt6`, `p_12 = 1/(2 pi sqrt3)` and `Q/(120 lambda_2 lambda_4 D) = 3/4`;
   - `72^(-1/6) 6^(2/3) = sqrt6 12^(-1/6)` and `3^(1/3) 6^(1/3) = 12 sqrt3 12^(-5/6)` give `C_0 = atom/(6 pi^(3/2))` and
     `2 B_2 = 9 atom'/pi^(3/2)`;
   - both are exact equalities, and the two reductions are also checked against #214's formulas in floating point.
4. **Truncation stability.** The whole derivation is repeated with series order 12 and polynomial order 8, and every
   result is identical.
5. **The ratios.** `kappa_d Gamma(5/6)/(12^(2/3) Gamma(1/6))` must meet the interval quotient of the enclosures.

## 5. Evaluation

- `Gamma(1/6)` and `Gamma(5/6)` come from Stirling's series at `q + 10`, with the remainder bounded by the first
  omitted term, and the exact product (`gam.py`: the code of Math-#219's `consts.py`).
- `12^(rational)` is `exp(log)`; `pi` and `sqrt` come from `ia.py` and `elem.py` (Math-#219, byte-identical; `ia.py` is
  also Math-#217's).
- Outward one-ulp rounding is used throughout. Publication widens by `1e-14` relative and rounds outward to 16 digits.
- `--check` re-derives everything and requires the regenerated document to equal `RESULTS.json`.

## 6. Verification

- `python3 -B -S certificate.py --check` takes about one second. It runs the exact derivation, the checks of §4 and the
  evaluation, then compares with `RESULTS.json`.
- Five seeded defects must each exit 1:
  - `target`: the pin target `11 k` instead of `12 k`;
  - `finite-part`: the `l = 0` term without the subtraction of `A_2(b, 0)`;
  - `cone-sign`: the sign of the cone cross term;
  - `truncation`: polynomial order 3;
  - `sphere`: `|S^1| = pi`.
- The workflow `.github/workflows/c2-exact.yml` runs, for `-B -S` and `-B -O -S`: the manifest and pin check,
  `--check`, the mutants, the controls, and a clean-tree check.

## 7. Floating controls (`controls.py`; not part of the certificate)

1. **A finite-`r` kernel.**
   - `A_r(b, k)` is computed at finite `r` directly from the closed-form kernel derivatives at the displaced points,
     `D^g K(z) = prod (-1)^(g_i) He_(g_i)(z_i) e^(-z_i^2/2)`, with 60-digit conditioning and no Taylor jets.
   - The Richardson estimate `2 D(r) - D(2r)`, with `D(r) = (A_r - A_0)/r^2`, converges to the exact `A_2(b, k)` at the
     rate `O(r^2)`, at five points in `d = 1, 2, 3`.
   - The relative errors at `r = 0.01, 0.005, 0.0025` are `1.3e-4`, `3.2e-5`, `8.0e-6` (`d = 1`), with ratios `3.75` to
     `4.17` per halving everywhere.
2. **[D]'s floating values.** All nine (`c`, `c2`, `c2/c` for `d = 1, 2, 3`) are correct roundings of the certified
   midpoints. The largest difference, `4.0e-13`, is for `c(d = 3)`, against a half-unit of `5e-13`.

## 8. What this does not do

- **Gaussian kernel only.** The periodized covariance changes the jets by `1 + O(e^(-L^2/8))` ([D] §0). No torus
  transfer of `c2` is made. The finite part and the typed indicator do not fit the homogeneity argument of Math-#219's
  Lemma S.
- **No `d >= 4`.** The method extends; the cone then needs the 3D eigenvalue reduction.
- **The definition is consumed.**
  - The identification of `c2` as the `ell^(1/3)` coefficient is [D]'s (formal), [T]'s (candidate density, candidate
    status) and Math-#220's (elder density, conditional on #187), and is not reviewed here.
  - So is the `O(r^3)` replacement of the typed indicator (§1).
- Not a review of any source. Same GitHub account as every lane; zero organizational-independence credit.
  **I will not merge.**

## 9. Provenance

- **Sources** (`SOURCE_MAP.json`):
  - [R] `frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md` (the two-point kernel);
  - [SIDE24] `coefficients/side24_v1/PROOF.md` (1).

  Both are on `main` and verified by the workflow.
- **Unmerged, recorded and not checked on this tree:**
  - [D] Math-#216 `NOTE.md` and `c2_check.py` at head `4f0927f`;
  - [T] Math-#218 `PROOF.md` at head `7f09d34`;
  - [D1] Math-#214 `PROOF.md` at head `f4a58df`.
- **Files:**
  - the certificate: `certificate.py`, `exact.py`, `pseries.py`, `gam.py`, `ia.py`, `elem.py`;
  - `controls.py`;
  - `RESULTS.json`, `SOURCE_MAP.json`, `SOURCE_FILES.json`.
