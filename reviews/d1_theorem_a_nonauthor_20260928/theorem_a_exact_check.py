"""Exact checks for the nonauthor review of D1 Theorem A (parent Sections 3-7 and the cap import).

Python standard library only. Everything is exact rational arithmetic. A small
sparse Laurent-polynomial class verifies algebraic identities as polynomial
identities, not at sample points. Part P runs an exact-rational falsification
probe of the typed-weight bounds (6.1) and (6.2).

Groups (IDs follow the Grok D1 interface table: A2 = parent Section 3,
A3 = Section 5, A5 = (6.1), A6 = (6.2), A7 = Section 7, CAP = the
marked-cylinder cap import):

  A2  contact frame determinant, target, and U3 as an exact positive average;
  A3  Peano/trapezoid identities behind (5.1)-(5.2), block determinant (5.3),
      congruence erratum D_r = diag(r^-1/2, I);
  A5  Schur / determinant-lemma form of the canceled pivot (6.1);
  A6  algebra from (5.1)+(5.3)+Weyl to the bounds in (6.2);
  A7  (7.3) integral identity, the power ledger of (7.4)-(7.8), m=1 split (7.5);
  CAP every rational constant of the cap theorem, the F'' identity (11) for
      scalar and vector transverse coordinates, and the kappa rescaling;
  P   exact falsification probe of (6.1)/(6.2) in m = 1, 2, 3, including
      extremal instances attaining equality.

Not a continuum proof. Gaussian statements (uniform covariance gap, density
(3.5), residual independence, uniform integrability, the floor z_*) are argued
in REVIEW.md, not checked here.
"""
import argparse
import itertools
import json
import random
import sys
from fractions import Fraction as F


# --------------------------------------------------------------------------
# Sparse Laurent polynomials over Q with named variables.
# A monomial is a sorted tuple of (name, exponent) pairs with exponent != 0.
# --------------------------------------------------------------------------

def _mono_mul(a, b):
    d = dict(a)
    for v, e in b:
        n = d.get(v, 0) + e
        if n:
            d[v] = n
        else:
            d.pop(v, None)
    return tuple(sorted(d.items()))


class P:
    __slots__ = ("t",)

    def __init__(self, t=None):
        self.t = {m: c for m, c in (t or {}).items() if c != 0}

    @staticmethod
    def c(x):
        return P({(): F(x)})

    @staticmethod
    def v(name, e=1):
        return P({((name, e),): F(1)})

    @staticmethod
    def lift(o):
        return o if isinstance(o, P) else P.c(o)

    def __add__(self, o):
        o = P.lift(o)
        t = dict(self.t)
        for m, c in o.t.items():
            t[m] = t.get(m, 0) + c
        return P(t)

    __radd__ = __add__

    def __neg__(self):
        return P({m: -c for m, c in self.t.items()})

    def __sub__(self, o):
        return self + (-P.lift(o))

    def __rsub__(self, o):
        return P.lift(o) - self

    def __mul__(self, o):
        o = P.lift(o)
        t = {}
        for m1, c1 in self.t.items():
            for m2, c2 in o.t.items():
                m = _mono_mul(m1, m2)
                t[m] = t.get(m, 0) + c1 * c2
        return P(t)

    __rmul__ = __mul__

    def __pow__(self, n):
        out = P.c(1)
        for _ in range(n):
            out = out * self
        return out

    def is_zero(self):
        return not self.t

    def d(self, name):
        t = {}
        for m, c in self.t.items():
            dm = dict(m)
            e = dm.get(name, 0)
            if e == 0:
                continue
            if e == 1:
                dm.pop(name)
            else:
                dm[name] = e - 1
            key = tuple(sorted(dm.items()))
            t[key] = t.get(key, 0) + c * e
        return P(t)

    def antider(self, name):
        t = {}
        for m, c in self.t.items():
            dm = dict(m)
            e = dm.get(name, 0)
            if e == -1:
                raise ValueError("log term")
            dm[name] = e + 1
            key = tuple(sorted(dm.items()))
            t[key] = t.get(key, 0) + c / (e + 1)
        return P(t)

    def subs(self, name, q):
        q = P.lift(q)
        out = P()
        for m, c in self.t.items():
            dm = dict(m)
            e = dm.pop(name, 0)
            if e < 0:
                raise ValueError("negative power substitution")
            rest = P({tuple(sorted(dm.items())): c})
            out = out + rest * (q ** e)
        return out

    def integrate(self, name, lo, hi):
        a = self.antider(name)
        return a.subs(name, hi) - a.subs(name, lo)

    def coeff(self, name, e):
        """Coefficient of name^e (as a polynomial in the other variables)."""
        t = {}
        for m, c in self.t.items():
            dm = dict(m)
            if dm.get(name, 0) != e:
                continue
            dm.pop(name, None)
            key = tuple(sorted(dm.items()))
            t[key] = t.get(key, 0) + c
        return P(t)

    def exponents(self, name):
        return sorted({dict(m).get(name, 0) for m in self.t})


def det(M):
    n = len(M)
    total = P()
    for perm in itertools.permutations(range(n)):
        inv = sum(1 for i in range(n) for j in range(i + 1, n) if perm[i] > perm[j])
        term = P.c(-1 if inv % 2 else 1)
        for i in range(n):
            term = term * M[i][perm[i]]
        total = total + term
    return total


def adj(M):
    n = len(M)
    out = [[P() for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            minor = [[M[a][b] for b in range(n) if b != j] for a in range(n) if a != i]
            cof = det(minor) if minor else P.c(1)
            out[j][i] = cof if (i + j) % 2 == 0 else -cof
    return out


def quad(beta, M):
    n = len(beta)
    s = P()
    for i in range(n):
        for j in range(n):
            s = s + beta[i] * M[i][j] * beta[j]
    return s


R = P.v("r")
RI = P.v("r", -1)


# --------------------------------------------------------------------------
# A2: contact frame (3.1)-(3.4)
# --------------------------------------------------------------------------

def check_a2(mut):
    out = {}
    # Rows of T_ax acting on (f(a), f_x(a), f(c), f_x(c)).
    u3_scale = 7 if mut == "u3-row" else 6
    T_ax = [
        [P.c(F(1, 2)), P.c(0), P.c(F(1, 2)), P.c(0)],
        [-RI, P.c(0), RI, P.c(0)],
        [P.c(0), -RI, P.c(0), RI],
        [u3_scale * 2 * RI ** 3, u3_scale * RI ** 2, -u3_scale * 2 * RI ** 3, u3_scale * RI ** 2],
    ]
    d_ax = det(T_ax)
    ok_ax = (d_ax - 12 * RI ** 4).is_zero()
    T_tr = [[P.c(F(1, 2)), P.c(F(1, 2))], [-RI, RI]]
    ok_tr = (det(T_tr) - RI).is_zero()
    ledger = {}
    for dd in range(2, 7):
        m = dd - 1
        ledger[str(dd)] = -(4 + m) == -(dd + 3)
    out["axial_det_equals_12_r^-4"] = ok_ax
    out["transverse_det_equals_r^-1"] = ok_tr
    out["abs_det_T_r_equals_12_r^-(d+3)_for_d_2_to_6"] = all(ledger.values())

    # Target (3.3): f(a)=b, f(c)=b-k r^3, f_x(a)=f_x(c)=0.
    b, k = P.v("b"), P.v("k")
    O = [b, P.c(0), b - k * R ** 3, P.c(0)]
    U = [sum((T_ax[i][j] * O[j] for j in range(4)), P()) for i in range(4)]
    target = [b - k * R ** 3 * F(1, 2), -k * R ** 2, P.c(0), 12 * k]
    out["target_v_r_exact"] = all((U[i] - target[i]).is_zero() for i in range(4))

    # U3 is exactly a positive weighted average of f_xxx:
    # U3 = int_a^c w(t) f_xxx(t) dt with w = 6 (t-a)(c-t)/r^3 >= 0 and int w = 1.
    x, t = P.v("x"), P.v("t")
    f = sum((P.v("c%d" % j) * x ** j * F(1, _fact(j)) for j in range(10)), P())
    a_, c_ = -R * F(1, 2), R * F(1, 2)
    fa, fc = f.subs("x", a_), f.subs("x", c_)
    fxa, fxc = f.d("x").subs("x", a_), f.d("x").subs("x", c_)
    U0 = (fa + fc) * F(1, 2)
    U1 = (fc - fa) * RI
    U2 = (fxc - fxa) * RI
    U3 = u3_scale * RI ** 2 * (fxa + fxc - 2 * (fc - fa) * RI)
    w = 6 * (t - a_) * (c_ - t) * RI ** 3
    fxxx_t = f.d("x").d("x").d("x").subs("x", t)
    avg = (w * fxxx_t).integrate("t", a_, c_)
    out["U3_equals_positive_average_of_f_xxx"] = (U3 - avg).is_zero()
    out["U3_weight_mass_one"] = (w.integrate("t", a_, c_) - 1).is_zero()
    # Contact limits and the absence of odd r powers (mean-square rate O(r^2)).
    lim = [(U0, "c0"), (U1, "c1"), (U2, "c2"), (U3, "c3")]
    out["U_r_limits_are_contact_jet"] = all(
        (u.coeff("r", 0) - P.v(cn)).is_zero() and min(u.exponents("r")) >= 0 for u, cn in lim)
    out["U_r_minus_contact_is_O_r^2"] = all(
        all(e == 0 or e >= 2 for e in u.exponents("r")) for u, _ in lim)
    r2 = U3.coeff("r", 2)
    out["U3_r^2_term_is_f5_over_40_and_f4_cancels"] = (r2 - P.v("c5") * F(1, 40)).is_zero()
    return out


def _fact(n):
    out = 1
    for i in range(2, n + 1):
        out *= i
    return out


# --------------------------------------------------------------------------
# A3: endpoint identities (5.1)-(5.3) and the congruence erratum
# --------------------------------------------------------------------------

def check_a3(mut):
    out = {}
    x, t, s = P.v("x"), P.v("t"), P.v("s")
    f = sum((P.v("c%d" % j) * x ** j * F(1, _fact(j)) for j in range(10)), P())
    a_, c_ = -R * F(1, 2), R * F(1, 2)
    f1, f2, f3 = f.d("x"), f.d("x").d("x"), f.d("x").d("x").d("x")
    fa, fc = f.subs("x", a_), f.subs("x", c_)
    # Trapezoid/Hermite identity: f(c)-f(a) = (r/2)(f'(a)+f'(c)) - (1/2) int (t-a)(c-t) f''' dt.
    K = (t - a_) * (c_ - t)
    herm = (K * f3.subs("x", t)).integrate("t", a_, c_)
    lhs = fc - fa
    rhs = R * F(1, 2) * (f1.subs("x", a_) + f1.subs("x", c_)) - herm * F(1, 2)
    out["hermite_trapezoid_identity"] = (lhs - rhs).is_zero()
    out["hermite_kernel_mass_r^3_over_6"] = (K.integrate("t", a_, c_) - R ** 3 * F(1, 6)).is_zero()
    # f'(c)-f'(a) = r f''(a) + int (c-s) f'''(s) ds = r f''(c) - int (s-a) f'''(s) ds.
    id_a = f1.subs("x", c_) - f1.subs("x", a_) - R * f2.subs("x", a_) - (
        (c_ - s) * f3.subs("x", s)).integrate("s", a_, c_)
    id_c = f1.subs("x", c_) - f1.subs("x", a_) - R * f2.subs("x", c_) + (
        (s - a_) * f3.subs("x", s)).integrate("s", a_, c_)
    out["endpoint_f_xx_identities"] = id_a.is_zero() and id_c.is_zero()
    out["endpoint_kernel_masses_r^2_over_2"] = (
        ((c_ - s).integrate("s", a_, c_) - R ** 2 * F(1, 2)).is_zero()
        and ((s - a_).integrate("s", a_, c_) - R ** 2 * F(1, 2)).is_zero())
    # |alpha| <= M3/2 uses (1/r) int_a^c |t-a| dt = r/2.
    out["alpha_beta_average_constant_r_over_2"] = (
        ((t - a_).integrate("t", a_, c_) * RI - R * F(1, 2)).is_zero())
    # Under the pins f'(a)=f'(c)=0, f(c)-f(a)=-k r^3: with f''' == 12k the three
    # averages give alpha_M=-6k, alpha_S=6k, U3=12k exactly.
    k = P.v("k")
    out["constant_f_xxx_gives_alpha_M_-6k_alpha_S_6k"] = (
        (-(c_ - s) * 12 * k).integrate("s", a_, c_) * RI * RI + 6 * k).is_zero() and (
        ((s - a_) * 12 * k).integrate("s", a_, c_) * RI * RI - 6 * k).is_zero()

    # (5.3): det H / r = alpha det A - r beta^T adj(A) beta, symbolic, m = 1, 2, 3.
    # Erratum: D_r = diag(r^-1/2, I) with rho = sqrt(r).
    ok53, okD, okOld = True, True, True
    rho = P.v("rho")
    for m in (1, 2, 3):
        al = P.v("al")
        be = [P.v("be%d" % i) for i in range(m)]
        A = [[P.v("A%d%d" % (min(i, j), max(i, j))) for j in range(m)] for i in range(m)]
        H = [[R * al] + [R * be[j] for j in range(m)]]
        for i in range(m):
            H.append([R * be[i]] + [A[i][j] for j in range(m)])
        coef = 2 if mut == "bordered-det" else 1
        rhs53 = al * det(A) - coef * R * quad(be, adj(A))
        ok53 &= (det(H) - R * rhs53).is_zero()
        # Congruence with rho^2 = r.
        Hr = [[e.subs("r", rho * rho) for e in row] for row in H]
        Dg = [P.v("rho", -1)] + [P.c(1)] * m
        DHD = [[Dg[i] * Hr[i][j] * Dg[j] for j in range(m + 1)] for i in range(m + 1)]
        want = [[al] + [rho * be[j] for j in range(m)]]
        for i in range(m):
            want.append([rho * be[i]] + [A[i][j] for j in range(m)])
        okD &= all((DHD[i][j] - want[i][j]).is_zero() for i in range(m + 1) for j in range(m + 1))
        okD &= (det(DHD) * rho * rho - det(Hr)).is_zero()
        Dold = [rho] + [P.c(1)] * m
        okOld &= (Dold[0] * Hr[0][0] * Dold[0] - al * rho ** 4).is_zero()
    out["block_determinant_5.3_m_1_2_3"] = ok53
    out["erratum_congruence_entries_and_det_H_over_r"] = okD
    out["displayed_diag_sqrt_r_gives_alpha_r^2_singular_limit"] = okOld
    return out


# --------------------------------------------------------------------------
# A5/A6: algebra behind (6.1) and (6.2)
# --------------------------------------------------------------------------

def check_a5_a6(mut):
    out = {}
    ok_lemma, ok_s, ok_w = True, True, True
    for m in (1, 2, 3):
        be = [P.v("be%d" % i) for i in range(m)]
        A = [[P.v("A%d%d" % (min(i, j), max(i, j))) for j in range(m)] for i in range(m)]
        tt = P.v("tt")
        Mt = [[A[i][j] - tt * be[i] * be[j] for j in range(m)] for i in range(m)]
        # Matrix determinant lemma: det(A - t bb^T) = det A - t b^T adj(A) b.
        ok_lemma &= (det(Mt) - (det(A) - tt * quad(be, adj(A)))).is_zero()
        # (h/2) prod(l_j+rh) + r (h^2/4) prod_{j>=2}(l_j+rh) = (h/2)[l_1+(3/2)rh] prod_{j>=2}.
        h = P.v("h")
        lam = [P.v("l%d" % j) for j in range(1, m + 1)]
        tail = P.c(1)
        for j in range(1, m):
            tail = tail * (lam[j] + R * h)
        lhs = h * F(1, 2) * (lam[0] + R * h) * tail + R * h * h * F(1, 4) * tail
        three_halves = F(1) if mut == "mixed-square" else F(3, 2)
        rhs = h * F(1, 2) * (lam[0] + three_halves * R * h) * tail
        ok_s &= (lhs - rhs).is_zero()
        prodl = P.c(1)
        for j in range(m):
            prodl = prodl * lam[j]
        prodW = P.c(1)
        for j in range(1, m):
            prodW = prodW * lam[j] * (lam[j] + R * h)
        W = (R * h * F(1, 2) * prodl) * (R * rhs)
        ok_w &= (W - R * R * h * h * F(1, 4) * lam[0] * (lam[0] + F(3, 2) * R * h) * prodW).is_zero()
    out["determinant_lemma_schur_form_of_6.1"] = ok_lemma
    out["saddle_bound_algebra_3_over_2"] = ok_s
    out["typed_weight_product_6.2"] = ok_w
    return out


# --------------------------------------------------------------------------
# A7: Section 7 integrals and power ledger
# --------------------------------------------------------------------------

def check_a7(mut):
    out = {}
    lam, D, E, U = P.v("lam"), P.v("D"), P.v("E"), P.v("U")
    integ = (lam * (lam + E * R * U)).integrate("lam", P.c(0), D * R * U * U)
    want = R ** 3 * (D ** 3 * F(1, 3) * U ** 6 + E * D ** 2 * F(1, 2) * U ** 5)
    out["7.3_integral_identity"] = (integ - want).is_zero()
    # Ledger for m >= 2: r^2 U^(2m) prefactor times r^3 U^6 -> r^5 U^(2m+6); / Z ~ r^2 -> r^3.
    led = True
    for m in range(2, 8):
        r_pow = 2 + 3
        u_pow = 2 + 2 * (m - 1) + 6
        led &= (r_pow == 5) and (u_pow == 2 * m + 6) and (r_pow - 2 == 3)
    out["m_ge_2_ledger_r^5_U^(2m+6)_then_r^3"] = led
    # m = 1 split (7.5): (J+l)^2 <= 2J^2 + 2l^2 exactly; and if 4 D r l <= 1 then
    # l <= 2 D r J^2 + 2 D r l^2 forces l <= 4 D r J^2.
    J = P.v("J")
    out["(J+l)^2_le_2J^2+2l^2"] = ((2 * J * J + 2 * lam * lam - (J + lam) ** 2) - (J - lam) ** 2).is_zero()
    rng = random.Random(20260928)
    split_ok, far_nonempty = True, True
    for _ in range(4000):
        Dq = F(rng.randrange(1, 400), rng.randrange(1, 40))
        rq = F(1, rng.randrange(1, 400))
        Jq = 1 + F(rng.randrange(0, 400), rng.randrange(1, 40))
        lq = F(rng.randrange(1, 10 ** 6), rng.randrange(1, 10 ** 4))
        big = 1 / (Dq * rq) + lq
        for cand in (lq, big):
            if cand <= Dq * rq * (Jq + cand) ** 2:
                far = cand > 1 / (4 * Dq * rq)
                if mut == "drop-far-branch":
                    far = False
                if not (cand <= 4 * Dq * rq * Jq ** 2 or far):
                    split_ok = False
        # Every lambda >= 1/(D r) lies in the MAJORANT event lambda <= D r (J+lambda)^2 that (7.5)
        # splits, so the decomposition must keep a far branch. This is not actual depth failure.
        far_nonempty &= big <= Dq * rq * (Jq + big) ** 2
    out["7.5_near_far_split_of_majorant_exact_random_4000"] = split_ok
    out["majorant_event_contains_far_branch_l_ge_1_over_Dr"] = far_nonempty
    # The source uses only: depth failure => majorant membership. The converse is false. OpenAI
    # review 5341593068 example: k=K=1, D=4/3, r=1/1000, J=M3=12, lambda=750 is in the majorant
    # (and M3 <= K(J+lambda)), but the actual depth threshold (4/(3k)) r M3^2 is 24/125 < 750.
    kq, Kq, Dq, rq, Jq, M3q, lq = F(1), F(1), F(4, 3), F(1, 1000), F(12), F(12), F(750)
    thr = F(4, 3) / kq * rq * M3q ** 2
    out["majorant_membership_does_not_imply_depth_failure"] = (
        Dq == 4 * Kq ** 2 / (3 * kq) and lq >= 1 / (Dq * rq) and lq <= Dq * rq * (Jq + lq) ** 2
        and M3q <= Kq * (Jq + lq) and thr == F(24, 125) and lq > thr)
    # Near branch: h <= K(1+4D) J^2; exact integral gives r^3 J^6 times a constant, with
    # prefactor r^2 h^2/4 -> r^5 J^10.
    Kc = P.v("K")
    hn = Kc * (1 + 4 * D) * J * J
    near = (lam * (lam + F(3, 2) * R * hn)).integrate("lam", P.c(0), 4 * D * R * J * J)
    near_w = R * R * hn * hn * F(1, 4) * near
    out["near_branch_is_r^5_J^10"] = near_w.exponents("r") == [5] and near_w.exponents("J") == [10]
    # Far branch and M4 exception: (4Dr)^4 and (10r/(3k))^4 give r^4 on W/r^2, so numerators
    # are r^6; total (7.8) is C3 r^3 + C4 r^4.
    out["far_and_M4_numerators_r^6"] = (4 + 2 == 6) and (6 - 2 == 4)
    return out


# --------------------------------------------------------------------------
# CAP: marked-cylinder cap theorem constants and identity (11)
# --------------------------------------------------------------------------

def check_cap(mut):
    out = {}
    x = P.v("x")
    a_, c_ = -R * F(1, 2), R * F(1, 2)
    K = (x - a_) * (c_ - x)
    # f(S)-f(M) = -kappa r^3 = -(1/2)(r^3/6) avg(f_xxx), so avg = 12 kappa = 2 at kappa = 1/6.
    kap6 = F(1, 6)
    out["kernel_mass_r^3_over_6_and_average_2_at_kappa_1_6"] = (
        (K.integrate("x", a_, c_) - R ** 3 * F(1, 6)).is_zero()
        and kap6 / (F(1, 2) * F(1, 6)) == 2)
    # Product distance from any x0 in [-r/2, r/2] (and from M) to D is <= 5r/2 + 2r = 9r/2 < 5r.
    out["product_distance_9r_over_2_lt_5r"] = F(5, 2) + 2 == F(9, 2) and F(9, 2) < 5
    out["f_xxx_ge_7_over_4"] = 2 - 5 * F(1, 20) == F(7, 4)
    out["delta_gt_22r"] = (8 * 2 - 5 == 11) and (2 * 11 == 22)
    # (6): max_{|x|<=2r} |x^2 - r^2/4| = 15 r^2/4, so ||w|| <= (15/8) m r^2 < 2 m r^2.
    xs = [F(i, 64) for i in range(-128, 129)]
    out["w_bound_15_over_8"] = max(abs(q * q - F(1, 4)) for q in xs) / 2 == F(15, 8) and F(15, 8) < 2
    # (7): (1/r) int_{-r/2}^{r/2} |x-t| dt  equals |x| outside and x^2/r + r/4 inside; max 2r.
    def avg_abs(q):
        if abs(q) >= F(1, 2):
            return abs(q)
        return q * q + F(1, 4)
    out["w_prime_bound_2mr"] = max(avg_abs(q) for q in xs) == 2
    # (8)-(10): u = 2/k + 2/k^2 <= 24/121, m u = (1 + 6/k + 5/k^2)/4 <= 48/121 for k >= 11.
    uk = lambda kk: F(2, kk) + F(2, kk * kk)
    mu = lambda kk: F(kk + 5, 8) * uk(kk)
    out["u_at_11_is_24_over_121"] = uk(11) == F(24, 121)
    out["mu_identity_and_value_48_over_121"] = all(
        mu(kk) == (1 + F(6, kk) + F(5, kk * kk)) / 4 for kk in range(11, 200)) and mu(11) == F(48, 121)
    out["u_and_mu_decrease_for_k_ge_11"] = all(
        uk(kk + 1) < uk(kk) and mu(kk + 1) < mu(kk) for kk in range(11, 400))
    # (12)
    u0, mu0 = F(24, 121), F(48, 121)
    adverse = mu0 * (3 + 3 * u0 + u0 * u0)
    Fpp = F(7, 4) - adverse
    out["adverse_2554128_over_1771561"] = adverse == F(2554128, 1771561)
    out["F2_lower_2184415_over_7086244_gt_quarter"] = Fpp == F(2184415, 7086244) and Fpp > F(1, 4)
    # (13)
    b = P.v("b")
    q8 = (x - a_) * (x - c_) * F(1, 8)
    left = q8.integrate("x", -2 * R, a_)
    right = q8.integrate("x", c_, 2 * R)
    sgap = b - R ** 3 * F(1, 6)
    out["longitudinal_9r^3_over_32_both_sides"] = (
        (left - R ** 3 * F(9, 32)).is_zero() and (right - R ** 3 * F(9, 32)).is_zero())
    out["b_minus_9_32_equals_s_minus_11_96"] = (
        (b - R ** 3 * F(9, 32)) - (sgap - R ** 3 * F(11, 96))).is_zero() and (
        (sgap + R ** 3 * F(9, 32)) - (b + R ** 3 * F(11, 96))).is_zero()
    out["q8_second_derivative_quarter"] = (q8.d("x").d("x") - F(1, 4)).is_zero()
    # (14): ||y-h|| > 2r - 2r/11 = 20r/11; (delta/2)(20r/11)^2 > 11 r (400/121) r^2 = 4400 r^3/121 > r^3/6.
    radial = F(22, 2) * F(20, 11) ** 2
    out["radial_4400_over_121_gt_one_sixth"] = (
        2 - F(2, 11) == F(20, 11) and radial == F(4400, 121) and radial > F(1, 6))
    # Kappa rescaling f -> f/(6 kappa).
    kap = F(7, 3)
    out["kappa_rescaling"] = (
        F(8) / (6 * kap) == F(4, 3) / kap and 6 * kap / 20 == 3 * kap / 10
        and 6 * kap * F(1, 4) == 3 * kap / 2 and 6 * kap * F(9, 32) == 27 * kap / 16
        and 6 * kap * F(11, 96) == 11 * kap / 16 and 6 * kap * F(4400, 121) == F(26400, 121) * kap)
    # Parent G_r uses exactly the rescaled constants, and D = 4K^2/(3 k_-).
    out["parent_G_r_constants_match_cap"] = F(4, 3) == F(8, 6) and F(3, 10) == F(6, 20)
    # (11): F'' = f_xxx + 3 f_xxy[h'] + 3 f_xyy[h',h'] + f_yyy[h',h',h'] on the ridge,
    # checked on a family with explicitly known ridge y = q(x), for m = 1 and m = 2.
    c3 = 2 if mut == "ridge-coefficient" else 3
    out["ridge_third_derivative_identity_m1"] = _ridge_identity_m1(c3)
    out["ridge_third_derivative_identity_m2"] = _ridge_identity_m2(c3)
    return out


def _poly_x(coeffs):
    x = P.v("x")
    return sum((F(cf) * x ** i for i, cf in enumerate(coeffs)), P())


def _ridge_identity_m1(c3):
    y = P.v("y")
    A = _poly_x([1, -2, 3, 5, -1, 2])
    C = _poly_x([3, 1, -2])
    q = _poly_x([0, F(1, 2), -3, 1])
    e = _poly_x([2, -1])
    g = _poly_x([-1, 3])
    z = y - q
    f = A - C * z * z * F(1, 2) + e * z ** 3 + g * z ** 4
    on = lambda p: p.subs("y", q)
    # The ridge is y = q(x): f_y vanishes there.
    if not on(f.d("y")).is_zero():
        return False
    Fx = on(f.d("x"))
    lhs = Fx.d("x").d("x")
    hp = q.d("x")
    fx3 = on(f.d("x").d("x").d("x"))
    fxxy = on(f.d("x").d("x").d("y"))
    fxyy = on(f.d("x").d("y").d("y"))
    fyyy = on(f.d("y").d("y").d("y"))
    rhs = fx3 + c3 * fxxy * hp + c3 * fxyy * hp * hp + fyyy * hp ** 3
    return (lhs - rhs).is_zero() and not (lhs - on(f.d("x").d("x").d("x"))).is_zero()


def _ridge_identity_m2(c3):
    y1, y2 = P.v("y1"), P.v("y2")
    A = _poly_x([0, 1, -1, 2, 1])
    q1 = _poly_x([0, 1, -2])
    q2 = _poly_x([0, -1, 0, 1])
    C11, C12, C22 = _poly_x([2, 1]), _poly_x([F(1, 2), -1]), _poly_x([3, 0, 1])
    z1, z2 = y1 - q1, y2 - q2
    f = A - (C11 * z1 * z1 + 2 * C12 * z1 * z2 + C22 * z2 * z2) * F(1, 2)
    f = f + _poly_x([1, 1]) * z1 ** 3 + _poly_x([-2]) * z1 * z1 * z2 + _poly_x([0, 3]) * z1 * z2 * z2 \
        + _poly_x([1]) * z2 ** 3 + _poly_x([1, 0, 1]) * z1 * z1 * z2 * z2
    on = lambda p: p.subs("y1", q1).subs("y2", q2)
    if not (on(f.d("y1")).is_zero() and on(f.d("y2")).is_zero()):
        return False
    lhs = on(f.d("x")).d("x").d("x")
    hp = [q1.d("x"), q2.d("x")]
    ys = ["y1", "y2"]
    rhs = on(f.d("x").d("x").d("x"))
    for i in range(2):
        rhs = rhs + c3 * on(f.d("x").d("x").d(ys[i])) * hp[i]
    for i in range(2):
        for j in range(2):
            rhs = rhs + c3 * on(f.d("x").d(ys[i]).d(ys[j])) * hp[i] * hp[j]
    for i in range(2):
        for j in range(2):
            for l in range(2):
                rhs = rhs + on(f.d(ys[i]).d(ys[j]).d(ys[l])) * hp[i] * hp[j] * hp[l]
    return (lhs - rhs).is_zero()


# --------------------------------------------------------------------------
# P: exact falsification probe of (6.1)/(6.2)
# --------------------------------------------------------------------------

def mat_mul(A, B):
    n, k, m = len(A), len(B), len(B[0])
    return [[sum((A[i][l] * B[l][j] for l in range(k)), F(0)) for j in range(m)] for i in range(n)]


def mat_T(A):
    return [list(r) for r in zip(*A)]


def mat_inv(A):
    n = len(A)
    M = [list(A[i]) + [F(int(i == j)) for j in range(n)] for i in range(n)]
    for col in range(n):
        piv = next(i for i in range(col, n) if M[i][col] != 0)
        M[col], M[piv] = M[piv], M[col]
        pv = M[col][col]
        M[col] = [v / pv for v in M[col]]
        for i in range(n):
            if i != col and M[i][col] != 0:
                fac = M[i][col]
                M[i] = [vi - fac * vc for vi, vc in zip(M[i], M[col])]
    return [row[n:] for row in M]


def fdet(A):
    n = len(A)
    M = [list(r) for r in A]
    d = F(1)
    for col in range(n):
        piv = next((i for i in range(col, n) if M[i][col] != 0), None)
        if piv is None:
            return F(0)
        if piv != col:
            M[col], M[piv] = M[piv], M[col]
            d = -d
        d *= M[col][col]
        for i in range(col + 1, n):
            fac = M[i][col] / M[col][col]
            M[i] = [vi - fac * vc for vi, vc in zip(M[i], M[col])]
    return d


def cayley(rng, m):
    """Rational orthogonal matrix (I-K)(I+K)^-1 from a random rational skew K."""
    Km = [[F(0)] * m for _ in range(m)]
    for i in range(m):
        for j in range(i + 1, m):
            v = F(rng.randrange(-9, 10), rng.randrange(1, 7))
            Km[i][j], Km[j][i] = v, -v
    I = [[F(int(i == j)) for j in range(m)] for i in range(m)]
    Im = [[I[i][j] - Km[i][j] for j in range(m)] for i in range(m)]
    Ip = [[I[i][j] + Km[i][j] for j in range(m)] for i in range(m)]
    return mat_mul(Im, mat_inv(Ip))


def rational_unit(rng, m):
    if m == 1:
        return [F(rng.choice((-1, 1)))]
    if m == 2:
        tq = F(rng.randrange(-20, 21), rng.randrange(1, 9))
        n = 1 + tq * tq
        return [(1 - tq * tq) / n, 2 * tq / n]
    u = F(rng.randrange(-20, 21), rng.randrange(1, 9))
    w = F(rng.randrange(-20, 21), rng.randrange(1, 9))
    n = 1 + u * u + w * w
    return [2 * u / n, 2 * w / n, (1 - u * u - w * w) / n]


def neg_definite(H):
    n = len(H)
    return all(fdet([[-H[i][j] for j in range(k)] for i in range(k)]) > 0 for k in range(1, n + 1))


def bordered(r, al, be, A):
    m = len(be)
    H = [[r * al] + [r * be[j] for j in range(m)]]
    for i in range(m):
        H.append([r * be[i]] + list(A[i]))
    return H


def probe(mut):
    rng = random.Random(61622026)
    pivot = F(1, 4) if mut == "pivot-quarter" else F(1, 2)
    mixed = F(1) if mut == "mixed-square" else F(3, 2)
    shift = 0 if mut == "no-shift" else 1
    stats = {}
    all_ok = True
    for m in (1, 2, 3):
        n_typed = n_total = eq61 = eq62 = viol = 0
        for trial in range(700):
            extremal = trial % 7 == 0
            r = F(1, rng.choice((2, 3, 5, 10, 50)))
            h = F(rng.randrange(1, 60), rng.randrange(1, 9))
            lam = sorted(F(rng.randrange(1, 300), rng.randrange(1, 30)) for _ in range(m))
            O = cayley(rng, m)
            B = mat_mul(mat_mul(O, [[lam[i] if i == j else F(0) for j in range(m)] for i in range(m)]), mat_T(O))
            AM = [[-v for v in row] for row in B]
            v1 = [O[i][0] for i in range(m)]  # unit eigenvector of B for lam[0]
            if extremal:
                alM, beM = -h / 2, [F(0)] * m
                alS = h / 2
                beS = [h / 2 * vi for vi in v1]
                AS = [[AM[i][j] - (r * h if i == j else 0) for j in range(m)] for i in range(m)]
            else:
                alM = -h / 2 * F(rng.randrange(1, 101), 100)
                alS = h / 2 * F(rng.randrange(-100, 101), 100)
                beM = [h / 2 * F(rng.randrange(0, 101), 100) * vi for vi in rational_unit(rng, m)]
                beS = [h / 2 * F(rng.randrange(0, 101), 100) * vi for vi in rational_unit(rng, m)]
                O2 = cayley(rng, m)
                e = [r * h * F(rng.randrange(-100, 101), 100) for _ in range(m)]
                Ed = mat_mul(mat_mul(O2, [[e[i] if i == j else F(0) for j in range(m)] for i in range(m)]), mat_T(O2))
                AS = [[AM[i][j] + Ed[i][j] for j in range(m)] for i in range(m)]
            HM, HS = bordered(r, alM, beM, AM), bordered(r, alS, beS, AS)
            dM, dS = abs(fdet(HM)), abs(fdet(HS))
            detB = F(1)
            for lv in lam:
                detB *= lv
            tail = F(1)
            tailW = F(1)
            for lv in lam[1:]:
                tail *= lv + shift * r * h
                tailW *= lv * (lv + shift * r * h)
            bS = r * h / 2 * (lam[0] + mixed * r * h) * tail
            n_total += 1
            if dS > bS:
                viol += 1
            if dS == bS:
                eq62 += 1
            if neg_definite(HM):
                n_typed += 1
                bM = r * pivot * h * detB
                if dM > bM or dM > r * abs(alM) * detB:
                    viol += 1
                if dM == bM:
                    eq61 += 1
                bW = r * r * h * h / 4 * lam[0] * (lam[0] + mixed * r * h) * tailW
                if mut == "pivot-quarter":
                    bW = bW / 2
                if dM * dS > bW:
                    viol += 1
        stats["m%d" % m] = {"instances": n_total, "typed_maxima": n_typed,
                            "equality_6.1": eq61, "equality_6.2_saddle": eq62, "violations": viol}
        all_ok &= viol == 0
    return all_ok, stats


# --------------------------------------------------------------------------

MUTANTS = ("u3-row", "bordered-det", "mixed-square", "drop-far-branch", "ridge-coefficient",
           "pivot-quarter", "no-shift")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mutant", choices=MUTANTS)
    args = ap.parse_args()
    mut = args.mutant
    groups = {
        "A2_contact_frame": check_a2(mut),
        "A3_endpoint_and_erratum": check_a3(mut),
        "A5_A6_typed_weight_algebra": check_a5_a6(mut),
        "A7_boundary_layer": check_a7(mut),
        "CAP_marked_cylinder": check_cap(mut),
    }
    probe_ok, probe_stats = probe(mut)
    passed = all(all(v for v in g.values()) for g in groups.values()) and probe_ok
    result = {
        "checks": groups,
        "probe_6.1_6.2_exact": {"passed": probe_ok, "by_m": probe_stats},
        "passed": passed,
        "scientific_effect": "NONE",
        "scope": "exact identities and constants only; Gaussian steps are argued in REVIEW.md",
    }
    sys.stdout.write(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
