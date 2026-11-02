"""One final producer documentary closure, reusing every known proof/copy ID."""
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

B = Path('/workspace/scratch/actual-source-regular-local-collar-construct')
S = Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025/SourceActualRegularLocalCollar.lean')
ACTIVE = 'final-documents001'
EMPTY = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
cache_path = B/'FIRST_ID_CACHE.json'
cache = json.loads(cache_path.read_text())
now = datetime.now(timezone.utc).isoformat()
new_hashes = 0
reuses = 0


def read(path):
    return json.loads(Path(path).read_text())


def identity(path):
    global new_hashes, reuses
    path = Path(path)
    st = path.stat()
    marker = [st.st_size, st.st_mtime_ns]
    prior = cache.get(str(path))
    if prior and prior.get('marker') == marker:
        reuses += 1
        return prior
    if st.st_size == 0:
        digest = EMPTY
        origin = 'Literal known EMPTY identity REUSED; zero hashes'
        reuses += 1
    else:
        # Only previously unrecorded immutable documentary payloads reach here.
        # Actual source/object/version/copy identities have already been cached.
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        origin = 'FIRST previously unrecorded NEW immutable documentary payload ID, once'
        new_hashes += 1
    row = {'path': str(path), 'bytes': st.st_size, 'sha256': digest,
           'marker': marker, 'first_observed_utc': datetime.now(timezone.utc).isoformat(),
           'origin': origin}
    cache[str(path)] = row
    return row


def write(name, value):
    path = B/name
    assert not path.exists(), str(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(value, str):
        path.write_text(value)
    else:
        path.write_text(json.dumps(value, indent=2) + '\n')
    return identity(path)


def receipt(label):
    return read(B/'runs'/label/'receipt.json')


source = cache[str(S)]
own = cache[str(B/'build/SourceActualRegularLocalCollar.olean')]
ordinary = cache[str(B/'RegularLocalCollarControls.lean')]
ordinary_object = cache[str(B/'build/RegularLocalCollarControls.olean')]
harness = cache[str(B/'FalseControl.lean')]
prod_inventory = read(B/'INVENTORY_CLASSIFIED.json')
ord_inventory = read(B/'CONTROLS_INVENTORY_CLASSIFIED.json')
strict, kernel = receipt('fixtures004'), receipt('kernel001')
controls, ordinary_inv, negative = receipt('controls004'), receipt('ordinary-inventory001'), receipt('false-control001')
assert all(r['exit_code'] == 0 for r in [strict, kernel, controls, ordinary_inv])
assert negative['exit_code'] == 1
assert (B/'runs/false-control001/stdout.log').read_text().count('⊢ False') == 1
assert negative['streams']['stderr.log']['bytes'] == 0
assert prod_inventory['owned_constants'] == 80 and ord_inventory['owned_constants'] == 55
assert source['sha256'] == '82823ac4360cbfb6eda057eb9fc212c870842703a14f5222454df70f19ed0d96'

closed = []
historical = {}
for path in sorted((B/'runs').glob('*/receipt.json')):
    r = read(path)
    closed.append({'label': r['label'], 'scope_kind': r['scope_kind'],
        'record_path': str(path), 'command_argv': r['command_argv'], 'cwd': r['cwd'],
        'start_utc': r['start_utc'], 'end_utc': r['end_utc'],
        'elapsed_seconds': r['elapsed_seconds'], 'exit_code': r['exit_code'],
        'streams': r['streams'], 'before_snapshot_count': len(r['before_snapshots']),
        'outer_receipt': str(B/'outer'/r['label']/'RECEIPT.json'),
        'entry_receipt': str(B/'entry'/r['label']/'RECEIPT.json')})
    for phase in ['before', 'after']:
        for canonical, row in r[phase].items():
            if not row:
                continue
            key = (canonical, row['sha256'])
            group = historical.setdefault(key, {'canonical_path': canonical,
                'bytes': row['bytes'], 'sha256': row['sha256'],
                'receipt_occurrences': [], 'retained_immutable_paths': []})
            group['receipt_occurrences'].append({'run': r['label'], 'phase': phase})
            snapshot = r['before_snapshots'].get(canonical) if phase == 'before' else None
            if snapshot and snapshot not in group['retained_immutable_paths']:
                group['retained_immutable_paths'].append(snapshot)

counts = Counter(r['scope_kind'] for r in closed)
assert counts == {'math': 17, 'documentary': 21}
external = []
for family in ['initial-external-freeze001', 'known-empty-amendment001']:
    external.append({'family': family, 'scope': 'documentary external literal Python-c',
        'legacy_wrapper_labels': 'root65-* honestly retained',
        'original_layer_records': [str(B/family/layer/('01-'+layer)/'RECEIPT.json')
            for layer in ['worker', 'outer', 'entry']],
        'original_split_streams': [str(B/family/layer/('01-'+layer)/stream)
            for layer in ['worker', 'outer', 'entry'] for stream in ['stdout.log', 'stderr.log']]})

# Current worker and enclosing wrappers close AFTER this child. Adopt these
# exact paths only after actual entry closure; never hash their live streams.
deferred = [B/'runs'/ACTIVE/name for name in ['receipt.json', 'stdout.log', 'stderr.log']]
for layer in ['outer', 'entry']:
    deferred += [B/layer/ACTIVE/name for name in ['RECEIPT.json', 'RESULT.json', 'stdout.log', 'stderr.log']]
deferred_set = {str(p) for p in deferred}

doc_ids = {}
doc_ids['FINAL_IDS.json'] = write('FINAL_IDS.json', {
    'status': 'ALL66_MATHEMATICS_CLOSED_NO_REPLAY', 'observed_utc': now,
    'module': 'SourceActualRegularLocalCollar', 'namespace': 'I4SourceActualRegularLocalCollar',
    'sole_authored_public_Prop': 'actualSource_quotient_regular_local_collar',
    'public_data_global_instances': 0, 'source': source, 'source_lines': 745,
    'eligible_final_new_own_object': own,
    'strict': str(B/'runs/fixtures004/receipt.json'),
    'all_owned_std3': str(B/'runs/inventory001/receipt.json'),
    'all_owned_classification': str(B/'INVENTORY_CLASSIFIED.json'),
    'exactly_one_final_complete_kernel': str(B/'runs/kernel001/receipt.json'),
    'production_constants': 80, 'counts': prod_inventory['classification_counts'],
    'producer_canonical_object_copies': 0,
    'root_sourcecut_and_only_eligible_copy': 'Separate ROOT records govern; producer makes no Git/canonical-copy claim',
    'mathematical_execution_after_final_negative': 'NONE',
    'provider_distinct_review': 'Separate process; same-family credit0/scienceNONE'})
doc_ids['CONTROL_IDS.json'] = write('CONTROL_IDS.json', {
    'status': 'SEPARATE_ORDINARY_AND_ONE_CLOSED_NEGATIVE_COMPLETE', 'observed_utc': now,
    'ordinary_source': ordinary, 'ordinary_source_lines': 299,
    'ordinary_object_ineligible_for_archive_cache_or_canonical_copy': ordinary_object,
    'ordinary_strict': str(B/'runs/controls004/receipt.json'),
    'ordinary_ALL55_std3': str(B/'runs/ordinary-inventory001/receipt.json'),
    'ordinary_classification': str(B/'CONTROLS_INVENTORY_CLASSIFIED.json'),
    'counts': ord_inventory['classification_counts'], 'ordinary_named_kernel': 'NONE',
    'ordinary_AUTHOR': '/root/regular_collar_prospective', 'ordinary_TEXT_helpers': 0,
    'sole_mutation': 'ONLY actual fderiv!=0 omitted, fixed original actual maximum/O; same complete chart/all-epsilon closed-cut and slice outputs',
    'counterproof': 'Independently derived actual global F<=3, exact-target inverse(0,rho/2) in actual source forced above3; no production collar/PC or64/65 call',
    'negative_harness': harness, 'negative_initial_freeze': str(B/'NEGATIVE_INITIAL_CUSTODY.json'),
    'negative_receipt': str(B/'runs/false-control001/receipt.json'),
    'negative_assertion_closed_no_assumed_mutation_hypothesis_axiom_parameter': True,
    'negative_actual_exit_code': 1, 'stdout': negative['streams']['stdout.log'],
    'stderr': negative['streams']['stderr.log'], 'intended_unsolved_False_goals': 1})
doc_ids['INCIDENTAL_PUBLIC_API_READ_EXPOSURE.json'] = write('INCIDENTAL_PUBLIC_API_READ_EXPOSURE.json', {
    'status': 'HONEST_INCIDENTAL_ADJACENT_PRIVATE_EXPOSURE_NO_PRIVATE_API_CALL_OR_BODY_COPY',
    'source': 'SourceFiniteTrig.lean', 'actual_read_block': 'lines248–282',
    'exposure': 'Narrow public toSource interface read also exposed adjacent private representedSample/value/field/scalarSeries helper text',
    'implementation': 'Owned production and ordinary actual samples separately derive field formula through PUBLIC definitions, own finite HasSum and PUBLIC toSource_eval; no private generated name/body copy or old ordinary object',
    'independence': 'No unexposed-author or independent scientific credit; same-family credit0/scienceNONE',
    'root_clarification': 'PUBLIC I4Foundation.scalarSeries definition is allowed; PRIVATE derived SourceFiniteTrig helper is not called',
    'old_proof_verification_replays': 0})

report = f'''# Stage66 producer report — actual regular local quotient collar

All mathematical work is closed; no further mathematical replay is needed.
Production is745lines/{source['bytes']}B SHA {source['sha256']}; final own object
{own['bytes']}B SHA {own['sha256']}. Final strict fixtures004 passed
{strict['start_utc']}–{strict['end_utc']}; exhaustive ALL80 exact-module-owned
standard-three inventory passed; the EXACTLY ONE complete final own-module
kernel001 passed {kernel['start_utc']}–{kernel['end_utc']}, with empty streams.

The sole public Prop uses original positive period/sample/physical point and
literal actual fderiv!=0. Every prescribed ambient open O gets ONE centered
actual quotient-to-Pi2 chart, source inside O, EXACT centered max-norm ball
target and original actual height F=c+coordinate1. The SAME witness gives
nonempty PC actual CLOSED uppercut traces AND level slices for EVERY
|epsilon|<rho, including negative epsilon and literal equality. No hm,
inertia, desired-chart/certificate premise, C1 torus atlas or norm-isometry
claim. Only qualified old PUBLIC actual-field/IFT/AddCircle/source APIs;
no64/65 mathematical dependency or old private/control-body copy.

One complete PRIVATE physical-adapter TEXT original was authored by
/root/regular_collar_physical_text after FULL accepted-context ACK23:21:45
and root release23:22:56.127340; original completion23:27:57/six-file bundle
present23:29:07 preceded producer FIRST IDs and ONE integration. Helper
executions/probes/hashes/objects0. B_ORIGINAL_CUSTODY/B_INTEGRATION001 and
FULL original/integration/amendment patches retain this lineage. Producer
owns all quotient/O/inverse-ball/finite geometry/public assembly/fixtures/
ordinary/counterproof/harness/amendments/executions. No hidden second author.

Both privacy scopes reconstruct the same original period2 finite source
cos(pi*x)+2cos(pi*y) through PUBLIC conversion/shift/zero-sample inputs and
their own finite HasSum proof, retaining actual normalization. Actual basis
fderiv evaluations test both partial cases, and the seam lift has actual
quotient/value/derivative checks. Prescribed neighborhoods use PHYSICAL E2
balls radius1/8. Selected charts retain universal epsilon and consume0 and
±rho/2, exact equality inverse points, distinct same-slice inverse points
and their actual JoinedIn. No independently selected charts are equated.

Separate producer-authored ordinary Controls is299lines/{ordinary['bytes']}B
SHA {ordinary['sha256']}, strict controls004 PASS, separately exhaustive
ALL55-owned/std3 PASS; no ordinary named kernel. Its own actual max value3,
whole zero derivative, openness/membership and global quotient F<=3 support
an independent structural inverse(0,rho/2) contradiction. That proof calls
neither production collar/PC conclusions nor64/65/global Morse results.
The sole mutation omits ONLY derivative!=0 and retains all fixed original
maximum/O/chart/all-epsilon cut/slice outputs. Public ordinary closed Prop
and its proved negation precede the ONE importing assertion. The296B
harness SHA {harness['sha256']} was FIRST-frozen before its sole invocation;
false-control001 {negative['start_utc']}–{negative['end_utc']} exited1 with
exact120B ONE unsolved False/0stderr. No assumed mutation, hypothesis, axiom,
parameter, counterproof replay or second mutation.

All17 mathematical workers are retained: seven successful calls (including
reused partial milestones), nine development failures and the sole intended
negative. controls001's missing scratch --root stopped before elaboration;
all actual corrections/full originals/patches and later success remain.
Current closure adds one documentary worker to38 closed dedicated workers,
for39 dedicated workers=17math22doc,39outer39entry/234 original splitstreams.
Two earlier external Python-c documentary families under known root65 triple
wrappers add12 original splitstreams. Their legacy root65 labels are
disclosed; new66 scripts FIRST IDs/snapshots preceded their own executions.
The11 current closure paths are explicitly deferred to root AFTER real
entry closure; no pending end-time or self-ID is fabricated.

Custody defects are retained honestly: one initial avoidable known-empty
metadata digest, fixed forward by literal EMPTY-ID reuse before later math;
one duplicate-label outer directory guard rejection BEFORE any child/Lean
run, retained as the actual returned combined traceback with explicit stream
limits; one read-only exec transport failure recovered by ONLY the failed
read retry, no mathematical worker replay. Ordinary classification initially
split the coincident module/namespace prefix incorrectly; original JSON/TSV
and full classifier amendment remain, stored ALL55 raw was reclassified
without rerunning Lean. Incidental adjacent old PRIVATE fixture text exposure
is disclosed separately; no private API/body copy or unexposed credit.

All known source/object/history/context/helper/snapshot IDs are reused;
new immutable documentary payloads receive FIRST IDs once, known EMPTY and
exact copies inherit IDs. No old proof/kernel/control/source/object hash
campaign, object snapshot or producer canonical copy. Root alone owns Git,
shared registration/cache/external publication and the eligible new own
object placement after an actual sourcecut. Ordinary/helper/old objects are
ineligible. Current final technical/custody review and root publication
records remain separately attributable; this is not provider-distinct
scientific acceptance. OpenDraft/noReady/noMerge/same-family0/scienceNONE;
014KMath403 STOP/no denial workaround. Future67 extras are EXCLUDED here.

Uniform adjacency/overlap persistence/clearance, lower compact clopen
separation, actual critical-event component inclusions, maximum/minimum
events, global saddle/elder choices, exhaustive H0/once-count, Borel/Rice/
PairLaw and Parent remain OPEN. Original global goal ACTIVE_UNMET; continue
beyond this local theorem. Completed applicable verification remains reusable
across agents/sessions/heads/handoffs; provider process is separate.
'''
doc_ids['REPORT.md'] = write('REPORT.md', report)
doc_ids['HANDOFF.md'] = write('HANDOFF.md', f'''# Stage66 producer handoff

All mathematics complete. Reuse fixtures004 strict, ALL80/std3 inventory001,
EXACTONE kernel001, separate controls004 strict/ALL55 ordinary-inventory001,
and sole296B closed assertion false-control001→120B ONE False/0stderr.
Production745lines {source['sha256']}; eligible own{own['bytes']}B {own['sha256']}.
Ordinary299lines {ordinary['sha256']}; ordinary object INELIGIBLE.

Read REPORT.md, FINAL_IDS.json, CONTROL_IDS.json, both classified inventories,
B original/integration records, every actual retained source/runner/context/
harness original/full patch, all real receipts/streams and explicit exposure/
orchestration/transport/classification history. Do not attribute this report's
reading to root or the independent reviewer. Reading limits/technical review
belong to their own records. No further math, source/object digest, ordinary
kernel, object copy or unchanged check is required by this handoff.

PUBLICATION_ALLOWLIST_FINAL.json is an explicit text-only frozen list; do not
glob a later live producer tail. Exact current-final11 closure paths become
eligible ONLY after actual entry/final-documents001/RECEIPT.json exit0.
Worker streams then have cached identities; root adopts remaining previously
unrecorded closed metadata identities FIRST once, no producer rerun or
recursive self-hash. FINAL_DOCUMENT_IDS records final-document first IDs;
its own ID is cached AFTER writing it and not recursively embedded.

Root alone performs actual sourcecut, eligible NEW own-object placement ONCE,
shared metadata registration/one bounded association attempt, explicit apply,
normal draft-branch publication/readback/new-head CI. All old/helper/ordinary/
further object actions SKIP. Provider-distinct process is separate from this
completed mathematical evidence; samefamily0/scienceNONE/openDraft/noMerge.
Future67 fourproper rootEXTRA documents are excluded66archive/manifest/registry.
Creator6482857252, nextCP23:45UTC28Oct/currentHARD03:30UTC29Oct/end unchanged;
no automatic extension or successor implementation seat. Originalglobalgoal
ACTIVE_UNMET and continues after local publication.
''')

doc_ids['EXECUTION_RECORD_INDEX.json'] = write('EXECUTION_RECORD_INDEX.json', {
    'status': 'ALL_ORIGINAL_CLOSED_RECORDS_PLUS_EXPLICIT_FINAL_DOCUMENTARY_TAIL',
    'observed_utc': now, 'closed_dedicated_worker_count_at_generation': len(closed),
    'closed_counts': dict(counts), 'actual_closed_runs': closed,
    'current_documentary_worker': str(B/'runs'/ACTIVE/'STARTED.json'),
    'after_actual_entry_closure': {'dedicated_workers': 39, 'math': 17,
        'documentary': 22, 'outer': 39, 'entry': 39, 'original_split_streams': 234},
    'external_first_documentary_capture_families': external,
    'external_original_split_streams': 12,
    'prechild_duplicate_guard': str(B/'ORCHESTRATION_DUPLICATE_LABEL001.json'),
    'read_only_transport_failure': str(B/'EXEC_READONLY_TRANSPORT_FAILURE001.json'),
    'rule': 'All full original receipts/argv/code/cwd/timing/status/streams remain verbatim files; this index avoids duplicating full before/after maps'})
doc_ids['HISTORICAL_ID_BINDINGS.json'] = write('HISTORICAL_ID_BINDINGS.json', {
    'status': 'DEDUPLICATED_ACTUAL_RECORDED_VERSION_TO_IMMUTABLE_PATH_BINDINGS',
    'groups': list(historical.values()), 'distinct_canonical_versions': len(historical),
    'receipt_occurrences': sum(len(x['receipt_occurrences']) for x in historical.values()),
    'rule': 'Exact original receipt before/after fields remain authority; retain actual snapshot paths, never attach historical ID to changed current path. No literal repeated large JSON reading claim.'})

new_doc_names = ['ARTIFACT_IDENTITIES.json', 'PUBLICATION_ALLOWLIST_FINAL.json',
                 'FINAL_READY.json', 'FINAL_DOCUMENT_IDS.json']
excluded = {'.olean', '.ilean', '.pyc', '.bin', '.c', '.o', '.so', '.a', '.index', '.pkl'}
paths = [S]
for path in sorted(B.rglob('*')):
    if not path.is_file() or path == cache_path:
        continue
    if path.suffix in excluded or {'build', '__pycache__', '.lake'} & set(path.relative_to(B).parts):
        continue
    paths.append(path)
paths += [B/name for name in new_doc_names]
paths += deferred
paths = sorted(set(paths), key=str)

members = []
for path in paths:
    if str(path) in deferred_set or not path.exists() or path.name in new_doc_names:
        continue
    members.append(identity(path))
doc_ids['ARTIFACT_IDENTITIES.json'] = write('ARTIFACT_IDENTITIES.json', {
    'status': 'CLOSED_TEXT_PAYLOAD_FIRST_IDS_AND_KNOWN_VERSION_COPY_REUSE',
    'observed_utc': now, 'artifacts': members, 'artifact_count': len(members),
    'late_final_documents': 'FINAL_DOCUMENT_IDS.json plus its own cached identity',
    'current11_closure_paths': [str(p) for p in deferred],
    'initial_avoidable_known_empty_metadata_digest': 1,
    'no_mathematical_verification_or_source_object_hash_replay': True})
doc_ids['PUBLICATION_ALLOWLIST_FINAL.json'] = write('PUBLICATION_ALLOWLIST_FINAL.json', {
    'status': 'FROZEN producer text-only66 allowlist; adopt only after actual final-documents001 entry exit0',
    'paths': [str(p) for p in paths], 'path_count': len(paths), 'source_only': str(S),
    'excluded': 'All binaries/build/cache, mutable FIRST_ID_CACHE, old modules/evidence, future67 rootEXTRAs, shared metadata/config/external files',
    'root_appendix': 'Root separately appends actual sourcecut/copy/release/reading/technical review; producer performs no Git/canonical copying',
    'closure_final_deferred_actual_paths': [str(p) for p in deferred],
    'closure_identity_policy': 'Adopt actual closed11 paths after real enclosing entry closure; cached worker stream IDs reused; remaining NEW closed documentary IDs FIRST once, no producer replay/self hash'})
doc_ids['FINAL_READY.json'] = write('FINAL_READY.json', {
    'status': 'ALL66_MATH_AND_IMMUTABLE_PRODUCER_BUNDLE_READY_AFTER_ACTUAL_ENTRY_CLOSURE',
    'observed_utc': now, 'source': source, 'eligible_own_object': own,
    'ordinary_source': ordinary, 'harness': harness,
    'production_ALL_owned_std3': 80, 'ordinary_ALL_owned_std3': 55,
    'exactly_one_complete_final_production_kernel': True,
    'ordinary_kernel_count': 0, 'sole_intended_closed_negative': True,
    'helper_count': 1, 'helper_integration_count': 1, 'helper_executions': 0,
    'final_documentary_layer_closure_still_pending_at_write': True,
    'actual_tail_paths': [str(p) for p in deferred],
    'sourcecut_copy_registration_remote_CI': 'Root-only separate records govern; no producer action/claim',
    'final_technical_and_custody_review': 'Separately attributable reviewer/root records; this producer makes no reading or acceptance claim for them',
    'mathematical_replay_needed': False, 'global_goal': 'ACTIVE_UNMET'})

write('FINAL_DOCUMENT_IDS.json', {
    'status': 'FINAL_DOCUMENT_FIRST_IDS_REUSED_NO_RECURSIVE_SELF_BINDING',
    'observed_utc': datetime.now(timezone.utc).isoformat(), 'documents': list(doc_ids.values()),
    'self_identity': 'Collected once in FIRST_ID_CACHE AFTER this file is written; never recursively embedded',
    'deferred_actual_paths': [str(p) for p in deferred],
    'root_rule': 'Wait for real entry closure; reuse any closed worker stream IDs then FIRST-adopt only remaining new closed metadata payloads'})
cache_path.write_text(json.dumps(cache, indent=2) + '\n')
print(json.dumps({'status': 'FINAL66_PRODUCER_DOCUMENTS_WRITTEN_AWAIT_ACTUAL_ENCLOSING_CLOSURE',
    'observed_utc': datetime.now(timezone.utc).isoformat(), 'dedicated_worker_count_after_closure': 39,
    'math': 17, 'documentary': 22, 'external_documentary_families': 2,
    'frozen_allowlist_paths': len(paths), 'new_unrecorded_documentary_hashes_once': new_hashes,
    'known_ID_reuses': reuses, 'source_object_digest_replays': 0,
    'current_deferred_closure_paths': len(deferred)}))
