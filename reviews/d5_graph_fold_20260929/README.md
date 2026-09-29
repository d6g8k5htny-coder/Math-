# D5 graph/proof-index fold — 2026-09-29

This additive integration executes the already reviewed, declarative D5 reconciliation against the live downstream graph and repairs the public proof index/catalog. It does not alter proof bodies, `STATUS.md`, `LANDING_CLAIMS.json`, prizes or scientific Booleans.

Scope:
- planar `d=2`, fixed `T`, compact marks with `k>=k_->0`, existential constants;
- D5-a–D5-d all-height first moments and D5-e–D5-f window-only first moments;
- reviewed planar C6 upper bound `E N(N-1)<=C r^3 log(1/r)`.

Explicitly open: shrinking witness collision, sharp `Theta(r^3)`, Palm/size-biased repair, `d>=3` first moments, numerical constants, RN/24-jet/JETMOD and elder selection.

Run:

```sh
python -B -S reviews/d5_graph_fold_20260929/verify.py
python -B -O -S reviews/d5_graph_fold_20260929/verify.py
```

The verifier checks exact proposed nodes/edges and negative controls for a missing node, stale fingerprint, missing edge and accidental witness closure. Passing software checks are not mathematical acceptance.
