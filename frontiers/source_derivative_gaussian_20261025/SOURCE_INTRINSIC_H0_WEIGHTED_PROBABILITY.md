# Frozen precode: fixed-axis intrinsic finite-bar Borel event and probability

26October2026. Root fully read and adopted this bounded design and the separate source/API preflight; original scratch drafts remain preserved. This document makes no implementation or qualification claim. Proposed module `SourceIntrinsicH0WeightedProbability.lean`, namespace `I4SourceIntrinsicH0WeightedProbability`. REPORT gives the concrete API/proof route. No in-flight H0/53 source/helper was inspected; only the allowed intrinsic-interface contract documents were read. Root owns native pickup, pre-source concrete control freeze, code authorization, new-only qualification, cache/registration/Git/publication.

Scientific effect NONE; same-family/provider-distinct credit0. Owner `/workspace/AGENTS.md` requires completed applicable verification reuse and separation from pending review/process work. No old source, proof, check, kernel/audit/control or hash campaign is replayed.

## Two public data definitions

Use the **prospective qualified** `I4SourceIntrinsicH0Interface.h0Interface`, literal Lifetime namespace/predicates, original positive-period actual source and the old fixed-axis endpoint lifts.

```text
sourceIntrinsicFiniteBarEvent (L r:ℝ) : Set(SmoothSample2 L) :=
 {omega | IsFiniteBar 2 L (h0Interface 2 L)
    (actualField 2 L omega) (endpointLiftM r) (endpointLiftS r)}.

sourceIntrinsicFiniteBarProbability {L:ℝ}(hL:0<L)(r b k:ℝ) : ℝ :=
 (sourceCompactFoldWeightedLaw hL.ne' r b k).real
    (sourceIntrinsicFiniteBarEvent L r).
```

The event depends only on L,r; b,k select its actual posterior/weighted law. This is not Good renamed as a bar event, not an arbitrary bounded p, and not a `PairLawInterface` constructor. Keep the physical source weight and sourceGapLaw unchanged. The function is total, but probability bounds are asserted on the stated normalized interval only.

## Exactly two public written propositions

Specifications below are not elaboration-checked declarations.

**1. `sourceIntrinsicFiniteBarEvent_measurable`**

```text
{L:ℝ}(hL:0<L)(r:ℝ) :
  MeasurableSet(sourceIntrinsicFiniteBarEvent L r).
```

Prove actual Borel measurability on the full original smooth carrier. It is not merely a Borel superset, a Good-event implication, an outer-measure bound or a statement with desired event measurability as a premise.

**2. `sourceIntrinsicFiniteBarProbability_uniform`**

```text
{L:ℝ}(hL:0<L)(B k0 k1:ℝ)
(hB:0<=B)(hk0:0<k0)(hk01:k0<=k1) :
∃ C rStar:ℝ, 0<=C ∧ 0<rStar ∧ rStar<=1 ∧ rStar<=L/2 ∧
  ∀ r,0<r→r<=rStar→∀ b k,|b|<=B→k0<=k→k<=k1→
    let QW=sourceCompactFoldWeightedLaw hL.ne' r b k
    let E=sourceIntrinsicFiniteBarEvent L r
    let p=sourceIntrinsicFiniteBarProbability hL r b k
    IsProbabilityMeasure QW ∧
    QW.real E^c=1-p ∧
    0<=p ∧ p<=1 ∧ 0<=1-p ∧ 1-p<=C*r^3.
```

Take C from qualified44 and rStar as half the minimum of44's radius and the prospective intrinsic actual-law radius. Transfer its same Good→literal IsFiniteBar event through existing QW≪sourceGapLaw. Use E's proved Borel property and actual probability normalization for the complement identity. No extra inverse, numerator, normalizer, Gaussian/Morse or geometric certificate appears as a final premise; C/rStar precede r,b,k.

Additional public propositions require root acknowledgement before freeze. All norm-space cut/death/type/AE inclusion/measure-transfer helpers remain private and fully inventoried.

## Required private mathematical joins

1. On E2→ᵇℝ, fixed M and h, prove the **existing** strict-clearance event open using the strict older-endpoint margin and the old attained compact-path minimum. Supremum-norm perturbations retain the same endpoint/path witnesses.
2. Nonempty clearance is a countable union of rational open cuts; its complement is Borel. For guarded death D with empty default0, prove
   `{F|h<D} = O_h ∪ (if h<0 then EmptyCut else∅)`.
   Use `measurable_of_Ioi` to obtain Borel death, and old C263/51 for exact nonessential/whole-cut characterization. Do not replace the guarded definition by an unguarded supremum or omit its empty branch.
3. Build the actual norm-Borel scalar field map from the already qualified order-zero derivative BCF by bounded fixed evaluation and literal-coordinate precomposition. Public `compLeftContinuousBounded` and `compContinuousCLM` give the operators; no new C3-torus function-space identification or quotient path lift.
4. Prove the exact literal planar type criteria on actual smooth fields: criticality via the two derivative coordinates; maximum iff a<0,det>0; saddle iff det<0. Use actual Hessian coordinate transport/symmetry and complementary-sign subspace definitions. Handle the zero-diagonal indefinite case; old square-completion sufficiency alone is not the full equivalence. Derive the finite jet observations Borel using qualified norm-Borel derivative maps at orders0/1/2.
5. Express the intrinsic full cut equality as nonempty cut plus guarded death=g(S), and combine with genuine types, positive fixed distance and positive gap. This yields E itself Borel without global-Morse or arbitrary-interface assumptions.
6. Compose only existing44 probability/Good-complement estimate, AC and prospective chosen-interface actual Good→IsFiniteBar theorem. AE complement inclusion plus finite measure monotonicity and `probReal_compl_eq_one_sub` gives the actual mass/probability result.

Choose this Borel route once; do not add a second weighted-support/conditional-Morse measurability construction. If Borel/type joins remain unfinished, label any available bound as outer mass only and do not call it the stated actual event probability.

## Finite meaningful controls and one mutation

- Generic zero/constant BCF: empty older cut, guarded death0 and correct upper-cut preimages on both sides of0. No essential default produces an intrinsic threshold pair.
- Exact finite Hessian cases: negative definite diag(−1,−1), saddle diag(1,−1), and zero-diagonal saddle `[[0,1],[1,0]]`; ordinary XY normalization and `det[[1,2],[2,3]]=−1`.
- Actual r=0: M=S, so the literal positive height-gap conjunct makes E empty. This is an event control, not a probability/radius claim at singular pins.
- Actual L=2,B=3,k0=1,k1=2 with symbolic r in the existential interval and all allowed b,k: literal E, actual QW mass, complement identity and C*r³ bound. No numerical effective radius or invented Good sample.

**Sole mutation:** remove the empty-cut branch from the new guarded-death Ioi-preimage formula. The zero BCF at h=−1 has D=0 and no older point, so −1<D is true and O_(−1) false. Reuse the established old empty-cut/default mathematics; prove only the concrete norm-BCF instance required by the new preimage formula. Root freezes one separately passed witness and one intended-False harness; no fabricated source realization, unrelated type/import/linter failure or additional mutation campaign.

## Completion boundary

This identifies the actual fixed-axis probability of the chosen intrinsic literal finite-bar event and bounds its failure. It does not identify an arbitrary PL.p, prove all-frame Parent A, establish canonical global finite-event labels/once-counting, or give Rice/density/count results. The actual local interval on Good and the off-Morse intrinsic threshold extension retain their existing exact scope. Future frame transport must preserve the original lattice/source/law and prove the actual event correspondence, not assume global O(2) invariance.

Root's future new-only exact-source qualification covers all owned private/generated/data/public declarations and affected controls, one kernel and one mutation, preserving all failures/commands/streams/exits/times/source-object lineage. No old evidence freshness replay, no admissions/custom axioms/native_decide/implemented_by/umbrella import. Provider-distinct/process and scientific acceptance remain separate.

Canonical standing authority (links alone do not establish reading):

- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OWNER_MANDATE_20261015.md
- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OP-AUTONOMY-20260923-v2.1.md
