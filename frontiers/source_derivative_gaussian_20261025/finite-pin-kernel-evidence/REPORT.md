# Finite pin-kernel implementation report

26 October2026. Producer `/root/actual_fold_candidate_construct` (OpenAI/GPT-6),
delegated by `/root`. Only `SourceFinitePinKernel.lean` and this scratch directory
were written. Scientific effect **NONE**; provider-distinct credit **0**.

## Frozen result and exact scope

Source6893 bytes, SHA256 `d45fbf6ca2d7a2c3e54a8edcd5d5c482497751ec1c3d820a1a198a204c8ce5d1`.
Eligible object `build/SourceFinitePinKernel.olean`,227840 bytes,
SHA256 `9d6ab1b544efd400b3ef2d58d1dedbafdd36563993a30558fa1e6fee2fdb362f`.
Only this source-bound named own-module object is cache-eligible; no ilean was
generated and no freshness compile was run. Root owns all cache/registration/
publication actions and local sourcecut `27184289e3bf49853b3e6fe3fa4f5b5bd4445af1`.
No current-source hosted-CI result is claimed from PRECODE checks.

The nine intended public declarations are implemented without scope amendment:
three definitions `finitePairing`, `residualCoefficient`, `finiteShiftSample`;
six propositions `finitePairing_residualCoefficient`,
`residualCoefficient_summable`,
`coefficientGram_posDef_of_finite_kernel_rightInverse`,
`finiteShiftSample_val`, `rawPins_finiteShiftSample`, and
`rawPosteriorSample_finiteShiftSample`.

The generic Gram theorem derives original-coefficient row separation from the
finite pin-kernel and original-observation right-inverse pairings, then reuses
`coefficientGram_posDef_of_separating`. R is arbitrary; no normal equations,
residual-rank/positivity certificate, Countable/Fintype coefficient index, or
covariance interpretation is assumed. It permits p=0 and q=0. Pairing order is
observation coefficient times direction coefficient.

The finite shift uses existing finite-change carrier invariance on the literal
original SmoothSample2L, for every realL including0. The exact raw pin response
uses the accepted weighted derivative series and a private finite-support
HasSum adapter. Posterior commutation holds for arbitraryr including0, arbitrary
six-targett and every original sample, with onlyhL:L≠0 and the explicit finite
rawpin-kernel identities. No invertibility, small-radius, Gaussian, Morse or
positive-gap premise was added.

This is finite witness algebra and deterministic same-carrier commutation. It
constructs no actual remote trigonometric jet witnesses/rank, Gaussian free-block
independence, conditional Morse/distinct-values theorem, endpoint determinant
nullity, Sard/tie result or elder/H0/Parent conclusion.

## New qualification and preserved failures

Control contract was frozen before source, matching the root-frozen contract.
PRECODE `72baa5feeaae88131ec7e3cc8daa479e1791da29` contract/plan were read explicitly;
pickup6414496852 at11:06:43UTC and checkpoint11:40/terminal12:40 were retained.
No timer reset, workers, old source edits or old verification campaign occurred.

- Werror development002 PASS11:10:06UTC,3.6525s, empty stdout/stderr. Its completed
  applicable evidence is reused on the unchanged final bytes, following the
  owner's `/workspace/AGENTS.md` rule. Explicit final freeze followed that compile
  and preceded inventory, controls and kernel; the plan's nominal ordering was
  not used to justify an identical-source relabel/freshness compile. The exact-source
  reviewer explicitly accepted strict-evidence reuse.
- Inventory001 PASS11:12:39UTC,3.9867s. Actual module-index exhaustive15 constants:
  **6 public written propositions,3 definitions,3 private written proof helpers,
  3 generated proof constants**. Every transitive axiom row is exactly the
  standard three: propext,Classical.choice,Quot.sound. No Prop bundles or extra
  public API. All generated/private declarations are separately classified.
- Controls002 PASS11:13:17UTC,4.2197s, empty streams. Fourteen substantive controls
  cover nontrivial pairing, a=(1,1),b=(0,1),v=(−1,1), arbitraryR positivity,
  R7 residual pairing, summability,p0/q0,originalL0carrier,concreteDCshift,
  raw response at0/arbitraryr,and everytargetposterior at0/arbitraryr.
- One distinct omitted-hker mutation, final false-kernel002, rejects at exactly
  one **False**,11:13:17UTC,4.3083s, no unrelated diagnostics. Fin1 a=b=R=v=1
  retains the original-observation right inverse but has zero residual Gram;
  the proved finite algebra counterexample is in context. This is not an actual
  source-jet sample. Attempt001's unused-simp warning is preserved without
  being credited as clean rejection.
- Exactly **one** named own-module kernel001 PASS11:14:05UTC,5.7586s, empty
  stdout/stderr. Source/object identities stayed unchanged throughout.

All **eight** actual invocations retain command,cwd,start/end,walltime,exit,
source snapshot,full stdout/stderr and available objects under `runs/`.
Development001 preserves renamed-Finsupp-lemma/missing-namespace failures;
controls001 preserves the finite-summability API and unused-simp failures.
Nothing was discarded or silently rerun. Structured records are
`RAW_LEDGER.jsonl`, `EXECUTION_RECORD_INDEX.json`, `SOURCE_OBJECT_IDENTITIES.json`,
`CONTROL_RECEIPT.json`, `INVENTORY.json`, `TARGET_CLASSIFICATION.json`,
`STATIC_SCOPE.json`, `AUTHOR_LINEAGE.json` and `HANDOFF.json`.

## Reuse and review

Completed45modules/1083targets/32inputs at8d86a06 and all applicable upstream
mathematics remain reusable. Prior actual-candidate source and its completed
checks were neither edited nor rechecked. Pending different-family/process
requirements do not erase that mathematics. No old build/kernel/audit/control/
hash campaign was replayed. No config,repository metadata,production cache,
commit or external action was performed by this producer.

Read-only exact-source source/spec review **PASS/no amendments**:
`/workspace/scratch/finite-pin-kernel-source-review/REPORT.md`. It inspected the
retained qualification records without reexecution; same OpenAI family gives
provider-distinct credit0. Root handles remaining publication/current-source CI
and separate provider-distinct process. No further mathematical recheck is
indicated for unchanged frozen material.
