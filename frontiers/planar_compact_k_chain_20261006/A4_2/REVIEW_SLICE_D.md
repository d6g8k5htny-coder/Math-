## A4.2 slice D nonauthor review — PASS_SCOPED, conditional; no required amendment

Dylan Roy — delegated AI review. Actual performer: OpenAI / Codex, root in the existing reader/handoff conversation (workspace 8d41438e1e36). This completes and releases **only** pickup [5975694119](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5975694119).

**Exact target:** [A4.2 5974565257](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5974565257), **§3 Corollary PD_ER (i)–(iv)** and its conversion proof. UTF-8 REST body, no added newline: **17,411 B**, SHA-256 `2dd72e3fee20aae4596aa0f24232872e5a4ad82a34d49c72a25cfc2a40150922`. Re-read immediately before verdict: unchanged and unedited. This is not a verdict on §1's JB_K/DB_K/ES_K/FT_K or §2's Theorem ER_K.

### Retained interfaces actually read
- [PD 5973476391](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5973476391): **14,294 B**, SHA-256 `7da0f672ab30a91a6e5787583326f0b14397a4addbb9e07b162cd2a3143e0e98`; §0 and §2 steps1–6.
- [C102 5967305153](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5967305153): **28,794 B**, SHA-256 `1a89b365bec20e353b84d5ac17b1acbe9179d48e4e4137e04d3c7e40ad207628`; (1.10)'s uniform `A_r=A_0+O(r)`, boundedness and positive floor.
- [P §§11–12](https://github.com/d6g8k5htny-coder/Math-/blob/42f19d7dc4109c2359520b7cbde24b6bb1fca110/imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md): **40,261 B**, blob `dfed3b8d318a3ab1950957f393307733a4bef3f2`, SHA-256 `9350ad6eaba6626b93c3dedeef9e2ff816e5cdf1c8318e85fb27499141c84bc7`. Exact pushforward and direct nonselected counting measure; not subtraction of infinite moments.
- C103's population/selection interface, as retained by PD, was read from 5967841127. Its proof is not reaccepted here.
- **Assumption for this slice:** ER_K's compact-K uniform bound `|ϱ_r−a_fail|≤C r^(2/3)log(1/r)^(8/3)`. Establishing that input remains outside this verdict.

### Analytic review

**1. Cutoff and logarithm.** Shrink the retained PD cutoff so `r_*≤r_K`, and take `ℓ_*≤min(k_-r_*³,1/k_+,e^(-1))`. For every `k∈K` and `ℓ<ℓ_*`, `r=(ℓ/k)^(1/3)<r_*`. Also `k≤1/ℓ`, so
`0<log(1/r)=(1/3)log(k/ℓ)≤(2/3)log(1/ℓ)`.
Together with `r^(2/3)≤k_-^(-2/9)ℓ^(2/9)`, this gives the stated uniform transformed error. There is no hidden small-k limit: the constant depends on the fixed positive `k_-`.

**2. Density.** P (11.1)–(11.2) with the failure factor `1−p_r=r³ϱ_r` gives exactly
`ℓ^(-2/3)ν_rej=∫ A_rϱ_r/(3k^(5/3))`.
Split `A_rϱ_r−A_0a_fail=A_r(ϱ_r−a_fail)+(A_r−A_0)a_fail`. Compactness, the bounded interfaces and ER_K give
`|ℓ^(-2/3)ν_rej−C_fail|≤C[ℓ^(2/9)log(1/ℓ)^(8/3)+ℓ^(1/3)]`.
Because `ℓ≤e^(-1)`, the latter term is dominated by the former. Multiplication by `ℓ^(2/3)` yields (i), exponent **8/9**.

**3. Cumulative and weighted moments.** The nonselected counting measure itself is positive, so Tonelli applies to `ℓ^q` even for negative q. The main integral is finite for `q>−5/3`, with coefficient `1/(q+5/3)`. Substitute `ℓ=ts`, write `A=log(1/t)≥1`, and use
`[A+log(1/s)]^(8/3)≤A^(8/3)[1+log(1/s)]³`.
Put `a=q+17/9`. The remaining majorant is
`J(a)=∫₀¹s^(a−1)(1+log(1/s))³ds=1/a+3/a²+6/a³+6/a⁴`,
by `s=e^(-x)` and integration by parts. It is finite for `a>0) and decreases strictly there. For `q>−5/3`, `a>2/9`, hence
`J(a)<J(2/9)=24579/8=3072.375<3073`.
Thus (iii)'s constant is genuinely uniform in q on the entire stated open range. At `q=0`,
`J(17/9)=228168/83521<3`,
giving (ii), with main coefficient **3/5** and error exponent **17/9**. The logarithmic error alone has threshold `q>−17/9`; the stricter `q>−5/3` comes from the main term. No divergent candidate-minus-selected expectations are used.

**4. Fraction.** Retained PD (o) supplies `ℓ^(1/3)ν_cand=c_cand+O(ℓ^(1/3))`, with `c_cand>0`. Shrink the cutoff to keep the denominator above `c_cand/2`. Dividing (i) by this density gives the main factor `ℓ`; the numerator error contributes `ℓ^(11/9)log(1/ℓ)^(8/3)`, while the denominator error is `O(ℓ^(4/3))` and is dominated. This proves (iv).

### Independent finite arithmetic evidence
I used my own exact rational calculation, not the author's checker; one local Python invocation completed with exit0. It checked both constants, the three exponents and 50 q-values just above the main integrability threshold. These checks corroborate arithmetic; the all-q result follows from the analytic monotonicity above. The core calculation is fully reproducible:

```python
from fractions import Fraction as F
from math import comb, factorial
def J(a):
    return sum(F(comb(3,j)*factorial(j),1)/a**(j+1) for j in range(4))
print(J(F(17,9)))  # 228168/83521
print(J(F(2,9)))   # 24579/8
density_error = F(-1,3) + 1 + F(2,3)/3
print(density_error, density_error+1, density_error+F(1,3))
# 8/9 17/9 11/9
```

### Boundaries, exposure and release
**PASS_SCOPED for the conditional §3 conversion; no required or optional amendment.** Retain ER_K as an unresolved premise until §1–§2 receive their own substantive reviews. This verdict does not accept those lemmas, extend to shrinking/growing K, higher dimension, replacement/once-counted bars, unrestricted lifetime laws, source-to-Lean alignment or scientific status.

Source-exposed reviewer; previous A4.1 review work and C124 reader/publication context disclosed. No A4.2/PD authorship is established in this conversation. C103/C124 OpenAI-source exposure is retained rather than counted as independent acceptance. Author controls were not read or run for this slice. Actual author of A4.2/PD: Anthropic Claude; actual reviewer: OpenAI/Codex; same GitHub account, **organizational-independence credit0**. Owner-reported ongoing review is separate, with no further human-review gate requested.

Fresh main229 read through pickup5975694119 and live refs main9093629769f40db76f1311d8ee920d5a82a38b89 / Math42f19d7dc4109c2359520b7cbde24b6bb1fca110 were unchanged. No competing slice-D pickup observed. **Claim5975694119 released on publication.** No branch, source, register, UI, Lean, acceptance label or merge changed. Next unresolved work: A4.2 slices A–C (§1 transfers and §2 assembly). Scientific effect NONE.
