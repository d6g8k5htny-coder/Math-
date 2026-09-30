# Remote singleton coefficient numerics (planar, parent kernel)

**Object:** `CL-C6-REMOTE-COEFF-NUMERICS-20260930-v1`. **Author lane:** Anthropic / Claude. **Kind:** numerical
note (floating-point quadrature with convergence checks; no proof, no enclosure). **Scientific effect:** NONE.

Evaluates the contact kernel `Lambda_j(x; b, k, u)` of [RM] (13) in the plane for the parent kernel
`K(z) = exp(-|z|^2/2)` and its `L`-periodization, its far-field value, the correlation-hole constant
`c_hole = integral_(R^2) (Lambda - Lambda_inf) dx`, and the remote singleton mass `k integral_X Lambda dx`
that enters `nu(1)` by [CL] (1.4). Companion of the near-coefficient note (Math-#168), whose values of
`alpha_1 = nu_near(1)` are quoted to assemble `nu(1)`.

- `NOTE.md` — statement of what is evaluated, exact structure, method, values, precision, non-claims.
- `remote.py` — standard-library script: `--check` (exact controls and replay against `RESULTS.json`), full run
  regenerates `RESULTS.json`; `--mutant {hermite-sign, det-abs, weight-indicator}` must exit 1.
- `RESULTS.json` — all numbers, grids and convergence checks.
- `SOURCE_MAP.json` — pinned sources on `main` (blob identities); `SOURCE_FILES.json` — packet manifest.
- Workflow `.github/workflows/c6-remote-coefficient-numerics.yml` replays manifest, pins, both check modes and the
  mutants.

Same GitHub account as every other lane; zero organizational-independence credit. The author will not merge.
