# Soft rejected pairs in `d = 2`

**Author-side proof candidate and conjectures (Anthropic Claude). Scientific effect: NONE. Nonauthor review required.**

Object `CL-SOFT-REJECTED-20261002-v1`. Full text: [`PROOF.md`](PROOF.md).

## Result

Math- #229 proves `ρ_rej(ℓ) = B_{d,L} + (I^{cand} − c₁)ℓ^{1/4} − ν_eld^{far,r_0^*}(ℓ) + O(ℓ^{3/7})`. Math- #240 Remark 1 leaves
the cusp end `κ = ℓ/r⁴ → ∞` open. In `d = 2` this note describes that end.

| | Statement | Status |
|---|---|---|
| **Theorem 1** | `κ𝒜^{rej}(b, κ, u) = F₀(b, u) + O(κ^{−1})`, with `F₀ = (5/24)π₀p_A(0 \| b)E[γ⁶]` (Gaussian kernel: `25π₀p_A(0 \| b)`). The rejected weight sits on `λ = −A ∈ [γ²/(24κ), γ²/(8κ)]`. | proof |
| **Lemma 2** | The elder decision in the fold-scale soft model `G_k` (new jets `B = ∂_uA`, `C₃ = ∂_Θ³f`), by a one-dimensional scan, including a case where the saddle is a slice minimum | proof (model) |
| **Lemma 3** | Elder whenever `φ ≤ (1/20)min(1, \|t\|^{−1}, \|χ₀\|^{−2/3})`; so `I(t, χ₀) ≤ (8000/3)max(1, \|t\|³, χ₀²)` | proof (model) |
| **Proposition 4** | Gaussian kernel: the fold-scale rejection rate is `F₀(b)H(k)` with `H(k) = 1 + (12/25)k² + O(k³)`. The elder edge `φ_e = 1/3 + t/3 + 10t²/27` contributes `+312/25`, and the pin density `e^{−12k²}` contributes `−12`. | proof (given the model) |
| **Lemma 5** | The composite `∫∫∫𝒜^{rej}(b, ℓ/r⁴, u)H(ℓ/r³)` equals `(I^{cand} − c₁)ℓ^{1/4} + R_{2/3}ℓ^{2/3} + O(ℓ^{3/4})`, where `R_{2/3} = ∫∫∫u⁴[F(u^{−3}) − F₀]` | proof |
| **Conjecture 6** | `(k/r)r^{−2}A_r^{rej}(b, k, u) → F(k; b, u)` as `r → 0` at fixed `k` | conjecture |
| **Conjecture 7** | `ρ_rej + ν_eld^{far,r_0^*} = B_{2,L} + (I^{cand} − c₁)ℓ^{1/4} + R_{2/3}ℓ^{2/3} + O(ℓ^{3/4})`; Gaussian kernel: `R_{2/3} ≈ −0.049 ± 0.003` | conjecture, with evidence |

Conjecture 7 needs two inputs that are not yet available (PROOF §4):
- (i) the soft layer `λ ≍ r`;
- (ii) the intermediate separations, where the best bounds are `ℓ^{4/9}log(1/ℓ)` (#229) and `ℓ^{3/5}` (#237).

A third input, (iii) the far elder density, is needed only to remove `ν_eld^{far,r_0^*}` from the left side. #187 bounds it by
`Cℓ^{2/3}`, and #188 (open) claims `O(ℓ^N)`.

## Evidence (exploration; outside the repository)

| | Result |
|---|---|
| Theorem 1 | `κ𝒜^{rej}(0, κ)/F₀(0) = 0.751, 0.977, 0.9985, 0.9999` at `κ = 1, 4, 16, 64`; the `1/κ` coefficient `c(b) = 0.3b` is confirmed at `b = ±1` |
| Lemma 2 | agrees with a two-dimensional flood fill on 900 random typed parameter points (one near-degenerate point needs a smaller level offset) |
| `H` | `H(0.2) = 1.004`, `H(0.4) = 0.727`, `H(0.6) = 0.201`, `H(0.8) = 0.018`. With `C₃` ignored, `R_{2/3}` would be `−0.104`; with the pin density alone, `−0.807`. |
| #216's Monte Carlo | rejected adjacent pairs with `s = r/ℓ^{1/4} < 0.8`: 37 observed, 35.3 from the composite, 4,322 from the cusp kernel alone |

## Controls

`soft_check.py` uses the standard library and exact rationals; control S8 is a fixed floating-point implementation of
Lemma 2. Its output is `RESULTS.json`, byte-identical under `-O`.

| Control | Checks |
|---|---|
| S1 | Theorem 1: the change of variables (`1/384`), `∫_{1/3}^1(φ^{−4} − φ^{−2}) = 20/3`, `5/24`, the factor `25` |
| S2 | the algebra of `G_k`: derivatives, pins, `det H_M = 6λ̃ + Y`, `det H_S = −6λ̃ + Y`, the normalization, weight and measure, the typed window |
| S3 | Gaussian kernel: given `∇f = 0`, the third-order jets are independent with variances `(6, 2, 2, 6)` and uncorrelated with even jets; `a′ = 12` |
| S4 | the elder edge (3.3) by exact truncated series; the double zero at `t = 0`; the Jacobian |
| S5 | `I(t, 0) = 20/3 − 20t + (52/3)t² + O(t³)` |
| S6 | `E[γ⁶t²] = 576k²`, `h₂ = 312/25`, `312/25 − 12 = 12/25`, the moment identities |
| S7 | every inequality in the proof of Lemma 3, with exact rational bounds |
| S8 | Lemma 2 on 16 fixed parameter points with known answers, including case (D′) |
| S9 | Lemma 5's error exponents (all `3/4`) |
| S10 | the limit field (2.1), including its `r`-correction, on exactly pinned degree-6 fields |

Mutants `M1`–`M10` each fail only their own control, and an unknown label exits 2:

    python3 -B -S soft_check.py                  # exit 0, output = RESULTS.json
    python3 -B -S soft_check.py --mutant M1      # exit 1

## Review record

- **Same-family referee.** A clean-context referee (Anthropic Claude) read the note against its sources at the declared blobs.
  Its verdict was **MAJOR REVISION**, with no BLOCKING finding:
  - one MAJOR finding: Conjecture 7 must keep the far elder density and state the missing inputs (ii)–(iii);
  - eight MINOR findings and nineteen NITs.
  All of them are applied. Among them:
  - the definition of `F` and `R_{2/3}` for the torus field;
  - Lemma 2's genericity hypothesis;
  - a false closed form for `I(t, 0)` on `[t*, 1)`;
  - one number in Theorem 1's remarks;
  - a new control S10 for the limit field (2.1).
- **The referee's independent checks.** A sympy derivation of (2.1); the contact law of the Gaussian kernel; an independent
  quadrature of Theorem 1; a 500-point two-dimensional test of Lemma 2; the `I(t, 0)` table; `H₀`.
- **Delta check of the revision** (the same referee): **ACCEPT WITH MINOR FIXES**, with no BLOCKING or MAJOR finding. Its three
  new MINOR findings and seven NITs are applied:
  - Lemma 2's genericity hypothesis, in its final form;
  - input (ii) now accounts for the composite's own part at small `κ`;
  - `H₀` had truncated the small-`γ` end. Correcting it moves `R_{2/3}` from `−0.050` to `−0.049`, inside the quoted
    uncertainty.
- **Independence.** The referee is the same provider and the same GitHub account as the author, so it carries zero
  organizational independence. Nonauthor review is required; the review slices are in PROOF §9.

## Not claimed

- Conjectures 6 and 7 are not proved, and `R_{2/3}` is not certified.
- Nothing for `d ≥ 3`.
- Nothing about the candidate density's own `ℓ^{2/3}` term.
- No change to #229, #240 or any other packet.
