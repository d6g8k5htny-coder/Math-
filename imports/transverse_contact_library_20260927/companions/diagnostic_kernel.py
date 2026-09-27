"""Unperiodized Bargmann-Fock diagnostic only; NOT a certified enclosure.

The exact periodic theorem uses its own conditional Gaussian covariance.
This optional standard-library Simpson calculation checks the new contact
integral on one unperiodized example and reports a refinement ladder.
"""
import json
from math import cos, erf, exp, isfinite, pi, sin, sqrt

def kernel(n=64, *, u=-0.5, v=1.0, b=0.0, k=1/6):
    if type(n) is not int or n<2 or n%2:
        raise ValueError('positive even Simpson subdivision count >=2 required')
    if not all(isfinite(t) for t in (u,v,b,k)) or v==0 or k<=0:
        raise ValueError('finite parameters, v !=0 and k>0 required')
    phi=exp(-b*b/4)/sqrt(2*pi)
    Phi=0.5*(1+erf(b/2))
    z0=36*k*k*((b*b+2)*Phi+b*sqrt(2)*phi)
    if z0<=0:
        raise ValueError('normalizer underflow/cancellation; use higher precision')
    pref=144*k*k/(z0*abs(v)**7)
    total=0.0
    for i in range(n+1):
        ph=pi*i/(2*n);sn,cs=sin(ph),cos(ph);theta=sn*sn
        low=-1-2*sn;high=1-2*cs;width=high-low
        wi=1 if i in (0,n) else (4 if i%2 else 2)
        inner=0.0
        for j in range(n+1):
            w=low+width*j/n
            q=6*k*(w-2*u)/v
            D=u*u-.25;Lc=2*u**3-1.5*u-.5
            c=-12*k*D/v**2-2*q*u/v
            d=12*k*(Lc+theta)/v**3+3*q*D/v**2
            g=exp(-b*b/4-q*q/4-c*c/4-d*d/12)/(16*sqrt(3)*pi*pi)
            dm=4*theta-(w+1)**2
            ds=4*(1-theta)-(w-1)**2
            dx=-((w+1-2*theta)**2+4*theta*(1-theta))
            wj=1 if j in (0,n) else (4 if j%2 else 2)
            inner+=wj*g*(9*k*k/(v*v))**3*dm*ds*dx
        total+=wi*inner*width*(2*sn*cs)
    return pref*total*(pi/(2*n)/3)*(1/n/3)

if __name__=='__main__':
    print(json.dumps({
        'meaning':'uncertified numerical diagnostic, not periodic/SIDE24 coefficient',
        'covariance':'exp(-|x-y|^2/2), unperiodized',
        'parameters':{'u':-.5,'v':1.,'b':0.,'k':1/6},
        'saddle_contact_kernel_estimates':[{'n':n,'estimate':kernel(n)}for n in (16,32,64,128,256)],
        'rigorous_error_bound':None,
        'independent_analytic_acceptance':False,
    },indent=2)+'\n')
