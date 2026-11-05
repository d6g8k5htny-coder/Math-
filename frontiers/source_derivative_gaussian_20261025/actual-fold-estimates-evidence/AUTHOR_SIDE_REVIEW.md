# Fresh author-side source review: actual fold estimates

## Scope and exact review target

Reviewed the new `SourceAdaptiveFoldEstimates.lean` only, against the binding
`SOURCE_ACTUAL_FOLD_ESTIMATES.md` and `SOURCE_ACTUAL_FOLD_ESTIMATES_PLAN.md`, read
first. The binding published pre-code revision supplied at dispatch is
`48b2ffb8b3204108ad53f8f6ad4c7decd774196a`.

The review target is the immutable
`/workspace/scratch/actual-fold-estimates-source-review/SOURCE_AT_REVIEW.lean.txt`
and its `REVIEW_PACKAGE.diff`: supplied SHA256
`980d8f238a085c6fc56bfffd0af278bcc248fb2f523c15662b603957b36c8a20`,
43,120 bytes, 896 lines. This supplied source identity was not rehashed. All
line references below refer to that frozen source, not a later working copy.

Reviewer: OpenAI Codex, fresh same-family author-side review. This contributes
**zero different-family/provider-distinct review credit**. No subagents were
used. The only written artifact is this report; no source edits, builds,
tests, kernels, controls, axiom/inventory/hash rechecks, commits, or posts were
performed.

The workspace owner instruction on reuse of completed applicable verification
is binding. Accepted 34-module/25-input qualification, actual-source/Peano,
boundary/path, Cap and H0 mathematical evidence remains reusable. Narrow reads
of the chart, source-majorant, weighted-integral and boundary-constructor
interfaces resolved the new assembly's dependencies; this was not an old-proof
reaudit. The two helper reports were read and their completed scratch evidence
reused. A pending process requirement does not invalidate that mathematics.

## Findings and verdicts

- **Critical:** none.
- **Important:** none.
- **Minor:** none.

**SPEC compliance verdict: PASS for the frozen new-source mathematical and
interface contract.** Both required closed endpoints and all finite analytic
ingredients are present with the prescribed constants, domains and premise
discipline. This source review does not certify completion of the separate
producer qualification, controls, evidence registration or publication tasks.

**Mathematical task-quality verdict: PASS within the requested conditional,
centered fixed-axis slice.** The source derives the wider rectangle and the
attained boundary/path from actual source derivative bounds and the normalized
actual law. I found no hidden desired conclusion, domain contraction, norm
substitution, omitted physical scaling, quantifier weakening, or additional
vacuity assumption.

## Substantive review basis

| Obligation | Frozen-source assessment |
| --- | --- |
| Exact sample, scale and constants | Lines 285–289 define exactly `T = max 1 (1/(6*k₀)) * (8*sourceGammaRadius L sample)` and `κ = -sourceQ L sample/(6*k*r)`. The physical radius remains in the denominator. The closed statements at 848–861 and 872–886 repeat these literal definitions on the same `sample`, with `V = actualFoldPotential r k sample`, `R = 4/sqrt κ`, `c = κ/2`, `M₀=T`, `M₁=3*T`, `M₂=T`, and `A=2-3*r*T`. |
| Ordered actual third and fourth bounds; norms | Lines 314–348 prove the product/max-norm to Pi/sup-norm inclusion is contractive and derive a full actual operator bound from `pullback_jet` and the accepted actual source derivative majorant. Lines 350–374 specialize this to third bound `T` and fourth bound `r*T`, using `k₀≤k` with `k₀>0`. This legitimately supplies the stronger operator hypothesis used later; no entrywise-to-operator or Euclidean substitution occurs. Lines 519–531 bound every ordered third coordinate triple; 834–844 bound arbitrary ordered fourth tuples of axes. |
| Fixed component last, both mixed orders, source symmetry | Lines 376–436 establish the ordered wrappers with physical Y or X appended last. Lines 447–484 transport the proved actual source permutation identity to `Hy=Gx`. The assembly retains separate ordered Gxy/Gyx and Hxy/Hyx entries at 799–807 and 813–831, with literal tuples `ex,ey,ey`, `ey,ex,ey`, `ex,ey,ex`, and `ey,ex,ex`. |
| Two pins on the full older interval | The integrated helper at 20–169 proves the quadratic envelope and derivative bound for all of `J=[-3/2,3/2]`. Its convex comparison explicitly treats both outer arms; Rolle supplies a derivative zero between the pins. Lines 745–756 instantiate it with the actual transverse component, actual full third bound and normalized actual pins. The resulting center bound is `T`, not a central-only `T/8` bound. |
| Coordinate mean-value transport | Lines 486–617 use the newly derived full operator bound in the mean-value inequality, then the proved product norm estimate `‖p-q‖≤|Δx|+|Δy|`. They obtain all requested Gy, Gx, Hy and K oscillations, including the `r*T` coefficient for K. The full operator bound makes this route valid with the stated coordinate constants. The transverse center identity at 597–601 gives exactly `Gy(0,0)=-κ`. |
| Full rectangle derivative/sign bounds | Lines 758–780 use the full `J` and `|y|≤R≤1/8` to obtain `|Gy+κ|≤2*T`, `Gy≤-κ/2`, `|Gx|≤3*T`, and `|Hy|≤3*T`; no old half-unit gate is used. Lines 680–712 prove strict vertical boundary signs by the mean-value consequence of `Gy≤-c` along the complete vertical segment. Lines 781–785 supply the strict margin using `c*R=2*sqrt κ` and `T<2*sqrt κ`. |
| Peano normalization and axial lower bound | Lines 630–638 reuse the accepted Peano mass identity to get mass 1. Lines 641–678 derive weight nonnegativity, compare K at every point of the full rectangle with all pin-interval axial points using distance at most 3, and apply the completed `abs_weighted_integral_sub_mass_le` at scale 1. The actual normalized integral is 2, giving `|2-K(x,y)|≤3*r*T`. Lines 821–825 use the correct side of that absolute-value estimate for `Hxx≥2-3*r*T`. Old Peano mathematics is not reproved. |
| Numerical budgets and positivity | The integrated numeric helper at 173–281 derives all budget fields from precisely `1≤T`, `0<r`, `r*T^5≤1/100`, and `1024*T^5≤κ`. Positivity of κ, c and sqrt κ and the sqrt-square identity appear at 200–204 before divisions or squared comparisons. The internal error bound is `42*T²/κ`, the exposed bound is the allowed safe `72*T²/κ`, and curvature/capture/drop are proved. Lines 735–737 instantiate the helper with the actual T and κ; 786–812 assemble the exact structural fields and both actual budgets. |
| Closed law quantifiers and premise discipline | Lines 848–868 choose `δ` from `sourceGapLaw_normalized_fold_data hL` before introducing `k₀,r,b,k`; thus δ depends on hL alone and satisfies `0<δ≤1`. The law is exactly `sourceGapLaw hL r b k`, with arbitrary real b and positive k derived from `0<k₀≤k`. Only the two advertised numeric cutoffs remain as implications. Normalized data is an internal premise at 719 and is discharged under the actual law at 865–868. No final IsUnit, pin, desired sign, structural, derivative/profile, ridge, path or budget premise remains. |
| One attained witness and scope | Lines 872–894 reuse the closed structural theorem and call the qualified `exists_transverse_ridge_boundary_path` with the derived capture/drop budgets. A single `U,z` carries both `RidgeScalarData` and `RectangleBoundaryPathData`. The source claims no probability of satisfying the cutoffs, framed/isotropic result, physical torus injectivity, elder/H0 interpretation or Parent A/B join. |
| Source hygiene | Lines 1–3 import the two qualified modules and the narrow Rolle module. Reading the frozen source found no admissions, custom axioms, `native_decide`, `implemented_by`, or full Mathlib umbrella import. The exhaustive classified axiom/inventory qualification remains producer-owned. |

## Reused helper lineage

The source integration annotations at lines 19 and 171 identify the two
disjoint helper bodies once. Their supplied frozen section identities and
completed scratch evidence are reused, without fresh scratch elaboration,
kernel or hash checks:

- Two-pin helper: source
  `d85a5ff3e6be506b1762dfe91a6f0a3efc44229311b4f448c0b90e84b0b31038`,
  section
  `5cd3f6ef111a6045e4e3a8b52af6bec5c5f2616b77131c7e5452560c73a4f87c`;
  report `/workspace/scratch/fold-two-pin-bounds/REPORT.md`.
- Numeric helper: source
  `123bf1063c4d4360b656f68753caa75d3d58de1d143735344805037228489bfe`,
  section
  `1fd2fb6af035481a5ae460da928bf9efa2dd029fe376bfe87e143af183570c71`;
  report `/workspace/scratch/fold-numeric-budget/REPORT.md`.

Both helpers and this review are same-provider author-side contributions.

## Qualification and provider-process limits

The producer's new-module qualification was concurrent with this review. No
final producer receipt was supplied or assumed. The strict final-source
compile, exactly one own-module kernel, exhaustive classified inventory/axiom
coverage, required positive and negative controls (including the sole-False
omitted-κ rejection and nonzero-b/`k≠1/6` closed-law exercise), recorded
failures/commands/exits/timings and source-object bindings belong to that
separate evidence package. This report makes no claim that those tasks have
finished and requests no duplicate execution of completed applicable checks.

Provider-distinct new-source review remains a separate process requirement;
this OpenAI review earns zero such credit. Scientific effect remains NONE.
Any source change after the supplied frozen cut requires only a review of the
actual changed scope and its affected obligations; unchanged accepted material
must retain its completed evidence.
