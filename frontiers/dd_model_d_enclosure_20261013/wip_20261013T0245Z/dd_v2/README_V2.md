# Certificate v2 (exact sliver geometry): a re-run candidate, not the certificate of record

`dd_v2/` is `dd/` (the certificate pinned at `35ae8fbb`, with control C10 at `11ca8934`) with one change: `ddvq._vcell` enlarges a sliver cell's half-width until the cell contains both of its endpoints (checked in exact rational arithmetic), so the gaps that control C10 bounds in v1 do not arise (`dd_gapcheck.py` on this directory reports 0 gaps). Every other file is byte-identical to `dd/`. The node files of this directory, when produced (workflow `dd-wip-shards.yml` dispatched with `dir: dd_v2`), differ from v1's only at the narrow-regime nodes, in the last digits of the sliver terms.

PROTOTYPE / UNVERIFIED until read; scientific effect NONE. The certificate of record is v1 with C10 (Math- `frontiers/lifetime_dd_model_d_20261013/`, Math-#448 landed, #449).
