"""Numerical evaluation of the planar near cluster coefficients alpha_1, alpha_2 (CL-C6-CLUSTER-COEFF-NUMERICS-20260930-v1).

Standard library only. NOT a proof and NOT a certified enclosure: floating-point quadrature and Monte Carlo with
reported standard errors. Scientific effect NONE.

    python -B -S coefficients.py            # full run: writes RESULTS.json (GH40, GH60, MC 1e6 per k)
    python -B -S coefficients.py --check    # quick replay: exact identities, closed forms, GH40 against RESULTS.json
    python -B -S coefficients.py --check --mutant NAME   # rc 1 for each name in MUTANTS
"""
import argparse, json, math, random, sys
from fractions import Fraction as F

MUTANTS = ('cubic-sign', 'antiderivative', 'typed-boundary')
MUTANT = None
K_VALUES = (F(1, 2), F(1), F(2))
B_VALUES = (F(0), F(1))

# ------------------------------------------------------------------ exact part: continuum Gaussian kernel jets
JETS = {'f': (0, 0), 'fx': (1, 0), 'fz': (0, 1), 'fxx': (2, 0), 'fxz': (1, 1), 'fzz': (0, 2),
        'fxxx': (3, 0), 'fxxz': (2, 1), 'fxzz': (1, 2), 'fzzz': (0, 3)}

def hermite_moment(m):
    """d^m/dx^m exp(-x^2/2) at 0 = (-1)^(m/2) (m-1)!! for even m, 0 for odd m."""
    if m % 2: return F(0)
    v = F(1)
    for j in range(1, m, 2): v *= j
    return v if (m // 2) % 2 == 0 else -v

def exact_cov():
    """Cov(d^alpha f(0), d^beta f(0)) = (-1)^|beta| d^(alpha+beta) K(0), K(z) = exp(-|z|^2/2)."""
    C = {}
    for u, au in JETS.items():
        for v, av in JETS.items():
            sign = -1 if (av[0] + av[1]) % 2 else 1
            C[(u, v)] = sign * hermite_moment(au[0] + av[0]) * hermite_moment(au[1] + av[1])
    return C

def solve(A, B):
    n = len(A); m = len(B[0]); Ab = [A[i][:] + B[i][:] for i in range(n)]
    for i in range(n):
        piv = next(r for r in range(i, n) if Ab[r][i] != 0)
        Ab[i], Ab[piv] = Ab[piv], Ab[i]; p = Ab[i][i]
        Ab[i] = [x / p for x in Ab[i]]
        for r in range(n):
            if r != i and Ab[r][i] != 0:
                f = Ab[r][i]; Ab[r] = [x - f * y for x, y in zip(Ab[r], Ab[i])]
    return [row[n:] for row in Ab]

def regression(C, targets, outputs):
    """(coefficient matrix K, conditional covariance) with mean = K . target values."""
    S_tt = [[C[(r, c)] for c in targets] for r in targets]
    S_ot = [[C[(r, c)] for c in targets] for r in outputs]
    S_oo = [[C[(r, c)] for c in outputs] for r in outputs]
    Kt = solve(S_tt, [list(col) for col in zip(*S_ot)])          # S_tt^-1 S_ot^T
    K = [list(col) for col in zip(*Kt)]                            # S_ot S_tt^-1
    cov = [[S_oo[i][j] - sum(K[i][t] * S_ot[j][t] for t in range(len(targets))) for j in range(len(outputs))]
           for i in range(len(outputs))]
    return K, cov

def require(ok, msg):
    if not ok: raise ValueError(msg)

def exact_structure():
    C = exact_cov()
    K_even, cov_even = regression(C, ['f', 'fxx', 'fxz'], ['fzz'])
    require(K_even == [[F(-1), F(0), F(0)]], 'even block: mean of f_zz given (f, f_xx, f_xz) = (b,0,0) is -b')
    require(cov_even == [[F(2)]], 'even block: conditional variance of f_zz is 2')
    K_odd, cov_odd = regression(C, ['fx', 'fz', 'fxxx'], ['fxxz', 'fxzz', 'fzzz'])
    require(all(K_odd[i][2] == 0 for i in range(3)), 'odd block: no dependence on the f_xxx = 12k pin')
    require(K_odd[0][0] == 0 and K_odd[2][0] == 0 and K_odd[1][1] == 0, 'odd block: parity zeros')
    require(cov_odd == [[F(2), F(0), F(0)], [F(0), F(2), F(0)], [F(0), F(0), F(6)]],
            'odd block: (f_xxz, f_xzz, f_zzz) | pins ~ N(0, diag(2, 2, 6))')
    return {'mu_A': '-b', 'var_A': 2, 'odd_mean': [0, 0, 0], 'odd_cov_diag': [2, 2, 6],
            'var_fxxx': str(C[('fxxx', 'fxxx')]), 'cov_fx_fxxx': str(C[('fx', 'fxxx')])}

# ------------------------------------------------------------------ lattice sums for the exact periodized kernel
def lattice_cov(L):
    N = int(math.ceil(L * 2.6)) + 3; c = 2 * math.pi ** 2 / L ** 2
    Z = 0.0; M = {}
    for n1 in range(-N, N + 1):
        for n2 in range(-N, N + 1):
            w = math.exp(-c * (n1 * n1 + n2 * n2)); Z += w
            for p in range(0, 7, 2):
                for q in range(0, 7, 2):
                    M[(p, q)] = M.get((p, q), 0.0) + w * n1 ** p * n2 ** q
    C = {}
    for u, au in JETS.items():
        for v, av in JETS.items():
            p, q = au[0] + av[0], au[1] + av[1]
            if p % 2 or q % 2: C[(u, v)] = 0.0; continue
            coef = (2j * math.pi / L) ** (au[0] + au[1]) * (-2j * math.pi / L) ** (av[0] + av[1])
            C[(u, v)] = (coef * M[(p, q)] / Z).real
    return C

# ------------------------------------------------------------------ the s-integral of the pin weight over {n = j}
def cubic_g(s, B, k, D2):
    sgn = 1 if MUTANT == 'cubic-sign' else -1
    return -2 * s ** 3 + 3 * B * s ** 2 + sgn * B ** 3 - 12 * k * D2

def cubic_roots(B, k, D2):
    g = lambda s: cubic_g(s, B, k, D2)
    pts = sorted({-1e3 * (1 + abs(B) + k + D2), B, 0.0, 1e3 * (1 + abs(B) + k + D2)})
    while g(pts[0]) <= 0: pts[0] *= 2
    while g(pts[-1]) >= 0: pts[-1] *= 2
    roots = []
    for lo, hi in zip(pts[:-1], pts[1:]):
        glo, ghi = g(lo), g(hi)
        if glo == 0: roots.append(lo); continue
        if glo * ghi < 0:
            for _ in range(200):
                mid = 0.5 * (lo + hi); gm = g(mid)
                if gm == 0: lo = hi = mid; break
                if glo * gm < 0: hi, ghi = mid, gm
                else: lo, glo = mid, gm
            roots.append(0.5 * (lo + hi))
    return sorted(set(roots))

def shear(a, b, c, k):
    B = b - a * a / (12 * k); D = (c - a * b / (4 * k) + a ** 3 / (72 * k * k)) / 2
    return B, D

def typed_top(B):
    return -abs(B) if MUTANT == 'typed-boundary' else -abs(B) / 2

def n_classifier(s, a, b, c, k):
    B, D = shear(a, b, c, k)
    if not s < typed_top(B): return 0
    g = cubic_g(s, B, k, D * D)
    if s > B: return 2 if g > 0 else 1
    return 1 if g < 0 else 0

def n_direct(s, a, b, c, k):
    """critical points of G(u, Z) = C(u) + (s + Bu) Z^2/2 + (D/3) Z^3 off Z = 0 with height in (-k, 0)."""
    B, D = shear(a, b, c, k); Cu = lambda u: 2 * k * u ** 3 - 1.5 * k * u - k / 2; hs = []
    if abs(D) > 1e-14:
        A2 = 6 * k + B ** 3 / (2 * D * D); A1 = B * B * s / (D * D); A0 = B * s * s / (2 * D * D) - 1.5 * k
        if abs(A2) < 1e-14: us = [-A0 / A1] if abs(A1) > 1e-14 else []
        else:
            disc = A1 * A1 - 4 * A2 * A0
            us = [] if disc < 0 else [(-A1 + sg * math.sqrt(disc)) / (2 * A2) for sg in (1, -1)]
        for u in us:
            w = s + B * u; Z = -w / D
            if abs(Z) > 1e-12: hs.append(Cu(u) + w * Z * Z / 2 + D * Z ** 3 / 3)
    elif abs(B) > 1e-14:
        u = -s / B; Z2 = 3 * k * (1 - 4 * u * u) / B
        if Z2 > 1e-14: hs += [Cu(u), Cu(u)]
    return sum(1 for h in hs if -k < h < 0)

def antiderivative(s, B, k):
    if MUTANT == 'antiderivative': return 12 * k * k * s ** 3 - 9 * k * k * B * s
    return 12 * k * k * s ** 3 - 9 * k * k * B * B * s        # of 9 k^2 (4 s^2 - B^2)

def I_j(a, b, c, k):
    B, D = shear(a, b, c, k); D2 = D * D; top = typed_top(B)
    roots = cubic_roots(B, k, D2); g = lambda s: cubic_g(s, B, k, D2)
    bps = [-math.inf] + roots + [math.inf]; pos, neg = [], []
    for lo, hi in zip(bps[:-1], bps[1:]):
        if lo == -math.inf and hi == math.inf: mid = 0.0
        elif lo == -math.inf: mid = hi - 1.0 - abs(hi)
        elif hi == math.inf: mid = lo + 1.0 + abs(lo)
        else: mid = 0.5 * (lo + hi)
        (pos if g(mid) > 0 else neg).append((lo, hi))
    def clip(lo, hi, a_, b_):
        lo2, hi2 = max(lo, a_), min(hi, b_)
        return antiderivative(hi2, B, k) - antiderivative(lo2, B, k) if hi2 > lo2 else 0.0
    I1 = sum(clip(lo, hi, -1e300, top) for lo, hi in neg)
    I2 = sum(clip(lo, hi, B, top) for lo, hi in pos) if B < top else 0.0
    return I1, I2

# ------------------------------------------------------------------ prefactor p_b(0) / z_0, closed form
def phi(x): return math.exp(-x * x / 2) / math.sqrt(2 * math.pi)
def Phi(x): return 0.5 * math.erfc(-x / math.sqrt(2))

def prefactor(k, b):
    """p_b(0) / z_0 with A ~ N(-b, 2): p_b(0) = phi(b/sqrt2)/sqrt2, z_0 = 36 k^2 E[A^2 1{A<0}]."""
    t = b / math.sqrt(2)
    m2 = (b * b + 2) * Phi(t) + math.sqrt(2) * b * phi(t)
    return phi(t) / math.sqrt(2) / (36 * k * k * m2), m2

# ------------------------------------------------------------------ quadrature
def gauss_hermite(n):
    """probabilists' Gauss-Hermite nodes/weights (sum of weights 1), by Newton on normalized Hermite functions."""
    nodes = []
    for i in range(1, n // 2 + 1):
        if i == 1: x = math.sqrt(2 * n + 1) - 1.85575 * (2 * n + 1) ** (-1 / 6)
        elif i == 2: x = nodes[-1] - 1.14 * n ** 0.426 / nodes[-1]
        elif i == 3: x = 1.86 * nodes[-1] - 0.86 * nodes[0]
        elif i == 4: x = 1.91 * nodes[-1] - 0.91 * nodes[-2]
        else: x = 2 * nodes[-1] - nodes[-2]
        for _ in range(100):
            p0 = 1.0 / math.pi ** 0.25; pm, pc = p0, math.sqrt(2) * x * p0
            for j in range(2, n + 1):
                pm, pc = pc, math.sqrt(2 / j) * x * pc - math.sqrt((j - 1) / j) * pm
            dx = pc / (math.sqrt(2 * n) * pm); x -= dx
            if abs(dx) < 1e-15: break
        nodes.append(x)
    out = []
    for x in sorted(set(nodes + [-v for v in nodes] + ([0.0] if n % 2 else []))):
        p0 = 1.0 / math.pi ** 0.25; pm, pc = p0, math.sqrt(2) * x * p0
        for j in range(2, n + 1):
            pm, pc = pc, math.sqrt(2 / j) * x * pc - math.sqrt((j - 1) / j) * pm
        w = 2.0 / (2 * n * pm * pm) / math.sqrt(math.pi)
        out.append((x * math.sqrt(2), w))
    return out

SIG = (math.sqrt(2.0), math.sqrt(2.0), math.sqrt(6.0))   # odd block: N(0, diag(2, 2, 6)), exact structure

def J_gh(k, order):
    gh = gauss_hermite(order); J1 = J2 = 0.0
    for x1, w1 in gh:
        for x2, w2 in gh:
            for x3, w3 in gh:
                i1, i2 = I_j(SIG[0] * x1, SIG[1] * x2, SIG[2] * x3, k); w = w1 * w2 * w3
                J1 += w * i1; J2 += w * i2
    return J1, J2

def J_mc(k, n, seed):
    rng = random.Random(seed); s1 = s2 = q1 = q2 = 0.0
    for _ in range(n):
        i1, i2 = I_j(SIG[0] * rng.gauss(0, 1), SIG[1] * rng.gauss(0, 1), SIG[2] * rng.gauss(0, 1), k)
        s1 += i1; s2 += i2; q1 += i1 * i1; q2 += i2 * i2
    m1, m2 = s1 / n, s2 / n
    return m1, m2, math.sqrt(max(q1 / n - m1 * m1, 0) / n), math.sqrt(max(q2 / n - m2 * m2, 0) / n)

def sig6(x): return float('%.6g' % x)

# ------------------------------------------------------------------ controls
def controls():
    ex = exact_structure()
    # lattice sums at L = 24 and 12 agree with the continuum table
    dev = 0.0
    for L in (24.0, 12.0):
        C = lattice_cov(L)
        for key, val in exact_cov().items():
            dev = max(dev, abs(C[key] - float(val)))
    require(dev < 1e-9, 'lattice-sum jet covariances match the continuum Gaussian table')
    # classifier against direct root count on the typed domain
    rng = random.Random(5); mism = 0
    for _ in range(4000):
        k = rng.choice([0.5, 1.0, 2.0]); a, b, c = (rng.uniform(-4, 4) for _ in range(3))
        B, _ = shear(a, b, c, k); s = -abs(B) / 2 - rng.uniform(0, 6)
        mism += n_classifier(s, a, b, c, k) != n_direct(s, a, b, c, k)
    require(mism == 0, 'classifier agrees with the direct critical-point count on the typed domain')
    # closed forms: [LM] cubic gives (0, 48 k^5); B = 0 family gives (72 k^3 D^2, 0); exact antiderivative identity
    for k in (0.5, 1.0, 2.0):
        i1, i2 = I_j(0.0, -2 * k, 0.0, k)
        require(abs(i1) < 1e-9 and abs(i2 - 48 * k ** 5) < 1e-9 * (1 + 48 * k ** 5), '[LM] cubic mass 48 k^5 on n = 2')
        i1, i2 = I_j(0.0, 0.0, 1.0, k)
        require(abs(i2) < 1e-9 and abs(i1 - 18 * k ** 3) < 1e-9 * (1 + 18 * k ** 3), 'B = 0 family mass 72 k^3 D^2 on n = 1')
    kq, Bq = F(1), F(-2); Fq = lambda s: 12 * kq * kq * s ** 3 - 9 * kq * kq * Bq * Bq * s
    require(Fq(Bq / 2) - Fq(Bq) == 48, 'exact antiderivative of 9k^2(4s^2 - B^2) over (B, B/2) at k = 1, B = -2')
    require(sum(w for _, w in gauss_hermite(40)) - 1 < 1e-12 and abs(sum(x * x * w for x, w in gauss_hermite(40)) - 1) < 1e-10,
            'Gauss-Hermite weights normalized')
    return ex, dev

def main():
    global MUTANT
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--check', action='store_true'); ap.add_argument('--mutant', choices=MUTANTS)
    args = ap.parse_args(); MUTANT = args.mutant
    try:
        ex, dev = controls()
        if args.check:
            ref = json.load(open('RESULTS.json'))
            for k in K_VALUES:
                J1, J2 = J_gh(float(k), 40)
                rec = ref['per_k'][str(k)]
                for got, name in ((J1, 'J1_gh40'), (J2, 'J2_gh40')):
                    require(abs(got - rec[name]) <= 1e-6 * (1 + abs(rec[name])), 'GH40 replay matches RESULTS.json for ' + name)
            print(json.dumps({'passed': True, 'mode': 'check', 'scientific_effect': 'NONE'}, sort_keys=True))
            return 0
        out = {'schema': 1, 'object': 'CL-C6-CLUSTER-COEFF-NUMERICS-20260930-v1', 'scientific_effect': 'NONE',
               'certified': False, 'method': 'exact contact regression + interval-exact s-integral + Gauss-Hermite / Monte Carlo',
               'exact_structure': ex, 'lattice_vs_continuum_max_dev': sig6(dev), 'per_k': {}, 'prefactor': {}}
        for k in K_VALUES:
            kf = float(k)
            g40 = J_gh(kf, 40); g60 = J_gh(kf, 60); mc = J_mc(kf, 1000000, seed=2026)
            rec = {'J1_gh40': g40[0], 'J2_gh40': g40[1], 'J1_gh60': sig6(g60[0]), 'J2_gh60': sig6(g60[1]),
                   'J1_mc': sig6(mc[0]), 'J2_mc': sig6(mc[1]), 'J1_mc_se': sig6(mc[2]), 'J2_mc_se': sig6(mc[3]),
                   'ratio2_gh60': sig6(g60[1] / (g60[0] + g60[1])), 'palm_near_gh60': sig6(2 * g60[1] / (g60[0] + 2 * g60[1]))}
            out['per_k'][str(k)] = rec
            for b in B_VALUES:
                pf, m2 = prefactor(kf, float(b))
                out['prefactor'][f'k={k},b={b}'] = {'p_b0_over_z0': sig6(pf), 'm2_b': sig6(m2), 'z0': sig6(36 * kf * kf * m2),
                                                     'alpha1_gh60': sig6(pf * g60[0]), 'alpha2_gh60': sig6(pf * g60[1]),
                                                     'alpha1_mc': sig6(pf * mc[0]), 'alpha2_mc': sig6(pf * mc[1])}
            print(f'k={k}: done', file=sys.stderr, flush=True)
        json.dump(out, open('RESULTS.json', 'w'), indent=2, sort_keys=True); open('RESULTS.json', 'a').write('\n')
        print(json.dumps({'passed': True, 'mode': 'full', 'scientific_effect': 'NONE'}, sort_keys=True))
        return 0
    except ValueError as exc:
        print(json.dumps({'passed': False, 'error': str(exc)}, sort_keys=True)); return 1

if __name__ == '__main__':
    sys.exit(main())
