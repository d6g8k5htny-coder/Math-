# Certified planar normalizer floor (C8, first band)

**Object:** `CL-C8-NORMALIZER-FLOOR-PLANAR-20260930-v1`. **Author lane:** Anthropic / Claude. **Kind:** certified numerical
constant (exact rational interval arithmetic; every transcendental bracketed by a series with an explicit remainder).
**Scientific effect:** NONE (no register, catalog, GRAPH or STATUS change; C8 stays OPEN).

Proves, for the parent torus kernel of [LP] in `d = 2`, every orthonormal frame and every side `L >= 10`, and for every
`r in [1/8, 1/2]`, `b in [0, 1]`, `k in [1/2, 2]`, the explicit floor `Z_r / r^2 >= z_*` for the full normalizer
`Z_r = E_Q |det H_M det H_S| 1{H_M < 0, index H_S = 1}` of [LP] section 1 (the constant whose existence is (5.5) there).
The value and the full table of per-sub-box floors are in `RESULTS.json` (`z_star`, `table`); NOTE.md states the
method and the exact scope.

- `NOTE.md` — statement, method (midpoint-jet preconditioning, exact Laurent-polynomial cancellation, torus remainder
  bound, block Cholesky with coupling shrink, cell sums with endpoint minima), values, controls, non-claims.
- `floor.py` — standard-library script (Python `>= 3.11`): `--check` replays the manifest-pinned floor exactly on two
  sub-boxes, verifies the stored minimum, the floating controls and the constants; the full run (`--procs 4`, about an
  hour) regenerates `RESULTS.json`; `--mutant {swap-minmax, drop-torus-error, sign-saddle}` must exit 1.
- `RESULTS.json`, `SOURCE_MAP.json` (two main-resident pins: [LP], [NUM]), `SOURCE_FILES.json`.
- Workflow `.github/workflows/c8-normalizer-floor-planar.yml` replays manifest, pins, both check modes and the mutants.

Same GitHub account as every other lane; zero organizational-independence credit. The author will not merge.
