# Isolate signing on disposable legacy-workflow fixture commits

Dylan Roy — delegated AI engineering. Actual author OpenAI / GPT-6 Astra Pro,
`legacy-fixture-signing-20261006-r11`, pickup Math-#348/6009734461.
Scientific effect **NONE**; source-exposed, organizational-independence credit0.
No author self-merge or change to ordinary repository signing policy.

## Scope and exact predecessor

This is an isolated follow-on to #348 head
`b5c8fe833548a671e4eae9764c15b47acbc5aee4`, NOT a modification of that author's
branch and NOT permission to merge into it. The final route is after the actual
#330/#348 parent integration, current-main residual diff and applicable checks,
then separate eligible integration. Their owners retain their scopes.

The predecessor test file is
`tests/test_legacy_json_workflows.py`, Git blob
`ef2fa58503334d647333922bd688b1dec0023036`, SHA256
`491e5572d01ea693406a6ed482af0baf3a1cc9dbf4c044a5d2fa4afce4f1063d`.
The complete helper `30b1194d606835e785ebfba65e131254776ac84f` and contracts
`349fc3276ce02ba80aecd7ecc897e37349c65007` are unchanged.

The #348 reader's completed review6009308695 recorded one ambient signing
commit timeout in its normal run and an isolated success with signing disabled.
That historical observation is not rewritten as a full successful normal run.
This change addresses the disclosed signing dependency, not the parent's separate
TTY-width repair or #342's automatic-maintenance mechanism.

## Smallest behavioral change

Only the disposable commit inside `LegacyWorkflowTests.case` gains
`-c commit.gpgsign=false`. Git's explicit command configuration overrides the
inherited configuration for that invocation. It is not written into a repository,
home/global configuration, or later command. Normal project commits continue to
follow their signing settings. No signing key, signing agent or user credential
is accessed, created or changed.

All fifteen existing test methods are AST-identical. All module definitions other
than that commit argument and the new `LegacySigningTests` class are unchanged.
The three workflows, protocol helper, 17 measured rejection reports, scientific
checkers/results/manifests and formal sources are not edited. Existing direct
invocation of this test file discovers the two new methods without workflow changes.
The original 15-second commit and 45-second shell limits are unchanged.

Configuration reference: https://git-scm.com/docs/git-config
(`commit.gpgSign` and the ENVIRONMENT paragraph: explicit `git -c` takes precedence
over GIT_CONFIG_COUNT key/value pairs). The repair is command-local, not a global
instruction to disable signed commits.

## Regression is real-process, key-free and fail-closed

The new tests run actual Git and the complete existing fixture, not a mocked
subprocess. Their private child environment removes inherited GIT_* variables,
turns off system/global file reads, and provides a synthetic signing configuration
with commit.gpgsign=true, gpg.format=openpgp and a nonexistent synthetic key label.
The configured signer is an inert local shell script: append one marker and exit17.
It cannot produce a signature. The probe is POSIX-only and explicitly skips elsewhere.

For each active workflow family, a separate interpreter invokes the real
`LegacyWorkflowTests.case`. It must complete the full expected checker inventory,
return success and empty stderr, record exactly one actual fixture commit, and
never invoke the inert signer. Before and after, the inherited signing setting
must still read true. No suppressed exception or empty trace can pass these checks.
A separate positive control commits without the override and must fail after the
real signer child and its exact marker are observed. This proves the hostile
configuration and trace can detect the behavior the fix excludes.

## Actual local execution

CPython3.13.5 / Git2.47.3 / Linux, standard library. Source reconstruction was
checked against native Git identities before import; direct GitHub DNS failed.
This is a selected-source environment, not a full repository checkout.

Before adding the command option, both normal and optimized focused runs reported
**two methods / three intended family assertion failures / zero errors**, exit1.
The positive-control method passed; each real fixture commit reached the inert
signer and failed before its checker. After the option, both focused runs passed.

Final whole-file runs on the exact candidate:
- normal: **17/17 OK**, exit0, 86.544s;
- optimized: **17/17 OK**, exit0, 86.968s.

Both retain the prior fifteen methods and their existing whole-shell/PTY behavior;
the new two methods add three family signing-isolation cases and one real signer
positive control. These are not new mathematical tests. Ordinary unittest stderr
is retained; empty stdout agrees, but elapsed-time stderr is not byte-identical.

One earlier full normal run was interrupted by a 180-second external tool deadline
without a completed verdict. Its partial output is retained and not counted as
success or as a repaired test defect. The final two independent runs above
completed with bounded 900-second outer process budgets, no retry inside tests.

Run from the repository root:

```sh
python -B -S tests/test_legacy_json_workflows.py
python -B -O -S tests/test_legacy_json_workflows.py
```

For RED sensitivity, keep this new class but restore only the original fixture
commit argument. Run `LegacySigningTests` in each mode: three intended assertion
failures, zero errors; positive control must still succeed.

## Assurance and integration boundaries

This eliminates the demonstrated inherited signing dependency for this specific
disposable commit. It does not identify every historical timeout, authenticate
normal signed commits, suppress maintenance, repair all fixture environment
contamination, or guarantee operation under hostile templates/hooks/arbitrary Git
settings. The inert OpenPGP-program test is not execution of the original reviewer's
SSH signer or a real key operation.

Fresh applicable hosted checks and one nonauthor engineering review are required.
An existing parent PASS does not review these new bytes. Do not claim local Lean,
a new scientific calculation, numerical certification, full field alignment,
physical Mac installation or whole-program closure. Preserve all prior failures
and exact source/review identities. No protection, sharing or scientific-status
change is part of this follow-on.
