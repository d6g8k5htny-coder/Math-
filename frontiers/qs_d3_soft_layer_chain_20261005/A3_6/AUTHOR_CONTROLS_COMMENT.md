## QS addendum A3.6: author controls, exact executable and stdout

This publishes the standard-library control script that A3.6 ([6002480647](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6002480647)) cites, so anyone can replay it. It checks finite algebra, constants, elementary integrals and exponent ledgers only; it does not prove the analytic statements.

Dylan Roy — delegated AI work. Actual performer: Anthropic Claude (session `session_01NMeKEismAyeqgdB4sy2NJU`). Scientific effect: NONE.

**Extraction rule.** The same as in [5971055189](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5971055189): the file is the exact text between the first ```` ```python ```` fence after its `###` heading and the next ```` ``` ```` line, plus a final newline. The expected stdout is the single JSON line in the following ```` ```json ```` fence, plus one newline.

**Run.** Each full run takes about 2 s.
- `python3 -B -S a36_exact.py`: exit 0, with exactly the stdout below.
- `python3 -B -O -S a36_exact.py`: byte-identical output. No check depends on an `assert`.
- `--mutant M1` … `M13`: each exits 1 in both modes and names its failing groups on stderr (identical stderr in both modes):
  - `M1` (J with 576k C3 in place of 576k^2 C3 (chart identity)): exits 1; stderr names `X1_chart`, `X12_witness`, `X16_endpoint_chain`.
  - `M2` (Jacobian gamma^6/96 in place of gamma^6/384): exits 1; stderr names `X2_jacobian`.
  - `M3` (c_* = 3/(250 Lambda^2): A_* replaced by Lambda): exits 1; stderr names `X5_elder_floor`.
  - `M4` (radius constant 25/24 in place of 25/96): exits 1; stderr names `X7_radius`.
  - `M5` (hard-gap integral (1/4) y delta^4 in place of (5/4) y delta^4): exits 1; stderr names `X9_hardgap`.
  - `M6` (C82 exact value J_delta(0,R) = delta R^2/12 in place of /24): exits 1; stderr names `X8_levelband`.
  - `M7` (elder ledger with w = r^(-1/8)): exits 1; stderr names `X11_ledgers`.
  - `M8` (chord height h/2 in place of h): exits 1; stderr names `X13_chord`.
  - `M9` (C_tau with (8 + 288k) in place of (8 + 288k + 1152k^2)): exits 1; stderr names `X6_endpoint_floor`.
  - `M10` (neutral-surface constant 8 in place of 16): exits 1; stderr names `X14_coverage`.
  - `M11` (G3-minus threshold beta > 1/6 in place of beta > 1/8): exits 1; stderr names `X15_G3minus`.
  - `M12` (eps_V = 2 K0 e/c_* in place of 4 K0 e/c_* (step 5 inclusion)): exits 1; stderr names `X17_inclusions`.
  - `M13` (far end of the chord bounded by u >= -3/2 in place of -5/2 (W_R)): exits 1; stderr names `X13_chord`.
- `--bogus`, `--mutant M14` and a bare `--mutant`: exit 2.

The output was produced with Python 3.11.15. The script uses only `json`, `random`, `sys`, `fractions` and `math`.

### a36_exact.py

- **File:** 27547 bytes, SHA-256 `751b215c5d0208e3a649df2807acd599720c2ef6d1c5ff079a0846270af250c8`.
- **Stdout:** 573 bytes, SHA-256 `82bb5a5e9d4f6a38199371c3ac90076d6143349a533f64b32dcd62dab7640623`.

```python
"""QS addendum A3.6: author controls (exact rational arithmetic, standard library only).

Finite algebra behind A3.6 (the d = 3 weighted decision on the bounded soft layer).
It checks identities, constants, elementary integrals and exponent ledgers. It does
not prove the Gaussian estimates of A3.4/A3.5, C82's Theorem LB, or any topology.

Usage:
  python3 -B -S a36_exact.py                 exit 0, one JSON line on stdout
  python3 -B -S a36_exact.py --mutant Mj     j = 1..13: exit 1, the failing control named on stderr
  any other argument                         exit 2
"""
import json
import random
import sys
from fractions import Fraction as F
from math import isqrt

MUTANTS = {
    "M1": "J with 576k C3 in place of 576k^2 C3 (chart identity)",
    "M2": "Jacobian gamma^6/96 in place of gamma^6/384",
    "M3": "c_* = 3/(250 Lambda^2): A_* replaced by Lambda",
    "M4": "radius constant 25/24 in place of 25/96",
    "M5": "hard-gap integral (1/4) y delta^4 in place of (5/4) y delta^4",
    "M6": "C82 exact value J_delta(0,R) = delta R^2/12 in place of /24",
    "M7": "elder ledger with w = r^(-1/8)",
    "M8": "chord height h/2 in place of h",
    "M9": "C_tau with (8 + 288k) in place of (8 + 288k + 1152k^2)",
    "M10": "neutral-surface constant 8 in place of 16",
    "M11": "G3-minus threshold beta > 1/6 in place of beta > 1/8",
    "M12": "eps_V = 2 K0 e/c_* in place of 4 K0 e/c_* (step 5 inclusion)",
    "M13": "far end of the chord bounded by u >= -3/2 in place of -5/2 (W_R)",
}


def usage_exit():
    sys.stderr.write("usage: a36_exact.py [--mutant M1..M13]\n")
    sys.exit(2)


MUT = None
if len(sys.argv) == 1:
    pass
elif len(sys.argv) == 3 and sys.argv[1] == "--mutant" and sys.argv[2] in MUTANTS:
    MUT = sys.argv[2]
else:
    usage_exit()

RNG = random.Random(2026100536)
GROUPS = []
FAILED = []


class Group:
    def __init__(self, name):
        self.name, self.n, self.bad = name, 0, 0
        GROUPS.append(self)

    def check(self, ok, msg=""):
        self.n += 1
        if not ok:
            self.bad += 1
            if self.name not in FAILED:
                FAILED.append(self.name)


def rq(lo, hi, den=89):
    a, b = int(F(lo) * den), int(F(hi) * den)
    return F(RNG.randint(a, b), den)


def rq_nz(lo, hi, den=89):
    while True:
        x = rq(lo, hi, den)
        if x != 0:
            return x


S = 10 ** 40


def sqrt_lo(q):
    q = F(q)
    return F(isqrt(q.numerator * S * S // q.denominator), S)


def sqrt_hi(q):
    q = F(q)
    return F(isqrt(q.numerator * S * S // q.denominator) + 1, S)


def simpson(f, a, b):
    """Simpson's rule: exact for polynomials of degree <= 3 (an independent check of hand antiderivatives)."""
    return (b - a) / 6 * (f(a) + 4 * f((a + b) / 2) + f(b))


def boole(f, a, b):
    """Boole's rule: exact for polynomials of degree <= 5."""
    h = (b - a) / 4
    return 2 * h / 45 * (7 * f(a) + 32 * f(a + h) + 12 * f(a + 2 * h) + 32 * f(a + 3 * h) + 7 * f(b))


# --------------------------------------------------------------------------- the model
def cubic_params(lam, gam, B, C3, k):
    """QS section 7 in A3.4's normalization: D = gamma^2 - 12kB, J = 8g^3 - 144kBg + 576k^2C3."""
    D = gam ** 2 - 12 * k * B
    J = 8 * gam ** 3 - 144 * k * B * gam + (576 * k * C3 if MUT == "M1" else 576 * k * k * C3)
    psi = 24 * lam / gam ** 2
    return D, J, psi, D / gam ** 2, J / gam ** 3


def PQS(psi, c, R, u, Z):
    return 2 * u ** 3 - F(3, 2) * u - F(1, 2) - (psi + 2 * c * u) * Z ** 2 / 48 + R * Z ** 3 / 3456


def gradPQS(psi, c, R, u, Z):
    return (6 * u * u - F(3, 2) - c * Z * Z / 24, -(psi + 2 * c * u) * Z / 24 + R * Z * Z / 1152)


def hessdet(psi, c, R, u, Z):
    puu, puz, pzz = 12 * u, -c * Z / 12, -(psi + 2 * c * u) / 24 + R * Z / 576
    return puu * pzz - puz * puz


def Gk(lam, gam, B, C3, k, X, z):
    """#243 (0.2), as in A3.5 section 0."""
    return (2 * X ** 3 - F(3, 2) * X - F(1, 2) + (gam / 2) * (X * X - F(1, 4)) * z - (lam / 2) * z * z
            + (k * B / 2) * X * z * z + (k * k * C3 / 6) * z ** 3)


A_ = lambda Lam: 12 * Lam            # A_* = 12 Lambda
ASQ = F(4, 27)                       # a^2, a = 2/(3 sqrt 3)


def tau_hat_hi(psi, c, R, kap):
    """Upper bound for QS's tau-hat = a + |c|/(24 sqrt3 kappa) + |R|/(3456 kappa^(3/2))."""
    return (sqrt_hi(ASQ) + abs(c) / (24 * kap) * sqrt_hi(F(1, 3))
            + abs(R) / (3456 * kap * sqrt_lo(kap)))


def tau_hat_lo(psi, c, R, kap):
    return (sqrt_lo(ASQ) + abs(c) / (24 * kap) * sqrt_lo(F(1, 3))
            + abs(R) / (3456 * kap * sqrt_hi(kap)))


# =========================================================================== X1 chart
g = Group("X1_chart")
for _ in range(400):
    k = rq(F(1, 4), 3)
    gam = rq_nz(-3, 3)
    lam, B, C3 = rq(-2, 4), rq(-3, 3), rq(-3, 3)
    D, J, psi, c, R = cubic_params(lam, gam, B, C3, k)
    Y = 3 * k * B - gam * gam / 4
    aM, aS = 6 * lam + Y, 6 * lam - Y
    g.check(D == -4 * Y)
    g.check(aM == gam * gam * (psi - c) / 4 and aS == gam * gam * (psi + c) / 4)
    for _ in range(3):
        u, Z = rq(-3, 3), rq(-3, 3)
        g.check(Gk(lam, gam, B, C3, k, u - Z / 12, Z / gam) == PQS(psi, c, R, u, Z))

# =========================================================================== X2 Jacobian
g = Group("X2_jacobian")
for _ in range(300):
    gam = rq_nz(-3, 3)
    psi, c = rq(0, 9), rq(-4, 4)
    lam = gam * gam * psi / 24
    D = c * gam * gam
    Y = -D / 4
    w = (6 * lam + Y) * (6 * lam - Y)
    jac = gam ** 6 / (96 if MUT == "M2" else 384)
    g.check(w * gam * gam / 24 == jac * (psi * psi - c * c))

# =========================================================================== X3 poles
g = Group("X3_poles")
for _ in range(300):
    k, gam = rq(F(1, 4), 3), rq_nz(-3, 3)
    D, J, psi, c, R = cubic_params(rq(0, 2), gam, rq(-3, 3), rq(-3, 3), k)
    g.check(gam ** 6 * abs(c) ** 3 == abs(D) ** 3 and gam ** 6 * R * R == J * J)

# =========================================================================== X4 raw tau
g = Group("X4_tau_raw")
for _ in range(300):
    k, gam = rq(F(1, 4), 3), rq_nz(-3, 3)
    lam, B, C3 = rq(F(1, 50), 3), rq(-3, 3), rq(-3, 3)
    D, J, psi, c, R = cubic_params(lam, gam, B, C3, k)
    if not psi > abs(c):
        continue
    for a_i, kap in ((gam * gam * (psi - c) / 4, (psi - c) / 48), (gam * gam * (psi + c) / 4, (psi + c) / 48)):
        g.check(kap == a_i / (12 * gam * gam))
        g.check(abs(c) / (24 * kap) == abs(D) / (2 * a_i))                       # times 1/sqrt3 both sides
        g.check(R * R / (3456 ** 2 * kap ** 3) == 3 * J * J / (144 ** 2 * a_i ** 3))  # squares of the R-terms

# =========================================================================== X5 elder floor
g = Group("X5_elder_floor")
# the R-bound on E is the tau_S bound: equality case of R^2 = 16(psi-2c)^2(psi+c)
for _ in range(200):
    psi = rq(F(1, 10), 9)
    c = rq(-psi + F(1, 89), psi / 2)
    R2 = 16 * (psi - 2 * c) ** 2 * (psi + c)
    g.check(R2 * 48 ** 3 / (3456 ** 2 * (psi + c) ** 3) == ASQ * (psi - 2 * c) ** 2 / (psi + c) ** 2)
# m_S = 2/(125 tau_S^2) with tau_S <= 3 a A_*/a_S gives 3 a_S^2/(250 A_*^2); e_M >= 27/512 > 3/250
for Lam in (F(1, 3), F(1), F(5, 2)):
    tS = 3 * A_(Lam)                  # tau_S <= tS * a / a_S; square: tS^2 a^2 / a_S^2
    g.check(F(2, 125) / (tS ** 2 * ASQ) == F(3, 250) / A_(Lam) ** 2)
    g.check(F(3, 250) / A_(Lam) ** 2 == F(1, 12000) / Lam ** 2)
g.check(F(1, 8) / (16 * ASQ) == F(27, 512) and F(27, 512) > F(3, 250))
# sampled on A1's elder side (psi >= 2c, R^2 <= 16(psi-2c)^2(psi+c)) intersected with D_Lambda, which
# contains E (mu is not evaluated): m_S >= c_* a_S^2 and tau_M <= 4a (A1 W1), in the rigorous direction
# (an upper enclosure of the left side against a lower enclosure of the right side)
for _ in range(1500):
    Lam = rq(F(1, 5), 3)
    gam = rq_nz(-3, 3)
    lam = rq(F(1, 89), Lam)
    psi = 24 * lam / gam ** 2
    c = rq(-psi + psi / 89, psi / 2, den=97)
    Rmax2 = 16 * (psi - 2 * c) ** 2 * (psi + c)
    R = rq(-1, 1, den=61) * sqrt_lo(Rmax2)
    aS = gam * gam * (psi + c) / 4
    kS, kM = (psi + c) / 48, (psi - c) / 48
    mS_lo = F(2, 125) / tau_hat_hi(psi, c, R, kS) ** 2
    cstar = F(3, 250) / (Lam ** 2 if MUT == "M3" else A_(Lam) ** 2)
    g.check(mS_lo >= cstar * aS * aS)
    if R == 0 and c == psi / 2:
        # the equality case of tau_M <= 4a: the middle term is (|c|/(24 kappa_M))/sqrt3 = 2/sqrt3 = 3a,
        # since (2/sqrt3)^2 = 4/3 = 9 a^2; with R = 0, tau_M = a + 3a = 4a exactly
        g.check(abs(c) / (24 * kM) == 2 and F(4, 3) == 9 * ASQ)
    else:
        g.check(tau_hat_hi(psi, c, R, kM) <= 4 * sqrt_lo(ASQ))
    g.check(aS < A_(Lam))

# =========================================================================== X6 endpoint floor
g = Group("X6_endpoint_floor")


def pythag():
    m, n = RNG.randint(1, 9), RNG.randint(0, 9)
    h = m * m + n * n
    return F(m * m - n * n, h), F(2 * m * n, h)


def targeted():
    """Near-extremal jets for the C3 term: t on the C3 components along (c^3, 3c^2 s, 3c s^2, s^3)."""
    co, si = F(20, 29), F(21, 29)
    lam_ = F(3, 10)
    return co, si, [F(0)] * 5 + [lam_ * co ** 3, lam_ * 3 * co * co * si, lam_ * 3 * co * si * si, lam_ * si ** 3]


for it in range(820):
    kp = rq(F(1, 4), 3)
    k = rq(F(1, 4), kp)
    co, si = pythag()
    t = [rq(-4, 4) for _ in range(9)]
    if it >= 800:                                   # 20 near-extremal cases with k = k_+ = 3 and lambda_2 = 0
        kp = k = F(3)
        co, si, t = targeted()
    # frame partials: t_xx1, t_xx2, t_x11, t_x12, t_x22, t_111, t_112, t_122, t_222
    gam = co * t[0] + si * t[1]
    B = co * co * t[2] + 2 * co * si * t[3] + si * si * t[4]
    C3 = co ** 3 * t[5] + 3 * co * co * si * t[6] + 3 * co * si * si * t[7] + si ** 3 * t[8]
    lam2 = F(0) if it >= 800 else rq(-3, 3)
    tn_hi = sqrt_hi(sum(x * x for x in t))
    Pw_lo = 1 + abs(lam2) + sqrt_lo(sum(x * x for x in t))
    g.check(abs(gam) <= tn_hi and abs(B) <= 2 * Pw_lo and abs(C3) <= 2 * Pw_lo)
    D = gam * gam - 12 * k * B
    J = 8 * gam ** 3 - 144 * k * B * gam + 576 * k * k * C3
    cJ = (8 + 288 * kp) if MUT == "M9" else (8 + 288 * kp + 1152 * kp * kp)
    g.check(abs(D) <= (1 + 24 * kp) * Pw_lo ** 2 and abs(J) <= cJ * Pw_lo ** 3)
    # three-term square inequality for tau_M in raw jets, with a_M in (0, A_*)
    Lam = rq(F(1, 5), 3)
    aM = rq(F(1, 89), A_(Lam) - F(1, 89))
    x1, x2, x3 = F(2, 3), abs(D) / (2 * aM), abs(J) / (48 * aM * sqrt_lo(aM))
    tauM2_hi = (x1 + x2 + x3) ** 2 / 3 * F(1)          # tau_M = (x1 + x2 + x3)/sqrt3, J-term rounded up
    Ctau = F(4, 9) * A_(Lam) ** 3 + (1 + 24 * kp) ** 2 * A_(Lam) / 4 + cJ ** 2 / 2304
    g.check(tauM2_hi <= (F(4, 9) * aM ** 3 + D * D * aM / 4 + J * J / 2304) / aM ** 3 * (1 + F(1, 10 ** 30)))
    g.check(tauM2_hi <= Ctau * Pw_lo ** 6 / aM ** 3 * (1 + F(1, 10 ** 30)))

# =========================================================================== X7 radius
g = Group("X7_radius")
for _ in range(500):
    gam = rq(-6, 6)
    lam = rq(F(1, 89), 4)
    w = rq(5, 40)
    cE = F(25, 24) if MUT == "M4" else F(25, 96)
    # rho_E >= w  <=>  sqrt(24 lam) <= (5/2)(|g|+12)/(w - 3/2)  <=>  lam <= (25/96)(|g|+12)^2/(w-3/2)^2
    lhs = 24 * lam * (w - F(3, 2)) ** 2 <= F(25, 4) * (abs(gam) + 12) ** 2
    g.check(lhs == (lam <= cE * (abs(gam) + 12) ** 2 / (w - F(3, 2)) ** 2))
    lhsR = 24 * lam * (w - F(5, 2)) ** 2 <= F(289, 36) * (abs(gam) + 12) ** 2
    g.check(lhsR == (lam <= F(289, 864) * (abs(gam) + 12) ** 2 / (w - F(5, 2)) ** 2))
    g.check(w - F(5, 2) >= w / 2)
for _ in range(200):
    U = rq(F(1, 89), 3)
    # int_0^U int_0^{12 l} s(12 l - s) ds dl = 72 U^4 and int int ds dl = 6 U^2, computed independently
    # by Simpson's rule, which is exact for these polynomials (degree 2 inside, degree 3 outside)
    inner = lambda l: simpson(lambda s: s * (12 * l - s), F(0), 12 * l)
    g.check(inner(U) == 288 * U ** 3)
    g.check(simpson(inner, F(0), U) == 72 * U ** 4)
    g.check(simpson(lambda l: simpson(lambda s: F(1), F(0), 12 * l), F(0), U) == 6 * U * U)
    # C94's normalization: s' = 4s, ds' = 4 ds, s'(48 l - s')/16 = s(12 l - s); so 288 U^4 = 4 * 72 U^4
    innerC = lambda l: simpson(lambda s2: s2 * (48 * l - s2) / 16, F(0), 48 * l)
    g.check(simpson(innerC, F(0), U) == 288 * U ** 4 == 4 * (72 * U ** 4))

# =========================================================================== X8 level band
g = Group("X8_levelband")
for _ in range(300):
    R = rq_nz(-9, 9)
    dl = rq(F(1, 89), F(1, 2))
    # c = 0: the only extra saddle is sigma = 1, Z = 48 psi/R, mu = 1 - 16 psi^3/R^2 (C82 (4))
    psi = rq(F(1, 10), 5)
    Z = 48 * psi / R
    u = F(-1, 2)
    gu, gz = gradPQS(psi, F(0), R, u, Z)
    g.check(gu == 0 and gz == 0 and hessdet(psi, F(0), R, u, Z) < 0)
    g.check(PQS(psi, F(0), R, u, Z) + 1 == 1 - 16 * psi ** 3 / R ** 2)
    # {|mu| <= delta} <=> psi^3 in [R^2(1-delta)/16, R^2(1+delta)/16]; int psi^2 dpsi = [psi^3]/3
    val = (R * R * (1 + dl) / 16 - R * R * (1 - dl) / 16) / 3
    g.check(val == dl * R * R / (12 if MUT == "M6" else 24))
for _ in range(200):
    gam = rq_nz(-3, 3)
    k = rq(F(1, 4), 3)
    D, J, psi, c, R = cubic_params(rq(0, 2), gam, rq(-3, 3), rq(-3, 3), k)
    dl = rq(F(1, 89), F(1, 2))
    g.check(gam ** 6 / 384 * dl * (F(1024, 3) * abs(c) ** 3 + 64 * R * R)
            == dl / 384 * (F(1024, 3) * abs(D) ** 3 + 64 * J * J))

# =========================================================================== X9 hard gap
g = Group("X9_hardgap")


def gap_integral(y, r, dl):
    # int_0^dl l(l^2 y + r) dl + int_dl^oo dl^5 l^-5 l (l^2 y + r) dl
    inner = y * dl ** 4 / 4 + r * dl ** 2 / 2
    outer = y * dl ** 5 * (1 / dl) + r * dl ** 5 * (1 / (3 * dl ** 3))
    return inner + outer


for _ in range(300):
    y, r, dl = rq(F(1, 89), 9), rq(0, 1), rq(F(1, 89), 5)
    coef = F(1, 4) if MUT == "M5" else F(5, 4)
    g.check(gap_integral(y, r, dl) == coef * y * dl ** 4 + F(5, 6) * r * dl ** 2)
    # independently: Simpson on [0, delta] (a cubic), and on [delta, oo) the substitution l = delta/x,
    # dl = delta x^-2 dx, which turns dl^5 l^-5 l (l^2 y + r) into delta^4 y + delta^2 r x^2 on (0, 1]
    part1 = simpson(lambda l: l * (l * l * y + r), F(0), dl)
    part2 = simpson(lambda x: dl ** 4 * y + dl ** 2 * r * x * x, F(0), F(1))
    g.check(part1 + part2 == coef * y * dl ** 4 + F(5, 6) * r * dl ** 2)
# Markov majorant: 1{lam y^2 <= eps N^2} <= N^10 min(1, (eps/(lam y^2))^5)
for _ in range(500):
    lam2, y, eps, N = rq(F(1, 89), 4), rq(F(1, 89), 4), rq(F(1, 89), 2), rq(1, 6)
    ind = 1 if lam2 * y * y <= eps * N * N else 0
    g.check(ind <= N ** 10 * min(F(1), (eps / (lam2 * y * y)) ** 5))
# the away integral and the choice d1 = sqrt(eps): total (1 + 5/24) eps + (1 + 5/18) r sqrt(eps)
for _ in range(200):
    s_ = rq(F(1, 89), 1)
    eps, r = s_ * s_, rq(0, 1)
    d1 = s_
    away = F(5, 24) * eps ** 4 * d1 ** -6 + F(5, 18) * r * eps ** 2 * d1 ** -3
    g.check(d1 ** 2 + r * d1 + away == F(29, 24) * eps + F(23, 18) * r * s_)
    # the away bound: int_{d1}^oo [(5/4) eps^4 y^-7 + (5/6) r eps^2 y^-4] dy, with y = d1/x, is
    # int_0^1 [(5/4) eps^4 d1^-6 x^5 + (5/6) r eps^2 d1^-3 x^2] dx; Boole's rule is exact for degree 5
    g.check(boole(lambda x: F(5, 4) * eps ** 4 * d1 ** -6 * x ** 5 + F(5, 6) * r * eps ** 2 * d1 ** -3 * x * x,
                  F(0), F(1)) == away)

# =========================================================================== X10 Markov splits
g = Group("X10_splits")
for _ in range(200):
    s_ = rq(F(1, 89), 1)
    eps, r = s_ * s_, rq(0, 1)
    d1 = s_
    g.check(d1 ** 2 + r * d1 + eps ** 2 * (d1 ** -2 / 2 + r * d1 ** -3 / 3) == F(3, 2) * eps + F(4, 3) * r * s_)
    # independently: int_{d1}^oo s^-4 (s + r) ds with s = d1/x is int_0^1 (x d1^-2 + r x^2 d1^-3) dx
    g.check(simpson(lambda x: x / d1 ** 2 + r * x * x / d1 ** 3, F(0), F(1)) == d1 ** -2 / 2 + r * d1 ** -3 / 3)
    # and the strip int_0^{d1} (s + r) ds = d1^2/2 + r d1 <= d1^2 + r d1
    g.check(simpson(lambda s: s + r, F(0), d1) == d1 * d1 / 2 + r * d1)
    t_ = rq(F(1, 89), 1)
    epsh = t_ ** 3
    d2 = t_
    g.check(d2 ** 2 + r * d2 + epsh ** 2 * (d2 ** -4 / 4 + r * d2 ** -5 / 5) == F(5, 4) * t_ ** 2 + F(6, 5) * r * t_)
    # int_{d2}^oo s^-6 (s + r) ds with s = d2/x is int_0^1 (x^3 d2^-4 + r x^4 d2^-5) dx (Boole: exact)
    g.check(boole(lambda x: x ** 3 / d2 ** 4 + r * x ** 4 / d2 ** 5, F(0), F(1)) == d2 ** -4 / 4 + r * d2 ** -5 / 5)

# =========================================================================== X11 ledgers
g = Group("X11_ledgers")
beta = F(1, 8) if MUT == "M7" else F(1, 16)
dexp, p = F(1, 2), 2
e = 1 - 4 * beta                              # e = r w^4 = r^(1 - 4 beta)
elder = {"w^-8": 8 * beta, "r w^-4": 1 + 4 * beta, "e": e, "r e^(1/2)": 1 + e / 2, "d": dexp, "r": F(1),
         "(e/d)^p": p * (e - dexp), "(e/d)^4": 4 * (e - dexp), "r (e/d)^2": 1 + 2 * (e - dexp),
         "e^4": 4 * e, "r e^2": 1 + 2 * e, "r^2 w^4": 2 - 4 * beta}
rejected = {"w^-8": 8 * beta, "r w^-4": 1 + 4 * beta, "e^(2/3)": 2 * e / 3, "r e^(1/3)": 1 + e / 3,
            "d": dexp, "r": F(1), "(e/d)^p": p * (e - dexp)}
g.check(min(elder.values()) == F(1, 2))
g.check(sorted(kk for kk, vv in elder.items() if vv == F(1, 2)) == ["(e/d)^p", "d", "w^-8"])
g.check(min(rejected.values()) == F(1, 2))
g.check(sorted(kk for kk, vv in rejected.items() if vv == F(1, 2)) == ["(e/d)^p", "d", "e^(2/3)", "w^-8"])
g.check(F(1, 2) - beta > 0 and e > dexp)       # r^(1/2) w <= 1 and e/d -> 0

# =========================================================================== X12 witnesses
g = Group("X12_witness")
for Lam in (F(1, 2), F(1), F(6), F(7, 3)):
    for k in (F(1, 3), F(1), F(5, 2)):
        lam, gam = Lam / 2, F(1)
        B = (1 + 6 * Lam) / (12 * k)
        C3 = (4 + 72 * Lam) / (576 * k * k)
        D, J, psi, c, R = cubic_params(lam, gam, B, C3, k)
        g.check(psi == 12 * Lam and c == -6 * Lam and R == 0)
        g.check(psi > abs(c) and psi >= 2 * c and R * R < 16 * (psi - 2 * c) ** 2 * (psi + c))
        sigma_line = psi / c                        # 48 c sigma + R Z = 48 psi with R = 0
        g.check(sigma_line < -1)                    # the conic sigma^2 + |c| Z^2/36 = 1 needs |sigma| <= 1
        # the open condition of C82 (7): for c < 0, extra points need R^2 + 64 c (psi^2 - c^2) >= 0
        g.check(R * R + 64 * c * (psi * psi - c * c) == -41472 * Lam ** 3 < 0)
        Y = 3 * k * B - gam * gam / 4
        g.check(6 * lam + Y > 0 and 6 * lam - Y > 0)
# the rejected witness at Lambda = 6: psi = 72, R = 3456 = sqrt(32 psi^3)
for k in (F(1, 3), F(1), F(5, 2)):
    Lam = F(6)
    lam, gam = Lam / 2, F(1)
    B = 1 / (12 * k)
    R0 = F(3456)
    C3 = (R0 + 4) / (576 * k * k)
    D, J, psi, c, R = cubic_params(lam, gam, B, C3, k)
    g.check(psi == 72 and c == 0 and R == R0 and R * R == 32 * psi ** 3)
    u, Z = F(-1, 2), 48 * psi / R
    g.check(gradPQS(psi, c, R, u, Z) == (0, 0) and hessdet(psi, c, R, u, Z) < 0)
    g.check(PQS(psi, c, R, u, Z) == F(-1, 2))
    Y = 3 * k * B - gam * gam / 4
    g.check(6 * lam + Y > 0 and 6 * lam - Y > 0)

# =========================================================================== X13 chord
g = Group("X13_chord")
psi, c, R = F(72), F(0), F(3456)
M = (F(-1, 2), F(0))
Yp = (F(-1, 2), 48 * psi / R)
h = -PQS(psi, c, R, *Yp)
g.check(h == F(1, 2))
hh = h / 2 if MUT == "M8" else h
for j in range(41):
    t_ = F(j, 20)
    pt = (M[0] + t_ * (Yp[0] - M[0]), M[1] + t_ * (Yp[1] - M[1]))
    g.check(PQS(psi, c, R, *pt) == hh * (2 * t_ ** 3 - 3 * t_ * t_))
far = (2 * Yp[0] - M[0], 2 * Yp[1] - M[1])
g.check(F(-5, 2) <= far[0] <= F(3, 2) and far[1] ** 2 * psi < 34 ** 2)
# rational extra saddles with general c (QS Q4's construction): sigma in (-1, 3), Z != 0,
# c = 36(sigma^2 - 1)/Z^2 (the conic), R = 48(psi - c sigma)/Z (the line), psi > |c|,
# det Hess = (c - sigma psi)/4 < 0, and 0 < h < 1. Checks: M3(f) and K inside W_R (C97 (R8)).
SADDLES = []
uR_lo = F(-3, 2) if MUT == "M13" else F(-5, 2)
while len(SADDLES) < 400:
    sg = F(RNG.randint(-99, 299), 100)
    Zs = rq_nz(-4, 4, den=97)
    if sg * sg == 1:
        continue
    c = 36 * (sg * sg - 1) / (Zs * Zs)
    psi = abs(c) + rq(F(1, 37), 11)
    R = 48 * (psi - c * sg) / Zs
    if not (c - sg * psi < 0):
        continue
    Yq = (-sg / 2, Zs)
    if gradPQS(psi, c, R, *Yq) != (0, 0):
        g.check(False, "not critical")
        continue
    hq = -PQS(psi, c, R, *Yq)
    if not (0 < hq < 1):
        continue
    SADDLES.append((psi, c, R, Yq, hq))
    for j in range(9):
        t_ = F(j, 4)
        pt = (M[0] + t_ * (Yq[0] - M[0]), M[1] + t_ * (Yq[1] - M[1]))
        g.check(PQS(psi, c, R, *pt) == hq * (2 * t_ ** 3 - 3 * t_ * t_))
    farq = (2 * Yq[0] - M[0], 2 * Yq[1] - M[1])      # K is a segment: its extremes are its endpoints
    g.check(uR_lo <= farq[0] <= F(3, 2) and farq[1] ** 2 * psi < 34 ** 2)
    g.check(-1 < sg < 3)

# =========================================================================== X14 coverage
g = Group("X14_coverage")
for _ in range(300):
    k = rq(F(1, 4), 3)
    gam = rq_nz(-3, 3)
    lam, B = rq(F(1, 89), 3), rq(-3, 3)
    D = gam * gam - 12 * k * B
    psi, c = 24 * lam / gam ** 2, D / gam ** 2
    if not psi > abs(c):
        continue
    # F as a polynomial in C3: leading coefficient (576 k^2)^2
    def Fpoly(C3):
        J = 8 * gam ** 3 - 144 * k * B * gam + 576 * k * k * C3
        cst = 8 if MUT == "M10" else 16
        return J * J - cst * (24 * lam - 2 * D) ** 2 * (24 * lam + D)
    f0, f1, f2 = Fpoly(F(0)), Fpoly(F(1)), Fpoly(F(2))
    g.check((f2 - 2 * f1 + f0) / 2 == (576 * k * k) ** 2)
    # neutral point (C98 (B16)): if R^2 = 16(psi-2c)^2(psi+c) with psi+c a square, the point
    # sigma = 1 + 2c/psi, Z^2 = 144(psi+c)/psi^2 is an extra critical point with P + 1 = 0
for _ in range(300):
    q = rq(F(1, 10), 4)
    psi = rq(F(1, 10), 6)
    c = q * q - psi
    if not (psi > abs(c)):
        continue
    R = 4 * (psi - 2 * c) * q
    sigma = 1 + 2 * c / psi
    Z = 12 * q / psi
    u = -sigma / 2
    if R == 0:
        continue
    if R * Z != 48 * (psi - c * sigma):
        Z, R = -Z, R          # the line fixes the sign of Z
    g.check(R * Z == 48 * (psi - c * sigma))
    g.check(gradPQS(psi, c, R, u, Z) == (0, 0))
    g.check(PQS(psi, c, R, u, Z) + 1 == 0)
    cst = 8 if MUT == "M10" else 16
    g.check(R * R == cst * (psi - 2 * c) ** 2 * (psi + c))

# =========================================================================== X15 G3-minus
g = Group("X15_G3minus")
thr = F(1, 6) if MUT == "M11" else F(1, 8)
for n in range(1, 64):
    b_ = F(n, 256)                                  # beta in (0, 1/4)
    ok_exp = (1 - 4 * b_) < F(1, 2)                 # delta = r^(1-4 beta) >> r^(1/2)
    g.check(ok_exp == (b_ > thr))
for _ in range(300):
    Cp, r = rq(F(1, 10), 5), rq(F(1, 10 ** 4), F(1, 10))
    s_ = rq(1, 3)
    dl = 2 * Cp * s_ * sqrt_hi(r)                   # delta >= 2 C' r^(1/2)
    lower = (dl ** 4 - (Cp * sqrt_hi(r)) ** 4) / 4  # int_{C' sqrt r}^{delta} l^3 dl (rounded down)
    g.check(lower >= dl ** 4 / 8)
# the two-sided range: for 3/16 < beta < 1/4 and p = 4, the least exponent of (G3.5) is 7 - 16 beta,
# which is the lower bound's exponent; for beta <= 3/16 the least exponent is 4
for n in range(1, 64):
    b_ = F(n, 256)
    ups = [F(4), 5 - 4 * b_, 6 - 8 * b_, 7 - 16 * b_, 3 + 4 * (1 - 4 * b_)]
    if b_ > F(3, 16):
        g.check(min(ups) == 7 - 16 * b_ and 7 - 16 * b_ < 4)
    else:
        g.check(min(ups) == 4)
# the box of step 2: lam in [Lambda/4, Lambda/2] and |Y| <= Lambda give w_lambda >= 5 Lambda^2/4
for _ in range(300):
    Lam = rq(F(1, 10), 5)
    lam = Lam / 4 + Lam / 4 * rq(0, 1)              # exact endpoints (rq truncates its bounds)
    Yj = Lam * rq(-1, 1)
    g.check((6 * lam + Yj) * (6 * lam - Yj) >= F(5, 4) * Lam ** 2 and lam > 0)

# =========================================================================== X16 endpoint chain
g = Group("X16_endpoint_chain")
# on the rational saddles of X13, with jets built from (psi, c, R): C97 (R7) h >= 4/(27 tau_M^2), and
# 4/(27 tau_M^2) >= c_h a_M^3/P^6 for the least admissible P, Lambda = lam and k_+ = k (strongest case)
for (psi, c, R, Yq, hq) in SADDLES:
    gam = rq_nz(-2, 2)
    k = rq(F(1, 4), 3)
    lam = gam * gam * psi / 24
    B = (1 - c) * gam * gam / (12 * k)
    C3 = (R + 4 - 12 * c) * gam ** 3 / (576 * k * k)
    D, J, psi2, c2, R2 = cubic_params(lam, gam, B, C3, k)
    g.check(psi2 == psi and c2 == c and R2 == R)
    kM = (psi - c) / 48
    g.check(hq >= F(4, 27) / tau_hat_lo(psi, c, R, kM) ** 2)          # rigorous: tau_lo <= tau_M
    aM = gam * gam * (psi - c) / 4
    P0 = max(F(1), abs(gam), abs(B) / 2, abs(C3) / 2)
    Lam, kp = lam, k
    Ctau = F(4, 9) * A_(Lam) ** 3 + (1 + 24 * kp) ** 2 * A_(Lam) / 4 + (8 + 288 * kp + 1152 * kp * kp) ** 2 / 2304
    ch = F(4, 27) / Ctau
    g.check(aM < A_(Lam))
    g.check(F(4, 27) / tau_hat_hi(psi, c, R, kM) ** 2 >= ch * aM ** 3 / P0 ** 6)  # rigorous: tau_hi >= tau_M

# =========================================================================== X17 inclusions
g = Group("X17_inclusions")
# Theorem E3 step 4: if T1 + T2 >= (1/2) min(v, -mu), then one of T1, T2 is >= v/4 or >= -mu/4
for _ in range(2000):
    T1, T2 = rq(0, 2), rq(0, 2)
    v, mneg = rq(F(1, 89), 3), rq(F(1, 89), 3)
    if T1 + T2 >= min(v, mneg) / 2:
        g.check(T1 >= v / 4 or T2 >= v / 4 or T1 >= mneg / 4 or T2 >= mneg / 4)
# the factors in eps_V, eps'_V, delta_B, delta_4 and eps_h, tested at the boundary of each inclusion
fac = 2 if MUT == "M12" else 4
for _ in range(300):
    K0, Ce, ce, kp = rq(F(1, 2), 9), rq(1, 99), rq(F(1, 10 ** 4), F(1, 10), den=10 ** 6), rq(F(1, 4), 3)
    k = rq(F(1, 4), kp)
    N, e, aS, rho = rq(1, 5), rq(F(1, 10 ** 3), F(1, 10), den=10 ** 6), rq(F(1, 10), 2), rq(F(1, 100), F(1, 4), den=10 ** 4)
    # V1 at its boundary: v = c_* a_S^2 and K0 N e = v/4 must lie in {a_S^2 <= eps_V N}
    v = ce * aS * aS
    e1 = v / (4 * K0 * N)
    g.check(aS * aS <= fac * K0 * e1 / ce * N)
    # V2 at its boundary: C_e k N^2 e/lam2 = v/4 must lie in {lam2 a_S^2 <= eps'_V N^2}
    lam2 = 4 * Ce * k * N * N * e / v
    g.check(lam2 * aS * aS <= 4 * Ce * kp * e / ce * N * N)
    # F_B: lam2 <= C_B k N^2 r w^4 lies in {lam2 <= delta_B N^2}, delta_B = C_B k_+ e
    CB = rq(16, 400)
    g.check(CB * k * N * N * e <= CB * kp * e * N * N)
    # V4 off the band: -mu > 2 rho and C_e k N^2 e/lam2 >= -mu/4 give lam2 <= delta_4 N^2, delta_4 = 2 C_e k_+ e/rho
    mneg = 2 * rho + rq(F(1, 10 ** 3), 1, den=10 ** 6)
    lam2b = 4 * Ce * k * N * N * e / mneg
    g.check(lam2b <= 2 * Ce * kp * e / rho * N * N)
    # V3 off the band: K0 N e >= -mu/4 > rho/2 gives 2 K0 N e >= rho
    g.check(not (K0 * N * e >= mneg / 4) or 2 * K0 * N * e >= rho)
    # rejected: K0 N e = 2 h with h = c_h a_M^3/P^6 must lie in {a_M^3 <= eps_h N P^6}, eps_h = K0 e/(2 c_h)
    chh, aM, Pw = rq(F(1, 10 ** 6), F(1, 100), den=10 ** 8), rq(F(1, 10), 3), rq(1, 4)
    h = chh * aM ** 3 / Pw ** 6
    e2 = 2 * h / (K0 * N)
    g.check(aM ** 3 <= K0 * e2 / (2 * chh) * N * Pw ** 6)

# --------------------------------------------------------------------------- report
out = {"object": "CL-QS-A3-6-CONTROLS-20261005-v2",
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
{"groups": {"X10_splits": [1000, 1000], "X11_ledgers": [5, 5], "X12_witness": [72, 72], "X13_chord": [4443, 4443], "X14_coverage": [896, 896], "X15_G3minus": [726, 726], "X16_endpoint_chain": [1600, 1600], "X17_inclusions": [3702, 3702], "X1_chart": [2000, 2000], "X2_jacobian": [300, 300], "X3_poles": [300, 300], "X4_tau_raw": [1104, 1104], "X5_elder_floor": [4707, 4707], "X6_endpoint_floor": [3280, 3280], "X7_radius": [2300, 2300], "X8_levelband": [1100, 1100], "X9_hardgap": [1500, 1500]}, "object": "CL-QS-A3-6-CONTROLS-20261005-v2", "passed": true, "total": 29035}
```

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
_Generated by [Claude Code](https://claude.ai/code)_