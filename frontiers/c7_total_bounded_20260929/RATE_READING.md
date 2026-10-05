# C7 rate reading: keep the gap cutoff in the rejected-density bound

**Object:** C7-GAP-CUTOFF-RATES-20261005-v1. **Scientific effect: NONE.**
Dylan Roy — delegated AI mathematical work. Actual author: OpenAI / GPT-6
Astra Pro, session `github-rules-and-closure-round4-20261005`.
This is an additive, source-conditional consequence and clarification, not a
fresh audit of the imported Gaussian estimates or a scientific-status decision.
The original C7 proof is by Anthropic Claude; its attribution is unchanged.

## 1. Source and corrected reading

Source: `frontiers/c7_total_bounded_20260929/PROOF.md` at Math- commit
`5b012335b279d1f93b930e7b906da09164332c47`, Git blob
`28748b086ec6761ef467dc67cba475fbdf8b7455`, SHA-256
`16c0efe372c1b1f26460aaa109287fed78e6fbd2dd00a0530998db296278dd01`.
Consumed slices are the statement of (K2), the rejected-intensity identity and
Gaussian pin-density bound in §4, and `1-e <= 1_{G_r^c}` there. These are imported
premises here, not re-proved or inferred from CI. Use the same fixed `d >= 2`,
`L > 0`, per-volume convention, sphere measure and canonical density version.

The final §4 remark juxtaposes an `O(ell^(1/4))` bound and “rarer” language about
an `ell^(2/3)` scale. Read that comparison as follows:

> The region `r <= k`, with unrestricted positive gap marks, has a rejected-
> density upper bound `O(ell^(1/4))`. On each fixed positive compact gap window
> the stronger upper bound is `O_K(ell^(2/3))`. These concern different integration
> domains. Neither upper bound alone asserts a sharp asymptotic or little-o.
> In particular, `O(ell^(1/4))` does not imply `O(ell^(2/3))`.

The mathematical estimates in §4 and Corollary T are unchanged. The bound below
makes the distinction quantitative. It is a bound on a marked **density**, not
a probability, and it does not identify cap failure with actual elder failure.

## 2. Explicit cutoff bound

Let `r0 > 0` be a radius on which (K2) and the §4 pin bound apply, reduced to
`r0 <= 1` if necessary. For `ell > 0` and `kappa >= 0`, let `R_kappa(ell)` denote
the rejected-density contribution with

    r = (ell/k)^(1/3),   0 < r <= r0,   r <= k,   k >= kappa,

integrating over all birth marks `b` and directions as in §4. This is a subset
of the source's near region: that larger region also includes `r > k`.
Set

    a = max{kappa, ell^(1/4), ell/r0^3} > 0.

The three lower bounds on `k` express the three restrictions exactly. In
particular, the `ell/r0^3` floor is not removed when `r0` is small.
There is a finite constant `C0`, depending on the imported constants and fixed
`d,L` but not on `ell,kappa`, such that

    0 <= R_kappa(ell) <= (3 C0/5) ell^(2/3) a^(-5/3).       (CR)

**Proof from the specified interfaces.** On the generic locus the elder mark
satisfies `0 <= 1-e <= 1_{G_r^c}`. The source's exact §4 identity gives

    R_kappa(ell)
      = 4 ell^(-1/3) int_{k>=a} int_b int_u
          pi_r(v_r) E_Q[(W_r/r^2)(1-e)] k^(-2/3) dσ db dk.

By (K2), with a nonnegative finite exponent `N` enlarged if needed, and the
source's bound `pi_r(v_r) <= C_pi exp(-c(b^2+k^2))`, this is at most

    4 C_K C_pi ell^(2/3) int_a^infinity k^(-8/3)
      int_b int_u (1+|b|+k)^N exp(-c(b^2+k^2)) dσ db dk.

Here `r^3/k = ell/k^2`; the factor `ell^(-1/3)` from the lifetime Jacobian has
been retained. The inner integral is uniformly bounded in `k >= 0`: use
`(1+|b|+k)^N <= (1+|b|)^N(1+k)^N`, the finite Gaussian polynomial integral
in `b`, the bounded function `(1+k)^N exp(-c k^2)`, and finite sphere area.
Absorb these constants into `C0`. Finally,

    int_a^infinity k^(-8/3) dk = (3/5) a^(-5/3),

which proves (CR). All integrands are nonnegative, so these restrictions and
bounds require no cancellation. There is **no division by `Z_r`** and no use of
the separately corrected normalized-probability remark. ∎

## 3. Consequences and limits

For `0 < ell <= min(1,r0^4)`, the spatial floor is at most `ell^(1/4)`.

- **Unrestricted gaps (`kappa=0`).** (CR) gives `O(ell^(1/4))` for the
  specific region `r <= k`. It gives no such bound for the omitted `r > k`
  region or for the entire unrestricted rejected population.
- **Fixed positive cutoff.** For fixed `kappa>0` and additionally
  `ell <= kappa^4`, (CR) gives `O(kappa^(-5/3) ell^(2/3))`.
  Restriction to any fixed compact interval `[kappa,k_plus]` can only reduce
  this nonnegative contribution. The constant is not uniform as `kappa -> 0`.
- **Shrinking cutoffs.** For `kappa=ell^alpha`, `alpha>=0` fixed, (CR) gives

      R_{ell^alpha}(ell)
        <= (3 C0/5) ell^[2/3 - (5/3) min(alpha,1/4)].       (SC)

  For `0 <= alpha <= 1/4`, the exponent interpolates from `2/3` to `1/4`.
  For `alpha >= 1/4`, it stays `1/4` because the condition `r <= k` sets the
  effective lower cutoff. This is not a claim that the density attains the bound.

For a scalar illustration of the logical distinction, the function
`h(ell)=ell^(1/4)` is `O(ell^(1/4))` but
`h(ell)/ell^(2/3)=ell^(-5/12) -> infinity`. Also an `O(ell^(2/3))`
bound does not by itself imply `o(ell^(2/3))`. These observations are not
counterexamples to a theorem about the actual Gaussian field; they explain why
the two-domain upper bounds must not be converted into stronger conclusions.

This note changes no statement, hypothesis, constant, or checker in the original
proof; no lower bound or sharp coefficient is newly proved. It does not assert
normalized-law, total-rejection, full-persistence, uniform-in-d/L, or global
next-order closure. Theorem U and the source's treatment of `r>k` retain their
separate roles. The existing normalized-form erratum is preserved unchanged.

## 4. Reproducible finite algebra controls

The sole Python block below is a standard-library diagnostic, not an analytic
or Lean proof. Save it as `cutoff_check.py`. Run `python -B -S cutoff_check.py`
and `python -B -S -O cutoff_check.py`; they must print identical JSON with
45 domain/Jacobian cases, 21 shrinking-cutoff cases, and 3 ratio/integral cases.
In each mode, appending any of `M1 M2 M3 M4 M5` separately must exit 1 with
`CUTOFF_CHECK_FAIL`. The mutations omit respectively the `r<=k` floor, spatial
floor, lifetime Jacobian, correct rate ordering, and the cubic-substitution
Jacobian factor. They mutate this diagnostic, not the historical C7 checker.

The author ran those commands and observed the stated outcomes before publication.
The unchanged hosted C7 workflow checks inventory and replays the historical
checker; it does **not** execute this embedded appendix. Its CI result must not
be described as executing these controls. A nonauthor can reproduce them directly.
Embedded code SHA-256 (UTF-8, including its final newline): `27c908a6c34564b40d6ab53a530055cf77216a5f511b31ddc9c8a13214cb4ad2`.

```python
"""Finite algebra checks only; the analytic argument is in RATE_READING.md."""
from fractions import Fraction as F
import json
import sys

mutant = sys.argv[1] if len(sys.argv) == 2 else "NONE"
if len(sys.argv) > 2 or mutant not in {"NONE", "M1", "M2", "M3", "M4", "M5"}:
    raise SystemExit("usage: cutoff_check.py [M1|M2|M3|M4|M5]")

def require(ok, label):
    if not ok:
        raise SystemExit("CUTOFF_CHECK_FAIL: " + label)

cases = 0
for n in (2, 3, 5):
    t = F(1, n)
    ell = t ** 12
    for r0 in (F(1), F(1, 4), F(1, 64)):
        for kappa in (F(0), t ** 2, t ** 3, t ** 4, F(2)):
            floors = [kappa]
            if mutant != "M1":
                floors.append(t ** 3)  # ell^(1/4)
            if mutant != "M2":
                floors.append(ell / r0 ** 3)
            a = max(floors)
            require(a > 0, "positive cutoff")
            require(ell <= a ** 4, "K2 domain r<=k")
            require(ell <= a * r0 ** 3, "spatial domain r<=r0")
            scale_cubed = ell ** (3 if mutant == "M3" else 2) / a ** 5
            require(scale_cubed == (t ** (-4) * ell) ** 3 / a ** 5,
                    "lifetime Jacobian ell^(-1/3) retained")
            cases += 1

shrinking = 0
for n in (2, 3, 5):
    t = F(1, n)
    ell = t ** 12
    for j in range(7):
        a = max(t ** j, t ** 3, ell)  # r0=1, kappa=ell^(j/12)
        require(ell ** 2 / a ** 5 == t ** (24 - 5 * min(j, 3)),
                "shrinking cutoff exponent and saturation")
        shrinking += 1
    require((t ** 3) / (t ** 8) == t ** (-5), "rate ratio identity")
    require(t ** 3 <= t ** 8 if mutant == "M4" else t ** 3 > t ** 8,
            "O(ell^(1/4)) alone is not O(ell^(2/3))")
    c = F(1, 5) if mutant == "M5" else F(3, 5)
    tail = c / t ** 5  # integral from k=t^3 to infinity
    require(5 * tail * t ** 5 == 3, "k=u^3 Jacobian factor")

print(json.dumps({"domain_and_jacobian_cases": cases,
                  "shrinking_cutoff_cases": shrinking,
                  "rate_ratio_and_integral_cases": 3,
                  "scientific_acceptance": False}, sort_keys=True))
```

## 5. Preservation and review boundary

This proposal adds this note, appends a reading pointer to the existing README,
and updates only that README inventory row plus this note's new row in
`SOURCE_FILES.json`. Original proof/checker/results and the normalized erratum
keep their exact hashes. Other inventory metadata and the original M1–M3 list
are unchanged; the diagnostic's M1–M5 are not that historical list.

A bounded nonauthor review is needed for (CR)/(SC), the exact density/domain
interpretation, constants and nonclaims, and the inventory/preservation delta.
This author's finite checks do not supply independent review or scientific
acceptance. The broader audit issue main#259 is not closed by this note.
