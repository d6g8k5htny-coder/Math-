# C299 nonauthor source addendum — candidate 3 after actual hosted failure

Actual reviewer: OpenAI Codex `/root/c299_nonauthor_review`, delegated by root chat `01a0bbb5-2fcb-77f0-b78b-4d220ddd7ab2` for Dylan Roy.

**Disposition: ACCEPT_SCOPED_SOURCE_REPAIR for the next bounded hosted development attempt.** The frozen changes address the actual candidate 2 diagnostics without changing the mathematical map, public assumptions or four-part endpoint. No new blocking mathematical source issue is identified in this diff. Candidate 3 compilation is unconfirmed; this source disposition is not formal theorem acceptance or a prediction that every elaboration issue is resolved.

## Actual failed run and evidence boundary

I fully read and freshly hashed the extracted candidate 2 stdout and phase receipt:

- `build-CriticalRidge.stdout`: 4227 bytes, SHA-256 `6287a34ab9f1cfb469f5152c2e523c7f3f1bbc9ab7573f7f01e924120b10877a`.
- `build-CriticalRidge.receipt.json`: SHA-256 `0024de398e7b8c50ff015cf0101e37f54302bc8d5602c8c3cf8a3bc72109e50d`.

I also read the extracted aggregate's context, phase results and final failure. The actual hosted run is `39438543701`, attempt 1, job `c299-hosted-formal`, PR491. Its PR head is `c8d66bde8ce496c1007e4a3f6b0a9f9f93762bfb`; the tested checkout is the distinct merge commit `396e7ee43ec39fa5145909e1f809fc91fec6b014`, tree `0f734451a5cdd70274dbf4018155039793844af4`, with reported PR base `8c226134ac0a0169dbb43311082e5353ed5c922c`. I inspected root's extracted evidence, not a new independent remote download.

The aggregate records three successful upstream builds, then the CriticalRidge build returns 1 after 17.856697 seconds without timeout. The before/after inventories contain the same three upstream objects and no CriticalRidge object. The object-validation error therefore records the missing required build output; it does not establish corruption of an earlier input. Audit compilation, kernel replays and negative fixtures were not reached. Aggregate status is HOLD_NOT_COMPLETED.

Actual diagnostics identify the restriction-map construction/typeclass mismatch, its downstream definitional-equality failure, a deprecated `ContinuousLinearMap.zero_apply` rejected under warnings-as-errors, type mismatches in the smoothness/derivative composition, the IFT eventual-equality normalization and reversed constant-derivative arguments. The final diagnostic also says that a declaration uses `sorry`. The source contains no authored `sorry`; the failed elaboration's recovery diagnostic is nevertheless retained and cannot be accepted as a proved declaration.

The earlier source acceptance concerned the mathematical construction and explicitly left compilation unconfirmed. These actual failures establish that candidate 2 was not an accepted compiled implementation.

## Exact candidate and changed proof assessment

Candidate 3 is 8485 bytes, SHA-256 `2a93240fa5034544a1dbcf5ec0a10ab11be1ca5d05f60b4df0e2663fa769f442`. I freshly hashed the working file, immutable author snapshot and root publication copy; all match. I fully read `CANDIDATE3.diff` and `CANDIDATE3_FREEZE.json` and reread the changed source in context. The stored diff hashes to `6d2626edb280aec9a5ff273502bbee3292feb494ce2af56c0488880bb1e3024e`.

The changes are limited to the diagnosed representation and elaboration details:

1. Restriction of a covector is now built directly with `toFun ℓ := ℓ.comp V.subtypeL`, extensional proofs of linearity and continuity of composition with a fixed continuous linear map. This is the same restriction map used by the mathematical argument. Its concrete application also addresses the downstream restricted-Hessian evaluation problem.
2. C2 regularity uses `ContDiff.clm_comp` on the actual derivative covector and constant inclusion. The derivative proof analogously uses `HasFDerivAt.clm_comp` with the zero derivative of the constant inclusion and identifies the resulting map by extensionality. Neither change weakens smoothness or assumes a derivative.
3. The zero-evaluation rewrite uses the current `zero_apply` name.
4. The IFT eventual equation explicitly simplifies the chosen local name `r` and the product-zero projection, while retaining the same selected function and common neighborhood.
5. The derivative of the constant zero covector now calls `hasFDerivAt_const` with the covector value first and the ambient base point second.

I inspected the corresponding declarations at the already pinned Mathlib source: `Continuous.clm_comp_const`, `ContDiff.clm_comp`, `HasFDerivAt.clm_comp`, and `hasFDerivAt_const`. In particular, the last signature is value-then-point; the correction matches the actual source. This source compatibility is not a substitute for elaboration.

The direct restriction map evaluates to the same `Df(p+w+v)|V`. Strict-negative block invertibility, C3-to-C2 regularity, one selected implicit ridge and differentiation of its actual eventual equation are unchanged. All nine public declaration names/types and the final hypotheses/conclusions remain unchanged. The independently reconstructed proof and adversarial examples in the historical mathematical review remain applicable; no full repeated proof review was necessary. No additional premise, chart, LPC claim, axiom or admitted proof has been introduced in the diff.

## Publication binding for the next attempt

I freshly verified root's candidate 3 publication manifest SHA-256 `e652634cd6c80faaf889704b291e14c3ae2c25a3edb37fdec5f4c8273d17fb1b`. An independent textual comparison shows that only the CriticalRidge byte count/hash entry changes from the previous final manifest.

The corresponding workflow hashes to `8157a5f8ca2a92f6b31d7cb3c5834ce43423316394683d1c9b5e077a385c3add`; its only difference is replacement of the manifest digest. The copied driver and tests remain exactly `e4c5b9dd02e2ba2f98da27707c42ef861d9039b52864833d2164a3114f318f49` and `62400129fda7b863d692397deac2a9d83b7f1101d98b53ed1043f0ef8cfd604e`. Their E1 review and unconditional development HOLD remain applicable.

The changed source is a concrete reason for a new bounded attempt; it is not an unchanged retry of the native timeout or hosted failure. Actual final diagnostic qualification still requires reaching and reviewing the real negative fixtures. All historical failed-run records and preceding reviews remain intact.

## Limits and attribution

I performed only source/evidence reads, hashes and diffs and wrote this separate review artifact. No formal/test/mathematical program or remote action was executed, and no author source was edited. I am the actual source-exposed nonauthor reviewer, same provider, organizational independence credit 0, blind review 0, human review 0. No human review by Dylan is claimed; scientific effect NONE.

The ridge's actual compilation, complete census, named kernel checks and final formal acceptance remain unconfirmed. Critical neighborhood basis, quotient/full LPC, ordinary bars and scientific conclusions remain OPEN. Full research goal ACTIVE_UNMET.
