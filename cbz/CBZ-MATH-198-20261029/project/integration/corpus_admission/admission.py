"""Default-deny integrity and documented-policy admission, never a proof/novelty oracle."""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path, PurePosixPath
import re

BLOCKED_PATH = Path(__file__).with_name('blocked_evidence.json')
BLOCKED_SHA256 = '9b4ea3af111abbad2184f4fba3c19511b0d9b1d6f34164b4392d2bc28dc169bb'
ALLOWED_AXIOMS = frozenset(('propext', 'Classical.choice', 'Quot.sound'))
SPLITS = frozenset(('train', 'validation', 'test'))
FAMILY_TYPES = ('theorem', 'derivation', 'source', 'transport')
BINDING_FIELDS = ('task_id', 'target', 'target_ref', 'source_ref', 'proof_ref',
                  'runtime_id', 'baseline_id', 'kind')
MAX_BYTES = 8 * 1024 * 1024
MAX_INTEGER_DIGITS = 4300
BOOLEAN_METADATA = frozenset((
    'root_closed', 'kernel_checked', 'checked_insertion', 'exact_target_match',
    'synthetic_fixture', 'source_exposed', 'training_eligible', 'discovery_eligible',
    'blocked_trace', 'disclosure_complete', 'self_theorem_local', 'exposure_reviewed',
    'proof_dependency_reviewed', 'source_lineage_reviewed', 'claimed_eligible',
    'self_dependency_not_audited', 'closed_candidate_terms_recorded',
    'synthetic_current_theorem_local', 'documented_policy_admission',
    'kernel_executed', 'scientific_corpus_established', 'actual_training_authorized',
    'claimed_eligibility_ignored',
))


class AdmissionError(ValueError):
    def __init__(self, code):
        self.code = code
        super().__init__(code)


def require(condition, code):
    if not condition:
        raise AdmissionError(code)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    _validate_json_scalars(value)
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False,
                      allow_nan=False).encode()


def _validate_json_scalars(value):
    # JSON's booleans and integers are different types. Python's False == 0
    # must never turn malformed declared metadata into reviewed policy evidence.
    stack = [value]
    while stack:
        current = stack.pop()
        if isinstance(current, dict):
            for key, nested in current.items():
                require(isinstance(key, str), 'invalid_json_key')
                try:
                    key.encode('utf-8', errors='strict')
                except UnicodeError as error:
                    raise AdmissionError('invalid_unicode') from error
                if key in BOOLEAN_METADATA:
                    require(type(nested) is bool, 'boolean_metadata_type')
                stack.append(nested)
        elif isinstance(current, list):
            stack.extend(current)
        elif isinstance(current, str):
            try:
                current.encode('utf-8', errors='strict')
            except UnicodeError as error:
                raise AdmissionError('invalid_unicode') from error
        elif isinstance(current, float):
            require(math.isfinite(current), 'nonfinite_json')


def _finite_float(token):
    value = float(token)
    require(math.isfinite(value), 'nonfinite_json')
    return value


def _bounded_integer(token):
    require(len(token.lstrip('-')) <= MAX_INTEGER_DIGITS, 'invalid_json')
    return int(token)


def content_id(prefix, value):
    return prefix + ':' + digest(canonical(value))


def _object_pairs(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate_json_key')
        result[key] = value
    return result


def read_bytes(path):
    require(path.is_file() and not path.is_symlink(), 'missing_or_unsafe_file')
    require(path.stat().st_size <= MAX_BYTES, 'file_size_limit')
    return path.read_bytes()


def parse(data):
    try:
        value = json.loads(data, object_pairs_hook=_object_pairs, parse_float=_finite_float,
                           parse_int=_bounded_integer,
                           parse_constant=lambda _: (_ for _ in ()).throw(AdmissionError('nonfinite_json')))
        _validate_json_scalars(value)
        return value
    except AdmissionError:
        raise
    except (UnicodeError, ValueError, RecursionError) as error:
        raise AdmissionError('invalid_json') from error


def _string(value):
    return isinstance(value, str) and bool(value.strip())


def _sha(value):
    return isinstance(value, str) and re.fullmatch('[0-9a-f]{64}', value) is not None


def _read_ref(base, reference):
    require(isinstance(reference, dict) and set(reference) == {'path', 'sha256'}, 'artifact_reference_schema')
    relative = reference['path']
    require(_string(relative) and _sha(reference['sha256']), 'artifact_reference_schema')
    require('\x00' not in relative, 'unsafe_artifact_path')
    posix = PurePosixPath(relative)
    require(not posix.is_absolute() and relative == posix.as_posix()
            and all(part not in ('', '.', '..') for part in posix.parts), 'unsafe_artifact_path')
    path = base
    for part in posix.parts:
        path = path / part
        require(not path.is_symlink(), 'unsafe_artifact_path')
    require(path.resolve().is_relative_to(base.resolve()), 'unsafe_artifact_path')
    data = read_bytes(path)
    require(digest(data) == reference['sha256'], 'artifact_digest_mismatch')
    return data


def _families(value):
    require(isinstance(value, dict) and set(value) == set(FAMILY_TYPES), 'families_required')
    for name in FAMILY_TYPES:
        values = value[name]
        require(isinstance(values, list) and all(_string(x) for x in values)
                and len(values) == len(set(values)), 'families_required')
        if name != 'transport':
            require(bool(values), 'families_required')
    return value


def _legacy_payload(data):
    # Known raw export hashes are checked separately. These flags catch relabeled
    # legacy payloads without pretending to reconstruct unsaved candidate terms.
    markers = (b'DIAGNOSTIC_ONLY_NOT_DISCOVERY_OR_TRAINING_READY', b'OPEN_CONTEXT_ONLY',
               b'GLOBAL_ENVIRONMENT_ONLY')
    if any(marker in data for marker in markers):
        return True
    candidates = [data] + data.splitlines()
    for line in candidates:
        try:
            value = json.loads(line)
        except (ValueError, UnicodeError, RecursionError):
            continue
        stack = [value]
        while stack:
            nested = stack.pop()
            if isinstance(nested, dict):
                if (nested.get('self_dependency_not_audited') is True
                        or nested.get('closed_candidate_terms_recorded') is False
                        or nested.get('synthetic_current_theorem_local') is True):
                    return True
                stack.extend(nested.values())
            elif isinstance(nested, list):
                stack.extend(nested)
    return False


def _blocked_artifact(artifact, blocked):
    target = artifact.get('target')
    require(target not in blocked['targets'] and not
            (isinstance(target, str) and target.startswith('UniversalLaw.Spec.P15.')),
            'known_source_exposed_target')
    require(artifact.get('task_id') not in blocked['endpoint_ids']
            and target not in blocked['theorems'], 'known_source_exposed_target')
    forbidden = set(blocked['source_hashes']) | {x['sha256'] for x in blocked['historical_files']}
    for key in ('source_ref', 'proof_ref', 'target_ref'):
        reference = artifact.get(key)
        if isinstance(reference, dict):
            require(reference.get('sha256') not in forbidden, 'known_blocked_evidence_hash')


def _validate_record(record, policy, base, blocked):
    require(isinstance(record, dict), 'record_schema')
    artifact_id = record.get('artifact_id')
    require(isinstance(artifact_id, str) and artifact_id in policy['artifacts'], 'unknown_trusted_artifact')
    artifact = policy['artifacts'][artifact_id]
    require(isinstance(artifact, dict), 'trusted_artifact_schema')
    _blocked_artifact(artifact, blocked)
    require('attestation_ref' in artifact, 'missing_attestation')
    require('provenance_ref' in artifact, 'missing_provenance')
    require(all(key in artifact for key in BINDING_FIELDS), 'trusted_artifact_schema')
    binding = {key: artifact[key] for key in BINDING_FIELDS}
    require(artifact_id == content_id('artifact', binding), 'artifact_identity_mismatch')
    for key in ('task_id', 'target', 'runtime_id', 'baseline_id'):
        require(_string(artifact[key]), 'trusted_artifact_schema')
    fixture = artifact['kind'] == 'fixture'
    require(artifact['kind'] in ('fixture', 'candidate'), 'trusted_artifact_schema')
    require(fixture == (policy['mode'] == 'fixture_only'), 'policy_mode_mismatch')
    split = record.get('split')
    require(split in SPLITS, 'split_required')
    families = _families(record.get('families'))
    identity = {'artifact_id': artifact_id, 'split': split, 'families': families}
    require(record.get('id') == content_id('record', identity), 'record_identity_mismatch')
    require(set(record) <= {'id', 'artifact_id', 'split', 'families', 'claimed_eligible'}, 'record_schema')

    payloads = {key: _read_ref(base, artifact[key]) for key in
                ('source_ref', 'proof_ref', 'target_ref', 'acceptance_receipt_ref',
                 'provenance_ref', 'attestation_ref')}
    require(not any(_legacy_payload(value) for value in payloads.values()),
            'historic_blocked_trace')
    receipt = parse(payloads['acceptance_receipt_ref'])
    require(isinstance(receipt, dict) and receipt.get('schema') == 'ul-corpus-root-acceptance-v1',
            'receipt_schema')
    expected = {'artifact_id': artifact_id, 'task_id': artifact['task_id'], 'target': artifact['target'],
                'source_sha256': artifact['source_ref']['sha256'],
                'proof_sha256': artifact['proof_ref']['sha256'],
                'target_sha256': artifact['target_ref']['sha256'],
                'runtime_id': artifact['runtime_id'], 'baseline_id': artifact['baseline_id']}
    require(all(receipt.get(key) == value for key, value in expected.items()), 'receipt_binding_mismatch')
    require(receipt.get('status') == 'accepted', 'receipt_not_accepted')
    require(receipt.get('source_exposed') is not True, 'source_exposed')
    require(receipt.get('training_eligible') is not False
            and receipt.get('discovery_eligible') is not False, 'receipt_declares_ineligible')
    require(receipt.get('root_closed') is True, 'root_not_closed')
    require(receipt.get('kernel_checked') is True and receipt.get('checked_insertion') is True
            and receipt.get('exact_target_match') is True, 'proof_acceptance_incomplete')
    require(type(receipt.get('metavariable_count')) is int and receipt['metavariable_count'] == 0
            and type(receipt.get('free_variable_count')) is int and receipt['free_variable_count'] == 0,
            'open_proof')
    axioms = receipt.get('axioms')
    require(isinstance(axioms, list) and all(isinstance(a, str) for a in axioms)
            and len(axioms) == len(set(axioms)) and set(axioms) <= ALLOWED_AXIOMS, 'forbidden_axiom')
    require(receipt.get('synthetic_fixture') is fixture, 'fixture_label_mismatch')

    provenance = parse(payloads['provenance_ref'])
    require(isinstance(provenance, dict) and provenance.get('schema') == 'ul-corpus-provenance-v1'
            and provenance.get('artifact_id') == artifact_id, 'provenance_binding_mismatch')
    origin = provenance.get('origin_id')
    require(_string(origin), 'provenance_incomplete')
    history = provenance.get('source_history')
    require(isinstance(history, list) and bool(history) and all(_string(x) for x in history)
            and provenance.get('disclosure_complete') is True, 'provenance_incomplete')
    disclosed = '\n'.join([origin, str(provenance.get('historical_trace_id', ''))] + history)
    require(not any(marker in disclosed for marker in blocked['historic_origin_markers'])
            and provenance.get('blocked_trace') is False
            and provenance.get('historical_trace_id') == '', 'historic_blocked_trace')
    require(provenance.get('source_exposed') is False, 'source_exposed')
    require(provenance.get('synthetic_fixture') is fixture, 'fixture_label_mismatch')

    attestation = parse(payloads['attestation_ref'])
    require(isinstance(attestation, dict) and
            attestation.get('schema') == 'ul-corpus-policy-attestation-v1', 'attestation_schema')
    require(attestation.get('artifact_id') == artifact_id and
            attestation.get('provenance_sha256') == artifact['provenance_ref']['sha256'],
            'attestation_binding_mismatch')
    require(_string(attestation.get('review_id')) and attestation.get('reviewer') in policy['reviewers'],
            'reviewer_not_trusted')
    require(attestation.get('source_exposed') is False, 'source_exposed')
    require(attestation.get('self_theorem_local') is False, 'self_local_forbidden')
    require(attestation.get('exposure_reviewed') is True, 'exposure_review_required')
    require(attestation.get('proof_dependency_reviewed') is True and
            attestation.get('source_lineage_reviewed') is True, 'policy_review_required')
    permitted = attestation.get('permitted_splits')
    require(isinstance(permitted, list) and bool(permitted)
            and all(isinstance(value, str) and value in SPLITS for value in permitted)
            and len(permitted) == len(set(permitted)), 'reviewed_family_or_split_mismatch')
    require(attestation.get('families') == families and split in permitted,
            'reviewed_family_or_split_mismatch')
    for family_type, values in families.items():
        for family in values:
            require(policy['family_split'].get(family_type + ':' + family) == split,
                    'frozen_family_split_mismatch')
    require(attestation.get('synthetic_fixture') is fixture, 'fixture_label_mismatch')
    outcome = 'approved_for_fixture' if fixture else 'approved_for_documented_policy'
    require(attestation.get('review_outcome') == outcome, 'policy_review_not_approved')
    return {'id': record['id'], 'task_id': artifact['task_id'], 'artifact_id': artifact_id,
            'split': split, 'admission': 'policy_admitted_fixture' if fixture else 'policy_admitted',
            'synthetic_fixture': fixture}


def verify_dataset(dataset_path, policy_path, expected_policy_sha256):
    """Verify byte bindings and declared admission policy using an out-of-band policy pin.

    Receipts/attestations must be operator-trusted, not supplied by the dataset.
    This checks their content and integrity; it never executes a kernel or proves
    historical non-exposure, reviewer honesty, scientific novelty, or a useful RL corpus.
    """
    result = {'schema': 'ul-corpus-admission-result-v1', 'status': 'denied', 'records': [],
              'violations': [], 'documented_policy_admission': False,
              'kernel_executed': False, 'scientific_corpus_established': False,
              'actual_training_authorized': False, 'claimed_eligibility_ignored': True}
    try:
        blocked_bytes = read_bytes(BLOCKED_PATH)
        require(digest(blocked_bytes) == BLOCKED_SHA256, 'blocked_registry_digest_mismatch')
        blocked = parse(blocked_bytes)
        require(blocked.get('known_endpoint_count') == 49 and len(blocked.get('targets', [])) == 49,
                'blocked_registry_schema')
        require(_sha(expected_policy_sha256), 'independent_policy_pin_required')
        policy_path, dataset_path = Path(policy_path), Path(dataset_path)
        policy_bytes, dataset_bytes = read_bytes(policy_path), read_bytes(dataset_path)
        require(digest(policy_bytes) == expected_policy_sha256, 'policy_digest_mismatch')
        result.update(policy_sha256=expected_policy_sha256, dataset_sha256=digest(dataset_bytes),
                      blocked_registry_sha256=BLOCKED_SHA256)
        policy, dataset = parse(policy_bytes), parse(dataset_bytes)
        require(isinstance(policy, dict) and policy.get('schema') == 'ul-corpus-trusted-policy-v1'
                and _string(policy.get('policy_id')) and policy.get('mode') in
                ('fixture_only', 'attested_candidates') and isinstance(policy.get('artifacts'), dict)
                and isinstance(policy.get('family_split'), dict), 'policy_schema')
        reviewers = policy.get('reviewers')
        require(isinstance(reviewers, list) and bool(reviewers) and all(_string(x) for x in reviewers)
                and len(reviewers) == len(set(reviewers)), 'policy_reviewers_required')
        require(isinstance(dataset, dict) and dataset.get('schema') == 'ul-corpus-proposal-v1'
                and _string(dataset.get('dataset_id')) and isinstance(dataset.get('records'), list)
                and bool(dataset['records']), 'dataset_schema')
        seen_ids, seen_artifacts, seen_tasks, family_uses = set(), set(), set(), {}
        for record in dataset['records']:
            try:
                require(isinstance(record, dict), 'record_schema')
                identifier = record.get('id')
                require(isinstance(identifier, str), 'record_schema')
                require(identifier not in seen_ids, 'duplicate_record_id')
                seen_ids.add(identifier)
                artifact_id = record.get('artifact_id')
                require(isinstance(artifact_id, str), 'record_schema')
                require(artifact_id not in seen_artifacts, 'duplicate_artifact_id')
                seen_artifacts.add(artifact_id)
                artifact = policy['artifacts'].get(artifact_id, {})
                if isinstance(artifact, dict) and _string(artifact.get('task_id')):
                    require(artifact['task_id'] not in seen_tasks, 'duplicate_task_id')
                    seen_tasks.add(artifact['task_id'])
                families = _families(record.get('families'))
                split = record.get('split')
                require(isinstance(split, str) and split in SPLITS, 'split_required')
                for family_type, values in families.items():
                    for family in values:
                        key = family_type + ':' + family
                        family_uses.setdefault(key, set()).add(split)
                accepted = _validate_record(record, policy, policy_path.parent, blocked)
                result['records'].append(accepted)
            except (ValueError, UnicodeError, OSError, KeyError, TypeError, RecursionError) as error:
                code = error.code if isinstance(error, AdmissionError) else 'malformed_record_or_missing_evidence'
                result['violations'].append({'record_id': record.get('id') if isinstance(record, dict) else None,
                                              'code': code})
        for family, splits in sorted(family_uses.items()):
            if len(splits) > 1:
                result['violations'].append({'record_id': None, 'code': 'cross_split_family_overlap',
                                              'family': family, 'splits': sorted(splits)})
        if not result['violations']:
            result['status'] = 'policy_admitted_fixture' if policy['mode'] == 'fixture_only' else 'policy_admitted'
            result['documented_policy_admission'] = True
        else:
            # No row-level positive label survives a dataset-level refusal.
            result['records'] = [dict(record, admission='denied_with_dataset') for record in result['records']]
    except (ValueError, UnicodeError, OSError, KeyError, TypeError, RecursionError) as error:
        code = error.code if isinstance(error, AdmissionError) else 'malformed_input_or_missing_evidence'
        result['violations'].append({'record_id': None, 'code': code})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('dataset', type=Path)
    parser.add_argument('--policy', required=True, type=Path)
    parser.add_argument('--expected-policy-sha256', required=True,
                        help='Independent operator-trusted pin; do not read this from the proposal')
    args = parser.parse_args()
    result = verify_dataset(args.dataset, args.policy, args.expected_policy_sha256)
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0 if result['documented_policy_admission'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
