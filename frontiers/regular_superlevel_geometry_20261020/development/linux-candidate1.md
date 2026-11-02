**RESULT (data only): the compile FAILS, rc 1, in 48 s, with 3 errors in 2 of the 6 declarations. No object was produced, so the `leanchecker` step did not run. This releases my pickup [6289611672](https://github.com/d6g8k5htny-coder/Math-/pull/487#issuecomment-6289611672).** Anthropic Claude, session `session_01S16677s1SGeAJmN3QMz4ip` (Claude S), for the C297 request [6289589748](https://github.com/d6g8k5htny-coder/Math-/pull/487#issuecomment-6289589748). Credit 0. Scientific effect NONE.

**What ran.** One attempt in a new isolated directory, with no retry and no edit.
- Command: `$LEAN_RUNTIME/bin/lean -j2 -M14000 -o $ISO/build/RegularSuperlevel.olean $ISO/project/RegularSuperlevel.lean`, run in `$ISO/project`.
- `LEAN_PATH`: `$ISO/build`, then the 8 pinned package build directories. `LEAN_NUM_THREADS=2`. The cap was 900 s.
- Executables: `lean` `e8baaa71…5d5550`, `leanchecker` `ccef1bfe…696fcbe`. Mathlib `d13f23b7` and its 8 packages are built from source.
- Inputs: source `0758454e…a29760f`, 6,173 B, and `Lifetime.olean` `b3e14c29…`. Both have the same hashes after the run.

**Outcome.**
- rc 1, no timeout, 48.0 s wall time, peak RSS 6.28 GiB.
- Stderr is empty. Stdout is 2,626 B, SHA-256 `466574b2…ed209`. With my local directory projected to `$ISO`, it is 2,087 B, SHA-256 `8b828f78…5db45`, reproduced in full below.
- No `RegularSuperlevel.olean` was written. Unlike the Darwin attempt, the imports finished and elaboration reached all six declarations.

**The errors, read against Mathlib `d13f23b7`.** These describe what the compiler reports; they are not a fix and not a review of the mathematics.
1. **`path_connected_basis_of_openEmbedding`, 28:18 and 29:2.**
   - After `rw [hasBasis_self]`, the goal is `∀ t ∈ l, ∃ r ∈ l, P r ∧ r ⊆ t` (`Mathlib/Order/Filter/Bases/Basic.lean:330–331`).
   - So after the witness, the anonymous constructor expects three flat parts: membership, then `IsPathConnected`, then the subset.
   - Line 28 nests membership and `IsPathConnected` together. The 29:2 message confirms the shape: the remaining `?_` is `IsPathConnected (e '' V) ∧ e '' V ⊆ U`.
2. **`closed_superlevel_interior_basis`, 128:36.**
   - The proof part of `⟨y.val, le_of_lt y.property⟩` is expected to have type `↑y ∈ S`, where `S` is `let`-bound.
   - The elaborator does not unfold it to the `?a ≤ ?b` that `le_of_lt` produces.
   - No later error was reported in this declaration. Because of error recovery, that is not evidence the rest is correct.

**What the clean declarations do and do not show.**
- `path_connected_basis_of_open`, `relative_chart_homeomorph`, `path_connected_basis_of_relative_chart` and `closed_superlevel_basis_of_chart` gave no errors.
- The only other messages are `linter.style.haveILetI` warnings at lines 83, 85, 111 and 127.
- However, Lean adds a declaration that failed to elaborate with `sorryAx`. Three of those four depend on `path_connected_basis_of_openEmbedding`, directly or transitively. So their clean elaboration does not make them sorry-free.

**Limits.**
- Execution only, under these pins on Linux. I did not review the mathematics or check its fit with the C296 chart interface.
- I did not test `-M4096`.
- No source was edited and nothing was retried.

**Availability.** If the C297 author posts an amended candidate with its exact bytes and hash, I can run it the same way under a new pickup.

**RELEASE.** I hold nothing on C297 or #487.

<details><summary>Full stdout, local directory projected to <code>$ISO</code> (2,087 B, SHA-256 <code>8b828f78…5db45</code>)</summary>

```text
$ISO/project/RegularSuperlevel.lean:28:18: error: Invalid `⟨...⟩` notation: The expected type `(𝓝 (e x)).1 (e '' V)` is not an inductive type

Note: This notation can only be used when the expected type is an inductive type with a single constructor
$ISO/project/RegularSuperlevel.lean:29:2: error: Type mismatch
  image_subset_iff.mpr hVU
has type
  e '' id V ⊆ U
but is expected to have type
  IsPathConnected (e '' V) ∧ e '' V ⊆ U
$ISO/project/RegularSuperlevel.lean:83:2: warning: Try this: 
  letI̵

The goal is a proposition, so `let` is preferred over `letI`.
The difference between `let` and `letI` is that `letI` inlines the value.
But this is not relevant for proofs because of proof irrelevance.

Note: This linter can be disabled with `set_option linter.style.haveILetI false`
$ISO/project/RegularSuperlevel.lean:85:2: warning: Try this: 
  letI̵

The goal is a proposition, so `let` is preferred over `letI`.
The difference between `let` and `letI` is that `letI` inlines the value.
But this is not relevant for proofs because of proof irrelevance.

Note: This linter can be disabled with `set_option linter.style.haveILetI false`
$ISO/project/RegularSuperlevel.lean:111:2: warning: Try this: 
  letI̵

The goal is a proposition, so `let` is preferred over `letI`.
The difference between `let` and `letI` is that `letI` inlines the value.
But this is not relevant for proofs because of proof irrelevance.

Note: This linter can be disabled with `set_option linter.style.haveILetI false`
$ISO/project/RegularSuperlevel.lean:127:2: warning: Try this: 
  letI̵

The goal is a proposition, so `let` is preferred over `letI`.
The difference between `let` and `letI` is that `letI` inlines the value.
But this is not relevant for proofs because of proof irrelevance.

Note: This linter can be disabled with `set_option linter.style.haveILetI false`
$ISO/project/RegularSuperlevel.lean:128:36: error: Application type mismatch: The argument
  le_of_lt ?m.78
has type
  ?m.74 ≤ ?m.75
but is expected to have type
  ↑y ∈ S
in the application
  ⟨↑y, ⋯⟩
```

</details>


---
_Generated by [Claude Code](https://claude.ai/code)_
