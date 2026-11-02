# C291 exact formalization scope

Status: implementation in progress. This document specifies the target and its
review obligations; it is not a build, kernel, alignment or delivery receipt.

The sole target is a definition
`I4LifetimeField.actualGaussianFieldInterface (d : ℕ) (L : ℝ) (hL : 0 < L)`
whose result is the unchanged
`UniversalLaw.Spec.Lifetime.GaussianFieldInterface d L`.
No additional theta, covariance, Gaussianity, convergence, smoothness or existence
premise is admitted. The source is the literal repaired Fourier coefficient law,
restricted to its explicit full-measure all-order summability carrier. The
constructor must retain `SmoothSample d L`, its existing measurable space,
`smoothLaw d L`, and `smoothSourceField d L` composed only with the canonical
Euclidean-coordinate equivalence.

## Source and theorem correspondence

The byte-pinned original `Lifetime.lean` has SHA-256
`90f4892608e953ecc696bb32ea159d1c178ceb8a1c6edfd11acfceb14af462c6`.
Its eleven fields are unchanged: carrier, sigma-algebra, measure, probability,
field, every-sample smoothness, every-sample periodicity, theta summability,
quadratic-form nonnegativity, exact finite linear-combination Gaussian law, and
the raw product integral covariance identity. The repaired `SourceSmoothCarrier`
has SHA-256
`5defdf223e85e7ccd23b5a903a1a306fe7f723727eb6aabf62eef523ef8639ed`.
The full old-source inventory and development-object lineage are retained in
`evidence/INITIAL_CACHE_COPY.json`; final verification must distinguish inherited
objects from an actual rebuild of the unchanged source closure.

The conventional source arguments are the frozen C290 `THETA_BRIDGE.md` and
`FIELD_CONSTRUCTOR.md`, SHA-256 respectively
`f41dc947c6850044b354dd848d624d0c8978a5a4dde2811240f2f5bcfb9aff4b`
and `f3fcf8162185888a7e442ebb8d12269472ced981460ff08104ee1c349389c19b`.
Their earlier nonauthor review is source context. It does not review new Lean
bytes or establish kernel acceptance of this implementation.

| New module | Exact obligation |
| --- | --- |
| `SourceThetaBridge` | Summability and positivity of the image-space theta series; full Fourier identity with scale `(sqrt (2*pi)/L)^d`; division by the full zero-lag normalizer; equality with the existing source spectral kernel. |
| `SourceLifetimeGeometry` | Canonical Euclidean coordinate transport; literal sample field; every-sample smoothness and periodicity; measurable evaluations and source-law Gaussian and moment transport. |
| `SourceLifetimeField` | Exact quadratic-form variance, nonnegativity, zero means, raw product integrals, all finite-combination Gaussian laws, and assembly of all eleven original fields. |
| Controls and audit | Literal projections, degenerate dimensions and coefficient families, meaningful mutations, complete declaration inventory including private/generated declarations, transitive axiom audit and separate kernel replay. |

All dimensions including `d = 0` and all finite evaluation families including
`m = 0` are retained. Repeated points and cancelling coefficients may have zero
variance. No strict positive-definiteness premise or division by variance is
permitted. Complex absolutely convergent products precede taking real parts;
the Fourier sum is not replaced by an unjustified product of cosines. The
normalizer includes the full lattice and zero mode. Centered covariance only
becomes the required raw product integral after both means are proved zero.

## Evidence and remaining scientific scope

Successful elaboration, a complete transitive axiom audit restricted to
`propext`, `Classical.choice`, `Quot.sound`, and separate standard named-module kernel replay are
separate observations. Exact-hash nonauthor source/result review is also
separate. OpenAI subagent review does not count as provider-distinct alignment
or a human review by Dylan Roy. Source changes stale prior review bindings.

This target constructs the specified Gaussian field interface. It does not
construct critical-point or persistence-bar measures, prove Morse genericity,
identify elder pairing with branch adjacency, turn contact integrals into
once-counted bars, prove an all-small-bars converse, or close a regional
shrinking multiple-witness collision bound. Global factorial estimates do not
discharge that regional node. Existing normalizers and parameter/limit orders
for those downstream tasks remain unchanged. The lifetime density exponent,
cumulative short-bar law and full universality conclusions are not established
by this constructor alone. No scientific register is promoted by this packet.

All work is delegated AI work for Dylan Roy. The actual implementation executors
are OpenAI Codex `/root/c290_theta_bridge` and
`/root/c291_field_feasibility`; `/root` coordinates, prepares controls and
verification, and handles custody. Publication, hosted checks, private custody,
and registration require their own exact receipts. A locally present numbered
directory does not establish delivery.

## 2026-10-18T00:16Z preserved final audit timeout and scoped recovery

The original final sequence has eighteen successful fresh builds followed by an actual audit timeout. The SourceLifetimeAxiomAudit child exited -15 at its420-second wall-clock cap, with425.671035042seconds including termination and post-execution checks. Both output logs are empty. All nineteen frozen source hashes and eighteen imported object hashes are unchanged; no audit object was produced. FINAL_SEQUENCE_RESULT.json remains HOLD_FAILED_PHASE with SHA256a8dddfaf3d46287a573b70fae91d71ba000b219ea4d4b0bed148341e0fe4825d. This does not identify a mathematical error and the successful development audit does not replace this missing final gate.

After nonauthor source review of the recovery scripts, the distinct recovery driver started at00:14:32Z. It reuses the eighteen successful builds, retries only the unresolved audit with900seconds and the same two-thread/4GiB limits, and will run the five previously unstarted standard named-module kernel checks only if that audit succeeds. The original failure is retained and the recovery START binds its exact receipt, original result, inventory and eighteen objects. No successful phase or mathematical source is rerun or changed. Final recovery success, dependency byte rehash, review, publication and custody remain pending.

The private-unused-axiom control is now terminal with its intended rejection. The independent actual mutation verifier passed265checks across all five negative-control executions. The separate negative audit stops at the forbidden axiom and is not a completed standard-only census.

The original claim0ab44ede-8d54-476b-afc3-d12f25f914a3 was renewed by eventf8661616-4a22-400a-a6ff-036a2c81eeef at23:53:58Z, actual Work Events2315, exact14cellreadback. Expiry is01:53:58Z. Math419 checkpoint6243400462 and timeout/recovery6243595738 were read back exactly. Next checkpoint00:35Z or earlier substantive result. No foreign ownership or scientific status changes.

## 2026-10-18T00:27Z successful final audit and kernel child-discovery recovery

The final audit retry completed exit0 without timeout in458.501998958seconds. Its full409declaration/18module/40private census stdout SHA256ce6920b72fbdfc6794051d690a10cf97792ffebe8b2c9145c2b10dcf2116ccea matches the reviewed development output; all nineteen fresh source builds now have successful receipts. No proof bytes changed.

The first standard kernel invocation exited1 in3.943259375seconds, with the exact error that it could not execute external process lean. All nineteen compiled objects and source hashes are unchanged. The parent wrapper used the absolute checker path but omitted the pinned child Lean executable from PATH. This is an executable-discovery failure, not a kernel rejection. The second sequence remains immutable HOLD_FAILED_RECOVERY_PHASE.

A source-reviewed kernel-only recovery START records00:25:40.329796Z, using the pinned binary directory and four standard OS paths, verifying actual child discovery and hashing the resolved binary. Its receipt records this deterministic PATH. It retries only the unresolved first kernel and executes the other four unstarted kernels, at420seconds/two threads; all nineteen successful compilations are reused. Final acceptance now requires twenty-four successful phases and both preserved failures, plus the terminal full dependency byte rehash. No kernel success, final review or delivery is inferred from this checkpoint. Public checkpoint6243709075 was read back exactly after one transport-error attempt was followed by a bounded read showing no matching new comment. Next checkpoint00:45Z or earlier substantive result; claim2315 expiry01:53:58 unchanged.

## 2026-10-18T00:42Z final local execution complete

All nineteen fresh local source builds and all five standard named-module kernel replays are terminal exit0 with unchanged frozen source/object bindings. FINAL_SEQUENCE_TERMINAL_RESULT.json records twenty-four successful phases; the two actual failed attempts remain separate and immutable. No successful phase was rerun. The final audit reports409declarations/18modules/40private, standardthreeaxioms only. Kernel times are159.30799075,166.17090033399998,162.78719725,166.48990975 and201.561246458seconds.

The complete terminal dependency byte rehash ran00:40:45.728106Z to00:41:16.298861Z and matched all83,897artifacts/8,418,477,755bytes with the exact full pathset and zero mismatches. This does not claim that the dependency sources were rebuilt. Final nonauthor result review is now requested; its full actual execution verifier has not yet been received. GitHub candidate, hosted checks, immutable private custody/master and registration remain pending. The current Mathmain source branch is3a67c1b1d05e03c6ef0f587f9b8abe30f5e37739, actual tree7abb35928ef92f82ec6fbe14348c4ee0ff79b3be, complete3052entries with no new C291 package path. All28currentlyopenPRheads match the earlier bounded inventory for still-open targets; recently delivered/closed foreign scopes are not reopened. WorkEvents2315:2332 contains our unexpired renewal and unrelated NUM/proxy claims only. Main419 remains the liveboard at1560comments with no later explicit successor.
