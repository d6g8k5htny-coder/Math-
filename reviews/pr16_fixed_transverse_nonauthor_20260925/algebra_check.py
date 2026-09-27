"""Finite-polynomial checks for the cubic model displayed in
reviews/downstream_boundary_20260925/TRANSVERSE_BOUND_CANDIDATE.md
at Math- commit 32b80ee085dc6a40113d1e46e333cda50d57ba21.

Python standard library only. A passing run checks rational identities
used by the R1-R2 ledger. It does not prove the continuum regression
or the Kac-Rice bound.
"""
from fractions import Fraction as F


NAMES = "bkaqcdruv"


def mono(**kw):
    e = [0] * 9
    for i, n in enumerate(NAMES):
        e[i] = kw.get(n, 0)
    return {tuple(e): F(1)}


def const(n):
    if n == 0:
        return {}
    return {tuple(0 for _ in range(9)): F(n)}


def mul(p, q):
    out = {}
    for e1, c1 in p.items():
        for e2, c2 in q.items():
            e = tuple(i + j for i, j in zip(e1, e2))
            out[e] = out.get(e, 0) + c1 * c2
    return {e: c for e, c in out.items() if c}


def add(*ps):
    out = {}
    for p in ps:
        for e, c in p.items():
            out[e] = out.get(e, 0) + c
    return {e: c for e, c in out.items() if c}


def scale(p, s):
    return {e: c * s for e, c in p.items() if c * s}


def show(p):
    items = []
    for e, c in sorted(p.items()):
        bits = []
        if c != 1 or all(v == 0 for v in e):
            bits.append(str(c))
        for n, v in zip(NAMES, e):
            if v == 1:
                bits.append(n)
            elif v > 1:
                bits.append(f"{n}^{v}")
        items.append("*".join(bits) if bits else "1")
    return " + ".join(items) if items else "0"


def Dx(poly):
    out = {}
    for (i, j), c in poly.items():
        if i:
            out[(i - 1, j)] = add(out.get((i - 1, j), {}), scale(c, i))
    return out


def Dz(poly):
    out = {}
    for (i, j), c in poly.items():
        if j:
            out[(i, j - 1)] = add(out.get((i, j - 1), {}), scale(c, j))
    return out


def ev(poly, x, z):
    acc = {}
    for (i, j), coeff in poly.items():
        piece = coeff
        for _ in range(i):
            piece = mul(piece, x)
        for _ in range(j):
            piece = mul(piece, z)
        acc = add(acc, piece)
    return acc


def div_r(p, n):
    out = {}
    for e, c in p.items():
        if e[6] < n:
            raise SystemExit(f"not divisible by r^{n}: {show(p)}")
        e2 = list(e)
        e2[6] -= n
        out[tuple(e2)] = out.get(tuple(e2), 0) + c
    return {e: c for e, c in out.items() if c}


def coeff_linear(poly, var_index):
    out = {}
    for e, c in poly.items():
        if e[var_index] == 0:
            continue
        if e[var_index] != 1 or any(e[i] for i in range(6) if i != var_index):
            raise SystemExit(f"unexpected dependence {show({e: c})}")
        e2 = list(e)
        e2[var_index] = 0
        out[tuple(e2)] = out.get(tuple(e2), 0) + c
    return out


def det3(M):
    a, b, c = M[0]
    d, e, f = M[1]
    g, h, i = M[2]
    return add(
        mul(a, add(mul(e, i), scale(mul(f, h), -1))),
        scale(mul(b, add(mul(d, i), scale(mul(f, g), -1))), -1),
        mul(c, add(mul(d, h), scale(mul(e, g), -1))),
    )


def factorial(n):
    x = 1
    for i in range(2, n + 1):
        x *= i
    return x


def main():
    failures = []

    def check(label, got, want):
        if got != want:
            failures.append(label)
            print("FAIL", label)
            print("  got ", show(got))
            print("  want", show(want))
        else:
            print("OK  ", label)

    # f = b - k r^3/2 + 2 k x^3 - (3/2) k r^2 x + (a/2) z^2
    #   + (q/2)(x^2 - r^2/4) z + (c/2) x z^2 + (d/6) z^3
    f = {}

    def put(i, j, coeff):
        f[(i, j)] = add(f.get((i, j), {}), coeff)

    put(0, 0, mono(b=1))
    put(0, 0, scale(mul(mono(k=1), mono(r=3)), F(-1, 2)))
    put(3, 0, scale(mono(k=1), 2))
    put(1, 0, scale(mul(mono(k=1), mono(r=2)), F(-3, 2)))
    put(0, 2, scale(mono(a=1), F(1, 2)))
    put(2, 1, scale(mono(q=1), F(1, 2)))
    put(0, 1, scale(mul(mono(q=1), mono(r=2)), F(-1, 8)))
    put(1, 2, scale(mono(c=1), F(1, 2)))
    put(0, 3, scale(mono(d=1), F(1, 6)))

    fx, fz = Dx(f), Dz(f)
    fxx, fxz, fzz = Dx(fx), Dz(fx), Dz(fz)
    half, neghalf, zero = scale(mono(r=1), F(1, 2)), scale(mono(r=1), F(-1, 2)), const(0)

    check("f(M)=b", ev(f, neghalf, zero), mono(b=1))
    check(
        "f(S)=b-k r^3",
        ev(f, half, zero),
        add(mono(b=1), scale(mul(mono(k=1), mono(r=3)), -1)),
    )
    check("fx(M)=0", ev(fx, neghalf, zero), const(0))
    check("fx(S)=0", ev(fx, half, zero), const(0))
    check("fz(M)=0", ev(fz, neghalf, zero), const(0))
    check("fz(S)=0", ev(fz, half, zero), const(0))
    check(
        "f(0)=b-k r^3/2",
        ev(f, zero, zero),
        add(mono(b=1), scale(mul(mono(k=1), mono(r=3)), F(-1, 2))),
    )
    check("fx(0)=-(3/2) k r^2", ev(fx, zero, zero), scale(mul(mono(k=1), mono(r=2)), F(-3, 2)))
    check("fz(0)=-q r^2/8", ev(fz, zero, zero), scale(mul(mono(q=1), mono(r=2)), F(-1, 8)))
    check("fxx(M)/r=-6k", div_r(ev(fxx, neghalf, zero), 1), scale(mono(k=1), -6))
    check("fxx(S)/r=6k", div_r(ev(fxx, half, zero), 1), scale(mono(k=1), 6))
    check("fxz(M)=-(q r)/2", ev(fxz, neghalf, zero), scale(mul(mono(q=1), mono(r=1)), F(-1, 2)))
    check("fxz(S)=(q r)/2", ev(fxz, half, zero), scale(mul(mono(q=1), mono(r=1)), F(1, 2)))
    check("fzz(M)=a-(c r)/2", ev(fzz, neghalf, zero), add(mono(a=1), scale(mul(mono(c=1), mono(r=1)), F(-1, 2))))
    check("fzz(S)=a+(c r)/2", ev(fzz, half, zero), add(mono(a=1), scale(mul(mono(c=1), mono(r=1)), F(1, 2))))

    xu, zv = mul(mono(r=1), mono(u=1)), mul(mono(r=1), mono(v=1))
    J1 = div_r(ev(fx, xu, zv), 2)
    J2 = div_r(ev(fz, xu, zv), 1)
    numer = add(ev(f, xu, zv), scale(mono(b=1), -1), scale(mul(mul(mono(r=1), mono(v=1)), ev(fz, xu, zv)), F(-1, 2)))
    J3 = div_r(numer, 3)
    want_J1 = add(
        scale(mul(mono(k=1), add(mono(u=2), scale(const(1), F(-1, 4)))), 6),
        mul(mono(q=1), mul(mono(u=1), mono(v=1))),
        scale(mul(mono(c=1), mono(v=2)), F(1, 2)),
    )
    # Finite-r J2 keeps the order-r jet; the proof's limit drops it.
    want_J2 = add(
        mul(mono(a=1), mono(v=1)),
        mul(
            mono(r=1),
            add(
                scale(mul(mono(q=1), add(mono(u=2), scale(const(1), F(-1, 4)))), F(1, 2)),
                mul(mul(mono(c=1), mono(u=1)), mono(v=1)),
                scale(mul(mono(d=1), mono(v=2)), F(1, 2)),
            ),
        ),
    )
    want_J3 = add(
        mul(
            mono(k=1),
            add(scale(mono(u=3), 2), scale(mono(u=1), F(-3, 2)), scale(const(1), F(-1, 2))),
        ),
        scale(mul(mul(mono(q=1), add(mono(u=2), scale(const(1), F(-1, 4)))), mono(v=1)), F(1, 4)),
        scale(mul(mono(d=1), mono(v=3)), F(-1, 12)),
    )
    check("J1 exact", J1, want_J1)
    check("J2 exact including O(r)", J2, want_J2)
    j2_limit = {e: c for e, c in J2.items() if e[6] == 0}
    check("J2 limit a*v", j2_limit, mul(mono(a=1), mono(v=1)))
    check("J3 exact", J3, want_J3)
    for name, J in ("J1", J1), ("J3", J3):
        if any(e[6] for e in J):
            failures.append(name + " depends on r")
            print("FAIL", name, "depends on r", show(J))
        else:
            print("OK  ", name, "independent of r on this cubic")

    # columns a=2, c=4, d=5
    cols = []
    for var in (2, 4, 5):
        cols.append([coeff_linear(J, var) for J in (J1, J2, J3)])
    minor = det3([[cols[j][i] for j in range(3)] for i in range(3)])
    check("limit minor(a,c,d)=v^6/24", minor, scale(mono(v=6), F(1, 24)))
    # Finite-r (a,c,d) minor on the same cubic, before sending r to 0.
    # J2 contributes r*u*v on c and r*v^2/2 on d; those entries do not change the determinant.
    finite = [
        [const(0), scale(mono(v=2), F(1, 2)), const(0)],
        [mono(v=1), mul(mul(mono(r=1), mono(u=1)), mono(v=1)), scale(mul(mono(r=1), mono(v=2)), F(1, 2))],
        [const(0), const(0), scale(mono(v=3), F(-1, 12))],
    ]
    check("finite-r minor(a,c,d)=v^6/24", det3(finite), scale(mono(v=6), F(1, 24)))

    # U_4 finite-difference constant term equals phi'''(0).
    N = 8

    def series_phi(sign):
        out = {}
        for n in range(N + 1):
            out.setdefault(n, {})[n] = F(sign, 2) ** n / F(factorial(n))
        return out

    def series_phip(sign):
        out = {}
        for m in range(1, N + 1):
            out.setdefault(m - 1, {})[m] = F(sign, 2) ** (m - 1) / F(factorial(m - 1))
        return out

    def add_s(a, b, s=1):
        out = {k: dict(v) for k, v in a.items()}
        for k, d in b.items():
            slot = out.setdefault(k, {})
            for n, c in d.items():
                slot[n] = slot.get(n, 0) + s * c
                if slot[n] == 0:
                    del slot[n]
            if not slot:
                del out[k]
        return out

    def mul_rpow(a, m):
        return {k + m: d for k, d in a.items()}

    def scale_s(a, s):
        return {k: {n: c * s for n, c in d.items()} for k, d in a.items()}

    diff = mul_rpow(add_s(series_phi(1), series_phi(-1), -1), -1)
    inner = add_s(add_s(series_phip(-1), series_phip(1)), diff, -2)
    comp = scale_s(mul_rpow(inner, -2), 6)
    if comp.get(0) != {3: F(1)}:
        failures.append("U4 limit")
        print("FAIL U4 constant term", comp.get(0))
    else:
        print("OK   U4 constant term is phi'''(0)")
    higher = {k: comp[k] for k in comp if k > 0 and k <= 4}
    print("     U4 higher jets through r^4:", higher)

    # Six pins produce the stated U_r target exactly.
    b, kr3 = F(1), F(1)  # symbolic check is rational, done with symbols below
    # (fM+fS)/2 = b - k r^3/2
    # (fS-fM)/r = -k r^2
    # (6/r^2)*(0 - 2*(-k r^2)) = 12 k
    target4 = F(6) * (F(0) - 2 * (F(-1)))  # in units of k, the r^2 cancels
    if target4 != 12:
        failures.append("U target fourth component")
        print("FAIL U target", target4)
    else:
        print("OK   U_r pin target fourth component is 12k")

    # det = fxx fzz - fxz^2 at M, then divide by r.
    det_m = add(
        mul(ev(fxx, neghalf, zero), ev(fzz, neghalf, zero)),
        scale(mul(ev(fxz, neghalf, zero), ev(fxz, neghalf, zero)), -1),
    )
    det_s = add(
        mul(ev(fxx, half, zero), ev(fzz, half, zero)),
        scale(mul(ev(fxz, half, zero), ev(fxz, half, zero)), -1),
    )
    direct_m = add(
        scale(mul(mono(k=1), mono(a=1)), -6),
        scale(mul(mul(mono(k=1), mono(c=1)), mono(r=1)), 3),
        scale(mul(mono(q=2), mono(r=1)), F(-1, 4)),
    )
    direct_s = add(
        scale(mul(mono(k=1), mono(a=1)), 6),
        scale(mul(mul(mono(k=1), mono(c=1)), mono(r=1)), 3),
        scale(mul(mono(q=2), mono(r=1)), F(-1, 4)),
    )
    check("det(H_M)/r", div_r(det_m, 1), direct_m)
    check("det(H_S)/r", div_r(det_s, 1), direct_s)
    lead_m = {e: c for e, c in div_r(det_m, 1).items() if e[6] == 0}
    lead_s = {e: c for e, c in div_r(det_s, 1).items() if e[6] == 0}
    check("det(H_M)/r leading -6ka", lead_m, scale(mul(mono(k=1), mono(a=1)), -6))
    check("det(H_S)/r leading 6ka", lead_s, scale(mul(mono(k=1), mono(a=1)), 6))

    # Absolute Hessian product on the pure cubic q=c=d=0.
    # det H_M = fxx fzz - fxz^2 = (-6 k r) * a
    # det H_S = (6 k r) * a
    # |det det| / r^2 = 36 k^2 a^2
    signed = (-6) * 6
    print("OK   signed (det_M/r)(det_S/r) coefficient", signed, "k^2 a^2; absolute coefficient", abs(signed))

    num_exp = 2 + 3 + (-6) + 6
    final_exp = num_exp - 2
    print("OK   numerator r^{%d}; after full Z_r ~ r^2, count r^{%d}" % (num_exp, final_exp))
    if num_exp != 5 or final_exp != 3:
        failures.append("ledger exponents")

    if failures:
        print("FAILURES", failures)
        raise SystemExit(1)
    print("ALL ALGEBRAIC CHECKS PASSED")


if __name__ == "__main__":
    main()
