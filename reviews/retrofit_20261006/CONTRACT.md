# Retrofit evidence records — contract v0.1

**Proposed** shared format for the retrofit dispatch in
[main#275 6018658478](https://github.com/d6g8k5htny-coder/main/issues/275#issuecomment-6018658478)
(contract role accepted in [6018831775](https://github.com/d6g8k5htny-coder/main/issues/275#issuecomment-6018831775)).
It follows the closure-evidence protocol proposed in
[main#276](https://github.com/d6g8k5htny-coder/main/pull/276) and the decision record v1.1 in
[main#275](https://github.com/d6g8k5htny-coder/main/issues/275).

**Scientific effect: NONE.** A record states that an exact source object does or does not have a record on one
evidence axis. It is not a review, an acceptance, a status, a register transition or an independence claim. No
shard edits proof, review or result bytes, `GRAPH.json`, `STATUS.md`, `PROOF_INDEX.md` or any index.

## Files

Each shard writes exactly one file, `reviews/retrofit_20261006/<SHARD>/RECORDS.json`, plus an optional `NOTE.md` in
the same directory. One writer per shard directory. Shards never write here, in another shard's directory or in
shared code. `CONTRACT_EXAMPLE.json` beside this file shows the shape and is not an authoritative record.

The inventory map of dispatch row I is out of scope for v0.1. Its membership classes are not evidence states.

## Shape

```json
{
  "schema": "retrofit-records/v0.1",
  "shard": "B1_side24",
  "baseline": {"Math-": "08f86862f859ac4804b4fd6c6477a7ed0421e37f",
               "main": "cddbb7f6cf3f57f3b495277f7da148287e027b19"},
  "author": {"provider": "...", "model_or_agent": "...", "session": "... or UNKNOWN"},
  "scientific_effect": "NONE",
  "status_authority": false,
  "records": [{
    "id": "B1-001",
    "subject": {"repository": "Math-", "commit": "<40 hex>", "path": "relative/path", "blob": "<40 hex>"},
    "delta": false,
    "axis": "numerical_reproduction",
    "state": "recorded",
    "evidence": [{"kind": "file", "repository": "Math-", "commit": "<40 hex>", "path": "...", "blob": "<40 hex>"},
                 {"kind": "github_comment", "repository": "main", "ref": "6018658478"},
                 {"kind": "github_review", "repository": "Math-", "ref": "<review id>", "commit": "<40 hex>"},
                 {"kind": "workflow_run", "repository": "Math-", "ref": "<run id>", "attempt": 1, "job": null,
                  "run_head_sha": "<40 hex>", "checked_commit": null, "purpose": "check", "conclusion": "failure",
                  "expected_conclusion": "success"}],
    "performer": {"provider": "...", "model_or_agent": "...", "session": "... or UNKNOWN"},
    "exposure": "what the performer had read",
    "independence_credit": 0,
    "alias_of": null,
    "notes": ""
  }]
}
```

Every object has exactly the keys shown, and no others. In particular there is no `status`, `verdict` or
`classification` field.

| Field | Rule |
|---|---|
| `shard` | Matches its directory name (`[A-Z][A-Za-z0-9_]*`) |
| `baseline` | Exactly the pinned v0.1 cut. A later cut is a new contract version |
| `subject` | An exact object: repository, commit, path and Git blob. With `delta: false` the commit is the baseline. A candidate object sets `delta: true` and pins its own commit. When verified against a clone, the commit must be a commit object and the path must name a blob in it (not a tree or a submodule) |
| `axis` | `source_review`, `provider_distinct_review`, `blind_reconstruction`, `adversarial_attack`, `formal_evidence`, `numerical_reproduction`, `novelty`, `human_reading`, `custody`, `observable_statement` |
| `state` | `recorded` (evidence linked), `not_recorded` (checked, none found), `unknown` (not checked), `not_applicable`. Availability only; see below |
| `evidence` | Required for `recorded`, empty for `not_recorded` and `not_applicable`. One item per native object. A `file` item carries commit, path and blob. `github_comment`, `github_review` and `workflow_run` items carry the numeric GitHub id as `ref`. A `github_review` also carries its native `commit_id` as `commit`. A `github_comment` has no commit: a SHA quoted in a comment body is never a native binding. A `workflow_run` also carries `attempt` (positive integer), `job` (numeric job id as a string, or `null` for the whole run), `run_head_sha` (the run's native `head_sha`), `checked_commit` (see below, or `null`), `purpose` (`check` or `negative_control`), `conclusion` (GitHub's native value, copied as served: `success`, `failure`, `cancelled`, `skipped`, `timed_out`, `neutral`, `action_required`, `stale` or `startup_failure`) and `expected_conclusion` (`success` or `failure`) |
| `performer` | Who produced the evidence, not who wrote the record. `UNKNOWN` where unknown; never `Human` or Dylan's name for an AI executor. This is the writer's obligation and a reviewer's check: the validator enforces the shape only and cannot tell whether an attribution is true |
| `exposure` | What that performer had read. Required |
| `independence_credit` | Always the integer `0`. Organizational independence is not established by these records |
| `alias_of` | `null`, or the `id` of a canonical record in the same file (one whose own `alias_of` is `null`) when this record restates exactly that record's evidence, for example for a byte alias of its subject. The alias has the same axis, the same state and the same evidence items (in any order). There are no chains, so there are no cycles. A copy of a verdict posted as a separate native object is its own evidence item in its own record, with the original named in `notes`. Aliases are counted separately and never as additional evidence. Aliasing is within one file; the aggregate does not deduplicate across shards |

Quoted verdict words may appear inside `notes` as quotations. They never become a field value.

### State is availability, not outcome

`recorded` means linked evidence exists. It does not mean the referenced event succeeded or that it supports the
subject. A failed run, a review that asks for changes, an integration intention and a landing receipt are each
`recorded` as their own evidence items; none of them is collapsed into another or into a pass. A negative control
that fails as intended is recorded with `purpose: negative_control`, `conclusion: failure` and
`expected_conclusion: failure`, so it is not mistaken for a failed check. A later event never relabels an earlier
one: a later successful run is a new item and the earlier failure stays as served.

### Run head is not the checked commit

`run_head_sha` is the run's native `head_sha`. For a `pull_request` run that is the pull request's head, while the
default checkout is the merge ref (`refs/pull/<n>/merge`), a different commit; an explicit checkout can differ again.
`checked_commit` is the commit the job actually checked out, taken only from that run's own evidence (its checkout
step or a receipt it produced), and that evidence is recorded as its own item in the same record. When the checkout was
not inspected, `checked_commit` is `null`; it is never copied from `run_head_sha`. For example, Math- run
`37412915949` (`pull_request`) has `run_head_sha` `89170cf0…` and checked the merge commit `3e56e964…`, whose parents
are the base `532bc63f…` and that head.

## Validation

```sh
python3 -B -S tools/retrofit_record_check.py --repo <Math- clone> [--main-repo <main clone>] reviews/retrofit_20261006/<SHARD>/RECORDS.json
python3 -B -S tools/retrofit_record_check.py --aggregate --repo <Math- clone> reviews/retrofit_20261006/*/RECORDS.json
```

The checker rejects:
- duplicate JSON keys and `NaN` or `Infinity`;
- unknown or missing keys, unknown axes or states, and status words used as a state;
- a non-baseline commit without `delta: true`;
- a `subject` or `file` blob that differs from Git (with `--repo` or `--main-repo`);
- a `recorded` state without evidence;
- a `github_review` without its native 40-hex `commit`, or a `github_comment` that carries a commit;
- a `workflow_run` without the full binding (attempt, job, run head, checked commit or `null`, purpose, native
  conclusion, expected conclusion), or with a value outside those enums;
- non-zero or Boolean independence credit;
- an `alias_of` that dangles, names itself or another alias, or differs from its canonical record in axis, state or
  evidence;
- a commit that is not a commit object, or a path that is not a blob, when verified against a clone;
- the same input file twice (under any spelling) and two inputs that declare the same shard.

A malformed value of any JSON type is reported as a violation of its file; the remaining files are still read.

`--aggregate` prints, per exact subject (full repository, commit, path and blob) and axis, the states recorded by
each shard, with aliases counted separately. `evidence_items_non_alias` counts evidence items as listed;
`distinct_evidence_items` counts identical items once across all inputs. Neither is a count of independent evidence
or of coverage of any inventory. It writes nothing. A later, separately reviewed change may join landed records onto the downstream-gate
graph view (Math-#381). That join is not part of v0.1.

## Not in v0.1

- No scientific status, acceptance or promotion field.
- No shared manifest or index.
- No schema for the inventory map.
- No automatic import into GRAPH, STATUS or PROOF_INDEX.
- No selection of a run as a success. A later consumer may use a `workflow_run` item for a claim only when its
  `checked_commit` is not `null` and, with its `job` and `purpose`, binds to that claim, and its `conclusion` equals
  its `expected_conclusion`. Run success or a matching pull-request head never establishes coverage of a base.

Changes to this contract take a new version and their own nonauthor review. Records written under v0.1 stay valid
under v0.1.
