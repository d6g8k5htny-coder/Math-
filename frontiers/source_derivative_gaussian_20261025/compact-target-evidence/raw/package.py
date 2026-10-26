import collections, hashlib, json, pathlib, re, shutil, subprocess

root = pathlib.Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
raw = pathlib.Path('/workspace/scratch/compact-target-moments')
out = pathlib.Path('/workspace/scratch/compact-target-evidence-packaging')
out.mkdir(exist_ok=True)
(out/'sources').mkdir(exist_ok=True)
(out/'objects').mkdir(exist_ok=True)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,obj): (out/name).write_text(json.dumps(obj,indent=2)+'\n')
source = root/'SourceCompactTargetMoments.lean'
shutil.copy2(source,out/'sources'/source.name)
shutil.copytree(raw,out/'raw',dirs_exist_ok=True)
for f in (root/'.lake/build/lib/lean').glob('SourceCompactTargetMoments.*'):
    if f.is_file(): shutil.copy2(f,out/'objects'/f.name)

namespace = 'I4SourceCompactTargetMoments.'
written = []
for line_no,line in enumerate(source.read_text().splitlines(),1):
    m = re.match(r'^(theorem|def|lemma|instance) ([A-Za-z0-9_]+)',line)
    if m: written.append(dict(kind=m[1],name=namespace+m[2],line=line_no))
env = []
axioms = {}
for line in (raw/'inventory-01.log').read_text().splitlines():
    if line.startswith('INVENTORY|'):
        _,kind,name=line.split('|')
        env.append(dict(kind=kind,name=name))
    if line.startswith('AXIOMS|'):
        _,name,axiom_str=line.split('|')
        axioms[name]=[s.strip() for s in axiom_str.strip('[]').split(',') if s.strip()]
allowed={'propext','Classical.choice','Quot.sound'}
assert all(set(a)<=allowed for a in axioms.values())
assert all(d['name'] in axioms for d in written)
for d in written:
    d['axiom_coverage']=dict(kind='DIRECT_LEAN_COLLECTAXIOMS_REPORT',axioms=axioms[d['name']],
        record='raw/inventory-01.json',log='raw/inventory-01.log')
generated=[dict(d,axioms=axioms[d['name']]) for d in env if d['name'] not in {e['name'] for e in written}]
write('COMPACT_TARGET_PUBLIC_INVENTORY.json',dict(source_sha256=sha(source),count=len(written),
    kind_counts=dict(collections.Counter(d['kind'] for d in written)),public_targets=written,
    generated_declarations=generated,generated_count=len(generated),instance_count=0,
    axioms_allowed=sorted(allowed),audit_method='Direct Lean collectAxioms on every matching environment declaration, including both definitions and all generated declarations. No inference from a combined list.'))
proofs=[d['name'] for d in written if d['kind'] in ['theorem','lemma']]
write('PUBLIC_PROOF_NAMES_APPEND.json',proofs)
(out/'PUBLIC_PROOF_NAMES_APPEND.txt').write_text('\n'.join(proofs)+'\n')
write('DEFINITIONS_AND_DATA.json',dict(definitions=[d for d in written if d['kind']=='def'],instances=[],opaque=[],custom_axioms=[]))

commands=[]
for f in sorted(raw.glob('*.json')):
    record=json.loads(f.read_text())
    if 'command' in record:
        commands.append(dict(label=f.stem,record='raw/'+f.name,command=record['command'],
            exit_code=record['exit_code'],source_sha256=record.get('source_sha256_before'),
            elapsed_seconds=record['elapsed_seconds']))
write('EXECUTION_RECORD_INDEX.json',commands)

def local_source(module):
    rel=pathlib.Path(*module.split('.')).with_suffix('.lean')
    for base in [root,root/'inputs']:
        p=base/rel
        if p.exists(): return p
    return None
seen={}
def deps(path):
    key=str(path.relative_to(root))
    if key in seen: return
    imports=[]
    for line in path.read_text().splitlines():
        if line.startswith('import '): imports.extend(line.split()[1:])
    module=key.removeprefix('inputs/').removesuffix('.lean').replace('/','.')
    obj=root/'.lake/build/lib/lean'/pathlib.Path(*module.split('.')).with_suffix('.olean')
    seen[key]=dict(source_sha256=sha(path),imports=imports,cached_object=str(obj),
        cached_object_sha256=sha(obj) if obj.exists() else None,
        evidence_role='NEW_QUALIFIED_MODULE' if path==source else 'REUSED_COMPLETED_VERIFICATION_NO_REPLAY')
    for imp in imports:
        p=local_source(imp)
        if p: deps(p)
deps(source)
write('SOURCE_OBJECT_IDENTITIES.json',dict(sourcecut_base='458058b9a004482de4e80ddae6d1a34ba31287eb',
    final_registered_sourcecut='PENDING_ROOT_INTEGRATION',local_import_closure=seen,
    source=sha(source),objects={f.name:sha(f) for f in (out/'objects').iterdir()}))

brief=root/'SOURCE_COMPACT_TARGET_MOMENTS.md'
write('AUTHOR_HELPER_LINEAGE.json',dict(author='OpenAI Codex /root/compact_target_moments',
    assignment_from='/root',binding_brief=dict(path=str(brief),sha256=sha(brief),frozen_sourcecut='458058b9a004482de4e80ddae6d1a34ba31287eb'),
    producer_owned_source=['SourceCompactTargetMoments.lean'],subagents=[],old_source_edits=[],
    local_proof_reuse=[
        'sourceInverse_prescribed_uniform_bounds hL 0: actual inverse bounded near contact',
        'sourceEndpoint_parameter_limits hL 0: actual covariance invertible eventually',
        'posterior_sampleMajorant_le: every target and actual coefficient shift',
        'sampleMajorant_prior_moment: original Gaussian weighted series, every natural order',
        'sourceGammaRadius_le_fifth: actual radius bounded by fifth derivative majorant',
        'rawPinKernel_eq_confluent: every-target coefficient sampling transport'],
    disclosure='New generic affine majorant integrability proof repeats the mathematical add_pow_le route of the existing private drift_majorant_integrable_pow, since a private declaration cannot be imported. No old source changed.'))

write('CONTROL_RECEIPT.json',dict(
    positive=dict(record='raw/positive-controls-02.json',exit_code=0,
        scope=['five arbitrary target components with first coordinate 1, hence target nonzero',
            'all-natural moments at those targets on one common interval',
            'k=1 target row5=12 and different from k=1/6',
            'k=1 exact every-target raw kernel transport',
            'k=1 height moments for every real height on one common interval',
            'no finite height-independent norm bound for the actual gap target']),
    rejected=[dict(record='raw/reject-height.json',exit_code=1,expected='False remains after norm_num',
        mutation='Replace actual target first coordinate b-k*r^3/2 by -k*r^3/2 at r=1/2,b=3,k=1'),
        dict(record='raw/reject-cubic.json',exit_code=1,expected='False remains after norm_num',
        mutation='Replace actual raw gap k*r^3 by k at r=1/2,b=3,k=1')],
    failure_history=['compile-01: missing namespace, composed-function simplification, vector norm proof details',
        'compile-02: namespace, divide inequality, redundant absolute-value rewrite',
        'positive-controls-01: norm expression in no-uniform-height-bound control needed aligned simplification'],
    success_reuse='Do not rerun successful unchanged compilation/kernel/audit/control checks merely because of integration or handoff. Any new verification must identify the changed scope or unmet obligation.'))

write('COMPACT_TARGET_EVIDENCE_CATALOG.json',dict(schema_version=1,
    role='Qualification of one new actual-source moment module; inherited verification reused',
    scope=['SourceCompactTargetMoments'],source_sha256=sha(source),
    base_sourcecut='458058b9a004482de4e80ddae6d1a34ba31287eb',sourcecut='PENDING_ROOT_INTEGRATION',
    compile_record='raw/compile-03.json',kernel_record='raw/kernel.json',
    named_kernel_checks=1,axiom_record='raw/inventory-01.json',
    public_inventory='COMPACT_TARGET_PUBLIC_INVENTORY.json',controls='CONTROL_RECEIPT.json',
    identity_record='SOURCE_OBJECT_IDENTITIES.json',lineage='AUTHOR_HELPER_LINEAGE.json',
    parent_inventory='Existing 29-module/25-input completed verification is reusable under /workspace/AGENTS.md. No frozen check was rerun.',
    process_review=dict(provider_distinct_review='PENDING_SEPARATE_PROCESS_REQUIREMENT',
        mathematical_evidence='Compile, one named kernel check, direct axiom audit and controls complete for the new module. Process review does not invalidate completed mathematics.'),
    no_inference=['angular or weighted normalizer bounds','capture or elder conclusions',
        'geometric Palm conclusions','parent application status','scientific status changes']))

(out/'SCOPE.md').write_text('''# Compact-target moment evidence

The new module proves one positive radius interval, depending only on the actual
nonzero period L, for every six-dimensional target p and every natural moment n.
The integral of the actual sourceGammaRadius^n is at most C_n(1+norm p)^n and
is integrable. No desired moment or covariance-invertibility estimate is a final
premise. Actual inverse continuity/contact nondegeneracy are inherited results.

The original-sample pointwise posterior majorant uses a fixed nonnegative
summable combination of actual order-five and confluent coefficient weights.
Its Gaussian moments are under the unchanged original smoothLaw.

The varying-gap target is (b-k*r^3/2,0,0,0,0,12*k). Its actual kernel law
specializes exactly to the old law at k=1/6. The raw target identity for
(b,b-k*r^3,0,0,0,0) uses the every-target raw/confluent coefficient sampling lift.
For bounded |k| the moments are at most C_n(1+|b|)^n uniformly in b and k on
one interval independent of b,k,n; the proof even reuses the all-target interval.

Qualification covers only SourceCompactTargetMoments and its new controls.
The final warningAsError compile is compile-03; kernel.json records the single
named leanchecker invocation; inventory-01 audits each declaration directly
with Lean.collectAxioms. The public source inventory has 10 theorems and 2
definitions, no instances; 11 generated declarations are disclosed separately.
Only propext, Classical.choice and Quot.sound occur. All command failures,
successful commands, logs, source snapshots and object identities are preserved.

The frozen 29-module/25-input verification is reused, never replayed. Source
integration and final sourcecut are root-owned and pending. Different-family
review remains a separate process obligation. No weighted/angular normalizer,
capture, elder, geometric Palm, parent, or scientific-status conclusion follows.
''')
(out/'HANDOFF.md').write_text('''# Root integration handoff

Source: SourceCompactTargetMoments.lean, SHA256
4fc28898f09381b4bfd0a15324556d2f3cb68f4b39063aa3acf12db7759ccfc8.
All new mathematical qualification is complete; do not replay unchanged checks.

Root owns lakefile registration, manifests, final sourcecut, commits and posts.
Append the 10 names from PUBLIC_PROOF_NAMES_APPEND.txt; disclose the two
definitions separately from those public proof names. The exact public inventory
also discloses 11 generated declarations. The sourcecut fields are explicitly
PENDING_ROOT_INTEGRATION rather than an invented commit receipt.

Provider-distinct review is a process obligation separate from completed Lean
verification. No claim to that review or any scientific status change is made.
''')

files={str(p.relative_to(out)):sha(p) for p in out.rglob('*') if p.is_file() and p.name!='RAW_EVIDENCE_INDEX.json'}
write('RAW_EVIDENCE_INDEX.json',dict(files=files,file_count=len(files)))
print(json.dumps(dict(package=str(out),public_count=len(written),generated_count=len(generated),
    proof_names=len(proofs),source_sha256=sha(source),files=len(files),import_closure_count=len(seen)),indent=2))
