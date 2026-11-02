# SPEC65 — coherent actual saddle lower and positive closed uppercuts

28 October 2026. **Adopted PRECODE65 contract; implementation inactive.**
Root adopted this contract after personally reading the complete three
drafts and the independent full precode-design review, PASS with no
amendments. The accompanying adoption record carries the actual UTC.
Public64 remains a conditional unqualified future dependency until its
qualification and publication. No source/helper proof text, harness,
execution, author seat, external claim, GO, role or timer is authorized
by adoption. The draft author and document reviewer are not65 proof
authors. Same-family technical credit zero; science NONE.

Read with the companion PLAN and CONTROLS. The accepted design basis is retained unchanged as dated local adoption
evidence in `/workspace/scratch/actual-source-saddle-uppercuts-preflight/REPORT.md`
and its `DESIGN_DELTA.md`; independent review is retained under
`/workspace/scratch/actual-source-saddle-uppercuts-source-review/`.
The delta requires the same-chart inherited all-δ lower traces below.
The earlier upper-bound-removal negative was discarded before adoption;
it is not a second mutation.

## Future dependency and one new local leaf

The adopted 64 design proposes
`I4SourceActualQuotientSaddleCollar.actualSource_quotient_saddle_local_collar`
in `SourceActualQuotientSaddleCollar`. **Public 64 remains an unqualified
future dependency until its qualification and publication.** This draft
does not assert that its import or theorem is currently available. Later
complete context must bind the qualified published public declaration and
its exact source/object lineage; no private 64 body or Controls binary is
an input to 65.

Conditional on that dependency, call public 64 exactly once internally for
each prescribed ambient O, retain one chart witness unchanged, and add the
uniform positive closed uppercut geometry. Project its already-returned
all-δ lower-trace conclusion into the same new endpoint. Do not make a
separate 64 call to obtain lower traces: that could select a different
noncanonical chart. No normal-form or quotient-chart construction is
reimplemented here.

## Sole public proposition, no public data

Proposed module: `SourceActualSaddleUppercuts.lean`.
Namespace: `I4SourceActualSaddleUppercuts`.
Exactly one authored public proposition:
`actualSource_quotient_saddle_uniform_closed_uppercuts`.
No public definitions, data, aliases, fixture library, generic geometry
library, component quotient or global instances.

The literal objects and only local inputs are:

| Notation | Existing actual object |
| --- | --- |
| L,hL | Original `L : ℝ` and `hL : 0<L` |
| ω | `I4SmoothCarrier.SmoothSample 2 L` |
| E2 | `UniversalLaw.Spec.Lifetime.E 2`, the physical Euclidean carrier |
| g | `I4LifetimeField.actualField 2 L ω` |
| X | Actual physical point in E2 |
| hcrit | `UniversalLaw.Spec.Lifetime.IsCriticalPoint 2 g X` |
| hI | Full literal `UniversalLaw.Spec.Lifetime.HessianHasInertia 2 g X 1` |
| Torus | `I4Torus.SourceTorus 2 L` |
| F | `SourceActualFoldTorus.actualTorusField hL.ne' ω` |
| q | `I4Torus.torusProjection 2 L (I4LifetimeField.coordinates 2 X)` |
| c | F(q), equal to g(X) by the actual pullback |
| Point2 | `Fin 2 → ℝ` with its existing Pi/max norm |

Full hI includes complementary one-dimensional negative and positive
definite subspaces for the actual Hessian, not a bare index tag. No global
`IsMorseDistinct`, unused hm, desired chart, nonsingularity certificate,
supplied branch statement or global event certificate is a public premise.
Index convention remains j=2 maximum, j=1 saddle, j=0 minimum; only j=1 is
in this leaf. Existing actual smoothness enters through public 64.

## Exact output and quantifier order

For every ambient open O containing q, derive one ρ>0 and one
`OpenPartialHomeomorph Torus Point2` φ satisfying:

1. q∈φ.source, φ(q)=0, φ.source⊆O, and
   φ.target equals exactly the centered Point2 ball of radius ρ.
2. For every z∈φ.source,

       F(z) = c − (φ(z)₀)² + (φ(z)₁)².

3. For this same φ, for every δ≥0,

       IsPathConnected (φ.source ∩ {z : c−δ ≤ F(z)}).

4. Let ε₀=ρ²/4, with ε₀>0. For this same φ and every 0<ε<ε₀,
   use only transparent bound terms

       Uε  = φ.source ∩ {z : c+ε ≤ F(z)},
       Bε⁺ = Uε ∩ {z : 0 < φ(z)₁},
       Bε⁻ = Uε ∩ {z : φ(z)₁ < 0}.

   Return `IsPathConnected Bε⁺`, `IsPathConnected Bε⁻`,
   `Disjoint Bε⁺ Bε⁻`, Uε=Bε⁺∪Bε⁻, and for all p,r∈Uε,

       JoinedIn Uε p r  ↔  0 < φ(p)₁ * φ(r)₁.

`IsPathConnected` includes nonemptiness. The order is **∀O, ∃oneρ,φ,
structural outputs, then ∀δ≥0 and ∀0<ε<ρ²/4**. All conclusions use the
same actual source, chart, field, carrier, period, center and level.
No chart/radius/source choice is made per sign, per ε, per δ or per side
of the critical level. The δ and ε quantifiers are independent after the
single witness choice. The public proposition expands actual objects and
branch terms through existing names or transparent local lets; no private
definition leaks into its statement.

The output is a closed **field inequality** restricted to an open chart
source, hence is closed relative to that source. No claim that Uε is closed
in the whole torus is made. The uppercut is not replaced by a strict cut.
No 64 strict-branch package is re-exported; its public strict JoinedIn
conclusion may be used internally for no crossing.

## Only new geometry: three segments in the Pi2 box

Write Q(u,v)=−u²+v². The exact target ball is |u|<ρ, |v|<ρ.
For ε>0, Q≥ε forces v≠0, giving the disjoint sign partition.
The fixed target points (0,±ρ/2) are in the target and satisfy Q=ρ²/4,
so they witness both branches for every ε<ε₀ without reselection.

For positive-branch endpoints (u,v),(u′,v′), put H=max(v,v′) and
m=max(|u|,|u′|). Use the three segments

    (u,v) → (u,H) → (u′,H) → (u′,v′).

Vertical coordinates remain positive and no smaller than the relevant
endpoint height; the middle segment has |horizontal coordinate|≤m.
The endpoint cut inequalities imply H²≥ε+m², so all three segments stay
in Q≥ε. Every coordinate stays strictly within the Pi box because H,m<ρ.
Reflect the second coordinate for the negative branch. No square root,
SOC library, Pi/physical-Euclidean isometry or new affine calculus library
is needed. Finite geometry and chart transport remain private.

Map through the inverse chart only on its exact target, retaining source
membership and inverse equations along the entire path. A path in Uε is
also in 64's strict trace because ε>0; its public strict JoinedIn
equivalence supplies the no-crossing implication. The new branch paths
give the converse. The lower-trace output is the already-returned public
64 fact, projected without further shrinking the chart.

## Genuine controls and sole negative

CONTROLS requires the unchanged original period-2 finite source with actual
field cos(πX₀)+2cos(πX₁), both genuine saddles, small prescribed ambient
neighborhoods and the seam lift. Actual criticality and full complementary
inertia must be derived, with no global hm fixture. The equality-at-cutoff
case ε*=ρ²/16 uses actual inverse points (0,±ρ/4) to test the closed
inequality. No private 64 fixture/control copy or public fixture library.

The sole mutation changes only **ε>0 to ε≥0**, retaining ε<ε₀, the same
chart/source/field/carrier and the closed cut. At ε=0, a structure-only
inverse vertical segment joins the fixed opposite-sign witnesses through
the actual q, contradicting the proposed sign-product JoinedIn test.
The independent counterproof must not use 65 production branch geometry
or the inherited lower-PC output as a shortcut. It is a nonempty local
critical-boundary collision, not a strict/closed substitution. The
discarded omission-of-upper-bound proposal is not another negative.

## OPEN scope and authority

Private same-chart inclusions for ε₁≤ε₂ and their sign-labelled JoinedIn
consequences may be retained only for an identified consumer; they are
not new public API or a global component-inclusion theorem.

Regular quotient collars, finite graph/adjacency and edge persistence,
lower compact clopen separation, actual global critical-event component
inclusions, exhaustive elder/once-count/H0 interpretation, measurable/Borel
counts, Rice/PairLaw and Parent conclusions remain OPEN. Local arms may
join outside the chart; coherent traces on both sides do not prevent that.
Maximum/minimum leaves remain separate.

Workspace AGENTS requires reuse of completed applicable verification and
accepted mathematics across agents/sessions/heads/handoffs. A future wrapper
does not erase its qualified dependencies. Provider process remains
separate. Contract adoption is not mathematical qualification or implementation
authority; future public 64 qualification/publication remains a dependency.
