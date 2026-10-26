# Bounded next contract: flat-torus C^K interface

Read-only author-side reconnaissance by OpenAI/Codex
`/root/uniform_jet_moment_sources/torus_interface_recon`. No proof compilation,
old verification, production edits, or scientific-review credit. The already
qualified norm-Borel theorem is reused unchanged.

## Source target and current exact boundary

GP-DER-197 published export lines 211–253 requires `X=C^3(T_L^2;R)` with the
usual C3 norm, Borel conditional law, and continuous gradient map to C2/C1.
The source fixes L=24. Its exact public blob is
`13067e7547e4f1913dd55cf5173fe5b02b6f9816`.

`SourceSmoothTopology.compatiblePeriodicJets d L K` is already the exact bounded
periodic real-cover C^K jet model. Its zeroth component determines the whole
underlying global field, and it already has the actual norm-Borel source map and
conditional laws. What is absent is a defined normed space of torus C^K fields
and a proved identification with that global model. Do not treat this as absent
norm measurability of the actual jets: that theorem is complete.

## Smallest useful successor

Use positive side length p (L=24 for the source application). For arbitrary
nonzero signed source L, p=|L| is also a valid period; that small sign bridge
preserves the literal field and avoids adding positive-L as a source-law premise.

1. Define `FlatTorusCk d p K` as bundled scalar `ContMDiff K` functions on the
   EXISTING `I4TorusC4.actualChartedSpace`; alternatively bundle a function F with
   `ContDiff R K (F o torusProjection d p)` and prove this is equivalent to that
   same chartwise manifold definition. The alternative is not an assumed
   realization: establish both implications using quotient charts.
2. For a compatible global jet, descend its unique witness f to the torus by
   `F q = f(torusRepresentative d p q)`. Prove independence of representative,
   exact pullback `F o projection=f`, and C^K in the existing flat charts.
3. Conversely, pull back any F in that torus C^K space. Prove C^K of the pullback,
   periodicity, and periodicity of every actual iterated derivative. Descend each
   derivative to a continuous torus-valued operator map, use compactness to bound
   it, and form the actual compatible BCF tuple.
4. Prove these maps inverse (global zeroth-jet uniqueness and projection
   surjectivity). Define the norm through this actual derivative tuple; its
   topology is then genuinely the maximum uniform derivative topology on the
   torus. Prove the exact norm equality between torus derivative suprema and
   global-cover suprema using projection surjectivity, not a continuous section.
5. Compare this norm with a declared conventional C^K norm. Max and sum across
   K+1 orderwise operator norms obey max<=sum<=(K+1)max. If conventional partial
   derivatives are used, for the existing l-infinity domain norm, each ordered
   coordinate derivative is <= the k-linear operator norm and the operator norm
   is <= d^k times the largest ordered-coordinate derivative. In d=2,K=3 the
   safe uniform factor is 8. Passing ordered derivatives to multiindices uses
   derivative symmetry. A Euclidean convention requires its finite-dimensional
   change-of-norm bounds instead; it is not automatically isometric.
6. Push the existing actual norm-Borel source/conditional maps through this
   proved continuous equivalence. This gives the same torus C3 Borel law and
   conditional law for every measurable functional. The already proved
   eventual current covariance invertibility discharges the final hL-only law.

This successor can stop after the explicit C3 topological equivalence and law.
Completeness/separability are needed to reproduce GP197's exact phrase
"separable Banach" or use generic standard-Borel constructions; they are not a
premise for composing the ALREADY explicit kernel. A Borel capture theorem on
the conventional C3 target still needs its selector/flow source join.

## Reusable exact source APIs

- `inputs/SourceTorus.lean`: `SourceTorus=Fin d -> AddCircle p` (line 14),
  projection (16), measurable representative (19), projection-representative
  right inverse (35), lattice-equivalence proof (40), actual field pullback
  (58). The latter proof generalizes directly to ANY periodic f.
- `inputs/SourceTorusC4.lean`: quotientChart (13), chart inverse literally
  projection (20), chart covering (24), actualChartedSpace (43), chart
  transitions locally translations (52), manifold structure (99), and the
  `torusSourceField_contMDiff_ae` proof pattern (111). Replace its ae hypothesis
  by a compatible witness's actual `ContDiff` proof to obtain an EVERY-field
  descent theorem. No old theorem needs editing or rerunning.
- `SourceSmoothTopology.lean`: actual all-order periodicity and compatible
  witness uniqueness are already public. The current topology is the maximum
  operator-derivative topology, with explicit metric criterion.

## Pinned Mathlib API / honest gaps

- `Topology/Algebra/Group/Quotient.lean`: generated additive analogues of
  `QuotientGroup.isOpenQuotientMap_mk` (line 55),
  `QuotientGroup.isQuotientMap_mk` (40), and `isOpenMap_coe` (52).
- `Topology/Constructions.lean`: `IsOpenQuotientMap.piMap` (808), so the finite
  product torus projection is an open quotient. This is the clean generic
  descent-continuity route. `Topology/Maps/Basic.lean`:
  `IsQuotientMap.continuous_iff` (360). Product quotients should not be inferred
  from an arbitrary product of quotient maps; the open-quotient result is exact.
- `Topology/Instances/AddCircle/Defs.lean`:
  `AddCircle.continuous_mk'` (227), `coe_eq_zero_iff` (215), `liftIco_continuous`
  (833). The one-dimensional lift is available but iterated representative
  continuity is not the correct global-section argument.
- `Topology/Instances/AddCircle/Real.lean`: compactSpace for positive period
  (33). Finite product compactness supplies compact torus; its projection is
  surjective independently of compactness.
- `Geometry/Manifold/ContMDiffMap.lean`: the bundled ContMDiff map type and
  ContinuousMapClass exist, but this file defines NO C^K norm/topology or Banach
  structure. Taking that type alone does not solve the function-space join.
- `Topology/ContinuousMap/Compact.lean`:
  `ContinuousMap.linearIsometryBoundedOfCompact`; compact continuous operator
  fields can be interchanged with BCFs with the sup norm.
- `Topology/ContinuousMap/SecondCountableSpace.lean`: second-countable
  continuous-map space (84), separable continuous-map space (108), for locally
  compact second-countable domain and second-countable target. Periodic jets
  descend to a finite tuple of these compact-domain spaces, so no assertion
  that all real-cover BCFs are separable is needed.
- `Analysis/Calculus/UniformLimitsDeriv.lean`:
  `hasFDerivAt_of_tendstoUniformly` (430), or locally-uniform version (398), is
  the core API for closedness of derivative compatibility if completeness of
  the compatible-jet subspace is required. This higher-order induction has NOT
  been implemented here.
- `Analysis/Distribution/ContDiffMapSupportedIn.lean`: a useful model of the
  same derivative-structure-map topology (`structureMapLM`, 489;
  `isUniformEmbedding_pi_structureMapCLM`, 582;
  `continuous_iff_comp_order_le`, 609). It applies to compactly supported
  Euclidean functions, not periodic torus functions, so it cannot be imported
  as a ready torus C3 Banach theorem.

The only genuine implementation cost is a new general function-space interface:
quotient/chart descent is narrow; selecting and implementing the conventional
norm plus derivative compatibility/complete-space structure is larger. None of
these are counterexamples or defects in the completed actual norm-Borel theorem.

Owner-mandate references carried into this handoff:
https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OWNER_MANDATE_20261015.md
https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OP-AUTONOMY-20260923-v2.1.md
