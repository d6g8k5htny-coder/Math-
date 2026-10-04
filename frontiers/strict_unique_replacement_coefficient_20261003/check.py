"""C113 finite exact author controls, not analytic acceptance.

No network, external packages, random sampling, asserts or source mutations.
The proof of every fixed positive-width band uses continuity, not the finite
list of examples here. The q perturbation, positive open Gaussian mass and
actual elder interpretation remain analytic/source-bound proof obligations.
"""

from fractions import Fraction as F
import json


CHECKS = 0
REJECTIONS = []


def require(condition, message):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise RuntimeError(message)


def rational(value):
    if type(value) not in (int, F):
        raise ValueError("an int or Fraction, excluding bool, is required")
    return F(value)


def anchor(v, k):
    v, k = rational(v), rational(k)
    if not F(1, 2) < v < 1 or not k > 0:
        raise ValueError("require 1/2 < v < 1 and k > 0")
    c = v * v - F(1, 4)  # Z^2 at either extra root
    x, beta, s = -v, -12 * k, -12 * k * v
    z = 2 * v**3 - F(3, 2) * v + F(1, 2)
    distance_squared = (x + F(1, 2))**2 + c
    # All expressions are evaluated directly at X=-v and Z^2=c.
    gradient_x = 6 * k * (x * x - F(1, 4)) + beta * c / 2
    gradient_z_coefficient = s + beta * x
    height = (2 * k * x**3 - 3 * k * x / 2 - k / 2
              + s * c / 2 + beta * x * c / 2)
    hxx, hzz, hxz_squared = 12 * k * x, s + beta * x, beta**2 * c
    determinant = hxx * hzz - hxz_squared
    pin_m_det = (-6 * k) * (s - beta / 2)
    pin_s_det = (6 * k) * (s + beta / 2)
    sigma = (s - beta)**2 * (beta + 2 * s)
    delta = beta**3
    h_poly = beta**3 - 4 * beta * s**2
    weight = 9 * k**2 * (4 * s**2 - beta**2)
    return {
        "v": v, "k": k, "c": c, "z": z,
        "distance_squared": distance_squared,
        "gap_ratio_squared": z**2 / distance_squared**3,
        "gradient_x": gradient_x,
        "gradient_z_coefficient": gradient_z_coefficient,
        "height": height, "determinant": determinant,
        "pin_m_det": pin_m_det, "pin_s_det": pin_s_det,
        "sigma": sigma, "delta": delta, "h_poly": h_poly,
        "weight": weight,
    }


def verify_anchor(v, k):
    a = anchor(v, k)
    c, z, d2 = a["c"], a["z"], a["distance_squared"]
    require(a["gradient_x"] == 0, "extra-root axial criticality")
    require(a["gradient_z_coefficient"] == 0, "extra-root transverse criticality")
    require(a["height"] == -k * z, "exact extra-root height")
    require(z == 2 * (v - F(1, 2))**2 * (v + 1), "height factorization")
    require(0 < z < 1, "both extra roots lie strictly in the window")
    require(d2 == v * (2 * v - 1), "original-coordinate distance")
    require(0 < d2 < 1, "positive distance approaching the pin distance")
    require(a["determinant"] == -144 * k**2 * c, "correct Hessian determinant")
    require(a["determinant"] < 0, "both extra roots are saddles")
    require(a["pin_m_det"] == 72 * k**2 * (v - F(1, 2)), "maximum pin determinant")
    require(a["pin_m_det"] > 0 and -6 * k < 0, "maximum pin negative definite")
    require(a["pin_s_det"] == -72 * k**2 * (v + F(1, 2)), "saddle pin determinant")
    require(a["pin_s_det"] < 0, "saddle pin has mixed inertia")
    require(a["sigma"] == -1728 * k**3 * (1-v)**2 * (1+2*v), "Sigma identity")
    require(a["delta"] == -1728 * k**3, "Delta identity")
    require(a["h_poly"] == 1728 * k**3 * (4*v*v-1), "H identity")
    require(a["sigma"] < 0 and a["delta"] < 0 < a["h_poly"], "strict source exclusions")
    require(a["weight"] == -a["pin_m_det"] * a["pin_s_det"], "original typed weight")
    require(a["weight"] == 5184 * k**4 * c > 0, "positive determinant product")
    require(a["gap_ratio_squared"] == (2*v-1)*(v+1)**2/(4*v**3), "gap ratio identity")
    require(4*v**3-(2*v-1)*(v+1)**2 == (v-1)**2*(2*v+1), "gap ratio endpoint factorization")
    require(0 < a["gap_ratio_squared"] < 1, "gap ratio below one at the symmetric anchor")
    # The squared derivative of the two height values' difference is c^3/9.
    # This checks its algebraic positivity, not the implicit function theorem.
    require(c**3 / 9 > 0, "nonzero height-splitting derivative squared")
    return a


def band_witness(klo, khi, clo, chi):
    klo, khi, clo, chi = map(rational, (klo, khi, clo, chi))
    if not 0 < klo < khi or not 0 < clo < chi:
        raise ValueError("positive strictly ordered interval endpoints required")
    k, t = (klo + khi) / 2, (clo + chi) / 2
    for n in range(2, 257):
        v = 1 - F(1, 2**n)
        a = anchor(v, k)
        distance2 = t**2 * a["distance_squared"]
        gap2 = k**2 * a["gap_ratio_squared"]
        if clo**2 < distance2 < chi**2 and klo**2 < gap2 < khi**2:
            require(clo < t < chi and klo < k < khi, "pinned saddle strictly eligible")
            require(clo**2 < distance2 < chi**2, "both extra saddles' strict radius filters")
            require(klo**2 < gap2 < khi**2, "both extra saddles' strict gap filters")
            require(-k < a["height"] < 0, "both extra saddles' strict window filters")
            return {"K": [str(klo), str(khi)], "band": [str(clo), str(chi)],
                    "n": n, "v": str(v)}
    raise RuntimeError("finite example did not produce a witness within the search cap")


def reject_false(name, false_statement):
    require(not false_statement, "incorrect alternative survived: " + name)
    REJECTIONS.append(name)


def reject_input(name, function):
    try:
        function()
    except ValueError:
        require(True, name)
        REJECTIONS.append(name)
        return
    raise RuntimeError("invalid input was accepted: " + name)


def main():
    for v in [F(3, 4), F(9, 10), F(99, 100), F(999, 1000)] + [1-F(1, 2**n) for n in range(3, 17)]:
        for k in [F(1, 1000), F(1, 2), F(1), F(7, 3), F(1000)]:
            verify_anchor(v, k)

    examples = [
        (F(1, 2), F(2), F(1, 2), F(2)),
        (F(1), F(1001, 1000), F(1), F(1001, 1000)),
        (F(1, 10**6), F(1, 10**6)+F(1, 10**12), F(7), F(7)+F(1, 10**9)),
        (F(10), F(10)+F(1, 10**12), F(1, 100), F(1, 100)+F(1, 10**12)),
        (F(1, 10**9), F(2, 10**9), F(10**6), F(10**6)+F(1, 10**6)),
    ]
    witnesses = [band_witness(*bounds) for bounds in examples]

    for mass1 in [F(0), F(1, 7), F(1), F(13, 2)]:
        for mass2 in [F(0), F(1, 17), F(1), F(17)]:
            cr, cu = mass1 + mass2, mass1 + mass2 / 2
            require(cr-cu == mass2/2, "exact reciprocal coefficient difference")
            require((cu < cr) == (mass2 > 0), "strictness is equivalent to positive D=2 mass")

    a = anchor(F(3, 4), F(1))
    reject_false("draft determinant -432", a["determinant"] == -432*a["k"]**2*a["c"])
    reject_false("extra-root height sign reversed", a["height"] == a["k"]*a["z"])
    reject_false("omit axial displacement from distance", a["distance_squared"] == a["c"])
    reject_false("omit cubic distance power in gap", a["gap_ratio_squared"] == a["z"]**2/a["distance_squared"])
    eligible = {"pin", "higher_extra", "lower_extra"}
    rejected = eligible - {"higher_extra"}
    d = len(rejected)
    require(d == 2, "source excludes only the actual partner")
    require(sum(F(1, d) for _ in rejected) == 1, "one bar from two rejected candidates")
    reject_false("count actual partner as a third rejected saddle", F(1, d) == F(1, len(eligible)))
    reject_false("drop lower extra saddle from reciprocal", F(1, d) == F(1, len(rejected-{"lower_extra"})))
    mass1, mass2 = F(7, 3), F(0)
    reject_false("strict gap from zero D=2 mass", mass1+mass2/2 < mass1+mass2)
    reject_input("zero-width gap interval", lambda: band_witness(F(1), F(1), F(1), F(2)))
    reject_input("zero-width radius interval", lambda: band_witness(F(1), F(2), F(1), F(1)))
    reject_input("nonpositive gap interval", lambda: band_witness(F(0), F(1), F(1), F(2)))
    reject_input("nonpositive radius interval", lambda: band_witness(F(1), F(2), F(0), F(1)))
    reject_input("v at height-zero boundary", lambda: anchor(F(1, 2), F(1)))
    reject_input("v at pinned-height boundary", lambda: anchor(F(1), F(1)))
    reject_input("nonpositive k", lambda: anchor(F(3, 4), F(0)))
    reject_input("floating input", lambda: anchor(0.75, F(1)))
    reject_input("boolean input", lambda: anchor(F(3, 4), True))

    print(json.dumps({
        "status": "PASS_FINITE_CONTROLS", "passed": True, "checks": CHECKS,
        "control_kinds": ["rational root/height/Hessian identities", "retained polynomial signs",
                          "positive squared height-splitting derivative", "finite strict band witnesses",
                          "finite reciprocal coefficient identity", "false alternatives and invalid inputs"],
        "finite_band_witnesses": witnesses,
        "negative_controls_rejected": REJECTIONS,
        "scientific_effect": "NONE",
        "scope": "Finite author controls only; no Gaussian, continuity, IFT, elder-selection or theorem acceptance.",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
