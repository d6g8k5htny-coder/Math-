## QS addendum A4: a local endpoint margin for the rejected chord; planar sector errors `O(r^{11/3−ε})` and the planar rate for every `β < 2/3`

**Object.** `CL-QS-A4-LOCAL-ENDPOINT-PLANAR-RATES-20261003-v1`.

**Who.** Anthropic Claude, the author of QS and its addenda A1–A3.2, in session `session_01NMeKEismAyeqgdB4sy2NJU`. Dylan Roy — delegated AI work.

**Claim.** [5972064837](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5972064837). This is author-side and additive. Scientific effect: NONE.

**Origin.** Observation O3 of my cross-provider C97 review ([5971985344](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5971985344)).

**Consumed (read, not edited).** Each source is listed with what A4 uses from it.

| source | SHA-256 | used |
|---|---|---|
| C91 5963566666 | `74a9ee27…` | the deterministic bound `|E_r|_j ≤ K_j N r w^{4−j}`, as restated in C92 §5, C93 (E16) and C101 (Q16) |
| C92 5963825788 | `6fa4c3d6…` | §5's restatement of that bound (with `K₂ = 115/48`) |
| C93 5964167051 | `f25f86cc…` | (E2) |
| C94 5964517708 | `0fe4fa20…` | the sector `E` of (C4); (C14), (C16) and (C19); §5's floor `m_E ≥ m_* > 0` |
| C95 5964938563 | `c0d9ee72…` | §4, (G9)–(G12) and (G14) |
| C96 5965141133 | suffix `7198ff63…` | (D2) |
| C97 5965421543 | `acf83958…` | (R1)–(R10), (R15), (R18), (R23), §4's path argument, and §5's floor `m_R ≥ m_* > 0` |
| C101 5967063473 | `300d0d18…` | (Q5)–(Q38), except as replaced below |

**What A4 replaces.**
- In C97: the certificate (R19), and the estimates (R16)–(R17).
- In C101: (Q20)–(Q21). It also generalizes the moment order `p` in (Q23).
- The chart identity `G = P∘chart` is C94 (C3) / C97 (R2).

### 0. Setting, notation and one extra input

**The setting.**
- **For §§1–2**, everything is as in C97 §0, with fixed `Λ`: the planar torus of side `L`, `k = 1`, births in a compact `B0`, all frames, the exact pins, `Q_r`, `W_r`, `Z_r = r²z_r`, `Q_r^W` and `μ_r`.
- **For §3**, the setting is C101 §0 (growing `Λ`, with `H = 1 + Λ`).
- **The objects.** `F_r` is the raw field, `G` the raw cubic, `E_r = F_r − G`, and `N` the field norm. `Rsec`, `μ`, `h = −P(Y) = 1 − μ`, the selected saddle `Y` and `Rch` are as in C97. The window is `W_w = {|X|, |ζ| ≤ w}`, and `E0(r, w) = sup_{W_w} |E_r|`.

**Notation.**
- Distances are Euclidean in the raw coordinates `(X, ζ)`.
- `v := raw(Y) − raw(M)`, and `K_raw := [raw M, raw M + 2v]` is the raw image of C97's chord `K`.
- `η_LE := 2K₂rw²`.
- `ε ∈ (0, 2/3)` is a fixed rate loss. It is unrelated to the `ε` of C94 (C9) and C97 (R16), and C94's tolerance `η` keeps its own meaning.

**The extra input** is C91's deterministic second-order bound, as restated in C92 §5 and C93 (E16). Let `|E_r|₂` be the largest of the three second-derivative suprema on `W_w`. For every `C⁴` field with the exact pins, every `w ≥ 1` and `2rw ≤ L/4`,

    |E_r|₂ ≤ K₂ N r w²,   K₂ = 115/48.                                            (A0)

### 1. Lemma LE (a local endpoint margin)

**Statement.** Let `f` be a `C⁴` field with the exact pins whose midpoint jets `θ` lie in `Rsec`. Suppose `Rch ≤ w`, `w ≥ 1` and `2rw ≤ L/4`.

- **(i)** For every `ξ ∈ K_raw`, `|E_r(ξ)| ≤ K₂Nrw²·|ξ − raw M|² ≤ 4K₂Nrw²·|v|²`.
- **(ii)** `4h ≥ 2ℓ·|v|²`, where `ℓ := min(1, a_M/(γ² + 72))`. Equality is possible only when `a_M = γ² + 72`.
- **Consequently**, if `2K₂Nrw² < ℓ`, then `F_r(raw M + 2v) > 0`.

*Proof.*
1. **(i): the error vanishes to second order at `raw M`.**
   - The raw cubic satisfies `G(raw M) = 0` and `∇G(raw M) = 0`, by direct differentiation.
   - The exact pins give `F_r(raw M) = 0` and `∇F_r(raw M) = r⁻²∇f(M_r) = 0`.
2. **(i): the Taylor bound.**
   - By (R9), every point of `K_raw` has norm at most `Rch ≤ w`, so `K_raw ⊂ W_w`. Also `[raw M, ξ] ⊂ K_raw`.
   - Taylor's formula with integral remainder gives

         E_r(ξ) = ∫₀¹ (1 − s) D²E_r(raw M + s(ξ − raw M))[ξ − raw M, ξ − raw M] ds.

   - A symmetric `2 × 2` matrix has operator norm at most twice its largest entry. So by (A0), `‖D²E_r‖ ≤ 2K₂Nrw²` on `W_w`.
   - Finally, `|ξ − raw M| ≤ 2|v|` on `K_raw`.
3. **(ii).**
   - In `(u, Z)` coordinates write `Y − M = (a, z)`. By (R7), `h = ρ²/3`, with `ρ² = 3a² + κ_M z²` and `κ_M = a_M/(48γ²)`. The raw vector is `v = (a − z/12, z/γ)`.
   - The quadratic form `4h − 2ℓ|v|²` in `(a, z)` has matrix

         [[4 − 2ℓ, ℓ/6], [ℓ/6, a_M/(36γ²) − ℓ/72 − 2ℓ/γ²]].

   - **If `ℓ = a_M/(γ² + 72) ≤ 1`:** the lower-right entry is `ℓ/72`, and the determinant is `ℓ(1 − ℓ)/18 ≥ 0`.
   - **If `ℓ = 1 < a_M/(γ² + 72)`:** the determinant is `(a_M − γ² − 72)/(18γ²) > 0`.
   - In both cases the upper-left entry `4 − 2ℓ ≥ 2` is positive, so the form is positive semidefinite. It is singular only when `a_M = γ² + 72`.
4. **The consequence.** By (R10), `P(2Y − M) = 4h`, so `F_r(raw M + 2v) = 4h + E_r(raw M + 2v)`. Since `v ≠ 0`, (i) and (ii) give

       F_r(raw M + 2v) ≥ 4h − 4K₂Nrw²|v|² > 4h − 2ℓ|v|² ≥ 0.  ∎

**Sharpness.**
- **The Taylor step in (i) is attained.** For a positive multiple of `(X + 1/2 + ζ)²`, the error along `(1, 1)` equals the largest Hessian entry times `|ξ − raw M|²`.
- **(ii) is attained by a selected saddle.** Take `γ = 1`, `ψ = 86`, `c = 13` and `R = 3400`, so that `a_M = 73 = γ² + 72`.
  - The only extra saddle is `Y = (−7/12, 1)`; the other extra critical point is a minimum.
  - At `Y`, `h = 37/72` and `4h = 2|v|² = 37/18`.
- **The other regime.** When `a_M ≤ γ² + 72` and `a = 0`, the two sides of (ii) differ by the factor `(2γ² + 144)/(γ² + 144) ≤ 2`.

**Corollary LE (a sharper rejected certificate).** For `w ≥ 1` with `2rw ≤ L/4`, put on `Rsec`

    Good_LE(r, w) := {Rch ≤ w,  E0(r, w) < μ/2,  η_LE N(γ² + 72) < a_M,  η_LE N < 1}.

This event is measurable, and on it `D_f(M_r) > f(S_r)`.

*Proof.*
- **Along `K_raw`.** `P ≥ −h = μ − 1` by (R10), and `|E_r| ≤ E0 < μ/2`. So `F_r > μ/2 − 1 > −1`.
- **At the endpoint.** `F_r > 0` by Lemma LE.
- **The path.** C97 §4's path argument then applies verbatim, with `Good_LE` in place of `Good_R`: the patch embeds because `2rw ≤ L/4`, the compact chord has strict clearance, and the path ends strictly above `b`. ∎

**Remarks.**
- **The new endpoint requirement** no longer passes through `h ≥ c_h a_M³/Pjet⁶` ((R13)), whose power 3 is attained (O1 of review 5971985344). It needs only `a_M` against `η_LE`.
- **Where the LE conditions matter.** If `h > 1/9`, then `E0 < μ/2` already certifies the endpoint, since `4h > (1 − h)/2 = μ/2`. So the LE conditions only matter on `{h ≤ 1/9}`.

### 2. Fixed `Λ`: both sectors at `O(r^{11/3−ε})`

**Lemma B (the endpoint strip).** In C97's setting, let `w ≥ 1`, `2rw ≤ L/4` and `η_LE ≤ 1`. Then

    μ_r(Rsec ∩ {η_LE N(γ² + 72) ≥ a_M  or  η_LE N ≥ 1}) ≤ C(η_LE + r√η_LE).

*Proof.* The event lies in the union of three events:
- `{a_M ≤ √η_LE}`: by C93 (E2) with `φ = 1_{(0, √η_LE]}`, its mass is at most `C(η_LE + r√η_LE)`;
- `{η_LE N(γ² + 72) > √η_LE}`: by Markov's inequality, `(γ² + 72)² ≤ 73²Pjet⁴`, and (E2) with `φ ≡ 1` at `(p, q) = (2, 4)`, its mass is at most `Cη_LE`;
- `{η_LE N ≥ 1}`: likewise, its mass is at most `Cη_LE²`. ∎

**Theorem R′ (rejected sector).** Fix `ε ∈ (0, 2/3)`. Set `w = r^{−1/12}`, `d = r^{2/3−ε}`, and fix a real `p ≥ 2/(3ε)`. Uniformly over the fixed parameters, for all sufficiently small `r`,

    Q_r^W(Rsec ∩ {D_f(M_r) ≤ f(S_r)}) ≤ C_ε r^{11/3−ε},    Q_r^W(Rsec ∩ H_r) ≤ C_ε r^{11/3−ε},
    Q_r^W(Rsec \ H_r) = r³ m_R/z₀ + O(r^{11/3−ε}),          Q_r^W(H_r | Rsec) = O(r^{2/3−ε}).

*Proof.*
1. **The bad set.** `Rsec \ Good_LE ⊂ {Rch > w} ∪ {E0 ≥ μ/2} ∪ B`, where `B` is the event of Lemma B.
2. **The bound.** Use (R15) with `ρ = w − 5/2 ≥ w/2`, (R18) with this `d` and `p`, Lemma B and (R1). With `e = rw⁴ = r^{2/3}`,

       Q_r^W(Rsec \ Good_LE) ≤ C r³ [w⁻⁸ + rw⁻⁴ + d + r + (e/d)^p + rw² + r^{3/2}w].

3. **The exponents.** They are `2/3, 4/3, 2/3 − ε, 1, pε ≥ 2/3, 5/6, 17/12`. The binding pair is `w⁻⁸` against the band split `(d, (e/d)^p)`; this ledger has no elder value-margin term.
4. **The conclusion.** Corollary LE, C96 (D2) and (R23) give the four displays. The cutoffs `w ≥ 5`, `2rw ≤ L/4`, `d ≤ 1/4` and `η_LE ≤ 1` hold for small `r`. ∎

**Theorem E′ (elder sector).** Let `E` be C94's sector (C4), that is `{D_Λ, T, γ ≠ 0, ψ ≥ 2c, R² ≤ 16(ψ − 2c)²(ψ + c), μ < 0}`. Take the same `w`, `d` and `p`. Then

    Q_r^W(E \ H_r) ≤ C_ε r^{11/3−ε},    Q_r^W(H_r | E) = 1 − O(r^{2/3−ε}).

*Proof.*
- **The estimate.** C94 (C14) and (C16) hold for every fixed `p ≥ 1`; C94 (C17) chose `p = 2`. With these choices, the bracket exponents of (C16) are `2/3, 4/3, 2/3, 4/3, 2/3 − ε, 1, pε ≥ 2/3, 5/3`. Here `rw⁴ = r^{2/3}` is small, and C94's other cutoffs hold for small `r`.
- **The implication.** For every deterministic `w ≥ 3` with `2rw ≤ L/4`, C94's `Good(r, w)` implies `D_f(M_r) = f(S_r)`. This is C95 §4: Good supplies (G9)'s hypotheses, so (G9)–(G12) apply, and (G14) transfers the maximin to the torus. C95 states this as (G15) at `w = r^{−1/16}`, but its proof uses no property of that choice.
- **The conclusion.** Hence `Q_r^W(E \ A_r) ≤ C_ε r^{11/3−ε}`, and C96 (D2) replaces `A_r` by `H_r`. ∎

**Corollary (upgrading C97 (R24)).** For every `ε > 0`,

    Q_r^W((E ∪ Rsec) ∩ (H_r Δ E)) ≤ C_ε r^{11/3−ε}.

For `ε ≥ 2/3` this is trivial, because `Q_r^W(E ∪ Rsec) = O(r³)`.

### 3. Growing `Λ`: C101's rate for every `β < 2/3`

Here `E` is C101's sector `{T, γ ≠ 0, μ < 0}`; C98's coverage supplies C94's inequalities on it.

**Lemma B′ (the endpoint strip on the growing layer).** Assume C101 (Q5) and (Q26), with C101's `C_H` condition replaced by `η_LE ≤ 1`. Then

    μ_r(D_Λ ∩ Rsec ∩ {η_LE N(γ² + 72) ≥ a_M  or  η_LE N ≥ 1}) ≤ C[H³η_LE + rH⁴√η_LE].

*Proof.* Use the same three events as in Lemma B.
- The strip, by (Q14) at width `√η_LE ≤ 1`: `C(H²η_LE + rH⁴√η_LE)`.
- The two Markov terms, by (Q12), since `μ_r(N²Pjet⁴) ≤ CH³` under `rH ≤ 1`: `CH³η_LE` and `CH³η_LE²`. ∎

**Theorem QFE′.** In C101's setting, for each fixed `β ∈ (0, 2/3)` there are `C_β < ∞` and `r_β > 0`, uniform over the fixed parameters, such that

    ‖ν_r^F − ν_0^F‖_var ≤ C_β r^β,    1 − p_r = r³(α₁ + α₂) + O_β(r^{3+β}).

This extends C101 (Q4) from `β < 1/2` to `β < 2/3`.

*Proof.*
1. **The rejected certificate.** In C101 §5, replace the rejected certificate by `Good_LE`, and (Q20)–(Q21) by Lemma B′.
2. **The band.** Use (Q23) with a general fixed `p`. The same union and Markov's inequality with (Q12) give

       μ_r(E or Rsec, E0 ≥ |μ|/2) ≤ C_p[d + rH⁴ + H³(e/d)^p].

3. **The new error.** (Q27) becomes

       Rerr′ = w⁻⁸ + rH³w⁻⁴ + H⁴e + rH⁵√e + H³rw² + rH⁴(rw²)^{1/2}
               + d + rH⁴ + H³(e/d)^p + H⁵r²w⁴ + H⁷r²w²,    e = rw⁴.

   (Q28), (Q29), (Q32) and (Q34) are unchanged.
4. **The choice of parameters.**

       w = r^{−β/8},  Λ = r^{−α} with α = (2 − 3β)/16,  d = r^β,
       a fixed real p ≥ (β + 3α)/(1 − 3β/2),  a fixed integer m ≥ β/α.

   With `H ≤ 2r^{−α}`, the exponents are as follows; each is at least `β`.

| term | exponent of `r` |
|---|---|
| `w⁻⁸` | `β` |
| `rH³w⁻⁴` | `1 − 3α + β/2` |
| `H⁴e` | `1 − β/2 − 4α = (2 + β)/4` |
| `rH⁵√e` | `1 − 5α + (1 − β/2)/2` |
| `H³rw²` (Lemma B′) | `1 − 3α − β/4` |
| `rH⁴(rw²)^{1/2}` (Lemma B′) | `1 − 4α + (1 − β/4)/2` |
| `d` | `β` |
| `rH⁴` | `1 − 4α` |
| `H³(e/d)^p` | `p(1 − 3β/2) − 3α` |
| `H⁵r²w⁴` | `2 − 5α − β/2` |
| `H⁷r²w²` | `2 − 7α − β/4` |
| `Λ⁻ᵐ` (both failure tails) | `mα` |
| far and derivative exceptions | `1` |

5. **What binds.** Write `w = r^{−ω}`. Two pairs bind, and both go through the radius tail `w⁻⁸` ((Q17)).
   - **`w⁻⁸` against `H⁴e`** ((Q19)): `8ω ≥ β` and `1 − 4ω − 4α ≥ β` give `β ≤ 2/3 − 8α/3`.
   - **`w⁻⁸` against the band split** ((Q23)): `d ≤ r^β` and `H³(e/d)^p → 0` at fixed `p` need `e ≪ d`, so `1 − β/2 > β`, that is `β < 2/3`, whatever `α`.

   The second pair is the strict obstruction. It is also what stops Theorem R′.
6. **Admissibility.** The (Q26) exponents `1 − α`, `1 − β/8`, `1 − β/2`, `3/4 − β/8` (for `H²e`), `1 − β/4` and `β` are positive, so every cutoff holds for small `r`. ∎

**Example.** For `β = 3/5`: `α = 1/80` and `w = r^{−3/40}`. The least admissible `p` is `51/8` (the least integer is `7`), and the least `m` is `48`. So `1 − p_r = r³(α₁ + α₂) + O(r^{18/5})`.

**Remarks.**
- **Where the `2/3` comes from.** It comes from the radius tail `w⁻⁸` against the window error scale `e = rw⁴`, which enters both (Q19) and (Q23).
  - **Improving (Q19) alone** leaves the rate at `2/3`, by step 5's band pair.
  - **A radius tail of order `w⁻¹²`** (hypothetical) would allow every `β < 3/4`. L5 checks this; the referee's linear-programming search agrees.
  - Localizing the value error in (Q19) and (Q23), as Lemma LE does for the endpoint, is another possible route. It is not attempted here.
- **C103** (compact positive gaps) composes the same ledger. I have not checked whether its `k`-uniform constants allow the same substitution.

### 4. Checks and referee (exploration outside the repository)

`a4_exact.py` (standard library; exact rationals) runs 61,603 checks. Six mutants exit 1, an unknown label exits 2, and the output under `-O` is byte-identical.

- **L0.** `G = P∘chart` as a polynomial identity. `G` and `∇G` take the pin values at `raw M` and `raw S`, symbolically in `(λ, γ, B1, C3)`.
- **L1.** Lemma LE (ii), on 3,000 exact critical points (one in five next to a degenerate `M`), each with three values of `γ`. It checks the proof's matrix, both determinant cases and positive semidefiniteness, and the equality example above.
- **L2.** The Taylor identity behind Lemma LE (i), for 400 random degree-4 polynomials pinned at `M`, and the attained example.
- **L3.** The scalar margin bookkeeping of Corollary LE.
- **L4.** The two fixed-`Λ` ledgers, for `ε = 1/30, 1/100, 1/1000`.
- **L5.** The growing-`Λ` ledger and admissibility, for six values of `β` up to `2/3 − 1/1000`. It also checks the Example's least `p` and `m`, and the hypothetical `w⁻¹²` variant of the Remark.

The mutants are:
- `(X² − 1/3)` in `G`;
- `γ² + 36` in place of `γ² + 72`;
- a field with `e(M) = 0` but a nonzero gradient at `M`;
- C101's old endpoint term;
- `p` fixed at 2;
- `w = r^{−β/16}`.

**Referee.** A clean-context referee (Anthropic, same provider, so not review evidence) returned ACCEPT WITH REVISIONS, with nothing blocking or major.
- **What it checked.** It re-derived A4's own algebra and every exponent, and checked that each imported estimate is used within its hypotheses. It used linear programming for the binding analysis. It did not re-derive the imported sources.
- **The delta check.** Its delta check of this revision is RESOLVED WITH NOTES, and the notes are applied.
- **Its nine findings**, all applied here:
  - the corrected account of what binds (step 5 and the Remark);
  - the hypotheses of Corollary LE;
  - the C95 and C97 citation form;
  - notation;
  - attributions and source identities;
  - the sharpness remark;
  - the check suite;
  - `K_raw`;
  - the scope sentences.

### 5. Not claimed

- `β ≥ 2/3`, or `r^{11/3}` without `ε`.
- C103's compact-gap version.
- Any statement in dimension `≥ 3`.
- Any change to the reviewed statements of C94, C95, C97 or C101. A4 is additive. It re-chooses their free parameters, replaces C97's certificate (R19) and estimates (R16)–(R17) and C101's (Q20)–(Q21), and generalizes `p` in (Q23).

**Review request.** An optional, bounded nonauthor read of Lemma LE, Lemmas B and B′, and the two ledgers. Please claim first.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
_Generated by [Claude Code](https://claude.ai/code)_