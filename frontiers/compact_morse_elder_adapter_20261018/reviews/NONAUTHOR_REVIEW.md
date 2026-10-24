# C292 nonauthor mathematical review

Decision: **ACCEPT_SCOPED_CONVENTIONAL**.

Reviewer: OpenAI/Codex `/root/c292_geometry_review`, a fresh nonauthor reviewer delegated for Dylan Roy by the C292 owner. Review date: 18 October 2026 UTC. Provider and organization are the same as the author and parent; organizational-independence credit is **0**. This is an AI mathematical/source review, not human review, provider-distinct review, Lean elaboration, kernel verification, or scientific acceptance.

There are no must-fix mathematical or interface findings against the frozen artifact identified below. The accepted conclusion is exactly the deterministic construction of the closed trap and a higher-endpoint closed path at the literal C263 death, followed by conventional consumption of the existing single ordinary-H0 interval constructor. The exclusions in the proof remain operative.

## Exact artifact and exposure

The complete `PROOF.md` was read after the parent declared it ready for review. Its 268 lines contain **25,662 bytes** and have SHA-256:

```text
39f92734da35aa4c3ad97ea9d8e194cea4ee3a0b23054a8a412f331294d74762
```

The accompanying `SOURCE_IDENTITIES.json` has **13,452 bytes** and SHA-256:

```text
8b0fc8892a1936ad6a37c49b45e5fcf987154068fb7107e07b0b48d55c9f5d44
```

Both identities were computed from the actual local bytes. The relevant copied source bodies also matched their manifest byte lengths and SHA-256 values. The C292 `inputs/C291/inputs/Lifetime.lean` copy was additionally compared byte for byte with `continuation291/publication-package/inputs/Lifetime.lean`; they are equal, with 51,383 bytes and SHA-256 `90f4892608e953ecc696bb32ea159d1c178ceb8a1c6edfd11acfceb14af462c6`.

The task instruction disclosed the intended adapter and exact sources before review. Before opening the new proof, I independently reconstructed the necessary compact-Morse argument from those source interfaces and sent the parent interim checkpoints about the fixed older endpoint and critical-level path-connectivity obligations. I did not edit the author's proof, supply replacement author text, or communicate proposed repairs to its author. I then read the complete frozen proof and compared each substantive step with that reconstruction. This is fresh nonauthor review of the artifact, with task/design exposure and same-provider limitations explicitly disclosed; it is not an independence claim based merely on a different agent name.

Read scope:

- Complete `SuperlevelBar.lean`, `TorusTopology.lean`, `OrdinaryH0.lean`, `ElderClearance.lean`, `ElderBridge.lean`, and `ElderInterval.lean` at the supplied Math- cut `c8ec07034608741585111603f1b506393c340908` through the frozen local copies.
- Complete C291 `SourceLifetimeGeometry.lean` and `SourceLifetimeField.lean`; relevant literal smoothness, periodicity, derivative, inertia, nondegenerate-maximum, Morse-distinct, and persistence-interface predicates in the frozen Lifetime and Field files.
- Contextual finite-H0 §§3–4, structural-source manifold convention and §2 Morse/elder discussion, and asymmetric-source §6 ordinary-H0 splitting discussion. I did not reopen the full stochastic proofs, integrated historical reviews, or all claims in those source families.

The repository cuts and Git blob associations are those recorded by the parent source manifest. I independently verified the local byte identities, not a fresh remote raw-file fetch or Git commit ancestry. Hashes identify what was reviewed; they do not establish the mathematics. No numerical experiment, test suite, Lean command, compiler, kernel audit, source edit, or remote post was performed in this review.

## Reconstructed theorem and premise audit

The theorem fixes `n >= 1`, `L > 0`, a literal smooth periodic Euclidean function `g`, the literal `IsMorseDistinct` hypothesis, a literal nondegenerate maximum `M`, and nonessentiality in the actual C263 sense. On the genuine period quotient `X`, with descended `F`, birth `m = g(M)`, and the existing number `delta = superlevelBar_deathHeight g M`, it defines `C` as the path component of the projected maximum in `{F > delta}` and `D = closure C`.

It derives `delta < m`, closedness and maximum membership of `D`, `F <= m` on `D`, `F <= delta` on its frontier, and an actual path in `{F >= delta}` to one point `Q` with `F(Q) > m`. It additionally derives that `Q` can be a nondegenerate local maximum and that the path attains `delta`.

I checked that no desired closed path, trap, death equality, elder pairing, saddle label, finite-bar count, H0 equation, or interval split occurs among the new theorem's inputs. The nondegeneracy conjunct of `IsMorseDistinct` is genuinely used. The distinct-critical-height conjunct is retained but is not used to smuggle in a unique merger or a quotient-distance identity. The proof says this explicitly.

The declared classical imports are adequate and remain explicit: smooth quotient charts for the discrete translation lattice; finite-dimensional smooth calculus and the inverse function theorem; the local Morse lemma; elementary compact and locally path-connected topology. The proof does not pretend these imports have been formalized in the current companion files. No handle-attachment theorem, critical-free flow, global elder basis, or all-bars theorem is needed to close its stated argument.

## Substantive step checks

### 1. Literal inertia really supplies a Morse Hessian

The source predicate gives complementary negative and positive subspaces, not an orthogonal eigenspace decomposition. The proof correctly addresses this distinction. For a symmetric Hessian `B`, a radical vector `z = v + w` satisfies

```text
B(v,v) = -B(w,v) = -B(v,w) = B(w,w).
```

The left expression is nonpositive and is zero only if `v = 0`; the right expression is nonnegative and is zero only if `w = 0`. Thus both vanish and the radical is zero. Finite dimension makes the associated Hessian map invertible. Smoothness supplies the symmetry that this argument requires. At the specified maximum the negative subspace has full dimension and is the whole tangent space, giving negative definiteness. This step does not assume a stronger Morse predicate in place of the literal one.

Translation quotient charts preserve the function and its coordinate derivatives without a scale change. The critical set of the descended function is closed, and the inverse function theorem makes each of its points isolated. Compact metrizability then forces finiteness. The proof includes closedness; an arbitrary discrete nonclosed subset of a compact space would not suffice.

### 2. Closed superlevels are locally path connected, including critical levels

For `F > a`, a small open manifold neighborhood lies in `{F >= a}`. At a regular point of `F = a`, the submersion form gives a half-space. At a nondegenerate critical point of `F = a`, the local Morse form gives the homogeneous quadratic cone `||u||^2 - ||v||^2 >= 0`.

Intersections of this cone with centered open coordinate balls are relatively open neighborhoods of the vertex and are star shaped about it: multiplication by any scalar in `[0,1]` preserves the quadratic inequality and the ball. Their radii can be made arbitrarily small. At nonvertex boundary points the gradient of the quadratic form is nonzero, giving the regular case. Positive- and negative-definite cases give an open neighborhood or a singleton as appropriate. Thus local path connectivity is proved at all relevant points, for `n = 1` as well as higher dimensions.

Consequently each connected component of a closed superlevel is path connected. The proof does not make the false assertion that arbitrary compact connected sets are path connected.

### 3. The literal death lies strictly below birth

C263 continuity and nonessentiality give a nonempty bounded clearance set and its exact strict cut. A small Euclidean ball at `M` has all heights at most `m`, with all punctured-ball heights strictly below `m`. Its nonempty compact boundary sphere has a maximum `c0 < m` because `n >= 1`.

Every endpoint of height greater than `m` lies outside that ball. Every continuous path from `M` to such an endpoint crosses its boundary, so any strict clearance is strictly below `c0`. The real supremum therefore obeys `delta <= c0 < m`. This is a uniform barrier argument, not the invalid inference that a supremum is strictly below `m` merely because each member is.

This step is conducted in the actual Euclidean space of C263. It requires no arbitrary choice of a torus lift endpoint and is unaffected by winding paths. The exact existing projection/lifting equivalence then transfers the strict cut to the quotient.

### 4. A fixed genuinely older endpoint survives the limiting levels

For every `a < delta`, the open-superlevel path component `U_a` of the maximum contains a point of height greater than `m`. Local path connectivity makes `U_a` open and relatively closed in `{F > a}`, so `closure(U_a) intersect {F > a} = U_a`.

The maximum of `F` on this compact closure has height greater than `m > a`, hence belongs to the open set `U_a`. It is therefore a local maximum of `F` itself, not merely a constrained maximum. Its derivative vanishes; its Hessian is nonpositive by the second-derivative test and nonsingular by the proved Morse property, hence negative definite. It belongs to the finite set of older local maxima.

A finite pigeonhole argument on the levels `delta - 1/(j+1)` yields one fixed older maximum `Q` along an infinite, hence cofinal, increasing subsequence. This resolves the endpoint problem: the strict inequality `F(Q) > m` is never replaced by a limiting inequality `F(Q) >= m`. Neither the global maximum nor a preselected older point is incorrectly required to be the endpoint at this death.

### 5. Nested compact components give the needed closed path

At each subsequence level, the connected component `K_l` of the maximum in the closed superlevel is compact and connected and contains the same `Q`. Raising the level gives a connected subset of the previous superlevel containing the same maximum, so component maximality proves nesting. Their compact connected intersection contains both endpoints and lies in `{F >= delta}`.

The proof uses this intersection only to put the endpoints in the same connected component of `{F >= delta}`. Section 4's local path connectivity of that ambient closed superlevel then gives a path in its component. It does not assert that the intersection itself is path connected and does not take a convergent subsequence in an unjustifiably compact path space.

The path's attained minimum is at least `delta`. If it were greater than `delta`, it would be a strict higher-endpoint path at `delta`, contradicting the exact C263 cut after quotient transport. Thus the minimum equals `delta`; strict exclusion and closed attainment are used consistently.

### 6. The constructed closure has exactly the required trap bounds

The strict-death component `C` is open in the quotient and relatively closed in `{F > delta}`. Thus `D intersect {F > delta} = C` and `C` lies in the interior of `D`. A point of `C` higher than `m` would itself give a forbidden strict higher-endpoint path at `delta`, so `F <= m` on `C` and, by continuity, on its closure `D`.

For a frontier point of the closed set `D`, height greater than `delta` would put it in `C` and then in the interior of `D`, a contradiction. This proves the frontier bound. The older endpoint is outside `D` because of the height ceiling. Nothing requires `D` to be a ball, smooth domain, or bounded Euclidean lift. Its active trace may have several components; the consumer only requires a clopen trace and a height ceiling.

### 7. The ordinary-H0 consumer matches without hidden premises

I compared the argument directly with `elderTrap_of_boundary` and `elderBoundaryDirectSummand` in the frozen `ElderBridge.lean`. The geometric data supply every argument: closed `D`, frontier height bound, strict death drop, maximum height and membership, height ceiling, a strictly higher point, and an actual closed-level path. The constructor is generic in a topological space, so applying it to the quotient is legitimate. No conversion of a quotient path to an arbitrarily prescribed Euclidean endpoint is made.

`ElderInterval.lean` defines the actual interval on `-m <= t < -delta`. Its section is the difference of the two point classes and its retraction is the indicator of membership in the fixed `D`, descended to path components and transported by `ordinaryH0_filtrationIso`. Active clopen separation makes that indicator well-defined. The height ceiling gives the prebirth naturality square; the closed path gives the active-to-dead section square. These are actual requirements, and both are supplied.

The composite retraction after section equals the identity because the maximum is inside `D` and the older point is outside. The resulting kernel complement gives the displayed natural direct-sum isomorphism. Ordinary point classes remain nonzero under augmentation; it is their difference that vanishes. Characteristic two causes no defect. This is one interval summand, without a claim of a simultaneous or exhaustive decomposition.

## Counterexample and boundary checks

1. **Dropping Hessian symmetry:** the complementary-sign predicate alone is insufficient for a nonsymmetric bilinear form. For example the matrix `[[1,1],[-1,-1]]` has a positive first coordinate line and negative second coordinate line but is singular. The proof explicitly obtains symmetry from smooth scalar calculus before its radical argument.
2. **Replacing Morse geometry by compact connectedness:** a compact connected space such as the closed topologist's sine curve need not be path connected. The proof supplies the quadratic-cone local argument and uses it on the ambient closed superlevel, avoiding this failure.
3. **Allowing moving higher endpoints to converge without a fixed gap:** strict inequalities `F(y_j) > m` can be lost under limits. The finite older-maxima and cofinal-subsequence step fixes one endpoint before taking compact intersections.
4. **Bounding each clearance only by birth:** values all less than `m` can have supremum `m`. The compact sphere supplies the genuinely smaller common bound `c0`.
5. **Using the total essential default as a death:** the C263 constant function of height `-1` has default death `0`, so an unconditional death/start bound is false. The present nonessentiality assumption invokes the nonempty supremum branch and excludes this case.
6. **Confusing strict and closed levels:** the proof excludes a strict higher path at `delta` while deriving one with heights at least `delta`. Its interval includes birth and excludes death, in agreement with the actual formal convention.
7. **Demanding arbitrary lifts:** the topology source's constant-path control refutes an arbitrary preselected lift endpoint. The proof uses the higher-endpoint equivalence with its existential endpoint and states its actual closed path on the quotient.
8. **Treating the dying class as an ordinary point class:** ordinary augmentation sends each point class to `1`. The proof and consumer use the point-class difference, so no reduced-H0 substitution is hidden.
9. **Promoting one split to all bars or saddle labels:** the constructed regions and endpoints can depend on the maximum. No compatibility, once-counting, unique merger saddle, or full elder relation has been derived here. The proof excludes each of those promotions.
10. **Promoting deterministic source applicability to an almost-sure result:** C291 supplies smoothness and periodicity of its literal sample, but the reviewed theorem still assumes the sample's Morse predicate. No measurable family of choices or probability-one Morse statement is produced.

These are mathematical controls and interface checks, not executed experiments or counts of passing tests.

## Findings and permitted use

No mathematical amendment is required for the frozen proof. The explicit imports, their scope, and the exclusion of newly formalized or stochastic conclusions are sufficient for conventional acceptance of this adapter. The proof's historical author label remains “pending separate nonauthor review”; this separate report records the review decision without altering or pretending to rehash a different author artifact.

The accepted composition may be used as a conventional mathematical source for the future formal adapter from literal smooth-periodic Morse inputs to the existing geometric interval constructor. It does not certify the new adapter in Lean, re-run historical source builds, audit all imported kernels/axioms, establish almost-sure Morse genericity of the literal Gaussian source, derive all-bars once-counting or saddle pairing, resolve collision or remote-complement estimates, confer provider-distinct/human approval, or change scientific status. Scientific effect: **NONE**.
