# Joint two-remote first-jet Gaussian: read-only preflight review

26 October2026. Reviewer `/root/two_remote_firstjet_arithmetic`, delegated by root. This report concerns only the prospective `SourceTwoRemoteFirstJetGaussian` contract, not an implemented or qualified module. **No material mathematical or public-API feasibility blocker was found.** The four public data definitions and two public propositions have a sound route through existing accepted public results, subject to prospective53 first becoming qualified and available.

Read completely the three draft documents in `/workspace/scratch/two-remote-firstjet-gaussian-preflight/`: `REPORT.md`, `SOURCE_TWO_REMOTE_FIRSTJET_GAUSSIAN.md`, and `PLAN.md`. Read only the relevant accepted public source/API excerpts identified below. No in-flight53 source/helper or H0 source was inspected for this task. The separately frozen53 arithmetic helper files remain unchanged; their identities and verification status were not refreshed.

No implementation, Lean/name probe, build, kernel, axiom audit, control execution, hash campaign, Git, cache/registry/configuration action, or external fetch/post occurred. Completed applicable source/Gaussian/Gram verification remains reusable under `/workspace/AGENTS.md`; a new agent, session, report, freeze or pending process requirement does not justify replay. Scientific effect NONE; same-family/provider-distinct credit0.

## One actual joint Gaussian input is supported

`SourceDerivativeGaussian.lean:154`, `smoothSourceField_derivativeVector_hasGaussianLaw`, accepts a finite family with heterogeneous derivative orders, points and directions. Its conclusion is on the unchanged original `smoothLaw d L`, with only `L ≠ 0`; its documented scope includes order zero and repeated observations. Thus it applies once to the actual12-vector consisting of raw6 and joint remote firstjet6. The ledger in the draft is correct:

- Raw order `(fM,fS,fxM,fxS,fyM,fyS)` has orders `(0,0,1,1,1,1)`.
- Remote order `(f(x),fx(x),fy(x),f(y),fx(y),fy(y))` has orders `(0,1,1,0,1,1)`.

Order-zero evaluations and the ordinary first derivatives require only finite definitional/API conversions. The raw coefficient family is public `rawPinCoefficient` (`SourceRawPinConditioning.lean:31`), defined as the first six existing derivative-coefficient rows. The remote coefficient match is the prospective53 written contract's first-three-at-x/first-three-at-y definition. That match is not assumed to have been elaborated or qualified by this preflight.

A fixed finite-coordinate continuous linear map from `Fin12 → ℝ` to `(Fin6 → ℝ) × (Fin6 → ℝ)` gives genuine joint Gaussianity of `(U,V)`. This uses one sample and one joint derivative theorem. Separate one-point Gaussian laws or independence are not substituted for this step.

`inputs/ResearchFormalCoreR1/GaussianRegressionKernel.lean:200`, `regression_residual_jointGaussian`, takes an arbitrary finite continuous linear correction B and arbitrary centers. It requires no covariance normal equations, covariance inverse or rank premise. At centers0/0 its second projection gives Gaussianity of `V − B U`; the existing Gaussian translation construction gives `V − B U + R*t`. Singular covariances and repeated coordinates therefore cause no obstruction to the sampling-law theorem. A second scalar-series Gaussian route is unnecessary and outside the adopted design.

## Literal posterior observation and four data definitions

The public49 data (`SourceRemoteJetGaussian.lean:20,28,38,42`) retain the ordinary six-jet, total raw regression correction, residual coefficient Gram and full target mean. Public `remoteJet_rawPosteriorSample` at line128 is pointwise for every sample, real radius, point and raw target under signed `L ≠ 0`. Selecting coordinates0/1/2 at x and y and concatenating gives exactly the proposed private identity

```text
Jxy(rawPosteriorSample hL r t omega)
  = Jxy(omega) − Rxy*rawPins(omega) + Rxy*t.
```

The proposed `Rxy` concatenates the same public49 correction rows, with raw pin columns unchanged. Consequently this identity concerns the literal actual posterior sample; it does not silently replace that sample by a newly defined affine observation. It has no separation, positive-radius or invertibility hypothesis.

The four public data definitions correctly expose only Jxy, actual Rxy, full mean Rxy*t and target-free `Gram(B − Rxy*a)`. No new source, kernel, cross-covariance or generic regression data object is required. In particular, the mean must keep all raw target coordinates and the covariance must have no target argument. A nonzero target in a singular configuration does not by itself assert that Rxy*t is nonzero; the proposed singular-case control should retain its stated sampling meaning.

`SourceRawPinConditioning.lean:212` supplies measurability of the actual posterior map, and `rawPinKernel_apply` at line246 identifies the actual kernel at every target with the pushforward of the unchanged source law. Global observation measurability has a public route through `SourceSmoothTopology.lean:72,109`, `sourceDerivativeBCF_apply` and `sourceDerivativeBCF_borel`, at orders0/1, fixed spatial evaluation and directions, then finite concatenation and toLp. No private49 measurability or series helper needs to be named or copied.

## Mean, covariance and law identification have public joins

The required deterministic/finite joins are new composition obligations, not new assumptions or reasons to repeat accepted source mathematics:

1. `SourceEndpointParameters.lean:30`, `smoothSourceField_derivative_integral_zero`, gives all12 coordinate means0. Joint Gaussianity gives the necessary integrability. Finite-vector integral equality, continuous-linear-map integral commutation and translation then yield mean Rxy*t.
2. `SourceDerivativeGaussian.lean:176`, `smoothSourceField_derivative_covariance`, gives each actual12-coordinate covariance as the convergent coefficient pairing. Its points/directions can differ, so cross-remote covariance is included rather than inferred from marginal laws.
3. Gaussian coordinate MemLp2 supports the public covariance addition/subtraction and finite-sum rules. In Mathlib's `Probability/Moments/Covariance.lean`, `covariance_fun_sum_fun_sum` (line294), scalar covariance multiplication (lines136/139), and the constant-translation rules (lines89–111) support the finite affine transport.
4. `ContactJetCovariance.lean:80`, `coefficient_product_summable`, together with public derivative/raw row summability, permits the finite-sum/tsum interchange. The fixed12-to6 transport identifies the covariance with the exact Gram of `B − Rxy*a`. No sample-weighted residual series, almost-sure infinite-series rearrangement or new generic matrix/covariance library is needed.
5. `SourceEndpointParameters.lean:150`, `finiteGaussian_law_parameters`, accepts the actual finite Gaussian observation, its derived mean and coordinate covariance. It returns both PosSemidef and equality with the literal multivariate Gaussian, including singular cases. Composing with the public kernel pushforward gives the proposed law theorem.

This route supports all signed nonzero L and all real r,x,y,t. The law does not need the five separation conditions. For PosDef only, prospective53's adopted arbitrary6×6 correction Gram theorem can be applied directly at the actual Rxy after that module is qualified. Its five quotient inequalities are exactly the intended geometry; no M/S separation, nonzero/positive radius, supplied rank/witness/PosDef or target hypothesis is added.

## The actual equal-point cross-block mutation is sound

At L=2,r=0,x=y=(1,0),t=0, the two observed triples are literally identical on every actual sample. This configuration belongs to the unrestricted sampling-law scope. The point x is quotient-distinct from the repeated pin0, so public49 `remoteResidualCovariance_posDef` (`SourceRemoteJetGaussian.lean:284`) applies to the one-point six-jet. Its value diagonal is strictly positive by public `Matrix.PosDef.diag_pos`.

Public49's actual marginal sampling law (line269), together with the public covariance pushforward rule and `covariance_eval_multivariateGaussian`, identifies the common actual value variance with that positive diagonal. Hence the actual joint cross covariance at coordinates0 and3 equals that same positive number. No arbitrary Gaussian source realization or RCD assertion at r=0 is introduced.

Deleting the cross-remote3×3 blocks gives a candidate covariance with entry0,3 equal0. **Future implementation must still prove this candidate matrix PosSemidef before using the MVG covariance formula.** This is a short fixed3+3 principal/block-diagonal adapter: the shared3×3 marginal is a principal submatrix of the public49 positive matrix (`Matrix.PosDef.submatrix`, with `.posSemidef`), and the block-diagonal quadratic form is the sum of the two marginal quadratic forms. This finite adapter is feasible; it is not supplied as a hypothesis, not yet elaborated here, and does not require a new generic block-matrix library.

With that adapter, public `covariance_eval_multivariateGaussian` identifies the mutated MVG cross covariance as0. Equality with the actual joint sampling law would force its positive common variance to vanish. The separately passed finite covariance-mismatch control can therefore reduce the one concrete mutated equality to an intended False. It targets the new joint covariance composition, rather than replaying53's distinct collision-rank negative. Only this one mutation campaign is proposed; unrelated type/import/linter failures must not count as rejection.

## Disposition and limits

The proposed four-data/two-proposition contract is suitable for root's later freeze and proper native pickup, after prospective53 qualification/availability is confirmed. Remaining implementation work consists of the finite index ledger, actual public-identity assembly, CLM split/correction, mean/covariance/Gram rewrites, observation measurability and the fixed mutation PSD adapter. None has been executed or claimed complete by this review.

The result would establish the actual all-r joint6 sampling law and the five-separation PosDef composition. It would not establish remote independence, all-r RCD/fiber validity, a conditional height/gradient Schur law, critical-value-tie incidence, global Morse, canonical H0/Lifetime labels, measurable selection, Rice/count density or Parent results. Pending different-actual-family scientific alignment, hosted checks and publication are separate process obligations and do not erase applicable completed mathematical evidence.

Canonical authority carried for onward onboarding; link delivery does not establish reading:

- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OWNER_MANDATE_20261015.md
- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OP-AUTONOMY-20260923-v2.1.md
- https://github.com/d6g8k5htny-coder/main/blob/main/governance/OWNER_DECISION_20261025_REVIEW_FAMILIES.md
