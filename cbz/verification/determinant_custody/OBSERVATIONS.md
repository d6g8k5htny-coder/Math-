# Observed determinant custody adverse controls

At source head ac6f8f656d7e8fb5b4154be4ce6651d10bbfe293 (the ARM diagnostic descendant of source39eb978), normal job123731156582 and optimized job123731155933 each ran25 controls: 18 passes, exactly seven failures and zero errors. The seven are Git child environment redirect, nested build symlink, generated-audit/log/unreferenced evidence symlinks, and wrong-exit/wrong-reason mutation-grader false kills. All original output excerpts are retained alongside this file. This is actual RED on the old source; it does not qualify a fix.

The corrected x86 nested-build fixture at source164f084 ran16 tests in normal job123721658218, with exactly two failures and zero errors: nested build symlink and the already known inherited Lean path. The earlier fixture error is separately preserved. The later candidate implements the corresponding changes; its own full tests, reason-bound mutations and actual kernel build remain pending.

## Further observed source-specific checks

At source4c40d9e5 (initial guard before synthetic-fixture adaptation), x86 normal job123726212792 ran192 tests and produced3 failures and24 errors. Its failure output remains in x86-initial-fixture-red.log; it is not a result for the later source.

At ARM diagnostic source694b131e, normal job123737192089 and optimized job123737192406 each passed30 focused controls and detected all ten declared gate source mutants for their named reasons. The exact stdout/stderr excerpts are retained in arm-ten-guard-mutants-*.log. This predecessor predates the active-receipt ordering fix and the second grader self-mutation. The current source's corresponding full qualification remains pending.
