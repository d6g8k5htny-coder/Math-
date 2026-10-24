# Lifetime note C7: the elder density's `ℓ^{2/3}` term, and #242's Conjecture 7 in its `o(ℓ^{2/3})` form

Object: `CL-C7-ELDER-TWO-THIRDS-20261007-v1`. Claim: main#229 [6030036698](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6030036698).
Author: Anthropic Claude (claude.ai session `session_01NMeKEismAyeqgdB4sy2NJU`), 7 October 2026, for Dylan Roy (delegated AI
work). The same session wrote #187, #188, #220, #229, #240 and #242 and notes TS, EM, EM.1, LU, C3 and SL. The consumed
packets in turn consume OpenAI-authored sources, among them [R], [P] and [182].
Disposition: AUTHOR-SIDE PROOF CANDIDATE; NONAUTHOR REVIEW REQUIRED. Scientific effect: NONE — no register, graph, STATUS,
PROOF_INDEX, prize or Boolean change; no numerical constant is certified. Same GitHub account as every lane;
organizational independence 0. Before posting, three clean-context Claude subagents of this session refereed the draft in
three slices. All three returned AMEND with no blocking finding. The five non-blocking findings (one found by two slices)
were: the constant of (E′) must not depend on `ε`; Remark 3 misstated what a rate, and what the `O(ℓ^{3/4})` form, would
need; and #188 is a premise of (C7.1)–(C7.2), not only of (C7.3). Every finding, with 31 nits, is applied here, one of them
differently from the proposal (Remark 3's last input is an elder bound near `κ = r`, not on `κ ≤ r²`); the controls comment
lists them. These are author-side reads and earn no review credit.

**What is new.**
- **Theorem E (the elder weight on `κ ≤ r`)** (§1). For `0 < r ≤ r_*` and `0 < k ≤ r²`, uniformly in `u`,
  `0 ≤ 𝐓_r^{eld}(k, u) ≤ C[Υ(r, κ) + r²κ^{2/3}]`, with `Υ(r, κ) := min(rκ, r³(1 + log₊(κ/r²)))`.
  - Addendum EM.1's Theorem S‴⁺ has `rκ` in place of `Υ`. The two agree for `κ ≤ r²`. For `r² ≤ κ ≤ r`,
    `Υ = r³(1 + log(κ/r²))`: at most `rκ`, and with the factor `1 + log(κ/r²)` in place of the `log(2/r)` of #229's typed
    mass `r³log(2/r)`.
  - The new input is one line of note EM's own §4.1: on typed pairs in the good event `𝒢`, `s < s + s_S ≤ 12κ + 2ε̃`, so the
    soft curvature `s` is capped by typedness as well as by Lemma X's threshold. Note EM used the cap only for `s_S`.
- **Corollary E1 (the remainders without the logarithm)** (§2). The intermediate elder mass on `[ℓ^{1/5}, r_0^*]` is
  `O(ℓ^{2/3})`. So `ν_eld` and `ρ_rej` have remainder `O(ℓ^{2/3})`, and SIDE24's relative remainder is `O(ℓ)`, against note
  LU's `O(ℓ^{2/3}log(1/ℓ))` and `O(ℓ log(1/ℓ))`.
- **Lemma D (the ridge dichotomy)** (§3). Deterministic. On [N]'s window, an elder pair keeps the window ridge between the
  heights of `S` and `M` on all of `[−½, ½]` or on all of `[−3, −½]`. The proof uses only escape paths along the ridge and
  traps of #220's kind, and the absence of a second critical point at the height of `S`, which holds almost surely (Lemma D′).
- **Proposition G₀ (the elder kernel at gaps of order `r³`)** (§4). For every `c > 0`, `r^{−3}𝐓_r^{eld}(cr³, u) → 0` as
  `r ↓ 0`, uniformly in `u`. This is the one scale at which Theorem E's bound is of order `r³` and could carry an `ℓ^{2/3}`
  term of its own (Remark 1). There Lemma D turns `e = 1` into an `f₄`-window of width `O(κ + r²)`, where typedness leaves
  width `O(r)`.
- **Theorem C7 (the `ℓ^{2/3}` term of the elder density)** (§5). In every `d ≥ 2` and for every `L`, as `ℓ ↓ 0`,

      ν_eld(ℓ) = c ℓ^{−1/3} + c₁ ℓ^{1/4} + c₂ ℓ^{1/3} + (c₃ − R_{2/3}) ℓ^{2/3} + ν_eld^{far,r_0^*}(ℓ) + o(ℓ^{2/3}),         (C7.1)
      ρ_rej(ℓ) + ν_eld^{far,r_0^*}(ℓ) = B_{d,L} + (I^{cand} − c₁) ℓ^{1/4} + R_{2/3} ℓ^{2/3} + o(ℓ^{2/3}),                (C7.2)

  with `c₃` of note C3 and `R_{2/3}` of note SL. (C7.2) is #242's Conjecture 7 with `o(ℓ^{2/3})` in place of `O(ℓ^{3/4})`,
  and with `R_{2/3}` as in (SL), which is #242's (4.2) whenever the latter converges absolutely. The proof uses #188's
  Theorem G twice: at a fixed separation `ρ₀ ∈ (0, r_*]`, for the intermediate elder mass in (C7.1)–(C7.2), and at `r_0^*`,
  where it makes the far terms `O(ℓ^N)` (C7.3). For SIDE24 (`d = 3`, `L = 24`),
  `ν_{3,24}(ℓ) = cℓ^{−1/3}(1 + (c₁/c)ℓ^{7/12} + (c₂/c)ℓ^{2/3} + ((c₃ − R_{2/3})/c)ℓ + o(ℓ))`.

**Not claimed.**
- No rate. The remainder of (C7.1)–(C7.2) is `o(ℓ^{2/3})`, as in notes C3 and SL, whose dominated-convergence limits it
  consumes. #242's `O(ℓ^{3/4})` form of Conjecture 7 stays open (Remark 3).
- No value and no sign of `c₃ − R_{2/3}` for the torus field. In the model (`L = ∞`) the exploration values of notes C3 and SL
  (#244) give `c₃ − R_{2/3} ≈ 0.062` (`d = 2`) and `≈ 0.077` (`d = 3`) (Remark 5); nothing is claimed at `L = 24`.
- `R_{2/3}` is note SL's, with the `b`-integral inside; it equals #242's (4.2) when (4.2) converges absolutely (note SL,
  *Not claimed* and Remark 1; its Remark 2 is the Gaussian case). Nothing pointwise in `b`.
- No change to any statement of #187, #188, #220, #229, #237, #240, #242, notes TS, EM, EM.1, LU, C3 or SL. Corollary E1
  replaces note LU's remainders only.
- No certified number; no uniformity in `d` or `L`; nothing beyond the existential scope of the consumed sources. Whether
  IBA2-009 closes is for the audit's owners.

**Consumed.**
- Note EM (main#229 6023010944, with successor text 6023434026; Slice A PASS 6023042554, Slice B AMEND 6023045290, Slice C
  PASS 6023050789, readback PASS 6023435335): §0 (notation, `𝒩̄`, `H̃`, `μ`, `s`, `s_S`, `𝒢`, `ℬ`); §4.1 (a)–(f) (the ridge's
  second derivatives `g_𝔉″(−½) = −s` and `g_𝔉″(½) = s_S`, (4.1), (4.2), the bound `λ ≥ 2μ/3`, (4.5), the weight of (e) and
  (4.6), the layers and shells); §4.2 (the bad region's typed mass `E_Q[(W_r/r²)1_ℬ] ≤ Cr²(κ + r)r^{5/2}P^N`); §4.3; §5
  (`[r_*, r_0^*]` by note TS's (S″.2)).
- Addendum EM.1 (main#229 6024077582; Slice A PASS 6024106995, Slice B PASS 6024112289): Lemma B (B.1), with its radius
  (§2).
- Note TS (main#229 6020794123, with successor text 6021299833; read in every slice, readback PASS 6021301151): §0 (the
  kernels, `𝓐^{eld}`, `𝓐^{con}`, and `z = f₄ + 3|q|` on `{A < 0}`); §1 (`r_0^* ≤ L/(4√2)`, from #220's proof of Lemma S′);
  Theorem TL⁻; §5 (the decomposition (5.1), the three bounds on the cusp side, (5.0), and `I^{eld}` on `[ρ, ℓ^{1/5}]`).
- Note LU (main#229 6025486512, with successor text 6026230530; read in every slice, readback PASS 6026231785): Theorem U⁼;
  Theorem P⁺; §5 (its decomposition and ledger, with #187's far bound `O(ℓ^{2/3})` in it).
- Note C3 (main#229 6027862273; Slice A PASS 6027878271, Slice B PASS 6027885396, Slice C PASS 6028019347): Theorem C3; §4
  (the definition (4.1) of `D_r`, and the limit of `ℓ^{−2/3}∫_0^ρ∫D_r` at its fixed split).
- Note SL (main#229 6028358916; Slice A PASS 6028372615, Slice B PASS 6028379432): Theorem SL.
- [N] = #240 `frontiers/elder_cusp_parity_20261002/PROOF.md` (blob `16a1db06`): Lemma Q′ under (Q′1)–(Q′2) (its "Moreover"
  part, (1.2′)–(1.3′), and Steps Q1, Q2′, Q3, Q4 of its proof); (3.0) and Lemma R₂ ((3.2)).
- #220 `frontiers/elder_third_order_20261001/PROOF.md` (blob `c8767dde`): §0 (the pinned law `Q`, the elder mark with
  [182]'s maximin death level (2), and the identity `ν_eld = ∫_0^{r_0}∫∫r^{−2}A_r^{eld} + ν_eld^{far,r_0}` for every
  `r_0 ∈ (0, r_0^*]`); Steps Q2, Q3 ((1.4)) and the trap of Step Q6, Case R⁻; the proof of Lemma H (a) (`Q` as the Gaussian
  regression on the pin rows, and [P] §2's linear independence of derivative evaluation functionals at distinct sites);
  §2's facts (F3), (F4) and (2.1) under `Q`; and §4's identification of its far term with #187's (0.1), in the proof of
  (E3.3).
- #187 `frontiers/far_elder_rate_20260930/PROOF.md` (blob `07260114`): the definition (0.1), for the identification in §5;
  and its far bound `O(ℓ^{2/3})`, through note LU's ledger (Corollary E1).
- #229 `frontiers/third_order_rate_20261001/PROOF.md` (blob `110ed33a`): (W⁺.2) and (W⁺.3), through notes TS and LU.
- #242 `frontiers/soft_rejected_pairs_20261002/PROOF.md` (blob `271412db`): §0 (the identity
  `I^{cand} − c₁ = ∫_0^∞∫∫𝒜^{rej}(b, s^{−4}, u)db dσ ds`); Conjecture 7 (4.3) and its `R_{2/3}` (4.2).
- #188 `frontiers/far_elder_flat_ridge_20260930/PROOF.md` (blob `0b089b89`; merged on Math- 4 October at `f7f083ec`; an
  author-side candidate of this session, with OpenAI / GPT-5.6 Sol's nonauthor analytic ACCEPT of the proof at v1 `85f0586`,
  Math-#188 review 5366444067, whose §§1–3 are byte-identical in v1.1, confirmation 5974766943): the definition (0.1) and
  Theorem G (0.2).

**Cited only.** #237 §5 and #218 (through notes TS, LU and C3); #243's Theorem FL (a premise of Theorem SL; Remark 3);
Theorem QSF of the C89 extension on Math-#188 (OpenAI / Codex, comment 5963100306, review 5963217842, PASS_TECHNICAL_SCOPED;
Remark 3); #244 and #242 §5 (the model values of `R_{2/3}`); note C3 §5 and Corollary G′ (the model value of `c₃` and its
sign); #242 §4's inputs (i)–(iii) and its matched-asymptotics count; Lemma X of note EM and note TS's Remark 1 (for
Remark 2 and the prior work); Bulinskaya's lemma (for Lemma D′).

**Prior work and overlap.** I searched main#229, #259 and #275 and the Math- tree at `34618d0d` for Conjecture 7, `R_{2/3}`,
the elder mass on `κ ≤ r`, and the scale `k ≍ r³`.
- #242 §4 states Conjecture 7 and its inputs (i)–(iii). Note SL proved the integrated content of input (i) in `o(ℓ^{2/3})`
  form, and its Remark 1 recorded that the `o`-form of Conjecture 7 then reduces to the separations `κ ≤ 1`. Note C3's
  Remark 3 recorded the equivalence with an `ℓ^{2/3}` term `c₃ − R_{2/3}` of the near elder density.
- Addendum EM.1 (Corollary EM.1) bounds the elder mass on `κ ≤ r` by `O(ℓ^{2/3}log(1/ℓ))`, which note LU's Corollary LU
  carries. Note EM had `O(ℓ^{9/14})`, and its Remark 2 gives `O(ℓ^{2/3}log(1/ℓ))` for its good region alone; note TS's
  Remark 1 records `O(ℓ^{2/3})` as a formal target, not proved. No source identifies that mass, proves it without the
  logarithm, or isolates the scale `k ≍ r³`.
- No claim on main#229 covers these objects. This note's claim is [6030036698](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6030036698).

## 0. Setting and statements

Setting and notation are note TS's (§0), with note EM's §0 and [N]'s §1. In particular `κ = k/r`, `ℓ = kr³ = κr⁴`,
`P = 1 + |b| + k`, `M = −ru/2`, `S = ru/2`, `f(M) = b`, `f(S) = b − κr⁴`, and `e = 1{d_f(M) = f(S)}` with [182]'s maximin
death level `d_f(M)`.
- *Note EM's objects.* `𝒩̄ = C₀𝒩`; the window coordinates `Φ(X, Ξ) = rXu + r²ΘΞ` and `𝔉 = r^{−4}(f∘Φ − b)`; `H̃`, `D`,
  `μ = λ_min(−D)`, `s` and `s_S`; the good event `𝒢 = {A < 0, λ ≥ C_G𝒩r}` and the bad region `ℬ = {W_r > 0} ∖ 𝒢`.
- *[N]'s objects.* `Γ̃ = |A^{−1}γ|`, `ε̃`, `R′` and (Q′1)–(Q′2); the window `𝒲′ := [−3, 2] × {|Ξ| ≤ R′}`; the ridge maximizer
  `Ξ_𝔉(X)` and the ridge `g_𝔉(X) := 𝔉(X, Ξ_𝔉(X))` on `[−3, 2]`; the cusp ridge
  `g(X) = κ[2(X + ½)²(X − 1) + 3φ(X² − ¼)²] = 2κ(X + ½)²(X − 1) + (z/24)(X² − ¼)²` with `z = f₄ − 3q`, `q = γᵀA^{−1}γ` and
  `φ = z/(72κ)`; `h := g_𝔉 − g`; and Lemma R₂'s `Q₁ = f₅/120 − ηᵀA^{−1}γ/12 + γᵀA^{−1}BA^{−1}γ/8` and `ε₂′`.
- *Kernels.* `Q = Q_{r,b,k}` is the pinned law at fixed birth height `b` (#220 §0), and
  `𝐓_r^{eld}(k, u) = ∫_R r^{−2}A_r^{eld}(b, k, u)db` (note TS §0), with `r^{−2}A_r^{eld} = 12π_r(v_r)r^{−2}E_Q[(W_r/r²)e]` and
  `π_r(v_r) ≤ Ce^{−c(b² + k²)}` (note EM §4.3). So a bound `E_Q[(W_r/r²)e1_E] ≤ Cr²βP^N` on an event `E` gives a part of
  `𝐓_r^{eld}` of at most `C′β`, uniformly in `u` ("integrating in `b`").
- *Constants.* `C, c, N` depend only on `d` and `L` (and on named parameters), may change from line to line, and never
  depend on `r`, `k`, `κ`, `b` or `u`.

For `0 < κ ≤ r ≤ 1` put, with `log₊ := max(log, 0)`,

    Υ(r, κ) := min( rκ,  r³(1 + log₊(κ/r²)) ).                                                                      (0.1)

**Theorem E (the elder weight on `κ ≤ r`).** There are `r_* > 0` and `C, N` such that for `0 < r ≤ r_*`, `b ∈ R`,
`u ∈ S^{d−1}` and `0 < k ≤ r²`,

    E_Q[(W_r/r²) e] ≤ C r² [ Υ(r, κ) + r²κ^{2/3} ] P^N,        0 ≤ 𝐓_r^{eld}(k, u) ≤ C [ Υ(r, κ) + r²κ^{2/3} ].         (E)

Moreover, with the same `r_*`, `C` and `N` (in particular `C` does not depend on `ε`), for `0 < ε ≤ 1` the part of the
good region where `μ < ε` satisfies

    E_Q[(W_r/r²) e 1_{𝒢∩{μ<ε}}] ≤ C r² [ εrκ + r^{7/3}κ^{2/3}log(2/r) ] P^N,                                           (E′)

so the corresponding part of `𝐓_r^{eld}(k, u)` is at most `C[εrκ + r^{7/3}κ^{2/3}log(2/r)]`, uniformly in `u`.

**Corollary E1 (the remainders without the logarithm).** As `ℓ ↓ 0`, `∫_{ℓ^{1/5}}^{r_0^*}∫𝐓_r^{eld}(ℓ/r³, u)dσ(u)dr = O(ℓ^{2/3})`,
and

    ν_eld(ℓ) = cℓ^{−1/3} + c₁ℓ^{1/4} + c₂ℓ^{1/3} + O(ℓ^{2/3}),        ρ_rej(ℓ) = B_{d,L} + (I^{cand} − c₁)ℓ^{1/4} + O(ℓ^{2/3}).   (E1)

For SIDE24, `ν_{3,24}(ℓ) = cℓ^{−1/3}(1 + (c₁/c)ℓ^{7/12} + (c₂/c)ℓ^{2/3} + O(ℓ))`.

**Lemma D (the ridge dichotomy).** Deterministic. In [N] §1's setting (`0 < r ≤ r_Q`, `𝒩 ≥ max(1, ‖f‖_{C⁵})`, and
`A ≤ −λI` with `λ > 0`), let `f ∈ C⁵(X)` have the pins, let `κ > 0`, and assume (Q′1)–(Q′2) and `H̃ < 0`. Assume moreover

    (G)  no point of Φ(𝒲′) other than S is a critical point of f with value f(S).

If `e(f) = 1`, then `g_𝔉(X) ∈ [−κ, 0]` for every `X ∈ [−½, ½]`, or `g_𝔉(X) ∈ [−κ, 0]` for every `X ∈ [−3, −½]`. (G) is
needed by the argument: a ridge with a local minimum of value `−κ` in `(−½, ½)` can defeat both escape and trap and both
alternatives (control K4's tie witness, and mutant M8).

**Lemma D′ ((G) is generic).** For `0 < r ≤ r_0^*`, `b ∈ R`, `u ∈ S^{d−1}` and `0 < k ≤ 1`, `Q`-almost surely no point of `X`
other than `S` is a critical point of `f` with value `f(S)`. In particular (G) holds `Q`-almost surely on `{A < 0}`, where
`𝒲′` is defined.

**Proposition G₀ (the elder kernel at gaps of order `r³`).** For every `c > 0`,
`lim_{r↓0} r^{−3} sup_{u∈S^{d−1}} 𝐓_r^{eld}(cr³, u) = 0`.

**Theorem C7 (the `ℓ^{2/3}` term of the elder density).** In every `d ≥ 2` and for every `L`, (C7.1) and (C7.2) hold as
`ℓ ↓ 0`, with `c₃` of note C3 ((C3)) and `R_{2/3}` of note SL ((SL)); the proof uses #188's Theorem G at a fixed separation
`ρ₀ ≤ r_*` (§5). By #188's Theorem G at `ρ = r_0^*`, `ν_eld^{far,r_0^*}(ℓ) = O(ℓ^N)` for every `N`, so

    ν_eld(ℓ) = cℓ^{−1/3} + c₁ℓ^{1/4} + c₂ℓ^{1/3} + (c₃ − R_{2/3})ℓ^{2/3} + o(ℓ^{2/3}),
    ρ_rej(ℓ) = B_{d,L} + (I^{cand} − c₁)ℓ^{1/4} + R_{2/3}ℓ^{2/3} + o(ℓ^{2/3}).                                         (C7.3)

## 1. Proof of Theorem E

Take `r_*` as in addendum EM.1 §2 (Lemma B). It is at most note EM §4's, so `r_* ≤ min(r_0^*, r_Q) ≤ 1/10`; its extra
condition `r + r^{3/2} ≤ L/4` already holds for `r ≤ min(r_0^*, 1/10)`, since `r_0^* ≤ L/(4√2)` (note TS §1). Fix
`0 < r ≤ r_*`, `b`, `u` and `0 < k ≤ r²`, so `κ ≤ r`.

*The good region.* Follow note EM §4.1 (a)–(f), with one change in (d)–(f).
- *A second cap on `s`.* On `𝒢 ∩ {W_r > 0}`, `s_S > 0`, so (4.1) gives `s < s + s_S ≤ 12κ + 2ε̃`. By (4.2) and `λ ≥ 2μ/3`
  (EM §4.1 (d)), `2ε̃ ≤ C♮𝒩̄²r/μ`. With (4.5), on `𝒢 ∩ {W_r > 0} ∩ {e = 1}`

      s < ε*(κ, μ, 𝒩) := min( ε̄(κ, μ, 𝒩),  12κ + C♮𝒩̄²r/μ ).                                                       (1.1)

  By (1.1), (4.6) holds with `ε*` in place of `ε̄`. Both entries of `ε*` increase with `𝒩`, so on `{2^j ≤ 𝒩 < 2^{j+1}}` the
  indicator `1{s < ε*(κ, μ, 𝒩)}` is at most `1{s < ε*_j(μ)}`, with `ε*_j(μ) := ε*(κ, μ, 2^{j+1})`. As `ε*_j(μ)` is a function
  of `D`, EM's `ã`-integration given `(β̃, D)` gives `Cε*_j(μ)²`, and (V.3) bounds the shell `[x, 2x]` of layer `j` by
  `C2^{jN}P^N x sup_{μ∈[x,2x]} r³με*_j(μ)²`.
- *The integrand.* EM §4.1 (f) gives `με̄² ≤ C𝒩̄^N[μκ² + κ + r^{4/3}κ^{2/3}μ^{−1}]`, and directly
  `μ(12κ + C♮𝒩̄²r/μ)² ≤ C𝒩̄^N[μκ² + κr + r²μ^{−1}]`. Since `min(a + b, c + d) ≤ min(a, d) + b + c` for `a, b, c, d ≥ 0`,
  applied pointwise in `μ` with `a = κ`, `b = μκ² + r^{4/3}κ^{2/3}μ^{−1}`, `c = μκ² + κr` and `d = r²μ^{−1}`,

      με*² ≤ C𝒩̄^N [ μκ² + κr + r^{4/3}κ^{2/3}μ^{−1} + min(κ, r²μ^{−1}) ]                                             (1.2)

  (control K1).
- *The shells.* The dyadic `x` of layer `j` lie in `[x_j, y_j]`, with `y_j = C₀2^{j+1}`, and there are at most `Clog(2/r)` of
  them (EM §4.1 (f)). So `Σ_x x² ≤ C2^{2j}`, `Σ_x x ≤ C2^j` and `Σ_x 1 ≤ Clog(2/r)`. A shell's factor `x` turns the last
  term of (1.2), at `μ ∈ [x, 2x]`, into at most `x·min(κ, r²/x) = min(xκ, r²)`, and

      Σ_x min(xκ, r²) ≤ C 2^j min( κ, r²(1 + log₊(κ/r²)) ):                                                          (1.3)

  the sum is at most `Σ_x xκ ≤ 2y_jκ = 4C₀2^jκ`; and the terms with `xκ ≤ r²` form a geometric series with sum at most `2r²`.
  The others each equal `r²` and number at most `n₊ ≤ max(0, log₂(y_jκ/r²) + 1) ≤ log₂(4C₀) + j + log₂₊(κ/r²)`. So
  `Σ_x min(xκ, r²) ≤ r²(2 + n₊) ≤ (4 + log₂C₀)2^jr²(1 + log₊(κ/r²))` (control K2).
- *Layer `j`.* By (1.2)–(1.3), layer `j` contributes at most
  `C2^{jN}P^N r³[κ² + κr + r^{4/3}κ^{2/3}log(2/r) + min(κ, r²(1 + log₊(κ/r²)))]`. As `κ ≤ r`, `κ² ≤ κr`, and
  `κr ≤ min(κ, r²(1 + log₊(κ/r²)))` (if `κ ≤ r²` the minimum is `κ ≥ κr`; otherwise it is at least `r² ≥ κr`). Summing the
  layers as in EM (`p` large),

      E_Q[(W_r/r²) e 1_𝒢] ≤ C r² [ Υ(r, κ) + r^{7/3}κ^{2/3}log(2/r) ] P^N.                                           (1.4)

- *(E′).* A point with `μ < ε` lies in a shell `[x, 2x]` with `x < ε`. Keeping only those shells (dyadic, all below `ε`),
  `Σ_{x<ε} x² ≤ 2ε²`, `Σ_{x<ε} x ≤ 2ε` and `Σ_{x<ε} min(xκ, r²) ≤ 2εκ`, so the bracket of layer `j` becomes
  `2ε²κ² + 2εκr + 2εκ + r^{4/3}κ^{2/3}log(2/r) ≤ 6εκ + r^{4/3}κ^{2/3}log(2/r)` (`ε, κ, r ≤ 1`). Summing the layers gives
  (E′). These sums, and hence `C`, do not depend on `ε`.

*The bad region.* Lemma B of addendum EM.1 gives `E_Q[(W_r/r²)e1_ℬ] ≤ Cr²[rκ + r²κ^{2/3}]P^N`, and note EM §4.2 ("without
the elder mark") gives `E_Q[(W_r/r²)1_ℬ] ≤ Cr²(κ + r)r^{5/2}P^N ≤ 2Cr²r^{7/2}P^N`. So the bad region costs at most
`Cr²[min(rκ, r^{7/2}) + r²κ^{2/3}]P^N`, and `min(rκ, r^{7/2}) ≤ Υ(r, κ)`: if `κ ≤ r²` the left side is at most `rκ = Υ`;
otherwise `Υ ≥ r³ ≥ r^{7/2}`.

*Conclusion.* Add the two regions, and use `r^{7/3}κ^{2/3}log(2/r) ≤ Cr²κ^{2/3}` (`r^{1/3}log(2/r) ≤ C` on `(0, 1/10]`). This
is the first bound of (E). The bound on `𝐓_r^{eld}` follows from it as in note EM §4.3, by integrating
`12π_r(v_r)r^{−2}E_Q[(W_r/r²)e]` in `b`; (E′) passes to `𝐓_r^{eld}` in the same way. ∎

## 2. Proof of Corollary E1

Substitute `r = ℓ^{1/6}t`. Then `rκ = ℓ/r³ = ℓ^{1/2}t^{−3}`, `r³ = ℓ^{1/2}t³`, `κ/r² = ℓ/r⁶ = t^{−6}` and `dr = ℓ^{1/6}dt`
(control K3). So

    ∫_{ℓ^{1/5}}^{r_*} Υ(r, ℓ/r⁴) dr ≤ ℓ^{2/3} ∫_0^∞ Υ̃(t) t³ dt,        Υ̃(t) := min( t^{−6},  1 + 6log₊(1/t) ),         (2.1)

and `∫_0^∞ Υ̃(t)t³dt = 9/8`. For `t ≥ 1`, `Υ̃ = t^{−6}` and `∫_1^∞ t^{−3}dt = 1/2`. For `t ≤ 1`, put `y = t⁶`; since
`log(1/y) ≤ 1/y − 1`, `y(1 + log(1/y)) ≤ 1`, so `Υ̃ = 1 + 6log(1/t)`, and `∫_0^1 t³(1 + 6log(1/t))dt = 1/4 + 6/16 = 5/8`
(control K3). Also `∫_{ℓ^{1/5}}^{r_*}r²κ^{2/3}dr = ℓ^{2/3}∫_{ℓ^{1/5}}^{r_*}r^{−2/3}dr ≤ 3r_*^{1/3}ℓ^{2/3}`. On `[r_*, r_0^*]`, note
TS's (S″.2) gives `O(ℓ^{2/3})` (note EM §5). So the elder mass on `[ℓ^{1/5}, r_0^*]` is `O(ℓ^{2/3})`.

In note LU §5's ledger (at `σ = 5/24`) this replaces the row `ℓ^{2/3}log(1/ℓ)` of Corollary EM.1. Every other row has
exponent `≥ 2/3`, and the two with a logarithm have exponents `3/4` and `5/6` (control K7). So the first line of note LU's
(LU) holds with `O(ℓ^{2/3})`. Subtracting it from note LU's Theorem P⁺ gives the second (`cℓ^{−1/3}` and `c₂ℓ^{1/3}` cancel).
For SIDE24 divide by `cℓ^{−1/3}`: `2/3 + 1/3 = 1`. ∎

## 3. Proofs of Lemmas D and D′

*Window facts.* Assume (Q′1)–(Q′2). [N]'s Lemma Q′ ("Moreover" part, with Steps Q1, Q2′, Q3 and Q4 of its proof) gives:
- (W1) `Φ` embeds a neighbourhood of `𝒲′`, and `∂_Ξ²𝔉 ≤ −(λ/2)I` on `𝒲′`.
- (W2) For each `X ∈ [−3, 2]`, `𝔉(X, ·)` has a unique maximizer `Ξ_𝔉(X)` over `{|Ξ| ≤ R′}`, in the interior. `X ↦ Ξ_𝔉(X)`
  is continuous (indeed `C¹`, by the implicit function theorem as in #220's Step Q2, and uniqueness of the maximizer),
  `g_𝔉` is `C²`, `g_𝔉(−½) = 0`, `g_𝔉(½) = −κ`, `g_𝔉′(±½) = 0`, and `g_𝔉′(X) = ∂_X𝔉(X, Ξ_𝔉(X))` (the envelope identity). As
  `H̃ < 0`, `g_𝔉″(−½) = −s < 0`, as in note EM §4.1 (a), whose derivation uses only Steps Q1, Q2′ and Q4 and so holds under
  (Q′1)–(Q′2) without `𝒢`. So `M̂` is a strict local maximum of the ridge.
- (W3) On `|Ξ| = R′`, `𝔉(X, Ξ) ≤ g_𝔉(X) − (9/4)(κ + 1)` (#220 (1.4); [N] Step Q3).

Three consequences:
- (i) *Ridge extrema are critical points.* If `X₀ ∈ (−3, 2)` is a local extremum of `g_𝔉`, then `∂_Ξ𝔉 = 0` at the interior
  maximizer and `∂_X𝔉 = g_𝔉′(X₀) = 0` by (W2). So `Φ(X₀, Ξ_𝔉(X₀))` is a critical point of `f`, with value `b + r⁴g_𝔉(X₀)`.
- (ii) *Escape.* Let `X₁ ∈ [−3, ½)` with `g_𝔉(X₁) > 0`, and suppose `g_𝔉 > −κ` on the closed interval between `−½` and `X₁`.
  The ridge curve `X ↦ Φ(X, Ξ_𝔉(X))` over that interval runs from `M` to a point above `b`, and along it `f > f(S)`; by
  compactness its minimum exceeds `f(S)`. So `d_f(M) > f(S)` and `e = 0` ([182] (2)).
- (iii) *Trap.* Let `X_L ∈ [−3, −½)` and `X_R ∈ (−½, 2]` with `g_𝔉(X_L) < −κ`, `g_𝔉(X_R) < −κ` and `g_𝔉 ≤ 0` on
  `[X_L, X_R]`. Put `t* := max(g_𝔉(X_L), g_𝔉(X_R), −(9/4)(κ + 1)) < −κ` and `𝒟 := (X_L, X_R) × {|Ξ| < R′}`. On `∂𝒟`,
  `𝔉 ≤ t*`: at the end slices because `𝔉 ≤ g_𝔉`, on `|Ξ| = R′` by (W3) and `g_𝔉 ≤ 0`. In `𝒟`, `𝔉 ≤ g_𝔉 ≤ 0`. So the path
  component of `{f > b + r⁴t*}` containing `M` lies in `Φ(𝒟)` (by (W1), `Φ(𝒟)` is open with boundary in `Φ(∂𝒟)`) and has
  supremum at most `b`, and every path from `M` to a point above `b` leaves it. Hence `d_f(M) ≤ b + r⁴t* < f(S)` (or
  `d_f(M) = −∞`) and `e = 0`. This is #220's trap of Case R⁻ (Step Q6).

*Proof of Lemma D.* Assume `e = 1` and (G). By (i) and (G), no local extremum of `g_𝔉` in `(−3, ½)` has the value `−κ`.

*Case 1: `g_𝔉 > 0` somewhere on `(−½, ½)`.* Put `X₁ := inf{X ∈ (−½, ½) : g_𝔉(X) > 0}`, so `g_𝔉 ≤ 0` on `[−½, X₁]` and
`g_𝔉(X₁) = 0`. If `m₁ := min_{[−½, X₁]}g_𝔉 > −κ`, pick `X₁′ ∈ (X₁, ½)` with `g_𝔉(X₁′) > 0` and `g_𝔉 > −κ` on `[X₁, X₁′]`
(continuity at `X₁`); (ii) gives `e = 0`, a contradiction. If `m₁ = −κ`, it is attained at an interior point of
`[−½, X₁]` (both end values are `0`), which is then a local minimum of `g_𝔉` with value `−κ`, excluded. So `m₁ < −κ`, and
Case 2 applies.

*Case 2: `g_𝔉 < −κ` somewhere on `(−½, ½)`.* Put `X₀ := inf{X ∈ (−½, ½) : g_𝔉(X) < −κ}`. Then `X₀ > −½`, `g_𝔉 ≥ −κ` on
`[−½, X₀]` and `g_𝔉(X₀) = −κ`.
- *The right side.* Suppose `g_𝔉 > 0` somewhere on `(−½, X₀)`, and put `X₁ := inf{X ∈ (−½, X₀) : g_𝔉(X) > 0}`. As in
  Case 1, `g_𝔉 ≤ 0` on `[−½, X₁]` and `g_𝔉(X₁) = 0`, and now `m₁ := min_{[−½, X₁]}g_𝔉 ≥ −κ`. If `m₁ > −κ`, (ii) with a point
  `X₁′ ∈ (X₁, X₀)` chosen as in Case 1 gives `e = 0`; if `m₁ = −κ`, it is an excluded local minimum. So `g_𝔉 ∈ [−κ, 0]` on `[−½, X₀]`. Choose `X_R ∈ (X₀, ½)` with
  `g_𝔉(X_R) < −κ` and `g_𝔉 ≤ 0` on `[X₀, X_R]` (`g_𝔉(X₀) = −κ < 0`, and `X₀` is an infimum).
- *The left side.* If `g_𝔉 ∈ [−κ, 0]` on all of `[−3, −½]`, the second alternative holds. Otherwise
  `B_L := {X ∈ [−3, −½) : g_𝔉(X) ∉ [−κ, 0]}` is nonempty and relatively open in `[−3, −½)`. It stays away from `−½`, since
  `g_𝔉 ∈ [−κ, 0]` near `−½` (`g_𝔉(−½) = g_𝔉′(−½) = 0` and `g_𝔉″(−½) = −s < 0`). A nonempty, relatively open subset of
  `[−3, −½)` that stays away from `−½` has its supremum in `(−3, −½)` and does not contain it. So `X_L′ := sup B_L` lies in
  `(−3, −½) ∖ B_L`, `g_𝔉 ∈ [−κ, 0]` on `[X_L′, −½]`, points of `B_L` accumulate at `X_L′` from the left, and by continuity
  `g_𝔉(X_L′) ∈ {0, −κ}`.
  - If `g_𝔉(X_L′) = 0`, points of `B_L` just left of `X_L′` have `g_𝔉 > 0`. If `min_{[X_L′, −½]}g_𝔉 > −κ`, (ii) with such a
    point gives `e = 0`. Otherwise the minimum `−κ` is attained in `(X_L′, −½)` (both end values are `0`) at a local minimum,
    excluded.
  - If `g_𝔉(X_L′) = −κ`, points of `B_L` just left of `X_L′` have `g_𝔉 < −κ`; pick one, `X_L`, with `g_𝔉 ≤ 0` on
    `[X_L, X_L′]`. Then `g_𝔉 ≤ 0` on `[X_L, X_R]`, and (iii) gives `e = 0`.

  Both contradict `e = 1`. So in Case 2 the second alternative holds.

*Case 3: neither.* Then `g_𝔉 ∈ [−κ, 0]` on `(−½, ½)`, hence on `[−½, ½]` by continuity: the first alternative. ∎

*Proof of Lemma D′.* Under `Q` the field is the torus field `F` conditioned on its pin rows, the `2d + 2` functionals
`f(M)`, `f(S)`, `∇f(M)`, `∇f(S)` with target `(b, b − kr³, 0, 0)` (#220 §0, and its proof of Lemma H (a)).
- *Nondegeneracy at three points.* By [P] §2, as quoted in #220's proof of Lemma H (a), "any finite list of distinct
  derivative evaluation functionals at distinct sites is linearly independent". (Directly: the covariance of [P] §1's
  field has all its Fourier weights positive, being the normalized `L`-periodization of `e^{−|z|²/2}`; so a functional
  `Λ = Σ_j(a_jδ_{x_j} + b_j·∇δ_{x_j})` of zero variance annihilates every trigonometric polynomial, hence every `C¹` function,
  and testing with `C¹` bumps gives `a_j = 0` and `b_j = 0`.) So the values and gradients at distinct points have a
  nondegenerate joint Gaussian law.
- *The conditioned field.* Fix `x ∉ {M, S}`. By the first bullet at the points `M, S, x`, the pins together with
  `Y(x) := (∇f(x), f(x) − f(S))` have a nondegenerate joint law. So under `Q` the vector `Y(x)` is Gaussian with a
  nondegenerate covariance (a Schur complement), continuous in `x`, and its density is bounded uniformly for `x` in compact
  subsets of `X ∖ {M, S}` and arguments near `0`.
- *No zero.* Bulinskaya's lemma, in its multiparameter form, says: a random field with `C¹` paths on an open subset of
  `R^d`, with values in `R^{d′}`, `d′ > d`, and one-point densities bounded near a level uniformly on compact subsets,
  almost surely does not take that level. Apply it to `Y` (`d′ = d + 1`) on the open sets
  `{x : |x − M| > 1/n, |x − S| > 1/n}`, whose closures are compact in `X ∖ {M, S}`, and let `n → ∞`: almost surely no
  `x ∉ {M, S}` has `Y(x) = 0`. And `M` is not a critical point at the level `f(S)`, since `f(M) − f(S) = kr³ > 0`. ∎

## 4. Proof of Proposition G₀

Fix `c > 0` and `ε ∈ (0, 1]`. For `r ≤ min(r_*, 1/c)` put `k := cr³`, so `k ≤ r²` and `κ = cr² ≤ r`. Split `{W_r > 0}` into
`ℬ`, `𝒢 ∩ {W_r > 0, μ < ε}` and `𝒢 ∩ {W_r > 0, μ ≥ ε}` (on `𝒢 ∩ {W_r > 0}`, `H̃ < 0`, so `D < 0` and `μ` is defined).
- *`ℬ`.* By note EM §4.2 ("without the elder mark"), integrated in `b` as in §1, this part of `𝐓_r^{eld}` is at most
  `C(κ + r)r^{5/2} ≤ 2Cr^{7/2}`.
- *`𝒢 ∩ {W_r > 0, μ < ε}`.* By (E′), whose constant does not depend on `ε`, at most
  `C[εrκ + r^{7/3}κ^{2/3}log(2/r)] = C[εcr³ + c^{2/3}r^{11/3}log(2/r)]`.
- *`𝒢 ∩ {W_r > 0, μ ≥ ε}`.* At most `C_εr²(κ + r²) = C_ε(c + 1)r⁴`, shown below.

Dividing by `r³` (control K6), `limsup_{r↓0} r^{−3}sup_u𝐓_r^{eld}(cr³, u) ≤ Cεc` for every `ε ∈ (0, 1]`, with `C` independent
of `ε`, so the limit is `0`.

*The part `𝒢 ∩ {μ ≥ ε}`.* Work under `Q` at fixed `b`, as in note EM §4.1, and integrate in `b` at the end.
- (a) *The weight.* On `𝒢 ∩ {W_r > 0}`, (Q′1)–(Q′2) hold (note EM §4.1 (a)) and `H̃ < 0`. By note EM §4.1 (e),
  `W_r/r² = r²ss_S|det D||det D_S| ≤ 3r²μ²𝒩̄^{2m−2}ss_S`. By (4.1)–(4.2), `λ ≥ 2μ/3` and `κ ≤ r`, both `s` and `s_S` are
  below `12κ + 2ε̃ ≤ C𝒩̄²r/μ`. So `W_r/r² ≤ C𝒩̄^Nr⁴`.
- (b) *The ridge.* On `{e = 1}`, off the null set of Lemma D′, Lemma D gives `X* ∈ {0, −1}` with `g_𝔉(X*) ∈ [−κ, 0]`.
- (c) *The window.* Lemma R₂ applies: its hypotheses are (Q′1)–(Q′2) and `𝒩̄ ≥ max(1, ‖f‖_{C⁶})`, and the latter holds by
  note EM §0, since `𝒩̄ = C₀𝒩` bounds every derivative of order `≤ 9` along unit vectors. It gives
  `|g_𝔉(X*) − g(X*) − rQ₁X*(X*² − ¼)²| ≤ ε₂′`. At `X* = 0`, `g(0) = −κ/2 + z/384`, so `z/384 ∈ [−κ/2 − ε₂′, κ/2 + ε₂′]`. At
  `X* = −1`, `g(−1) = −κ + 3z/128` and `rQ₁X*(X*² − ¼)² = −(9/16)rQ₁`, so `3z/128 − (9/16)rQ₁ ∈ [−ε₂′, κ + ε₂′]` (control
  K5). So `z` lies in the union `I` of two intervals, determined by `κ`, `rQ₁` and `ε₂′`, with
  `|I| ≤ (384 + 128/3)(κ + 2ε₂′) ≤ 427(κ + 2ε₂′)`.
- (d) *The probability.* On `{A < 0}`, `z = f₄ + 3|q|` (note TS §0), and neither `q = γᵀA^{−1}γ` nor `Q₁` involves `f₄`
  ([N] (3.0)). `ε₂′ = C₉[𝒩̄r²(1 + Γ̃)³ + 𝒩̄²r²(1 + Γ̃)²/λ]` increases with `𝒩̄`. In the layer `{2^j ≤ 𝒩 < 2^{j+1}}`,
  evaluating `ε₂′` at `𝒩̄ = C₀2^{j+1}` gives a set `I_j` of values of `f₄`, a union of two intervals that depends only on `J″`
  (the free jets other than `f₄`, #220 §2), with `|I_j| ≤ 427(κ + 2ε′_{2,j})`. On `𝒢 ∩ {W_r > 0, μ ≥ ε}`,
  `λ ≥ 2μ/3 ≥ 2ε/3`, so
  `Γ̃ ≤ |γ|/λ ≤ 2|γ|/ε` and `ε′_{2,j} ≤ Cε^{−3}2^{2j}r²(1 + |γ|)³`. Hence, off a `Q`-null set,

      (W_r/r²) e 1_{𝒢∩{μ≥ε}} 1{2^j ≤ 𝒩 < 2^{j+1}} ≤ C2^{jN} r⁴ 1{A < 0, λ ≥ 2ε/3, f₄ ∈ I_j} 1{𝒩 ≥ 2^j}.

  Take `E_Q`. By #220's (F4), `P_Q(𝒩 ≥ 2^j | J′) ≤ C_p2^{−jp}(P + |J′|)^p`, and `(P + |J′|)^p ≤ (P + |J″|)^p(1 + |f₄|)^p`. By
  #220's (F3) and (2.1), `E_Q[(1 + |f₄|)^p1{f₄ ∈ I} | J″] ≤ C_p(P + |J″|)^p|I|` for each `J″`-measurable interval `I`. Under
  `Q`, `J″` is Gaussian with mean of size `O(P)` and bounded covariance (#220 (F3)). So the layer contributes at most
  `C_p2^{j(N−p)}r⁴E_Q[(P + |J″|)^{2p}|I_j|1{λ ≥ 2ε/3}] ≤ C_pε^{−3}2^{j(N+2−p)}r⁴(κ + r²)P^{N′}`. With `p` large, summing over
  `j`, `E_Q[(W_r/r²)e1_{𝒢∩{μ≥ε}}] ≤ C_εr²·r²(κ + r²)P^N`, and integrating in `b` gives `C_εr²(κ + r²)`. ∎

## 5. Proof of Theorem C7

Use note TS §5's decomposition (5.1) with `ρ := ℓ^σ` and `σ := 4/19`, as note LU §5 does with `σ = 5/24`:

    ν_eld − cℓ^{−1/3} − ν_eld^{far,r_0^*} = 𝒦₁ − 𝒦₂ + I^{eld} + J₄,                                                    (5.1)

with `𝒦₁ = ∫_0^ρ∫(𝐓_r − r^{−2}𝐀₀)`, `𝒦₂ = ∫_0^ρ∫𝐓_r^{rej}`, `I^{eld} = ∫_ρ^{r_0^*}∫𝐓_r^{eld}` and `J₄ = −∫_ρ^∞∫r^{−2}𝐀₀` (integrands
at `(ℓ/r³, u)`). Since `1/5 < σ < 1/4`, `ℓ^{1/4} < ρ < ℓ^{1/5}`. For small `ℓ`, `ρ` is below note C3's fixed split
`ρ_f = min(r₄, r₀/2)` (note LU §4; this `r₀` is #237 §5's radius) and below the radius of Theorem TL⁻ at
`θ := (1 − 4σ)/σ = 3/4`, and `ℓ^{1/5} < r_*`. The choice `σ = 4/19` balances the two rows `ρ⁸/ℓ` and `ℓ³ρ^{−11}` below, at
`13/19`; any `σ ∈ (5/24, 7/33)` would do. The exponents below are derived from their integrands by control K7.
- *`𝒦₁`.* With note C3's `D_r` ((4.1) there), `𝐓_r − r^{−2}𝐀₀ = 𝐓_r(0) + [𝐀₂(k) − 𝐀₂(0)] + 𝓐(κ) + D_r`. As in note LU §5:
  `∫_0^ρ∫[𝐀₂(ℓ/r³) − 𝐀₂(0)] = c₂ℓ^{1/3} + O(ℓ²ρ^{−5})`, `∫_0^ρ∫𝓐(ℓ/r⁴) = I^{cand}ℓ^{1/4} − ∫_ρ^∞∫𝓐(ℓ/r⁴)`, and
  `0 ≤ ∫_0^ρ∫𝐓_r(0) ≤ Cρ⁴log(2/ρ)` (#229 (W⁺.3)). Note C3's §4 gives `ℓ^{−2/3}∫_0^{ρ_f}∫D_r → c₃`. On `[ρ, ρ_f]`, `κ ≤ 1` and
  `k ≤ 1`, so Theorem U⁼ gives `|D_r| ≤ C(r²κ + rk) = 2Cℓr^{−2}`, which integrates to at most `2Cℓ/ρ = 2Cℓ^{15/19}`. So

      𝒦₁ = ∫_0^ρ∫𝐓_r(0) + c₂ℓ^{1/3} + I^{cand}ℓ^{1/4} − ∫_ρ^∞∫𝓐(ℓ/r⁴) + c₃ℓ^{2/3} + O(ℓ²ρ^{−5} + ℓ^{15/19}) + o(ℓ^{2/3}).
- *`𝒦₂`.* On `[0, ℓ^{1/4}]`, Theorem SL. On `[ℓ^{1/4}, ρ]`, `κ = ℓ/r⁴ ≥ ℓρ^{−4} = ρ^θ ≥ r^θ`, so Theorem TL⁻ applies, and its
  error integrates to at most `C∫_{ℓ^{1/4}}^ρ(ℓr^{−2} + r⁷/ℓ)dr ≤ C(ℓ^{3/4} + ρ⁸/ℓ) = O(ℓ^{3/4} + ℓ^{13/19})`. With #242 §0's
  identity, `𝒦₂ = (I^{cand} − c₁)ℓ^{1/4} − ∫_ρ^∞∫𝓐^{rej}(ℓ/r⁴) + R_{2/3}ℓ^{2/3} + o(ℓ^{2/3})`.
- *The cusp tails and `J₄`* (note TS §5). `𝒦₁ − 𝒦₂ + J₄` equals `c₂ℓ^{1/3} + c₁ℓ^{1/4} + (c₃ − R_{2/3})ℓ^{2/3}` plus
  `−∫_ρ^∞∫𝓐^{eld} + ∫_ρ^∞∫[𝓐^{con} − r^{−2}𝐀₀] + ∫_0^ρ∫𝐓_r(0) + o(ℓ^{2/3})`. Here `0 ≤ ∫_ρ^∞∫𝓐^{eld} ≤ Cℓ³ρ^{−11} = Cℓ^{13/19}`,
  the contact difference is at most `Cℓ⁴ρ^{−13} = Cℓ^{24/19}` ((5.0)), `∫_0^ρ∫𝐓_r(0) ≤ Cℓ^{16/19}log(1/ℓ)`, and the
  `O(ℓ²ρ^{−5} + ℓ^{15/19}) = O(ℓ^{15/19})` of `𝒦₁` (`ℓ²ρ^{−5} = ℓ^{18/19}`) joins them. All are `o(ℓ^{2/3})`.
- *`I^{eld}`.* On `[ρ, ℓ^{1/5}]`, note TS §5 gives at most `C(ℓ³ρ^{−11} + ℓ²ρ^{−6}log(1/ℓ)) = O(ℓ^{13/19} + ℓ^{14/19}log(1/ℓ))`.
  On `[ℓ^{1/5}, r_0^*]` the elder mass `𝔐(ℓ) := ∫_{ℓ^{1/5}}^{r_0^*}∫𝐓_r^{eld}dσ dr` is `o(ℓ^{2/3})`, shown below.

Collecting gives (C7.1). Theorem C3 minus (C7.1), with `ρ_rej = ν_cand − ν_eld`, gives (C7.2): `cℓ^{−1/3}` and `c₂ℓ^{1/3}`
cancel, and `c₃ − (c₃ − R_{2/3}) = R_{2/3}`. With #188's Theorem G at `ρ = r_0^* ≤ L/(4√2) < L/4` (note TS §1, from #220's
proof of Lemma S′), the far terms are `O(ℓ^N)`, which is (C7.3). For SIDE24 divide by `cℓ^{−1/3}`.

*`𝔐(ℓ) = o(ℓ^{2/3})`.* Fix `ρ₀ ∈ (0, r_*]`; then `ρ₀ ≤ r_0^*` (note EM §4 takes `r_* ≤ min(r_0^*, r_Q)`).
- *`[ρ₀, r_0^*]`.* #220 §0's identity `ν_eld = ∫_0^{r_0}∫∫r^{−2}A_r^{eld} + ν_eld^{far,r_0}`, at `r_0 = ρ₀` and at `r_0 = r_0^*`,
  gives `∫_{ρ₀}^{r_0^*}∫𝐓_r^{eld}dσ dr = ν_eld^{far,ρ₀}(ℓ) − ν_eld^{far,r_0^*}(ℓ) ≤ ν_eld^{far,ρ₀}(ℓ)`. That far term is #188's (0.1)
  at `ρ = ρ₀`. #220 §4 (proof of (E3.3)) identifies the far term at `r_0^*` with #187's (0.1) at `ρ = r_0^*`, by comparing the
  domain `{dist(0, y) ≥ r_0^*}`, `O_y`, `v_{b,ℓ}`, `p_y`, `Q_{y,b,ℓ}`, `W` and the mark term by term. All of these except the
  domain are defined pointwise in `y`, so the same comparison identifies the far term at `r_0 = ρ₀` with #187's (0.1) at
  `ρ = ρ₀`; and #188's (0.1) is built from the same objects (#188 §0: "as in [P] §14 and Math- #187 §0"). By #188's
  Theorem G (`ρ₀ < L/4`) it is `O(ℓ^N)`, with a constant that depends on `ρ₀`.
- *`[ℓ^{1/5}, ρ₀]`.* By (E), `𝐓_r^{eld} ≤ min(𝐓_r^{eld}, CΥ) + Cr²κ^{2/3}`, and the second part integrates to at most
  `3Cρ₀^{1/3}ℓ^{2/3}`. For the first, substitute `r = ℓ^{1/6}t` as in §2 and put `G_r(c, u) := r^{−3}𝐓_r^{eld}(cr³, u)`. Since
  `κ/r² = t^{−6}` and `r^{−3}Υ(r, κ) = Υ̃(t)` when `κ = t^{−6}r²`,

      ℓ^{−2/3}∫_{ℓ^{1/5}}^{ρ₀}∫ min(𝐓_r^{eld}, CΥ) dσ dr = ∫_{S^{d−1}}∫_{ℓ^{1/30}}^{ρ₀ℓ^{−1/6}} min( t³G_{ℓ^{1/6}t}(t^{−6}, u), Ct³Υ̃(t) ) dt dσ(u).

  For fixed `t` and `u`, Proposition G₀ with `c = t^{−6}` sends the integrand to `0` as `ℓ ↓ 0`, and `Ct³Υ̃(t)` is integrable
  on `(0, ∞)` (§2). The integrand is jointly measurable in `(t, u)`: `𝐓_r^{eld}(ℓ/r³, u)` is jointly measurable in `(r, u)`,
  as an integrand of #220 §0's identity, and `t ↦ ℓ^{1/6}t` is smooth. So by dominated convergence along every sequence
  `ℓ_n ↓ 0`, on `(0, ∞) × S^{d−1}` with `dt dσ`, the integral tends to `0`.

So `limsup ℓ^{−2/3}𝔐(ℓ) ≤ 3Cρ₀^{1/3}` for every `ρ₀`, with `C` independent of `ρ₀`, and `𝔐(ℓ) = o(ℓ^{2/3})`. ∎

## 6. Remarks

1. **A third scale.** #242 §4's matched-asymptotics count has cusp-side powers `ℓ^{(j+1)/4}` and fold-side powers
   `ℓ^{(j+1)/3}`. Theorem E is of order `r³` exactly at `κ ≍ r²`, that is `k ≍ r³` and `r ≍ ℓ^{1/6}`: in (2.1) the mass of
   `t³Υ̃(t)` sits at `t ≍ 1`. Before Proposition G₀ this scale could have carried an `ℓ^{2/3}` term of its own,
   `ℓ^{2/3}∫∫t³lim G(t^{−6}, u)dt dσ ≥ 0`, which would have broken Conjecture 7. Proposition G₀ shows it does not. Without G₀,
   §5 still gives the one-sided statement `ρ_rej + ν_eld^{far,r_0^*} ≤ B_{d,L} + (I^{cand} − c₁)ℓ^{1/4} + R_{2/3}ℓ^{2/3} + o(ℓ^{2/3})`,
   since `𝔐 ≥ 0`. That statement needs neither Proposition G₀ nor Theorem E nor #188; with Corollary E1 the other side holds
   with `O(ℓ^{2/3})`.
2. **Why Lemma X is not enough there.** Lemma X certifies `e = 0` when `s ≳ (κ/μ)^{1/2}`. At `κ ≍ r²` and `μ ≍ 1` this is
   `s ≳ r`, which is also the cap that typedness puts on `s`; so Lemma X alone cannot make the elder weight smaller than the
   typed weight there. Lemma D uses the ridge over a unit interval instead. An elder pair must keep `g_𝔉` between `−κ` and
   `0` there, and with Lemma R₂ that pins the quartic coefficient `z` to a window of width `O(κ + r²)`, against the width
   `O(r)` that typedness allows (`|z| < 72κ + 12ε̃`, note EM (4.1)).
3. **Rates.** Notes C3 and SL identify `c₃` and `R_{2/3}` by dominated convergence, without a rate, so (C7.1)–(C7.2) have
   none.
   - *The mass `𝔐`.* Taking `ε = ε(r) → 0` in §4 would give a small power rate only to the part `∫∫min(𝐓_r^{eld}, CΥ)` of `𝔐`
     on `[ℓ^{1/5}, ρ₀]`. The other two parts have none at fixed `ρ₀`: the term `r²κ^{2/3}` of (E) contributes
     `3Cρ₀^{1/3}ℓ^{2/3}`, and #188's Theorem G bounds `ν_eld^{far,ρ₀}` only at fixed `ρ₀`, with a constant that must blow up
     as `ρ₀ ↓ 0` (#188 Remark 6, conditionally). A power rate for `𝔐` would also need `ρ₀ = ℓ^β`, with a far bound at that
     moving separation, such as Theorem QSF of the C89 extension on Math-#188, which is not used here.
   - *#242's `O(ℓ^{3/4})` form of Conjecture 7* would need all of this, rates in note C3 (Lemmas F₃ and T₁) and note SL
     (#243's Theorem FL), and two further inputs. In §5's ledger the rows `ρ⁸/ℓ` (Theorem TL⁻'s `r³/κ`) and `ℓ³ρ^{−11}` (the
     elder cusp tail, and (W⁺.2) on `[ρ, ℓ^{1/5}]`) have exponents `8σ − 1` and `3 − 11σ`. No `σ` puts both at `3/4` or above
     (`9/44 < 7/32`), and their balance, at `σ = 4/19`, is `13/19`. So one input is a rejected bound sharper than `r³/κ` on
     `[ℓ^{1/4}, ρ]`, or an elder matching on `[ρ, ℓ^{1/5}]` (addendum EM.1, §3). The other is an elder bound below `r²κ^{2/3}`
     near `κ = r`: that term of (E) already integrates to `3(2^{1/3} − 1)ℓ^{11/15}` on `[ℓ^{1/5}, 2ℓ^{1/5}]`, where `κ ≍ r`, and
     `11/15 < 3/4`.
4. **`R_{2/3}` and #242's (4.2).** As in note SL's Remark 2: `R_{2/3}` here has the `b`-integral inside; when
   `v⁴(F(v^{−3}; b, u) − F₀(b, u))` is integrable in `(v, b, u)`, as for the Gaussian kernel, Fubini gives #242's (4.2).
5. **Model values (exploration, not claimed).** For the Gaussian kernel, note C3's §5 gives `c₃ ≈ 0.0128` (`d = 2`) and
   `≈ 0.0161` (`d = 3`), and #244 (with #242 §5) gives `R_{2/3} ≈ −0.0488` and `≈ −0.0614`. So `c₃ − R_{2/3} ≈ 0.062` and
   `≈ 0.077`, about `0.84c` and `1.85c` with C3's ratios `c₃/c ≈ 0.174` and `0.385`. The model value of `c₃ − R_{2/3}` is
   therefore positive (numerically; only the sign of the model `c₃` is proved, note C3's Corollary G′), and about four
   fifths of it is `−R_{2/3}`, the soft layer of the rejected density. Nothing is claimed for the torus field at `L = 24`.
6. **Corollary E1 without the rest.** Corollary E1 uses only Theorem E, note TS's (S″.2) on `[r_*, r_0^*]` (through note EM
   §5), and note LU's §5 (its decomposition and ledger, with #187's far bound) and Theorem P⁺. It does not need notes C3 or
   SL, Lemmas D and D′, Proposition G₀ or #188.

## 7. Exact controls (`c7_exact.py`; stdlib; exact rationals; deterministic; byte-identical under `-O`)

The script and its stdout are published in the next comment, with the extraction rule.
- **K1** (1.2)'s inequality `min(a + b, c + d) ≤ min(a, d) + b + c` on random nonnegative rationals; the expansion
  `μ(12κ + Ar/μ)² = 144μκ² + 24Aκr + A²r²/μ` and its bound; and (1.2)'s instance, with §1's `a, b, c, d`, on exact perfect
  powers (`r = p³`, `κ = q³ ≤ r`, so `r^{4/3}κ^{2/3} = p⁴q²`).
- **K2** (1.3): for random rationals `0 < κ ≤ r ≤ 1/10` and dyadic shells `x = x₀2^i ≤ y = 2^{j+1}`, the sum `Σ_x min(xκ, r²)`
  against `2yκ` and against `r²(2 + n₊)`, where `n₊` is the exact number of shells with `xκ > r²`; the geometric part `≤ 2r²`;
  `2^{n₊−1}r² < yκ` when `n₊ ≥ 1`; and `n₊ ≤ j + 1 + max(m, 0)`, with `2^m` the least power of `2` at or above `κ/r²`. At least
  50 of the 500 samples have `n₊ ≥ 3`.
- **K3** The substitution of §2 on exact sixth powers (`ℓ = a⁶`, rational `t`): `rκ = ℓ^{1/2}t^{−3}`, `r³ = ℓ^{1/2}t³`,
  `κ/r² = t^{−6} = (1/t)⁶` (with the log coefficient `6` as the mutable parameter), and the first entry of `r^{−3}Υ`;
  `r²κ^{2/3} = ℓ^{2/3}r^{−2/3}` on exact powers; the integral `9/8`, from exact antiderivatives of `t³(1 + 6log(1/t))` (as
  Laurent polynomials in `t` and `log t`) and of `t^{−3}`; and `y(1 + (1/y − 1)) = 1`, the identity behind
  `y(1 + log(1/y)) ≤ 1`.
- **K4** Lemma D's case analysis on a discrete model: 4000 random ridges on the grid of `[−3, 2]` with step `1/8`, with
  `g(−½) = 0`, `g(½) = −κ`, values `κ(m + ½)/K` elsewhere (so no tie with `0` or `−κ`: the discrete form of (G)), and both
  neighbours of `−½` in `(−κ, 0)`. The escape rule (ii) and the trap rule (iii) are applied on the grid as in §3. Whenever
  neither fires, the ridge lies in `[−κ, 0]` at every grid point of `[−½, ½]` or at every grid point of `[−3, −½]`. Each of
  the four outcomes (escape, trap, first alternative, second alternative only) occurs at least 25 times. And one tie
  witness (`κ = 1`; `g(0) = −1`, a local minimum at the level of `S`; `g(1/8) = ½`; `g = −½` at the other grid points of
  `(−½, 2]` and at `−5/8`; `g = −2` left of `−5/8`), for which neither rule fires and both alternatives fail: the
  configuration that (G) excludes.
- **K5** The window of §4 (c): exact values `(X² − ¼)² = 1/16, 9/16` and `2(X + ½)²(X − 1) = −½, −1` at `X = 0, −1`;
  `X(X² − ¼)² = −9/16` at `X = −1`; the identity `κ[2(X + ½)²(X − 1) + 3φ(X² − ¼)²] = 2κ(X + ½)²(X − 1) + (z/24)(X² − ¼)²` with
  `φ = z/(72κ)`; the cusp ridge's pin values `g(−½) = 0`, `g(½) = −κ`, `g′(±½) = 0`; on random rationals, that a ridge value
  in `[−κ, 0]` at `X = 0` or `X = −1` (with an error `|δ| ≤ ε₂′`) puts `z` in the stated interval; the endpoints of both
  intervals, attained at `δ = ∓ε₂′`; and `384 + 128/3 = 1280/3 ≤ 427`.
- **K6** Proposition G₀ at `κ = cr²`: the exponents `7/2`, `11/3` and `4`, each above `3`, and the surviving `εcr³`; and,
  exactly on `r = s²` with `cr ≤ 1`, `k = cr³ ≤ r²`, `κ ≤ r`, `(κ + r)r^{5/2} ≤ 2r^{7/2}` and `r²(κ + r²) = (c + 1)r⁴`.
- **K7** The ledgers, each row derived from its integrand (a monomial in `κ = ℓr^{−4}`, `k = ℓr^{−3}` and `r`, integrated over
  `[0, ρ]`, `[ρ, ∞)` or `[ℓ^{1/4}, ∞)`). At `σ = 4/19` the nine integrands of §5 give `15/19` (twice), `3/4`, `13/19`, `13/19`,
  `24/19`, `16/19`, `18/19` and `14/19`, all above `2/3` and equal to the stated values; `θ = 3/4`, `1 − 4σ = (3/4)σ`,
  `1/5 < σ < 1/4`, `5/24 < σ < 7/33`, `8σ − 1 = 3 − 11σ = 13/19`, and `9/44 < 7/32`. At `σ = 5/24` (Corollary E1) note LU's
  ledger with the new row reproduces LU's stated exponents, its least exponent is `2/3`, attained only by rows without a
  logarithm, and the two rows with a logarithm sit at `3/4` and `5/6`.

Mutants, each rejected with exit 1, empty stdout and `FAILED: <group>` on stderr. Invalid arguments exit 2 with the usage
line.

| Mutant | Change | Fails at |
|---|---|---|
| M1 | (1.2)'s inequality without the term `c` | `K1_minsum` |
| M2 | (1.3) without the count `n₊` (the bound `2r²`) | `K2_shells` |
| M3 | `Υ̃`'s log coefficient `6 → 5` (rejected first by `κ/r² = (1/t)⁶`; the integral check alone also rejects it, `17/16 ≠ 9/8`) | `K3_integral` |
| M4 | the trap rule (iii) dropped from Lemma D's case analysis | `K4_dichotomy` |
| M5 | the window constant `384 → 192` (as if `(X² − ¼)² = 1/8` at `X = 0`) | `K5_window` |
| M6 | the bad region's exponent `7/2 → 3` | `K6_scale` |
| M7 | `σ = 5/24` in §5 (the row `ρ⁸/ℓ` at exactly `2/3`) | `K7_ledger` |
| M8 | K4's ridges with ties at `0` and `−κ` allowed, that is, (G) dropped | `K4_dichotomy` |

**What the controls do not test.** Note EM's estimates (4.1)–(4.6), (V.3) and the layers; Lemma B; Lemma Q′, Step Q3 and
Lemma R₂ of [N]; Lemma D′'s nondegeneracy and Bulinskaya argument; #220's (F3), (F4) and (2.1); notes TS, LU, C3 and SL;
#188 and the far-term identification; and dominated convergence. K4 tests the conclusion of Lemma D on piecewise-linear
ridges without ties, given rules (ii) and (iii); its tie witness and M8 show that (G) cannot be dropped from the case
analysis. It does not test the window facts.

## 8. Review slices

- **A: §§0–2.** The statements; Theorem E (the cap (1.1), (1.2)–(1.4), (E′), the bad region); Corollary E1 (the substitution,
  (2.1), note LU's ledger). Controls K1–K3 and K7's `σ = 5/24` part; mutants M1–M3.
- **B: §§3–4.** Lemma D (the window facts, escape, trap and the three cases); Lemma D′; Proposition G₀ (the three parts, the
  weight, the window with Lemma R₂, and the probability with #220's (F3), (F4) and (2.1)). Controls K4–K6; mutants M4–M6
  and M8.
- **C: §§5–6 and the header.** Theorem C7 (the decomposition at `σ = 4/19`, the inputs from notes C3, SL, LU and TS, the cusp
  tails, `I^{eld}`, `𝔐` with #220 §0's identity, #188 and dominated convergence), the remarks, and the header for
  overclaim. Control K7; mutant M7.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
_Generated by [Claude Code](https://claude.ai/code)_