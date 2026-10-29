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
- Three observation passes on 2026-10-29: 17:17Z (`main` `8151f592`, 26 PRs, 110 branches),
  17:34Z (28 PRs, 112 branches) and **23:05Z (`main` `9f8dbb4d`, 29 PRs, 153 branches)** — the
  committed files describe the last one; `meta.observed_at_utc` / `meta.main_sha` say so in each
  file. Git refs are fetched with `--prune`; the git ref list is the authority (the REST `branches`
  listing had paginated to a wrong count earlier, as CBZ-MATH-198 also found).
- `fetched/CONTEXT.json` records the cut (clock, `main` sha, the full `refs/remotes/origin/*`
  snapshot) and `FETCHED_MANIFEST.json` binds every raw GitHub response by SHA-256 and size. The
  bodies (≈ 8 MB) are not committed; the performer retains them and republishes on request. The
  generator replays from them with `--offline`, reusing the recorded clock and refs, and the replay
  was checked byte-identical to the live run (only `meta.replay` differs: `live` vs
  `offline from CONTEXT.json`).

## Results

| Recommended disposition | PRs |
|---|---:|
| `ACTIVE-OWNER-LANE` (updated within 24 h of observation; their lane's call) | 14 |
| `STACK-DEPENDENT` (base is another branch) | 6 |
| `QUARANTINE-ARCHIVE` (stale; latest verdict not PASS, or a hold) | 5 |
| `INTEGRATE-CANDIDATE` (base `main`, merge-tree clean, required check green, latest verdict PASS/PASS_SCOPED) | 4 |
| **Total open PRs** | **29** |

| Branch class | Branches |
|---|---:|
| `OPEN_PR_REF` (head or base of an open PR) | 31 |
| `UNMERGED_NO_PR` (work not on `main`, no pull request) | 121 |
| `MERGED_NO_PR_PRUNE_ELIGIBLE` | 0 |
| `PROTECTED` (`main`) | 1 |

So Math- has **no prune-eligible merged branch**; its Phase 2 work is the open PRs and the
PR-less branches. Between the first and the third pass the federation itself moved: Root's and
other Codex lanes created 40 `cbz/*` and `codex/cbz-*` working branches, which the third pass
classifies `ACTIVE-LANE` / `OPEN_PR_REF` rather than disposing of them. Every record carries `recreate_command` / `recoverable_ref_command`
(`git push origin <tip>:refs/heads/<name>`), so any later archive or prune is recoverable from
these files alone.

### The 121 unmerged, PR-less branches (`UNMERGED_BRANCHES.md`, `unmerged_branches.json`; third pass, 23:05Z)

| Recommended disposition | Branches |
|---|---:|
| `ARCHIVE-BUNDLE` (distinct work, no PR, stale or conflicting or signalled: bundle + delete, recreate command recorded) | 76 |
| `ACTIVE-LANE` (touched within 24 h — today's `cbz/*` consolidation branches) | 30 |
| `SUPERSEDED-BY-OPEN-PR` (tip is an ancestor of an open PR head — rides that PR) | 11 |
| `INTEGRATE-REVIEW` (clean, signal-free, ≤ 50 paths, touched within 14 days) | 2 |
| `SUPERSEDED-CONTENT-ON-MAIN` (every changed tree entry already equals `main`'s) | 2 |

Facts behind the 76 `ARCHIVE-BUNDLE` rows (unchanged across the passes): **24 have unrelated
history** (no merge-base with `main`; most are September `chatgpt/` and `cursor/` review or custody
branches); **41 conflict** with `main` in `merge-tree`; 13 carry lexical signals; the rest are stale.
Rows flagged `integrable_if_wanted` (clean merge-tree, zero signals, ≤ 50 paths, related history) can
still get a PR from a lane that wants them; otherwise they are archived like the rest.

Integrate candidates at observation: #372, #482, #487, #490, #492 (see `DISPOSITIONS.md` for the
verdict comment each rests on). #482 and #487 carry lexical Layer A signals (`admit` additions in
`.lean`; one skip; one float indicator in a check path); `READINGS.md` records the manual reading of
every flagged line in every open PR — all are prose, version strings, a comment, an environment
guard or a subprocess timeout, so none is a Layer A hazard.

## Files

- `DISPOSITIONS.md`, `dispositions.json` — one record per open PR: head/base/stack position,
  ancestor and blob-equality tests against `main`, `merge-tree` onto `main` (and onto the base for
  stacked PRs), commits ahead/behind, changed paths (first 200; the full sorted list is bound by
  `changed_paths_sha256`), lexical Layer A signals, latest verdict token with its comment id, review
  states, check-run conclusions, explicit do-not-merge flag, recency, recommended disposition.
- `BRANCHES.md`, `branches.json` — one record per branch: tip, last commit date, ancestor-of-`main`,
  open-PR membership, commits ahead of `main`, class, recreate command.
- `UNMERGED_BRANCHES.md`, `unmerged_branches.json` — for each unmerged PR-less branch: merge-base
  (or unrelated history), commits ahead, changed paths (first 200 + SHA-256 of the full list),
  changed directories, how many changed blobs already equal `main`'s, lexical signals, merge-tree
  cleanliness, containment in an open PR head, lane prefix, days since last commit, recommendation
  (`disposition_lib.recommend_branch`) and the `integrable_if_wanted` flag.
- `generate.py` — the generator (stdlib + git + `gh` REST). `disposition_lib.py` — the pure
  classification logic. `test_disposition_lib.py`, `test_generate.py` — 60 tests, run in both modes.
- `FETCHED_MANIFEST.json` — SHA-256/size of every raw GitHub response used (including
  `CONTEXT.json`, the recorded cut).
- `READINGS.md` — the manual reading of each flagged line (what the lexical signal actually is).

## Reproduce

```sh
cd <Math- clone>
git fetch origin '+refs/heads/*:refs/remotes/origin/*' --prune
cd cbz/evidence/math-pr-dispositions
python3 -W error -m unittest test_disposition_lib test_generate   # 60 tests
python3 -O -m unittest test_disposition_lib test_generate
python3 generate.py --repo <Math- clone> --out .                  # live refetch (writes fetched/)
python3 generate.py --repo <Math- clone> --out . --offline fetched # replay of the recorded cut
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
- **The branch table is also fixed and documented** (`disposition_lib.recommend_branch`):
  SUPERSEDED-BY-OPEN-PR when the tip is inside an open PR head; else ARCHIVE-BUNDLE for unrelated
  history; else SUPERSEDED-CONTENT-ON-MAIN when every changed blob equals `main`'s; else ACTIVE-LANE
  within 24 h; else INTEGRATE-REVIEW only for a clean, signal-free, ≤ 50-path branch touched within
  14 days; else ARCHIVE-BUNDLE. `integrable_if_wanted` repeats the INTEGRATE-REVIEW conditions
  without the age bound.
- **Supersession compares tree entries, not blob ids alone.** Changed paths are listed NUL-delimited
  with rename detection off (a rename is its deletion plus its addition; non-ASCII names are literal),
  and each path's `(mode, object id)` on the head must equal `main`'s, so a chmod-only change, a
  rename whose source survives on `main`, or a file `main` lacks is never "already on main" (four
  Codex findings on #529, each with a regression test).
- Check-run conclusions are those recorded at the PR head at observation time, not fresh runs
  (B-005): an integrator re-runs on the current base before merging.
