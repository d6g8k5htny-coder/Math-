# Actual author-side execution, not an analytic review

Performer OpenAI / GPT-6 Astra Pro. New candidate code and proof; scientific
effect NONE. The controls use standard-library integer/Fraction arithmetic only.

The initial21 mathematical tests encountered21 explicit NotImplemented errors
on the unfinished interfaces. The first implementation passed20 and exposed a
wrong hand-entered test fixture at a singular transverse matrix: the independently
computed common coefficient is75/4, so the correct answer is-5625/16, not-4041/16.
Only the expected fixture was corrected, after checking the full Hessian. Three
further controls passed, giving24. The8 explicit-budget tests initially had6
missing-interface errors and2 passing elementary checks. They passed after the
budget functions were implemented. Two independent planar regression/cone checks
were then added; the mathematical suite has34 methods.

The6 real-Git/source-verifier tests initially produced9 assertion failures on
placeholder implementations. After implementation all6 passed. Final combined
suite:40 methods PASS in both ordinary and optimized Python, with identical
serialized controls output matching RESULTS.json. The exact continuous proof is
PROOF.md, not an inference from those40 methods.

Controls cover64 polynomial endpoint-Hessian comparisons including singular
matrices, fixed-k versus cusp coefficient falsifiers, the linear fifth derivative,
order8 covariances and scores, anisotropic conditional means, birth marginalization,
independent d1/d2 reference recovery, scaling, exact Gaussian moment cubature,
coarse Lipschitz arithmetic, lattice counts, exponential tail inequalities and
outward transport of the three supplied reference intervals. The6 Git fixtures
check literal identities, inventory drift, duplicate JSON, symlinks, historical
versus worktree reads, real replacement refs and unsafe path/object rejections.

The original #223 symbolic/interval pipeline and a Gaussian-field simulation were
NOT rerun. Its three reference c2 intervals are consumed as source data, not
newly certified here. Higher-dimensional field laws and the continuum constant
are not formally verified by this test suite. Tests in dimensions beyond3 check
algebra only; no explicit numerical bound in those dimensions is asserted.

Local network retrieval failed DNS. Local-only verification deliberately reports
historical_sources_checked=false. The added workflow must fetch the two pinned
commits, authenticate all five source path/blob/size/SHA256 bindings, and compare
the copied reference intervals with historical RESULTS.json. No hosted success
is anticipated in this author-time file. Any actual hosted result is a later
PR receipt bound to its actual tested commit, not a modification of this record.

The proof and budget require new nonauthor review, particularly every estimate
in Section6. An execution success does not establish their continuum validity or
promote the imported actual-persistence coefficient identification. No source
proof, numerical table, scientific flag, prize or existing formal scope changed.
