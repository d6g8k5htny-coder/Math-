#!/usr/bin/env python3
"""Grid maximin (the elder rule, discretised) on sampled pinned cubics.  Standard library only.

EXPLORATION, NOT PROOF, NOT RUN IN CI.  Scientific effect: NONE.

What it does.  For sampled typed jets theta = (s, B, D) of the sheared pinned cubic (LOCAL_PAIRING.md (2.1))

    P(u, Z) = 2k(u-1)(u+1/2)^2 + (Z^2/2)(s + B u) + (D/3) Z^3,      M = (-1/2, 0), S = (1/2, 0),

it (i) computes every critical point in closed form ([CUB] (C7), (C13): the extra roots lie on the line
s + Bu + DZ = 0 and their u-coordinates solve (12kD^2 + B^3)u^2 + 2B^2 s u + Bs^2 - 3kD^2 = 0; for D = 0 they
sit at u0 = -s/B with Z^2 = (3k - 12k u0^2)/B), counts the strict-window ones (n) and cross-checks n with the
[CUB] classifier; (ii) computes the ordinary superlevel maximin death level of M on a square grid by the
literal elder rule: cells are processed in decreasing order of P and merged with 8-neighbours by union-find;
the death level is the value at which M's component first joins a component containing a point older than
M (P > 0), and the merge cell is recorded; (iii) compares the grid death level with h_* = max window critical
value (or -k when n = 0) and the merge cell with the position of the highest extra window saddle (or S).

Boundary.  The grid covers the box |u|, |Z| <= R with R chosen from the window critical points (R <= 6).  A boundary cell
with P > -k is marked "older" only when the quadratic derivative of t -> P(tu,tZ) is strictly positive
throughout [1,3] and P(3u,3Z) > 0. Endpoints and any interior quadratic minimum are checked with exact
rational arithmetic on the binary64 input values. Such a cell has an outward path, above its value
after departure, to a positive point. Other boundary cells are ordinary cells.

Limits.  Grid error near a nondegenerate saddle is of order h^2 (h the spacing) plus one cell of
8-connectivity; ties of the two extra saddle heights closer than the tolerance are reported as ties.  Close to
the typed boundary s = -|B|/2 the saddle at S is nearly degenerate in Z (P ~ -k + (Z^2/2)(s + B/2) there), so
the merge cell can sit some distance along that flat valley while the death level is still exact; the level
comparison is the primary check, the merge-cell comparison the secondary one.  Runtime about two minutes
for the default sample sizes (pure Python union-find on up to 361k cells per jet).
Nothing here certifies the Gaussian steps of LOCAL_PAIRING.md.

Usage:  python3 elder_grid.py [SEED] [N_SAMPLES] [N0_SAMPLES] [SPACING]
Output: RESULTS_EXPLORATION.json next to this file.
"""
import json
import math
import os
import random
import sys
from fractions import Fraction


def A(k, u):
    return 2*k*(u - 1)*(u + 0.5)**2


def P(k, s, B, D, u, Z):
    return A(k, u) + (Z*Z/2)*(s + B*u) + (D/3)*Z**3


def grad(k, s, B, D, u, Z):
    return (6*k*u*u - 1.5*k + (B/2)*Z*Z, Z*(s + B*u + D*Z))


def classifier_n(k, s, B, D):
    """[CUB] Theorem C in the sheared parameters (typed domain s < -|B|/2), else None."""
    if not (s < -abs(B)/2):
        return None
    T = -(s - B)**2*(B + 2*s)/(12*k)
    if s > B:
        return 2 if D*D < T else 1
    return 1 if D*D > T else 0


def quadratic_roots(a2, a1, a0):
    if abs(a2) < 1e-14:
        return [-a0/a1] if abs(a1) > 1e-14 else []
    disc = a1*a1 - 4*a2*a0
    if disc < 0:
        return []
    q = math.sqrt(disc)
    return [(-a1 + q)/(2*a2), (-a1 - q)/(2*a2)]


def critical_points(k, s, B, D):
    """All critical points of P: the pins and the extra roots (closed form)."""
    extra = []
    if abs(D) > 1e-12:
        for u in quadratic_roots(12*k*D*D + B**3, 2*B*B*s, B*s*s - 3*k*D*D):
            Z = -(s + B*u)/D
            if abs(Z) > 1e-9:
                extra.append((u, Z))
    elif abs(B) > 1e-12:
        u = -s/B
        Z2 = (3*k - 12*k*u*u)/B
        if Z2 > 0:
            extra += [(u, math.sqrt(Z2)), (u, -math.sqrt(Z2))]
    out = []
    for (u, Z) in extra:
        gu, gz = grad(k, s, B, D, u, Z)
        if abs(gu) < 1e-7*max(1.0, k) and abs(gz) < 1e-7*max(1.0, k):
            out.append((u, Z, P(k, s, B, D, u, Z)))
    return out


def window_roots(k, cps):
    return [(u, Z, val) for (u, Z, val) in cps if -k < val < 0]


def outward_ray_older(k, s, B, D, u, Z):
    """Conservative full-segment ray test for the supplied (rounded) jet."""
    k, s, B, D, u, Z = map(Fraction, (k, s, B, D, u, Z))
    # P(tu,tZ) = a*t^3 + b*t^2 + c*t - k/2.
    a = 2*k*u**3 + B*u*Z**2/2 + D*Z**3/3
    b, c = s*Z**2/2, -3*k*u/2
    derivative = lambda t: 3*a*t*t + 2*b*t + c
    values = [derivative(1), derivative(3)]
    if a > 0:
        vertex = -b/(3*a)
        if 1 < vertex < 3:
            values.append(derivative(vertex))
    return min(values) > 0 and 27*a + 9*b + 3*c - k/2 > 0


def grid_death(k, s, B, D, cps, spacing):
    """Discrete elder rule on the box |u|,|Z| <= R.  Returns (death, merge_u, merge_Z, R, ncells)."""
    reach = 1.0
    for (u, Z, val) in cps:
        if -k <= val <= 0:               # only the window geometry sets the box; Lemma 2.1(b) handles the outside
            reach = max(reach, abs(u), abs(Z))
    R = min(6, int(math.ceil(1.6*reach + 1.0)))
    nper = int(round(1.0/spacing))
    N = 2*R*nper + 1                     # nodes per axis; M and S are exact nodes since 1/2 is a multiple of h
    h = 2.0*R/(N - 1)
    W = N + 2                            # padded width: a never-processed border removes all bounds checks

    def coord(i):
        return -R + i*h

    total = W*W
    vals = [0.0]*total
    older = bytearray(total)
    for i in range(N):
        u = coord(i)
        base = (i + 1)*W + 1
        boundary_i = (i == 0 or i == N - 1)
        for j in range(N):
            Z = coord(j)
            v = P(k, s, B, D, u, Z)
            idx = base + j
            vals[idx] = v
            if v > 0:
                older[idx] = 1
            elif v > -k and (boundary_i or j == 0 or j == N - 1):
                if outward_ray_older(k, s, B, D, u, Z):
                    older[idx] = 1
    iM = int(round((-0.5 + R)/h)); jM = int(round(R/h))
    idxM = (iM + 1)*W + (jM + 1)
    vals[idxM] = 0.0                     # exact pin value
    older[idxM] = 0

    parent = list(range(total))
    comp_older = bytearray(older)
    processed = bytearray(total)
    interior = [(i + 1)*W + (j + 1) for i in range(N) for j in range(N)]
    order = sorted(interior, key=vals.__getitem__, reverse=True)
    offsets = (-W - 1, -W, -W + 1, -1, 1, W - 1, W, W + 1)
    m_seen = False
    for idx in order:
        processed[idx] = 1
        ra = idx
        while parent[ra] != ra:
            parent[ra] = parent[parent[ra]]
            ra = parent[ra]
        for d in offsets:
            nb = idx + d
            if not processed[nb]:
                continue
            rb = nb
            while parent[rb] != rb:
                parent[rb] = parent[parent[rb]]
                rb = parent[rb]
            if ra != rb:
                parent[rb] = ra
                if comp_older[rb]:
                    comp_older[ra] = 1
        if idx == idxM:
            m_seen = True
        if m_seen:
            rM = idxM
            while parent[rM] != rM:
                parent[rM] = parent[parent[rM]]
                rM = parent[rM]
            if comp_older[rM]:
                i, j = divmod(idx, W)
                return vals[idx], coord(i - 1), coord(j - 1), R, N*N
    return None, None, None, R, N*N


def sample_n1(rng, k):
    """Chart sampler: a typed jet with a prescribed extra strict-window root (u1, Z1)."""
    while True:
        u1 = rng.uniform(-1.45, 0.45)
        b0 = 3 - 12*u1*u1
        lo, hi = abs(b0)/2, 3 - 6*u1
        if lo < hi:
            break
    v = lo + rng.uniform(0.05, 0.95)*(hi - lo)
    Z1 = rng.choice((-1.0, 1.0))*math.exp(rng.uniform(math.log(0.3), math.log(1.8)))
    s = -k*v/Z1**2
    B = k*b0/Z1**2
    D = k*(v - b0*u1)/Z1**3
    return s, B, D


def sample_n0(rng, k):
    while True:
        B = rng.uniform(-3, 3)
        s = -abs(B)/2 - rng.uniform(0.02, 3)
        D = rng.uniform(-3, 3)
        if classifier_n(k, s, B, D) == 0:
            return s, B, D


def run_one(k, s, B, D, spacing, tol):
    cps = critical_points(k, s, B, D)
    win = window_roots(k, cps)
    n = len(win)
    n_cls = classifier_n(k, s, B, D)
    if win:
        top = max(win, key=lambda t: t[2])
        h_star = top[2]
        target = (top[0], top[1])
        heights = sorted([t[2] for t in win], reverse=True)
        tie = len(heights) >= 2 and heights[0] - heights[1] < tol
    else:
        h_star = -k
        target = (0.5, 0.0)
        tie = False
    death, mu, mz, R, ncells = grid_death(k, s, B, D, cps, spacing)
    row = {'s': s, 'B': B, 'D': D, 'n': n, 'n_classifier': n_cls, 'h_star': h_star,
           'death': death, 'R': R, 'cells': ncells, 'tie_within_tol': tie}
    if death is None:
        row['status'] = 'no_death_found'
        return row
    row['merge_cell'] = [mu, mz]
    row['target'] = list(target)
    row['level_error'] = abs(death - h_star)
    row['merge_distance'] = math.hypot(mu - target[0], mz - target[1])
    row['level_match'] = row['level_error'] <= tol
    row['merge_match'] = row['merge_distance'] <= 3*spacing or tie
    row['status'] = 'ok'
    return row


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    n1 = int(sys.argv[2]) if len(sys.argv) > 2 else 40
    n0 = int(sys.argv[3]) if len(sys.argv) > 3 else 15
    spacing = float(sys.argv[4]) if len(sys.argv) > 4 else 0.02
    rng = random.Random(seed)
    rows = []
    for k in (1.0, 0.5):
        tol = 0.01*max(1.0, k)
        for _ in range(n1):
            s, B, D = sample_n1(rng, k)
            rows.append(dict(k=k, kind='chart_n>=1', **run_one(k, s, B, D, spacing, tol)))
            sys.stderr.write('.'); sys.stderr.flush()
        for _ in range(n0):
            s, B, D = sample_n0(rng, k)
            rows.append(dict(k=k, kind='typed_n=0', **run_one(k, s, B, D, spacing, tol)))
            sys.stderr.write('o'); sys.stderr.flush()
    # the [ELDER] witness (s, B, D) = (-3k/2, -2k, 0), k = 1: both extra saddles at -7/32 (a tie by construction)
    rows.append(dict(k=1.0, kind='elder_witness', **run_one(1.0, -1.5, -2.0, 0.0, spacing, 0.01)))
    summary = {}
    for kind in ('chart_n>=1', 'typed_n=0', 'elder_witness'):
        sub = [r for r in rows if r['kind'] == kind]
        summary[kind] = {
            'samples': len(sub),
            'classifier_agrees_with_closed_form_count': sum(1 for r in sub if r['n'] == r['n_classifier']),
            'death_found': sum(1 for r in sub if r['status'] == 'ok'),
            'level_match': sum(1 for r in sub if r.get('level_match')),
            'merge_match': sum(1 for r in sub if r.get('merge_match')),
            'ties_within_tol': sum(1 for r in sub if r['tie_within_tol']),
            'by_n': {str(m): sum(1 for r in sub if r['n'] == m) for m in (0, 1, 2)},
            'max_level_error': max([r.get('level_error', 0.0) for r in sub] or [0.0]),
        }
    out = {'object': 'CL-LOCAL-PAIRING-20260930-v1', 'kind': 'exploration (stdlib grid maximin); not proof; not CI',
           'scientific_effect': 'NONE', 'seed': seed, 'spacing': spacing, 'n1_per_k': n1, 'n0_per_k': n0,
           'k_values': [1.0, 0.5], 'summary': summary, 'rows': rows}
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'RESULTS_EXPLORATION.json')
    with open(path, 'w') as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
        fh.write('\n')
    print(json.dumps(summary, indent=1, sort_keys=True))


if __name__ == '__main__':
    main()
