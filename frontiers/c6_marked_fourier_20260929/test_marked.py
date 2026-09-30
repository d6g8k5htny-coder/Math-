"""Finite normalization and boundary controls; not Gaussian continuum verification."""
import unittest
from fractions import Fraction as F
import marked as m

class MarkedTests(unittest.TestCase):
 def test_holder_needs_twice_the_rate(self):
  self.assertFalse(m.admissible_rate(F(1),F(3,4)))
  self.assertFalse(m.admissible_rate(F(1),F(1,2)))
  self.assertTrue(m.admissible_rate(F(1),F(1,4)))
 def test_dimension_exponent(self):
  self.assertEqual(m.alpha(2),1);self.assertEqual(m.alpha(3),F(2,3));self.assertEqual(m.alpha(4),F(1,2))
 def test_conditional_mean_is_not_dropped(self):
  self.assertEqual(m.regression_second(1,F(1,2),1,3,0),3)
  self.assertEqual(m.regression_second(1,F(1,2),1,3,1),7)
 def test_residual_projection_decreases_variance(self):
  for c in (F(-1),F(-1,2),F(0),F(1,2),F(1)):
   self.assertLessEqual(m.regression_second(1,c,1,0,0),1)
 def test_tail_prefactor_is_retained(self):
  self.assertEqual(m.exponential_moment_bound(2,F(1,2),7),F(10,3))
  self.assertGreater(m.exponential_moment_bound(2,F(1,2),7),m.exponential_moment_bound(2,F(1,2),1))
 def test_cutoff_three_positive_rates(self):
  for d in range(2,11):
   v=m.cutoff_rates(d,F(3,5))
   self.assertTrue(all(x>0 for x in v))
   self.assertEqual(v[1],F(3,5)*F(2*d+1,4*d))
 def test_one_original_weight_and_normalizer(self):
  probs=[F(1,2),F(1,3),F(1,6)];counts=[0,1,2];weights=[1,2,3]
  self.assertEqual(m.weighted_mark(probs,counts,weights,F(2)),F(16,5))
 def test_count_weight_is_required(self):
  self.assertEqual(m.weighted_mark([F(3,4),F(1,4)],[0,3],[1,1],2),6)
 def test_nonempty_and_sizebiased_are_distinct(self):
  p=[F(7,10),F(2,10),F(1,10)];n=[0,1,3]
  self.assertEqual(m.nonempty(p,n),[F(0),F(2,3),F(1,3)])
  self.assertEqual(m.sizebiased(p,n),[F(0),F(2,5),F(3,5)])
  self.assertNotEqual(m.nonempty(p,n),m.sizebiased(p,n))
 def test_cluster_tail_includes_n(self):
  self.assertEqual(m.tail_bound(F(2),F(1,100),4,2),F(1,3200))
 def test_exact_finite_exponential_cluster_family(self):
  eps=F(1,1024);n=list(range(17));p=[F(0)]+[eps/F(k*4**k) for k in range(1,17)]
  p[0]=1-sum(p[1:]);M=m.weighted_mark(p,n,[1]*17,2)
  self.assertEqual(M,eps*(1-F(1,2**16)));self.assertLess(M,eps)
  for k in range(1,17):self.assertLessEqual(sum(p[k:]),m.tail_bound(1,eps,k,2))
 def test_factorial_constant_growth_exponent(self):
  for d in range(2,8):
   for p in range(2,8):self.assertEqual(m.factorial_power(d,p),F(d*(p-1),2))
 def test_pgf_first_order_is_exact(self):
  eps=F(1,100);probs=[1-3*eps,eps,2*eps];counts=[0,2,3]
  for z in (F(0),F(1,4),F(1,2),F(1)):
   self.assertEqual(sum(p*z**n for p,n in zip(probs,counts)),1+eps*m.levy_exponent(probs,counts,eps,z))
 def test_replica_independence_is_an_extra_assumption(self):
  eps=F(1,10);z=F(1,2)
  single=1-eps+eps*z**2
  independent=single**2;identical_copies=1-eps+eps*z**4
  self.assertNotEqual(independent,identical_copies)
 def test_no_unique_limit_from_uniform_moment_bounds(self):
  eps=F(1,100)
  self.assertNotEqual(m.levy_exponent([1-eps,eps],[0,2],eps,F(1,2)),m.levy_exponent([1-eps,eps],[0,3],eps,F(1,2)))
 def test_higher_factorial_lower_bound_not_implied(self):
  eps=F(1,100)
  self.assertEqual(m.factorial_mean([1-eps,eps],[0,2],2),2*eps)
  self.assertEqual(m.factorial_mean([1-eps,eps],[0,2],3),0)
 def test_bad_inputs(self):
  with self.assertRaises(ValueError):m.alpha(1)
  with self.assertRaises(ValueError):m.exponential_moment_bound(1,1,2)
  with self.assertRaises(ValueError):m.sizebiased([1],[0])
  with self.assertRaises(ValueError):m.regression_second(1,2,1,0,0)

if __name__=='__main__':unittest.main()
