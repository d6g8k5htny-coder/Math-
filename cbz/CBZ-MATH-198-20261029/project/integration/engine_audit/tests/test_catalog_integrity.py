"""Catalog assertions reject disposable mutations of real saved artifacts."""
import copy
import json
from pathlib import Path
import shutil
import tempfile
import unittest

import catalog

class CatalogIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.prior = self.root/'prior'
        shutil.copytree(catalog.PRIOR, self.prior)
        self.project = self.root/'project'
        # The independently archived source bytes are the fixture. Only the
        # seventeen closed source-chain modules belong to this binding.
        shutil.copytree(self.prior/'evidence/final01/frozen_sources', self.project/'formal')
        self.path = self.root/'catalog.json'
        shutil.copyfile(catalog.CATALOG, self.path)
        self.original = json.loads(self.path.read_text())
    def verify(self):
        return catalog.verify_catalog(self.path, project=self.project, prior=self.prior)
    def write(self, path, value):
        path.write_text(json.dumps(value, ensure_ascii=False))
    def test_all_49_source_bindings_replay_from_portable_fixture(self):
        value = self.verify()
        self.assertEqual(len(value['endpoints']), 49)
        full = next(e for e in value['endpoints'] if e['id'] == 'p15.FullTransformedPriceBudget')
        self.assertIn('∀ K : ℕ, paletteNumber F.b F.H F.d ≤ K →', full['statement'])
        self.assertIn('coverCost F K c ≤ cappedHazard rhoStar (mu F p)', full['statement'])
        self.assertEqual(full['proof_source_sha256'], '01234a50ceafa98e79cff97b171cda46ccb717537fb0fea4a1b2e31e5f6fecb1')
    def test_target_theorem_body_source_and_training_tamper_each_reject(self):
        cases = [('target', 'UniversalLaw.Spec.P15.UnrestrictedDownset'),
                 ('theorem', 'UniversalLaw.P15Closure.fullTransformedPriceBudget'),
                 ('statement', 'def PaletteNumberAttained : Prop := True\n'),
                 ('statement_sha256', '0'*64), ('proof_source_sha256', '0'*64),
                 ('source_exposed', False), ('training_eligible', True)]
        for field, replacement in cases:
            with self.subTest(field=field):
                changed = copy.deepcopy(self.original)
                changed['endpoints'][0][field] = replacement
                self.write(self.path, changed)
                with self.assertRaises(ValueError): self.verify()
        self.write(self.path, self.original)
    def test_python_equal_but_differently_typed_metadata_rejects(self):
        for field, replacement in (('training_eligible', 0), ('source_exposed', 1),
                                   ('proof_source_line', 175.0)):
            with self.subTest(field=field):
                changed = copy.deepcopy(self.original)
                changed['endpoints'][0][field] = replacement
                self.write(self.path, changed)
                with self.assertRaises(ValueError): self.verify()
                certificate = self.root/'certificate.json'
                self.write(certificate, catalog.export_value(changed, changed['endpoints'][0]['target']))
                with self.assertRaises(ValueError):
                    catalog.verify_certificate(certificate, catalog_path=self.path,
                                               project=self.project, prior=self.prior)
                self.write(self.path, self.original)
                # The independently trusted catalog stays unchanged, while an
                # exported record alone is given a Python-equal wrong type.
                value = catalog.export_value(self.original, self.original['endpoints'][0]['target'])
                value['endpoint'][field] = replacement
                self.write(certificate, value)
                with self.assertRaises(ValueError):
                    catalog.verify_certificate(certificate, catalog_path=self.path,
                                               project=self.project, prior=self.prior)

    def test_duplicate_or_omitted_endpoint_cannot_replace_coverage(self):
        for endpoints in (self.original['endpoints'][:-1],
                          self.original['endpoints'][:-1]+[self.original['endpoints'][0]]):
            changed = copy.deepcopy(self.original)
            changed['endpoints'] = endpoints
            self.write(self.path, changed)
            with self.assertRaises(ValueError): self.verify()
    def test_coherently_changed_catalog_and_export_still_reject(self):
        changed = copy.deepcopy(self.original)
        changed['endpoints'][0]['target'] = 'UniversalLaw.Spec.P15.FalseSubstitute'
        self.write(self.path, changed)
        # An internally consistent export digest is not an admission authority.
        value = catalog.export_value(changed, 'UniversalLaw.Spec.P15.FalseSubstitute')
        certificate = self.root/'certificate.json'
        self.write(certificate, value)
        with self.assertRaises(ValueError):
            catalog.verify_certificate(certificate, catalog_path=self.path,
                                       project=self.project, prior=self.prior)
    def test_certificate_metadata_tamper_rejects_even_with_unchanged_proof_source(self):
        value = catalog.export_value(self.original, 'p15.FullTransformedPriceBudget')
        certificate = self.root/'certificate.json'
        self.write(certificate, value)
        catalog.verify_certificate(certificate, catalog_path=self.path,
                                   project=self.project, prior=self.prior)
        value['endpoint']['training_eligible'] = True
        self.write(certificate, value)
        with self.assertRaises(ValueError):
            catalog.verify_certificate(certificate, catalog_path=self.path,
                                       project=self.project, prior=self.prior)
    def test_current_supporting_proof_module_drift_rejects(self):
        source = self.project/'formal/Closure/RatioGate.lean'
        source.write_text(source.read_text()+'\n-- changed supporting module\n')
        with self.assertRaisesRegex(ValueError, 'current copied formal source drift'): self.verify()
    def test_changed_original_statement_cannot_be_reclassified_by_metadata(self):
        source = self.project/'formal/Specifications/P15.lean'
        source.write_text(source.read_text().replace('def FullTransformedPriceBudget ', 'def WeakerFullTransformedPriceBudget '))
        changed = copy.deepcopy(self.original)
        changed['provenance']['copied_formal_sources_sha256']['formal/Specifications/P15.lean'] = catalog.sha(source)
        self.write(self.path, changed)
        with self.assertRaisesRegex(ValueError, 'current copied formal source drift'): self.verify()
    def test_saved_audit_body_type_axiom_rows_are_bound_to_sealed_stream(self):
        source = self.prior/'evidence/final01/16-Completion.FinalAudit/stdout.txt'
        source.write_text(source.read_text().replace('|closed|kernel|declaration|', '|closed|unverified|declaration|', 1))
        with self.assertRaisesRegex(ValueError, 'prior evidence hash mismatch'): self.verify()
    def test_receipt_path_tamper_and_coherent_manifest_repin_both_reject(self):
        result_path = self.prior/'evidence/final01/results.json'
        value = json.loads(result_path.read_text())
        value['records'][0]['receipt'] = '../../outside/receipt.json'
        self.write(result_path, value)
        with self.assertRaisesRegex(ValueError, 'prior evidence hash mismatch'): self.verify()
        manifest_path = self.prior/'checksum_manifest.json'
        manifest = json.loads(manifest_path.read_text())
        manifest['files']['evidence/final01/results.json'] = catalog.sha(result_path)
        self.write(manifest_path, manifest)
        with self.assertRaisesRegex(ValueError, 'trust anchor mismatch'): self.verify()
    def test_stream_path_escape_and_symlink_are_rejected(self):
        for name in ('/tmp/outside', '../outside', 'a/../../outside', './same', 'a//b'):
            with self.subTest(name=name), self.assertRaises(ValueError):
                catalog.file_at(self.prior, name)
        source = self.project/'formal/Specifications/P15.lean'
        outside = self.root/'spec.lean'
        source.rename(outside)
        source.symlink_to(outside)
        with self.assertRaisesRegex(ValueError, 'symlink'): self.verify()

if __name__ == '__main__': unittest.main()
