"""Read-only projection of completed new-scope records; never executes Lean or Git."""
import collections
import hashlib
import json
import pathlib
import re
import shutil

OUT = pathlib.Path('/workspace/scratch/curvature-evidence-packaging')
PACKET = pathlib.Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
SCRATCH = pathlib.Path('/workspace/scratch')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read(path):
    return json.loads(path.read_text())

def write(name, data):
    (OUT / name).write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')

def public_simple(path):
    """Only used on the two single-namespace modules; author inventories for others."""
    namespace = None
    targets = []
    for line_no, line in enumerate(path.read_text().splitlines(), 1):
        ns = re.match(r'^namespace\s+(\S+)', line)
        if ns:
            namespace = ns.group(1)
        decl = re.match(r'^(?:noncomputable\s+)?(theorem|lemma|def|instance)\s+(\w+)', line)
        if decl:
            targets.append({'name': namespace + '.' + decl.group(2), 'kind': decl.group(1), 'line': line_no})
    return targets

roots = {
    'scalar-product': SCRATCH / 'scalar-product-curvature',
    'pin-curvature': SCRATCH / 'pin-curvature-implementation',
    'curvature-decomposition': SCRATCH / 'source-curvature-implementation',
    'weighted-curvature': SCRATCH / 'weighted-curvature-implementation',
    'cutoff-arithmetic-helper': SCRATCH / 'curvature-cutoff-arithmetic',
    'variance-floor-helper': SCRATCH / 'gaussian-variance-floor',
}
files = []
execution_records = []
for label, directory in roots.items():
    for source in sorted(directory.rglob('*')):
        if not source.is_file() or source.suffix in {'.olean', '.ilean', '.pyc'} or '__pycache__' in source.parts:
            continue
        destination = OUT / 'raw' / label / source.relative_to(directory)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        entry = {'path': str(destination.relative_to(OUT)), 'original_path': str(source),
                 'bytes': source.stat().st_size, 'sha256': sha(source)}
        files.append(entry)
        if source.suffix == '.json':
            data = read(source)
            if isinstance(data, dict) and ('command' in data or 'checks' in data or 'build' in data):
                execution_records.append({**entry, 'record': data,
                    'projection_role': 'Read-only index of an existing author record; not a newly executed verification receipt.'})

pin = read(SCRATCH / 'pin-curvature-implementation/qualification_receipt.json')
decomposition = read(SCRATCH / 'source-curvature-implementation/QUALIFICATION_RECEIPT.json')
weighted = read(SCRATCH / 'weighted-curvature-implementation/qualification_receipt.json')
specs = [
    ('SourcePinCurvatureBounds', pin['source_sha256'], read(SCRATCH / 'pin-curvature-implementation/public_targets.json')['targets']),
    ('ScalarProductCurvatureBound', 'fb77c9a4eaf165a39c6c06535fbb3f3f164bca12ddbc2f29b01a33e512564b71', public_simple(PACKET / 'ScalarProductCurvatureBound.lean')),
    ('SourceCurvatureDecomposition', decomposition['source_sha256'], read(SCRATCH / 'source-curvature-implementation/targets.json')),
    ('SourceWeightedCurvatureBound', weighted['source_sha256'], public_simple(PACKET / 'SourceWeightedCurvatureBound.lean')),
]

def printed(log):
    text = log.read_text()
    reports = {name: [a.strip() for a in axioms.split(',') if a.strip()]
               for name, axioms in re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]", text)}
    reports.update({name: [] for name in re.findall(r"'([^']+)' does not depend on any axioms", text)})
    return reports

reports = {
    'SourcePinCurvatureBounds': ('raw/pin-curvature/axioms.log', printed(SCRATCH / 'pin-curvature-implementation/axioms.log')),
    'ScalarProductCurvatureBound': ('raw/scalar-product/scalar-product-controls-01.log', printed(SCRATCH / 'scalar-product-curvature/scalar-product-controls-01.log')),
    'SourceCurvatureDecomposition': ('raw/curvature-decomposition/18-public-axiom-audit.log', printed(SCRATCH / 'source-curvature-implementation/18-public-axiom-audit.log')),
    'SourceWeightedCurvatureBound': ('raw/weighted-curvature/AxiomAudit-01.log', printed(SCRATCH / 'weighted-curvature-implementation/AxiomAudit-01.log')),
}
modules = []
all_targets = []
for module, expected_hash, targets in specs:
    source = PACKET / (module + '.lean')
    assert sha(source) == expected_hash, (module, 'final source identity changed')
    dest = OUT / 'sources' / source.name
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, dest)
    log, proof_reports = reports[module]
    for target in targets:
        target['module'] = module
        if target['name'] in proof_reports:
            target['axiom_coverage'] = {'kind': 'DIRECT_PRINTED_REPORT', 'log': log, 'axioms': proof_reports[target['name']]}
        else:
            assert target['kind'] == 'def', (module, target, 'uncovered proof or instance')
            target['axiom_coverage'] = {'kind': 'DEFINITION_NOT_DIRECTLY_PRINTED', 'note': 'Named definition is compiled/kernel checked with its module; do not describe it as an axiom-print target.'}
        all_targets.append(target)
    modules.append({'module': module, 'source_path': str(source), 'frozen_source_copy': str(dest.relative_to(OUT)),
                    'source_sha256': expected_hash, 'line_count': len(source.read_text().splitlines()),
                    'source_commit': None, 'source_commit_note': 'Root owns the future integration cut; do not attribute current frozen bytes to an earlier partial source commit.',
                    'public_inventory_count': len(targets), 'kind_counts': dict(collections.Counter(t['kind'] for t in targets)),
                    'direct_printed_reports': len(proof_reports), 'targets': targets})

modules[0].update({
    'qualification_receipt': 'raw/pin-curvature/qualification_receipt.json',
    'compile': 'raw/pin-curvature/compile10.json', 'kernel': 'raw/pin-curvature/kernel.json',
    'axiom_record': 'raw/pin-curvature/axioms.json', 'controls': 'raw/pin-curvature/control_receipt.json',
    'qualification_notes': [
        'Final compile10 warningAsError, kernel once, and 71-declaration audit exit0; all63 proof targets and8 definitions directly reported.',
        'Controls reuse compile06 olean36dd25c17899... whose source SHA7989e229... is explicit. Positive control observed additive wrapper sourcefdccc592... while importing that unchanged artifact.',
        'compile06-consumed-source.reconstructed.lean is a reconstruction from unchanged final prefix matching the original recorded SHA; it is not a captured original source snapshot.',
        'Final receipt states all prior declarations unchanged; appended convenience exports received final-source compile/kernel/audit. Controls were not rerun merely for additive integration.',
        'Positive controls exit0 with one unnecessarySimpa suggestion; missing-cubic-pin and negative-radius controls exit1 at False.',
        'compile08 and compile09 were terminated with actual exit143; all failed/intermediate records retained.'
    ],
    'author_lineage': pin['author_side_helper_lineage']})
modules[1].update({
    'compile': 'raw/scalar-product/scalar-product-02.json',
    'kernel': 'raw/scalar-product/scalar-product-kernel.json',
    'axiom_record': 'raw/scalar-product/scalar-product-controls-01.json',
    'controls': 'raw/scalar-product/scalar-product-controls-02.json',
    'qualification_notes': [
        'Final compile02/kernel/controls02 have genuine subprocess JSON before/after source bindings and exit0 empty logs.',
        'All3 valid direct axiom reports occur in controls01 overall exit1 due to the unrelated concrete uniform-law a+a versus2*a simplification error; overall command remains failed.',
        'Controls02 corrected only scratch controls and removed the prints to reuse the existing reports; no separate clean axiom-audit command is claimed.',
        'Controls include actual uniform scalar law with residual radius2 and zero-radius cutoff arithmetic; scalar statements have literal product/density/moment premises.'
    ],
    'author_lineage': [
        {'agent': '/root/normalizer_palm_research', 'contribution': 'Scalar product integral and generic regular curvature integration proofs, production author.'},
        {'agent': '/root', 'contribution': 'Regular-cutoff arithmetic transplanted unchanged from CurvatureCutoff.lean.', 'raw': 'raw/cutoff-arithmetic-helper/RECEIPT.json'}]})
modules[2].update({
    'qualification_receipt': 'raw/curvature-decomposition/QUALIFICATION_RECEIPT.json',
    'compile': 'raw/curvature-decomposition/16-explicit-contract-exports.json',
    'kernel': 'raw/curvature-decomposition/19-kernel-replay.json',
    'axiom_record': 'raw/curvature-decomposition/18-public-axiom-audit.json',
    'controls': 'raw/curvature-decomposition/20-controls-fixed.json',
    'qualification_notes': [
        'Final16 compile and20 controls warningAsError exit0 empty,18 all112 public declarations directly printed standard axioms only,19 named kernel once exit0 empty; production SHA before/after final in all records.',
        'Counts include89 theorem/lemma targets,2 named instances and21 definitions; audited definitions are not counted as proofs.',
        'Control17 failed only for unused-hypothesis warning;20 changed scratch control only. Older01-14 failed/partial production snapshots and outputs retained.',
        'Controls prove an arbitrary residual may alter posterior curvature and zero-variance atom rejects a bounded density estimate, alongside actual all-pin reconstruction/product law.',
        'Helper source.sha256 files are after-execution observations, not before/after subprocess receipts. Final integrated source16/audit18/kernel19 gives applicable qualification.',
        'Variance-floor helper RECEIPT explicitly records an after-execution source hash; no retroactive machine source snapshot invented.'
    ], 'author_lineage': decomposition['coauthors']})
modules[3].update({
    'qualification_receipt': 'raw/weighted-curvature/qualification_receipt.json',
    'compile': 'raw/weighted-curvature/SourceWeightedCurvatureBound-10.log',
    'kernel': 'raw/weighted-curvature/KernelReplay-01.log',
    'axiom_record': 'raw/weighted-curvature/AxiomAudit-01.log',
    'controls': 'raw/weighted-curvature/qualification_receipt.json',
    'receipt_kind': 'Author-created aggregate of actual tool-observed command/capture/exit history, source/control/log/artifact hashes; not a separately generated subprocess before/after receipt.',
    'qualification_notes': [
        'Final-10 compile andPositiveControls-02 warningAsError exit0 empty, kernel01 exit0 empty,14 proof reports only standard axioms; author confirms source unchanged since final build.',
        'Four event definitions are separately inventoried, compiled/kernel checked and not directly printed in the14-proof axiom audit.',
        'RejectedZeroEpsilon andRejectedOmitRegularCutoff each exit1 at intendedFalse; all failed source/control attempts retained.',
        'No failed containers or reconstructed command/capture prefixes in this lane; exact executed capture pipelines are in the original aggregate receipt.'
    ], 'author_lineage': [
        {'agent': '/root/regression_kernel', 'contribution': 'Production weighted cubic proof; actual all-natural radius moment scratch support copied once by pin-curvature owner.', 'raw': 'raw/weighted-curvature/radius/RadiusMoments.lean'},
        {'agent': '/root/normalizer_palm_research', 'contribution': 'Qualified scalar-product dependency, with root arithmetic coauthor.'},
        {'agent': '/root/dm2_landed_composition', 'contribution': 'Qualified actual pin-curvature dependency, with peano_strategy helper.'},
        {'agent': '/root/uniform_jet_moment_sources', 'contribution': 'Qualified actual curvature decomposition dependency, with gaussian_reference_probe and root helpers.'}]})

kind_counts = dict(collections.Counter(t['kind'] for t in all_targets))
direct = [t for t in all_targets if t['axiom_coverage']['kind'] == 'DIRECT_PRINTED_REPORT']
assert all(set(t['axiom_coverage']['axioms']) <= {'propext','Classical.choice','Quot.sound'} for t in direct)
membership = {
    'scope_id': 'SOURCE_CURVATURE_FOUR_NEW_MODULES_20261026',
    'modules': [{'module': m['module'], 'source_sha256': m['source_sha256'], 'public_inventory_count': m['public_inventory_count'], 'kind_counts': m['kind_counts']} for m in modules],
    'new_public_declarations': len(all_targets), 'kind_counts': kind_counts,
    'new_theorem_lemma_targets': kind_counts.get('theorem',0)+kind_counts.get('lemma',0),
    'new_named_instances': kind_counts.get('instance',0), 'new_definitions': kind_counts.get('def',0),
    'direct_printed_declarations': len(direct),
    'direct_printed_proofs_and_instances': sum(t['kind'] != 'def' for t in direct),
    'direct_printed_definitions': sum(t['kind'] == 'def' for t in direct),
    'definitions_without_direct_reports': [t['name'] for t in all_targets if t['axiom_coverage']['kind'] != 'DIRECT_PRINTED_REPORT'],
    'excluded_successor': 'SourcePinPreservingQuartic.lean: newly authorized/active successor, outside these four qualified modules.',
    'excluded_comparison': 'Published analytic paper comparison is a research candidate, not Lean-qualified evidence or a target in this catalog.'
}
write('CURVATURE_MEMBERSHIP.json', membership)
write('CURVATURE_PUBLIC_INVENTORY.json', {'scope': membership['scope_id'], 'targets': all_targets})
write('EXECUTION_RECORD_INDEX.json', {'role': 'Projection of existing records, not new verification execution.', 'records': execution_records})
write('RAW_EVIDENCE_INDEX.json', {'files': files, 'file_count': len(files)})
catalog = {
    'schema_version': 1, 'scope_id': membership['scope_id'], 'scientific_effect': 'NONE',
    'goal_status': 'FULL_ORIGINAL_RESEARCH_GOAL_ACTIVE',
    'qualification_role': 'Four individually author-qualified new modules only; unchanged18 modules and23 exact inputs reused. No combined build or new baseline verification.',
    'worktree': str(PACKET), 'source_contract_commit': '8236e1d', 'integration_cut': None,
    'integration_cut_note': 'Parent owns production manifest/library registration and future public source/evidence cut. Local source status is not itself a published review cut.',
    'membership': membership, 'modules': modules,
    'reused_baseline': {
        'module_count': 18, 'proof_instance_declaration_count': 292,
        'endpoint_group_count': 182, 'field_group_full_inventory_count': 110,
        'field_group_registered_direct_audit_count': 109,
        'exact_input_count': 23,
        'input_binding_sha256_from_existing_binding': '42292a58cf84e118b34f4b8b952fa3b650126dc3d167cee85d8048b9bc6d4b13',
        'endpoint_catalog_sha256_from_existing_catalog': 'b814de0d24141dd0f2fd9087b61c2d7eeb1596836eb439898a5c7506675fc24b',
        'field_catalog_sha256_from_existing_catalog': 'ab5dd99afb038dc314c478ebbb6fe45ef36ab622f724b817615991cdee9b805a',
        'wholefield_cut': '37f8f01db8b7e30190f09bf784d1b4e3419da540',
        'wholefield_review_record': str(PACKET / 'curvature-evidence/REUSED_WHOLEFIELD_REVIEW.json'),
        'wholefield_review_result': 'https://github.com/d6g8k5htny-coder/Math-/pull/513#issuecomment-6405469445',
        'wholefield_review': 'Anthropic Claude01Cz PASS_SCOPED at exact37f8f01; no Lean replay by reviewer. Applies to previous4fieldmodules only, not this new curvature extension.',
        'reuse_policy': 'OwnerAGENTS25Oct2026: completed applicable verification reusable, no unchanged checks repeated for handoff/session/process. This packaging does not rehash, duplicate or reverify old18/23 files.'},
    'new_scope_evidence': {'raw_files': len(files), 'existing_execution_or_aggregate_records': len(execution_records),
                           'raw_index': 'RAW_EVIDENCE_INDEX.json', 'execution_index': 'EXECUTION_RECORD_INDEX.json'},
    'author_provider_family': 'OpenAI',
    'lineage_rule': 'All listed implementation and helper contributors are OpenAI author-side; scientific independence/review credit0. Different-family review is tracked separately.',
    'packaging_actions': 'Read/copy/hash only new-scope source/evidence; no production edits, commits, posts, Lean, kernel, tests, builds or unchanged baseline hash/check reruns.',
    'not_claimed': ['Different-family alignment acceptance for the new four curvature modules', 'Geometric critical-point Palm disintegration',
                    'Noncapture inclusion, Morse/capture/elder/adjacency/counting results', 'P0.2/GT5/later parent closure',
                    'Active fifth successor or analytic comparison qualified by this catalog', 'Completion of the original research goal']
}
write('CURVATURE_EVIDENCE_CATALOG.json', catalog)
print(json.dumps({'catalog_sha256': sha(OUT/'CURVATURE_EVIDENCE_CATALOG.json'), 'membership': membership,
                  'raw_file_count': len(files), 'record_count': len(execution_records)}, indent=2))
