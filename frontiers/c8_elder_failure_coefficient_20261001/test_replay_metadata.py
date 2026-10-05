"""Reject false publication metadata without rerunning the expensive cubature."""
import copy
import json
from pathlib import Path
import unittest

import certificate as C


class ReplayMetadataTests(unittest.TestCase):
    def setUp(self):
        # Small raw enclosures exercise the real derivation and comparator.
        self.raw = {'leaves': {'fixture': 1}, 'J': {
            k: {'J_fail': (4.0, 4.1), 'J_2': (1.0, 1.1),
                'E2B': (1.0, 1.1), 'E2T': (2.0, 2.1),
                'EV_boxes': (0.1, 0.2), 'EH2_boxes': (0.2, 0.3),
                'tail': 0.01}
            for k in (0.5, 1.0, 2.0)}}
        self.doc = C.document(self.raw)
        published = json.loads(Path(C.HERE, 'RESULTS.json').read_text())
        for key in ('object', 'scientific_effect', 'certified', 'arithmetic', 'parameters'):
            self.doc[key] = copy.deepcopy(published[key])

    def test_published_metadata_accepts_valid_replay(self):
        self.assertEqual(C.compare(self.doc, self.raw), [])

    def test_changed_header_is_rejected(self):
        for key, value in [('object', 'different packet'), ('scientific_effect', 'ACCEPT'),
                           ('certified', False), ('certified', 1), ('arithmetic', 'exact')]:
            with self.subTest(key=key, value=value):
                doc = copy.deepcopy(self.doc)
                doc[key] = value
                self.assertTrue(C.compare(doc, self.raw))

    def test_changed_parameters_are_rejected(self):
        for key, value in [('k', [0.5, 1.0]), ('tol3', {'V': 1e-2, 'H2': 1e-8}),
                           ('tol4', 1e-2), ('box_half_width_sigma', 9.0),
                           ('initial_cells', 4), ('initial_k_cells', 4),
                           ('k_split_scale', 0.9), ('k_elementary_level', 4)]:
            with self.subTest(key=key):
                doc = copy.deepcopy(self.doc)
                doc['parameters'][key] = value
                self.assertTrue(C.compare(doc, self.raw))

    def test_missing_or_extra_header_is_rejected(self):
        for key in ('object', 'scientific_effect', 'certified', 'arithmetic', 'parameters'):
            with self.subTest(missing=key):
                doc = copy.deepcopy(self.doc)
                del doc[key]
                self.assertTrue(C.compare(doc, self.raw))
        doc = copy.deepcopy(self.doc)
        doc['unverified_claim'] = True
        self.assertTrue(C.compare(doc, self.raw))

    def test_result_and_leaf_checks_remain_active(self):
        doc = copy.deepcopy(self.doc)
        doc['leaves']['fixture'] = 2
        self.assertTrue(C.compare(doc, self.raw))
        doc = copy.deepcopy(self.doc)
        doc['results']['k=0.5']['J_fail'] = ['0', '1']
        self.assertTrue(C.compare(doc, self.raw))


if __name__ == '__main__':
    unittest.main()
