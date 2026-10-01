"""Finite corroborating controls; the continuum proof is not tested here."""
from fractions import Fraction as F
from pathlib import Path
import json
import tempfile
import unittest
import check_exact as c


class ExactControls(unittest.TestCase):
    def test_ten_exact_sources_are_verified(self):
        self.assertEqual(c.verify_sources(), 10)

    def test_counts_include_multifields_with_their_full_weight(self):
        self.assertEqual(c.count_statistics({0:F(3,4),1:F(1,8),2:F(1,8)}),
                         (F(3,8),F(1,4),F(1,8),F(1,4),F(1,4)))

    def test_exact_count_occurrence_identity(self):
        for n in range(12):
            e,p,x,m,s=c.count_statistics({n:F(1)})
            self.assertEqual(e-p,x)
            self.assertLessEqual(x,m)
            self.assertLessEqual(2*(n>=2),m)

    def test_first_moment_alone_does_not_identify_occurrence(self):
        h=F(1,4); lam=F(3,2); p=lam*h**5/2
        e,event,excess,multi,second=c.count_statistics({0:1-p,2:p})
        self.assertEqual(e,lam*h**5)
        self.assertEqual(event/h**5,lam/2)
        self.assertEqual(excess/h**5,lam/2)

    def test_small_multi_probability_does_not_control_weight(self):
        # As h=1/m ->0: P(N>=2)/h^5=h, but E[N;N>=2]/h^5=1.
        for m in [2,3,10]:
            h=F(1,m); p=h**6
            e,event,excess,multi,second=c.count_statistics({0:1-p,m:p})
            self.assertEqual(event/h**5,h)
            self.assertEqual(multi/h**5,1)

    def test_first_moment_excess_does_not_control_second_moment(self):
        # P(N=m)=h^7 gives multi/h^5=h but factorial/h^5=1-h.
        for m in [2,3,10]:
            h=F(1,m); p=h**7
            e,event,excess,multi,second=c.count_statistics({0:1-p,m:p})
            self.assertEqual(multi/h**5,h)
            self.assertEqual(second/h**5,1-h)

    def test_signed_field_first_mark_and_error(self):
        fields=[(F(1,2),()),(F(1,4),(F(-1),)),(F(1,4),(F(1),F(1)))]
        total,average,event,excess=c.mark_statistics(fields)
        self.assertEqual((total,average,event,excess),(F(1,4),F(0),F(1,2),F(1,4)))
        self.assertLessEqual(abs(total-average),excess)

    def test_empty_field_zero_denominator(self):
        self.assertEqual(c.mark_statistics([(F(1),())]),(F(0),)*4)

    def test_single_selected_bar_mark_law(self):
        h=F(1,5)
        total,average,event,excess=c.mark_statistics([(1-h**5,()),(h**5,(F(2,3),))])
        self.assertEqual(total/event,F(2,3))
        self.assertEqual(average/event,F(2,3))
        self.assertEqual(excess,0)

    def test_volume_factor_for_occurrence(self):
        L=F(24); coefficient=F(7,13); h=F(1,100)
        probability=L**2*coefficient*h**5
        self.assertEqual(probability/h**5,L**2*coefficient)
        self.assertNotEqual(probability/h**5,coefficient)

    def test_radial_measure_exponent(self):
        self.assertEqual(F(1)+F(3)+F(1),5)  # r, failure r^3, dr
        self.assertEqual((F(3)**5-F(1)**5)/5,F(242,5))

    def test_affine_hessian_midpoint(self):
        pars=(F(1),F(-2),F(2),F(3),F(5))
        a=(F(-1,2),F(1,3)); b=(F(2,3),F(-1,4))
        self.assertEqual(c.cubic_hessian(pars,a),(F(-16,3),F(0),F(-11,6)))
        midpoint=tuple((x+y)/2 for x,y in zip(a,b))
        ha,hb,hm=(c.cubic_hessian(pars,z) for z in (a,b,midpoint))
        self.assertEqual(hm,tuple((x+y)/2 for x,y in zip(ha,hb)))

    def test_degree_three_restriction_is_essential(self):
        # Quartic -(x²-1)²-y² has two critical strict maxima.
        for x in [F(-1),F(1)]:
            self.assertEqual(-4*x*(x*x-1),0)
            self.assertEqual(-12*x*x+4,-8)
        # Its Hessian at x=0 is +4, not midpoint of endpoint values -8.
        self.assertNotEqual(F(4),F(-8))

    def test_homogeneous_coercivity_requires_discriminant(self):
        # H=x³ alone has grad H=0 along nonzero y-axis.
        x,y=F(0),F(1)
        self.assertEqual((3*x*x,F(0)),(F(0),F(0)))
        self.assertNotEqual(x*x+y*y,0)

    def test_annulus_budget_includes_linear_term(self):
        self.assertEqual(c.annulus_budget(F(2),F(16),F(1,64),F(1,16)),F(29,128))
        self.assertLess(c.annulus_budget(F(2),F(16),F(1,64),F(1,16)),F(3,4))
        # A false budget dropping C/R can accept R=1 even when error exceeds c.
        self.assertGreater(c.annulus_budget(F(3,5),F(1),F(1,1000),F(1,1000)),1)

    def test_invalid_count_laws_rejected(self):
        for law in [{-1:F(1)},{True:F(1)},{0:F(1,2)},{0:F(-1),1:F(2)}]:
            with self.assertRaises(ValueError): c.count_statistics(law)

    def test_wrong_manifest_digest_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'SOURCES.json'; path.write_text('{}')
            with self.assertRaisesRegex(ValueError,'manifest digest'):
                c.verify_sources(Path(tmp),path)

    def test_source_bytes_and_blob_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); (root/'x').write_bytes(b'abc')
            good={'local_path':'x','bytes':3,
                  'sha256':'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad',
                  'blob':'f2ba8f84ab5c1bce84a7b441cb1959cfc7093b7f'}
            c.verify_entry(root,good)
            for key,value in [('bytes',True),('sha256','0'*64),('blob','0'*40),('local_path','../x')]:
                with self.assertRaises(ValueError): c.verify_entry(root,dict(good,**{key:value}))
            (root/'link').symlink_to(root/'x')
            with self.assertRaises(ValueError): c.verify_entry(root,dict(good,local_path='link'))

if __name__=='__main__':
    unittest.main()
