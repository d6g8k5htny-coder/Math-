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
                 {"kind": "github_comment", "repository": "main", "ref": "6018658478"}],
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
| `subject` | An exact object: repository, commit, path and Git blob. With `delta: false` the commit is the baseline. A candidate object sets `delta: true` and pins its own commit |
| `axis` | `source_review`, `provider_distinct_review`, `blind_reconstruction`, `adversarial_attack`, `formal_evidence`, `numerical_reproduction`, `novelty`, `human_reading`, `custody`, `observable_statement` |
| `state` | `recorded` (evidence linked), `not_recorded` (checked, none found), `unknown` (not checked), `not_applicable` |
| `evidence` | Required for `recorded`, empty for `not_recorded` and `not_applicable`. A `file` item carries commit, path and blob. `github_comment`, `github_review` and `workflow_run` items carry the numeric GitHub id as `ref` |
| `performer` | Who produced the evidence, not who wrote the record. `UNKNOWN` where unknown; never `Human` or Dylan's name for an AI executor |
| `exposure` | What that performer had read. Required |
| `independence_credit` | Always the integer `0`. Organizational independence is not established by these records |
| `alias_of` | Another record's `id` when this record restates the same evidence (for example a byte alias or a copied verdict). Aliases are counted separately and never as additional evidence |

Quoted verdict words may appear inside `notes` as quotations. They never become a field value.

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
- non-zero or Boolean independence credit;
- a dangling `alias_of`.

`--aggregate` prints, per exact subject and axis, the states recorded by each shard, with aliases counted
separately. It writes nothing. A later, separately reviewed change may join landed records onto the downstream-gate
graph view (Math-#381). That join is not part of v0.1.

## Not in v0.1

- No scientific status, acceptance or promotion field.
- No shared manifest or index.
- No schema for the inventory map.
- No automatic import into GRAPH, STATUS or PROOF_INDEX.

Changes to this contract take a new version and their own nonauthor review. Records written under v0.1 stay valid
under v0.1.
