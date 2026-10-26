# Frozen precode: two actual remote first jets, finite witnesses and residual Gram

26 October2026. Root adopted and froze this bounded specification after the read-only preflight and technical review; neither implementation nor qualification is claimed by this document. The original scratch draft remains preserved. Proposed module `SourceTwoRemoteFirstJetWitness.lean`, namespace `I4SourceTwoRemoteFirstJetWitness`. REPORT records the public API assessment, concrete construction and boundaries. Root owns native pickup, implementation authorization, exact pre-source concrete control freeze, qualification, cache/registration and external publication.

Reuse qualified47/48 trig/source/jet/finite-kernel/Gram evidence and all accepted applicable mathematics. No in-flight52 code/helper is consumed. Owner `/workspace/AGENTS.md` requires completed verification reuse and prohibits rechecking unchanged material merely for a new agent, session, freeze or handoff. New/changed obligations alone warrant scoped checks; mathematical evidence and pending independent/provider-distinct process remain separate. Scientific effect NONE; credit0.

## One public data definition

```text
twoRemoteFirstJetCoefficient (L:ℝ) (x y:Fin2→ℝ) :
  Fin6 → SourceMode2 → ℝ
```

Literal order is `(valueX,dxX,dyX,valueY,dxY,dyY)`: first three public48 `remoteJetCoefficient` rows at x followed by first three at y. Original signed real period, source modes, weights and ordinary derivatives are retained. No observation, covariance, residual, multiplier, interpolant or desired-result data structure needs public definition.

Write `a=rawPinCoefficient L r`, `B=twoRemoteFirstJetCoefficient L x y`; raw rows remain `(fM,fS,fxM,fxS,fyM,fyS)`.

## Exactly two public written propositions

The following are specifications, not elaboration-checked signatures. Both take precisely:

```text
{L:ℝ} (hL:L≠0) (r:ℝ) (x y:Fin2→ℝ)
(hxM:pi_L x≠pi_L(endpointM r))
(hxS:pi_L x≠pi_L(endpointS r))
(hyM:pi_L y≠pi_L(endpointM r))
(hyS:pi_L y≠pi_L(endpointS r))
(hxy:pi_L x≠pi_L y),       pi_L=torusProjection 2 L.
```

No endpoint/endpoint separation or nonzero/positive radius is added. r=0 and repeated quotient pins remain allowed.

**1. `actual_finite_twoRemoteFirstJet_witnesses`**

```text
∃ v:Fin6→(SourceMode2→₀ℝ),
 (∀ i s, finitePairing (a i) (v s)=0) ∧
 (∀ j s, finitePairing (B j) (v s)=if j=s then1 else0)
```

Witnesses are internally constructed actual finite original directions. No supplied witness, interpolation/rank certificate or desired right-inverse premise.

**2. `actual_twoRemoteFirstJet_residual_coefficientGram_posDef`**

For every `R:Matrix(Fin6)(Fin6)ℝ`,

```text
(I4ContactGram.coefficientGram
  (I4SourceFinitePinKernel.residualCoefficient a B R)).PosDef.
```

Apply the already qualified generic `coefficientGram_posDef_of_finite_kernel_rightInverse` at p=q=6 using proposition1 and local row summability adapters. No supplied PosDef, pin inverse, target or probabilistic premise. Additional public propositions need root acknowledgement before freeze; private/generated/data remain inventory-only.

## Required minimal construction

For each chosen remote p with other remote q, choose independently one coordinate separating p from each of M,S,q. For each avoided point use `(1-cos(c*(z_j-a_j)))²`, c=`sourceC L`. Multiply the three factors into P. Literal quotient separation and public period facts derive `A=P(p)>0`; the appropriate vanishing squared factor gives value/gradient0 at M,S,q. Only first-jet vanishing is required.

Use existing `localGerm c p 0/1/2`. For a target first jet tau, set

```text
a0=tau0/A,
a1=(taux-dP(p)[X]*a0)/A,
a2=(tauy-dP(p)[Y]*a0)/A,
F=P*(a0*g0+a1*g1+a2*g2).
```

Public germ identities plus ordinary first-derivative rules give tau at p and zero first jets at the three avoided points. No full second-jet inverse, Hessian constraint or six-germ interpolation is needed. The reused public `jet2_mul` may supply only its first three product coordinates if useful.

Build the actual finite polynomial for F with qualified47 operations and convert via `toSource`. Construct three basis functions at x and three at y, then concatenate. Their cross-remote first jets are zero, so the joint B6 pairings are the literal identity. Pin pairings use the original raw rows. Represented finite lists may have duplicate frequencies; accepted47 semantics already handles those.

Keep all coordinate-positivity/period adapters, smoothness/product/combination proofs, finite polynomial data/evaluation, row-pairing and summability adapters private. Do not access48's private helpers or change upstream sources to expose them. Reuse old germ/finite-trig/source/Gram proofs without another mathematical campaign.

## Required pre-source concrete control contract

Producer acknowledges and freezes the concrete finite harness before source or any text-helper implementation:

- At L=2,r=0,x=`![1,0]`,y=`![0,1]`, instantiate actual witness directions: all36 raw zeros and all36 observation identity entries. Repeated pins and different coordinate choices are genuine.
- Distinct target vector `(1,2,3,4,5,6)` checks the actual concatenated first-jet order.
- Signed L=-2 on the repeated-pin instance, plus a negative-radius instance L=2,r=-1,x=`![0,0]`,y=`![0,1]`.
- Arbitrary-correction PosDef at R=0 and concrete nonsymmetric `R j i=(j.val+1)*(i.val+2)` as reals.

**Sole mutation:** omit only hxy. At L=2,r=0,x=y=`![1,0]`, hL and all four remote/pin inequalities remain true, with exact integer-parity proof that `(1:AddCircle2)≠0`. New coefficient rows0 and3 coincide. Column0's desired identity equations demand their same finite pairing equal1 and0, proving nonexistence. Root freezes one separately proved collision counterexample and one sole-False mutation harness, with no unrelated diagnostics counted as rejection. This refutes the desired joint witness theorem, not merely the particular construction.

## Completion boundary

This leaf proves joint first-jet6 finite right inverses modulo raw pins and arbitrary-correction Gram PosDef. It makes no joint Gaussian-law, density, finite-free-coordinate independence, critical-value-tie, conditional Morse, canonical H0/Lifetime, selection/Rice or Parent claim. No two-site second-jet12 rank or uniform spectral floor is needed. Later joint law/incidence must be explicit; one-point laws do not supply it automatically.

Root's new-only exact-source qualification covers this module's complete private/generated/data/public inventory, controls, one kernel and mutation, retaining all actual attempts/commands/streams/exits/timings/lineage. Reuse applicable unchanged successes rather than timestamp/freeze replays. No admissions/custom axioms/native_decide/implemented_by or Mathlib umbrella import. Cache/registration/Git/publication and independent/process accounting remain root-owned.

Canonical standing links for future onboarding (links alone do not establish reading):

- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OWNER_MANDATE_20261015.md
- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OP-AUTONOMY-20260923-v2.1.md
