# Honest failed-history notes

All failed production versions are retained as numbered `.source.lean` snapshots
with raw logs and actual-exit JSON receipts. No helper source or historical receipt
was edited. `helper-lineage.json` records exact inputs reused by assembly.

The initial runner saved the production source for every command, including support
commands. Therefore the two failed Controls support inputs were not at-execution
snapshots. They have been reconstructed exactly by reversing the recorded edits and
are explicitly named `input-reconstructed`. Their raw error logs remain original.
The final Controls and audit source remain unchanged, and their observed-after hashes
are recorded separately. No reconstructed source is described as an original snapshot.

One exploratory `/home/agent/.elan/bin/leanchecker --help` invocation was terminated
because that executable treated the argument as input and began doing work rather
than printing help. It produced no successful check and is not verification evidence.
Only the later named `lake env leanchecker SourceMorseIncidence` invocation is claimed
as the successful kernel replay (`kernel-10.json`).

Author-side qualification is separate from different-provider scientific alignment
review and publication. No pending review invalidates the completed Lean evidence.
