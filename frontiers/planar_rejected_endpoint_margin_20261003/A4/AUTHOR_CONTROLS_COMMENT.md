## QS addendum A4: author controls, exact executable and stdout

This publishes the standard-library control script that [A4 (5972396791)](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5972396791) cites, so anyone can replay it. It checks finite algebra only. It does not prove the imported Gaussian estimates (C92, C93, C94, C101), the continuous path argument or C96's identification.

Dylan Roy — delegated AI work. Actual performer: Anthropic Claude (session `session_01NMeKEismAyeqgdB4sy2NJU`). Scientific effect: NONE.

**Extraction rule.**
- The file is the exact text between the ```` ```python ```` fence under the `###` heading and the next ```` ``` ```` line, plus one final newline.
- The expected stdout is the text in the following ```` ```text ```` fence, plus one final newline.
- The byte counts below include those newlines.

**Run.**
- `python3 -B -S a4_exact.py`: exit 0, with exactly the stdout shown.
- `-O` mode: byte-identical output.
- `python3 a4_exact.py BOGUS`: exit 2.
- Each mutant label exits 1: `G_QUARTER`, `LOCAL_36`, `NO_PIN_GRAD`, `OLD_ENDPOINT`, `P_TWO` and `OMEGA_HALF`.

The output was produced with Python 3.11.15. A run takes about 4 seconds.

### a4_exact.py

- **File:** 17262 bytes, SHA-256 `f880ffb044a3102781c71cb3b4ac65d65260c31588c6835520349e5c7bdc2b95`.
- **Stdout:** 502 bytes, SHA-256 `022ff38c96e6378dd4dc9c00e14deebf167443d71fd6d2b0cee6f483d95cc28e`.

```python
#!/usr/bin/env python3
"""QS addendum A4: author controls (exact rational checks, standard library only).

Object: CL-QS-A4-LOCAL-ENDPOINT-PLANAR-RATES-20261003-v1 (main issue 229).
Author: Anthropic Claude, session_01NMeKEismAyeqgdB4sy2NJU, for Dylan Roy (delegated AI work).

Usage: python3 a4_exact.py [MUTANT]
  exit 0: every check passes; exit 1: some check fails; exit 2: unknown label.
Mutant labels (each must make the script exit 1):
  G_QUARTER     raw cubic with (gamma/2)(X^2 - 1/3)zeta instead of (gamma/2)(X^2 - 1/4)zeta
  LOCAL_36      margin with gamma^2 + 36 instead of gamma^2 + 72
  NO_PIN_GRAD   Taylor remainder identity used without the first-order term, for fields
                with e(M) = 0 but a nonzero gradient at M (adds X + 1/2)
  OLD_ENDPOINT  growing-Lambda ledger keeping C101's H^4 e^(2/3) endpoint term
  P_TWO         growing-Lambda ledger with the moment order fixed at p = 2
  OMEGA_HALF    growing-Lambda ledger with w = r^(-beta/16)
These checks test finite algebra only. They do not prove the imported Gaussian estimates
(C92, C93, C94, C101), the continuous path argument or C96's identification.
"""
import sys
import random
from fractions import Fraction as F

MUTANTS = ("G_QUARTER", "LOCAL_36", "NO_PIN_GRAD", "OLD_ENDPOINT", "P_TWO", "OMEGA_HALF")
MUT = None
if len(sys.argv) > 1:
    MUT = sys.argv[1]
    if MUT not in MUTANTS:
        print("unknown mutant label: %s" % MUT)
        sys.exit(2)

RNG = random.Random(20261003_4)
RESULTS, FAILS = [], []


class Group:
    def __init__(self, name):
        self.name, self.n, self.bad = name, 0, 0

    def check(self, ok, msg=""):
        self.n += 1
        if not ok:
            self.bad += 1
            if len(FAILS) < 12:
                FAILS.append("%s: %s" % (self.name, msg))

    def close(self):
        RESULTS.append((self.name, self.n - self.bad, self.n))


def rq(lo, hi, den=97):
    a, b = int(F(lo) * den), int(F(hi) * den)
    return F(RNG.randint(a, b), den)


def rq_nonzero(lo, hi, den=97):
    while True:
        x = rq(lo, hi, den)
        if x != 0:
            return x


def P(u, Z, psi, c, R):
    return 2 * u**3 - F(3, 2) * u - F(1, 2) - (psi + 2 * c * u) * Z**2 / 48 + R * Z**3 / 3456


def crit_family(n):
    """Exact critical points Y = (-sigma/2, Z) of typed cubics; one in five near a degenerate M."""
    out = []
    while len(out) < n:
        if len(out) % 5 == 4:
            Zv = rq_nonzero(F(-1, 20), F(1, 20), 9973)
            sg = 1 + rq(F(-1, 50), F(1, 50), 9973) * Zv**2
            cv = 36 * (sg**2 - 1) / Zv**2
            psv = cv * sg + rq_nonzero(-20, 20) * Zv / 48
        else:
            sg = rq(-5, 5)
            Zv = rq_nonzero(-12, 12)
            cv = 36 * (sg**2 - 1) / Zv**2
            psv = abs(cv) + rq(F(1, 97), 30)
        if not psv > abs(cv):
            continue
        Rv = 48 * (psv - cv * sg) / Zv
        out.append((psv, cv, Rv, -sg / 2, Zv))
    return out


CRIT = crit_family(3000)

# =====================================================================
# L0  the pins of the raw cubic: G = P o chart, G and grad G vanish at raw M = (-1/2, 0),
#     G = -1 and grad G = 0 at raw S = (1/2, 0) (symbolic in lambda, gamma, B1, C3)
# =====================================================================
g = Group("L0 raw cubic: G = P o chart; pins at raw M and raw S")
NV = 6  # X, zeta, lambda, gamma, B1, C3


def pv(i):
    e = [0] * NV
    e[i] = 1
    return {tuple(e): F(1)}


def pc(c):
    return {tuple([0] * NV): F(c)} if c else {}


def padd(*ps):
    r = {}
    for q in ps:
        for k, v in q.items():
            r[k] = r.get(k, 0) + v
    return {k: v for k, v in r.items() if v != 0}


def psc(q, c):
    return {k: v * F(c) for k, v in q.items()} if c else {}


def pmul(*ps):
    r = ps[0]
    for q in ps[1:]:
        out = {}
        for k1, v1 in r.items():
            for k2, v2 in q.items():
                k = tuple(x + y for x, y in zip(k1, k2))
                out[k] = out.get(k, 0) + v1 * v2
        r = {k: v for k, v in out.items() if v != 0}
    return r


def pdiff(q, i):
    out = {}
    for k, v in q.items():
        if k[i] > 0:
            kk = list(k)
            kk[i] -= 1
            out[tuple(kk)] = out.get(tuple(kk), 0) + v * k[i]
    return {k: v for k, v in out.items() if v != 0}


def psub_xz(q, x0, z0):
    out = {}
    for k, v in q.items():
        kk = (0, 0) + k[2:]
        out[kk] = out.get(kk, 0) + v * x0**k[0] * z0**k[1]
    return {k: v for k, v in out.items() if v != 0}


X_, Z_, LAM, GAM, B1_, C3_ = (pv(i) for i in range(NV))
qc = F(-1, 3) if MUT == "G_QUARTER" else F(-1, 4)
Gp = padd(psc(pmul(X_, X_, X_), 2), psc(X_, F(-3, 2)), pc(F(-1, 2)),
          pmul(psc(GAM, F(1, 2)), padd(pmul(X_, X_), pc(qc)), Z_),
          psc(pmul(LAM, Z_, Z_), F(-1, 2)), psc(pmul(B1_, X_, Z_, Z_), F(1, 2)),
          psc(pmul(C3_, Z_, Z_, Z_), F(1, 6)))
uu = padd(X_, psc(pmul(GAM, Z_), F(1, 12)))
Dq = padd(pmul(GAM, GAM), psc(B1_, -12))
Jq = padd(psc(pmul(GAM, GAM, GAM), 8), psc(pmul(B1_, GAM), -144), psc(C3_, 576))
Pchart = padd(psc(pmul(uu, uu, uu), 2), psc(uu, F(-3, 2)), pc(F(-1, 2)),
              psc(padd(psc(pmul(LAM, Z_, Z_), 24), psc(pmul(Dq, Z_, Z_, uu), 2)), F(-1, 48)),
              psc(pmul(Jq, Z_, Z_, Z_), F(1, 3456)))
g.check(padd(Gp, psc(Pchart, -1)) == {}, "G = P o chart (psi Z^2 = 24 lambda zeta^2, c Z^2 = D zeta^2, R Z^3 = J zeta^3)")
for (x0, val) in ((F(-1, 2), F(0)), (F(1, 2), F(-1))):
    g.check(psub_xz(Gp, x0, F(0)) == pc(val), "G value at raw pin")
    g.check(psub_xz(pdiff(Gp, 0), x0, F(0)) == {}, "d G/dX = 0 at raw pin")
    g.check(psub_xz(pdiff(Gp, 1), x0, F(0)) == {}, "d G/dzeta = 0 at raw pin")
g.close()

# =====================================================================
# L1  Lemma LE (ii): 4h >= 2 min(1, a_M/(gamma^2+72)) |v|^2, v = raw(Y - M)
# =====================================================================
g = Group("L1 LE margin: 4h >= 2 min(1, a_M/(g^2+72))|v|^2")
cst = F(36) if MUT == "LOCAL_36" else F(72)
tight = F(0)
for (psv, cv, Rv, uY, Zv) in CRIT:
    h = -P(uY, Zv, psv, cv, Rv)
    a, z = uY + F(1, 2), Zv
    kM = (psv - cv) / 48
    rho2 = 3 * a**2 + kM * z**2
    g.check(h == rho2 / 3 and h > 0, "h = rho^2/3 (C97 (R7))")
    for gv in (rq_nonzero(-5, 5), rq_nonzero(F(-1, 4), F(1, 4), 997), rq_nonzero(-40, 40)):
        raw2 = (a - z / 12)**2 + (z / gv)**2
        aM = gv**2 * (psv - cv)
        g.check(raw2 <= 2 * a**2 + z**2 * (F(1, 72) + 1 / gv**2), "|v|^2 <= 2a^2 + z^2(1/72 + 1/g^2)")
        g.check(kM / (F(1, 72) + 1 / gv**2) == F(3, 2) * aM / (gv**2 + 72), "kappa_M/(1/72+1/g^2) = (3/2)a_M/(g^2+72)")
        bound = 2 * min(F(1), aM / (gv**2 + cst)) * raw2
        g.check(4 * h >= bound, "4h >= bound")
        if bound > 0:
            tight = max(tight, bound / (4 * h))
        # the proof: 4h - 2l|v|^2 is the quadratic form with matrix [[4-2l, l/6], [l/6, q22]]
        ell = min(F(1), aM / (gv**2 + 72))
        q22 = aM / (36 * gv**2) - ell / 72 - 2 * ell / gv**2
        form = (4 - 2 * ell) * a**2 + 2 * (ell / 6) * a * z + q22 * z**2
        g.check(form == 4 * h - 2 * ell * raw2, "matrix reproduces 4h - 2l|v|^2")
        det = (4 - 2 * ell) * q22 - (ell / 6)**2
        if aM <= gv**2 + 72:
            g.check(q22 == ell / 72 and det == ell * (1 - ell) / 18, "case l = a_M/(g^2+72): entry l/72, det l(1-l)/18")
        else:
            g.check(det == (aM - gv**2 - 72) / (18 * gv**2) and det > 0, "case l = 1: det (a_M-g^2-72)/(18g^2) > 0")
        g.check(4 - 2 * ell > 0 and det >= 0, "positive semidefinite")
g.check(tight > F(1, 3), "the bound is not vacuous (ratio > 1/3 attained)")
# equality is attained by a selected saddle: gamma = 1, psi = 86, c = 13, R = 3400, Y = (-7/12, 1)
pe, ce, Re, ue, Ze, ge = F(86), F(13), F(3400), F(-7, 12), F(1), F(1)
he = -P(ue, Ze, pe, ce, Re)
ae, ze = ue + F(1, 2), Ze
raw2e = (ae - ze / 12)**2 + (ze / ge)**2
g.check(6 * ue**2 - F(3, 2) - ce * Ze**2 / 24 == 0 and -(pe + 2 * ce * ue) * Ze / 24 + Re * Ze**2 / 1152 == 0, "Y critical")
g.check((12 * ue) * (-(pe + 2 * ce * ue) / 24 + Re * Ze / 576) - (ce * Ze / 12)**2 < 0, "Y a saddle")
g.check(he == F(37, 72) and ge**2 * (pe - ce) == ge**2 + 72, "h = 37/72 and a_M = g^2 + 72")
g.check(4 * he == 2 * raw2e, "equality 4h = 2|v|^2 = 37/18")
g.close()

# =====================================================================
# L2  Lemma LE (i) mechanism: exact Taylor identity along [M, p] with pinned M,
#     e(p) = int_0^1 (1-s) D^2 e(M + s d)[d, d] ds, d = p - M, when e(M) = 0, grad e(M) = 0.
# =====================================================================
g = Group("L2 LE Taylor identity with exact pins")


def poly_eval(cf, x, y):
    return sum(c * x**i * y**j for (i, j), c in cf.items())


def poly_d(cf, var):
    out = {}
    for (i, j), c in cf.items():
        if var == 0 and i > 0:
            out[(i - 1, j)] = out.get((i - 1, j), 0) + c * i
        if var == 1 and j > 0:
            out[(i, j - 1)] = out.get((i, j - 1), 0) + c * j
    return out


def integrate_poly_s(coeffs):
    """int_0^1 sum_k coeffs[k] s^k ds"""
    return sum(c / (k + 1) for k, c in enumerate(coeffs))


def poly_mul_s(p1, p2):
    out = [F(0)] * (len(p1) + len(p2) - 1)
    for i, a in enumerate(p1):
        for j, b in enumerate(p2):
            out[i + j] += a * b
    return out


def along(cf, M, d):
    """coefficients in s of cf(M + s d), cf of total degree <= 4"""
    # expand by sampling at 6 points and solving exactly (Lagrange) -- degree <= 4 in s
    pts = [F(k) for k in range(6)]
    vals = [poly_eval(cf, M[0] + s * d[0], M[1] + s * d[1]) for s in pts]
    # Newton divided differences -> monomial coefficients
    n = len(pts)
    coef = list(vals)
    for j in range(1, n):
        for i in range(n - 1, j - 1, -1):
            coef[i] = (coef[i] - coef[i - 1]) / (pts[i] - pts[i - j])
    mono = [F(0)] * n
    for i in range(n - 1, -1, -1):
        # mono = mono * (s - pts[i]) + coef[i]
        new = [F(0)] * n
        for k in range(n - 1):
            new[k + 1] += mono[k]
        for k in range(n):
            new[k] -= pts[i] * mono[k]
        new[0] += coef[i]
        mono = new
    return mono


for _ in range(400):
    M = (F(-1, 2), F(0))
    cf = {}
    for i in range(5):
        for j in range(5 - i):
            if i + j >= 2:
                cf[(i, j)] = rq(-3, 3)
    # shift so that the polynomial is centred at M: e(x, y) = q(x + 1/2, y) has e(M) = 0, grad e(M) = 0
    def e_cf(cf=cf):
        out = {}
        for (i, j), c in cf.items():
            # (x + 1/2)^i y^j expanded
            from math import comb
            for k in range(i + 1):
                out[(k, j)] = out.get((k, j), 0) + c * comb(i, k) * F(1, 2)**(i - k)
        return out
    ecf = e_cf()
    if MUT == "NO_PIN_GRAD":
        ecf[(1, 0)] = ecf.get((1, 0), 0) + 1        # adds X + 1/2: e(M) = 0 kept, grad e(M) != 0
        ecf[(0, 0)] = ecf.get((0, 0), 0) + F(1, 2)
    g.check(poly_eval(ecf, *M) == 0, "e(M) = 0")
    gx, gy = poly_d(ecf, 0), poly_d(ecf, 1)
    pin_grad = (poly_eval(gx, *M) == 0 and poly_eval(gy, *M) == 0)
    if MUT != "NO_PIN_GRAD":
        g.check(pin_grad, "grad e(M) = 0")
    p = (rq(-3, 3), rq(-3, 3))
    d = (p[0] - M[0], p[1] - M[1])
    exx, exy, eyy = poly_d(gx, 0), poly_d(gx, 1), poly_d(gy, 1)
    quad = {}
    for (cfk, wgt) in ((exx, d[0] * d[0]), (exy, 2 * d[0] * d[1]), (eyy, d[1] * d[1])):
        for k, val in cfk.items():
            quad[k] = quad.get(k, 0) + val * wgt
    s_coeffs = along(quad, M, d)
    rem = integrate_poly_s(poly_mul_s([F(1), F(-1)], s_coeffs))
    g.check(poly_eval(ecf, *p) == rem, "e(p) = int (1-s) D^2e[d,d] ds")
# sharpness of LE (i): e = (m/2)(X + 1/2 + zeta)^2 has largest Hessian entry m and,
# along d parallel to (1, 1), |e(M + d)| = m |d|^2 exactly
for _ in range(50):
    mm = rq(F(1, 97), 5)
    sc = rq_nonzero(-3, 3)
    d = (sc, sc)
    val = mm / 2 * (d[0] + d[1])**2
    g.check(val == mm * (d[0]**2 + d[1]**2), "LE (i) attained by (m/2)(X + 1/2 + zeta)^2")
g.close()

# =====================================================================
# L3  Corollary LE, scalar margin bookkeeping: with E0 < mu/2 along K and the LE endpoint
#     bound, the chord stays above -1 and ends above 0
# =====================================================================
g = Group("L3 Good_LE scalar margin bookkeeping")
cnt = 0
for (psv, cv, Rv, uY, Zv) in CRIT:
    h = -P(uY, Zv, psv, cv, Rv)
    if not (0 < h < 1):
        continue
    mu = 1 - h
    a, z = uY + F(1, 2), Zv
    for gv in (rq_nonzero(-5, 5), rq_nonzero(F(-1, 4), F(1, 4), 997)):
        cnt += 1
        raw2 = (a - z / 12)**2 + (z / gv)**2
        aM = gv**2 * (psv - cv)
        m_loc = min(F(1), aM / (gv**2 + 72))
        th = rq(F(1, 100), F(99, 100))
        E0 = th * mu / 2                                  # window error E0 < mu/2
        X = th * m_loc                                    # X = 2 K2 N r w^2 < min(1, a_M/(g^2+72))
        end_err = 2 * X * raw2                            # LE (i): |E_r(2Y-M)| <= 4 K2 N r w^2 |v|^2
        vals = [h * (2 * t**3 - 3 * t**2) - E0 for t in (F(k, 8) for k in range(17))]
        g.check(min(vals) > -1, "g > -1 on K")
        g.check(4 * h - end_err > 0, "g(2Y - M) > 0")
g.check(cnt > 1000, "coverage")
g.close()

# =====================================================================
# L4  fixed-Lambda ledgers: rejected (C97 with LE) and elder (C94 (C16)),
#     w = r^(-1/12), d = r^(2/3 - eps), p = ceil(2/(3 eps))
# =====================================================================
g = Group("L4 fixed-Lambda ledgers: exponent 2/3 - eps")
for eps in (F(1, 30), F(1, 100), F(1, 1000)):
    om = F(1, 12)
    e = 1 - 4 * om
    d = F(2, 3) - eps
    p = -(-F(2, 3) // eps)          # ceiling
    rej = [8 * om, 1 + 4 * om, d, F(1), p * (e - d), 1 - 2 * om, F(3, 2) - om]
    eld = [8 * om, 1 + 4 * om, e, 1 + e / 2, d, F(1), p * (e - d), 2 - 4 * om]
    g.check(min(rej) == F(2, 3) - eps, "rejected ledger")
    g.check(min(eld) == F(2, 3) - eps, "elder ledger")
    g.check(1 - om > 0 and e > 0 and d > 0, "cutoffs vanish")
g.close()

# =====================================================================
# L5  growing-Lambda ledger (C101 with LE): every beta < 2/3
#     omega = beta/8, alpha = (2 - 3 beta)/16, delta = beta,
#     p >= (beta + 3 alpha)/(1 - 3 beta/2), m >= beta/alpha.
# =====================================================================
g = Group("L5 growing-Lambda ledger: every beta < 2/3")
for beta in (F(1, 4), F(1, 2), F(3, 5), F(13, 20), F(2, 3) - F(1, 100), F(2, 3) - F(1, 1000)):
    om = beta / 16 if MUT == "OMEGA_HALF" else beta / 8
    al = (2 - 3 * beta) / 16
    de = beta
    e = 1 - 4 * om
    p = 2 if MUT == "P_TWO" else int(-(-(beta + 3 * al) // (1 - 3 * beta / 2))) + 1
    m = int(-(-beta // al)) + 1
    terms = {
        "w^-8": 8 * om,
        "rH^3w^-4": 1 - 3 * al + 4 * om,
        "H^4e": e - 4 * al,
        "rH^5sqrt(e)": 1 - 5 * al + e / 2,
        "H^3rw^2 (LE endpoint)": 1 - 3 * al - 2 * om,
        "rH^4(rw^2)^(1/2) (LE endpoint)": 1 - 4 * al + (1 - 2 * om) / 2,
        "d": de,
        "rH^4": 1 - 4 * al,
        "H^3(e/d)^p": p * (e - de) - 3 * al,
        "H^5r^2w^4": 2 - 5 * al - 4 * om,
        "H^7r^2w^2": 2 - 7 * al - 2 * om,
        "Lambda^-m": m * al,
        "far/derivative": F(1),
    }
    if MUT == "OLD_ENDPOINT":
        terms["H^4e^(2/3)"] = F(2, 3) * e - 4 * al
        terms["rH^5e^(1/3)"] = 1 - 5 * al + e / 3
    g.check(min(terms.values()) >= beta, "all exponents >= beta at beta=%s" % beta)
    adm = [1 - al, 1 - om, e, e - 2 * al, 1 - 2 * om, de]
    g.check(all(x > 0 for x in adm), "admissibility exponents positive")
# the Example: beta = 3/5 needs exactly p = 7 and m = 48 at the minimum
b5, a5 = F(3, 5), F(1, 80)
g.check((2 - 3 * b5) / 16 == a5, "alpha(3/5) = 1/80")
for pp_, ok in ((F(51, 8) - F(1, 1000), False), (F(51, 8), True), (6, False), (7, True)):
    g.check((pp_ * (1 - 3 * b5 / 2) - 3 * a5 >= b5) == ok, "least real p = 51/8; least integer p = 7")
for mm_, ok in ((47, False), (48, True)):
    g.check((mm_ * a5 >= b5) == ok, "minimal m = 48")
# the Remark's illustration: a radius tail w^-12 (hypothetical) would allow every beta < 3/4
for beta in (F(2, 3), F(7, 10), F(3, 4) - F(1, 100), F(3, 4) - F(1, 1000)):
    om = beta / 12
    e = 1 - 4 * om
    al = (1 - 4 * beta / 3) / 8
    de = beta
    p = int(-(-(beta + 3 * al) // (e - de))) + 1
    m = int(-(-beta // al)) + 1
    terms = [12 * om, 1 - 3 * al + 4 * om, e - 4 * al, 1 - 5 * al + e / 2, 1 - 3 * al - 2 * om,
             1 - 4 * al + (1 - 2 * om) / 2, de, 1 - 4 * al, p * (e - de) - 3 * al,
             2 - 5 * al - 4 * om, 2 - 7 * al - 2 * om, m * al, F(1)]
    g.check(min(terms) >= beta, "w^-12 tail: all exponents >= beta at beta=%s" % beta)
g.close()

# ---------------------------------------------------------------------
total = sum(t for _, _, t in RESULTS)
passed = sum(p for _, p, _ in RESULTS)
for name, p, t in RESULTS:
    print("%-58s %5d/%-5d %s" % (name, p, t, "PASS" if p == t else "FAIL"))
print("mutant: %s" % (MUT if MUT else "none"))
print("total checks: %d; failures: %d" % (total, total - passed))
for f in FAILS:
    print("  FAIL " + f)
sys.exit(0 if passed == total else 1)
```

```text
L0 raw cubic: G = P o chart; pins at raw M and raw S           7/7     PASS
L1 LE margin: 4h >= 2 min(1, a_M/(g^2+72))|v|^2            57005/57005 PASS
L2 LE Taylor identity with exact pins                       1250/1250  PASS
L3 Good_LE scalar margin bookkeeping                        3309/3309  PASS
L4 fixed-Lambda ledgers: exponent 2/3 - eps                    9/9     PASS
L5 growing-Lambda ledger: every beta < 2/3                    23/23    PASS
mutant: none
total checks: 61603; failures: 0
```

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
_Generated by [Claude Code](https://claude.ai/code)_