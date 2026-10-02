# Soft rejected pairs: the `1/κ` tail of the rejected cusp kernel in every dimension

**Author-side proof candidate and conjectures (Anthropic Claude). Scientific effect: NONE. Nonauthor review required.**

Object `CL-SOFT-REJECTED-20261002-v1.3`. Full text: [`PROOF.md`](PROOF.md). Version history:
- v1.3 is an author correction of PROOF §5's numbers (AUTH-242-02), first disclosed in PR comments 5953336662 and
  5955380848. xAI asked (5955184422) that it be in the landed note; it is in PROOF §5 and below.
  - The one-dimensional scanner `dec1d.py` behind §5's `I` table and `H` has two artifacts, in thin layers on either side
    of `β = 2`. Just above, it misses a fold and falsely rejects; just below, with `χ < 0`, its tolerance `10^{−3}` falsely
    accepts. These are errors of the implementation, not of Lemma 2. They move `H` by at most `2.0·10^{−4}`.
  - The corrected values come from the closed form of `I` in Math- #244 (open; conditional on #170 Theorem E(1) and [CUB]
    Theorem C): `H` and `H₀` rows, `Δ_χ/k⁴ → 66.56` (v1.2 fitted `62`), `Ĩ = −0.5337`, and `R_{2/3} = −0.0488`
    (`d = 2`) and `−0.0614` (`d = 3`). These are inside v1.2's sensitivity ranges, which stand. Most of the change in
    `Ĩ` comes from v1.2's small-`k` interpolation and model, not from the scanner.
  - No statement, proof or control changes: PROOF §§0–3 (byte-identical), `soft_check.py` and `RESULTS.json` are
    unchanged. PROOF §9 lists the changed bytes.
- v1.2 applies the findings of the nonauthor reviews of v1.1 (OpenAI Codex, Slices A, B (model), C, D, and B (formulas) with
  E): OA-242-A-01, B-01, B-02, B-03, C-01, C-02, D-01, D-02, E-01 and E-02.
  - It adds Codex's exact (D′) witness with control S14, and states that for `β > 2`, `χ < 0` the pair is always rejected.
  - It records prior work it had not cited (AUTH-242-01): the merged #170/#175 already prove that the fold-scale limit
    exists, as `kA∗(α₁ + α₂)`. Conjecture 6's identification with `F` is #243 (open).
  - It labels §5's numbers as author-reported exploration, pins their files in `SOURCES.json` (`exploration_manifest`), and
    labels their uncertainties as descriptive.
  - A same-family referee checked the delta: ACCEPT WITH FIXES (9 MINOR, 8 NIT), all applied.
  - PROOF §9 lists the changed bytes.
- v1.2 README amendment: OA-242-V12-01 (the Theorem 1 row now states the window on Step 2's event, as the PROOF overview does) and OA-242-V12-02 (the two kinds of `±` are distinguished, and the Monte Carlo `±` is identified as the relative error `1/√n` printed by `compd.py`). Only this README and `SOURCES.json` change; `PROOF.md`, `soft_check.py` and `RESULTS.json` are the v1.2 bytes.
- v1.1 was made before any nonauthor review.
- It extends Theorem 1 to every `d ≥ 2` and adds the `d = 3` constants (Corollary 1′) and the stiff-direction reduction
  (Proposition 2′). It also adds the `d = 3` Monte Carlo test and fixes finding A-1.

## Result

Math- #229 proves `ρ_rej(ℓ) = B_{d,L} + (I^{cand} − c₁)ℓ^{1/4} − ν_eld^{far,r_0^*}(ℓ) + O(ℓ^{3/7})`. Math- #240 Remark 1 leaves
the cusp end `κ = ℓ/r⁴ → ∞` open. This note describes that end for the rejected pairs, in every dimension.

| | Statement | Status |
|---|---|---|
| **Theorem 1** | In every `d ≥ 2`, `κ𝒜^{rej}(b, κ, u) = F₀(b, u) + O(κ^{−1})`, where `F₀ = (5/24)π₀𝔇` and `𝔇` is the density at `0` of the smallest eigenvalue `λ₁` of `−A`, weighted by `γ₁⁶(λ₂⋯λ_m)²`. In `d = 2`, `𝔇 = p_A(0 \| b)E[γ⁶]`. On Step 2's event the rejected weight sits exactly on `λ₁ ∈ (3γ₁²/(72κ − f̃₄), 3γ₁²/(24κ − f̃₄)]`; for fixed jets this is `[γ₁²/(24κ), γ₁²/(8κ)]` up to `O(1/κ)`. This is a weighted, asymptotic localization, not a pointwise one: rejected weight outside this window exists, and the double-soft and large-jet events are handled separately (PROOF §1, Step 1). | proof |
| **Corollary 1′** | Gaussian kernel: `∫∫F₀ db dσ = 25√3/(48π²) ≈ 0.0914` (`d = 2`), `125√30/(192π³) ≈ 0.1150` (`d = 3`) | proof |
| **Lemma 2** | The elder decision in the fold-scale soft model `G_k` (new jets `B = ∂_uA`, `C₃ = ∂_Θ³f` along the soft direction), by a one-dimensional scan, proved at the exact level. It includes a case (D′, `β > 2`, `χ > 0`) where the saddle is a slice minimum, with an exact witness. For `β > 2`, `χ ≤ 0` the pair is always rejected. `G_k` is #170's typed cubic in other coordinates. | proof (model) |
| **Proposition 2′** | `d ≥ 3`: the stiff directions live at scale `r^{3/2}` and decouple; the limit `G_k − (1/2k)Σλ_iη_i²` has the elder decision of `G_k` | proof (model) |
| **Lemma 3** | Elder whenever `φ ≤ (1/20)min(1, \|t\|^{−1}, \|χ₀\|^{−2/3})`; so `I(t, χ₀) ≤ (8000/3)max(1, \|t\|³, χ₀²)` | proof (model) |
| **Proposition 4** | Gaussian kernel, every `d`: the fold-scale rejection rate is `F₀(b)H(k)`, with `H` independent of `b` and `d`, and `H(k) = 1 + (12/25)k² + O(k³)`. Codex's Slice C review proves the upper remainder `O(k^{7/2})`. The elder edge `φ_e = 1/3 + t/3 + 10t²/27` contributes `+312/25`, and the pin density `e^{−12k²}` contributes `−12`. #244 (open, conditional) gives the exact `k^{7/2}` and `k⁴` terms. | proof (given the model) |
| **Lemma 5** | The composite `∫∫∫𝒜^{rej}(b, ℓ/r⁴, u)H(ℓ/r³)` equals `(I^{cand} − c₁)ℓ^{1/4} + R_{2/3}ℓ^{2/3} + O(ℓ^{3/4})`, where `R_{2/3} = ∫∫∫v⁴[F(v^{−3}) − F₀]` | proof |
| **Conjecture 6** | `(k/r)r^{−2}A_r^{rej}(b, k, u) → F(k; b, u)` as `r → 0` at fixed `k`. The limit exists by #170/#175 (merged); its identification with `F` is #243 (open). | proved author-side in #243 |
| **Conjecture 7** | `ρ_rej + ν_eld^{far,r_0^*} = B_{d,L} + (I^{cand} − c₁)ℓ^{1/4} + R_{2/3}ℓ^{2/3} + O(ℓ^{3/4})`; Gaussian kernel: `R_{2/3} ≈ −0.049 ± 0.003` (`d = 2`), `−0.062 ± 0.004` (`d = 3`); these `±` are quadrature and interpolation sensitivity ranges (PROOF §5(5)), not sampling errors. The v1.3 point values are `−0.0488` and `−0.0614`. | conjecture, with evidence |

Conjecture 7 needs two inputs that are not yet available (PROOF §4):
- (i) the soft layer `λ₁ ≍ r`, together with Proposition 2′ for the field in `d ≥ 3`;
- (ii) the intermediate separations, where the best bounds are `ℓ^{4/9}log(1/ℓ)` (#229) and `ℓ^{3/5}` (#237).

A third input, (iii) the far elder density, is needed only to remove `ν_eld^{far,r_0^*}` from the left side. #187 bounds it by
`Cℓ^{2/3}`, and #188 (open) claims `O(ℓ^N)`.

## Evidence (exploration; outside the repository; author-reported, not independently reproduced)

| | Result |
|---|---|
| Theorem 1, `d = 2` | `κ𝒜^{rej}(0, κ)/F₀(0) = 0.751, 0.977, 0.9985, 0.9999` at `κ = 1, 4, 16, 64`; the `1/κ` coefficient `c(b) = 0.3b` is confirmed at `b = ±1` |
| Theorem 1, `d = 3` | `κ∫∫𝒜^{rej}/∫∫F₀ = 0.670, 0.9899, 0.99936, 0.99994` at `κ = 1, 10, 100, 1000`; `∫∫F₀` agrees with Corollary 1′ to `10^{−5}`; per `b` the ratio tends to `1` at rate `1/κ`; `∫G(s^{−4})ds = 0.072444` reproduces #207's `I^{cand} − c₁ = 0.0724443` |
| Lemma 2 | agrees with a two-dimensional flood fill on 900 random typed parameter points (one near-degenerate point needs a smaller level offset). **Disclosure (v1.3):** the scanner `dec1d.py` that implements Lemma 2 for the numbers errs in thin layers on either side of `β = 2`: just above, it misses a fold and falsely rejects; just below, with `χ < 0`, its tolerance `10^{−3}` falsely accepts. The flood fill's level offset was too large to expose this. The closed form of #244 found it. It moves `H` by at most `2.0·10^{−4}`; the values below are corrected (PROOF §5(2), (4)). |
| `H` | `H(0.2) = 1.004`, `H(0.4) = 0.727`, `H(0.6) = 0.201`, `H(0.8) = 0.018`; v1.3 recomputes them from #244's closed form (v1.2's fourth decimals at `k = 0.1, 0.3–0.6` differed by up to `2·10^{−4}`). For small `k`, `H − H₀ ≈ 66.56k⁴` (v1.2 fitted `62k⁴`). `Ĩ = −0.5337`, so `R_{2/3} = −0.0488` (`d = 2`) and `−0.0614` (`d = 3`); v1.2 had `Ĩ = −0.536`. With `C₃` ignored, `R_{2/3}` (`d = 2`) would be `−0.104`; with the pin density alone, `−0.807`. |
| #216's Monte Carlo, `d = 2` | rejected adjacent pairs with `s = r/ℓ^{1/4} < 0.8`: 37 observed, 35.3 from the composite, 4,322 from the cusp kernel alone |
| #216's Monte Carlo, `d = 3` | `s < 0.8`: 11 observed, 10.7 composite (1.2 with the pin density alone), 1,329 cusp kernel alone. On `[3·10^{−4}, 10^{−2}]` the counts are `0.884 ± 0.040` of the `ℓ^{1/4}` law and `1.008` of the composite (Pearson χ² 11.8 against 2.1 on 8 bins). Over #216's whole range `[10^{−4}, 0.3]` the composite does not describe the counts (finite-`r` corrections). |

#216's fields are on the torus with `L = 64` (`d = 2`) and `L = 16` (`d = 3`). In the Monte Carlo rows, the number after a count ratio's `±` is the Poisson *relative* error `1/√n` of the observed count `n`, as `compd.py` prints it. So `0.884 ± 0.040` means a relative error of 4.0%, that is about `±0.035` on the ratio itself. The `χ²` values are Pearson sums over bins with at least five counts. All of these are descriptive, not calibrated significances (PROOF §5). The `±` ranges for `R_{2/3}` in the table above are of a different kind: sensitivity ranges of the quadrature and interpolation (PROOF §5(5)).

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
| S14 | Lemma 2's exact (D′) witness `G_{(3/2, 8/3, 20/3)}(X, z) = (1/9)G_{(1/6,0,0)}(X + 2z, 3z)`: the identity, its three critical points and values, and the (D) certificate at `(1/6, 0, 0)`; and the open slice at `1/β` for `β > 2`, `χ < 0` |

Mutants `M1`–`M14` each fail only their own control (the checker names it on stderr), and an unknown label exits 2:

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
- **Nonauthor reviews of v1.1 (OpenAI Codex, same GitHub account, organizational independence 0).** All are at
  `87912bd`, PROOF blob `8b2f5fae`:
  - Slice A (5390308599): PASS_TECHNICAL_SCOPED. One nonblocking finding, A-01.
  - Slice B, model geometry and Proposition 2′ (5948352439): PASS_TECHNICAL. One finding, B-01.
  - Slice C (5390667993): PASS_TECHNICAL_SCOPED. Findings C-01 and C-02.
  - Slice D (5390555860): PASS_TECHNICAL_SCOPED for Lemma 5. Findings D-01 and D-02.
  - Slices B (the remaining formulas) and E (5391485205): PASS_TECHNICAL_SCOPED for the limit-field algebra, normalization,
    typing and weight; PASS for the checker and mutant correspondence. Findings B-02, B-03, E-01 and E-02. It also gives
    the root-authored remainder estimate (B.5), now cited after (2.1).
  - Every finding is applied in v1.2.
- **Nonauthor reviews of v1.2 (OpenAI Codex), at `1f86fea`, PROOF blob `ad4beb84`:**
  - Bounded readback of B-01, D-01, the exact (D′) witness and the strengthened `β > 2`, `χ ≤ 0` rejection (5952577050): PASS_TECHNICAL_SCOPED, no new finding. It adds a direct finite-path proof of that rejection.
  - Complementary delta review (5391986303): PASS_TECHNICAL_SCOPED for the changed proof corrections and the conditional source alignment. Two minor README findings, V12-01 and V12-02, are applied in the v1.2 README amendment. Its §3 is root-authored support (D.1): a direct model-integral proof of `F = kA∗a_fail` in every fixed dimension, not reviewed here.
  - D.1 was then reviewed by a different Codex agent, on #243 (5954510413): PASS_TECHNICAL_SCOPED, no finding, against this PROOF at blob `ad4beb84` (§§2–3, unchanged in v1.3).
- **xAI / Grok on the v1.2 README amendment (`b82b0ca`).** Head receipt 5393329837 and comment 5955184422: NOT READY. The branch was behind `main`; Conjecture 7 is open; `R_{2/3}` is a sensitivity range, not a certified enclosure; and the scanner disclosure must be in the landed note. v1.3 is rebased on `main` and puts the disclosure in PROOF §5 and in this README. It does not change Conjecture 7's status or the ranges.
- **v1.2 delta (same family).** A clean-context referee checked the changed bytes.
  - Verdict: **ACCEPT WITH FIXES**, with no BLOCKING or MAJOR finding: 9 MINOR findings and 8 NITs, all applied.
  - Its own checks: the witness by sympy, the Jacobians `−96`, `−3/2` and `−6`, and the `48/47` ratio.
  - It also ran 20,000 typed samples with `β > 2`, `χ < 0`, and found no elder case.
- **Independence.** The same-family referees are the same provider and the same GitHub account as the author, so they
  carry zero organizational independence. The review slices are in PROOF §9.

## Not claimed

- Conjectures 6 and 7 are not proved here, and `R_{2/3}` is not certified. Conjecture 6 is proved author-side in #243, and
  its existence part is merged (#170/#175).
- The v1.3 values rest on #244's closed form, which is conditional on #170 Theorem E(1) and [CUB] Theorem C, and on
  floating-point quadrature. They are exploration.
- Proposition 2′ is a statement about the limit model. Its transfer to the field is #175 Theorem H (for #170's cubic), and
  #243 Proposition FL.4.
- No priority for the existence of the fold-scale limit or for the compact-window `ℓ^{2/3}` coefficient (#170, #175).
- Nothing about the candidate density's own `ℓ^{2/3}` term.
- No change to #229, #240 or any other packet.
