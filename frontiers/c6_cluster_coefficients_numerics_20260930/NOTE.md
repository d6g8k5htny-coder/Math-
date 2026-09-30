# Numerical values of the planar near cluster coefficients `alpha_1`, `alpha_2`

**Object:** CL-C6-CLUSTER-COEFF-NUMERICS-20260930-v1.
**Author:** Anthropic Claude (Claude Code session `session_015wNj8LPTKXsaT68G3DgPPh`), 30 September 2026.
**Disposition:** numerical evaluation. **Not a proof, not a certified enclosure.** Floating-point quadrature and Monte
Carlo values with reported standard errors, for the explicit finite-dimensional Gaussian integrals that the cluster-law
candidates define. Every packet on the C6 cluster line lists "no numerical value of `nu(1)`, `nu(2)`" as a non-claim;
this note supplies values for the *near* coefficients only, and says exactly what they are conditional on.
**Scientific effect:** NONE. No `STATUS`, `PROOF_INDEX`, `GRAPH`, claim, catalog, prize or source body changes.
Same GitHub account as every lane; zero organizational-independence credit.

## 1. What is evaluated

Planar model of [LP] (`d = 2`), torus side `L`, variance-one periodized Gaussian field with spectral weights
`a_n = exp(-2 pi^2 |n|^2 / L^2) / sum_j exp(-2 pi^2 |j|^2 / L^2)` ([LP] §2), pins `f(M) = b`, `f(S) = b - k r^3`,
`grad f(M) = grad f(S) = 0`, original weight `W_r` and full normalizer `Z_r`. The near coefficients of the cluster law
are, in the notation of [CL] (1.3) and (3.11) at `d = 2` (equivalently Theorem F of [CUB]),

    alpha_j = (1/z_0) integral_(R^4) h_0(0, a, beta, c) w_0(s, a, beta) 1{ n(s, a, beta, c) = j } ds da dbeta dc,   j = 1, 2,

where `h_0` is the contact density of `(f_zz, f_xxz, f_xzz, f_zzz)(0)` given the contact pins
`U_0 = (f, f_x, f_xx, f_xxx, f_z, f_xz)(0) = (b, 0, 0, 12k, 0, 0)`, `z_0 = lim Z_r / r^2`, `w_0 = [-6k(s - beta/2) -
a^2/4]_+ [a^2/4 - 6k(s + beta/2)]_+` is the pin weight, and `n` is the number of extra critical points of the pinned cubic
`F_0` with height in `(-k, 0)`. In the cluster law, `nu(2) = alpha_2` and `nu(1) = alpha_1 + k integral_X Lambda`; the
remote part `k integral_X Lambda` ([RM]) is **not** evaluated here.

Everything below is conditional on these formulas, i.e. on [CL] Theorem N (author-side, Math-#159, unmerged) or on
[CUB] Theorem F (merged, Claude-accepted) for the near coefficients as *lower bounds* of the global intensities. The
numbers do not accept either source.

## 2. Exact structure of the contact regression (checked exactly, control `exact_structure`)

Because `a_n` depends only on `|n|` through a Gaussian, `K_L` is the periodization of `K(z) = exp(-|z|^2/2)`; the jet
covariances at one site are the continuum values up to `O(exp(-L^2/2))`, and the lattice sums at `L = 24` and `L = 12`
reproduce them to `1.4e-13` (control `lattice_vs_continuum`). With `Cov(d^alpha f, d^beta f) = (-1)^|beta| d^(alpha+beta) K(0)`
and `d^(2m) exp(-x^2/2)|_0 = (-1)^m (2m-1)!!`:

| jets | covariance |
|---|---|
| `Var f, Var f_x, Var f_z, Var f_xz` | `1` |
| `Var f_xx, Var f_zz, Var f_xxz, Var f_xzz` | `3` |
| `Var f_xxx, Var f_zzz` | `15` |
| `Cov(f, f_xx) = Cov(f, f_zz) = Cov(f_x, f_xzz) = Cov(f_z, f_xxz)` | `-1` |
| `Cov(f_xx, f_zz) = Cov(f_xxx, f_xzz) = Cov(f_xxz, f_zzz)` | `1`, `3`, `3` |
| `Cov(f_x, f_xxx) = Cov(f_z, f_zzz)` | `-3` |

Parity splits the ten jets into the even block `(f, f_xx, f_xz, f_zz)` and the odd block `(f_x, f_z, f_xxx, f_xxz, f_xzz,
f_zzz)` with zero cross-covariance ([CUB] Theorem B). Exact regression (rational arithmetic):

- Even block: `A = f_zz | (f, f_xx, f_xz) = (b, 0, 0)` is `N(-b, 2)`. Hence `p_b(0) = phi(b/sqrt2)/sqrt2` and
  `z_0 = 36 k^2 m_(2,b)`, `m_(2,b) = E[A^2 1{A < 0}] = (b^2 + 2) Phi(b/sqrt2) + sqrt2 b phi(b/sqrt2)`; in particular
  `z_0 = 36 k^2` exactly at `b = 0` and `m_(2,1) = 3 Phi(1/sqrt2) + sqrt2 phi(1/sqrt2) = 2.72014...`.
- Odd block: `(a, beta, c) = (f_xxz, f_xzz, f_zzz) | (f_x, f_z, f_xxx) = (0, 0, 12k)` is `N(0, diag(2, 2, 6))` for every
  `k` and `b`: the regression coefficient of every output on the `f_xxx = 12k` pin vanishes (for `f_xzz` it is
  `[-1, 3] . [[1, -3], [-3, 15]]^(-1) = [-1, 0]`), and the parity zeros kill the rest.

Therefore

    alpha_j(k, b) = [ phi(b/sqrt2) / ( sqrt2 . 36 k^2 m_(2,b) ) ] . J_j(k),      J_j(k) = E_( (a,beta,c) ~ N(0, diag(2,2,6)) ) [ I_j(a, beta, c; k) ],

and the ratio `alpha_2/(alpha_1 + alpha_2) = J_2/(J_1 + J_2)` is independent of `b` ([CUB] Theorem B), while its `k`
dependence is genuine (the jet law does not scale with `k`).

## 3. The `s`-integral, exactly

With `B = beta - a^2/(12k)`, `D = (c - a beta/(4k) + a^3/(72k^2))/2` and the sheared cubic
`G(u, Z) = C(u) + (s + Bu) Z^2/2 + (D/3) Z^3` ([CUB] (C2)–(C3), [CL] (3.12)), the pin weight on the typed domain
`s < -|B|/2` is `w_0 = 9k^2 (4s^2 - B^2)`, and the classifier ([CUB] Theorem C) reads, with

    g(s) = -2 s^3 + 3 B s^2 - B^3 - 12 k D^2 = 12k ( T_*(s) - D^2 ),      T_*(s) = -(s - B)^2 (B + 2s) / (12k),

`n = 2` iff `s > B` and `g(s) > 0`; `n = 1` iff `g(s) < 0`; `n = 0` iff `s <= B` and `g(s) > 0`. So

    I_j(a, beta, c; k) = integral_(s < -|B|/2) 9k^2 (4s^2 - B^2) 1{n = j} ds

is a sum over at most two intervals with endpoints among the real roots of the cubic `g` (found by bracketed
bisection to machine precision), of the exact antiderivative `12 k^2 s^3 - 9 k^2 B^2 s`. Closed forms used as
controls: the [LM] cubic `(a, beta, c) = (0, -2k, 0)` gives `(I_1, I_2) = (0, 48 k^5)` (`n = 2` exactly on `(B, B/2)`);
the family `(0, 0, c)` gives `(72 k^3 D^2, 0)` with `D = c/2`. The classifier is checked against a direct count of the
critical points of `G` (quadratic in `u`, heights in `(-k, 0)`) on 4000 random typed samples (control `classifier`), and
`I_j` against brute-force `s`-quadrature during development (agreement `1e-4`, the quadrature error). Lemma 3.6 of [CL]
(`-s <= 2|B| + (32 k D^2)^(1/3)` on `{n >= 1}`) is the reason the outer integrand is a polynomial times a Gaussian and
the outer integral converges.

## 4. Numerical values

Outer integration over `(a, beta, c) ~ N(0, diag(2, 2, 6))`: tensor Gauss–Hermite of orders 40 and 60 (64,000 and
216,000 nodes) and Monte Carlo with `10^6` samples (fixed seed), standard errors from the sample variance. The
integrand is bounded and piecewise smooth (kinks where a root of `g` crosses `-|B|/2` or `B`), so Gauss–Hermite
converges algebraically; the two orders and the Monte Carlo value bracket the truth to the digits shown.

| `k` | `J_1` GH40 / GH60 / MC (`±` s.e.) | `J_2` GH40 / GH60 / MC (`±` s.e.) | `J_2/(J_1+J_2)` | near Palm excess `2J_2/(J_1+2J_2)` |
|---|---|---|---|---|
| `1/2` | 35.652 / 35.676 / 35.559 ± 0.086 | 1.121 / 1.109 / 1.115 ± 0.0062 | 0.0301 | 0.0585 |
| `1` | 169.63 / 169.61 / 169.37 ± 0.28 | 3.249 / 3.255 / 3.281 ± 0.022 | 0.0188 | 0.0370 |
| `2` | 1104.2 / 1103.7 / 1102.6 ± 1.7 | 8.421 / 8.641 / 8.875 ± 0.073 | 0.0078 | 0.0154 |

`J_j(k) = E_(N(0, diag(2,2,6)))[I_j]`; the ratio columns are `b`-free. Prefactor `p_b(0)/z_0` and the coefficients `alpha_j = (p_b(0)/z_0) J_j` (GH60 values; MC in `RESULTS.json`):

| `k` | `b` | `z_0 = 36 k^2 m_(2,b)` | `p_b(0)/z_0` | `alpha_1` | `alpha_2` |
|---|---|---|---|---|---|
| `1/2` | `0` | 9 | 0.031344 | 1.118 | 0.0347 |
| `1/2` | `1` | 24.4813 | 0.008974 | 0.3202 | 0.00995 |
| `1` | `0` | 36 | 0.007836 | 1.329 | 0.0255 |
| `1` | `1` | 97.9251 | 0.0022435 | 0.3805 | 0.0073 |
| `2` | `0` | 144 | 0.001959 | 2.162 | 0.0169 |
| `2` | `1` | 391.7 | 0.00056088 | 0.619 | 0.00485 |

Reading: at `k = 1`, `b = 0`, `alpha_1 ≈ 1.33` and `alpha_2 ≈ 0.026`; about 1.9% of nonempty near clusters are two-point clusters, and the near part of the Palm excess `2 nu(2)/(nu(1) + 2 nu(2))` of [C6] Corollary P is at most about 3.7% (the remote singleton part of `nu(1)` only lowers it). The two-point share decreases in `k` (3.0% at `k = 1/2`, 0.78% at `k = 2`). Precision: `J_1` is known to about `0.2%` (GH40, GH60 and MC agree within the MC standard error); `J_2` to about `1%` at `k = 1/2` and `k = 1` and about `3%` at `k = 2`, where GH60 and MC differ by three standard errors because the integrand's kinks slow the Gauss–Hermite convergence; the MC value with its standard error is the better estimate of `J_2` there.

`L`-independence: the values at `L = 24` (the parent's SIDE24 application), `L = 12` and `L = 6` agree to the digits
shown, as §2 predicts (`exp(-L^2/2)` corrections). The full run is `coefficients.py` (writes `RESULTS.json`); the
replay mode `--check` re-verifies the exact structure, the closed forms, the classifier and the order-40 quadrature
against `RESULTS.json` (tolerance `1e-6`, floating point), and three mutants (`cubic-sign`, `antiderivative`,
`typed-boundary`) exit 1.

## 5. What these numbers are not

Not certified: no interval arithmetic; the Monte Carlo standard errors and the Gauss–Hermite order comparison are the
only error indications. Not the full `nu(1)`: the remote singleton coefficient `k integral_X Lambda` of [RM] is a
separate two-site Gaussian integral, not evaluated. Not a statement about `d >= 3`: the odd/even block structure and
the `N(0, diag(2, 2, 6))` law are planar. Not an acceptance of [CL] or [CUB]: if either near-coefficient formula fails
review, these are numbers for a formula, not for the model. Not a rate, not a finite-`r` statement.

## 6. Provenance

Sources and their exact bytes are in `SOURCE_MAP.json`: [LP] and [CUB] on `main`; [CL] at the head of Math-#159 (not
required on `main`). `coefficients.py` is standard-library Python; `RESULTS.json` is its output rounded to six
significant digits. The [LM] cubic `(−3k/2, 0, −2k, 0)` and the classifier are the same objects as in [CUB] and [CL];
no new mathematics is claimed here beyond the exact regression identities of §2, which are elementary.
