# Certified planar normalizer floor (C8, first band)

**Object:** `CL-C8-NORMALIZER-FLOOR-PLANAR-20260930-v1`. **Author lane:** Anthropic / Claude. **Kind:** certified numerical
constant (exact rational interval arithmetic; every transcendental bracketed by a series with an explicit remainder).
**Scientific effect:** NONE (no register, catalog, GRAPH or STATUS change; C8 stays OPEN).

Proves, for the parent torus kernel of [LP] in `d = 2`, every orthonormal frame, every side `L >= 12`, and every
`r in [1/64, 1/2]`, `b in [0, 1]`, `k in [1/2, 2]`, the explicit floor `Z_r / r^2 >= z_* = 3.5044` (the band
`[1/8, 1/2]` alone holds for `L >= 10`; the band `[1/64, 1/8]` has floor `7.0499`) for the full normalizer
`Z_r = E_Q |det H_M det H_S| 1{H_M < 0, index H_S = 1}` of [LP] section 1 (the constant whose existence is (5.5) there).
The values and the full tables of per-sub-box floors are in `RESULTS.json` (`combined`, `bands.high`, `bands.low`); NOTE.md states the
method and the exact scope.

- `NOTE.md` — statement, method (midpoint-jet preconditioning, exact Laurent-polynomial cancellation, torus remainder
  bound, block Cholesky with coupling shrink, cell sums with endpoint minima), values, controls, non-claims.
- `floor.py` — standard-library script (Python `>= 3.11`): `--check` replays the manifest-pinned floor exactly on twelve
  sub-boxes of the two bands, verifies the stored minimum, the floating controls and the constants (about three minutes);
  `--check-full --procs N` regenerates all 11904 sub-box floors and compares them exactly (about 85 minutes on four cores;
  the workflow's on-demand `full-regeneration` job); the full run (`--procs 4`) regenerates `RESULTS.json`;
  `--mutant {swap-minmax, drop-torus-error, sign-saddle}` must exit 1.
- `RESULTS.json`, `SOURCE_MAP.json` (two main-resident pins: [LP], [NUM]), `SOURCE_FILES.json`.
- Workflow `.github/workflows/c8-normalizer-floor-planar.yml` replays manifest, pins, both check modes and the
  mutants on every pull request, and regenerates every sub-box on demand (`workflow_dispatch`).

Same GitHub account as every other lane; zero organizational-independence credit. The author will not merge.
