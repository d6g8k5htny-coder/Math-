import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from fixture_builder import build_fixture, content_id, write_json
from admission import verify_dataset


class AdmissionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.dataset_path, self.policy_path, self.pin = build_fixture(self.root)
        self.dataset = json.loads(self.dataset_path.read_text())
        self.policy = json.loads(self.policy_path.read_text())

    def check(self, repin=True):
        write_json(self.dataset_path, self.dataset)
        write_json(self.policy_path, self.policy)
        if repin:
            self.pin = hashlib.sha256(self.policy_path.read_bytes()).hexdigest()
        return verify_dataset(self.dataset_path, self.policy_path, self.pin)

    def first(self):
        record = self.dataset['records'][0]
        return record, self.policy['artifacts'][record['artifact_id']]

    def alter(self, field, change):
        _, artifact = self.first()
        reference = artifact[field]
        path = self.root / reference['path']
        payload = json.loads(path.read_text())
        change(payload)
        write_json(path, payload)
        reference['sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()

    def rebind_first(self):
        # Model a newly operator-pinned proposal so deeper semantic controls are
        # reached without treating an old content ID as mutable.
        record, artifact = self.first()
        old_id = record['artifact_id']
        keys = ('task_id', 'target', 'target_ref', 'source_ref', 'proof_ref',
                'runtime_id', 'baseline_id', 'kind')
        new_id = content_id('artifact', {key: artifact[key] for key in keys})
        self.alter('acceptance_receipt_ref', lambda a: a.update(
            artifact_id=new_id, task_id=artifact['task_id'], target=artifact['target'],
            source_sha256=artifact['source_ref']['sha256'],
            proof_sha256=artifact['proof_ref']['sha256'],
            target_sha256=artifact['target_ref']['sha256']))
        self.alter('provenance_ref', lambda a: a.update(artifact_id=new_id))
        self.alter('attestation_ref', lambda a: a.update(
            artifact_id=new_id, provenance_sha256=artifact['provenance_ref']['sha256']))
        self.policy['artifacts'].pop(old_id)
        self.policy['artifacts'][new_id] = artifact
        record['artifact_id'] = new_id
        record['id'] = content_id('record', {key: record[key] for key in
                                            ('artifact_id', 'split', 'families')})

    def denied(self, report, code):
        self.assertEqual(report['status'], 'denied')
        self.assertIn(code, [x['code'] for x in report['violations']])
        self.assertFalse(report['scientific_corpus_established'])
        self.assertFalse(report['actual_training_authorized'])

    def test_synthetic_positive_is_fixture_only(self):
        report = self.check()
        self.assertEqual(report['status'], 'policy_admitted_fixture')
        self.assertEqual(len(report['records']), 2)
        self.assertFalse(report['kernel_executed'])
        self.assertFalse(report['scientific_corpus_established'])
        self.assertFalse(report['actual_training_authorized'])

    def test_tampered_receipt_rejected_without_policy_repin(self):
        _, artifact = self.first()
        path = self.root / artifact['acceptance_receipt_ref']['path']
        path.write_text('{}')
        self.denied(self.check(), 'artifact_digest_mismatch')

    def test_missing_attestation_default_denies(self):
        _, artifact = self.first()
        del artifact['attestation_ref']
        self.denied(self.check(), 'missing_attestation')

    def test_missing_exposure_review_default_denies(self):
        self.alter('attestation_ref', lambda a: a.pop('exposure_reviewed'))
        self.denied(self.check(), 'exposure_review_required')

    def test_exposed_known_endpoint_cannot_be_overridden(self):
        _, artifact = self.first()
        artifact['target'] = 'UniversalLaw.Spec.P15.RhoStarEnclosure'
        self.dataset['claimed_eligible'] = True
        self.denied(self.check(), 'known_source_exposed_target')

    def test_old_self_hypothesis_trace_denied_even_claimed_eligible(self):
        self.alter('provenance_ref', lambda a: a.update(origin_id='ul-integrated-discovery:serial_transition_traces'))
        self.dataset['claimed_eligible'] = True
        self.denied(self.check(), 'historic_blocked_trace')

    def test_self_local_attestation_denied(self):
        self.alter('attestation_ref', lambda a: a.update(self_theorem_local=True))
        self.denied(self.check(), 'self_local_forbidden')

    def test_family_overlap_rejected_after_recomputed_record_id(self):
        a, b = self.dataset['records']
        b['families']['derivation'] = a['families']['derivation']
        identity = {k: b[k] for k in ('artifact_id', 'split', 'families')}
        b['id'] = content_id('record', identity)
        self.denied(self.check(), 'cross_split_family_overlap')

    def test_duplicate_record_ids_rejected(self):
        self.dataset['records'].append(copy.deepcopy(self.dataset['records'][0]))
        self.denied(self.check(), 'duplicate_record_id')

    def test_immutable_record_identity_rejects_changed_split(self):
        self.dataset['records'][0]['split'] = 'validation'
        self.denied(self.check(), 'record_identity_mismatch')

    def test_policy_pin_cannot_be_changed_by_proposal(self):
        self.policy['reviewers'].append('dataset-author')
        self.denied(self.check(repin=False), 'policy_digest_mismatch')

    def test_forbidden_axiom_even_trusted_receipt_denied(self):
        self.alter('acceptance_receipt_ref', lambda a: a.update(axioms=['sorryAx']))
        self.denied(self.check(), 'forbidden_axiom')

    def test_open_proof_even_trusted_receipt_denied(self):
        self.alter('acceptance_receipt_ref', lambda a: a.update(root_closed=False, free_variable_count=1))
        self.denied(self.check(), 'root_not_closed')

    def test_metavariable_even_trusted_receipt_denied(self):
        self.alter('acceptance_receipt_ref', lambda a: a.update(metavariable_count=1))
        self.denied(self.check(), 'open_proof')

    def test_weaker_or_different_target_receipt_rejected(self):
        self.alter('acceptance_receipt_ref', lambda a: a.update(target='False -> False'))
        self.denied(self.check(), 'receipt_binding_mismatch')

    def test_unreviewed_provenance_denied(self):
        self.alter('provenance_ref', lambda a: a.update(disclosure_complete=False))
        self.denied(self.check(), 'provenance_incomplete')

    def test_source_exposure_attestation_denied(self):
        self.alter('attestation_ref', lambda a: a.update(source_exposed=True))
        self.denied(self.check(), 'source_exposed')

    def test_unknown_artifact_denied(self):
        self.dataset['records'][0]['artifact_id'] = 'artifact:' + '0' * 64
        self.denied(self.check(), 'unknown_trusted_artifact')

    def test_path_escape_denied(self):
        _, artifact = self.first()
        artifact['proof_ref']['path'] = '../outside'
        self.rebind_first()
        self.denied(self.check(), 'unsafe_artifact_path')

    def test_symlink_denied(self):
        _, artifact = self.first()
        path = self.root / artifact['proof_ref']['path']
        target = path.with_suffix('.real')
        path.rename(target)
        path.symlink_to(target.name)
        self.denied(self.check(), 'unsafe_artifact_path')

    def test_nonobject_dataset_is_clean_denial(self):
        self.dataset = []
        self.denied(self.check(), 'dataset_schema')

    def test_omitted_family_is_default_denial(self):
        self.dataset['records'][0]['families']['source'] = []
        self.denied(self.check(), 'families_required')

    def test_all_49_known_targets_are_blocked(self):
        blocked = json.loads((ROOT / 'blocked_evidence.json').read_text())
        self.assertEqual(len(blocked['targets']), 49)
        _, artifact = self.first()
        for target in blocked['targets']:
            with self.subTest(target=target):
                artifact['target'] = target
                self.denied(self.check(), 'known_source_exposed_target')

    def test_known_proof_hash_cannot_be_hidden_by_target_rename(self):
        blocked = json.loads((ROOT / 'blocked_evidence.json').read_text())
        _, artifact = self.first()
        artifact['proof_ref']['sha256'] = blocked['source_hashes'][0]
        self.denied(self.check(), 'known_blocked_evidence_hash')

    def test_both_historical_export_hashes_are_permanently_blocked(self):
        blocked = json.loads((ROOT / 'blocked_evidence.json').read_text())
        _, artifact = self.first()
        self.assertEqual(len(blocked['historical_files']), 2)
        for historical in blocked['historical_files']:
            with self.subTest(path=historical['path']):
                artifact['source_ref']['sha256'] = historical['sha256']
                self.denied(self.check(), 'known_blocked_evidence_hash')

    def test_relabelled_open_context_payload_stays_blocked(self):
        _, artifact = self.first()
        path = self.root / artifact['proof_ref']['path']
        path.write_text('{"schema":"new-label","context":"OPEN_CONTEXT_ONLY","eligible":true}')
        artifact['proof_ref']['sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
        self.rebind_first()
        self.denied(self.check(), 'historic_blocked_trace')

    def test_unfrozen_family_denied(self):
        self.policy['family_split'].clear()
        self.denied(self.check(), 'frozen_family_split_mismatch')

    def test_attestation_split_requires_list(self):
        self.alter('attestation_ref', lambda a: a.update(permitted_splits='train'))
        self.denied(self.check(), 'reviewed_family_or_split_mismatch')

    def test_empty_dataset_denied(self):
        self.dataset['records'] = []
        self.denied(self.check(), 'dataset_schema')

    def test_untrusted_reviewer_denied(self):
        self.alter('attestation_ref', lambda a: a.update(reviewer='dataset-author'))
        self.denied(self.check(), 'reviewer_not_trusted')

    def test_fake_boolean_is_not_acceptance(self):
        self.alter('acceptance_receipt_ref', lambda a: a.update(root_closed='true'))
        self.denied(self.check(), 'boolean_metadata_type')

    def test_missing_independent_pin_denies(self):
        report = verify_dataset(self.dataset_path, self.policy_path, '')
        self.denied(report, 'independent_policy_pin_required')

    def test_duplicate_json_policy_key_denies(self):
        self.policy_path.write_text('{"schema":"x","schema":"ul-corpus-trusted-policy-v1"}')
        pin = hashlib.sha256(self.policy_path.read_bytes()).hexdigest()
        self.denied(verify_dataset(self.dataset_path, self.policy_path, pin), 'duplicate_json_key')

    def test_nested_legacy_self_dependency_flag_cannot_be_relabelled(self):
        self.alter('provenance_ref', lambda a: a.update(
            renamed_metadata={'self_dependency_not_audited': True, 'claimed_eligible': True}))
        self.denied(self.check(), 'historic_blocked_trace')

    def test_receipt_exposure_cannot_be_overridden_by_new_attestation(self):
        self.alter('acceptance_receipt_ref', lambda a: a.update(source_exposed=True))
        self.denied(self.check(), 'source_exposed')

    def test_receipt_declared_ineligibility_cannot_be_overridden(self):
        self.alter('acceptance_receipt_ref', lambda a: a.update(training_eligible=False))
        self.denied(self.check(), 'receipt_declares_ineligible')

    def test_malformed_optional_receipt_booleans_deny_after_trusted_repin(self):
        fields = ('source_exposed', 'training_eligible', 'discovery_eligible')
        for field in fields:
            for malformed in (0, 1, 0.0, 1.0, None, 'true', 'false'):
                with self.subTest(field=field, value=malformed):
                    self.alter('acceptance_receipt_ref',
                               lambda a: [a.pop(key, None) for key in fields])
                    self.alter('acceptance_receipt_ref',
                               lambda a: a.update({field: malformed}))
                    self.denied(self.check(), 'boolean_metadata_type')

    def test_malformed_boolean_metadata_in_each_document_denies(self):
        for document, field in (('provenance_ref', 'blocked_trace'),
                                ('attestation_ref', 'exposure_reviewed')):
            with self.subTest(document=document):
                original = copy.deepcopy(self.policy)
                _, artifact = self.first()
                path = self.root / artifact[document]['path']
                saved = path.read_bytes()
                self.alter(document, lambda a: a.update({field: 1}))
                self.denied(self.check(), 'boolean_metadata_type')
                path.write_bytes(saved)
                self.policy = original
        self.policy['source_exposed'] = 0
        self.denied(self.check(), 'boolean_metadata_type')
        del self.policy['source_exposed']
        self.dataset['claimed_eligible'] = 1
        self.denied(self.check(), 'boolean_metadata_type')

    def test_huge_integer_json_returns_typed_denial(self):
        self.dataset_path.write_text('{"schema":"ul-corpus-proposal-v1","large":' + '1' * 5000 + '}')
        self.denied(verify_dataset(self.dataset_path, self.policy_path, self.pin), 'invalid_json')

    def test_surrogate_family_string_returns_typed_denial(self):
        self.dataset['records'][0]['families']['source'] = ['\ud800']
        self.denied(self.check(), 'invalid_unicode')

    def test_exponent_overflow_unused_metadata_cannot_admit(self):
        text = json.dumps(self.dataset)
        self.dataset_path.write_text(text[:-1] + ',"unused":1e10000}')
        self.denied(verify_dataset(self.dataset_path, self.policy_path, self.pin), 'nonfinite_json')

    def test_nonfinite_constants_deny(self):
        for constant in ('NaN', 'Infinity', '-Infinity', '-1e10000'):
            with self.subTest(constant=constant):
                text = json.dumps(self.dataset)
                self.dataset_path.write_text(text[:-1] + ',"unused":' + constant + '}')
                self.denied(verify_dataset(self.dataset_path, self.policy_path, self.pin), 'nonfinite_json')

    def test_embedded_nul_in_artifact_path_returns_denial(self):
        _, artifact = self.first()
        artifact['proof_ref']['path'] = 'artifacts/0/proof\x00.txt'
        self.rebind_first()
        self.denied(self.check(), 'unsafe_artifact_path')

    def test_output_boolean_metadata_remains_typed(self):
        report = self.check()
        for name in ('kernel_executed', 'scientific_corpus_established',
                     'actual_training_authorized'):
            self.assertIs(report[name], False)
        self.assertIs(report['documented_policy_admission'], True)
        self.assertIs(report['claimed_eligibility_ignored'], True)
        for record in report['records']:
            self.assertIs(record['synthetic_fixture'], True)


if __name__ == '__main__':
    unittest.main()
