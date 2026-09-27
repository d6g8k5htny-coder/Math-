"""Exact finite ledgers for the all-height annulus bridge candidate.

These helpers check algebra/scaling only. They do not certify Gaussian
covariance bounds, Kac--Rice hypotheses, or mathematical acceptance.
"""
from fractions import Fraction as Q
from math import factorial
import json


def exact(x):
    if isinstance(x,bool) or not isinstance(x,(int,Q)):
        raise TypeError('use an integer or exact Fraction')
    return Q(x)


def contact_gradient(k,u,v,q,c):
    k,u,v,q,c=map(exact,(k,u,v,q,c))
    return 6*k*(u*u-Q(1,4))+q*u*v+c*v*v/2


def transverse_matrix(u,v):
    u,v=map(exact,(u,v))
    # Columns are the genuinely random midpoint jets (f_zz,f_xxz,f_xzz).
    return [[Q(0),u*v,v*v/2],[v,Q(0),Q(0)]]


def aspect_matrix(u,alpha,beta):
    u,alpha,beta=map(exact,(u,alpha,beta))
    if abs(u)<=1:
        raise ValueError('fixed longitudinal chart requires |u|>1')
    if alpha<0 or alpha*alpha+beta*beta!=1:
        raise ValueError('closed unit semicircle required')
    aq=u*(u*u-Q(1,4))/6
    bt=(u*u-Q(1,4))/2
    return [[aq*alpha,u*beta,Q(0)],[Q(0),bt*alpha,beta]]


def aspect_minors(u,alpha,beta):
    u,alpha,beta=map(exact,(u,alpha,beta))
    aspect_matrix(u,alpha,beta)  # Validate the same domain.
    aq=u*(u*u-Q(1,4))/6
    bt=(u*u-Q(1,4))/2
    return aq*bt*alpha**2, aq*alpha*beta, u*beta**2


def rank_floor(u):
    u=exact(u)
    if abs(u)<=1:
        raise ValueError('fixed longitudinal chart requires |u|>1')
    aq=u*(u*u-Q(1,4))/6
    bt=(u*u-Q(1,4))/2
    return min(aq*aq*bt*bt,u*u)/2


def suppression(r,v):
    r,v=map(exact,(r,v))
    if r<=0:
        raise ValueError('positive separation required')
    if v==0:
        return Q(1)
    return min(Q(1),(r/abs(v))**6)


def absorption_constant(c):
    c=exact(c)
    if c<=0:
        raise ValueError('positive Gaussian exponential coefficient required')
    # exp(-c/s^2) <= 7! c^-7 s^14 for s>0.
    return Q(factorial(7))/c**7


def power_ledger():
    gradient_r=-3
    normalizer_r=-2
    gradient_delta=-2
    sixth_moment_delta=-6
    three_hessians_r=6
    three_hessians_v=-6
    area_r=2
    outer_r=gradient_r+normalizer_r+three_hessians_r
    outer_v=gradient_delta+sixth_moment_delta+three_hessians_v
    inner_r=gradient_r+normalizer_r+gradient_delta+sixth_moment_delta
    order=7
    return {
        'gradient_density_r_power':gradient_r,
        'gradient_density_delta_power':gradient_delta,
        'original_normalizer_r_power':normalizer_r,
        'conditional_sixth_moment_delta_power':sixth_moment_delta,
        'three_hessian_geometric_r_power':three_hessians_r,
        'three_hessian_geometric_v_power':three_hessians_v,
        'physical_to_scaled_area_r_power':area_r,
        'outer_physical_r_power':outer_r,
        'outer_scaled_r_power':outer_r+area_r,
        'outer_inverse_v_power':-outer_v,
        'inner_physical_r_power':inner_r,
        'absorption_order':order,
        'inner_after_absorption_r_power':inner_r+2*order,
        'outer_after_absorption_v_power':outer_v+2*order,
        'height_window_r_power':0,
    }


def result():
    return {
        'object':'D5-ALL-HEIGHT-ANNULUS-BRIDGE-20260925-v1',
        'ledger':power_ledger(),
        'all_witness_heights':True,
        'dimension':2,
        'fixed_inner_radius_strictly_greater_than_one':True,
        'positive_compact_gap_marks_required':True,
        'mathematical_acceptance':False,
        'global_RN_closed':False,
        'scientific_effect':'NONE',
        'meaning':'finite algebra/scaling controls for an unreviewed analytic candidate',
    }


if __name__=='__main__':
    print(json.dumps(result(),indent=2,sort_keys=True))
