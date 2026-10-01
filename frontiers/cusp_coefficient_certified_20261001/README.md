# Certified cusp coefficient `c1` (Math-#207, (CU.2)), Gaussian kernel

`CL-CU-CUSP-COEFFICIENT-20261001-v1`. Author-side certified numerics; scientific effect NONE. See `NOTE.md`.

| `d` | `c1` | `c1 / c_(d,ref)` |
|---|---|---|
| `1` | `[-0.22760635877558, -0.22760635877504]` | |
| `2` | `[-0.269398825674, -0.269398825672]` | `[-3.66993776909, -3.66993776907]` |
| `3` | `[-0.211848347, -0.211848346]` | `[-5.07106215, -5.07106213]` |

Replay: `python3 -B -S certificate.py --check --procs N` (self-test, then a full recomputation against `RESULTS.json`).
Standard library only.
