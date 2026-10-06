"""Exact finite controls and small-source inventory; these do not execute Lean."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json
import re
import unittest

HERE = Path(__file__).resolve().parent
NAMES = [
    "entryMatrix", "entryMatrix_isHermitian", "entryMatrix_det", "entryMatrix_trace",
    "entryMatrix_quadratic", "entryMatrix_posDef_iff", "entryMatrix_posDef_iff_first_pos",
    "entryMatrix_posDef_measurableSet", "entryMatrix_char_det", "entryMatrix_mem_spectrum_iff",
    "entryMatrix_spectrum", "entryMatrix_eigenvalues_sq_sum"
]
GRID = tuple(Q(n, 2) for n in range(-3, 4))

class MatrixControls(unittest.TestCase):
    def test_exact_source_inventory(self):
        path = HERE / "CapI4Matrix.lean"
        self.assertTrue(path.is_file(), "missing CapI4Matrix implementation")
        source = path.read_text()
        declarations = re.findall(r"^(?:def|theorem)\s+(\w+)", source, re.M)
        self.assertEqual(declarations, NAMES)
        self.assertEqual(json.loads((HERE / "targets.json").read_text()),
                         ["CapI4Matrix." + n for n in NAMES])
        self.assertNotRegex(source, r"\b(?:sorry|admit|axiom|opaque|unsafe)\b")
        self.assertIn("!![e.1, e.2.1; e.2.1, e.2.2]", source)
    def test_quadratic_completion(self):
        for a, b, d, x, y in product(GRID, repeat=5):
            q = a*x*x + 2*b*x*y + d*y*y
            self.assertEqual(a*q, (a*x+b*y)**2 + (a*d-b*b)*y*y)
    def test_pivots_match_explicit_lower_root_sign(self):
        for a, b, d in product(GRID, repeat=3):
            pivots = a > 0 and a*d-b*b > 0
            spectral = a+d > 0 and (a+d)**2 > (a-d)**2 + 4*b*b
            self.assertEqual(pivots, spectral)
    def test_characteristic_product_and_frobenius(self):
        for t in GRID:
            for x, y, rho in [(0,0,0),(3,4,5),(-3,4,5),(5,-12,13)]:
                a, b, d = t+x, Q(y), t-x
                lo, hi = t-rho, t+rho
                self.assertEqual(lo+hi, a+d)
                self.assertEqual(lo*hi, a*d-b*b)
                self.assertEqual(lo*lo+hi*hi, a*a+2*b*b+d*d)
                for s in GRID:
                    self.assertEqual((s-a)*(s-d)-b*b, (s-lo)*(s-hi))
    def test_boundary_and_det_only_countermodels(self):
        self.assertEqual(Q(-1)*Q(-1)-0, 1)
        self.assertFalse(-1 > 0)  # positive determinant is not positivity
        self.assertEqual(Q(0)*Q(1)-0, 0)  # semidefinite boundary is excluded
        self.assertLess(Q(1)*Q(1)-Q(2)**2, 0)
    def test_negative_controls_are_exact_cone_mutations(self):
        script = (HERE / "replay.sh").read_text()
        self.assertIn("RejectBoundary", script)
        self.assertIn("RejectDetOnly", script)
        self.assertIn("entryMatrix (0, (0, 1))", script)
        self.assertIn("entryMatrix (-1, (0, -1))", script)
        self.assertIn("audit_negative", script)
    def test_contract_has_all_theorem_uses(self):
        contract = (HERE / "Contract.lean").read_text()
        for name in NAMES[1:]:
            self.assertIn("CapI4Matrix." + name, contract)

if __name__ == "__main__":
    unittest.main()
