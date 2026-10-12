#!/usr/bin/env python3
"""Corollary PD3 ledger: exact exponent and constant bookkeeping (standard library only).

Usage: python3 pd3_ledger.py [MUTANT]; exit 0 iff every check passes, 1 on a failure, 2 on an unknown label.
Mutants: RATE_THIRD (r^beta read as l^beta instead of l^(beta/3)), LOG_HALF (log(1/r) <= (1/2) log(1/l) in place of (2/3)),
CUM_HALF (cumulative constant 1/2 for 3/5), MOM_2000 (moment constant 2000 in place of 3073).
It checks finite arithmetic only, not the analytic inputs ([P] sections 10-12, #175 section 7, [R] (R11), A3.8, A3.9).
"""
import sys
from fractions import Fraction as F
from math import factorial, comb

MUTANTS = ("RATE_THIRD", "LOG_HALF", "CUM_HALF", "MOM_2000")
MUT = None
if len(sys.argv) > 1:
    MUT = sys.argv[1]
    if len(sys.argv) > 2 or MUT not in MUTANTS:
        print("unknown mutant label: %s" % " ".join(sys.argv[1:]))
        sys.exit(2)
n = bad = 0


def check(ok, msg):
    global n, bad
    n += 1
    if not ok:
        bad += 1
        print("FAIL " + msg)


def l_exp_of_r(e):
    """r = (l/k)^(1/3) with k >= k_-: r^e <= k_-^(-e/3) l^(e/3)."""
    return e if MUT == "RATE_THIRD" else e / 3


# (i), power-law family: l^(-2/3) nu_rej - C_fail = O(r^beta) + O(r), so the relative error is l^(beta/3) (beta < 1)
for beta in (F(1, 10), F(1, 3), F(1, 2), F(3, 5), F(2, 3) - F(1, 1000)):
    err = min(l_exp_of_r(beta), l_exp_of_r(F(1)))
    check(err == beta / 3, "beta=%s: relative error l^(beta/3)" % beta)
    check(F(2, 3) + err == (2 + beta) / 3, "beta=%s: density error l^((2+beta)/3)" % beta)
    for q in (F(-3, 2), F(-1), F(0), F(1), F(5, 2)):
        check(q > F(-5, 3) and q + F(2, 3) + err > -1, "beta=%s q=%s: integrable error" % (beta, q))
        check(q + F(2, 3) + err + 1 == q + (5 + beta) / 3, "beta=%s q=%s: moment error t^(q+(5+beta)/3)" % (beta, q))
    check(1 + min(err, F(1, 3)) == 1 + beta / 3, "beta=%s: fraction error l^(1+beta/3)" % beta)
check((2 + F(2, 3)) / 3 == F(8, 9), "the supremum (2+beta)/3 -> 8/9, attained with the logarithm")
# (i), endpoint: r^(2/3) <= k_-^(-2/9) l^(2/9) and log(1/r) = (1/3) log(k/l) <= (1/3)(log(1/l) + log k_+) <= (2/3) log(1/l) when k_+ <= 1/l
check(l_exp_of_r(F(2, 3)) == F(2, 9), "endpoint: r^(2/3) is l^(2/9)")
logc = F(1, 2) if MUT == "LOG_HALF" else F(2, 3)
# with x = log(1/l) >= log k_+ (that is k_+ <= 1/l): (1/3)(x + log k_+) <= (1/3)(2x) = (2/3) x; the mutant's 1/2 fails at log k_+ = x
for x in (F(1), F(3), F(10)):
    for lk in (F(0), x / 2, x):
        check((x + lk) / 3 <= logc * x, "log bound at x=%s, log k_+=%s" % (x, lk))
check(F(2, 3) + F(2, 9) == F(8, 9) and F(5, 3) + F(2, 9) == F(17, 9) and 1 + F(2, 9) == F(11, 9), "endpoint exponents 8/9, 17/9, 11/9")
# (ii)-(iii): integrate l^q l^(8/9) log(1/l)^(8/3) on (0, t], l = t s: log(1/l) <= log(1/t)(1 + log(1/s)), (1+log(1/s))^(8/3) <= (1+log(1/s))^3;
# int_0^1 s^(q+8/9) (1 + log(1/s))^3 ds = sum_j C(3,j) j!/(q+17/9)^(j+1), finite iff q > -17/9, and for q > -5/3 at most sum_j C(3,j) j! (9/2)^(j+1)
S = sum(F(comb(3, j) * factorial(j)) * F(9, 2) ** (j + 1) for j in range(4))
check(S == F(24579, 8), "sum_j C(3,j) j! (9/2)^(j+1) = 24579/8")
mom = 2000 if MUT == "MOM_2000" else 3073
check(S < mom, "the moment constant %d exceeds 24579/8" % mom)
for q in (F(-5, 3) + F(1, 1000), F(-1), F(0), F(2)):
    a = q + F(17, 9)
    check(a > F(2, 9), "q=%s: q + 17/9 > 2/9" % q)
    check(sum(F(comb(3, j) * factorial(j)) / a ** (j + 1) for j in range(4)) <= S, "q=%s: the series is at most 24579/8" % q)
s0 = sum(F(comb(3, j) * factorial(j)) / F(17, 9) ** (j + 1) for j in range(4))
check(s0 < 3, "at q = 0 the series is below 3 (it is %s)" % float(s0))
lead = F(1, 2) if MUT == "CUM_HALF" else F(3, 5)
check(lead == 1 / (F(2, 3) + 1), "cumulative constant 1/(5/3) = 3/5")
# the q threshold: the main term l^(q+2/3) is integrable at 0 iff q > -5/3
for q in (F(-5, 3), F(-17, 10)):
    check(not (q + F(2, 3) > -1), "q=%s: the main term is not integrable, so (iii) needs q > -5/3" % q)
check(F(-17, 9) + F(8, 9) == -1, "the error term alone is integrable exactly for q > -17/9")
# c_cand of [P] (11.3): 4 k^(-2/3) pi_0 z_0 = 12 pi_0 z_0/(3 k^(2/3))
check(F(12, 3) == 4, "c_cand: 12/3 = 4")
# A3.9: A_0 alpha^(3)/(3 k^(5/3)) = F/(3 k^(8/3)) since alpha^(3) = F/(k A_0)
check(F(5, 3) + 1 == F(8, 3), "C_fail integrand: k^(5/3) * k = k^(8/3)")
print("Corollary PD3 ledger: %d checks, %d failures; mutant: %s" % (n, bad, MUT or "none"))
sys.exit(0 if bad == 0 else 1)
