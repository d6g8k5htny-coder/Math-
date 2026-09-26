# T-RN-COMPLETE-REGION — Complete-region RN count

**Status:** open theorem.

## Target

A single theorem bounding the actual count-weighted integral on the **complete** declared RN region (not only remote-fixed or annulus pieces).

## Needed to close

1. Stitch author-closed pieces: [T-FIXED-REMOTE](../closed-theorems/T-FIXED-REMOTE.md), [T-ALL-HEIGHT-ANNULUS](../closed-theorems/T-ALL-HEIGHT-ANNULUS.md) / [T-FIXED-ANNULUS-WINDOW](../closed-theorems/T-FIXED-ANNULUS-WINDOW.md), [T-FIXED-TRANSVERSE](../closed-theorems/T-FIXED-TRANSVERSE.md), and [T-AXIAL-DENSITY](../closed-theorems/T-AXIAL-DENSITY.md) only where scoped. The accepted all-height fixed-annulus bound already covers the fixed-scale transverse chart away from the pins; do not list that chart as a remaining geometric hole.
2. Close remaining geometric gaps: [L-SHRINKING-EXCLUSION](../open-lemmas/L-SHRINKING-EXCLUSION.md) (mesoscopic `r ≪ dist ≪ ρ`), [L-PIN-COLLISION](../open-lemmas/L-PIN-COLLISION.md), and pin neighborhoods. Density-only intermediate-belt work ([L-INTERMEDIATE-BELT](../open-lemmas/L-INTERMEDIATE-BELT.md)) is not the count-stitch blocker once the annulus theorem is consumed.
3. Decide height-window versus all-height for each piece and document the union.
4. Independent review of the stitched statement ([main #67](https://github.com/d6g8k5htny-coder/main/issues/67) RN bullet).
