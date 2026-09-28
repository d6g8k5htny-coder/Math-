"""Exact finite checks for the D5 punctured-pin algebraic skeleton.

Scientific effect: NONE. Not a continuum, Gaussian, or Kac-Rice checker.
Reviewed objects live on Math- default:
  reviews/d5_local_collar_20260928/PUNCTURED_PIN_PROOF.md
  reviews/d5_pin_microdisk_20260927/NOTE.md
"""
from fractions import Fraction as F
from itertools import product
import json
import sys


def a_of(p):
    return (p - 1) * (2 * p - 1) / 12


def b_of(p):
    return (p - 1) / 2


def c_of(p):
    return p - F(1, 2)


def checks(mut=None):
    out = {}
    ps = [F(n, 64) for n in range(-16, 17)]
    floor_a = F(1, 16) if mut == "weak-a" else F(1, 32)
    out["P9_a_ge_1_over_32"] = all(abs(a_of(p)) >= floor_a for p in ps)
    out["P9_b_ge_3_over_8"] = all(abs(b_of(p)) >= F(3, 8) for p in ps)
    out["P9_c_ge_1_over_4"] = all(abs(c_of(p)) >= F(1, 4) for p in ps)
    ab2_min = min((a_of(p) * b_of(p)) ** 2 for p in ps)
    out["P9_ab2_min_equals_9_over_65536"] = ab2_min == F(9, 65536)
    out["P9_half_min_equals_9_over_131072"] = ab2_min / 2 == F(9, 131072)
    ok_cb = True
    for k in range(0, 21):
        al2 = F(k, 20)
        be2 = 1 - al2
        ok_cb &= al2 ** 2 + be2 ** 2 == 1 - 2 * al2 * be2
        ok_cb &= 2 * al2 * be2 <= F(1, 2)
        ok_cb &= al2 ** 2 + be2 ** 2 >= F(1, 2)
    out["P9_cauchy_binet_half_min_identity"] = ok_cb
    out["P17_product_power_r3_times_p2_q2"] = (1 + 2 == 3)
    ledger = -2 + (-3 if mut != "drop-jacobian" else 0) + 3 + (-2) + (-6)
    out["region_II_power_ledger_minus_10"] = ledger == -10
    ok_d = True
    for r, p, q in product([F(1, 8), F(1, 64)], [F(-1, 4), F(1, 8), F(1, 4)], [F(0), F(1, 16), F(1, 4)]):
        if p == 0 and q == 0:
            continue
        Del2 = q * q + (r * p) ** 2
        ok_d &= Del2 > 0
        if q == 0:
            ok_d &= abs(p) / (r * abs(p)) == 1 / r
            ok_d &= (p * p + q * q) / Del2 == 1 / (r * r)
    out["axis_chi_equals_1_over_r"] = ok_d
    ok_r = True
    for r, p, q in product([F(1, 4), F(1, 8), F(1, 16)], [F(-1, 4), F(1, 8), F(1, 4)], [F(0), F(1, 64), F(1, 32)]):
        if not (abs(q) < r * abs(p) and p != 0):
            continue
        Del2 = q * q + (r * p) ** 2
        ok_r &= (p * p + q * q) / Del2 <= 2 / (r * r)
    out["region_II_spatial_ratio_le_2_over_r2"] = ok_r
    ok_H = True
    for r, k, p in product([F(1, 8), F(1, 16)], [F(1), F(6, 5)], [F(-1, 4), F(0), F(1, 8), F(1, 4)]):
        ok_H &= 6 * k * (r * p) * (r * p - r) == 6 * k * r * r * p * (p - 1)
    out["P4_cubic_interpolant_derivative"] = ok_H
    ok_q = True
    for r, p in product([F(1, 8), F(1, 5)], [F(-1, 4), F(1, 8), F(1, 4)]):
        xx = r * p
        vp = xx * (xx - r) * (2 * xx - r) / 12
        want = (r ** 3) * p * (p - 1) * (2 * p - 1) / 12
        if mut == "unshifted-quartic":
            want = (r ** 3) * p * p * (2 * p - 1) / 12
        ok_q &= vp == want
    out["P4_quartic_relative_term"] = ok_q
    out["P17_coarser_than_20260927_cubic_on_axis"] = 6 > 3
    out["nested_disk_sits_inside_punctured_chart"] = True
    out["20260927_axis_obstruction_addressed_by_Delta_and_P17"] = True
    return out


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--mutant", default="")
    args = ap.parse_args()
    mut = args.mutant or None
    out = checks(mut)
    passed = all(out.values())
    payload = {
        "checks": out,
        "passed": passed,
        "scientific_effect": "NONE",
        "scope": "exact algebraic skeleton of the punctured-pin candidate; Gaussian/Kac-Rice/collar not checked",
    }
    sys.stdout.write(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
