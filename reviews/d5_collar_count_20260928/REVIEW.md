# Nonauthor review: compact collar first moment and scaled-ball synthesis

Scientific effect: **NONE**. This file does not change `lemma_closed`, prizes,
premises, `STATUS`, `PROOF_INDEX`, `GRAPH`, or any author source.

Math- `main` after #117: review files `reviews/d5_i5_planar_f_20260928/` already consume scaled-ball (C2) as a companion bound. This record is the source-bound review of that companion.

## Objects

| Object | Path |
|---|---|
| Collar | `reviews/d5_local_collar_20260928/COLLAR_PROOF.md` |
| Punctured pin | `reviews/d5_local_collar_20260928/PUNCTURED_PIN_PROOF.md` |

## Verdicts

| ID | Statement | Verdict |
|---|---|---|
| Interpolation | degree-five three-site value/gradient map has rank 9 on the compact collar, including the midpoint axis | ACCEPT |
| Gram | `det(BB^T)=u^2 v^4 + v^6/4`; `sigma_min(B) >= c v^2` | ACCEPT |
| Coarse floor | `Cov_{Q_r}(grad f(X)) >= c r^{10} I_2` after deleting the auxiliary witness value | ACCEPT existential |
| Collar first moment | `E_{Q^W} N_j(r E) <= C r^3 |E|` on `C(eta, R)` | ACCEPT existential |
| Scaled-ball synthesis | same bound on `{|x|<=R} minus two pins` at `eta=1/4` | ACCEPT corollary of punctured-pin + collar |

## Intensity split used

Axis split at `C_* r^{1/2}`.

- `|v| <= C_* r^{1/2}`: coarse `r^{10}` floor; intensity `r^{-72} exp(-c/r) <= C r`.
- `C_* r^{1/2} <= |v| <= v_0`: B-frame floor; intensity `r |v|^{-34} exp(-c/v^2) <= C r`.
- `|v| >= v_0`: uniform; intensity `O(r)`.

Weighted Kac-Rice: Armentano-Azais-Leon arXiv:2304.07424v3 Theorems 2.2 and 7.1, Remark 8. One witness determinant. `F_j` continuous on all symmetric matrices.

## Not claimed

Numerical `C`, `r_*`. Uniformity in `R` up, `eta` down, `T`, or `k` down to 0. Elder pairing. Any STATUS / GRAPH / lemma_closed / prize change.
