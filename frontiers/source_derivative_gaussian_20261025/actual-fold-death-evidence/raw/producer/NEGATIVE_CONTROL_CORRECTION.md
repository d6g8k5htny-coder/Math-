# Correction of negative-control evidence shape

Root identified that false-control-001 failed by equation type mismatch, not
a sole residual False. The initial summary labeling was inaccurate. Original
raw source, log and receipt remain in runs/false-control-001; initial report,
control receipt and identity summary are saved in summary-history.

Only scratch FalseMutation.lean was changed to rewrite the proved physical
death2 into its claimed wrong equation and norm_num. New false-control-002
exited1 in 2.624248028s with one error, exactly unsolved goals / ⊢ False.
REPORT.md, CONTROL_RECEIPT.json, EXECUTION_RECORD_INDEX.json and the scratch
mutation identity were corrected. No production edit, new kernel, inventory
or positive-control rerun occurred. Completed applicable evidence is reused.
