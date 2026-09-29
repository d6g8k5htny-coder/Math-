# D5 graph/proof-index fold — 2026-09-29

This additive integration executes the already reviewed, declarative D5 reconciliation against the live downstream graph and repairs the public proof index/catalog. It does not alter proof bodies, `STATUS.md`, `LANDING_CLAIMS.json`, prizes or scientific Booleans.

Scope:
- planar `d=2`, fixed `T`, compact marks with `k>=k_->0`, existential constants;
- D5-a–D5-d all-height first moments and D5-e–D5-f window-only first moments;
- reviewed planar C6 upper bound `E N(N-1)<=C r^3 log(1/r)`.

Separate reviewed/merged packets are not folded by this planar transition: the fixed-dimensional D5 first moments in `frontiers/d5_dimension_lift_20260929/` (Math-#141), the sharp Palm route in `frontiers/c6_palm_route_20260929/` (Math-#145), and the conditional rare-cluster consequences in `frontiers/c6_rare_cluster_laws_20260929/` (Math-#153).

Explicitly open in this graph fold: the regional shrinking witness-collision mechanism and its `OPEN_ACTIVE` node. Numerical constants and RN/24-jet/JETMOD remain outside this fold; no elder-selection or other register transition is inferred.

Run:

```sh
python -B -S reviews/d5_graph_fold_20260929/verify.py
python -B -O -S reviews/d5_graph_fold_20260929/verify.py
```

The verifier checks exact proposed nodes/edges and negative controls for a missing node, stale fingerprint, missing edge and accidental witness closure. Passing software checks are not mathematical acceptance.
