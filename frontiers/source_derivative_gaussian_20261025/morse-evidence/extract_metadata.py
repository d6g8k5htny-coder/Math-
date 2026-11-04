"""Metadata-only extraction from the existing checked source snapshot and exhaustive audit.
This script performs no Lean invocation, proof check, baseline hashing, or production edit.
"""
from pathlib import Path
import collections,datetime,hashlib,json,re,shutil

out=Path('/workspace/scratch/morse-evidence-packaging')
ev=Path('/workspace/scratch/morse-incidence-production')
snapshot=ev/'module-08.source.lean'
source_path='frontiers/source_derivative_gaussian_20261025/SourceMorseIncidence.lean'
commit='1b1badc823725e6025823395463d4948c5cdf6d4'
frozen_sha='b93fe8f7856d4e632b3ff823788469720ae0814440bbec744fde099d4f29f127'
text=snapshot.read_text()

# Full namespace and declaration list are recovered from the exact compiled snapshot.
# This source has no anonymous instances, macros declaring source constants, nested namespaces,
# or other declaration commands. All declaration headers are line-leading and named.
namespace=[];explicit=[];origin=None
for line_num,line in enumerate(text.splitlines(),1):
    mm=re.match(r'^/-! Preserved author-side helper: (.*?) -/$',line)
    if mm:origin=mm.group(1)
    if line_num>=1393:origin='new actual-source join and compact/IFT consequence'
    m=re.match(r'^namespace\s+(\S+)\s*$',line)
    if m:
        namespace.append(m.group(1));continue
    m=re.match(r'^end\s+(\S+)\s*$',line)
    if m and namespace and m.group(1)==namespace[-1]:
        namespace.pop();continue
    m=re.match(r'^(?P<private>private\s+)?(?P<kind>theorem|lemma|def|abbrev|instance)\s+(?P<name>[A-Za-z_][A-Za-z_0-9\']*)',line)
    if not m:continue
    d=m.groupdict();kind=d['kind'];public=not bool(d['private'])
    # Theorems/lemmas are proposition declarations. There are no named instances here.
    # All explicit defs/abbrevs in this source construct data/types/sets, and are kept
    # out of the proposition/instance registration append list.
    category=('public_proposition' if kind in ('theorem','lemma') else
              'public_named_instance' if kind=='instance' else 'public_definition_or_abbreviation') if public else 'private_explicit_proposition'
    explicit.append({'name':'.'.join(namespace+[d['name']]),'source_kind':kind,
        'visibility':'public' if public else 'private','declaration_category':category,
        'sort_classification':'Prop' if kind in ('theorem','lemma') else 'data/type',
        'source_line':line_num,'source_path':source_path,'code_integration_commit':commit,
        'source_sha256_reused':frozen_sha,'lineage':origin})

log=(ev/'axiom-09.log').read_text()
audit_names=re.findall(r'^AXIOMS ([^:]+):',log,re.M)
audit_count=int(re.search(r'COMPLETE_MODULE_AXIOM_AUDIT declarations=(\d+)',log).group(1))
assert len(audit_names)==audit_count==219
assert len(audit_names)==len(set(audit_names))
public=[d for d in explicit if d['visibility']=='public']
public_names={d['name'] for d in public}
assert len(public_names)==len(public)==140
assert public_names.issubset(audit_names)
private=[d for d in explicit if d['visibility']=='private']
private_audit_names=[n for n in audit_names if n.startswith('_private.')]
assert len(private)==len(private_audit_names)==1
private[0]['actual_audited_kernel_name']=private_audit_names[0]
generated=[n for n in audit_names if n not in public_names and n not in private_audit_names]
assert len(generated)==78

props=[d for d in public if d['source_kind'] in ('theorem','lemma')]
instances=[d for d in public if d['source_kind']=='instance']
defs=[d for d in public if d['source_kind'] in ('def','abbrev')]
append=props+instances
assert len(props)==99 and len(instances)==0 and len(defs)==41
assert collections.Counter(d['source_kind'] for d in defs)=={'def':40,'abbrev':1}
append_text=''.join(d['name']+'\n' for d in append)
(out/'append-names.txt').write_text(append_text)
(out/'append-names.json').write_text(json.dumps([d['name'] for d in append],indent=2)+'\n')
(out/'public-defs-abbrevs.txt').write_text(''.join(d['name']+'\n' for d in defs))
(out/'private-generated-audit-only.txt').write_text(''.join(n+'\n' for n in private_audit_names+generated))

by_name={d['name']:d for d in public}
final_short=['smoothLaw_ae_sourceMorseCube','smoothLaw_ae_sourceMorseCompact',
    'smoothLaw_ae_sourceMorse','sourceMorse_regular','smoothLaw_ae_finite_sourceCriticalCube']
final=[by_name['I4ActualSourceMorse.'+n] for n in final_short]

membership=[]
for n in audit_names:
    if n in public_names:
        d=by_name[n]
        membership.append({'name':n,'membership':d['declaration_category'],
            'source_kind':d['source_kind'],'source_line':d['source_line'],
            'registration_append':n in {x['name'] for x in append}})
    elif n in private_audit_names:
        membership.append({'name':n,'membership':'private_explicit_proposition',
            'source_kind':'private theorem','source_line':private[0]['source_line'],
            'registration_append':False})
    else:
        membership.append({'name':n,'membership':'generated_declaration_audit_only',
            'source_kind':'generated; not a source-explicit public declaration',
            'registration_append':False})

counts={'public_theorem_prop':99,'public_lemma_prop':0,
    'public_named_instance_prop':0,'public_named_instance_data':0,
    'public_def_data_or_type':40,'public_abbrev_type':1,
    'explicit_public_total':140,'private_explicit_theorem_prop':1,
    'generated_audit_only':78,'exhaustive_audit_total':219,
    'registration_append_count':99}
inventory={'schema_version':1,'purpose':'metadata-only public declaration membership and registration inventory',
    'source_path':source_path,'code_integration_commit':commit,
    'source_sha256_reused':frozen_sha,'source_snapshot_used':str(snapshot),
    'source_hash_status':'reused from completed module-08 qualification, not rechecked',
    'exhaustive_audit_used':str(ev/'axiom-09.log'),
    'verification_policy':'No proof, kernel, axiom audit or controls rerun. Existing applicable evidence is reused.',
    'counts':counts,'explicit_public_propositions_and_instances':append,
    'explicit_public_definitions_and_abbreviations':defs,
    'private_explicit_declarations':private,
    'generated_declarations_covered_only_by_exhaustive_audit_and_kernel':generated,
    'final_theorems':final}
(out/'PUBLIC_DECLARATIONS.json').write_text(json.dumps(inventory,indent=2)+'\n')
(out/'AUDIT_MEMBERSHIP.json').write_text(json.dumps({'audit_count':219,
    'audit_receipt':'raw-production/axiom-09.json','membership':membership},indent=2)+'\n')

# Copy only this new Morse lane's actual raw qualification/support artifacts, preserving
# bytes and names; prior 24 modules, Raw/Capture/Param and other baseline inputs are referenced.
raw=out/'raw-production'
raw.mkdir(exist_ok=True)
for p in ev.iterdir():
    if p.is_file():shutil.copy2(p,raw/p.name)

# Short registrar metadata. Digests here cover newly produced metadata only; no baseline
# source or historical qualification is rehashed/revalidated.
append_sha=hashlib.sha256(append_text.encode()).hexdigest()
meta={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'code_integration_commit':commit,'source_sha256_reused':frozen_sha,
    'append_count':99,'append_names_txt_sha256':append_sha,
    'append_json_count':99,'counts':counts,
    'append_order':'source declaration order; one fully qualified public proposition/instance name per line',
    'package_files':{'inventory':'PUBLIC_DECLARATIONS.json','audit_membership':'AUDIT_MEMBERSHIP.json',
        'append_plaintext':'append-names.txt','append_json':'append-names.json',
        'public_data_definitions':'public-defs-abbrevs.txt','private_generated_audit_only':'private-generated-audit-only.txt',
        'scope_and_lineage':'SCOPE_LINEAGE.md','prior_raw_qualification':'raw-production/'},
    'new_work':'metadata extraction and audit-name membership reconciliation only',
    'new_verification':'none; no Lean or kernel invocation',
    'baseline_reuse':'Prior 24 qualified modules/23 inputs plus completed Raw7/Capture8/Param source verification are reused by reference. No baseline hashes, copies or tests were performed.',
    'remaining_formal_nonclaims':['exact Lifetime Euclidean-coordinate transport',
        'C263 period-lattice quotient descent and exact quotient adapter',
        'literal HessianHasInertia transport','conditional Morse at every specified null pin',
        'distinct critical heights','Palm/counting/elder closure','capture/dynamics closure'],
    'provider_distinct_review':'Separate process requirement, not a mathematical verification erasure or a new author-side credit',
    'root_owned':'production lakefile, shared manifests, source integration commits, packaging registration and publication'}
(out/'PACKAGE.json').write_text(json.dumps(meta,indent=2)+'\n')

md=['# SourceMorseIncidence public declarations','',
    f'Frozen source cut `{commit}`; source SHA256 `{frozen_sha}` reused from completed qualification.',
    '', 'This inventory registers **99 explicit public Prop theorems**. There are no explicit lemmas or named instances. ',
    'The 40 public definitions and one public type abbreviation are inventoried separately. The complete existing ',
    '219-declaration audit also covers one explicit private theorem and 78 generated declarations; 219 is not a count of public theorems.',
    '', '| Fully qualified public theorem | Source line |','| --- | --- |']
md += [f"| `{d['name']}` | {d['source_line']} |" for d in props]
md += ['', '| Public definition or abbreviation | Kind | Source line |','| --- | --- | --- |']
md += [f"| `{d['name']}` | {d['source_kind']} | {d['source_line']} |" for d in defs]
(out/'PUBLIC_DECLARATIONS.md').write_text('\n'.join(md)+'\n')
print(json.dumps({'append_count':99,'append_names_txt_sha256':append_sha,'counts':counts,
    'membership_missing_public':[],'package':str(out)},indent=2))
