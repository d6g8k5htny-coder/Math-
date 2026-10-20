# C299 nonauthor engineering source review — first collector freeze

Actual reviewer: OpenAI Codex `/root/c299_nonauthor_review`, delegated by root chat `01a0bbb5-2fcb-77f0-b78b-4d220ddd7ab2` for Dylan Roy. Source review only; no program, Lean, compiler, test or workflow was executed by this reviewer. Native checkpoint: 2026-10-20 14:08:41 UTC.

**Disposition: AMEND before development dispatch for one concrete environment-receipt gap (E1).** The source otherwise implements the declared five-build/four-kernel/four-origin-census development sequence, with an unconditional final HOLD. This review is not formal verification or final negative-control qualification.

Root accepted E1 and assigned a narrow engineering amendment. This preliminary record preserves the original reviewed identities; a successor needs its own exact diff review. The mathematical candidate remains accepted at source scope under `b3c22e590f761953ba322ad2903978e3982179204ad5c4a166dffc5fa1558322`, with formal gates unconfirmed.

## Exact reviewed source

I fully read and freshly hashed these root publication files:

| File | Bytes | SHA-256 |
|---|---:|---|
| `publication/c299_hosted_verify.py` | 28907 | `126d1aa5b0dfd87eca4fa939d55d969020301e7d61a0a48eb063dfabfa7a2005` |
| `publication/test_c299_hosted_verify.py` | 13920 | `be6a5cc800446c9684cf77537437abafb1f2bbb8238dd042c15dc41dec916dfc` |
| `publication/project/CriticalRidgeAxiomAudit.lean` | 2728 | `cff55f5b7721a621530ae1020b81e6cc89ce5c405396145e1ca5d3cfba4b2fb7` |
| `publication/negative-project/WithoutCriticality.lean` | 944 | `6ebc44de843b951c312add4848962d76c4788cc10bdacf17002eb69fd370f1d2` |
| `publication/negative-project/WithoutNegativeDefiniteness.lean` | 872 | `ad204aee211aa3074621f56eeaf8e1a3f3a522b7c7cbe2bbdd67f3759833feb9` |
| `publication/HOSTED_SOURCE_MANIFEST.json` | 1731 | `3c80ed35bc7a28342b127ca08f046be913021ab28ff13119e698c981eb0aef6b` |
| `publication-workflow/c299-critical-ridge.yml` | 3030 | `70e7396d868f00097a862895954ad19962d9df96cb1d8c44a655b76e5e5874a1` |

I also fully read the publication's README, execution contract and upstream byte-equality record, plus the helper's additive amendment handoff. I independently compared the draft and publication workflow: the only difference is replacement of the manifest placeholder with the exact `3c80ed35...` digest. I freshly hashed all four copied proof/input sources; their hashes match the final manifest and the previously reviewed mathematical candidate.

The final manifest uses all three input origins at commit `7af365e8c8db1ae0275d4efe08a70a678f153ca2` under `frontiers/critical_level_attainment_20261020/final-project`. I read root's record of remote/native byte equality. I did not independently perform those remote fetches, and the driver explicitly leaves remote origin-byte equality to that separate custody check. The helper's historical candidate manifests are not substituted for the final publication manifest.

## Finding E1: effective environment is not retained

At driver lines 436–438 the child environment is copied from `os.environ`, its `LEAN_PATH` is prefixed with the new object directory, and its `LEAN_NUM_THREADS` is set to 2. The runtime probes, all five builds, kernel checks and fixtures receive that environment. The aggregate and phase receipts record commands, working directory, runtime/source/object identities and resource bounds, but they do not record the resulting `LEAN_PATH`, `PATH`, or a relevant Lean/Lake/loader override policy and its effective non-secret settings.

This leaves an actual evidence gap: the retained receipt cannot independently show the import-path precedence or the relevant inherited overrides used by the subprocesses. The code recipe and source identity document how the environment is constructed; they do not preserve the actual inherited values. Source/command binding is present, environment binding is incomplete.

The requested amendment is bounded evidence work: retain selected safe execution-environment fields and an explicit removed/preserved override policy, including the actual import search path. Do not dump the full process environment or credentials. The original collector has no final-acceptance bypass through this omission because final acceptance is unconditionally disabled, but dispatch should wait for the agreed source-bound amendment. I supplied no implementation patch and edited no engineering source.

## Sequence and scope reconstructed from source

The source gate requires an explicit manifest digest and exactly five named Lean sources plus two fixtures. It checks both length and SHA-256, rejects symlinked listed source paths, validates all three origin records, checks the repository's separate literal Lifetime source, and checks the Lean toolchain and exact nine package revisions. It records hashes of the verifier, its tests and the workflow. Runtime origin-byte verification is not implied by those checks.

The preflight binds actual GitHub repository, run, attempt, workflow and job, `GITHUB_SHA`, checked-out commit/tree/parents, and available PR head/base. It snapshots exact local source/support bytes before execution. Execution requires the unused source-preflight result and refuses an automatic retry. It creates the output directory with `exist_ok=False` and places that directory first in `LEAN_PATH`.

The five builds run in dependency order: Lifetime, TorusTopology, MorseFiniteCritical, CriticalRidge and CriticalRidgeAxiomAudit. Each must add its own main `.olean`, may add only its own declared auxiliary output suffixes, and must preserve prior objects. The full local output set is validated after builds. The four standard named-module kernel invocations cover TorusTopology, MorseFiniteCritical, CriticalRidge and CriticalRidgeAxiomAudit. Lifetime is freshly built and included in the axiom census but is intentionally excluded from the named-kernel loop; the documentation states that boundary.

The Lean audit enumerates `env.constants` by actual origin module index for Lifetime, TorusTopology, MorseFiniteCritical and CriticalRidge, with exporting disabled. It checks the declaration's presence in the kernel environment, collects every enumerated declaration's transitive axioms, rejects anything outside `propext`, `Classical.choice`, `Quot.sound`, and checks required names. It does not merely audit a sample of theorem names. The nine new public C299 declarations are required targets, alongside four consumed input declarations; they are not the census denominator. The audit module itself is built and kernel checked, but is not a fifth imported-origin census.

The Python census parser checks module order, module counts, every printed declaration, duplicate names, allowed axioms, the total, required targets, interrupted/truncated wrapped arrays and unknown audit markers. The current source supports the stated complete local-origin audit, subject to actual Lean elaboration and actual output still being unobserved in this review.

The runtime is resolved through the selected launcher, measured as actual `lean` and `leanchecker` binaries, version checked, and those exact binary paths are then used. Installed package Git revisions and tracked modifications are checked before and after. Dependency generated-object bytes are not comprehensively rehashed or rebuilt; this is the disclosed cached-import boundary, not a fresh verification of the entire Mathlib closure.

## Negative controls and final HOLD

Both fixtures import the actual candidate and reproduce its full four-part existential conclusion. WithoutCriticality retains negative definiteness and explicitly abstracts over the missing middle criticality premise. WithoutNegativeDefiniteness leaves the actual final negative-definiteness premise unapplied. These are intentionally ill-typed interface controls; they are not themselves mathematical counterexamples.

The prospective parser requires return code 1, exactly one source-named type mismatch, the actual theorem expression, precisely the omitted-premise-to-conclusion actual type, and all four exact expected conclusion fields. It rejects unrelated import, syntax, resource, panic, sorry and extra-error output. The spelling is explicitly prospective: real Lean pretty-printing has not yet qualified it.

The development loop attempts both distinct fixtures even if the first diagnostic spelling or exit is rejected, while an object-integrity failure aborts dependent work. Raw streams and each process receipt are persisted before classification errors propagate. A phase's `status: PASS` at this stage means the process had its expected exit and retained object integrity; it does not mean the missing premise was semantically verified. Every negative receipt explicitly keeps `intended_missing_premise_rejection=false` and `diagnostic_qualification_pending=true`; the aggregate sets `negative_predicates_qualified=false`.

Even if both prospective parsers match, `require_final_predicates()` unconditionally raises before the PASS assignment. No flag, command-line option, optimization-dependent assertion or fallback path bypasses that gate in this frozen driver. Any failure keeps aggregate `HOLD_NOT_COMPLETED`. The first hosted attempt can collect evidence but cannot establish final formal acceptance. A later qualified acceptance driver requires exact actual-diagnostic review, an explicit changed source identity and the applicable complete final sequence.

## Evidence persistence and reviewed tests

The driver preserves raw binary stdout/stderr, their sizes and hashes, command, working directory, timestamps, timeout/exit/spawn status and before/after object inventories. It terminates the child process group on timeout and records failures. Source identities are checked after each build and again after all controls; runtime binaries and object sets are checked again at the end. Amended per-phase records are saved with the aggregate. The workflow uploads the evidence directory on failure as well as success; a cancelled or missing upload is not established custody.

The workflow uses pinned action commits, read-only repository permissions and no persisted checkout credentials. It disables lean-action's ordinary build/test/lint and runs the explicit dedicated sequence. Runtime and mathematical success remain conditional on the actual hosted attempt and evidence readback. The final workflow's platform time cap does not extend the cooperative claim lease.

I read the full 11-control Python test source, the helper's two AMENDED_GREEN terminal receipts and both complete stderr reports. Those author records report return code 0 and eleven passing controls normally and under Python `-O`. Their controls exercise changed source hashes, missing audit targets, forbidden axioms, wrapped/truncated records, altered negative conclusions/premises, failed/timeout stream persistence, imported-object mutation, allowed new objects, receipt consistency, source admission and unconditional final HOLD. I did not rerun them. Synthetic diagnostic fixtures validate parser behavior only; they cannot establish actual Lean output or a formal theorem.

## Final boundary

Only E1 requires an amendment before the intended development dispatch in this review. No other blocking source defect has been identified in the reviewed collector at this stage. This is a bounded source judgment, not a claim that the first Lean run will compile or that all possible failure modes are exhaustively tested.

Reviewer is source exposed, same provider, nonauthor of the verifier and mathematical implementation; organizational independence credit 0, blind review 0, human review 0. Scientific effect NONE. The critical-basis, quotient/full-LPC, ordinary-bar and wider scientific obligations remain OPEN; full research goal ACTIVE_UNMET.
