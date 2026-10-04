#!/usr/bin/env python3
"""C127 cross-provider review controls: exact rational checks, standard library only.

Target: OA-C127-MIXED-INNER-REMOTE-20261004-v1, frozen in main issue 229 comment 5975032676:
PROOF.md (12,618 bytes, SHA-256 cf0dd27e...bf44) and FINITE_R_INTERPOLATION.md (18,630 bytes, c4f169c2...8187).
Reviewer: Anthropic Claude, session_01NMeKEismAyeqgdB4sy2NJU, for Dylan Roy (delegated AI review).
Written without the author controls (5975038530, 5975097180) or the first review (5975150796).

Usage: python3 c127_exact.py [MUTANT]   (exit 0 pass, 1 fail, 2 unknown label)
Mutants (each must exit 1):
  PSI3_TWO       psi''' = f_ttt + 2 f_ttz z' + ... (coefficient 2 in place of 3) in the exclusion lemma
  ROLLE_SIX      the pinned cubic's third derivative taken as 6 instead of 12
  SLAB_8R        the A-slab lower end -8 R r T^2 in place of -64 R r T^2 in (9)
  A_RESPONSE     A(q l^2) = q(0)(n.v)^2 in place of 2 q(0)(n.v)^2 (F20)
  DUAL_RHO8      the remote dual cost rho^-8 in place of rho^-9 (F25)-(F27)
  KERNEL_MASS    the U_r fourth-coordinate kernel (3/r^3)(s + r/2)(r/2 - s) in place of (6/r^3)(...)
  EXP_TABLE      the counted term r^(9/2) T^5 rho^-18 exponent 437/100 in place of 427/100
  STIRLING       N^q = sum_j S(q, j)(N)_j with S(q, j) replaced by binomial(q - 1, j - 1)
These checks test finite algebra, exact identities on polynomial fields, constants and exponent
bookkeeping only. They do not prove SC, C107, C6, DL, P, E1, E2, REC or CAP, the marked Kac-Rice
interface, the Gaussian conditioning or any measure-theoretic step.
"""
import math
import random
import sys
from fractions import Fraction as F

MUTANTS = ("PSI3_TWO", "ROLLE_SIX", "SLAB_8R", "A_RESPONSE", "DUAL_RHO8", "KERNEL_MASS", "EXP_TABLE", "STIRLING")
MUT = None
if len(sys.argv) > 1:
    MUT = sys.argv[1]
    if len(sys.argv) > 2 or MUT not in MUTANTS:
        print("unknown mutant label: %s" % " ".join(sys.argv[1:]))
        sys.exit(2)

RNG = random.Random(127_12618)
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
    a, b = int(math.floor(F(lo) * den)), int(math.floor(F(hi) * den))
    return F(RNG.randint(a, b), den)


def rq_pos(lo, hi, den=97):
    while True:
        x = rq(lo, hi, den)
        if x > 0:
            return x


# univariate polynomials as coefficient lists; bivariate as dicts {(i, j): c} in t^i z^j
def u_eval(p, x):
    return sum(c * x**i for i, c in enumerate(p))


def u_der(p):
    return [i * c for i, c in enumerate(p)][1:]


def u_mul(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def u_add(a, b):
    n = max(len(a), len(b))
    return [(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) for i in range(n)]


def b_eval(p, t, z):
    return sum(c * t**i * z**j for (i, j), c in p.items())


def b_dt(p):
    return {(i - 1, j): c * i for (i, j), c in p.items() if i > 0}


def b_dz(p):
    return {(i, j - 1): c * j for (i, j), c in p.items() if j > 0}


def b_add(a, b):
    out = dict(a)
    for k, v in b.items():
        out[k] = out.get(k, 0) + v
    return out


def b_mul(a, b):
    out = {}
    for (i, j), x in a.items():
        for (k, l), y in b.items():
            out[(i + k, j + l)] = out.get((i + k, j + l), 0) + x * y
    return out


def b_from_t(p):
    """univariate t-polynomial as bivariate."""
    return {(i, 0): c for i, c in enumerate(p)}


def b_pow(a, n):
    out = {(0, 0): F(1)}
    for _ in range(n):
        out = b_mul(out, a)
    return out


# =====================================================================
# J0  the exclusion lemma: psi''' on the critical graph; the pinned cubic; generalized Rolle; constants
# =====================================================================
g = Group("J0 exclusion lemma")
c3 = 2 if MUT == "PSI3_TWO" else 3
for _ in range(400):
    # f(t, z) = a(t) + (z - zeta(t))^2 b(t) + c (z - zeta(t))^3, so f_z(t, zeta(t)) = 0 identically
    a = [rq(-2, 2) for _ in range(5)]
    zeta = [rq(-1, 1) for _ in range(3)]
    bb = [rq(-2, 2) for _ in range(3)]
    cc = rq(-2, 2)
    w = b_add({(0, 1): F(1)}, {k: -v for k, v in b_from_t(zeta).items()})       # z - zeta(t)
    f = b_add(b_add(b_from_t(a), b_mul(b_pow(w, 2), b_from_t(bb))), {k: cc * v for k, v in b_pow(w, 3).items()})
    t = rq(-2, 2)
    z = u_eval(zeta, t)
    zp = u_eval(u_der(zeta), t)
    g.check(b_eval(b_dz(f), t, z) == 0, "f_z(t, zeta(t)) = 0")
    psi3 = u_eval(u_der(u_der(u_der(a))), t)                     # psi(t) = f(t, zeta(t)) = a(t)
    rhs = (b_eval(b_dt(b_dt(b_dt(f))), t, z) + c3 * b_eval(b_dz(b_dt(b_dt(f))), t, z) * zp
           + 3 * b_eval(b_dz(b_dz(b_dt(f))), t, z) * zp**2 + b_eval(b_dz(b_dz(b_dz(f))), t, z) * zp**3)
    g.check(psi3 == rhs, "psi''' = f_ttt + 3 f_ttz z' + 3 f_tzz z'^2 + f_zzz z'^3")
for _ in range(600):
    r = rq_pos(F(1, 50), 1)
    bb0 = rq(-3, 3)
    pc = [bb0 - r**3 / 2, -F(3, 2) * r**2, F(0), F(2)]            # the pinned cubic with k = 1
    g.check(u_eval(pc, -r / 2) == bb0 and u_eval(pc, r / 2) == bb0 - r**3, "pinned heights b, b - r^3")
    g.check(u_eval(u_der(pc), -r / 2) == 0 and u_eval(u_der(pc), r / 2) == 0, "pinned axial gradients")
    g.check(u_eval(u_der(u_der(u_der(pc))), F(0)) == (6 if MUT == "ROLLE_SIX" else 12), "the cubic's third derivative is 12")
    # any field with the same four pin data differs by e = (t^2 - r^2/4)^2 q(t); e''' changes sign in the pin interval
    qq = [rq(-2, 2) for _ in range(3)]
    e = u_mul(u_mul([-r**2 / 4, F(0), F(1)], [-r**2 / 4, F(0), F(1)]), qq)
    for s in (-r / 2, r / 2):
        g.check(u_eval(e, s) == 0 and u_eval(u_der(e), s) == 0, "e and e' vanish at both pins")
    e3 = u_der(u_der(u_der(e)))
    grid = [-r / 2 + r * F(i, 64) for i in range(65)]
    vals = [u_eval(e3, s) for s in grid]
    g.check(any(v == 0 for v in vals) or any(vals[i] * vals[i + 1] < 0 for i in range(64)) or all(v == 0 for v in e3),
            "generalized Rolle: e''' has a zero between the pins, so f_ttt = 12 somewhere there")
# the lemma's constants
for _ in range(2000):
    R = rq(1, 12)
    K = rq_pos(F(1, 10), 5)
    r = rq_pos(F(1, 1000), F(1, 4) / (R * K), 10000) if F(1, 4) / (R * K) > F(1, 1000) else F(1, 4) / (R * K)
    lam = (8 * R * K + 56 * R * K**2) * r * (1 + rq_pos(F(1, 100), 3))
    g.check(r * K <= F(1, 4) / R, "rK <= 1/(4R)")
    g.check(2 * R * K * r < lam / 4, "f_zz <= -lambda/2 throughout the cylinder")
    for tt in (F(0), R * r / 2, R * r):
        g.check(K / 2 * abs(tt**2 - r**2 / 4) <= K * R**2 * r**2, "two-node remainder |g(t)| <= (K/2)|t^2 - r^2/4| <= K R^2 r^2")
    a_ = 4 * R**2 * K * r**2 / lam
    g.check(a_ < R * r / 2, "a = 4R^2 K r^2/lambda < Rr/2")
    g.check(K * R**2 * r**2 - lam / 2 * a_ < 0, "f_z(t, a) < 0 and, symmetrically, f_z(t, -a) > 0")
    g.check(K * (R + F(1, 2)) * r + K * a_ <= 2 * R * K * r, "|f_tz| on the graph <= 2RKr")
    zp_max = 4 * R * K * r / lam
    g.check(zp_max < F(1, 2), "|zeta'| <= 4RKr/lambda < 1/2")
    g.check(K * (3 * zp_max + 3 * zp_max**2 + zp_max**3) <= 28 * R * K**2 * r / lam < F(1, 2), "|psi''' - f_ttt| <= 28RK^2 r/lambda < 1/2")
    g.check(K * (F(3, 2) * R + F(1, 2)) * r <= 2 * R * K * r <= F(1, 2), "|f_ttt(t, zeta) - 12| <= 2RKr <= 1/2")
    g.check(12 - F(1, 2) - F(1, 2) >= 11, "psi''' >= 11")
for _ in range(1000):
    R, T = rq(4, 12), rq(1, 20)
    lo = -(8 * R * T + 56 * R * T**2)
    g.check(lo >= (-8 if MUT == "SLAB_8R" else -64) * R * T**2, "(9): (8RT + 56RT^2) r <= 64 R r T^2 for T >= 1")
g.close()

# =====================================================================
# J1  the appendix: U_r right inverse, the fourth-coordinate kernel, the Hessian correction, |n.v| = |e.u|
# =====================================================================
g = Group("J1 interpolation appendix")


def U_r(p, r):
    a, c = -r / 2, r / 2
    f_a, f_c = b_eval(p, a, 0), b_eval(p, c, 0)
    ft_a, ft_c = b_eval(b_dt(p), a, 0), b_eval(b_dt(p), c, 0)
    fz_a, fz_c = b_eval(b_dz(p), a, 0), b_eval(b_dz(p), c, 0)
    return [(f_a + f_c) / 2, (f_c - f_a) / r, (ft_c - ft_a) / r, 6 / r**2 * (ft_a + ft_c - 2 * (f_c - f_a) / r),
            (fz_a + fz_c) / 2, (fz_c - fz_a) / r]


for _ in range(800):
    r = rq_pos(F(1, 50), 1)
    A = [rq(-3, 3) for _ in range(6)]
    pa = {(0, 0): A[0] - r**2 * A[2] / 8, (1, 0): A[1] - r**2 * A[3] / 24, (2, 0): A[2] / 2, (3, 0): A[3] / 6,
          (0, 1): A[4], (1, 1): A[5]}
    g.check(U_r(pa, r) == A, "(F11): U_r(p_a) = a")
    # the fourth coordinate is (6/r^3) int (s + r/2)(r/2 - s) f_ttt(s, 0) ds, a mass-one average, on quintics
    gq = [rq(-3, 3) for _ in range(6)]
    p5 = b_from_t(gq)
    g3 = u_der(u_der(u_der(gq)))
    ker = u_mul([r / 2, F(1)], [r / 2, F(-1)])                    # (s + r/2)(r/2 - s)
    integrand = u_mul(ker, g3)
    anti = [F(0)] + [c / (i + 1) for i, c in enumerate(integrand)]
    integral = u_eval(anti, r / 2) - u_eval(anti, -r / 2)
    six = 3 if MUT == "KERNEL_MASS" else 6
    g.check(U_r(p5, r)[3] == six / r**3 * integral, "U_r's fourth coordinate as a Peano-kernel average of f_ttt")
    kmass = [F(0)] + [c / (i + 1) for i, c in enumerate(ker)]
    g.check(six / r**3 * (u_eval(kmass, r / 2) - u_eval(kmass, -r / 2)) == 1, "the kernel has total mass one")
# (F20): d_v^2 (q l^2)(0) = 2 q(0) (d_v l(0))^2 for any q and any l with l(0) = 0
TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29)]
units = []
for (p_, q_, r_) in TRIPLES:
    for s1, s2 in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
        units.append((F(s1 * p_, r_), F(s2 * q_, r_)))
        units.append((F(s2 * q_, r_), F(s1 * p_, r_)))
for _ in range(600):
    q = {(i, j): rq(-2, 2) for i in range(3) for j in range(3 - i)}
    lq = {(i, j): rq(-2, 2) for i in range(3) for j in range(3 - i) if (i, j) != (0, 0)}   # l(0) = 0
    v = RNG.choice(units)
    # directional second derivative along v at the origin, through the line y = s v
    def along(p):
        out = {}
        for (i, j), c in p.items():
            # (s v0)^i (s v1)^j = s^(i+j) v0^i v1^j
            out[i + j] = out.get(i + j, 0) + c * v[0]**i * v[1]**j
        return out
    prod = b_mul(q, b_mul(lq, lq))
    d2 = 2 * along(prod).get(2, 0)
    dvl = along(lq).get(1, 0)
    coef = 1 if MUT == "A_RESPONSE" else 2
    g.check(d2 == coef * q.get((0, 0), 0) * dvl**2, "(F20): A(q l^2) = 2 q(0)(n.v)^2")
# |n.v| = |e.u| for orthonormal pairs (u, v), (e, n) in the plane, both orientations
for _ in range(600):
    u = RNG.choice(units)
    e = RNG.choice(units)
    for v in ((-u[1], u[0]), (u[1], -u[0])):
        for n in ((-e[1], e[0]), (e[1], -e[0])):
            g.check(abs(n[0] * v[0] + n[1] * v[1]) == abs(e[0] * u[0] + e[1] * u[1]), "|n.v| = |e.u|")
g.close()

# =====================================================================
# J2  cost and composition ledgers: rho^-5, rho^-7, rho^-9, rho^18, rho^-36, and (15)
# =====================================================================
g = Group("J2 cost and composition ledgers")
g.check(2 * 1 + 3 == 5, "(F16): one separator q = psi_x and three derivatives: rho^-5")
g.check(5 + 2 == 7, "(F23): the Hessian correction divides by 2q(0)(n.v)^2 >= c rho^2: rho^-7")
remote = 8 if MUT == "DUAL_RHO8" else 9
g.check(2 * 4 + 1 == remote, "(F25)-(F27): four separators and one derivative: rho^-9")
g.check(2 * remote == 18, "(F5): the duality floor rho^18")
g.check(18 * 4 // 2 == 36, "(13)/(F29): four conditional coordinates give rho^-36")
g.check(max(4, 3, 5) <= 5, "frequencies |n|_1 <= 5 (pin dual 4, correction 3, remote 5)")
# (15): endpoints r^4 T^6, remote determinant T^2, A slab r T^2, height r^3, one Z_r ~ r^2
rp, Tp = 4 + 1 + 3 - 2, 6 + 2 + 2
g.check((rp, Tp) == (6, 10), "(15): r^6 T^10 rho^-36")
for _ in range(400):
    th = rq_pos(F(1, 1000), F(1, 8), 1000)
    # sinc(x) >= 1 - x^2/6 and |e.u| >= 1 - theta^2/6 >= 1/2 for theta <= pi/256 < 1/80
    g.check(th >= F(0) and 1 - th**2 / 6 >= F(1, 2), "1 - theta^2/6 >= 1/2")
g.check(F(355, 113) / 256 < F(1, 80), "theta <= pi/256 < 1/80")
g.close()

# =====================================================================
# J3  the moment conversion (5), the falsifier, (18) and the exponent table
# =====================================================================
g = Group("J3 moments and exponents")


def stirling2(n, k):
    if MUT == "STIRLING":
        return math.comb(n - 1, k - 1) if n >= 1 and k >= 1 else (1 if n == k == 0 else 0)
    s = [[0] * (n + 1) for _ in range(n + 1)]
    s[0][0] = 1
    for i in range(1, n + 1):
        for j in range(1, i + 1):
            s[i][j] = j * s[i - 1][j] + s[i - 1][j - 1]
    return s[n][k]


def falling(nn, j):
    out = 1
    for i in range(j):
        out *= nn - i
    return out


for q in range(1, 13):
    for nn in range(0, 25):
        g.check(nn**q == sum(stirling2(q, j) * falling(nn, j) for j in range(1, q + 1)), "N^q = sum S(q, j)(N)_j")
# the falsifier of section 7: factorial moments O(r^3) but E[N_R N_far] = r^3
for _ in range(200):
    r = rq_pos(F(1, 1000), F(1, 10), 1000)
    pr = r**3
    g.check(pr * falling(2, 2) == 2 * r**3 and pr * 1 * 1 == r**3, "falsifier: (N)_2 = 2 r^3 while E[N_R N_far] = r^3")
# (18) at rho = r^(1/100), T = r^(-1/100), m = 600
al, be, m = F(1, 100), F(1, 100), 600
trunc_event = 6 - 10 * be - 36 * al
tail_event = m * be
counted = F(3, 2) + trunc_event / 2
counted_tail = F(3, 2) + tail_event / 2
g.check(trunc_event == F(277, 50), "truncated event r^6 T^10 rho^-36 = r^(277/50)")
g.check(tail_event == 6, "tail event T^-600 = r^6")
g.check(counted == (F(437, 100) if MUT == "EXP_TABLE" else F(427, 100)), "counted term r^(9/2) T^5 rho^-18 = r^(427/100)")
g.check(counted_tail == F(9, 2) and counted_tail >= counted, "counted tail r^(9/2), dominated by r^(427/100)")
g.check(counted + 2 == F(627, 100), "times Z_r <= z* r^2: r^(627/100)")
g.check(counted - 3 == F(127, 100), "the mixed count is r^(127/100) below the r^3 scale")
# the cutoff conditions at r <= small threshold: r^(99/100) <= 1/(4R) etc. are positive powers
g.check(1 - al > 0 and 1 - be > 0, "r <= rho/8 and rT <= 1/(4R) hold for small r")
g.close()

# ---------------------------------------------------------------------
total = sum(t for _, _, t in RESULTS)
passed = sum(p for _, p, _ in RESULTS)
for name, p, t in RESULTS:
    print("%-40s %6d/%-6d %s" % (name, p, t, "PASS" if p == t else "FAIL"))
print("mutant: %s" % (MUT if MUT else "none"))
print("total checks: %d; failures: %d" % (total, total - passed))
for f_ in FAILS:
    print("  FAIL " + f_)
sys.exit(0 if passed == total else 1)
