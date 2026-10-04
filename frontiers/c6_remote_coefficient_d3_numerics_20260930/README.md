# Remote singleton coefficient in d = 3 (numerical note)

Object `CL-C6-REMOTE-COEFF-D3-NUMERICS-20260930-v1`. Scientific effect NONE; not certified; nonauthor read open.

`NOTE.md` evaluates the contact kernel `Lambda_j(x)` of [RM] (13) in dimension `d = 3` for the continuum parent kernel:
its far field (exact shifted-GOE quadrature), the correlation-hole constant `c_hole = integral (Lambda - Lambda_inf) d^3x`
(Monte Carlo with common random numbers, standard errors reported) and the torus integral
`k integral_X Lambda = k (L^3 Lambda_inf + c_hole)` for `L = 12, 24`, assembled with the `d = 3` near coefficients
`a_j^(3) = R_3(b) alpha_j^(2)` (Math-#184, conditional; Math-#168 planar values) into `nu(1)`, `nu(2)`.

    python -B -S remote3.py --check          # rc 0 (also with -O); about half a minute
    python -B -S remote3.py --check --mutant hermite-sign   # rc 1 (also det-abs, weight-indicator)
    python -B -S remote3.py                  # regenerates RESULTS.json (about an hour)

`SOURCE_MAP.json` pins the consumed sources on `main`; `SOURCE_FILES.json` is the packet manifest.
