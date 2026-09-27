"""Uncertified unperiodized-Bargmann-Fock diagnostic; stable exponential scaling.

The finite square cutoff, quadrature grids and comparison values are diagnostic,
not interval error bounds. This does not evaluate the finite-L periodic model.
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path
from angular_contact import bf_z0, left_amplitude


def scaled_value(b,k,u,v,n):
    D=u*u-.25;Q0=-6*k*D/u;w0=u+.25/u
    theta0=-(2*u-3)*(2*u+1)**3/(32*u)
    K=1+v*v/(4*u*u);mean=Q0/(2*u*K);sigma=math.sqrt(2/K)
    cutoff=9.;h=2*cutoff/n
    grid=[]
    for i in range(n+1):
        z=-cutoff+i*h
        weight=(1 if i in (0,n) else 4 if i%2 else 2)*math.exp(-z*z/2)
        grid.append((z,weight))
    total=0.
    for zz,weight_c in grid:
        c=mean+sigma*zz
        w=w0-c*v*v/(12*k*u)
        inner=0.
        for tt,weight_d in grid:
            d=math.sqrt(6)*tt
            theta=theta0+c*D*v*v/(8*k*u)+d*v**3/(12*k)
            if not 0<theta<1:continue
            f1=4*theta-(w+1)**2
            f2=(w-1)**2-4*(1-theta)
            f3=(w+1-2*theta)**2+4*theta*(1-theta)
            if f1>0 and f2>0:
                inner+=weight_d*(9*k*k)**3*f1*f2*f3
        total+=weight_c*inner
    expectation=total*h*h/(9*2*math.pi)
    prefactor=math.exp(-b*b/4+Q0*Q0/(16*u*u*K))/(4*math.pi*bf_z0(b,k)*abs(u)*math.sqrt(K))
    return prefactor*expectation


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    if args.output.exists():raise SystemExit('new output required')
    b,k,u=0.,1.,-1.25;lim=left_amplitude(b,k,u)
    rows=[]
    for v in (.6,.4,.25,.15,.08):
        values=[scaled_value(b,k,u,v,n) for n in (80,160,320)]
        rows.append({'v':v,'scaled_lambda_grids':dict(zip(('80','160','320'),values)),
                     'scaled_lambda_over_limit':values[-1]/lim})
    report={'model':'unperiodized Bargmann-Fock, not SIDE24',
            'b':b,'k':k,'u':u,'scaling':'|v|^8 exp(Q0^2/(4 v^2)) Lambda_1',
            'asymptotic_amplitude':lim,'sigma_cutoff':9,'rows':rows,
            'certified_error_enclosure':False,'independent_acceptance':False}
    args.output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps(report,indent=2,sort_keys=True))

if __name__=='__main__':main()
