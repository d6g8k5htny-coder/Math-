# Frozen precode: separate endpoint Hessian-three witnesses

26 October2026, root freeze16:07UTC. New module `SourceEndpointHessianWitness.lean`, namespace `I4SourceEndpointHessianWitness`. Frozen scope: one public coefficient definition and exactly two public propositions. Root publishes this contract/native pickup before source; producer freezes concrete controls before implementation. Root owns shared metadata/cache/configuration/Git/external publication.

## Reuse and exact scope

Reuse qualified49/1105/32 at `374c1a8d087a147e60fee3be1452c345f138c98f` (native49result/only-own release6420802319), including qualified48/1101/32 and its actual finite-trig/jet/kernel APIs, all applicable prior source/Gram/series evidence and accepted conventional mathematics. Qualified48 publication9a1f52b/result6416959065/sourcecut689b8eef7dd2107e51d46007c1be3dfd4a909b81 and all applicable source/finite-trig/jet/Gram evidence remain reusable. This algebraic leaf consumes48 exported APIs and does not require49 law proofs to be replayed. Root read/adopted the full supporting contract and finite plan before freeze.

`/workspace/AGENTS.md` controls: completed applicable verification stays reusable on unchanged hypotheses/dependencies. A new agent, handoff, freeze or process requirement does not justify replay. Additional checking must name a changed scope, defect or uncovered obligation and stay within it. Different-family/provider-distinct review and hosted/publication process remain separate from mathematical evidence. Scientific effect **NONE**; same-family/provider-distinct credit **0**.

Construct three original finite coefficient directions for the ordinary symmetric Hessian at M and, separately, three for S. Each family annihilates all six literal raw pin rows and has the three Hessian identity pairings at its chosen endpoint. Derive marginal residual coefficient-Gram PosDef for **every** real correction matrix of shape3×6, with no supplied witnesses, rank/positivity certificate, pin inverse, target, law or global Morse premise.

Do not assert a joint six-Hessian rank/law, a density theorem, determinant nullity, critical-value tie exclusion, Gaussian free-coordinate decomposition, conditional Morse, canonical finite-event H0 labels, `IsFiniteBar`, frames/Rice or Parent closure. No joint family of six directions must have zero Hessian pairings at the other endpoint. Only its **value and first derivatives** need vanish there.

## Literal actual rows and minimum public data

Use original signed `L:ℝ`, `hL:L≠0`, `SourceMode 2`, `X=Fin 2→ℝ`, `M=endpointM r=![-r/2,0]`, `S=endpointS r=![r/2,0]`, and original `directionX/directionY`. Let tag `e:Fin 2` select M at0 and S at1; tag is not a new sample carrier.

One public data definition suffices:

```text
endpointHessianCoefficient (L r : ℝ) (e : Fin 2) :
    Fin 3 → SourceMode 2 → ℝ
```

Define it literally by selecting the existing `rawDerivativeCoefficient` rows below; a private row-index adapter is enough. No separate public covariance, residual, point, polynomial, witness or observation data definition is needed for this leaf.

| e | j=0 | j=1 | j=2 | Actual ordinary observation |
|---|---|---|---|---|
|0 (M)|row6|row7|row8|`(fxx(M),fxy(M),fyy(M))`|
|1 (S)|row9|row10|row11|`(fxx(S),fxy(S),fyy(S))`|

The rows are exactly `I4SourceConfluentLimits.rawDerivativeCoefficient L r index`, matching `rawPinsWithHessians L r` indices6…11 through the already proved `rawPinsWithHessians_series`. The mixed entry is the ordinary derivative with directions `![directionX,directionY]`, **without a factor2 or a factorial**. The six raw pin rows retain `(fM,fS,fxM,fxS,fyM,fyS)`.

Privately match each selected coefficient row to the corresponding public source48 `remoteJetCoefficient L endpoint` row3/4/5, or directly to `derivativeCoefficient 2 L 2 endpoint ![X,X]/![X,Y]/![Y,Y]`. Prove the three-case summability adapter with existing `derivativeCoefficient_summable`. Do not access another module's private constants or change its API.

**Schur boundary:** `sourceEndpointSchurAt L r` is the covariance of the *adjusted interleaved* order `(xxM,xxS,xyM,xyS,yyM,yyS)`, with the first four entries divided by `r` and confluent pin terms subtracted. It is not the ordinary three-row Gram defined here. A later marginal covariance join uses selectors `(0,2,4)` at M and `(1,3,5)` at S with weights `(r,r,1)`, under the accepted actual regression/inverse hypotheses. This leaf proves no new Schur equality or positivity of that six-by-six matrix.

## Exactly two public propositions

Signatures are specifications, not elaboration-checked source. Write `a=rawPinCoefficient L r` and `b e=endpointHessianCoefficient L r e`.

**1. `actual_finite_endpointHessian_witnesses`**

```text
{L:ℝ} (hL:L≠0) (r:ℝ)
(hsep : torusProjection 2 L (endpointM r) ≠
        torusProjection 2 L (endpointS r)) :
∃ v : Fin 2 → Fin 3 → (SourceMode 2 →₀ ℝ),
  (∀ e i s, finitePairing (a i) (v e s) = 0) ∧
  (∀ e j s, finitePairing (b e j) (v e s) = if j=s then 1 else 0)
```

Each `e` has its own three finite directions. No conclusion relates `b(other e)` to `v e`; this is two marginal right inverses, not a joint six-row right inverse.

**2. `actual_endpointHessian_residual_coefficientGram_posDef`**

```text
{L:ℝ} (hL:L≠0) (r:ℝ) (hsep : literal quotient inequality above)
(e:Fin 2) (R:Matrix (Fin 3) (Fin 6) ℝ) :
  (I4ContactGram.coefficientGram
    (I4SourceFinitePinKernel.residualCoefficient a (b e) R)).PosDef
```

The generic public `coefficientGram_posDef_of_finite_kernel_rightInverse` is polymorphic in natural row sizes `p,q` and accepts **p=6,q=3 directly**. Its only additional inputs are row summability and the actual finite pairings. Instantiate it once for the chosen `e` with the internally constructed family; no new generic Gram theorem is needed. Preserve arbitrary signed radius and correction matrix; no `r>0`, small-radius or invertibility premise may appear.

Extra public propositions require root acknowledgement before freeze. Private/generated/data constants remain fully inventoried, without additional public research-target credit.

## Concrete minimal multiplier construction

Let `c=sourceC L=2π/L`, nonzero from `hL`. For chosen endpoint `p` and other endpoint `q`, use the **fixed x-axis** multiplier

```text
Aq(y)=1-cos(c*(y0-q0)),       Pq(y)=Aq(y)^2,
alpha=Pq(p).
```

Because both literal endpoints have second coordinate0, `hsep` implies their first coordinates differ in `AddCircle L`. The public elementary period facts `Real.cos_eq_one_iff` and `AddCircle.coe_eq_zero_iff` give `cos(c*(p0-q0))≠1`. Together with `cos<=1`, derive `Aq(p)>0` and `alpha>0` **internally**. No coordinate choice, supplied multiplier positivity or radius bound is needed. Source48's matching helpers are private; derive this short endpoint-specific adapter using public period APIs rather than naming private declarations.

At the other pin, `Aq(q)=0`, hence `Pq(q)=0` and `dPq(q)=0` by the product/power derivative rule. These are the only required vanishing orders. Squaring provides them directly; do not require zero Hessian there or claim cross-endpoint Hessian pairings.

At the chosen pin use the three existing source48 germs

```text
g0(y)=localGerm c p 3 y = (1-cos(c*(y0-p0)))/c²,
g1(y)=localGerm c p 4 y = sin(c*(y0-p0))*sin(c*(y1-p1))/c²,
g2(y)=localGerm c p 5 y = (1-cos(c*(y1-p1)))/c².
```

The public `localGerm_jet2` already proves their own value/gradient vanish and their ordinary Hessian-three rows are the standard basis. Reuse it, with no derivative campaign on these germs. Define the desired functions

```text
Fs(y) = alpha⁻¹ * Pq(y) * gs(y),        s:Fin3.
```

At p, the lower germ jets vanish, so the public `jet2_mul` product rule reduces the Hessian to `alpha⁻¹ * Pq(p) * Hess(gs)`: only one scalar inverse is needed. There is no six-jet triangular inversion. At p its value/gradient are zero from the germ; at q they are zero from the multiplier. Thus all raw6 function pins vanish and the selected Hessian3 is exactly the identity.

Represent these functions by explicit **private** `TrigPoly` data using qualified47 `constant`, list append, `scale`, `translate` and `mul`: the shifted axis cosine is one translated cosine term; shifted sine is a cosine term with offset `-π/2`; `Pq` is the square of `constant1 - axisCos(q)`; the germs are the three displayed products/scalings. Multiply and scale by `alpha⁻¹`, then take

```text
v e s = I4SourceFiniteTrig.toSource L (the explicit polynomial for Fs).
```

Use public `eval_*`, `toSource_derivative` and ordinary order0/1/2 conversions to derive both finite pairing families in original `SourceMode 2`. Necessary local polynomial/evaluation, smoothness, row and finite-index helpers stay private. No new source, measure or original amplitude convention is introduced.

## Meaningful bounded controls and one honest mutation

The producer freezes concrete names and a finite harness before source code, covering only this affected scope:

1. **Literal row selection/order:** show the M/S coefficient triples select raw rows `(6,7,8)` / `(9,10,11)` and directions `(XX,XY,YY)`. Match actual `rawPinsWithHessians` observations, retaining no factor2 on XY. Distinct Hessian target coefficients `(1,2,3)` expose permutations and mixed-entry normalization errors.
2. **Actual original directions:** at `L=2,r=1` instantiate both endpoint families. Check all36 raw pin pairings and all18 own Hessian pairings, using directions obtained from the actual internally constructed theorem rather than supplied arbitrary coefficients. Both endpoints are genuinely distinct quotient points.
3. **Signed period/radius:** instantiate `L=-2,r=1` and one negative-radius instance, e.g. `L=2,r=-1`, retaining the original sample/source coefficients and swapped endpoint positions. No positive-radius or positive-period assumption may be introduced.
4. **Arbitrary rectangular correction:** instantiate each3×6 residual Gram at zero correction and at a concrete nonzero nonsymmetric matrix, e.g. `R j i=(j.val+1)*(i.val+2)` as real numbers. This checks the actual p=6,q=3 interface and absence of any pin-inverse requirement.
5. **Minimum construction facts:** at `L=2,r=1`, each other-pin multiplier has `alpha=4`; prove own germ value/gradient0, other multiplier value/gradient0, and retain ordinary XY normalization. These facts support the actual source witness controls and the mutation below.

**Sole mutation: omit the factor `alpha⁻¹` from the concrete witness polynomial while retaining the identity pairing claim.** Use `L=2,r=1`, chosen endpoint M and column0 (the XX germ). Here `c=π`, `p0-q0=-1`, `cos(-π)=-1`, so `alpha=(1-(-1))²=4`. The unnormalized actual polynomial `Pq*g0` has Hessian XX entry4 at M by public `localGerm_jet2/jet2_mul`. Its finite original direction produced by `toSource` therefore has the **literal row6 pairing4**, whereas the mutated right-inverse claim demands1. The proved counterexample is `4≠1`, linked through that actual polynomial and original coefficient pairing. Freeze a harness deriving exactly one intended `False` from this mismatch, with no unrelated missing-name, type, import or linter failure counted as rejection. One mutation campaign suffices.

**Do not use omission of endpoint separation as a false rank mutation.** At coincident quotient pins the raw observations still constrain only value and gradient; Hessian-three can remain free. For example at `r=0`, the three unmultiplied germs at the common pin have raw6 pairings0 and Hessian identity. The chosen multiplier normalization degenerates there, but that does not refute the stronger existential rank/PosDef theorem. The separation assumption is sufficient for this chosen construction, not proved necessary for marginal Hessian rank. No collision nonexistence claim is made.

## Qualification boundary and sources

After root's frozen precode/native pickup, qualify only this new module's actual source/private/generated inventory and meaningful controls, with the established exact-source strict/audit/one-own-module-kernel/sole-False/source-spec review route. Reuse applicable unchanged successful evidence; do not rebuild47/48 or49 for timestamps. Preserve all actual new failures, commands, exits, streams, timing, snapshots and source/object lineage. Helpers, if root dispatches any, receive no duplicate standalone audit/kernel/control campaign or extra theorem credit. No custom axioms, admissions, `native_decide`, `implemented_by` or Mathlib umbrella import.

Primary public sources read: `SourceConfluentPins.lean:120`; `SourceConfluentLimits.lean:24,26,30,35,95`; `SourceRawPinConditioning.lean:32,35`; `SourceEndpointRegression.lean:36`; `SourceEndpointParameters.lean:192`; `SourceFinitePinKernel.lean:21,44,67`; `SourceRemoteJetWitness.lean:199,442` and public `jet2_mul`; `SourceFiniteTrig.lean:63,67,72,84,119,227,276`. Reading qualified source is not new verification.

Canonical standing authority for onward onboarding (links alone do not establish reading):

- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OWNER_MANDATE_20261015.md
- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OP-AUTONOMY-20260923-v2.1.md

## Current operational checkpoint

Native49result delivered16:05:03 after its unchanged14:10/15:10times; original claimant released only its own completed stage and preserved the15:52watch observation. This new endpoint claim has its own finite checkpoint17:00/terminal18:00UTC26October2026 or invocationend, without resetting any earlier stage. Current-source hostedCI and different-family scientific review are separate from completed local mathematical evidence. No merge/Ready/protection/status change.
