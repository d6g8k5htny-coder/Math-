#!/usr/bin/env python3
"""
GP-DATA-114-v1.0
Outward-rounded interval certificate for a full-dimensional degree-four
uniform-q Route-B PRCP box for r in (0,1/20].

Scope:
- certifies all 0<r<=1/20 with fixed q in a negative interval;
- gives positive widths in q and the other eight jet coordinates;
- certifies degree-four gates G0-G7 by interval sufficient conditions;
- certifies degree-four capture only; mass, exact-field transfer, P0.1, and P0.2 remain separate.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from mpmath import iv


def I(lo, hi=None):
    if hi is None:
        hi = lo
    return iv.mpf([str(lo), str(hi)])


def lower(x) -> float:
    return float(x.a)


def upper(x) -> float:
    return float(x.b)


def absmax(x) -> float:
    return max(abs(lower(x)), abs(upper(x)))


CENTER = {
    'a': 0.0025,
    'w': 0.0,
    'z': 1.0,
    'q': -1.0,
    'c40': 0.0,
    'c31': 0.0,
    'c22': 0.0,
    'c13': 0.0,
    'c04': 0.0,
}

RADII = {
    'a': 0.0001,
    'w': 0.001,
    'z': 0.01,
    'q': 0.02,
    'c40': 0.01,
    'c31': 0.01,
    'c22': 0.01,
    'c13': 0.01,
    'c04': 0.01,
}

R = I('0', '0.05')
R_MAX = 0.05
SIGMA = 0.1
KAPPA = 0.01
MU = 1 / (40 * iv.sqrt(I(2)))


def flow_x(X, Y, p):
    r, a, w = R, p['a'], p['w']
    c40, c31, c22, c13 = p['c40'], p['c31'], p['c22'], p['c13']
    return (
        X**2 - I('0.25') + a*X*Y + w*Y**2/2
        + r*(
            c40*(X**3-X/4)/6
            + c31*(3*X**2-I('0.25'))*Y/6
            + c22*X*Y**2/2
            + c13*Y**3/6
        )
    )


def flow_y(X, Y, p):
    r, a, w, z, s = R, p['a'], p['w'], p['z'], p['_s']
    c31, c22, c13, c04 = p['c31'], p['c22'], p['c13'], p['c04']
    return (
        a*(X**2-I('0.25'))/2 + s*Y + w*X*Y + z*Y**2/2
        + r*(
            c31*(X**3-X/4)/6
            + c22*X**2*Y/2
            + c13*X*Y**2/2
            + c04*Y**3/6
        )
    )


def hessian(X, Y, p):
    r, a, w, z, s = R, p['a'], p['w'], p['z'], p['_s']
    c40, c31, c22, c13, c04 = p['c40'], p['c31'], p['c22'], p['c13'], p['c04']
    j11 = (
        2*X + a*Y
        + r*(c40*(3*X**2-I('0.25'))/6 + c31*X*Y + c22*Y**2/2)
    )
    j12 = (
        a*X + w*Y
        + r*(
            c31*(3*X**2-I('0.25'))/6
            + c22*X*Y
            + c13*Y**2/2
        )
    )
    j22 = (
        s + w*X + z*Y
        + r*(c22*X**2/2 + c13*X*Y + c04*Y**2/2)
    )
    return j11, j12, j22


def cone_axis(xi, t, p):
    # Continuous quotient xi_dot/xi after X=1/2-xi, Y=t*xi.
    r, a, w = R, p['a'], p['w']
    c40, c31, c22, c13 = p['c40'], p['c31'], p['c22'], p['c13']
    return (
        12*a*t*xi - 6*a*t
        - 2*c13*r*t**3*xi**2
        + 6*c22*r*t**2*xi**2 - 3*c22*r*t**2*xi
        - 6*c31*r*t*xi**2 + 6*c31*r*t*xi - c31*r*t
        + 2*c40*r*xi**2 - 3*c40*r*xi + c40*r
        - 6*t**2*w*xi - 12*xi + 12
    )/12


def cone_y_quotient(xi, t, p):
    # Continuous quotient y_dot/xi after X=1/2-xi, Y=t*xi.
    r, a, w, z, s = R, p['a'], p['w'], p['z'], p['_s']
    c31, c22, c13, c04 = p['c31'], p['c22'], p['c13'], p['c04']
    return (
        12*a*xi - 12*a
        + 4*c04*r*t**3*xi**2
        - 12*c13*r*t**2*xi**2 + 6*c13*r*t**2*xi
        + 12*c22*r*t*xi**2 - 12*c22*r*t*xi + 3*c22*r*t
        - 4*c31*r*xi**2 + 6*c31*r*xi - 2*c31*r
        + 24*s*t + 12*t**2*xi*z - 24*t*w*xi + 12*t*w
    )/24


def make_box(radii=None):
    radii = RADII if radii is None else radii
    return {k: I(CENTER[k]-radii[k], CENTER[k]+radii[k]) for k in CENTER}


def certify(radii=None, kappa=KAPPA):
    radii = RADII if radii is None else radii
    if any(radii[k] <= 0 for k in CENTER):
        return {'pass': False, 'failure_class': 'FULL_DIMENSIONAL_BOX_FAIL', 'failed_gates': ['positive_width_all_coordinates']}

    p = make_box(radii)
    q_hi = CENTER['q'] + radii['q']
    if not (q_hi < 0):
        return {'pass': False, 'failure_class': 'Q_NEGATIVITY_FAIL', 'failed_gates': ['q_strictly_negative']}
    s_worst = q_hi / R_MAX
    p['_s'] = I(s_worst)
    kap = I(kappa)
    xi = I(0, SIGMA)
    t = I(-kappa, kappa)

    F = abs(p['a'])/8 + R*abs(p['c31'])/48
    A = (abs(p['z']) + R*abs(p['c13'])/2)*F
    B = R*abs(p['c04'])*F**2/2
    C = abs(p['w'])/2 + MU + R*abs(p['c22'])/8 + A/MU + B/MU**2
    W = F/MU

    AS = 1 + R*p['c40']/12
    BS = p['a']/2 + R*p['c31']/12
    DS = p['_s'] + p['w']/2 + R*p['c22']/8
    AM = -1 + R*p['c40']/12
    BM = -p['a']/2 + R*p['c31']/12
    DM = p['_s'] - p['w']/2 + R*p['c22']/8
    detS = AS*DS - BS**2
    detM = AM*DM - BM**2
    axial = AS-DS
    tau_upper = float('inf') if lower(axial) <= 0 else absmax(BS)/lower(axial)

    axis = cone_axis(xi, t, p)
    upper_cone = kap*cone_axis(xi, kap, p) - cone_y_quotient(xi, kap, p)
    lower_cone = kap*cone_axis(xi, -kap, p) + cone_y_quotient(xi, -kap, p)

    Xc = I(-0.5+SIGMA, 0.5-SIGMA)
    top = -flow_y(Xc, W, p)
    bottom = flow_y(Xc, -W, p)
    Ystrip = I(-upper(W), upper(W))
    drift = -flow_x(Xc, Ystrip, p)
    _, _, py = hessian(Xc, Ystrip, p)

    rho = 2*iv.sqrt(I(SIGMA**2)+W**2)
    rho_upper = upper(rho)
    Xcap = I(-0.5-rho_upper, -0.5+rho_upper)
    Ycap = I(-rho_upper, rho_upper)
    h11, h12, h22 = hessian(Xcap, Ycap, p)
    offdiag = absmax(h12)

    bounds = {
        'threshold_slack': lower(-p['_s']-C),
        'saddle_det_negative_margin': -upper(detS),
        'maximum_A_negative_margin': -upper(AM),
        'maximum_D_negative_margin': -upper(DM),
        'maximum_det_positive_margin': lower(detM),
        'axial_gap_margin': lower(axial),
        'cone_slope_margin': kappa-2*tau_upper,
        'cone_axis_margin': lower(axis),
        'cone_upper_inward_margin': lower(upper_cone),
        'cone_lower_inward_margin': lower(lower_cone),
        'handoff_margin': lower(W)/2-kappa*SIGMA,
        'strip_top_inward_margin': lower(top),
        'strip_bottom_inward_margin': lower(bottom),
        'central_drift_margin': lower(drift),
        'partial_y_contraction_margin': -upper(py),
        'chart_x_margin': 0.75-(0.5+rho_upper),
        'chart_y_margin': 1-rho_upper,
        'capture_gershgorin_margin_1': lower(-h11)-offdiag,
        'capture_gershgorin_margin_2': lower(-h22)-offdiag,
    }
    failed = [k for k,v in bounds.items() if not (v > 0)]
    return {
        'pass': not failed,
        'failure_class': None if not failed else 'INTERVAL_GATE_FAIL',
        'failed_gates': failed,
        'box': {k: [CENTER[k]-radii[k], CENTER[k]+radii[k]] for k in CENTER},
        'radii': radii,
        'fixed': {'r_interval': [0.0, R_MAX], 'q_interval': [CENTER['q']-radii['q'], CENTER['q']+radii['q']], 's_upper_worst': s_worst, 'sigma': SIGMA, 'kappa': kappa, 'mu_interval': [lower(MU), upper(MU)]},
        'derived_intervals': {'W': [lower(W), upper(W)], 'rho': [lower(rho), upper(rho)], 'tau_upper': tau_upper},
        'lower_bounds': bounds,
        'monotonicity_ledger': {
            'domain': '0<r<=1/20 and q in [-1.02,-0.98]',
            'relation': 's=q/r <= q_hi/r_max = -19.6',
            'worst_case_s': 'All stored lower margins are monotone nondecreasing as s becomes more negative; evaluate at largest admissible s=-19.6.',
            'affected_gates': [
                'threshold', 'endpoint typing', 'axial gap', 'cone faces',
                'strip faces', 'partial-y contraction', 'capture h22'
            ],
            's_independent_gates': [
                'cone axis', 'handoff', 'central X drift', 'chart containment',
                'capture h11'
            ]
        },
    }


def controls():
    out = []

    r0 = dict(RADII); r0['c04'] = 0
    a = certify(r0)
    out.append({'id': 'NC1_ZERO_WIDTH', 'required': 'FULL_DIMENSIONAL_BOX_FAIL', 'observed': a['failure_class'], 'pass': a['failure_class']=='FULL_DIMENSIONAL_BOX_FAIL'})

    r1 = dict(RADII); r1['c40'] = 500
    b = certify(r1)
    out.append({'id': 'NC2_TYPING_DESTROYED', 'required_any_failed_gate': ['saddle_det_negative_margin','maximum_det_positive_margin'], 'observed': b['failed_gates'], 'pass': bool(set(b['failed_gates']) & {'saddle_det_negative_margin','maximum_det_positive_margin'})})

    r2 = dict(RADII); r2['q'] = 1.1
    c = certify(r2)
    out.append({'id': 'NC3_Q_BOX_CROSSES_ZERO', 'required': 'Q_NEGATIVITY_FAIL', 'observed': c['failure_class'], 'pass': c['failure_class']=='Q_NEGATIVITY_FAIL'})

    d = certify(dict(RADII), kappa=0.00001)
    out.append({'id': 'NC4_CONE_TOO_NARROW', 'required_failed_gate': 'cone_slope_margin', 'observed': d['failed_gates'], 'pass': 'cone_slope_margin' in d['failed_gates']})

    r4 = dict(RADII); r4['a'] = 0.5
    e = certify(r4)
    out.append({'id': 'NC5_CAPTURE_CHART_DESTROYED', 'required_any_failed_gate': ['chart_x_margin','capture_gershgorin_margin_1'], 'observed': e['failed_gates'], 'pass': bool(set(e['failed_gates']) & {'chart_x_margin','capture_gershgorin_margin_1'})})

    assert all(x['pass'] for x in out)
    return out


def main():
    source = Path(__file__).read_bytes()
    primary = certify()
    assert primary['pass']
    receipt = {
        'schema': 'p01-uniformq-degree4-box/1.0',
        'source_filename': Path(__file__).name,
        'source_bytes': len(source),
        'source_sha256': hashlib.sha256(source).hexdigest(),
        'box_id': 'P01-UNIFORMQ-D4-BOX-001',
        'primary': primary,
        'negative_controls': controls(),
        'overall': 'PASS_UNIFORM_R_FIXED_Q_FULL_DIMENSIONAL_DEGREE4_INTERVAL_BOX',
        'explicit_exclusions': [
            'NO Gaussian or Palm mass lower bound in this source',
            'NO exact-field transfer',
            'NO exact full-field Palm or adjacency theorem',
            'NO P0.1/P0.2/Theorem B promotion',
        ],
    }
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
