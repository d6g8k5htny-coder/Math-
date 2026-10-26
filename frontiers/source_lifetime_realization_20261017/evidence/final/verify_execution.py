"""Independently bind C291 terminal execution records to exact source/object bytes.

This reads evidence; it never compiles, reruns a successful phase, or promotes
scientific status. The final master calls verify on the immutable packet.
"""
from pathlib import Path
from datetime import datetime
import gzip
import hashlib
import json
import re


ORIGINAL_RUNNER_SHA256 = '085164704a7331c74a85e14b5993096ebad41eb055af6a9bc4d7eda4821ee57b'
RECOVERY_RUNNER_SHA256 = '623a42d9d4e6c979ba8691df2b3c7c8c4c797afc32e62a063ab0d95b7ff8f216'
RECOVERY_DRIVER_SHA256 = 'b518ea542a51c73682fc3e05fc4e170849c74a87ecf79cafde8183084adb9827'
FAILED_SEQUENCE_SHA256 = 'a8dddfaf3d46287a573b70fae91d71ba000b219ea4d4b0bed148341e0fe4825d'
FAILED_RECEIPT = 'final-runs/20261018T000515Z-build-SourceLifetimeAxiomAudit-93b1c912/RECEIPT.json'
FAILED_RECEIPT_SHA256 = 'f8b60044d19050e1284501ec90f04d92f3f0f9e521138085784456050ec98560'
KERNEL_RECOVERY_RUNNER_SHA256 = '1b62aa59ec23f108604c98a175fb988d0e2d776cf1024ae39a43913bb4b06d77'
KERNEL_RECOVERY_DRIVER_SHA256 = '16f81f0d18395f80da719a4a60141caaf95923eb09c4ca333a7ef2c58fc95d2b'
AUDIT_RECOVERY_SEQUENCE_SHA256 = 'e28e03d16b3df144317b5f1fe1bbec48379665b3dd39db4422d52209c549dc07'
RECOVERED_AUDIT_RECEIPT = 'final-runs/20261018T001437Z-build-SourceLifetimeAxiomAudit-20f1f279/RECEIPT.json'
RECOVERED_AUDIT_RECEIPT_SHA256 = '0a8243a3cf688098e9c9882868b58534a68b76628905ced4ad470f3d3ea8b152'
KERNEL_FAILED_RECEIPT = 'final-runs/20261018T002219Z-kernel-SourceThetaBridge-9ba2eb35/RECEIPT.json'
KERNEL_FAILED_RECEIPT_SHA256 = '212e50ad5c569370191c488d57717e6744374c6b5596a76980540e4791539baa'
KERNEL_LAUNCH_STDERR = ("uncaught exception: process 'lean' exited with code 255\n"
                        "stderr:\ncould not execute external process 'lean'\n\n").encode()
KERNEL_PATH_FIELDS = {'path_prefix', 'process_path', 'resolved_lean_sha256'}
ORIGINAL_SUCCESS_RECEIPTS = {
    'GaussianSeriesFoundation': ('final-runs/20261017T231625Z-build-GaussianSeriesFoundation-1c941865/RECEIPT.json', '31ebde6646f84d821803d41bf5467bb585bafc23ec3cf7b3086fba682ab61cc8'),
    'SpectralWeights': ('final-runs/20261017T231722Z-build-SpectralWeights-bfb833bc/RECEIPT.json', 'e167f8c80155bf6bd9f37554499bc14c9d2cf35cefbfb63da41c5320b733cc82'),
    'Lifetime': ('final-runs/20261017T231805Z-build-Lifetime-5d16e5f2/RECEIPT.json', '2e17a76c1bdf42dff58ccebfb8c272c984d8d259c78d1068bee8740417d3f5b4'),
    'SourceFourierSeries': ('final-runs/20261017T232503Z-build-SourceFourierSeries-8869fd1b/RECEIPT.json', '213cb36c5dd0cfdf0fcbabbd277dd71be4132cdd5c7c4e47872fa3ddd29bdd07'),
    'SourceLattice': ('final-runs/20261017T233033Z-build-SourceLattice-f9efae75/RECEIPT.json', 'b821901ebbc07b489333763e77bbc0a54bad1c04da48c2e7945d6b2d3b9d55b4'),
    'SourceGaussianLaw': ('final-runs/20261017T233504Z-build-SourceGaussianLaw-0b4340f3/RECEIPT.json', 'c24210b8578d83784067fba870e1f3376e4a0c18e6f17a040bb23fdd30d16bbe'),
    'SourceC4': ('final-runs/20261017T234128Z-build-SourceC4-cdfd8719/RECEIPT.json', '661cba6c60bc9ed8b47e98830018254e891901ac1fa7a1eacb2ac1170d473cb6'),
    'SourceKernel': ('final-runs/20261017T234227Z-build-SourceKernel-48e372e9/RECEIPT.json', '0c63197a96f8ae44efef0339322b39cbaa4db263cc752dbd7d29a51429dd8b0d'),
    'SourceSmooth': ('final-runs/20261017T234353Z-build-SourceSmooth-af5e7e62/RECEIPT.json', 'a1dbc150148e119cbb321977bd1309674a6232f92bd7ae84746d882a21f7175b'),
    'SourceCovariance': ('final-runs/20261017T234444Z-build-SourceCovariance-79d69d23/RECEIPT.json', '29fce1f9cfb929d0eed2f1f3e929e1768448b44311f569c92efeecf181b2a053'),
    'SourceThetaBridge': ('final-runs/20261017T234549Z-build-SourceThetaBridge-944396e3/RECEIPT.json', '39ddabb72b07160fc47b97bc3f1f77f16da10ad33184cd858d50cc0af2b0eb75'),
    'SourceTorus': ('final-runs/20261017T234857Z-build-SourceTorus-399f4d4f/RECEIPT.json', '504cb736f01e65fbe285983f9a60467acf83dd99ba408ef8d6b1ad45f9e851d8'),
    'SourceTorusC4': ('final-runs/20261017T234958Z-build-SourceTorusC4-92783463/RECEIPT.json', '4839f6c45f3943513c76745328f9067a35c537bb00f563000d0bc17e84a49009'),
    'SourceSmoothCarrier': ('final-runs/20261017T235059Z-build-SourceSmoothCarrier-9f6db2a2/RECEIPT.json', '875b32a8c6edb05e0341420ed78ab66db038ef9f768d33a11fc382c8d567af1c'),
    'SourceSmoothControls': ('final-runs/20261017T235155Z-build-SourceSmoothControls-90c54bce/RECEIPT.json', '562777fffae0fe5c8b4d4bfdea60b9f3ded208aa48519af11424af5c1aefa354'),
    'SourceLifetimeGeometry': ('final-runs/20261017T235258Z-build-SourceLifetimeGeometry-ff7a456a/RECEIPT.json', 'b7ff359e27017ef8697e33bc8393bf9bfece6aee03ade49fb349a6dbe7d6615a'),
    'SourceLifetimeField': ('final-runs/20261017T235644Z-build-SourceLifetimeField-bb85810f/RECEIPT.json', 'd0fffedc91d40bb17e99aa8a846aa52c45912e1a06a0d0b47b64012c623f7cac'),
    'SourceLifetimeControls': ('final-runs/20261018T000106Z-build-SourceLifetimeControls-b95a48e0/RECEIPT.json', 'cda622561c94f0a9ecf8b1a67b95ff9fa5d54cd7830fd8f68f902f57eb146573'),
}
START_FIELDS = {
    'kind', 'module', 'command', 'started_utc', 'source_before', 'inventory_sha256',
    'objects_before', 'lean_path', 'dependency_artifact_inventory_sha256',
    'dependency_artifact_count', 'dependency_check', 'executable_sha256', 'runner_sha256',
    'timeout_seconds', 'threads', 'kernel_scope', 'scientific_effect', 'child_pid'}


def recovery_history_checks(old, seq, start, failed, invhash, phase_order, ck):
    """Check the exact recovery relation; accepting this alone is not final verification."""
    ck('original_failed_sequence_status', old['status'] == 'HOLD_FAILED_PHASE' and
       old['source_inventory_sha256'] == invhash and old['scientific_effect'] == 'NONE')
    ck('original_exact_nineteen_build_attempts',
       [(p['kind'], p['module']) for p in old['phases']] == phase_order[:19] and
       [p['returncode'] for p in old['phases']] == [0] * 18 + [1])
    ck('failed_audit_actual_timeout', failed['kind'] == 'build' and
       failed['module'] == 'SourceLifetimeAxiomAudit' and failed['returncode'] == -15 and
       failed['timed_out'] is True and failed['timeout_seconds'] == 420 and
       420 <= failed['seconds'] < 430 and failed['child_pid'] > 0 and failed['threads'] == 2)
    ck('failed_audit_no_mutation_or_product', failed['source_unchanged'] is True and
       failed['imported_objects_unchanged'] is True and failed['integrity_error'] is None and
       failed['source_before'] == failed['source_after'] and
       failed['objects_before'] == failed['objects_after'] and len(failed['objects_before']) == 18 and
       not any(n.split('.')[0] == 'SourceLifetimeAxiomAudit' for n in failed['objects_before']) and
       'produced_objects' not in failed and 'object_sha256' not in failed)
    phase = old['phases'][-1]
    ck('failed_audit_temporal_binding',
       datetime.fromisoformat(old['phases'][-2]['ended_utc']) <=
       datetime.fromisoformat(phase['started_utc']) <= datetime.fromisoformat(failed['started_utc']) <=
       datetime.fromisoformat(failed['ended_utc']) <= datetime.fromisoformat(phase['ended_utc']) <=
       datetime.fromisoformat(old['ended_utc']))
    ck('audit_recovery_stopped_at_kernel_launch', seq['status'] == 'HOLD_FAILED_RECOVERY_PHASE' and
       seq['source_inventory_sha256'] == invhash and seq['scientific_effect'] == 'NONE')
    ck('exact_reused_eighteen_phase_records', seq['phases'][:18] == old['phases'][:18] and
       seq['started_utc'] == old['started_utc'])
    ck('exact_audit_recovery_twenty_attempts',
       [(v['kind'], v['module']) for v in seq['phases']] == phase_order[:20] and
       [v['returncode'] for v in seq['phases']] == [0] * 19 + [1])
    recovery = {
        'failed_sequence': {'path': 'FINAL_SEQUENCE_RESULT.json', 'sha256': FAILED_SEQUENCE_SHA256},
        'failed_receipt': {'path': FAILED_RECEIPT, 'sha256': FAILED_RECEIPT_SHA256},
        'reason': 'OBSERVED_420_SECOND_AUDIT_TIMEOUT',
        'recovered_runner_sha256': RECOVERY_RUNNER_SHA256}
    ck('explicit_recovery_provenance', seq['recovery'] == recovery)
    ck('recovery_start_binding', set(start) == {
       'started_utc', 'recovery', 'inventory_sha256', 'objects_before', 'driver_sha256'} and
       start['recovery'] == recovery and start['inventory_sha256'] == invhash and
       start['objects_before'] == failed['objects_after'] and
       start['driver_sha256'] == RECOVERY_DRIVER_SHA256)
    ck('recovery_after_observed_failure', datetime.fromisoformat(old['ended_utc']) <=
       datetime.fromisoformat(start['started_utc']) <= datetime.fromisoformat(seq['phases'][18]['started_utc']))


def kernel_recovery_history_checks(middle, seq, start, failed, invhash, phase_order, ck):
    """Bind the second observed failure without treating child discovery as kernel replay."""
    ck('kernel_failure_actual_process', failed['kind'] == 'kernel' and
       failed['module'] == 'SourceThetaBridge' and failed['returncode'] == 1 and
       failed['timed_out'] is False and failed['timeout_seconds'] == 420 and
       0 <= failed['seconds'] < 10 and failed['child_pid'] > 0 and failed['threads'] == 2)
    ck('kernel_failure_no_mutation_or_product', failed['source_unchanged'] is True and
       failed['imported_objects_unchanged'] is True and failed['integrity_error'] is None and
       failed['source_before'] == failed['source_after'] and
       failed['objects_before'] == failed['objects_after'] and len(failed['objects_before']) == 19 and
       'produced_objects' not in failed and 'object_sha256' not in failed and
       not (KERNEL_PATH_FIELDS & set(failed)))
    phase = middle['phases'][-1]
    ck('kernel_failure_temporal_binding',
       datetime.fromisoformat(middle['phases'][-2]['ended_utc']) <=
       datetime.fromisoformat(phase['started_utc']) <= datetime.fromisoformat(failed['started_utc']) <=
       datetime.fromisoformat(failed['ended_utc']) <= datetime.fromisoformat(phase['ended_utc']) <=
       datetime.fromisoformat(middle['ended_utc']))
    ck('sequence_success', seq['status'] == 'PASS_LOCAL_SOURCE_BUILD_AND_STANDARD_KERNEL_REPLAY' and
       seq['source_inventory_sha256'] == invhash and seq['scientific_effect'] == 'NONE')
    ck('exact_reused_nineteen_successful_phase_records', seq['phases'][:19] == middle['phases'][:19] and
       seq['started_utc'] == middle['started_utc'] and seq['recovery'] == middle['recovery'])
    ck('complete_phase_order', [(v['kind'], v['module']) for v in seq['phases']] == phase_order and
       all(v['returncode'] == 0 for v in seq['phases']))
    recovery = {
        'failed_sequence': {'path': 'FINAL_SEQUENCE_RECOVERED_RESULT.json',
                            'sha256': AUDIT_RECOVERY_SEQUENCE_SHA256},
        'failed_receipt': {'path': KERNEL_FAILED_RECEIPT, 'sha256': KERNEL_FAILED_RECEIPT_SHA256},
        'reason': 'PINNED_LEAN_CHILD_NOT_ON_PATH', 'runner_sha256': KERNEL_RECOVERY_RUNNER_SHA256}
    ck('explicit_kernel_recovery_provenance', seq['kernel_recovery'] == recovery)
    ck('kernel_recovery_start_binding', set(start) == {
       'started_utc', 'kernel_recovery', 'inventory_sha256', 'objects_before', 'driver_sha256'} and
       start['kernel_recovery'] == recovery and start['inventory_sha256'] == invhash and
       start['objects_before'] == failed['objects_after'] and
       start['driver_sha256'] == KERNEL_RECOVERY_DRIVER_SHA256)
    ck('kernel_recovery_after_observed_failure', datetime.fromisoformat(middle['ended_utc']) <=
       datetime.fromisoformat(start['started_utc']) <= datetime.fromisoformat(seq['phases'][19]['started_utc']))


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(path.read_text())


def verify(root):
    root = Path(root)
    checks = []

    def ck(name, condition):
        checks.append({'name': name, 'passed': bool(condition)})
        if not condition:
            raise ValueError(name)

    invp = root / 'FINAL_SOURCE_INVENTORY.json'
    inv = read(invp)
    invhash = digest(invp.read_bytes())
    ck('reviewed_frozen_inventory', invhash == '82f685a5d71671d9e682ca3df87485e97e8321e16f89c094965a49c2f8a100fe')
    expected = {v['name']: v['sha256'] for v in inv['sources']}
    new = ['SourceThetaBridge', 'SourceLifetimeGeometry', 'SourceLifetimeField',
           'SourceLifetimeControls', 'SourceLifetimeAxiomAudit']
    old = ['GaussianSeriesFoundation', 'SpectralWeights', 'SourceFourierSeries',
           'SourceLattice', 'SourceKernel', 'SourceGaussianLaw', 'SourceCovariance',
           'SourceC4', 'SourceSmooth', 'SourceTorus', 'SourceTorusC4',
           'SourceSmoothCarrier', 'SourceSmoothControls']
    ck('nineteen_unique_sources', len(expected) == len(inv['sources']) == 19)
    ck('five_new_modules', inv['new_modules'] == new)
    ck('exact_source_module_set', inv['old_modules'] == old and
       set(expected) == {n + '.lean' for n in old + ['Lifetime'] + new})
    ck('exact_unique_build_order', len(inv['build_order']) == 19 and
       set(inv['build_order']) == set(old + ['Lifetime'] + new))
    legacy_path = root / 'evidence/INITIAL_CACHE_COPY.json'
    ck('original_source_record_binding', digest(legacy_path.read_bytes()) ==
       'bd47de169c04e16669b14a671c6792a2f4d24e6e1373b3ad3f09227ddbace59a')
    legacy = read(legacy_path)
    ck('unchanged_thirteen_original_sources', len(legacy) == 13 and
       {v['source'] for v in legacy} == {n + '.lean' for n in old} and
       all(expected[v['source']] == v['source_sha256'] for v in legacy))
    ck('original_target_identity', expected['Lifetime.lean'] ==
       '90f4892608e953ecc696bb32ea159d1c178ceb8a1c6edfd11acfceb14af462c6')
    ck('literal_source_carrier_identity', expected['SourceSmoothCarrier.lean'] ==
       '5defdf223e85e7ccd23b5a903a1a306fe7f723727eb6aabf62eef523ef8639ed')
    for item in inv['sources']:
        data = (root / 'final-project' / item['name']).read_bytes()
        ck('frozen_source:' + item['name'], len(data) == item['bytes'] and
           digest(data) == item['sha256'])
        pub = root / 'publication-package' / (
            item['name'] if item['name'][:-5] in new else 'inputs/' + item['name'])
        ck('published_source:' + item['name'], pub.read_bytes() == data)
    init = read(root / 'evidence/FINAL_BUILD_INITIALIZATION.json')
    ck('empty_final_build', init['build_was_created_empty'] is True and
       init['initial_objects'] == [] and init['source_inventory_sha256'] == invhash)
    depbytes = gzip.decompress((root / 'FINAL_DEPENDENCY_ARTIFACTS.json.gz').read_bytes())
    ck('full_dependency_inventory_binding', digest(depbytes) ==
       inv['dependency_artifact_inventory_sha256'])
    deps = json.loads(depbytes)
    ck('dependency_inventory_exact_count', len(deps['artifacts']) == 83897)
    ck('dependency_inventory_unique_paths', len({v['path'] for v in deps['artifacts']}) == 83897)
    ck('dependency_inventory_bytes', sum(v['stat'][0] for v in deps['artifacts']) ==
       deps['total_bytes'] == 8418477755)
    rehash = read(root / 'FINAL_DEPENDENCY_REHASH.json')
    ck('terminal_full_dependency_byte_rehash', rehash['status'] ==
       'PASS_EXACT_DEPENDENCY_BYTES_AND_PATHSET' and rehash['mismatches'] == [] and
       rehash['final_paths_match'] is True and rehash['count'] == len(deps['artifacts']) and
       rehash['inventory_sha256'] == digest(depbytes))
    original_runner = (root / 'run_final_phase.py').read_bytes()
    recovery_runner = (root / 'run_recovery_phase.py').read_bytes()
    recovery_driver = (root / 'run_recovery_sequence.py').read_bytes()
    ck('original_runner_identity', digest(original_runner) == ORIGINAL_RUNNER_SHA256)
    ck('reviewed_audit_only_recovery_runner', digest(recovery_runner) == RECOVERY_RUNNER_SHA256)
    ck('reviewed_recovery_driver', digest(recovery_driver) == RECOVERY_DRIVER_SHA256)
    ck('reviewed_kernel_recovery_runner', digest((root / 'run_kernel_recovery_phase.py').read_bytes()) ==
       KERNEL_RECOVERY_RUNNER_SHA256)
    ck('reviewed_kernel_recovery_driver', digest((root / 'run_kernel_recovery_sequence.py').read_bytes()) ==
       KERNEL_RECOVERY_DRIVER_SHA256)
    oldp = root / 'FINAL_SEQUENCE_RESULT.json'
    ck('frozen_original_failed_sequence', digest(oldp.read_bytes()) == FAILED_SEQUENCE_SHA256)
    oldseq = read(oldp)
    failedpath = root / FAILED_RECEIPT
    ck('frozen_actual_failed_audit_receipt', digest(failedpath.read_bytes()) == FAILED_RECEIPT_SHA256)
    failed = read(failedpath)
    middle_path = root / 'FINAL_SEQUENCE_RECOVERED_RESULT.json'
    ck('frozen_audit_recovery_failed_sequence', digest(middle_path.read_bytes()) == AUDIT_RECOVERY_SEQUENCE_SHA256)
    middle = read(middle_path)
    kernel_failed_path = root / KERNEL_FAILED_RECEIPT
    ck('frozen_actual_kernel_launch_failure', digest(kernel_failed_path.read_bytes()) == KERNEL_FAILED_RECEIPT_SHA256)
    kernel_failed = read(kernel_failed_path)
    seq = read(root / 'FINAL_SEQUENCE_TERMINAL_RESULT.json')
    recovery_start = read(root / 'FINAL_RECOVERY_START.json')
    kernel_recovery_start = read(root / 'FINAL_KERNEL_RECOVERY_START.json')
    phase_order = [('build', n) for n in inv['build_order']] + [('kernel', n) for n in new]
    ck('twenty_four_phases', len(phase_order) == 24)
    recovery_history_checks(oldseq, middle, recovery_start, failed, invhash, phase_order, ck)
    kernel_recovery_history_checks(middle, seq, kernel_recovery_start, kernel_failed,
                                   invhash, phase_order, ck)
    ck('failed_source_and_dependency_binding', failed['inventory_sha256'] == invhash and
       failed['source_before'] == failed['source_after'] == expected and
       failed['dependency_artifact_inventory_sha256'] == digest(depbytes) and
       failed['dependency_artifact_count'] == 83897 and
       failed['runner_sha256'] == ORIGINAL_RUNNER_SHA256 and failed['executable_sha256'] ==
       '1b370cfcbf44e80d1b004ab1b1ab9a4c73951f9f7c242140bcff9bc577576554')
    for stream in ['stdout', 'stderr']:
        data = (failedpath.parent / (stream + '.txt')).read_bytes()
        ck('failed_audit_empty_' + stream, data == b'' and digest(data) == failed[stream + '_sha256'])
    failed_start = read(failedpath.parent / 'START.json')
    ck('failed_audit_start_record', set(failed_start) == START_FIELDS and
       failed_start == {k: failed[k] for k in START_FIELDS})
    ck('kernel_failure_source_and_dependency_binding', kernel_failed['inventory_sha256'] == invhash and
       kernel_failed['source_before'] == kernel_failed['source_after'] == expected and
       kernel_failed['dependency_artifact_inventory_sha256'] == digest(depbytes) and
       kernel_failed['dependency_artifact_count'] == 83897 and
       kernel_failed['runner_sha256'] == ORIGINAL_RUNNER_SHA256 and
       kernel_failed['lean_path'] == failed['lean_path'] and kernel_failed['executable_sha256'] ==
       'cfde41cb11dde58c84e9c60c551fd104bb2fc1104ad44dca932a923120272a35')
    for stream, wanted in [('stdout', b''), ('stderr', KERNEL_LAUNCH_STDERR)]:
        data = (kernel_failed_path.parent / (stream + '.txt')).read_bytes()
        ck('kernel_launch_failure_exact_' + stream, data == wanted and
           digest(data) == kernel_failed[stream + '_sha256'])
    kernel_failed_start = read(kernel_failed_path.parent / 'START.json')
    ck('kernel_launch_failure_start_record', set(kernel_failed_start) == START_FIELDS and
       kernel_failed_start == {k: kernel_failed[k] for k in START_FIELDS})
    ck('dependency_rehash_after_sequence', datetime.fromisoformat(rehash['started_utc']) >=
       datetime.fromisoformat(seq['ended_utc']))
    found = {}
    paths = sorted((root / 'final-runs').glob('*/RECEIPT.json'))
    ck('exact_twenty_six_terminal_receipts', len(paths) == 26)
    failures = []
    for p in paths:
        r = read(p)
        key = (r['kind'], r['module'])
        if r['returncode'] != 0:
            failures.append(p.relative_to(root).as_posix())
            continue
        ck('unique_successful_final_phase:' + str(key), key not in found)
        found[key] = (p, r)
    ck('exactly_two_documented_failures', failures == [FAILED_RECEIPT, KERNEL_FAILED_RECEIPT])
    ck('exact_successful_final_receipt_set', len(found) == 24 and set(found) == set(phase_order))
    ck('exact_eighteen_original_build_receipts', set(ORIGINAL_SUCCESS_RECEIPTS) ==
       {mod for _, mod in phase_order[:18]})
    for mod, (relative, sha256) in ORIGINAL_SUCCESS_RECEIPTS.items():
        p, _ = found[('build', mod)]
        ck('reused_receipt:' + mod, p.relative_to(root).as_posix() == relative and
           digest(p.read_bytes()) == sha256)
    audit_path, _ = found[('build', 'SourceLifetimeAxiomAudit')]
    ck('exact_reused_successful_audit_receipt', audit_path.relative_to(root).as_posix() ==
       RECOVERED_AUDIT_RECEIPT and digest(audit_path.read_bytes()) == RECOVERED_AUDIT_RECEIPT_SHA256)
    executed_root = Path(failed['command'][-1]).parent.parent
    binary_dir = Path(failed['command'][0]).parent
    ck('frozen_execution_root', str(executed_root) ==
       '@C291_ROOT@')
    objects = {}
    previous_end = datetime.fromisoformat(seq['started_utc'])
    for position, (kind, mod) in enumerate(phase_order):
        path, r = found[(kind, mod)]
        label = kind + ':' + mod
        phase = seq['phases'][position]
        ck(label + ':temporal_order', previous_end <= datetime.fromisoformat(phase['started_utc']) <=
           datetime.fromisoformat(r['started_utc']) <= datetime.fromisoformat(r['ended_utc']) <=
           datetime.fromisoformat(phase['ended_utc']) <= datetime.fromisoformat(seq['ended_utc']))
        previous_end = datetime.fromisoformat(phase['ended_utc'])
        ck(label + ':actual_success', r['returncode'] == 0 and not r['timed_out'] and
           r['source_unchanged'] and r['imported_objects_unchanged'] and
           r['integrity_error'] is None)
        ck(label + ':source_and_dependency_binding', r['inventory_sha256'] == invhash and
           r['source_before'] == r['source_after'] == expected and
           r['dependency_artifact_inventory_sha256'] == digest(depbytes) and
           r['dependency_artifact_count'] == 83897)
        ck(label + ':own_object_chain', r['objects_before'] == objects)
        for stream in ['stdout', 'stderr']:
            b = (path.parent / (stream + '.txt')).read_bytes()
            ck(label + ':' + stream + '_digest', digest(b) == r[stream + '_sha256'])
        start_record = read(path.parent / 'START.json')
        start_fields = START_FIELDS | KERNEL_PATH_FIELDS if kind == 'kernel' else START_FIELDS
        ck(label + ':start_record_binding', set(start_record) == start_fields and
           start_record == {k: r[k] for k in start_fields})
        is_recovery = (kind, mod) == ('build', 'SourceLifetimeAxiomAudit')
        timeout = 900 if is_recovery else 420
        runner = (KERNEL_RECOVERY_RUNNER_SHA256 if kind == 'kernel' else
                  RECOVERY_RUNNER_SHA256 if is_recovery else ORIGINAL_RUNNER_SHA256)
        ck(label + ':bounded_actual_process', r['child_pid'] > 0 and r['threads'] == 2 and
           0 <= r['seconds'] < timeout + 10 and r['timeout_seconds'] == timeout)
        ck(label + ':runner_binding', r['runner_sha256'] == runner)
        ck(label + ':exact_import_paths', r['lean_path'] == failed['lean_path'])
        if kind == 'kernel':
            ck(label + ':pinned_child_discovery', r['path_prefix'] == str(binary_dir) and
               r['process_path'] == ':'.join([str(binary_dir), '/usr/bin', '/bin', '/usr/sbin', '/sbin']) and
               r['resolved_lean_sha256'] ==
               '1b370cfcbf44e80d1b004ab1b1ab9a4c73951f9f7c242140bcff9bc577576554')
        else:
            ck(label + ':no_retroactive_path_fields', not (KERNEL_PATH_FIELDS & set(r)))
        if kind == 'build':
            command = [str(binary_dir / 'lean'), '-j2', '-M4096']
            if mod in new:
                command.append('-DwarningAsError=true')
            command += ['-o', str(executed_root / 'final-build' / (mod + '.olean')),
                        str(executed_root / 'final-project' / (mod + '.lean'))]
        else:
            command = [str(binary_dir / 'leanchecker'), '-v', mod]
        ck(label + ':exact_command', r['command'] == command)
        ck(label + ':scientific_effect', r['scientific_effect'] == 'NONE')
        if is_recovery:
            ck('failed_attempt_in_object_chain', failed['objects_before'] ==
               failed['objects_after'] == r['objects_before'] == objects and
               datetime.fromisoformat(failed['ended_utc']) < datetime.fromisoformat(r['started_utc']))
        if position == 19:
            ck('kernel_launch_failure_in_object_chain', kernel_failed['objects_before'] ==
               kernel_failed['objects_after'] == r['objects_before'] == objects and
               datetime.fromisoformat(kernel_failed['ended_utc']) < datetime.fromisoformat(r['started_utc']))
        ck(label + ':executable_binding', r['executable_sha256'] == (
           '1b370cfcbf44e80d1b004ab1b1ab9a4c73951f9f7c242140bcff9bc577576554' if kind == 'build'
           else 'cfde41cb11dde58c84e9c60c551fd104bb2fc1104ad44dca932a923120272a35'))
        if kind == 'build':
            ck(label + ':produced_only_target', bool(r['produced_objects']) and
               all(n.split('.')[0] == mod for n in r['produced_objects']))
            objects.update(r['produced_objects'])
            ck(label + ':new_warnings_are_errors', mod not in new or '-DwarningAsError=true' in r['command'])
        else:
            ck(label + ':standard_kernel_scope', r['command'][-2:] == ['-v', mod] and '--fresh' not in r['command'])
        ck(label + ':object_chain_after', r['objects_after'] == objects)
        ck(label + ':primary_object_identity', r['object_sha256'] == objects[mod + '.olean'])
    actual_objects = {p.name: digest(p.read_bytes()) for p in (root / 'final-build').iterdir() if p.is_file()}
    ck('final_object_bytes_exactly_rebuilt', actual_objects == objects)
    ap, _ = found[('build', 'SourceLifetimeAxiomAudit')]
    output = (ap.parent / 'stdout.txt').read_text()
    counts = dict((m, int(c)) for m, c in re.findall(r'^LIFETIME_AUDIT_MODULE (\S+) COUNT (\d+)$', output, re.M))
    expected_counts = dict(zip([
        'GaussianSeriesFoundation', 'SpectralWeights', 'SourceFourierSeries', 'SourceC4',
        'SourceGaussianLaw', 'SourceLattice', 'SourceKernel', 'SourceCovariance',
        'SourceTorus', 'SourceTorusC4', 'SourceSmooth', 'SourceSmoothCarrier',
        'SourceSmoothControls', 'Lifetime', 'SourceThetaBridge', 'SourceLifetimeGeometry',
        'SourceLifetimeField', 'SourceLifetimeControls'],
        [12, 28, 25, 10, 10, 27, 7, 4, 16, 14, 26, 33, 10, 103, 34, 16, 12, 22]))
    ck('exact_eighteen_census_modules', counts == expected_counts)
    blocks = list(re.finditer(r'^LIFETIME_AUDIT_MODULE (\S+) COUNT (\d+)\n(.*?)(?=^LIFETIME_AUDIT_MODULE |^LIFETIME_AUDIT_STANDARD_ONLY_PASS)', output, re.M | re.S))
    ck('per_module_declaration_census', len(blocks) == 18 and all(
       len(re.findall(r'^LIFETIME_AUDIT_DECL ', b.group(3), re.M)) == int(b.group(2)) for b in blocks))
    decls = re.findall(r'^LIFETIME_AUDIT_DECL (\S+) AXIOMS \[([^\]]*)\]', output, re.M)
    ck('whole_module_axiom_census', len(counts) == 18 and sum(counts.values()) == len(decls) == 409)
    ck('unique_declarations', len({n for n, _ in decls}) == len(decls))
    ck('private_declarations_included', sum(n.startswith('_private.') for n, _ in decls) == 40)
    ck('standard_axioms_only', all(set(a.replace('\n', '').replace(' ', '').split(',')) - {''}
       <= {'propext', 'Classical.choice', 'Quot.sound'} for _, a in decls))
    audit_source = (root / 'final-project/SourceLifetimeAxiomAudit.lean').read_text()
    required = re.findall(r'`([\w.]+)', audit_source.split('let required : Array Name := #[', 1)[1].split(']', 1)[0])
    ck('all_required_declarations', len(required) == 27 and set(required) <= {n for n, _ in decls})
    ck('single_complete_audit_pass', output.count('LIFETIME_AUDIT_STANDARD_ONLY_PASS COUNT 409') == 1)
    ck('no_audit_error_or_warning', not re.search(r'\b(?:error|warning)(?:\([^)]*\))?:|sorryAx', output))
    return {'checks': checks, 'phase_count': len(phase_order), 'terminal_receipts': 26,
            'documented_failed_attempts': 2, 'declarations': len(decls),
            'private_declarations': 40, 'dependency_artifacts': len(deps['artifacts']),
            'scientific_effect': 'NONE'}
