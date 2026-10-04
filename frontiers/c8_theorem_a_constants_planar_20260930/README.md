# Explicit cap-route constants for Theorem A in the plane (C8: certified `C`, `r_*`, `z_*` on a declared band)

**Object:** `CL-C8-THEOREM-A-CONSTANTS-PLANAR-20260930-v1`. **Author lane:** Anthropic / Claude. **Kind:** author-side theorem
with explicit constants, certified by exact rational interval arithmetic (standard library only). **Scientific effect:**
NONE: no register, catalog, GRAPH or STATUS change, and catalog entry C8 stays OPEN.

**Setting.** The planar six-pin law of [LP] with the good event
`G_r = {lambda_min(-A_M) > (4/(3k)) r M_3^2, r M_4 <= 3k/10}` of [LP] section 7 / [CAP] (1). Theorem E (`NOTE.md`) holds on
the band `b in [0, 1]`, `k in [1/2, 2]`, uniformly over frames and torus sides `L >= 10`, and for the reference kernel:

    Q^W(G_r^c) <= C(r_*) r^3   and   Z_r / r^2 >= z(r_*)      for 0 < r <= r_*,

| `r_*` | `C(r_*)` | `C r_*^3` | `z(r_*)` |
|---|---|---|---|
| `1/4096` | `5355315.0638` | `7.8e-5` | `8.9953` |
| `1/2048` | `5362302.4479` | `6.3e-4` | `8.9907` |
| `1/1024` | `5377835.0775` | `5.1e-3` | `8.9815` |
| `1/512` | `5415659.2391` | `0.0404` | `8.9629` |
| `1/256` | `9370799.9311` | `0.559` | `8.9217` |

(`1/128` and `1/64` are also certified, with `C r_*^3 > 1`.)

**Theorem E' (v1.1).** The same holds at the fixed-axis SIDE24 point `(b, k) = (6/5, 1/6)` of [CAP] §1:

| `r_*` | `C'(r_*)` | `C' / c_G(6/5, 1/6)` | `C' r_*^3` |
|---|---|---|---|
| `1/4096` | `39322.818` | `1.100` | `5.8e-7` |
| `1/2048` | `43092.238` | `1.206` | `5.1e-6` |
| `1/1024` | `1283859.690` | `35.9` | `0.0012` |
| `1/512` | `117316965.49` | `3283` | `0.874` |

This replaces [CAP]'s `2.4 x 10^23`, which is nontrivial only below `r = 1.6 x 10^-8`.

**What follows.**
- **Explicit Theorem A.** Since `1 - p_r <= Q^W(G_r^c)` ([LP] §8), [LP] Theorem A (1.1) holds on this band with explicit
  pairs, for example `(C, r_*) = (5415659.2391, 1/512)` or `(9370799.9311, 1/256)`. [LP] §16 lists such a pair among the items
  it does not supply. For the SIDE24 law, `1 - p_elder(r) <= 39322.818 r^3` for `r <= 1/4096`.
- **Near-optimal for the cap route.** The constants are within `0.6%`–`1.8%` of the sharp cap coefficient
  `c_G(0, 2) = 5324360.44` of Math-#203, below which no cap-route constant can go.
- **Normalizer floor.** Together with Math-#195, `Z_r / r^2 >= 3.5044` on all of `(0, 1/2]` for `L >= 12`.

**Files.**
- `NOTE.md`: statement, the exact identities, Lemmas 1–5 (exact covariance series with a frame- and `L`-uniform torus
  remainder; averaging identities for `M_3`; the Taylor bound for `M_4`; the root bounds after regression on `f_yy(M)`; the
  normalizer floor), the main term, the rare branches, bands, values, Monte Carlo controls, and non-claims.
- `theorem_a.py`: the certificate and its replay.
  - `--check --procs N` replays the parameters, 11 sampled bands and both `C` tables exactly against `RESULTS.json`.
  - `--check-full` replays all 153 bands, in about ten minutes on four cores.
  - `--mutant {no-delta, cap-half, no-zfloor-correction, no-om-term}` must exit 1.
  - With no flags it regenerates `RESULTS.json`.
  - `--mc R B K N SEED` is the floating Monte Carlo control.
- `RESULTS.json` (one line per band: 28 box bounds, 28 floors, the largest tail part, the SIDE24 bound and floor),
  `SOURCE_MAP.json` (pins [LP] and [CAP] on `main`; read-only references to Math-#203 and Math-#195), `SOURCE_FILES.json`.
- Workflow `.github/workflows/c8-theorem-a-constants-planar.yml` replays the manifest, the pins, `--check-full` and `--check`
  in the two interpreter modes, the four mutants, and a clean tree.

Same GitHub account as every other lane; zero organizational-independence credit. The author will not merge.
