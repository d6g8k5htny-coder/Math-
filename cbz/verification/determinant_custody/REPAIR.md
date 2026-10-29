# Determinant source custody: test-first checkpoint

At exact tests-only head 0da245019678d354ec23e3aa6cd2fa17985c8215, native optimized job 123716184699 executed 11 real-Git tests and failed 10 assertions with no errors. The full relevant test output is preserved in optimized-red.log. The normal job was still queued when this repair was prepared.

This candidate binds the manifest, all package file bytes, external admission helper, loaded driver, and dependency tracked bytes to the observed commit and lock; checks HEAD before and after execution; rejects untracked Lean inputs and Git environment redirection. Its pre/post checks do not prove that input bytes could not be changed and restored during execution. The supported custody conclusion assumes source/dependency stability between observations; an actual read-only execution boundary would be needed to eliminate that assumption.

No source mutation controls, full component suite or kernel execution for this revised source are claimed yet. Existing numerical bounds and Lean files are unchanged.
