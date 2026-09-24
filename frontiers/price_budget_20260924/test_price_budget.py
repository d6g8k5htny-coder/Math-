"""Finite controls, not analytic review of the universal theorem."""
from fractions import Fraction as Q
import itertools
import json
from pathlib import Path
import unittest
import price_budget as p


def brute_tail(ps, a):
    total=Q(0)
    for bits in itertools.product((0,1), repeat=len(ps)):
        if sum(bits)>a:
            product=Q(1)
            for b,x in zip(bits,ps): product*=x if b else 1-x
            total+=product
    return total


class PriceBudgetTests(unittest.TestCase):
    def test_phi_upper_zero(self): self.assertEqual(p.phi_upper(0),0)
    def test_phi_upper_one(self): self.assertEqual(p.phi_upper(1),1)
    def test_phi_upper_quarter(self): self.assertEqual(p.phi_upper(Q(1,4)),Q(1,3))
    def test_float_refused(self):
        with self.assertRaises(TypeError): p.phi_upper(0.25)
    def test_bool_refused(self):
        with self.assertRaises(TypeError): p.phi_upper(True)
    def test_out_of_range_refused(self):
        for x in (-1,2):
            with self.assertRaises(ValueError): p.phi_upper(x)
    def test_invalid_capacity_refused(self):
        for x in (0,True,Q(1),-1):
            with self.assertRaises(ValueError): p.audit_block([Q(1,4)]*3,x,2)
    def test_actual_block_size_required(self):
        with self.assertRaisesRegex(ValueError,'block size'): p.audit_block([Q(1,4)]*2,1,2)
    def test_tail_exact_half(self): self.assertEqual(p.tail_probability([Q(1,2)]*3,1),Q(1,2))
    def test_tail_deterministic_endpoints(self):
        self.assertEqual(p.tail_probability([0,1,1],1),1)
        self.assertEqual(p.tail_probability([0,0,1],1),0)
    def test_tail_subset_enumeration(self):
        for ps in itertools.product((Q(0),Q(1,16),Q(1,4),Q(1,2),Q(1)),repeat=3):
            for a in (1,2): self.assertEqual(p.tail_probability(ps,a),brute_tail(ps,a))
    def test_tail_capacity_two(self):
        for ps in itertools.product((Q(1,4),Q(1,2)),repeat=5):
            self.assertEqual(p.tail_probability(ps,2),brute_tail(ps,2))
    def test_zero_price_retained_budget(self):
        result=p.audit_block([Q(0),Q(1,4),Q(1,4)],1,2)
        self.assertTrue(result['certified_sufficient_budget'])
        self.assertEqual(result['all_transformed_prices_product_upper'],0)
        self.assertGreater(result['local_failure'],0)
    def test_low_probability_factor(self):
        for ps in itertools.product((Q(0),Q(1,16),Q(1,4)),repeat=3):
            result=p.audit_block(ps,1,2)
            self.assertTrue(result['low_probability_hypotheses'])
            self.assertLessEqual(result['all_transformed_prices_product_upper'],Q(16,27)*result['local_failure'])
    def test_low_probability_larger_capacities(self):
        for a in range(1,9):
            for d in range(2,7):
                self.assertLessEqual(p.uniform_ratio_bound(Q(1,4),a,d),Q(16,27))
                self.assertTrue(p.audit_block([Q(1,4)]*(a*d+1),a,d)['certified_sufficient_budget'])
    def test_ratio_extremizer(self): self.assertEqual(p.uniform_ratio_bound(Q(1,4),1,2),Q(16,27))
    def test_demand_one_not_promoted(self):
        self.assertFalse(p.low_probability_conditions([Q(1,4)]*2,1,1))
    def test_large_probabilities_not_low_probability(self):
        self.assertFalse(p.low_probability_conditions([Q(1,2)]*3,1,2))
    def test_previous_counterexample_refused(self):
        result=p.audit_block([Q(1,2)]*2,1,1)
        self.assertEqual(result['local_failure'],Q(1,4))
        self.assertFalse(result['certified_sufficient_budget'])
        self.assertIn('not-certified',result['reason'])
    def test_high_failure_cap(self):
        result=p.audit_block([Q(9,10)]*2,1,1)
        self.assertTrue(result['certified_sufficient_budget'])
        self.assertEqual(result['reason'],'local-hazard-cap-is-one')
    def test_noncertification_is_not_infeasibility(self):
        # Equal half probabilities on three vertices: the sufficient envelope fails,
        # but this routine must not declare all true transformed-price covers impossible.
        result=p.audit_block([Q(1,2)]*3,1,2)
        self.assertFalse(result['certified_sufficient_budget'])
        self.assertNotIn('infeasible',result['reason'])
    def test_inflated_rational_price(self):
        x=Q(1,40900)
        self.assertEqual(p.positive_inflated_price(x),Q(81801,3345620000))
        self.assertGreater(p.positive_inflated_price(x),x)
        self.assertLess(p.positive_inflated_price(x),p.phi_upper(x))
    def test_actual_816_example(self):
        result=p.demo()['six_block_example']
        self.assertEqual(result['unchanged_palette'],816)
        self.assertEqual(result['coordinates'],2454)
        self.assertTrue(result['block_budget_certified'])
    def test_published_output(self):
        path=Path(__file__).with_name('RESULTS.json')
        self.assertEqual(json.loads(path.read_text()),p.demo())
        self.assertFalse(p.demo()['scientific_acceptance'])
    def test_size_limit(self):
        with self.assertRaisesRegex(ValueError,'limit'): p.audit_block([Q(1,4)]*4097,1,4096)
    def test_uniform_ratio_endpoint_refused(self):
        with self.assertRaises(ValueError): p.uniform_ratio_bound(1,1,2)


if __name__=='__main__': unittest.main()
