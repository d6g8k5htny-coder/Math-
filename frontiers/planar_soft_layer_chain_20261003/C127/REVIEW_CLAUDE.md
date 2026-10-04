## Cross-provider nonauthor review of C127 (quantitative mixed inner/remote window witnesses): ACCEPT (PASS_TECHNICAL_SCOPED), no amendment

**Who.** Dylan Roy — delegated AI review. Actual performer: Anthropic Claude (session `session_01NMeKEismAyeqgdB4sy2NJU`).
- Claim: [5975216884](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5975216884), released by this post.
- Independence: provider-distinct (Anthropic, against OpenAI/Codex authors and an OpenAI/Codex first reviewer). It runs through the same GitHub account, so organizational-independence credit is 0.
- This is a second review. The first is OpenAI/Codex 5975150796 (PASS_SCOPED).
- Owner review is as recorded in 5973603003. Scientific effect: NONE.

**Target.** The frozen files in [5975032676](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5975032676) (created = updated, 00:34:37Z), extracted by their markers:
- `PROOF.md`: 12,618 bytes, SHA-256 `cf0dd27e…bf44`;
- `FINITE_R_INTERPOLATION.md`: 18,630 bytes, SHA-256 `c4f169c2…8187`;
- `SOURCES.json`: 5,408 bytes, SHA-256 `1f9015f2…35f0`.

All nine source blobs match at `bbe85e2`: SC `16c56821`, C107 `59678278`, C6 `89eb8adf`, P `dfed3b8d`, E1 `213594d6`, E2 `fe9b9ce4`, REC `75da2597`, DL `9d82c707` and CAP `0633aca3`.

**Verdict.** **ACCEPT / PASS_TECHNICAL_SCOPED** for Theorem C127, (3)–(4), and the appendix lemma (F4)–(F6). The retained interfaces are exactly as §2 states them:
- P §§2–5, read with E1, E2, REC and CAP;
- DL Theorem G_d (1.7) and C6 Theorem Q, giving (5);
- C6 Lemma 5.1 with E2;
- C107's method;
- SC §3 as context.

I found no mathematical error. I did not read or run the author controls (5975038530, 5975097180) before this verdict.

### What I checked
- **§3, the planar exclusion lemma**, line by line.
  - **Transverse concavity.** `f_zz ≤ −λ/2` holds in the cylinder because `λ > 8RKr`.
  - **The strip.** The two-node remainder gives `|g(t)| ≤ (K/2)|t² − r²/4| ≤ KR²r²`, also off the pin interval. With `g′`'s interior zero, `|g′| ≤ K(R + 1/2)r`. The strip `a = 4R²Kr²/λ < Rr/2` then carries a unique transverse zero `ζ(t)`.
  - **The graph's slope.** `|f_tz| ≤ K(3R/2 + 1/2)r ≤ 2RKr` on the graph, so `|ζ′| ≤ 4RKr/λ < 1/2`.
  - **The formula for ψ‴.** `ψ‴ = f_ttt + 3f_ttzζ′ + 3f_tzzζ′² + f_zzzζ′³`. I checked it exactly on polynomial fields `a(t) + (z − ζ)²b(t) + c(z − ζ)³` with `f_z(t, ζ(t)) ≡ 0`.
  - **The error.** The perturbation is at most `K|ζ′|(3 + 3/2 + 1/4) ≤ 19RK²r/λ ≤ 28RK²r/λ < 1/2`.
  - **The forced value 12.** Every field with the four pin data differs from the pinned cubic `b − r³/2 − (3/2)r²t + 2t³` (whose third derivative is 12) by `e = (t² − r²/4)²q`. So `e‴` has a zero between the pins (generalized Rolle), and then `|f_ttt − 12| ≤ 2RKr ≤ 1/2`. Hence `ψ‴ ≥ 11`, and the strictly convex `ψ′` has only the two pinned zeros.
- **(9)–(10).**
  - On `K ≤ T`, `rT ≤ 1/(4R)` and `N_R > 0`, the contrapositive gives `A ≥ −(8RT + 56RT²)r ≥ −64RrT²`. Negative definiteness at `M` and `|f_vv(M) − A| ≤ rK/2` give `A < rT/2`.
  - Each endpoint has one column `O(rT)` and one `O_R(rT²)`, so Hadamard gives `r⁴T⁶`, and the remote determinant is at most `T²`.
- **The appendix.**
  - **The pin block.** (F11) gives `U_r(p_a) = a`. U3 equals `(6/r³)∫(s + r/2)(r/2 − s)f_ttt`, a unit-mass average, which I checked exactly on quintics.
  - **The chart.** The chord `d = S_0(ru/2)` has `|d| ≤ r/2`, `e·u ≥ 1 − θ²/6 ≥ 1/2`, and `θ ≤ π/256`.
  - **The one-separator pin dual** costs `ρ⁻⁵`.
  - **The Hessian correction** responds with `A(qℓ²) = 2q(0)(n·v)²`. I checked this exactly for any `q` and any `ℓ` with `ℓ(0) = 0`. Also `|n·v| = |e·u|` for both orientations, so the response is `≥ c_Lρ²` and the pin and Hessian duals cost `ρ⁻⁷`.
  - **The remote dual.** `q_R = ψ_Mψ_Sψ_0²` kills the pin first jets and, through the fourth-order zero at 0, `A`. The quotient value and product-rule gradient give the remote first jet exactly, at cost `ρ⁻⁸` and `ρ⁻⁹`.
  - **Covariance and density.** The covariance floor is `ρ¹⁸`, and the four-dimensional conditional density is `ρ⁻³⁶`.
- **§§5–6.**
  - **(14)–(15).** The one-point marked Kac–Rice formula for the remote count carries the mark `W_r1{N_R > 0, K ≤ T}`, and `K ≤ T` is kept until `|det H_x| ≤ CT²` is used. The `A`-slab is integrated against the joint density of `(A, f(x), ∇f(x))`. The ledger `r⁴T⁶ · T² · rT² · r³ · L² · ρ⁻³⁶ / (z_*r²) = C r⁶T¹⁰ρ⁻³⁶` is exact.
  - **(16).** `W_r ≤ Cr²K⁴` with the full floor and `P (4.1)`.
  - **(5).** The Stirling identity `N^q = Σ S(q, j)(N)_j` holds exactly for `q ≤ 12`, `N ≤ 24`.
  - **(18).** Cauchy–Schwarz at `q = 2p + 4`.
  - **The table.** At `ρ = r^{1/100}`, `T = r^{−1/100}` and `m = 600`, the powers are exactly `277/50`, `6`, `427/100`, `9/2` and `627/100`.
  - **The falsifier of §7** (`N = 2` with probability `r³`) is exact.

### Observations (not findings)
- **O1. The exponent is one admissible choice.**
  - (17)–(18) hold for every admissible `(r, ρ, T)`. With `ρ = r^α` and `T = r^{−β}`, (18) reads `r^{9/2 − 18α − 5β} + r^{3/2 + mβ/2}`. The §6 cutoff conditions (`r ≤ ρ/8`, `Rr < ρ/2`, `rT ≤ 1/(4R)`, `ρ ≤ ρ_0`) hold for small `r` whenever `0 < α < 1` and `0 < β < 1`.
  - So for each fixed `α ∈ (0, 1/36)` and `ε > 0`, taking `β` small and `m` large gives `E_{Q_r^W}[N^pN_RN_far^{r^α}] = O(r^{9/2 − 18α − ε})`. In particular the mixed term is `O(r⁴)` for every `ρ = r^α` with `0 < α < 1/36`.
  - The theorem's `α = 1/100` gives `427/100`.
- **O2. The `ρ⁻⁹` cost comes from the remote block, and it is attained there.** I built all ten periodic duals end to end in floating point at `L = 2π` (companion script).
  - They reproduce `L(φ_d) = d` to relative error `≤ 3 × 10⁻⁸`. The size reflects float cancellation amplified by `1/r³` in U3.
  - The remote duals grow like `ρ^{−9.12}`, with `ℓ¹ × ρ⁹` between `1.4 × 10⁴` and `2.3 × 10⁴` for `ρ = 0.4 → 0.05`.
  - The pin and Hessian duals grow only like `ρ^{−4.94}`, inside their `ρ⁻⁷` bound.
  - So the floor `ρ¹⁸`, and the density `ρ⁻³⁶`, are tight for this construction and are set by `q_R`'s four separators. Lowering 427/100 would need a cheaper remote dual.
- **O3. The exclusion constants have slack.** The two-node remainder gives `KR²r²/2`, not only `KR²r²`, and the `ψ‴` perturbation constant is 19, not only 28. This is harmless.

### Comparison with the first review (read after my verdict)
- The OpenAI review 5975150796 (PASS_SCOPED, no required amendment) and this one agree on every step:
  - the pin identities and Hermite cancellation;
  - the chart chord and its sinc bounds;
  - the one-separator pin cost `ρ⁻⁵`;
  - the Hessian correction `2q(0)(n·v)²`, not `2q(0)`;
  - the fourth-order remote factor and its product rule;
  - the floor `ρ¹⁸` and the four-dimensional `ρ⁻³⁶`;
  - the exclusion constants;
  - the slab `−64RrT² ≤ A < rT/2`;
  - the Borel-mark composition;
  - the ledger and the falsifier.
- Its nonblocking precision, that E2 is literally a C² statement read in C⁴ through its regression continuity, is consistent with my reading.
- Its exact rational-circle construction of all ten duals is stronger evidence for the appendix's identities than my floating-point build.
- This review adds:
  - O1 (every `α ∈ (0, 1/36)` gives `O(r⁴)`);
  - O2 (the remote cost is attained, the pin and Hessian costs are not);
  - O3;
  - the exact `ψ‴` identity on fields with a known critical graph;
  - the Rolle step through `(t² − r²/4)²q`;
  - the unit-mass U3 kernel.

### Reviewer controls
These are posted separately for replay.
- **`c127_exact.py`** (standard library): 35,715 exact rational checks in four groups (J0–J3).
  - Eight mutants each exit 1, and an unknown label exits 2.
  - The output is byte-identical under `-O` and `-B -S` (Python 3.11.15).
- **`c127_numeric.py`** (standard library, floating point): the ten periodic duals end to end and their `ℓ¹` cost.

### Exposure and boundary
- I did not draft or contribute to C127, SC or C107. I reviewed C107 cross-provider (5975206133).
- C6 and DL were written by another Anthropic Claude session (`015wNj8L…`), and REC by a third (`017Mi3hx…`). I contributed to none of them.
- I compared with the first review only after reaching this verdict.
- This review accepts Theorem C127 at its stated scope: planar, fixed `L`, compact births, all frames, physical `k = 1`, fixed `R ≥ 4` and `p ≥ 0`, and `ρ = r^{1/100}` (O1 records the admissible range). It accepts nothing about:
  - the retained sources (DL, C6, SC, C107, P and the rest);
  - both-inner collisions, growing annuli or shrinking gaps;
  - bar identification, a lifetime density, or global closure.
- It authorizes no merge or status change.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
_Generated by [Claude Code](https://claude.ai/code)_