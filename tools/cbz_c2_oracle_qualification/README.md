# Exact C2 oracle qualification

Component ID: CBZ-C2-ORACLE-QUALIFICATION. This is a finite external qualification of `reviews/c2_interval_audit_20261001/oracle.py`, not a new numerical engine. The original oracle, its tests, review packet and source packet remain unchanged. The source pin is SHA256 `b462b1b24613f74abd66042e0f347f69423595e9a1aedf1c6b45197425afe075`, Git blob `094bdf84bc8be7aedb4e50e1b1b3732ce0e6f112`, observed at Math `e877242cf68fb24c605066f16dd07f513ee75a1d`.

The only mathematical output scope is the nine supplied closed forms for c, c2 and c2/c in dimensions1,2,3. Their identification with Gaussian persistence coefficients, the analytic derivation, full arithmetic-engine correctness, kernel verification, semantic completeness and federation qualification are not established here. The original positive-real Stirling remainder argument remains in the original REVIEW.md; the tests do not replace that argument.

## Replay from the Math root

Use Python3 with its standard library only. The observed runtime was Python3.12.14. Every output path below must be new; repeat with different names when preserving another run.

```
python3 -B -S tools/cbz_c2_oracle_qualification/test_qualification.py --report-json /tmp/c2-external-normal-NEW.json
python3 -B -O -S tools/cbz_c2_oracle_qualification/test_qualification.py --report-json /tmp/c2-external-optimized-NEW.json
python3 -B -S tools/cbz_c2_oracle_qualification/test_runner.py -v
python3 -B -O -S tools/cbz_c2_oracle_qualification/test_runner.py -v
python3 -B -S tools/cbz_c2_oracle_qualification/run_mutations.py --evidence-dir /tmp/c2-cut-normal-NEW
python3 -B -O -S tools/cbz_c2_oracle_qualification/run_mutations.py --evidence-dir /tmp/c2-cut-optimized-NEW
```

Original packet controls remain separate:

```
cd reviews/c2_interval_audit_20261001
python3 -B -S -m unittest -v
python3 -B -O -S -m unittest -v
python3 -B -S verify.py --local-only
```

Local-only packet verification does not authenticate unavailable historical upstream Git objects.

CI wiring is in `.github/workflows/c2-interval-audit.yml`. The original peer-source authentication and run block are preserved verbatim. The tool directory is eligible for pull-request execution. An added step runs all 19 current runner controls and both full declared mutation campaigns in normal/optimized modes, each campaign including its complete 25-case baseline. A new temporary directory retains copied original/tool sources and process evidence. The pinned upload-artifact action runs after a started qualification step even when it fails; retention is explicitly 30 days. Local step replay is recorded separately from any actual hosted result, which is not anticipated here.

## Verification domain

The25 external methods check exact inputs/cache aliases, dyadic and decimal outward rounding, interval corners/zero division, integer powers, selected atan/log/exp remainders, radical brackets, Gamma domain/log-Gamma(1)=0, the nine literal endpoint pairs, and results scope/containment. Wrong computed intervals, missing references, incomplete computed keys and falsified published pairs are actually injected with temporary patches. The exp-tail test temporarily uses a finer output grid to expose an omitted positive term; the original source and production240-bit setting remain unchanged.

The original `results()` raises on false containment and missing references. It does not itself reject a missing computed key. The external qualification assertion independently requires the exact nine-key set; the source-key-omission mutant demonstrates this check. This qualification must not be represented as adding that guard to the preserved original oracle.

The12 declared mutants change the original oracle source, not expected output data: exact-type guard, dyadic upper rounding, zero-divisor rejection, atan/log/exp remainders, root upper endpoint, Gamma remainder, decimal upper rounding, results containment, missing-reference silent omission and computed-key omission. Each has a literal unique anchor and a named test. The campaign first runs the complete25-case baseline; a test added or removed without updating the inventory causes refusal. Each mutant then runs its explicit intended test. The100% threshold means all12 of this finite inventory, not all possible defects or programs.

A kill requires an exit1 unittest assertion failure in that exact named method, matching case identity/count and source hash, with no errors, skips, unexpected successes or launch/timeout/source-change failure. Multiple failing subcases are normalized to their real parent method. An exit0 mutant survives; a crash, malformed/missing report, wrong assertion or changed case inventory is INVALID. Baseline failure prevents mutant admission. Stale/ambiguous substitutions and original source-pin changes are refused before a cut executes. The CLI returns0 only for its fully qualified declared cut,1 for a failed cut,2 for refused input. Its output explicitly keeps kernel, semantic and federation certificate flags false.

Twelve real-process/unit runner controls exercise a passing baseline, intended assertion, survivor, startup crash, input-dependent crash, skipped child, unintended assertion, stale/ambiguous anchors, altered source pin, newly added baseline case, stale campaign and an original changed after its initial pin read. All 12 passed normally and with `-O`. The original 38 methods and the external 25 baseline also passed in both modes; all 12 declared source mutants were killed in both modes. Earlier RED and harness-correction evidence is retained in the candidate receipt. The admitted baseline must match the original pin at execution, and the original must remain unchanged through the completed campaign.

That12-control cut is historical. The repaired collector now emits `unittest.body-phase/v1`: supported lifecycle, successful setup, actual body entry/exit, successful teardown and completion of every cleanup, plus typed per-test event counters. A kill requires each designated failure to be an actual BODY AssertionError; fixture-phase failures refuse even if their ID and exit match. The complete baseline must attest every body. The current19 runner controls include real setup/teardown/cleanup counterexamples, a genuine body-kill positive, counter-provenance falsifiers and direct stale-output refusal in both modes. Existing probe output remains refused without overwriting its observation. Only new phase-sealed source-bound cuts qualify this repaired source; the prior12 mutant observations are not retroactively relabelled.

## Ownership and maintenance

Owner:none. Maintenance:zero; dormant until deliberately edited. Any change to the oracle pin, tests, runner, declared mutations or scope requires another baseline, runner-control and complete declared mutation cut. `REGISTRY.json` records this component's bounded tool entry. No reserved reviewer, approval queue, background process or root-document writer is installed.
