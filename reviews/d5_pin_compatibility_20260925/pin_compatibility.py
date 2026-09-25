"""Exact deterministic pin/Taylor regression witness; not a Gaussian closure.

Only fractions.Fraction and standard-library operations are used. No external source
or scientific-status record is written. D denotes the longitudinal fourth derivative.
"""
from fractions import Fraction as Q
from math import factorial
import json


def family(r, k=1, b=0, A=-2, a=0, c=0, d=0, D=0):
    r,k,b,A,a,c,d,D = map(Q, (r,k,b,A,a,c,d,D))
    if r <= 0 or k <= 0:
        raise ValueError('positive radius and gap mark required')
    # F=b-k*r^3/2+2*k*x^3-3*k*r^2*x/2+A*z^2/2
    #   +a*(x^2-r^2/4)*z/2+c*x*z^2/2+d*z^3/6
    #   +D*(x^2-r^2/4)^2/24.
    return {
        (0,0): b-k*r**3/2+D*r**4/384,
        (3,0): 2*k, (1,0): -3*k*r**2/2,
        (0,2): A/2, (2,1): a/2, (0,1): -a*r**2/8,
        (1,2): c/2, (0,3): d/6,
        (4,0): D/24, (2,0): -D*r**2/48,
    }


def derivative(poly, x, z, dx=0, dz=0):
    if type(dx) is not int or type(dz) is not int or min(dx,dz)<0:
        raise ValueError('nonnegative integer derivative orders required')
    x,z=Q(x),Q(z)
    return sum((v*Q(factorial(i),factorial(i-dx))*Q(factorial(j),factorial(j-dz))
                *x**(i-dx)*z**(j-dz)
                for (i,j),v in poly.items() if i>=dx and j>=dz), Q(0))


def corrected_rows(y1,y2,k=1,A=-2,a=0,c=0,d=0):
    y1,y2,k,A,a,c,d = map(Q,(y1,y2,k,A,a,c,d))
    return {
        'grad_x_r2': 6*k*(y1**2-Q(1,4))+a*y1*y2+c*y2**2/2,
        'grad_z_r1': A*y2,
        'grad_z_r2': a*(y1**2-Q(1,4))/2+c*y1*y2+d*y2**2/2,
        'height_r2': A*y2**2/2,
        'height_r3': -k/2+2*k*y1**3-3*k*y1/2+a*(y1**2-Q(1,4))*y2/2+c*y1*y2**2/2+d*y2**3/6,
    }


def hessian(poly,x,z):
    xx=derivative(poly,x,z,2,0); xz=derivative(poly,x,z,1,1); zz=derivative(poly,x,z,0,2)
    return {'xx':xx,'xz':xz,'zz':zz,'det':xx*zz-xz*xz}


def witness():
    r,k,y=Q(1,10),Q(1),Q(2)
    p=family(r,k,A=-2,a=2)
    return {
        'source_pr': 'd6g8k5htny-coder/Math-#9',
        'source_commit': '25141b9154b5afcaa16e526f1d9055a2a4e2483d',
        'source_proof_blob': 'd56613025439cce57e76e2846a80af908fcd2dd6',
        'r':str(r),'k':str(k),'axial_y1':str(y),
        'actual_fx_over_r2':str(derivative(p,r*y,0,1,0)/r**2),
        'unshifted_claim_fx_over_r2':str(6*k*y**2),
        'actual_fz_over_r2':str(derivative(p,r*y,0,0,1)/r**2),
        'unshifted_claim_fz_over_r2':str(y**2),
        'scope':'Exact deterministic counterexample to the displayed pin/Taylor expansion; not a counterexample to a Gaussian theorem.',
        'mathematical_program_closed':False,
    }


if __name__=='__main__':
    print(json.dumps(witness(),sort_keys=True,indent=2))
