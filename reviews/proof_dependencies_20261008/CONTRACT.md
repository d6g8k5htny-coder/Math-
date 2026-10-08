# Proof-slice provisional-5: bounded source-custody contract

This is the selected engineering pilot described in [Stage A offer6057671226](https://github.com/d6g8k5htny-coder/main/issues/281#issuecomment-6057671226). It records source-owned descriptive units and uses. Technical validity is neither mathematical applicability nor completeness, sufficiency, formal alignment or theorem acceptance. Scientific effect is NONE; there is no scientific-status register.

## Normative source chain and scope

The closed contract is R1 [6051274124](https://github.com/d6g8k5htny-coder/main/issues/281#issuecomment-6051274124), R1.1 [6051836749](https://github.com/d6g8k5htny-coder/main/issues/281#issuecomment-6051836749), R2 [6052532958](https://github.com/d6g8k5htny-coder/main/issues/281#issuecomment-6052532958), and the [type/precedence clarification6052611711](https://github.com/d6g8k5htny-coder/main/issues/281#issuecomment-6052611711). The retained provisional-4 [consumer/refusal refinement6054408354](https://github.com/d6g8k5htny-coder/main/issues/281#issuecomment-6054408354) supplies the residual diagnoses and safe scan; its blanket shared-conclusion refusal is superseded by the selected provisional-5 [ALL option and supplement6055192886](https://github.com/d6g8k5htny-coder/main/issues/281#issuecomment-6055192886). The [actual consumer disposition6056889154](https://github.com/d6g8k5htny-coder/main/issues/281#issuecomment-6056889154), [display/B51 addendum6057409473](https://github.com/d6g8k5htny-coder/main/issues/281#issuecomment-6057409473) and [engineering delta6057532513](https://github.com/d6g8k5htny-coder/main/issues/281#issuecomment-6057532513) complete the selected design. Earlier artifacts retain their own versions and scopes.

The two schema literals are proof-unit-inventory/v0-provisional-5 and proof-slice/v0-provisional-5. Stage A contains the real ExpectedInventory and the validator; paired v5 logic is exercised synthetically. A production companion B must be a later descendant of actual published A and bind A's exact identity. No companion or later UI is published by Stage A.

## Closed shapes

Every listed key is required; no additional key is admitted. Arrays use unique explicit IDs, never arbitrary ID maps. No duplicate JSON keys, NaN/Infinity, bool-as-int or scalar coercion is allowed. Text/ID means a nonempty string; string can be empty where the original contract permits it. Positive/integer fields are exact JSON integers. SHA-1 and SHA-256 are full lowercase hex. UTC dates have RFC3339 Z form with valid calendar values. File paths reject absolute paths, dot/traversal/empty components, backslashes and NUL. Native comment/review URLs must match the declared repository, container and native ID. A comment has no native commit field.

The following compact names correspond to the source contract: File=FileIdentity, Selection=SourceSelection, Text=SourcedText, Expected=ExpectedInventory, Slice=ProofSlice, Group=PremiseGroup, Binding=UseBinding, Boundary=ReadingBoundary, External=ExternalReference, Core=ResolvedUseCore, Snapshot=ResolvedUseSnapshot, Inference=InferenceContext, Member=PremiseMember, Contribution=ResolvedContributionGroup, CompleteBundle=CompleteBundleSnapshot. X prefixes denote fully expanded forms, never a second input format.

RecordIdentity is exactly Comment, Review or GitRecord, selected by its literal kind. No stored count, acceptance, score, truth value, formal coverage or numerical certificate field is admitted.

### File

```text
File = {
  repository: repository,
  commit: sha1,
  path: path,
  git_blob: sha1,
  sha256: sha256,
  bytes: integer,
}
```

### SourceFile

```text
SourceFile = {
  id: id,
  identity: File,
}
```

### Selection

```text
Selection = {
  source_id: id,
  lines: lines | null,
  locator: text,
  precision: 'exact_lines' | 'named_locator_unexpanded',
}
```

### XSelection

```text
XSelection = {
  file: File,
  lines: lines | null,
  locator: text,
  precision: 'exact_lines' | 'named_locator_unexpanded',
}
```

### Performer

```text
Performer = {
  provider: string | null,
  agent: string | null,
  session: string | null,
  exposure: text,
}
```

### Comment

```text
Comment = {
  kind: 'github_comment_snapshot',
  repository: repository,
  issue: positive,
  comment_id: decimal,
  url: text,
  updated_at: date,
  body_bytes: integer,
  body_sha256: sha256,
}
```

### Review

```text
Review = {
  kind: 'github_review_snapshot',
  repository: repository,
  pull_request: positive,
  review_id: decimal,
  native_commit: sha1,
  url: text,
  submitted_at: date,
  body_bytes: integer,
  body_sha256: sha256,
}
```

### GitRecord

```text
GitRecord = {
  kind: 'git_file',
  file: File,
}
```

### Record

```text
Record = {
  id: id,
  identity: RecordIdentity,
  performer: Performer,
  role: 'inventory' | 'omission_read' | 'author_response' | 'applicability_review' | 'design' | 'withdrawal',
  scope: text,
}
```

### RecordSelection

```text
RecordSelection = {
  record_id: id,
  locator: text,
}
```

### XRecordSelection

```text
XRecordSelection = {
  record: RecordIdentity,
  locator: text,
}
```

### Text

```text
Text = {
  text: text,
  source_refs: Selection[],
  record_refs: RecordSelection[],
  unknown_refs: id[],
}
```

### XText

```text
XText = {
  text: text,
  source_refs: XSelection[],
  record_refs: XRecordSelection[],
  unknowns: XUnknown[],
}
```

### Unknown

```text
Unknown = {
  id: id,
  description: Text,
  affects_use_ids: id[],
  provenance: RecordSelection[],
}
```

### XUnknown

```text
XUnknown = {
  id: id,
  description: XText,
  affects_use_ids: id[],
  provenance: XRecordSelection[],
}
```

### Semantics

```text
Semantics = {
  model: Text,
  observables: Text[],
  normalization: Text,
  parameters: Text,
  limit_order: Text,
  conclusion: Text,
  exclusions: Text[],
}
```

### XSemantics

```text
XSemantics = {
  model: XText,
  observables: XText[],
  normalization: XText,
  parameters: XText,
  limit_order: XText,
  conclusion: XText,
  exclusions: XText[],
}
```

### Boundary

```text
Boundary = {
  id: id,
  source_id: id,
  consumed_lines: lines[],
  excluded_lines: lines[],
  reason: Text,
}
```

### XBoundary

```text
XBoundary = {
  id: id,
  file: File,
  consumed_lines: lines[],
  excluded_lines: lines[],
  reason: XText,
}
```

### Root

```text
Root = {
  statement_id: id,
  source_statement: Selection,
  entry_unit_ids: id[] (minimum 1),
  graph_node: string | null,
  museum_card: string | null,
  semantics: Semantics,
  reading_boundaries: Boundary[],
}
```

### Conclusion

```text
Conclusion = {
  unit_id: id,
  source: XSelection,
}
```

### ExpectedUnit

```text
ExpectedUnit = {
  id: id,
  section: integer,
  lines: lines,
  locator: text,
}
```

### ExpectedUse

```text
ExpectedUse = {
  id: id,
  consumer_unit_id: id,
  kind: 'premise' | 'context' | 'reading_correction' | 'scope_guard' | 'check',
}
```

### ExpectedGroup

```text
ExpectedGroup = {
  owner_unit_id: id,
  group_id: id,
  combination: 'ALL',
  conclusion: Conclusion,
  premise_use_ids: id[] (minimum 1),
}
```

### Bundle

```text
Bundle = {
  id: id,
  combination: 'ALL',
  conclusion: Conclusion,
  group_ids: id[] (minimum 2),
  basis: Text,
}
```

### Extraction

```text
Extraction = {
  rule: 'maximal-contiguous-nonempty-nonheading-blocks',
  heading_boundaries: [310, 482],
  payload_lines: [312, 480],
  line_convention: 'one-based-inclusive-original-LF',
}
```

### Expected

```text
Expected = {
  schema: 'proof-unit-inventory/v0-provisional-5',
  root_statement_id: id,
  root_boundary: Root,
  source: File,
  sources: SourceFile[] (minimum 1),
  records: Record[],
  unknowns: Unknown[],
  extraction: Extraction,
  expected_units: ExpectedUnit[] (minimum 1),
  expected_uses: ExpectedUse[],
  provenance: RecordSelection[],
  expected_groups: ExpectedGroup[],
  consumer_span_rule: 'whole_unit' | 'same_file_contained_exact',
  read_at: date,
  inventory_record: RecordSelection,
  omission_read_record: RecordSelection,
  expected_bundles: Bundle[],
}
```

### Group

```text
Group = {
  id: id,
  combination: 'ALL',
  conclusion: id,
  premise_use_ids: id[] (minimum 1),
  basis: RecordSelection[],
}
```

### Use

```text
Use = {
  id: id,
  kind: 'premise' | 'context' | 'reading_correction' | 'scope_guard' | 'check',
  binding: Binding,
  provenance: RecordSelection[],
  applicability_reviews: ReviewBinding[],
  unknown_refs: id[],
}
```

### Binding

```text
Binding = {
  consumer_statement_id: id,
  consumer_unit_id: id,
  consumer_source: Selection,
  supplier_ids: id[],
  claimed_interface: Text,
  parameter_mapping: Text,
  context: Text,
  source_reading: ReadingUse[],
}
```

### ReadingUse

```text
ReadingUse = {
  boundary_id: id,
  supplier_ids: id[],
  applies_to: Selection[],
  explanation: Text,
}
```

### XReadingUse

```text
XReadingUse = {
  boundary: XBoundary,
  suppliers: XSupplier[],
  applies_to: XSelection[],
  explanation: XText,
}
```

### External

```text
External = {
  title: string,
  authors: string[],
  edition_or_version: string | null,
  theorem_or_section: string | null,
  url: string | null,
  retained_record: RecordSelection | null,
}
```

### XExternal

```text
XExternal = {
  title: string,
  authors: string[],
  edition_or_version: string | null,
  theorem_or_section: string | null,
  url: string | null,
  retained_record: XRecordSelection | null,
}
```

### Supplier

```text
Supplier = {
  id: id,
  kind: 'inventory_unit' | 'source_section' | 'import' | 'external' | 'unnamed',
  unit_ids: id[],
  source_refs: Selection[],
  external_ref: External | null,
  interface: Text,
  expansion: 'in_slice' | 'unexpanded',
  unknown_refs: id[],
}
```

### XSupplier

```text
XSupplier = {
  id: id,
  kind: 'inventory_unit' | 'source_section' | 'import' | 'external' | 'unnamed',
  unit_ids: id[],
  source_refs: XSelection[],
  external_ref: XExternal | null,
  interface: XText,
  expansion: 'in_slice' | 'unexpanded',
  unknowns: XUnknown[],
}
```

### Unit

```text
Unit = {
  id: id,
  source: Selection,
  section: integer,
  description: Text,
  uses: Use[],
  premise_groups: Group[],
  related_unit_ids: id[],
}
```

### InventoryBinding

```text
InventoryBinding = {
  expected_inventory: File,
  extraction_record: RecordSelection,
  correction_records: RecordSelection[],
}
```

### History

```text
History = {
  id: id,
  kind: 'inventory_statement' | 'omission_observation' | 'author_inventory_amendment' | 'applicability_observation' | 'supersession_note',
  record: RecordSelection,
  affects_unit_ids: id[],
  affects_use_ids: id[],
  text: string,
}
```

### Core

```text
Core = {
  consumer_statement_id: id,
  consumer_statement_source: XSelection,
  consumer_semantics: XSemantics,
  consumer_unit_id: id,
  consumer_source: XSelection,
  suppliers: XSupplier[],
  claimed_interface: XText,
  parameter_mapping: XText,
  context: XText,
  source_reading: XReadingUse[],
}
```

### Member

```text
Member = {
  use_id: id,
  use_kind: 'premise',
  core: Core,
}
```

### Inference

```text
Inference = {
  group_id: id,
  combination: 'ALL',
  conclusion: Conclusion,
  premises: Member[] (minimum 1),
}
```

### Contribution

```text
Contribution = {
  group_id: id,
  owner_unit_id: id,
  combination: 'ALL',
  conclusion: Conclusion,
  members: Member[] (minimum 1),
}
```

### CompleteBundle

```text
CompleteBundle = {
  bundle_id: id,
  combination: 'ALL',
  conclusion: Conclusion,
  basis: XText,
  groups: Contribution[] (minimum 2),
}
```

### ReviewBinding

```text
ReviewBinding = {
  record: RecordSelection,
  reviewed_use: Snapshot,
  scope: Text,
  disposition_as_recorded: string,
  limitations: Text[],
  later_disposition_records: RecordSelection[],
}
```

### Slice

```text
Slice = {
  schema: 'proof-slice/v0-provisional-5',
  artifact_kind: 'source_companion',
  id: id,
  read_at: date,
  author: Performer,
  scientific_effect: 'NONE',
  status_authority: False,
  independence_credit: 0,
  root: Root,
  sources: SourceFile[] (minimum 1),
  records: Record[],
  inventory_binding: InventoryBinding,
  units: Unit[] (minimum 1),
  suppliers: Supplier[],
  unknowns: Unknown[],
  history: History[],
  bundles: Bundle[],
}
```

### Snapshot

```text
Snapshot = {
  consumer_statement_id: id,
  consumer_statement_source: XSelection,
  consumer_semantics: XSemantics,
  consumer_unit_id: id,
  consumer_source: XSelection,
  suppliers: XSupplier[],
  claimed_interface: XText,
  parameter_mapping: XText,
  context: XText,
  source_reading: XReadingUse[],
  use_id: id,
  use_kind: 'premise' | 'context' | 'reading_correction' | 'scope_guard' | 'check',
  inference_context: Inference | null,
  bundle_context: CompleteBundle | null,
}
```

## Identity, selections and evidence custody

FileIdentity's six fields are indivisible. Commit/path membership and original blob framing, byte count and SHA-256 must agree. Source selections use authenticated UTF-8, original LF-delimited inclusive lines; CR sources require another extraction version. Exact selections have a bounded non-null pair. Named unexpanded locators have null lines and remain visibly unresolved, never terminal proofs.

The source-side CLI takes one explicitly mapped Math repository with a complete non-shallow object store. It uses the unchanged retrofit load_strict and _git_blob helpers; raw payload reads preserve binary stdout, including terminal spaces/newlines, and use the same sanitized GIT environment with --no-replace-objects and --no-lazy-fetch. Missing objects/backend capability are explicit technical unavailability. There is no runtime fetch, install, live-comment lookup, worktree fallback or clone write.

Native capture files are read from the artifact's own commit, adjacent to it under records/comment-<native-id>-<body-sha256>.json (or review- for a native review). Capture fields preserve the actual native ID, canonical URL, parent URL, revision/submission metadata and exact untrimmed UTF-8 body. The body must reproduce its declared length/hash. A native review also matches native_commit. A git_file record authenticates its complete file identity. Edited versions get distinct filenames; current bodies never fill older missing evidence. Retained captures establish their recorded custody cut, not current platform state or proof validity.

The in-memory validation APIs consume already acquired raw source/capture maps. Git membership is enforced by the source-side CLI or verify_file_identity before those APIs are used. Browser work remains a later two-buffer consumer and cannot claim to have reread Git source or native records.

## Source and owner joins

ExpectedInventory carries its own source/record/unknown tables. Its source equals its P table entry. Root and provenance resolve against those tables, never the companion's. Expected units preserve the ordered source-authored ID/section/line/locator tuples, including zero-use units. Expected use membership is ID/owner/kind; source authors and a separate reader supply that denominator. Counts are derived only after validation and do not establish omission-freedom.

Every companion Unit resolves to its independently expected full file/line/locator and section, including non-conclusion zero-use rows. Each physically owned Use names that same expected owner and root statement. Its exact consumer selection uses the same complete file identity. whole_unit requires exact equality; same_file_contained_exact permits an exact contained subspan with its retained source-authored locator. An authenticated foreign source is still a source-join failure.

Conclusions are derived from joined units, including immutable source selections; independently supplied conclusion selections must agree. Group members equal exactly their owner's complete recorded premise uses. There is zero or one group per owner; zero premise uses means zero groups. Every other kind stays outside those groups. Source reading ranges are ordered, disjoint, bounded and separate from exclusions. Reading-use selections and referenced supplier selections for that boundary stay inside its consumed ranges. Context/provenance links are not inference edges. Reject mapped cycles from conclusions through recorded groups to inventory-unit suppliers; unexpanded sources cannot certify the absence of hidden cycles.

## Complete recorded ALL bundles

A shared joined conclusion has exactly one explicit bundle, with exactly all groups targeting that conclusion. No implicit grouping, second route, OR, borrowed member, duplicate or orphan bundle is supported. Each group retains its separate owner and unchanged premise set. Nonempty bundle basis.record_refs must identify the actual source-selected contribution and scope; code authenticates and compares them, while source review decides whether the cited text supports the selection.

Render the sentence: “Recorded contributions read together (ALL); mathematical sufficiency is not assessed.” A bundled group has no standalone proof route. The later reader takes group order from ExpectedInventory.expected_bundles.group_ids and member order from ExpectedInventory.expected_groups.premise_use_ids, independently of canonical comparison or companion order. It renders basis text verbatim, including both B51 caveats; it adds no bundle count, acceptance colour or sufficiency score.

## Fully expanded review targets and history

Expand every SourceSelection source_id to its complete file identity, every record_id to its RecordIdentity, supplier_ids to full suppliers, boundary_id to its complete expanded reading boundary, and unknown_refs to fully expanded unknowns. Expanded reading boundaries replace their source_id with file so no mutable source-table indirection survives. Other fields retain their values. Reject unknown-reference cycles. Direct Use.unknown_refs remain provenance; applicability-changing qualifications must also be recorded in target-bearing interface, parameter, context or reading fields.

A current target is constructed from the actual validated Use and owner, not a cached expansion. Core contains only the original ten resolved fields. A premise Snapshot adds use_id, use_kind and its complete own-group inference_context. A bundled premise also has the entire complete bundle_context, including every contribution group's own member cores and resolved bundle basis. Non-premises have both contexts null; unbundled premises have bundle_context null. Member cores never contain nested contexts, history or reviews. Own members/owners/conclusions must be internally consistent; duplicate IDs remain invalid.

Canonical target equality sorts inference premises and contribution members by exact UTF-8 use ID, and bundle groups by exact UTF-8 group ID. Group descriptors canonicalize premise_use_ids; bundle descriptors canonicalize group_ids. All other source-significant arrays retain order. Object-key order is immaterial; scalar types are exact. The companion's ordered unit list stays bound to the independent expected unit list.

Stored historical snapshots are checked as their own fully expanded objects. Their source identities are authenticated, but old IDs/fields are never resolved or filled through today's tables. A well-formed earlier v5 target can differ and remain earlier-target evidence. Missing bundle_context in a v3/v4 target is not migrated: retain the old artifact via provenance/history instead. A ReviewBinding must use an applicability_review record and its holding Use ID. Technical target equality is necessary for scope correspondence, never sufficient for applicability or mathematical acceptance. Narrow inventory/omission/source-design observations remain provenance at their original scope. Empty applicability_reviews and permitted attributed unknown/unexpanded states are valid.

## Refusal order and results

1. Acquire required input buffers; verify their externally fixed bytes/identities
2. Strict UTF-8/JSON parsing
3. Type-guarded scan of current inference fields for explicit ANY/OR or a second distinct group under one owner; never scan quotation/history text
4. Closed shapes and duplicate IDs, inventory first
5. Companion InventoryBinding equals the caller's independent A identity
6. Original source/capture authentication and source/owner/conclusion joins
7. Unsupported composition, inventory then companion: missing bundle for shared conclusion or distinct bundles for one conclusion
8. Within-file consistency, inventory then companion: complete member sets, ownership, cardinality, references and ranges
9. Expected-versus-companion typed equality of membership, root, extraction selector and complete group/bundle descriptors
10. Current target reconstruction, historical comparison and remaining mapped-cycle checks

Earlier failures win. The exact six reasons are INPUT_UNAVAILABLE, IDENTITY_MISMATCH, CONTRACT_SHAPE, UNSUPPORTED_INFERENCE, EXPECTED_INVENTORY_MISMATCH and SOURCE_JOIN_MISMATCH. Unsupported composition is not a proof-false label. A malformed shape/duplicate/missing reference is CONTRACT_SHAPE; a fixed source/owner/span contradiction is SOURCE_JOIN_MISMATCH; a coherent candidate disagreement with the independent expectation is EXPECTED_INVENTORY_MISMATCH. The outer InventoryBinding mismatch is IDENTITY_MISMATCH. Residual within-file problems are CONTRACT_SHAPE. Full source-selected bundle absence can also be a pre-pinning source-data disposition; the CLI never interprets agreement prose automatically.

A refusal exposes no artifact-derived counts or graph. Success may report transient expected counts and exact target-correspondence results with an explicit engineering-only meaning. Expected counts contain units, uses, the five use-kind totals and unknown_annotations, never a bundle count. Historical “114 inferential +1 check” stays a separately attributed quotation and is not a typing rule.

## Invocation and publication order

```sh
python3 -B -S tools/proof_slice_check.py --repo . --inventory-commit FULL_A_CANDIDATE --inventory-path reviews/proof_dependencies_20261008/P_C/EXPECTED_INVENTORY.json
python3 -B -S tools/proof_slice_check.py --repo . --expected-commit PUBLISHED_A --expected-path reviews/proof_dependencies_20261008/P_C/EXPECTED_INVENTORY.json --companion-commit CHECKED_B --companion-path reviews/proof_dependencies_20261008/P_C/PROOF_SLICE.json
```

Inventory mode authenticates the artifact and retained captures at its explicit commit. Paired mode independently receives A and B, requires A ancestry and unchanged expected-file blob in B, and authenticates each side's retained captures at that side's commit. A has no self-commit field. The CLI returns0 for technical validity and2 with a structured refusal otherwise; successful reports bind actual artifact/source/capture identities and the checker/consumed-tool bytes and Python mode.

Stage A's existing downstream job runs focused controls and real inventory-only validation in normal and optimized modes at GITHUB_SHA, retaining evidence under its existing artifact. Stage B later replaces the phase requirement with unconditional paired validation and literal published A; deletion must never trigger an “if companion exists” success fallback. Required hosted checks and independent source-data/engineering reads precede distinct integration. Existing proof/GRAPH/STATUS, sealed packet counts, formal aggregate and protection contexts are untouched.
