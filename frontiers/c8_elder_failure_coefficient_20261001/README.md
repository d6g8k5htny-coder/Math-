# Certified planar near cluster coefficients and the elder-failure constant

Certified interval enclosures, for the reference planar kernel, of the near cluster coefficients `alpha_1`, `alpha_2`
(`nu(2) = alpha_2`) of [NUM] at `k = 1/2, 1, 2`, `b = 0, 1`, and of the constant `C_fail^{B,K}` of [S] §9 on
`[0, 1] x [1/2, 2]`. Details and the method are in [NOTE.md](NOTE.md).

- `J_fail(1/2)` is in `[36.783058, 36.786801]`, `J_fail(1)` in `[172.84636, 172.86021]` and `J_fail(2)` in
  `[1111.98227, 1112.03079]`.
- `J_2(1/2)` is in `[1.1061, 1.1095]`, `J_2(1)` in `[3.2531, 3.2625]` and `J_2(2)` in
  `[8.8250, 8.8527]`. The last settles the Gauss–Hermite / Monte Carlo disagreement that [NUM] reported at
  `k = 2`.
- `C_fail^{B,K}` is in `[0.0027244, 0.0027312]`, about `1.5 x 10^5` below the cap-route constant
  `C_{B,K}(1/4096) = 402.53` of Math-#215.

**Method.** A third-order box scheme:
- second-order Taylor expansion in `(B, w = |u|)`, where the Hessian of the failure integrand is bounded and explicit;
- interval Hessian ranges times exact Gaussian moments, intersected with first-order monotone bounds;
- `k` as a fourth box coordinate for `C_fail`.

**Arithmetic.** Standard-library Python and binary64 interval arithmetic; no transcendental library value is trusted.

**Replay.** `python3 -B -S certificate.py --check` (CI in both interpreter modes, with five mutants). Floating controls:
`python3 -B certificate.py --controls`.

**Scientific effect:** NONE. Author-side; conditional on the sources' identifications ([NUM] from [CL]/[CUB], [S]).
Same GitHub account as every lane; zero organizational-independence credit.
