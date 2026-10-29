# Exact mathematical source snapshots

This one-shot source-preservation workflow serves CBZ criteria1–3 and9. It creates six annotated tags at the exact commits in `plan.json`: the five paper deliveries Q-7522 throughQ-7526 and the complete source514 history. Existing tags are never moved or overwritten. Every source commit must exist and every final remote annotated-tag peel must equal the declared commit. All before/after remote readbacks, including failures, are retained as a native artifact.

Run `.github/workflows/cbz-preserve-math-deliveries.yml` by its PR event or workflow_dispatch. Its standard Git commands are fully specified in that workflow. It requires contents:write solely to create these repository-local tags; it does not delete or rewrite any existing ref, change mathematics or tests, close PRs, or admit a theorem. The canonical integrator supplies exact proof/quarantine boundaries and verifies native tag objects before terminal dispositions.

The self-verification is the actual six-member Git object/type/remote peel check plus independent native API readback by the integrator. Initial state: NOT_RUN. This is an operational source-preservation helper, not a Layer A mathematical auditor. Maintenance owner:none — bounded one-shot source snapshot. Preserve its plan and observed results in the federation Decision Ledger and tool registry.
