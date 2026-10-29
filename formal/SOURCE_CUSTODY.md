# Core receipt source custody

This wrapper closes the reproduced false commit qualification in the core gate.
It does not prove any additional mathematical statement or discharge application
hypotheses. The compiled proof collector in gate_helper.py remains byte-identical:
SHA-256 ff8a5374597772b2d37054fd722c2243c4b552a63802c69f7c605519832be6c4.

## Contract

Before execution and after the helper completes, gate.py checks the exact HEAD,
stage-zero index, working bytes, regular-file modes and SHA-256 manifest bindings
for every bound formal source plus manifest.json and manifest.overlay.json.
The checks read actual bytes independently of Git's assume-unchanged and
skip-worktree flags. An overlay refreshed only in the working tree cannot qualify
as committed source. Loaded wrapper/helper bytes must match the committed files;
the helper is compiled directly from the retained source bytes rather than
admitted from an unrelated Python bytecode cache. The final helper receipt must
name the preflight commit. Refused final observations remove the receipt while
retaining refusal logs. A new execution removes a stale receipt before admission.

Dependency observations verify all tracked files against each pinned Git tree
and index, and reject extra Lean source/compiled-interface files outside the
explicit .lake cache output domain. Owned formal symlinks and all gitlinks are refused. Dependency file symlinks
are checked by literal link bytes and their resolved, tracked in-repository
regular-file target; none is skipped. This preserves the three symlinks present
in the exact locked Batteries/Mathlib trees. These are preflight/final observations
in an isolated worktree, not a claim of continuous filesystem monitoring.
The dynamic run adapter passes the current effective formal root to each Lean
process and preserves an explicitly selected compiled-admission copy.

## Verification

From the repository root with Python 3.11.16:

    python -B -S -m unittest discover -s formal/tests -p 'test_*.py' -v
    python -B -S -O -m unittest discover -s formal/tests -p 'test_*.py' -v
    python -B -S formal/gate.py

For actual kernel execution install the exact Lean toolchain and locked
dependencies described in formal/README.md, retrieve the matching Mathlib cache,
then run:

    LEAN_NUM_THREADS=2 python -B -S formal/gate.py --execute

The Python tests simulate Lean process outcomes only in the explicitly named
orchestration fixtures. Their passes are not substituted for kernel execution.
test_source_custody.py uses real temporary Git repositories for source custody.
test_source_custody_mutation.py runs thirteen planted source regressions in
separate child processes and requires each selected control to fail for its
declared reason. Optimized parents explicitly launch optimized children.
The finite mutation threshold is 13/13, or 100 percent of the declared set.

## Observed source qualification

At commit 5522d13478b8ec0baa803a98356592ff1b8c1efe, native Actions run
40943199596 executed jobs 123691643285 (normal) and 123691643830 (optimized):
266 tests passed without skips in each mode, including all original 244 cases,
20 real-Git cases, one dynamic-cwd case and the eleven-mutation suite.
Both jobs passed source preflight with composite digest
7671f5cd7b126193f9c72f1175f9a6f2893c8d0248f452f027d8e3f6efe986f3.
Earlier RED run 40942448854 executed 18 tests in each mode and observed sixteen
assertion failures, with no setup errors, against the original wrapper.
Earlier 263-case fixture failures are preserved alongside the successful logs;
the fixture correction preserves subprocess.check_output's bytes/text contract.

Raw native job logs and their SHA-256 manifest are under
evidence/cbz-core-custody-20261029/. These are source-tool qualification
observations at their exact cuts. The fresh actual kernel run and its receipt
are recorded separately; source-test success alone is not a kernel certificate.

Maintenance owner: none; self-contained. Canonical federation tool registration
is in main/GOVERNANCE.md and main/TOOLING.md. This tool serves CBZ criteria
4, 6, 9 and 11 and preserves the existing mathematical bounds and target set.

## Superseded-run orchestration

.github/workflows/cbz-retire-superseded-runs.yml is a narrow trusted-push
administrative tool. It verifies seven typed selection controls, fully paginates
nonterminal runs, and re-reads both current PR head and run state immediately
before requesting cancellation of an obsolete PR source cut. It preserves all
current-head runs, test definitions and artifacts. It grants no test/kernel credit.
It uses an independent ARM runner pool because the shared x64 queue was saturated.

Observed run 40947126080/job 123705321047 passed the seven policy controls,
enumerated 93 nonterminal runs, retained 63 current/terminal records and requested
cancellation of 27 superseded records. The recorded actions are requests, not
claims that those tests passed or that every cancellation was already terminal.
The full actual report and raw job log are preserved with the source observations.
