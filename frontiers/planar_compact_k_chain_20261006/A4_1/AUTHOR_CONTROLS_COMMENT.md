## QS addendum A4.1: author controls, exact executable and stdout

These are the standard-library script and the 50-digit exploration behind [A4.1 5973261552](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5973261552). They are author-side controls, not review evidence. They check finite algebra, exactly pinned polynomial fields and exponent ledgers only; they do not prove the Gaussian or geometric steps imported from C103, C101, C97 and A4.

Dylan Roy — delegated AI work. Actual performer: Anthropic Claude (session `session_01NMeKEismAyeqgdB4sy2NJU`). Scientific effect: NONE.

**Extraction rule.**
- Each file is the exact text between its ```` ```python ```` fence under the `###` heading and the next ```` ``` ```` line, plus one final newline.
- Each expected output is the text in the following ```` ```text ```` fence, plus one final newline.
- The byte counts below include those newlines.

**Run.**
- `python3 -B -S a41_exact.py`: exit 0, with exactly the stdout shown. A run takes about 5 seconds.
- `-O` mode and plain `python3`: byte-identical output.
- `python3 a41_exact.py BOGUS`: exit 2.
- Each of the six mutant labels exits 1 (table below).
- `a41_numeric.py` needs mpmath and must sit next to `a41_exact.py`, whose helper section it executes. It is exploration, not a control.

The outputs were produced with Python 3.11.15 (mpmath 1.3.0).

**Groups.**

| group | what it checks |
|---|---|
| W0 | Lemma LE_K (i) on 120 exactly pinned degree-5 fields over five `K` entries (two singletons), with `w ∈ {1, 3, 6}`. Also (A0_K) on the remainder-extremal fields `(7/2)(x ± z)⁴/24` plus pins (corner ratio up to 0.984). |
| W1 | Lemma LE (ii) as a positive-semidefinite form on 6,000 random `(γ, a_M)`, and the equality example `4h = 2\|v\|² = 37/18` |
| W2 | Corollary LE_K's scalar bookkeeping and Lemma B′_K's monomials |
| W3 | the growing-`Λ` ledger, every closed form in the table, admissibility (including `C_η rw² = (5/6)η_K`), the Example and the failure at `β = 2/3`, for eight values of `β` |
| W4 | the fixed-`Λ` ledger for `ε = 1/30, 1/100, 1/1000` |

**Mutants.** Each was actually run; each exits 1.

| label | change | first failing group | failed checks |
|---|---|---|---:|
| `K2_UNIT` | `K₂(1) = 115/48` in place of `K₂(K)` | W0 | 16 |
| `LE_36` | `γ² + 36` in place of `γ² + 72` | W1 | 2816 |
| `OLD_ENDPOINT` | C103 (S18) terms kept in place of Lemma B′_K | W3 | 18 |
| `P_TWO` | band Markov order fixed at `p = 2` | W3 | 16 |
| `W_HALF` | `w = r^{−β/16}` | W3 | 22 |
| `ALPHA_4` | `α = (2 − 3β)/4` | W3 | 33 |

### a41_exact.py

- **File:** 17190 bytes, SHA-256 `57b440967161d2cfbc17e7a93d39627616cda52f63a2cb30b7c5fa64552830c1`.
- **Stdout:** 562 bytes, SHA-256 `e94b02574a21ea629019965c1b0c7f95f2c07bcfd8f84cbd194001aa870bae12`.

```python
#!/usr/bin/env python3
"""QS addendum A4.1 controls: exact rational checks, standard library only.

A4.1 makes A4's planar rate (main issue 229, comment 5972396791) uniform over a
compact positive gap interval K, by composing A4's Lemma LE / Corollary LE /
Lemma B' and the general-p band with C103's k-uniform interfaces (comment
5967841127). Author: Anthropic Claude, session_01NMeKEismAyeqgdB4sy2NJU, for
Dylan Roy (delegated AI work). Author-side controls, not review evidence.

Usage: python3 a41_exact.py [MUTANT]
  exit 0: every check passes; exit 1: some check fails; exit 2: unknown label.
Mutant labels (each must make the script exit 1):
  K2_UNIT       eta_K built from K2 at k = 1 (115/48) instead of C103's K2(K)
  LE_36         gamma^2 + 36 in place of gamma^2 + 72 in Lemma LE (ii)
  OLD_ENDPOINT  C103's (S18) term H^4 e^(2/3) + r H^5 e^(1/3) kept in place of Lemma B'_K
  P_TWO         the band Markov order p fixed at 2
  W_HALF        w = r^(-beta/16) in place of r^(-beta/8)
  ALPHA_4       Lambda = r^(-alpha) with alpha = (2 - 3 beta)/4
These checks test finite algebra, exactly pinned polynomial fields and exponent
ledgers only. They do not prove the Gaussian or geometric steps imported from
C103, C101, C97 and A4.
"""
import sys
import random
from fractions import Fraction as F
from math import ceil

MUTANTS = ("K2_UNIT", "LE_36", "OLD_ENDPOINT", "P_TWO", "W_HALF", "ALPHA_4")
MUT = None
if len(sys.argv) > 1:
    MUT = sys.argv[1]
    if len(sys.argv) > 2 or MUT not in MUTANTS:
        print("unknown mutant label: %s" % " ".join(sys.argv[1:]))
        sys.exit(2)

RNG = random.Random(41_5972949776)
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


# ---------- bivariate polynomials {(i, j): coef} ----------
def pdiff(p, ax):
    out = {}
    for (i, j), c in p.items():
        if ax == 0 and i:
            out[(i - 1, j)] = out.get((i - 1, j), 0) + c * i
        if ax == 1 and j:
            out[(i, j - 1)] = out.get((i, j - 1), 0) + c * j
    return {kk: v for kk, v in out.items() if v != 0}


def peval(p, x, z):
    return sum(c * x**i * z**j for (i, j), c in p.items())


def pscale_vars(p, sx, sz):
    return {(i, j): c * sx**i * sz**j for (i, j), c in p.items()}


def padd(p, q, sq=1):
    out = dict(p)
    for kk, v in q.items():
        out[kk] = out.get(kk, 0) + sq * v
    return {kk: v for kk, v in out.items() if v != 0}


def pmul(p, q):
    out = {}
    for (i1, j1), a in p.items():
        for (i2, j2), b in q.items():
            kk = (i1 + i2, j1 + j2)
            out[kk] = out.get(kk, 0) + a * b
    return {kk: v for kk, v in out.items() if v != 0}


def ppow(p, n):
    out = {(0, 0): F(1)}
    for _ in range(n):
        out = pmul(out, p)
    return out


def K2_of(km, kp):
    """C103 (S12) / C91 (W3): K2(K) = 17/(48 k_-) + 1/24 + max(1/k_-, 1, k_+) (1 + k_+)^2 / 2"""
    if MUT == "K2_UNIT":
        return F(115, 48)
    return F(17, 48) / km + F(1, 24) + max(1 / km, F(1), kp) * (1 + kp)**2 / 2


def solve4(A, rhs):
    M = [row[:] + [v] for row, v in zip(A, rhs)]
    n = 4
    for c in range(n):
        piv = next(r_ for r_ in range(c, n) if M[r_][c] != 0)
        M[c], M[piv] = M[piv], M[c]
        for r_ in range(n):
            if r_ != c and M[r_][c] != 0:
                fct = M[r_][c] / M[c][c]
                M[r_] = [x - fct * y_ for x, y_ in zip(M[r_], M[c])]
    return [M[i][4] / M[i][i] for i in range(n)]


def pin_field(p, k, r, b):
    """add a cubic in x and (d0 + d1 x) z to p so that the C103 pins hold exactly"""
    a = r / 2
    px, pz = pdiff(p, 0), pdiff(p, 1)
    A = [[1, -a, a**2, -a**3], [1, a, a**2, a**3], [0, 1, -2 * a, 3 * a**2], [0, 1, 2 * a, 3 * a**2]]
    rhs = [b - peval(p, -a, 0), b - k * r**3 - peval(p, a, 0), -peval(px, -a, 0), -peval(px, a, 0)]
    cvec = solve4([[F(x) for x in row] for row in A], rhs)
    f = dict(p)
    for i, cv in enumerate(cvec):
        f[(i, 0)] = f.get((i, 0), 0) + cv
    zp, zm = peval(pz, a, 0), peval(pz, -a, 0)
    f[(0, 1)] = f.get((0, 1), 0) - (zp + zm) / 2
    f[(1, 1)] = f.get((1, 1), 0) - (zp - zm) / (2 * a)
    return {kk: v for kk, v in f.items() if v != 0}


def error_poly(f, k, r, b):
    """E_r = F_r - G_y in C103's normalization F_r(X, z) = (f(rX, rkz) - b)/(k r^3)"""
    Fr = {kk: c / (k * r**3) for kk, c in pscale_vars(f, r, r * k).items()}
    Fr[(0, 0)] = Fr.get((0, 0), 0) - b / (k * r**3)
    A_ = 2 * f.get((0, 2), 0)
    lam, gam, B, C = -k * A_ / r, 2 * f.get((2, 1), 0), k * 2 * f.get((1, 2), 0), k**2 * 6 * f.get((0, 3), 0)
    G = {(3, 0): F(2), (1, 0): F(-3, 2), (0, 0): F(-1, 2), (2, 1): gam / 2, (0, 1): -gam / 8,
         (0, 2): -lam / 2, (1, 2): B / 2, (0, 3): C / 6}
    return padd(Fr, G, -1)


def N4_window(f, r, k, w):
    quart = []
    for i in range(5):
        p_ = f
        for _ in range(i):
            p_ = pdiff(p_, 0)
        for _ in range(4 - i):
            p_ = pdiff(p_, 1)
        quart.append(p_)
    corners = [(sx * r * w, sz * r * k * w) for sx in (-1, 1) for sz in (-1, 1)]
    return max(abs(peval(q_, x, z)) for q_ in quart for x, z in corners)


# =====================================================================
# W0  Lemma LE_K (i): E_r vanishes to second order at raw M, and |E_r(xi)| <= K2(K) N r w^2 |xi - raw M|^2 on W_w
# =====================================================================
g = Group("W0 Lemma LE_K (i) on pinned fields at gap k")
Kints = [(F(1, 2), F(2)), (F(1, 3), F(1)), (F(1), F(3)), (F(2), F(2)), (F(1), F(1))]
MX = F(-1, 2)
ratio_rand, ratio_ext, ratio_hess = F(0), F(0), F(0)


def le_i_checks(f, k, r, b, w, km, kp, tag):
    global ratio_rand, ratio_ext
    E = error_poly(f, k, r, b)
    Ex, Ez = pdiff(E, 0), pdiff(E, 1)
    g.check(peval(E, MX, 0) == 0 and peval(Ex, MX, 0) == 0 and peval(Ez, MX, 0) == 0, "E(raw M) = 0, grad E(raw M) = 0")
    N4 = N4_window(f, r, k, w)
    K2 = K2_of(km, kp)
    best = F(0)
    if tag == "extremal":
        # the input (A0_K) itself: second partials of E at the window corners against K2(K) N r w^2
        global ratio_hess
        sec = [pdiff(pdiff(E, 0), 0), pdiff(pdiff(E, 0), 1), pdiff(pdiff(E, 1), 1)]
        lower = max(abs(peval(d_, sx * w, sz * w)) for d_ in sec for sx in (-1, 1) for sz in (-1, 1))
        g.check(lower <= K2 * N4 * r * w**2, "(A0_K): |E|_2 <= K2(K) N r w^2 (k=%s)" % k)
        ratio_hess = max(ratio_hess, lower / (K2 * N4 * r * w**2))
    for _ in range(40):
        xi = (rq(-w, w, 199), rq(-w, w, 199))
        d2 = (xi[0] - MX)**2 + xi[1]**2
        if d2 == 0:
            continue
        lhs = abs(peval(E, xi[0], xi[1]))
        rhs = K2 * N4 * r * w**2 * d2
        g.check(lhs <= rhs, "|E(xi)| <= K2(K) N r w^2 |xi - M|^2 (%s, k=%s)" % (tag, k))
        best = max(best, lhs / rhs)
    return best


for idx in range(120):
    km, kp = Kints[idx % len(Kints)]
    k = km if idx % 3 == 0 else (kp if idx % 3 == 1 else rq(km, kp))
    r, b = rq(F(1, 200), F(1, 20), 997), rq(-2, 2)
    p = {}
    for i in range(6):
        for j in range(6 - i):
            if i + j >= 2:
                p[(i, j)] = rq(-3, 3) * (10 if i + j >= 4 else 1)
    f = pin_field(p, k, r, b)
    for w in (F(1), F(3), F(6)):
        ratio_rand = max(ratio_rand, le_i_checks(f, k, r, b, w, km, kp, "random"))
# remainder-extremal fields: N0 (x + sig z)^4 / 24 plus pins, at the endpoints of K
for km, kp in Kints:
    for k in sorted({km, kp}):
        for sig in (1, -1):
            r, b, N0 = F(1, 50), F(1, 3), F(7, 2)
            lin = {(1, 0): F(1), (0, 1): F(sig)}
            p = {kk: N0 * c / 24 for kk, c in ppow(lin, 4).items()}
            f = pin_field(p, k, r, b)
            for w in (F(5), F(10)):
                ratio_ext = max(ratio_ext, le_i_checks(f, k, r, b, w, km, kp, "extremal"))
g.close()

# =====================================================================
# W1  Lemma LE (ii): the quadratic form 4h - 2 l |v|^2 in (a, z) is PSD (k-free; A4 verbatim)
# =====================================================================
g = Group("W1 Lemma LE (ii), k-free")
c72 = 36 if MUT == "LE_36" else 72
for _ in range(6000):
    gam = rq_nonzero(-6, 6)
    aM = rq(F(1, 97), 200)
    kapM = aM / (48 * gam**2)
    ell = min(F(1), aM / (gam**2 + c72))
    # 4h - 2 ell |v|^2 with h = (3a^2 + kap z^2)/3 and v = (a - z/12, z/gamma)
    m11 = 4 - 2 * ell
    m12 = ell / 6
    m22 = 4 * kapM / 3 - 2 * ell / 144 - 2 * ell / gam**2
    g.check(m22 == aM / (36 * gam**2) - ell / 72 - 2 * ell / gam**2, "matrix entry (2,2)")
    g.check(m11 > 0 and m22 >= 0 and m11 * m22 - m12**2 >= 0, "PSD")
    a_, z_ = rq(-3, 3), rq(-3, 3)
    form = 4 * (3 * a_**2 + kapM * z_**2) / 3 - 2 * ell * ((a_ - z_ / 12)**2 + z_**2 / gam**2)
    g.check(form == m11 * a_**2 + 2 * m12 * a_ * z_ + m22 * z_**2, "form = matrix")
    g.check(form >= 0, "4h >= 2 l |v|^2")
# the attained case gamma = 1, a_M = 73: Y = (-7/12, 1) in (u, Z) coordinates relative to the chart, h = 37/72
gam, aM = F(1), F(73)
a_, z_ = F(-7, 12) + F(1, 2), F(1)
kapM = aM / (48 * gam**2)
h = (3 * a_**2 + kapM * z_**2) / 3
v2 = (a_ - z_ / 12)**2 + (z_ / gam)**2
g.check(h == F(37, 72) and 4 * h == 2 * v2 == F(37, 18), "equality example 4h = 2|v|^2 = 37/18")
g.close()

# =====================================================================
# W2  Corollary LE_K and Lemma B'_K bookkeeping
# =====================================================================
g = Group("W2 Corollary LE_K and Lemma B'_K")
for _ in range(4000):
    gam = rq(-6, 6)
    aM = rq(F(1, 97), 200)
    eta, N = rq(F(1, 10**6), 1, 10**6), rq(1, 100)
    ell = min(F(1), aM / (gam**2 + 72))
    if eta * N * (gam**2 + 72) < aM and eta * N < 1:
        g.check(eta * N < ell, "LE_K conditions give 2 K2 N r w^2 < l")
    h, mu = None, None
    h = rq(F(1, 1000), F(999, 1000), 1000)
    mu = 1 - h
    E0 = rq(0, F(1, 2), 1000)
    if E0 < mu / 2:
        g.check(-h - E0 > -1, "chord clearance from E0 < mu/2 alone")
    if h > F(1, 9) and E0 < mu / 2:
        g.check(4 * h - E0 > 0, "h > 1/9: the endpoint is automatic")
# Lemma B'_K as monomials in (r, H, eta): near strip at delta = sqrt(eta), plus two Markov terms
VARS = ("r", "H", "e", "w", "d", "eta", "Lam")


def mono(**kw):
    return tuple(F(kw.get(v_, 0)) for v_ in VARS)


def mmul(*ms):
    return tuple(sum(x) for x in zip(*ms))


def mpow(m, t):
    return tuple(x * F(t) for x in m)


near = {mmul(mono(H=2), mpow(mono(eta=1), 1)), mmul(mono(r=1, H=4), mono(eta=F(1, 2)))}
markov = {mmul(mono(H=3), mono(eta=1)), mmul(mono(H=3), mono(eta=2))}
claimed = {mono(H=3, eta=1), mono(r=1, H=4, eta=F(1, 2))}


def dominated(t, S):
    """t <= C s for some s in S when H >= 1, eta <= 1, r <= 1: same r power, H power <=, eta power >="""
    return any(t[0] == s_[0] and t[1] <= s_[1] and t[5] >= s_[5] and t[2:5] == s_[2:5] and t[6] == s_[6] for s_ in S)


g.check(all(dominated(t, claimed) for t in near | markov), "B'_K terms dominated by H^3 eta + r H^4 sqrt(eta)")
g.check(claimed <= near | markov, "both claimed terms occur")
# eta_K at K = {1} is A4's eta_LE = 2 K2 r w^2 with K2 = 115/48
g.check(2 * K2_of(F(1), F(1)) == F(115, 24), "eta_K(1) = (115/24) r w^2")
g.close()

# =====================================================================
# W3  the compact-K ledger (Rerr'_K, tails) for every beta < 2/3, and admissibility
# =====================================================================
g = Group("W3 growing-Lambda ledger at compact K")


def ledger(beta):
    alpha = (2 - 3 * beta) / (4 if MUT == "ALPHA_4" else 16)
    om = beta / 16 if MUT == "W_HALF" else beta / 8          # w = r^(-om)
    p = F(2) if MUT == "P_TWO" else max(F(1), (beta + 3 * alpha) / (1 - 3 * beta / 2))
    m = max(1, ceil(beta / alpha))
    ex = 1 - 4 * om                                            # e = r w^4
    eta = 1 - 2 * om                                           # eta_K ~ r w^2
    H = -alpha
    terms = {
        "w^-8": 8 * om,
        "r H^3 w^-4": 1 + 3 * H + 4 * om,
        "H^4 e": 4 * H + ex,
        "r H^5 sqrt(e)": 1 + 5 * H + ex / 2,
        "d": beta,
        "r H^4": 1 + 4 * H,
        "H^3 (e/d)^p": 3 * H + p * (ex - beta),
        "H^5 r^2 w^4": 5 * H + 2 - 4 * om,
        "H^7 r^2 w^2": 7 * H + 2 - 2 * om,
        "Lambda^-m (both tails)": m * alpha,
        "far/derivative exceptions": F(1),
    }
    if MUT == "OLD_ENDPOINT":
        terms["H^4 e^(2/3)"] = 4 * H + 2 * ex / 3
        terms["r H^5 e^(1/3)"] = 1 + 5 * H + ex / 3
    else:
        terms["H^3 eta_K"] = 3 * H + eta
        terms["r H^4 sqrt(eta_K)"] = 1 + 4 * H + eta / 2
    adm = {"r H / k_-": 1 + H, "r (1 + k_+) w": 1 - om, "e": ex, "H^2 e": 2 * H + ex,
           "eta_K, C_eta r w^2": eta, "d": beta}
    return alpha, p, m, terms, adm


BETAS = [F(1, 10), F(1, 4), F(1, 3), F(1, 2), F(3, 5), F(13, 20), F(2, 3) - F(1, 100), F(2, 3) - F(1, 1000)]
for beta in BETAS:
    alpha, p, m, terms, adm = ledger(beta)
    for name, ex_ in terms.items():
        g.check(ex_ >= beta, "beta=%s: %s exponent %s >= beta" % (beta, name, ex_))
    g.check(min(terms.values()) == beta, "beta=%s: the minimum is attained (w^-8 and d)" % beta)
    for name, ex_ in adm.items():
        g.check(ex_ > 0, "beta=%s: admissibility power %s = %s > 0" % (beta, name, ex_))
    # closed forms of the exponents quoted in A4.1
    if MUT is None:
        g.check(terms["H^4 e"] == (2 + beta) / 4 and adm["H^2 e"] == F(3, 4) - beta / 8 and adm["r H / k_-"] == 1 - alpha,
                "closed forms (2+beta)/4, 3/4-beta/8, 1-alpha")
        g.check(terms["H^3 eta_K"] == (10 + 5 * beta) / 16 and terms["r H^4 sqrt(eta_K)"] == 1 + 5 * beta / 8,
                "closed forms (10+5beta)/16, 1+5beta/8")
        g.check(terms["r H^3 w^-4"] == (10 + 17 * beta) / 16 and terms["r H^5 sqrt(e)"] == (14 + 11 * beta) / 16
                and terms["r H^4"] == (2 + 3 * beta) / 4 and terms["H^5 r^2 w^4"] == (22 + 7 * beta) / 16
                and terms["H^7 r^2 w^2"] == (18 + 17 * beta) / 16, "closed forms of the remaining table rows")
        g.check(terms["w^-8"] == beta and terms["d"] == beta, "w^-8 and d always attain beta")
# C_eta r w^2 = (5K2/3) r w^2 = (5/6) eta_K, so eta_K <= 1 implies C103's C_eta r w^2 <= 1
for km, kp in Kints:
    K2 = K2_of(km, kp)
    g.check(F(5, 3) * K2 == F(5, 6) * (2 * K2), "C_eta r w^2 = (5/6) eta_K (K=[%s,%s])" % (km, kp))
# the example beta = 3/5: alpha = 1/80, w = r^(-3/40), least p = 51/8, least m = 48
if MUT is None:
    alpha, p, m, terms, adm = ledger(F(3, 5))
    g.check(alpha == F(1, 80) and (F(3, 5) + 3 * alpha) / (1 - F(9, 10)) == F(51, 8) and m == 48, "example beta = 3/5")
# beta = 2/3 is not reached: the band pair fails for every fixed p
beta = F(2, 3)
alpha = (2 - 3 * beta) / 16
g.check(alpha == 0, "alpha(2/3) = 0: no room for a growing layer")
for p in (F(2), F(10), F(1000)):
    g.check((1 - beta / 2 - beta) * p <= 0, "at beta = 2/3, (e/d)^p does not vanish for any p")
g.close()

# =====================================================================
# W4  fixed Lambda: the sector errors O_K(r^(11/3 - eps))
# =====================================================================
g = Group("W4 fixed-Lambda sector ledger at compact K")
for eps in (F(1, 30), F(1, 100), F(1, 1000)):
    om = F(1, 24) if MUT == "W_HALF" else F(1, 12)
    ex = 1 - 4 * om
    d = F(2, 3) - eps
    p = F(2) if MUT == "P_TWO" else F(2) / (3 * eps)
    terms = {"w^-8": 8 * om, "r w^-4": 1 + 4 * om, "e": ex, "r sqrt(e)": 1 + ex / 2, "d": d, "r": F(1),
             "(e/d)^p": p * (ex - d), "r^2 w^4": 2 - 4 * om, "r^2 w^2": 2 - 2 * om}
    if MUT == "OLD_ENDPOINT":
        terms["e^(2/3)"] = 2 * ex / 3
    else:
        terms["eta"] = 1 - 2 * om
        terms["r sqrt(eta)"] = 1 + (1 - 2 * om) / 2
    for name, ex_ in terms.items():
        g.check(ex_ >= F(2, 3) - eps, "eps=%s: %s exponent %s >= 2/3 - eps" % (eps, name, ex_))
    g.check(3 + min(terms.values()) == F(11, 3) - eps, "eps=%s: Q^W sector error r^(11/3 - eps)" % eps)
g.close()

# ---------------------------------------------------------------------
total = sum(t for _, _, t in RESULTS)
passed = sum(p for _, p, _ in RESULTS)
for name, p, t in RESULTS:
    print("%-46s %6d/%-6d %s" % (name, p, t, "PASS" if p == t else "FAIL"))
print("Lemma LE_K (i), largest |E(xi)| / (K2(K) N4 r w^2 |xi - M|^2): random %.3f, remainder-extremal %.3f"
      % (float(ratio_rand), float(ratio_ext)))
print("(A0_K) on remainder-extremal fields, largest corner |E|_2 / (K2(K) N4 r w^2): %.3f" % float(ratio_hess))
print("mutant: %s" % (MUT if MUT else "none"))
print("total checks: %d; failures: %d" % (total, total - passed))
for f_ in FAILS:
    print("  FAIL " + f_)
sys.exit(0 if passed == total else 1)
```

```text
W0 Lemma LE_K (i) on pinned fields at gap k     16104/16104  PASS
W1 Lemma LE (ii), k-free                        24001/24001  PASS
W2 Corollary LE_K and Lemma B'_K                 3741/3741   PASS
W3 growing-Lambda ledger at compact K             202/202    PASS
W4 fixed-Lambda sector ledger at compact K         36/36     PASS
Lemma LE_K (i), largest |E(xi)| / (K2(K) N4 r w^2 |xi - M|^2): random 0.046, remainder-extremal 0.138
(A0_K) on remainder-extremal fields, largest corner |E|_2 / (K2(K) N4 r w^2): 0.984
mutant: none
total checks: 44084; failures: 0
```

### a41_numeric.py (exploration, mpmath)

- **File:** 5743 bytes, SHA-256 `83d4b06cda23d0366ce0a6631442e5dc4ea24d694b14718351dcbda9899d96c7`.
- **Output:** 315 bytes, SHA-256 `d210cc5c6a5da56498b43669b033dfb39ba8abd689a06b7d021048e42186269b`.

```python
#!/usr/bin/env python3
"""A4.1 exploration (outside any repository; mpmath allowed here).

End-to-end test of Lemma LE_K / Corollary LE_K at gap k != 1 on exactly pinned
polynomial fields whose midpoint jets y lie in Rsec:
  f = b + k r^3 G_y(x/r, z/(r k)) + p(x, z) + (exact pin corrections),
with p of degree 4-5, so the midpoint jets are exactly y. In C103's normalization
F_r(X, zeta) = (f(rX, rk zeta) - b)/(k r^3) = G_y + E_r. The highest extra saddle
Y of P_QS is computed in closed form (conic x line) at 50 digits. Whenever the LE
conditions hold with eta_K = 2 K2(K) r w^2 and N4 (the supremum of the fourth
partials on the physical window), the doubled chord endpoint must satisfy
F_r(raw M + 2v) > 0; the Taylor bound |E_r(xi)| <= K2(K) N4 r w^2 |xi - raw M|^2
is also checked along the chord.
"""
import random
from fractions import Fraction as F
import mpmath as mp
import types
_src = open("a41_exact.py").read()
_cut = _src.index("# W0  Lemma LE_K (i)")
_src = _src[:_src.rindex("# =====", 0, _cut)]     # helpers only, no checks, no exit
X = types.SimpleNamespace()
_ns = {"__name__": "a41_helpers"}
exec(compile(_src, "a41_exact.py (helpers)", "exec"), _ns)
X.__dict__.update(_ns)

mp.mp.dps = 50
RNG = random.Random(41_2026_1003)


def rq(lo, hi, den):
    return F(RNG.randint(int(F(lo) * den), int(F(hi) * den)), den)


def DJ(y):
    lam, gam, B, C = y
    return gam**2 - 12 * B, 8 * gam**3 - 144 * B * gam + 576 * C


def n_y(y):
    lam = y[0]
    D, J = DJ(y)
    Phi = J**2 - 64 * (12 * lam - D)**2 * (24 * lam + D)
    if 12 * lam < D:
        return 2 if Phi < 0 else 1
    return 1 if Phi > 0 else 0


def mpf(x):
    return mp.mpf(x.numerator) / x.denominator


def highest_saddle(y):
    lam, gam, B, C = y
    D, J = DJ(y)
    psi, c, R = mpf(24 * lam / gam**2), mpf(D / gam**2), mpf(J / gam**3)
    a2, a1 = 6 * R**2 - 384 * c**3, -384 * c**2 * psi
    a0 = -mp.mpf(3) / 2 * R**2 - 96 * c * psi**2
    disc = a1**2 - 4 * a2 * a0
    best = None
    if disc >= 0 and abs(a2) > mp.mpf(10)**-40:
        for u in ((-a1 + mp.sqrt(disc)) / (2 * a2), (-a1 - mp.sqrt(disc)) / (2 * a2)):
            Z = 48 * (psi + 2 * c * u) / R
            P = 2 * u**3 - mp.mpf(3) / 2 * u - mp.mpf(1) / 2 - (psi + 2 * c * u) * Z**2 / 48 + R * Z**3 / 3456
            det = 12 * u * (-(psi + 2 * c * u) / 24 + R * Z / 576) - (c * Z / 12)**2
            if det < 0 and (best is None or P > best[2]):
                best = (u, Z, P)
    return best


def G_val(y, Xv, z):
    lam, gam, B, C = [mpf(t) for t in y]
    return (2 * Xv**3 - mp.mpf(3) / 2 * Xv - mp.mpf(1) / 2 + gam / 2 * (Xv**2 - mp.mpf(1) / 4) * z
            - lam / 2 * z**2 + B / 2 * Xv * z**2 + C / 6 * z**3)


def E_val(E, Xv, z):
    return sum(mpf(c) * Xv**i * z**j for (i, j), c in E.items())


stats = dict(fields=0, le_hold=0, endpoint_fail=0, taylor_fail=0, min_end_ratio=mp.mpf(10)**9, max_taylor=mp.mpf(0),
             near_boundary=0)
Kints = [(F(1, 2), F(2)), (F(1, 3), F(1)), (F(1), F(3)), (F(2), F(2))]
tries = 0
while stats["fields"] < 3000:
    tries += 1
    km, kp = Kints[tries % len(Kints)]
    k = rq(km, kp, 97)
    y = (rq(F(1, 50), 4, 97), rq(F(-3), 3, 97), rq(-2, 2, 97), rq(-2, 2, 97))
    lam, gam, B, C = y
    if gam == 0:
        continue
    aM, aS = 24 * lam - gam**2 + 12 * B, 24 * lam + gam**2 - 12 * B
    if not (aM > 0 and aS > 0) or n_y(y) == 0:
        continue
    Y = highest_saddle(y)
    if Y is None or not (-1 < Y[2] < 0):
        continue
    u, Z, P = Y
    h = -P
    vX, vz = (u + mp.mpf(1) / 2) - Z / 12, Z / mpf(gam)          # raw(Y) - raw(M)
    Rch = mp.mpf(5) / 2 + 3 * (abs(mpf(gam)) + 12) / mp.sqrt(24 * mpf(lam))
    w = F(int(mp.ceil(Rch)) + 1)
    r = F(1, RNG.choice([2000, 5000, 20000, 100000]))
    b = rq(-1, 1, 97)
    # f = b + k r^3 G_y(x/r, z/(rk)) as an exact polynomial in (x, z)
    G = {(3, 0): F(2), (1, 0): F(-3, 2), (0, 0): F(-1, 2), (2, 1): gam / 2, (0, 1): -gam / 8,
         (0, 2): -lam / 2, (1, 2): B / 2, (0, 3): C / 6}
    f0 = {(i, j): k * r**3 * c / (r**i * (r * k)**j) for (i, j), c in G.items()}
    f0[(0, 0)] += b
    scale = F(10)**RNG.randint(-1, 3)
    p = {(i, j): rq(-3, 3, 97) * scale for i in range(6) for j in range(6 - i) if i + j >= 4}
    f = X.pin_field(X.padd(f0, p), k, r, b)
    E = X.error_poly(f, k, r, b)
    stats["fields"] += 1
    N4 = X.N4_window(f, r, k, w)
    K2 = X.K2_of(km, kp)
    eta = 2 * K2 * r * w**2
    le = eta * N4 * (gam**2 + 72) < aM and eta * N4 < 1
    for t in (mp.mpf(1) / 2, mp.mpf(1), mp.mpf(3) / 2, mp.mpf(2)):
        xi = (-mp.mpf(1) / 2 + t * vX, t * vz)
        bound = mpf(K2 * N4 * r * w**2) * ((xi[0] + mp.mpf(1) / 2)**2 + xi[1]**2)
        e = abs(E_val(E, xi[0], xi[1]))
        stats["max_taylor"] = max(stats["max_taylor"], e / bound)
        if e > bound:
            stats["taylor_fail"] += 1
    if le:
        stats["le_hold"] += 1
        end = G_val(y, -mp.mpf(1) / 2 + 2 * vX, 2 * vz) + E_val(E, -mp.mpf(1) / 2 + 2 * vX, 2 * vz)
        ratio = end / (4 * h)
        stats["min_end_ratio"] = min(stats["min_end_ratio"], ratio)
        if end <= 0:
            stats["endpoint_fail"] += 1
        if eta * N4 * (gam**2 + 72) > aM / 2:
            stats["near_boundary"] += 1

print("pinned fields with jets in Rsec, k in K: %d (from %d draws)" % (stats["fields"], tries))
print("LE_K conditions held: %d (of which %d with eta N (g^2+72) > a_M/2)" % (stats["le_hold"], stats["near_boundary"]))
print("endpoint F_r(raw M + 2v) <= 0 while LE_K held: %d" % stats["endpoint_fail"])
print("min F_r(raw M + 2v) / 4h while LE_K held: %s" % mp.nstr(stats["min_end_ratio"], 6))
print("Taylor bound along chords: failures %d; max |E| / (K2 N4 r w^2 |xi-M|^2) = %s" % (stats["taylor_fail"], mp.nstr(stats["max_taylor"], 4)))
```

```text
pinned fields with jets in Rsec, k in K: 3000 (from 11963 draws)
LE_K conditions held: 153 (of which 76 with eta N (g^2+72) > a_M/2)
endpoint F_r(raw M + 2v) <= 0 while LE_K held: 0
min F_r(raw M + 2v) / 4h while LE_K held: 0.995708
Taylor bound along chords: failures 0; max |E| / (K2 N4 r w^2 |xi-M|^2) = 0.01107
```

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
_Generated by [Claude Code](https://claude.ai/code)_