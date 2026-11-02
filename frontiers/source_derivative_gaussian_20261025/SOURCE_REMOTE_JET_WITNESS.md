# Frozen precode — actual finite remote 2-jet witnesses and residual Gram positivity

Root-frozen contract, 26 October 2026. Add module `SourceRemoteJetWitness.lean`, namespace `I4SourceRemoteJetWitness`. This is a bounded actual-source leaf immediately after the frozen SourceFiniteTrig representation bridge, not another generic-only checkpoint. Root has reviewed and frozen this contract and plan before implementation.

The original scratch-only draft was written by OpenAI/Codex `/root/candidate_inertia` in `/workspace/scratch/remote-jet-witness-contract/` only. No implementation, checks, hashes, Git/repository/cache changes, external posts or subagents. Scientific effect **NONE**; provider-distinct credit **0**. Draft theorem snippets are specifications, not compiled declarations or completion claims.

## Inputs, evidence and exact scope

Reuse completed **47 modules / 1096 targets / 32 inputs** at `c0398e27fe8da6363a9a1f6d50c206918778491e`, accepted conventional finite interpolation mathematics, and all applicable qualified source/Gram/summability/calculus evidence. Root reports SourceFiniteTrig frozen at **`d0f0dea0`**, with its seven public propositions and qualification complete; source cut32732ff7c343b6ee0fd5b66cbdf72cda3cf48f2c and qualified ownolean5b96c7d331cd73697379c52a59a5b93749c134d89971b6926a79def657949c4c now in production cache. This draft consumes its frozen `SOURCE_FINITE_TRIG.md` contracts; it neither inspects its in-flight qualification nor claims it already qualified. Final integration consumes the object when root makes that dependency available under the existing qualification route.

Read authority and detailed interface assessments:

- `/workspace/scratch/finite-jet-arithmetic-preflight/REPORT.md`.
- `/workspace/scratch/torus-phase-separation-preflight/REPORT.md`.
- `/workspace/scratch/conditional-remote-jet-preflight/REPORT.md`.
- The frozen source packet `SOURCE_FINITE_TRIG.md`.
- `/workspace/AGENTS.md` and repository/standing owner authority already read in onboarding.

Owner reuse rule is binding: completed applicable verification remains evidence under unchanged hypotheses/dependencies; a new agent, session, freeze or pending process requirement does not justify replay. New checks must identify an actual change, defect or uncovered obligation and stay within its affected scope. Mathematical evidence and provider-distinct/process obligations remain separate.

Canonical onboarding links, which do not establish recipient reading:

- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OWNER_MANDATE_20261015.md
- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OP-AUTONOMY-20260923-v2.1.md

The actual finite-witness and Gram theorems require exactly:

- Original real `L` with `hL : L ≠ 0`, retaining the same original source modes/weights and period.
- Arbitrary real `r`; no `r≠0`, small-radius restriction or positivity.
- Arbitrary `x : Fin 2 → ℝ` whose literal `I4Torus.torusProjection 2 L x` differs from each endpoint projection.
- For Gram positivity, arbitrary correction `R : Matrix (Fin 6) (Fin 6) ℝ`.

Do not assume pin-covariance invertibility, endpoint separation from each other, a target, a posterior/kernel law, a supplied interpolation witness, a desired rank/Gram certificate, or a global Morse event. Repeated pins, including `r=0`, are admissible whenever x avoids their common quotient point. This algebraic theorem makes no conditioning-law claim at a singular pin configuration.

## Carriers, six-jet and exact original coefficient rows

Write `X := Fin 2 → ℝ`, `eX := I4SourceConfluentPins.directionX = ![1,0]`, `eY := directionY = ![0,1]`, `M := endpointM r = ![-r/2,0]`, `S := endpointS r = ![r/2,0]`. Use the original `SourceMode 2` and `I4SourceFinitePinKernel.finitePairing`, with fixed observation-times-direction order.

Proposed concrete data:

```lean
jet2 (f : X → ℝ) (x : X) : Fin 6 → ℝ :=
  ![f x, fderiv ℝ f x eX, fderiv ℝ f x eY,
    iteratedFDeriv ℝ 2 f x ![eX,eX],
    iteratedFDeriv ℝ 2 f x ![eX,eY],
    iteratedFDeriv ℝ 2 f x ![eY,eY]]
```

The order is **`(value,dx,dy,dxx,dxy,dyy)`**, with ordinary derivatives and no factorial normalization. Outer/inner mixed order is `eX,eY`, as in the existing endpoint Hessian API. Work directly in Pi coordinates; no Lifetime/product-coordinate norm conversion is needed.

Define `remoteJetCoefficient L x : Fin 6 → SourceMode 2 → ℝ` as the explicit six row vector:

```text
0: m ↦ modeCoefficient 2 L m x
1: derivativeCoefficient 2 L 1 x (fun _ ↦ eX)
2: derivativeCoefficient 2 L 1 x (fun _ ↦ eY)
3: derivativeCoefficient 2 L 2 x ![eX,eX]
4: derivativeCoefficient 2 L 2 x ![eX,eY]
5: derivativeCoefficient 2 L 2 x ![eY,eY].
```

Use the qualified `I4SourceDerivativeGaussian.derivativeCoefficient`. This explicit vector avoids new dependent-order indexing. Its row summability follows from the existing `derivativeCoefficient_summable`; the value row is the order-zero specialization via `iteratedFDeriv_zero_apply`. Keep this short adapter private unless another agreed consumer needs it.

Pin rows are **literally** `I4SourceRawPinConditioning.rawPinCoefficient L r i`, in existing order:

```text
0: value at M; 1: value at S;
2: dx at M;    3: dx at S;
4: dy at M;    5: dy at S.
```

Do not permute this into remote-jet order or introduce replacement pin rows. Private explicit-row adapters may unfold the existing `rawDerivativeOrder/Point/Directions` and use finite-index case splitting; the conclusion must use the original `rawPinCoefficient`. Its existing `rawPinCoefficient_summable hL r i` is reused directly.

## Useful public jet API: three intended propositions

Use `c : ℝ`, arbitrary `x : X`, and the concrete six germ functions:

```text
G₀(y)=1
G₁(y)=sin(c*(y₀−x₀))/c
G₂(y)=sin(c*(y₁−x₁))/c
G₃(y)=(1−cos(c*(y₀−x₀)))/c²
G₄(y)=sin(c*(y₀−x₀))*sin(c*(y₁−x₁))/c²
G₅(y)=(1−cos(c*(y₁−x₁)))/c².
```

Data definitions and their private smoothness helpers do not add public proposition targets. Three public jet propositions suffice:

1. **`localGerm_jet2 (c) (hc : c ≠ 0) (x) (j s : Fin 6)`**:
   `jet2 (localGerm c x s) x j = if j=s then 1 else 0`.
2. **`jet2_mul (P Q : X → ℝ) (hP : ContDiff ℝ 2 P) (hQ : ContDiff ℝ 2 Q) (x)`**: the actual six-jet of `fun y ↦ P y * Q y` equals the six product formulas below.
3. **`jet2_interpolate_mul (c) (hc : c ≠ 0) (x) (P : X → ℝ) (hP : ContDiff ℝ 2 P) (hp : P x ≠ 0) (t : Fin 6 → ℝ)`**: the actual jet at x of the **defined** function `fun y ↦ P y * ∑ s, a s * localGerm c x s y` equals t, with the explicit coefficients defined below.

No desired jet or rank predicate is a premise. LocalGerm smoothness holds for every c because its denominators are constant in y; only the identity theorem needs c nonzero. The multiplier need only be C² and nonzero at x, with no sign assumption. Public data names are fixed by the root appendix below.

For `p=jet2 P x`, `q=jet2 Q x`, the product formulas, in order, are:

```text
p₀q₀
pₓq₀+p₀qₓ
pᵧq₀+p₀qᵧ
pₓₓq₀+2pₓqₓ+p₀qₓₓ
pₓᵧq₀+pₓqᵧ+pᵧqₓ+p₀qₓᵧ
pᵧᵧq₀+2pᵧqᵧ+p₀qᵧᵧ.
```

Multiplication by P is thus lower triangular with diagonal p₀. Use a concrete data function `inverseMulJet2Coefficients p t` defined by:

```text
a₀=t₀/p₀
aₓ=(tₓ−pₓa₀)/p₀
aᵧ=(tᵧ−pᵧa₀)/p₀
aₓₓ=(tₓₓ−pₓₓa₀−2pₓaₓ)/p₀
aₓᵧ=(tₓᵧ−pₓᵧa₀−pₓaᵧ−pᵧaₓ)/p₀
aᵧᵧ=(tᵧᵧ−pᵧᵧa₀−2pᵧaᵧ)/p₀.
```

These are six explicit scalar divisions/operations, not a chosen abstract inverse. A private scalar inverse identity and private finite-jet linearity derive the public interpolation theorem. No determinant theorem, generic Fourier library, ring instance or Prop-valued desired-result bundle is needed. Generic Hessian symmetry need only be consumed if reversed mixed entries are explicitly requested; the one fixed mixed order suffices.

## Same-period separation, annihilator and finite polynomial assembly

For the actual assembly fix `c := sourceC L = 2*Real.pi/L`, nonzero under hL. From each literal quotient inequality independently derive a coordinate `jM,jS : Fin 2` with

```text
0 < 1−cos(c*(x jM−M jM)),
0 < 1−cos(c*(x jS−S jS)).
```

The torus helper supplies the scalar equivalence `cos(c*(a-b))=1 ↔ (a:AddCircle L)=(b:AddCircle L)` and the dimension-two positive-factor extraction, using unrestricted integer-period APIs. This works for negative L and adds no phase-range, representative, fundamental-domain or positive-period hypothesis. Keep helper propositions private in the integrated source to preserve the five intended public target count below, unless root explicitly elects an extra reusable public API.

Define, for those selected coordinates,

```text
AM(y)=1−cos(c*(y jM−M jM))
AS(y)=1−cos(c*(y jS−S jS))
P(y)=AM(y)²*AS(y)².
```

Derive internally that P is smooth, `P x>0`, `P M=P S=0`, and `fderiv ℝ P M eX/eY = fderiv ℝ P S eX/eY = 0`. Only value and first derivatives at pins are needed; do not add an unnecessary full higher-jet vanishing theorem. Repeated pins cause no problem. Derive the annihilation of `P*Q` from the actual product rule, for each smooth interpolant Q.

Producer represents this **concrete** P and each concrete local germ using SourceFiniteTrig operations, retaining original L:

- Axis cosines use integer coordinate frequencies and translated offsets.
- Axis sines use the cosine offset `−π/2` followed by the frozen `translate L center` convention.
- `1−cos` uses constant, append and scale; squared pin factors and mixed sine use `mul`.
- Germ normalization uses scale by `c⁻¹` or `(c²)⁻¹`.
- The six-term combination uses append and scale with the explicit inverse coefficients.
- The final interpolant polynomial is `mul annihilatorPoly localCombinationPoly`.

Use the seven frozen SourceFiniteTrig correctness theorems to prove its evaluated function equals `P*Q` **globally**. Do not reconstruct the source conversion, mode amplitude positivity, finite-shift carrier or infinite-series derivative argument already supplied by source47. No fixed mode-box bound is required for this pointwise finite Finsupp theorem.

For each `s : Fin 6`, set target `t j := if j=s then 1 else 0`. Let `Fs` be the resulting concrete finite trigonometric polynomial and take `v s := I4SourceFiniteTrig.toSource L Fs`. Apply `toSource_eval`/`toSource_derivative` at each pin and x, with orders 0/1/2 as appropriate. Prove the two literal pairing families below. All coefficients use **original SourceMode 2**; no new source or posterior carrier is introduced.

## Actual endpoint: two intended public propositions

4. **`actual_finite_remoteJet_witnesses`**, with the following exact essential shape:

```lean
{L : ℝ} (hL : L ≠ 0) (r : ℝ) (x : Fin 2 → ℝ)
(hxM : I4Torus.torusProjection 2 L x ≠
  I4Torus.torusProjection 2 L (I4SourceConfluentPins.endpointM r))
(hxS : I4Torus.torusProjection 2 L x ≠
  I4Torus.torusProjection 2 L (I4SourceConfluentPins.endpointS r)) :
∃ v : Fin 6 → (I4Source.SourceMode 2 →₀ ℝ),
  (∀ i s, I4SourceFinitePinKernel.finitePairing
    (I4SourceRawPinConditioning.rawPinCoefficient L r i) (v s) = 0) ∧
  (∀ j s, I4SourceFinitePinKernel.finitePairing
    (remoteJetCoefficient L x j) (v s) = if j=s then 1 else 0)
```

Use the actual namespace of `SourceMode` supplied by the existing imports; the fully qualified spelling above follows the current source interface. The existential is a **conclusion proved by the internally constructed finite polynomials**. It is not a public witness assumption. No general remote rank certificate or arbitrary desired smooth interpolant is accepted as a substitute.

5. **`actual_remote_residual_coefficientGram_posDef`** with exactly the same `hL,r,x,hxM,hxS` and arbitrary `R : Matrix (Fin 6) (Fin 6) ℝ`:

```lean
(I4ContactGram.coefficientGram
  (I4SourceFinitePinKernel.residualCoefficient
    (I4SourceRawPinConditioning.rawPinCoefficient L r)
    (remoteJetCoefficient L x) R)).PosDef
```

Derive this by the just-constructed actual witnesses, qualified `coefficientGram_posDef_of_finite_kernel_rightInverse`, existing raw row summability and the private remote row summability adapter. Do not repeat its finite separation/Gram proof, Gaussian regression or Schur theory. ANY correction R is intentional, including matrices at configurations where actual pin-covariance inverse does not exist.

These five are the proposed complete public written-proposition list. Other needed private analytic, torus, scalar, row and representation helpers belong in the actual-module inventory but earn no independent public research-target registration. Any additional public proposition requires root acknowledgement before freeze. Data definitions and generated artifacts remain inventory-only.

## Controls to freeze before code

Root/producer freezes concrete source/control statements before implementation, covering new actual joins rather than rechecking source47 or qualified46:

- The six germs give the six **actual** jets at arbitrary translated x and nonzero c, including the mixed entry 1 and all five other zero entries for each germ. The pure second-derivative product coefficients carry 2; the mixed cross terms each carry 1.
- The explicit inverse works for nonconstant multipliers, not only P=1. Include a concrete smooth P with nonzero first derivatives at x, and a target with a second-order component, so the correction terms and denominator normalization are exercised. A constant P=2 instance separately checks amplitude scaling.
- Pin-factor values and first derivative annihilation at M and S are obtained from the concrete represented factors. Check the literal raw row order `(M,S,dxM,dxS,dyM,dyS)`, not a newly permuted proxy.
- An actual original-mode witness instance with `L=2`, `r=1`, `x=![0,0]` (both pin phases are ±π/2), all 36 remote pairings and all 36 raw pin pairings. Obtain v from the internally constructed actual theorem/data; do not supply arbitrary finite coefficients as a premise.
- A repeated-pin instance `L=2`, `r=0`, `x=![1,0]`, where cosπ=−1 separates x from the common endpoint. This witnesses the intended absence of pin invertibility, `r≠0` and endpoint-distinctness assumptions.
- A negative-period instance, for example `L=−2`, `r=0`, `x=![1,0]`, retains literal L and discharges both quotient inequalities through the same scalar cosine route.
- Actual residual Gram positivity for arbitrary R; parameterized arbitrary-R control is stronger than checking only R=0. If concrete instances aid independent control readability, use both R=0 and a nonzero matrix without changing the theorem assumptions.

### Sole negative mutation and mathematical counterexample

Drop **only `hxM`**, retaining `hL` and `hxS`, from the actual witness assertion. The frozen counterexample is:

```text
L=2, r=1,
x=M=![−1/2,0], S=![1/2,0].
```

Here `torusProjection 2 2 x ≠ torusProjection 2 2 S`: the zeroth coordinate phase is `π*(−1)=−π`, whose cosine is −1 by `Real.cos_neg`/`Real.cos_pi`, so the scalar equivalence rules out quotient equality. Thus the **retained** hxS is valid.

The remote value row at x=M equals literal pin row 0. For any purported witnesses, `hker 0 0` makes its finite pairing with v0 equal 0, while `hright 0 0` makes the **same pairing** equal 1. This gives the concrete scalar contradiction `0=1`. Prove the nonexistence from these actual row identities; a real-lift-only counterexample is insufficient.

The mutation harness must isolate the weakened claim and reject at exactly **one intended `False` target**, with no missing-hypothesis/unbound-variable/import/linter errors counted as the expected rejection. Keep the valid collision counterexample separate from the sole false mutation. Do not add a second unrelated negative campaign. No false replacement theorem enters production source/cache.

## Ownership, qualification and completion boundary

Root dispatches exactly two disjoint scratch helpers: jet arithmetic and torus separation. They provide only needed frozen sections for **one-time textual integration** into this new module; producer never imports/copies a helper object into a production cache. Helpers have bounded own-source strict-development elaboration only, no standalone kernel/audit/control campaign, external posts, old-source/config/cache/manifest changes or worker dispatches. Helper target credit and provider-distinct credit are 0. Root owns all shared registration, configuration, qualified cache copying, Git and publication.

Producer owns new `SourceRemoteJetWitness.lean` plus assigned scratch. It assembles the actual finite polynomials/witnesses and Gram conclusion, freezes the integrated source, and runs the single integrated new-module qualification: applicable strict Werror evidence reused when exact source/dependencies are unchanged, exactly one own-module kernel after freezes, exhaustive actual-module-index standard-three/classifications for every constant/artifact, meaningful frozen controls, and the one counterexample-backed sole-False mutation. Preserve every attempt, failure, command, exit, measured time, full stream, source snapshot and source/object lineage. No admissions/custom axioms/native_decide/implemented_by/umbrella Mathlib import. No extra compilation merely for freshness, helper repackaging or an ilean.

This source proves actual finite original-mode remote interpolation and residual Gram positivity. It does not yet identify the actual conditional remote Gaussian law/covariance on each raw target, discharge a small-radius pin inverse, claim a law at singular configurations, establish quantitative covariance floors, global conditional Morse/distinctness, Sard/incidence, equal-value ties, canonical H0/Lifetime labels, joint selection, frames/Rice or Parent Lean. Those later bridges retain accepted mathematics and separate process obligations.

## Root-frozen data and qualification routing

Fix public data names jet2, localGerm, mulJet2, inverseMulJet2Coefficients, interpolant, remoteJetCoefficient. mulJet2 is the concrete six-entry product displayed above; jet2_mul concludes equality with it. interpolant c x P t y is literally P y * sum_s(inverseMulJet2Coefficients (jet2 P x) t s * localGerm c x s y). Keep the five public written proposition names exactly as specified. Any additional public proposition needs root acknowledgment; new data/private/generated constants remain complete-inventory entries.

Producer actual_fold_candidate_construct owns ONLY SourceRemoteJetWitness.lean and /workspace/scratch/remote-jet-witness-construct. Root-dispatched candidate_inertia owns ONLY /workspace/scratch/remote-jet-arithmetic, supplying one needed frozen section of concrete data/public three jet propositions/private arithmetic and calculus helpers. Root-dispatched conversation_rpc_followup owns ONLY /workspace/scratch/remote-jet-torus-separation, supplying one needed frozen section of private same-period scalar equivalence/positive-coordinate extraction. Agree the exact data/helper APIs directly before heavy proofs; workers spawn no agents. Each helper begins source ONLY after producer acknowledges its control contract frozen. Both needed sections integrate exactly once before the producer's sole own-module kernel; no helper-object import or independent helper kernel/audit/control campaign.

The new uncovered obligations are exactly these new jet calculus, actual finite polynomial assembly, torus/collision adapters and two actual witness/Gram theorems. Reuse all47 completed proof checks and objects. Source47 and SourceFinitePinKernel must never be rebuilt to freshen timestamps or re-establish completed evidence. Preserve all new actual failures/full streams/commands/exits/timings/source snapshots/object lineage; no original-byte snapshot is invented if not captured. No full Mathlib import, admissions, custom axioms, native_decide or implemented_by. Standard three axioms and subsets only; exhaustive actual-module-index inventory must include every private/generated/structure/foreign-namespace constant and separately classify data vs five written public propositions. No Prop-valued desired-result records.

Source/kernel equality at degenerate radius is not an assertion of a conditioning law there. Keep ANYr and repeated pins in finite-witness/Gram statements, as in the controls. The later actual every-target Gaussian pushforward/covariance join is outside this source. Independent review/provider-distinct process never erases completed mathematical verification. Scientific effectNONE.
