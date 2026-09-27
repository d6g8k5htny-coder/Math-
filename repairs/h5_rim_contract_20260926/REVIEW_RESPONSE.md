# Review response: H5 rim input contract

Date: 2026-09-26. Scientific effect: **NONE**.

## Reviewed head and verdict

OpenAI nonauthor review examined Math- commit
`0e248ad3ab5263c9a83b7740796a7206619d52de` and returned **AMEND**. The reviewer
made no source edits and receives zero organizational-independence credit.
The review confirmed the pinned historical finding while identifying two
reusable-interface defects:

1. a failure-only tail after the last `rimprobes_done` marker left `block` empty
   and `block_failed` true, but the EOF gate tested only `block`, so the prior
   completed constants were returned;
2. numeric JSON `rho_hi` reached `Decimal` through a binary float even though
   the contract promised exact decimal strings. Numerically equal float angle
   encodings were likewise accepted by Python dictionary/set equality.

The first defect is blocking because it contradicts the advertised fail-closed
handling of failed/unfinished coverage. The other two are exact-input schema
defects. A filename such as `h5_results_r0.05_anything.jsonl` remains accepted
by design: the interface promises radius binding, not a fixed producer suffix.

## Successor changes

- EOF now rejects `block_failed` even when no successful rim row followed the
  last completion marker.
- `rho_hi` must be a JSON string before conversion to `Decimal`.
- every rim angle must have exact JSON integer type (`bool` and float reject).
- three regression tests reproduce the previously accepted inputs and bind the
  corrected behavior.

The reviewer also suggested checking `[175]` again immediately before the CLI
success message. Source hashes fix the two inputs and the report tests assert
the mismatch list; the successor additionally makes the CLI check explicit so
the printed statement is itself fail-closed.

## Preserved review findings

The review independently confirmed final rim rows 30–39 terminated by line 58,
nine exact 20-place truncations, angle 175 as the sole mismatch, the exact
ledger-derived doubled value, and the direction of the `rho/C_flat` effect. It
did not rerun the numerical hunt, certify the ledger envelope, prove H5-RIM
flatness, or change any theorem or premise status.
