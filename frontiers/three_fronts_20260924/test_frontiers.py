"""Finite exact algebra, probability counterexamples and actual-coordinate P15 checks."""
from fractions import Fraction as Q
from itertools import combinations, product
import unittest
import frontier_math as f


class MatrixControls(unittest.TestCase):
    def test_empty_determinant(self):
        self.assertEqual(f.det(()),1)
    def test_determinant_two_implementations(self):
        for a,b,c in product(range(-2,3),repeat=3):
            x=((a,b),(b,c)); self.assertEqual(f.det(x),f.det_permutations(x))
    def test_three_by_three_determinants(self):
        for v in product((-1,0,1),repeat=6):
            a,b,c,d,e,g=v; x=((a,b,c),(b,d,e),(c,e,g))
            self.assertEqual(f.det(x),f.det_permutations(x))
    def test_symmetric_inertia_zero_pivot(self):
        self.assertEqual(f.inertia(((0,2),(2,0))),(1,0,1))
    def test_rank_deficiency(self):
        self.assertEqual(f.inertia(((1,1,0),(1,1,0),(0,0,0))),(0,2,1))
    def test_negative_definite(self):
        self.assertEqual(f.inertia(((-2,1),(1,-2))),(2,0,0))
    def test_nonsymmetric_refused(self):
        with self.assertRaises(ValueError): f.inertia(((1,2),(0,1)))
    def test_filtered_index_is_essential(self):
        self.assertEqual(f.filtered_det(((-1,0),(0,2)),0),0)
        self.assertEqual(f.filtered_det(((-1,0),(0,2)),1),2)
    def test_singular_filtered_value(self):
        self.assertEqual(f.filtered_det(((1,1),(1,1)),0),0)
    def test_exact_block_identity(self):
        for a,b,c,alpha in product((-1,0,1),repeat=4):
            x=((a,b),(b,c)); beta=(Q(2),Q(-1)); r=Q(1,9)
            self.assertEqual(f.det(f.block(alpha,beta,x,Q(1,3))),alpha*f.det(x)-r*f.adjugate_quadratic(x,beta))
    def test_block_bound_is_sharp(self):
        a=((0,),); beta=(1,); r=Q(1,4)
        change=abs(f.filtered_det(f.block(1,beta,a,Q(1,2)),1)-f.filtered_det(f.block(1,beta,a,0),1))
        self.assertEqual(change,r)
        self.assertEqual(change,f.block_index_bound(a,beta,r))
    def test_all_index_crossings(self):
        cases=0
        for a,b,c,alpha in product((-1,0,1),repeat=4):
            x=((a,b),(b,c))
            for beta in ((0,0),(1,0),(1,1),(-1,2)):
                for q in (Q(1,5),Q(1,2),Q(1)):
                    left=f.block(alpha,beta,x,0); right=f.block(alpha,beta,x,q)
                    for index in range(4):
                        self.assertLessEqual(abs(f.filtered_det(right,index)-f.filtered_det(left,index)),f.block_index_bound(x,beta,q*q))
                        cases+=1
        self.assertEqual(cases,3888)
    def test_singular_adjugate(self):
        self.assertEqual(f.adjugate_quadratic(((1,0),(0,0)),(0,1)),1)
    def test_affine_identity_three_transverse(self):
        a=((1,2,0),(2,0,1),(0,1,-1)); beta=(1,-1,2); r=Q(4,9)
        self.assertEqual(f.det(f.block(2,beta,a,Q(2,3))),2*f.det(a)-r*f.adjugate_quadratic(a,beta))
    def test_contact_cubic_exact(self):
        self.assertEqual(f.contact_rows((0,0,0,1),Q(1,5))[3],6)
    def test_contact_fifth_order_error(self):
        for r in (Q(1,2),Q(1,7),Q(1,20)):
            self.assertEqual(f.contact_rows((0,0,0,0,0,1),r)[3],3*r*r)
    def test_contact_targets(self):
        for k in (Q(1,6),Q(2),Q(1,100)):
            r=Q(1,7); b=Q(3,2)
            # f=2k*x^3-(3/2)k*r^2*x+b-k*r^3/2 has critical pins and gap k*r^3.
            self.assertEqual(f.contact_rows((b-k*r**3/2,-Q(3,2)*k*r*r,0,2*k),r),
                             (b-k*r**3/2,-k*r*r,0,12*k))
    def test_no_float_input(self):
        with self.assertRaises(ValueError): f.det(((1.0,),))
        with self.assertRaises(ValueError): f.block_index_bound(((1,),),(1,),True)


class RateAndCountControls(unittest.TestCase):
    def test_dimension_cancellation(self):
        self.assertEqual([f.radial_power(d) for d in range(2,21)],[1]*19)
    def test_small_and_large_split_exponents(self):
        x=f.rate_ledger(); self.assertEqual(x['inner_contact'],Q(7,18)); self.assertEqual(x['outer_loss'],Q(7,18))
    def test_delta_applicability(self):
        self.assertEqual(f.rate_ledger()['outer_delta'],Q(1,9))
    def test_lower_cutoff_controls_final_rate(self):
        x=f.rate_ledger(); self.assertEqual(min(x['inner_contact'],x['outer_loss'],x['lower_cutoff']),Q(1,3))
    def test_invalid_split(self):
        for a in (0,Q(1,4),1):
            with self.assertRaises(ValueError): f.rate_ledger(a)
    def test_integrated_small_k_models(self):
        for n in range(2,12):
            x=Q(1,n); ell=x**18; eta=x**3; a=8*x**18; ell23=x**12
            contact=Q(3,7)*(x**7-128*x**42)
            r2=3*ell23*(Q(1,2)/x**6-Q(1)/x)
            self.assertGreaterEqual(contact,0); self.assertGreaterEqual(r2,0)
            self.assertLessEqual(contact+r2,2*x**6)
            self.assertLessEqual(Q(3,11)*ell*(x**(-11)-1),x**7)
    def test_holder_p2(self): self.assertEqual(f.holder_exponent(2),Q(3,2))
    def test_holder_p4(self): self.assertEqual(f.holder_exponent(4),Q(9,4))
    def test_holder_growing_moment(self): self.assertEqual(f.holder_exponent(4,2),Q(7,4))
    def test_holder_not_cubic_at_finite_order(self):
        for p in range(2,51): self.assertLess(f.holder_exponent(p),3)
    def test_holder_invalid(self):
        with self.assertRaises(ValueError): f.holder_exponent(1)
    def test_log_count_defeats_cubic_constant(self):
        for n in (1,2,8,32,128):
            v=f.rare_count(n); self.assertEqual(v['mean']/v['probability'],n)
    def test_count_event_direction(self):
        v=f.rare_count(20); self.assertLess(v['probability'],v['mean'])
    def test_counterexample_moments_eventually_decrease(self):
        for p in range(1,13):
            for n in range(max(p,2),max(p,2)+10):
                self.assertLess(f.rare_count(n+1,p)['moment'],f.rare_count(n,p)['moment'])
    def test_holder_sharp_model(self):
        for p in (2,3,4):
            for n in range(1,8):
                r=Q(1,2**(p*n)); prob=r**3; count=2**(3*n)
                self.assertEqual(prob*count**p,1)
                self.assertEqual(prob*count,Q(1,2**(3*n*(p-1))))


class P15Controls(unittest.TestCase):
    def model(self): return f.Model((1,1,1),(1,1,1),((0,1,2),))
    def test_actual_minimal_witnesses(self):
        m=self.model(); self.assertEqual(m.actual_minimal_forbidden(),m.structural_forbidden())
        self.assertEqual(len(m.structural_forbidden()),11)
    def test_actual_local_restrictions(self):
        m=self.model()
        for block,a in zip(m.blocks,m.capacities):
            sub=block
            while True:
                self.assertEqual(m.good(sub),sub.bit_count()<=a)
                if sub==0: break
                sub=(sub-1)&block
    def test_positive_nonempty_cover(self):
        m=self.model(); self.assertEqual(m.sizes,(2,2,2))
        self.assertTrue(all(b and not m.avoids_cover(b) for b in m.blocks))
    def test_actual_coloring_vs_macro_demands(self):
        for capacities,demands in (((1,1),(1,1)),((1,2),(2,1)),((2,2),(1,1)),((1,1,1),(1,1,1))):
            b=len(capacities); edges=(tuple(range(b)),)
            m=f.Model(capacities,demands,edges); table=m.chromatic_table()
            k=f.palette_optimum(demands,edges)
            residual=m.full
            for block in m.blocks: residual^=block&-block
            self.assertEqual(table[residual],k)
            self.assertEqual(table[m.full],f.palette_optimum(tuple(d+1 for d in demands),edges))
            self.assertTrue(all(table[s]<=k for s in range(m.full+1) if m.avoids_cover(s)))
    def test_all_three_block_clutters(self):
        candidates=(frozenset((0,1)),frozenset((0,2)),frozenset((1,2)),frozenset((0,1,2)))
        cases=sets=0
        for flags in product((0,1),repeat=4):
            edges=tuple(e for e,x in zip(candidates,flags) if x)
            if any(e<g for e in edges for g in edges): continue
            m=f.Model((1,1,1),(1,1,1),edges)
            self.assertEqual(m.actual_minimal_forbidden(),m.structural_forbidden())
            table=m.chromatic_table(); k=f.palette_optimum((1,1,1),edges)
            for s in range(m.full+1):
                if m.avoids_cover(s): self.assertLessEqual(table[s],k); sets+=1
            cases+=1
        self.assertEqual(cases,9); self.assertEqual(sets,243)
    def test_incomplete_transversal_detected(self):
        m=self.model(); witnesses=set(m.structural_forbidden())
        cross=next(w for w in witnesses if all((w&b).bit_count()==1 for b in m.blocks))
        witnesses.remove(cross)
        self.assertFalse(any(cross&w==w for w in witnesses))
        self.assertFalse(m.good(cross))
    def test_clutter_refusal(self):
        with self.assertRaises(ValueError): f.Model((1,1,1),(1,1,1),((0,1),(0,1,2)))
    def test_singleton_macro_refusal(self):
        with self.assertRaises(ValueError): f.Model((1,1),(1,1),((0,),))
    def test_zero_capacity_refused(self):
        with self.assertRaises(ValueError): f.Model((0,1),(1,1),())
    def test_empty_macro_family(self): self.assertEqual(f.palette_optimum((1,2,3),()),3)
    def test_triangle_not_edge_load_two(self): self.assertEqual(f.palette_optimum((1,1,1),((0,1),(1,2),(0,2))),3)
    def test_uniform_compressed_benchmark(self):
        k,ps=f.uniform_palette((408,)*6,3)
        self.assertEqual(k,816); self.assertTrue(all(len(p)==408 for p in ps))
        for color in range(k): self.assertEqual(sum(color in p for p in ps),3)
    def test_uniform_against_residual_dp(self):
        for b in range(2,5):
            for rank in range(1,b+1):
                edges=tuple(combinations(range(b),rank+1))
                for demands in product((1,2),repeat=b):
                    k,ps=f.uniform_palette(demands,rank)
                    self.assertEqual(k,f.palette_optimum(demands,edges))
                    self.assertTrue(all(sum(color in p for p in ps)<=rank for color in range(k)))
    def test_actual_probability_budget(self):
        m=self.model(); v=f.budget_certificate(m,(Q(1,5),)*m.n,(Q(1,6),)*m.n)
        self.assertGreater(v['cost'],0); self.assertTrue(v['local_cost_le_failure'])
        self.assertLessEqual(v['cost'],v['sum_local_failures'])
        self.assertLess(v['good_probability'],v['product_local_good'])
    def test_price_range_not_silently_extended(self):
        m=self.model()
        with self.assertRaises(ValueError): f.budget_certificate(m,(Q(1,5),)*m.n,(Q(1,4),)*m.n)
    def test_zero_probability_keeps_setwise_generators(self):
        m=self.model(); v=f.budget_certificate(m,(Q(0),)*m.n,(Q(0),)*m.n)
        self.assertEqual(v['cost'],0); self.assertEqual(v['good_probability'],1)
        self.assertEqual(len(m.blocks),3)
    def test_generator_price_is_product(self):
        self.assertEqual(f.local_generator_cost((Q(1,3),Q(1,5))),Q(1,15))
    def test_large_witness_counts(self):
        v=f.large_example(); self.assertEqual(v['crossing_minimal_quadruples'],419743994415)
        self.assertEqual(v['internal_minimal_pairs'],500616); self.assertEqual(v['original_vertices'],2454)
    def test_large_low_failure_is_rational(self):
        v=f.large_example(); self.assertEqual(v['failure_upper'],'2449227/8180000000')
        self.assertTrue(v['failure_below_3_over_10000'])
    def test_large_exhaustive_refusal(self):
        m=f.Model((1,)*6,(408,)*6,tuple(combinations(range(6),4)))
        with self.assertRaises(ValueError): m.actual_minimal_forbidden()
        with self.assertRaises(ValueError): m.structural_forbidden()
    def test_no_acceptance_from_output(self):
        self.assertFalse(f.output()['scientific_acceptance'])
        self.assertFalse(f.output()['rn']['triple_integral_evaluated'])


if __name__=='__main__': unittest.main()
