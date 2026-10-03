#!/usr/bin/env python3
"""C124 cross-provider review controls: exact rational checks, standard library only.

Target: C124-PLANAR-K1-CORRELATED-BAND-ENDPOINT-LOG-RATE-20261003-v1, main issue 229, comment 5974162498
(20,668 bytes, SHA-256 90148657...520f).
Reviewer: Anthropic Claude, session_01NMeKEismAyeqgdB4sy2NJU, for Dylan Roy (delegated AI review).
Written without the author's controls (5974185757) or any other reviewer's code. Disclosed stake: C124
consumes the reviewer's A4.

Usage: python3 c124_exact.py [MUTANT]   (exit 0 pass, 1 fail, 2 unknown label)
Mutants (each must exit 1):
  CHART_12     d lambda = (gamma^2/12) d psi in place of gamma^2/24 (Lemma JB)
  SHELL_2A     the dyadic shell sum bounded by 2a in place of 4a (Lemma DB)
  ES_SIX       epsilon_0 = 1/(6 C_*^2) in place of 1/(12 C_*^2) (Lemma ES)
  FT_R4        the near-branch weight r^4 J^10 in place of r^5 J^10 (Lemma FT, (14))
  W_SIXTEENTH  the fixed-layer window w = r^(-1/16) in place of r^(-1/12) (section 7)
  TABLE_H3     the w^(-8) row with H^3 in place of H^(8/3) ((18) table)
These checks test finite algebra, exact sums and exponent bookkeeping only. They do not prove C82 LB,
C101's interfaces, P4.2's residual, the Gaussian moment bounds, C95/C96/C98's identification or any
measure-theoretic step.
"""
import math
import random
import sys
from fractions import Fraction as F

MUTANTS = ("CHART_12", "SHELL_2A", "ES_SIX", "FT_R4", "W_SIXTEENTH", "TABLE_H3")
MUT = None
if len(sys.argv) > 1:
    MUT = sys.argv[1]
    if len(sys.argv) > 2 or MUT not in MUTANTS:
        print("unknown mutant label: %s" % " ".join(sys.argv[1:]))
        sys.exit(2)

RNG = random.Random(124_5974162498)
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


# =====================================================================
# G0  Lemma JB: chart Jacobian, weight, pole cancellation; the error term over |lambda| <= Lambda
# =====================================================================
g = Group("G0 Lemma JB chart and poles")
jac = F(1, 12) if MUT == "CHART_12" else F(1, 24)
for _ in range(4000):
    gam, B1, C3 = rq(-4, 4), rq(-4, 4), rq(-4, 4)
    if gam == 0:
        continue
    D, J = gam**2 - 12 * B1, 8 * gam**3 - 144 * B1 * gam + 576 * C3
    c, R = D / gam**2, J / gam**3
    l1, l2 = rq(0, 3), rq(0, 3)
    p1, p2 = 24 * l1 / gam**2, 24 * l2 / gam**2
    if p1 != p2:
        g.check((l2 - l1) / (p2 - p1) == jac * gam**2, "d lambda = (gamma^2/24) d psi")
    aM, aS = 24 * l1 - D, 24 * l1 + D
    g.check(aM * aS / 16 * jac * gam**2 == gam**6 * (p1**2 - c**2) / 384, "w_lambda d lambda = (gamma^6/384)(psi^2 - c^2) d psi")
    g.check(gam**6 * abs(c)**3 == abs(D)**3 and gam**6 * R**2 == J**2, "gamma^6 |c|^3 = |D|^3, gamma^6 R^2 = J^2")
    # the multiplier of C82 LB after the Jacobian: (delta/384)[(1024/3)|D|^3 + 64 J^2]
    g.check(gam**6 / 384 * ((F(1024, 3)) * abs(c)**3 + 64 * R**2) == (F(1024, 3) * abs(D)**3 + 64 * J**2) / 384, "LB multiplier in raw jets")
for Lam in [F(k, 3) for k in range(3, 60)]:
    H = 1 + Lam
    g.check(2 * Lam <= 2 * H and H**3 * 2 * Lam <= 2 * H**4, "error term r H^3 int_{-Lambda}^{Lambda} d lambda <= 2 r H^4")
g.close()

# =====================================================================
# G1  Lemma DB: dyadic shells, exact sums, the tail region, and the countermodel
# =====================================================================
g = Group("G1 Lemma DB dyadic summation")
shell_const = 2 if MUT == "SHELL_2A" else 4
for _ in range(3000):
    a = rq_pos(F(1, 10**6), F(1, 4), 10**7)
    b = rq_pos(0, 1, 1000)
    m = 0
    while not (F(1, 4) <= 2**m * a < F(1, 2)):
        m += 1
        if m > 80:
            break
    g.check(F(1, 4) <= 2**m * a < F(1, 2), "the integer m with 2^m a in [1/4, 1/2) exists")
    shells = sum(2 * a * F(1, 2**j) + b * F(1, 4**j) for j in range(m))
    g.check(shells <= shell_const * a + F(4, 3) * b, "sum_j [2a 2^-j + b 4^-j] <= 4a + (4/3) b")
    for j in range(m):
        g.check(2**(j + 1) * a <= F(1, 2), "each shell width 2^(j+1) a <= 1/2 (JB applies)")
    # the implications used: |mu| <= a N with 2^j a < |mu| gives N > 2^j; |mu| > 2^m a >= 1/4 gives (4 a N)^2 > 1
    for _k in range(5):
        N = rq_pos(1, 10**4)
        j = RNG.randrange(m + 1)
        mu = rq_pos(2**j * a, 2**(j + 1) * a, 10**7)
        if 2**j * a < mu <= a * N:
            g.check(N > 2**j and N**2 / 4**j > 1, "shell j: N > 2^j, so 1 < N^2 4^-j")
        mu2 = rq_pos(2**m * a, 2, 10**7)
        if 2**m * a < mu2 <= a * N:
            g.check((4 * a * N)**2 > 1, "tail: 1 < (4 a N)^2 = 16 a^2 N^2")
# countermodel: U uniform on (0, 1), N = ceil(log2(1/U)), e_m = 2^-m/m: {U <= 2^-m} lies in {U <= e_m N}
for mm in range(1, 40):
    em = F(1, 2**mm * mm)
    for k in range(1, 30):
        U = F(k, 2**(mm + 5)) * F(32, 30)            # U in (0, 2^-m]
        if U > F(1, 2**mm):
            continue
        N = 0
        while F(1, 2**N) > U:
            N += 1                                     # N = ceil(log2(1/U))
        g.check(N >= mm and U <= em * N, "countermodel: U <= 2^-m implies U <= e_m N")
    g.check(F(1, 2**mm) == mm * em, "P(U <= e_m N) >= 2^-m = m e_m, unbounded relative to e_m")
g.close()

# =====================================================================
# G2  Lemma ES: Gaussian moments, the exponential-square series and the tail bound
# =====================================================================
g = Group("G2 Lemma ES constants")
eps_den = 6 if MUT == "ES_SIX" else 12
for n in range(1, 120):
    dfact = 1
    for k in range(1, 2 * n, 2):
        dfact *= k
    g.check(dfact <= (2 * n)**n, "(2n - 1)!! <= (2n)^n")
    g.check(math.factorial(n) * 3**n >= n**n, "n! >= (n/3)^n (from e < 3)")
    # term_n = eps0^n C*^(2n) (2n)^n / n!  with eps0 = 1/(12 C*^2):  = (2n)^n / (12^n n!) <= (6/12)^n = 2^-n
    term = F((2 * n)**n, eps_den**n * math.factorial(n))
    g.check(term <= F(1, 2**n), "series term <= 2^-n, so E exp(eps0 J^2) <= sum 2^-n = 2")
g.check(sum(F(1, 2**n) for n in range(0, 200)) < 2, "sum_{n>=0} 2^-n = 2")
for _ in range(500):
    e0 = rq_pos(F(1, 100), 3)
    x2 = 10 / e0                                       # the maximizer of x^10 exp(-e0 x^2/2) satisfies e0 x^2 = 10
    g.check(e0 * x2 == 10, "d/dx [x^10 exp(-e0 x^2/2)] = 0 at e0 x^2 = 10")
    # value there: x^10 exp(-5) = (10/e0)^5 exp(-5) = (10/(e0 e))^5
    g.check(x2**5 == (10 / e0)**5, "the maximum is (10/(e0 e))^5")
    A2, J2 = rq_pos(0, 9), rq_pos(0, 9)
    if J2 > A2:
        g.check(e0 * J2 / 2 <= e0 * J2 - e0 * A2 / 2, "on J > A: exp(e0 J^2/2) <= exp(e0 J^2) exp(-e0 A^2/2)")
g.close()

# =====================================================================
# G3  Lemma FT: the near-branch integral and the scaling to the failure measure
# =====================================================================
g = Group("G3 Lemma FT near branch")
rpow = 4 if MUT == "FT_R4" else 5
for _ in range(3000):
    r, Jr, Dc, Cc = rq_pos(F(1, 1000), F(1, 2), 1000), rq_pos(1, 9), rq_pos(F(1, 10), 5), rq_pos(F(1, 10), 5)
    Lt, kap = 4 * Dc * r * Jr**2, Cc * r * Jr**2
    integral = Lt**3 / 3 + kap * Lt**2 / 2             # int_0^Lt l (l + kap) dl
    g.check(integral == r**3 * Jr**6 * (64 * Dc**3 / 3 + 8 * Cc * Dc**2), "int_0^(4 Dcap r J^2) l (l + C r J^2) dl = O(r^3 J^6)")
    weight = r**2 * Jr**4 * integral
    g.check(weight == r**rpow * Jr**10 * (64 * Dc**3 / 3 + 8 * Cc * Dc**2), "r^2 J^4 * (...) = C r^5 J^10")
    g.check(r**-3 * r**5 / r**2 == 1, "r^-3 (r^5 / Z_r with Z_r >= c r^2) is O(1)")
for Lam in [F(k, 2) for k in range(2, 80)]:
    C0 = F(7, 3)
    if Lam >= C0:
        A2 = Lam / C0
        g.check(A2 * C0 == Lam, "near and |lambda| > Lambda force J^2 > Lambda/C0 = A^2")
g.close()

# =====================================================================
# G4  section 7, fixed layer: w = r^(-1/12), e = r^(2/3); the eleven exponents of (15)
# =====================================================================
g = Group("G4 fixed-layer exponents")
bw = F(1, 16) if MUT == "W_SIXTEENTH" else F(1, 12)    # w = r^-bw
e = 1 - 4 * bw
fixed = [8 * bw, 1 + 4 * bw, e, 1 + e / 2, 1 - 2 * bw, 1 + (1 - 2 * bw) / 2, e, F(1), 2 * e, 2 - 4 * bw, 2 - 2 * bw]
g.check(fixed == [F(2, 3), F(4, 3), F(2, 3), F(4, 3), F(5, 6), F(17, 12), F(2, 3), F(1), F(4, 3), F(5, 3), F(11, 6)], "the eleven listed exponents")
g.check(min(fixed) == F(2, 3) and 3 + min(fixed) == F(11, 3), "(4): the fixed-layer mismatch is O(r^(11/3))")
g.close()

# =====================================================================
# G5  (18): Lambda = D log(1/r), H = 1 + Lambda, w = (r H^4)^(-1/12), e = r^(2/3) H^(-4/3); the table
# =====================================================================
g = Group("G5 (18) table")
# a monomial r^x H^y is represented by (x, y); w = r^(-1/12) H^(-1/3), e = r^(2/3) H^(-4/3)
w_ = (F(-1, 12), F(-1, 3))
e_ = (F(2, 3), F(-4, 3))


def mono(*parts):
    x = sum(p[0] * k for p, k in parts)
    y = sum(p[1] * k for p, k in parts)
    return (x, y)


r_, H_ = (F(1), F(0)), (F(0), F(1))
rows = {
    "w^-8": mono((w_, -8)),
    "r H^3 w^-4": mono((r_, 1), (H_, 3), (w_, -4)),
    "H^4 e": mono((H_, 4), (e_, 1)),
    "r H^5 sqrt(e)": mono((r_, 1), (H_, 5), (e_, F(1, 2))),
    "H^3 r w^2": mono((H_, 3), (r_, 1), (w_, 2)),
    "r H^4 sqrt(r w^2)": mono((r_, 1), (H_, 4), (r_, F(1, 2)), (w_, 1)),
    "e": e_,
    "r H^4": mono((r_, 1), (H_, 4)),
    "H^3 e^2": mono((H_, 3), (e_, 2)),
    "H^5 r^2 w^4": mono((H_, 5), (r_, 2), (w_, 4)),
    "H^7 r^2 w^2": mono((H_, 7), (r_, 2), (w_, 2)),
}
table = {
    "w^-8": (F(2, 3), F(3) if MUT == "TABLE_H3" else F(8, 3)),
    "r H^3 w^-4": (F(4, 3), F(13, 3)),
    "H^4 e": (F(2, 3), F(8, 3)),
    "r H^5 sqrt(e)": (F(4, 3), F(13, 3)),
    "H^3 r w^2": (F(5, 6), F(7, 3)),
    "r H^4 sqrt(r w^2)": (F(17, 12), F(11, 3)),
    "e": (F(2, 3), F(-4, 3)),
    "r H^4": (F(1), F(4)),
    "H^3 e^2": (F(4, 3), F(1, 3)),
    "H^5 r^2 w^4": (F(5, 3), F(11, 3)),
    "H^7 r^2 w^2": (F(11, 6), F(19, 3)),
}
for name, mon in rows.items():
    g.check(mon == table[name], "(18) row %s" % name)
    x, y = mon
    g.check(x > F(2, 3) or (x == F(2, 3) and y <= F(8, 3)), "row %s is O(r^(2/3) H^(8/3))" % name)
# the conditions (17) as r -> 0 with H ~ log(1/r): positive r-powers beat polylog factors
conds = {"r H": mono((r_, 1), (H_, 1)), "r w": mono((r_, 1), (w_, 1)), "e": e_, "H^2 e": mono((H_, 2), (e_, 1)),
         "r w^2": mono((r_, 1), (w_, 2))}
for name, (x, y) in conds.items():
    g.check(x > 0, "(17): %s -> 0" % name)
g.check(w_[0] < 0, "(17): w = r^(-1/12) H^(-1/3) -> infinity, so w >= 5 eventually")
g.check(e_[0] > 0, "2 K0 e <= 1/4 eventually")
g.close()

# =====================================================================
# G6  normalization of the conditional laws, and the tail choice Lambda = D log(1/r)
# =====================================================================
g = Group("G6 normalization and tails")
for _ in range(3000):
    M0 = rq_pos(F(1, 10), 5)
    Mstar = M0 * rq_pos(F(1, 10), 1, 1000)
    m0 = M0
    m = m0 + rq(-Mstar / 4, Mstar / 4, 1000)
    n0 = rq(-m0, m0, 1000)                              # nu_0(phi), |phi| <= 1
    tv = rq_pos(0, Mstar / 4, 1000)                       # ||nu - nu_0|| >= |m - m0| and >= |nu(phi) - nu_0(phi)|
    if abs(m - m0) > tv:
        continue
    n = n0 + rq(-tv, tv, 1000)
    if m < Mstar / 2:
        continue
    lhs = abs(n / m - n0 / m0)
    g.check(lhs <= tv / m + abs(m - m0) / m <= 2 * tv / m <= 4 * tv / Mstar, "||nu/m - nu0/m0|| <= 4 ||nu - nu0||/M_*")
for cexp in [F(k, 10) for k in range(1, 30)]:
    Dst = max(F(1), 1 / cexp)
    g.check(cexp * Dst >= 1, "exp(-c D_* log(1/r)) = r^(c D_*) <= r")
g.close()

# ---------------------------------------------------------------------
total = sum(t for _, _, t in RESULTS)
passed = sum(p for _, p, _ in RESULTS)
for name, p, t in RESULTS:
    print("%-46s %6d/%-6d %s" % (name, p, t, "PASS" if p == t else "FAIL"))
print("mutant: %s" % (MUT if MUT else "none"))
print("total checks: %d; failures: %d" % (total, total - passed))
for f_ in FAILS:
    print("  FAIL " + f_)
sys.exit(0 if passed == total else 1)
