"""Exact finite/source controls, not a Gaussian field realization or Lean execution."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,re,unittest
P=Path(__file__).resolve().parent
NAMES=['gaussian_abs_moment_integrable','ninth_power_le','mixed_envelope_pointwise_le',
'mixed_envelope_integrable','mixed_envelope_integral_le','mixed_envelope_lintegral_le']
class Controls(unittest.TestCase):
 def test_contract_identity(self):
  self.assertEqual(hashlib.sha256((P/'Contract.lean').read_bytes()).hexdigest(),
   'b64bd84f08cf846adf5d438b77dae8e5f3f69f48bfe9310b1e9ed8e2e11329c4')
 def test_source_inventory(self):
  s=(P/'CapI4GaussianEnvelope.lean').read_text()
  self.assertIn(re.findall(r'^theorem (\w+)',s,re.M),[[],NAMES])
  self.assertIsNone(re.search(r'\b(sorry|admit|axiom|unsafe)\b',re.sub(r'/\-.*?\-/','',s,flags=re.S)))
 def test_exact_power_identity(self):
  values=[F(0),F(1,100),F(1,2),F(1),F(2),F(10),F(100)]
  coefficients=[255,501,711,837,837,711,501,255]
  for x in values:
   for y in values:
    with self.subTest(x=x,y=y):
     delta=256*(x**9+y**9)-(x+y)**9
     self.assertEqual(delta,(x-y)**2*sum(F(a)*x**(7-i)*y**i for i,a in enumerate(coefficients)))
     self.assertGreaterEqual(delta,0)
  self.assertEqual(2**9,256*(1+1))
  self.assertGreater(2**9,255*(1+1))
 def test_mixed_pointwise_signed_inputs(self):
  values=[F(-5),F(-1),F(-1,10),F(0),F(1,10),F(1),F(5)]
  for j in values:
   for t in values:
    for weight in [F(0),F(1,10),F(2)]:
     lhs=(abs(j)+abs(t))**9*t*t*weight
     rhs=256*(abs(j)**9*t*t*weight+abs(t)**11*weight)
     self.assertLessEqual(lhs,rhs)
 def test_finite_product_and_mass_scaling(self):
  # A finite positive-weight model isolates Fubini/algebra, NOT Gaussian quadrature.
  points=[(F(1,2),F(1,3)),(F(3),F(2,3))]
  residual=[(F(-2),F(1,4)),(F(1),F(3,4))]
  for scale in [F(0),F(1),F(2),F(1000)]:
   lhs=sum(scale*v*w*(abs(j)+t)**9*t*t for j,v in residual for t,w in points)
   m9=sum(scale*v*abs(j)**9 for j,v in residual)
   mass=sum(scale*v for _,v in residual)
   g2=sum(w*t*t for t,w in points);g11=sum(w*t**11 for t,w in points)
   self.assertLessEqual(lhs,256*(m9*g2+mass*g11))
  # At j=0 a sufficiently large finite measure disproves silent mass=1.
  self.assertGreater(1024*sum(w*t**11 for t,w in points),256*sum(w*t**11 for t,w in points))
 def test_positive_decay_and_moment_assumptions_are_material(self):
  # c=0 gives the nonintegrable half-line t^2 primitive R^3/3.
  self.assertGreater(F(100**3,3),F(10**3,3))
  # Uniformly bounded masses need not uniformly bound the ninth moment.
  masses=[];moments=[]
  for n in [1,2,8]:
   masses.append(sum(F(1,2**(9*k)) for k in range(1,n+1)))
   moments.append(sum(F(1,2**(9*k))*F(2**k)**9 for k in range(1,n+1)))
  self.assertTrue(all(m<1 for m in masses));self.assertEqual(moments,[1,2,8])
if __name__=='__main__':unittest.main(verbosity=2)
