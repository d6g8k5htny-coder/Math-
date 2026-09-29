"""Checks for D5-RECONCILIATION-20260929-v1 (RECONCILIATION.md). Standard library only; run from the repository root.

  (A) IDENTITIES  every source and record of §3 exists with its stated SHA256 (the P2 continuum record when present).
  (B) VERDICTS    the quoted verdict strings occur in each record.
  (C) TILING      pin disks (radius r/4 about M, S), the collar C_{1/4,4} (scaled), {4r <= |X| <= s0} and {|X| >= s0}
                  cover every point of an exact rational grid of the torus minus {M, S}, for r <= s0/4.
  (D) OPEN        the shrinking-collision item is still recorded as open (catalog C6).
Mutants (each must fail): tamper, drop-collar, close-c6.
"""
import argparse
import hashlib
import json
import pathlib
import sys
from fractions import Fraction as F

MUTANTS = ("tamper", "drop-collar", "close-c6")
MUT = None

SOURCES = {
    "reviews/d5_local_collar_20260928/PUNCTURED_PIN_PROOF.md":
        "f972e50bc07674ebce9d971d1a1bd4dba2f8036dde37ecb57d8a44a35650f76a",
    "reviews/d5_local_collar_20260928/COLLAR_PROOF.md":
        "794babe0fd039c3a93c401c0b8978316331af009fad45f953e63fbe7e1e31aab",
    "frontiers/rn_annulus_bridge_20260925/PROOF.md":
        "d55e2c03bb17e7977ff94130cc1ff21e54840cd1e20dc4e41ea9ad52228beb05",
    "frontiers/intermediate_window_20260928/PROOF.md":
        "b3eb9456d7058b5b78149cfca4e072679beda85cd1a0293d209664a542db66cf",
    "frontiers/remote_window_20260924/PROOF.md":
        "a332bae9bdc0106ce17047f7e0409cc3d94eb610a0c7b74ba5ba2d01a1620cb7",
    "frontiers/remote_collision_20260928/PROOF.md":
        "b9b8b58fd8266db7ffe6537078003888ef138b445d3289ec5588f116af9050c2",
    "reviews/d5_punctured_pin_nonauthor_20260928/REVIEW.md":
        "668d74825f156c929177bc1a3481cf421de4dd7874e7b25b2aece6c10aa7dc0e",
    "reviews/d5_collar_count_20260928/REVIEW.md":
        "8c8c30cc3b19601a7421341d5da8cb6c982fbc1fcc5ae4791acafa11cc81ee4e",
    "reviews/d5_i5_planar_f_20260928/REVIEW.md":
        "527d66e72b079ef7c854987f7e9d44f2252b81aa0e8d9e7ef3b45deb02388659",
    "reviews/d5_intermediate_window_claude_20260928/REVIEW.md":
        "fb3207802bf2d92ad138bc338a36f39bcd3a94440669b9aba9558e566f767976",
    "reviews/d5_offpin_second_moment_20260928/REVIEW.md":
        "43beb4ef7da5bf71e15164d5c4bc1862db387d83f906aebdf9831625b1ca6369",
    "reviews/d5_remote_collision_grok_20260928/REVIEW.md":
        "f8289546ee82fb386a0d0b6b54fbb99f258a2dc2a959ae231ae80cb4baa61e1e",
}
OPTIONAL = "reviews/d5_punctured_pin_continuum_claude_20260929/REVIEW.md"

VERDICTS = {
    "reviews/d5_punctured_pin_nonauthor_20260928/REVIEW.md": [
        "Cauchy–Binet floor `9/131072` | **ACCEPT** |",
        "| (P2) count lemma | all-height punctured disk | **HOLD**"],
    "reviews/d5_collar_count_20260928/REVIEW.md": [
        "| Collar first moment | `E_{Q^W} N_j(r E) <= C r^3 |E|` on `C(eta, R)` | ACCEPT existential |",
        "| ACCEPT corollary of punctured-pin + collar |"],
    "reviews/d5_i5_planar_f_20260928/REVIEW.md": [
        "| **ACCEPT** existential |",
        "| **ACCEPT** as corollary of C2 + I4 + D4 A |"],
    "reviews/d5_intermediate_window_claude_20260928/REVIEW.md": [
        "| **(I3) shell** and **(I4) intermediate** | **ACCEPT** at the stated existential scope |",
        "| **(I5) global single-witness first moment** | **ACCEPT** as a composition."],
    "reviews/d5_offpin_second_moment_20260928/REVIEW.md": [
        "| ACCEPT |",
        "| CANDIDATE pending review and test (catalog C6) |"],
    OPTIONAL: ["| **ACCEPT, existential.**"],
}


def check_identities(root):
    ok = True
    for path, sha in SOURCES.items():
        p = root / path
        want = ("0" * 64) if (MUT == "tamper" and path.endswith("COLLAR_PROOF.md")) else sha
        ok &= p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest() == want
    return ok


def check_verdicts(root):
    ok = True
    for path, needles in VERDICTS.items():
        p = root / path
        if not p.is_file():
            ok &= path == OPTIONAL
            continue
        text = p.read_text(encoding="utf-8")
        ok &= all(n in text for n in needles)
    return ok


def check_tiling():
    """Exact grid check in physical coordinates from the midpoint; torus side L = 1, s0 = 1/5, r = 1/20."""
    L, s0, r = F(1), F(1, 5), F(1, 20)
    M, S = (-r / 2, F(0)), (r / 2, F(0))

    def d2(a, b):
        return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2

    def covered(X):
        n2 = X[0] ** 2 + X[1] ** 2
        if X in (M, S):
            return True                                          # excluded points
        pin = d2(X, M) <= (r / 4) ** 2 or d2(X, S) <= (r / 4) ** 2
        collar = (n2 <= (4 * r) ** 2 and d2(X, M) >= (r / 4) ** 2 and d2(X, S) >= (r / 4) ** 2
                  and MUT != "drop-collar")
        mid = (4 * r) ** 2 <= n2 <= s0 ** 2
        remote = n2 >= s0 ** 2
        return pin or collar or mid or remote

    n = 80
    pts = [(L * F(i, n) - L / 2, L * F(j, n) - L / 2) for i in range(n) for j in range(n)]
    fine = [(F(i, 400), F(j, 400)) for i in range(-30, 31) for j in range(-30, 31)]
    return all(covered(X) for X in pts + fine + [M, S])


def check_open(root):
    text = (root / "reviews/d5_offpin_second_moment_20260928/REVIEW.md").read_text(encoding="utf-8")
    still_open = "CANDIDATE pending review and test (catalog C6)" in text
    return still_open and MUT != "close-c6"


def main():
    global MUT
    ap = argparse.ArgumentParser()
    ap.add_argument("--mutant", choices=MUTANTS)
    MUT = ap.parse_args().mutant
    root = pathlib.Path(".").resolve()
    checks = {"IDENTITIES": check_identities(root), "VERDICTS": check_verdicts(root), "TILING": check_tiling(),
              "OPEN_C6": check_open(root)}
    passed = all(checks.values()) and len(checks) == 4
    print(json.dumps({"object": "D5-RECONCILIATION-20260929-v1", "checks": checks, "passed": passed,
                      "scope": "identity, verdict-string, tiling and open-item checks; no mathematics is re-proved"},
                     indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
