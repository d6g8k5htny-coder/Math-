"""Exact contract and finite premise controls. Not a Gaussian model or Lean proof."""
from fractions import Fraction as F
from pathlib import Path
import hashlib, re, unittest
HERE=Path(__file__).resolve().parent
NAMES=['jointLaw_of_independence','residual_law_mass','independent_weight_bound_ae']
class ContractTests(unittest.TestCase):
    def test_contract_identity(self):
        self.assertEqual(hashlib.sha256((HERE/'Contract.lean').read_bytes()).hexdigest(), 'b21f5891e75cf0697bf265078fed96c6d34c0c596096831069a07566c047abd2')
    def test_inventory_without_admissions(self):
        source=(HERE/'CapI4Independent.lean').read_text()
        text=re.sub(r'/\-.*?\-/','',source,flags=re.S)
        self.assertIsNone(re.search(r'\b(sorry|admit|axiom|unsafe)\b',text))
        self.assertIn(re.findall(r'^theorem (\w+)',source,re.M), [[],NAMES])
    def test_original_independence_not_conditioned_independence(self):
        law={(j,b):F(1,4) for j in (0,1) for b in (0,1)}
        self.assertEqual(sum(law.values()),1)
        self.assertEqual(sum(w*j*b for (j,b),w in law.items()),F(1,4))
        selected={(j,b):2*w for (j,b),w in law.items() if j==b}
        self.assertEqual(sum(selected.values()),1)
        self.assertEqual(sum(w*j*b for (j,b),w in selected.items()),F(1,2))
    def test_mass_cannot_be_dropped_for_arbitrary_measure(self):
        for mass in [F(0),F(1),F(2),F(7,3)]:
            self.assertEqual(sum([mass*F(3,5),mass*F(2,5)]),mass)
        self.assertNotEqual(2*F(60),F(60))
    def test_null_weight_exception(self):
        masses=[F(1,2),F(1,2),F(0)]
        weights=[F(1),F(2),F(10**6)]
        bound=[F(2),F(2),F(0)]
        self.assertFalse(all(w<=b for w,b in zip(weights,bound)))
        self.assertTrue(all(m==0 or w<=b for m,w,b in zip(masses,weights,bound)))
        self.assertLessEqual(sum(m*w for m,w in zip(masses,weights)),sum(m*b for m,b in zip(masses,bound)))
if __name__=='__main__':unittest.main(verbosity=2)
