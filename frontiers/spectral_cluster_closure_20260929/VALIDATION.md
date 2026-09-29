# Verification record at author publication

Scientific effect NONE; finite evidence is not analytic acceptance.

Actual local execution:
- Initial mathematical stub:12 tests,12 intended assertion failures. Expanded stub checks followed.
- Initial implementation replay exposed one erroneous positive fixture: x=2,U=1,r=1/10,a=1 violates the premise x<=aU^2+ar^2x^2 since2>1.04. Corrected the test to x=1, without weakening the premise or modifying the valid implementation.
- Mathematical suite including CLI checks:32 tests pass in normal and optimized modes.
- Source-custody placeholder:13 tests produced17 expected assertion failures including subtests; valid fixture passed. Implemented complete Git-object/mode and byte identity checks.
- Full local suite:45 tests pass in normal and optimized modes. The deterministic checker output matches RESULTS.json. Eight named false variants exit1 in each mode; unknown labels exit2. All packet identities are generated from exact local bytes.

Custody fixtures use real isolated Git repositories. They cover wrong size/SHA256/blob, missing path/commit, unsafe paths, duplicate source IDs, empty inventories, duplicate JSON, Git leaf and parent symlinks, and packet symlinks. Source verification authenticates the pinned tree/blob rather than following a worktree link.

The container could not obtain a complete remote checkout, so actual project Git-object verification is not claimed local. Default hosted replay is configured to fetch and verify EVERY declared source, including historical audit and prior-credit entries. Hosted success and full repository/formal checks must be read at the actual current PR head before any integration. No Lean formalization of the new analytic proof is claimed.

## Hosted nested-directory repair

Initial hosted run36646437664 failed at source verification, job109670396383, because `git ls-tree` interpreted the pinned repository-root path relative to the nested packet cwd. Both source fetches and inventory authentication had succeeded; the error was not a missing upstream proof. A new real-Git nested-packet regression failed before repair (None!=1). Adding `--full-tree` makes root-relative source paths independent of cwd. The mathematical PROOF.md and all premise identities remain unchanged. Latest local suite:46 tests per mode. The original failing hosted run is retained; the successor still needs its own hosted result.
