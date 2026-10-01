from fractions import Fraction as F
from itertools import product, combinations
import unittest
import cap_audit as c

class ExactGeometry(unittest.TestCase):
    def test_constants(self):
        a=c.constants()
        self.assertEqual(a['ridge_lower'],F(2184415,7086244))
        self.assertGreater(a['ridge_lower'],F(1,4))
        self.assertEqual(a['axis_drop_normalized'],F(9,32))
        self.assertEqual(a['axis_excess_normalized'],F(11,96))
        self.assertEqual(a['side_drop_normalized'],F(4400,121))
    def test_forced_hermite_mean(self):
        # Exact positive Hermite kernel, not a sampled derivative.
        ker={(0,):F(1,4),(2,):F(-1)}
        self.assertEqual(c.integral(ker,F(-1,2),F(1,2)),F(1,6))
        self.assertEqual(-F(1,2)*2*c.integral(ker,F(-1,2),F(1,2)),-F(1,6))
    def test_general_mark_scaling(self):
        for r in (F(1),F(1,10),F(1,100)):
            for k in (F(1,6),F(1),F(3)):
                m=12*k; n=0; lam=200*k*r
                self.assertTrue(c.good_event(r,k,m,n,lam))
                self.assertTrue(c.good_event(r,F(1,6),m/(6*k),n,lam/(6*k)))
                self.assertEqual(6*k*F(9,32)*r**3,F(27,16)*k*r**3)
    def test_depth_and_fourth_derivative_are_required(self):
        self.assertFalse(c.good_event(1,1,12,0,192))
        self.assertTrue(c.good_event(1,1,12,F(3,10),256))
        self.assertFalse(c.good_event(1,1,12,F(31,100),256))
    def test_invalid_rational_inputs(self):
        for x in (True,1.0,'1'):
            with self.assertRaises((TypeError,ValueError)):c.good_event(x,1,12,0,256)
        with self.assertRaises(ValueError):c.good_event(1,0,12,0,256)
    def test_vector_average_no_common_rolle_zero(self):
        # w=(x^2-1/4, x^3-x/4), w(+/-1/2)=0;
        # w'_1=2x vanishes only at0, w'_2(0)=-1/4.
        w1={(2,):F(1),(0,):-F(1,4)}; w2={(3,):F(1),(1,):-F(1,4)}
        for x in (F(-1,2),F(1,2)):
            self.assertEqual(c.value(w1,(x,)),0);self.assertEqual(c.value(w2,(x,)),0)
        self.assertEqual(c.value(c.derivative(w1,0),(F(0),)),0)
        self.assertEqual(c.value(c.derivative(w2,0),(F(0),)),-F(1,4))
        self.assertEqual(c.integral(c.derivative(w1,0),F(-1,2),F(1,2)),0)
        self.assertEqual(c.integral(c.derivative(w2,0),F(-1,2),F(1,2)),0)
    def test_vector_ridge_third_derivative(self):
        # f=q(x)-lambda_i/2 (y_i-h_i(x))^2; g=q independently.
        dim=3; x=c.variable(dim,0); y=c.variable(dim,1); z=c.variable(dim,2)
        one={(0,0,0):F(1)}
        q=c.add(c.scale(c.power(x,3),2),c.scale(x,-F(3,2)),c.scale(one,-F(1,2)))
        for t in (F(-2),F(1,3),F(2)):
            h1=c.scale(c.add(c.power(x,2),c.scale(one,-F(1,4))),t)
            h2=c.scale(c.add(c.power(x,3),c.scale(x,-F(1,4))),t)
            f=c.add(q,c.scale(c.power(c.add(y,c.scale(h1,-1)),2),-7),c.scale(c.power(c.add(z,c.scale(h2,-1)),2),-11))
            for xx in (F(-3,4),F(0),F(2,3)):
                pt=(xx,c.value(h1,(xx,0,0)),c.value(h2,(xx,0,0)))
                vv=(F(1),c.value(c.derivative(h1,0),pt),c.value(c.derivative(h2,0),pt))
                answer=F(0)
                for i,j,k in product(range(dim),repeat=3):
                    dd=c.derivative(c.derivative(c.derivative(f,i),j),k)
                    answer+=c.value(dd,pt)*vv[i]*vv[j]*vv[k]
                self.assertEqual(answer,12)
                self.assertEqual(c.value(c.derivative(f,1),pt),0)
                self.assertEqual(c.value(c.derivative(f,2),pt),0)
    def test_congruence_erratum(self):
        t=F(1,4);r=t*t; a=-6;b=3;A=-2
        H=[[r*a,r*b],[r*b,A]]
        correct=c.diagonal_congruence(H,[1/t,1]);wrong=c.diagonal_congruence(H,[t,1])
        self.assertEqual(correct,[[F(-6),F(3,4)],[F(3,4),F(-2)]])
        self.assertNotEqual(wrong,correct)
        self.assertEqual(wrong[0][0],r*r*a)

class JetFalsifier(unittest.TestCase):
    def test_same_three_jets_but_older_route(self):
        f0,f1=c.falsifier()
        for xx in (F(-1,2),F(1,2)):
            for total in range(4):
                for i in range(total+1):
                    a,b=f0,f1
                    for _ in range(i):a=c.derivative(a,0);b=c.derivative(b,0)
                    for _ in range(total-i):a=c.derivative(a,1);b=c.derivative(b,1)
                    self.assertEqual(c.value(a,(xx,0)),c.value(b,(xx,0)))
        self.assertEqual(c.value(f0,(F(-1,2),0)),0)
        self.assertEqual(c.value(f0,(F(1,2),0)),-1)
        self.assertTrue(c.good_event(1,1,12,0,256))
        self.assertGreater(c.value(f1,(F(-1,2),F(1,16))),0)
    def test_entire_shortcut_not_just_endpoints(self):
        # Along x=-1/2, polynomial is 65536(y^2-1/1024)^2 -1/16 + y^5.
        y=c.variable(2,1);one={(0,0):F(1)}
        exact=c.add(c.scale(c.power(c.add(c.power(y,2),c.scale(one,-F(1,1024))),2),65536),c.scale(one,-F(1,16)),c.power(y,5))
        f0,f1=c.falsifier()
        section={}
        for (i,j),a in f1.items():section[(0,j)]=section.get((0,j),F(0))+a*F(-1,2)**i
        self.assertEqual(c.clean(section),c.clean(exact))
        # y>=0 gives the path-wide lower bound -1/16 > saddle height -1.
        self.assertGreater(-F(1,16),-1)
    def test_changed_neighborhood_norm_blocks_false_promotion(self):
        _,f1=c.falsifier();four=f1
        for _ in range(4):four=c.derivative(four,1)
        self.assertEqual(c.value(four,(F(-1,2),0)),24*65536)
        self.assertFalse(c.good_event(1,1,12,24*65536,256))

class TopologyAnalogue(unittest.TestCase):
    def test_ridge_alone_not_sufficient(self):
        weights={'M':F(0),'S':F(-1),'O':F(1),'B':-F(1,2)}
        edges=[('M','S'),('S','O'),('M','B'),('B','O')]
        self.assertEqual(c.graph_maximin(weights,edges,'M'),-F(1,2))
        self.assertEqual(c.graph_maximin(weights,edges[:2],'M'),-1)
    def test_boundary_alone_not_sufficient(self):
        self.assertIsNone(c.graph_maximin({'M':F(0),'S':F(-1)},[('M','S')],'M'))
    def test_equal_birth_is_not_an_older_endpoint(self):
        self.assertIsNone(c.graph_maximin({'M':F(0),'S':F(-1),'T':F(0)},[('M','S'),('S','T')],'M'))
    def test_arbitrary_exterior_does_not_bypass_full_cut(self):
        count=0;ext=['O','A','B','C'];optional=list(combinations(ext,2))
        for vals in product((F(-3),-F(1,2),F(2)),repeat=3):
            weights={'M':F(0),'I':-F(1,4),'S':F(-1),'L':F(-2),'O':F(1),**dict(zip(ext[1:],vals))}
            for mask in range(1<<len(optional)):
                edges=[('M','I'),('I','S'),('M','L'),('S','O'),('L','A')]+[e for j,e in enumerate(optional) if mask>>j&1]
                got=c.graph_maximin(weights,edges,'M')
                self.assertEqual(got,-1)
                self.assertEqual(got,c.graph_threshold_oracle(weights,edges,'M'))
                count+=1
        self.assertEqual(count,1728)

if __name__=='__main__':unittest.main()
