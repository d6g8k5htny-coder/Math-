# Constructed C2 transverse ridge — author-side source review

Date: 26 October 2026. Read-only review; the sole written artifact is this report.

## Scope and identity

The frozen contract was read from commit `66037c5`, path
`frontiers/source_derivative_gaussian_20261025/SOURCE_ADAPTIVE_FOLD_TRANSVERSE_RIDGE.md`.
The reviewed implementation is the 533-line `SOURCE_AT_REVIEW.lean.txt` supplied
with `REVIEW_PACKAGE.diff`, corresponding to the new
`AdaptiveFoldTransverseRidge.lean` only.

Reviewed source SHA256:
`715b01c2ae3b6e2bceb4196e53361530c8c9c69550e7cf675904cd5661b3de20`.
The production source in `/workspace/Math-curvature-20261026` was byte-identical
when inspected. Findings and line references below apply to that exact snapshot.
Any later source change needs a review limited to that change.

This is an OpenAI same-family, author-side review. It supplies **zero
different-family scientific-review credit**. No external API or coordination
seat was used.

## Findings and verdicts

No Critical, Important, or Minor findings.

**Specification-compliance verdict: PASS for the reviewed source.** The final
theorem `exists_unique_c2_transverse_ridge_with_jets` (lines 477–531) constructs
the requested objects and packages the required conclusions. This verdict does
not substitute for the separately required qualification artifacts.

**Mathematical task-quality verdict: PASS for the reviewed source.** The theorem
establishes the intended structural existence/regularity step rather than
assuming an existing ridge or presenting a weaker auxiliary lemma as the final
result. No hidden desired regularity premise, circular construction, invalid
denominator cancellation, or product/Euclidean norm identification was found.

## Substantive review

- **Literal derivatives and structural inputs.** Lines 22–27 define the
  coordinate vectors and actual `fderiv` partials. The potential theorem takes
  C4 regularity on an open `O`, rectangle inclusion, positive `R,c`, the actual
  negative second vertical partial, and strict boundary signs (lines 202–214,
  477–494). No ridge, ridge continuity, elder certificate, or scalar-barrier
  conclusion is a premise of either existence theorem.
- **Collar and construction.** The collar lemma takes the interior of the set
  of structurally good slices (lines 43–81). Compactness of the full closed
  vertical interval upgrades joint neighborhoods to a horizontal neighborhood,
  retaining domain inclusion, the `-c/2` margin, and strict boundary signs.
  IVT plus strict antitonicity constructs a unique interior root on each collar
  slice (lines 84–115). Choice occurs only after this proof (lines 181–198).
- **Regularity without assumed continuity.** Lines 144–166 build the local
  C2 implicit function from the proved vertical invertibility, keep that local
  function in the vertical interior by its own continuity, and use already
  established root uniqueness to prove eventual equality with the chosen
  function. Thus C2 regularity is a conclusion. Full first and second
  derivatives follow on the open `U` (lines 234–242, 499–505), including the
  original interval endpoints whenever they belong to that interval.
- **Actual jets and nonzero denominator.** Lines 245–306 differentiate the
  actual zero equation twice, including the derivative of the tangent vector.
  The resulting formulas use the actual `Gx`, `Gy`, and `D2G`. Vertical
  concavity proves and retains the nonzero denominator in the final theorem
  (lines 498–505, 517–520); it is not silently assumed there.
- **Structural numerical bounds.** Lines 354–383 explicitly expand all four
  bilinear coordinate terms. Lines 386–422 bound division using the negative
  denominator and coordinate estimates. Lines 425–470 prove the center-to-root
  estimate using the scalar mean-value inequality on the full vertical segment.
  The final hypotheses place `M0,M1,M2` bounds on the rectangle, independently
  of the chosen ridge, and the final quantitative conclusions use the stronger
  original `-c` bound on `Icc l u` (lines 485–507, 521–529). No numerical bound
  is incorrectly extended to the collar where only `-c/2` is supplied.
- **Potential/profile jets and scope.** Lines 311–351 define the literal
  potential restriction and horizontal-partial profile slope, and prove all
  three full derivative statements. Lines 508–510 instantiate these for the
  constructed ridge. The source claims no actual Gaussian-source structural
  sign adapter, ambient boundary/path theorem, elder/counting theorem, or
  Parent A/B closure. It has no full `Mathlib` umbrella import.

The quantifiers are coherent: root uniqueness is slice-wise on `U`, arbitrary
behavior of the global extension outside `U` is immaterial, and the numerical
bounds concern the original interval. There is no `l ≤ u` premise, so an empty
`Icc l u` is allowed; this is a valid generalization, not a claim of nonempty
ridge behavior for a reversed interval. For a nonempty intended interval, both
endpoints lie in `U`. Similarly, a separate `0 ≤ M0` premise is unnecessary:
the center bound implies it at every point where a quantitative conclusion is
requested.

## Evidence versus remaining process

The binding `/workspace/AGENTS.md` instruction was honored: completed applicable
verification is reusable, and a new review, session, handoff, or pending process
requirement does not erase it. The accepted unchanged 31-module/25-input and
pinned-Mathlib evidence was not replayed or re-audited.

This review performed no Lean build, named-kernel replay, axiom/inventory run,
positive/negative control, source edit, commit, post, or publication. The
producer was qualifying the frozen source concurrently. No new producer
qualification report was available at the inspected scratch locations when
this report was written; therefore this report neither asserts nor rejects
completion of the new-only compile, named replay, exact standard-three-axiom
inventory, substantive controls, and artifact/lineage preservation obligations.
Their evidence must be recorded separately and reused once available.

Provider-distinct scientific review remains a separate process requirement;
this same-family source review does not satisfy it. Neither that pending
process requirement nor the concurrent qualification stage changes the
established mathematics of unchanged accepted material.
