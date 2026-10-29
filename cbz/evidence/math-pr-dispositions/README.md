# Math- open pull requests and branches — CBZ-0 Phase 2 disposition evidence

Unit `CBZ0-MATH-PR-BRANCH-DISPOSITIONS-01N-20261029`, pickup
[main#684/6503304668](https://github.com/d6g8k5htny-coder/main/issues/684#issuecomment-6503304668).
Performer: Anthropic Claude, Claude Code session `session_01NMeKEismAyeqgdB4sy2NJU` (Claude01N).
Written under `GOVERNANCE.md` B-003 (Root owns canonical files and the serial integration/cleanup
queue; this directory is delegated evidence only). Credit 0. Scientific effect NONE.

**This directory closes, merges or deletes nothing.** It records, for every open Math- pull request
and every Math- branch, the facts an integrator needs for a terminal disposition, plus a
*recommended* disposition from a fixed decision table. The integrator decides.

## Observation

- Repository `d6g8k5htny-coder/Math-`, `main` = `8151f592918a845bf19eb8eafaf8444540a32734`
  (the same cut as tag `pre-cbz-discovery-1`).
- GitHub state fetched 2026-10-29 17:17Z (pull requests, issue comments, reviews, check runs);
  git refs fetched with `--prune` at the same time: **110 branches** (the REST `branches` listing
  paginated to 149 earlier that day; the git ref list is the authority, as CBZ-MATH-198 also found).
- `FETCHED_MANIFEST.json` binds every raw GitHub response by SHA-256 and size. The bodies
  (7.2 MB) are not committed; the performer retains them and republishes on request. The
  generator replays from them with `--offline`.

## Results

| Recommended disposition | PRs |
|---|---:|
| `QUARANTINE-ARCHIVE` (stale; latest verdict not PASS, or a hold) | 9 |
| `STACK-DEPENDENT` (base is another branch) | 9 |
| `INTEGRATE-CANDIDATE` (base `main`, merge-tree clean, required check green, latest verdict PASS/PASS_SCOPED) | 5 |
| `ACTIVE-OWNER-LANE` (updated within 24 h of observation; their lane's call) | 3 |
| **Total open PRs** | **26** |

| Branch class | Branches |
|---|---:|
| `OPEN_PR_REF` (head or base of an open PR) | 28 |
| `UNMERGED_NO_PR` (work not on `main`, no pull request) | 81 |
| `MERGED_NO_PR_PRUNE_ELIGIBLE` | 0 |
| `PROTECTED` (`main`) | 1 |

So Math- has **no prune-eligible merged branch**; its Phase 2 work is the 26 PRs and the 81
PR-less branches (25 last touched in September, 56 in October; 41 are fewer than 10 commits
ahead of `main`). Every record carries `recreate_command` / `recoverable_ref_command`
(`git push origin <tip>:refs/heads/<name>`), so any later archive or prune is recoverable from
these files alone.

Integrate candidates at observation: #372, #482, #487, #490, #492 (see `DISPOSITIONS.md` for the
verdict comment each rests on). #482 and #487 carry lexical Layer A signals (`admit` additions in
`.lean`; one skip; one float indicator in a check path) — a reader must look before integration.

## Files

- `DISPOSITIONS.md`, `dispositions.json` — one record per open PR: head/base/stack position,
  ancestor and blob-equality tests against `main`, `merge-tree` onto `main` (and onto the base for
  stacked PRs), commits ahead/behind, changed paths (first 200; the full sorted list is bound by
  `changed_paths_sha256`), lexical Layer A signals, latest verdict token with its comment id, review
  states, check-run conclusions, explicit do-not-merge flag, recency, recommended disposition.
- `BRANCHES.md`, `branches.json` — one record per branch: tip, last commit date, ancestor-of-`main`,
  open-PR membership, commits ahead of `main`, class, recreate command.
- `generate.py` — the generator (stdlib + git + `gh` REST). `disposition_lib.py` — the pure
  classification logic. `test_disposition_lib.py`, `test_generate.py` — 27 tests, run in both modes.
- `FETCHED_MANIFEST.json` — SHA-256/size of every raw GitHub response used.

## Reproduce

```sh
cd <Math- clone>
git fetch origin '+refs/heads/*:refs/remotes/origin/*' --prune
cd cbz/evidence/math-pr-dispositions
python3 -W error -m unittest test_disposition_lib test_generate   # 27 tests
python3 -O -m unittest test_disposition_lib test_generate
python3 generate.py --repo <Math- clone> --out .                  # live refetch (writes fetched/)
python3 generate.py --repo <Math- clone> --out . --offline fetched # replay
```

A live run observes the federation at a later time and will differ wherever PRs moved; the
`observed_at_utc` and `main_sha` fields in `meta` say which cut a file describes.

## Limits, stated plainly

- **Layer A signals are lexical.** `layer_a_signals` counts added lines in `.lean` files containing
  `sorry`, `admit`, `axiom` or `native_decide`, deleted `def test_` lines and deleted test files,
  added `unittest`/`pytest` skips, and float indicators added in check/certificate-named Python
  paths. A hit says "look here"; zero hits certify nothing (B-006). The mutation-tested scanner of
  Math-#527 is the G0/G1 candidate, not this.
- **Verdict tokens are lexical.** The latest comment containing `PASS_SCOPED`/`PASS`/`AMEND`/
  `BLOCK`/`HOLD`/`REJECTED`/"do not merge" is reported with its id; a reader confirms the context.
  `DO_NOT_MERGE` in a PR body counts only when not aimed at another branch ("do not merge into X" is
  a scope note).
- **The decision table is fixed and documented** (`disposition_lib.recommend`): SUPERSEDED when the
  head is an ancestor of `main` or every changed blob already equals `main`'s; else STACK-DEPENDENT
  when the base is not `main`; else ACTIVE-OWNER-LANE when updated within 24 h; else
  QUARANTINE-ARCHIVE on an explicit hold; else INTEGRATE-CANDIDATE only with a clean merge-tree, a
  green `math-downstream-gates` at the head and a PASS-class latest verdict; else QUARANTINE-ARCHIVE.
  It encodes no judgement about the mathematics.
- Check-run conclusions are those recorded at the PR head at observation time, not fresh runs
  (B-005): an integrator re-runs on the current base before merging.
