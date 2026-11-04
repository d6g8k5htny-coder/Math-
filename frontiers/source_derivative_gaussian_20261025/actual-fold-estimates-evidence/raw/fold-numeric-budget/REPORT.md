# Frozen scalar adaptive budget helper

Owner: OpenAI author-side scratch helper `/root/fold_numeric_budget` for producer
`/root/actual_fold_estimates_construct`. This is one same-provider contribution,
with zero provider-distinct review credit. Scientific effect NONE.

Binding task read first: `/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025/SOURCE_ACTUAL_FOLD_ESTIMATES.md`, binding published revision `48b2ffb8b3204108ad53f8f6ad4c7decd774196a` supplied in dispatch. Numeric section of `/workspace/scratch/actual-fold-estimates-preflight/REPORT.md` then read. No old qualification was repeated or erased.

## Frozen integration section

Copy exactly `FrozenSection.lean.txt`, whose namespace is `I4ActualFoldNumeric`.
It requires `import AdaptiveFoldBoundaryPath` (already qualified cached import).
Source `NumericBudget.lean` SHA256: `123bf1063c4d4360b656f68753caa75d3d58de1d143735344805037228489bfe`.
Section SHA256: `1fd2fb6af035481a5ae460da928bf9efa2dd029fe376bfe87e143af183570c71`.

The exact exposed theorem signature is:

```lean
I4ActualFoldNumeric.numerical_budget {T r κ : ℝ}
    (hT : 1 ≤ T) (hr : 0 < r)
    (hrT : r * T ^ 5 ≤ 1 / 100) (hκ : 1024 * T ^ 5 ≤ κ) :
    I4ActualFoldNumeric.NumericalBudget T r κ
```

`NumericalBudget` has precisely producer-requested fields `kappa_pos`, `c_pos`,
`radius_pos`, `radius_le`, `twice_T_le`, `strict_center`, `rT_le`, `slope_le`,
`error_le`, `curvature`, `capture`, `drop`, `radius_curvature_eq`.
The error uses the actual qualified `AdaptiveFoldBoundaryPath.profileError`,
with an internal proved `42*T^2/κ` estimate and exposed requested `72*T^2/κ` bound.
All denominator positivity and `Real.sqrt κ ^ 2 = κ` occur explicitly before use.

## New-only elaboration evidence

| Run | Exit | Measured seconds |
| --- | ---: | ---: |
| compile-001 | 1 | 23.406239902 |
| compile-002 | 1 | 15.284555911 |
| compile-003 | 0 | 15.476143935 |
| probe-001 | 0 | 3.762063000 |

`probe-001` only queried theorem signatures in a scratch import. `compile-001`
failed at the final `radius_curvature_eq` tactic because `eq_div_iff.mp` did not
match that goal. Every earlier required scalar estimate elaborated in that run.
`compile-002` failed solely on the strict unnecessary `<;>` linter after the
square-root identity correction. `compile-003` passed strict warning-as-error
elaboration with no output. No standalone helper kernel, axiom inventory,
controls, old build, or old hash audit was run. Producer owns its single final
integrated module's qualification and controls.

Each run preserves source snapshot (compile runs), stdout, stderr, exact command,
exit and elapsed wall time under `runs/`. `run.py` preserves the elaboration
command. This helper emitted no object: the producer must record the integrated
source/object identity as part of its new-module qualification.

The owner instruction in `/workspace/AGENTS.md` remains binding: completed,
applicable verification is reusable, and a new handoff alone does not warrant
rechecking. Pending provider-distinct process requirements remain separate from
completed mathematical evidence.

Standing owner onboarding links carried forward:
<https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OWNER_MANDATE_20261015.md>
and
<https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OP-AUTONOMY-20260923-v2.1.md>.
No statement that this helper read those external links is made.
