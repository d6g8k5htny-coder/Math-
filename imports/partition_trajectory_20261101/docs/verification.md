# Verification guide

Run from the package root:

```bash
python3 -m partition_trajectory
python3 -m unittest discover -s tests -v
```

The test command should report 12 passing tests.

## Exact model checkpoints

| Suite | Expected result |
|---|---|
| Parity reuse | 4 solutions |
| x-then-z | 0 solutions; stage 1 obstruction `{(0,0),(0,1)}` |
| Greedy retention | 36 solutions; first final partition `{(0,0)},{(0,1)},{(1,0),(1,1)}` |
| Flexibility | 108 empty, 36 O0-only, 36 O1-only, 0 joint |
| Single-task divergence | Pareto points `(0.12, 0.281917)` and `(0.25, 0.311278)`; full floor `0.12` |
| Temporal capacity 3 | Frontier `(0,0,0.25)`, `(0,0.25,0)`, `(0.25,0,0)`; no all-zero trajectory |
| Temporal capacity 4 | All-zero trajectory exists |
| Randomized minimax | Distribution-level `0.125`; realization-level `0.25` |
| Asymmetric example | Gap `0.0225`; robust total `0.475`; specialized mixture `0.5375` |
| Correlated boundary | Gaps `0`, `0.03`, `0.05`, `0.05` for κ `0`, `0.06`, `0.10`, `0.20` |

## Independent theorem checks

For independent channels, the suite verifies

\[
U_{\mathrm{real}}-U_{\mathrm{dist}}
=0.125(1-2\alpha)(1-2\beta)
\]

at multiple channel rates. It also verifies that this identity is not extrapolated to correlated channels.

## Clean execution

Copy only the source tree to a clean directory, then run the two commands above. The runtime has no third-party dependencies and does not depend on the original workspace.
