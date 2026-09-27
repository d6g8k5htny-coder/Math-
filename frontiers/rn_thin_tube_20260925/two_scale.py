"""Exact algebra for the TWO_SCALE_ADDENDUM; not an analytic proof checker.

Reuse the existing rational-polynomial engine. In returned contact polynomials,
slots (x,z,u) denote (alpha,beta,u); no numerical covariance model is substituted.
"""
from __future__ import annotations
from fractions import Fraction as Q
import json
import thin_tube as p


def contact_rows():
    gap=p.add(p.power(p.u,2),p.constant(Q(-1,4)))
    a=p.scale(p.mul(p.u,gap),Q(1,6))
    b=p.scale(gap,Q(1,2))
    alpha,beta=p.x,p.z
    return [[p.mul(a,alpha),p.mul(p.u,beta),{}],
            [{},p.mul(b,alpha),beta]]


def normalized_orders(polynomial, component):
    """Expand derivative at (r*u,r*t), then put r=delta*alpha,t=delta*beta.

    component 1 is divided by r^2*delta; component 2 by r*delta.
    Exact powers of delta, including negative drift orders, are returned.
    """
    if type(component) is not int or component not in (1,2):
        raise ValueError('component must be integer 1 or 2')
    base=3-component
    derivative=p.derivative(polynomial,component)
    raw=p.substitute(derivative,{1:p.mul(p.r,p.u),2:p.mul(p.r,p.v)})
    out={}
    for e,c in raw.items():
        r_degree,physical_x,physical_z,u_degree,t_degree=e
        if physical_x or physical_z or r_degree<base:
            raise ValueError('polynomial is incompatible with the claimed normalization')
        order=r_degree+t_degree-base-1
        term=p.monomial((0,r_degree-base,t_degree,u_degree,0),c)
        out[order]=p.add(out.get(order,{}),term)
    return {order:terms for order,terms in out.items() if terms}


def contact_limit(polynomial,component):
    orders=normalized_orders(polynomial,component)
    if any(n<0 for n in orders):
        raise ValueError('singular residual: original finite-r pins were not removed')
    return orders.get(0,{})


def minors(rows=None):
    rows=contact_rows() if rows is None else rows
    return [p.determinant([[rows[0][i],rows[0][j]],
                           [rows[1][i],rows[1][j]]])
            for i,j in ((0,1),(0,2),(1,2))]


def power_width_exponent(gamma):
    if type(gamma) is float or type(gamma) is bool:
        raise ValueError('use an exact rational gamma')
    gamma=Q(gamma)
    if not 0<gamma<=1:
        raise ValueError('this corollary requires 0<gamma<=1')
    return -3-7*gamma


def report():
    return {
        'object':'D5-TWO-SCALE-20260925-v1',
        'coordinates':'(r*u,r*t)',
        'delta':'sqrt(r^2+t^2)',
        'aspect_constraint':'alpha>=0, alpha^2+beta^2=1',
        'normalization':['r^2*delta','r*delta'],
        'contact_rows':[['a(u)*alpha','u*beta','0'],['0','b(u)*alpha','beta']],
        'a':'u*(u^2-1/4)/6', 'b':'(u^2-1/4)/2',
        'minors':['a*b*alpha^2','a*alpha*beta','u*beta^2'],
        'density_bound':'C*r^-3*delta^-2*exp(-c/delta^2)',
        'weighted_density_bound':'C*r^-5*delta^-8*exp(-c/delta^2)',
        'power_width_count':'C*r^(-3-7*gamma)*exp(-c_gamma/r^(2*gamma))',
        'scope':'d=2; fixed L,A>1,B; compact b; 0<k_-<=k<=k_+; delta small',
        'original_proof_changed':False,
        'analytic_verification_by_tests':False,
        'independent_review':False,
        'fixed_scaled_annulus_closed':False,
        'scientific_effect':'NONE',
    }

if __name__=='__main__':
    print(json.dumps(report(),indent=2,sort_keys=True))
