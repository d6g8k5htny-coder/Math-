"""80-digit Gaussian Schur diagnostic for the D5 obstruction ledger (stdlib only).

Planar Bargmann-Fock field, covariance K(x, y) = exp(-|x - y|^2 / 2).
Pins: the six endpoint pins f(M) = b, f(S) = b - k r^3, grad f(M) = grad f(S) = 0
with M = (0, 0), S = (r, 0) (axis t, transverse s), optionally extended by the
witness gradient pins grad f(X) = 0 at X = M + r (0, q) (the on-axis slice p = 0).

For each second jet at M and S the script prints the conditional mean and
variance under the six-pin and eight-pin laws. It also cross-checks the direct
Schur complement against the closed forms of CLOSED_FORMS_FTS_FTT.md.

This is a finite diagnostic at fixed (b, k, q, r). It is numerical corroboration
of conditional-moment scales, not a proof of any uniform statement.

    python -B -S incoming/grok-cycle4-20260926/harper/schur_diagnostic.py
    python -B -S incoming/grok-cycle4-20260926/harper/schur_diagnostic.py --mutate
"""
from __future__ import annotations

import sys
from decimal import Decimal as D, getcontext

getcontext().prec = 80

MUTATE = False  # negative control: wrong sign for odd-order covariances


class CheckError(Exception):
    pass


def check(cond: bool, msg: str) -> None:
    if not cond:
        raise CheckError(msg)


def hermite(n: int, x: D) -> D:
    """Probabilists' Hermite polynomial He_n(x)."""
    if n == 0:
        return D(1)
    a, b = D(1), x
    for m in range(1, n):
        a, b = b, x * b - m * a
    return b


Jet = tuple[tuple[int, int], tuple[D, D]]  # ((order_t, order_s), (t, s))


def cov(fa: Jet, fb: Jet) -> D:
    """Cov(d^a f(x), d^b f(y)) = (-1)^{|a|} He_{a1+b1}(u1) He_{a2+b2}(u2) e^{-|u|^2/2}, u = x - y."""
    (a1, a2), (x1, x2) = fa
    (b1, b2), (y1, y2) = fb
    u1, u2 = x1 - y1, x2 - y2
    parity = (a1 + a2) % 2
    sign = D(1) if (parity == 0) == (not MUTATE) else D(-1)
    return sign * hermite(a1 + b1, u1) * hermite(a2 + b2, u2) * (-(u1 * u1 + u2 * u2) / 2).exp()


def solve(A: list[list[D]], B: list[list[D]]) -> list[list[D]]:
    n = len(A)
    M = [row[:] + b[:] for row, b in zip(A, B)]
    m = len(B[0])
    for i in range(n):
        piv = max(range(i, n), key=lambda r: abs(M[r][i]))
        M[i], M[piv] = M[piv], M[i]
        check(M[i][i] != 0, 'singular pin Gram')
        for r in range(n):
            if r != i:
                f = M[r][i] / M[i][i]
                for c in range(i, n + m):
                    M[r][c] -= f * M[i][c]
    return [[M[i][n + j] / M[i][i] for j in range(m)] for i in range(n)]


TARGETS = ('f_tt(M)', 'f_ts(M)', 'f_ss(M)', 'f_tss(M)', 'f_tt(S)', 'f_ts(S)', 'f_ss(S)')


def conditional(r: D, b: D, k: D, q: D, witness: bool) -> dict[str, tuple[D, D]]:
    """Conditional (mean, variance) of the second jets given the pins."""
    zero = D(0)
    M_, S_, X_ = (zero, zero), (r, zero), (zero, r * q)
    pins: list[Jet] = [((0, 0), M_), ((0, 0), S_), ((1, 0), M_), ((0, 1), M_), ((1, 0), S_), ((0, 1), S_)]
    vals = [b, b - k * r ** 3, zero, zero, zero, zero]
    if witness:
        pins += [((1, 0), X_), ((0, 1), X_)]
        vals += [zero, zero]
    gram = [[cov(p, p2) for p2 in pins] for p in pins]
    jets: dict[str, Jet] = {
        'f_tt(M)': ((2, 0), M_), 'f_ts(M)': ((1, 1), M_), 'f_ss(M)': ((0, 2), M_), 'f_tss(M)': ((1, 2), M_),
        'f_tt(S)': ((2, 0), S_), 'f_ts(S)': ((1, 1), S_), 'f_ss(S)': ((0, 2), S_)}
    out = {}
    for name in TARGETS:
        tg = jets[name]
        c = [[cov(tg, p)] for p in pins]
        w = solve(gram, c)
        mean = sum((w[i][0] * vals[i] for i in range(len(pins))), zero)
        var = cov(tg, tg) - sum((w[i][0] * c[i][0] for i in range(len(pins))), zero)
        out[name] = (mean, var)
    return out


def closed_form_var_ftt(r: D) -> D:
    """Identity TT of CLOSED_FORMS_FTS_FTT.md."""
    E = (r * r).exp()
    r2, r4, r6 = r * r, r ** 4, r ** 6
    num = r6 * E - r4 * E - r4 + 4 * r2 * E - 4 * r2 - 2 * E * E + 4 * E - 2
    den = r4 * E - (E - 1) ** 2
    return num / den


def closed_form_var_fts(r: D) -> D:
    """Identity TS of CLOSED_FORMS_FTS_FTT.md."""
    E = (r * r).exp()
    return (E - 1 - r * r) / (E - 1)


def mean_series_M(r: D, b: D, k: D) -> D:
    """E[f_tt(M) | six pins] through r^8, as displayed in D5_OBSTRUCTION_LEDGER.md Section 4
    and derived by exact series division in test_ftt_conditional_mean.py."""
    return (-6 * k * r - b / 4 * r ** 2 + k * r ** 3 + b / 24 * r ** 4 - k / 20 * r ** 5
            - b / 192 * r ** 6 - k / 120 * r ** 7 + b / 5760 * r ** 8)


def mean_series_S(r: D, b: D, k: D) -> D:
    """E[f_tt(S) | six pins] through r^8 (same source)."""
    return (6 * k * r - b / 4 * r ** 2 - k * r ** 3 + b / 24 * r ** 4 + D(3) / 10 * k * r ** 5
            - b / 192 * r ** 6 - k / 30 * r ** 7 + b / 5760 * r ** 8)


def run_checks(b: D, k: D, q: D, radii: tuple[str, ...]) -> list[str]:
    lines = []
    tol = D(10) ** -60
    for rs in radii:
        r = D(rs)
        six = conditional(r, b, k, q, False)
        eight = conditional(r, b, k, q, True)
        # Independent cross-check of the exact conditional-mean series (series division vs direct 80-digit Schur).
        check(abs(six['f_tt(M)'][0] - mean_series_M(r, b, k)) < 2 * r ** 9, 'E[f_tt(M)|6 pins] differs from its series through r^8 at r=' + rs)
        check(abs(six['f_tt(S)'][0] - mean_series_S(r, b, k)) < 2 * r ** 9, 'E[f_tt(S)|6 pins] differs from its series through r^8 at r=' + rs)
        # Cross-check: direct Schur complement against the closed forms (six pins).
        check(abs(six['f_tt(M)'][1] - closed_form_var_ftt(r)) < tol, 'Var(f_tt(M)|6 pins) differs from Identity TT at r=' + rs)
        check(abs(six['f_ts(M)'][1] - closed_form_var_fts(r)) < tol, 'Var(f_ts(M)|6 pins) differs from Identity TS at r=' + rs)
        # The witness gradient pins are odd/even mixed at a displaced point; they must not change f_tt(M).
        check(abs(six['f_tt(M)'][1] - eight['f_tt(M)'][1]) < tol, 'witness pins changed Var(f_tt(M))')
        mtt, vtt = eight['f_tt(M)']
        # Fluctuation scale of f_tt(M): Var/r^4 within the series prefix r^4/6 - r^6/30 + r^8/360 (tolerance r^10).
        series = r ** 4 / 6 - r ** 6 / 30 + r ** 8 / 360
        check(abs(vtt - series) < r ** 10, 'Var(f_tt(M)) off the TT series prefix at r=' + rs)
        # Mean correction of f_tt(M) is order r^2 (not r^3): |E + 6kr| / r^2 stays bounded and is not o(r) unless b = 0.
        corr = (mtt + 6 * k * r) / (r * r)
        check(abs(corr) <= abs(b) / 2 + D(1) / 10 + k * r, 'mean correction of f_tt(M) exceeds (|b|/2 + 1/10 + k r) r^2 at r=' + rs)
        # Eight-pin law: f_ss(M) = O_p(r |q|) with Var -> (3/2) r^2 q^2; f_ss(S) = O_p(r) with Var -> 2 r^2.
        mM, vM = eight['f_ss(M)']
        check(abs(vM / (r * r * q * q) - D(3) / 2) < D(1) / 100, 'Var(f_ss(M)|8 pins) not ~ (3/2) r^2 q^2 at r=' + rs)
        mS, vS = eight['f_ss(S)']
        check(D('1.9') < vS / (r * r) < D('2.0'), 'Var(f_ss(S)|8 pins)/r^2 outside (1.9, 2.0) at r=' + rs)
        check(abs(mS) <= (abs(b) / 2 + D(1) / 10) * r * r + k * r ** 3, 'E[f_ss(S)|8 pins] not O((|b|/2) r^2) at r=' + rs)
        mts, vts = eight['f_ts(S)']
        check(vts < D(1) / 10 * r * r, 'Var(f_ts(S)|8 pins) not O(r^2) at r=' + rs)
        # Six-pin law alone: f_ss(S) is order one (mean -> -b, Var -> 2). This is the coarse bound the ledger v1 used.
        check(abs(six['f_ss(S)'][1] - 2) < D(1) / 100 and abs(six['f_ss(S)'][0] + b) < D(1) / 10, 'six-pin f_ss(S) not order one at r=' + rs)
        lines.append(
            f"r={rs}: Var(f_tt(M))/r^4={float(vtt / r ** 4):.10f}  (E[f_tt(M)]+6kr)/r^2={float(corr):+.5f}  "
            f"8-pin: Var(f_ss(M))/(r^2 q^2)={float(vM / (r * r * q * q)):.5f}  Var(f_ss(S))/r^2={float(vS / (r * r)):.5f}  "
            f"E[f_ss(S)]/r^2={float(mS / (r * r)):+.5f}  Var(f_ts(S))/r^2={float(vts / (r * r)):.5f}  "
            f"6-pin: Var(f_ss(S))={float(six['f_ss(S)'][1]):.5f} E[f_ss(S)]={float(six['f_ss(S)'][0]):+.5f}")
    return lines


def main(argv: list[str]) -> int:
    global MUTATE
    MUTATE = '--mutate' in argv
    b, k, q = D(1), D(6) / D(5), D(1) / D(5)
    radii = ('0.1', '0.05', '0.025', '0.0125')
    try:
        lines = run_checks(b, k, q, radii)
    except CheckError as exc:
        print('FAIL: ' + str(exc) + (' (mutation detected, as required)' if MUTATE else ''))
        return 1
    if MUTATE:
        print('FAIL: mutation was not detected')
        return 2
    print('\n'.join(lines))
    print('SCHUR_DIAGNOSTIC_PASSED: direct 80-digit Schur matches Identities TS/TT; six-pin f_tt(M) fluctuation O_p(r^2) '
          'with mean correction O(b r^2); eight-pin f_ss(M)=O_p(r|q|), f_ss(S)=O_p(r), f_ts(S)=O_p(r). '
          'Finite diagnostic at b=1, k=6/5, q=1/5; not a uniform theorem.')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
