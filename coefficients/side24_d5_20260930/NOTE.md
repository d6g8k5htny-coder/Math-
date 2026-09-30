# SIDE24 in dimension five: the birth-integrated cone moment `D_4`, certified, with `c_{5,ref}` and `c_{5,24}`

**Object:** `CL-SIDE24-D5-COEFFICIENT-20260930-v1`. **Author lane:** Anthropic / Claude (Claude Code
`session_017Mi3hxjaxV45x6zo6o1ee3`). **Kind:** certified numerical constant with its exact reduction (interval arithmetic
over `decimal` at 60 digits, exact integer roots, series with explicit remainders, one-dimensional Taylor quadrature with
Cauchy remainders). **Scientific effect:** NONE. No register, catalog, GRAPH or STATUS change; `coefficients/side24_v1`
unchanged; catalog entry C8 stays OPEN. Continuation of `coefficients/side24_d4_20260930` (Math-#199); scope claimed there
(comment 5917654115). Same GitHub account as every lane: zero organizational-independence credit.

## 0. Statement

For the reference law of SIDE24 in dimension `d = m + 1` (`A = Q + sqrt(2/3) Z I_m`, `Q` the `m x m` GOE of density
`∝ exp(-tr Q^2/4)`), `D_m = E[det(A)^2 1{A < 0}]` is the cone moment of [LP] (15.1). The `d = 4` record reduced `D_3` to
one dimension; this record does the same for `D_4` and certifies

    D_4 = 14.21876345897735760130646567787407831734060......        (enclosure width 3.9e-42),
    c_{5,ref} = Gamma(7/6) (3/2)^(1/3) D_4 / (12 sqrt3 pi^(7/2)) = 0.0132193193800849680760334875146413965210528......,
    |c_{5,24}/c_{5,ref} - 1| <= delta = 1.8554e-107.

The same code re-runs the `m = 2` and `m = 3` pipelines (rules D2_EXACT: `29/6 - sqrt6`; D3_CONSISTENT: the `D_3`
enclosure of Math-#199), evaluates Mehta's `Z_4 = 1536 pi` through the identical `m = 4` machinery (rule MEHTA_Z4), and
reproduces SIDE24's `d = 2, 3` intervals from the general coefficient formula (rule SIDE24_CONSISTENT).

## 1. The decoupling for every `m`

With the sector coordinates `mu_m = -a`, `mu_{m-j} = -(a + t_j)`, `t_j = p_1 + ... + p_j` (`j = 1, ..., m-1`), and
`T = sum_j t_j`, `S = -(m a + T)`, `|mu|^2 = m a^2 + 2 a T + sum_j t_j^2`, so the exponent of the `D_m` integrand is

    Q = |mu|^2/4 - S^2/(4(m+3)) = alpha a^2 + beta a + rest,
    alpha = 3m/(4(m+3)),   beta = 3T/(2(m+3)),   rest = sum_j t_j^2/4 - T^2/(4(m+3)).

The `a`-integral is exact as in the `d = 4` record (`G_0 = (1/2) sqrt(pi/alpha) e^{beta^2/(4 alpha)} erfc(beta/(2 sqrt alpha))`,
`G_{n+1} = (n G_{n-1} - beta G_n)/(2 alpha)`), and `beta^2/(4 alpha) = 3T^2/(4 m (m+3))`. Decompose `t = (T/(m-1)) 1 + u`
with `1 . u = 0`: `sum_j t_j^2 = T^2/(m-1) + |u|^2`. Hence

    erfc branch:        rest - beta^2/(4 alpha) = T^2/(4 m (m-1)) + |u|^2/4,
    polynomial branch:  rest                    = T^2/((m-1)(m+3)) + |u|^2/4,

for every `m` (`m = 3`: `s^2/24 + q^2/8` and `s^2/12 + q^2/8` with `s = T`, as in Math-#199; the general identity
`1/(4(m-1)) - 1/(4(m+3)) = 1/((m-1)(m+3))` gives the second line). The `erfc` argument is `beta/(2 sqrt alpha) = T sqrt(3/(4 m (m+3)))`:
`T sqrt21/28` at `m = 4`.

**`m = 4`.** `u = ((-2p_2 - p_3)/3, (p_2 - p_3)/3, (p_2 + 2p_3)/3)` and `|u|^2/4 = (p_2^2 + p_2 p_3 + p_3^2)/6`, the same
binary form as at `m = 3`; the region is `p_2, p_3 > 0`, `2 p_2 + p_3 < T` (from `p_1 = (T - 2p_2 - p_3)/3 > 0`). With
`v = 2 p_2 + p_3` (`p_2 = (v - p_3)/2`, `dp_1 dp_2 dp_3 = dT dv dp_3/6`): `|u|^2/4 = v^2/24 + p_3^2/8` and the region is
`0 < p_3 < v < T`. Writing the `a`-integrated polynomial of either branch as `sum_{a,k} T^a e_{a,k}(v) p_3^k`,

    I_4 = int_0^inf dT [ c_E e^{-T^2/48} erfc(T sqrt21/28) sum_a T^a L^E_a(T) + e^{-T^2/21} sum_a T^a L^R_a(T) ],
    L^X_a(T) = int_0^T e^{-v^2/24} q^X_a(v) dv,     q^X_a(v) = sum_k e^X_{a,k}(v) J_k(v),     J_k(v) = int_0^v p^k e^{-p^2/8} dp,      (1.1)

with `c_E = (1/2) sqrt(pi/alpha) = (1/2) sqrt(7 pi/3)`, and `D_4 = sqrt(3/7) . 4!/Z_4 . (1/6) I_4` (the `4!` orderings,
the Jacobian `1/6`). `Z_4 = 2^5 (2 pi)^2 Gamma(3/2) Gamma(2) Gamma(5/2) Gamma(3)/Gamma(3/2)^4 = 1536 pi` (Mehta), which the
same machinery re-derives: with `lambda_4 = t` free, `|lambda|^2/4 = (t - T/4)^2 + T^2/48 + |u|^2/4`, the `t`-integral is
`sqrt pi`, and `Z_4 = 4! sqrt pi (1/6) int dT e^{-T^2/48} int_0^T dv e^{-v^2/24} int_0^v V e^{-p_3^2/8} dp_3` with the
Vandermonde `V = p_1 p_2 p_3 (p_1+p_2)(p_2+p_3)(p_1+p_2+p_3)`, `p_1 = (T - v)/3` (rule MEHTA_Z4). The script verifies the
decoupled structure of both exponents symbolically before evaluating anything.

## 2. Cumulative integrals as Taylor factors

Every factor of (1.1) is entire in `T`, including the `L_a`: `L_a' (T) = e^{-T^2/24} q_a(T)` is a product of factors whose
Taylor coefficients at a centre `s_0` are known (`exp(-gamma s^2)` by its recurrence, the `J_k` by theirs, polynomials
exactly), so the coefficients of `L_a` at `s_0` are `L_a(s_0)` and `g_{n-1}/n` for `n >= 1`. The value `L_a(s_0)` is the
certified integral of `g_a` over `[0, s_0]`: the cells are traversed in increasing order, each cell contributes its full
integral to a running value at the grid points, and at the cell centre the left half-cell integral is added (both from
the same Taylor expansion of `g_a` at `s_0`, with the odd moments `int_{-h/2}^0 x^n dx = (-1)^n (h/2)^{n+1}/(n+1)` for the
half cell). On the disc `|z - s_0| <= rho`, `|L_a(z)| <= |L_a(s_0)| + rho . M_{g_a}(rho)` by integrating along the segment.
The outer integrand of a cell is then assembled as `const . prod(prefactors) . sum_a T^a L_a` in Taylor arithmetic with
the products of a short polynomial and a Taylor list done in `O(deg . K)`.

## 3. Certified quadrature

As in the `d = 4` record (v1.1): order `K = 40` at each centre; cells of width `1/2` on `[0, 30]` and `1` on `[30, 60]`
(on `[30, 90]` for the `Z_4` check, whose integrand decays only as `e^{-T^2/48}`);
the omitted tail of the (everywhere convergent) Taylor series at the centre bounded by Cauchy's estimate at the centre,
`|c_n| <= M_F(rho)/rho^n` with `rho = 6`, integrated with the geometric factor `1/(1 - h/(2 rho))`; disc bounds
`|e^{-gamma z^2}| <= e^{gamma rho^2} e^{-gamma (|s_0| - rho)_+^2}`, `|erfc(kappa z)| <= 1 + (2 kappa/sqrt pi)|z| e^{kappa^2 rho^2}`,
`|J_k(z)| <= |z|^{k+1} e^{rho^2/8}/(k+1)`, polynomials by absolute coefficients, and the `L_a` bound of section 2. Beyond
`T = 60`: `erfc(x) <= e^{-x^2}` (`x >= 0`), so the `erfc` branch decays as `e^{-T^2(1/48 + 21/784)} = e^{-T^2/21}` like the
polynomial branch, `|L_a(T)| <= Lbar_a := sum_{k,j} |e_{a,k,j}| J_k(inf) int_0^inf v^j e^{-v^2/24} dv`, and the tail is
bounded by the incomplete-gamma estimates of the `d = 4` record. The `m = 2` and `m = 3` integrals are the `d = 4`
record's, re-run unchanged.

## 4. The coefficient and the torus transfer in `d = 5`

`c_{d,ref} = Gamma(7/6) (3/2)^(1/3) |S^{d-1}| D_{d-1} / (sqrt3 sqrt pi (2 pi)^d)` ([LP] (15.2), `p_G(0) p_V(0) = (2 pi)^{-d}/sqrt3`,
`tau^{4/3} = 6^{2/3}`); `|S^4| = 2 pi^{5/2}/Gamma(5/2) = 8 pi^2/3`, so `c_{5,ref} = Gamma(7/6) (3/2)^(1/3) D_4 / (12 sqrt3 pi^{7/2})`
(rule CLOSED_FORM_D5 against the general formula; `d = 2, 3` inside SIDE24's intervals, `d = 4` equal to Math-#199's).

**Transfer to `K_24`, `d = 5`** (SIDE24 sections 2-4 with the `d = 5` constants). (i) Image bound: the shell `|n|_inf = j`
holds `(2j+1)^5 - (2j-1)^5 = 160 j^4 + 80 j^2 + 2 <= 242 j^4` points with `|n|^2 <= 5 j^2`, so
`sum_{n != 0} |n|^6 e^{-288 |n|^2} <= 30250 sum_j j^{10} e^{-288 j^2} <= 60500 e^{-288}` (ratio of successive terms below `1/2`),
and every 3-jet covariance entry of `K_24` is within `E_5 = 60500 (76 . 24^6 + 15) e^{-288} = 7.3625e-111` of its reference value.
(ii) Sandwich: the jet `(G, t, svec H)` has dimension `n = d + 1 + d(d+1)/2 = 21`; spectral norm of the difference at most
`2 n E_5`; `C_ref >= I/3` (Hessian block eigenvalues `d + 2 = 7` and `2`, odd block `1` and `8 +- sqrt58`); hence
`(1 - eps) C_ref <= C_24 <= (1 + eps) C_ref` with `eps = 126 E_5 = 9.2768e-109`. (iii) Ratios: `a = m + 2/3 + n_A/2 = 29/3`
(`n_A = m(m+1)/2 = 10`), `b = d + n_A/2 = 10`; since `(1+eps)^{29/3} <= (1+eps)^{10}`, the ratio lies in `[1/(1+delta), 1+delta]`
with `delta = (1+eps)^{10}/(1-eps)^{10} - 1 = 20 eps + O(eps^2)` (computed without cancellation; rule TRANSFER_BOUND
certifies `19 eps <= delta <= 21 eps` for every represented value, `delta.lo >= 19 eps.hi` and `delta.hi <= 21 eps.lo`, and
records that the enclosures of `delta` and `20 eps` intersect: the offset `delta - 20 eps ~ 210 eps^2 ~ 2e-214` lies far below
the arithmetic resolution of the two enclosures, so `20 eps <= delta` is not separable and is not claimed as certified). So `|c_{5,24}/c_{5,ref} - 1| <= 1.8554e-107`, below the arithmetic width; the printed
digits of `c_{5,24}` are those of `c_{5,ref}`. The exact periodic constant is enclosed, not equated to the reference.

## 5. Values (`RESULTS.json`)

| quantity | enclosure (leading digits) | width |
|---|---|---|
| `D_2` | `29/6 - sqrt6` (rule D2_EXACT) | `1e-50` |
| `D_3` | `5.3231802688898968949231987396872606357843885294...` (= Math-#199) | `6.5e-47` |
| `D_4` | `14.21876345897735760130646567787407831734060......` | `3.9e-42` |
| `Z_4` (quadrature) | `4825.4863159139224142786202367173164301268521974...` ∋ `1536 pi` (rule MEHTA_Z4) | `1.8e-45` |
| `c_{2,ref}`, `c_{3,ref}`, `c_{4,ref}` | inside SIDE24's `d = 2, 3` intervals; `0.0233216660029528350945...` | |
| `c_{5,ref}` | `0.0132193193800849680760334875146413965210528......` | `3.6e-45` |
| `c_{5,24}` | the same digits; `|c_{5,24}/c_{5,ref} - 1| <= 1.8554e-107` | |
| `E_5`, `eps`, `delta` | `7.3625e-111`, `9.2768e-109`, `1.8554e-107` | |

Floating controls (not part of the certificate; ten digits in `RESULTS.json`): orthant midpoint quadratures of the
`m`-dimensional integral (`m = 2, 3, 4`; the `m = 4` grid `28^4` on `[-14, 0]^4` is coarse, `13.51`), and the 3-D
midpoint quadrature of the `a`-integrated `(p_1, p_2, p_3)` integrand (`56^3`, `14.53`), which uses none of the
`(T, v)` substitutions, the `J_k` or the cumulative integrals. Offline, the latter at `60^3` and `120^3` (`14.4878`,
`14.2852`) Richardson-extrapolates to `14.2176`; a Monte Carlo of the `4 x 4` matrix definition gives `13.4 +- 1.3`.

## 6. Rules, mutants, verification

`python3 -B -S cone_moment_d5.py` (also `-B -O -S`; about eighty seconds) prints `RESULTS.json` and exits `0` only if all
thirteen rules hold: FLOAT_INSIDE, D2_EXACT, D3_CONSISTENT (intersects Math-#199's enclosure, width below `1e-40`),
MEHTA_Z4 (intersects both Mehta's value and `1536 pi`, width below `1e-40`; the quadrature width is `1.8e-45`), WIDTHS,
SIDE24_CONSISTENT, CLOSED_FORM_D5,
TRUNCATION_NESTING (order `20`, cells of width `1`: intersects and is wider), MONOTONE (`4/3 < D_2 < D_3 < D_4`,
`c_{2,ref} > c_{3,ref} > c_{4,ref} > c_{5,ref} > 0`), IMAGE_BOUND (`E_5` in `(7e-111, 8e-111)`), TRANSFER_BOUND (section 4:
`19 eps <= delta <= 21 eps` in the proving direction, intersection with `20 eps`, `c_{5,24}` encloses `c_{5,ref}`),
LIBRARY_EXACT (the decimal module's `exp`, `sqrt` and the interval negation against exact rational brackets), PINNED.
Mutants (`--mutant`, each must exit `1`): `shift-variance` (`S^2/24` for `S^2/28` at `m = 4`), `vandermonde`,
`erfc-branch` (halved), `remainder-dropped` (order `6`, cells of width `1`, no remainder), `mehta` (`Z_5` for `Z_4`),
`sphere-area` (`4 pi^2` for `8 pi^2/3`), `image-shells` (half the shell count), `sandwich-exponent` (`b = 8`),
`recurrence` (`P_3` scaled by `101/100`), `jacobian` (`1/2` for `1/6`, also in the `Z_4` check), `cumulative-half`
(the left half-cell integral omitted from `L_a(s_0)`). The workflow `side24-d5-coefficient.yml` replays the manifest,
the three main-resident pins, the SIDE24 intervals quoted in the script, both interpreter modes byte for byte against
`RESULTS.json` and the eleven mutants in each, on a clean tree.

## 7. What this does not do

Not a proof or review of [LP] or SIDE24 sections 1-4 (consumed at their scope). Not `d >= 6`: the decoupling of section 1
holds for every `m`, but the `u`-integral for `m = 5` is over a three-dimensional simplex slice and would need one more
level of cumulative integrals (the method extends; it is not done here). Not a window coefficient, `C`, `r_*` or `z_*`;
no closed form for `D_4`. No register, catalog, GRAPH or STATUS change; C8 stays OPEN. Claude reads of this packet count
for nothing; the author will not merge.

## 8. Provenance

Pins on `main 3e0a91b` ([LP] `dfed3b8d`, SIDE24 `PROOF.md` `44b66f04`, `ENCLOSURE.json` `57af39a0`) verified by the
workflow; read, not pinned: the SIDE24 remainder record and the C8 catalog entry; unmerged companion Math-#199 at `4fc6d15`
(the `d = 4` record whose `m = 2, 3` pipelines and interval toolkit are re-used verbatim and whose `D_3` enclosure is
quoted). Mehta's integral at `m <= 4` is verified inside the record (`m = 4` by rule MEHTA_Z4). No external numerical
library is used.

## 9. Revisions

- **v1.1 (Codex review 5371328766 on `33d50de`, three P2 findings, all taken).** (i) The displayed `D_4` and `c_{5,ref}`
  values in sections 0 and 5 carried digits beyond the common prefix of the two endpoints; they now stop at the last common
  digit (`D_4 = 14.21876345897735760130646567787407831734060…`, 43 significant digits; `c_{5,ref} = …5210528…`). (ii) The
  `Z_4` quadrature width was misreported as `1e-53` (the width of Mehta's closed-form interval); it is `1.8e-45`, and rule
  MEHTA_Z4 now requires width below `1e-40`. (iii) Rule TRANSFER_BOUND compared endpoints in the non-proving direction; it now
  certifies `19 eps <= delta <= 21 eps` for every represented value (`delta.lo >= 19 eps.hi`, `delta.hi <= 21 eps.lo`) and
  records the intersection of the `delta` and `20 eps` enclosures (section 4). No certified value changed; the two rule
  thresholds tightened.
