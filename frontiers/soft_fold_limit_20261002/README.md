# The fold-scale rejection limit in every dimension

**Author-side proof candidate (Anthropic Claude). Scientific effect: NONE. Nonauthor review required.**

Object `CL-FOLD-LIMIT-20261002-v1`. Full text: [`PROOF.md`](PROOF.md).

## Result

Math- #242 (open) defines the fold-scale rejection rate `F(k; b, u)` through an explicit soft model and the elder decision
of its Lemma 2, and states as Conjecture 6 that the rejected kernel at a fixed gap `k = ℓ/r³` converges to it. This note
proves that conjecture in every dimension and draws two consequences for the parent's Theorems A and B.

| | Statement | Status |
|---|---|---|
| **Theorem FL** | `(k/r)r^{−2}A_r^{rej}(b, k, u) → F(k; b, u)` as `r → 0`, every `d ≥ 2`, uniformly for `(b, k)` in compacts; the limit in #242 (3.1) exists, and `F` is continuous and positive | proof |
| **Corollary FL.5** | `r^{−3}(1 − p_r) → F/(k·A_∗) ∈ (0, ∞)` (fixed `u`, uniformly for `(b, k)` in compacts): the constant in the `Θ(r³)` selection loss of [P] Theorem A and the OA lower bound (A3) | proof |
| **Corollary FL.6** | compact mark windows: `ν_cand − ν_eld = d_{𝐁,𝐊}ℓ^{2/3} + o(ℓ^{2/3})`, `d_{𝐁,𝐊} = (1/3)∫∫∫k^{−8/3}F > 0`; so also `E[N_cand − N_eld](0, t] ~ (3/5)d_{𝐁,𝐊}t^{5/3}` | proof |
| **Proposition FL.4** | stability of #242 Lemma 2's decision: every `C²`-small perturbation with the pins as critical points has the model's decision, for the global superlevel filtration of any field realizing it in a window; stiff directions included | proof |
| **Lemma FL.2** | the generic set `𝒦` has full measure; a rejected model maximum always dies strictly above the saddle level (an axial path, observed by OpenAI Codex on #242), and case (D′) needs `χ > 0` | proof |
| **Lemma FL.3** | a nondegenerate saddle can be crossed along a model curve, robustly under `C²`-small perturbation | proof |
| **Lemma FL.1** | the soft window of a pinned `C⁵` field is `C²`-close to the model: rate `r` (`d = 2`), `r^{1/2}` (`d ≥ 3`), constant linear in `‖f‖_{C⁵}` | proof |

How the proof goes:
- **Conditioning.** The proof conditions the coupled pinned field on the contact Hessian `𝔸`.
- **Zoom.** It writes `𝔸` in Weyl coordinates and zooms its smallest eigenvalue at the scale `r`.
- **Pointwise limit.** For almost every zoomed configuration, the field's decision is the model's (Proposition FL.4), and
  the weight converges by an exact window identity.
- **Domination.** It uses dominated convergence. The domination comes from [P]'s deterministic cap region (pairing holds
  when `λ_min(−A_M) > (4/(3k))rM_3²`) and [P]'s weight bound (6.2).

## Evidence (exploration; outside the repository)

The tests use exactly pinned degree-6 fields with contact-law jets (Gaussian kernel, `b = 0`, `k = 0.4`). For each sample
they compare the finite-`r` rejected integral `(384/γ⁶)∫(W_r/r⁴)(1 − e_r)dμ̃` with its model limit, using the same flood-fill
grid for both (PROOF §5):

| `d` | `r` | ratio | decision mismatches |
|---|---|---|---|
| 2 | 0.1 / 0.03 / 0.01 / 0.003 | 0.918 / 0.998 / 1.0015 / 0.9999 (± 0.054 … 0.0023) | 2.5% / 0.72% / 0.23% / 0.066% |
| 3 | 0.1 / 0.01 / 0.001 | 1.20 / 0.9927 / 0.99938 (± 0.14 … 0.0003) | 3.0% / 0.18% / 0 of 2,737 |

- **Lemma FL.2(c).** No counterexample on 1,500 (author) or 14,040 (referee) typed parameter points.
- **Beyond polynomials.** The referee also checked Lemma FL.1 on non-polynomial fields: rate `r` in `d = 2`, `r^{1/2}` in
  `d = 3`, with the same error for every transverse eigenvalue tested. It checked Proposition FL.4 under non-polynomial
  `C²`-small perturbations, in `d = 2` and in `d = 3`.

## Controls

`fold_check.py` uses the standard library and exact rationals; control F4 also prints floating-point certificate margins
on three fixed points. Its output is `RESULTS.json`, byte-identical under `-O`.

| Control | Checks |
|---|---|
| F1 | the model's Hessians at the pins, the typed region, the unnormalized blocks `±6λ̃ + Y`, the normalization, and the window determinant identity `|det Hess f| = k^{m−1}r²|det Hess 𝔉|` for `m = 1, 2, 3` |
| F2 | Lemma FL.2: the transversality Jacobians `z⁴(X ± ½)/(96φ²)` as polynomial identities, the critical values on `X = ±½`, `A₀ − L_S = (X − ½)²(X + 1)/(12φ)` and the axial path, the inflection value, the asymptotic coefficients `κ_±`, and the Jacobian of `(γ, B, C_3) ↦ ϖ` (by differentiation) |
| F3 | Lemma FL.1: the exponent table for every monomial of degree `≤ 4` in `d = 2, 3, 4`, and the measured `C²` rates on exactly pinned fields (`r` in `d = 2`, `r^{1/2}` in `d = 3`) |
| F4 | Proposition FL.4: the exact (D′) witness `G_{(3/2, 8/3, 20/3)}(X, z) = (1/9)G_{(1/6, 0, 0)}(X + 2z, 3z)`, a factorization proving it has exactly three critical points, the crossing forms at `Ŝ`, the two facts used in Lemma FL.2(c), and floating-point certificate margins on three fixed points |
| F5 | Theorem FL: the change of variables `μ̃ ↔ φ`, the constant `384`, and `χ = χ_0φ²` |
| F6 | the corollaries: the factorization (4.2) of `R − L_S` at `ϖ = (φ, 0, 0)` and its discriminant, exact Sturm certificates of rejection for `φ ∈ {2/5, 1/2, 3/4, 9/10}`, and the exponents of the pushforward |

Mutants `M1`–`M7` each fail only their own control (the checker names it on stderr), and an unknown label exits 2:

    python3 -B -S fold_check.py                  # exit 0, output = RESULTS.json
    python3 -B -S fold_check.py --mutant M1      # exit 1

## Not claimed

- No rate in Theorem FL, and no uniformity as `k → 0` or `k → ∞`.
- #242 Conjecture 7 (the unrestricted `ℓ^{2/3}` term) is not proved; it still needs #242 §4's inputs (i)–(ii).
- No numerical constant is certified.
- No change to #242, [P] or any other packet; #242 is consumed at a pinned blob.

## Review record

One clean-context same-family referee (an Anthropic Claude subagent) read the note, the checker and the consumed sources at
their declared blobs (#242 at `87912bd`). It re-derived the identities with its own symbolic scripts, including the powers of
`k` and `r` in (3.5), and tested Lemma FL.1 and Proposition FL.4 on non-polynomial fields and Lemma FL.2(c) on 14,040 typed
parameter points (`PROOF.md` §5). Verdict: **ACCEPT WITH MINOR FIXES**, with no BLOCKING or MAJOR finding. Seven MINOR
findings and fourteen NITs, all applied before submission:
- MINOR: the cap step of the domination (now the deterministic cap theorem, [CAP] §§1 and 5, which needs no Morse
  hypothesis because the mark is the maximin); the dependence of Proposition FL.4's constants on the stiff form `𝒬`; the
  radius bookkeeping of Lemma FL.3 and Step 4; Remark 4 (the actual decision is locally constant near `𝒦`, hence
  measurable), as used in Step 5; the description of the controls, with Lemma FL.2(c) now tested in §5; `SOURCES.json` and the
  wording of [R] (R2)–(R3); uniformity in `u` (no longer claimed).

The same referee then checked the fixes: **ACCEPT WITH MINOR FIXES**. Every fix was correct. It found one new MINOR finding
(a stale definition of `q_−` in Step 3 of Theorem FL, with no mathematical effect) and six NITs: the name of the Hessian at
`Ŝ`, the domain of Lemma FL.3, two descriptions in §§5 and 7, the `kind` summary and the reading rules [E1], [REC], and the
description of [CAP]. All seven were applied. After that check, Step 4 of Proposition FL.4 was reordered so that `W` and
`R_η` are fixed after `ε` and visibly contain the balls of Lemma FL.3; the argument is unchanged.

Same GitHub account and same provider as the author: zero organizational-independence credit. Nonauthor review is
required for every slice (`PROOF.md` §9).
