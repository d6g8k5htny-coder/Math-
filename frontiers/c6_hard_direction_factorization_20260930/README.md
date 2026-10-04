# Hard-direction factorization of the near cluster coefficients (Gaussian kernel)

Object `CL-C6-HARD-DIRECTION-FACTORIZATION-20260930-v1`. Scientific effect NONE; not certified; nonauthor review open.

`PROOF.md` proves that for the unit Gaussian kernel the [SC] (17) near cluster measure in dimension `d` is the
planar measure times an explicit factor: for every functional `g` of the soft cubic `(s, a, beta, c)`,
`integral g dM^(d) = R_d(b) integral g dM^(2)` with `R_d(b) = N_d(b) m_(2,b) / m_(d,b)` (a shifted-GOE eigenvalue
integral over a conditioned determinant moment). Consequently `a_j^(d) = R_d(b) a_j^(2)`, `C_*^(d) = R_d(b) C_*^(2)`,
`a_2/a_1` and every normalized microscopic shape law are dimension-independent, and `R_3(0) = (32 + 28 sqrt2)/17`.

`factorization.py` (standard library) checks Lemma 1 exactly in `d = 2..5`, evaluates `R_d(b)` for `d = 2..5`,
`b = 0, 1`, cross-checks by Monte Carlo and by a finite-`r` evaluation of `Z_r / r^2`, and assembles the `d = 3, 4, 5`
near coefficients from Math-#168's planar values.

    python -B -S factorization.py --check          # rc 0 (also with -O); under ten seconds
    python -B -S factorization.py --check --mutant drop-vandermonde   # rc 1 (also hard-power-two, drop-spectral-constant)
    python -B -S factorization.py                  # regenerates RESULTS.json (about ten minutes)

`SOURCE_MAP.json` pins the consumed sources on `main`; `SOURCE_FILES.json` is the packet manifest.
