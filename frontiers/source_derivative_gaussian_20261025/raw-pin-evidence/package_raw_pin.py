"""Projection/copy of existing new-module qualification; no Lean or Git invocation."""
import collections
import hashlib
import json
import pathlib
import re
import shutil

OUT = pathlib.Path('/workspace/scratch/raw-pin-evidence-packaging')
RAW = pathlib.Path('/workspace/scratch/raw-pin-conditioning')
JOIN = pathlib.Path('/workspace/scratch/actual-geometric-palm-join')
PACKET = pathlib.Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
EXPECTED = '77e521c7fc3fc3da1c922a4ef547b065be58b232b321480948c8fe50d76c2aa5'

def read(path):
    return json.loads(path.read_text())

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')

def copy(source, relative):
    destination = OUT / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    return {'path': str(relative), 'original_path': str(source),
            'bytes': destination.stat().st_size, 'sha256': sha(destination)}

qualification = read(RAW / 'QUALIFICATION_RECEIPT.json')
inventory = read(RAW / 'public_targets.json')
coverage = read(RAW / 'AXIOM_COVERAGE.json')
assert qualification['source_sha256'] == inventory['source_sha256'] == coverage['source_sha256'] == EXPECTED

# Copy only this new module's evidence. Binary artifacts are identified by their
# recorded hashes; no unchanged dependency source/artifact is read or rehashed.
raw_files = []
records = []
for source in sorted(RAW.rglob('*')):
    if not source.is_file() or source.suffix in {'.olean', '.ilean', '.pyc'}:
        continue
    item = copy(source, pathlib.Path('raw/SourceRawPinConditioning') / source.relative_to(RAW))
    raw_files.append(item)
    if source.suffix == '.json':
        value = read(source)
        if isinstance(value, dict) and ('command' in value or 'checks' in value or 'commands' in value):
            records.append({**item, 'record': value,
                'role': 'Index of an existing record, not newly executed verification.'})

# These are the actual private-algebra helper sources/attempts used by the new
# module. Their existing qualification is reused; only new-package copies hashed.
helper_files = []
helper_names = ['RawConfluentLift.lean','algebra-01.json','algebra-01.log',
                'algebra-01.source.lean','algebra-02.json','algebra-02.log',
                'algebra-02.source.lean','algebra-03.json','algebra-03.log','run_new_algebra.py']
for name in helper_names:
    item = copy(JOIN / name, pathlib.Path('helpers/inverse-congruence') / name)
    helper_files.append(item)
    if name.endswith('.json'):
        records.append({**item, 'record': read(JOIN/name),
            'role': 'Previously completed new-module helper record; no new execution.'})

source_item = copy(RAW / 'compile-05.source.lean', pathlib.Path('source/SourceRawPinConditioning.lean'))
assert source_item['sha256'] == EXPECTED
contract_item = copy(PACKET / 'SOURCE_RAW_PIN_CONDITIONING.md', pathlib.Path('contract/SOURCE_RAW_PIN_CONDITIONING.md'))

# Conventional application is preserved separately and cannot enter the Lean
# manifest target list or be described as a compiled Kac–Rice/count theorem.
conventional_files = []
for name in ['APPLICATION_PROOF.md','REUSED_SOURCES.json','SOURCE_CONTRACT.md',
             'SOURCE_RAW_PIN_CONDITIONING_PROPOSAL.md']:
    conventional_files.append(copy(JOIN/name, pathlib.Path('conventional')/name))
assert conventional_files[0]['sha256'] == 'bbf61e080cfcbaaeb78b160921943d8500fd8f1878a0109c3148ddfb446c54d2'

public = []
for target in inventory['targets']:
    public.append({**target, 'axiom_coverage': {
        'kind': 'DIRECT_PRINTED_REPORT', 'axioms': coverage['reports'][target['name']],
        'record': 'raw/SourceRawPinConditioning/axioms-01.json',
        'log': 'raw/SourceRawPinConditioning/axioms-01.log'}})
proofs_instances = [target for target in public if target['kind'] in {'theorem','lemma','instance'}]
definitions = [target for target in public if target['kind'] == 'def']
assert len(public) == 37 and len(proofs_instances) == 30 and len(definitions) == 7
assert all(set(target['axiom_coverage']['axioms']) <= {'propext','Classical.choice','Quot.sound'} for target in public)

private = []
for line_number, line in enumerate((OUT/source_item['path']).read_text().splitlines(), 1):
    match = re.match(r'^private theorem\s+(\w+)', line)
    if match:
        private.append({'name': match[1], 'line': line_number,
                        'coverage': 'Final named module kernel; transitive dependencies of directly printed public source exports. No production-private direct print claimed.'})
assert len(private) == 5

write('RAW_PIN_PUBLIC_INVENTORY.json', {'source_sha256': EXPECTED, 'count':37,
    'kind_counts':inventory['kind_counts'], 'public_targets':public,
    'private_helpers':private})
write('RAW_PIN_TARGET_APPEND.json', {'scope':'SourceRawPinConditioning only',
    'source_sha256':EXPECTED,'count':30,'kind_counts':dict(collections.Counter(t['kind'] for t in proofs_instances)),
    'targets':proofs_instances})
write('SOURCE_MANIFEST_APPEND.json', {
    'scope':'New raw-pin module only; root merges this fragment into its current manifest.',
    'source_modules':['SourceRawPinConditioning.lean'],
    'targets':[target['name'] for target in proofs_instances],
    'new_target_count':30, 'definitions_separately_inventoried':[target['name'] for target in definitions],
    'files':{'SourceRawPinConditioning.lean':EXPECTED},
    'base_context_from_parent_instruction':{'unchanged_modules':24,'unchanged_exact_inputs':23,
        'standalone_total_modules_after_append':25,'standalone_total_proof_instance_targets_after_append':645,
        'concurrent_new_modules':'Excluded; root adds each separately at its own source/evidence cut.'},
    'qualification_receipt':'raw/SourceRawPinConditioning/QUALIFICATION_RECEIPT.json',
    'not_claimed':['Formal geometric Campbell/Kac–Rice theorem','Globally normalized mark Markov kernel','Original-goal closure']})

write('RAW_PIN_EXECUTION_INDEX.json', {'role':'Projection of actual existing command/exit/source/log/artifact records; no new checks.',
                                      'records':records})
all_files = [source_item,contract_item] + raw_files + helper_files + conventional_files
write('RAW_PIN_FILE_INDEX.json', {'scope':'New raw module, its actual helper history, and separate conventional application only.',
                                 'file_count':len(all_files),'files':all_files})
catalog = {
    'schema_version':1,'scope_id':'SOURCE_RAW_PIN_CONDITIONING_20261026',
    'module':'SourceRawPinConditioning','namespace':'I4SourceRawPinConditioning',
    'source_sha256':EXPECTED,'source_copy':source_item['path'],
    'source_copy_origin':'Exact final compile05 source snapshot, already bound by the successful final production compile receipt.',
    'production_path':str(PACKET/'SourceRawPinConditioning.lean'),
    'source_contract_commit':'abc3e5f008176e060e090d445a86bba60da52b95',
    'source_commit':None,'source_commit_status':'Await root code-commit identity; do not attribute this new module to a prior baseline cut.',
    'scientific_effect':'NONE','goal_status':'FULL_ORIGINAL_RESEARCH_GOAL_ACTIVE',
    'qualification_role':'Completed author-side new-module compile, named kernel once, full public axiom audit and controls reused unchanged.',
    'membership':{'public_declarations':37,'theorems':29,'named_instances':1,'definitions':7,
                  'manifest_proof_instance_append':30,'direct_public_axiom_reports':37,
                  'private_helpers':5,'private_helpers_public_targets':False},
    'public_inventory':'RAW_PIN_PUBLIC_INVENTORY.json','target_append':'RAW_PIN_TARGET_APPEND.json',
    'manifest_fragment':'SOURCE_MANIFEST_APPEND.json',
    'qualification_receipt':'raw/SourceRawPinConditioning/QUALIFICATION_RECEIPT.json',
    'axiom_coverage':'raw/SourceRawPinConditioning/AXIOM_COVERAGE.json',
    'checks':qualification['checks'],
    'observed_axioms':qualification['observed_axioms'],
    'named_kernel_replay_count':1,
    'same_lift_result':'The actual raw Fourier coefficient/covariance lift equals the existing confluent lift pointwise for every raw target and sample. Kernel equality includes prescribed null pins without using a.e. uniqueness or a zero-fiber substitution.',
    'conditioning_result':'HasCondDistrib id on rawPins is transported through the actual inverse measurable observation equivalence. Current covariance-unit premises are derived eventually from hL alone; residual independence proof is reused.',
    'weighted_result':'At literal raw target (b,b-r³/6,0,0,0,0), the physical Hessian weighted measure equals sourceSmoothWeightedLaw. Existing moments/floor/probability/event/endpoint/raw+type support are rewritten, retaining arbitrary b and means.',
    'strengthening':qualification['strengthening'],
    'zero_normalizer_boundary':'rawPrescribedWeightedMeasure is a measure at all parameters; probability only follows on the positive-floor interval. No globally normalized raw mark Markov kernel or zero-Z probability fallback is formalized.',
    'controls':qualification['control_semantics'],
    'history':qualification['failure_history'],
    'author_side_helper_lineage':qualification['author_side_helper_lineage'],
    'lineage_rule':'All authors/helpers are OpenAI author-side. Independent-family review credit is separate and not claimed for this new module.',
    'baseline_reuse':{'modules':24,'exact_inputs':23,
        'role':'Frozen existing applicable verification reused; no source copies, dependency hashes, builds or checks of baseline material.',
        'standalone_parent_registration':'25 modules /645 proof-instance targets after this30-name append, per parent instruction only; concurrent new modules excluded.'},
    'conventional_application':{'path':'conventional/APPLICATION_PROOF.md',
        'sha256':'bbf61e080cfcbaaeb78b160921943d8500fd8f1878a0109c3148ddfb446c54d2',
        'role':'Separate conventional actual geometric critical-pair Campbell/Palm source application using already reviewed GAD/finiteL admission. Not Lean qualified or a manifest proof target.',
        'null_pin_caveat':'Canonical Gaussian/Rice mark version is identified pointwise through the same coefficient lift; arbitrary disintegrations are unique only intensity-almost-everywhere.',
        'formal_boundary':'No formal geometric count, finite-incidence area or Kac–Rice theorem is introduced.'},
    'file_index':'RAW_PIN_FILE_INDEX.json','execution_index':'RAW_PIN_EXECUTION_INDEX.json',
    'copied_files':len(all_files),'raw_module_files':len(raw_files),'private_algebra_helper_files':len(helper_files),
    'conventional_application_files':len(conventional_files),
    'packaging_actions':'Read/copy/index only existing new-module source/evidence; hash only new package copies; no old24/23 files read for hash/verification, no Lean/kernel/build/tests, no production edits/commits/posts.',
    'not_claimed':qualification['not_claimed']
}
write('RAW_PIN_EVIDENCE_CATALOG.json',catalog)
print(json.dumps({'catalog_sha256':sha(OUT/'RAW_PIN_EVIDENCE_CATALOG.json'),
                  'copied_files':len(all_files),'existing_execution_or_aggregate_records':len(records),
                  'public_declarations':37,'manifest_append':30,'definitions':7},indent=2))
