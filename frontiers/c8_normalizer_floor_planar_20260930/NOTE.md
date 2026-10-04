# A certified floor for the planar full normalizer: `Z_r / r^2 >= z_*` on a declared band (C8, first constant)

**Object:** `CL-C8-NORMALIZER-FLOOR-PLANAR-20260930-v1`. **Author lane:** Anthropic / Claude (Claude Code
`session_015wNj8LPTKXsaT68G3DgPPh`). **Kind:** certified numerical constant: exact rational interval arithmetic in the
standard library, every transcendental (`exp`, `Phi`, `sqrt`, `pi`) bracketed by a series with an explicit remainder,
every rounding outward or budgeted. **Scientific effect:** NONE. No register, catalog, GRAPH or STATUS change; catalog
entry C8 (`reviews/candidates_pending_20260928/CANDIDATES.md`) stays OPEN: this note supplies one of its listed
constants, `z_*`, on one declared band and none of `C`, `r_*`, `c_{B,K}`, `c_{d,L}`.

## 0. Statement

Let `f` be the unit-variance stationary Gaussian field on the torus `R^2 / (L Z^2)` with the parent kernel
`K_L(z) = sum_n exp(-|z + Ln|^2/2) / sum_n exp(-|Ln|^2/2)` ([LP] section 1). For an orthonormal frame with axial unit
vector `u`, radius `r`, birth `b` and gap `k`, let `Q = Q_{r,b,k,R}` be the Gaussian regression at the six pins
`f(M) = b`, `f(S) = b - k r^3`, `grad f(M) = grad f(S) = 0`, `M = -(r/2) u`, `S = (r/2) u`, and

    W_r = |det H_M  det H_S| 1{H_M < 0, index H_S = 1},      Z_r = E_Q W_r      ([LP] section 1).

**Certified inequality.** For every frame and every `(b, k)` with `0 <= b <= 1`, `1/2 <= k <= 2`:

    L >= 12,   1/64 <= r <= 1/2 :    Z_r / r^2  >=  z_*  =  3.5044 ,
    L >= 10,   1/8  <= r <= 1/2 :    Z_r / r^2  >=  3.5044   (high band),
    L >= 12,   1/64 <= r <= 1/8 :    Z_r / r^2  >=  7.0499   (low band),

with the sharper sub-box floors of `RESULTS.json` (`bands.high.table`: 192 x 8 x 6 boxes on `[1/8, 1/2]`;
`bands.low.table`: 56 x 8 x 6 boxes on `[1/64, 1/8]`; `r` in steps of `1/512`, `b` of `1/8`, `k` of `1/4`): in particular
`Z_r / r^2 >= 7.6517` for `r <= 1/32`, `>= 7.4705` for `r <= 1/16`, `>= 6.5593` for `1/8 <= r <= 3/16`,
`>= 6.0085` for `1/8 <= r <= 1/4`, `>= 4.7822` for `1/8 <= r <= 3/8` (all `b`, `k` in the band), and for every box the floor
scales as `k_lo^2 x q(box)` with `q` certified for `Z_r / (r^2 k^2)`. The high-band minimum is attained at
`r=[255/512,1/2],b=[0,1/8],k=[1/2,3/4]`, the low-band minimum at `r=[63/512,1/8],b=[0,1/8],k=[1/2,3/4]`. The low band needs `L >= 12`
because the periodization remainder enters the preconditioned functionals with the factor `r^-10` (section 2).

This is the constant whose existence is [LP] (5.5) (`0 < z_* <= Z_r / r^2`), with a number on a declared band. It is
a lower bound, not an enclosure: the floating Monte Carlo controls of section 4 put the true `Z_r / r^2` at `1.1` to
`2` times the floor across the bands (`0.50` to `0.89` as a ratio floor / MC).

## 1. Reduction to a six-dimensional Gaussian and the r -> 0 limit

Under `Q` the six Hessian entries `(f_xx, f_xy, f_yy)(M), (f_xx, f_xy, f_yy)(S)` are jointly Gaussian with mean
`mu(r, b, k)` and covariance `C(r)`, and `Z_r = E[|det H_M||det H_S| 1{...}]` is their integral against that law.
As `r -> 0`, [LP] (5.2)-(5.4): `f_xx(M) = -6 k r + O(r^2)`, `f_xx(S) = 6 k r + O(r^2)`, `f_xy = O(r)`, and the transverse
entries converge to the contact law `A_0 ~ N(-b, 2)` ([NUM]; Math-#184 Lemma 1 in general `d`), so that

    Z_r / r^2 -> z_0(b, k) = 36 k^2 E[A_0^2 1{A_0 < 0}],   A_0 ~ N(-b, 2)                  (5.4)

(`z_0(0, k) = 36 k^2`, `z_0(1, k) = 97.925 k^2`). The certified band is a finite-`r` statement and does not use (5.4);
`z_0` appears only as a floating control (section 4).

## 2. Method

**Preconditioned jets.** The raw pin covariance is nearly singular (`det ~ r^6`), so interval regression on the raw
pins would lose everything. Instead the pins are the midpoint-jet combinations

    p1 = (f(M) + f(S))/2,   p2 = (f(S) - f(M))/r,   p4 = (f_x(S) - f_x(M))/r,
    p3' = 12 [(f_x(M) + f_x(S))/2 - p2] / r^2,   q1 = (f_y(M) + f_y(S))/2,   q2 = (f_y(S) - f_y(M))/r,

with values `(b - k r^3/2, -k r^2, 12 k, 0, 0, 0)` (limits `f, f_x, f_xxx, f_xx, f_y, f_xy` at the midpoint), and the
targets are

    w_M = f_yy(M),  om = (f_yy(S) - f_yy(M))/r,
    T_M = [f_xx(M) - p4 + (r/2) p3'] / r^2,  tau = (T_S - T_M)/r  with  T_S = [f_xx(S) - p4 - (r/2) p3'] / r^2,
    v_M = [f_xy(M) - q2] / r,  nu = (v_S + v_M)/r  with  v_S = [f_xy(S) - q2] / r

(limits `f_yy, f_xyy, f_xxxx/12, f_xxxxx/60, -f_xxy/2, f_xxxy/6`). Both covariance matrices have `O(1)` nondegenerate
limits, so the `6 x 6` interval Gaussian elimination and the `6 x 6` interval Cholesky factor are well conditioned on
every band. The Hessian is recovered exactly: `f_xx(M) = r^2 T_M - 6 k r`, `f_xx(S) = r^2 (T_M + r tau) + 6 k r`,
`f_xy(M) = r v_M`, `f_yy(M) = w_M`, `f_yy(S) = w_M + r om` (the pin values enter through `p4 = 0`, `p3' = 12 k`,
`q2 = 0`). The conditional mean is exactly `b alpha(r) + k beta(r)` (the pin values are linear in `(b, k)`), so the
centred coordinates `y = x - b alpha - k beta` have conditional mean zero for every `(b, k)`: the cell probabilities
depend on `r` only, and `b`, `k` enter the determinant bounds only.

**Exact cancellation.** Every raw covariance `Cov(d^u f(s), d^v f(t)) = (-1)^c He_{a+c}(Delta) exp(-Delta^2/2) .
(-1)^d He_{b+d}(0)`, `Delta = t - s in {0, +-r}`, is a Hermite polynomial times `exp(-r^2/2)`; with the Taylor
polynomial of `exp(-r^2/2)` to order `48` it is an exact Laurent polynomial in `r` plus a remainder bounded by
`(r^2/2)^25 / 25!` times the Hermite maximum. The preconditioned functionals carry powers `r^-1 ... r^-5`; the script
asserts that every negative power cancels exactly in every one of the `108` covariance polynomials before evaluating
them on the band (a structural check of the jet algebra). Evaluation is a term-by-term interval sum.

**Torus remainder (any frame).** In the frame `R`, `K_L(R w) = [G(w) + sum_{n != 0} G(w + R^T n L)] / Theta`,
`G = exp(-|.|^2/2)`, `Theta = sum_n G(nL) in [1, 1 + eps_0]`. For `|gamma| <= 4` and `|w| <= r`, with
`|He_j(t)| <= (|t| + 3)^j` (`j <= 4`) and `h(s) = (s + 3)^4 exp(-s^2/2)` decreasing for `s > 1`,

    |sum_{n != 0} d^gamma G(w + R^T n L)| <= eps(L, r) := 8 h(L - r) + 4096 (L + 3)^4 exp(-(2L - r)^2/2) / (1 - 32 exp(-L^2/2))

(shell `|n|_inf = 1`: eight points at distance `>= L - r`; shells `m >= 2`: `8m` points, `(mL - r)^2 >= (2L - r)^2 +
(m - 2) L^2` and `m^5 <= 32 . 32^(m-2)`). Every raw entry is widened by `+-eps` before the cancellation step, the
whole covariance is divided by `Theta` at the end (a common positive factor leaves the regression coefficients unchanged
and scales the conditional covariance by `1/Theta in [1/(1 + eps_0), 1]`). At `L = 10`, `eps(10, 1/2) = 4.93e-15`,
`eps_0 = 4.41e-17`; the cross-block Cholesky entries this produces are of size `1e-9` to `1e-6` and are absorbed below.
The preconditioned functionals carry coefficients up to `r^-5`, so a raw perturbation `eps` becomes `eps r^-10` in the
`O(1)` covariances: `5e-6` at `L = 10`, `r = 1/8`, but `60` at `L = 10`, `r = 1/64`, where the interval Cholesky fails; the low
band is therefore declared for `L >= 12`, where `eps(12, 1/8) = 9.37e-26` gives `3e-8` at `r = 1/64`.
Determinants and indices are frame invariant, so the rotated-frame Hessian is the one of [LP].

**Cells and the lower bound.** With `L` the interval Cholesky factor of `C` in the order `(w_M, om, T_M, tau, v_M, nu)`
and `z` standard normal, `y = L z`. On `|z|_inf <= Z_MAX = 8` the cross-block part of `(L z)_i` is at most
`eta_i = 8 sum_{j not in block(i)} |L_ij|`, so for a box `B` in `y`-space

    P(y in B) >= prod_blocks P_block(B shrunk by eta) - 12 (1 - Phi(8)),

the block events being independent (disjoint `z` coordinates). The boxes are cells: `w_M` in `40` slabs on
`[-5 sd, 9/8]`, `om` in `40` slabs on `+-5 sd`, `T_M` in `8` slabs on `+-4 sd` with `tau` in one `+-4 sd` box, `|v_M|`
in `6` slabs up to `3.5 sd` with `nu` in one `+-3.5 sd` box. On each cell, in the coordinates divided by `r k`,

    det H_M / (r k) >= (H_xx(M)/(r k)) . w_M - r v_M^2 / k   (both factors negative on the cell, `v` slab maximum),
    |det H_S| / (r k) >= -(H_xx(S)/(r k)) . (w_M + r om)      (`H_xy(S)^2 >= 0` dropped),

every factor an interval over the cell, the `(r, b, k)` box and the torus widening, and

    Z_r / (r^2 k^2) >= sum_cells [det H_M / (r k)]_lo [|det H_S| / (r k)]_lo P(cell)_lo ,

the cells being disjoint events. Certifying `Z_r / (r^2 k^2)` rather than `Z_r` removes the `(6 k r)^2` factor's
variation over the box; the floor for the box is `q . k_lo^2`.

**Rectangle probabilities.** For a `2 x 2` block `y_p = L_pp z_a`, `y_q = L_qp z_a + L_qq z_b` and a rectangle
`[l_p, h_p] x [l_q, h_q]`,

    P = integral_A^B phi(s) g(s) ds,   g(s) = Phi((h_q - L_qp s)/L_qq) - Phi((l_q - L_qp s)/L_qq),

`A = l_p / L_pp`, `B = h_p / L_pp`. **Lemma (endpoint minimum).** For parallel affine `u(s) > l(s)`, `g = Phi(u) - Phi(l)`
is unimodal with a maximum: `g' = u' (phi(u) - phi(l))` and `phi(u) > phi(l)` iff `|u| < |l|` iff `u + l < 0` (as
`u > l`), and `u + l` is monotone in `s`. Hence the minimum of `g` on a piece is attained at an endpoint, and
`P >= sum_pieces min(g(s_i), g(s_{i+1}))_lo (Phi(s_{i+1}) - Phi(s_i))_lo` with `10` (`8`) pieces per cell; the
intervals in `L_pp, L_qp, L_qq` make this a bound for every covariance in the band (the range `[A, B]` is taken inner).

**Constants.** `exp(-t)` by the alternating series after halving to `t <= 1/2`; `pi` by Machin; square roots by
integer `isqrt` brackets; `Phi(x)` by the series `1/2 + (2 pi)^(-1/2) sum (-1)^n x^(2n+1) / (2^n n! (2n+1))` in fixed
point (ulp `2^-200`) with an integer bound `E_n` on the accumulated rounding error of each term (`E_{n+1} =
floor(E_n x_hi^2 / (2(n+1))) + 2`), the `x` rounding (`|d Sigma / dx| <= 1`), and the alternating tail (first omitted
term, in the decreasing regime `x^2 <= 2n`); `|x| <= 12`, beyond which `Phi` is replaced by `0` or `1` (only
widening). All interval endpoints are rounded outward to `2^-160`.

## 3. Values (`RESULTS.json`)

Combined floor: `z_* = 3.5044` (`L >= 12`, `r in [1/64, 1/2]`); high band `3.5044` (attained at `r=[255/512,1/2],b=[0,1/8],k=[1/2,3/4]`,
valid for `L >= 10`); low band `7.0499` (attained at `r=[63/512,1/8],b=[0,1/8],k=[1/2,3/4]`). Floors by `r`-range (minimum over all
`b`, `k` sub-boxes with `r` in the range):

| `r` range | floor of `Z_r / r^2` | at `(b, k)` box |
|---|---|---|
| `[1/64, 1/32]` | `7.6517` | `b in [0, 1/8], k in [1/2, 3/4]` |
| `[1/64, 1/16]` | `7.4705` | `b in [0, 1/8], k in [1/2, 3/4]` |
| `[1/64, 1/8]` | `7.0499` | `b in [0, 1/8], k in [1/2, 3/4]` |
| `[1/8, 3/16]` | `6.5593` | `b in [0, 1/8], k in [1/2, 3/4]` |
| `[1/8, 1/4]` | `6.0085` | `b in [0, 1/8], k in [1/2, 3/4]` |
| `[1/8, 3/8]` | `4.7822` | `b in [0, 1/8], k in [1/2, 3/4]` |
| `[1/8, 1/2]` | `3.5044` | `b in [0, 1/8], k in [1/2, 3/4]` |

Floors at fixed `(b, k)` corners (minimum over the `r`-bands in the range), against the floating Monte Carlo of
`Z_r / r^2` at the worst corner `(r_hi, b_lo, k_lo)` of the box attaining the floor and the limit `z_0(b_lo, k_lo)`.
High band:

| box (`b`, `k`) | `r <= 1/4`: floor / MC (s.e.) | `r <= 1/2`: floor / MC (s.e.) | `z_0(b_lo, k_lo)` |
|---|---|---|---|
| `b in [0, 1/8], k in [1/2, 3/4]` | `6.0085` / `8.353` (`0.095`) | `3.5044` / `6.957` (`0.083`) | `9.000` |
| `b in [0, 1/8], k in [5/4, 3/2]` | `39.6829` / `52.003` (`0.593`) | `24.5913` / `41.434` (`0.502`) | `56.250` |
| `b in [0, 1/8], k in [7/4, 2]` | `78.0461` / `101.493` (`1.159`) | `47.3116` / `78.071` (`0.961`) | `110.250` |
| `b in [1/2, 5/8], k in [1/2, 3/4]` | `10.5508` / `14.360` (`0.131`) | `6.3815` / `12.258` (`0.116`) | `15.308` |
| `b in [1/2, 5/8], k in [5/4, 3/2]` | `69.6284` / `89.412` (`0.819`) | `45.0348` / `73.344` (`0.705`) | `95.674` |
| `b in [1/2, 5/8], k in [7/4, 2]` | `137.0291` / `174.582` (`1.602`) | `87.1241` / `138.847` (`1.355`) | `187.521` |
| `b in [7/8, 1], k in [1/2, 3/4]` | `15.4017` / `20.678` (`0.163`) | `9.5303` / `17.920` (`0.145`) | `21.888` |
| `b in [7/8, 1], k in [5/4, 3/2]` | `101.6349` / `128.778` (`1.016`) | `67.5804` / `107.627` (`0.884`) | `136.798` |
| `b in [7/8, 1], k in [7/4, 2]` | `200.1061` / `251.529` (`1.988`) | `131.2506` / `204.401` (`1.702`) | `268.124` |

Low band:

| box (`b`, `k`) | `r <= 1/16`: floor / MC (s.e.) | `r <= 1/8`: floor / MC (s.e.) | `z_0(b_lo, k_lo)` |
|---|---|---|---|
| `b in [0, 1/8], k in [1/2, 3/4]` | `7.4705` / `8.822` (`0.099`) | `7.0499` / `8.728` (`0.098`) | `9.000` |
| `b in [0, 1/8], k in [5/4, 3/2]` | `47.0643` / `55.144` (`0.619`) | `45.0742` / `54.546` (`0.614`) | `56.250` |
| `b in [0, 1/8], k in [7/4, 2]` | `92.1467` / `108.077` (`1.214`) | `88.4466` / `106.858` (`1.204`) | `110.250` |
| `b in [1/2, 5/8], k in [1/2, 3/4]` | `12.9311` / `15.048` (`0.136`) | `12.2491` / `14.911` (`0.135`) | `15.308` |
| `b in [1/2, 5/8], k in [5/4, 3/2]` | `81.4752` / `94.056` (`0.853`) | `78.2739` / `93.178` (`0.846`) | `95.674` |
| `b in [1/2, 5/8], k in [7/4, 2]` | `159.5667` / `184.340` (`1.671`) | `153.6276` / `182.550` (`1.659`) | `187.521` |
| `b in [7/8, 1], k in [1/2, 3/4]` | `18.7088` / `21.565` (`0.169`) | `17.7588` / `21.389` (`0.168`) | `21.888` |
| `b in [7/8, 1], k in [5/4, 3/2]` | `117.8971` / `134.787` (`1.055`) | `113.4950` / `133.658` (`1.048`) | `136.798` |
| `b in [7/8, 1], k in [7/4, 2]` | `230.9466` / `264.171` (`2.068`) | `222.8022` / `261.865` (`2.053`) | `268.124` |

## 4. Precision and controls (floating, not certified)

- The floor is a certified lower bound; its distance from the truth is the sum of the cell-minimum losses (the
  determinant is replaced by its minimum over each cell), the box widths in `(r, b, k)`, the `+-c sd` truncations and
  the dropped `H_xy(S)^2`. The floating Monte Carlo controls (`40000` samples, seed `2026`, direct regression of the
  six raw Hessian entries, continuum kernel) give ratios floor / MC between `0.50` and `0.89` over
  the `76` control boxes of the two bands (the low band reaches `0.85`–`0.90`); every floor lies below its control by more than five standard errors and below the
  `r -> 0` limit `z_0(b_lo, k_lo)` (both are `--check` rules; they are consistency checks, not part of the proof).
- The preconditioned exact regression agrees with the direct floating regression of the six raw entries to `1e-9`
  relative at `r = 1/4, 3/8` and to `1e-5` at `r = 1/32`, where the direct regression on the raw pins is ill conditioned
  (`--check` rule); the point-band enclosures of the preconditioned regression have widths below `1e-6` at all three.
- Sensitivity to the band width: at `r = 1/8` the same sub-box certified with `r`-bands of width `1/32`, `1/128`,
  `1/512` gives floors of `0.51`, `0.69`, `0.74` of the Monte Carlo value (the interval Cholesky widths scale with the
  band width); `1/512` is the production choice.

## 5. What this does not do

Not an enclosure of `Z_r / r^2` (a lower bound only, `1.1` to `2` times below the truth). Not a value of `C`, `r_*`,
`c_{B,K}` or `c_{d,L}` of [LP] Theorems A-C, and no statement about `p_r`, the elder selection, the boundary layer of
[LP] section 7, or any `d >= 3` normalizer. Planar only, `L >= 12` on `[1/64, 1/2]` and `L >= 10` on `[1/8, 1/2]` (the
`L = 24` SIDE24 torus included), aligned or rotated frames, `b in [0, 1]`, `k in [1/2, 2]`; nothing for `r < 1/64`
(where the floor tends to `z_0`), `r > 1/2`, or `L < 10`. Not a review of [LP]; the definitions of `Q`, `W_r`, `Z_r` are consumed as stated, and (5.4)-(5.5)
are not revalidated (the certified band does not use them). No register, catalog, GRAPH or STATUS change; C8 stays
OPEN. Same GitHub account as every lane; zero organizational-independence credit. The author will not merge.

## 6. Verification

`python3 -B -S floor.py --check` (and `-B -O -S`; about three minutes): re-derives the certified floor of twelve sub-boxes
(each band's argmin box, six high-band boxes one per 32 `r`-bands, four low-band boxes one per 18) from scratch and requires exact agreement with
`RESULTS.json`; checks that each band's stored `z_star` is the minimum of its table and the combined statement; checks every floating control (floor `<=` MC `+ 5` s.e., floor `<= 1.01 z_0`); checks the
preconditioned regression against the direct floating regression at three point bands, the Laurent cancellations, and
the bracketing of `pi`, `Phi(1)`, `exp(-1)`. Mutants (`--mutant`, must exit 1): `swap-minmax` (piece maximum instead
of minimum in the rectangle bound; the floor exceeds its Monte Carlo control), `drop-torus-error` (`eps = eps_0 = 0`;
exact replay fails), `sign-saddle` (index condition of `H_S` reversed; exact replay fails). The workflow
`c8-normalizer-floor-planar.yml` replays the manifest, the two main-resident pins, both check modes and the mutants.
`python3 -B -S floor.py --check-full --procs N` regenerates **every** one of the 11904 sub-box floors (9216 high, 2688 low) and requires exact
agreement with `RESULTS.json` (`--band low,high` and `--rbands i,j,...` restrict to bands or listed `r`-bands for a partial check); the workflow's
`full-regeneration` job runs it on demand (`workflow_dispatch`, two cores, about three hours), since the per-pull-request
job cannot carry it in both interpreter modes with the mutants. The certificate for a stored floor is its exact
regeneration; the manifest authenticates the bytes, not their derivation. The full run (`--procs 4`; 64 minutes for the high band and about 20 for the low band
on four cores) regenerates `RESULTS.json` deterministically (exact rationals; the floating controls are seeded).

## 7. Provenance

Pins ([LP] `dfed3b8d`, [NUM] `2648314f`) on `main` `3e0a91b`, verified by the workflow; `SOURCE_FILES.json` fingerprints
the packet. Method notes: the preconditioning is the finite-`r` form of the midpoint-jet expansion used in [LP]
section 5 and Math-#184 Lemma 1; the torus remainder bound is elementary; no external numerical library is used.
