# C293 author notes: finite literal quotient critical set

## Scope and source relationship

The assigned deliverable formalizes the finite-critical-set dependency already proved conventionally in C292, Section 4. It does not reopen or replace that conventional proof. The public endpoint is the finiteness of the full image of all `UniversalLaw.Spec.Lifetime.IsCriticalPoint` points under the actual C263 `TorusFiltration.torus_proj`.

The implementation imports only the supplied, source-verified `Lifetime.lean` and `TorusTopology.lean`; these import the pinned Mathlib. The literal Euclidean space, iterated-Frechet Hessian, inertia encoding, lattice scale, periodicity, and quotient remain unchanged. No product-of-circles torus is substituted.

The primary theorem `TorusMorseFinite.quotientCriticalSet_finite` assumes literal `IsSmooth`, `IsLPeriodic`, and `IsMorseDistinct`, with `L > 0`. Its core theorem only uses the nondegeneracy-at-critical-points conjunct of the Morse-distinct predicate. No finite event list, finite critical set, inverse certificate, closed-level path, elder pairing, or barcode conclusion is a premise.

## Proof structure

1. Identify the literal `iteratedFDeriv` Hessian with `fderiv` of `fderiv`, and derive its symmetry from real `C^2` smoothness.
2. For a kernel vector `z = v + w` in the complementary inertia subspaces, symmetry and the kernel equation give `B(v,v) = B(w,w)`. The opposite definite signs force `v = w = 0`. Cross terms are retained; the subspaces are not assumed Hessian-orthogonal.
3. Use the real Riesz equivalence and finite-dimensional injective-endomorphism equivalence to turn the derivative of `fderiv` into an actual continuous linear equivalence. Apply Mathlib's inverse function theorem to derive an isolating open neighborhood of each literal critical point.
4. Derive periodicity of `fderiv` by differentiating the exact lattice-translation identity. Construct the continuous dual-valued derivative on C263's quotient using `Quotient.lift` and prove the literal pullback identity.
5. Identify the quotient critical set with the zero set of this descended derivative. It is closed. The projection is open because the supplied C263 theorem constructs a covering map. Images of the Euclidean isolating neighborhoods isolate quotient critical points.
6. Apply actual quotient compactness and Mathlib's compact-discrete finiteness theorem.

The deterministic proof works for every natural dimension. C292's application retains its own `d >= 1` scope. There is no coefficient-field or limit-order change: the present theorem is real scalar deterministic geometry and has no asymptotic parameter.

## Deliberate mathematical boundary

This unit proves no Morse normal form and no closed-superlevel local path connectivity. Those remain substantive imports needed by the larger C292 closed-level attainment argument. Finiteness of quotient critical points is not a finite-event or elder-registration theorem, not a proof of all small bars or exhaustive once-counting, and not a regional shrinking-collision estimate. It does not modify an owner's separate elder-registration scope.

## Build and review status

Initial source written at approximately 2026-10-18 02:12 UTC. Both exact dependency modules compiled successfully with no stdout/stderr: `Lifetime.lean` in 186.78 seconds and `TorusTopology.lean` in 169.07 seconds, with unchanged input hashes. These builds were launched by the parent and their terminal receipts were read by the author.

The complete first author attempt compiled successfully in 135.75 seconds, exit code 0, no timeout, source unchanged. Its source SHA-256 is `514445e386599258472310fdab555006a206fba9c65ca864d4a7dc103cb5998c`; the exact source is retained as `project/AuthorProbeAttempt001.lean`. Receipt: `runs/20261018T021538Z-MorseFiniteCritical-092f8343/RECEIPT.json`. It emitted four warnings for deprecated `ContinuousLinearMap.add_apply` / `ContinuousLinearMap.zero_apply` aliases, with no errors.

The cleaned candidate changes only those four aliases to `add_apply` / `zero_apply`; no theorem statement or proof structure changes. Its source SHA-256 is `95a660134eda49eecfe6181884bd23b4e4ca210e228d2463de29e5f821df047b`, 9,445 bytes, 223 lines. The exact source is also retained as `project/AuthorProbeAttempt002.lean`. The targeted cleaned-source run is `runs/20261018T022037Z-MorseFiniteCritical-67cf4c01`. It completed at 2026-10-18 02:22:53 UTC in 135.41 seconds, exit code 0, no timeout, source unchanged, with empty stdout and stderr. The resulting `MorseFiniteCritical.olean` SHA-256 is `34ff2a9ed529609dd48a22204b8eacc66eeb943805e2d6e8dee4481cde8ef4e2`.

The author module is frozen at that cleaned-source hash for substantive review and parent final verification. Both author attempts succeeded; the first attempt's warnings are preserved rather than suppressed or discarded. A source scan found no `sorry`, `admit`, `axiom`, or `unsafe` declaration in the author module. This scan is not an axiom audit of the imported proof dependencies.

All author runs use the assigned bounded serial `run_lean.py` with Lean 4.34.1, two threads, 4096 MiB memory limit, 240-second timeout, and the supplied pinned dependency cache. No shared source or dependency cache is modified. Run receipts and source snapshots remain available. Parent final frozen-artifact verification, kernel/axiom audit, and substantive review are separate gates.

The author and assigned reviewer are same-provider and source-exposed. Neither source inspection nor author compilation constitutes independent scientific acceptance.
