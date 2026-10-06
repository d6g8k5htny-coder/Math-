"""Exact finite diagnostics; not a replacement for the source-bound Gaussian proof."""
from fractions import Fraction as F
import importlib.util
from pathlib import Path
import unittest

class JointRankTests(unittest.TestCase):
    def module(self):
        p = Path(__file__).with_name('joint_rank.py')
        self.assertTrue(p.is_file(), 'joint-rank diagnostic has not been implemented')
        spec = importlib.util.spec_from_file_location('joint_rank', p)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        return m

    def test_block_one(self):
        m=self.module(); self.assertEqual(m.block_polynomial(1), {0:-1,1:1})

    def test_block_two(self):
        m=self.module(); self.assertEqual(m.block_polynomial(2), {1:1,2:-4,3:6,4:-4,5:1})

    def test_block_three(self):
        m=self.module(); self.assertEqual(m.block_polynomial(3), m.expected_block(3))

    def test_joint_determinant_and_rank(self):
        m=self.module()
        for z in m.PHASES:
            with self.subTest(z=z):
                a=m.witness(z)
                determinant,rank=m.eliminate(a)
                expected=m.mul(m.qc(16),m.mul(m.power(z,4),m.power(m.sub(z,m.qc(1)),14)))
                self.assertEqual(rank,12)
                self.assertEqual(determinant,expected)

    def test_collision_is_not_nondegenerate(self):
        m=self.module(); determinant,rank=m.eliminate(m.witness(m.qc(1)))
        self.assertEqual(rank,6); self.assertEqual(determinant,m.qc(0))

    def test_missing_mode_loses_rank(self):
        m=self.module(); a=m.witness(m.qc(0,1))
        self.assertEqual(m.eliminate(a[:-1])[1],11)

    def test_duplicate_jet_loses_rank(self):
        m=self.module(); a=m.witness(m.qc(0,1))
        # Two identical jet columns must not be called independent Hessian entries.
        for row in a: row[-1]=row[-2]
        self.assertLess(m.eliminate(a)[1],12)

    def test_witness_modes_and_block_structure(self):
        m=self.module(); self.assertEqual(len(set(m.MODES)),12)
        a=m.witness(m.qc(3,4,5)); zero=m.qc(0)
        self.assertTrue(all(a[i][j]==zero for i in range(6) for j in range(6,12)))
        self.assertTrue(all(a[i][j]==zero for i in range(6,10) for j in range(10,12)))

    def test_physical_scaling_and_positive_weight_witness(self):
        m=self.module()
        for r in map(F,['1','1/2','1/7','1/100']):
            # Physical endpoint vector -> scaled vector determinant r^-4.
            scale=[1/r,1/r,1/r,1/r,F(1),F(1)]
            product=F(1)
            for x in scale: product*=x
            self.assertEqual(product,r**-4)
            v=(-F(1),F(1),F(0),F(0),-F(1),-F(1))
            self.assertEqual(m.typed_weight(r,v),1)

if __name__=='__main__': unittest.main()
