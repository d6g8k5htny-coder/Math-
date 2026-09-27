"""Finite-pin algebra and conservative stitching ledgers, not analytic verification.

The existing exact polynomial ring has variables (r,x,z,u,v), with v=t here.
All arithmetic is rational. No numerical covariance grid substitutes for a proof.
"""
from __future__ import annotations
from fractions import Fraction as Q
import json
import thin_tube as p


def contact_matrix():
    """Rows J1,J2,J3; columns f_zz,f_xxz,f_xzz,f_zzz at contact."""
    gap=p.add(p.power(p.u,2),p.constant(Q(-1,4)))
    return [[{},p.mul(p.u,p.v),p.scale(p.power(p.v,2),Q(1,2)),{}],
            [p.v,{},{},{}],
            [{},p.scale(p.mul(gap,p.v),Q(1,4)),{},p.scale(p.power(p.v,3),Q(-1,12))]]


def extract_contact(f):
    """Exact coefficients after (x,z)=(r*u,r*v), including height shear."""
    replacements={1:p.mul(p.r,p.u),2:p.mul(p.r,p.v)}
    value=p.substitute(f,replacements)
    gx=p.substitute(p.derivative(f,1),replacements)
    gz=p.substitute(p.derivative(f,2),replacements)
    height=p.add(value,p.scale(p.mul(p.mul(p.r,p.v),gz),Q(-1,2)))
    for raw,order in ((gx,2),(gz,1),(height,3)):
        if any(p.coefficient_r(raw,n) for n in range(order)):
            raise ValueError('input does not have the required pin-compatible cancellations')
    return [p.coefficient_r(gx,2),p.coefficient_r(gz,1),p.coefficient_r(height,3)]


def cutoff_margin(q):
    q=Q(q)
    return 1-12*q


def cutoff_safe(q):
    q=Q(q)
    return 0<q<=1 and cutoff_margin(q)>0


def triangle_inverse(u,t):
    u,t=Q(u),Q(t)
    if not t:raise ValueError('collinear configuration needs the inner chart')
    return [[Q(1),-(u+Q(1,2))/t],[Q(0),1/t]]


def ledger():
    eigenfloor=12
    density=Q(3,2)*eigenfloor
    sixth_moment=6*eigenfloor
    geometric=6
    raw_density=-6
    triple_determinant=6
    height_window=3
    normalizer=-2
    intensity=raw_density+triple_determinant+height_window+normalizer
    return {'object':'D5-FIXED-ANNULUS-STITCH-20260925-v1',
            'eigenfloor_t':eigenfloor,'density_t':int(density),
            'sixth_moment_t':sixth_moment,'geometric_t':geometric,
            'total_angular_t':int(density)+sixth_moment+geometric,
            'raw_density_r':raw_density,'triple_determinant_r':triple_determinant,
            'height_window_r':height_window,'normalizer_r':normalizer,
            'physical_intensity_r':intensity,'area_r':2,'count_r':intensity+2,
            'cutoff':'r^(1/24)','covariance_perturbation_margin':'r^(1/2)',
            'outer_chart_covers_axis':False,'analytic_verification':False,
            'independent_review':False,'global_RN_closed':False,
            'scientific_effect':'NONE'}

if __name__=='__main__':print(json.dumps(ledger(),indent=2,sort_keys=True))
