# Lifetime note SL: the rejected density's `ℓ^{2/3}` term on the soft layer `κ ≥ 1`, and the matching `F → F₀`

Object: `CL-SL-SOFT-LAYER-TWO-THIRDS-20261007-v1`. Claim: main#229 6028351320.
Author: Anthropic Claude (claude.ai session `session_01NMeKEismAyeqgdB4sy2NJU`), 7 October 2026, for Dylan Roy (delegated AI
work). The same session wrote [K], #188, #242, #243, #244 and notes TL and C3. The consumed packets in turn consume
OpenAI-authored sources, among them [R] and [P].
Disposition: AUTHOR-SIDE PROOF CANDIDATE; NONAUTHOR REVIEW REQUIRED. Scientific effect: NONE — no register, graph, STATUS,
PROOF_INDEX, prize or Boolean change; no numerical constant is certified. Same GitHub account as every lane;
organizational independence 0. Before posting, a clean-context Claude subagent of this session refereed the draft. It
returned AMEND with no blocking finding: one misattributed source, one mis-cited passage, one overclaim in the header, and
nits, among them a simpler domination that makes ordinary dominated convergence suffice. Every finding is applied here,
and the controls comment lists them. This is an author-side read and earns no review credit.

**What is new.**
- **Lemma SL₀ (the fold limit after birth integration)** (§1). For every `k > 0` and `u`,
  `κ𝐓_r^{rej}(k, u) → ℱ(k, u) := ∫_RF(k; b, u)db` as `r ↓ 0`, with `κ = k/r`; and `0 ≤ ℱ(k, u) ≤ Ce^{−ck²}(1 + k)^N`. Note TL's
  Remark 2 records this limit as a remark from cited results. Here it is a lemma with its proof.
- **Corollary SL₁ (the matching `F → F₀`, after birth integration)** (§1). For `0 < k ≤ 1` and every `u`,
  `|ℱ(k, u) − ℱ₀(u)| ≤ Ck²`, where `ℱ₀(u) := ∫_RF₀(b, u)db`. So, for the torus field, the fold-scale limit of #243 and the
  cusp-scale limit of #242 Theorem 1 agree in the overlap `k → 0`, at rate `k²`, after the birth height is integrated
  out. #242's Proposition 4 had the matching only for the Gaussian kernel on `R^d`, pointwise in `b`, as #243's *Matching*
  records.
- **Theorem SL (the soft layer to `o(ℓ^{2/3})`)** (§1). In every `d ≥ 2` and for every `L`, as `ℓ ↓ 0`,

      ∫_0^{ℓ^{1/4}}∫_{S^{d−1}} 𝐓_r^{rej}(ℓ/r³, u) dσ(u) dr = ℓ^{1/4}∫_0^1∫_{S^{d−1}} 𝓐^{rej}(s^{−4}, u) dσ(u) ds + R_{2/3} ℓ^{2/3} + o(ℓ^{2/3}),
      R_{2/3} := ∫_{S^{d−1}}∫_0^∞ v⁴ (ℱ(v^{−3}, u) − ℱ₀(u)) dv dσ(u),

  with the `v`-integral absolutely convergent.
  - This identifies the `O(ℓ^{2/3})` of note TL's Corollary TL1.
  - It is the integrated content of #242's input (i) (§4 there), in its `o(ℓ^{2/3})` form: the contribution of the
    separations `κ ≥ 1`, not a two-scale approximation of the kernel. On those separations the actual rejected kernel
    contributes, up to `o(ℓ^{2/3})`, the two terms that #242's Lemma 5 gives its composite there when Lemma 5's hypothesis on
    `H` holds: the cusp part `ℓ^{1/4}∫_0^1∫𝓐^{rej}` and `R_{2/3}ℓ^{2/3}`, with `R_{2/3}` as in (SL).
  - The proof is dominated convergence in the fold variable, as in note C3. Note TL's Theorem TL and the two bounds of its
    §5 dominate, Lemma SL₀ and #242 Theorem 1 give the pointwise limit, and Corollary SL₁ gives the integrability of the
    limit.

**Not claimed.**
- No rate: the remainder is `o(ℓ^{2/3})`. #242's `O(ℓ^{3/4})` form of input (i) would need #243's limit with a rate. #243
  gives none (its *What is not claimed*: Theorem FL is a limit without rate), and its §6 (the item on #242 Conjecture 7)
  records that a rate needs quantitative margins in Proposition FL.4.
- Input (ii) of #242 §4, the separations with `κ ≤ 1`, is untouched. So #242's Conjecture 7 stays open, also in its
  `o(ℓ^{2/3})` form (Remark 1).
- Nothing pointwise in `b`. `R_{2/3}` is defined with the `b`-integral inside; it equals #242's (4.2) when
  `v⁴(F(v^{−3}; b, u) − F₀(b, u))` is integrable in `(v, b, u)`, as for the Gaussian kernel (Remark 2).
- No value of `R_{2/3}` for the torus field. The model values of #244 are for the Gaussian kernel's jet law, and the transfer of
  `F` (or `H`) to the torus field is not proved here (as in note TL's Remark 2).
- No certified number; no uniformity in `d` or `L`; nothing beyond the existential scope of the consumed sources.

**Consumed.**
- Note TL (main#229 6017975404; read in every slice: Slices A–B PASS 6018510549, Slice C PASS 6018013576, Slice D PASS
  6018770333): §0 ((0.1), (0.2), the constants); Theorem TL (TL); §5's two bounds (`0 ≤ 𝐓_r^{rej} ≤ C/κ` from [K] (K2) with
  [R] (R5), in the pointwise form `r^{−2}A_r^{rej} ≤ Cπ_r(v_r)(r/k)P^N`; `0 ≤ 𝓐^{rej} ≤ C/κ`).
- #242 `frontiers/soft_rejected_pairs_20261002/PROOF.md` (blob `271412db`): §0 (with (0.2), (G2), and the identity
  `I^{cand} − c₁ = ∫_0^∞∫∫𝒜^{rej}(b, s^{−4}, u)db dσ ds`); (3.1), the definition of `F`; Theorem 1 (1.0) and the definition
  of `F₀`.
- #243 `frontiers/soft_fold_limit_20261002/PROOF.md` (blob `6502cf7b`): Theorem FL ((0.0) for every `d ≥ 2`, `L`, `b`, `k > 0`
  and `u`).
- [K] `frontiers/c7_total_bounded_20260929/PROOF.md` (blob `28748b08`), (K2), through note TL; [R]
  `frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md` (blob `247b3ecf`), (R5).

**Cited only.** #242's §4 (inputs (i)–(iii)), Lemma 5 (for comparison), Conjecture 7 and Proposition 4; #244 (`R_{2/3}` for
the Gaussian kernel, numerically); #243's *Matching*, Corollary FL.6 and its Remark 2 (with #170 §9 and #175 §7: the
compact-window coefficient), and its §6; note C3 (main#229 6027862273, read in every slice; its Remark 3 and the coefficient
`c₃`); #188 `frontiers/far_elder_flat_ridge_20260930/PROOF.md` (blob `0b089b89`; merged on Math- 4 October at `f7f083ec`,
an author-side candidate; the far elder density `O(ℓ^N)`); notes TS, EM, EM.1 and LU (the separations with `κ ≤ 1`); the
planar chain C91–C127 (fixed or compact gap).

**Prior work and overlap.** Before drafting I searched main#229 (every comment since 3 October), the Math- tree at
`34618d0d` (for `R_{2/3}`, Conjecture 7 and the soft layer) and the project archive.
- Note TL's Remark 2 states the birth-integrated fold limit (here Lemma SL₀) as a remark from cited results, and says that
  the `k²/κ` part of (TL) carries `R_{2/3}`. It does not identify that term.
- #243 explains why the unrestricted coefficient needs the two-scale composite (Remark 2 after its Corollary FL.6, and
  *Matching*), and records that the matching `F(k) → F₀` was proved only for the Gaussian kernel.
- #243's Corollary FL.6, which is #170 §9 and #175 §7, gives the coefficient on compact gap windows `𝐊 ⊂ (0, ∞)`. The
  planar chain C91–C127 works at fixed or compact gap.
- No packet, note or claim identifies the unrestricted soft-layer coefficient, or proves the matching for the torus field.

## 0. Setting and statements

Setting and notation are note TL's §0, which are [N] §0, #237 §§0–1 and #242 §0: `d ≥ 2`, `m = d − 1`, `L > 0`, the [P] field
on `R^d/(LZ^d)`, the pins `M = −ru/2` and `S = ru/2` at gap `k`, `κ := k/r` and `ℓ = kr³ = κr⁴`. In particular:
- `𝐓_r^{rej}(k, u) := ∫_R r^{−2}A_r^{rej}(b, k, u)db` is the birth-integrated rejected kernel (TL (0.1)), and
  `𝓐^{rej}(κ, u) := ∫_R𝒜^{rej}(b, κ, u)db` its cusp limit (TL (0.2));
- `F(k; b, u)` is #242's fold-scale rejection rate (#242 (3.1)), and #243's Theorem FL proves
  `lim_{r↓0}(k/r)·r^{−2}A_r^{rej}(b, k, u) = F(k; b, u)` for every `b`, `k > 0` and `u`;
- `F₀(b, u) = (5/24)π₀(u; v₀(b, 0))𝔇(b, u)` is #242's cusp-scale limit (#242 (1.0)), with `κ𝒜^{rej}(b, κ, u) → F₀(b, u)`.

Constants `C, c, N` depend only on `d` and `L`. Put (`ℱ` is not #242's window map `Φ`, nor note TL's local `Φ` and `F`)

    ℱ(k, u) := ∫_R F(k; b, u) db,        ℱ₀(u) := ∫_R F₀(b, u) db.                                                        (0.1)

**Lemma SL₀ (the fold limit after birth integration).** For every `k > 0` and `u ∈ S^{d−1}`,
`lim_{r↓0} κ𝐓_r^{rej}(k, u) = ℱ(k, u)`, with `κ = k/r`. Moreover `0 ≤ ℱ(k, u) ≤ Ce^{−ck²}(1 + k)^N` for all `k > 0`, and
`0 ≤ ℱ₀(u) ≤ C`.

**Corollary SL₁ (the matching).** For `0 < k ≤ 1` and `u ∈ S^{d−1}`,

    |ℱ(k, u) − ℱ₀(u)| ≤ C k².                                                                                         (SL₁)

**Theorem SL (the soft layer to `o(ℓ^{2/3})`).** In every `d ≥ 2` and for every `L`, as `ℓ ↓ 0`,

    ∫_0^{ℓ^{1/4}}∫_{S^{d−1}} 𝐓_r^{rej}(ℓ/r³, u) dσ(u) dr = ℓ^{1/4}∫_0^1∫_{S^{d−1}} 𝓐^{rej}(s^{−4}, u) dσ(u) ds + R_{2/3} ℓ^{2/3} + o(ℓ^{2/3}),
    R_{2/3} := ∫_{S^{d−1}}∫_0^∞ v⁴ (ℱ(v^{−3}, u) − ℱ₀(u)) dv dσ(u).                                                     (SL)

The integrand of `R_{2/3}` is bounded by `C min(1, v^{−2})`, so the integral converges absolutely.

## 1. Proofs

*Proof of Lemma SL₀.* Fix `k > 0` and `u`. For `r ≤ min(k, r₀)`, note TL §5 (from [K] (K2), the cap event and [R] (R5)) gives
`0 ≤ r^{−2}A_r^{rej}(b, k, u) ≤ Cπ_r(v_r)(r/k)P^N` with `π_r(v_r) ≤ Ce^{−c(b²+k²)}` and `P = 1 + |b| + k`. Hence

    0 ≤ (k/r)·r^{−2}A_r^{rej}(b, k, u) ≤ C e^{−c(b² + k²)} (1 + |b| + k)^N,                                              (1.1)

a function of `b` that is integrable and does not depend on `r`. By #243 Theorem FL the left side tends to `F(k; b, u)` for
every `b`. Dominated convergence in `b` gives `κ𝐓_r^{rej}(k, u) = ∫(k/r)r^{−2}A_r^{rej}db → ∫F(k; b, u)db = ℱ(k, u)`. Letting
`r ↓ 0` in (1.1) gives `0 ≤ F(k; b, u) ≤ Ce^{−c(b²+k²)}(1 + |b| + k)^N`, and integrating in `b` gives the bound on `ℱ`.
Finally `F₀ ≥ 0`, and by #242 Theorem 1 integrated in `b` (as in note TL §5),
`|κ𝓐^{rej}(κ, u) − ℱ₀(u)| ≤ ∫Cκ^{−1}(1 + |b|)^Ne^{−cb²}db ≤ C/κ` for `κ ≥ 1`. At `κ = 1`, #242 (0.2) gives
`0 ≤ 𝒜^{rej}(b, 1, u) ≤ 432π₀(u; v₀(b, 0))E₀[Δ² | b] ≤ C(1 + |b|)^Ne^{−cb²}` ((G2) of #242 §0 and [R] (R5)), so
`𝓐^{rej}(1, u) ≤ C` and `ℱ₀(u) ≤ 𝓐^{rej}(1, u) + C ≤ C`. ∎

*Proof of Corollary SL₁.* Fix `0 < k ≤ 1` and `u`. For `r ≤ min(k, r₀)`, `κ = k/r ≥ 1` and `k = κr ≤ 1`, so (TL) applies:
`|𝐓_r^{rej}(k, u) − 𝓐^{rej}(κ, u)| ≤ Cr²(1 + κ)`. Multiply by `κ`. Since `κr² = rk` and `κ²r² = k²`,

    |κ𝐓_r^{rej}(k, u) − κ𝓐^{rej}(κ, u)| ≤ C(rk + k²).                                                                 (1.2)

Let `r ↓ 0` at fixed `k`: then `κ → ∞`. The first term tends to `ℱ(k, u)` (Lemma SL₀), and the second to `ℱ₀(u)`, since
`|κ𝓐^{rej}(κ, u) − ℱ₀(u)| ≤ C/κ`. The right side tends to `Ck²`. ∎

*Proof of Theorem SL.* Put `D_r(k, u) := 𝐓_r^{rej}(k, u) − 𝓐^{rej}(k/r, u)` and split the left side of (SL) as

    ∫_0^{ℓ^{1/4}}∫𝓐^{rej}(ℓ/r⁴, u) dσ dr + ∫_0^{ℓ^{1/4}}∫D_r(ℓ/r³, u) dσ dr.                                         (1.3)

Both terms are finite, since `𝐓_r^{rej}` and `𝓐^{rej}` are at most `C/κ` on `κ ≥ 1`.
- *The cusp part.* With `r = ℓ^{1/4}s`, `ℓ/r⁴ = s^{−4}` and `dr = ℓ^{1/4}ds`, so the first term of (1.3) is exactly
  `ℓ^{1/4}∫_0^1∫𝓐^{rej}(s^{−4}, u)dσ ds`.
- *The fold variable.* In the second term put `r = ℓ^{1/3}v`. Then `k = ℓ/r³ = v^{−3}`, `κ = k/r = ℓ^{−1/3}v^{−4}`, and
  `r ≤ ℓ^{1/4}` if and only if `v ≤ ℓ^{−1/12}`, if and only if `κ ≥ 1`. With `ψ_ℓ(v, u) := v·D_r(k, u)/r` at these values,

      ∫_0^{ℓ^{1/4}}∫D_r(ℓ/r³, u) dσ dr = ℓ^{2/3} ∫_0^{ℓ^{−1/12}}∫ ψ_ℓ(v, u) dσ dv.                                       (1.4)

- *The pointwise limit.* Fix `v > 0` and `u`, so `k = v^{−3}` is fixed, and let `ℓ ↓ 0`. Then `r ↓ 0` and `κ → ∞`, and
  `D_r(k, u)/r = (1/k)·κD_r(k, u) = (1/k)[κ𝐓_r^{rej}(k, u) − κ𝓐^{rej}(κ, u)] → (1/k)(ℱ(k, u) − ℱ₀(u))` by Lemma SL₀ and
  #242 Theorem 1. So `ψ_ℓ(v, u)1{v ≤ ℓ^{−1/12}} → v⁴(ℱ(v^{−3}, u) − ℱ₀(u))`.
- *Domination*, on `v ≤ ℓ^{−1/12}` (so `κ ≥ 1`, that is `r ≤ k`), for `ℓ` so small that `ℓ^{1/4} ≤ r₀`:
  - for `v ≤ 1` (`k ≥ 1`), the two bounds of note TL §5 (the first needs `r ≤ min(k, r₀)`, the second `κ ≥ 1`; both hold)
    give `|D_r| ≤ 2C/κ`, so `|ψ_ℓ| ≤ 2Cv/(κr) = 2Cv/k = 2Cv⁴ ≤ 2C`;
  - for `1 ≤ v ≤ ℓ^{−1/12}` (`k ≤ 1 ≤ κ`), (TL) gives `|D_r| ≤ C(r² + rk) ≤ 2Crk`, since `r ≤ k`, so `|ψ_ℓ| ≤ 2Cvk = 2Cv^{−2}`.

  So `|ψ_ℓ(v, u)1{v ≤ ℓ^{−1/12}}| ≤ g(v) := 2C1{v ≤ 1} + 2Cv^{−2}1{v ≥ 1}`, which is integrable on `(0, ∞)` and does not depend
  on `ℓ` or `u`.
- *Conclusion.* The integrands are jointly measurable in `(r, u)` (as in note TL's Corollary TL1), so `ψ_ℓ` is measurable in
  `(v, u)`. By dominated convergence along every sequence `ℓ_n ↓ 0`, on `(0, ∞) × S^{d−1}` with the finite measure `dσ`, the
  double integral in (1.4) tends to `R_{2/3}`. The limit inherits the bound `g`: `|v⁴(ℱ(v^{−3}, u) − ℱ₀(u))| ≤ 2C` for `v ≤ 1`
  and `≤ 2Cv^{−2}` for `v ≥ 1` (also from Lemma SL₀ and from (SL₁) with `k = v^{−3}`). This is (SL). ∎

## 2. Remarks

1. **What remains of Conjecture 7.** #242's Conjecture 7 with `o(ℓ^{2/3})` in place of `O(ℓ^{3/4})`, and with `R_{2/3}` as in
   (SL) (which is #242's (4.2) whenever the latter converges absolutely), reads
   `ρ_rej + ν_eld^{far,r_0^*} = B_{d,L} + (I^{cand} − c₁)ℓ^{1/4} + R_{2/3}ℓ^{2/3} + o(ℓ^{2/3})`. By #242 §0,
   `I^{cand} − c₁ = ∫_0^∞∫𝓐^{rej}(s^{−4}, u)dσ ds`. Theorem SL accounts for the separations with `κ ≥ 1` (`r ≤ ℓ^{1/4}`) and for
   the part `s ≤ 1` of this integral. So that form of Conjecture 7 is equivalent to its `κ ≤ 1` half: the rejected pairs with
   `r ≥ ℓ^{1/4}`, together with the far pairs, must contribute `B_{d,L} + ℓ^{1/4}∫_1^∞∫𝓐^{rej}(s^{−4}, u)dσ ds + o(ℓ^{2/3})` to
   `ρ_rej + ν_eld^{far,r_0^*}`. That is #242's input (ii). The far elder term is `O(ℓ^N)` by #188 (merged; an author-side
   candidate), so it may be dropped. With note C3's Remark 3, the same statement would give the near elder density's
   `ℓ^{2/3}` coefficient `c₃ − R_{2/3}`.
2. **The Gaussian kernel.** For the model case `C(z) = e^{−|z|²/2}` on `R^d`, #242 Proposition 4 gives `F = F₀H(k)` with
   `|H(k) − 1| ≤ C min(1, k²)`. Then `v⁴(F − F₀)` is integrable in `(v, b, u)`, so Fubini turns `R_{2/3}` into #242's (4.2),
   `(∫∫F₀ db dσ)·Ĩ` with `Ĩ = ∫_0^∞v⁴(H(v^{−3}) − 1)dv`. #244's closed form gives `R_{2/3} ≈ −0.048779` (`d = 2`) and
   `≈ −0.061375` (`d = 3`) for the model's jet law (exploration). As in note C3, Theorem SL itself is stated for the torus
   field, and the transfer of these values to it is not proved here.
3. **The matching in the model.** In the model, `H(k) = 1 + (12/25)k² + O(k³)` (#242 Proposition 4), so `ℱ − ℱ₀` is of
   exact order `k²` there. (SL₁) has the same order, for the torus field, from (TL): the `k²/κ` part of (TL) is exactly what
   (1.2) turns into `Ck²`.
4. **Why `o(ℓ^{2/3})`.** Theorem SL uses #243's limit only pointwise in `k`, and (TL) only as a dominating function. #242's
   `O(ℓ^{3/4})` form of input (i) would follow from that limit with a rate `O(r^{1/4})` (with integrable weights in `k`)
   uniformly over the soft layer, since `r = ℓ^{1/3}v` turns `r^{1/4}` into `ℓ^{1/12}v^{1/4}`; #243's argument gives no rate
   (its *What is not claimed*).
5. **Consistency.** On a compact gap window `k ∈ 𝐊 ⊂ (0, ∞)`, the same computation without the subtraction of `𝓐^{rej}`
   reproduces, after birth integration, the form of #243's Corollary FL.6: the coefficient `(1/3)∫_𝐊k^{−8/3}ℱ(k, u)dk` per
   direction, since `r = ℓ^{1/3}v` and `v⁴dv = (1/3)k^{−8/3}dk` there. Theorem SL removes the window, at the price of
   subtracting the cusp limit.

## 3. Exact controls (`sl_exact.py`; stdlib; exact rationals; deterministic; byte-identical under `-O`)

The script and its stdout are published in the next comment, with the extraction rule.
- **S1** The substitutions, on exact perfect powers `ℓ = t^{12}`: `r = ℓ^{1/4}s` gives `ℓ/r⁴ = s^{−4}`; `r = ℓ^{1/3}v` gives
  `k = v^{−3}` and `κ = ℓ^{−1/3}v^{−4}`; `r ≤ ℓ^{1/4} ⟺ v ≤ ℓ^{−1/12} ⟺ κ ≥ 1`; and `v ≤ 1 ⟺ k ≥ 1`.
- **S2** The identities behind (1.2) and (1.4): `κr² = rk`, `κ²r² = k²`, `D/r = (1/k)κD`, the Jacobian `ℓ^{1/3}·ℓ^{1/3} = ℓ^{2/3}`,
  and the weight `v·(1/k) = v⁴`.
- **S3** The domination on the soft layer `v ≤ ℓ^{−1/12}`: on `v ≤ 1`, `2v/(κr) = 2v⁴ ≤ 2`; on `1 ≤ v`, `r ≤ k` and
  `v(r² + rk)/r ≤ 2vk = 2v^{−2}`.
- **S4** The exponents of the limit's bound, `4` at `v → 0` and `4 − 6 = −2` at `v → ∞` (the `−2` of `g`), and the identity
  `κr²(1 + κ) = rk + k²` behind (1.2) (its `r → 0` limit, which gives (SL₁), is not tested).

Mutants, each rejected with exit 1, empty stdout and `FAILED: <group>` on stderr:

| Mutant | Change | Fails at |
|---|---|---|
| M1 | the fold variable `r = ℓ^{1/4}v` in place of `ℓ^{1/3}v` | `S1_substitution` |
| M2 | the Jacobian `ℓ^{1/3}` in place of `ℓ^{2/3}` | `S2_identities` |
| M3 | the domination tested beyond the soft layer (`v` up to `2ℓ^{−1/12}`, where `r > k`) | `S3_domination` |
| M4 | the weight `v³` in place of `v⁴` (the exponent at `v → ∞` becomes `−3`, not the `−2` of `g`; `v³` would still be integrable) | `S4_integrability` |

**What the controls do not test.** Theorem TL, the bounds of note TL §5, #243's Theorem FL, #242's Theorem 1, dominated
convergence, and any numerical value.

## 4. Review slices

- **A: §§0–1.** The statements, Lemma SL₀, Corollary SL₁ and Theorem SL, against note TL, #242 and #243. Controls S1–S4,
  mutants M1–M4.
- **B: §2 and the header.** The remarks, the consumed and cited sources, and the header for overclaim.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
_Generated by [Claude Code](https://claude.ai/code)_