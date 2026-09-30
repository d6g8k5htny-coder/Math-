# SIDE24 in dimension four: the birth-integrated cone moment `D_3`, certified, with `c_{4,ref}` and `c_{4,24}`

**Object:** `CL-SIDE24-D4-COEFFICIENT-20260930-v1`. **Author lane:** Anthropic / Claude (Claude Code
`session_017Mi3hxjaxV45x6zo6o1ee3`). **Kind:** certified numerical constant with its exact reduction: interval arithmetic
over `decimal` (60 digits, directed rounding), exact integer roots, series with explicit remainders, and a one-dimensional
Taylor quadrature whose remainder is bounded by Cauchy's estimate. **Scientific effect:** NONE. No register, catalog,
GRAPH or STATUS change; `coefficients/side24_v1` is unchanged; catalog entry C8 stays OPEN. Scope claimed on Math-#197
(comment 5916664092). Same GitHub account as every lane: zero organizational-independence credit.

## 0. Statement

`coefficients/side24_v1` evaluates the coefficient (15.2) of [LP] for the periodized Gaussian kernel of side `L = 24` in
`d = 2, 3`. Its reference law (section 1 there) is, in dimension `d = m + 1`: the transverse Hessian given `V = 0` is
`A = Q + sqrt(2/3) Z I_m`, `Q` the `m x m` GOE with density proportional to `exp(-tr Q^2/4)` (diagonal variance `2`,
off-diagonal `1`) and `Z` an independent standard normal, and the cone moment of [LP] (15.1) is

    D_m = E[ det(A)^2 1{A negative definite} ],        D_1 = 4/3,   D_2 = 29/6 - sqrt6.

**Certified.** `D_3 = 5.323180268889896894923198739687260635784388529409...` (enclosure width `6.3e-47`), whence, by [LP]
(15.2) with `|S^3| = 2 pi^2`, `p_G(0) p_V(0) = (2 pi)^-4/sqrt3`, `tau^2 = 6`,

    c_{4,ref} = Gamma(7/6) (3/2)^(1/3) D_3 / (8 sqrt3 pi^(5/2)) = 0.023321666002952835094521194952856885153101372363...

and for the torus kernel `K_24` in `d = 4`, by the covariance sandwich of SIDE24 sections 3-4 with the `d = 4` constants,

    |c_{4,24} / c_{4,ref} - 1| <= delta = 1.5702e-108,       c_{4,24} = 0.023321666002952835094521194952856885153101372363...

The same code path at `d = 2, 3` returns enclosures inside SIDE24's intervals for `c_{2,24}` and `c_{3,24}` (rule
SIDE24_CONSISTENT), and its `m = 2` cone moment encloses `29/6 - sqrt6` (rule D2_EXACT), which tests every step of the
reduction that `m = 3` shares.

## 1. The cone moment as a shifted GOE integral

Let `lambda_1, ..., lambda_m` be the eigenvalues of `Q`, with joint density `|Delta(lambda)| exp(-|lambda|^2/4) / Z_m` on
`R^m` (unordered), `Z_m = int_{R^m} prod_{i<j} |lambda_i - lambda_j| exp(-|lambda|^2/4) dlambda`. Mehta's integral at
`beta = 1`, after `lambda = sqrt2 x`, gives

    Z_m = 2^(m/2 + m(m-1)/4) (2 pi)^(m/2) prod_{j=1}^m Gamma(1 + j/2) / Gamma(3/2)^m:    Z_1 = 2 sqrt pi,  Z_2 = 8 sqrt(2 pi),  Z_3 = 48 sqrt2 pi

(`Z_2` is also the elementary `(1/2) int |u| e^{-u^2/8} du int e^{-v^2/8} dv`; `Z_3` is re-derived in closed form below
and is a certified rule). With `c = sqrt(2/3)` the eigenvalues of `A` are `mu_i = lambda_i + cZ`, `A < 0` iff all
`mu_i < 0`, and `det(A)^2 = prod mu_i^2`. Writing `S = sum mu_i` and integrating `Z` first,

    int phi(z) exp(-|mu - cz 1|^2/4) dz = exp(-|mu|^2/4) int phi(z) exp(czS/2 - m c^2 z^2/4) dz
                                       = sqrt(3/(m+3)) exp(-|mu|^2/4 + S^2/(4(m+3))),

since `int phi(z) exp(uz - vz^2) dz = (1 + 2v)^{-1/2} exp(u^2/(2(1+2v)))` with `u = cS/2`, `v = m c^2/4`,
`1 + 2v = 1 + m/3 = (m+3)/3` and `u^2/(2(1+2v)) = (S^2/6) . 3/(2(m+3)) = S^2/(4(m+3))`. Hence

    D_m = sqrt(3/(m+3)) / Z_m . int_{(-inf,0)^m} prod_i mu_i^2 prod_{i<j} |mu_i - mu_j| exp(-|mu|^2/4 + S^2/(4(m+3))) dmu.   (1.1)

For `m = 1`: `(sqrt3/2) (2 sqrt pi)^-1 int_{-inf}^0 mu^2 e^{-3 mu^2/16} dmu = 4/3`. For `m = 2` the `m!` orderings are
equal, and in `mu_2 = -a`, `mu_1 = -a - p` the exponent is `(3/10) a^2 + (3/10) a p + (1/5) p^2`; the `a`-integral is exact
(section 2 with `alpha = 3/10`, `beta = 3p/10`) and the script's quadrature of the resulting one-dimensional integral
encloses `29/6 - sqrt6` to `1e-50` (rule D2_EXACT). This is the end-to-end check of the `a`-integration recurrence, the
`erfc` branch, the Mehta constant and the quadrature.

**`Z_3` in closed form.** The decoupling of section 2 also evaluates Mehta's constant at `m = 3` without the general
formula: on the ordered sector put `lambda_3 = t`, `lambda_2 = t - p`, `lambda_1 = t - p - q` (`t` real, `p, q > 0`), so
`|Delta| = p q (p+q)` and `|lambda|^2/4 = (3/4)(t - s/3)^2 + (p^2 + pq + q^2)/6` with `s = 2p + q`; the `t`-integral is
`2 sqrt(pi/3)`, and in `(s, q)` the rest is `s^2/24 + q^2/8` with `p q (p+q) = q (s^2 - q^2)/4`. Hence
`Z_3 = 6 . 2 sqrt(pi/3) . (1/8) int_0^inf e^{-s^2/24} [s^2 J_1(s) - J_3(s)] ds = (3/2) sqrt(pi/3) int_0^inf e^{-s^2/24} (4 s^2 - 32 + 32 e^{-s^2/8}) ds`,
and `int_0^inf s^2 e^{-s^2/24} ds = 12 sqrt6 sqrt pi`, `int_0^inf e^{-s^2/24} ds = sqrt6 sqrt pi`, `int_0^inf e^{-s^2/6} ds = (1/2) sqrt6 sqrt pi`
give `(3/2) sqrt(pi/3) . 32 sqrt6 sqrt pi = 48 sqrt2 pi`. Rule MEHTA_Z3 certifies this integral by the section 3 quadrature and
requires it to enclose both the Mehta value and `48 sqrt2 pi`.

## 2. `m = 3`: exact reduction to one dimension

On the ordered sector `mu_1 < mu_2 < mu_3 < 0` put `mu_3 = -a`, `mu_2 = -a - p`, `mu_1 = -a - p - q` (`a, p, q > 0`,
Jacobian `1`). Then `prod mu_i^2 = a^2 (a+p)^2 (a+p+q)^2`, `|Delta| = p q (p+q)`, and

    |mu|^2/4 - S^2/24 = Q(a, p, q) = (3/8) a^2 + (1/3) p^2 + (5/24) q^2 + (1/2) a p + (1/4) a q + (1/3) p q,

so that `D_3 = (1/sqrt2) (6/Z_3) I_3 = I_3 / (16 pi)`, `I_3 = int_{(0,inf)^3} a^2 (a+p)^2 (a+p+q)^2 p q (p+q) e^{-Q} da dp dq`.

**The `a`-integral.** With `alpha = 3/8`, `beta = p/2 + q/4`, `G_n(beta) = int_0^inf a^n e^{-alpha a^2 - beta a} da`:

    G_0 = (1/2) sqrt(pi/alpha) e^{beta^2/(4 alpha)} erfc(beta/(2 sqrt alpha)),   G_1 = (1 - beta G_0)/(2 alpha),
    G_{n+1} = (n G_{n-1} - beta G_n)/(2 alpha)                                     (integrate (a^n e^{...})' over (0, inf)),

so `G_n = P_n(beta) G_0 + R_n(beta)` with polynomials `P_n` (degree `n`) and `R_n` (degree `n-1`) of rational
coefficients. Expanding `a^2 (a+p)^2 (a+p+q)^2 = sum_n w_n(p,q) a^n` (`n = 2..6`) and multiplying by `p q (p+q)`,

    I_3 = int_{(0,inf)^2} [ (1/2) sqrt(8 pi/3) P_E(p,q) e^{-(p^2 + pq + q^2)/6} erfc((2p+q)/(2 sqrt6)) + P_R(p,q) e^{-(p^2/3 + 5q^2/24 + pq/3)} ] dp dq,

because `beta^2/(4 alpha) = p^2/6 + pq/6 + q^2/24` cancels against the `(p,q)` part of `Q` to leave `-(p^2 + pq + q^2)/6`,
and `beta/(2 sqrt alpha) = (2p + q)/(2 sqrt6)`; `P_E = sum_n w_n P_n(beta) . pq(p+q)` (degree `9`), `P_R = sum_n w_n R_n(beta) . pq(p+q)`
(degree `8`), all with rational coefficients computed exactly by the script.

**Decoupling.** With `s = 2p + q` and `q` (so `p = (s - q)/2`, `dp dq = ds dq/2`, region `0 < q < s`):

    p^2 + pq + q^2 = s^2/4 + 3 q^2/4,      p^2/3 + 5q^2/24 + pq/3 = s^2/12 + q^2/8,

so both exponents split, `-(s^2/24 + q^2/8)` and `-(s^2/12 + q^2/8)`, and the `erfc` depends on `s` alone (the script
verifies this structure symbolically before evaluating anything). Writing `P_E((s-q)/2, q) = sum_k e_k(s) q^k`,
`P_R((s-q)/2, q) = sum_k r_k(s) q^k` (`k <= 9`) and `J_k(s) = int_0^s q^k e^{-q^2/8} dq`,

    I_3 = (1/2) int_0^inf [ (1/2) sqrt(8 pi/3) e^{-s^2/24} erfc(s/(2 sqrt6)) sum_k e_k(s) J_k(s) + e^{-s^2/12} sum_k r_k(s) J_k(s) ] ds,   (2.1)
    J_0 = sqrt(2 pi) erf(s/(2 sqrt2)),   J_1 = 4 (1 - e^{-s^2/8}),   J_{k+2} = -4 s^{k+1} e^{-s^2/8} + 4(k+1) J_k.

Every factor in (2.1) is an entire function of `s`: polynomials, `exp(-gamma s^2)`, `erf`/`erfc` of a multiple of `s`, and
the `J_k`.

## 3. Certified quadrature (Taylor expansion with Cauchy remainders)

On each cell `[s_0 - h/2, s_0 + h/2]` (`h = 1/2`, `s_0` rational, `0 < s < T = 60`) the integrand `F` is expanded to order
`K = 40` at `s_0`: the Taylor coefficients of `exp(-gamma s^2)` come from `(n+1) y_{n+1} = -2 gamma (s_0 y_n + y_{n-1})`
with `y_0 = exp(-gamma s_0^2)` (an interval), those of `erf(kappa s)`/`erfc(kappa s)` from the Gaussian's
(`(2 kappa/sqrt pi) exp(-kappa^2 s^2)`) by division by `n + 1`, with `erf(kappa s_0)` from the positive series, those of the
`J_k` from their recurrence in Taylor arithmetic, and polynomials exactly; products are Cauchy products of interval
coefficient lists. The cell integral of the degree-`K` polynomial is exact (odd powers vanish). For the remainder: `F` is entire, so its
Taylor series at `s_0`, `F(s_0 + x) = sum_n c_n x^n`, converges for every `x`, and Cauchy's estimate at the centre gives
`|c_n| <= M_F(rho)/rho^n` for every `n`, where `M_F(rho)` bounds `|F(z)|` on `|z - s_0| <= rho` (`rho = 6`); by the
triangle inequality `M_F` is the corresponding sum of products of factor bounds, each elementary on the disc:

    |exp(-gamma z^2)| <= exp(gamma rho^2) exp(-gamma (|s_0| - rho)_+^2),
    |erf(kappa z)| <= (2 kappa/sqrt pi) |z| exp(kappa^2 rho^2),        |erfc(kappa z)| <= 1 + that,
    |J_k(z)| = |int_0^1 (tz)^k e^{-t^2 z^2/8} z dt| <= |z|^(k+1) exp(rho^2/8)/(k+1),      |poly(z)| <= sum |c_j| |z|^j,

with `|z| <= |s_0| + rho` (for `exp`: `|e^{-gamma z^2}| = e^{-gamma(x^2 - y^2)}`, `|y| <= rho`, `|x| >= (|s_0| - rho)_+`; for
`erf` and `J_k`: integrate along the segment from `0` to `z`, on which `|e^{-t^2}| <= e^{(Im t)^2}`). The omitted tail
of the series integrates to at most

    int_{-h/2}^{h/2} sum_{n > K} |c_n| |x|^n dx <= M_F(rho) sum_{n > K} rho^{-n} 2 (h/2)^{n+1}/(n+1)
                                            <= M_F(rho) rho^{-(K+1)} . 2 (h/2)^{K+2}/(K+2) . 1/(1 - h/(2 rho))

per cell (`1/(n+1) <= 1/(K+2)` and the geometric series in `h/(2 rho) = 1/24`; of order `1e-33` here). The v1.0 text
applied Cauchy's estimate at an off-centre point `xi` with the full radius `rho`, which is not justified (the disc around
`xi` inside the bounded disc has radius `rho - |xi - s_0|`); the centre-based tail bound above replaces it (Codex
4148001628) and is what the script computes.
Beyond `T` each branch is bounded by `|const| . tail_poly(s) e^{-gamma s^2}` with `erfc <= 2`, `|J_k| <= J_k(inf) = (1/2) 8^{(k+1)/2} Gamma((k+1)/2)`,
and `int_T^inf s^j e^{-gamma s^2} ds = (1/2) gamma^{-(j+1)/2} Gamma((j+1)/2, gamma T^2)`, the upper incomplete gamma
bounded by `x^{a-1} e^{-x}/(1 - (a-1)/x)` (`a > 1`) or `x^{a-1} e^{-x}` (`a <= 1`); at `T = 60` this is below `1e-45`.
The `m = 1` and `m = 2` integrals go through the same routine (their integrands are `poly . exp` and
`poly . exp . erfc`); rule TRUNCATION_NESTING re-runs `m = 3` with `K = 20`, `h = 1` and requires the coarser enclosure
to intersect and to be wider.

## 4. The coefficient and the torus transfer in `d = 4`

[LP] (15.2) for the reference kernel: `c_{d,ref} = Gamma(7/6) (24)^{-1/3} pi^{-1/2} |S^{d-1}| p_G(0) p_V(0) tau^{4/3} D_{d-1}`
with `p_G(0) p_V(0) = (2 pi)^{-d}/sqrt3`, `tau^{4/3} = 6^{2/3}`, `|S^{d-1}| = 2 pi^{d/2}/Gamma(d/2)`, i.e.

    c_{d,ref} = Gamma(7/6) (3/2)^(1/3) |S^{d-1}| D_{d-1} / (sqrt3 sqrt pi (2 pi)^d):
    d = 2: /(2 sqrt3 pi^(3/2)),   d = 3: /(2 sqrt3 pi^(5/2))   (SIDE24 (1)),   d = 4: c_{4,ref} = Gamma(7/6) (3/2)^(1/3) D_3 / (8 sqrt3 pi^(5/2)).

The script evaluates the general formula (rule CLOSED_FORM_D4 compares it with the displayed `d = 4` form) and at
`d = 2, 3` with the certified `D_1`, `D_2` lands inside SIDE24's `c_{2,24}`, `c_{3,24}` intervals widened by their
`1e-106` periodization allowance (rule SIDE24_CONSISTENT).

**Transfer to `K_24`, `d = 4`.** SIDE24 sections 2-4 are dimension-generic except for three constants, restated here.
(i) Image bound: for `|x| >= 1` every unit-direction contraction of order `q <= 6` of `phi = exp(-|x|^2/2)` is bounded by
`76 |x|^6 phi(x)`, and by `15` at `0` (SIDE24 section 2). In `d = 4` the shell `|n|_inf = j` holds `(2j+1)^4 - (2j-1)^4 = 64 j^3 + 16 j <= 80 j^3`
points with `|n|^2 <= 4 j^2`, so `sum_{n != 0} |n|^6 e^{-288 |n|^2} <= 5120 sum_j j^9 e^{-288 j^2} <= 10240 e^{-288}` (successive
terms have ratio below `1/2`), and every covariance entry of the 3-jet of `K_24` is within
`E_4 = 10240 (76 . 24^6 + 15) e^{-288} = 1.2462e-111` of its reference value (normalization `S >= 1`).
(ii) Sandwich: the joint covariance of `(G, t, svec H)` has dimension `n = d + 1 + d(d+1)/2 = 15`, so the spectral norm of
the difference is at most `2 n E_4 = 30 E_4`; the reference matrix satisfies `C_ref >= I/3` in every `d` (Hessian block
eigenvalues `d + 2` and `2`; odd block eigenvalues `1` and `8 +- sqrt58 > 1/3`), hence `(1 - eps) C_ref <= C_24 <= (1 + eps) C_ref`
with `eps = 90 E_4 = 1.1215e-109`, in every frame, and the same for marginals and Schur complements.
(iii) Ratios: as in SIDE24 section 4, the integrand of (15.2) changes by a factor between `(1-eps)^a/(1+eps)^b` and
`(1+eps)^a/(1-eps)^b` with `a = m + 2/3 + n_A/2 = 20/3` (`h` of degree `2m` under covariance scaling, `tau^{4/3}`, the
density-comparison constant with `n_A = m(m+1)/2 = 6`) and `b = d + n_A/2 = 7` (the two `d`-dimensional densities at `0`
and the determinant factor). Since `(1+eps)^{20/3} <= (1+eps)^7`, the ratio lies in `[1/(1+delta), 1 + delta]` with
`delta = (1+eps)^7/(1-eps)^7 - 1 = [sum_k (C(7,k) - (-1)^k C(7,k)) eps^k]/(1-eps)^7 = 14 eps + O(eps^2)`, computed without
cancellation (rule TRANSFER_BOUND certifies `13 eps <= delta <= 15 eps` for every represented value, `delta.lo >= 13 eps.hi`
and `delta.hi <= 15 eps.lo`, and records that the enclosures of `delta` and `14 eps` intersect: the offset
`delta - 14 eps ~ 105 eps^2 ~ 1e-216` lies far below the arithmetic resolution of the two enclosures, so `14 eps <= delta`
is not separable and is not claimed as certified); positivity of every reference integrand lets the
bound pass through the angular integral. So `|c_{4,24}/c_{4,ref} - 1| <= 1.5702e-108`, far below the arithmetic width of
`c_{4,ref}`, and the printed digits of `c_{4,24}` are those of `c_{4,ref}`. The exact periodic constant is not claimed equal to
the reference constant; it is enclosed.

## 5. Values (`RESULTS.json`)

| quantity | enclosure (leading digits) | width |
|---|---|---|
| `D_1` | `4/3` (rule D1_EXACT) | `< 1e-40` |
| `D_2` | `2.38384359055015523513604925862744194136738585267666...` = `29/6 - sqrt6` (rule D2_EXACT) | `1e-50` |
| `D_3` | `5.323180268889896894923198739687260635784388529409...` | `6.3e-47` |
| `c_{2,ref}` | `0.07340691930603427103013596295777...` (inside SIDE24's `c_{2,24}` interval) | `2.4e-50` |
| `c_{3,ref}` | `0.04177593184059834334293666542857...` (inside SIDE24's `c_{3,24}` interval) | `1.9e-52` |
| `c_{4,ref}` | `0.023321666002952835094521194952856885153101372363...` | `2.7e-49` |
| `c_{4,24}` | the same digits; `|c_{4,24}/c_{4,ref} - 1| <= 1.5702e-108` | |
| `E_4`, `eps`, `delta` | `1.2462e-111`, `1.1215e-109`, `1.5702e-108` | |
| `Z_3` | `48 sqrt2 pi = 213.25838103...` (floating cube quadrature `212.2`) | |

Floating controls (not part of the certificate; printed to ten digits): orthant midpoint quadrature of (1.1) at
`m = 1, 2, 3` (`1.333333333`, `2.383737`, `5.3098` on a `90^3` grid) and the `(p, q)` midpoint quadrature of the
`a`-integrated integrand (`5.32335`, `1200^2` grid, error `O(h^2)`), which does not use the `s`-substitution, the
`q`-integration or the `J_k`. Offline, the same `(p, q)` quadrature at `2400^2` and `4800^2` points (`5.3232355`,
`5.3231941`) Richardson-extrapolates to `5.3231802687`, within `2e-10` of the certified `D_3`.

## 6. Rules, mutants, verification

`python3 -B -S cone_moment_d4.py` (also `-B -O -S`; about thirty seconds) prints `RESULTS.json` and exits `0` only if all
thirteen rules hold: FLOAT_INSIDE (the four floating controls and the `Z_3` cube within their tolerances), D1_EXACT,
D2_EXACT, WIDTHS (`D_1`, `D_2` below `1e-40`, `D_3` and `c_{4,ref}` below `1e-30`), SIDE24_CONSISTENT, CLOSED_FORM_D4,
TRUNCATION_NESTING, MONOTONE (`D_1 < D_2 < D_3`, `c_{2,ref} > c_{3,ref} > c_{4,ref} > 0`), IMAGE_BOUND (`E_4` in
`(1.2e-111, 1.3e-111)`), TRANSFER_BOUND, MEHTA_Z3 (section 1), LIBRARY_EXACT (the decimal module's `exp` and `sqrt`, and the interval negation,
against exact rational brackets at six arguments), PINNED (forty-six digits of `D_3`, forty-eight of `c_{4,ref}`, fifty of
`pi`). Mutants (`--mutant`, each must exit `1`): `shift-variance` (`S^2/20` for `S^2/24` at `m = 3`), `vandermonde`
(the Vandermonde factor dropped), `erfc-branch` (the `erfc` branch halved), `remainder-dropped` (order `6`, cells of
width `1`, no Cauchy remainder), `mehta` (`Z_4` for `Z_3`), `sphere-area` (`4 pi` for `2 pi^2`), `image-shells` (half the
shell count), `sandwich-exponent` (`b = 5`), `recurrence` (`P_3` scaled by `101/100`). The workflow
`side24-d4-coefficient.yml` replays the manifest, the three main-resident pins, checks that the SIDE24 intervals quoted in
the script are those of `ENCLOSURE.json`, runs both interpreter modes byte for byte against `RESULTS.json` and the nine
mutants in each, on a clean tree.

## 7. What this does not do

Not a proof or review of [LP] or of SIDE24's sections 1-4, which are consumed at their stated scope (the reference law,
the identification of (15.2) with the persistence coefficient, the covariance sandwich). Not `d >= 5` (the `m = 4` sector
integral has three remaining variables after the `a`-integration; whether a linear substitution decouples them as
`s = 2p + q` does here is not examined). Not a window coefficient, a finite-radius quantity, `C`, `r_*` or `z_*`; not a
closed form for `D_3` (the one-dimensional integral (2.1) is of `erf . erfc . Gaussian . polynomial` type and may have one
in terms of `arctan` and square roots; none is claimed). No register, catalog, GRAPH or STATUS change; C8 stays OPEN.
Claude reads of this packet count for nothing; the author will not merge.

## 8. Provenance

Pins on `main 3e0a91b` ([LP] `dfed3b8d`, SIDE24 `PROOF.md` `44b66f04`, `ENCLOSURE.json` `57af39a0`) verified by the
workflow; read, not pinned: the SIDE24 remainder record (`0bcf0a6f`) and the C8 catalog entry (`02455f05`).
`SOURCE_FILES.json` fingerprints the packet. The general `Z_m` is Mehta's integral (the Gaussian specialization of
Selberg's integral, Mehta, *Random Matrices*, chapter 17); at `m <= 3`, the only cases used, it is verified inside the
record (`m = 1` trivially, `m = 2` by the elementary two-variable integral, `m = 3` by rule MEHTA_Z3). Cauchy's estimate
and the Lagrange remainder are elementary. The interval class is the repaired class of Math-#190 v1.3 / Math-#197 (exact
negation, explicit contexts, rule LIBRARY_EXACT). No external numerical library is used.

## 9. Revisions

- **v1.1 (Codex review thread 4148001628 on `54dd458`, taken).** The v1.0 text applied Cauchy's estimate off-centre without
  shrinking the radius; the remainder is now the centre-based Taylor tail with the geometric factor `1/(1 - h/(2 rho))`
  (section 3, `enclose_integral`). Values unchanged.
- **v1.2 (Codex thread 4148778791 on Math-#200, the same construction there; applied here for consistency).** Rule
  TRANSFER_BOUND compared endpoints in the non-proving direction and section 4 described it as checking
  `14 eps <= delta <= 15 eps`; it now certifies `13 eps <= delta <= 15 eps` for every represented value (`delta.lo >= 13 eps.hi`,
  `delta.hi <= 15 eps.lo`) and records the intersection of the `delta` and `14 eps` enclosures (section 4). No certified value
  changed. Math-#201 gives `D_3` in closed form, `(50 pi + 200 arctan 2 - 228)/(9 pi)`, at 47 common digits with this record's
  enclosure; this record is otherwise unchanged and its section 7 non-claim stands as written at v1.0.
