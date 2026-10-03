# The cap-failure coefficient in the plane (C8: what any cap-route constant `C_cap` must exceed)

**Object:** `CL-C8-CAP-FAILURE-COEFFICIENT-PLANAR-20260930-v1`. **Author lane:** Anthropic / Claude. **Kind:** author-side
limit theorem with certified enclosures of its coefficient (exact rational interval arithmetic; standard library only).
**Scientific effect:** NONE (no register, catalog, GRAPH or STATUS change; C8 stays OPEN: no `C`, no `r_*` supplied).

For the planar six-pin law of [LP] and the good event `G_r = {lambda_min(-A_M) > (4/(3k)) r M_3^2, r M_4 <= 3k/10}` of
[LP] section 7 / [CAP] (1), Theorem G (`NOTE.md`) gives the exact leading behaviour of the cap-failure probability that the
proof of Theorem A bounds ([LP] (7.8)):

    Q^W(G_r^c) = c_G(b, k) r^3 + o(r^3),      c_G(b, k) = R(b) J(k),

with `R(b)` in closed form and `J(k)` a three-dimensional Gaussian expectation reduced to one-dimensional integrals and
certified at `k in {1/6, 1/2, 3/4, 1, 3/2, 2}` for the reference kernel (`J(k) = 2359296 k^3 (1 + delta(k))`, `delta -> 0`;
the finite-torus jet-law deviation, of order `L^6 e^{-L^2/2}`, is not enclosed). Reference-kernel consequences: every
cap-route constant `C_cap` (any constant with `Q^W(G_r^c) <= C_cap r^3`) at `(b, k)` is at least `c_G(b, k)`; on the
Math-#195 band `C_cap > 5.3 x 10^6` (not a lower bound for the constant of Theorem A's `1 - p_r <= C r^3`, which bounds a
smaller probability); the cap route is informative only below `r = c_G^{-1/3}` (`6 x 10^-3` at the band's corner `(0, 2)`);
the recorded cap-route constant `≈ 2.36 x 10^23` of [CAP] at `(6/5, 1/6)` exceeds the reference-kernel sharp cap coefficient
`c_G^{ref}(6/5, 1/6)` by more than `6 x 10^18` (the comparison with SIDE24's own finite-`L` coefficient is not enclosed); the criterion overstates the true failure rate `alpha_1 + alpha_2` by `10^4`–`10^6`.

- `NOTE.md` — statement, proof of Theorem G (coupling, regression on `f_yy(M)`, dominated convergence, parity), the
  one-dimensional reduction, certification method, tables, consequences, non-claims.
- `cap_coefficient.py` — `--check --procs N` recomputes every enclosure and compares exactly with `RESULTS.json` (about four
  minutes per `k` on one core); `--mutant {no-third-jet, sign-lo, variance-yyy}` must exit 1; no flags regenerates
  `RESULTS.json`; `--quick K` certifies one `k`.
- `RESULTS.json`, `SOURCE_MAP.json` (pins [LP], [CAP], [NUM], [S] on `main`), `SOURCE_FILES.json`.
- Workflow `.github/workflows/c8-cap-failure-coefficient-planar.yml` replays manifest, pins, both interpreter modes and the
  six mutant runs on every pull request.

Same GitHub account as every other lane; zero organizational-independence credit. The author will not merge.
