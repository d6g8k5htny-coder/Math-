#!/usr/bin/env python3
"""Corollary PD ledger: exact exponent and constant bookkeeping (standard library only).

Usage: python3 pd_ledger.py [MUTANT]; exit 0 iff every check passes, 1 on a failure, 2 on an unknown label.
Mutants: RATE_THIRD (r^beta read as l^beta instead of l^(beta/3)), CUM_HALF (cumulative constant 1/2 for 3/5),
FRAC_ONE (nonselected-fraction error l^(1 + 1/4) instead of l^(1 + 1/12)).
It checks finite arithmetic only, not the analytic inputs (ELDER section 9, C102 (1.10), C103 (S3), A4.1).
"""
import sys
from fractions import Fraction as F

MUTANTS = ("RATE_THIRD", "CUM_HALF", "FRAC_ONE")
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
    """r = (l/k)^(1/3): r^e is O(l^(e/3)) uniformly for k >= k_-"""
    return e if MUT == "RATE_THIRD" else e / 3


# (i) the density: l^(-2/3) nu_rej - C_fail = O(r^beta) + O(r) with r^3 = l/k
for beta, name in ((F(1, 4), "C103"), (F(1, 10), "A4.1"), (F(1, 2), "A4.1"), (F(3, 5), "A4.1"), (F(2, 3) - F(1, 1000), "A4.1")):
    err = min(l_exp_of_r(beta), l_exp_of_r(F(1)))           # the A_r - A_0 = O(r) term is O(l^(1/3))
    check(err == beta / 3, "%s beta=%s: relative error l^(beta/3)" % (name, beta))
    dens = F(2, 3) + err
    check(dens == (2 + beta) / 3, "%s beta=%s: density error l^((2+beta)/3)" % (name, beta))
    # (ii)/(iii) integrate l^q * l^dens on (0, t]: finite iff q + dens > -1; exponent q + dens + 1
    for q in (F(-3, 2), F(-1), F(0), F(1), F(5, 2)):
        check(q > F(-5, 3) and q + dens > -1, "beta=%s q=%s: integrable error" % (beta, q))
        check(q + dens + 1 == q + (5 + beta) / 3, "beta=%s q=%s: moment error t^(q+(5+beta)/3)" % (beta, q))
    lead = F(1, 2) if MUT == "CUM_HALF" else F(3, 5)
    check(lead == 1 / (F(2, 3) + 1), "cumulative constant 1/(5/3) = 3/5")
    # (iv) nonselected fraction: l * [C + O(l^err)] / [c + O(l^(1/3))]
    frac_err = 1 + (F(1, 4) if MUT == "FRAC_ONE" and name == "C103" else min(err, F(1, 3)))
    check(frac_err == 1 + beta / 3, "%s beta=%s: fraction error l^(1+beta/3)" % (name, beta))
check(F(2, 3) + F(1, 4) / 3 == F(3, 4) and 1 + F(1, 4) / 3 == F(13, 12) and F(5, 3) + F(1, 12) == F(7, 4),
      "C103 instance: l^(3/4), l^(13/12), t^(7/4)")
# the q threshold: the main term l^(q+2/3) is integrable at 0 iff q > -5/3, the error l^(q+3/4) iff q > -7/4
for q in (F(-5, 3), F(-17, 10), F(-7, 4) + F(1, 1000)):
    check(not (q + F(2, 3) > -1), "q=%s: the main term is not integrable, so (iii) needs q > -5/3" % q)
    check(q + F(3, 4) > -1, "q=%s: the error term alone is integrable" % q)
check(not (F(-7, 4) + F(3, 4) > -1), "q=-7/4: the error term is not integrable either")
check((2 + F(2, 3)) / 3 == F(8, 9), "the A4.1 supremum (2+beta)/3 -> 8/9")
print("Corollary PD ledger: %d checks, %d failures; mutant: %s" % (n, bad, MUT or "none"))
sys.exit(0 if bad == 0 else 1)
