# C6 cluster coefficient numerics (CL-C6-CLUSTER-COEFF-NUMERICS-20260930-v1)

Numerical values (floating point, with standard errors; **not certified**) of the planar near cluster coefficients
`alpha_1`, `alpha_2` defined by the C6 cluster-law candidates ([CL] Math-#159 (1.3)/(3.11) at `d = 2`, [CUB] Theorem F)
for the exact periodized Gaussian kernel of the parent [LP]. Scientific effect NONE.

- `NOTE.md`: what is evaluated, the exact contact-regression structure (`A ~ N(-b, 2)`, odd block `N(0, diag(2,2,6))`,
  `z_0 = 36 k^2 m_(2,b)`), the exact interval structure of the `s`-integral, the values, and what they are not.
- `coefficients.py`: standard library only. `python -B -S coefficients.py` recomputes `RESULTS.json` (several minutes);
  `python -B -S coefficients.py --check` replays the exact controls and the order-40 quadrature against `RESULTS.json`;
  `--check --mutant NAME` exits 1 for `cubic-sign`, `antiderivative`, `typed-boundary`.
- `RESULTS.json`: `J_j(k)` (Gauss–Hermite 40/60, Monte Carlo `10^6` with standard errors), the exact prefactor
  `p_b(0)/z_0`, and `alpha_j(k, b)` for `k in {1/2, 1, 2}`, `b in {0, 1}`.
- `SOURCE_MAP.json`, `SOURCE_FILES.json`: pins and manifest.

Not evaluated: the remote part `k integral Lambda` of `nu(1)`; anything for `d >= 3`; any rate or enclosure.
