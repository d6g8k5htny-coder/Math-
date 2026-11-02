# Frozen precode — SourceIntrinsicH0Interface

Root-requested exact design, 26 October 2026. New module `SourceIntrinsicH0Interface.lean`, namespace `I4SourceIntrinsicH0Interface`. This packet precedes any future native pickup or code. It is not an implementation, qualification or scientific result. Root fully read and adopted this contract and its complete source/API preflight review before native claim/code. Same-family/provider-distinct credit0; scientific effect NONE.

Read with the adopted feasibility report `/workspace/scratch/intrinsic-h0-interface-preflight/REPORT.md`. Qualified51 is already published (`d6af030`, RESULT6421767087), with exact production source unchanged. Existing C263, ordinary-H0, actual candidate/death/torus/summand and conventional compact-Morse/barcode evidence are reusable. No old build, kernel, audit, controls, hash campaign or mathematical review is restarted because this is a new module, agent, session, handoff or process requirement.

## Exact new semantic content and hard boundary

Construct a literal `UniversalLaw.Spec.Lifetime.SuperlevelBarInterface d L` from the actual ordinary-H0 older-merger time cut of51. Its pair relation is defined by the complete H0-map vanishing cut plus genuine endpoint types. It is not defined merely by the desired scalar equality of a chosen death number and saddle height.

For this explicitly chosen intrinsic interface, the accepted actual local-fold candidate event yields literal `IsFiniteBar` and retains the same actual torus cut and genuine interval/complement. No supplied global `IsMorseDistinct` is needed for this local consequence: this interface's off-Morse extension has an explicit homology-map definition.

For an arbitrary supplied interface I, transfer of the relation/literal finite-bar predicate remains explicitly conditional on smoothness, periodicity and supplied `IsMorseDistinct`. Essential death values are not determined by that record's maximin clause, so no total equality of arbitrary interface records or their essential death defaults is asserted.

No global canonical finite-event labels, chosen saddle function, exhaustive barcode, once-counting, Borel/count identity, global a.e. Morse theorem, probability estimate, actual PairLaw identification or Parent A/B claim is included. The `ElderPartner` record field name does not turn the H0 threshold-pair extension into a separately established canonical global labeling. No generic quotient path-lifting theorem is required for the local result.

## Imports and definitions

Expected direct imports only:

```text
import SourceH0OlderClearance
import SourceActualFoldCandidate
```

No endpoint52 dependency, new field library, umbrella Mathlib or private foreign API. Use the literal Lifetime namespace/types, with E definitionally the old C263 carrier. Coefficients of the interface itself are fixed to ℝ; its supporting local actual torus interval remains available for each arbitrary field K.

For private implementation, set

```text
C(g,M) := {h : ℝ | I4SourceH0OlderClearance.h0OlderClearance ℝ g M h}.
D(g,M) := if C(g,M).Nonempty then sSup C(g,M) else 0.
```

These may be private definitions or local abbreviations. The default0 is only a total real empty-cut convention, not an essential ordinary-H0 death. The actual maps are exactly the already qualified51 maps: [M]−[P] at birth time −g(M), actual closed-superlevel inclusion to −c, a strictly older P and h<c≤g(M). Do not reimplement those maps, their component comparison or the compact path minimum.

Exactly **two authored public definitions** are frozen:

### `h0ThresholdPair`

```lean
 def h0ThresholdPair {d : ℕ} (g : E d → ℝ) (M S : E d) : Prop :=
   IsNondegMax d g M ∧ IsIndexSaddle d g S ∧
     {h : ℝ | h0OlderClearance ℝ g M h} = Set.Iio (g S)
```

This definition is total and has no smoothness, periodicity, Morse or continuity argument. Its whole-cut condition forces a nonempty cut and thus an actual older endpoint; essentiality cannot slip in through the scalar default0. Genuine maximum/saddle types remain conjuncts. It is a threshold relation; it does not choose an individual merger saddle.

### `h0Interface`

```lean
 noncomputable def h0Interface (d : ℕ) (L : ℝ) :
     UniversalLaw.Spec.Lifetime.SuperlevelBarInterface d L
```

Freeze its data fields to:

```text
 deathHeight := D
 IsEssential := TorusFiltration.superlevelBar_isEssential
 ElderPartner := h0ThresholdPair
```

Populate the three proof fields from51/C263 as described below. Do not take an existing desired interface as input. The constructor exists for all d,L because its fields are conditional; the actual source application retains the old meaningful `0<L` premise.

## Exactly three authored public propositions

Signatures below are specifications, not elaboration-checked declarations. Open the already accepted namespaces for readable names; qualification may be inserted without changing types. Necessary private helper propositions/data and all generated declarations remain separately inventoried.

### 1. `h0Interface_cut_death_eq_C263`

```lean
 theorem h0Interface_cut_death_eq_C263
     {d : ℕ} (L : ℝ) (g : E d → ℝ) (hg : Continuous g) (M : E d) :
     {h : ℝ | h0OlderClearance ℝ g M h} =
         TorusFiltration.superlevelBar_clearanceSet g M ∧
       (h0Interface d L).deathHeight g M =
         TorusFiltration.superlevelBar_deathHeight g M
```

This includes essential points **only for the explicitly constructed intrinsic interface**, whose empty default is fixed. Proof:51 generic equivalence and definitional C263 clearance equality give the set equality; substitute it into the two guarded-supremum definitions. No new compactness, homology or supremum theory.

Construction helpers may also prove, privately, the generic continuous threshold-pair characterization:

```text
h0ThresholdPair g M S ↔
  IsNondegMax d g M ∧ IsIndexSaddle d g S ∧
    ¬ superlevelBar_isEssential g M ∧ D(g,M)=g S.
```

Forward uses nonemptiness of Iio(g S), actual older-endpoint existence from the H0 predicate, and its supremum. Reverse uses51's nonessential real-cover cut. This characterization is stronger than the record's supplied-Morse clause, so that clause's Morse premise may be unused; it is not thereby proved a.e.

### 2. `h0Interface_morse_compatibility`

```lean
 theorem h0Interface_morse_compatibility
     {d : ℕ} (L : ℝ) (I : SuperlevelBarInterface d L)
     (g : E d → ℝ) (hs : IsSmooth d g)
     (hp : IsLPeriodic d L g) (hm : IsMorseDistinct d L g)
     (M S : E d) :
     (I.ElderPartner g M S ↔ h0ThresholdPair g M S) ∧
       (IsFiniteBar d L I g M S ↔
         IsFiniteBar d L (h0Interface d L) g M S)
```

Essentiality agrees directly. Compare a supplied I's death to D only under explicit nonessentiality, using equality of strict cuts; do not compare essential default values. Then use I's supplied-Morse pair clause and the intrinsic characterization. The literal finite-bar equivalence follows with candidate/gap conjuncts unchanged.

No conclusion about arbitrary I is asserted off the supplied Morse locus. No equality of record objects is asserted.

### 3. `sourceGapLaw_intrinsic_h0_finiteBar_uniform`

```lean
 theorem sourceGapLaw_intrinsic_h0_finiteBar_uniform
     {L : ℝ} (hL : 0 < L) :
     ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧ δ ≤ L/2 ∧
       ∀ (K : Type) [Field K],
       ∀ k₀ : ℝ, 0 < k₀ → ∀ r : ℝ, 0 < r → r < δ →
         ∀ b k : ℝ, k₀ ≤ k → ∀ᵐ sample ∂sourceGapLaw hL.ne' r b k,
           let T := sourceT k₀ sample
           let κ := sourceKappa r k sample
           let g := actualField 2 L sample
           let M := I4SourceActualFoldCandidate.endpointLiftM r
           let S := I4SourceActualFoldCandidate.endpointLiftS r
           let F := SourceActualFoldTorus.actualTorusField hL.ne' sample
           let Mbar := I4Torus.torusProjection 2 L (endpointM r)
           r*T^5 ≤ 1/100 → 1024*T^5 ≤ κ →
             IsFiniteBar 2 L (h0Interface 2 L) g M S ∧
             g M = b ∧ g S = b-k*r^3 ∧
             (h0Interface 2 L).deathHeight g M = b-k*r^3 ∧
             {h : ℝ | h0OlderClearance ℝ g M h} = Set.Iio (b-k*r^3) ∧
             {h : ℝ | h0OlderClearance K F Mbar h} = Set.Iio (b-k*r^3) ∧
             ∃ C : ℝ ⥤ ModuleCat K,
               Nonempty (TorusFiltration.superlevel_h0Filtration F
                   (ModuleCat.of K K) ≅
                 TorusFiltration.elderInterval K b (b-k*r^3) ⊞ C)
```

Take exactly the radius and a.e. event from accepted `sourceGapLaw_actual_candidate_death_h0 hL`; it already includes both real/torus strict cuts, literal candidate types, positive gap, exact heights and the actual interval/complement. Transfer its real cut through51 to `h0ThresholdPair`; obtain literal `IsFiniteBar` by conjunction with accepted candidate/gap facts. Transfer the same sample's torus cut through51 and accepted torus continuity. Keep the old interval/complement unchanged. No second source-law event intersection is necessary.

Radius remains before K and all marks; a.e. remains inside each fixed target. Same original positive period, source law, sample, actual field, actual torus, endpoint lifts/projections, absolute levels and exactly the two existing sample cutoffs. No common event over uncountably many marks, no inverse/trap/global-Morse premise, no new effective radius. The public theorem deliberately uses `0<L` inherited from the literal candidate application;51's signed `L≠0` theorem remains unchanged.

The two cut equalities imply agreement of their real suprema with b−k r³ by existing `csSup_Iio`; no extra public proposition is needed for this one-line consequence.

## Finite meaningful control contract, frozen before future source

A future producer first freezes concrete harness names before code, retaining this bounded scope. Harness imports only the new module and existing narrow APIs. No control-only dependency additions.

1. **`constant_essential_default_and_no_pair`.** On literal E1, L=2, constant g=7 and M=0: the actual H0 older-endpoint cut is empty, intrinsic essentiality holds, intrinsic death is0, and `h0ThresholdPair g M S` is false for every S because the cut cannot equal a nonempty Iio. This checks the empty-default guard and prevents a default from being treated as an actual finite death.
2. **`linear_numeric_death_not_a_pair`.** On E1 use g(x)=x(0), M=S=0. Its actual H0 transition cut is Iio0, its intrinsic death and g(S) are both0, and M is nonessential, but it is not a genuine maximum (its derivative is nonzero), so the threshold pair is false. This is a new-interface control of the type conjuncts and of the failure of numeric death equality alone; it is not an old H0-control replay. Use the existing linear functional/derivative APIs and51, without a new homology proof or library.
3. **`essentialShiftInterface` and `essential_default_counterexample`.** Construct a scratch-only valid supplied interface on d=1,L=2 by retaining intrinsic essentiality and relation, and setting its death to17 at essential points and to the intrinsic death at nonessential points. Its maximin field is unchanged on its guarded domain. In its pair field the nonessential conjunct ensures the relevant death value is also unchanged. At constant g=7,M=0, this valid interface has death17 while the intrinsic interface has death0. Prove that concrete inequality separately. This control demonstrates why arbitrary supplied interfaces' essential defaults cannot be total-equal.
4. **`actual_positive_period_uniform`.** Instantiate proposition3 at L=2,b=3,k₀=k=1, with symbolic positive r in the existential interval, and every coefficient field K already allowed by the theorem. Check literal `IsFiniteBar` for the chosen intrinsic interface, absolute death3−r³, both actual H0 cuts and the exact actual torus interval/complement. Retain the same two cutoffs and δ before K/r. No concrete sample satisfying cutoffs or numerical effective radius is invented.
5. **`actual_given_interface_requires_morse`.** On that same symbolic actual sample/event, for arbitrary supplied I, keep an explicit `IsMorseDistinct 2 2 g` hypothesis and transfer the passed intrinsic literal `IsFiniteBar` through proposition2. Do not assert or derive this premise from the two local endpoint types. Existing actual smoothness/periodicity are consumed.

No characteristic-two control is requested:51 already supplies the coefficient-independent semantic join, and its retained narrow-import availability attempt found no Field(ZMod2) instance. No replay or new field library is justified here.

## Exactly one honest counterexample mutation

**Sole mutation:** remove the nonessential guard when comparing an arbitrary supplied interface's deathHeight with the intrinsic death. This targets the exact boundary used in the private supplied-interface comparison underlying proposition2. It is not a mutation of51, an unrelated source failure or a broader negative campaign.

A separately passed `essential_default_counterexample` from control3 supplies an actual inhabitant `essentialShiftInterface : SuperlevelBarInterface 1 2` and the concrete constant g=7,M=0 values17 and0. The sole scratch negative `FalseEssentialDefaultMutation.lean` asserts equality of those two values, i.e. the unguarded comparison specialized to this actual case. Simplifying by the separately passed value facts leaves exactly one intended `False` goal.

No hypothetical arbitrary false equivalence, inaccessible private API, missing import, type/linter failure or fabricated sample counts as rejection. The mutable claim is precisely “remove ¬essential from supplied-I death comparison”; the constructor's guarded total-default behavior and production relation stay frozen. Do not replace this by a broad symbolic unsolved goal. Run one concrete negative attempt only after its witness controls pass; preserve all actual failures and streams. The alternate interface/control objects are never production eligible.

## Qualification and process boundary

Future qualification is new-module-only: exact strict source evidence reused after freeze; exhaustive actual owned-module inventory including private/generated/data/public/foreign names; standard axioms only (`propext`, `Classical.choice`, `Quot.sound`); finite mandatory controls; one sole-False concrete mutation; exactly one own-module leanchecker; final actual source/spec review. No .ilean freshness compilation. Preserve every new attempt/source/harness/command/time/exit/full original streams and source-object lineage. No sorry/admit/custom axiom/native_decide/implemented_by/umbrella import.

No unchanged old H0/C263/candidate/source/torus/kernel/controls/hash campaign is rerun. Pending provider-distinct alignment, hosted checks, registry/Git/publication and actual scientific-source identification remain separate process requirements; they do not erase completed mathematics. Root alone owns shared config/cache/registry/Git/external publication. Producer owns only the future new source and its assigned scratch; no concurrent source is inspected or consumed. A new pickup must receive its own root-recorded timing; no old timer is restarted by this design.

Canonical onward authority; links alone do not establish reading:

- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OWNER_MANDATE_20261015.md
- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OP-AUTONOMY-20260923-v2.1.md
