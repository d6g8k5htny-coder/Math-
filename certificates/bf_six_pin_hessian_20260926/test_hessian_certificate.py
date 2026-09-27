"""Finite exact controls; the all-order analytic proof must be read separately."""
import copy
from fractions import Fraction as F
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parent

class HessianCertificateTests(unittest.TestCase):
    def setUp(self):
        path=ROOT/'hessian_certificate.py'
        self.assertTrue(path.exists(), 'Missing endpoint-Hessian certificate implementation')
        spec=importlib.util.spec_from_file_location('hessian_subject',path)
        self.m=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.m)

    def test_regression_polynomials(self):
        self.assertEqual(self.m.regression_check(), {'gram_determinant':True,'schur_numerator':True,'inverse_identity':True})

    def test_regression_inputs_are_kernel_derivatives(self):
        P=self.m.Poly;r,c=self.m.R,self.m.C
        def hermite(n,z):
            a,b=P(1),z
            if n==0:return a
            for k in range(1,n):a,b=b,z*b-k*a
            return b
        def cov(alpha,beta,site_a,site_b):
            d=(site_a-site_b)*r
            return (-1)**sum(alpha)*hermite(alpha[0]+beta[0],d)*hermite(alpha[1]+beta[1],P(0))*(c if site_a!=site_b else P(1))
        pins=[((0,0),0),((1,0),0),((0,0),1),((1,0),1)]
        G,b=self.m.regression_inputs()
        self.assertEqual(G,[[cov(a,z,i,j) for z,j in pins] for a,i in pins])
        self.assertEqual(b,[cov((2,0),a,0,i) for a,i in pins])
        for a,i in pins+[((0,1),0),((0,1),1),((2,0),0),((1,1),0)]:
            self.assertEqual(cov((0,2),a,0,i)+cov((0,0),a,0,i),0)
        self.assertEqual(cov((0,2),(0,2),0,0)+2*cov((0,2),(0,0),0,0)+1,2)

    def test_wrong_gram_sign_is_not_an_identity(self):
        G,b=self.m.regression_inputs();G[0][3]=-G[0][3];G[3][0]=G[0][3]
        with self.assertRaises(ValueError):self.m.regression_check(G,b)

    def test_wrong_cross_vector_is_refused(self):
        G,b=self.m.regression_inputs();b[3]=-b[3]
        with self.assertRaises(ValueError):self.m.regression_check(G,b)

    def test_series_leading_cancellations(self):
        self.assertEqual([self.m.d_coeff(n) for n in range(4)], [F(0)]*4)
        self.assertEqual([self.m.a_coeff(n) for n in range(6)], [F(0)]*6)
        self.assertEqual(self.m.d_coeff(4),F(1,12));self.assertEqual(self.m.a_coeff(6),F(1,72))

    def test_forward_difference_seeds(self):
        self.assertEqual(self.m.positivity_seeds(), {'D':[2,8,14], 'A':[10,46,94,122]})

    def test_finite_coefficients_match_exponential_convolutions(self):
        from math import factorial
        for n in range(4,25):
            self.assertEqual(self.m.d_coeff(n),sum(F(1,factorial(k)*factorial(n-k)) for k in range(1,n))-F(1,factorial(n-2)))
        for n in range(6,25):
            self.assertGreater(self.m.a_coeff(n),0)

    def test_uniform_axial_bounds_strictly_imply_target(self):
        lo,hi=self.m.axial_bounds(F(1,40))
        self.assertGreater(lo,F(1,7));self.assertLess(hi,F(1,5))

    def test_smaller_radius_is_not_worse(self):
        a,b=self.m.axial_bounds(F(1,40));c,d=self.m.axial_bounds(F(1,80))
        self.assertGreaterEqual(c,a);self.assertLessEqual(d,b)

    def test_radius_domain_is_strict(self):
        for r in [F(0),F(-1,40),F(1,2),1,True,0.025,'1/40']:
            with self.subTest(r=r):
                with self.assertRaises((ValueError,TypeError)):self.m.axial_bounds(r)

    def test_report_has_specific_law_and_matrix_scope(self):
        r=self.m.build_report()
        self.assertEqual(r['covariance_lower'],'1/7');self.assertEqual(r['covariance_upper'],'2')
        self.assertEqual(r['coordinates'],['f_tt(M)/r^2','f_ts(M)/r','f_ss(M)'])
        self.assertEqual(r['conditioning'],'six linear endpoint pins; no determinant or type reweighting')
        self.assertEqual(r['model'],'unperiodized planar Bargmann-Fock, K=exp(-|x-y|^2/2)')
        self.assertFalse(r['scientific_status_authority']);self.assertEqual(r['review_status'],'REVIEW_REQUIRED')
        self.assertEqual(r['r_domain'],'0<r<=1/40')
        self.assertEqual(r['centered_residual_determinant_second_moment_upper'],str(2*F(1,5)+3*F(1,2)**2)+' * r^4')

    def test_certificate_rejects_every_scope_and_bound_mutation(self):
        original=self.m.build_report();self.m.validate_report(original)
        for key,val in [('covariance_lower','1/6'),('covariance_upper','1'),('r_domain','0<=r<=1/40'),('conditioning','Palm'),('model','SIDE24'),('review_status','ACCEPT'),('scientific_status_authority',True),('kernel_checked',True)]:
            with self.subTest(key=key):
                altered=copy.deepcopy(original);altered[key]=val
                with self.assertRaises(ValueError):self.m.validate_report(altered)

    def test_certificate_rejects_extra_fields_and_numeric_identifiers(self):
        for change in [{'lemma_closed':True},{'covariance_lower':1},{'dimension':True}]:
            with self.assertRaises(ValueError):self.m.validate_report(dict(self.m.build_report(),**change))

    def test_checked_json_matches_generated_certificate(self):
        self.assertTrue((ROOT/'CERTIFICATE.json').exists(),'Missing generated certificate')
        self.m.validate_report(json.loads((ROOT/'CERTIFICATE.json').read_text()))

    def test_cli_normal_and_optimized_identical(self):
        outputs=[]
        for flags in [[],['-O']]:
            p=subprocess.run([sys.executable,*flags,'-B','-S',str(ROOT/'hessian_certificate.py')],capture_output=True,text=True,timeout=10)
            self.assertEqual(p.returncode,0,p.stderr);outputs.append(p.stdout)
        self.assertEqual(*outputs);self.m.validate_report(json.loads(outputs[0]))

    def test_cli_changed_claim_fails_in_both_modes(self):
        bad=self.m.build_report();bad['covariance_lower']='1/6'
        with tempfile.TemporaryDirectory() as d:
            pth=Path(d)/'bad.json';pth.write_text(json.dumps(bad))
            for flags in [[],['-O']]:
                p=subprocess.run([sys.executable,*flags,'-B','-S',str(ROOT/'hessian_certificate.py'),'--check',str(pth)],capture_output=True,text=True,timeout=10)
                self.assertNotEqual(p.returncode,0);self.assertIn('REFUSED',p.stderr)

if __name__=='__main__':unittest.main()
