# LEDGER.json schema note: residual_items status

Scientific effect: NONE. Additive documentation; changes no proof, review verdict, status value, graph node, prize or premise.

In `LEDGER.json`, each entry of `residual_items` has `"status": "DISCHARGED"`. Here that value means only:

- **residual review remark addressed** by the interfaces or reconciliation sections listed in `discharged_by`;
- **not an OBL discharge**: no open obligation (OBL-*, including OBL-H5-JETMOD) is discharged, closed or promoted by these rows;
- **no fail-closed flag affected**: `lemma_closed`, `prizes_solved`, `discharges_OBL_H5_JETMOD`, `certified_C_H` and similar controls are unchanged.

`reconciliation_check.py` requires the literal value `DISCHARGED` (L107 and L177), so the value is kept as is; this note documents its meaning without renaming it.
