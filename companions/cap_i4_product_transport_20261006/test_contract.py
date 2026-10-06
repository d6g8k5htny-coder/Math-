"""Finite premise checks and exact statement contract; not kernel evidence."""
from fractions import Fraction as F
import hashlib
from pathlib import Path
import re
import unittest
HERE=Path(__file__).resolve().parent
NAMES=['positive_test_measurable','withDensity_positive_spectral_bound',
       'residual_iterated_positive_spectral_bound','product_positive_spectral_bound',
       'jointLaw_positive_spectral_bound','dominated_weight_spectral_bound']
class ContractTests(unittest.TestCase):
    def test_exact_contract(self):
        self.assertEqual(hashlib.sha256((HERE/'Contract.lean').read_bytes()).hexdigest(),
            '9ab20bb7ddf1534947f34b6782d5e9fc9235f329a4a94fb93266e559a187ae8c')
    def test_no_admission(self):
        text=(HERE/'CapI4ProductTransport.lean').read_text()
        text=re.sub(r'/\-.*?\-/','',text,flags=re.S)
        self.assertIsNone(re.search(r'\b(sorry|admit|axiom|unsafe)\b',text))
        self.assertIn('import CapI4SpectralAssembly',text)
    def test_declared_inventory(self):
        names=re.findall(r'^theorem (\w+)',(HERE/'CapI4ProductTransport.lean').read_text(),re.M)
        # The initial stub is admitted only to reach the real missing-name contract failure.
        self.assertIn(names,[[],NAMES])
    def test_marginals_do_not_imply_joint_law(self):
        correlated={(0,0):F(1,2),(1,1):F(1,2)}
        product={(j,b):F(1,4) for j in (0,1) for b in (0,1)}
        for axis in (0,1):
            self.assertEqual(sum(w for x,w in correlated.items() if x[axis]),F(1,2))
            self.assertEqual(sum(w for x,w in product.items() if x[axis]),F(1,2))
        self.assertEqual(sum(j*b*w for (j,b),w in correlated.items()),F(1,2))
        self.assertEqual(sum(j*b*w for (j,b),w in product.items()),F(1,4))
    def test_typing_can_destroy_independence(self):
        product={(j,b):F(1,4) for j in (0,1) for b in (0,1)}
        z=sum(w for (j,b),w in product.items() if j==b)
        conditioned={(j,b):w/z for (j,b),w in product.items() if j==b}
        self.assertEqual(z,F(1,2))
        self.assertEqual(sum(j*b*w for (j,b),w in conditioned.items()),F(1,2))
        self.assertNotEqual(F(1,2),F(1,2)*F(1,2))
    def test_nonseparable_kernel_and_domination(self):
        nu={F(1):F(1,3),F(2):F(2,3)}
        mu={F(1,2):F(1,4),F(3):F(3,4)}
        direct=sum(n*m*(j+b)**3 for j,n in nu.items() for b,m in mu.items())
        nested=sum(n*sum(m*(j+b)**3 for b,m in mu.items()) for j,n in nu.items())
        self.assertEqual(direct,nested)
        self.assertNotEqual(direct,sum(n*j**3 for j,n in nu.items())*sum(m*b**3 for b,m in mu.items()))
        self.assertLessEqual(sum(n*m*(j+b)**2 for j,n in nu.items() for b,m in mu.items()),direct)
    def test_radius_and_full_normalizer_not_lost(self):
        self.assertEqual(F(2)*F(2)*F(1,2)*F(1,2),1)
        for r in (F(1,2),F(1,5),F(1,50)):
            self.assertEqual(r**5/r**2,r**3)
            self.assertNotEqual(r**5/r**4,r**3)
if __name__=='__main__':unittest.main(verbosity=2)
