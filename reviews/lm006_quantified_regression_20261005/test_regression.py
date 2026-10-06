"""Exact rational controls; these tests do not execute Lean or an infinite field."""
from fractions import Fraction as F
from pathlib import Path
import importlib.util, itertools, json, subprocess, sys, unittest
P=Path(__file__).with_name('regression_check.py')
class RegressionTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(P.is_file(), 'quantified-regression implementation not supplied')
        spec=importlib.util.spec_from_file_location('regression_check', P)
        self.m=importlib.util.module_from_spec(spec); spec.loader.exec_module(self.m)
    def test_kernel_constants(self):
        self.assertEqual(self.m.kernel_constants(), (F(3,16),F(1,8),F(1,4)))
    def test_frame_inverse(self):
        for r in (F(1),F(1,2),F(1,8)):
            for j in range(12):
                raw=tuple(F((j+3*i)%11-5,3) for i in range(6))
                self.assertEqual(self.m.inverse_frame(self.m.frame(raw,r),r),raw)
    def test_contact_rows(self):
        p,v,d=self.m.model(F(0))
        self.assertEqual(self.m.mul(p,self.m.transpose(p)),self.m.eye(6))
        m,res=self.m.condition(p,v,d)
        self.assertEqual(m[:2], [F(-1),F(1)])
        self.assertEqual(res[0], [F(0)]*11)
        self.assertEqual(res[1], [F(0)]*11)
        self.assertEqual(res[4],res[5])
    def test_residual_orthogonality(self):
        for k in range(1,9):
            p,v,d=self.m.model(F(1,2**k)); m,res=self.m.condition(p,v,d)
            self.assertEqual(self.m.mul(res,self.m.transpose(p)), [[F(0)]*6 for _ in range(6)])
    def test_conditional_mean(self):
        p=[[1,0],[0,1]]; v=[[2,1],[-1,3]]; d=[F(1,3),F(-2)]
        mean,res=self.m.condition(p,v,d)
        self.assertEqual(mean,[F(-4,3),F(-19,3)])
        self.assertEqual(res,[[F(0),F(0)],[F(0),F(0)]])
    def test_common_coupling_second_moment(self):
        m=[F(1,2),F(-1)]; n=[F(0),F(2)]
        a=[[F(1),F(2)],[F(-1),F(1)]]; b=[[F(2),F(1)],[F(0),F(-2)]]
        total=F(0)
        for z in itertools.product((-1,1),repeat=2):
            diff=[m[i]-n[i]+sum((a[i][j]-b[i][j])*z[j] for j in range(2)) for i in range(2)]
            total+=sum(x*x for x in diff)/4
        self.assertEqual(total,self.m.coupling_error_sq((m,a),(n,b)))
    def test_quantified_rate_and_nontrivial_error(self):
        y=self.m.condition(*self.m.model(F(0)))
        K2=F(10042,3)**2+F(2590)**2
        for k in range(6,15):
            r=F(1,2**k); p,v,d=self.m.model(r)
            e2=self.m.coupling_error_sq(self.m.condition(p,v,d),y)
            self.assertLessEqual(e2,K2*r*r)
            self.assertGreaterEqual(e2,F(1,2)*r*r)
    def test_pin_and_target_row_rates(self):
        p0,v0,_=self.m.model(F(0))
        for k in range(1,10):
            r=F(1,2**k); p,v,_=self.m.model(r)
            self.assertLessEqual(self.m.frob2(self.m.sub(p,p0)),4*r*r)
            self.assertLessEqual(self.m.frob2(self.m.sub(v,v0)),4*r*r)
    def test_singular_square_root_and_weaker_regularities(self):
        for n in (2,4,8,16,32):
            r=F(1,n)
            self.assertGreater(r,r*r)
            # F(x)=|x|^(7/2), h=1/n^2: adjusted A=21/(8n), r=2/n^2.
            self.assertEqual(F(21,8*n)/F(2,n*n),F(21*n,16))
            pins,targets,d=self.m.rough_model(n)
            mean,res=self.m.condition(pins,targets,d)
            h=F(1,n*n)
            expected=F(441,64)*h/(1+F(49,4)*h**3+F(9,16)*h**7)
            self.assertEqual(sum(x*x for x in res[0]),expected)
    def test_input_rejections(self):
        for r in (F(-1),F(2),True,0.1):
            with self.assertRaises((ValueError,TypeError)): self.m.model(r)
        with self.assertRaises(ValueError): self.m.inverse([[1,1],[1,1]])
        with self.assertRaises(ValueError): self.m.condition([[1,0]], [[1]], [1])
    def test_cli_controls_and_faults(self):
        names=['CONDITIONAL_MEAN','RESIDUAL_ORTHOGONALITY','CUBIC_PIN_TARGET','KERNEL_LIPSCHITZ_MASS','NO_SQRT_LIPSCHITZ','EXTRA_REGULARITY_REQUIRED']
        outputs=[]
        for flags in (['-B','-S'],['-B','-O','-S']):
            run=subprocess.run([sys.executable,*flags,str(P)],capture_output=True,text=True,timeout=20)
            self.assertEqual(run.returncode,0,run.stderr); self.assertEqual(run.stderr,'')
            self.assertGreater(json.loads(run.stdout)['controls'],0); outputs.append(run.stdout)
            for i,name in enumerate(names,1):
                bad=subprocess.run([sys.executable,*flags,str(P),'--mutant','M'+str(i)],capture_output=True,text=True,timeout=20)
                self.assertEqual((bad.returncode,bad.stdout,bad.stderr),(1,'','REGRESSION_FAIL: '+name+'\n'))
        self.assertEqual(outputs[0],outputs[1])
    def test_cli_invalid(self):
        for flags in (['-B','-S'],['-B','-O','-S']):
            for args in (['--mutant','M9'],['--bogus'],['--mutant']):
                run=subprocess.run([sys.executable,*flags,str(P),*args],capture_output=True,text=True,timeout=10)
                self.assertEqual(run.returncode,2)
if __name__=='__main__': unittest.main()
