# Certified cusp coefficient `c1` (Math-#207, (CU.2)), Gaussian kernel

**Erratum 1 (13 October 2026):** `ERRATUM_20261013.md` records that the manuscript's correction ratio is enclosed, and that
its reading as the relative correction of [CU] (CU.1) is conditional on Theorem CU and on side24_v1's `c_(3,24)`. It answers
the second-provider read 5975882973 (XA-219-01..04); no number or code changes.

`CL-CU-CUSP-COEFFICIENT-20261001-v1` (v1.1). Author-side certified numerics; scientific effect NONE. See `NOTE.md`.

| `d` | `c1` | `c1 / c_(d,ref)` |
|---|---|---|
| `1` | `[-0.22760635877558, -0.22760635877504]` | |
| `2` | `[-0.269398825674, -0.269398825672]` | `[-3.66993776909, -3.66993776907]` |
| `3` | `[-0.211848347, -0.211848346]` | `[-5.07106215, -5.07106213]` |

For the [P] torus field of every side `L >= 24` (Lemma S), including SIDE24: `c1/c_(3,24)` is in
`[-5.07106215, -5.07106213]` and `c1/c_(2,24)` in `[-3.66993776909, -3.66993776907]`.

Replay: `python3 -B -S certificate.py --check --procs N` (self-test, then a full recomputation against `RESULTS.json`).
Standard library only.
