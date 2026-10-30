# C296 Regular-Point Chart Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Kernel-check the literal regular scalar chart at a noncritical point of the project space `E d`, without weakening C294's closed-superlevel local-path-connectivity premise.

**Architecture:** Add one isolated Lean package based on Math- PR #487 head `7af365e8c8db1ae0275d4efe08a70a678f153ca2`. The package copies C294's exact `Lifetime.lean` input, proves only the strict-derivative/surjective-derivative chart interface, and carries positive, negative, and axiom-audit modules. A packet-specific GitHub workflow provides red-then-green hosted execution because the local runtime cannot read `/proc/<pid>/exe` in this environment.

**Tech Stack:** Lean 4.34.1; Mathlib `d13f23b723b8a846827a245b89c10fc7d3f11612`; GitHub Actions `leanprover/lean-action@f061402b660e0c34644504b324e830f2991d4865`.

**Spec:** `frontiers/critical_level_attainment_20261020/SCOPE.md`, narrowed by C295 finding `Math-#487/6289066726` and C296 pickup `Math-#487/6289277782`.

## Global Constraints

- Preserve every existing C294/C293 byte; the new packet is additive.
- Scientific effect remains NONE; no formal or scientific registry promotion.
- Do not prove or suggest a critical-point Morse chart, quotient transport, half-space relative LPC, or removal of C294's `LocallyPathConnectedSpace` premise.
- Pin Lean 4.34.1, Mathlib `d13f23b723b8a846827a245b89c10fc7d3f11612`, and every hosted source head used as evidence.
- Treat the local `/proc/<pid>/exe` denial as a stop for local Lean execution; do not patch or bypass it.

## Review Focus

- Noncriticality must be used to prove the scalar derivative is nonzero; the negative module omits exactly that premise.
- Continuous-linear-map versus linear-map coercion must preserve the exact derivative and range statement.
- First-coordinate equality is global as a function equality, while inverse/homeomorphism claims remain restricted to source/target.
- The base point and `(g x, 0)` must be proved members of the chart's source and target.
- No theorem may silently imply closed-superlevel local path connectivity at critical points.

---

### Task 1: Hosted red test for the missing project chart

**Files:**
- Create: `frontiers/regular_point_chart_20261020/lean-toolchain`
- Create: `frontiers/regular_point_chart_20261020/lakefile.toml`
- Create: `frontiers/regular_point_chart_20261020/Lifetime.lean`
- Create: `frontiers/regular_point_chart_20261020/RegularPointChart.lean`
- Test: `frontiers/regular_point_chart_20261020/RegularPointChartInterface.lean`
- Create: `.github/workflows/c296-regular-point-chart.yml`

**Interfaces:**
- Consumes: C294 `UniversalLaw.Spec.Lifetime.E`, `IsSmooth`, and `IsCriticalPoint` from the exact copied `Lifetime.lean`.
- Produces: a failing interface test naming the intended `regularPointChart` declaration and its source/target identities.

- [x] **Step 1: Write the failing interface test**

The test imports `RegularPointChart` and invokes the wished-for chart plus first-coordinate, self, source-membership, and target-membership declarations at arbitrary `d`, `g`, and `x` under smoothness and noncriticality.

- [x] **Step 2: Run the hosted test to verify it fails**

Run: open a draft PR from `codex/c296-regular-point-chart-20261020` to `codex/c294-critical-level-attainment-20261020` and wait for `c296-regular-point-chart`.

Expected: FAIL at the exact red commit because `regularPointChart` (or its first intended helper) is unknown; setup/toolchain/source errors do not count as RED.

- [x] **Step 3: Commit the red harness**

Commit message: `test: pin C296 regular-point chart interface`

### Task 2: Minimal literal chart implementation

**Files:**
- Modify: `frontiers/regular_point_chart_20261020/RegularPointChart.lean`
- Test: `frontiers/regular_point_chart_20261020/RegularPointChartInterface.lean`
- Test: `frontiers/regular_point_chart_20261020/WithoutNoncriticality.lean`
- Test: `frontiers/regular_point_chart_20261020/RegularPointChartAxiomAudit.lean`

**Interfaces:**
- Consumes: `(hg 1).hasStrictFDerivAt`, `Module.Dual.range_eq_top_of_ne_zero`, and `HasStrictFDerivAt.implicitToOpenPartialHomeomorph` at the pinned Mathlib revision.
- Produces: `regularPointDerivative_range_eq_top`, `regularPointHasStrictFDerivAt`, `regularPointChart`, `regularPointChart_fst`, `regularPointChart_self`, `mem_regularPointChart_source`, and `mem_regularPointChart_target`.

- [x] **Step 1: Implement only the derivative and chart declarations required by the failing interface test**

Use `fderiv ℝ g x` literally; derive strict differentiability from `IsSmooth`; convert noncriticality to a nonzero continuous linear functional, then to full scalar range; invoke the existing Mathlib chart.

- [x] **Step 2: Add the omitted-noncriticality interface rejection**

The negative module must fail by leaving the required `¬ IsCriticalPoint d g x` argument unsupplied. The workflow must require a nonzero exit and a diagnostic mentioning `IsCriticalPoint`; timeout/import/syntax/unknown-production-identifier failures do not count.

- [x] **Step 3: Run hosted tests to verify they pass**

Expected: positive modules build with warnings as errors; the negative module is rejected for the intended missing premise; named-module `leanchecker` and the axiom audit succeed.

- [x] **Step 4: Commit the minimal implementation**

Commit message: `feat: instantiate the regular scalar chart`

### Task 3: Freeze source identities and hand off review

**Files:**
- Create: `frontiers/regular_point_chart_20261020/README.md`
- Create: `frontiers/regular_point_chart_20261020/SCOPE.md`
- Create: `frontiers/regular_point_chart_20261020/SOURCE_SHA256SUMS`
- Create: `frontiers/regular_point_chart_20261020/RESULTS.md`

**Interfaces:**
- Consumes: exact green head, workflow run/job identities, test streams, and Git blob/SHA-256 identities.
- Produces: a source-bound reviewable packet and explicit release record; no acceptance or integration claim.

- [x] **Step 1: Record exact source, toolchain, positive/negative, axiom, and hosted-run identities**

- [ ] **Step 2: Re-run the full hosted workflow at the frozen documentation head**

Expected: all C296 jobs green at the new exact head; previous green evidence is stale if source bytes changed.

- [ ] **Step 3: Commit documentation and request bounded nonauthor review**

Commit message: `docs: freeze C296 execution scope`

- [ ] **Step 4: Post result/release on Math-#487 and pointer on main#419**

The release must state exact head, source blobs/digests, run IDs, negative-control reason, axiom scope, local platform denial, and all exclusions.
