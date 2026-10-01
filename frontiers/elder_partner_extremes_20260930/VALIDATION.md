# Author-side validation, not analytic acceptance

The initial eight-method mathematics scaffold failed all eight assertions.
After implementation those eight passed. Expanded mathematics tests now total28.
The separate13-method source/inventory scaffold produced20 failing assertions,
including subtests. A local attempt to reuse an older verifier found no mounted
file at that path and left the scaffold unchanged; its failed replay was not
called success. The completed verifier was then written and all13 tests passed.

Fresh final baseline:41 tests PASS in normal Python and41 PASS with -O, both
also under the hosted GIT_NO_REPLACE_OBJECTS=1 environment. Each mode executes
all six named semantic mutants (return1) and an unknown label (return2), with
identical deterministic baseline stdout and no stderr. Mathematical core:
-893 rational shape/selector/companion checks;
-40 direct original-cubic gradient/value/Hessian cases;
-12 independent exact inner-root Jacobians from the square coordinates;
-independent dense polynomial interpolation of moment integrals;
-rational bisection/interval enclosures for the algebraic height density;
-small-height and small-ratio finite diagnostics, strict boundaries and ties;
-the exact finite physical-radius-order counterexample retained from PR169.

Custody tests use real temporary Git repositories: full identity fields,
missing/unsafe paths, omitted/duplicated IDs, noncommit tree/blob objects,
symlink payloads, historical replacement forgery and packet drift. These are
simulated failures, not observed tampering of the user's sources.

All code is Python standard library. Runtime Python3.13.5; the target workflow
uses Python3.11.16 as in the existing repository. Exploratory symbolic algebra
was used privately to cross-check strip constants, not as a shipped dependency.
The final manuscript's rounded second-moment decimal was corrected against the
exact rational result before publication; no source file or earlier review changed.

No complete project checkout could be obtained locally (the public raw-host
request failed DNS). Hence local-only replay explicitly reports
source_pins_checked=false. Historical authentication of the five ACTUAL source
objects remains the hosted requirement. The two elder source bindings supply
SHA256 and Git blob; the other three also include declared byte size. No size
was invented for an unread full-byte copy. A matching content hash is not a
proof that the source's mathematics or external review is correct.

The new actual-source composition, infinite-dimensional domination and weak
transfer require source-bound nonauthor analytic review. Neither these finite
tests nor existing Lean workflow success formalizes this manuscript. Any
hosted success must be recorded against its actual head/run, not anticipated
in this author-time record. No self-merge or scientific register transition.
