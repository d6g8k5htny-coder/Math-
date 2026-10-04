from fractions import Fraction as F
import unittest
import check as c

class ExactFoldTests(unittest.TestCase):
    def test_cubic_values(self):
        for q in (F(1,20),F(1,9),F(1,3)):
            mu,b,s,gap=c.fold_values(q)
            self.assertEqual(mu,q*q);self.assertEqual(b,F(2,3)*q**3)
            self.assertEqual(s,-b);self.assertEqual(gap,F(4,3)*q**3)
    def test_curvature_sandwich(self):
        for alpha in (F(1),F(3,2),F(2),F(5,2),F(3)):
            mu,b,s,gap=c.fold_values(F(1,11),alpha)
            self.assertGreater(gap,0);self.assertLess(mu**3,gap**2)
            self.assertLess(gap**2,4*mu**3)
    def test_cap_faces(self):
        for a in (F(1,128),F(1,16),F(1,8)):
            axial,lateral=c.cap_slack(a)
            self.assertEqual(axial,F(77,300)*a**3)
            self.assertGreater(axial,a**3/4)
            self.assertEqual(lateral,F(9,64)*a*a)
            self.assertGreater(lateral,a*a/16)
    def test_actual_inertia_under_shear(self):
        for q in (F(1,100),F(1,9)):
            for v in (F(-1,10),F(0),F(1,8)):
                hm=c.hessian(q,v);hs=c.hessian(-q,v)
                self.assertLess(hm[1][1],0);self.assertEqual(c.det(hm),2*q)
                self.assertEqual(c.det(hs),-2*q)
    def test_inverse_parameter_map(self):
        a=[[F(9,8),F(1,16)],[F(-1,16),F(7,8)]]
        b=[F(1,16),F(-1,32)];x=c.solve(a,b)
        self.assertEqual([sum(a[i][j]*x[j] for j in range(2)) for i in range(2)],b)
    def test_uniform_volume(self):
        for n in range(1,8):
            self.assertEqual(c.lower_volume(n),F(1,5**n))
    def test_matrix_closeness(self):
        self.assertEqual(c.row_error([[F(9,8),F(1,16)],[F(-1,16),F(7,8)]]),F(3,16))
    def test_multiplicity_exponent(self):
        self.assertEqual(c.exponent(2),F(4,3));self.assertEqual(c.exponent(5),F(10,3))
    def test_mixture_measures(self):
        law=[(F(1,4),()),(F(1,2),('a',)),(F(1,4),('a','b'))]
        z=c.measures(law)
        self.assertEqual(z['m'],1);self.assertEqual(z['p'],F(3,4))
        self.assertEqual(z['I'],{'a':F(3,4),'b':F(1,4)})
        self.assertEqual(z['J'],{'a':F(5,8),'b':F(1,8)})
        self.assertEqual(z['R'],{'a':F(1,8),'b':F(1,8)})
    def test_tv(self):
        self.assertEqual(c.tv({'a':F(1)},{'b':F(1)}),1)
    def test_input_rejections(self):
        with self.assertRaises(TypeError):c.fold_values(0.5)
        with self.assertRaises(ValueError):c.fold_values(-F(1))
        with self.assertRaises(ValueError):c.lower_volume(0)
        with self.assertRaises(ValueError):c.solve([[F(0)]],[F(1)])
        with self.assertRaises(ValueError):c.measures([(F(1,2),('a',))])


class AdditionalControls(unittest.TestCase):
    def test_exact_gap_ratio(self):
        for alpha in (F(1),F(7,5),F(3)):
            for q in (F(1,40),F(2,19),F(1)):
                mu,b,s,g=c.fold_values(q,alpha)
                self.assertEqual(g*g/mu**3,F(32,9)/alpha)
    def test_unfolding_window(self):
        self.assertEqual(F(1,4)**3,F(1,64))
        self.assertEqual(4*F(1,2)**3,F(1,2))
        self.assertGreater(F(1,64),0);self.assertLess(F(1,2),1)
    def test_curvature_types_not_endpoint_guesses(self):
        for a in (F(-1,8),F(1,8)):
            h=c.hessian(a,F(1,9))
            self.assertEqual(h[0][0]-h[0][1]*h[1][0]/h[1][1],-2*a)
    def test_linear_preimage_cover(self):
        # Correlated coordinates are allowed: none of these matrices is diagonal.
        for n in range(2,7):
            a=[[F(i==j)+F((-1)**(i+j),8*n) for j in range(n)] for i in range(n)]
            self.assertLessEqual(c.row_error(a),F(1,4))
            self.assertLessEqual(abs(c.det(a)),F(5,4)**n)
            shift=[F((-1)**i,4) for i in range(n)]
            target=[F((-1)**(i+1),2) for i in range(n)]
            s=c.solve(a,[x-y for x,y in zip(target,shift)])
            self.assertLessEqual(max(map(abs,s)),1)
    def test_nonindependent_unfolding_not_required(self):
        a=[[F(1),F(1,5)],[F(1,5),F(1)]]
        self.assertEqual(c.det(a),F(24,25));self.assertLess(c.row_error(a),F(1,4))
    def test_rank_defect_cannot_unfold_two_folds(self):
        a=[[F(1),F(1)],[F(1),F(1)]]
        self.assertEqual(c.det(a),0);self.assertGreater(c.row_error(a),F(1,4))
        with self.assertRaises(ValueError):c.solve(a,[F(1),F(0)])
    def test_jacobian_factor_is_required(self):
        for n in range(1,7):
            actual=(F(1,4)/F(5,4))**n
            self.assertEqual(c.lower_volume(n),actual)
            self.assertGreater(F(1,4)**n,actual)
    def test_support_tail_markov_scale(self):
        # Fixed positive-probability tail event, not a t-dependent small ball.
        for eps in (F(1,1000),F(1,13),F(1)):
            mean=eps/4
            self.assertLessEqual(mean/(eps/2),F(1,2))
    def test_all_count_identities(self):
        for n in range(8):
            law=[(F(1,3),()),(F(1,3),('a',)),(F(1,3),tuple('b' for _ in range(n)))]
            z=c.measures(law);ex=z['m']-z['p']
            self.assertLessEqual(z['D']/2,ex);self.assertLessEqual(ex,z['D'])
            self.assertEqual(ex,z['p2']+F(max(n-1,0),3)*(n>=3))
            self.assertEqual(sum(z['R'].values()),ex)
            self.assertLessEqual(sum(z['R'].values())-sum(z['R2'].values()),z['tail'])
    def test_marked_mixture_identity(self):
        law=[(F(1,8),()),(F(3,8),('a',)),(F(1,4),('a','b')),(F(1,4),('b','c','c'))]
        z=c.measures(law);m,p=z['m'],z['p'];ex=m-p
        a={k:v/m for k,v in z['I'].items()};b={k:v/p for k,v in z['J'].items()}
        excess={k:v/ex for k,v in z['R'].items()}
        for k in a.keys()|b.keys()|excess.keys():
            self.assertEqual(a.get(k,0),p/m*b.get(k,0)+ex/m*excess.get(k,0))
        self.assertEqual(c.tv(a,b),ex/m*c.tv(excess,b))
    def test_same_marks_no_tv_lower_bound(self):
        z=c.measures([(F(1,2),('a',)),(F(1,2),('a','a'))])
        self.assertGreater(z['m']-z['p'],0)
        a={k:v/z['m'] for k,v in z['I'].items()};b={k:v/z['p'] for k,v in z['J'].items()}
        self.assertEqual(c.tv(a,b),0)
    def test_singleton_count_mark_detects_bias(self):
        law=[(F(1,2),()),(F(1,3),('one',)),(F(1,6),('two','two'))]
        z=c.measures(law);m,p=z['m'],z['p'];ex=m-p
        self.assertEqual(z['J']['one']/p-z['I']['one']/m,z['p1']*ex/(m*p))
    def test_bernoulli_falsifier(self):
        for k in (2,3,5,9):
            q=F(1,k**7);p=q*q
            z=c.measures([((1-p)**2,()),(2*p*(1-p),('one',)),(p*p,('two','two'))])
            self.assertEqual(z['m'],2*p);self.assertEqual(z['p'],2*p-p*p)
            self.assertEqual(z['D'],2*p*p)
            self.assertEqual(z['D']/F(1,k**30),2*k*k)
    def test_count_obstruction_exponents(self):
        self.assertEqual(c.exponent(2)-F(10,7),-F(2,21))
        self.assertLess(c.exponent(2),F(10,7))
    def test_cumulative_and_mark_rates(self):
        self.assertEqual(F(3,7)+1,F(10,7))
        self.assertEqual(F(10,7)-F(2,3),F(16,21))
        self.assertLess(F(2,3),F(16,21))
    def test_negative_inputs_do_not_alias(self):
        for x in (True,0.5,'1/2'):
            with self.assertRaises(TypeError):c.fold_values(x)
        with self.assertRaises(ValueError):c.measures([(F(-1),()),(F(2),('a',))])
        with self.assertRaises(ValueError):c.tv({'a':F(1,2)},{'a':F(1)})

if __name__=='__main__':unittest.main()
