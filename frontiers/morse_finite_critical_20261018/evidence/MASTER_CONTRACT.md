# C293 final master artifact contract

`final_master.py` is an engineering artifact verifier. It consumes completed local build/kernel/audit/negative-control evidence and remote/custody readbacks. It does not run Lean, leanchecker, a network request, or a mathematical proof. Its only child process is the established canonical delivery builder's read-only `verify` operation. Author implementation of this verifier is not another nonauthor mathematical review.

The script is deliberately not executed during authoring. It may be invoked once only after every record below exists and is final. It exclusively creates `FINAL_MASTER_START.json` and `FINAL_MASTER.json`. The start marker is created with exclusive creation before verification. Any later caught exception, including an interrupt, creates a `HOLD_ARTIFACT_VERIFICATION` result containing the error and checks so far. A second invocation refuses without modifying previous evidence. Successful status is `PASS_ARTIFACT_VERIFICATION_NOT_THEOREM_PROOF`, with `scientific_effect: NONE`.

## Exact local evidence

- `FINAL_SOURCE_INVENTORY.json` must retain SHA-256 `f1a429935146b4e406e9ba8cc9ff8b84f7d40c22cc4fea74920dfc013c4911de`. It identifies exactly `Lifetime`, `TorusTopology`, `MorseFiniteCritical`, `MorseFiniteControls`, and `MorseFiniteAxiomAudit`. Each named `.lean` must match the inventory's bytes and hash in both `project/` and `final-project/`; the latter contains exactly these five files.
- `SOURCE_INPUTS.json` retains its actual two-row schema. It binds the two immutable dependency sources, `Lifetime.lean` and `TorusTopology.lean`, using `project_path`, `bytes`, `sha256`, `blob`, and `verified_blob`. Five final sources does not mean five immutable upstream input rows. The three new sources are bound by the exact final inventory, successful receipts, and later publication Git blobs.
- `FINAL_DEPENDENCY_ARTIFACTS.json` and `run_final_phase.py` match the hashes already fixed by the final inventory. The master checks receipt dependency census cardinalities and the recorded inventory binding; it does not freshly rehash the shared dependency cache. The execution wrapper's explicit C291-byte-hash/metadata-reuse qualification remains in force.
- `FINAL_SEQUENCE_START.json` and `FINAL_SEQUENCE_RESULT.json` match the final inventory. The start binds the current `run_final_sequence.py` hash. The result must be `PASS_FROZEN_BUILD_AND_STANDARD_KERNEL_REPLAY`, with precisely the five ordered builds followed by the three ordered new-module kernel phases, all exit code 0.
- `final-runs/*/RECEIPT.json` must contain exactly eight unique phase receipts, matching those phases. Each has `status: PASS`, `returncode: 0`, `timed_out: false`, `process_reaped: true`, the frozen runner/inventory hashes, exact source maps before/after, true unchanged flags, and the pinned executable SHA. Its stream files must match their recorded hashes. The new builds must have `-DwarningAsError=true`. Non-audit builds require empty stdout/stderr. Object maps must form an unchanged chain from no local objects to the final five-module objects. Kernels must use the standard `leanchecker -v Module` command, with no `--fresh` claim. The current `final-build/` pathset and bytes must equal the resulting map.
- The successful audit build's stdout is parsed directly using `re.finditer` over the full text, so Lean's wrapped axiom lists remain single records. An axiom-list match excludes both bracket characters internally and is bounded to 4,096 characters. Exactly the four module-origin census sections must occur once, each with its exact positive declaration count. Every declaration name is globally unique; each reported transitive axiom list is a subset of `propext`, `Classical.choice`, and `Quot.sound`; exactly one final total equals the unique declaration count. The frozen census must have 169 declarations, and every raw declaration marker must have been parsed. Every name in the frozen audit source's `required` array, including `TorusMorseFinite.quotientCriticalSet_finite`, must occur. A claimed summary JSON is not substituted for this raw census.
- `negative-final/RECEIPT.json` and its stdout/stderr use the current `run_negative.py` schema. Status must be `PASS_EXPECTED_MISSING_PREMISE_REJECTION`, nonzero return code, no timeout, all source/object bindings unchanged, and pinned Lean identity. Raw output must contain `type mismatch` and `IsMorseDistinct`, and must not contain the tested import/syntax/object-file failure markers. The source is `negative-project/WithoutMorse.lean`. This is interface rejection, not a counterexample theorem.

## Acceptance record to produce

`ROOT_ACCEPTANCE.json` requires these fields (additional provenance fields are welcome):

```json
{
  "verdict": "ACCEPT_SCOPED_FORMAL",
  "source_sha256": "95a660134eda49eecfe6181884bd23b4e4ca210e228d2463de29e5f821df047b",
  "source_inventory_sha256": "f1a429935146b4e406e9ba8cc9ff8b84f7d40c22cc4fea74920dfc013c4911de",
  "review_path": "reviews/CHOSEN_FINAL_REVIEW_FILENAME.md",
  "review_sha256": "ACTUAL_REVIEW_BYTES_SHA256",
  "organizational_independence_credit": 0,
  "human_review_credit": 0,
  "scientific_effect": "NONE"
}
```

`review_path` is a safe path relative to C293 and selects the substantive final review artifact; the script does not invent its filename. The record must continue to disclose the actual same-provider/source-exposed review arrangement.

## Publication, CI and custody records to produce

`GITHUB_READBACK.json` retains C292's per-file schema: `path_prefix`, `head`, and `files`, whose rows have `relative_path`, `bytes`, `sha256`, `remote_sha256`, `raw_byte_match`, `git_blob`, and `tree_blob`. The prefix is exactly `frontiers/morse_finite_critical_20261018/`. `head` is a full 40-character lowercase commit ID. Rows have unique paths, cover exactly the local `publication-package/` files, and collectively include all five frozen source byte hashes. Each local file must match its length and SHA, actual remote SHA with `raw_byte_match: true`, and the Git blob computed from its actual bytes, identical to the native tree blob. These checks bind supplied remote readback evidence; the master itself performs no network read.

`HOSTED_CI_READBACK.json` requires the same `head`, `scientific_effect: NONE`, and exactly three distinct jobs. Each job requires `id`, `head_sha`, `status: completed`, and `conclusion: success`; each head equals the publication head. Its new execution field is exactly:

```json
{"new_formal_execution": "LOCAL_ONLY_NOT_REGISTERED_IN_HOSTED_FORMAL"}
```

Existing hosted registered-target success is not coverage of these new local formal modules.

The archive is `C293_MORSE_FINITE_CRITICAL_DELIVERY.zip`. The canonical builder is `../continuation288/PACKET/TOOLS/research_delivery.py`, SHA-256 `88d6e30182ae682d27f4d156f6c935f8373168ca6ff14d3141cd69c4b036d3a3`. Its `verify` command must succeed. The ZIP has exactly the unique manifest-listed payload members plus its generated `DELIVERY_MANIFEST.json`. Manifest payload paths equal the complete native `PACKET/` file set, with every member byte-identical to its native file. Do not place the generated manifest into native `PACKET/` as an additional payload file.

`PRIVATE_CUSTODY_RECEIPT.json` requires actual archive `bytes`, `sha256`, `owner_only: true`, and `actual_raw_download_equal: true`. `REMOTE_READBACK.zip` must be byte-identical to the native archive. All evidence files read by the master are SHA-256 checked again at the end of the same invocation, including frozen sources, final objects, receipts/logs, review, publication files, archive, and native packet members. No archive is rebuilt and no record is repaired by the master.

## Focused parser correction verification before first master invocation

The reviewer found that the initial line-by-line census parser counted only 131 of the actual 169 declarations because 38 axiom lists wrap across lines. Only the census parser was changed in `final_master.py`; the frozen Lean proof and all other master checks remain unchanged. The corrected parser was checked on actual `final-runs/20261018T030411Z-build-MorseFiniteAxiomAudit-53575871/stdout.txt`, 19,899 bytes, SHA-256 `9f41da11dc9c082106bba058a36649e6886c8f8334ad0b9917fb1b58fd434be8`.

The check extracted the exact census statements from the script's parsed Python AST and executed only that block in an isolated in-memory namespace with a checking function and a read function restricted to the frozen audit source. It did not import the master module or call `verify()`/`main()`. The actual output passed 344 focused checks with module counts `Lifetime: 103/103`, `TorusTopology: 38/38`, `MorseFiniteCritical: 20/20`, `MorseFiniteControls: 8/8`; 169 unique declarations; and all 21 required names present. Each of six in-memory negative controls was rejected: deleted declaration, duplicate declaration, injected `sorryAx`, unclosed axiom bracket, wrong final total, and wrong module count. The standard-axiom and complete-census gates remain active. `FINAL_MASTER_START.json` and `FINAL_MASTER.json` were absent both before and after this focused verification. This is parser engineering evidence, not an additional proof execution or a consuming final-master run.
