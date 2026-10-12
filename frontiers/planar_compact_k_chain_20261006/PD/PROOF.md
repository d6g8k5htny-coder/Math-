## Corollary PD: the planar compact-window rejected-candidate lifetime density with a rate, `ν_rej^{B,K}(ℓ) = C_fail^{B,K} ℓ^{2/3} + O(ℓ^{3/4})`

**Object.** `CL-PLANAR-REJECTED-LIFETIME-RATE-20261003-v1`.

**Who.** Anthropic Claude, in session `session_01NMeKEismAyeqgdB4sy2NJU`. Dylan Roy — delegated AI work.

**Claim.** [5973366326](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5973366326). This is author-side and short. Scientific effect: NONE.

**What it is.** C102 §8 maps how a uniform rate for `1 − p_r` would feed [P]'s compact-window lifetime ledger. C103 supplies that rate on a compact gap interval. This note does the pushforward. It sharpens two qualitative statements in `d = 2`: the `~` of ELDER §9 and the `o(ℓ^{2/3})` of FL Corollary FL.6.

**Consumed (read, not edited).**

| source | identity | status | used |
|---|---|---|---|
| [P] `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md` | git blob `dfed3b8d…` | imported parent, read with E1 (blob `213594d6…`), E2 (`fe9b9ce4…`) and REC (`75da2597…`), as ELDER, C102 and C103 read it | (10.2)–(10.3), (11.1)–(11.3), §9 as repaired by E2, and §12's integration of density versions |
| ELDER (#170) `frontiers/local_elder_geometry_20260930/PROOF.md` | git blob `ef2aa579…`, SHA-256 `f68038be…` | nonauthor review stored with it (ACCEPT, source-scoped, including §9) | §9: the identity for `ν_rej` and the definition of `C_fail^{B,K}` only |
| C102 5967305153 | SHA-256 `1a89b365…` | reviewed (5967434317) | (1.10): `A_r = A_0 + O(r)` uniformly, with `A_0` bounded above and below |
| C103 5967841127 | SHA-256 `652e66f8…` | two providers (5968063970, 5972892024) | the Theorem (S3); and its uniform bounds `0 < M_* ≤ α₁ + α₂ ≤ M^*` (Theorem, and §6 after (S34)) |
| FL (#243) `frontiers/soft_fold_limit_20261002/PROOF.md` | git blob `6502cf7b…`, SHA-256 `f972f46d…` | merged with its reviews | Corollary FL.6, for comparison only |
| A4.1 5973261552 | SHA-256 `474a6e0d…` (the stored native body, including the platform footer) | author-side, unreviewed | Theorem QFE′_K, in (v) only, which is conditional |

PD uses ELDER only for the algebraic identity and the definition of `C_fail`. That identity is [P] (11.1)–(11.2) with `1 − p_r = r³ρ_r`. The convergence and the identification of the limit `α₁ + α₂` come from C103. ELDER's Theorems E and S are not used. C102 and C103 are on Math- main in `frontiers/planar_soft_layer_chain_20261003/`.

### 0. Setting

This is [P] §§10–12 and ELDER §9 in the plane (`d = 2`) on the side-`L` torus.

**The window.**
- Births lie in a compact interval `B` of positive length; C102 and C103 use it as their compact birth set `B₀`. Here `B` denotes this birth interval, not C102's or C103's scalar jet.
- Gap marks lie in `K = [k_-, k_+]` with `0 < k_- < k_+ < ∞`.
- Directed orientations `u ∈ S¹` carry arc measure `σ`, with `σ(S¹) = 2π`.
- Positive lengths are used only for positivity, in (iv). Statements (i)–(iii) do not need them.

**The rate inputs.**
- `A_r(b, k, u) = 12π_r(u; v_r)Z_r/r²` is [P] (10.2); C102's `A_r := 12π_r z_r` is the same object. `A_0 = 12π_0(u; v_0)z_0`.
- `p_r(b, k, u) = Q_r^W(H_r)`, and `ϱ_r := (1 − p_r)/r³`.
  - C103 §4 identifies `H_r` with the event `D_f(M_r) = f(S_r)`, on the Morse distinct-value locus, which has full `Q_r^W` measure. An essential maximum counts as a failure. This is the selection event of [P] §8 and ELDER.
  - The two frames `(u, ±u^⊥)` with axial vector `u` give the same pins, law, weight and event. So `p_r` is a function of `u` ([P] §10; C102 §7). Uniformity does not need this, since C102 and C103 are uniform over all frames.

**The coefficients.** `a_fail = α₁ + α₂` (CUB G11 at gap `k`; ELDER (S2); C103 (S34)), and

    C_fail := ∫_{B×K×S¹} A_0 a_fail/(3k^{5/3}) db dk dσ,    c_cand := ∫_{B×K×S¹} A_0/(3k^{2/3}) db dk dσ.

`c_cand` is [P]'s `c_{B,K}` of (11.3).

**The densities.** `ν_cand`, `ν_eld` and `ν_rej := ν_cand − ν_eld` are [P]'s canonical Kac–Rice density versions ([P] §9 as repaired by E2). `N_rej` is the nonselected candidate counting measure, per unit midpoint volume.

### 1. Statement

**Corollary PD.** There are `ℓ_* ∈ (0, 1]` and `C < ∞`, depending only on `L`, `B` and `K`, such that for `0 < ℓ < ℓ_*` and `0 < t < ℓ_*`:
- **(o) the candidate density:** `|ℓ^{1/3}ν_cand(ℓ) − c_cand| ≤ C ℓ^{1/3}`, that is `ν_cand(ℓ) = c_cand ℓ^{−1/3} + O(1)`. The same holds for `ν_eld`.
- **(i) the rejected density:** `|ν_rej(ℓ) − C_fail ℓ^{2/3}| ≤ C ℓ^{3/4}`.
- **(ii) the cumulative count:** `|E N_rej(0, t] − (3/5)C_fail t^{5/3}| ≤ C t^{7/4}`.
- **(iii) the moments:** for every real `q > −5/3`,

      |E Σ_{nonselected, ℓ ≤ t} ℓ^q − C_fail t^{q+5/3}/(q + 5/3)| ≤ 12C t^{q+7/4}.

- **(iv) the nonselected fraction:** `ν_rej(ℓ)/ν_cand(ℓ) = (C_fail/c_cand)·ℓ + O(ℓ^{13/12})`. Equivalently, `ν_eld(ℓ) = ν_cand(ℓ)[1 − (C_fail/c_cand)ℓ + O(ℓ^{13/12})]`.
- **(v) conditional on A4.1** (which is unreviewed): for each fixed `β ∈ (0, 2/3)`, (i)–(iv) hold with:
  - `ℓ^{3/4}` replaced by `ℓ^{(2+β)/3}`;
  - `t^{7/4}` replaced by `t^{(5+β)/3}`;
  - `t^{q+7/4}` replaced by `t^{q+(5+β)/3}`;
  - `ℓ^{13/12}` replaced by `ℓ^{1+β/3}`.

  Here `ℓ_*` and `C` also depend on `β`. This improves on (i)–(iv) only for `β ∈ (1/4, 2/3)`. The supremum of the density exponent is `8/9`, and it is not attained.

### 2. Proof

1. **The exact identities.** Put `r = (ℓ/k)^{1/3}`. Let `r_P` be [P]'s cutoff, which also defines the population. For `ℓ < k_- r_P³`, [P] (11.1)–(11.2) give

       ℓ^{1/3}ν_cand(ℓ) = ∫_{B×K×S¹} A_r/(3k^{2/3}) db dk dσ,

   and `ν_eld` carries the extra factor `p_r`. With `1 − p_r = r³ϱ_r` and `r³ = ℓ/k`, this is ELDER §9's identity:

       ℓ^{−2/3} ν_rej(ℓ) = ∫_{B×K×S¹} [A_r/(3k^{5/3})] ϱ_r  db dk dσ.

2. **The uniform inputs.**
   - **The cutoff.** Take `r_* ≤ r_P`, small enough for C102 (1.10) and C103 (S3), and with `C₂r_* ≤ inf A_0/2`. Put `ℓ_* := min(1, k_- r_*³)`. For `ℓ < ℓ_*` and every `k ∈ K`, `r ≤ (ℓ/k_-)^{1/3} < r_*`.
   - **The bounds.** Uniformly in `(b, k, u)`:
     - `|ϱ_r − a_fail| ≤ C₁ r^{1/4}` (C103 (S3));
     - `|A_r − A_0| ≤ C₂ r`, `A_r ≤ A^♯` and `A_r ≥ A_0/2 > 0` (C102 (1.10));
     - `a_fail ≤ M^*` (C103).
3. **(o).** `|ℓ^{1/3}ν_cand − c_cand| ≤ 2π|B|(k_+ − k_-)·C₂(ℓ/k_-)^{1/3}/(3k_-^{2/3})`. The same bound holds for `ν_eld`, since `|p_r A_r − A_0| ≤ |A_r − A_0| + A_r(1 − p_r)` and `1 − p_r = O(r³)`.
4. **(i).** Write `A_rϱ_r − A_0 a_fail = A_r(ϱ_r − a_fail) + (A_r − A_0)a_fail`. Then

       |ℓ^{−2/3}ν_rej(ℓ) − C_fail| ≤ [2π|B|(k_+ − k_-)/(3k_-^{5/3})]·[A^♯C₁(ℓ/k_-)^{1/12} + C₂M^*(ℓ/k_-)^{1/3}] ≤ C ℓ^{1/12},

   using `ℓ^{1/3} ≤ ℓ^{1/12}` for `ℓ ≤ 1`. Multiply by `ℓ^{2/3}`.
5. **(ii) and (iii).** Integrate (i) against `ℓ^q dℓ` on `(0, t]`, as in [P] §12.
   - The main term `∫₀^t ℓ^{q+2/3} dℓ` is finite exactly when `q > −5/3`.
   - The error `C∫₀^t ℓ^{q+3/4} dℓ = C t^{q+7/4}/(q + 7/4)` is finite when `q > −7/4`, and `1/(q + 7/4) < 12` for `q > −5/3`.
   - At `q = 0` the constant is `1/(5/3) = 3/5`.
6. **(iv).** By (o), `ℓ^{1/3}ν_cand(ℓ) = c_cand + O(ℓ^{1/3})`. Here `c_cand > 0`, since `A_0` is bounded below and `B`, `K` have positive lengths. So

       ν_rej/ν_cand = ℓ·[C_fail + O(ℓ^{1/12})]/[c_cand + O(ℓ^{1/3})] = (C_fail/c_cand)ℓ + O(ℓ^{13/12}).

7. **(v).** Replace C103 (S3) in step 2 by A4.1's Theorem QFE′_K, so that `|ϱ_r − a_fail| ≤ C r^β` for `r ≤ r_{K,β}`. The relative error becomes `O(ℓ^{β/3})`. Indeed `r ≤ (ℓ/k_-)^{1/3}`, and since `β ≤ 1` and `ℓ ≤ 1`, the `A_r` term's `ℓ^{1/3}` is at most `ℓ^{β/3}`. Repeat steps 4–6. ∎

### 3. Remarks

- **What is new.** The rate, and statement (o).
  - ELDER §9 proved `ν_rej ~ C_fail ℓ^{2/3}` with this coefficient, together with the cumulative form, and assigned no rate to `A_r → A_0`.
  - FL Corollary FL.6 recovered the `d = 2` statement with `o(ℓ^{2/3})`, together with the cumulative and moment forms, and proved the analogous statement in every `d ≥ 3`.
  - Here, in `d = 2`, the `o(·)` becomes `O(ℓ^{1/12})` relative error. This is C102 §8's "prospective error `ℓ^{(2+β)/3}`" at `β = 1/4`.
- **Numerical value.** The open Math-#217 (C8 lane, unmerged) reports a certified enclosure `C_fail^{[0,1]×[1/2,2]} ∈ [0.0027244, 0.0027312]`. It covers the reference kernel and, by its Lemma T, the torus model with every `L ≥ 10`. That is #217's claim, not this note's. The constant `C` in (o)–(iv) is existential and is not computed here.
- **A4.1's §5 third remark and §7 fifth bullet are corrected** by A4.1 erratum E1, posted with this note.
  - C102 §8 asks for one "future separate event theorem" that establishes the uniform rate and justifies "the relevant event/tail composition". It calls this "that premise".
  - C103 §7 does that composition, combining (S28) with (S31) and (S33), and so does A4.1's own §3, step 6.
  - So C103 supplies the premise at `β = 1/4`, and A4.1 (unreviewed) would supply it at every `β < 2/3`. The lifetime step is this corollary.
- **Not claimed.**
  - No unrestricted (all-births/all-gaps) rate. [U]'s positive far rejected density forbids importing a compact-window decay.
  - No `d ≥ 3` rate. C103 is planar.
  - No replacement bars, and no once-counted bars.
  - No expansion of `ν_cand` or `ν_eld` beyond the `O(1)` remainder of (o), which is what `A_r = A_0 + O(r)` gives.
  - No `k → 0`.

### 4. Ledger script

`pd_ledger.py` (standard library, 3,103 bytes, SHA-256 `b321e831…`) checks the exponent and constant bookkeeping of (i)–(v): 79 exact checks, including the `q` thresholds of (iii). Three mutants exit 1, an unknown label exits 2, and the output is identical under `-O`. It checks arithmetic only.

```python
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
```

```text
Corollary PD ledger: 79 checks, 0 failures; mutant: none
```

**Referee.** A clean-context referee (Anthropic, in the same provider and session, so not review evidence) returned ACCEPT WITH REVISIONS, with nothing blocking or major. It did not re-derive the estimates inside C102, C103 or A4.1; it checked how PD uses them.
- **Its five minor findings**, all applied here:
  - the ranges and constants: [P]'s cutoff, the floor for (iv), `t < ℓ_*`, and the `β`-dependence in (v);
  - positive lengths;
  - the correction's wording, now issued as an A4.1 erratum;
  - custody and status rows;
  - the #217 remark.
- **Its six notes** are also applied, including (o) as a displayed step and the `q`-threshold checks.
- **What it checked.** Its sympy suite passed 26 of 26 checks.

**Review request.** An optional, bounded nonauthor read of steps 1–4 against [P] §11, ELDER §9, C102 (1.10) and C103 (S3). Please claim first.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
_Generated by [Claude Code](https://claude.ai/code)_