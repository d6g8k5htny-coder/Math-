# C299 native artifact master: bound-input contract

Author: OpenAI Codex `/root/c297_hosted_verifier`, delegated for Dylan Roy, author of the C297 engineering precedent and this adaptation. Same-provider author exposure; no independent, human or scientific credit. This code adapts frozen C297 final_master.py SHA256 `000acdc299363caaa7882863d94e04547f6f3b88969358c7e6df8df695428757`. It performs local artifact/record checks only: no subprocess, Lean, network, Git command or canonical-builder execution. Separate unittest controls exercise inert bytes and predicates; they never call main or the complete verify method.

Actual final invocation, after root freezes inputs and obtains source review:

`python3 -B -S engineering-preflight/master/final_master.py --root /absolute/continuation299`

The script must be within that root. Fixed external names are FINAL_MASTER_INPUTS.json, FINAL_MASTER_START.json and FINAL_MASTER.json. Start/result use exclusive creation; repetition is refused. A failed acceptance retains HOLD and all checks already evaluated. The root's captured FINAL_MASTER.stdout/stderr remain external too. There is no --self-test CLI; use the separate declared unittest controls.

## Final input envelope

Each `identity` below is exactly `{path, bytes, sha256}`: contained native path, integer nonnegative size and lowercase SHA256. Root supplies actual final values; the current development source/run/HOLD cannot fill this envelope as a final PASS.

- `schema_version`: 1.
- `expected`: fields described below; repeated exactly in root acceptance.
- `master_source`, `master_notes`, `master_contract`: identities of this exact executable, these notes and the actual final execution/acceptance contract.
- `source_manifest`: identity of the final five-module/two-control manifest.
- `github_readback`, `publication_inputs`, `github_commit`, `github_ref`, `github_pr`, `github_tree`: identities of decoded native records and final publication list using the C297 schema below.
- `publication_directory`: contained complete native directory corresponding to `frontiers/critical_ridge_20261020/`, excluding its separate workflow. An explicitly assembled composite is allowed. Exact membership and every byte must match publication; frozen prior directories remain history.
- `upstream_readback`: identity of the three-row projection described below, retaining the actual underlying source readbacks in packet custody.
- `formal_config_readback`: identity of three rows `{path,native_file,bytes,sha256,git_blob}` for the existing formal toolchain, lakefile and lockfile.
- `tested_merge_commit`, `hosted_ci`: identities of the native tested-merge commit and CI record below.
- `hosted_artifact_zip`: original downloaded final artifact ZIP identity; `hosted_artifact_directory`: contained extraction directory; `hosted_member_prefix`: normally empty, otherwise explicitly validated.
- `root_acceptance`: identity of the reviewed acceptance record below.
- Optional `review_projections`: rows `{original:identity,public_path,public_identity:{bytes,sha256}}` only when a public-safe review differs from its native original.
- `historical_hosted_attempts`: nonempty rows `{archive:identity,report:identity,run_id,run_attempt,head,status}`. Each original ZIP's unique RESULT.json must byte-match the native report and remain HOLD_NOT_COMPLETED without completed_at; its run/attempt and head must match actual context and differ from the final attempt. Include every actual development attempt selected by root, including development1 run39438543701. This generic historical schema does not mislabel compiler failure as negative semantic success.
- `retained_inputs`: nonempty list of identities for other required history, source/claim/author timeout evidence, declarations, failure streams and raw coordination records. The master hashes them, but does not infer their substantive conclusions automatically.
- `custody`: `{archive:identity,remote_archive:identity,receipt:identity,canonical_verification:identity,bindings:[{source_path,packet_path},...]}` with the C297 acyclic semantics below.

`expected` has exactly these fields:

- Positive integer `pr`, `run_id`, `run_attempt`; actual 40-hex `head`, `base`, `tree`, `tested_commit`, `tested_tree`.
- `source_manifest_sha256`; `support_sha256` mapping exactly `.github/workflows/c299-critical-ridge.yml`, `frontiers/critical_ridge_20261020/c299_hosted_verify.py`, and the matching test_c299_hosted_verify.py to their final reviewed digests.
- `module_counts`: actual positive counts for Lifetime, TorusTopology, MorseFiniteCritical, CriticalRidge. These are cross-checked against independently parsed complete output, not assumed census counts.
- `required_ci_names`: distinct actual applicable job names, including downstream-replay, formal / formal-evidence and math-downstream-gates. Every supplied applicable current-head job must succeed. The dedicated C299 job is checked separately.
- `negative_qualification`: exactly `{status:"QUALIFIED",diagnostics:{WithoutCriticality:record,WithoutNegativeDefiniteness:record}}`. Each record has exact stdout_sha256, stderr_sha256 and whitespace-normalized expression, actual, expected sections from reviewed actual final output. Stream/section identity is additional binding, not a substitute for the master’s independent source-specific omitted-premise and full four-part conclusion checks. Its current display grammar is prospective until real diagnostics exist; any actual spelling correction requires reviewed master code and affected controls, not an envelope-only bypass.

## C297-compatible publication and native CI records

`github_readback`: repository, pr, head, base, tree, tree_untruncated=true, native_remote_byte_equality=true, pr_body_exact_readback=true, files_count, bytes and files. Each file row includes path, local, remote_file, bytes, sha256, remote_sha256, git_blob, tree_blob, raw_byte_match=true. The publication-input JSON is a list with path/local/bytes/sha256 matching these rows. When a prior raw read is reused, supply byte_read_ref and reused_same_git_blob; old read refs are allowed only when their bytes and Git blob equal the final current-tree leaf. Newly changed bytes need their own final raw read. Counts are derived; there is no historical 29/39/50-file constant.

Current decoded commit/ref/PR/tree records bind actual SHA, base, repository, PR number and every publication/formal-config blob. A tree projection is accepted only if explicitly labeled by scope_note and native_entry_count, with every used path and no other projected paths; original native tree must be untruncated. Root preserves the original full record separately. The native PR base must equal the frozen final base. The native tested-merge commit must have exactly two parents, final head and base; hosted shallow-checkout parent output may honestly be empty.

`upstream_readback` is three rows `{module,commit,path,raw_file:identity,git_blob,raw_byte_match:true}`. Actual raw bytes must equal the final corresponding published Lean input. Current intended origins are commit7af365e8c8db1ae0275d4efe08a70a678f153ca2 under frontiers/critical_level_attainment_20261020/final-project; final values are bound by the final source manifest and actual readback rather than hardcoded. Do not convert merely cited provenance into a byte-readback claim.

`hosted_ci` uses C297 fields repository/head/tested_commit/run_id/run_attempt; actual decoded `run`, `job`, `artifact`; `download:{artifact_id,bytes,sha256}`; and `applicable_jobs` records with unique id/name/head_sha/status/conclusion/run_id/run_attempt. The dedicated job object must contain actual `steps`, all completed successfully with distinct step numbers. `job_log` is the identity of its full decoded log containing the tested checkout commit. Optional `additional_native_evidence` binds original envelopes, other applicable logs/steps and readbacks without substituting them for the native objects. Artifact metadata must name the exact run/attempt, correct head and unexpired actual archive size; native SHA256 digest, when supplied, must match the downloaded archive.

## Reviewed acceptance and scientific boundary

Root acceptance is `{verdict:"ACCEPT_SCOPED_FORMAL_EVIDENCE",expected:<exact envelope.expected>,author,reviewer,root,exposure,human_review_credit:0,organizational_independence_credit:0,scientific_effect:"NONE",reviews:{...}}`.

The five required review roles are source_review / ACCEPT_SCOPED_SOURCE, engineering_review / ACCEPT_SCOPED_ENGINEERING_SOURCE, negative_qualification_review / ACCEPT_SCOPED_NEGATIVE_DIAGNOSTICS, hosted_artifact_review / ACCEPT_SCOPED_FORMAL_HOSTED, master_source_review / PASS_SCOPED_MASTER_SOURCE_REVIEW. Each maps to exactly `{path,bytes,sha256,verdict}`, with distinct nonempty review files and exact passing verdicts. These are acceptance-role labels for root's truthful assessment of the actual source-bound reviews, not an instruction to rewrite historical review wording. Root must assess substantive reviews; hashing a file does not reproduce its judgment. No hardcoded review hash creates a code/review self-hash cycle.

The master requires final PASS_HOSTED_C299_EXACT_TARGETS plus negative_predicates_qualified=true and no classification errors. Each negative must have intended_missing_premise_rejection=true, diagnostic_qualification_pending=false, candidate_parser_match=true and no classification error. The current development collector deliberately fails these gates. There is no theorem, provider-distinct, human-review or broad scientific promotion implied by artifact acceptance.

## Execution and custody checks

Exactly 13 ordered phases bind the two runtime probes, five fresh local builds, four standard named-module kernels and two negatives. Every aggregate/per-phase receipt and stdout/stderr byte identity is compared. Commands/cwd/resources, environment-contract policy/digests/selected values, fresh-object search precedence, empty initial inventory, allowed new outputs, unchanged imported objects and final downloaded objects are checked. The audit independently parses all wrapped records, rejects malformed/unknown/forbidden/duplicate/missing targets and measures all four origins and 13 required public interfaces. Runtime paths derive from the actual printed prefix; their hashes remain executor-measured records. Cached dependency objects are not all rebuilt or rehashed here.

The trusted canonical builder runs separately under root control; this master does not execute or reimplement its structural verifier. Canonical verification must report ok/files/manifest_sha256/archive_bytes/archive_sha256/scientific_effect. Private receipt must report owner_only=true, actual_raw_download_equal=true, bytes and sha256. The master verifies original/raw-Drive equality, canonical manifest digest/count, every manifest payload's bytes/size/hash and exact PACKET membership.

Inline custody.bindings must cover every file actually consumed before custody except external cycle-causing files. Each source is outside PACKET and maps uniquely to a safe packet-relative destination; native source, PACKET file and canonical payload must match. Required coverage includes executable/notes/contract, source/config/readback/review files, hosted ZIP and every extracted consumed member, history and retained inputs. This prevents a valid unrelated packet from passing. Include all needed extractions, unlike the initial incomplete C298 selection; do not assume ZIP possession supplies absent native files.

Exclude current FINAL_MASTER_INPUTS.json, FINAL_MASTER_START.json, FINAL_MASTER.json, FINAL_MASTER.stdout, FINAL_MASTER.stderr, current archive/raw-download/private-receipt/canonical-verification files from packet bindings and canonical payload names. Those files remain external. Canonical archive limits and build are root-owned. Later public/R17 delivery receipts remain truthful external completion evidence. Keep private signed locators/governance data out of public projections.
