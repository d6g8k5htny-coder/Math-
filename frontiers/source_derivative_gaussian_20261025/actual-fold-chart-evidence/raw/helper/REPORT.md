# Actual fold chart: finite coordinate and pullback helper

26 October 2026. Scratch-only author-side helper for
`/root/actual_fold_chart_construct`. Owner directory:
`/workspace/scratch/actual-fold-chart-jets`. No production/shared source,
lakefile, manifest, commit, post, kernel check, declaration/axiom audit,
control, or subagent operation was performed by this task. Scientific effect:
NONE. Author/provider: OpenAI. Different-family review credit: zero.

The workspace owner clarification of 25 October 2026 is binding: completed
applicable verification is reusable, unchanged material is not checked again
because of a new agent or handoff, and provider-distinct process requirements
remain separate from mathematical verification. The existing 32-module and
25-input evidence and accepted source/Peano identities were reused. None of
those old proofs or checks was rerun. The producer's integrated new module
will cover the needed declarations in its one required kernel/audit workflow;
this helper did not duplicate that workflow.

## Binding and coordination

Read before implementation:

- `/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025/SOURCE_ACTUAL_FOLD_CHART.md`,
  supplied frozen publication binding `0d802f10b68254068f23348ca8a63ea225180772`.
- `/workspace/scratch/actual-fold-chart-preflight/REPORT.md`.
- Workspace and repository `AGENTS.md`; the former's verification-reuse rule
  is carried above. Repository canonical onboarding links remain
  <https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OWNER_MANDATE_20261015.md>
  and
  <https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OP-AUTONOMY-20260923-v2.1.md>.

The supplied publication identity is a source binding, not the result of a
new old-source hash/control check. Existing API source bodies were inspected
read-only. No old module elaboration or kernel checking was requested.

Namespace/interface were agreed directly with the producer before authoring:
`I4ActualFoldChartJets`, generic `V`, first derivative scales, axial third
identity, center transverse identity, smoothness. The producer then requested
the two scalar axial curve bridges, and confirmed their generic
`G : ℝ × ℝ → ℝ` signatures before the final freeze.

## Frozen source and one-time integration

Frozen complete source:
`frozen/ActualFoldChartJets.lean`, identical to the successful checked input
`runs/005/ActualFoldChartJets.lean`.

Complete source SHA256:
`b40252ce1d537414657a5a952fdb97975206d83afd6bd148de35d88fd394aa3b`.

Integrate the needed bodies **once**, with this author-side attribution, from
source lines 4–164 inclusive. Exact bytes are also in
`frozen/IntegrationSection.lean.txt`; they include `noncomputable section`,
opens, namespace, and final namespace end, and exclude the two imports and
following blank line. Section SHA256:
`89ced04bcf5de1eaeccf73e7fdc22b0954a3059fa044159725176db8042112fc`.

Required imports are exactly:

```lean
import SourcePinPreservingQuartic
import AdaptiveFoldTransverseRidge
```

The first supplies the already proved Pi-domain component smoothness and
ordered component derivative identity. The second supplies the actual
qualified `Vx`, `Vy`, `ex`, and `ey`. No Mathlib umbrella import, admission,
custom axiom, `native_decide`, or `implemented_by` is present. The task makes
no separate declaration-axiom-audit claim.

Successful checked object: `runs/005/ActualFoldChartJets.olean`, SHA256
`5ce1fa5e5dab4f28890765a42243016f7bc59643c8d1fb6d7ffd989ca6c818b1`.
Own-source/section/object byte identities are recorded in
`frozen/IDENTITY.json`; they do not replace mathematical checking.

## Exact exported interface

The following are in `I4ActualFoldChartJets`. Here `directionX` and
`directionY` are the existing qualified `I4SourceConfluentPins` definitions,
and all partials below are the actual qualified definitions from
`AdaptiveFoldTransverseRidge`.

```lean
def coordMap : (ℝ × ℝ) →L[ℝ] (Fin 2 → ℝ) :=
  ContinuousLinearMap.pi ![ContinuousLinearMap.fst ℝ ℝ ℝ,
    ContinuousLinearMap.snd ℝ ℝ ℝ]

@[simp] theorem coordMap_apply (p : ℝ × ℝ) :
  coordMap p = ![p.1, p.2]

def chartMap (r : ℝ) : (ℝ × ℝ) →L[ℝ] (Fin 2 → ℝ) := r • coordMap

@[simp] theorem chartMap_apply (r : ℝ) (p : ℝ × ℝ) :
  chartMap r p = r • ![p.1, p.2]

def V (f : (Fin 2 → ℝ) → ℝ) (r k : ℝ) (p : ℝ × ℝ) : ℝ :=
  f (r • ![p.1, p.2]) / (6 * k * r ^ 3)

theorem V_contDiff (f : (Fin 2 → ℝ) → ℝ)
  (hf : ContDiff ℝ (⊤ : ℕ∞) f) (r k : ℝ) :
  ContDiff ℝ (⊤ : ℕ∞) (V f r k)

theorem pullback_jet (f : (Fin 2 → ℝ) → ℝ)
  (hf : ContDiff ℝ (⊤ : ℕ∞) f) (n : ℕ) (a r : ℝ)
  (p : ℝ × ℝ) (v : Fin n → ℝ × ℝ) :
  iteratedFDeriv ℝ n (fun q => a * f (r • ![q.1, q.2])) p v =
    a * r ^ n * iteratedFDeriv ℝ n f (r • ![p.1, p.2])
      (fun i => ![(v i).1, (v i).2])

theorem Vx_eq (f : (Fin 2 → ℝ) → ℝ)
  (hf : ContDiff ℝ (⊤ : ℕ∞) f) (r k : ℝ) (hr : r ≠ 0)
  (p : ℝ × ℝ) :
  AdaptiveFoldTransverseRidge.Vx (V f r k) p =
    fderiv ℝ f (r • ![p.1, p.2]) directionX / (6 * k * r ^ 2)

theorem Vy_eq (f : (Fin 2 → ℝ) → ℝ)
  (hf : ContDiff ℝ (⊤ : ℕ∞) f) (r k : ℝ) (hr : r ≠ 0)
  (p : ℝ × ℝ) :
  AdaptiveFoldTransverseRidge.Vy (V f r k) p =
    fderiv ℝ f (r • ![p.1, p.2]) directionY / (6 * k * r ^ 2)

theorem axial_third_eq (f : (Fin 2 → ℝ) → ℝ)
  (hf : ContDiff ℝ (⊤ : ℕ∞) f) (r k : ℝ) (hr : r ≠ 0)
  (p : ℝ × ℝ) :
  fderiv ℝ (fderiv ℝ (AdaptiveFoldTransverseRidge.Vx (V f r k))) p
      AdaptiveFoldTransverseRidge.ex AdaptiveFoldTransverseRidge.ex =
    iteratedFDeriv ℝ 3 f (r • ![p.1, p.2])
      ![directionX, directionX, directionX] / (6 * k)

theorem transverse_center_eq (f : (Fin 2 → ℝ) → ℝ)
  (hf : ContDiff ℝ (⊤ : ℕ∞) f) (r k : ℝ) (hr : r ≠ 0) :
  fderiv ℝ (AdaptiveFoldTransverseRidge.Vy (V f r k)) (0, 0)
      AdaptiveFoldTransverseRidge.ey =
    iteratedFDeriv ℝ 2 f 0 ![directionY, directionY] / (6 * k * r)

theorem curve_deriv (G : ℝ × ℝ → ℝ)
  (hG : ContDiff ℝ (⊤ : ℕ∞) G) (u : ℝ) :
  deriv (fun t => G (t, 0)) u =
    AdaptiveFoldTransverseRidge.Vx G (u, 0)

theorem curve_iteratedDeriv_three (G : ℝ × ℝ → ℝ)
  (hG : ContDiff ℝ (⊤ : ℕ∞) G) (u : ℝ) :
  iteratedDeriv 3 (fun t => G (t, 0)) u =
    fderiv ℝ (fderiv ℝ (AdaptiveFoldTransverseRidge.Vx G)) (u, 0)
      AdaptiveFoldTransverseRidge.ex AdaptiveFoldTransverseRidge.ex
```

The algebraic scale identities need only `r ≠ 0`; no `k ≠ 0` premise is
needed because Lean's real division identities also agree at `k = 0`.
The producer's physical application assumes positive `r,k` as required.
No unproved norm isometry, Euclidean norm transport, mixed-partial symmetry,
new source law, or ridge existence is claimed. The center identity retains
the required physical `r` denominator.

## Calculation used

`pullback_jet` is a single short calculation from the explicit CLM chain
rule, constant multiplication, and multilinearity. It is generic in `n`
because the same proof is shorter than separate finite proofs; no general
affine calculus library was added. `Vx_eq` and `Vy_eq` specialize order one.
`axial_third_eq` applies the order-two pullback to the existing actual
physical derivative component. `transverse_center_eq` applies order one.
Both invoke the existing `derivativeComponent_iteratedFDeriv`, whose
`Fin.snoc` places the fixed differentiated direction last. The curve bridge
uses the literal product-domain axis CLM and the actual coordinate partial.
No existing Pi-line or component theorem was reproved.

## Commands, preserved failures, and measured times

All five compilation inputs and complete stdout/stderr are preserved under
`runs/001` through `runs/005`. Each `meta.json` records the exact argv, cwd,
start time, measured Python `perf_counter` elapsed seconds, and Lean exit.
`run_compile.py` is the exact runner. All attempts were strict
`-DwarningAsError=true`, and each new revision was checked only to address
the errors from the previous revision.

| Run | Lean exit | Measured seconds | Result / obligation addressed |
| --- | ---: | ---: | --- |
| 001 | 1 | 0.6220843380069709 | External scratch input needed explicit Lean package root. |
| 002 | 1 | 4.183154287995421 | First elaboration: CLM application coercions, implicit point, surplus solved-goal tactics, and scalar composition expression. |
| 003 | 1 | 3.459594220003055 | Explicit smoothness goal and chain-rule rewrite; deprecated `ContinuousMultilinearMap.smul_apply` replaced with `smul_apply`. |
| 004 | 1 | 5.311498887997004 | Remaining smoothness lambda needed the product type annotation. |
| 005 | 0 | 9.312634333997266 | Final source passed with empty stdout/stderr. |

Run 005 exact command, cwd the source package directory:

```text
lake env lean --root=/workspace/scratch/actual-fold-chart-jets/runs/005 -DwarningAsError=true -o /workspace/scratch/actual-fold-chart-jets/runs/005/ActualFoldChartJets.olean /workspace/scratch/actual-fold-chart-jets/runs/005/ActualFoldChartJets.lean
```

The runner records compile status itself; its own Python process exited zero
after printing each record, including failed Lean attempts. Run 001 omitted
the later `--root=...` option. Full commands are retained in the run records.

One preliminary read-only source search exited 2 because one requested
Mathlib source path did not exist; exact command and error are retained in
`inspection-failure-001.md`. It was an API-location lookup, not proof
verification. No separately measured wall time was taken for read-only
inspection/edit/freeze commands; do not infer one from compilation timings.
No mathematical verification was repeated after run 005: its exact input
bytes were frozen and sent for integration.

## Handoff boundary

The producer owns actual-field wrappers, raw and normalized endpoint pins,
the actual-law/common-interval result, Peano use, polynomial controls,
integrated-module qualification, and source publication. This helper is only
the deterministic coordinate/jet calculation. Its zero different-family
credit and the preserved verification-reuse rule must accompany integration.
