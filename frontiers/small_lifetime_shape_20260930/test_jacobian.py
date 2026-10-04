"""Independent exact differentiation of the square-to-lifetime shape map."""
from fractions import Fraction as F
import unittest
import shape

class Dual:
    def __init__(self,x,dr=0,dz=0):self.x,self.dr,self.dz=F(x),F(dr),F(dz)
    @staticmethod
    def cast(v):return v if isinstance(v,Dual) else Dual(v)
    def __add__(self,v):
        v=self.cast(v);return Dual(self.x+v.x,self.dr+v.dr,self.dz+v.dz)
    __radd__=__add__
    def __neg__(self):return Dual(-self.x,-self.dr,-self.dz)
    def __sub__(self,v):return self+-self.cast(v)
    def __rsub__(self,v):return self.cast(v)+-self
    def __mul__(self,v):
        v=self.cast(v);return Dual(self.x*v.x,self.dr*v.x+self.x*v.dr,self.dz*v.x+self.x*v.dz)
    __rmul__=__mul__
    def __truediv__(self,v):
        v=self.cast(v);return Dual(self.x/v.x,(self.dr*v.x-self.x*v.dr)/v.x**2,(self.dz*v.x-self.x*v.dz)/v.x**2)
    def __pow__(self,n):
        ans=Dual(1)
        for _ in range(n):ans=ans*self
        return ans

class JacobianTests(unittest.TestCase):
    def test_direct_doublet_density_binding(self):
        count=0
        for r0 in (F(1,100),F(1,5),F(1,2),F(4,5)):
            for z0 in (F(1,7),F(2,5),F(3,4)):
                r,z=Dual(r0,1,0),Dual(z0,0,1)
                w=1+2*r*z/(1+r)
                p=((1+r)*w*w+(1-r))/(4*w)
                x=p-F(1,2)
                e=r**3*z*z*(1+z)*(r*z+r+2)/((1+r)*(2*r*z+r+1))
                determinant=e.dr*x.dz-e.dz*x.dr
                self.assertTrue(shape.in_support(e.x,x.x))
                self.assertTrue(shape.doublet(e.x,x.x))
                self.assertEqual(shape.kernel(e.x,x.x)*abs(determinant),shape.square_density(r0,z0))
                pair=shape.companion(e.x,x.x)
                self.assertEqual(-pair[2],1/r0)
                count+=1
        self.assertEqual(count,12)

if __name__=='__main__':unittest.main()
