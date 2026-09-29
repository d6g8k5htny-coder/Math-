"""Independent exact checks for the R1/R2 slice of OA-SARD-ROBUST-CHARTS-20260929-v1 (Math-#135 PROOF.md §§3-6, §9).

All arithmetic is exact (fractions). Trigonometric values are used only at quarter periods.
  CLOSED_CONTACT  §9 arc g_eps(t) = ((t-1)(t-2), (t-1)^2 + eps) on [0, 5/2] against Sigma = {0} x [0, 2]. The robust
                  predicate (F1)-(F4) rejects eps = 0 (first closed contact at an endpoint), and its first-contact time
                  is continuous at every accepted eps. The first-interior-hit rule is not continuous at eps = 0.
  EARLY_PREFIX    at eps > 0 the prefix [0, tau - delta] is separated from the CLOSED Sigma (min x = delta(1 + delta));
                  the whole travelled prefix [0, tau] is not.
  TERMINAL_SLACK  g_c(t) = (t - 1 - c, 1/2) on [0, 1]: a terminal-time hit (c = 0) is rejected; with slack the hit
                  continues.
  BR_TORUS        F = sin(2 pi x)(2 - cos 2 pi y): exactly four critical points; the saddles (3/4, 0) and (1/4, 0) are
                  joined along the invariant line y = 0 through (1, 0). The endpoint hit on {1} x [0, 1/200] is rejected;
                  the centred segment {1} x [-1/200, 1/200] gives the continuous hit y = delta under translation.
  IFT             (R1a) on x(t, c) = t^2 - 1 - c at 1 + c = q^2 gives dtau/dc = 1/(2q), matching exact secants.
Mutants (each must fail): relint-rule, whole-prefix, no-terminal-slack, endpoint-accept, sign-flip.
"""
import argparse
import json
import sys
from fractions import Fraction as F

MUTANTS = ("relint-rule", "whole-prefix", "no-terminal-slack", "endpoint-accept", "sign-flip")
MUT = None
TINY = F(1, 10 ** 7)


def continuous_at_accepted(fn, points, lip=2):
    """At each accepted point p, p +/- TINY is accepted with |tau change| <= lip * TINY."""
    ok = True
    for p in points:
        acc, tau = fn(p)
        if not acc:
            continue
        for s in (-TINY, TINY):
            acc2, tau2 = fn(p + s)
            ok &= acc2 and abs(tau2 - tau) <= lip * TINY
    return ok


# ---------- §9 smooth arc against the closed segment {0} x [0, 2] ----------
def eps_arc(eps):
    """(accepted, tau). x(t) = (t-1)(t-2) vanishes on [0, 5/2] exactly at t = 1, 2; x(0) = 2, so g(0) is off Sigma."""
    y = {t: (t - 1) ** 2 + eps for t in (F(1), F(2))}
    if MUT == "relint-rule":
        inner = [t for t in (F(1), F(2)) if 0 < y[t] < 2]
        return (bool(inner), inner[0] if inner else None)
    hits = [t for t in (F(1), F(2)) if 0 <= y[t] <= 2]
    if not hits:
        return (False, None)
    tau = hits[0]
    relint = 0 < y[tau] < 2                      # (F2)
    transverse = 2 * tau - 3 != 0                # (F4): x'(tau)
    slack = 0 < tau < F(5, 2)                    # (F1) launch / terminal slack
    return (relint and transverse and slack, tau)


def interior_rule(eps):
    return next((t for t in (F(1), F(2)) if 0 < (t - 1) ** 2 + eps < 2), None)


def check_closed_contact():
    pts = [F(0)] + [s * F(1, 10 ** k) for k in range(1, 6) for s in (1, -1)]
    ok = continuous_at_accepted(eps_arc, pts)
    ok &= not eps_arc(F(0))[0]
    ok &= all(eps_arc(F(1, 10 ** k)) == (True, F(1)) for k in range(1, 6))
    ok &= all(eps_arc(-F(1, 10 ** k)) == (True, F(2)) for k in range(1, 6))
    ok &= interior_rule(F(0)) == 2 and interior_rule(TINY) == 1       # the rejected rule jumps
    return ok


def check_early_prefix():
    tau, delta = F(1), F(1, 10)
    ok = all(2 * t - 3 < 0 for t in (F(0), F(1, 2), F(1), F(149, 100)))  # x decreasing on [0, 3/2]
    end = tau if MUT == "whole-prefix" else tau - delta
    min_x = (end - 1) * (end - 2)                # min of x on [0, end], end <= 3/2
    return ok and min_x > 0 and min_x == delta * (1 + delta)


# ---------- terminal slack ----------
def terminal(c):
    tau = 1 + c                                  # x(t) = t - 1 - c on [0, 1]; y = 1/2 lies inside [0, 1]
    if not 0 <= tau <= 1:
        return (False, None)
    slack = tau < 1 or MUT == "no-terminal-slack"
    return (slack and tau > 0, tau)


def check_terminal():
    pts = [F(0), F(1, 10)] + [-F(1, 10 ** k) for k in range(1, 6)]
    return continuous_at_accepted(terminal, pts) and not terminal(F(0))[0] and not terminal(TINY)[0]


# ---------- BR torus example ----------
SIN = {F(0): 0, F(1, 4): 1, F(1, 2): 0, F(3, 4): -1}
COS = {F(0): 1, F(1, 4): 0, F(1, 2): -1, F(3, 4): 0}


def br_jet(x, y):
    """grad in units 2 pi and Hessian in units 4 pi^2 of F = sin(2 pi x)(2 - cos 2 pi y) at quarter points."""
    x, y = x % 1, y % 1
    sx, cx, sy, cy = SIN[x], COS[x], SIN[y], COS[y]
    grad = (cx * (2 - cy), sx * sy)
    hess = ((-sx * (2 - cy), cx * sy), (cx * sy, sx * cy))
    return grad, hess


def br_hit(delta, lo, hi):
    """Translated field F(x, y - delta): the connecting orbit is y = delta and crosses x = 1 once, at (1, delta)."""
    if not lo <= delta <= hi:
        return (False, None)
    inside = lo <= delta <= hi if MUT == "endpoint-accept" else lo < delta < hi
    return (inside, delta)


def check_br():
    quarter = [F(k, 4) for k in range(4)]
    crit = {}
    for x in quarter:
        for y in quarter:
            g, h = br_jet(x, y)
            if g == (0, 0):
                det = h[0][0] * h[1][1] - h[0][1] * h[1][0]
                tr = h[0][0] + h[1][1]
                crit[(x, y)] = "saddle" if det < 0 else ("max" if tr < 0 else "min")
    ok = crit == {(F(1, 4), F(0)): "saddle", (F(3, 4), F(0)): "saddle",
                  (F(1, 4), F(1, 2)): "max", (F(3, 4), F(1, 2)): "min"}
    ok &= all(br_jet(x, F(0))[0][1] == 0 for x in quarter)            # y = 0 invariant (F_y = 0 there)
    ok &= br_jet(F(1), F(0))[0][0] == 1                                # transverse crossing of x = 1
    low, cen = (lambda d: br_hit(d, F(0), F(1, 200))), (lambda d: br_hit(d, F(-1, 200), F(1, 200)))
    pts = [F(0), F(1, 400), F(-1, 400), F(1, 200)]
    ok &= not low(F(0))[0] and low(F(1, 400)) == (True, F(1, 400)) and not low(F(-1, 400))[0]
    ok &= continuous_at_accepted(low, pts) and continuous_at_accepted(cen, pts, lip=1)
    ok &= all(cen(d)[0] for d in pts[:3])
    return ok


# ---------- (R1a) ----------
def check_ift():
    ok = True
    for q in (F(3, 2), F(5, 3), F(7, 4)):
        c, tau = q * q - 1, q                    # x(t, c) = t^2 - 1 - c, first (unique) zero on [0, 2] at t = q
        dx_dc, dx_dt = F(-1), 2 * tau
        d = dx_dc / dx_dt if MUT == "sign-flip" else -dx_dc / dx_dt
        ok &= d == 1 / (2 * q)
        h = F(1, 10 ** 6)
        secant = h / ((q + h) ** 2 - 1 - c)
        ok &= abs(secant - d) <= h
    return ok


def main():
    global MUT
    ap = argparse.ArgumentParser()
    ap.add_argument("--mutant", choices=MUTANTS)
    MUT = ap.parse_args().mutant
    checks = {"CLOSED_CONTACT": check_closed_contact(), "EARLY_PREFIX": check_early_prefix(),
              "TERMINAL_SLACK": check_terminal(), "BR_TORUS": check_br(), "IFT": check_ift()}
    passed = all(checks.values()) and len(checks) == 5
    print(json.dumps({"object": "CLAUDE-REVIEW-SARD-R1R2-20260929-v1", "checks": checks, "passed": passed,
                      "scope": "exact finite controls of the boundary examples only; R1/R2 are reviewed in REVIEW.md"},
                     indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
