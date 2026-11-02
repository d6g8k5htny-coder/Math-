# Root-adopted PRECODE record — pending publication and actual pickup

This is the bounded prospective58 contract. The concrete companion SOURCE_FRAMED_CONFLUENT_COVARIANCE_CONTROLS.md is root-read. Implementation awaits actual PRECODE publication, native pickup, root control freeze and GO. Planned checkpoint21:30UTC/terminal23:45UTC26October/invocation end; these are not live timers before actual pickup. Historical design-only provenance below is preserved. No completed mathematics is rechecked for these process steps.

# Concrete control contract for prospective58 — SourceFramedConfluentCovariance

26 October2026. Prepared for ROOT FREEZE/GO from the adopted complete preflight and separate PASS review. This file does not claim a native pickup, published precode, source implementation or qualification. Root will supply the proper precode/native claim, checkpoint/terminal and implementation GO. Only this control contract and READINESS.md are authorized at this stage; no source, harness, helper implementation text, Lean/probe/check/build/kernel/audit/hash campaign or external action is authorized now.

Root owns shared metadata/config/cache/registry/Git/external publication. Future producer ownership is only the new SourceFramedConfluentCovariance.lean and this assigned scratch, subject to root GO. Prior55/56/57 source, helpers and frozen evidence are outside this task; none is a mathematical dependency or permission to inspect/change it.

## Exact public inventory and original carrier

Exactly THREE public data definitions, in I4SourceFramedConfluentCovariance:

1. framedConfluentCoefficient: seven actual original SourceMode2 coefficient rows, total in L,z,R,r.
2. framedConfluentVector: scalarSeries of those same seven rows against the original sampleInclusion2 L on SmoothSample2 L.
3. framedConfluentCovariance: exactly coefficientGram of framedConfluentCoefficient.

Exactly THREE public written propositions: framedConfluentVector_actual, framedConfluent_family_bounds, framedConfluent_covariance_uniform_floor. All needed coordinate/curve/finite-jet/trig/continuity/compact-matrix adapters, shorthands and generated declarations are private/inventory-only; no additional public type alias, envelope/square definition, covariance model, law, weight, event or probability object is introduced.

Use literal physical z:E2 and R:OrthonormalBasis(Fin2)ℝ(E2), e=R0,n=R1, with both orientations. Actual physical mode functions are the unchanged original modeCoefficient composed with I4LifetimeField.coordinates2. Samples/law stay SmoothSample2 L/smoothLaw2 L. All analytic propositions assume original signed L≠0, never replace it by |L| or silently use a Lifetime smoothness wrapper requiring0<L. Derive signed smoothness/chain rules from actualField=smoothSourceField∘coordinates and the public signed-source smoothness theorem.

## Frozen row ledger, parameters and conclusions

Let M=z−(r/2)e and S=z+(r/2)e. O6 is (F(M),F(S),D_e F(M),D_e F(S),D_n F(M),D_n F(S)) on the same original field/sample. Row order0..6 is:

- 0: endpoint average of F;
- 1: endpoint average of D_e F;
- 2: endpoint average of D_n F;
- 3: integral D_ee F(z+rte) over t∈[−1/2,1/2];
- 4: integral D_en F(z+rte) over the same interval;
- 5: SIX times integral (1/4−t²)D_eee F(z+rte);
- 6: D_nn F(z).

The coefficient family applies this identical ledger to each original mode. Row4 is the ordinary mixed derivative, with no off-diagonal normalization/factor2. Row5's Peano kernel has integral1/6; its prefactor6 gives contact cubic derivative1 on the normalized witness. At r=0, the vector is exactly (F,F_e,F_n,F_ee,F_en,F_eee,F_nn)(z). The six lower-jet positions are0,1,2,3,4,6; the first-six principal pin embedding is i:Fin6↦Fin.castAdd1 i, and the final transverse row is6:Fin7. These distinct index choices must not be conflated.

Prop1 concludes joint HasGaussianLaw on unchanged smoothLaw, exact coordinate covariance=the declared Gram, pointwise actual row6, pointwise actual contact7 at r=0, and for every signed r≠0 the first6 pointwise vector=public confluentTransform r O6. The zero value is the Peano extension, never a quotient assigned at0. Apply old scalar pin3/pin4/pin5 identities on actual directional curves. Prove samplewise series–Peano interchange using the carrier's finite sum of weighted order0–3 properties; it is not an assumed law. Use public scalar-series finite Gaussian/covariance and carrier transport, with no marginal-independence or rotated-sample shortcut.

Prop2 exposes the envelope by an explicit public-type let:
A#(m)=8*sum(j:Fin4,orderModeBound (j:ℕ) 2 L m).
It concludes A#≥0, weighted summability of orderModeBound ell*A# for EVERY ell:ℕ, the coefficient bound for every z,R,REAL r,row,mode, and the uniform entrywise contact limit. Summability of A# and A#² and samplewise sum |omega_m|A# are privately derived as needed. The public midpoint domain is transparent: for every a:Fin2, |(coordinates2 z)a|≤|L|/2. No inaccessible private square/envelope convention appears in a public proposition.

The contact-limit quantifier order is: for every eps>0, one delta>0 BEFORE z in that closed square, every literal frame R, every0≤r≤delta, and all seven row pairs. Moving-direction joint multilinear evaluation and fixed-interval Peano/Gram continuity are new private obligations, not a claim that the old fixed-direction continuity theorem already has these parameters.

Prop3 chooses gamma,Lambda,delta BEFORE midpoint/frame/radius/vector, with gamma>0,Lambda>0,delta>0,delta≤1,delta≤|L|/8. On the same explicit square and every R,0≤r≤delta it concludes, for every v:Fin7→ℝ,
gamma*sum(v_i²)≤v·(Gv)≤Lambda*sum(v_i²), with derived G.PosDef, principal G6.PosDef/invertibility and the SAME gamma lower bound on the transverse Schur expression. G6(i,j)=G(castAdd1 i,castAdd1 j). The exact Schur expression is G(6,6)−sum(i,j:Fin6,G(6,castAdd1 i)*(G6⁻¹)(i,j)*G(castAdd1 j,6)). No rank/witness/inverse/PosDef/Schur-floor certificate is a final premise.

## Required finite and compact joins

Use public qualified47 finiteTrig constructors/evaluation/toSource APIs and qualified48 public jet2/localGerm/localGerm_jet2/jet2_mul only. Public jet2_scale/jet2_sum/basis APIs were not exported; any finite-linearity adapters are new private work, not fictitious dependencies. Rebuild finite trig representations through public constructors, without old private germPoly/row-pairing names.

For e=(a,b),n=(c,d), the lower-jet coordinate rows are value; a Fx+b Fy; c Fx+d Fy; a²Fxx+2abFxy+b²Fyy; acFxx+(ad+bc)Fxy+bdFyy; c²Fxx+2cdFxy+d²Fyy. The full determinant is Delta⁴=1 for Delta=ad−bc=±1. Both orientations and ordinary XY are mandatory. With alpha=2pi/L, choose j with e_j≠0 and use the normalized axis sine cube (sin(alpha(x_j−z_j))/alpha)³/(6e_j³): its lower jets vanish and D_e³ at z is1. Match the lower six targets, then correct target5 independently with that cube. Construct actual finite original-mode directions and pairings, not a supplied interpolation/rank certificate. Apply old separating-Gram positivity.

Each individual frame vector's source Pi norm is≤1. Do not claim the full frame map from a product/max norm is contractive or coordinates is a Euclidean-to-Pi isometry. Use A#² domination and finite multilinear evaluation for joint Gram continuity. Compact closed frame pairs (norms1,inner0), the closed midpoint square and the Euclidean unit sphere give a DERIVED positive contact minimum m. The entrywise perturbation bound is |vᵀDeltaGv|≤7eta*sum(v_i²); eta=m/14 yields gamma=m/2. Choose the closed radius endpoint inside an open continuity neighborhood, then intersect with1 and |L|/8. The quantitative Schur lower bound follows by the vector (−G6⁻¹b,1), whose squared norm≥1. Old contact_schur_pos alone supplies strict positivity, not this common numeric gamma. No eigenvalue/parameter-family library or source-law rotation assumption is introduced.

## Meaningful positive controls after root GO

All are new-family application controls; old proofs/objects/checks are reused unchanged.

1. Standard frame, z=0: first6 agree with the accepted fixed-axis confluent pins for signed nonzero r, and r=0 matches exact contact order0,1,2,3,4,5,6 above. Verify only the new specialization join, not the old pin/contact proofs.
2. Normal reflection e unchanged,n↦−n: actual coefficient row signs are (1,1,−1,1,−1,1,1); row2 and ordinary mixed row4 change sign, row5 and row6 do not. This exercises orientation−1 and deterministic Gram sign congruence; it is not arbitrary O(2) invariance.
3. Actual rational non-axis frame e=(3/5,4/5),n=(−4/5,3/5), physical midpoint coordinates(1/3,−1/5), original L=−2 and signed nonzero r=−1/3: instantiate actual row/Peano/vector identities and covariance API on the unchanged source. Also use the reflected n to exercise the other orientation. No equality with the standard-frame covariance is asserted.
4. Envelope API exposes exactly factor8 and Fin4 orders0..3; exercise a weighted order above3 (e.g.ell7) to prevent a finite-C3 surrogate. Bounds remain all-z/all-real-r. Individual source-coordinate direction bounds are separate from the false full-map contraction claim.
5. At L=−2 and the concrete midpoint in the explicit fundamental square, instantiate the uniform lower/upper/principal/Schur conclusion for the rational frame and its reflection with the SAME existential gamma,Lambda,delta. Test r=0 and, symbolically,r=delta/2. No fabricated effective numerical radius or floor is required.
6. Independently establish the finite original-source sine-cube witness below, with lower jets zero, correct cubic contact pairing1 and omitted-factor pairing1/6.

## Sole mutation, frozen before any implementation

The ONLY mutation removes factor6 in row5's Peano coefficient formula while retaining the contact identity. Fix L=2,z=0,standard e=ex,n=ey,r=0. Build an ACTUAL finite original-mode direction v using public finiteTrig/toSource_derivative for f(x,y)=sin(pi*x)³/(6*pi³). Prove lower jets0 and physical D_e³f(0)=1, then prove finitePairing(correct row5,v)=1 and finitePairing(mutant row5,v)=1/6. This passed positive mismatch must exist before ONE separate intended-False harness. The harness targets exactly the missing-factor contact identity and reduces that concrete contradiction to ONE False; unrelated diagnostics are not rejection evidence.

Do not edit the actual source for the mutation, invent a positive-probability Gaussian realization, or run an alternative negative campaign. In particular, do not claim rank collapse: a nonzero row scaling can preserve positive definiteness.

## Qualification and completion boundary

After proper native claim/root GO, qualify only this genuinely new module/private adapter inventory/controls. Retain every actual attempt/source+harness snapshot/command/time/exit/full produced stream and helper lineage. Reuse exact-byte successful strict evidence after freeze; exhaustive actual-module ownership inventory includes private/data/generated/foreign-generated constants; only standard-three axioms/subsets, no admissions/custom axioms/native_decide/implemented_by/umbrella Mathlib/foreign private API. Exactly ONE final own-module kernel, meaningful positive controls, and one counterexample-backed sole-False mutation. No .ilean freshness compile, full Lake build, old dependency/kernel/audit/control/hash campaign or producer production-cache copy. Approved helpers, if root later assigns them, are text-only, frozen before once integration, zero execution/object/campaign/target credit.

Stop after actual source7 Gaussian/Gram identification, every-order weighted envelope, compact-uniform contact limit and DERIVED G7/principal/Schur floors. No posterior/conditional law, physical weight, event Borelness/mass, all-frame IsFiniteBar, normalized probability, PL object, canonical selector/global elder, Morse/tie/Rice/count/Parent theorem is claimed. Qualified conventional mathematics remains reusable. Different actual-family review/process remains separate from mathematical verification. Scientific effect NONE; same-family/provider-distinct/organizational independence credit0.

Canonical authority carried for onward onboarding; link delivery does not establish reading:

- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OWNER_MANDATE_20261015.md
- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OP-AUTONOMY-20260923-v2.1.md
- https://github.com/d6g8k5htny-coder/main/blob/main/governance/OWNER_DECISION_20261025_REVIEW_FAMILIES.md
