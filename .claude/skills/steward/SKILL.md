---
name: steward
description: Math- conventions for driving a pull request to a mergeable state. Covers frozen heads while a nonauthor read is open, AMEND timing and readbacks, the packet and Lean gates, stacked-base reconciliation, merge commits only, and integration by a non-author lane. Read before acting on CI, review or merge-state events on a Math- PR that you opened or drive for its author.
---

# Steward: driving a Math- pull request

This skill summarizes rules that bind this repository and records current lane practice from main#229 (for example main#229 5974405061: "The heads stay frozen while a read is open. I apply AMENDs only after the verdict is posted"). A statement tied to a source below restates that source. A statement marked *(practice)* records lane practice only and adds no rule. On any conflict, the sources win.

It was written against these exact source identities (repository, commit, path, git blob):

| Source | Repository @ commit | Path | Git blob |
|---|---|---|---|
| Agent entry | Math- @ `61a67b5dffb5b0b7abe6f14bc96116c54b60ec0c` | [`AGENTS.md`](https://github.com/d6g8k5htny-coder/Math-/blob/61a67b5dffb5b0b7abe6f14bc96116c54b60ec0c/AGENTS.md) | `ca2f0fa247f7052c702de9b4f8e595226468c622` |
| Owner stop (historical) | Math- @ `61a67b5` | [`OWNER_STOP.md`](https://github.com/d6g8k5htny-coder/Math-/blob/61a67b5dffb5b0b7abe6f14bc96116c54b60ec0c/OWNER_STOP.md) | `234a579b64140068d28bb7081ce3c2fa9d5e5417` |
| Required-check contract | Math- @ `61a67b5` | [`docs/FORMAL_REQUIRED_CHECKS.md`](https://github.com/d6g8k5htny-coder/Math-/blob/61a67b5dffb5b0b7abe6f14bc96116c54b60ec0c/docs/FORMAL_REQUIRED_CHECKS.md) | `d4440638bc58134e4f1c941bad62203cba8eb37f` |
| Agent entry | main @ `9093629769f40db76f1311d8ee920d5a82a38b89` | [`AGENTS.md`](https://github.com/d6g8k5htny-coder/main/blob/9093629769f40db76f1311d8ee920d5a82a38b89/AGENTS.md) | `f649d88a8ecd9c6501d3137b5b330985e9c1f701` |
| Current workflow | main @ `9093629` | [`governance/OP-WORKFLOW-20260930.md`](https://github.com/d6g8k5htny-coder/main/blob/9093629769f40db76f1311d8ee920d5a82a38b89/governance/OP-WORKFLOW-20260930.md) | `1fdf548377769d3723a43dfb7f441175d930810d` |
| Privacy rule | main @ `9093629` | [`governance/OP-PRIVACY-20260927.md`](https://github.com/d6g8k5htny-coder/main/blob/9093629769f40db76f1311d8ee920d5a82a38b89/governance/OP-PRIVACY-20260927.md) | `dd7eca9ff36b19b07338d5ed0a6f1133d2075a81` |

**Check the live versions too.** They are [Math- `AGENTS.md`](../../../AGENTS.md), [`docs/FORMAL_REQUIRED_CHECKS.md`](../../../docs/FORMAL_REQUIRED_CHECKS.md) and `main`'s [`governance/`](https://github.com/d6g8k5htny-coder/main/tree/main/governance). If a source's blob has changed, the current source governs, and this summary needs a successor revision.

Cross-lane coordination (claims, ledgers, routing, releases) happens in [main#229](https://github.com/d6g8k5htny-coder/main/issues/229).

## 1. Identity, roles and credit

- **One GitHub account carries every lane.** Name the actual performer (provider, agent or session) in every comment and record. The owner-facing attribution for review is "Dylan Roy — delegated AI review", followed immediately by the actual performer, provider, agent and reviewed scope (OP-WORKFLOW-20260930, "Delegated owner review"). Lanes also write "Dylan Roy — delegated AI work" for non-review work *(practice)*.
- **The named integration owner controls branch refresh, readiness changes and the merge** (OP-WORKFLOW-20260930). An author replay is not a nonauthor review (OP-WORKFLOW-20260930), and a self-review does not erase an unresolved AMEND (`docs/FORMAL_REQUIRED_CHECKS.md`). *(practice)* The author does not approve or merge its own PR, and a non-author lane integrates (for example main#229 5974405061: "No merge by this lane").
- **Independence credit.**
  - A same-provider read is useful technical work but earns zero organizational-independence credit, and an author replay is not a nonauthor review ([OP-WORKFLOW-20260930](https://github.com/d6g8k5htny-coder/main/blob/9093629769f40db76f1311d8ee920d5a82a38b89/governance/OP-WORKFLOW-20260930.md), "Match verification to the change").
  - Owner statement recorded by Anthropic Claude session `017Mi3hx…` in main#229 comment 5974405061 (Dylan Roy, 2026-10-03, about 23:01Z): "Grok bots can count as a review". That comment applies it to that session's packets: a Grok Bot agent's read counts as a nonauthor, non-Claude review for integration readiness when it is posted in the target PR thread with an explicit pickup that names the head, a PASS / AMEND / BLOCK verdict, and the scope actually checked. The record names the actual performer as `Grok Bot agent N (Grok Bot support agent; non-Claude, nonauthor lane)`. Same-account organizational-independence credit stays 0. Claude reads of that session's packets still do not count.
- **xAI/Grok (including Cursor) agents work here only as support** for the non-Grok lanes, at those lanes' request ([`AGENTS.md`](../../../AGENTS.md)). No self-assigned repository changes, no takeover of another lane, and no restarted timers or loops ([`AGENTS.md`](../../../AGENTS.md); `main` [`AGENTS.md`](https://github.com/d6g8k5htny-coder/main/blob/9093629769f40db76f1311d8ee920d5a82a38b89/AGENTS.md)). The 2026-09-27 stop in [`OWNER_STOP.md`](../../../OWNER_STOP.md) is historical and lifted. Cite only what such agents have published.
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

1. **A read starts with a pickup comment** *(practice)* that names the PR, the slice and the exact head SHA.
2. **While a read is open, the head is frozen.** *(practice)* Push nothing to it, not even an optional nit, because that would stale the read.
3. **The verdict is PASS, AMEND (with the exact change) or BLOCK (with the reason)** *(practice)*, followed by the scope actually checked and what was not checked.
4. **Apply an AMEND only after its verdict is posted.** *(practice)* Then:
   - push one commit that does exactly what the AMEND says;
   - reply on the PR, naming the commit;
   - request a byte-diff readback of `old-head..new-head`.

   A readback checks the delta, not the whole packet again.
5. **Optional and non-blocking points never start a push on their own.** *(practice)*
   - Reply once (stays as is and why, or rides a later push).
   - Carry the plainly correct ones into the next push that changes those files for another reason, or into a stacked successor PR. The reviewed head then stays the one the reads hashed.
6. **Changed reviewed bytes, dependencies or scope invalidate the affected review.** A base-only merge carries a review forward only if a bounded comparison shows that the reviewed slice is unchanged. That slice covers:
   - the packet bytes;
   - every reviewed dependency (the imported or pinned sources it consumes, and its workflow).

   Fresh integration checks are also needed. If the base changed any reviewed dependency, the affected review needs a successor disposition, even when the packet directory is byte-identical.

## 4. Checks

**Required.** `math-downstream-gates` is the required aggregate. It depends on `downstream-replay` and `formal / formal-evidence` succeeding at the tested commit. Packet workflows add their own jobs, for example `certify-and-reject-mutants` for coefficient packets and `kernel-evidence` for the Lean cap packet. A missing, skipped, neutral or cancelled result is not success. Old receipts are never rebound to a new commit.

**Packet checkers (Python standard library only).**
- Run each checker exactly as its packet's workflow does. Many coefficient packets run `python3 -B -S <checker>.py` and `python3 -B -O -S <checker>.py` and require output byte-identical to each other and to the packet's `RESULTS.json` (for example `.github/workflows/c8-window-coefficient-planar.yml`); others use their own mode (for example `certificate.py --check` in `.github/workflows/c2-exact.yml`).
- Every mutant must be rejected exactly as that packet's workflow specifies (for example exit code 1 in `.github/workflows/c2-exact.yml` and `.github/workflows/c8-window-coefficient-planar.yml`). If a packet's workflow also requires a JSON `"passed": false`, require it there only; do not add a JSON requirement to a packet whose contract lacks one.
- Where a packet has `SOURCE_FILES.json` (bytes, SHA-256 and git blob), its workflow checks `pins_on_main` against `main` (for example `c6-tail-constant-certified.yml`, `c8-window-coefficient-planar.yml`). Other packets keep their own source records; follow the packet's workflow. If `main` changes a pinned file, re-pin and refresh the record as an ordinary reviewed change. Never weaken the check.

**Lean packets.** Each has its own recipe; use the one in its README and workflow.
- **The cap packet, `frontiers/cap_first_exit_lean_20261002/`**, run from that directory:
  - `python3 -B -S gate.py` in source mode;
  - `python3 -B -S -m unittest test_gate` and the same with `-O`;
  - `python3 gate.py --execute` with the pinned toolchain (`lake` on `PATH`). It builds fresh, replays with `leanchecker`, audits axioms (only `propext`, `Classical.choice` and `Quot.sound` are allowed) and runs three negative controls. All three must be REJECTED.
- **`formal/`**, run from the repository root, as in [`formal/README.md`](../../../formal/README.md) and `.github/workflows/formal-lean.yml`:
  - `python3 -m unittest discover -s formal/tests -v`, and the same with `-O`;
  - `python3 formal/gate.py` (source only, no Lean);
  - `python3 formal/gate.py --execute` after `lake exe cache get` in `formal/`. It fails unless the pinned project builds, `leanchecker` rechecks the package, all 13 declarations have axiom reports restricted to `propext`, `Classical.choice` and `Quot.sound`, and five executable negative controls are rejected.

After any change to a packet file, update that package's manifest (`MANIFEST.json` for the cap packet, `formal/manifest.json` for `formal/`) as its gate requires and run the source gate again. A kernel-checked build is engineering evidence. It is not an alignment review and not scientific acceptance.

**Red CI on your PR is work now.**
- Reproduce the failure, root-cause it, fix it in scope, validate locally and push.
- **If a nonauthor read is open when CI turns red, the head stays frozen** (§3.2; main#229 5974405061: "The heads stay frozen while a read is open"). Post one comment on the PR naming the failing check, its root cause and the planned fix. Push the fix after the verdict is posted, or earlier only if the reader releases the pickup or agrees on the PR to re-point to the new head *(practice)*. A red head cannot merge in the meantime, so the freeze costs time, not correctness.
- "Flake" is not a root cause. *(practice)* Re-run at most once, and only when the job died before any test body ran.
- Never skip, disable or quarantine a test. *(practice)* Never push an empty commit. Never close and reopen a PR to restart CI.
- Some certificate replays are long (tens of minutes). Check the job's earlier durations before treating it as stuck, and do not re-run a job that is still running.

## 5. Branches and pushes

- **Merge commits only.** *(practice)* No rebase, no amend, and no force-push on a reviewed or shared branch.
- **Change another owner's branch only after an explicit scoped handoff, a release, or a confirmed lease expiry**, followed by a check of its current state.
- **Verify the remote head after every push** *(practice)* with `git ls-remote origin <branch>`.
- **Stacked PRs.** *(practice)* When the lower PR merges:
  1. merge `main` into the next branch with a merge commit;
  2. verify by diff that the reviewed slice equals the reviewed head: the packet directory, its workflow, and every pinned or imported dependency it consumes (§3.6);
  3. run the gates again and push;
  4. post one comment stating the byte-identity, so the earlier review carries forward;
  5. retarget the PR to `main` if GitHub has not done so already.

## 6. Integration (for the integrator, never the author)

Immediately before merging, read again:
- the current head and base;
- the complete diff;
- the latest reviews and unresolved threads;
- ownership claims;
- the required checks for the current head/base pair. On pull requests they run against the tested synthetic merge commit (`docs/FORMAL_REQUIRED_CHECKS.md`), so a base change needs a fresh run. A result from an earlier head or base is not rebound.

Merge with `expected_head_sha` and a merge commit *(practice)*. If the branch is behind, update it with a merge commit under a supported expected-old-ref guard, and do not force past a mismatch. If another refresh already produced the same reviewed tree, compare its actual parents and affected source identities and adopt it rather than publishing a duplicate refresh (OP-WORKFLOW-20260930, "Integrate once the evidence is ready"). Confirm that the packet bytes are unchanged, and merge only on a fresh green run. Unresolved engineering AMENDs survive peer merges. Do not bypass protection or simulate another identity's approval. Record an unexpected merge honestly.

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
