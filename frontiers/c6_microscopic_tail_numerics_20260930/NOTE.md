# Numerical values of the planar microscopic radius-tail constants for the parent kernel

**Object:** `CL-C6-MICRO-TAIL-NUMERICS-20260930-v1`. **Author lane:** Anthropic / Claude. **Kind:** numerical note.
**Scientific effect:** NONE. **Certified:** no (deterministic Gauss quadrature with reported convergence; not an
enclosure). Third of the planar numerics notes after Math-#168 (near coefficients `alpha_1, alpha_2`) and
Math-#174 (remote coefficient `k integral_X Lambda`).

## 1. What is evaluated

[R] (Math-#166, merged) proves for the already-formed limiting microscopic measure `M` (the `r -> 0` limit taken
first) the point-intensity radius tail

    F(t) = integral sum_i 1{R_i > t} dM ~ C_* t^(-11),
    C_* = (216/11) k^7 (c_m/z_0) I J_cusp,    I = 246528/35,                                        (R13)

with `J_cusp = integral H(h) gamma(a)^11 h_0(A_0, Rot_O tau_cusp) da dxi dh dO` (R12) and
`gamma(a) = sqrt(1 + (a/(12k))^2)`, and lists "no numerical value of its Gaussian integral" as a non-claim. The
companions Math-#169 ([E]) and Math-#176 ([Q]), both merged but still conditional (§5), express further constants of the same measure through
the same cusp integrals: the whole-cluster split of the tail (E6) and the second-order coefficient `C_2`, the
total-variation coefficient `kappa |C_2/C_0|` of the radial ratio and the signed constant `B_sign` ((13), (16),
(19)). This note evaluates all of them in the plane for the parent kernel `K(z) = exp(-|z|^2/2)` ([LP] §2).

**Planar reduction.** In `d = 2` the spectral measure (17) of [SC] has `m = d - 1 = 1`, `c_1 = 1`, no hard
curvatures, and the Haar variable `O in O(1) = {±1}` averages trivially, because `p_odd` is invariant under
`(a, beta, c) -> (-a, beta, -c)`; `H(h) = 1`. Its density `h_0(A_0, tau)` at `A_0 = 0` is the raw contact density of
`(f_zz; f_xxz, f_xzz, f_zzz)` at `(0; a, beta, c)` given the contact pins `(f, f_x, f_z, f_xx, f_xz, f_xxx) =
(b, 0, 0, 0, 0, 12k)`, which by the exact regression of Math-#168 factors as `p_b(0) . p_odd(a, beta, c)` with
`p_b(0) = phi(b/sqrt2)/sqrt2` (the density of `f_zz | (f, f_xx, f_xz) = (b, 0, 0) ~ N(-b, 2)` at `0`) and
`p_odd = N(0, diag(2, 2, 6))`, for every `k, b`. These are the continuum jet covariances. For the periodized parent
kernel at side `L` they hold up to the lattice-moment deviation recorded by Math-#168 (`lattice_vs_continuum`: at
most `1.4e-13` at `L = 12, 24`; `L = 6` is not covered), so the values below are for the continuum covariance and
apply at `L >= 12`. Hence

    c_1 h_0(0, tau)/z_0 = [p_b(0)/z_0] p_odd(a, beta, c),   p_b(0)/z_0 = phi(b/sqrt2) / (sqrt2 . 36 k^2 m_(2,b)),

the prefactor of Math-#168, and `J_cusp(k) = integral gamma(a)^11 p_odd(a, a^2/(12k), a^3/(144k^2)) da` is a
one-dimensional Gaussian integral, `b`-free; all `b`-dependence of the constants sits in the prefactor.

**Near-mass identity (control).** The same root-resolved integral (R11) without the radius indicator is the near
point mass `integral n dM = a_1 + 2 a_2`, `a_j = integral 1{n = j} dM` ([SC] (18), (20); `n <= 2` by the classifier of
[SC] §6), which at `d = 2` are Math-#168's `alpha_j` (the near part of `Lambda_1` in [CL] (1.6), Math-#159, not
pinned here):

    alpha_1 + 2 alpha_2 = 108 k^7 [p_b(0)/z_0] integral_S Q(u, v) integral_(Z != 0) |Z|^(-12)
                          integral p_odd(a, beta(u, v, Z, a), c(u, v, Z, a)) da dZ du dv,                 (N)

with `beta = a^2/(12k) + k b_0(u)/Z^2`, `c = a^3/(144k^2) + a b_0(u)/(4Z^2) + 2k(v - b_0(u) u)/Z^3`. This
four-dimensional integral is evaluated independently here and compared with the merged Math-#168 values; agreement
is a consistency check between the [SC]/[R] parametrization (jet Jacobian `2`, root Jacobian `6`, weight `9`, multiplicity by the map) and the
[CL]/[CUB] parametrization of Math-#168, which integrates the classifier over the jets directly.

## 2. Exact structure

- Shape integrals over `S = {-3/2 < u < 1/2, |b_0|/2 < v < 3 - 6u}` with `Q = (4v^2 - b_0^2)(b_0 - 4uv)`, in rational
  arithmetic: `I = 246528/35`, `U_2 = integral u^2 Q = 240192/35`, `B = integral b_0 Q = -428544/7 = 3I - 12 U_2`,
  `U_abs = integral |u| Q = 5898627/880` ([Q] (12)); `E eta = 5771/7062` under `Q/I` ([R] H3); the outer doublet
  integral `J = 1083417/280` ([E] (E5), derived from the primitive (E20)); `11 U_2/(2I) = 4587/856`, `11 U_abs/(2I) = 4587821/876544` (author-side
  corollary in Math-#176 comment 5903080058, not part of the pinned [Q] bytes). The inner doublet integral `D = 27066286003/223205220 - (79298560/4782969) log 2 = 109.7699503...`
  ([E] E21) is quoted, not recomputed exactly (it was confirmed to `1e-13` by quadrature in the Slice C read).
- `kappa = (2/13)(11/13)^(11/2) = q_0^(-11) - q_0^(-13)` at `q_0 = sqrt(13/11)` ([Q] (16)).
- With the aligned planar cusp density ([Q] (21)–(22), `v_a = v_beta = 2`, `v_c = 6` for the continuum kernel):
  `D_a G_0 = -[a^2/24 + a^4/(3456 k^2)] G_0 <= 0`, so `C_2 > 0`.
- Assembly (`K_0 = 108 k^7 p_b(0)/z_0`; `C_0` below is [E]'s per-shape amplitude, `C_* = C_0 I` is [Q]'s `C_0`):

      C_0 = (216/11) k^7 [p_b(0)/z_0] J_cusp,           C_* = C_0 I,
      G_max ~ C_0 (I - D),  G_2 ~ C_0 J,  B_2 ~ C_0 D,  singleton ~ C_0 (I - D - J),
      C_2 = K_0 [ U_2 T_1 + (2B/13) T_2 ],   T_1 = integral gamma^9 (1 + 12A^2) G_0 da,  T_2 = integral gamma^13 D_a G_0 da,
      c = C_2/C_*,   d_TV(R/t, Pareto_11) = kappa c t^(-2) + O(t^(-4)),
      B_sign = (K_0/C_*) U_abs integral |A| gamma^10 G_0 da,   A = a/(12k).

  Every integrand in `a` is even, so the integrals are taken on `[0, 14]` and doubled (this also removes the kink of
  `|A|` at `0`); 96-point Gauss–Legendre, checked against 48 points.

## 3. Values

**Cusp integrals** (`b`-free):

| `k` | `J_cusp` | `T_1` | `T_2` | `integral |A| gamma^10 G_0` | max rel. dev. 48 vs 96 points |
|---|---|---|---|---|---|
| `0.5` | 0.0569758 | 0.0933384 | -0.0077782 | 0.0115205 | `1e-14` |
| `1.0` | 0.0485522 | 0.0561351 | -0.00467793 | 0.00468021 | `1e-15` |
| `2.0` | 0.0465858 | 0.0483768 | -0.0040314 | 0.0022051 | `2e-15` |

**Tail constants** (`F(t) ~ C_* t^(-11)` is the `r^(-3)`-scaled expected number of near points at scaled radius
`R > t`; the split rows are values of [E] (E6); `c`, `kappa c`, `B_sign` of [Q] (13), (16), (19) (conditional on [E]/[Q]; see §5)):

| `k` | `b` | `C_*` | `G_max` | `G_2` | `B_2` | singleton | `c = C_2/C_*` | `kappa c` | `B_sign` |
|---|---|---|---|---|---|---|---|---|---|
| `0.5` | `0.0` | 1.9297 | 1.8996 | 1.0601 | 0.030073 | 0.83957 | 9.7826 | 0.6 | 1.058 |
| `1.0` | `0.0` | 52.621 | 51.801 | 28.907 | 0.82006 | 22.894 | 6.9042 | 0.424 | 0.5045 |
| `2.0` | `0.0` | 1615.7 | 1590.5 | 887.55 | 25.179 | 702.95 | 6.2011 | 0.381 | 0.2477 |
| `0.5` | `1.0` | 0.55249 | 0.54388 | 0.30351 | 0.0086102 | 0.24038 | 9.7826 | 0.6 | 1.058 |
| `1.0` | `1.0` | 15.066 | 14.831 | 8.2763 | 0.23479 | 6.5549 | 6.9042 | 0.424 | 0.5045 |
| `2.0` | `1.0` | 462.58 | 455.37 | 254.11 | 7.209 | 201.26 | 6.2011 | 0.381 | 0.2477 |

`c` and `B_sign` are `b`-free (the prefactor cancels); the ratios `G_max/C_* = (I-D)/I = 0.98442`, `G_2/C_* = J/I
= 0.54934`, `B_2/C_* = D/I = 0.015584` are universal. In `RESULTS.json`, `C2_over_C0` uses [Q]'s `C_0 = C_*`;
`C0_per_shape` is [E]'s `C_0`. The numbers satisfy the bounds of the Math-#176 author-side corollary (comment 5903080058; not in the
pinned [Q] blob): `c > 4587/856 = 5.3586`
and `0 < B_sign < 4587821/876544 = 5.2340`. Reading: at `k = 1`, `b = 0` the near point mass is `1.380` and `C_* = 52.6`, so the asymptotic law puts `C_* 2^(-11) = 0.026` (about `1.9%` of it) beyond twice the pin distance and `3e-4` beyond
three; the radial ratio's total-variation distance from Pareto(11) at threshold `t` is `0.42/t^2` to leading order
(`4.7%` at `t = 3`), and the signed-mark distance decays only like `0.50/t`.

**Near-mass identity** (`alpha_1 + 2 alpha_2` from (N) at three shape-grid levels, against Math-#168):

| `k` | (N) at 32/64/96 shape points (`ns = 160`) | (N), `b = 0` | Math-#168 GH60 | Math-#168 MC (s.e. of `alpha_1`) | rel. dev. vs GH60 / MC |
|---|---|---|---|---|---|
| `0.5` | 37.9952 / 37.871 / 37.8825 | 1.1874 | 1.1877 | 1.1844 (0.0027) | -2.67e-04 / +2.48e-03 |
| `1.0` | 175.923 / 176.071 / 176.082 | 1.3798 | 1.3801 | 1.3786 (0.0022) | -2.22e-04 / +8.33e-04 |
| `2.0` | 1119.62 / 1120.53 / 1120.7 | 2.1954 | 2.196 | 2.1948 (0.0033) | -2.34e-04 / +2.87e-04 |

The shape-grid refinement at fixed `ns = 160` moves the integral by at most `3e-04` relative between the 64- and
96-point levels (the sequence is monotone with observed order about 2 at `k = 2` and about 3.5 at `k = 1`, and is not
monotone at `k = 1/2`, so no order is claimed; the integrand has an integrable singularity at the corner
`(u, v) = (-1/2, 0)` of `S`, where the `|Z|`-scale of the Gaussian cutoff diverges), and the log-`Z` order is converged: at `32 x 32` shape points,
`ns = 64, 96, 160, 256` give `175.6152`, `175.9278`, `175.9235`, `175.9235` at `k = 1` (an under-resolved `ns = 64`, the order of the
first version of this note, biased the identity low by `1.8e-3`, exactly the deviation then reported; the `a`-order
`32` and `48` agree to all digits). At the finest level the identity lies within `1.1`, `0.5` and `0.2` Monte Carlo
standard errors of `alpha_1` of the Math-#168 values at `k = 1/2, 1, 2`, and within `2.7e-04`, `2.2e-04`, `2.3e-04` relative of the GH60
values. This is the check that the two parametrizations agree; it is not a certification of either.
The deviations from GH60 are all negative and of the size of the remaining shape-grid movement of (N), which still
increases between the two finest levels; at `k = 2` the GH60 reference is itself not settled at this level (Math-#168
§4: `J_2(2)` GH60 lies 3.2 MC s.e. below MC and the third digit of `alpha_2(2)` is not established, about `4e-4`
relative in `alpha_1 + 2 alpha_2`).

## 4. Precision (empirical, not bounds)

- The one-dimensional cusp integrals agree between 48 and 96 Gauss–Legendre points to the relative deviations in
  the table (all at most `1.3e-14`); the constants inherit that precision and the exact prefactor.
- Three exact identities stated in Math-#190 (elementary: `G_0 = exp(-12 k^2 (gamma^6 - 1)) / sqrt(192 pi^3)` on the
  cusp, and `(a gamma^11)' = 12 gamma^11 - 11 gamma^9`) hold in this quadrature at machine precision and are
  `--check` rules since v3: `T_2 = -T_1/12` (`< 3e-18` absolute at every `k`), `T_b sqrt(192 pi^3) = (12k^2 + 1)/(36k^3)`
  (`8/9`, `13/36`, `49/288`; `< 6e-16`), and the rational factor `(11/2)(U_2 - B/78)/I = 66451/11128` of
  `c = C_2/C_* = (66451/11128) T_1/J_cusp` (exact). Since `T_1/J_cusp = 12 - 11 I_9/I_11 in (1, 12)`, Math-#190
  reports (information only, not consumed here) the bounds `5.9715 < c(k) < 71.658`, which would sharpen the corollary
  `c > 4587/856`; the floating-point values here (`9.78`, `6.90`, `6.20`) lie inside.
- Math-#190 (reviews/c6_tail_constant_certified_20260930, other Claude session; merged 2026-10-01 at `77b854c` as a review
  record filed as certified-arithmetic information, not a promotion; not consumed here)
  reports certified interval enclosures of every constant of this table and finds each value of `RESULTS.json`
  (blob `0b5ce76f`) within `9e-16` relative of its enclosure. That record is information for the reader; it is not a
  certification of this note, which stays floating point.
- The near-mass integral moves by at most `3e-04` relative between the 64- and 96-point shape levels at `ns = 160`,
  and by `4e-09` between `ns = 160` and `256`; its remaining error is of the former order, below the Math-#168 Monte
  Carlo standard error.

## 5. What the numbers are not

Not a proof and not an enclosure. `C_*` is a value of the reviewed formula (R13) of the merged [R]; the split and the
second-order/signed constants are values of formulas of [E] (Math-#169) and [Q] (Math-#176). Both are merged on main
after scoped nonauthor review, but their pinned bytes keep the disposition 'author-side conditional proof candidate'
and their source hypotheses remain. These values are therefore conditional on [E] and [Q] and their sources,
evaluated at their stated scope (planar, `r -> 0` first), with continuum spectral moments and no finite-`L`
periodization correction. Planar only (`d = 2`), parent
kernel only, aligned frame; no rate for `r -> 0`, no finite-`r` statement, no statement about the remote singleton
population. No register, catalog or STATUS change. Same GitHub account as every lane; zero
organizational-independence credit. The author will not merge.

## 6. Provenance

`tail_constants.py` (standard library; `--check` replays the exact controls, the cusp integrals and the complete
constants table for each `k` and both `b`, the low-level near-mass integral for each `k` with its log-`Z` study
entry, the assembly of the identity from the stored numbers, the identity tolerance against `RESULTS.json`, and the
three exact identities of §4; mutants `shape-integral`,
`gamma-power`, `cusp-shift` exit 1), `RESULTS.json` (full run, about fifteen minutes), `SOURCE_MAP.json`
(pins [R], [SC], [NUM], [CUB], [LP], [E], [Q] on `main` `3e0a91b`, all workflow-checked; [E] and [Q] were unmerged
companions in v1/v2 and were promoted to pins in v3 with their blobs unchanged),
`SOURCE_FILES.json`, workflow `c6-microscopic-tail-numerics.yml`.

Revision v3.1 (Slice C review 5974193134 on Math-#178, findings F1–F8, wording only): [E]/[Q] values are stated as
conditional although both are merged; the corollary bounds are attributed to Math-#176 comment 5903080058, not to the
pinned [Q]; Math-#190 is recorded as merged at `77b854c` and its bounds as information only; precision `1.3e-14`;
near point mass `1.380` (`C_* 2^(-11)` about `1.9%` of it); the two `C_0` conventions in `RESULTS.json` named;
continuum spectral moments stated. With the Slice A review 5974218952 (F1–F3): the planar regression is stated as the
continuum covariance, valid at `L >= 12` by the Math-#168 lattice control; the trivial `O(1)` average is named; `J`
is cited at [E] (E5). With the Slice B review 5974449197 (F1–F4): no convergence order is claimed for the shape grid;
the sign and size of the GH60 deviations are explained; the `±` is the MC standard error of `alpha_1`; the identity is
derived from the pinned [SC], with [CL] (1.6) cited as context only. `RESULTS.json` and `tail_constants.py` unchanged.
