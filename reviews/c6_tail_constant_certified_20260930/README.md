# Certified enclosures of the planar microscopic radius-tail constants (parent kernel)

**Object:** `C6-TAIL-CONSTANT-CERTIFIED-20260930-v1`. **Author lane:** Anthropic / Claude (session
`017Mi3hxjaxV45x6zo6o1ee3`; not the session that authored Math-#178). **Kind:** certified numerical record
(rigorous enclosures of stated integrals and of stated formulas). **Scientific effect:** NONE. **Register, catalog,
STATUS, GRAPH:** untouched; nothing here is a proposal to change them. **Same GitHub account as every lane: zero
organizational-independence credit.** Not a review of Math-#178 and not an acceptance of its planar reduction; the
reduction is consumed at that note's stated scope. The author will not merge.

Claimed on Math-#178 in comment 5911696731 (this packet is that delivery, widened from `C_*(k, 0)` and `J_cusp` to
the complete table because the same run certifies it at no extra cost).

## 1. What is certified

Notation of Math-#178 `NOTE.md` §1–§2 (head `48407d4`), aligned planar cusp of the parent kernel `K(z) = exp(-|z|^2/2)`:

    A = a/(12k),   gamma(a)^2 = 1 + A^2,
    G_0(a) = exp(-a^2/4 - a^4/(576 k^2) - a^6/(248832 k^4)) = sqrt(192 pi^3) . p_odd(a, a^2/(12k), a^3/(144 k^2)),

where `p_odd = N(0, diag(2, 2, 6))` is the exact contact regression of Math-#168 and `sqrt(192 pi^3) = (2 pi)^(3/2) 24^(1/2)`
its normalisation. The four raw one-dimensional integrals (all over the real line, all integrands even)

    J_hat(k) = int gamma^11 G_0 da,   T_1(k) = int gamma^9 (1 + 12 A^2) G_0 da,
    T_2(k)   = int gamma^13 D_a G_0 da = -int gamma^13 [a^2/24 + a^4/(3456 k^2)] G_0 da,   T_b(k) = int |A| gamma^10 G_0 da,

are enclosed rigorously for `k in {1/2, 1, 2}`, and from them, with `p_b(0)/z_0 = phi(b/sqrt2)/(sqrt2 . 36 k^2 m_(2,b))`,
`m_(2,b) = (b^2 + 2) Phi(b/sqrt2) + b sqrt2 phi(b/sqrt2)`, `K_0 = 108 k^7 p_b(0)/z_0`, and the exact shape integrals
`I = 246528/35`, `U_2 = 240192/35`, `B = -428544/7`, `U_abs = 5898627/880`, `J = 1083417/280`,
`D = 27066286003/223205220 - (79298560/4782969) log 2`, `kappa = (2/13)(11/13)^(11/2)`, the constants of the table:

    J_cusp = J_hat/sqrt(192 pi^3),   C_0 = (216/11) k^7 [p_b(0)/z_0] J_cusp,   C_* = C_0 I            ([R] (R12)-(R13) at d = 2),
    G_max = C_0 (I - D),  G_2 = C_0 J,  B_2 = C_0 D,  singleton = C_0 (I - D - J)                       ([E] E6, E20, E21),
    C_2 = K_0 [U_2 T_1 + (2B/13) T_2] / sqrt(192 pi^3),   c = C_2/C_*,   kappa c,                      ([Q] (13), (16)),
    B_sign = (K_0/C_*) U_abs T_b / sqrt(192 pi^3)                                                       ([Q] (19)),

for `b in {0, 1}`. Every printed interval `[lo, hi]` in `RESULTS.json` is a rigorous enclosure of the exact real number
defined by the displayed formulas; no value is fitted, sampled, extrapolated or rounded outward by hand.

Also certified, as a by-product: `pi`, `log 2`, `erf(1/2)` and `D` to more than 40 digits (`D = 109.76995034568798474609191114...`).

## 2. Method (every step is an enclosure)

- **Arithmetic.** Intervals of `decimal` numbers at 48 digits with directed rounding (floor context for lower ends,
  ceiling context for upper ends). `exp` and `sqrt` are correctly rounded by the `decimal` module and are widened by two
  units in the last place on each side. Rationals enter through outward-rounded division.
- **Constants.** `pi` from Machin's formula with the alternating-series bracket (both arctangent series stopped at
  consecutive partial sums); `log 2 = sum 1/(n 2^n)` with the geometric tail; `erf(1/2)` from its Maclaurin series with
  the alternating tail; `sqrt2`, `sqrt3` by interval `sqrt`.
- **Cells.** `[0, T]` with `T = 16` is cut into `160` cells of width `1/10`. On a cell of centre `c` and half-width `r`
  the integrand is expanded as a truncated Taylor series in `t = a - c` to order `K = 12` by Taylor-model arithmetic
  (sum, product, scalar, integer power, `exp`, `sqrt` on truncated series with interval coefficients). The expansion at
  the point `c` supplies the coefficients `p_0, ..., p_(K-1)`; the same recurrences evaluated with the whole cell in
  place of `c` give an interval `[q_K]` that contains `f^(K)(xi)/K!` for every `xi` in the cell (inclusion monotonicity of
  interval arithmetic applied to the exact coefficient recurrences). By Taylor's theorem with Lagrange remainder and
  `K` even, `int_(-r)^(r) f(c + t) dt` lies in `sum_(j even < K) p_j 2 r^(j+1)/(j+1) + [q_K] 2 r^(K+1)/(K+1)`; odd terms
  vanish by symmetry of the cell. The largest cell remainder width is printed (`max_cell_remainder_width`, at most
  `8e-18` at `k = 1/2`, `3e-21` at `k = 1`, `7e-23` at `k = 2`).
- **Tail.** For `a >= T` every integrand is bounded by `(1 + s a^2)^7 (1 + a^2)^2 e^(-a^2/4)` with `s = 1/(144 k^2)`
  (`gamma^15 a^2/24`, `gamma^9 (1 + 12 A^2)`, `gamma^11`, `A gamma^10` are all below it for `a >= 1`, `k >= 1/2`), and
  `int_T^inf a^(2j) e^(-a^2/4) da <= (2/T) 4^j j! e^(-T^2/4) sum_(i <= j) (T^2/4)^i / i!`. The bound is `3.5e-18`,
  `1.9e-21`, `1.9e-23` at `k = 1/2, 1, 2` and is added (for `T_2`, whose integrand is negative, subtracted) before doubling.
- **Rules (all nine must hold; `passed` is `false` and the exit code `1` otherwise).**
  `FLOAT_INSIDE` an independent 96-point Gauss-Legendre value on `[0, 14]` lies within `1e-11` relative of every raw
  enclosure; `NESTING` a coarser enclosure (a quarter of the cells, order `K - 4`) contains the fine one;
  `TRUNCATION_NESTING` the enclosure obtained by truncating at `T/2` (its own tail bound added) intersects the one at
  `T`; `WIDTHS` every raw width is below `1e-11` relative; `PINNED` the printed leading digits of `J_hat(k)`,
  `C_*(k, 0)`, `D`, `log 2`, `pi` begin both ends of the enclosures; `MONOTONE_IN_K` `J_hat(1/2) > J_hat(1) > J_hat(2)`
  as disjoint intervals; `CONSTANTS_RIGOROUS` `pi` is bracketed below `1e-40` and the pins hold; `TB_EXACT` and
  `T2_IDENTITY` the two exact identities of section 3 hold as interval statements.
- **Mutants (each must exit `1`, in both interpreter modes).** `gamma-power` (`gamma^10` in place of `gamma^11`),
  `cusp-shift` (drops the `a^6` term of `G_0`), `prefactor` (`p_b(0)/z_0` scaled by `385/384`), `pi-truncated`,
  `log2-truncated`, `tail-dropped` (no tail bound; caught only by `TRUNCATION_NESTING`), `tb-power` (`gamma^8` in the `T_b`
  integrand on both evaluation paths; caught only by `TB_EXACT`), `t2-weight` (the `a^4` weight of `D_a G_0` scaled by
  `1001/1000` on both paths; caught only by `T2_IDENTITY`).

Runtime about `30 s` per run (standard library only, `python -B -S certify_tail_constants.py`); the workflow runs the
script in both interpreter modes, compares the output byte for byte with `RESULTS.json`, and runs the eight mutants
under each mode.

## 3. Three exact identities (elementary; not used in `NOTE.md` at `48407d4`, which evaluates `T_1`, `T_2`, `T_b` separately)

**(a) The cusp density is Gaussian in `gamma^6`.** Since `gamma^6 - 1 = 3A^2 + 3A^4 + A^6` and `A^2 = a^2/(144 k^2)`,

    G_0(a) = exp(-12 k^2 (gamma(a)^6 - 1)),        G_0'(a) = -(a/2) gamma(a)^4 G_0(a).

**(b) `T_b` is rational.** With `w = gamma^2`, `a da = 72 k^2 dw`, and then `v = w^3`:

    T_b(k) = 2 int_0^inf (a/(12k)) w^5 e^(-12 k^2 (w^3 - 1)) da = 12k int_1^inf w^5 e^(-12 k^2 (w^3 - 1)) dw
           = 4k int_1^inf v e^(-12 k^2 (v - 1)) dv = 4k [1/(12 k^2) + 1/(144 k^4)] = (12 k^2 + 1)/(36 k^3),

so `T_b(1/2) = 8/9`, `T_b(1) = 13/36`, `T_b(2) = 49/288`; the enclosures contain these rationals (`TB_EXACT`). Hence

    B_sign(k) = (11 U_abs/(2I)) . T_b(k)/J_hat(k) = (4587821/876544) . (12 k^2 + 1) / (36 k^3 J_hat(k)),

with `11 U_abs/(2I) = 4587821/876544` the [Q]-corollary constant already displayed in Math-#178.

**(c) `T_2 = -T_1/12`.** `a^2/24 + a^4/(3456 k^2) = (a^2/24) gamma^2`, so `T_2 = -(1/24) int a^2 gamma^15 G_0 da`.
By (a), `a^2 gamma^15 G_0 = -2 a gamma^11 G_0'`, and integrating by parts (boundary terms vanish),

    int a^2 gamma^15 G_0 da = 2 int (a gamma^11)' G_0 da = 2 int (12 gamma^11 - 11 gamma^9) G_0 da,

because `(a gamma^11)' = gamma^11 + 11 A^2 gamma^9 = 12 gamma^11 - 11 gamma^9`. The same bracket is `T_1`:
`gamma^9 (1 + 12 A^2) = 12 gamma^11 - 11 gamma^9`. Therefore `T_2 = -T_1/12` (`T2_IDENTITY`: the enclosures of `T_2` and
of `-T_1/12` intersect at every `k`, at widths of `1e-16` to `1e-21`), and

    C_2 = K_0 T_1 (U_2 - B/78) / sqrt(192 pi^3),        c(k) = (66451/11128) . T_1(k)/J_hat(k),

with `11 (U_2 - B/78)/(2I) = 66451/11128 = 5.97151...`. `RESULTS.json` prints both evaluations (`c_reduced`,
`B_sign_reduced`) beside the assembled ones; they agree to the last digit.

**Consequence.** Writing `I_p(k) = int gamma^p G_0 da`, the whole table depends on two transcendental numbers per `k`,
`J_hat = I_11` and `T_1 = 12 I_11 - 11 I_9`; the family obeys `(1 + p) I_p - p I_(p-2) = 72 k^2 (I_(p+6) - I_(p+4))`
(from `int (a gamma^p G_0)' da = 0`), which does not relate `I_11` to `I_9` without lower members. Asymptotic remark
(not certified, not used): expanding `G_0` and `gamma^11` in `s = 1/(144 k^2)` gives `J_hat(k) = 2 sqrt(pi) (1 + 1/(18 k^2) + O(k^-4))`;
at `k = 2` this reads `3.5941` against the certified `3.59442`, at `k = 1` `3.7418` against `3.74614`.

## 4. Certified values

Raw integrals (`RESULTS.json` → `raw_integrals`; the bracket shows the digits at which the two ends differ; `w` is the width):

| `k` | `J_hat` | `T_1` | `T_2` | `T_b` |
|---|---|---|---|---|
| `1/2` | `4.396080052560476[29…33]` (w `4.3e-17`) | `7.2017156701259[6993…7017]` (w `2.3e-16`) | `-0.600142972510497[601…413]` (w `1.9e-16`) | `0.888888888888888[876…908]` (w `3.2e-17`) = `8/9` |
| `1` | `3.74614172836573455` (w `4.5e-20`) | `4.33121953848605581` (w `1.5e-19`) | `-0.360934961540504651` (w `1.4e-19`) | `0.361111111111111111` (w `2.4e-20`) = `13/36` |
| `2` | `3.59441780573178758` (w `1.5e-21`) | `3.73260661394902763` (w `2.9e-21`) | `-0.311050551162418969` (w `3.9e-21`) | `0.170138888888888889` (w `4.7e-22`) = `49/288` |

Normalised cusp integral and the `b`-free constants (`RESULTS.json` → `constants`, identical for `b = 0` and `b = 1`):

| `k` | `J_cusp = J_hat/sqrt(192 pi^3)` | `c = C_2/C_*` | `kappa c` | `B_sign` |
|---|---|---|---|---|
| `1/2` | `0.05697576550737183` | `9.782610960502025` | `0.600499647330249[7…8]` | `1.058314213529843` |
| `1` | `0.04855218515605283` | `6.904152846784694` | `0.4238072398409664` | `0.5045327835799602` |
| `2` | `0.04658575448725384` | `6.201090480499020` | `0.3806501824142391` | `0.2477466432952960` |

Tail constants (`F(t) ~ C_* t^(-11)` is the `r^(-3)`-scaled expected number of near points at scaled radius `> t`; the split
columns are [E]'s whole-cluster decomposition):

| `k` | `b` | `C_*` | `G_max` | `G_2` | `B_2` | singleton |
|---|---|---|---|---|---|---|
| `1/2` | `0` | `1.929709931071402` | `1.899636893866561` | `1.060062419071862` | `0.03007303720484126` | `0.8395744747946980` |
| `1/2` | `1` | `0.5524932519127913` | `0.5438830717750065` | `0.3035053733792919` | `0.00861018013778482[5…6]` | `0.2403776983957146` |
| `1` | `0` | `52.62118476458856` | `51.80112428725574` | `28.90680071538336` | `0.8200604773328205` | `22.89432357187237` |
| `1` | `1` | `15.06591691423265` | `14.83112624824110` | `8.276276176269632` | `0.2347906659915518` | `6.554850071971470` |
| `2` | `0` | `1615.678527435135` | `1590.499426843761` | `887.5531294407690` | `25.17910059137386` | `702.9462974029917` |
| `2` | `1` | `462.5832459558805` | `455.3742437416235` | `254.1144173196261` | `7.209002214256986` | `201.2598264219975` |

All sixteen digits shown are common to both ends of the enclosure unless a bracket says otherwise; the full intervals
(up to 48 digits) are in `RESULTS.json`. The universal ratios `(I - D)/I`, `J/I`, `D/I` and the bounds of [Q]'s
corollary (`c > 4587/856`, `0 < B_sign < 4587821/876544`) hold inside every enclosure.

## 5. Comparison with Math-#178

Every number in Math-#178 `RESULTS.json` (blob `0b5ce76f`, `per_k` cusp values and the complete `table`, 78 values, plus
`D_inner` and `kappa`) lies within `9e-16` relative of the corresponding certified enclosure, that is, at the rounding
level of its own floating-point arithmetic; 96-point Gauss-Legendre on `[0, 14]` was, for these integrands, accurate to
the last printed digit. The certification shares no code with `tail_constants.py` (different method, different
quadrature, different arithmetic) and does not consume its numbers except in this comparison. The near-mass identity
(N) of that note (a four-dimensional integral) is **not** certified here.

## 6. Exposure, disposition, non-claims

- **Exposure.** This session authored none of [R], [E], [Q], Math-#168 or Math-#178; it posted nonauthor reads of [E]
  Slices A, B, C (Math-#169) and of Math-#181/#185 slices. Same GitHub account and same provider as Math-#178's author:
  zero organizational-independence credit; a Claude read of a Claude packet counts for nothing towards acceptance.
- **What this record is.** A certified evaluation of formulas taken from merged sources ([R] (R12)-(R13); [E] E6, E20,
  E21; [Q] (12), (13), (16), (19), (21)-(22); all pinned on `main` by blob and checked by the workflow) through the planar
  reduction of Math-#178 §1, which is consumed at that note's stated scope and is not reviewed here. The three
  identities of section 3 are elementary calculus on the displayed integrands and change no formula of any source.
- **What it is not.** Not a proof of any theorem; not a review of Math-#178 (its Slice A/B/C read requests stand with
  the non-Claude lanes); no register, catalog, STATUS, PROOF_INDEX or GRAPH change. Catalog **C8** (numerical constants:
  finite `C`, `r_*`, `z_*`, `c_(B,K)`, `c_(d,L)` on a declared band) stays **OPEN**: the constants certified here are the
  limiting microscopic tail coefficients of the `r -> 0`-first law, a different object; this record is information for the
  integrators, not a C8 candidate. Planar (`d = 2`), parent kernel, aligned frame; no rate in `r`, no finite-`r` statement,
  nothing on the remote singleton population; `k in {1/2, 1, 2}` and `b in {0, 1}` only (any other `k`, `b` is a one-line
  change of the constants `KS`, `BS` and a rerun).

## 7. Files and reproduction

`certify_tail_constants.py` (standard library; `--mutant NAME`; `--T`, `--cells`, `--K` for experiments, the pinned run is
the default), `RESULTS.json` (the script's stdout, byte-identical in `-B -S` and `-B -O -S`), `SOURCE_FILES.json`
(manifest, the three `main` pins with blobs, the Math-#178 companion at head `48407d4`), workflow
`.github/workflows/c6-tail-constant-certified.yml` (manifest and pin verification, both modes against `RESULTS.json`,
the eight mutants under each mode in parallel, clean tree).

    python -B -S reviews/c6_tail_constant_certified_20260930/certify_tail_constants.py | diff - reviews/c6_tail_constant_certified_20260930/RESULTS.json
    python -B -S reviews/c6_tail_constant_certified_20260930/certify_tail_constants.py --mutant tail-dropped; echo $?   # 1
