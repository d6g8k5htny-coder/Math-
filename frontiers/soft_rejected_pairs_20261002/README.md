# Soft rejected pairs: the `1/κ` tail of the rejected cusp kernel in every dimension

**Author-side proof candidate and conjectures (Anthropic Claude). Scientific effect: NONE. Nonauthor review required.**

Object `CL-SOFT-REJECTED-20261002-v1.1`. Full text: [`PROOF.md`](PROOF.md). Version history:
- v1.1 was made before any nonauthor review.
- It extends Theorem 1 to every `d ≥ 2` and adds the `d = 3` constants (Corollary 1′) and the stiff-direction reduction
  (Proposition 2′). It also adds the `d = 3` Monte Carlo test and fixes finding A-1.

## Result

Math- #229 proves `ρ_rej(ℓ) = B_{d,L} + (I^{cand} − c₁)ℓ^{1/4} − ν_eld^{far,r_0^*}(ℓ) + O(ℓ^{3/7})`. Math- #240 Remark 1 leaves
the cusp end `κ = ℓ/r⁴ → ∞` open. This note describes that end for the rejected pairs, in every dimension.

| | Statement | Status |
|---|---|---|
| **Theorem 1** | In every `d ≥ 2`, `κ𝒜^{rej}(b, κ, u) = F₀(b, u) + O(κ^{−1})`, where `F₀ = (5/24)π₀𝔇` and `𝔇` is the density at `0` of the smallest eigenvalue `λ₁` of `−A`, weighted by `γ₁⁶(λ₂⋯λ_m)²`. In `d = 2`, `𝔇 = p_A(0 \| b)E[γ⁶]`. The rejected weight sits on `λ₁ ∈ [γ₁²/(24κ), γ₁²/(8κ)]`. | proof |
| **Corollary 1′** | Gaussian kernel: `∫∫F₀ db dσ = 25√3/(48π²) ≈ 0.0914` (`d = 2`), `125√30/(192π³) ≈ 0.1150` (`d = 3`) | proof |
| **Lemma 2** | The elder decision in the fold-scale soft model `G_k` (new jets `B = ∂_uA`, `C₃ = ∂_Θ³f` along the soft direction), by a one-dimensional scan, including a case where the saddle is a slice minimum | proof (model) |
| **Proposition 2′** | `d ≥ 3`: the stiff directions live at scale `r^{3/2}` and decouple; the limit `G_k − (1/2k)Σλ_iη_i²` has the elder decision of `G_k` | proof (model) |
| **Lemma 3** | Elder whenever `φ ≤ (1/20)min(1, \|t\|^{−1}, \|χ₀\|^{−2/3})`; so `I(t, χ₀) ≤ (8000/3)max(1, \|t\|³, χ₀²)` | proof (model) |
| **Proposition 4** | Gaussian kernel, every `d`: the fold-scale rejection rate is `F₀(b)H(k)`, with `H` independent of `b` and `d`, and `H(k) = 1 + (12/25)k² + O(k³)`. The elder edge `φ_e = 1/3 + t/3 + 10t²/27` contributes `+312/25`, and the pin density `e^{−12k²}` contributes `−12`. | proof (given the model) |
| **Lemma 5** | The composite `∫∫∫𝒜^{rej}(b, ℓ/r⁴, u)H(ℓ/r³)` equals `(I^{cand} − c₁)ℓ^{1/4} + R_{2/3}ℓ^{2/3} + O(ℓ^{3/4})`, where `R_{2/3} = ∫∫∫v⁴[F(v^{−3}) − F₀]` | proof |
| **Conjecture 6** | `(k/r)r^{−2}A_r^{rej}(b, k, u) → F(k; b, u)` as `r → 0` at fixed `k` | conjecture |
| **Conjecture 7** | `ρ_rej + ν_eld^{far,r_0^*} = B_{d,L} + (I^{cand} − c₁)ℓ^{1/4} + R_{2/3}ℓ^{2/3} + O(ℓ^{3/4})`; Gaussian kernel: `R_{2/3} ≈ −0.049 ± 0.003` (`d = 2`), `−0.062 ± 0.004` (`d = 3`) | conjecture, with evidence |

Conjecture 7 needs two inputs that are not yet available (PROOF §4):
- (i) the soft layer `λ₁ ≍ r`, together with Proposition 2′ for the field in `d ≥ 3`;
- (ii) the intermediate separations, where the best bounds are `ℓ^{4/9}log(1/ℓ)` (#229) and `ℓ^{3/5}` (#237).

A third input, (iii) the far elder density, is needed only to remove `ν_eld^{far,r_0^*}` from the left side. #187 bounds it by
`Cℓ^{2/3}`, and #188 (open) claims `O(ℓ^N)`.

## Evidence (exploration; outside the repository)

| | Result |
|---|---|
| Theorem 1, `d = 2` | `κ𝒜^{rej}(0, κ)/F₀(0) = 0.751, 0.977, 0.9985, 0.9999` at `κ = 1, 4, 16, 64`; the `1/κ` coefficient `c(b) = 0.3b` is confirmed at `b = ±1` |
| Theorem 1, `d = 3` | `κ∫∫𝒜^{rej}/∫∫F₀ = 0.670, 0.9899, 0.99936, 0.99994` at `κ = 1, 10, 100, 1000`; `∫∫F₀` agrees with Corollary 1′ to `10^{−5}`; per `b` the ratio tends to `1` at rate `1/κ`; `∫G(s^{−4})ds = 0.072444` reproduces #207's `I^{cand} − c₁ = 0.0724443` |
| Lemma 2 | agrees with a two-dimensional flood fill on 900 random typed parameter points (one near-degenerate point needs a smaller level offset) |
| `H` | `H(0.2) = 1.004`, `H(0.4) = 0.727`, `H(0.6) = 0.201`, `H(0.8) = 0.018`. With `C₃` ignored, `R_{2/3}` (`d = 2`) would be `−0.104`; with the pin density alone, `−0.807`. |
| #216's Monte Carlo, `d = 2` | rejected adjacent pairs with `s = r/ℓ^{1/4} < 0.8`: 37 observed, 35.3 from the composite, 4,322 from the cusp kernel alone |
| #216's Monte Carlo, `d = 3` | `s < 0.8`: 11 observed, 10.7 composite (1.2 with the pin density alone), 1,329 cusp kernel alone. On `[3·10^{−4}, 10^{−2}]` the counts are `0.884 ± 0.040` of the `ℓ^{1/4}` law and `1.008` of the composite (χ² 11.8 against 2.1 on 8 bins). Over #216's whole range `[10^{−4}, 0.3]` the composite does not describe the counts (finite-`r` corrections). |

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
| S11 | Theorem 1 in `m = 2, 3` rational eigenframes: the soft-window algebra with the factor `(λ₂⋯λ_m)²` and the double-soft implication |
| S12 | the Gaussian kernel in `d = 3`: the GOE law of `A`, the laws used in Corollary 1′, the odd jets along a rotated direction, the prefactor `(2π)^{−d}/(6√π)` from exact covariances, and the two constants |
| S13 | the expansion (2.6) of Proposition 2′ on exactly pinned degree-6 fields in `d = 3`, including the `r^{1/2}`-correction |

Mutants `M1`–`M13` each fail only their own control (the checker names it on stderr), and an unknown label exits 2:

    python3 -B -S soft_check.py                  # exit 0, output = RESULTS.json
    python3 -B -S soft_check.py --mutant M1      # exit 1

## Review record

- **Same-family referee on v1.** A clean-context referee (Anthropic Claude) read v1 against its sources at the declared
  blobs.
  - Its verdict was **MAJOR REVISION**, with no BLOCKING finding: one MAJOR finding (Conjecture 7 must keep the far elder
    density and state the missing inputs (ii)–(iii)), eight MINOR findings and nineteen NITs. All of them are applied.
  - Its delta check was **ACCEPT WITH MINOR FIXES**; its three MINOR findings and seven NITs are applied.
  - The referee also made independent checks: a sympy derivation of (2.1), the contact law of the Gaussian kernel, a
    quadrature of Theorem 1, a 500-point two-dimensional test of Lemma 2, the `I(t, 0)` table, and `H₀`.
- **v1.1.** A second clean-context same-family referee checked the delta (`REFEREE_B.md` in the project archive).
  - Its verdict was **ACCEPT WITH MINOR FIXES**: no BLOCKING or MAJOR finding, four MINOR findings and fourteen NITs. All
    are applied.
  - The MINOR findings were: Step 3 of Theorem 1 must bound the main term on the excluded sets; the `d = 3` `s`-integral
    needed a refined grid; the `d = 3` Monte Carlo statement overread #216's fit; and the packaging.
  - Its independent checks: the Gaussian-kernel laws by symbolic differentiation; both constants of Corollary 1′ by the
    per-`b` route; a Monte Carlo of `𝔡(b)`; an independent quadrature of `G₃` (agreeing to `3·10^{−7}`); (2.6) symbolically
    in `d = 3, 4`; the Hessian factor `(λ₂⋯λ_m)²`; and the mutant isolation matrix.
- **Independence.** The referees are the same provider and the same GitHub account as the author, so they carry zero
  organizational independence. Nonauthor review is required; the review slices are in PROOF §9.

## Not claimed

- Conjectures 6 and 7 are not proved, and `R_{2/3}` is not certified.
- Proposition 2′ is a statement about the limit model; its transfer to the field is part of Conjecture 6.
- Nothing about the candidate density's own `ℓ^{2/3}` term.
- No change to #229, #240 or any other packet.
