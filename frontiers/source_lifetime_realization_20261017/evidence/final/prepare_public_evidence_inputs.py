"""Select complete terminal evidence for a single explicit public projection.

No compiler, network request, source mutation, or implicit recursion through
private coordination records is performed. Run only after exact final review.
"""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent


def main():
    target = ROOT / 'PUBLIC_EVIDENCE_INPUTS.json'
    if target.exists():
        raise RuntimeError('input manifest already exists')
    files = {}

    def add(relative, role, destination=None):
        data = (ROOT / relative).read_bytes()
        data.decode('utf-8')
        record = {'source': relative, 'destination': destination or relative,
                  'sha256': hashlib.sha256(data).hexdigest(), 'role': role}
        if relative in files and files[relative] != record:
            raise RuntimeError('conflicting selection: ' + relative)
        files[relative] = record

    gates = {
        'source_inventory': 'FINAL_SOURCE_INVENTORY.json',
        'final_sequence': 'FINAL_SEQUENCE_TERMINAL_RESULT.json',
        'dependency_rehash': 'FINAL_DEPENDENCY_REHASH.json',
        'review_text': 'NONAUTHOR_REVIEW.md',
        'review_acceptance': 'ROOT_ACCEPTANCE.json',
        'negative_index': 'NEGATIVE_FINAL_INDEX.json'}
    roles = dict(review_text='final_review')
    for role, name in gates.items():
        add(name, roles.get(role, role))
    for path in sorted((ROOT / 'final-runs').glob('*/RECEIPT.json')):
        for name, role in [('START.json', 'final_start'), ('RECEIPT.json', 'final_receipt'),
                           ('stdout.txt', 'final_stdout'), ('stderr.txt', 'final_stderr')]:
            add(str((path.parent / name).relative_to(ROOT)), role)
    index = json.loads((ROOT / gates['negative_index']).read_text())
    if index['status'] != 'PASS':
        raise RuntimeError('negative evidence incomplete')
    for relative in index['receipts']:
        path = Path(relative)
        for name, role in [('START.json', 'negative_start'), ('RECEIPT.json', 'negative_receipt'),
                           ('stdout.txt', 'negative_stdout'), ('stderr.txt', 'negative_stderr')]:
            add(str(path.parent / name), role)
        for name in ['RUNNER.py', 'IMPORTED_RUNNER.py']:
            if (ROOT / path.parent / name).is_file():
                add(str(path.parent / name), 'verification_script')
    generation = Path(index['generation'])
    add(str(generation / 'MANIFEST.json'), 'negative_manifest')
    manifest = json.loads((ROOT / generation / 'MANIFEST.json').read_text())
    for module in manifest['modules']:
        name = str(generation / (module + '.lean'))
        add(name, 'negative_fixture', name + '.txt')
    for path in [ROOT / generation / 'BASE_SOURCE.lean', ROOT / generation / 'BASE_AUDIT.lean'] + sorted(
            (ROOT / generation / 'raw-clones').glob('*.lean')):
        name = str(path.relative_to(ROOT))
        add(name, 'negative_fixture', name + '.txt')
    baseline = json.loads((ROOT / index['positive_baseline_receipt']).read_text())
    for relative in baseline['baseline_development_receipts'].values():
        path = Path(relative)
        for name in ['RECEIPT.json', 'stdout.txt', 'stderr.txt']:
            add(str(path.parent / name), 'supporting_evidence')
    probe = Path('negative-project/instrumentation/proof-binding-0b581f8569781d82')
    add(str(probe / 'MANIFEST.json'), 'negative_manifest')
    name = str(probe / 'NegativeFixtureBindingProbe.lean')
    add(name, 'negative_fixture', name + '.txt')
    add(index['two_part_acceptance'], 'negative_acceptance')
    for name in ['prepare_final_inputs.py', 'run_final_phase.py', 'run_final_sequence.py',
                 'run_recovery_phase.py', 'run_recovery_sequence.py',
                 'run_kernel_recovery_phase.py', 'run_kernel_recovery_sequence.py',
                 'rehash_final_dependencies.py', 'verify_execution.py', 'verify_mutations.py',
                 'export_public_evidence.py', 'prepare_public_evidence_inputs.py']:
        add(name, 'verification_script')
    for name in ['SCOPE.md', 'FINAL_PREPARE_START.json', 'FINAL_SEQUENCE_START.json',
                 'FINAL_SEQUENCE_RESULT.json', 'FINAL_RECOVERY_START.json',
                 'FINAL_SEQUENCE_RECOVERED_RESULT.json', 'FINAL_KERNEL_RECOVERY_START.json',
                 'evidence/INITIAL_CACHE_COPY.json', 'evidence/FINAL_BUILD_INITIALIZATION.json',
                 'negative-project/NEGATIVE_RESULTS.md', 'negative-project/FINAL_NEGATIVE_EVIDENCE.json',
                 'REVIEW_C291_ACTUAL_FINAL_EXECUTION_VERIFICATION.json',
                 'REVIEW_C291_ACTUAL_MUTATION_VERIFICATION.json']:
        add(name, 'supporting_evidence')
    for path in sorted((ROOT / 'evidence/development-source-snapshots').glob('*.lean.txt')):
        add(str(path.relative_to(ROOT)), 'supporting_evidence')
    # The selected receipts contain no private storage locators. This list
    # includes every private Drive identifier known for this delivery route.
    private = json.loads((ROOT / 'evidence/PRIVATE_PREFLIGHT.json').read_text())
    ids = {private['destination']['id'], private['public_register']['id']}
    prior = json.loads((ROOT.parent / 'continuation290/PRIVATE_CUSTODY_RECEIPT.json').read_text())
    ids.add(prior['metadata']['id'])
    ids.update(v['id'] for v in private['ancestors'])
    config = {'schema_version': 1, 'private_identifier_inventory_complete': True,
              'private_identifiers': sorted(ids), 'gates': gates,
              'files': sorted(files.values(), key=lambda v: v['source'])}
    with target.open('x') as stream:
        stream.write(json.dumps(config, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'files': len(files), 'sha256': hashlib.sha256(target.read_bytes()).hexdigest()}))


if __name__ == '__main__':
    main()
