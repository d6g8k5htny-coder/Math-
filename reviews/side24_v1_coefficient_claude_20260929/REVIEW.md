# Nonauthor review: D3 SIDE24 coefficient package `coefficients/side24_v1` (second provider)

Object: CL-SIDE24-V1-REVIEW-20260929-v1. Reviewer: Anthropic / Claude (see provenance).

Scientific effect: **NONE**. This file records verdicts on an existing, unchanged package. It does not
change `lemma_closed`, prizes, premises, `STATUS`, `PROOF_INDEX`, `GRAPH`, `claims/LANDING_CLAIMS.json`
or any author source. The D3 disposition (REVIEWED_SCOPED, arithmetic enclosure of the stated
expression only) is not altered; this review adds a second nonauthor provider to its record.

## Object reviewed

All paths on Math- `main` at `3216e2e7153f9f07acedb70b97d9ab5a0d82ed47` (2026-09-29). The blobs are
byte-identical to the ones the first nonauthor review bound at `e329fba1e927a12dbb4f0d1556f85f39284d17a9`.

| Path | Blob | Bytes | SHA256 |
|---|---|---|---|
| `coefficients/side24_v1/PROOF.md` (SIDE24-COEFFICIENT-D23-20260924-v1, OpenAI / ChatGPT) | `44b66f04f89fcd87383b3603fa69f1feb64cdddd` | 10272 | `c06daccc4ba4b9168522b9888b76a7d599934fc3b91bd753ee5d492262917769` |
| `coefficients/side24_v1/coefficient.py` | `c2d3ff339f2b9953ec08e676240cdc5edcb17a3e` | 8073 | `03ae6d0f15160cb681f9bbb19a84dc861c3a0db3e881291ea621061cc90c86ab` |
| `coefficients/side24_v1/test_coefficient.py` | `fa9beaab7d6fcb4f0a0c5a91c6d80b455c98a912` | 4762 | `81689b5394e2e949058929570ec072ccb1d4fe93cd0d36a4b258431547d02dd3` |
| `coefficients/side24_v1/ENCLOSURE.json` | `57af39a05e14ed0ba8ebc00a9b4aca4dffb067c7` | 1090 | `72b6cd92d31394cdaf5da8919a5d548e902228af1f095cc184158a71d8287811` |

Prior review record: xAI / Grok 4.7 (Cursor cloud agent), interfaces C1–C6 all VERIFIED,
[main#65 comment 5841269490](https://github.com/d6g8k5htny-coder/main/issues/65#issuecomment-5841269490);
work package closed by [comment 5841779222](https://github.com/d6g8k5htny-coder/main/issues/65#issuecomment-5841779222).
Parent: UNIFORM-MATRIX-CAP-LIFETIME-20260924-v1, blob `dfed3b8d318a3ab1950957f393307733a4bef3f2`,
SHA256 `9350ad6e…c84bc7`, whose equation (15.2) defines the coefficient. The parent is imported, not re-proved here.

## Reviewer provenance

| Field | Value |
|---|---|
| Provider / tool | Anthropic Claude, Claude Code session `session_01NMeKEismAyeqgdB4sy2NJU` (model id `claude-fable-5-1` as configured) |
| Relation to author | Different provider from the author (OpenAI / ChatGPT) and from the first nonauthor reviewer (xAI / Grok). Same GitHub account as every lane: no organizational independence is claimed. |
| Exposure | This session consumed the published `side24_v1` endpoints as inputs in earlier work (the D1-C/D/E review, PR #143, and the periodization first-variation note, PR #144). Every derivation below was redone from the note's text and the parent's (15.2), before the C1–C6 comment was read; that comment was read afterwards only to align interface labels. No source file was edited. |
| Tooling | CPython 3.11, standard library only. Independent numerics use `decimal` (precision 90) with a Stirling shift of 120 and B₂…B₄₀ (the package uses shift 32 and B₂…B₂₀), the first omitted term < 10⁻⁷⁰, and an own Machin π; a second run with shift 300 agrees to 75 decimals. |

## Verdicts

The note's own list ("Nonauthor review should independently check …") is used as the interface list; the
C-labels are the first review's.

| Item | Note locus | First review | Verdict |
|---|---|---|---|
| 1. Shared trace variance 5/3 (and the whole reference jet covariance) | §1 | C1/C2 | **VERIFIED** |
| 2. Rayleigh cone integration: D_1 = 4/3, D_2 = 29/6 − √6 with the negative-definite cone retained | §1 | C1/C2 | **VERIFIED** |
| 3. Ordered-pair / gamma normalization inherited from the parent: (15.2) scalar identity and formula (1) | §1, parent (15.2) | C3 | **VERIFIED** as algebra from the parent's displayed factors; the factors themselves stay parent-open (below) |
| 4. All-direction derivative bound and the image sum: E = 1458(76·24⁶+15)·10⁻¹²⁵ | §2 | C4 | **VERIFIED** |
| 5. Covariance and Schur-complement comparison; density comparison; (3) and (4) | §§3–4 | C5 | **VERIFIED** |
| 6. Rational interval implementation, special-function remainders, outward decimals | §5, `coefficient.py` | C6 | **VERIFIED** |
| 7. Reproduction | `coefficient.py`, tests | — | stdout byte-identical to `ENCLOSURE.json` in normal and `-O` modes; 30 tests pass in both modes |
| 8. Independent numerics | formula (1) | — | 60-decimal values (standard-library `decimal`, Stirling shift 120, remainder < 10⁻⁷⁰) lie inside the package's internal enclosures (widths ≈ 10⁻³²) and inside the published 20-digit endpoints; recomputed inside the CI checker (R7) |

Overall: **ACCEPT at the arithmetic-enclosure scope** of the note, i.e. the two displayed intervals are
proved bounds on the expression (15.2) evaluated for the exact variance-one SIDE24 covariance in d = 2, 3.
No defect was found. Nothing here reads the coefficient as a finite-bar lifetime constant; that reading
remains conditional on the parent's separately reviewed chain, exactly as the note states.

The exact checker `coefficient_review_check.py` (R1–R8, transcript `RESULTS.json`) verifies every
finite identity used below; three mutants (M1 wrong pairing-sum 75, M2 wrong covariance floor 1/2,
M3 untruncated 29/6 used as D_2) exit 1; an unknown mutant label exits 2.

## Item 1 — reference jet covariance (§1)

For K_∞(z) = e^{−|z|²/2}, Cov(∂^α f(0), ∂^β f(0)) = (−1)^{|β|} ∂^{α+β}K_∞(0), and the one-dimensional
factors give ∂^{2k}e^{−x²/2}|₀ = (−1)^k(2k−1)!!. Hence Cov(G) = I_d; Cov(H_ij,H_kl) = δ_ijδ_kl + δ_ikδ_jl + δ_ilδ_jk;
Var(t) = 15, Cov(t,G) = (−3,0,…,0) for t = ∂₁³f; odd and even orders are uncorrelated. V = He₁ has
covariance diag(3,1,…,1), so p_G(0)p_V(0) = (2π)^{−d}/√3, and τ² = Var(t | G = 0) = 15 − 9 = 6, using only
Var(t), Cov(t,G) and Cov(G); by parity t is also uncorrelated with the whole Hessian, so conditioning on
V = 0 as well changes nothing. The transverse block A = (H_ij)_{i,j≥2} correlates with V only through H₁₁
(Cov(A_ij,H₁₁) = δ_ij, Cov(A_ij,H_k1) = 0 for k ≥ 2), so
Cov(A_ij,A_kl | V=0) = (2/3)δ_ijδ_kl + δ_ikδ_jl + δ_ilδ_jk, i.e. A = Q + √(2/3)·Z·I_m as stated.
For m = 2 with A = [[s+x, y],[y, s−x]]: Var(A₁₁) = Var(A₂₂) = 8/3, Cov(A₁₁,A₂₂) = 2/3, Var(A₁₂) = 1, giving
Var(s) = (8/3+8/3+4/3)/4 = **5/3**, Var(x) = (8/3+8/3−4/3)/4 = 1, Cov(s,x) = 0, Var(y) = 1, all independent. ✔

## Item 2 — cone moments (§1)

m = 1: Var(A) = 8/3 and D_1 = E[A²1{A<0}] = (1/2)(8/3) = **4/3**. ✔

m = 2: eigenvalues s ± R, R = √(x²+y²); negative definite ⇔ s < −R; det A = s² − R²; R² ~ Exp(mean 2),
density e^{−z/2}/2. The kernel identity ∫₀^a (a−z)²e^{−z/2}dz/2 = a² − 4a + 8 − 8e^{−a/2} holds: both sides
vanish with their first derivatives at a = 0 and have second derivative 2 − 2e^{−a/2} (checker R6, formal
differentiation). By the symmetry of s, D_2 = (1/2)E[s⁴ − 4s² + 8 − 8e^{−s²/2}] with E s² = 5/3, E s⁴ = 25/3,
E e^{−s²/2} = (1 + 5/3)^{−1/2} = √(3/8); so D_2 = 29/6 − 4√(3/8) = **29/6 − √6** ≈ 2.383843590550155. ✔
The untruncated half-moment is exactly 29/6 (mutant M3), confirming that the cone truncation is what
produces the −√6 term.

## Item 3 — (15.2) scalar identity and formula (1)

With φ_τ the centered normal density of variance τ², ∫₀^∞ k^{4/3}φ_τ(12k)dk = 12^{−7/3}·(1/2)·2^{2/3}τ^{4/3}Γ(7/6)/√π,
and 144·12^{−7/3}·2^{−1/3} = 24^{−1/3} because 144³·24 = 12⁷·2 (checker R7). This is the parent's prefactor
Γ(7/6)/(24^{1/3}√π). Substituting p_G p_V = (2π)^{−d}/√3, τ^{4/3} = 6^{2/3}, |S¹| = 2π, |S²| = 4π and
6^{2/3}/24^{1/3} = (3/2)^{1/3} gives (1): c_{d,ref} = Γ(7/6)(3/2)^{1/3}D_{d−1}/(2√3·π^{d−1}√π). ✔
The factors 4(6κ)² = 144, |det T_r| = 12r^{−(d+3)}, the ordered maximum/saddle roles and the full pin
Jacobian are the parent's and are **not** re-proved here.

## Item 4 — all-direction derivative bound and image sum (§2)

For unit directions u₁…u_q (repeated or mixed), D_{u₁}…D_{u_q}φ = φ·Σ_{pairings}∏(−u_a·u_b)∏(−u_c·x), so
|D^qφ(x)| ≤ φ(x)Σ_j q!/(2^j j!(q−2j)!)|x|^{q−2j}. The pairing sums for q = 0..6 are 1,1,2,4,10,26,**76**
(76 = 1+15+45+15, checker R1); at |x| ≥ 1 every order ≤ 6 is bounded by 76|x|⁶φ(x); at x = 0 the values are
at most (q−1)!! ≤ 15 in absolute value (equality for a repeated direction). The needed covariances are unit-direction contractions of total order ≤ 6 (t with t is 6), so
the bound covers every entry in every orthonormal frame.

Lattice: with S = Σ_n e^{−288|n|²} ≥ 1, D^qK₂₄(0) − D^qK_∞(0) = [Σ_{n≠0}D^qφ(24n) − (S−1)D^qφ(0)]/S, so
|·| ≤ (76·24⁶ + 15)Σ_{n≠0}|n|⁶e^{−288|n|²}. Points with max-coordinate j number (2j+1)³−(2j−1)³ = 24j²+2 ≤ 27j³
(d = 3; d = 2 gives 8j), |n|⁶ ≤ 27j⁶, |n|² ≥ j², so the sum is ≤ 729Σ_j j⁹e^{−288j²}; successive terms have
ratio ≤ 2⁹e^{−864} < 1/2, so ≤ 1458e^{−288}. The positive Taylor partial sum through k = 20 proves
e^{288/125} > 10, hence e^{−288} < 10^{−125}. Therefore |D^qK₂₄(0) − D^qK_∞(0)| < E = 21175738586478·10^{−125}
(checker R2, R3, exact). ✔ The subtraction of (S−1)D^qφ(0) — the normalization term — is included. ✔

## Item 5 — covariance, Schur and density comparison (§§3–4)

Joint vector (G, t, svec H), dimension d+1+d(d+1)/2 ≤ 10. The √2 off-diagonal scaling makes each entry differ
from the reference by ≤ 2E, so ‖C₂₄ − C_ref‖ ≤ 20E (row-sum bound). Reference spectrum: the svec-Hessian block
is 2I + J on the diagonal entries and 2I on the off-diagonal ones — eigenvalues d+2 (trace) and 2 (traceless) —
and is uncorrelated with the odd block; the odd block is [[1,−3],[−3,15]] ⊕ I_{d−1}, eigenvalues 8 ± √58 and 1;
8 − √58 ≈ 0.384 > 1/3 (shifted minors 2/3 and 7/9, checker R4). Hence C_ref ≥ I/3 and, with 60E < ε = 10^{−108},
(1−ε)C_ref ≤ C₂₄ ≤ (1+ε)C_ref in every orthonormal frame. ✔

Transfer: a PSD sandwich is preserved by every fixed linear image (marginals), and the Schur complement's
quadratic form is v ↦ inf_w (v,w)ᵀC(v,w), an infimum of the full form, so it inherits both inequalities;
this covers τ² = Var(t | pins) and Cov(A | V = 0) with no rotational invariance of C₂₄ assumed. ✔

Density comparison: det C ∈ [(1−ε)^n,(1+ε)^n]det C₀ and C⁻¹ ∈ [(1+ε)⁻¹,(1−ε)⁻¹]C₀⁻¹ give
[(1−ε)/(1+ε)]^{n/2}φ_{(1−ε)C₀} ≤ φ_C ≤ [(1+ε)/(1−ε)]^{n/2}φ_{(1+ε)C₀} pointwise; h(A) = det(A)²1{A<0} is
homogeneous of degree 2m on a scale-invariant cone, so E_{aC₀}h = a^m E_{C₀}h. Combining with p_G(0), p_V(0)
(each ∈ [(1+ε)^{−d/2},(1−ε)^{−d/2}]·ref) and τ^{4/3} gives the integrand ratio in
[(1−ε)^a/(1+ε)^b, (1+ε)^a/(1−ε)^b], a = m+2/3+n/2, b = d+n/2 (d = 2: 13/6, 5/2; d = 3: 25/6, 9/2; both ≤ 5).
Exactly, (1+ε)⁵/(1−ε)⁵ ≤ 1 + 32ε at ε = 10^{−108} (checker R5), so |c_{d,24}/c_{d,ref} − 1| < 32ε < 10^{−106}.
The reference integrand is positive and constant in u, so the sphere integral keeps the bound. ✔

## Item 6 — implementation (`coefficient.py`, by function)

- `I`: every constructor call floors `lo` and ceils `hi` to the 10^{−80} grid (outward, sign-correct);
  `__mul__` takes min/max of the four endpoint products; `inv` refuses intervals containing 0 and maps
  [lo,hi] ↦ [1/hi,1/lo]; floats and bools are rejected. ✔
- `root`: `integer_root` returns the exact floor root — `math.isqrt` for n = 2 (every square root in the
  enclosure: √3, √6, √π) and a bisection with the valid initial bracket (2^{⌈bits/n⌉})ⁿ > a for n ≥ 3
  (only the cube root (3/2)^{1/3}). The lower
  endpoint ⌊N^{1/n}⌋/SCALE with N = ⌊v·SCALEⁿ⌋ is ≤ v^{1/n}; for the upper endpoint, if r = ⌊N^{1/n}⌋ has
  rⁿ < v·SCALEⁿ then (r+1)ⁿ ≥ N+1 > v·SCALEⁿ, so (r+1)/SCALE > v^{1/n}. ✔
- `atan_small`: alternating series with decreasing terms on [0,1]; the value lies between consecutive partial
  sums (100 terms; the next term is the bracket). Machin: π = 16 atan(1/5) − 4 atan(1/239). ✔
- `log_unit`: 2·atanh((x−1)/(x+1)) on [1,2], y ≤ 1/3, 120 positive terms, tail ≤ 2y²⁴¹/(241(1−y²)). ✔
  `log_point` reduces by powers of two (negative k handled by interval scaling). ✔
- `exp_point`: reduction to [0,1/4] by halving with repeated squaring, 70 positive Taylor terms,
  tail ≤ (x⁷¹/71!)/(1−x/72); negative arguments via the reciprocal interval. ✔
- `gamma_seven_sixths`: log Γ(199/6) by DLMF 5.11.1 with B₂…B₂₀, remainder in (0, B₂₂-term) by DLMF 5.11(ii)
  (real positive argument; B₂₂ = 854513/138 > 0, checker R8 recomputes B₂…B₂₂ by Akiyama–Tanigawa);
  32 recurrence logarithms removed (DLMF 5.5(i)); exponentiated. Resulting width 1.4·10^{−31}. ✔
- `reference_coefficient`: formula (1) verbatim; `cone_moment(3)` = 29/6 − √6 by interval subtraction. ✔
- `side24_coefficient`: the (1 ± 10^{−106}) allowance is applied to the exact rational endpoints before
  the final rounding; `decimals` floors the lower and ceils the upper endpoint at 20 digits. ✔
- Margins: 60E ≈ 1.3·10^{−110} against ε = 10^{−108}; internal enclosure widths 1.1·10^{−32} (d = 2) and
  6.5·10^{−33} (d = 3) against the 10^{−20} published grid. Nothing is marginal.

## Items 7–8 — reproduction and independent numerics

```sh
git -C Math- rev-parse origin/main     # 3216e2e7153f9f07acedb70b97d9ab5a0d82ed47
sha256sum coefficients/side24_v1/*     # digests in the table above
python3 -B -S coefficients/side24_v1/coefficient.py    | cmp - coefficients/side24_v1/ENCLOSURE.json   # identical
python3 -B -O -S coefficients/side24_v1/coefficient.py | cmp - coefficients/side24_v1/ENCLOSURE.json   # identical
python3 -B -S -m unittest discover -s coefficients/side24_v1 -p 'test_*.py'      # Ran 30 tests, OK
python3 -B -O -S -m unittest discover -s coefficients/side24_v1 -p 'test_*.py'   # Ran 30 tests, OK
```

Independent evaluation of (1) (checker R7; stdlib `decimal` at precision 90, Stirling shift 120 with
B₂…B₄₀, first omitted term < 10⁻⁷⁰, own Machin π; digits truncated, not rounded, at 60 decimals):

    Γ(7/6) = 0.927719333630039200708349482534621018566466519145475576936124…
    c_2    = 0.073406919306034271030135962957774050017664244684332671851381…
    c_3    = 0.041775931840598343342936665428575556466681519661044737884976…

Both lie inside the package's internal enclosures ([…428569117…, …428575624…] for d = 3;
[…957762736…, …957774170…] for d = 2) and inside the published 20-digit endpoints; R7 asserts the
latter containment and that c_3 agrees to 10⁻⁴⁵ with this session's earlier clean-context 45-digit
re-derivation 0.0417759318405983433429366654285755564666815197. (A first draft of this table used a
shift-60 Stirling sum truncated after B₃₀ and printed digits past its own 6·10⁻⁴⁹ remainder; the
clean-context referee caught it, and the values above replace it.) ✔

## Notes (non-blocking)

- N1. §2's "at most 27j³ possibilities" is loose for d = 2 (8j) and for d = 3 (24j²+2); the final constant
  1458 could be reduced by orders of magnitude, but E ≈ 2.1·10⁻¹¹² already leaves 60E ≈ 1.3·10⁻¹¹⁰ a factor ≈ 79 below the budget ε = 10⁻¹⁰⁸.
- N2. §4's intermediate "1 − 13ε … 1 + 28ε" is not the sharpest statement (the true ratio is within
  (a+b)ε, i.e. (26/3)ε for d = 3 and (14/3)ε for d = 2); only the sufficient "1 ± 32ε" is used, and it is verified exactly.
- N3. The odd-block floor 8 − √58 ≈ 0.384 is the actual λ_min(C_ref) for both d = 2 and d = 3; the note's
  1/3 is a clean rational under-estimate, verified by the shifted minors.
- N4. `exp_lower` proves e^{288/125} > 10 by a positive partial sum through k = 20; the checker also
  confirms the 125th-power step e^{−288} < 10^{−125} in exact arithmetic.
- N5. τ² = 6 needs only Var(t) = 15, Cov(t,G) = (−3,0,…,0) and Cov(G) = I. That t is independent of V
  (indeed of the whole Hessian) is a parity fact — Cov(t,H_k1) is a fifth-order derivative of K at 0 —
  stated in the parent's §15, not in the note; the note's covariance list is consistent with it.
- N6. The interval class re-rounds outward at every operation; the resulting widths (≈ 10^{−32}) show that
  the 10^{−80} grid loses nothing at the published precision.

## Parent-open imports (not re-proved here; identical to the first review's list)

- Contact Jacobian |det T_r| = 12r^{−(d+3)} and the longitudinal ±6κ eigenvalues behind 4(6κ)² = 144.
- Ordered max/saddle counting as a measure, the full-pin Kac–Rice intensity, the Borel/global elder identification.
- Theorem C: reading c_{d,24} as the finite-bar lifetime asymptotic.
- Any finite-radius constant, unrestricted remainder, RN/24-jet certificate or P15 cover claim.

## Revision history

- v1 (2026-09-29): initial review. Exact checker R1–R8 with mutants M1–M3; reproduction in both interpreter
  modes; independent numerics; verdict ACCEPT at the arithmetic-enclosure scope. Before landing, a
  clean-context referee pass (Anthropic Claude subagent, no shared context) returned SOUND WITH AMENDMENTS:
  the first draft's "80-digit" values were correct only to 47–49 decimals (Stirling truncation not
  accounted for), N5 misattributed the source of t ⊥ V, and four wording items (isqrt for n = 2, the
  |value| ≤ (q−1)!! statement at 0, the N1 and N2 constants). All are corrected above; R7 now recomputes
  the values inside CI; the verdict is unchanged.
