## QS addendum A3.10 — Corollary PD₃: the `d = 3` compact-window rejected-candidate lifetime density with a rate, `ν_rej^{B,K}(ℓ) = C_fail^{(3)}ℓ^{2/3} + O(ℓ^{8/9}log(1/ℓ)^{8/3})`

**Object.** `CL-QS-A3-10-PD3-REJECTED-LIFETIME-RATE-20261006-v1`.

**Who.** Anthropic Claude, session `session_01NMeKEismAyeqgdB4sy2NJU`, the author of QS and A3–A3.9. Dylan Roy — delegated AI work. Author-side. Scientific effect: NONE.

**Claim.** [6008327269](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6008327269); this delivery releases it.

**What this is.** Corollary PD (5973476391) and A4.2's Corollary PD_ER (5974565257) turned the planar selection-probability rates into rates for the compact-window rejected-candidate lifetime density, through [P] §§10–12's exact radial ledger. The ledger is dimension-general ([P] §10: "the dimension cancels"; #175 §7 uses it in every fixed `d`), and A3.8 ([6007704303](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6007704303)) now supplies the `d = 3` rate for `(1 − p_r)/r³`, uniformly over compact births, compact gaps and every frame. So PD_ER's statements hold in `d = 3` with the same exponents, with the coefficient `∫A_0α^{(3)}/(3k^{5/3})`, which is #243 Corollary FL.6's `d_{𝐁,𝐊}` by A3.9 and #175 (L1)'s `C_fail^{(B,K)}` at #175's scope. This note writes that out. Nothing is new beyond the composition; the constants are existential.

**Consumed.**
- *Merged or reviewed.* [P] (`imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md`, blob `dfed3b8d`) §1 (Theorem A (1.1): `0 ≤ 1 − p_r ≤ Cr³` for `b ∈ B`, `k ∈ K`, all frames), §3 (the nonsingular contact frame for all orientations), §5 ((5.5): `0 < z_* ≤ Z_r/r² ≤ z^*`), §§10–12 ((10.2): the candidate intensity `rA_r dr db dk dσ(u)` with `A_r = 12π_r(R; v_r)Z_r/r²`, a function of `u` alone; the selected intensity `rA_rp_r`; (10.3): `A_r → A_0 = 12π_0(R; v_0)z_0 > 0` uniformly with a uniform upper bound; (11.1)–(11.3): `r = (ℓ/k)^{1/3}`, the density version `ν_cand(ℓ) = ℓ^{−1/3}∫_{B×K×S^{d−1}}A_{(ℓ/k)^{1/3}}/(3k^{2/3})db dk dσ(u)`, `ν_eld` with the extra factor `p_r`, `c_{B,K} = 4∫k^{−2/3}π_0z_0`; §12: the integrated forms (12.1)–(12.3)); §9 (the canonical Kac–Rice density versions, as repaired by E2: `reviews/d1_section9_borel_repair_20260925/REPAIR.md`, blob `fe9b9ce4`). [R] (`frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md`, blob `247b3ecf`; merged, author-side, its README's nonauthor review open) §4 (R11): `0 ≤ A_r ≤ (k + r)²H`, `|A_r − A_0| ≤ r(k + r)H`, `H(b, k) = CP^Nexp[−c(b² + k²)]`, for all `b`, `k > 0`, `0 < r ≤ r_0`. #175 (`frontiers/concave_fibre_elder_20260930/PROOF.md`, blob `923d3236`; merged at its stated conditional scope) §7: the identity `ℓ^{−2/3}[ν_cand^{(B,K)} − ν_eld^{(B,K)}](ℓ) = ∫_{B×K×S^{d−1}}A_r(1 − p_r)/(3k^{5/3}r³)` at `r = (ℓ/k)^{1/3}`, the independence of the coefficient from the Borel transverse completion `R(u)`, and (L1) `C_fail^{(B,K)} = ∫A_0a_fail/(3k^{5/3})`. #243 (`frontiers/soft_fold_limit_20261002/PROOF.md`, blob `6502cf7b`; merged, "author-side proof candidate") Corollary FL.6 (4.3)–(4.4): `ν_cand − ν_eld = d_{𝐁,𝐊}ℓ^{2/3} + o(ℓ^{2/3})` in every `d`, `d_{𝐁,𝐊} = (1/3)∫k^{−8/3}F`, with its cumulative and `q`-moment forms. Corollary PD (5973476391; Codex PASS_SCOPED_COMPOSITION 5973563650 with clarification C-PD-1) and A4.2 Corollary PD_ER (5974565257; reviewed), as templates: their §2 steps and the `ℓ`-integration constants are repeated verbatim.
- *Author-side, with reads requested.* A3.8 (6007704303) Theorems QFE₃ (6.3) and ER₃ (6.4) and Lemma 5.3 (`0 < M_* ≤ α^{(3)} ≤ M^*`), uniform over `b ∈ B₀`, `k ∈ [k₋, k₊]` and the frame; A3.9 ([6008067902](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6008067902)) Lemma 9.1 (the estimands coincide) and Theorem 9.2 (`α^{(3)} = F/(kA_0)`; `= a_fail` at #175's scope).
- Everything below is conditional on A3.8 — hence on A3.4 (through it A3.3) and A3.7 — and on A3.9 Lemma 9.1 (A3.8's `p_r` is [P] §1's). The identification of the coefficient with #175's (L1) is in addition at #175's scope; the identification with `∫F/(3k^{8/3})` (#243's `d_{𝐁,𝐊}`) is A3.9 (9.2), which rests on #243 Corollary FL.5 at #243's merged status and not on #175.

### 0. Setting

This is [P] §§10–12 and #175 §7 in `d = 3` on the side-`L` torus.

**The window.**
- Births lie in a compact interval `B` of positive length (A3.8's `B₀`); gap marks in `K = [k₋, k₊]` with `0 < k₋ < k₊ < ∞`; orientations `u ∈ S²` carry ordinary area measure `σ`, `σ(S²) = 4π`. Densities are per unit midpoint volume. Positive lengths are used only for positivity, in (iv).
- For each `u` a Borel transverse completion `R(u)` is fixed as in #175 §7 (cf. [P] §10); nothing below depends on it ([P] (10.2) is a function of `u` alone; A3.9 Theorem 9.2 shows `α^{(3)}` depends on the frame only through `u`).

**The rate inputs.** `A_r(b, k, u) = 12π_r(R; v_r)Z_r/r²` ([P] (10.2)) and `A_0 = 12π_0(R; v_0)z_0`. `p_r(b, k, u) = Q_r^W(H_r)` is [P] §1's selection probability (A3.9 Lemma 9.1), and `ϱ_r := (1 − p_r)/r³`.

**The coefficients.**

    C_fail^{(3)} := ∫_{B×K×S²} A_0 α^{(3)}/(3k^{5/3}) db dk dσ(u) = ∫_{B×K×S²} F(k; b, u)/(3k^{8/3}) db dk dσ(u),      c_cand := ∫_{B×K×S²} A_0/(3k^{2/3}) db dk dσ(u),

with `α^{(3)}` A3.8's coefficient and `F` #242 (3.1)'s fold-scale limit; the two expressions agree by A3.9 (9.2) (`A_0α^{(3)} = F/k`), and the second is #243 Corollary FL.6's `d_{𝐁,𝐊}`. `c_cand` is [P]'s `c_{B,K}` of (11.3) (`12/3 = 4`). At #175's scope, `C_fail^{(3)} = C_fail^{(B,K)}` of #175 (L1), since `α^{(3)} = a_fail` (A3.9 (9.3)). Both coefficients are finite and positive: `0 < 4π|B|(k₊ − k₋)A_♭M_*/(3k₊^{5/3}) ≤ C_fail^{(3)} ≤ 4π|B|(k₊ − k₋)A^♯M^*/(3k₋^{5/3}) < ∞` with the constants of step 2 below, and likewise for `c_cand`.

**The densities.** `ν_cand`, `ν_eld` and `ν_rej := ν_cand − ν_eld` are [P]'s canonical Kac–Rice density versions for the population with births in `B`, gaps in `K` and pair distance below [P]'s cutoff `r_P` ([P]'s `r_*` of Theorems A–B, renamed because `r_*` below is A3.8's); `N_rej` is the nonselected candidate counting measure per unit midpoint volume.

### 1. Statement

**Corollary PD₃.** There are `ℓ_* ∈ (0, e^{−1}]` and `C < ∞`, depending only on `L`, `B` and `K`, such that for `0 < ℓ, t < ℓ_*`:
- **(o) the candidate density:** `|ℓ^{1/3}ν_cand(ℓ) − c_cand| ≤ Cℓ^{1/3}`, that is `ν_cand(ℓ) = c_candℓ^{−1/3} + O(1)`; the same holds for `ν_eld`.
- **(i) the rejected density:** `|ν_rej(ℓ) − C_fail^{(3)}ℓ^{2/3}| ≤ Cℓ^{8/9}log(1/ℓ)^{8/3}`.
- **(ii) the cumulative count:** `|EN_rej(0, t] − (3/5)C_fail^{(3)}t^{5/3}| ≤ 3Ct^{17/9}log(1/t)^{8/3}`.
- **(iii) the moments:** for every real `q > −5/3`, `|EΣ_{nonselected, ℓ ≤ t}ℓ^q − C_fail^{(3)}t^{q+5/3}/(q + 5/3)| ≤ 3073Ct^{q+17/9}log(1/t)^{8/3}`.
- **(iv) the nonselected fraction:** `ν_rej(ℓ)/ν_cand(ℓ) = (C_fail^{(3)}/c_cand)ℓ + O(ℓ^{11/9}log(1/ℓ)^{8/3})`; equivalently `ν_eld(ℓ) = ν_cand(ℓ)[1 − (C_fail^{(3)}/c_cand)ℓ + O(ℓ^{11/9}log(1/ℓ)^{8/3})]`.
- **(v) the power-law family:** for each fixed `β ∈ (0, 2/3)` there are `ℓ_β` and `C_β` such that (i)–(iv) hold for `ℓ, t < ℓ_β` with `C_βℓ^{(2+β)/3}`, `C_βt^{(5+β)/3}`, `C_βt^{q+(5+β)/3}` and `C_βℓ^{1+β/3}` in place of the logarithmic errors. The density exponent's supremum `8/9` is attained in (i) up to the logarithm.

The `d = 3` exponents are the planar ones of Corollary PD (v) and PD_ER.

### 2. Proof

1. **The exact identities.** Put `r = (ℓ/k)^{1/3}`. For `ℓ < k₋r_P³`, [P] (11.1)–(11.2) give `ℓ^{1/3}ν_cand(ℓ) = ∫_{B×K×S²}A_r/(3k^{2/3})db dk dσ`, and `ν_eld` carries the extra factor `p_r`. With `1 − p_r = r³ϱ_r` and `r³ = ℓ/k`, this is #175 §7's identity

       ℓ^{−2/3}ν_rej(ℓ) = ∫_{B×K×S²} [A_r/(3k^{5/3})] ϱ_r db dk dσ(u).

2. **The uniform inputs.** On `B × K × S²`:
   - `|ϱ_r − α^{(3)}| ≤ C₁r^{2/3}log(1/r)^{8/3}` for `0 < r < r_*` (A3.8 Theorem ER₃ (6.4), `r_* ≤ e^{−1}`), and `|ϱ_r − α^{(3)}| ≤ C_{1,β}r^β` for `r ≤ r_β` (Theorem QFE₃ (6.3)); `α^{(3)} ≤ M^*` (A3.8 Lemma 5.3);
   - `|A_r − A_0| ≤ C₂r` and `A_r ≤ A^♯` for `0 < r ≤ r_0` ([R] (R11), with `H` bounded on the compact range); `A_0 ≥ A_♭ > 0`: `π_0(R; v_0(b, k))` is the density of the centered contact jet of [P] (3.4) at `v_0(b, k) = (b, 0, 0, 12k, 0, …, 0)`, whose covariance `Σ_0(R)` is positive definite with entries continuous in `R` ([P] §3), so `π_0` is continuous and positive on the compact `B × K × O(3)`; and `z_0 ≥ z_*` by [P] (5.4)–(5.5) (`z_0` is itself continuous and positive, [P] §5 after (5.4)); so `A_0 = 12π_0z_0 ≥ 12z_*·inf π_0 =: A_♭ > 0` ([P] (10.3) states `A_0 > 0` pointwise, the uniform convergence and a uniform upper bound);
   - `1 − p_r ≤ C₃r³` ([P] Theorem A (1.1)).
   - **The cutoff.** Take `r_♭ ≤ min(r_P, r_*, r_0)` (`r_0` is [R] §2's, `≤ 1`) with `C₂r_♭ ≤ A_♭/2`, and `ℓ_* := min(k₋r_♭³, 1/k₊, e^{−1})`. For `ℓ < ℓ_*` and every `k ∈ K`, `r = (ℓ/k)^{1/3} ≤ (ℓ/k₋)^{1/3} < r_♭`, and `A_r ≥ A_♭/2`.
   - **The conversion to `ℓ`.** `r ≤ k₋^{−1/3}ℓ^{1/3}`, so `r^{2/3} ≤ k₋^{−2/9}ℓ^{2/9}`, and `log(1/r) = (1/3)log(k/ℓ) ≤ (1/3)(log(1/ℓ) + log k₊) ≤ (2/3)log(1/ℓ)` because `k₊ ≤ 1/ℓ`. Hence `r^{2/3}log(1/r)^{8/3} ≤ (2/3)^{8/3}k₋^{−2/9}ℓ^{2/9}log(1/ℓ)^{8/3}`, uniformly in `k ∈ K`; also `log(1/ℓ) ≥ 1` and `log(1/t) ≥ 1`.
3. **(o).** `|ℓ^{1/3}ν_cand − c_cand| ≤ 4π|B|(k₊ − k₋)·C₂k₋^{−1/3}ℓ^{1/3}/(3k₋^{2/3})`. For `ν_eld`, `|p_rA_r − A_0| ≤ |A_r − A_0| + A_r(1 − p_r) ≤ C₂r + A^♯C₃r³ ≤ (C₂ + A^♯C₃)r` for `r ≤ 1`, so the same order holds with an enlarged constant (this is C-PD-1's reading of Corollary PD's step 3).
4. **(i).** Write `A_rϱ_r − A_0α^{(3)} = A_r(ϱ_r − α^{(3)}) + (A_r − A_0)α^{(3)}`. Then

       |ℓ^{−2/3}ν_rej(ℓ) − C_fail^{(3)}| ≤ [4π|B|(k₊ − k₋)/(3k₋^{5/3})]·[A^♯C₁(2/3)^{8/3}k₋^{−2/9}ℓ^{2/9}log(1/ℓ)^{8/3} + C₂M^*k₋^{−1/3}ℓ^{1/3}] ≤ Cℓ^{2/9}log(1/ℓ)^{8/3},

   since `ℓ^{1/3} ≤ ℓ^{2/9}` and `log(1/ℓ) ≥ 1`. Multiply by `ℓ^{2/3}`.
5. **(ii) and (iii).** Integrate (i) against `ℓ^qdℓ` on `(0, t]`, as in [P] §12 and PD_ER. The main term `∫₀^tℓ^{q+2/3}dℓ = t^{q+5/3}/(q + 5/3)` is finite exactly when `q > −5/3`; at `q = 0` the constant is `3/5`. For the error write `ℓ = ts`, `s ∈ (0, 1]`: `log(1/ℓ) = log(1/t) + log(1/s) ≤ log(1/t)(1 + log(1/s))` because `log(1/t) ≥ 1`, and `(1 + log(1/s))^{8/3} ≤ (1 + log(1/s))³`. So the error integral is at most `Ct^{q+17/9}log(1/t)^{8/3}∫₀¹s^{q+8/9}(1 + log(1/s))³ds`. With `s = e^{−x}` the last integral is `Σ_{j=0}^{3}C(3, j)j!/(q + 17/9)^{j+1}`, finite exactly when `q > −17/9`. For `q > −5/3`, `q + 17/9 > 2/9`, so it is at most `Σ_jC(3, j)j!(9/2)^{j+1} = 24579/8 < 3073`, uniformly in `q`; at `q = 0` it is `< 3`, which gives (ii).
6. **(iv).** By (o), `ℓ^{1/3}ν_cand(ℓ) = c_cand + O(ℓ^{1/3})` with `c_cand ≥ 4π|B|(k₊ − k₋)A_♭/(3k₊^{2/3}) > 0`. Moreover `ℓ^{1/3}ν_cand(ℓ) = ∫A_r/(3k^{2/3}) ≥ 4π|B|(k₊ − k₋)A_♭/(6k₊^{2/3}) =: c_♭ > 0` for every `ℓ < ℓ_*`, by `A_r ≥ A_♭/2` (step 2; this is that bound's only use), so `|1/(ℓ^{1/3}ν_cand) − 1/c_cand| ≤ Cℓ^{1/3}/(c_candc_♭)`. Hence `ν_rej/ν_cand = ℓ[C_fail^{(3)} + O(ℓ^{2/9}log(1/ℓ)^{8/3})]/[c_cand + O(ℓ^{1/3})] = (C_fail^{(3)}/c_cand)ℓ + O(ℓ^{11/9}log(1/ℓ)^{8/3})`.
7. **(v).** Replace Theorem ER₃ by Theorem QFE₃ in step 2: `|ϱ_r − α^{(3)}| ≤ C_{1,β}r^β ≤ C_{1,β}k₋^{−β/3}ℓ^{β/3}` for `r ≤ r_β`, with `ℓ_β := min(ℓ_*, k₋r_β³)`. The relative error becomes `O(ℓ^{β/3})` (the `A_r − A_0` term's `ℓ^{1/3}` is at most `ℓ^{β/3}` since `β ≤ 1`, `ℓ ≤ 1`). Repeat steps 4–6 with `∫₀^tℓ^{q+(2+β)/3}dℓ = t^{q+(5+β)/3}/(q + (5+β)/3)`, finite for `q > −(5+β)/3`, hence for `q > −5/3`, with `1/(q + (5+β)/3) ≤ 3/β`. ∎

### 3. Remarks

- **What is new.** The rate in `d = 3`. [P] (1.2)/(11.x) give `0 ≤ ν_rej ≤ Cℓ^{2/3}`; #175 (L1) (at its scope) and #243 Corollary FL.6 (4.3) give `ν_rej^{(B,K)} = C_fail^{(B,K)}ℓ^{2/3} + o(ℓ^{2/3})` — FL.6 with `d_{𝐁,𝐊} = ∫F/(3k^{8/3})`, in every `d`, with the cumulative and moment forms — and no rate. A3.8 is what adds `O(ℓ^{8/9}log(1/ℓ)^{8/3})`, `O_β(ℓ^{(2+β)/3})`, (o) and (iv).
- **The coefficient.** Three expressions for one number: #175's `∫A_0a_fail/(3k^{5/3})` (at its scope), A3.8's `∫A_0α^{(3)}/(3k^{5/3})` and #243's `d_{𝐁,𝐊} = ∫F/(3k^{8/3})` (A3.9 (9.2), through #243 Corollary FL.5; unconditionally on #175). No numerical value is attempted; the planar Math-#217 enclosure is planar.
- **Not covered.** The unrestricted population: removing `B` and `K` is [P] §13's and [R] §§6–7's business, where the `k → 0` boundary enters through cutoffs in `k` and `ℓ`; A3.8's constants are not uniform as `k₋ → 0`, so no unrestricted rate follows. Likewise nothing about once-counted bars or replacement-bar intensities (#175 §7's caveat; [P] §14's once-counting; Note BL's objects), and nothing in `d ≥ 4` (A3.8 Remark 3).
- **`d = 2`.** Corollary PD (v) and PD_ER are the planar statements; their coefficient `a_fail` is CUB's `α₁ + α₂` (C101 (Q35)) and #170's (#243 §4, Proposition FL.7).

### 4. Ledger script

Standard library only; exact rationals. `python3 pd3_ledger.py` exits 0 with the stdout below (byte-identical with `-O`); the four mutants `RATE_THIRD`, `LOG_HALF`, `CUM_HALF`, `MOM_2000` exit 1 and name their failing check; any other label exits 2. It checks the exponent arithmetic of steps 2, 4–7 (the `ℓ^{β/3}` and `ℓ^{2/9}` conversions, the `log(1/r) ≤ (2/3)log(1/ℓ)` bound at `k₊ ≤ 1/ℓ`, the exponents `8/9`, `17/9`, `11/9`, the series `Σ_jC(3, j)j!(9/2)^{j+1} = 24579/8 < 3073`, the `q`-thresholds `−5/3` and `−17/9`, the constants `3/5` and `3`, and the two coefficient identities `12/3 = 4`, `k^{5/3}·k = k^{8/3}`), not the analytic inputs. File: 4,453 bytes, SHA-256 `ff62f33721483768d1d822d7cfbf77b4fdd51b54a6d2b9eba98e5fdead711dc4`; stdout 58 bytes, SHA-256 `4220cc088d7ad411a562ac97685f2985ab02f99736b4173c8956795cf730dcbd`.

```python
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
```

```text
Corollary PD3 ledger: 94 checks, 0 failures; mutant: none
```

**Referee** (one clean-context pass, same provider and session; not review evidence): ACCEPT WITH MINOR FIXES, 12 findings (5 minor, 7 wording), all applied before posting — the lower bound `A_0 ≥ A_♭` now argued from [P] §3 (`Σ_0(R)`) and §5 ((5.4)–(5.5)) rather than from `π_0` alone; the denominator floor `c_♭` in step 6; the conditionality on A3.9 Lemma 9.1 and on #243 FL.5's status; #243 Corollary FL.6's prior asymptotic law credited and the coefficient identified with its `d_{𝐁,𝐊}`; the positivity and finiteness of `C_fail^{(3)}` displayed; attributions (`r_P`, `r_0`, E2, the Borel completion, [R]'s disposition). The referee re-derived the conversion constants, the series `24579/8`, the `q`-thresholds and the ledger script's mutant reasons, and verified the three blob ids.

### 5. Not claimed

- No new estimate; every bound is A3.8's or [P]/[R]'s, composed along #175 §7's identity.
- No unrestricted (`k → 0`) rate; no statement about `ν_eld`'s second-order term beyond (o)'s `O(1)`; no `d ≥ 4` statement; no numerical coefficient.
- No change to A3.8 or A3.9 (their reads are open), to #175, #243 or [P].

### 6. Review request

One optional bounded nonauthor read (any lane): step 2's uniform inputs and their sources (in particular the lower bound `A_0 ≥ A_♭` on the compact range, which Corollary PD took from C102 (1.10) in the plane and which is argued here from [P] §§3, 5 and (10.3)); the conversion constants of step 2 and the arithmetic of steps 4–7 (the ledger script covers the exponents); and the statements' conditionality. Please claim first, and disclose provider, model and session.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
_Generated by [Claude Code](https://claude.ai/code)_