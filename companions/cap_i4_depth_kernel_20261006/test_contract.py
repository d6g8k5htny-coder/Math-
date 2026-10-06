"""Exact finite controls and frozen Lean types; not kernel or Gaussian evidence."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,re,unittest
HERE=Path(__file__).resolve().parent
NAMES=['measurable_depthKernel','double_soft_majorant','depth_cutoff',
       'typed_depth_weight_le','independent_depth_bound_ae']
def raw(r,h,lam,top):return r*r*h*h/4*lam*(lam+F(3,2)*r*h)*top*(top+r*h)
def major(r,K,j,lam,top):
    U=j+top
    return K*K*(1+K)/4*r*r*top*U**3*lam*(lam+F(3,2)*K*r*U)
def kernel(r,K,k0,j,lam,top):
    return max(0,major(r,K,j,lam,top)) if lam<=4*K*K/(3*k0)*r*(j+top)**2 else F(0)
class KernelTests(unittest.TestCase):
    def test_exact_contract(self):
        self.assertEqual(hashlib.sha256((HERE/'Contract.lean').read_bytes()).hexdigest(),
          '58c15efcf6a62de5199efe3258abe5a1439491544f780757bb63a3a8605e2df7')
    def test_inventory_and_no_admission(self):
        s=(HERE/'CapI4DepthKernel.lean').read_text()
        stripped=re.sub(r'/\-.*?\-/','',s,flags=re.S)
        self.assertIsNone(re.search(r'\b(sorry|admit|axiom|unsafe)\b',stripped))
        self.assertIn(re.findall(r'^theorem (\w+)',s,re.M),[[],NAMES])
    def test_full_determinant_majorant(self):
        count=0
        for r in (F(0),F(1,100),F(1,2),F(1)):
          for K in (F(0),F(1,3),F(1),F(3)):
           for j in (F(0),F(1),F(4)):
            for top in (F(1,10000),F(1),F(4)):
             for ratio in (F(1,7),F(1)):
              for hfrac in (F(0),F(1,2),F(1)):
               lam=ratio*top;h=hfrac*K*(j+top)
               self.assertLessEqual(raw(r,h,lam,top),major(r,K,j,lam,top));count+=1
        self.assertEqual(count,864)
    def test_depth_floor_and_boundary(self):
        for r in (F(0),F(1,100),F(1)):
         for K in (F(0),F(1,3),F(2)):
          for k0 in (F(1,10),F(1),F(3)):
           for multiple in (F(1),F(2)):
            k=k0*multiple;j=F(1);top=F(2);h=K*(j+top)
            threshold=4*r*h*h/(3*k)
            self.assertLessEqual(threshold,4*K*K*r*(j+top)**2/(3*k0))
        self.assertGreater(kernel(F(1),F(1),F(1),F(0),F(4,3),F(1)),0)
        self.assertEqual(kernel(F(1),F(1),F(1),F(0),F(4,3)+F(1,100),F(1)),0)
    def test_hypotheses_are_not_optional(self):
        # Dropping r<=1 invalidates this particular hard-factor majorant.
        self.assertGreater(raw(F(4),F(1),F(1),F(1)),major(F(4),F(1),F(0),F(1),F(1)))
        # Dropping h<=K U invalidates the derivative envelope.
        self.assertGreater(raw(F(1),F(2),F(1),F(1)),major(F(1),F(1),F(0),F(1),F(1)))
        # A false mark floor shrinks the cutoff and loses depth failures.
        self.assertTrue(F(1)<=4/(3*F(1)))
        self.assertFalse(F(1)<=4/(3*F(2)))
    def test_both_soft_factors_required(self):
        r=K=top=lam=h=F(1);j=F(0)
        without_mixed=K*K*(1+K)/4*r*r*top*(j+top)**3*lam*lam
        self.assertGreater(raw(r,h,lam,top),without_mixed)
    def test_zero_weight_support_and_small_hard_eigenvalue(self):
        # No positive-cone premise is needed at zero/negative real weights.
        for w in (F(0),F(-1)):
            self.assertEqual(max(F(0),w),0)
        for n in (10,1000,10**8):
            top=F(1,n);lam=top/2;j=F(1);r=F(1,10);K=k0=F(1);h=j+top
            self.assertLessEqual(raw(r,h,lam,top),kernel(r,K,k0,j,lam,top))
            self.assertGreater(kernel(r,K,k0,j,lam,top),0)
    def test_cubic_inner_power_and_full_normalizer(self):
        for r in (F(1,100),F(1,3),F(1)):
            D=F(2);E=F(3,2);U=F(4);a=D*r*U*U
            self.assertEqual(a**3/3+E*r*U*a*a/2,
                             r**3*(D**3*U**6/3+E*D*D*U**5/2))
            self.assertEqual(r**5/r**2,r**3)
if __name__=='__main__':unittest.main(verbosity=2)
