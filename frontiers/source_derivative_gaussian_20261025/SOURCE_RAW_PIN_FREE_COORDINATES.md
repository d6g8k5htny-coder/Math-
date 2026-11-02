# Prospective precode — SourceRawPinFreeCoordinates

26 October2026. Root-adopted PRECODE contract. Implementation and qualification are pending; the actual native pickup and GO are separate process records. Proposed module `SourceRawPinFreeCoordinates.lean`, namespace `I4SourceRawPinFreeCoordinates`. Root owns the future proper PRECODE publication/native pickup, concrete control freeze, source cut and all shared metadata/cache/Git/external publication. The planned checkpoint is21:15UTC and terminal23:30UTC26October/invocation end; actual pickup delivery and freeze are recorded by root after PRECODE publication. Implementation awaits that actual pickup and explicit GO.

Read with historical `/workspace/scratch/raw-pin-free-coordinate-construct/READINESS.md` and the two accepted prospective preflight reports. Historical readiness is unchanged. This prospective contract adopts the later refinement: reuse public `unitDirection_hasLaw` for each standard scalar marginal after finite pairing/Gram normalization, while still proving the entire free vector jointly Gaussian and jointly independent. Do not build a new scalar mean/variance Gaussian proof chain.

Scientific effect NONE; same-family/provider-distinct credit0. Completed applicable source/Gaussian/carrier/finite-shift/raw-posterior verification remains reusable under `/workspace/AGENTS.md`. No new agent, session, freeze, cut or pending process requirement justifies an old build, kernel/audit/control/hash campaign. Prior55/56 proof and process records remain unchanged. No in-flight55 source/helper is inspected or consumed.

## Exact new semantic content

For a deterministic finite orthonormal family of finitely supported **original coefficient directions** in the literal six-row raw pin kernel, construct its entire Gaussian coordinate vector and the literal coefficientwise finite-projection residual on `SmoothSample 2 L`.

Prove a residual-first product pushforward whose second factor is the entire iid standard-Gaussian `Fin n → ℝ` law, and whose first factor is the law of the **whole literal residual sample**. Separate scalar marginal or scalar-own-residual independence statements are insufficient. Then prove exact sample-level raw posterior reconstruction at every full target and every real radius, including singular r=0.

The sampled coefficient sequence remains on its existing product Gaussian space/every-order smooth subtype. Only the deterministic directions have finite support. No sampled sequence is assumed to lie in coefficient l2. No independence, Gaussian law, residual rank, covariance invertibility or desired posterior formula is a frame assumption.

No frame-existence theorem for every parameter, uniform conditioning bound, conditional Morse theorem, singular-pin RCD/fiber statement, canonical global label, once-counting, Rice/density result, all-frame Parent theorem or spatial O(2) law invariance is included.

## Narrow dependencies and public surface

Expected existing source dependencies are `SourceFinitePinKernel` and `SourceCurvatureDecomposition`, with the already public general Gaussian/conditional-source APIs they expose. Add only genuinely necessary narrow Mathlib imports for finite Gaussian independence/product maps and empty pi law. No umbrella Mathlib, copied source package, private foreign generated API or new infinite-dimensional Gaussian library.

The exact authorized surface is one authored public **frame structure**, three authored public **maps**, and three authored public **propositions**. Structure constructors/projections and every generated/private/data declaration remain separately inventoried in future qualification. No additional public independence, raw-kernel product, null-section or reconstruction-auxiliary theorem is added without root changing the contract before pickup.

### Frame: `RawPinFreeFrame`

Signature specification:

```text
RawPinFreeFrame (L r : ℝ) (n : ℕ)
```

Freeze its fields to:

```text
chi : Fin n → (SourceMode 2 →₀ ℝ)
gram : ∀ j k : Fin n,
  finitePairing (fun m => chi j m) (chi k) = if j=k then 1 else 0
raw_kernel : ∀ (i : Fin 6) (j : Fin n),
  finitePairing (rawPinCoefficient L r i) (chi j) = 0
```

`finitePairing` is the accepted public observation-times-finite-direction pairing. Keep the raw-row argument first. The frame has no hL, r-nonzero, n-positive, law, independence, rank or desired-result field. It is deterministic data at its fixed L,r. The later probability/posterior propositions carry the existing necessary hL:L!=0 explicitly.

### Three maps

Use a private finite lift with the literal equation

```text
V_F(z) = sum j : Fin n, z j • F.chi j.
```

The three public map specifications are:

```text
freeCoordinate {L r : ℝ} {n : ℕ}
  (F : RawPinFreeFrame L r n) (omega : SmoothSample 2 L) : Fin n → ℝ

freeShiftSample {L r : ℝ} {n : ℕ}
  (F : RawPinFreeFrame L r n) (z : Fin n → ℝ)
  (omega : SmoothSample 2 L) : SmoothSample 2 L

freeResidualSample {L r : ℝ} {n : ℕ}
  (F : RawPinFreeFrame L r n) (omega : SmoothSample 2 L) : SmoothSample 2 L
```

Freeze their actual meanings by the following equations, not by replacement law or existence choice:

```text
freeCoordinate F omega j = finitePairing omega.val (F.chi j)
freeShiftSample F z omega = finiteShiftSample (V_F(z)) omega
freeResidualSample F omega = freeShiftSample F (-(freeCoordinate F omega)) omega
```

In particular the residual's original coefficient is

```text
omega.val m - sum j : Fin n, F.chi j m * freeCoordinate F omega j.
```

It is a finite orthogonal projection subtraction. Erasing all coefficients on the directions' support union is a different map and is not allowed. The accepted finite shift preserves the literal original smooth subtype; no new source summability theorem is required.

## Exactly three public proposition specifications

These are exact proposed statement shapes, not elaboration-checked declarations or implementation text. Existing namespace qualifications may be inserted without changing their types.

### 1. `freeMaps_measurable`

```text
{L r : ℝ} {n : ℕ} (F : RawPinFreeFrame L r n) :
  Measurable (freeCoordinate F) ∧
  Measurable (fun p : (Fin n → ℝ) × SmoothSample 2 L =>
    freeShiftSample F p.1 p.2) ∧
  Measurable (freeResidualSample F)
```

Finite sums/evaluations and the literal finite-shift carrier formula supply this bundled measurability. Do not add hL or n>0 merely for convenience if the maps need neither.

### 2. `freeResidual_freeCoordinate_joint_map`

```text
{L r : ℝ} {n : ℕ} (hL : L ≠ 0) (F : RawPinFreeFrame L r n) :
  (smoothLaw 2 L).map (fun omega =>
    (freeResidualSample F omega, freeCoordinate F omega)) =
  ((smoothLaw 2 L).map (freeResidualSample F)).prod
    (Measure.pi (fun _ : Fin n => gaussianReal 0 1))
```

The order is **residual first**. The first coordinate is the entire literal `SmoothSample 2 L` residual, not only finitely many coefficients, a scalar-direction residual, a different Gaussian field with matching covariance or an erased sample. The second factor is the entire iid vector law, not a statement of scalar marginals. Fin0 is included without a positive-dimension premise.

### 3. `rawPosteriorSample_free_reconstruction`

```text
{L r : ℝ} {n : ℕ} (hL : L ≠ 0) (F : RawPinFreeFrame L r n)
  (t : Fin 6 → ℝ) (omega : SmoothSample 2 L) :
  rawPosteriorSample hL r t omega =
    freeShiftSample F (freeCoordinate F omega)
      (rawPosteriorSample hL r t (freeResidualSample F omega))
```

This is equality of the original smooth samples, at all full targets and arbitrary r. Its coefficient formula is an evaluation consequence. No r!=0, covariance invertibility, residual-rank or conditional-distribution premise is introduced. It consumes accepted `rawPosteriorSample_finiteShiftSample`, not a new regression proof.

## Required private joins and reuse route

1. Finite pairing/lift arithmetic supplies the coordinate response to a free shift, zero coordinates of the full residual, literal sample reconstruction and zero raw pairings of the combined lift. Keep these support facts private unless root identifies a concrete consumer before freeze. Do not call another module's private pairing-linearity helper by a generated name.
2. For each free index j, finite support gives summability and the diagonal Gram identity gives the exact squared norm1. Identify its finite pairing with the accepted scalar `unitDirection`. Reuse **public `unitDirection_hasLaw`** for its standard Gaussian marginal. Do not copy the old private scalar Gaussian argument or create a new scalar mean/variance proof chain.
3. Independently prove the **whole** free vector jointly Gaussian. For a finite original-mode cylinder I, use accepted public `scalarSeries_finite_hasGaussianLaw` on row index `Fin n ⊕ I`, with all finite chi rows and coordinate single rows. Transport through the accepted observation map and a finite CLM subtracting every free projection. This yields joint Gaussianity of `(Z,R restricted to I)`.
4. Use accepted public covariance identities and finite sums to get the full Gram covariance and zero cross-covariances `Cov(Z_j,R_m)`. Apply `HasGaussianLaw.indepFun_of_covariance_eval` to the entire vector/cylinder pair. Use process independence for every finite residual cylinder, then the public measurable smooth-sample retraction to identify the whole literal residual.
5. Whole-vector Gaussianity and off-diagonal covariance0 give `iIndepFun` of its scalar coordinates. Combine this with the already reused standard scalar marginal laws through `iIndepFun.map_fun_eq_pi_map` to obtain the entire iid Gaussian pi law. Scalar marginals alone are not this argument. Fin0 must work through the same statement, with its empty pi law.
6. Combine whole-residual independence with that vector marginal and residual-first order to obtain proposition2. Rewrite the original sample as its full finite lift of the residual, then invoke the accepted all-target/all-radius posterior finite-shift engine for proposition3. No singular-pin RCD claim is used.

No optional posterior-product or Fubini/null-section public theorem is included. If a later consumer needs one, it may use proposition2 and the exact reconstruction as a separate bounded application.

## Finite concrete controls

The companion SOURCE_RAW_PIN_FREE_COORDINATES_CONTROLS.md fixes the exact concrete control names and the sole mutation. Root records its freeze before GO/source/helper implementation text. These specifications are not a witness implementation or harness.

### Zero dimension and scalar identification

- `empty_frame_maps_and_joint_law`: n0 empty frame, finite lift0, shift identity, residual identity and the unique empty free vector. Specialize the actual residual-first product theorem and empty Gaussian pi law; no n>0 workaround.
- `single_direction_identification`: the normalized one-direction coordinate/residual identifies with the already public scalar `unitDirection`/`unitDirectionCoefficientResidual` maps. This checks the new interface identification only; it does not rerun the accepted scalar Gaussian campaign.

### Four literal original cosine modes at L2,r0

Freeze A,B,C,D as the original cosine modes at frequencies `(1,0)`, `(2,0)`, `(0,1)`, `(0,2)`, respectively. Each has an explicit public half-lattice witness; Bool=false is cosine. No foreign private frequency/atom name is used, and a sine `(2,0)` is not an acceptable substitute.

For each mode q let Aq be its **actual** value coefficient at0, derived from `modeCoefficient 2 2 mq 0` and the source weight/sourceZ formula. Prove positivity from the public physical-weight/exponential/sourceZ/sqrt facts; do not assume a generic positive amplitude certificate.

Let `DAB=sqrt(AA²+AB²)` and `DCD=sqrt(AC²+AD²)`. The complete two-direction table is:

| Original mode | chi0 | chi1 |
| --- | --- | --- |
| A | AB/DAB | 0 |
| B | -AA/DAB | 0 |
| C | 0 | AD/DCD |
| D | 0 | -AC/DCD |
| all other modes | 0 | 0 |

`four_cosine_raw_frame` proves the complete Gram delta and **all six** literal raw row pairings at L2,r0. At that radius M=S=0, each cosine raw column is `(Aq,Aq,0,0,0,0)`. Prove those actual columns using public mode/phase/derivative definitions; do not use a private derivativeCoefficient-some shortcut. No confluent division, covariance inverse or rank premise.

### Rational rotation and positive projection-versus-erasure control

`rotated_frame_coordinates_and_projection` uses exactly

```text
O = [[3/5,4/5],[-4/5,3/5]],
psi0=(3*chi0+4*chi1)/5,
psi1=(-4*chi0+3*chi1)/5.
```

Both rotated directions have all four original support entries. Prove Gram/raw-kernel identities, `Zpsi=O Zchi` and equality of the **full** projection. This is deterministic finite-block arithmetic, not a claim of spatial O(2)-invariance of the torus/source law.

`projection_keeps_complement` uses the actual smooth single-mode sample with coefficient1 at A. The true residual at A is `AA²/DAB²>0`, also for the rotated frame; erase-on-support gives0. `Z(R)=0` alone is insufficient because erasure also has zero free coordinates. This is a mandatory positive control, not a second mutation.

### Actual singular-radius reconstruction and sole omission witness

`singular_posterior_reconstruction` uses L2,r0 and a symbolic full target for the accepted pointwise sample equality. No conditional distribution/fiber-support interpretation is attached to singular covariance.

For the sole negative's concrete data, freeze the unrotated chi frame, `omega1=finiteShiftSample chi1 (zeroSample 2 2)`, full target0 and diagnostic mode **C=cosine(0,1)**. Prove actual smooth carrier membership by the accepted finite shift, `Z0(omega1)=0`, `Z1(omega1)=1`, true residual=zeroSample and the literal posterior-at-target0 values. Let `q=AD/DCD>0`; the correct named-mode coefficient is q.

**Sole mutation:** omit the SECOND projection term chi1*Z1 from the residual but retain both free coordinates in reconstruction. Then the mutant residual equals omega1 and the reconstructed named-mode coefficient is2q. `second_projection_omission_counterexample` must separately prove the actual q-versus2q inequality before the one negative attempt.

The sole negative assertion is exactly that false mutant reconstruction equality at this actual carrier sample/target0/modeC. Simplification by the passed coefficient values and q>0 must leave one intended False, with no import/type/linter/private-name failure. No fabricated positive Gaussian mass for omega1, scalar variance mutation, regression-engine mutation, second negative campaign or old control replay.

## Future helper and qualification boundaries

Two prospective disjoint TEXT-only helpers may be useful, but **neither is started or authorized by this design**:

1. Generic finite Gaussian/application section: the general finite-row/CLM join, whole-vector joint Gaussianity/iIndepFun/pi law and whole residual process/retraction independence, using the producer's fixed deterministic identities and accepted public scalar marginal laws. No explicit mode controls or posterior rewrite.
2. Concrete finite-frame/control section: the four named modes, actual amplitudes, normalization/rotation/raw-six pairings and named coefficient mismatch. No desired probability law, independence assumption, rank premise or posterior engine duplication.

After proper GO and concrete control freeze, each complete helper section/import/provenance must freeze before **one integration**, with zero standalone execution. The producer alone integrates and owns actual source qualification and local amendments. The final module covers all helper text; no standalone helper qualification or credit is invented.

Future qualification is new-module-only: exact successful strict evidence reused after freeze/cut; full actual owned-module inventory including frame data/projections, private/generated/foreign names; standard axioms only `propext`, `Classical.choice`, `Quot.sound`; mandatory controls and one concrete sole-False mutation; exactly one own-module kernel; actual source/spec review and complete attempt/command/time/exit/original-stream/source-object lineage. No .ilean freshness compile.

No sorry/admit/custom axiom/native_decide/implemented_by/umbrella import/private foreign generated API. Reuse all completed source/Gaussian/carrier/finite-shift/posterior mathematics and qualified object routes without old payload hash/build/proof campaigns. Root alone owns current-claim review, PRECODE/native pickup, timing, source cuts, metadata/config/cache/registration/Git/external publication. Pending process/provider-distinct alignment stays separate from mathematical evidence.

Canonical onward authority, carried without claiming link reading:

- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OWNER_MANDATE_20261015.md
- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OP-AUTONOMY-20260923-v2.1.md
