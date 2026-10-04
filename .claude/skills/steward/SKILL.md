---
name: steward
description: Math- conventions for driving a pull request to a mergeable state. Covers frozen heads while a nonauthor read is open, AMEND timing and readbacks, the packet and Lean gates, stacked-base reconciliation, merge commits only, and integration by a non-author lane. Read before acting on CI, review or merge-state events on a Math- PR that you opened or drive for its author.
---

# Steward: driving a Math- pull request

This skill summarizes rules that already bind this repository. It adds none. On any conflict, these sources win:
- [`AGENTS.md`](../../../AGENTS.md);
- `main` [`AGENTS.md`](https://github.com/d6g8k5htny-coder/main/blob/main/AGENTS.md);
- the [current workflow](https://github.com/d6g8k5htny-coder/main/blob/main/governance/OP-WORKFLOW-20260930.md);
- the [privacy rule](https://github.com/d6g8k5htny-coder/main/blob/main/governance/OP-PRIVACY-20260927.md);
- [`docs/FORMAL_REQUIRED_CHECKS.md`](../../../docs/FORMAL_REQUIRED_CHECKS.md).

Cross-lane coordination (claims, ledgers, routing, releases) happens in [main#229](https://github.com/d6g8k5htny-coder/main/issues/229).

## 1. Identity, roles and credit

- **One GitHub account carries every lane.** Name the actual performer (provider, agent or session) in every comment and record. The owner-facing attribution is "Dylan Roy — delegated AI work" (or "— delegated AI review"), followed immediately by the actual performer.
- **The author never approves or merges its own PR.** Integration is done by a non-author lane. The named integration owner controls branch refresh, readiness changes and the merge.
- **Independence credit.**
  - A same-provider read is useful technical work but earns zero organizational-independence credit. A Claude read does not count as the nonauthor read of a Claude-authored packet.
  - Grok Bot agent reads count (owner ruling of 2026-10-03, main#229 comment 5974405061). The agreed performer line is "Grok Bot agent N (Grok Bot support agent; non-Claude, nonauthor lane)".
- **xAI/Grok and Cursor agents work here only as support**, at a lane's request ([`AGENTS.md`](../../../AGENTS.md)). Never restart stopped agents, timers or loops ([`OWNER_STOP.md`](../../../OWNER_STOP.md)). Cite only what such agents have published.
- **Never ask Dylan to re-approve autonomy he has already granted.**

## 2. The PR body is the disposition

Keep one short current disposition in the PR body:
- the current head and the owner;
- completed review scopes, each linked to its verdict;
- unresolved finding IDs ("none" when none are open);
- validation;
- the next action.

Update it on every material change. Link evidence rather than copying it. A closed issue or an outdated thread does not discharge an open obligation.

## 3. Reads, verdicts and AMENDs

1. **A read starts with a pickup comment** that names the PR, the slice and the exact head SHA.
2. **While a read is open, the head is frozen.** Push nothing to it, not even an optional nit, because that would stale the read.
3. **The verdict is PASS, AMEND (with the exact change) or BLOCK (with the reason)**, followed by the scope actually checked and what was not checked.
4. **Apply an AMEND only after its verdict is posted.** Then:
   - push one commit that does exactly what the AMEND says;
   - reply on the PR, naming the commit;
   - request a byte-diff readback of `old-head..new-head`.

   A readback checks the delta, not the whole packet again.
5. **Optional and non-blocking points never start a push on their own.**
   - Reply once (stays as is and why, or rides a later push).
   - Carry the plainly correct ones into the next push that changes those files for another reason, or into a stacked successor PR. The reviewed head then stays the one the reads hashed.
6. **Changed reviewed bytes, dependencies or scope invalidate the affected review.** A base-only merge does not. It needs a bounded comparison (the packet bytes are identical to the reviewed head) plus fresh integration checks.

## 4. Checks

**Required.** `math-downstream-gates` is the required aggregate. It depends on `downstream-replay` and `formal / formal-evidence` succeeding at the tested commit. Packet workflows add their own jobs, for example `certify-and-reject-mutants` for coefficient packets and `kernel-evidence` for the Lean cap packet. A missing, skipped, neutral or cancelled result is not success. Old receipts are never rebound to a new commit.

**Packet checkers (Python standard library only).**
- Run `python3 -B -S <checker>.py` and `python3 -B -O -S <checker>.py`. Their output must be byte-identical to each other and to the packet's `RESULTS.json`.
- Every mutant must be rejected, strictly: exit code 1 and `"passed": false`.
- `SOURCE_FILES.json` records bytes, SHA-256 and git blob. Workflows check its `pins_on_main` against `main`. If `main` changes a pinned file, re-pin and refresh the record as an ordinary reviewed change. Never weaken the check.

**Lean packets** (`frontiers/cap_first_exit_lean_20261002/`, and `formal/` under its own contract):
- `python3 -B -S gate.py` in source mode;
- `python3 -B -S -m unittest test_gate` and the same with `-O`;
- `python3 gate.py --execute` with the pinned toolchain (`lake` on `PATH`). It builds fresh, replays with `leanchecker`, audits axioms (only `propext`, `Classical.choice` and `Quot.sound` are allowed) and runs three negative controls. All three must be REJECTED.

After any change to a packet file, regenerate `MANIFEST.json` and run the source gate again. A kernel-checked build is engineering evidence. It is not an alignment review and not scientific acceptance.

**Red CI on your PR is work now.**
- Reproduce the failure, root-cause it, fix it in scope, validate locally and push.
- "Flake" is not a root cause. Re-run at most once, and only when the job died before any test body ran.
- Never skip, disable or quarantine a test. Never push an empty commit. Never close and reopen a PR to restart CI.
- Some replays are long; the SIDE24 `d = 6` certificate replay takes about 25–45 minutes. Wait for it rather than re-running.

## 5. Branches and pushes

- **Merge commits only.** No rebase, no amend, and no force-push on a reviewed or shared branch.
- **Change another owner's branch only after an explicit scoped handoff, a release, or a confirmed lease expiry**, followed by a check of its current state.
- **Verify the remote head after every push** with `git ls-remote origin <branch>`.
- **Stacked PRs.** When the lower PR merges:
  1. merge `main` into the next branch with a merge commit;
  2. verify that the packet bytes equal the reviewed head (by diff over the packet directory and its workflow);
  3. run the gates again and push;
  4. post one comment stating the byte-identity, so the earlier review carries forward;
  5. retarget the PR to `main` if GitHub has not done so already.

## 6. Integration (for the integrator, never the author)

Immediately before merging, read again:
- the current head and base;
- the complete diff;
- the latest reviews and unresolved threads;
- ownership claims;
- the required checks at the exact head.

Merge with `expected_head_sha` and a merge commit. If the branch is behind, use a merge-commit update. Confirm that the packet bytes are unchanged, and merge only on a fresh green run. Do not bypass protection or simulate another identity's approval. Record an unexpected merge honestly.

## 7. Never in a packet PR

- Edit `STATUS`, `PROOF_INDEX`, `GRAPH`, catalog or register surfaces, or create another status register.
- Flip `lemma_closed`, prize or premise flags. Packet PRs have scientific effect NONE.
- Publish private or personal material. Dylan's name and Gmail address are allowed by the privacy rule; nothing else personal is.
- Approve, merge or resolve a thread on another lane's behalf.

## 8. Comments and records

- **Check the latest comments before writing.** Be frugal: one comment per round, at the point where it resolves something, raises a real blocker or asks a question.
- **Answer each review thread where it was raised.** Resolve the threads you addressed.
- **Claims name the exact scope and paths**, carry a lease, and are released when the work finishes.
- **End agent-authored comments with the attribution footer your harness requires.**
