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
unmerged companions Math-#169 ([E]) and Math-#176 ([Q]) express further constants of the same measure through the
same cusp integrals: the whole-cluster split of the tail (E6) and the second-order coefficient `C_2`, the
total-variation coefficient `kappa |C_2/C_0|` of the radial ratio and the signed constant `B_sign` ((13), (16),
(19)). This note evaluates all of them in the plane for the parent kernel `K(z) = exp(-|z|^2/2)` ([LP] §2).

**Planar reduction.** In `d = 2` the spectral measure (17) of [SC] has `m = d - 1 = 1`, `c_1 = 1`, no hard
curvatures and no Haar variable; `H(h) = 1`. Its density `h_0(A_0, tau)` at `A_0 = 0` is the raw contact density of
`(f_zz; f_xxz, f_xzz, f_zzz)` at `(0; a, beta, c)` given the contact pins `(f, f_x, f_z, f_xx, f_xz, f_xxx) =
(b, 0, 0, 0, 0, 12k)`, which by the exact regression of Math-#168 factors as `p_b(0) . p_odd(a, beta, c)` with
`p_b(0) = phi(b/sqrt2)/sqrt2` (the density of `f_zz | (f, f_xx, f_xz) = (b, 0, 0) ~ N(-b, 2)` at `0`) and
`p_odd = N(0, diag(2, 2, 6))`, for every `k, b`. Hence

    c_1 h_0(0, tau)/z_0 = [p_b(0)/z_0] p_odd(a, beta, c),   p_b(0)/z_0 = phi(b/sqrt2) / (sqrt2 . 36 k^2 m_(2,b)),

the prefactor of Math-#168, and `J_cusp(k) = integral gamma(a)^11 p_odd(a, a^2/(12k), a^3/(144k^2)) da` is a
one-dimensional Gaussian integral, `b`-free; all `b`-dependence of the constants sits in the prefactor.

**Near-mass identity (control).** The same root-resolved integral (R11) without the radius indicator is the near
point mass `integral n dM = alpha_1 + 2 alpha_2` of Math-#168 ((1.6) of [CL], `Lambda_1 = nu_near(1) + 2 nu_near(2)`):

    alpha_1 + 2 alpha_2 = 108 k^7 [p_b(0)/z_0] integral_S Q(u, v) integral_(Z != 0) |Z|^(-12)
                          integral p_odd(a, beta(u, v, Z, a), c(u, v, Z, a)) da dZ du dv,                 (N)

with `beta = a^2/(12k) + k b_0(u)/Z^2`, `c = a^3/(144k^2) + a b_0(u)/(4Z^2) + 2k(v - b_0(u) u)/Z^3`. This
four-dimensional integral is evaluated independently here and compared with the merged Math-#168 values; agreement
ties the [SC]/[R] parametrization (jet Jacobian `2`, root Jacobian `6`, weight `9`, multiplicity by the map) to the
[CL]/[CUB] parametrization of Math-#168, which integrates the classifier over the jets directly.

## 2. Exact structure

- Shape integrals over `S = {-3/2 < u < 1/2, |b_0|/2 < v < 3 - 6u}` with `Q = (4v^2 - b_0^2)(b_0 - 4uv)`, in rational
  arithmetic: `I = 246528/35`, `U_2 = integral u^2 Q = 240192/35`, `B = integral b_0 Q = -428544/7 = 3I - 12 U_2`,
  `U_abs = integral |u| Q = 5898627/880` ([Q] (12)); `E eta = 5771/7062` under `Q/I` ([R] H3); the outer doublet
  integral `J = 1083417/280` ([E] E20); `11 U_2/(2I) = 4587/856`, `11 U_abs/(2I) = 4587821/876544` ([Q]
  corollary). The inner doublet integral `D = 27066286003/223205220 - (79298560/4782969) log 2 = 109.7699503...`
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
{{cusp_rows}}

**Tail constants** (`F(t) ~ C_* t^(-11)` is the `r^(-3)`-scaled expected number of near points at scaled radius
`R > t`; the split rows are conditional on [E]; `c`, `kappa c`, `B_sign` on [Q]):

| `k` | `b` | `C_*` | `G_max` | `G_2` | `B_2` | singleton | `c = C_2/C_*` | `kappa c` | `B_sign` |
|---|---|---|---|---|---|---|---|---|---|
{{table_rows}}

`c` and `B_sign` are `b`-free (the prefactor cancels); the ratios `G_max/C_* = (I-D)/I = 0.98442`, `G_2/C_* = J/I
= 0.54934`, `B_2/C_* = D/I = 0.015584` are universal. The bounds of [Q]'s corollary hold: `c > 4587/856 = 5.3586`
and `0 < B_sign < 4587821/876544 = 5.2340`. Reading: at `k = 1`, `b = 0` the near point mass is `1.378` and `C_*
= 52.6`, so the asymptotic law puts `C_* 2^(-11) = 0.026` of it beyond twice the pin distance and `3e-4` beyond
three; the radial ratio's total-variation distance from Pareto(11) at threshold `t` is `0.42/t^2` to leading order
(`4.7%` at `t = 3`), and the signed-mark distance decays only like `0.51/t`.

**Near-mass identity** (`alpha_1 + 2 alpha_2` from (N) at three shape-grid levels, against Math-#168):

| `k` | (N) at 32/64/96 shape points | (N), `b = 0` | Math-#168 GH60 | Math-#168 MC (s.e. of `alpha_1`) | rel. dev. vs GH60 / MC |
|---|---|---|---|---|---|
{{nm_rows}}

The four-dimensional integral converges from below (observed order about two in the shape grid; the integrand has
an integrable boundary singularity where the `|Z|`-scale of the Gaussian cutoff diverges) and at the finest level
lies within one Monte Carlo standard error of the Math-#168 value at every `k`. This is the check that the two
parametrizations agree; it is not a certification of either.

## 4. Precision (empirical, not bounds)

- The one-dimensional cusp integrals agree between 48 and 96 Gauss–Legendre points to the relative deviations in
  the table (all below `{{cusp_dev_max}}`); the constants inherit that precision and the exact prefactor.
- The near-mass integral moves by `{{nm_move}}` relative between the 64- and 96-point shape levels; its remaining
  error is of that order, below the Math-#168 Monte Carlo standard error.

## 5. What the numbers are not

Not a proof and not an enclosure. `C_*` is a value of the reviewed formula (R13) of the merged [R]; the split and the
second-order/signed constants are values of formulas in the unmerged candidates [E] and [Q] (their Slices B, C, D and
A, B respectively carry nonauthor reads at this writing) and are conditional on them. Planar only (`d = 2`), parent
kernel only, aligned frame; no rate for `r -> 0`, no finite-`r` statement, no statement about the remote singleton
population. No register, catalog or STATUS change. Same GitHub account as every lane; zero
organizational-independence credit. The author will not merge.

## 6. Provenance

`tail_constants.py` (standard library; `--check` replays the exact controls, the cusp integrals and `C_*` for each
`k`, the low-level near-mass integral, and the identity tolerance against `RESULTS.json`; mutants `shape-integral`,
`gamma-power`, `cusp-shift` exit 1), `RESULTS.json` (full run, about {{minutes}} minutes), `SOURCE_MAP.json`
(pins [R], [SC], [NUM], [CUB], [LP] on `main` `02772ec`; companions [E], [Q] unmerged, not workflow-checked),
`SOURCE_FILES.json`, workflow `c6-microscopic-tail-numerics.yml`.
