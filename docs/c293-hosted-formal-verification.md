# C293 hosted formal replay — engineering-only registration

**Scientific effect: NONE.** This is source-bound, hosted Lean verification of C293's conditional finite-critical-class declaration; it is not acceptance of C292, elder pairing, or the persistence-lifetime law.

## Ownership, source and current gates

Source PR: https://github.com/d6g8k5htny-coder/Math-/pull/482 at exact head 0ea97aff489f9420632b4cee81ad82dbec5fe88e. The stacked CI branch is based on that head; it does not change source modules, source reviews, historical receipts, negative controls, or original evidence.

The existing required math-downstream-gates invokes the original formal-lean.yml, which builds the independent formal/ target. Neither that required job nor the existing torus-filtration.yml companion executes this new C293 declaration. The latter's Claude companion ownership and the separate Sol/elder-registration work remain undisturbed.

The addition is a dedicated C293 workflow named c293-morse-finite.yml. Its c293-hosted-formal job is **not a branch-protection-required context** and is not inserted into formal/gate.py or the required aggregate. Enforcing it as required should follow separately with current gate owners after hosted execution, capacity evidence, source review and readback.

## Hosted invocation and pins

The job uses Lean 4.34.1 and exactly the existing formal Lake project and its nine package pins, including Mathlib d13f23b723b8a846827a245b89c10fc7d3f11612. Python source checks compare all five C293 Lean modules to their published byte counts/SHA-256 values and require exact identity with the canonical Lifetime and TorusTopology upstream files. A mutated control, pin, source or upstream copy fails closed; normal and optimized test modes exercise the guard.

To repeat after installing the formal Lake dependencies, execute from the repository root:

    python3 -B -S tools/c293_hosted_verify.py source
    python3 -B -S -m unittest discover -s tests -p test_c293_hosted_verify.py -v
    python3 -B -O -S -m unittest discover -s tests -p test_c293_hosted_verify.py -v
    cd formal
    lake env python3 -B -S ../tools/c293_hosted_verify.py execute

The runner verifies tested GitHub commit, repository, run ID and attempt; Lean version; exact installed revisions and clean source; then compiles from new isolated outputs in the order Lifetime, TorusTopology, MorseFiniteCritical, MorseFiniteControls, MorseFiniteAxiomAudit. The three new modules use warnings-as-errors; all builds and the negative control use -j2 -M14000.

**Memory deviation:** The original author receipts use -M4096. Anthropic/Claude's provider-distinct Linux replay, recorded in https://github.com/d6g8k5htny-coder/Math-/pull/482#issuecomment-6246988654 , needed -M14000 for six build/negative invocations. This workflow records the new limit without altering the original receipts.

All five new .olean files must match the published object SHA-256 values. Three named-module leanchecker -v passes, the full 169-declaration (103/38/20/8) standard-only transitive axiom audit, and the exact intended missing-IsMorseDistinct rejection are mandatory. A nonzero result for an unrelated reason is not a pass.

The 90-day workflow artifact contains phase stdout/stderr, digests and exact-run RESULT.json. Hosted standard named-module replay is **not** a hosted leanchecker --fresh of the entire import closure. External --fresh is a separate evidence record; neither implies institutional mathematical acceptance.

## Source review and protected integration

This change should receive review of its *CI verifier*, not substitute for the source author's C293 mathematical review. Inspect the new hosted c293-hosted-formal job and its real logs on the exact tested PR merge; do not reclassify old green checks. Keep this implementation stacked until C293 source PR #482 receives its own legitimate integration disposition. Do not automatically merge into the source author's draft branch, alter rulesets, waive reviewer independence or set a scientific status. Before any later merge, re-check ownership, base/head, source hashes, reviews, gates and the protected merge process.

C293 does not close critical-level local path connectivity or path attainment, the full C292 adapter, almost-sure Morse, elder pairing, exhaustive once-counting, all-small-bars converse, regional collisions or stochastic lifetime transfer.
