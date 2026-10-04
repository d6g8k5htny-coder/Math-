# The third-order lifetime laws with remainder `ℓ^{3/7}`: candidate and elder densities in every `d ≥ 2`

Object: CL-THIRD-ORDER-RATE-20261001-v1.
Author: Anthropic Claude (claude.ai session `session_01NMeKEismAyeqgdB4sy2NJU`), 1 October 2026.
Disposition: AUTHOR-SIDE PROOF CANDIDATE; NONAUTHOR REVIEW REQUIRED. Scientific effect: NONE — no register, graph,
STATUS, PROOF_INDEX, prize or Boolean change; no numerical constant is certified. Same GitHub account as every lane;
zero organizational independence.

**What is new.** Math- #218 (Theorem T) and Math- #220 (Theorem E3) expand the candidate and elder lifetime densities
to third order with remainder `O(ℓ^{4/11})`. This note improves both remainders to `O(ℓ^{3/7})`. It adds three
ingredients.
- **Lemma L** (§1). The cusp weight `y ↦ (c² − y²)₊` is locally Lipschitz with constant `|y| + |y′|`, which does not
  depend on `c`. The inequality itself is the one #218 Step C3 already uses, since `(c² − y²)₊ = c² − min(y², c²)`.
  What is new is using it in #218 Step C2 and #220 Step E3, which used the global constant `2c = 12κ|det A|` instead.
  That is where the factor `(1 + κ)²` of #218 (C.1) comes from, as #218's closing remark of §3 records; the remark
  proposed a parity argument to remove it, and Lemma L makes parity unnecessary.
- **A refined margin estimate** (§3, Step E2⁺). In #220, the elder decision's edge window `𝔅_4` is charged `O(rκ²)`.
  At large `κ`, the edge `|φ| ≈ 1/3` needs `|f₄ − 3γᵀA^{−1}γ| ≍ κ`. So either `|f₄| ≥ 6κ`, or the transverse
  concavity is `λ ≤ |γ|²/(2κ)`, an event of conditional probability `O(1/κ)` by #218 Lemma D. Each alternative saves
  a factor `κ`, so the charge drops from `O(rκ²)` to `O(rκ)`.
- **Proposition W⁺** (§4). Near pairs at small gap need the typed window `|Y| ≲ κ|det A| + r`. Since `Y` is affine
  in `f₄` with slope `det A/12`, this window has conditional probability `O(κ + r/|det A|)`. Hence
  `E_Q[W_r/r²] ≤ Cr²(κ + r)²(κ + r log(2/r))P^N` for `k ≤ r`. This is better than #198 (W.1) by the factor
  `κ + r log(2/r)`, and it controls the elder density at intermediate separations to `O(ℓ^{4/9}log(1/ℓ))`.

**Dependencies (consumed, unmerged).** This note cannot be integrated before the following, and must be rebound if any
of them changes:
- Math- #207 (`frontiers/cusp_second_order_20261001/PROOF.md`, blob `f6df5a73`, head `b12ff46`): §0 cusp objects,
  (0.2)/(CU.2) (the coefficient `c₁`), §7 (through #218).
- Math- #218 (`frontiers/candidate_third_order_20261001/PROOF.md`, blob `70ca57ef`, head `0cf048d`): Lemma D (1.1),
  (1.2), Lemma F (F.1)–(F.2), Lemma C and its proof (Steps C1–C3, (C.2)), Lemma O (O.1), (0.1) (`c₂`), and §4 (the
  decomposition `F + K + J₂ + … + J₅` and the bounds on `F`, `J₂`–`J₅`).
- Math- #220 (`frontiers/elder_third_order_20261001/PROOF.md`, blob `c8767dde`, head `70dcf31`): §0 (the near/far
  identity, `𝒜^{eld}`, `c₁`), Lemma Q, §2 (notation, facts (F1)–(F7), (2.1)–(2.2), Lemma G, Lemma CE and its proof,
  Steps E1–E6), Lemma O′ (O′.1), Lemma H (through Lemma S′), Lemma S′ (S′.1), and §4 (the decomposition
  `F^{eld} + K^{eld} + I^{eld} − J₄` and the bound on `F^{eld}`).

*Rebound on 1 October 2026, 15:40 UTC.* #220's PROOF changed from blob `736a35de` (head `e481d23`) to `c8767dde`
(head `70dcf31`) by a status-only update with no mathematical change: #187 is listed as merged, Lemma S′ states its
range `r ≤ r_0^* ≤ 1` and sign `−H̃ > 0`, and X8 has a negative witness. Every part of #220 consumed here is
unchanged. #207's head moved to `b12ff46` by a guarded main-only merge; its blob is unchanged.

**Merged inputs.** [R] with (R2)–(R5); [P] with [E1], [E2] and [REC] (§2 finite-jet rank, §15 parity); [Z]; [C7-K]
(K2); Math- #191 (`441152df`: Lemma E Steps 1–3, for (F1) at `k = 0`; §2, `r_0^*` and the `k = 0` identity); Math- #198
(`abfb98ae`: (3.1), the sign window and (3.2) of §3, Lemma W with its `k = 0` clause, (W.1), the `k = 0` identity in
the proof of (W.4), Lemma F′); Math- #187 (`07260114`, merged on 1 October 2026 at `c2f1270`: Theorem F at the single
separation `ρ = r_0^*`). **Cited only:** Math- #216 and #223 (values of `c₂`; #223 merged on 1 October at `f9ebba1`),
#211 (blob `ed0d3fa8`; the equal-height mass and a heuristic quoted in Remark 3), #188.

## 0. Statement

Setting and notation are those of #218 §0 and #220 §0:
- fixed `d ≥ 2`, `m = d − 1`, `L > 0`, the [P] field on `X = R^d/(LZ^d)`;
- near pins `M = −ru/2`, `S = ru/2` at heights `b`, `b − kr³`, the pinned law `Q = Q_{r,b,k}`, the pin density
  `π_r(v_r)`, `P = 1 + |b| + k`, `κ = k/r`;
- the scaled endpoint Hessians `K_M`, `K_S`, `W_r/r² = F_d(K_M)F_{d−1}(K_S)`, and the elder mark `e`;
- the kernels `A_r = 12π_r(v_r)E_Q[W_r/r²]`, `A_r^{eld} = 12π_r(v_r)E_Q[(W_r/r²)e]` and `A_0 = 12π_0(v_0)z_0`;
- the free jets `J′ ⊃ J″ ⊃ J‴` of `f = F_r` at `0` (#220 §2), with `f₄`, `γ`, `A`, `Δ = det A`, `λ = λ_min(−A)`,
  `B = ∂_uD_Θ²f(0)`, `Y_r = (f₄/12)Δ + 3k tr(adj(A)B) − γᵀadj(A)γ/4`, `Y′ = Y_r − 3k tr(adj(A)B)`, `φ_r = Y′/(6κΔ)`,
  and `𝒩_r = 1 + k + ‖F_r‖_{C⁹}`;
- the cusp kernels `𝒜^{cand}`, `𝒜^{eld}`, `𝒜^{con}`, the weight `w_κ(A, Y) := (36κ²(det A)² − Y²)₊1{A < 0}`, and the
  coefficients `c = c_{d,L}`, `B_{d,L}`, `I^{cand}` (#218 §0), `c₁` (#220 (0.2)) and `c₂` (#218 (0.1));
- `r₂ := min(r_0^*, 1/2, r_Q)` (#220 Lemma CE).

**Theorem T⁺ (the candidate density, remainder `ℓ^{3/7}`).** For every `d ≥ 2` and `L > 0`, as `ℓ ↓ 0`,

    ν_cand(ℓ) = c ℓ^{−1/3} + B_{d,L} + I^{cand} ℓ^{1/4} + c₂ ℓ^{1/3} + O(ℓ^{3/7}).                              (T⁺.1)

**Theorem E3⁺ (the elder density, remainder `ℓ^{3/7}`).** For every `d ≥ 2` and `L > 0`, as `ℓ ↓ 0`,

    ν_eld(ℓ) = c ℓ^{−1/3} + c₁ ℓ^{1/4} + c₂ ℓ^{1/3} + ν_eld^{far,r_0^*}(ℓ) + O(ℓ^{3/7}),                          (E3⁺.0)

and, by Math- #187's Theorem F at `ρ = r_0^*` (`ν_eld^{far,r_0^*}(ℓ) ≤ Cℓ^{2/3}`),

    ν_eld(ℓ) = c ℓ^{−1/3} + c₁ ℓ^{1/4} + c₂ ℓ^{1/3} + O(ℓ^{3/7}).                                              (E3⁺.1)

The elder density from the intermediate separations `[ℓ^{2/9}, r_0^*]` is `O(ℓ^{4/9}log(1/ℓ))`. (E3⁺.0) does not use
#187: it isolates the far part, so that for `0 < θ ≤ 3/7`, `ν_eld − cℓ^{−1/3} − c₁ℓ^{1/4} − c₂ℓ^{1/3} = O(ℓ^θ)` if and
only if `ν_eld^{far,r_0^*} = O(ℓ^θ)`. With #187 both sides hold at `θ = 3/7`.

**Corollary R⁺ (the rejected density).** `ρ_rej = ν_cand − ν_eld` satisfies

    ρ_rej(ℓ) = B_{d,L} + (I^{cand} − c₁) ℓ^{1/4} − ν_eld^{far,r_0^*}(ℓ) + O(ℓ^{3/7}) = B_{d,L} + (I^{cand} − c₁) ℓ^{1/4} + O(ℓ^{3/7}).   (R⁺.1)

**Proposition W⁺ (the typed window).** For `0 < r ≤ r_0^*`, `b ∈ R`, `u ∈ S^{d−1}` and `0 ≤ k ≤ r` (so `κ ≤ 1`),

    E_Q[W_r/r²] ≤ C r² (κ + r)² (κ + r log(2/r)) P^N,                                                            (W⁺.1)
    r^{−2}A_r(b, k, u) ≤ C (κ + r)² (κ + r log(2/r)) (1 + |b|)^N e^{−cb²}.                                       (W⁺.2)

At `k = 0` this gives `r^{d−1}Ψ_0(b, ru) ≤ Cr³log(2/r)(1 + |b|)^Ne^{−cb²}` for the equal-height kernel `Ψ_0` of [Z]
(Z2), and

    ∫_{0 < dist(0, y) < ρ} ∫_R Ψ_0(b, y) db dy ≤ C ρ⁴ log(2/ρ),        0 < ρ ≤ r_0^*,                            (W⁺.3)

which sharpens #198 (W.4) (`Cρ³`).

**How it works.** The decompositions are those of #218 §4 and #220 §4, with new split points:

    ρ_f := ℓ^{2/7},    ρ_c := ℓ^{2/9},    a := ℓ^{1/9}        (#218 and #220: ρ_f = ℓ^{3/11}, a = ℓ^{2/15}).

- *Cusp region `[ρ_f, ρ_c]`.* Lemma C⁺ (§2) and Lemma CE⁺ (§3) give the cusp kernels with errors
  `Cr(1 + κ)` and `C(r(1 + κ) + κ²r^{3/2} + κ³r²)`. #218 and #220 have `Cr(1 + κ)²`; its `rκ²` integrates to
  `ℓ²ρ_f^{−6}`, which is what forced `ρ_f = ℓ^{3/11}`.
- *Fold region `[0, ρ_f]`.* Unchanged: Lemma F's boundary layer and the rejected fold mass contribute `O(ρ_f⁵/ℓ)`,
  and the finite part `O(ℓρ_f^{−2})`.
- *Intermediate separations `[ρ_c, r_0^*]`.* Proposition W⁺ on `[ρ_c, a]`, Lemma S′ on `[a, r_0^*]`.
- *The ledger.* At `ρ_f = ℓ^{2/7}` the four error terms `ρ_f⁵/ℓ`, `ℓρ_f^{−2}`, `ℓ²ρ_f^{−11/2}` and `ℓ³ρ_f^{−9}` are
  exactly `ℓ^{3/7}`; every other term is `O(ℓ^{4/9}log(1/ℓ))` (§5; control R1).

**What is not claimed.**
- No sharpness of `3/7`. The formal next term is of order `ℓ^{1/2}` (#218 §0); Remark 1 explains why this method stops
  at `3/7`.
- No certified numerical value of `c`, `c₁`, `c₂`, `I^{cand}` or `B_{d,L}`.
- No uniformity in `d` or `L`, no finite-radius band, no statement about the adjacent-pair density.
- (E3⁺.1) and the second form of (R⁺.1) use #187 (merged) at the single separation `r_0^*`; (T⁺.1), (E3⁺.0), the first
  form of (R⁺.1) and Proposition W⁺ do not.
- Nothing beyond the existential scope of [R], [Z], [C7-K], #187, #191, #198, #207, #218 and #220.

## 1. A `κ`-free local Lipschitz bound

**Lemma L.** For `c ≥ 0` and `y, y′ ∈ R`,

    |(c² − y²)₊ − (c² − y′²)₊| ≤ |y − y′| (|y| + |y′|).                                                           (L.1)

Consequently, for every symmetric `A` and `κ > 0`, `|w_κ(A, Y) − w_κ(A, Y′)| ≤ |Y − Y′|(|Y| + |Y′|)`.

*Proof.* By symmetry assume `|y| ≤ |y′|`.
- If `|y′| ≤ c`, the left side is `|y² − y′²| = |y − y′||y + y′| ≤ |y − y′|(|y| + |y′|)`.
- If `|y| ≤ c < |y′|`, the left side is `c² − y² ≤ y′² − y² = (|y′| − |y|)(|y′| + |y|) ≤ |y′ − y|(|y| + |y′|)`.
- If `c < |y|`, both terms vanish.

For `w_κ` take `c = 6κ|det A|` on `{A < 0}`; off `{A < 0}` both weights vanish, so the left side is `0`. ∎

(L.1) is sharp: equality holds whenever `|y|, |y′| ≤ c` and `yy′ ≥ 0`. Since `(c² − y²)₊ = c² − min(y², c²)`, (L.1) is
the inequality `|min(y², c²) − min(y′², c²)| ≤ (|y| + |y′|)|y − y′|` that #218 Step C3 uses. The global Lipschitz
constant `2c` also holds, but `|y| + |y′|` has moments independent of `κ`, whereas `2c = 12κ|Δ|` grows with `κ`
(control R2).

## 2. The candidate cusp kernel with rate `r(1 + κ)`

**Lemma C⁺.** There are `C, c, N` such that for `0 < r ≤ min(r_0^*, 1/2)`, `b ∈ R`, `u ∈ S^{d−1}` and `κ > 0` with
`k := κr ≤ 1`,

    |r^{−2}(A_r − A_0)(b, κr, u) − (𝒜^{cand} − 𝒜^{con})(b, κ, u)| ≤ C r (1 + κ) (1 + |b|)^N e^{−cb²}.                 (C⁺.1)

*Proof.* Follow #218's proof of Lemma C on its coupling space, with `T`, `A_0 = D_y²F_0(0)`, `Δ := det A_0`,
`Y = (f₄/12)Δ + 3k tr(adj(A_0)B) − q` and `Y_0 = (f₄^{(0)}/12)Δ − (γ^{(0)})ᵀadj(A_0)γ^{(0)}/4` as there.
- *Step C1* is unchanged: (C.2) there gives `|r^{−2}F_d(K_M)F_{d−1}(K_S) − w_κ(A_0, Y)| ≤ Cr(1 + κ)T^N`. This is
  already linear in `κ`. Case 1's bounds are `24ηκ|Δ| + η²` and `2η(12κ|Δ| + 3η)` with `η = Cr(1 + k)T^{N₁}`, and
  Case 3's only `κ²` is `w_κ ≤ 36κ²r²T^{2m} = 36k²T^{2m}`, with `|m_Mm_S| ≤ C(k + η)²T^{2m}`. The `k²` parts are
  absorbed by `k² ≤ k = κr`, and the `η²` parts by `r² ≤ r`.
- *Step C2⁺.* #218 Step C2 gives `|Y − Y_0| ≤ 3k|tr(adj(A_0)B)| + Cr²T^N`. Also `|Y| + |Y_0| ≤ CT^N`, since
  `|f₄|, |γ|, ‖B‖, ‖A_0‖ ≤ T` and `k ≤ 1`. By Lemma L,
  `|w_κ(A_0, Y) − w_κ(A_0, Y_0)| ≤ |Y − Y_0|(|Y| + |Y_0|) ≤ C(k + r²)T^{N′}`. With Step C1 and `E[T^{N′}] ≤ CP^{N′}`,

      |E_Q[r^{−2}F_d(K_M)F_{d−1}(K_S)] − E_0[w_κ(A, Y) | v_0(b, k)]| ≤ C r(1 + κ) P^N,

  because `k + r² = r(κ + r) ≤ r(1 + κ)`. (On the right, as in #218, `A` and `Y` are the cusp objects of #218 §0 under
  the contact law at `v_0(b, k)`; `(A_0, Y_0)` has that law.) #218 had `Cκ(κr + r²)T^N` for this step, from the
  constant `12κ|Δ|`.
- *Step C3* is unchanged except for one estimate. The density step costs `|π_r(v_r) − π_0(v_0(b, k))|·E_0[w_κ] ≤
  Cr²P²·(1 + κ)²P^N`, and `r²(1 + κ)² = (r + k)² ≤ 2(r + k) = 2r(1 + κ)` because `r + k ≤ 2` (control R6).
- The identity `r^{−2}A_0(b, κr, u) = 12π_0(v_0(b, k))·36κ²E_0[Δ²1{A < 0} | v_0(b, k)]` and the parity step that moves the
  target from `v_0(b, k)` to `v_0(b, 0)` are #218's. The latter costs `O(k(1 + |b|)^Ne^{−cb²})`, "with no growth in
  `κ`", because it uses `|min(Y², c) − min(Ȳ², c)| ≤ (|Y| + |Ȳ|)|Y − Ȳ|`, which is (L.1).

Collecting, with `P^Ne^{−c(b² + k²)} ≤ C(1 + |b|)^Ne^{−cb²}`, gives (C⁺.1). ∎

So the parity argument proposed at the end of #218 §3 is not needed for the exponent. Parity would sharpen the
contribution of the `3k tr(adj(A_0)B)` term from `O(k)` to `O((1 + κ)k²)`, and probably to `O(k²)` (Remark 2; not
proved), but `O(k) = O(κr)` is already within (C⁺.1).

## 3. The elder cusp kernel

**Lemma CE⁺.** There are `C, c, N` such that for `0 < r ≤ r₂`, `b ∈ R`, `u ∈ S^{d−1}` and `κ > 0` with `κr ≤ 1`,

    |r^{−2}(A_r^{eld} − A_0)(b, κr, u) − (𝒜^{eld} − 𝒜^{con})(b, κ, u)| ≤ C (r(1 + κ) + κ²r^{3/2} + κ³r²) (1 + |b|)^N e^{−cb²}.   (CE⁺.1)

*Proof.* Follow #220's proof of Lemma CE. Step E1 is unchanged, and so is (2.3) there:

    |r^{−2}F_d(K_M)F_{d−1}(K_S)e − G(J′)| ≤ 2Cr(1 + κ)𝒩_r^N + w_κ(A, Y_r)1_𝔅,    G(J′) := w_κ(A, Y_r)1{|φ_r| < 1/3}.

Two steps change: Step E2 in its `𝔅_4` part, and Step E3.

*Step E2⁺ (wrong decisions).* #220 shows `𝔅 ⊂ 𝔅_λ ∪ 𝔅_κ ∪ 𝔅_4 ∪ 𝔅_5`, and that (Q1)–(Q3) of Lemma Q hold off
`𝔅_λ ∪ 𝔅_κ`. So `𝔅 ⊂ 𝔅_λ ∪ 𝔅_κ ∪ 𝔅_4′ ∪ 𝔅_5` with `𝔅_4′ := 𝔅_4 ∖ (𝔅_λ ∪ 𝔅_κ)`. Keep #220's bounds for the
other three events:
- `𝔅_λ`: `Cκ²min(1, κ)(r³ + r^{3/2} + (r/κ)^{3/2})P^N ≤ C(r + κ²r^{3/2})P^N`, since `κ²r³ = k²r ≤ r` and
  `κ^{1/2}r^{3/2} = k^{1/2}r ≤ r` (control R6);
- `𝔅_κ`: `Cr³P^N`;
- `𝔅_5`: `Cκ³r²P^N`.

The new estimate is

    E_Q[w_κ(A, Y_r)1_{𝔅_4′}] ≤ C κ r P^N        for every κ > 0.                                                 (3.1)

*Proof of (3.1).*
- *Where `𝔅_4′` lives.* On `𝔅_4′`, (Q3) holds: `ε* ≤ κ/4`. So `||φ_r| − 1/3| ≤ 2ε*/(3κ) ≤ 1/6` and
  `1/6 ≤ |φ_r| ≤ 1/2`, that is, `|f₄ − 3γᵀA^{−1}γ| = 72κ|φ_r| ≥ 12κ`. The weight vanishes unless `A < 0`, and then
  `|γᵀA^{−1}γ| ≤ |γ|²/λ`. Hence

      𝔅_4′ ∩ {w_κ > 0} ⊂ {|f₄| ≥ 6κ} ∪ {λ ≤ |γ|²/(2κ)}                                                          (3.2)

  (control R3). Also, as in #220, `𝔅_4` puts `f₄` in two `J″`-measurable intervals `I₄` of total length
  `192ε*`, with `ε* = 80C₁𝒩_r r(1 + Γ)²` and `Γ = |γ|/λ`.
- *The `𝒩_r`-layers.* As in #220, on `{𝒩_r ∈ [2^j, 2^{j+1})}` replace `𝒩_r` in `ε*` by `2^{j+1}`, so that `I₄`
  becomes `J″`-measurable. Bound `1{𝒩_r ≥ 2^j}` by (F4), `P(𝒩_r ≥ 2^j | J′) ≤ C_p2^{−jp}(P + |J′|)^p`, and then
  integrate `f₄` given `J″` by (2.1). The layer value `2^{j+1}` of `𝒩_r` in `ε*` is absorbed by `2^{−jp}`, and the sum
  over `j` converges for `p` large. Below, `ε*` stands for its layer value.
- *The first piece of (3.2).* There `1 ≤ |f₄|/(6κ)`, so `w_κ ≤ 36κ²Δ² ≤ 6κΔ²|f₄|`. Integrating `f₄` over `I₄` by
  (2.1) gives at most `CκΔ²ε*(P + |J″|)^p`. Since `Δ² ≤ λ²‖A‖^{2m−2}`, `Δ²(1 + Γ)² ≤ (λ + |γ|)²‖A‖^{2m−2}`, which
  is polynomial in `J″`. So this piece is `≤ CκrP^N`.
- *The second piece of (3.2).* Integrating `f₄` over `I₄` gives at most
  `Cκ²Δ²ε*(P + |J″|)^p ≤ Cκ²r(λ + |γ|)²‖A‖^{2m−2}(P + |J″|)^p` (in the layer), and `(λ + |γ|)² ≤ 2‖A‖² + 2|γ|²`
  since `λ ≤ ‖A‖`. This factor is polynomial in `J″` and does not depend on `κ`. Now condition on `J‴`, which
  contains `γ`. Since `{λ ≤ |γ|²/(2κ)} ∩ {A < 0} ⊂ {|λ_max(A)| ≤ |γ|²/(2κ)}`, (2.2) with `ε = |γ|²/(2κ)` gives the
  factor `C(P + |J‴|)^{n′}|γ|²/(2κ)`. So this piece is `≤ Cκ²r·κ^{−1}P^N = CκrP^N`. ∎

Collecting the four events, `E_Q[w_κ(A, Y_r)1_𝔅] ≤ C(r(1 + κ) + κ²r^{3/2} + κ³r²)P^N`. #220 had `Crκ²P^N` for
`𝔅_4`, which was the second source of `(1 + κ)²` in (CE.1).

*Step E3⁺ (removing the `k`-term).* `G₀(J′) := w_κ(A, Y′)1{|φ_r| < 1/3} = w_κ^{eld}(A, Y′)`, as in #220. By Lemma L,

    |G − G₀| = |w_κ(A, Y_r) − w_κ(A, Y′)|1{|φ_r| < 1/3} ≤ 3k|tr(adj(A)B)|(|Y_r| + |Y′|) ≤ Ck(1 + |J′|)^N,

so `E_Q|G − G₀| ≤ CkP^N = CκrP^N`. #220 had `Cκ²rP^N` here, from the constant `12κ|Δ|`.

*Steps E4–E6* are unchanged. They cost `Cκ²r²P^N`, `Cr²(1 + κ)²P^N` and `Ck²(1 + |b|)^N`. Here `κ²r² = k² ≤ k = κr`
and `r²(1 + κ)² ≤ 2r(1 + κ)` (control R6). Collecting all steps gives (CE⁺.1). ∎

(CE⁺.1) implies #220's (CE.1), since `κ²r^{3/2} + κ³r² ≤ 2κ²r` when `r ≤ 1` and `κr ≤ 1` (control R6). The two
nonlinear terms come from two of Lemma Q's bad events: `κ²r^{3/2}` from `𝔅_λ`, where the transverse concavity is
below its margin `λ₂`, and `κ³r²` from `𝔅_5 = {|φ_r| > 1}`, which the shift `3k tr(adj(A)B)` between `Y_r` and `Y′`
lets a pair inside the typed window `|Y_r| < 6κ|Δ|` reach. Both attain `3/7` exactly at the split of §5 (Remark 1).

## 4. The typed window

*Proof of Proposition W⁺.* Fix `0 < r ≤ r_0^*`, `b ∈ R`, `u` and `0 ≤ k ≤ r`. Every fact used below holds on all of
`(0, r_0^*]`:
- (F1) holds pathwise for every `r ≤ r_0^*` and `k > 0` (#220 §2). It also holds at `k = 0`: #191 Steps 1–3 are the
  same pathwise expansions there, and #198 Lemma W includes the pinned family at `k = 0` ("nothing below divides by
  `k`");
- (F3) and (2.1): `Cov_Q(J′)` is uniformly invertible on `(0, r_0^*]` (#218 Step F1);
- (F4): #218 (1.2) with `J₀ = J′`;
- (F5) and (2.2), as Schur complements in `Cov_Q(J′)`.

*Step W1 (pathwise).* Put `R̄ := max(|R_M|, |R_S|) ≤ C_Rr²𝒩_r^{N₁}` (by (F1), with `k ≤ 1`; `C_R` is (F1)'s constant, not
Lemma Q's `C₁`) and `η := C_Rr𝒩_r^{N₁} ≥ R̄/r`.
- On `{W_r > 0}` the pair is typed, so `det K_M det K_S < 0`. The sign window of #198 §3, applied to (F1), gives
  `|rY_r| ≤ 6k|Δ| + R̄` and `|det K_i| ≤ 12k|Δ| + 2R̄` (control R4).
- Dividing by `r`, `|Y_r| ≤ 6κ|Δ| + η`, and `W_r/r² = |det K_M det K_S| ≤ 4r²(6κ|Δ| + η)²`. Off `{W_r > 0}`,
  `W_r = 0`. Hence, everywhere,

      W_r/r² ≤ 4r²(6κ|Δ| + η)² 1{|Y_r| ≤ 6κ|Δ| + η}.                                                            (4.1)

*Step W2 (the window in `f₄`).* `Y_r` is affine in `f₄` with slope `Δ/12`, and its intercept is `J″`-measurable. So,
for a `J″`-measurable `η′`, `{|Y_r| ≤ 6κ|Δ| + η′}` is `{f₄ ∈ I}` for a `J″`-measurable interval `I` of length
`144κ + 24η′/|Δ|` (control R4); `Δ ≠ 0` almost surely.
- On `{𝒩_r ∈ [2^j, 2^{j+1})}`, `η ≤ η_j := C_Rr2^{(j+1)N₁}`. Bound `1{𝒩_r ≥ 2^j}` by (F4), then integrate `f₄` by
  (2.1). Using also the trivial bound `1`, this gives

      E_Q[W_r/r²] ≤ C r² Σ_{j≥0} 2^{−jp} E_Q[(6κ|Δ| + η_j)² min(1, 144κ + 24η_j/|Δ|)(P + |J″|)^p].

- By `(x + y)²min(1, a + b) ≤ 2(x² + y²)(a + min(1, b))` for `x, y, a, b ≥ 0` (control R4), the integrand is at most
  `C(κ²Δ² + η_j²)(κ + min(1, η_j/|Δ|))` times `(P + |J″|)^p`.

*Step W3 (the four terms).*
- `κ³Δ²` contributes `Cκ³P^N`.
- `κ²Δ²min(1, η_j/|Δ|) ≤ κ²|Δ|η_j` contributes `Cκ²r2^{jN′}P^N`.
- `κη_j²` contributes `Cκr²2^{2jN′}P^N`.
- `η_j²min(1, η_j/|Δ|)`. Condition on `J‴`, so that `A` is Gaussian with covariance in `[cI, CI]` and mean
  `O(P + |J‴|)` (F5). #218 Lemma D's second bound gives `E[(1 + ‖A‖)^n1{|Δ| < ε} | J‴] ≤ C(P + |J‴|)^{n′}ε` for every
  `ε > 0`. Split `{|Δ| < s}`, `{2^is ≤ |Δ| < 2^{i+1}s}` for `0 ≤ i < ⌈log₂(1/s)⌉`, and `{|Δ| ≥ 1}`. This gives, for
  `0 < s ≤ 1/2`,

      E[(1 + ‖A‖)^n min(1, s/|Δ|) | J‴] ≤ C(P + |J‴|)^{n′} s (4 + 2log₂(1/s)).                                 (4.2)

  With `s = η_j ≥ C_Rr`, `log₂(1/η_j) ≤ log₂(1/(C_Rr))`, so the term contributes `Cr³log(2/r)2^{3(j+1)N₁}P^N`. (For
  `s > 1/2` bound the minimum by `1 ≤ 2s`.)

Taking `p` large, the sum over `j` converges, and

    E_Q[W_r/r²] ≤ C r²(κ³ + κ²r + κr² + r³log(2/r))P^N ≤ C r²(κ + r)²(κ + r log(2/r))P^N

(control R5). This is (W⁺.1).

*(W⁺.2)* follows with `r^{−2}A_r = 12π_r(v_r)r^{−2}E_Q[W_r/r²]`, `π_r(v_r) ≤ Ce^{−c(b² + k²)}` ([R] (R5)) and
`P^Ne^{−ck²} ≤ C(1 + |b|)^N`.

*(W⁺.3).* At `k = 0`, `r^{d−1}Ψ_0(b, ru) = r^{−2}A_r(b, 0, u)`, as in #198's proof of (W.4) (#191 §2: the pin Jacobian, the
polar factor and the determinant scale). So (W⁺.2) at `κ = 0` gives `r^{d−1}Ψ_0(b, ru) ≤ Cr³log(2/r)(1 + |b|)^Ne^{−cb²}`.
Integrating over `b`, `u` and `r < ρ`, with `∫_0^ρ r³log(2/r) dr = (ρ⁴/4)(log(2/ρ) + 1/4)`, gives (W⁺.3). ∎

(W⁺.1) improves #198 (W.1), `E_Q[W_r/r²] ≤ C(k² + r⁴(1 + k)²)P^N = Cr²(κ² + r²)(…)` for `k ≤ r`, by the factor
`κ + r log(2/r)`. That factor is the conditional probability of the typed window, which (W.1) does not use. #198 notes
after its proof of Lemma W that the window `|rY| ≤ 6k|Δ| + O(r²)` is where the typed weight lives; (4.1)–(4.2) charge
it. The factor `log(2/r)` comes from integrating `f₄` alone, and may be an artifact: in the referee's `d = 2`
exploration (Gaussian kernel, Monte Carlo under the exact two-site regression), `E_Q[W_r/r²]/r² ≈ 0.03r³` at `k = 0`
for `r` from `0.4` down to `0.0125`, with no visible logarithm. The ledger does not need it removed.

## 5. Proof of Theorems T⁺ and E3⁺ and of Corollary R⁺

*Setup.* Put `ρ_f := ℓ^{2/7}`, `ρ_c := ℓ^{2/9}`, `a := ℓ^{1/9}`, `s_f := ρ_fℓ^{−1/4} = ℓ^{1/28}` and
`s_c := ρ_cℓ^{−1/4} = ℓ^{−1/36}`. Take `ℓ` so small that `ρ_c ≤ r₂`, `ρ_c < r_0` and `a < r_0^*`. Then
`ℓ^{1/3} < ρ_f < ℓ^{1/4} < ρ_c < a`, `k = ℓ/r³ ≤ ℓ^{1/7} ≤ 1` on `[ρ_f, ∞)`, and `κ = ℓ/r⁴ ≤ ℓ^{1/9} ≤ 1` on `[ρ_c, ∞)`.

*The candidate density.* Use #218 §4's decomposition `ν_cand − cℓ^{−1/3} − B_{d,L} = F + K + J₂ + J₃ + J₄ + J₅`, with its
fixed `r_0 ∈ (0, r_0^*]`, at these `ρ_f` and `ρ_c`. Its bounds on `F` and `J₂`–`J₅` hold for every
`ℓ^{1/3} ≤ ρ_f ≤ min(ℓ^{1/4}, r_0^*, 1/2)` and `ℓ^{1/4} < ρ_c < r_0`:
- `F = c₂ℓ^{1/3} + ρ_f∫∫A₂(b, 0, u) + O(ρ_f² + ρ_f⁵/ℓ + ℓρ_f^{−2})` (Lemma F and the finite part);
- `|J₂| ≤ Cρ_c³`, `|J₃| ≤ C(ℓ²ρ_c^{−7} + ℓρ_c^{−2})`, `0 ≤ −J₄ ≤ Cℓ²ρ_c^{−7}`, `|J₅| ≤ C_{r_0}ℓ`.

For `K`, use (C⁺.1) with `κ = ℓ/r⁴` in place of (C.1). The error is
`C∫_{ρ_f}^{ρ_c}r(1 + ℓr^{−4}) dr ≤ C(ρ_c² + ℓρ_f^{−2})`. The rest of #218's treatment of `K` is unchanged: the
upper tail `O(ℓ²ρ_c^{−7})`, the lower end by Lemma O `O(ℓ^{1/4}s_f⁵) = O(ρ_f⁵/ℓ)`, and the cancellation of
`±ρ_f∫∫A₂(b, 0, u)` against `F`. So

    ν_cand − cℓ^{−1/3} − B_{d,L} − I^{cand}ℓ^{1/4} − c₂ℓ^{1/3} = O(ρ_f² + ρ_f⁵/ℓ + ℓρ_f^{−2} + ρ_c² + ℓ²ρ_c^{−7} + ρ_c³ + ℓρ_c^{−2} + ℓ).

*The elder density.* Use #220 §4's identity at `r_0 = r_0^*`,
`ν_eld − cℓ^{−1/3} = F^{eld} + K^{eld} + I^{eld} − J₄ + ν_eld^{far,r_0^*}`, at these `ρ_f` and `ρ_c`.
- `F^{eld} = c₂ℓ^{1/3} + ρ_f∫∫A₂(b, 0, u) + O(ρ_f² + ρ_f⁵/ℓ + ℓρ_f^{−2})`. This is #220's bound; it uses `ρ_f ≤ ℓ^{1/4}`
  (so `k ≥ r`) and `ρ_f ≤ r₂ ≤ r_0^{[K]}`, and the rejected fold mass is `O(ρ_f⁵/ℓ)` by [C7-K] (K2).
- `K^{eld}`: (CE⁺.1) with `κ = ℓ/r⁴` gives the error

      C∫_{ρ_f}^{ρ_c}(r + ℓr^{−3} + ℓ²r^{−13/2} + ℓ³r^{−10}) dr ≤ C(ρ_c² + ℓρ_f^{−2} + ℓ²ρ_f^{−11/2} + ℓ³ρ_f^{−9}).

  The rest is #220's: `K^{eld} = c₁ℓ^{1/4} − ρ_f∫∫A₂(b, 0, u) + O(ℓ^{1/4}s_f⁵ + ℓ^{1/4}s_c^{−7})` plus that error, by
  (0.2), Lemma O′ with #218 Lemma O (`s ≤ s_f < 1` means `κ ≥ 1`), and the upper tail.
- `0 ≤ J₄ ≤ Cℓ²ρ_c^{−7}`.
- `I^{eld} = ∫_{ρ_c}^{r_0^*}∫∫r^{−2}A_r^{eld} ≥ 0`.
  - On `[ρ_c, a]`, `e ≤ 1` and (W⁺.2) give `r^{−2}A_r^{eld} ≤ C(1 + log(2/ρ_c))(κ + r)³(1 + |b|)^Ne^{−cb²}`, using
    `(κ + r)²(κ + rL) ≤ (1 + L)(κ + r)³` for `L = log(2/r) ≥ 0` and `log(2/r) ≤ log(2/ρ_c)`. Since
    `(κ + r)³ ≤ 4(κ³ + r³)` (control R5), this integrates to at most `C log(1/ℓ)(ℓ³ρ_c^{−11} + a⁴)`.
  - On `[a, r_0^*]`, Lemma S′ applies (`k ≤ r`). As in #220 §4 it gives at most `C(ℓ^{5/3}a^{−7} + ℓ^{2/3}a^{−2})`.

  So `0 ≤ I^{eld} ≤ C(ℓ^{5/9} + ℓ^{4/9})log(1/ℓ) + C(ℓ^{8/9} + ℓ^{4/9}) = O(ℓ^{4/9}log(1/ℓ))`.

The terms `±ρ_f∫∫A₂(b, 0, u)` cancel as in #220, and `ℓ^{1/4}s_f⁵ = ρ_f⁵/ℓ`, `ℓ^{1/4}s_c^{−7} = ℓ²ρ_c^{−7}`.

*The ledger* (control R1; exponents of `ℓ`):

| Term | Source | Exponent |
|---|---|---|
| `ρ_f⁵/ℓ` | Lemma F's layer; the rejected fold mass; Lemma O/O′'s tail | **3/7** |
| `ℓρ_f^{−2}` | the finite part; the linear term `rκ` of (C⁺.1), (CE⁺.1) | **3/7** |
| `ℓ²ρ_f^{−11/2}` | `κ²r^{3/2}` of (CE⁺.1) (elder only) | **3/7** |
| `ℓ³ρ_f^{−9}` | `κ³r²` of (CE⁺.1) (elder only) | **3/7** |
| `ρ_f²` | Lemma F | 4/7 |
| `ρ_c²`, `ℓ²ρ_c^{−7}` | cusp errors; upper tail; `J₃`, `J₄` | 4/9 |
| `a⁴log`, `ℓ^{2/3}a^{−2}` | `I^{eld}` (Proposition W⁺; Lemma S′) | 4/9 |
| `ℓ³ρ_c^{−11}log`, `ℓρ_c^{−2}` | `I^{eld}`; `J₃` | 5/9 |
| `ρ_c³`, `ν_eld^{far,r_0^*}` (with #187) | `J₂`; the far part | 2/3 |
| `ℓ^{5/3}a^{−7}`, `ℓ` | `I^{eld}`; `J₅` | 8/9, 1 |

The least exponent is `3/7`. Hence (T⁺.1) and (E3⁺.0). #198 Lemma F′ gives `0 ≤ ν_eld^{far,r_0^*} ≤ Cℓ^{1/3}`, and
#187's Theorem F at `ρ = r_0^*` gives `ν_eld^{far,r_0^*} ≤ C(r_0^*)ℓ^{2/3}`, which is (E3⁺.1); #220 §4 records that #187's
far density at `ρ = r_0^*` is the integral #198 (2.1) at `r_0 = r_0^*`. The equivalence for `θ ≤ 3/7` follows from
(E3⁺.0). Subtracting (E3⁺.0) from (T⁺.1) gives (R⁺.1); its second form uses #187. ∎

The splits are optimal for these error terms (control R1): `ρ_f = ℓ^{2/7}` balances `ρ_f⁵/ℓ` against `ℓρ_f^{−2}`,
`ρ_c = ℓ^{2/9}` balances `ρ_c²` against `ℓ²ρ_c^{−7}`, and `a = ℓ^{1/9}` balances `a⁴` against `ℓ^{2/3}a^{−2}`.

## 6. Remarks

1. **Why `3/7`.** Write the cusp errors per unit `r` at the fold end `r = ρ_f`, where `κ = ℓρ_f^{−4}`. At
   `ρ_f = ℓ^{2/7}` one has `κ = ρ_f^{−1/2}`, and then the boundary layer `r⁴/ℓ = 1/κ`, the linear term `rκ = k`, and
   the nonlinear terms `κ²r^{3/2}` and `κ³r²` are all equal to `ρ_f^{1/2}`. Times the length `ρ_f` of the interval,
   each gives `ℓ^{3/7}`.
   - The exponent is the balance of one family that increases with `ρ_f`, namely `ρ_f⁵/ℓ` (the `r³/k` layer of
     Lemma F, the rejected fold mass of [C7-K] (K2), and the `κ^{−1}` tail of Lemma O/O′), against three that
     decrease: `ℓρ_f^{−2}` (the finite part and the linear cusp error `rκ = k`), `ℓ²ρ_f^{−11/2}` and `ℓ³ρ_f^{−9}` (the
     last two for the elder density only).
   - The terms come in *matching* pairs. The `r³/k` layer of Lemma F matches the `κ^{−1}` tail of Lemma O, and the
     `C¹`-truncation `A₂(k) − A₂(0) = O(k)` in the finite part matches the linear cusp error `rκ = k`.
   - An exact max–min over the ledger (control R1; first observed by the referee) shows which pair blocks.
     - Remove the family `ρ_f⁵/ℓ`, that is, suppose the leading coefficients of the layer, the tail and the elder fold
       mass were computed and matched. Then both densities reach the next terms of the ledger, of order `ℓ^{4/9}` (with a
       logarithm for the elder density), subject to the next-order remainder of that expansion.
     - Remove instead only the linear pair `ℓρ_f^{−2}`, which needs the `O(r)`-correction `𝒜₃(κ)` of the cusp kernel;
       formally `𝒜₃` produces the next term, of order `ℓ^{1/2}` (#218 §0). This helps the candidate density, which
       reaches `ℓ^{4/9}`, but not the elder density: there `κ²r^{3/2}` and `κ³r²` balance `ρ_f⁵/ℓ` at the same
       `ρ_f = ℓ^{2/7}`.
   - So for the elder density, Lemma Q's bad events `𝔅_λ` and `𝔅_5` become the obstruction once the linear pair is
     resolved; improving them alone would not change the exponent.
2. **Parity (a sketch and an exploration; not used).** #218's closing remark of §3 proposed a parity argument for its
   `κ²`. Lemma L removes the `κ²` without it. Parity would give more. Under the contact law at `v_0(b, k)`, the odd
   jets are `N(12kw, Σ_o)` and independent of the even ones ((F7)); `tr(adj(A)B)` is odd, while `Y′`, `∂_Yw_κ(A, Y′)`
   and the elder window are even. So the first-order term of `w_κ(A, Y′ + 3k tr(adj(A)B)) − w_κ(A, Y′)` has mean `O(k²)`.
   The second-order remainder is `O(k²)` inside the elder window `|Y′| < 2κ|Δ|`, where the kink at `6κ|Δ|` is crossed only
   when `3k|tr(adj(A)B)| ≥ 4κ|Δ|`. For the candidate kernel the kink costs `O(κk²)` through the bounded density of
   `f₄`, so the bound is `O((1 + κ)k²)`. `O(k²)` is expected but not proved: crossing the kink needs
   `|f₄ − 3γᵀA^{−1}γ| ≈ 72κ`, hence `|f₄| ≳ κ` or `λ ≲ |γ|²/κ`, as in (3.2). In a `d = 2` toy model with these parities
   (deterministic quadrature; project archive), the difference `D(k)` satisfies `|D(k)|/k² ≤ 4.4` for `k ≤ 1/40` and
   `κ ∈ {1/2, 2, 8, 32}`, for both kernels. With parity broken, `D(k)/k` stays bounded uniformly in `κ`, as Lemma L
   predicts. Neither refinement changes the ledger.
3. **The equal-height kernel near the diagonal.** Math- #211 §2 (blob `ed0d3fa8`) records a heuristic: "The referee
   observed, heuristically, that at equal heights the two endpoint axial curvatures agree to leading order. That
   suggests `r^{d−1}Ψ_0 = O(r³)` and `I(s) ∝ s^{4−d}` near `0`, …". For the torus kernel, (W⁺.2) at `k = 0` proves this
   order up to the factor `log(2/r)`. In `d = 3` it gives `∫Ψ_0(b, se₁)db ≤ Cs log(2/s)` near `0`, consistent with the
   roughly linear rise of `I(s)` in #211's Monte Carlo for the Gaussian kernel. The proof goes through the typed
   window: at `k = 0` it forces `|Y_r| ≤ η = O(r)` (#198's remark after its proof of Lemma W), and this note's Step W2
   charges its conditional probability `O(min(1, r/|Δ|))`.
4. **The SIDE24 law.** With #207 §8 and #216 (Gaussian kernel, `d = 3`; numerical, not certified; #223 gives `c₂` in
   closed form), `c = 0.0417759`, `c₁ = −0.2118484` and `c₂/c = 3.859496`. Under (E3⁺.1),
   `ν_{3,24}(ℓ) = cℓ^{−1/3}(1 − 5.0711ℓ^{7/12} + 3.8595ℓ^{2/3} + O(ℓ^{16/21}))` up to the relative `O(e^{−L²/8})` of the
   kernel comparison; #220 had `O(ℓ^{23/33})`.
5. **Consistency.**
   - (C⁺.1) implies #218 (C.1), and (CE⁺.1) implies #220 (CE.1).
   - (T⁺.1) implies #218 (T.1); (E3⁺.0) implies #220 (E3.0); (E3⁺.1) implies #220 (E3.3).
   - (W⁺.1) implies #198 (W.1) for `k ≤ r`, since `(κ + r)²(κ + r log(2/r)) ≤ C(κ² + r²)`. (W⁺.3) implies (W.4).
   - (R⁺.1) implies #220 (E3′.0) and, with `I^{cand} − c₁ > 0` (#207 (CU′.2)), shows again that the rejected density
     approaches `B_{d,L}` from above.

## 7. Sources (exact identities in `SOURCES.json`)

| Tag | Path | Role |
|---|---|---|
| [R] | `frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md` (blob `247b3ecf`) | (R2)–(R5): pin densities, coupling, moments — consumed |
| [P] | `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md` (blob `dfed3b8d`) | §2 finite-jet rank, §15 parity factorization, through #218 and #220 — consumed |
| [E1] | `imports/lifetime_parent_20260925/ERRATUM_CONGRUENCE.md` (blob `213594d6`) | reading rule |
| [E2] | `reviews/d1_section9_borel_repair_20260925/REPAIR.md` (blob `fe9b9ce4`) | §9 replacement |
| [REC] | `reviews/d1_chain_reconciliation_20260928/RECONCILIATION.md` (blob `75da2597`) | reading rule |
| [Z] | `frontiers/c7_zero_gap_limit_20260929/PROOF.md` (blob `5b6328ea`) | (Z2)–(Z3): `Ψ_0`, `B_{d,L}` — consumed |
| [C7-K] | `frontiers/c7_total_bounded_20260929/PROOF.md` (blob `28748b08`) | (K2): the rejected fold mass — consumed |
| #191 | `frontiers/remainder_vanishing_20260930/PROOF.md` (merged; blob `441152df`) | Lemma E Steps 1–3 (for (F1) at `k = 0`); §2: `r_0^*`, the `k = 0` identity — consumed |
| #198 | `frontiers/remainder_rate_20260930/PROOF.md` (merged; blob `abfb98ae`) | §3 (3.1), the sign window, (3.2); Lemma W with its `k = 0` clause, (W.1); the proof of (W.4); Lemma F′ — consumed |
| #187 | `frontiers/far_elder_rate_20260930/PROOF.md` (merged 1 Oct at `c2f1270`; blob `07260114`) | Theorem F at `ρ = r_0^*`, for (E3⁺.1) and (R⁺.1) only — consumed |
| #207 | `frontiers/cusp_second_order_20261001/PROOF.md` (unmerged; blob `f6df5a73`, head `b12ff46`) | §0, (CU.2), §7 — **consumed, unmerged** |
| #218 | `frontiers/candidate_third_order_20261001/PROOF.md` (unmerged; blob `70ca57ef`, head `0cf048d`) | Lemmas D, F, C, O; (1.2); (0.1); §4 — **consumed, unmerged** |
| #220 | `frontiers/elder_third_order_20261001/PROOF.md` (unmerged; blob `c8767dde`, head `70dcf31`) | §0; Lemma Q; §2 facts, Lemmas G, CE; Lemmas O′, H, S′; §4 — **consumed, unmerged** |
| #216 | `frontiers/third_order_coefficient_20261001/NOTE.md` (unmerged) | values of `c₂`, Remark 4 — cited only |
| #223 | `frontiers/c2_exact_20261001/NOTE.md` (merged 1 Oct at `f9ebba1`; blob `a2798b87`) | `c₂` in closed form, Remark 4 — cited only |
| #211 | `frontiers/equal_height_mass_value_20261001/NOTE.md` (unmerged; blob `ed0d3fa8`, head `8e89fe8`) | the heuristic and Monte Carlo of Remark 3 — cited only |
| #188 | `frontiers/far_elder_flat_ridge_20260930/PROOF.md` (unmerged) | an alternative far bound — cited only |

## 8. Exact controls (`r37_check.py`; stdlib; exact rationals; byte-identical under `-O`)

- **R1** the ledger of §5. An error `r^pκ^q` on `[ρ_f, ρ_c]` integrates to `ℓ^q r^{p−4q+1}` at the dominating end. Checks:
  - the least exponent is `3/7` for both densities, attained exactly by the terms marked in the table;
  - every other term is `≥ 4/9`, and the intermediate separations give exactly `4/9`;
  - the hypotheses on the splits;
  - the optimality of `2/7`, `2/9` and `1/9` on rational grids;
  - the regressions `4/11` (#218's T1) and `2/5` (#220's intermediate bound);
  - that the old term `rκ²` would give `ℓ^{2/7}` at the new split;
  - the max–min of Remark 1: without the `ρ_f⁵/ℓ` family both densities reach `4/9`; without only the linear pair the
    candidate density reaches `4/9` and the elder density stays at `3/7`.
- **R2** Lemma L on random and edge rational instances, with equality instances, and instances where it improves on
  the constant `2c` by a factor `≥ 100`.
- **R3** the inclusion (3.2): on scalar instances with `|q| ≤ |γ|²/λ`, and on matrix instances `A = −O diag(μ)Oᵀ`
  (`m = 1, 2, 3`, rational orthogonal `O` by the Cayley transform, so `λ = min μ` exactly), where `q = γᵀA^{−1}γ` and
  `|q| ≤ |γ|²/λ` are computed exactly; and that (Q3) puts `|φ_r|` in `[1/6, 1/2]` on `𝔅_4`.
- **R4** the sign window and (4.1) on random rational data; the exact length `144κ + 24η/|Δ|` of the `f₄`-window; the
  splitting inequality of Step W2.
- **R5** `κ³ + κ²r + κr² + r³L ≤ (κ + r)²(κ + rL) ≤ (1 + L)(κ + r)³` for `L ≥ 0`, and `(κ + r)³ ≤ 4(κ³ + r³)`.
- **R6** the bookkeeping of Lemmas C⁺ and CE⁺, with `r = s²` and `κ = t²` (so that square roots are exact), and the
  comparison of (CE⁺.1) with (CE.1).
- **Mutants.** Each fails only its own control, and an unknown label exits 2:
  - M1 `ρ_f = ℓ^{3/11}`;
  - M2 the old cusp error `rκ²`;
  - M8 `ρ_c = ℓ^{1/4}`;
  - M6 `a = ℓ^{2/15}` (R1, all four);
  - M3 `max(|y|, |y′|)` in place of `|y| + |y′|` (R2);
  - M4 `12κ` in place of `6κ` in (3.2) (R3);
  - M5 `12η/|Δ|` in place of `24η/|Δ|` (R4);
  - M7 `r²(1 + κ)² ≤ r` (R6).

**What the controls do not test.** Lemmas C⁺ and CE⁺ and Proposition W⁺ as statements about random fields; the
conditional density facts (2.1)–(2.2), (4.2); the assembly. These are proved in prose. The controls test the
deterministic inequalities and the exponent arithmetic.

## 9. Review slices

- **A** §§1–2: Lemma L, and Lemma C⁺ as a change of #218's Step C2, with the bookkeeping of Step C3.
- **B** §3: Lemma CE⁺. The refined `𝔅_4′` estimate (3.1)–(3.2), with its use of (Q3), (2.1) and (2.2); Step E3⁺.
- **C** §§4–5: Proposition W⁺ ((4.1), the `f₄`-window, (4.2) and the dyadic layers); (W⁺.3); the assembly and the
  ledger.
