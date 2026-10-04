#!/usr/bin/env python3
"""C127 review: floating-point companion (standard library). Builds the appendix's ten periodic duals
end to end on the torus with L = 2 pi (omega = 1), evaluates the ten functionals (U_r, A, f(x), grad f(x))
from the Fourier coefficients, and measures the duals' l1 norms as rho -> 0.

Checks, to float precision: L(phi_d) = d for the ten unit data vectors (pin dual with the exact Hessian
correction (F22), and the remote duals (F26)); and the cost exponents: pin/Hessian duals ~ rho^-7,
remote duals ~ rho^-9, as in (F23) and (F27). Not exact arithmetic; it supports the written argument.
"""
import cmath
import math
import random

RNG = random.Random(127)


def psi(z, p):
    return sum(1 - math.cos(z[j] - p[j]) for j in range(2))


def psi_grad(z, p):
    return [math.sin(z[j] - p[j]) for j in range(2)]


def tp_mul(a, b):
    out = {}
    for ka, va in a.items():
        for kb, vb in b.items():
            k = (ka[0] + kb[0], ka[1] + kb[1])
            out[k] = out.get(k, 0) + va * vb
    return out


def tp_add(a, b, s=1.0):
    out = dict(a)
    for k, v in b.items():
        out[k] = out.get(k, 0) + s * v
    return out


def tp_scale(a, s):
    return {k: s * v for k, v in a.items()}


def tp_psi(p):
    out = {(0, 0): 2 + 0j}
    for j in range(2):
        e = [0, 0]
        e[j] = 1
        out[tuple(e)] = out.get(tuple(e), 0) - 0.5 * cmath.exp(-1j * p[j])
        e[j] = -1
        out[tuple(e)] = out.get(tuple(e), 0) - 0.5 * cmath.exp(1j * p[j])
    return out


def tp_sin(j, c):
    e1, e2 = [0, 0], [0, 0]
    e1[j], e2[j] = 1, -1
    return {tuple(e1): cmath.exp(-1j * c[j]) / 2j, tuple(e2): -cmath.exp(1j * c[j]) / 2j}


def tp_val(a, z):
    return sum(v * cmath.exp(1j * (k[0] * z[0] + k[1] * z[1])) for k, v in a.items()).real


def tp_grad(a, z):
    gx = sum(v * 1j * k[0] * cmath.exp(1j * (k[0] * z[0] + k[1] * z[1])) for k, v in a.items()).real
    gy = sum(v * 1j * k[1] * cmath.exp(1j * (k[0] * z[0] + k[1] * z[1])) for k, v in a.items()).real
    return [gx, gy]


def tp_d2(a, z, w):
    """second directional derivative along unit w at z."""
    return sum(-v * (k[0] * w[0] + k[1] * w[1]) ** 2 * cmath.exp(1j * (k[0] * z[0] + k[1] * z[1]))
               for k, v in a.items()).real


def tp_l1(a):
    return sum(abs(v) for v in a.values())


def functionals(phi, r, u, v, x):
    M = [-r / 2 * u[0], -r / 2 * u[1]]
    S = [r / 2 * u[0], r / 2 * u[1]]
    fM, fS = tp_val(phi, M), tp_val(phi, S)
    gM, gS = tp_grad(phi, M), tp_grad(phi, S)
    ftM, ftS = gM[0] * u[0] + gM[1] * u[1], gS[0] * u[0] + gS[1] * u[1]
    fzM, fzS = gM[0] * v[0] + gM[1] * v[1], gS[0] * v[0] + gS[1] * v[1]
    U = [(fM + fS) / 2, (fS - fM) / r, (ftS - ftM) / r, 6 / r**2 * (ftM + ftS - 2 * (fS - fM) / r),
         (fzM + fzS) / 2, (fzS - fzM) / r]
    A = tp_d2(phi, [0.0, 0.0], v)
    return U + [A, tp_val(phi, x)] + tp_grad(phi, x)


def pin_dual(a, alpha, r, u, v, x):
    M = [-r / 2 * u[0], -r / 2 * u[1]]
    S = [r / 2 * u[0], r / 2 * u[1]]
    q = tp_psi(x)

    def p_phys(y):
        t, z = y[0] * u[0] + y[1] * u[1], y[0] * v[0] + y[1] * v[1]
        val = (a[0] - r * r * a[2] / 8 + (a[1] - r * r * a[3] / 24) * t + a[2] / 2 * t * t + a[3] / 6 * t**3
               + z * (a[4] + a[5] * t))
        dt = a[1] - r * r * a[3] / 24 + a[2] * t + a[3] / 2 * t * t + a[5] * z
        dz = a[4] + a[5] * t
        return val, [dt * u[0] + dz * v[0], dt * u[1] + dz * v[1]]

    # chart (F14)
    d = [math.sin(r / 2 * u[0]), math.sin(r / 2 * u[1])]
    nd = math.hypot(*d)
    e = [d[0] / nd, d[1] / nd]
    n = [-e[1], e[0]]
    h = 2 * nd
    vals, cgr = [], []
    for s in (M, S):
        pv, pg = p_phys(s)
        qv, qg = psi(s, x), psi_grad(s, x)
        gv = pv / qv
        gg = [(pg[j] * qv - pv * qg[j]) / qv**2 for j in range(2)]
        gs = [gg[j] / math.cos(s[j]) for j in range(2)]          # chart (sine-coordinate) gradient
        vals.append(gv)
        cgr.append((gs[0] * e[0] + gs[1] * e[1], gs[0] * n[0] + gs[1] * n[1]))
    F00, Fh0 = vals
    Ft00, Fth0 = cgr[0][0], cgr[1][0]
    Fz00, Fzh0 = cgr[0][1], cgr[1][1]
    b0, b1 = F00, Ft00
    b2 = 3 * (Fh0 - F00) / h**2 - (2 * Ft00 + Fth0) / h
    b3 = (Fth0 + Ft00) / h**2 - 2 * (Fh0 - F00) / h**3
    c0, c1 = Fz00, (Fzh0 - Fz00) / h
    s1, s2 = tp_sin(0, [0.0, 0.0]), tp_sin(1, [0.0, 0.0])
    T = tp_add(tp_add(tp_scale(s1, e[0]), tp_scale(s2, e[1])), {(0, 0): complex(nd)})   # t = e.(S_0 + d)
    Z = tp_add(tp_scale(s1, n[0]), tp_scale(s2, n[1]))                                   # z = n.S_0 = ell
    T2 = tp_mul(T, T)
    P = tp_add({(0, 0): complex(b0)}, tp_scale(T, b1))
    P = tp_add(P, tp_scale(T2, b2))
    P = tp_add(P, tp_scale(tp_mul(T2, T), b3))
    P = tp_add(P, tp_scale(Z, c0))
    P = tp_add(P, tp_scale(tp_mul(T, Z), c1))
    phi0 = tp_mul(q, P)
    corr = tp_mul(q, tp_mul(Z, Z))
    q0 = psi([0.0, 0.0], x)
    nv = n[0] * v[0] + n[1] * v[1]
    ca = (alpha - tp_d2(phi0, [0.0, 0.0], v)) / (2 * q0 * nv * nv)
    return tp_add(phi0, tp_scale(corr, ca))


def remote_dual(beta, r, u, x):
    M = [-r / 2 * u[0], -r / 2 * u[1]]
    S = [r / 2 * u[0], r / 2 * u[1]]
    O = [0.0, 0.0]
    qR = tp_mul(tp_mul(tp_psi(M), tp_psi(S)), tp_mul(tp_psi(O), tp_psi(O)))
    qv = tp_val(qR, x)
    qg = tp_grad(qR, x)
    aR = beta[0] / qv
    bR = [beta[1 + j] / qv - beta[0] * qg[j] / qv**2 for j in range(2)]
    Sx = tp_add(tp_scale(tp_sin(0, x), bR[0]), tp_scale(tp_sin(1, x), bR[1]))
    return tp_mul(qR, tp_add({(0, 0): complex(aR)}, Sx))


print("ten-functional duals (U_r, A, f(x), grad f(x)): exactness and l1 cost as rho decreases")
res = {}
for rho in (0.4, 0.2, 0.1, 0.05):
    worst_pin = worst_rem = 0.0
    err = 0.0
    for trial in range(10):
        ang = RNG.uniform(0, 2 * math.pi)
        u = [math.cos(ang), math.sin(ang)]
        v = [-u[1], u[0]] if RNG.random() < 0.5 else [u[1], -u[0]]
        r = rho / 16
        th = RNG.uniform(0, 2 * math.pi)
        rad = rho * RNG.uniform(1.0, 1.5)
        x = [rad * math.cos(th), rad * math.sin(th)]
        for i in range(7):
            a = [0.0] * 6
            alpha = 0.0
            if i < 6:
                a[i] = 1.0
            else:
                alpha = 1.0
            phi = pin_dual(a, alpha, r, u, v, x)
            got = functionals(phi, r, u, v, x)
            want = a + [alpha, 0.0, 0.0, 0.0]
            nrm = tp_l1(phi)
            err = max(err, max(abs(g - w) for g, w in zip(got, want)) / nrm)
            worst_pin = max(worst_pin, nrm)
        for i in range(3):
            beta = [0.0, 0.0, 0.0]
            beta[i] = 1.0
            phi = remote_dual(beta, r, u, x)
            got = functionals(phi, r, u, v, x)
            want = [0.0] * 7 + beta
            nrm = tp_l1(phi)
            err = max(err, max(abs(g - w) for g, w in zip(got, want)) / nrm)
            worst_rem = max(worst_rem, nrm)
    res[rho] = (worst_pin, worst_rem)
    print("  rho=%.3f: max l1 pin/Hessian duals %.3e (x rho^7 = %.3e); remote duals %.3e (x rho^9 = %.3e);"
          " max |L(phi) - d| / l1 = %.1e" % (rho, worst_pin, worst_pin * rho**7, worst_rem, worst_rem * rho**9, err))
sp = math.log(res[0.05][0] / res[0.4][0]) / math.log(8)
sr = math.log(res[0.05][1] / res[0.4][1]) / math.log(8)
print("  fitted growth: pin/Hessian duals rho^-%.2f (proof: rho^-7); remote duals rho^-%.2f (proof: rho^-9)" % (sp, sr))
