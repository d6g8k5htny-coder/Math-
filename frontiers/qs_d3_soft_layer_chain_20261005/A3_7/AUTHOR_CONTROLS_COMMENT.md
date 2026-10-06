## QS addendum A3.7: author controls, exact executable and stdout

This publishes the standard-library control script that A3.7 ([6004622009](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6004622009)) cites, so anyone can replay it. It checks finite algebra, constants, coverings, elementary integrals and exponent ledgers only; it does not prove the analytic statements.

Dylan Roy — delegated AI work. Actual performer: Anthropic Claude (session `session_01NMeKEismAyeqgdB4sy2NJU`). Scientific effect: NONE.

**Extraction rule.** The same as in [5971055189](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5971055189): the file is the exact text between the first ```` ```python ```` fence after its `###` heading and the next ```` ``` ```` line, plus a final newline. The expected stdout is the single JSON line in the following ```` ```json ```` fence, plus one newline.

**Run.** Each full run takes about 3 s.
- `python3 -B -S a37_exact.py`: exit 0, with exactly the stdout below.
- `python3 -B -O -S a37_exact.py`: byte-identical output. No check depends on an `assert`.
- `--mutant M1` … `M17`: each exits 1 in both modes and names its failing group on stderr (identical stderr in both modes):
  - `M1` (LB3': whole-layer constant 4608 Lambda^3 in place of 9216 Lambda^3 (the case x > 1/2)): exits 1; stderr names `Y1_LB3prime`.
  - `M2` (MB3(a): Markov factor 2^-j N (order 1) in place of 4^-j N^2 (a valid covering whose series diverges)): exits 1; stderr names `Y2_MB3`.
  - `M3` (MB3(b): shells 2^j delta < lam2|mu| <= 2^(j+1) delta with the factor 16^-j N^4): exits 1; stderr names `Y2_MB3`.
  - `M4` (LE3(ii): margin with gamma^2 + 36 in place of gamma^2 + 72): exits 1; stderr names `Y3_LE3_margin`.
  - `M5` (LE3(ii): witness margin a_M/(gamma^2 + 72) (C97's normalization) in place of 4 a_M/(gamma^2 + 72)): exits 1; stderr names `Y3_LE3_margin`.
  - `M6` (LE3(i): pinned field without the y-linear correction c0 = -c2 r^2/4 (gradient pin broken)): exits 1; stderr names `Y4_LE3_taylor`.
  - `M7` (B3: gamma^2 + 72 <= 73 P in place of 73 P^2): exits 1; stderr names `Y5_B3`.
  - `M8` (Corollary LE3: far-end chord value 2h in place of 4h): exits 1; stderr names `Y6_corLE3`.
  - `M9` (ledgers: w = r^(-1/16) in place of r^(-1/12)): exits 1; stderr names `Y7_ledgers`.
  - `M10` (R3' ledger with A3.6's endpoint terms e^(2/3) + r e^(1/3) in place of eta_LE + r eta_LE^(1/2)): exits 1; stderr names `Y7_ledgers`.
  - `M11` (rider: step-5 total eps_V in place of (3/2) eps_V): exits 1; stderr names `Y8_A36_riders`.
  - `M12` (rider: step-6 total (5/24) eps'_V in place of (29/24) eps'_V): exits 1; stderr names `Y8_A36_riders`.
  - `M13` (rider: R3(b) total eps_h^(2/3) in place of (5/4) eps_h^(2/3)): exits 1; stderr names `Y8_A36_riders`.
  - `M14` (rider: eps'_V = 2 C_e k_+ e/c_* in place of 4 C_e k_+ e/c_*): exits 1; stderr names `Y8_A36_riders`.
  - `M15` (rider: delta_B = C_B k_- e in place of C_B k_+ e): exits 1; stderr names `Y8_A36_riders`.
  - `M16` (rider: delta_4 = C_e k_+ e/rho in place of 2 C_e k_+ e/rho): exits 1; stderr names `Y8_A36_riders`.
  - `M17` (rider: eps_h = K0 e/(4 c_h) in place of K0 e/(2 c_h)): exits 1; stderr names `Y8_A36_riders`.
- `--bogus`, `--mutant M18` and a bare `--mutant`: exit 2.

The output was produced with Python 3.11.15. The script uses only `json`, `random`, `sys`, `fractions` and `math`.

### a37_exact.py

- **File:** 23110 bytes, SHA-256 `0663bb8f6e7cc540a9f4cb82b3b22bcf2c880c000676e61f61ef52a8b771af24`.
- **Stdout:** 316 bytes, SHA-256 `02f5616de08d8b61a581c8661b82ce09551067df6f2e0d9be1940f3e67850c2c`.

```python
"""QS addendum A3.7: author controls (exact rational arithmetic, standard library only).

Finite algebra behind A3.7 (C124's correlated band and A4's endpoint margin in d = 3).
It checks identities, constants, coverings, elementary integrals and exponent ledgers.
It does not prove the Gaussian estimates of A3.4/A3.5, C82's Theorem LB, C91's window
bound (FW.0), or any topology.

Usage:
  python3 -B -S a37_exact.py                 exit 0, one JSON line on stdout
  python3 -B -S a37_exact.py --mutant Mj     j = 1..17: exit 1, the failing control named on stderr
  any other argument                         exit 2
"""
import json
import random
import sys
from fractions import Fraction as F
from math import isqrt

MUTANTS = {
    "M1": "LB3': whole-layer constant 4608 Lambda^3 in place of 9216 Lambda^3 (the case x > 1/2)",
    "M2": "MB3(a): Markov factor 2^-j N (order 1) in place of 4^-j N^2 (a valid covering whose series diverges)",
    "M3": "MB3(b): shells 2^j delta < lam2|mu| <= 2^(j+1) delta with the factor 16^-j N^4",
    "M4": "LE3(ii): margin with gamma^2 + 36 in place of gamma^2 + 72",
    "M5": "LE3(ii): witness margin a_M/(gamma^2 + 72) (C97's normalization) in place of 4 a_M/(gamma^2 + 72)",
    "M6": "LE3(i): pinned field without the y-linear correction c0 = -c2 r^2/4 (gradient pin broken)",
    "M7": "B3: gamma^2 + 72 <= 73 P in place of 73 P^2",
    "M8": "Corollary LE3: far-end chord value 2h in place of 4h",
    "M9": "ledgers: w = r^(-1/16) in place of r^(-1/12)",
    "M10": "R3' ledger with A3.6's endpoint terms e^(2/3) + r e^(1/3) in place of eta_LE + r eta_LE^(1/2)",
    "M11": "rider: step-5 total eps_V in place of (3/2) eps_V",
    "M12": "rider: step-6 total (5/24) eps'_V in place of (29/24) eps'_V",
    "M13": "rider: R3(b) total eps_h^(2/3) in place of (5/4) eps_h^(2/3)",
    "M14": "rider: eps'_V = 2 C_e k_+ e/c_* in place of 4 C_e k_+ e/c_*",
    "M15": "rider: delta_B = C_B k_- e in place of C_B k_+ e",
    "M16": "rider: delta_4 = C_e k_+ e/rho in place of 2 C_e k_+ e/rho",
    "M17": "rider: eps_h = K0 e/(4 c_h) in place of K0 e/(2 c_h)",
}


def usage_exit():
    sys.stderr.write("usage: a37_exact.py [--mutant M1..M17]\n")
    sys.exit(2)


MUT = None
if len(sys.argv) == 1:
    pass
elif len(sys.argv) == 3 and sys.argv[1] == "--mutant" and sys.argv[2] in MUTANTS:
    MUT = sys.argv[2]
else:
    usage_exit()

RNG = random.Random(2026100537)
GROUPS = []
FAILED = []


class Group:
    def __init__(self, name):
        self.name, self.n, self.bad = name, 0, 0
        GROUPS.append(self)

    def check(self, ok):
        self.n += 1
        if not ok:
            self.bad += 1
            if self.name not in FAILED:
                FAILED.append(self.name)


def rq(lo, hi, den=89):
    """A random rational in [lo, hi] (endpoints rounded toward zero at the given denominator)."""
    a, b = int(F(lo) * den), int(F(hi) * den)
    return F(RNG.randint(a, b), den)


def rq_nz(lo, hi, den=89):
    while True:
        x = rq(lo, hi, den)
        if x != 0:
            return x


def simpson(f, a, b):
    """Simpson's rule: exact for polynomials of degree <= 3."""
    return (b - a) / 6 * (f(a) + 4 * f((a + b) / 2) + f(b))


# --------------------------------------------------------------------------- the model (A3.6 section 0)
def cubic_params(lam, gam, B, C3, k):
    D = gam ** 2 - 12 * k * B
    J = 8 * gam ** 3 - 144 * k * B * gam + 576 * k * k * C3
    return D, J, 24 * lam / gam ** 2, D / gam ** 2, J / gam ** 3


def PQS(psi, c, R, u, Z):
    return 2 * u ** 3 - F(3, 2) * u - F(1, 2) - (psi + 2 * c * u) * Z ** 2 / 48 + R * Z ** 3 / 3456


def gradPQS(psi, c, R, u, Z):
    return (6 * u * u - F(3, 2) - c * Z * Z / 24, -(psi + 2 * c * u) * Z / 24 + R * Z * Z / 1152)


def hessdet(psi, c, R, u, Z):
    puu, puz, pzz = 12 * u, -c * Z / 12, -(psi + 2 * c * u) / 24 + R * Z / 576
    return puu * pzz - puz * puz


def Gk_poly(lam, gam, B, C3, k):
    """#243 (0.2) as a polynomial {(i, j): coeff} in (X, zeta)."""
    return {(3, 0): F(2), (1, 0): F(-3, 2), (0, 0): F(-1, 2), (2, 1): gam / 2, (0, 1): -gam / 8,
            (0, 2): -lam / 2, (1, 2): k * B / 2, (0, 3): k * k * C3 / 6}


def pev(p, x, y):
    return sum(v * x ** i * y ** j for (i, j), v in p.items())


def pdiff(p, dx, dy):
    out = {}
    for (i, j), v in p.items():
        if i < dx or j < dy:
            continue
        f = v
        for t in range(dx):
            f *= i - t
        for t in range(dy):
            f *= j - t
        key = (i - dx, j - dy)
        out[key] = out.get(key, 0) + f
    return out


def padd(p, q, s=1):
    out = dict(p)
    for kk, v in q.items():
        out[kk] = out.get(kk, 0) + s * v
    return out


# =========================================================================== Y1 LB3'
g = Group("Y1_LB3prime")
lam_const = 4608 if MUT == "M1" else 9216
for _ in range(1500):
    Lam = rq(F(1, 10), 6)
    gam = rq_nz(-3, 3)
    R = rq_nz(-60, 60)
    x = rq(F(1, 89), 3)
    psiL = 24 * Lam / gam ** 2
    # c = 0: the only extra saddle is sigma = 1, Z = 48 psi/R, mu = 1 - 16 psi^3/R^2 (C82 (4))
    lo3 = max(F(0), (1 - x) * R * R / 16)
    hi3 = min((1 + x) * R * R / 16, psiL ** 3)
    band = (hi3 - lo3) / 3 if hi3 > lo3 else F(0)          # int psi^2 dpsi over the truncated band
    # the bound x*Ł in gamma^6-free form: x [64 R^2 + (2/3) psi_L^3]; 9216 Lambda^3 = (2/3) gamma^6 psi_L^3
    g.check(band <= x * (64 * R * R + F(2, 3) * psiL ** 3))
    g.check(gam ** 6 * F(2, 3) * psiL ** 3 == 9216 * Lam ** 3)
    # the case x > 1/2: the whole layer (gamma^6/384) psi_L^3/3 = 12 Lambda^3 is at most x * (whole-layer constant)/384 * Lambda^3
    xx = F(1, 2) + rq(F(1, 89), F(1, 2))
    g.check(gam ** 6 / 384 * psiL ** 3 / 3 == 12 * Lam ** 3 <= xx * F(lam_const, 384) * Lam ** 3)
    if x <= 1 and psiL ** 3 >= (1 + x) * R * R / 16:
        g.check(band == x * R * R / 24)                      # C82 (4), untruncated
for _ in range(300):
    psi = rq(F(1, 10), 5)
    R = rq_nz(-9, 9)
    Z = 48 * psi / R
    g.check(gradPQS(psi, F(0), R, F(-1, 2), Z) == (0, 0) and hessdet(psi, F(0), R, F(-1, 2), Z) < 0)
    g.check(PQS(psi, F(0), R, F(-1, 2), Z) + 1 == 1 - 16 * psi ** 3 / R ** 2)
for _ in range(300):
    Lam, gam, k = rq(F(1, 10), 6), rq_nz(-3, 3), rq(F(1, 4), 3)
    lam, B, C3 = rq(F(1, 89), Lam), rq(-3, 3), rq(-3, 3)
    D, J, psi, c, R = cubic_params(lam, gam, B, C3, k)
    Y = 3 * k * B - gam * gam / 4
    # Jacobian (A3.6 (1.1)): w_lambda = a_M a_S = (gamma^4/16)(psi^2 - c^2), d lambda = (gamma^2/24) d psi
    g.check((6 * lam + Y) * (6 * lam - Y) == gam ** 4 / 16 * (psi * psi - c * c))
    g.check((6 * lam + Y) * (6 * lam - Y) <= 36 * lam * lam)
    # pole cancellation in Ł
    g.check(gam ** 6 / 384 * (F(1024, 3) * abs(c) ** 3 + 64 * R * R) == (F(1024, 3) * abs(D) ** 3 + 64 * J * J) / 384)
    # the whole layer: (gamma^6/384) psi_L^3/3 = 12 Lambda^3 = int_0^Lambda 36 l^2 dl; and 12 L^3 < 24 L^3 x for x > 1/2
    psiL = 24 * Lam / gam ** 2
    g.check(gam ** 6 / 384 * psiL ** 3 / 3 == 12 * Lam ** 3 == simpson(lambda l: 36 * l * l, F(0), Lam))
    g.check(F(2, 3) * (24 * Lam) ** 3 / 384 == 24 * Lam ** 3)
    # the c != 0 fibre: int_{|c|}^{psi_L} (psi^2 - c^2) dpsi <= psi_L^3/3 < (2/3) x psi_L^3 for x > 1/2
    whole = (psiL ** 3 - abs(c) ** 3) / 3 - c * c * (psiL - abs(c)) if psiL > abs(c) else F(0)
    xx = F(1, 2) + rq(F(1, 89), F(1, 2))
    g.check(0 <= whole <= psiL ** 3 / 3 < F(2, 3) * xx * psiL ** 3)
# C82's own density bound (14)/(17) at exact rational saddles with c != 0 and |v| <= 1/2 (consistency only; imported)
cnt = 0
while cnt < 300:
    sg = F(RNG.randint(-99, 299), 100)
    Zs = rq_nz(-4, 4, den=97)
    if sg * sg == 1:
        continue
    c = 36 * (sg * sg - 1) / (Zs * Zs)
    psi = abs(c) + rq(F(1, 37), 11)
    R = 48 * (psi - c * sg) / Zs
    if not (c - sg * psi < 0):
        continue
    v = PQS(psi, c, R, -sg / 2, Zs) + 1
    if abs(v) > F(1, 2):
        continue
    g.check(48 * (psi * psi - c * c) / (Zs * Zs) <= F(256, 3) * abs(c) ** 3 + 16 * R * R)
    cnt += 1

# =========================================================================== Y2 MB3
g = Group("Y2_MB3")
for _ in range(3000):
    dl = rq(F(1, 89), 2)
    N = rq(1, 60)
    mu = rq_nz(-40, 40)
    lam2 = rq(F(1, 89), 5)
    # (2.3): 1{|mu| <= dl N} <= 1{|mu| <= dl} + sum_j 4^-j N^2 1{|mu| <= 2^(j+1) dl}
    lhs = 1 if abs(mu) <= dl * N else 0
    rhs = F(1 if abs(mu) <= dl else 0)
    j = 0
    while 2 ** j * dl < abs(mu) * 2 and j < 60:
        fac = N / F(2 ** j) if MUT == "M2" else N * N / F(4 ** j)
        rhs += fac * (1 if abs(mu) <= 2 ** (j + 1) * dl else 0)
        j += 1
    g.check(lhs <= rhs)
    if lhs and abs(mu) > dl:
        jj = 0
        while not (2 ** jj * dl < abs(mu) <= 2 ** (jj + 1) * dl):
            jj += 1
        g.check(N > 2 ** jj)
    # (2.4): 1{lam2|mu| <= dl N^2} <= 1{lam2|mu| <= dl} + sum_j 16^-j N^4 1{lam2|mu| <= 4^(j+1) dl}
    q = lam2 * abs(mu)
    lhs = 1 if q <= dl * N * N else 0
    rhs = F(1 if q <= dl else 0)
    base = 2 if MUT == "M3" else 4
    j = 0
    while base ** j * dl < q * base and j < 60:
        rhs += N ** 4 / F(16 ** j) * (1 if base ** j * dl < q <= base ** (j + 1) * dl else 0)
        j += 1
    g.check(lhs <= rhs)
# the series and the totals of MB3
for n in range(0, 40):
    s1 = sum(F(2 ** (jj + 1), 4 ** jj) for jj in range(n + 1))
    s2 = sum(F(1, 4 ** jj) for jj in range(n + 1))
    s3 = sum(F(4 ** (jj + 1), 16 ** jj) for jj in range(n + 1))
    s4 = sum(F(1, 16 ** jj) for jj in range(n + 1))
    p1 = sum(F(1, 2 ** jj) * 2 ** (jj + 1) for jj in range(n + 1)) if MUT == "M2" else s1
    g.check(p1 <= 4 and s2 <= F(4, 3))                                  # bounded partial sums: what MB3 uses
    g.check(p1 == 4 - F(4, 2 ** (n + 1)) and s2 == F(4, 3) - F(4, 3) / 4 ** (n + 1))
    g.check(s3 == F(16, 3) - F(16, 3) / 4 ** (n + 1) and s4 == F(16, 15) - F(16, 15) / 16 ** (n + 1))
g.check(1 + F(4) == 5 and 1 + F(4, 3) == F(7, 3) and 1 + F(16, 3) == F(19, 3) and 1 + F(16, 15) == F(31, 15))

# =========================================================================== Y3 LE3(ii)
g = Group("Y3_LE3_margin")
ext = 36 if MUT == "M4" else 72


def ell_of(aM, gam):
    return min(F(1), 4 * aM / (gam * gam + ext))


for _ in range(4000):
    gam, aM = rq_nz(-6, 6), rq(F(1, 89), 40)
    a, z = rq(-3, 3), rq(-6, 6)
    ell = ell_of(aM, gam)
    kap = aM / (12 * gam * gam)
    h = (3 * a * a + kap * z * z) / 3
    v1, v2 = a - z / 12, z / gam
    form = 4 * h - 2 * ell * (v1 * v1 + v2 * v2)
    m11, m12, m22 = 4 - 2 * ell, ell / 6, aM / (9 * gam * gam) - ell / 72 - 2 * ell / (gam * gam)
    g.check(form == m11 * a * a + 2 * m12 * a * z + m22 * z * z)
    g.check(form >= 0 and m11 >= 2)
    det = m11 * m22 - m12 * m12
    if 4 * aM <= gam * gam + 72:
        g.check(m22 == ell / 72 and det == ell * (1 - ell) / 18)
    else:
        g.check(det == (4 * aM - gam * gam - 72) / (18 * gam * gam) and det > 0)
# exact rational extra saddles (sigma in (-1, 3), Z != 0; c from the conic, R from the line): 4h >= 2 ell |v|^2
cnt = 0
while cnt < 800:
    sg = F(RNG.randint(-99, 299), 100)
    Zs = rq_nz(-4, 4, den=97)
    if sg * sg == 1:
        continue
    c = 36 * (sg * sg - 1) / (Zs * Zs)
    psi = abs(c) + rq(F(1, 37), 11)
    R = 48 * (psi - c * sg) / Zs
    if not (c - sg * psi < 0):
        continue
    u = -sg / 2
    g.check(gradPQS(psi, c, R, u, Zs) == (0, 0) and hessdet(psi, c, R, u, Zs) < 0)
    h = -PQS(psi, c, R, u, Zs)
    gam = rq_nz(-4, 4)
    aM = gam * gam * (psi - c) / 4
    a, z = u + F(1, 2), Zs
    g.check(h == (3 * a * a + aM / (12 * gam * gam) * z * z) / 3)          # C97 (R7), d = 3 normalization
    v1, v2 = a - z / 12, z / gam
    g.check(4 * h >= 2 * ell_of(aM, gam) * (v1 * v1 + v2 * v2))
    cnt += 1
# A4's witness: gamma = 1, psi = 86, c = 13, R = 3400; a_M = 73/4, 4 a_M = gamma^2 + 72
psi, c, R, gam = F(86), F(13), F(3400), F(1)
A = (R * R - 64 * c ** 3) / 2304
disc = c * c * (R * R + 64 * c * (psi * psi - c * c)) / 576
g.check(disc == (psi * R / 24) ** 2 - 4 * A * (psi * psi - c * c))   # C82 (7) is the discriminant of (6)
sq = F(isqrt(disc.numerator), isqrt(disc.denominator))
g.check(sq * sq == disc)
roots = [((psi * R / 24) + s * sq) / (2 * A) for s in (1, -1)]
kinds = []
for Z in roots:
    sg = (psi - R * Z / 48) / c
    u = -sg / 2
    g.check(gradPQS(psi, c, R, u, Z) == (0, 0))
    kinds.append((hessdet(psi, c, R, u, Z) < 0, u, Z))
sad = [kk for kk in kinds if kk[0]]
g.check(len(sad) == 1 and (sad[0][1], sad[0][2]) == (F(-7, 12), F(1)))
u, Z = F(-7, 12), F(1)
h = -PQS(psi, c, R, u, Z)
aM = gam * gam * (psi - c) / 4
v1, v2 = (u - Z / 12) - F(-1, 2), Z / gam
ellw = min(F(1), aM / (gam * gam + 72)) if MUT == "M5" else ell_of(aM, gam)
g.check(aM == F(73, 4) and 4 * aM == gam * gam + 72 and h == F(37, 72))
g.check(4 * h == 2 * ellw * (v1 * v1 + v2 * v2) == F(37, 18))

# =========================================================================== Y4 LE3(i)
g = Group("Y4_LE3_taylor")
for _ in range(300):
    lam, gam, B, C3, k = rq(-2, 4), rq_nz(-3, 3), rq(-3, 3), rq(-3, 3), rq(F(1, 4), 3)
    G = Gk_poly(lam, gam, B, C3, k)
    g.check(pev(G, F(-1, 2), F(0)) == 0 and pev(pdiff(G, 1, 0), F(-1, 2), F(0)) == 0
            and pev(pdiff(G, 0, 1), F(-1, 2), F(0)) == 0)
    g.check(pev(G, F(1, 2), F(0)) == -1 and pev(pdiff(G, 1, 0), F(1, 2), F(0)) == 0
            and pev(pdiff(G, 0, 1), F(1, 2), F(0)) == 0)
for _ in range(200):
    k, r = rq(F(1, 4), 3), F(1, RNG.randint(5, 400))
    lamt, gam, B, C3 = rq(-2, 4), rq_nz(-3, 3), rq(-3, 3), rq(-3, 3)
    b = rq(-2, 2)
    a4 = rq(-3, 3)
    # the planar section p(x, y) = f(x u + y e1), exactly pinned at (-+r/2, 0): value b, b - k r^3, zero gradient
    p = {(0, 0): b - k * r ** 3 / 2 + a4 * r ** 4 / 16, (1, 0): -F(3, 2) * k * r * r, (2, 0): -a4 * r * r / 2,
         (3, 0): 2 * k, (4, 0): a4}
    c3, c2 = rq(-3, 3), gam / 2
    p[(3, 1)], p[(2, 1)], p[(1, 1)] = c3, c2, -c3 * r * r / 4
    p[(0, 1)] = F(0) if MUT == "M6" else -c2 * r * r / 4
    p[(0, 2)], p[(1, 2)], p[(0, 3)] = -r * lamt / k / 2, B / 2, C3 / 6
    for mono in ((2, 2), (1, 3), (0, 4)):
        p[mono] = rq(-3, 3)
    g.check(pev(p, -r / 2, F(0)) == b and pev(p, r / 2, F(0)) == b - k * r ** 3)
    g.check(pev(pdiff(p, 1, 0), r / 2, F(0)) == 0 and pev(pdiff(p, 0, 1), r / 2, F(0)) == 0)
    # the jets at 0 are the model's: gamma = p_xxy, B = p_xyy, C3 = p_yyy, lamt = -k p_yy/r
    g.check(pev(pdiff(p, 2, 1), F(0), F(0)) == gam and pev(pdiff(p, 1, 2), F(0), F(0)) == B
            and pev(pdiff(p, 0, 3), F(0), F(0)) == C3 and -k * pev(pdiff(p, 0, 2), F(0), F(0)) / r == lamt)
    # the chart: frak(X, zeta) = (p(rX, rk zeta) - b)/(k r^3), as a polynomial in (X, zeta)
    fr = {}
    for (i, j), v in p.items():
        key = (i, j)
        fr[key] = fr.get(key, 0) + v * r ** i * (r * k) ** j / (k * r ** 3)
    fr[(0, 0)] = fr.get((0, 0), 0) - b / (k * r ** 3)
    E = padd(fr, Gk_poly(lamt, gam, B, C3, k), -1)
    M = (F(-1, 2), F(0))
    g.check(pev(E, *M) == 0 and pev(pdiff(E, 1, 0), *M) == 0 and pev(pdiff(E, 0, 1), *M) == 0)
    # the integral Taylor identity along [raw M, xi]: E(xi) = int_0^1 (1 - s) h^T D^2E(M + s h) h ds (Simpson: exact)
    Exx, Exz, Ezz = pdiff(E, 2, 0), pdiff(E, 1, 1), pdiff(E, 0, 2)
    for _ in range(3):
        xi = (rq(-3, 3), rq(-3, 3))
        hx, hz = xi[0] - M[0], xi[1] - M[1]

        def integrand(s):
            X, Zz = M[0] + s * hx, M[1] + s * hz
            return (1 - s) * (pev(Exx, X, Zz) * hx * hx + 2 * pev(Exz, X, Zz) * hx * hz + pev(Ezz, X, Zz) * hz * hz)
        g.check(pev(E, *xi) == simpson(integrand, F(0), F(1)))

# =========================================================================== Y5 B3
g = Group("Y5_B3")
for _ in range(3000):
    eta, N = rq(F(1, 10 ** 4), 1, den=10 ** 6), rq(1, 30)
    gam = rq(-120, 120)
    P = max(F(1), abs(gam)) + rq(0, 3)
    aM = rq(F(1, 10 ** 4), 30, den=10 ** 6)
    if RNG.random() < 0.3:
        aM = eta * N * (gam * gam + 72) / 4                   # on the boundary of the event
    if eta * N * (gam * gam + 72) >= 4 * aM:
        # a_M <= sqrt(eta), or N (gamma^2 + 72) > 4 eta^(-1/2), in squared form
        g.check(aM * aM <= eta or N * N * (gam * gam + 72) ** 2 * eta > 16)
    bound = 73 * P if MUT == "M7" else 73 * P * P
    g.check(gam * gam + 72 <= bound)
    if N * N * (gam * gam + 72) ** 2 * eta > 16:
        g.check(1 < eta / 16 * N * N * (gam * gam + 72) ** 2 <= bound ** 2 * eta / 16 * N * N)
    if eta * N >= 1:
        g.check(1 <= eta * eta * N * N)
for _ in range(300):
    s_, r = rq(F(1, 89), 1), rq(0, 1)
    eta = s_ * s_
    g.check(simpson(lambda s: s + r, F(0), s_) == eta / 2 + r * s_)

# =========================================================================== Y6 Corollary LE3
g = Group("Y6_corLE3")
for _ in range(3000):
    eta, N = rq(F(1, 10 ** 4), 1, den=10 ** 6), rq(1, 30)
    gam, aM = rq_nz(-12, 12), rq(F(1, 10 ** 4), 30, den=10 ** 6)
    ell = min(F(1), 4 * aM / (gam * gam + 72))
    if eta * N * (gam * gam + 72) < 4 * aM and eta * N < 1:
        g.check(eta * N < ell)
    mu = rq(F(1, 89), F(88, 89))
    hY = 1 - mu
    e0 = rq(-1, 1) * mu / 2 * F(88, 89)                       # |e0| < mu/2
    g.check(-hY + e0 > -1)                                    # along K: P_QS >= -h_Y = mu - 1
    vsq = rq(F(1, 89), 9)
    if eta * N < ell and 4 * hY >= 2 * ell * vsq:
        g.check(4 * hY - 2 * eta * N * vsq > 0)               # the endpoint (LE3 (iii))
far = 2 if MUT == "M8" else 4
cnt = 0
while cnt < 300:
    sg = F(RNG.randint(-99, 299), 100)
    Zs = rq_nz(-4, 4, den=97)
    if sg * sg == 1:
        continue
    c = 36 * (sg * sg - 1) / (Zs * Zs)
    psi = abs(c) + rq(F(1, 37), 11)
    R = 48 * (psi - c * sg) / Zs
    if not (c - sg * psi < 0):
        continue
    Yq, M = (-sg / 2, Zs), (F(-1, 2), F(0))
    hq = -PQS(psi, c, R, *Yq)
    # C97 (R8) behind the range sigma in (-1, 3): h - (sigma - 1)^2/4 = (psi - c) Z^2/144 > 0 (A3.6 S1-O1)
    g.check(hq - (sg - 1) ** 2 / 4 == (psi - c) * Zs * Zs / 144 > 0)
    if not 0 < hq < 1:
        continue
    g.check((sg - 1) ** 2 < 4 * hq < 4 and -1 < sg < 3)
    for jj in range(9):
        t_ = F(jj, 4)
        pt = (M[0] + t_ * (Yq[0] - M[0]), M[1] + t_ * (Yq[1] - M[1]))
        g.check(PQS(psi, c, R, *pt) == hq * (2 * t_ ** 3 - 3 * t_ * t_) >= -hq)
    g.check(PQS(psi, c, R, 2 * Yq[0] - M[0], 2 * Yq[1] - M[1]) == far * hq)
    cnt += 1

# =========================================================================== Y7 ledgers
g = Group("Y7_ledgers")
om = F(1, 16) if MUT == "M9" else F(1, 12)


def elder(o):
    e = 1 - 4 * o
    return {"w^-8": 8 * o, "r w^-4": 1 + 4 * o, "e": e, "r e^(1/2)": 1 + e / 2, "r": F(1),
            "e^4": 4 * e, "r e^2": 1 + 2 * e, "r^2 w^4": 2 - 4 * o}


def rejected(o):
    e, eta = 1 - 4 * o, 1 - 2 * o
    d = {"w^-8": 8 * o, "r w^-4": 1 + 4 * o, "e": e, "r": F(1), "eta_LE": eta, "r eta_LE^(1/2)": 1 + eta / 2}
    if MUT == "M10":
        d = {"w^-8": 8 * o, "r w^-4": 1 + 4 * o, "e": e, "r": F(1), "e^(2/3)": 2 * e / 3, "r e^(1/3)": 1 + e / 3}
    return d


E1, R1 = elder(om), rejected(om)
g.check(min(E1.values()) == F(2, 3) and sorted(kk for kk, vv in E1.items() if vv == F(2, 3)) == ["e", "w^-8"])
g.check(min(R1.values()) == F(2, 3) and sorted(kk for kk, vv in R1.items() if vv == F(2, 3)) == ["e", "w^-8"])
g.check([E1[kk] for kk in ("w^-8", "r w^-4", "e", "r e^(1/2)", "r", "e^4", "r e^2", "r^2 w^4")]
        == [F(2, 3), F(4, 3), F(2, 3), F(4, 3), F(1), F(8, 3), F(7, 3), F(5, 3)])
g.check(F(1, 2) - om > 0 and 1 - 2 * om > 0 and om > 0)                  # r^(1/2) w -> 0 and eta_LE -> 0
g.check(F(1, 2) - om == F(5, 12) and 1 - 2 * om == F(5, 6))                 # their values at omega = 1/12
# omega = 1/12 is the unique maximizer of min(8 omega, 1 - 4 omega), and of both ledgers' minima
for n in range(1, 240):
    o = F(n, 960)
    mpair = min(8 * o, 1 - 4 * o)
    g.check(mpair <= F(2, 3) and (mpair == F(2, 3)) == (o == F(1, 12)))
    g.check(min(elder(o).values()) <= F(2, 3) and min(rejected(o).values()) <= F(2, 3))
# regression: A3.6's elder ledger at omega = 1/16 with rho = r^(1/2), p = 2 had minimum 1/2
e16 = F(3, 4)
a36 = [F(1, 2), F(5, 4), e16, 1 + e16 / 2, F(1, 2), F(1), 2 * (e16 - F(1, 2)), 4 * (e16 - F(1, 2)),
       1 + 2 * (e16 - F(1, 2)), 4 * e16, 1 + 2 * e16, F(7, 4)]
g.check(min(a36) == F(1, 2))

# =========================================================================== Y8 A3.6 riders
g = Group("Y8_A36_riders")
c5 = F(1) if MUT == "M11" else F(3, 2)
c6 = F(5, 24) if MUT == "M12" else F(29, 24)
c7 = F(1) if MUT == "M13" else F(5, 4)
for _ in range(300):
    s_, r = rq(F(1, 89), 1), rq(0, 1)
    eps = s_ * s_
    # step 5 (C94 (C9)-(C10)): d1 = sqrt(eps_V)
    g.check(s_ ** 2 + r * s_ + eps ** 2 * (s_ ** -2 / 2 + r * s_ ** -3 / 3) == c5 * eps + F(4, 3) * r * s_)
    # step 6: strip plus away part, (29/24) eps' + (23/18) r sqrt(eps')
    away = F(5, 24) * eps ** 4 * s_ ** -6 + F(5, 18) * r * eps ** 2 * s_ ** -3
    g.check(s_ ** 2 + r * s_ + away == c6 * eps + F(23, 18) * r * s_)
    # R3(b): d2 = eps_h^(1/3)
    t_ = rq(F(1, 89), 1)
    epsh = t_ ** 3
    g.check(t_ ** 2 + r * t_ + epsh ** 2 * (t_ ** -4 / 4 + r * t_ ** -5 / 5) == c7 * t_ ** 2 + F(6, 5) * r * t_)
f14 = 2 if MUT == "M14" else 4
f16 = 1 if MUT == "M16" else 2
f17 = 4 if MUT == "M17" else 2
for _ in range(600):
    K0, Ce, ce, km, kp = rq(F(1, 2), 9), rq(1, 99), rq(F(1, 10 ** 4), F(1, 10), den=10 ** 6), rq(F(1, 4), 1), rq(1, 3)
    k = kp if RNG.random() < 0.5 else km + (kp - km) * rq(0, 1)
    N, e, aS, rho = rq(1, 5), rq(F(1, 10 ** 3), F(1, 10), den=10 ** 6), rq(F(1, 10), 2), rq(F(1, 100), F(1, 4), den=10 ** 4)
    v = ce * aS * aS
    # V2 at its boundary: C_e k N^2 e/lam2 = v/4 must lie in {lam2 a_S^2 <= eps'_V N^2}, eps'_V = 4 C_e k_+ e/c_*
    lam2 = 4 * Ce * k * N * N * e / v
    g.check(lam2 * aS * aS <= f14 * Ce * kp * e / ce * N * N)
    # F_B at its boundary: lam2 = C_B k N^2 e must lie in {lam2 <= delta_B N^2}, delta_B = C_B k_+ e
    CB = rq(16, 400)
    dB = CB * (km if MUT == "M15" else kp) * e
    g.check(CB * k * N * N * e <= dB * N * N)
    # V4 off the band at its boundary: -mu = 2 rho, C_e k N^2 e/lam2 = -mu/4 gives lam2 <= delta_4 N^2
    mneg = 2 * rho
    lam2b = 4 * Ce * k * N * N * e / mneg
    g.check(lam2b <= f16 * Ce * kp * e / rho * N * N)
    # rejected at its boundary: K0 N e = 2 h, h = c_h a_M^3/P^6, must lie in {a_M^3 <= eps_h N P^6}
    chh, aM, Pw = rq(F(1, 10 ** 6), F(1, 100), den=10 ** 8), rq(F(1, 10), 3), rq(1, 4)
    h = chh * aM ** 3 / Pw ** 6
    e2 = 2 * h / (K0 * N)
    g.check(aM ** 3 <= K0 * e2 / (f17 * chh) * N * Pw ** 6)

# --------------------------------------------------------------------------- report
out = {"object": "CL-QS-A3-7-CONTROLS-20261005-v1",
       "groups": {gr.name: [gr.n - gr.bad, gr.n] for gr in GROUPS},
       "total": sum(gr.n for gr in GROUPS),
       "passed": not FAILED}
if FAILED:
    sys.stderr.write("FAILED: %s\n" % ", ".join(FAILED))
    if MUT:
        sys.stderr.write("mutant %s: %s\n" % (MUT, MUTANTS[MUT]))
    sys.exit(1)
sys.stdout.write(json.dumps(out, sort_keys=True) + "\n")
```

```json
{"groups": {"Y1_LB3prime": [7668, 7668], "Y2_MB3": [7775, 7775], "Y3_LE3_margin": [14407, 14407], "Y4_LE3_taylor": [2000, 2000], "Y5_B3": [11921, 11921], "Y6_corLE3": [6864, 6864], "Y7_ledgers": [484, 484], "Y8_A36_riders": [3300, 3300]}, "object": "CL-QS-A3-7-CONTROLS-20261005-v1", "passed": true, "total": 54419}
```

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
_Generated by [Claude Code](https://claude.ai/code)_