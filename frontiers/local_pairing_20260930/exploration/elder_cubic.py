"""Exploration: the elder-rule death partner of M in the limiting cubic landscape.

P(X,Z) = 2kX^3 - 3kX/2 - k/2 + (s/2)Z^2 + (a/2)(X^2-1/4)Z + (beta/2)XZ^2 + (c/6)Z^3   (CUB (C1))
M = (-1/2, 0) with P = 0 (maximum), S = (1/2, 0) with P = -k (saddle), typed iff s < -|B|/2.

Superlevel elder rule: descending the level, components are born at local maxima and merge at
saddles; at a merge the younger component (lower birth level) dies. A component containing a point
of arbitrarily large P (an unbounded component of the cubic) or a local maximum with value > 0 is
OLDER than M. d_P(M) = level of the saddle at which M's component first merges with an older one.
(M,S) is the elder pair iff that saddle is S.

Merge structure is computed from the Morse data: all critical points (resultant + Newton polish), the two
ascending gradient branches of every saddle (ODE, normalized gradient, escape radius R_far = 60), and
union-find in decreasing saddle order.  Exploration only: numpy/scipy/sympy, floating point, not run in CI,
not a proof.  Known limits: the escape radius is adequate for the sampled |s| >= 0.15 (the bounded part of
{P > -k} near the zero directions of the cubic form has radius ~ sqrt(2k/(|s| sin^2 phi)) << 60); the
pre-Newton root filter could drop roots for very large coefficients; results are recorded per sample.
"""
import sys, math, random, json
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

X, Z = sp.symbols('X Z', real=True)


def cubic_coeffs(k, s, a, beta, c):
    k, s, a, beta, c = [sp.Rational(str(round(float(t), 12))) for t in (k, s, a, beta, c)]
    P = 2*k*X**3 - sp.Rational(3, 2)*k*X - k/sp.Integer(2) + sp.Rational(1, 2)*s*Z**2 \
        + sp.Rational(1, 2)*a*(X**2 - sp.Rational(1, 4))*Z + sp.Rational(1, 2)*beta*X*Z**2 + c*Z**3/6
    return sp.Poly(P, X, Z)


def critical_points(k, s, a, beta, c):
    """All real critical points of P via the resultant in Z."""
    P = cubic_coeffs(k, s, a, beta, c).as_expr()
    PX = sp.diff(P, X); PZ = sp.diff(P, Z)
    res = sp.Poly(sp.resultant(PX, PZ, Z), X)
    xs = [complex(r) for r in np.roots([float(cf) for cf in res.all_coeffs()])]
    pts = []
    f_PX = sp.lambdify((X, Z), PX, 'numpy'); f_PZ = sp.lambdify((X, Z), PZ, 'numpy')
    for xr in xs:
        if abs(xr.imag) > 1e-7:
            continue
        x0 = xr.real
        # PX = 0 is quadratic in Z at fixed X
        qa = beta/2.0; qb = a*x0; qc = 6*k*x0**2 - 1.5*k
        if abs(qa) > 1e-12:
            disc = qb*qb - 4*qa*qc
            if disc < -1e-9:
                continue
            disc = max(disc, 0.0)
            zs = [(-qb + math.sqrt(disc))/(2*qa), (-qb - math.sqrt(disc))/(2*qa)]
        elif abs(qb) > 1e-12:
            zs = [-qc/qb]
        else:
            if abs(qc) > 1e-9:
                continue
            # a = beta = 0 and X = +-1/2: PZ = s Z + (c/2) Z^2 = 0
            zs = [0.0] + ([-2*s/c] if abs(c) > 1e-12 else [])
        for z0 in zs:
            if abs(f_PX(x0, z0)) < 1e-6 and abs(f_PZ(x0, z0)) < 1e-6:
                # polish with Newton
                v = np.array([x0, z0], dtype=float)
                H = sp.hessian(P, (X, Z)); f_H = sp.lambdify((X, Z), H, 'numpy')
                for _ in range(8):
                    g = np.array([f_PX(*v), f_PZ(*v)], dtype=float)
                    Hm = np.array(f_H(*v), dtype=float)
                    try:
                        v = v - np.linalg.solve(Hm, g)
                    except np.linalg.LinAlgError:
                        break
                if not any(np.hypot(*(v - q['pos'])) < 1e-6 for q in pts):
                    Hm = np.array(f_H(*v), dtype=float)
                    ev, evec = np.linalg.eigh(Hm)
                    kind = 'max' if ev[1] < 0 else ('min' if ev[0] > 0 else 'saddle')
                    val = float(sp.lambdify((X, Z), P, 'numpy')(*v))
                    pts.append({'pos': v, 'val': val, 'kind': kind, 'ev': ev, 'evec': evec})
    return pts, P


def ascend(P, start, direction, maxima, R_far=60.0):
    """Follow the normalized ascending gradient flow from start + eps*direction."""
    PX = sp.lambdify((X, Z), sp.diff(P, X), 'numpy'); PZ = sp.lambdify((X, Z), sp.diff(P, Z), 'numpy')
    def rhs(t, y):
        g = np.array([PX(y[0], y[1]), PZ(y[0], y[1])], dtype=float)
        n = np.hypot(*g)
        return g/(n + 1e-12)
    y0 = np.array(start, dtype=float) + 1e-3*np.array(direction, dtype=float)
    def far(t, y): return R_far - np.hypot(*y)
    far.terminal = True
    def near_max(t, y):
        return min(np.hypot(*(y - m['pos'])) for m in maxima) - 1e-4 if maxima else 1.0
    near_max.terminal = True
    sol = solve_ivp(rhs, (0, 400.0), y0, events=[far, near_max], max_step=0.02, rtol=1e-8, atol=1e-10)
    yend = sol.y[:, -1]
    if np.hypot(*yend) >= R_far - 1e-6:
        return ('inf', None)
    for i, m in enumerate(maxima):
        if np.hypot(*(yend - m['pos'])) < 5e-3:
            return ('max', i)
    # stalled (near a saddle or slow convergence): decide by gradient ascent continuation
    return ('unknown', None)


def elder_partner(k, s, a, beta, c):
    pts, P = critical_points(k, s, a, beta, c)
    maxima = [p for p in pts if p['kind'] == 'max']
    saddles = [p for p in pts if p['kind'] == 'saddle']
    # identify M and S
    iM = min(range(len(maxima)), key=lambda i: np.hypot(*(maxima[i]['pos'] - np.array([-0.5, 0.0]))))
    assert np.hypot(*(maxima[iM]['pos'] - np.array([-0.5, 0.0]))) < 1e-5, 'M not found'
    iS = min(range(len(saddles)), key=lambda i: np.hypot(*(saddles[i]['pos'] - np.array([0.5, 0.0]))))
    assert np.hypot(*(saddles[iS]['pos'] - np.array([0.5, 0.0]))) < 1e-5, 'S not found'
    # ascending branches of every saddle
    branches = []
    for sd in saddles:
        e = sd['evec'][:, 1]  # eigenvector of the positive eigenvalue (ascent direction)
        b1 = ascend(P, sd['pos'], e, maxima); b2 = ascend(P, sd['pos'], -e, maxima)
        branches.append((b1, b2))
    # union-find over maxima and the node 'inf'
    parent = {('max', i): ('max', i) for i in range(len(maxima))}; parent[('inf', None)] = ('inf', None)
    age = {('max', i): maxima[i]['val'] for i in range(len(maxima))}; age[('inf', None)] = math.inf
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    order = sorted(range(len(saddles)), key=lambda i: -saddles[i]['val'])
    M = ('max', iM); death = None; self_attach = 0
    for i in order:
        b1, b2 = branches[i]
        if b1[0] == 'unknown' or b2[0] == 'unknown':
            return {'status': 'unresolved', 'saddle': i, 'n_window': None}
        r1, r2 = find(b1), find(b2)
        rM = find(M)
        if r1 == r2:
            self_attach += 1  # both branches in one component (a loop); no death
            continue
        a1, a2 = age[r1], age[r2]
        # merge: the older root survives
        keep, drop = (r1, r2) if a1 >= a2 else (r2, r1)
        if drop == rM and age[keep] > age[rM]:
            death = (i, saddles[i]['val']); break
        if drop == rM:
            # M's component would be dropped only if older exists; equal ages impossible generically
            pass
        parent[drop] = keep
    window = [sd for j, sd in enumerate(saddles) if j != iS and -k < sd['val'] < 0]
    return {'status': 'ok', 'self_attachments': self_attach, 'death_saddle': None if death is None else death[0], 'death_val': None if death is None else death[1],
            'is_S': death is not None and death[0] == iS, 'n_window': len(window),
            'window_vals': sorted([sd['val'] for sd in window], reverse=True),
            'n_saddles': len(saddles), 'n_maxima': len(maxima), 'n_minima': len([p for p in pts if p['kind']=='min'])}


def cub_n(k, s, a, beta, c):
    """[CUB] Theorem C classifier (None if not typed)."""
    B = beta - a*a/(12*k); D = (c - a*beta/(4*k) + a**3/(72*k*k))/2
    if not (s < -abs(B)/2):
        return None
    T = -(s - B)**2*(B + 2*s)/(12*k)
    if s > B:
        return 2 if D*D < T else 1
    return 1 if D*D > T else 0


def sample_theta_n0(rng, k=1.0):
    """Sample typed jets with n = 0 by rejection on a box."""
    while True:
        s = -rng.uniform(0.2, 4); a = rng.uniform(-3, 3); beta = rng.uniform(-4, 4); c = rng.uniform(-4, 4)
        if cub_n(k, s, a, beta, c) == 0:
            return dict(s=s, a=a, beta=beta, c=c)


def sample_theta(rng, k=1.0):
    """Sample (u,v) in D_shape, Z != 0, a; return (s,a,beta,c) with an extra window root at (u - aZ/(12k), Z)."""
    while True:
        u = rng.uniform(-1.5, 0.5); b0 = 3 - 12*u*u
        lo, hi = abs(b0)/2, 3 - 6*u
        if lo < hi:
            break
    v = rng.uniform(lo, hi)
    Zr = rng.choice([-1, 1])*math.exp(rng.uniform(math.log(0.15), math.log(3.0)))
    a = rng.uniform(-3, 3)
    s = -k*v/Zr**2; B = k*b0/Zr**2; D = k*(v - b0*u)/Zr**3
    beta = B + a*a/(12*k); c = 2*D + a*B/(4*k) + a**3/(144*k*k)
    return dict(u=u, v=v, Z=Zr, a=a, s=s, beta=beta, c=c, B=B, D=D)


if __name__ == '__main__':
    # usage: elder_cubic.py SEED N [n0]   (third argument "n0" samples typed jets with no extra window root)
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 40
    mode_n0 = len(sys.argv) > 3 and sys.argv[3] == 'n0'
    k = 1.0
    out = []
    for i in range(N):
        th = sample_theta_n0(rng, k) if mode_n0 else sample_theta(rng, k)
        try:
            r = elder_partner(k, th['s'], th['a'], th['beta'], th['c'])
        except AssertionError as e:
            r = {'status': 'error', 'msg': str(e)}
        rec = {**{kk: float(vv) for kk, vv in th.items()}, **{kk: (vv if not isinstance(vv, np.generic) else float(vv)) for kk, vv in r.items()}}
        out.append(rec)
        print(json.dumps(rec, default=float))
    json.dump(out, open('elder_samples_%s%s.json' % (sys.argv[1] if len(sys.argv) > 1 else '0', '_n0' if mode_n0 else ''), 'w'), default=float)
