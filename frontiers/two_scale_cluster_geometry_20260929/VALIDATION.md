# Executed validation and scope

Scientific effect NONE. Finite tests are not analytic acceptance.

The mathematical companion was test-first: ten assertion failures were observed
against explicit missing-implementation stubs; implementation then passed those
ten tests and the expanded suite. A separate real-Git custody suite was written
against stubs: 19 tests produced 24 intended assertion failures (some tests had
multiple subcases), then all 19 passed after implementation. Logs are retained
in the conversation evidence bundle, not invented as upstream execution receipts.

Current standalone suite: 29 mathematical tests plus 19 custody tests = 48 tests
in each normal/optimized mode. The mathematical executable verifies 648 rational
stationary substitutions and exact root/weight/height constants. Eight semantic
mutants must each return1; an unknown mutant must return2. Normal and optimized
RESULTS.json outputs are byte-identical.

The source checker uses git ls-tree --full-tree for repository-root paths while
running from the nested packet directory. Fixtures include changed size/SHA/blob,
missing path, malformed commit, path traversal, leaf and parent Git symlinks,
missing/duplicate/empty inventories, duplicate JSON, and packet/manifest symlinks.
All six declared sources are mandatory; no prior or auxiliary source is skipped.

The local environment did not obtain a full network checkout of the project.
Therefore local-only replay explicitly reports source_pins_checked=false.
Actual project Git-object identities and the final packet inventory must pass
hosted replay at the published commit. Full downstream and existing Lean gates
remain separate and must be read at their current tested head/base. No local
full-repository run or Lean formalization of these new proofs is claimed.

Mathematical limits not validated by the checker: Gaussian rank/regression,
spatial root convergence, change-of-variables multiplicity, domination, two-scale
configuration topology, singular-support TV obstruction and the continuum tail
asymptotics. These are the written proof obligations for nonauthor reviewers.
