## Lifetime note SL: author controls, exact executable and stdout, and the author-side referee record

This publishes the standard-library control script that note SL ([6028358916](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6028358916)) cites in §3, so anyone can replay it. The controls check the finite algebra of the note: the substitutions (S1), the identities behind (1.2) and (1.4) (S2), the domination on the soft layer (S3), and the exponents of the limit's bound with the identity behind (1.2) (S4). They do not test the analytic inputs (note TL, #243's Theorem FL, #242's Theorem 1) or dominated convergence; §3 of the note says so.

Dylan Roy — delegated AI work. Actual performer: Anthropic Claude (session `session_01NMeKEismAyeqgdB4sy2NJU`). Scientific effect: NONE.

**Extraction rule.** The same as in [5971055189](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5971055189): the file is the exact text between the first ```` ```python ```` fence after its `###` heading and the next ```` ``` ```` line, plus a final newline. The expected stdout is the single JSON line in the following ```` ```json ```` fence, plus one newline.

**Identities.** `sl_exact.py`: 5,395 B, SHA-256 `745e7468b5c5ec71761820953c6e167477c9c8a5c52b94fb192639f114e61dc0`. Stdout: 178 B, SHA-256 `4aa5b6175488fb1de8b9b22f0adf7059091083f1eaaccf2f39666076a998a521`.

**Run.** A full run takes about 0.1 s.
- `python3 -B -S sl_exact.py`: exit 0, with exactly the stdout below (4,800 checks in four groups).
- `python3 -B -O -S sl_exact.py`: byte-identical output. No check depends on an `assert`.
- `--mutant M1` … `M4`: each exits 1 in both modes, with empty stdout and `FAILED: <group>` on stderr:
  - `M1` (the fold variable `r = ℓ^{1/4}v` in place of `ℓ^{1/3}v`): `S1_substitution`.
  - `M2` (the Jacobian `ℓ^{1/3}` in place of `ℓ^{2/3}`): `S2_identities`.
  - `M3` (the domination tested beyond the soft layer, `v` up to `2ℓ^{−1/12}`, where `r > k`): `S3_domination`, at the inequality from (TL).
  - `M4` (the weight `v³` in place of `v⁴`; the exponent at `v → ∞` becomes `−3`, not the `−2` of the dominating function, though `v³` would still be integrable): `S4_integrability`.
- An unknown label (`--mutant M5`), a bare `--mutant`, extra arguments, or any other argument: exit 2, with `usage: sl_exact.py [--mutant M1..M4]` on stderr.

The output was produced with Python 3.11.15. The script uses only `json`, `random` (with a fixed seed), `sys` and `fractions`.

**Author-side referee record (not review evidence).** Before posting, a clean-context Claude subagent of this session refereed the draft against note TL, #242, #243, [K], [R], #188 and note C3. It carries organizational-independence credit 0 and is not review evidence. Verdict: **AMEND**, no blocking finding; it found every step of the three proofs to hold as written. All findings are applied:
- SF-1: the header credited [K] to OpenAI; the same session wrote [K] (and #188). Corrected.
- SF-2: *Not claimed* attributed the phrase "quantitative margins in Proposition FL.4" to #243's *What is not claimed*; it is in #243 §6. Corrected.
- SF-3: *What is new* said that the kernel contributes "exactly the share of #242's composite". Lemma 5 needs a hypothesis on `H` not known for the torus field, and its remainder is `O(ℓ^{3/4})`. The bullet now says that Theorem SL is the integrated content of input (i), and that the two terms agree up to `o(ℓ^{2/3})` with those of Lemma 5's composite when its hypothesis holds.
- NITs applied:
  - `ℱ₀ ≤ C` by a direct route through #242 (0.2), (G2) and [R] (R5);
  - **the domination simplified**: on `κ ≥ 1`, `r ≤ k`, so (TL)'s `C(r² + rk) ≤ 2Crk`. The dominating function is then a fixed `g`, and ordinary dominated convergence replaces the generalized form. S3 and M3 are rebuilt accordingly;
  - measurability;
  - the hypotheses of note TL §5's two bounds;
  - #243's *Matching* records #242's result rather than proving it;
  - which of #243's Remarks 2;
  - #242's Lemma 5 moved to *Cited only*;
  - #188's merge on Math- (4 October, `f7f083ec`), which the referee's files did not show;
  - Remark 4 (a rate is a sufficient route);
  - Remark 1 (`R_{2/3}` as in (SL));
  - the integrability condition in *Not claimed*;
  - the descriptions of S4 and M4;
  - the notation `ℱ`, chosen to avoid #242's window map `Φ`.

### sl_exact.py

```python
"""Exact controls for note SL (CL-SL-SOFT-LAYER-TWO-THIRDS-20261007-v1).

Standard library only; exact rational arithmetic; deterministic; output identical under -O.
Usage: python3 -B -S sl_exact.py [--mutant M1..M4]
On success: one JSON line on stdout, exit 0.
On a failed control: nothing on stdout, 'FAILED: <group>' on stderr, exit 1.
On invalid arguments: usage on stderr, exit 2.
"""
import json
import random
import sys
from fractions import Fraction as F

USAGE = "usage: sl_exact.py [--mutant M1..M4]\n"
MUTANTS = {"M1", "M2", "M3", "M4"}


def parse(argv):
    if len(argv) == 0:
        return None
    if len(argv) == 2 and argv[0] == "--mutant" and argv[1] in MUTANTS:
        return argv[1]
    sys.stderr.write(USAGE)
    sys.exit(2)


MUT = parse(sys.argv[1:])
RNG = random.Random(20261007)


class Failed(Exception):
    pass


def need(cond, group):
    if not cond:
        raise Failed(group)


def pos(lo=1, hi=60, den=12):
    return F(RNG.randint(lo, hi), RNG.randint(1, den))


# ---------- S1: the substitutions on exact perfect powers l = t^12 ----------

def s1():
    n = 0
    for _ in range(400):
        t = F(RNG.randint(1, 9), RNG.randint(2, 12))            # l^{1/12} = t, l^{1/4} = t^3, l^{1/3} = t^4
        l = t ** 12
        s = pos()
        r = t ** 3 * s                                           # r = l^{1/4} s
        need(l / r ** 4 == s ** -4, "S1_substitution")
        v = pos()
        r = (t ** 3 if MUT == "M1" else t ** 4) * v              # r = l^{1/3} v
        k = l / r ** 3
        kap = k / r
        need(k == v ** -3, "S1_substitution")
        need(kap == t ** -4 * v ** -4, "S1_substitution")        # kappa = l^{-1/3} v^{-4}
        need((r <= t ** 3) == (v <= 1 / t) == (kap >= 1), "S1_substitution")
        need((v <= 1) == (k >= 1), "S1_substitution")
        n += 5
    return n


# ---------- S2: the identities behind (1.2) and (1.4) ----------

def s2():
    n = 0
    for _ in range(400):
        t = F(RNG.randint(1, 9), RNG.randint(2, 12))
        l = t ** 12
        v = pos()
        r = t ** 4 * v
        k = l / r ** 3
        kap = k / r
        D = F(RNG.randint(-99, 99), RNG.randint(1, 30))
        need(kap * r ** 2 == r * k and kap ** 2 * r ** 2 == k ** 2, "S2_identities")
        need(D / r == (1 / k) * kap * D, "S2_identities")
        jac = t ** 4 * (t ** 4 if MUT != "M2" else 1)            # dr = l^{1/3} dv, and D_r = r (D_r/r) = l^{1/3} v (D_r/r)
        need(jac == t ** 8, "S2_identities")                     # l^{1/3} l^{1/3} = l^{2/3} = t^8
        # int D_r dr = l^{1/3} int D dv = l^{1/3} int r (D/r) dv = l^{2/3} int v (D/r) dv
        need(t ** 4 * (r * (D / r)) == jac * (v * (D / r)), "S2_identities")
        need(v * (1 / k) == v ** 4, "S2_identities")              # the weight of the limit: v (1/k) = v^4
        n += 5
    return n


# ---------- S3: the domination on the soft layer v <= l^{-1/12} ----------

def s3():
    n = 0
    low = high = 0
    for _ in range(600):
        t = F(1, RNG.randint(2, 12))                            # l^{-1/12} = 1/t in [2, 12]
        l = t ** 12
        top = (2 if MUT == "M3" else 1) / t                     # M3: beyond the soft layer
        v = top * F(RNG.randint(1, 1000), 1000)
        r = t ** 4 * v
        k = l / r ** 3
        kap = k / r
        if MUT != "M3":
            need(kap >= 1 and r <= k, "S3_domination")           # the soft layer: kappa >= 1, r <= k
        if v <= 1:
            need(2 * v / (kap * r) == 2 * v ** 4 and 2 * v ** 4 <= 2, "S3_domination")    # |D| <= 2C/kappa
            low += 1
        else:
            need(v * (r ** 2 + r * k) / r <= 2 * v * k and 2 * v * k == 2 * v ** -2, "S3_domination")   # (TL), r <= k
            high += 1
        n += 1
    need(low >= 20 and high >= 20, "S3_domination")             # both ranges are exercised
    return n + 1


# ---------- S4: the integrability of the limit, and (SL1) ----------

def s4():
    n = 0
    w = 3 if MUT == "M4" else 4                                 # the weight v^w of R_{2/3}
    # v -> 0: |v^w (Phi - Phi0)| <= C v^w, integrable at 0 iff w > -1
    need(w > -1, "S4_integrability")
    # v -> infinity: |Phi(v^{-3}) - Phi0| <= C k^2 = C v^{-6}, so v^w v^{-6} must be integrable at infinity: w - 6 < -1
    need(w - 6 == -2 and w - 6 < -1, "S4_integrability")
    # the limit of the domination at v >= 1 is C v^{-2}, matching v^w v^{-6}
    need(w - 6 == -2, "S4_integrability")
    for _ in range(200):
        k = F(RNG.randint(1, 60), RNG.randint(60, 120))          # 0 < k <= 1
        r = F(RNG.randint(1, 50), RNG.randint(50, 5000))
        if r > k:
            continue
        kap = k / r
        need(kap * r ** 2 * (1 + kap) == r * k + k ** 2, "S4_integrability")   # kappa * C r^2 (1 + kappa) = C(rk + k^2)
        n += 1
    return n + 3


def main():
    groups = [("S1_substitution", s1), ("S2_identities", s2), ("S3_domination", s3), ("S4_integrability", s4)]
    counts = {}
    try:
        for name, fn in groups:
            counts[name] = fn()
    except Failed as ex:
        sys.stderr.write("FAILED: %s\n" % ex.args[0])
        sys.exit(1)
    out = {"object": "CL-SL-SOFT-LAYER-TWO-THIRDS-20261007-v1", "checks": counts, "total": sum(counts.values()),
           "passed": True}
    sys.stdout.write(json.dumps(out, sort_keys=True, separators=(",", ":")) + "\n")


if __name__ == "__main__":
    main()
```

```json
{"checks":{"S1_substitution":2000,"S2_identities":2000,"S3_domination":601,"S4_integrability":199},"object":"CL-SL-SOFT-LAYER-TWO-THIRDS-20261007-v1","passed":true,"total":4800}
```

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
_Generated by [Claude Code](https://claude.ai/code)_