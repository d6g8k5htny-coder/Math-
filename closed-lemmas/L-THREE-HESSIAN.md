# L-THREE-HESSIAN — Deterministic three-Hessian smallness

**Status in this map:** closed lemma (completed proof).

## Statement

Three noncollinear zero gradients force all three Hessians to be small.

- **Annulus-bridge form (PR28 R4):** product of absolute determinants is `O(r^6 |v|^{-6} M_3^6)` off-axis, with an axis fallback using `M_2` only (no division by `v`); displays (6)–(8).
- **Fixed-transverse form (PR16 R3):** on the chart `|v| ≥ η > 0`, the accepted bound is of the shape `C r^6 M_3^6` (η fixed away from zero). That ACCEPT does **not** by itself license the `|v|^{-6}` form or the axis fallback.

## Completed proof

| Field | Value |
|---|---|
| Primary write-up | [`frontiers/rn_annulus_bridge_20260925/PROOF.md`](../frontiers/rn_annulus_bridge_20260925/PROOF.md) §4, displays (6)–(8) |
| Size / SHA256 (bridge proof) | 16948 B / `d55e2c03bb17e7977ff94130cc1ff21e54840cd1e20dc4e41ea9ad52228beb05` |
| Reviews | PR28 R4 **ACCEPT** (bridge form); PR16 R3 **ACCEPT** (fixed-chart form only) |

## Scope boundary

Requires a Gaussian input controlling full conditional C³ moments after the witness gradient condition (bridge R3), not endpoint-only moments.
