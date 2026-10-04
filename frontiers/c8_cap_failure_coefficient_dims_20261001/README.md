# The cap-failure coefficient in every dimension (C8: what any cap-route constant must exceed in `d >= 3`)

**Object:** `CL-C8-CAP-FAILURE-COEFFICIENT-DIMS-20261001-v1`. **Author lane:** Anthropic / Claude. **Kind:** author-side limit
theorem (Theorem G_d, `d >= 3`) with certified `d = 3` coefficients (exact rational interval arithmetic, standard library
only). **Scientific effect:** NONE: no register, catalog, GRAPH or STATUS change; C8 stays OPEN; no `C` or `r_*` is supplied.

**Statement.** For the `d`-dimensional [LP] law and the [CAP] (1) good event with partial-block operator norms,

    Q^W(G_r^c) = c_G^(d)(b, k) r^3 + o(r^3),      c_G^(d) = R_d(b) . R(b) . J^(d)(k)   (reference kernel).

- `R_d(b)` is the hard-direction factor of Math-#184.
- `R(b)` is the planar factor of Math-#203.
- `J^(d)(k)` is the planar `J` with `M = max(12k, 2||v||, ||Omega||_op, ||Y||_op)` taken over the full transverse blocks.
  Here `v ~ N(0, I/2)`, `Omega ~ GOE`, and `Y` is the isotropic Gaussian cubic of Lemma 1, all independent.

**In `d = 3`.**
- **Certified values.**
  - `R_3(0) = (32 + 28 sqrt2)/17`.
  - `J^(3)(k)` is enclosed tightly at `k = 1, 3/2, 2`, by monotone coupling with Math-#203's certified planar `J` plus
    `chi^2` tails.
  - `c_G^(3)(0, 2) in [22424320.655069, 22424320.655072]`, which equals `R_3(0) c_G(0, 2)` to `1e-13`.
- **Consequences.**
  - Every `d = 3` cap-route constant at the band corner exceeds `2.24 x 10^7`.
  - The `d = 3` cap route is informative only below `r = 3.55 x 10^-3`.
  - The cap criterion's overstatement of the true `d`-dimensional failure is the planar one times `J^(d)/J^(2)`:
    `1 + O(1e-4)` for `k >= 1` (certified); Monte Carlo `1.0011` at `k = 3/4`, `1.135` at `k = 1/2` and `5.12` at the SIDE24
    gap `k = 1/6`.

**Files.**
- `NOTE.md`: statement, Lemma 1 (the `d = 3` contact law, exact), the `d`-dimensional weight, the proof of Theorem G_d
  (spectral coordinates, the near-corank strip from [LP] (7.4), dominated convergence), the certified `J^(3)` method,
  values, controls, and non-claims.
- `cap_coefficient_dims.py`:
  - `--check` re-verifies Lemma 1 and every certified enclosure against `RESULTS.json` in about one second;
  - `--mutant {no-y-tail, r3-one, no-bp, frob-omega-off}` must exit 1;
  - `--controls` recomputes the floating Monte Carlo and quadrature controls.
- `RESULTS.json`, `SOURCE_MAP.json` (pins [LP], [CAP], [SC] on `main`; read-only references to Math-#203 and Math-#184),
  `SOURCE_FILES.json`.
- Workflow `.github/workflows/c8-cap-failure-coefficient-dims.yml`.

Same GitHub account as every other lane; zero organizational-independence credit. The author will not merge.
