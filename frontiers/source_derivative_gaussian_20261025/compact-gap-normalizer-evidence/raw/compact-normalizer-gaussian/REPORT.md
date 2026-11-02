# Compact normalizer Gaussian lower-bound helper

26 October 2026, OpenAI/Codex `/root/compact_normalizer_gaussian`.
Scientific effect **NONE**; zero separate research targets and zero
provider-distinct review credit. This is author helper work for
`/root/compact_gap_normalizer_construct`, not independent review.

## Frozen delivery

Integrate `FROZEN_SECTION.lean` once into the new producer module. It is the
exact namespace section from the strict-elaborated `GaussianLower.lean`:

- Whole scratch source SHA256:
  `22266fc02dc57c3511d1d1b2da33b74cf85fb26ae464134d62c91f72d4e16863`
  (3713 bytes).
- Needed section SHA256:
  `2286f304a69e742b84d762f8df649d4788643237d67be90009ed2cfa76bf671f`
  (3532 bytes).
- Scratch-only elaboration object SHA256:
  `13ce7b56c3d87d4ea12c2d4a2ae2fde10e4d5bd37fa8567155bd4c1310e260f3`.

`FROZEN_HANDOFF.json` binds source, section, scratch object, imports and all
execution receipts. Never copy this helper object to the production cache.
The producer's one frozen new-module kernel check, actual-constant inventory,
axiom classification and controls cover the integrated helper section.
No separate helper kernel/audit/control run occurred.

## Exact API and mathematics

Namespace `SourceCompactGapNormalizer` contains four declarations:

```lean
def gaussianCompactLowerConstant (V M : ℝ) : ℝ :=
  (Real.sqrt (4 * Real.pi * V))⁻¹ * Real.exp (-(2 + M)^2 / V)

theorem gaussianCompactLowerConstant_pos {V : ℝ} (M : ℝ) (hV : 0 < V) :
  0 < gaussianCompactLowerConstant V M

theorem gaussianPDFReal_lower_compact (V M μ : ℝ) (ν : ℝ≥0)
  (hV : 0 < V) (hM : 0 ≤ M) (hμ : |μ| ≤ M)
  (hνlo : V / 2 ≤ (ν : ℝ)) (hνhi : (ν : ℝ) ≤ 2 * V)
  {x : ℝ} (hx : x ∈ Set.Icc (-2 : ℝ) (-1)) :
  gaussianCompactLowerConstant V M ≤ ProbabilityTheory.gaussianPDFReal μ ν x

theorem gaussianReal_Icc_lower_compact (V M μ : ℝ) (ν : ℝ≥0)
  (hV : 0 < V) (hM : 0 ≤ M) (hμ : |μ| ≤ M)
  (hνlo : V / 2 ≤ (ν : ℝ)) (hνhi : (ν : ℝ) ≤ 2 * V) :
  gaussianCompactLowerConstant V M ≤
    (ProbabilityTheory.gaussianReal μ ν).real (Set.Icc (-2 : ℝ) (-1))
```

The arbitrary bounded mean μ is preserved. On the interval, `|x|≤2` gives
`|x-μ|≤2+M`. The variance upper bound controls the inverse square-root
prefactor below; the variance lower bound controls the negative exponent
below. The proof explicitly derives `0 < (ν : ℝ)` from `V/2≤ν` and `V>0`;
the integral lemma also explicitly derives `ν≠0`. The Gaussian density is
integrable before Bochner integral comparison. The standard Gaussian integral
identity and the interval's exact length one yield the real mass lower bound.

The producer owns actual q-marginal composition, full product-law reuse,
parameter/radius choices, target mean bound and variance coercion from the
actual real variance. This section adds none of those model premises or laws.

## Scoped execution and retained failure

Only the new helper section was elaborated. Both commands had cwd
`/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025`:

```text
/home/agent/.elan/bin/lake env lean -DwarningAsError=true -R /workspace/scratch/compact-normalizer-gaussian -o /workspace/scratch/compact-normalizer-gaussian/build/GaussianLower.olean /workspace/scratch/compact-normalizer-gaussian/GaussianLower.lean
```

Each `runs/compile-00N/` retains its exact source snapshot, full output and
receipt with command, cwd, source/object identities, exit and UTC timings.
`compile-001` exited 1 after 3.0833 seconds: warning-as-error unnecessarySimpa
at the ν-nonzero contradiction. Replacing `simpa [h] using hνpos` with
`simp [h] at hνpos` resolves the linter. `compile-002` exited 0 with empty
output after 3.5889 seconds on the frozen source.

Lean 4.34.1 and Mathlib `d13f23b723b8a846827a245b89c10fc7d3f11612` are the
reused pinned environment, recorded previously in
`/workspace/scratch/gap-pin-curvature-construct/EXECUTION_ENVIRONMENT.json`.
The only imports are existing `SourceGapPinCurvature` and
`SourceCurvatureDecomposition`, using their qualified packet-cache objects.

## Reuse, authority and limits

Read `/workspace/AGENTS.md`, repository instructions/README, formal README,
SCOPE and required-check contract, the published PRECODE source contract and
plan, and `/workspace/scratch/compact-gap-normalizer-preflight/REPORT.md`.
Read the canonical local owner mandate, delegation and current workflow.
Preserve canonical links in future onboarding:

- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OWNER_MANDATE_20261015.md
- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OP-AUTONOMY-20260923-v2.1.md

Completed applicable verification is reusable evidence: 41 qualified source
modules/32 inputs and the old all-target Gaussian/product-law/upper-density
mathematics remain unchanged and were not replayed. New mathematical checking
was limited to the uncovered lower-density/unit-interval mass obligation.
Pending provider-distinct review is a distinct process and does not erase
completed mathematical evidence. No production/input/configuration/cache/
manifest write, worker, commit, post, standalone kernel, audit or control ran.
All helper writes are under `/workspace/scratch/compact-normalizer-gaussian`.
Root owns registration, publication and overall source qualification.
