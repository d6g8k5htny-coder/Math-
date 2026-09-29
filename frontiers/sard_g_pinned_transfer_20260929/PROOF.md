# SARD-G for pinned and tilted laws: the measure-dependent steps and their transfer

Object: CL-SARD-PINNED-TRANSFER-20260929-v1.
Author: Anthropic Claude (Claude Code session `session_017Mi3hxjaxV45x6zo6o1ee3`).
Disposition: AUTHOR-SIDE SOURCE NOTE; nonauthor review required.
Version: v2 (admissible-law scope for Corollary R0, per OpenAI review 5353818348; Theorem P unchanged).
Scientific effect: NONE. No register, graph, lemma flag, prize or source changes. R0 and C103 are not moved.

## 1. Why this is needed

In the q0 program, R0 is the Gaussian-Sard/Morse–Smale condition *for the conditioned flow*: the pinned law `Q_r`
and its tilt `Q_r^W` (q0 ledger, "MS-Sard / R0: a.s. Morse–Smale for the conditioned flow"). The SARD-G chain is
written for the unconditioned law `μ` of the periodized field on `X = C²(T_L²)`, which is the "full-Gaussian C103
corollary":
- SG (main `a1fc9581`);
- the robust-chart successor [RC-S] (Math-#135, blob `7e223706…`);
- the A2 note [A2] (Math-#138);
- the forthcoming A3/A4 proof.

The pinned laws are singular with respect to `μ`: they live on the null set `{U_r = v_r}`. The conclusion therefore
does not transfer by absolute continuity. This note identifies exactly which steps of the chain depend on the measure,
and proves that each of them holds for the pinned and tilted laws.

## 2. Which steps depend on the measure

Go through [RC-S] §§3–8 and [A2].
- **Deterministic statements about a fixed field or chart:**
  - R1 (first contact);
  - the chart predicate P1–P4, openness (R2) and coverage (R2b);
  - A2-T and A2-G, including the bound `|L_f(h)| ≤ C_f‖h‖_{C¹}`;
  - the countability of regular zeros on a line (R4).
- **Steps that use the measure `μ`:**
  - **(M1)** R3: density of covariance images in the Cameron–Martin space, and the independent residual.
  - **(M2)** A3–A4: the line derivative `L_f` is nonzero *on the Cameron–Martin space*.
  - **(M3)** the full-measure generic set `Ω_gen` (Morse, distinct critical values).
  - **(M4)** the Tonelli step of R4, which uses the independent standard-normal coordinate.

## 3. The localized form of A3–A4

**(L).** Let `f ∈ Ω_gen` lie in some `U_χ^rob` with `D_χ(f) = 0`. For every finite set `P` of critical points of `f`,
there is `φ ∈ C^∞(T²)` vanishing on a neighbourhood of `P` with `L_f(φ) ≠ 0`.

The announced A3/A4 proof (Math-#138 comment 5891507824) uses a `C²` bump transverse to an interior point of the
unstable half-arc, away from the endpoint neighbourhoods and the stable half-arc. Such a bump already satisfies (L).
The half-arc consists of regular points, so it has positive distance from every critical point, and the bump's support
can be shrunk to avoid any finite critical set `P`. This note uses (L) as its A3–A4 input and does not prove it.

## 4. Theorem P (pinned Gaussian laws)

**Setting.**
- Let `P ⊂ T²` be finite, and let `J_P h = (h(p), ∇h(p))_{p∈P}`, which is `3|P|` functionals.
- Let `f̃` be the centered Gaussian field obtained from the periodized field by regression on `J_P`, that is,
  conditioning on `J_P = 0`.
- Let `m ∈ C³(T²)` be deterministic with `∇m(p) = 0` for `p ∈ P`.
- Put `Q = Law(m + f̃)`. Then `Q`-a.s. every point of `P` is a critical point.

**Theorem P.** Assume the deterministic imports of §2, and (L). Assume also `Q(Ω_gen) = 1`, where `Ω_gen` means Morse
with distinct critical values. Then the saddle–saddle connection event is `Q`-null in the completed space.

*Proof.*

**(M1).** The covariance operator of `f̃` is `Q̃ℓ = Π_P Qℓ`, where `Π_P` is the `H`-orthogonal projection onto
`H_P = {h ∈ H : J_P h = 0}`. The Cameron–Martin space of `f̃` is `H_P` with the `H` inner product. For `h ∈ H_P`,
`⟨h, Q̃ℓ_n⟩_H = ⟨h, Qℓ_n⟩_H = h(x_n)`. So `h ⊥ Q̃ℓ_n` for all `n` forces `h = 0` on the dense set `S`, hence `h = 0`.
The images `Q̃ℓ` of rational combinations of point evaluations are therefore dense in `H_P`. The normalization, the
standard-normal coordinate `ξ_ℓ = ℓ(f̃)/√v_ℓ` and the independent residual `g_ℓ = m + f̃ − ξ_ℓ h_ℓ` are exactly as
in R3, now with `f̃`. The deterministic mean sits in the residual.

**(M2).** Take `φ` from (L), with `P` the pin set, which consists of critical points `Q`-a.s. Trigonometric polynomials
lie in `H` (every Fourier weight is positive) and are dense in `C²`, by Fejér means of the smooth `φ`, so choose
trigonometric polynomials `τ_n → φ` in `C²`. The functionals `J_P` are linearly independent on trigonometric
polynomials (distinct-site jets), so choose trigonometric polynomials `ψ_i` dual to them. Then
`h_n = τ_n − Σ_i (J_P τ_n)_i ψ_i ∈ H_P` and `h_n → φ` in `C²`, because `J_P τ_n → J_P φ = 0`. By A2-G part 2,
`L_f` is continuous in `C¹`, so `L_f(h_n) → L_f(φ) ≠ 0`. Thus `L_f|_{H_P} ≠ 0`, and by (M1) some `h_ℓ` has
`L_f(h_ℓ) ≠ 0`. This is (R3d) for `Q`.

**(M4).** R4 goes through verbatim. `B_{χ,ℓ}` is Borel by A2-T and A2-G part 3. On each open validity interval the
regular zeros are countable. Independence of `ξ_ℓ` and `g_ℓ` together with Tonelli gives `Q(B_{χ,ℓ}) = 0`.

**(M3)** is assumed. The covering (R2b) is deterministic. A countable union of null sets is null, so
`Q*(Connection) ≤ Q*(Connection ∩ Ω_gen) + Q(Ω_gen^c) = 0`. ∎

With `P = ∅` and `m = 0`, Theorem P is the full-Gaussian statement, so the theorem also re-derives that case under
the same imports.

## 5. Genericity for the laws used by R0

Fix an **admissible** law: distinct pin sites `M ≠ S` on `T²` and gap `k > 0`, within the validity regime of the
parent (its local cylinder and pin covariance, `0 < r ≤ r_0` below the torus injectivity scale), or a separately
proved extension. For example `r = L`, `u = e_1` identifies `M` and `S` on the torus, and then unequal pinned values
are impossible; such parameters are excluded. For each admissible law, `Q_r` is `Law(m_r + f̃)` with `P = {M, S}`.
The pins are values and gradients, so `J_P` is exactly the pin frame `U_r` up to an invertible map. `m_r` is the
regression mean, which has `∇m_r = 0` at `M` and `S`.

D1 parent §8, `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md` (sha `9350ad6e…`), accepted
within the D1 reconciliation of Math-#126, proves exactly `Q_r(Ω_gen) = 1`, and then `Q_r^W(Ω_gen) = 1` because
`0 < Z_r < ∞`. Its ingredients are:
- an overdetermined-zero lemma, applied to `(∇f(x), Hf(x)v)` away from the pins and to
  `(∇f(x), ∇f(y), f(x) − f(y))` on compact separated sets;
- pinned Hessian densities;
- ties to the pinned heights, which are distinct since `kr³ > 0`.

The same argument with no pins gives `μ(Ω_gen) = 1`. The pinned and tie cases then simply do not occur. So (M3)
is **discharged** for `μ` and for each admissible `Q_r` and `Q_r^W` by an already-accepted source.

**Corollary R0.** Assume the imports named in §7. Then for each fixed admissible law as above, `Q_r` and `Q_r^W` are
almost surely Morse–Smale. The `Q_r^W` case follows by absolute continuity with density `W_r/Z_r` *with respect to
`Q_r`*, and so only after Theorem P for `Q_r` itself: `Q_r^W` is not absolutely continuous with respect to the
unconditioned law.

The statement is per fixed law. It gives no common almost-sure set for uncountably many targets, and no uniform
quantitative constants as `r → 0`. No regional or numerical estimate follows.

For planar gradient flows, Morse–Smale means Morse together with no saddle–saddle connection. Gradient flows have no
periodic orbits, and every other stable/unstable intersection is transverse by dimension.

## 6. Finite companion

`transfer_check.py` works in exact rationals on a trigonometric circle model, with value-and-derivative pins at two
Pythagorean points. It checks four things:
1. The pin functionals have full rank on trigonometric polynomials.
2. The corrected approximant satisfies `J_P h = 0` exactly, and its correction is linear in `J_P τ`.
3. Projected covariance images `Π_P Qℓ` lie in `H_P` and reproduce `ℓ` on `H_P`.
4. Enough projected point evaluations span `H_P`.

Mutants that skip the correction, fail to project or duplicate a pin are rejected.

## 7. Scope and reading rule

**Proved here:**
- the classification of §2;
- Theorem P from its stated imports;
- the discharge of (M3) by D1 parent §8.

**Imports, not reviewed or proved here:**
- R1/R2 (A1; xAI/Harper's slice);
- A2-T and A2-G ([A2], Math-#138), or #137's alternative route;
- (L), the A3–A4 proof announced by OpenAI.

The literal Fréchet A2-D is neither needed nor claimed.

No R0 or C103 register change follows until those imports have their own nonauthor verdicts. No novelty claim is
made: parametric transversality for random fields is a known genre, and a planned prior-art search could not run
because the search quota was exhausted.
