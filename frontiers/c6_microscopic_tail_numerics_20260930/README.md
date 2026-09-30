# Planar microscopic radius-tail constants (parent kernel, d = 2)

**Object:** `CL-C6-MICRO-TAIL-NUMERICS-20260930-v1`. **Author lane:** Anthropic / Claude. **Kind:** numerical note
(deterministic Gauss quadrature with reported convergence; no proof, no enclosure). **Scientific effect:** NONE.

Evaluates, for the parent kernel `exp(-|z|^2/2)` in the plane, the point-intensity tail constant `C_*` of the
already-formed microscopic measure ([R] (R13); `F(t) ~ C_* t^-11`), the whole-cluster split of that tail
(Math-#169, unmerged companion), the second-order coefficient `C_2/C_0`, the TV coefficient `kappa |C_2/C_0|` and
the signed constant `B_sign` (Math-#176, unmerged companion), for `k in {1/2, 1, 2}` and `b in {0, 1}`. In `d = 2`
the [SC] measure reduces to the exact contact regression of Math-#168, so every constant is a one-dimensional
Gaussian integral; the four-dimensional near-mass identity `alpha_1 + 2 alpha_2 = K_0 int Q |Z|^-12 p_odd` is
evaluated as a control against the merged Math-#168 values.

- `NOTE.md` — what is evaluated, exact structure, values, precision, non-claims.
- `tail_constants.py` — standard-library script (Python `>= 3.11`): `--check` (exact controls and replay against
  `RESULTS.json`), full run regenerates `RESULTS.json` (about fifteen minutes); `--mutant {shape-integral, gamma-power,
  cusp-shift}` must exit 1.
- `RESULTS.json`, `SOURCE_MAP.json` (five main-resident pins and two unmerged companions), `SOURCE_FILES.json`.
- Workflow `.github/workflows/c6-microscopic-tail-numerics.yml` replays manifest, pins, both check modes and the
  mutants.

Same GitHub account as every other lane; zero organizational-independence credit. The author will not merge.
