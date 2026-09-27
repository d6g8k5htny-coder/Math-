from fractions import Fraction as Q

def corrected(k,u,v,a,q,c,d):
    k,u,v,a,q,c,d=map(Q,(k,u,v,a,q,c,d))
    gx=6*k*(u*u-Q(1,4))+q*u*v+Q(1,2)*c*v*v
    gy_lead=a*v
    gy_axial=Q(1,2)*q*(u*u-Q(1,4))
    hnext=k*(2*u**3-Q(3,2)*u-Q(1,2))+Q(1,2)*q*(u*u-Q(1,4))*v+Q(1,2)*c*u*v*v+Q(1,6)*d*v**3
    return gx,gy_lead,gy_axial,hnext

def exact_witness(r,b,k,u,v,a,q,c,d):
    r,b,k,u,v,a,q,c,d=map(Q,(r,b,k,u,v,a,q,c,d)); x=r*u; z=r*v
    f=b-k*r**3/Q(2)+2*k*x**3-Q(3,2)*k*r*r*x+a*z*z/Q(2)+q*(x*x-r*r/Q(4))*z/Q(2)+c*x*z*z/Q(2)+d*z**3/Q(6)
    fx=6*k*x*x-Q(3,2)*k*r*r+q*x*z+c*z*z/Q(2)
    fz=a*z+q*(x*x-r*r/Q(4))/Q(2)+c*x*z+d*z*z/Q(2)
    return f,fx,fz
