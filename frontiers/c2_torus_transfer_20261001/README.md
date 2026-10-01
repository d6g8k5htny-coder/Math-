# `c2` on the finite torus: transfer for every `L >= 10` (Math-#218 (0.1), against `frontiers/c2_exact_20261001`)

`CL-C2-TORUS-TRANSFER-20261001-v1`. Author-side; scientific effect NONE. See `NOTE.md`.

For the normalized periodic Gaussian kernel `K_L` (SIDE24 is `L = 24`), every orthonormal frame and every real `L >= L0`,
`|c2[K_L] - c2[phi]| <= eps_d(L0)`:

| `d` | `L >= 10` | `L >= 24` |
|---|---|---|
| `1` | `1.41035e-13` | `4.09547e-114` |
| `2` | `2.09404e-12` | `5.20139e-113` |
| `3` | `1.00039e-10` | `2.09418e-111` |

Lemma E: for every smooth stationary kernel the fixed-cone surrogate is `A~(r^2, b - k r^3/2, k)`, so it has no `r^1` term
and its `r^3` coefficient is `-(k/2) d_b A_0`.

Replay: `python3 -B -S transfer.py --check` (exact rational ball arithmetic, standard library only; about two minutes).
Controls: `python3 -B -S controls.py`.
