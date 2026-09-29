# SARD-G premise A2: where the regularity actually sits, and the weakest form the slicing needs

Object: CL-SARD-A2-REGULARITY-20260929-v2.
Author: Anthropic Claude (Claude Code session `session_017Mi3hxjaxV45x6zo6o1ee3`).
Disposition: AUTHOR-SIDE SOURCE NOTE; nonauthor review required.
Scientific effect: NONE. No register, graph, lemma flag, prize or source changes. C103 is not moved.

## 1. Contract

The robust-chart successor [RC-S] (Math-#135, `frontiers/sard_g_robust_charts_20260929/PROOF.md`, blob `7e223706…`)
imports two premises from SG (main `a1fc9581`), which lists "A2 parameter-dependent local invariant-manifold and
first-crossing regularity" but proves neither. The published A1–A6 reviews issue no A2 verdict.

- **A2-T.** The local branch germs and the finite regular flow arcs depend continuously on `f ∈ X = C²(T_L²)` in the
  `C¹` arc topology.
- **A2-D.** The same objects are `C¹` in the field parameter and the arc parameter.

[RC-S] §2 warns that any regularity loss "at the C2-field/C1-vector-field interface must be resolved in A2's own
review". This note makes three claims.

- **(J)** `F(x, f) = ∇f(x)` is jointly Fréchet-`C¹` on `T² × X`. A loss of one derivative appears only if one asks
  for `f ↦ γ_f` to be Fréchet `C¹` *into `C¹` arcs*. No step of [RC-S] asks for that.
- **(G)** Every use of A2-D in [RC-S] (R1a, R2's `C¹` mismatch, R3d, R4) needs only the weaker line form A2-G of §4,
  and A2-G follows from classical one-parameter theory.
- **(T)** A2-T follows from classical continuous-dependence theory.

§5 checks each use of A2-G against [RC-S]. The full Fréchet A2-D is recorded in §6 as cited theory, not proved here.
A3–A4 are not addressed.

## 2. Lemma J: the vector field is jointly `C¹` in position and field

Use the flat structure of `T_L² = ℝ²/(Lℤ)²`, so `∇` and `D²` are global. Define `F: T² × X → ℝ²` by
`F(x, f) = ∇f(x)`.

**Lemma J.** `F` is Fréchet `C¹`, with

    DF(x, f)[ξ, h] = D²f(x) ξ + ∇h(x).                                  (J1)

For all `x, y ∈ T²` and `f, g ∈ X`:

    |D²f(x) − D²g(y)| ≤ ‖f − g‖_{C²} + ω_{D²g}(|x − y|),                  (J2)
    sup_{‖h‖_{C²} ≤ 1} |∇h(x) − ∇h(y)| ≤ |x − y|,                          (J3)

where `ω` is a modulus of continuity.

*Proof.* `F` is linear in `f` and `C¹` in `x` for fixed `f`. The remainder

    F(x+ξ, f+h) − F(x, f) − D²f(x)ξ − ∇h(x)
      = [∇f(x+ξ) − ∇f(x) − D²f(x)ξ] + [∇h(x+ξ) − ∇h(x)]

is `o(|ξ|) + ‖h‖_{C²}|ξ| = o(|ξ| + ‖h‖)`. Continuity of `(x, f) ↦ DF(x, f)` in operator norm is exactly (J2) for
the `ξ`-part and (J3) for the `h`-part. (J3) is the mean-value inequality with `‖D²h‖_∞ ≤ ‖h‖_{C²}`. ∎

**Where a derivative is lost.** Consider `X → C¹(T²; ℝ²)`, `f ↦ ∇f(· + p(f))`, the field recentred at a moving
saddle `p(f)`. It is not differentiable in general for `f ∈ C² ∖ C³`: its derivative in `p` would be
`D²f(· + p) ∈ C¹`, which requires `D³f`. Proofs that recentre and then apply a Banach fixed-point argument in `C¹`
function spaces therefore lose a derivative. A second, easily missed loss occurs at a moving saddle. The unstable eigenline `e_u(f)` of `D²f(p(f))` is only
*continuous* in `f`: its derivative in direction `h` would involve `D²h(p) + D³f(p)[Dp(f)h]`, which needs `D³f`. So a
germ written as a graph over the MOVING eigenline need not be `C¹` in `f`, even though the geometric germ is. The
remedy is to use a graph coordinate over a FIXED direction, chosen once per atlas neighbourhood (§4). Transversality
keeps the germ a graph there, and the geometric first hit on a fixed section is independent of the parameterization.

The arguments of [RC-S] never recentre in `C¹` function spaces. They differentiate point
functionals `(s, f) ↦ γ_f(s)` and hitting times through the scalar implicit-function theorem (R1a), which needs only
(J1)–(J3) and their consequences below.

## 3. A2-T from continuous dependence

Let `f_0 ∈ U_χ^rob` and let `p_0` be a tracked hyperbolic saddle.
- **Saddles.** By (J1) and the implicit-function theorem, `p(f)` is `C¹` near `f_0`, with
  `Dp(f)[h] = −D²f(p)^{-1}∇h(p)`.
- **Local germs.** For `C¹` vector fields, the local stable and unstable manifolds of a hyperbolic equilibrium are
  `C¹` embedded curves that depend continuously on the vector field in the `C¹` topology (stable manifold theorem with
  continuous dependence; e.g. Palis–de Melo, *Geometric Theory of Dynamical Systems*, Ch. 2 §6; Hirsch–Pugh–Shub).
  Since `f ↦ ∇f ∈ C¹` is bounded linear, the four labelled germs, written as graphs over the continuing eigenlines,
  depend continuously on `f ∈ X` in the `C¹` arc topology.
- **Regular arcs.** On compact time intervals, solutions of `ẋ = ∇f(x)` and their first spatial derivatives depend
  continuously on the vector field in `C¹` (Gronwall).

Hence A2-T holds on the chart domains. This is the only premise R2's openness uses.

## 4. A2-G: the line form, from one-parameter theory

**A2-G.** For every `f ∈ U_χ^rob` and `h ∈ X`:
1. `t ↦ D_χ(f + th)` is `C¹` on the open set `{t: f + th ∈ U_χ^rob}`, with derivative at `t = 0` equal to `L_f(h)`.
2. `h ↦ L_f(h)` is linear, with `|L_f(h)| ≤ C_f ‖h‖_{C¹}`.
3. For each fixed `h`, `f ↦ L_f(h)` is continuous on `U_χ^rob`.

The same holds for the launch points, the hit parameters and the hit points.

*Proof.* Fix `f, h` and set `V_t(x) = ∇f(x) + t∇h(x)`. By Lemma J, `(x, t) ↦ V_t(x)` is `C¹`, and it is affine in
`t` with `∂_t V_t = ∇h ∈ C¹`. This is a one-parameter `C¹` family of planar vector fields, so classical
finite-parameter theory applies.
- The saddle `p(t)` is `C¹` by the implicit-function theorem.
- The local unstable and stable manifolds are `C¹` in `(a, t)` as graphs `w̃(a, t)` over a FIXED direction (the
  eigenline at `t = 0`), not over the moving eigenline (see §2).
  Suspend with `ṫ = 0`. The curve `{(p(t), t)}` is a normally hyperbolic curve of equilibria, and its local
  unstable (stable) manifold is `C¹` (Fenichel; Hirsch–Pugh–Shub). Alternatively, cite the parameter-dependent
  stable manifold theorem for `C¹` families.
- The flow is `C¹` in `(time, x, t)`, by classical dependence on parameters.
- Hitting times and points are `C¹`, by R1a.

This proves part 1 at `t = 0`, and at every point of the open set by applying the same argument at `f + t_0 h`.

**Linearity and the bound (part 2).** The `t`-derivative is obtained by linearizing at `t = 0`. The perturbation
enters the variational equations only through the forcing `∇h`, evaluated along the saddle, the germs and the arcs.
- The saddle moves by `−D²f(p)^{-1}∇h(p)`.
- The germ variation is the unique solution of the linearized invariance equation that stays bounded in backward
  time. It has the Lyapunov–Perron form `∫_{−∞}^0 (dichotomy kernel)·∇h(γ(σ)) dσ`. On the compact germ domain it is
  bounded by `C_f ‖∇h‖_{C⁰}`.
- The flow and hitting variations are Duhamel integrals of `∇h` along compact arcs, divided by the positive transverse
  margin in R1a.

All of these are linear in `h` and bounded by `C_f ‖h‖_{C¹}`.

**Continuity in `f` (part 3).** The data of these linear formulas depend continuously on `f ∈ X`:
- the orbit, `D²f` along it, and the eigenprojections, by §3;
- the exponential dichotomy on the germ domain, which is robust under `C¹`-small perturbations of the coefficient
  `D²f(γ(σ))`;
- the transverse margin, which is bounded below on the chart.

Dominated convergence in the convergent dichotomy integrals then gives continuity of `f ↦ L_f(h)`. ∎

`a2_check.py` gives an exact polynomial instance of the Lyapunov–Perron variation.
- For `V_t(x, y) = (x, −y + x² + t x³)` the unstable manifold is exactly `y = x²/3 + t x³/4`.
- Its `t`-derivative `x³/4` equals the backward integral `∫_{−∞}^0 e^{σ}(x e^{σ})³ dσ`.
- Two perturbations superpose linearly: `t_1 x³ + t_2 x⁴` gives `t_1 x³/4 + t_2 x⁴/5`.
- The saddle-displacement formula holds for `V_t = (x − t, −y + x²)`.

## 5. Each use in [RC-S] needs only A2-T and A2-G

| Use in [RC-S] | What is needed | Supplied by |
|---|---|---|
| R2 openness of `U_χ^rob` | continuity of germs, arcs and hits | A2-T (§3) with R1 |
| R1a hit derivative | `C¹` dependence of `(s, f) ↦ γ_f(s)` along the direction used | A2-G part 1 |
| R4: `B_{χ,ℓ}` Borel | `D_χ` continuous; `f ↦ ∂_{h_ℓ} D_χ(f)` continuous | A2-T; A2-G part 3 |
| R4: `F_g(t) = D_χ(g + t h_ℓ)` is `C¹` with `F_g' = L_{g+th_ℓ}(h_ℓ)` | line `C¹` with continuous derivative | A2-G parts 1 and 3 |
| R3d: some `h_ℓ` with nonzero derivative | `L_f|_H` linear, continuous, nonzero | A2-G part 2 (since `‖h‖_{C¹} ≤ C‖h‖_H`), with A3–A4 read for `L_f` |

The A3–A4 premise is phrased in [RC-S] for "the derivative of the mismatch". Its original route computes that
derivative as a curve contribution plus endpoint-supported terms applied to `h`, which is exactly `L_f(h)`. Reading
it for the line derivative `L_f` therefore changes nothing in that route. Its nonvanishing is not addressed here.

**Note for [RC-S] P2.** P2's "graph coordinate" should be read as a fixed-frame coordinate chosen with the atlas
neighbourhood. If it meant the moving eigen-coordinate, the germ parameterization could fail to be `C¹` in `f`.
R1a would then apply to a different, fixed-frame parameterization of the same geometric germ, with the same hit
point. No conclusion changes, but the wording should say which coordinate is meant.

## 6. The full Fréchet A2-D (cited theory, not proved here)

By Lemma J, the planar vector-field family `(x, f) ↦ ∇f(x)` is jointly `C¹` with a Banach parameter.
- Flows of `C¹` vector fields with a `C¹` Banach parameter are `C¹` in `(time, x, parameter)` (Dieudonné,
  *Foundations of Modern Analysis*, the chapter on differential equations).
- Local unstable manifolds depend `C¹` on Banach parameters by the Lyapunov–Perron method on a scale of exponentially
  weighted spaces (Vanderbauwhede–van Gils, 1987). The loss of exponent in the Nemytskii operator is handled there by
  the two-weight argument.

With (J1)–(J3) these give A2-D as stated in [RC-S]. This note does not reprove those theorems. The reduction of §5
means that [RC-S]'s conclusions need only §§3–4.

## 7. Reading rule

This note licenses exactly the following.
1. **Lemma J**, as proved in §2.
2. **A2-T and A2-G**, as consequences of the classical theorems named in §§3–4, under those theorems' stated
   hypotheses. The citation-based steps await nonauthor verification against primary sources.
3. **A reduced application of [RC-S].** R1a, R2's `C¹` mismatch, R3d (with A3–A4 read for the line derivative
   `L_f`) and R4 are to be read with **A2-G in place of A2-D**, as tabulated in §5.

It does **not** license the literal Fréchet sentence A2-D ("C1 in the field parameter" on `X`). That stronger
assertion stays an import of [RC-S], and §6 only cites it. A consumer that needs Fréchet differentiability of
`D_χ` on `X`, rather than its line derivatives, cannot use this note for it.

## 8. Scope

- Proved here: Lemma J; the reduction of §5.
- Classical theorems with explicit hypotheses: A2-T and A2-G.
- Cited only: the full A2-D.
- Not addressed: A3–A4, finite-jet nondegeneracy, `μ(Ω_gen) = 1`, the R1/R2 geometry (Harper's slice) and C103.
- The finite companion checks exact polynomial identities only.

## Revisions

- **v2** ([5891507824](https://github.com/d6g8k5htny-coder/Math-/pull/138#issuecomment-5891507824)): adds the §7 reading
  rule, which separates the reduced A2-G application from the unproved literal Fréchet A2-D. No other change.
