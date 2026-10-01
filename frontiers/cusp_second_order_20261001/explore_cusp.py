#!/usr/bin/env python3
"""EXPLORATION for PROOF.md (CL-CUSP-SECOND-ORDER-20261001-v1.1).  Standard library only, floating point.
NOT a control, NOT evidence of acceptance, NOT replayed by the workflow (it takes about a minute).

  X1  the actual global elder decision of random pinned plane quintics at the cusp scale (r = 0.01, k = kappa r),
      computed by a union-find maximin on a graded grid of the rescaled window, against the model window
      |phi| < 1/3 (phi = Y/(6 kappa Delta)); random phi, and phi targeted at +-(0.30, 0.32, 0.345, 0.36);
  X2  the second-order coefficient c_1 for the Gaussian kernel exp(-|z|^2/2) (L = infinity), with the leading
      constants c_2, c_3 for the ratio c_1/c: d = 2 by composite Gauss-Legendre quadrature, d = 3 by a
      deterministic quadrature over the negative-definite cone; each at two resolutions (the difference is the
      convergence evidence), and d = 3 also by an independent fixed-seed Monte Carlo over the same law; with the
      candidate coefficient I_cand = (3^(1/4)/2) c_1 and the rejected coefficient I_cand - c_1 of Theorem CU'.
Output: EXPLORE.json (numbers rounded; seeds fixed).
"""
import json
import math
import random
import sys

# ------------------------------------------------------------------------------------------------- X1

MONO = [(i, j) for i in range(6) for j in range(6) if i + j <= 5]
PINNED = [(0, 0), (1, 0), (2, 0), (3, 0), (0, 1), (1, 1)]


def solve4(A, b):
    n = 4
    M = [A[i][:] + [b[i]] for i in range(n)]
    for i in range(n):
        p = max(range(i, n), key=lambda r: abs(M[r][i]))
        M[i], M[p] = M[p], M[i]
        for r in range(n):
            if r != i:
                f = M[r][i] / M[i][i]
                M[r] = [x - f * y for x, y in zip(M[r], M[i])]
    return [M[i][n] / M[i][i] for i in range(n)]


def build(r, kap, free):
    c = dict(free)
    c[(0, 1)] = -c[(2, 1)] * r ** 2 / 4 - c[(4, 1)] * r ** 4 / 16
    c[(1, 1)] = -c[(3, 1)] * r ** 2 / 4
    A, rhs = [], []
    for x0, val in ((-r / 2, 0.0), (r / 2, -kap * r ** 4)):
        A.append([1, x0, x0 ** 2, x0 ** 3])
        rhs.append(val - c[(4, 0)] * x0 ** 4 - c[(5, 0)] * x0 ** 5)
    for x0 in (-r / 2, r / 2):
        A.append([0, 1, 2 * x0, 3 * x0 ** 2])
        rhs.append(-4 * c[(4, 0)] * x0 ** 3 - 5 * c[(5, 0)] * x0 ** 4)
    c[(0, 0)], c[(1, 0)], c[(2, 0)], c[(3, 0)] = solve4(A, rhs)
    return c


def feval(c, x, y):
    return sum(v * x ** i * y ** j for (i, j), v in c.items())


def hess(c, x, y):
    fxx = sum(v * i * (i - 1) * x ** (i - 2) * y ** j for (i, j), v in c.items() if i >= 2)
    fyy = sum(v * j * (j - 1) * x ** i * y ** (j - 2) for (i, j), v in c.items() if j >= 2)
    fxy = sum(v * i * j * x ** (i - 1) * y ** (j - 1) for (i, j), v in c.items() if i >= 1 and j >= 1)
    return fxx, fxy, fyy


def death_level(F, ny, nx, iM):
    n = ny * nx
    order = sorted(range(n), key=lambda p: -F[p])
    parent = [-1] * n
    top = [0.0] * n

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    for p in order:
        parent[p] = p
        top[p] = F[p]
        py, px = divmod(p, nx)
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dy == 0 and dx == 0:
                    continue
                qy, qx = py + dy, px + dx
                if 0 <= qy < ny and 0 <= qx < nx:
                    q = qy * nx + qx
                    if parent[q] >= 0:
                        a, b = find(p), find(q)
                        if a != b:
                            if top[a] < top[b]:
                                a, b = b, a
                            if parent[iM] >= 0 and find(iM) == b:
                                return F[p]
                            parent[b] = a
    return -math.inf


def trial(rng, r, kap, phi_target=None, nX=241, nZ=121, X0=-3.5, X1=2.5):
    free = {m: rng.gauss(0, 1) for m in MONO if m not in PINNED}
    free[(0, 2)] = -abs(free[(0, 2)]) - 0.3
    if phi_target is not None:
        a_, g_ = 2 * free[(0, 2)], 2 * free[(2, 1)]
        free[(4, 0)] = (6 * kap * phi_target + g_ ** 2 / (4 * a_)) / 2
    c = build(r, kap, free)
    fxxM, fxyM, fyyM = hess(c, -r / 2, 0.0)
    fxxS, fxyS, fyyS = hess(c, r / 2, 0.0)
    typed = (fyyM < 0 and fxxM * fyyM - fxyM ** 2 > 0) and (fxxS * fyyS - fxyS ** 2 < 0)
    a, f4, g = 2 * c[(0, 2)], 24 * c[(4, 0)], 2 * c[(2, 1)]
    phi = (f4 / 12 - g ** 2 / (4 * a)) / (6 * kap)
    if not typed:
        return {'typed': False, 'phi': phi}
    Xs = [X0 + (X1 - X0) * i / (nX - 1) for i in range(nX)]
    c02, c21 = c[(0, 2)], c[(2, 1)]
    RZ = 3.0 * math.sqrt(max(1.0, abs(c[(4, 0)]) * 81 + 2 * kap * 27) / abs(c02))
    h0 = 0.01 * math.sqrt((1.0 + kap) / abs(c02))
    du = 2.0 / (nZ - 1)
    lo, hi = 1e-6, 50.0
    for _ in range(100):
        al = 0.5 * (lo + hi)
        if RZ * al / math.sinh(al) * du > h0:
            lo = al
        else:
            hi = al
    Zs = [RZ * math.sinh(al * (-1 + du * k)) / math.sinh(al) for k in range(nZ)]
    F = []
    for Z in Zs:
        for X in Xs:
            Ys = -c21 * X * X / (2 * c02)
            F.append(feval(c, r * X, r * r * (Ys + Z)) / r ** 4)
    ZM = c21 * 0.25 / (2 * c02)
    iy = min(range(nZ), key=lambda k: abs(Zs[k] - ZM))
    ix = min(range(nX), key=lambda k: abs(Xs[k] + 0.5))
    while True:
        best = (F[iy * nX + ix], iy, ix)
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                qy, qx = iy + dy, ix + dx
                if 0 <= qy < nZ and 0 <= qx < nX and F[qy * nX + qx] > best[0]:
                    best = (F[qy * nX + qx], qy, qx)
        if best[1] == iy and best[2] == ix:
            break
        iy, ix = best[1], best[2]
    dl = death_level(F, nZ, nX, iy * nX + ix)
    elder = math.isfinite(dl) and abs(dl + kap) < 0.02 * kap + 5e-3
    return {'typed': True, 'phi': phi, 'kappa': kap, 'death': dl, 'elder': elder, 'model': abs(phi) < 1 / 3}


def run_X1():
    rng = random.Random(20261001)
    r = 0.01
    rand = []
    for _ in range(40):
        kap = math.exp(rng.uniform(math.log(0.1), math.log(5.0)))
        rand.append(trial(rng, r, kap))
    T = [x for x in rand if x['typed']]
    agree = sum(1 for x in T if x['elder'] == x['model'])
    tgt = []
    for phi in (0.30, 0.32, 0.345, 0.36, -0.30, -0.32, -0.345, -0.36):
        for _ in range(2):
            kap = math.exp(rng.uniform(math.log(0.3), math.log(3.0)))
            res = trial(rng, 0.003, kap, phi_target=phi)
            tgt.append({'phi_target': phi, 'kappa': round(kap, 3), 'typed': res['typed'], 'elder': res.get('elder')})
    return {'r': r, 'random_trials': len(rand), 'typed': len(T), 'agree_with_window_1_3': agree,
            'disagreements': [[round(x['phi'], 4), round(x['kappa'], 3)] for x in T if x['elder'] != x['model']],
            'targeted_r_0.003': tgt}


# ------------------------------------------------------------------------------------------------- X2

def hyp1f1_neg(a, b, x):
    """1F1(a; b; -x) for x >= 0 via Kummer's transformation e^{-x} 1F1(b-a; b; x) (positive series), with the
    large-x asymptotic expansion."""
    if x > 60.0:
        # 1F1(a;b;-x) ~ Gamma(b)/Gamma(b-a) x^{-a} sum_n (a)_n (a-b+1)_n / n! x^{-n}
        s, term = 1.0, 1.0
        for n in range(12):
            term *= (a + n) * (a - b + 1 + n) / ((n + 1) * x)
            s += term
        return math.gamma(b) / math.gamma(b - a) * x ** (-a) * s
    s, term, n = 1.0, 1.0, 0
    while True:
        term *= (b - a + n) / ((b + n) * (n + 1)) * x
        s += term
        n += 1
        if term < 1e-17 * s and n > x:
            break
    return math.exp(-x) * s


P = 7 / 4
GP = math.gamma((P + 1) / 2) / math.sqrt(math.pi) * 2 ** (P / 2)


def eabs_normal(m, v):
    """E|X|^{7/4}, X ~ N(m, v)."""
    return v ** (P / 2) * GP * hyp1f1_neg(-P / 2, 0.5, m * m / (2 * v))


def gauss_legendre(n):
    xs, ws = [], []
    for i in range(1, n + 1):
        x = math.cos(math.pi * (i - 0.25) / (n + 0.5))
        for _ in range(100):
            p0, p1 = 1.0, x
            for k in range(2, n + 1):
                p0, p1 = p1, ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
            dp = n * (x * p1 - p0) / (x * x - 1)
            dx = p1 / dp
            x -= dx
            if abs(dx) < 1e-16:
                break
        xs.append(x)
        ws.append(2 / ((1 - x * x) * dp * dp))
    return xs, ws


def composite(a, b, panels, xs, ws):
    out = []
    h = (b - a) / panels
    for k in range(panels):
        lo = a + k * h
        for x, w in zip(xs, ws):
            out.append((lo + (x + 1) * h / 2, w * h / 2))
    return out


def laguerre(n):
    """Gauss-Laguerre nodes and weights (weight e^{-s} on [0, oo)), Newton iteration on L_n."""
    xs, ws = [], []
    for i in range(1, n + 1):
        if i == 1:
            x = 3.0 / (1 + 2.4 * n)
        elif i == 2:
            x = xs[0] + 15.0 / (1 + 2.5 * n)
        else:
            x = xs[-1] + (1 + 2.55 * (i - 2)) / (1.9 * (i - 2)) * (xs[-1] - xs[-2])
        for _ in range(200):
            p0, p1 = 1.0, 1.0 - x
            for k in range(2, n + 1):
                p0, p1 = p1, ((2 * k - 1 - x) * p1 - (k - 1) * p0) / k
            dp = n * (p1 - p0) / x
            dx = p1 / dp
            x -= dx
            if abs(dx) < 1e-15 * max(1.0, x):
                break
        p0, p1 = 1.0, 1.0 - x
        for k in range(2, n + 2):
            p0, p1 = p1, ((2 * k - 1 - x) * p1 - (k - 1) * p0) / k
        xs.append(x)
        ws.append(x / ((n + 1) ** 2 * p1 * p1))
    return xs, ws


def ey_d2(pw, pg):
    """d = 2: (a, f4) ~ N(0, [[8/3, 2], [2, 30]]) given (f_xx, f_xy) = 0; gamma ~ N(0, 2); Y = (f4/12) a - gamma^2/4.
    J = E[|Y|^{7/4} |a|^{1/4} 1{a < 0}] by composite Gauss-Legendre in a = -w^4 (pw panels) and gamma (pg panels)."""
    Sa, Saf, Sf, Sg = 8 / 3, 2.0, 30.0, 2.0
    mu, s2 = Saf / Sa, Sf - Saf ** 2 / Sa
    gx, gw = gauss_legendre(12)
    wn = composite(0.0, (2 * Sa * 60) ** 0.125, pw, gx, gw)
    gn = composite(-14.0, 14.0, pg, gx, gw)
    EY = 0.0
    for w, ww in wn:
        a = -w ** 4
        jac = 4 * w ** 3
        pa = math.exp(-a * a / (2 * Sa)) / math.sqrt(2 * math.pi * Sa)
        v = (a / 12) ** 2 * s2
        inner = 0.0
        for g, gwt in gn:
            m = mu * a * a / 12 - g * g / 4
            inner += gwt * eabs_normal(m, v) * math.exp(-g * g / (2 * Sg)) / math.sqrt(2 * math.pi * Sg)
        EY += ww * jac * abs(a) ** 0.25 * pa * inner
    return EY


def ey_d3(npan, nth, nlag):
    """d = 3: the transverse block A given (f_xx, f_xy, f_xz) = 0 has eigenvalues t +- rho, t ~ N(0, 5/3) and
    rho ~ Rayleigh(1) independent (checker C7: Var f_yy = Var f_zz = 8/3, Cov = 2/3, Var f_yz = 1); A < 0 iff
    t < -rho.  gamma ~ N(0, 2 I) is isotropic, so in the eigenbasis -gamma^T adj(A) gamma / 4 = s (|l2| cos^2 th +
    |l1| sin^2 th) with s ~ Exp(1), th ~ U[0, pi/2]; f4 | A ~ N((3/5) tr A, 138/5) is integrated in closed form.
    J by composite Gauss-Legendre in rho in [0, 8] and u in [0, 14^(1/4)] (t = -rho - u^4: the cone, with the
    Delta^{1/4} endpoint singularity removed), trapezoid in th (spectral: a smooth function of cos 2th) and
    Gauss-Laguerre in s."""
    gx, gw = gauss_legendre(8)
    rn = composite(0.0, 8.0, npan, gx, gw)
    un = composite(0.0, 14.0 ** 0.25, npan, gx, gw)
    lx, lw = laguerre(nlag)
    cs2 = [math.cos(k * (math.pi / 2) / nth) ** 2 for k in range(nth + 1)]
    thw = [(0.5 if k in (0, nth) else 1.0) / nth for k in range(nth + 1)]
    st2 = 5.0 / 3.0
    EY = 0.0
    for rho, rw in rn:
        prho = rho * math.exp(-rho * rho / 2)
        for u, uw in un:
            w = u ** 4
            t = -rho - w
            pt = math.exp(-t * t / (2 * st2)) / math.sqrt(2 * math.pi * st2)
            a1, a2 = w, w + 2 * rho
            Delta = a1 * a2
            m0 = 0.1 * t * Delta
            v = (Delta / 12.0) ** 2 * 27.6
            inner = 0.0
            for c2, tw in zip(cs2, thw):
                lam = a2 * c2 + a1 * (1 - c2)
                inner += tw * sum(sw * eabs_normal(m0 + s * lam, v) for s, sw in zip(lx, lw))
            EY += rw * uw * 4 * u ** 3 * prho * pt * Delta ** 0.25 * inner
    return EY


def mc_d3(N, seed=1001, batches=10):
    """Independent Monte Carlo cross-check of ey_d3 (same law): rho ~ Rayleigh(1), t from the normal truncated to
    the cone t < -rho, weight P(t < -rho | rho); returns (mean, batch standard error)."""
    from statistics import NormalDist
    nd = NormalDist()
    rng = random.Random(seed)
    sig_t = math.sqrt(5 / 3)
    batch = N // batches
    acc, means = 0.0, []
    for i in range(batch * batches):
        rho = math.sqrt(-2.0 * math.log(1.0 - rng.random()))
        w = nd.cdf(-rho / sig_t)
        z = nd.inv_cdf(min(max(rng.random() * w, 1e-300), 1 - 1e-16))
        t = sig_t * z
        l1, l2 = t + rho, t - rho
        Delta = l1 * l2
        g1, g2 = rng.gauss(0, math.sqrt(2)), rng.gauss(0, math.sqrt(2))
        q = (g1 * g1 * l2 + g2 * g2 * l1) / 4
        acc += w * eabs_normal((0.6 * 2 * t) / 12 * Delta - q, (Delta / 12) ** 2 * 27.6) * Delta ** 0.25
        if (i + 1) % batch == 0:
            means.append(acc / batch)
            acc = 0.0
    m = sum(means) / len(means)
    return m, math.sqrt(sum((x - m) ** 2 for x in means) / (len(means) - 1) / len(means))


def run_X2():
    c2 = math.gamma(7 / 6) * 1.5 ** (1 / 3) * (4 / 3) / (2 * math.sqrt(3) * math.pi ** 1.5)
    c3 = math.gamma(7 / 6) * 1.5 ** (1 / 3) * (29 / 6 - math.sqrt(6)) / (2 * math.sqrt(3) * math.pi ** 2.5)
    k2 = -(16 / 7) * 2 ** 0.25 / math.pi ** 1.5          # c_1 = k_d J for the Gaussian kernel
    k3 = -(16 / 7) * 2 ** 0.25 / math.pi ** 2.5
    J2c, J2 = ey_d2(12, 28), ey_d2(24, 56)
    J3c, J3 = ey_d3(8, 8, 32), ey_d3(8, 8, 64)
    M3, se3 = mc_d3(8000000)
    q = 3 ** 0.25 / 2                                     # I_cand / c_1 (Theorem CU')
    return {'d2': {'J': round(J2, 10), 'J_coarse': round(J2c, 10), 'c': round(c2, 12), 'c1': round(k2 * J2, 8),
                   'c1_over_c': round(k2 * J2 / c2, 6), 'I_cand': round(q * k2 * J2, 8),
                   'rejected_coefficient': round((q - 1) * k2 * J2, 8),
                   'method': 'composite Gauss-Legendre, a = -w^4: 24x12 by 56x12 nodes (coarse: 12x12 by 28x12)'},
            'd3': {'J': round(J3, 9), 'J_coarse': round(J3c, 9), 'c': round(c3, 12), 'c1': round(k3 * J3, 8),
                   'c1_over_c': round(k3 * J3 / c3, 6), 'I_cand': round(q * k3 * J3, 8),
                   'rejected_coefficient': round((q - 1) * k3 * J3, 8),
                   'method': 'cone quadrature: Gauss-Legendre 64 x 64 in (rho, u), trapezoid 9 in theta, '
                             'Gauss-Laguerre 64 in s (coarse: Laguerre 32)',
                   'mc_check': {'J': round(M3, 5), 'J_se': round(se3, 5), 'c1': round(k3 * M3, 5),
                                'c1_se': round(-k3 * se3, 5),
                                'method': 'Monte Carlo on the cone, 8000000 samples, seed 1001, 10 batches'}}}


if __name__ == '__main__':
    out = {'object': 'CL-CUSP-SECOND-ORDER-20261001-v1.1 exploration', 'not_a_control': True}
    if len(sys.argv) < 2 or 'X2' in sys.argv[1:]:
        out['X2'] = run_X2()
    if len(sys.argv) < 2 or 'X1' in sys.argv[1:]:
        out['X1'] = run_X1()
    sys.stdout.write(json.dumps(out, indent=1, sort_keys=True) + '\n')
