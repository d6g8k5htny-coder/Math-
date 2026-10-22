# Compact-Morse torus geometry at the literal C263 death

Author composition, 18 October 2026 UTC. OpenAI/Codex `/root/adapter_feasibility_c292`, delegated by the active C292 owner for Dylan Roy. Status: **CONVENTIONAL PROOF DRAFT, PENDING SEPARATE NONAUTHOR REVIEW**. This document extracts and proves the geometric adapter needed by the existing ordinary-H0 interval construction. It does not claim a novel general Morse theorem, a new stochastic admission theorem, or a Lean implementation. The accepted conventional source leaves are reused, not reopened or replaced. Same-provider organizational-independence credit is zero; scientific effect NONE.

The source authority and exact byte identities are in [SOURCE_IDENTITIES.json](SOURCE_IDENTITIES.json). The parent owns current claim, review, custody and publication; this author writes only this proof, the exact source copies under `inputs/`, and the identity file. The separate elder-module registration study and source #468 ownership are unchanged.

## 1. What is new in this handoff, and what is already conventional

The conventional finite-H0 source, §§3–4, already identifies the intrinsic older-point threshold with the finite Morse merger level and proves once-counting through finite component/basis induction. The dimension-independent structural source, §2, states the same deterministic Morse/elder result on compact connected boundaryless smooth manifolds, with explicit classical Morse imports. Its §4 supplies a sufficient vector-ridge elder-transfer argument. The asymmetric source, §§2–6, derives geometric boundary/path inputs for its explicit two-dimensional chart and constructs an actual one-interval split conventionally. The existing Lean `ElderBridge.lean` then proves that arbitrary topological boundary/ceiling/path data instantiate the actual singular-H0 split.

C292 does not reprove their stochastic results or claim to discover their elder theorem. Its bounded new composition is the explicit choice

```text
D = closure(path component of M in the strict superlevel at C263 death),
```

and a complete derivation of that D's frontier and height bounds and a closed death-level path, directly from the literal smooth-periodic compact-Morse hypotheses. This produces the exact geometric inputs consumed by `elderBoundaryDirectSummand` without importing an elder pairing, a bar count, a splitting conclusion or a path attaining the desired death as an assumption. The argument includes the critical-level path-connectivity step that compact connected limits alone do not supply.

The current formal gap is still real: no local-Morse chart, finite quotient critical-set theorem, critical-level local path-connectivity theorem, or the new adapter has been implemented or compiled here. This proof is a conventional source for that later work, not a claim that those APIs already exist.

Principal immutable source routes:

- [ST: dimension-independent structural source, §§2 and 4](https://github.com/d6g8k5htny-coder/main/blob/df590a438f1252309270ca625c6fe8531ddadc3b/experiments/universality/fold_structural_universality/PROOF.md), 43,927 bytes, SHA-256 `3d952a906553d578876456539a8f0dcd64aedd45099e8394cbe9db99866ec531`.
- [FH: finite-H0 source, §§3–4](https://github.com/d6g8k5htny-coder/main/blob/85b928b326ff0586715a56ae91f51d3fbd89557a/experiments/universality/finite_h0_lifetime/PROOF.md), 27,064 bytes, SHA-256 `5ea91111fa5f3d78d7c4188ebe84b3bc2c452b05dfdfc62c74b03123cb2696d1`.
- [AE: asymmetric source, §§2–6](https://github.com/d6g8k5htny-coder/Math-/blob/c8ec07034608741585111603f1b506393c340908/frontiers/gaussian_short_bar_theory_20261017/asymmetric_elder/PROOF.md), 28,291 bytes, SHA-256 `6d07631c068019bf9f081ad0b6f50325679e3ab554f221265e002d5c047f17ac`; [actual integrated review](https://github.com/d6g8k5htny-coder/Math-/blob/c8ec07034608741585111603f1b506393c340908/frontiers/gaussian_short_bar_theory_20261017/asymmetric_elder/REVIEW.md), 25,687 bytes, SHA-256 `16678abc7de50986b0fc6d54303449bf1b4c5ba8b10f6a3ccc7f9d03a97a4e9f`.
- [Actual geometric formal consumer](https://github.com/d6g8k5htny-coder/Math-/blob/c8ec07034608741585111603f1b506393c340908/frontiers/asymmetric_elder_bridge_20261017/ElderBridge.lean), 3,683 bytes, SHA-256 `6b0be1116f6b357b0ffbda202c572c27c2788b98bee639e228375a5ebeea1fa9`.

Source wording matters. ST fixes a compact connected smooth Riemannian manifold without boundary of dimension d>=1, smooth real samples, ordinary superlevel H0 over any fixed coefficient field, increasing parameter minus the height, and the exclusion of the essential class. Its Morse facts are classical imports; a source-level proof is not a Lean theorem. AE's quantitative square/ridge hypotheses are specifically two-dimensional and include its embedded chart, half-chart endpoint and strict gap bounds. We do not extend that quantitative chart to higher dimensions. The present proof instead uses the genuine dimension-independent local Morse form. No Gaussian assumption or limit is needed for its deterministic result.

## 2. Exact inputs, literal transport and external imports

Fix an integer n>=1, a real L>0, and

```text
g : EuclideanSpace R (Fin n) -> R,
hsmooth   : UniversalLaw.Spec.Lifetime.IsSmooth n g,
hperiodic : UniversalLaw.Spec.Lifetime.IsLPeriodic n L g,
hMorse    : UniversalLaw.Spec.Lifetime.IsMorseDistinct n L g,
M         : EuclideanSpace R (Fin n),
hmaximum  : UniversalLaw.Spec.Lifetime.IsNondegMax n g M,
hfinite   : not TorusFiltration.superlevelBar_isEssential g M.
```

There is no finite-Fourier cutoff, coefficient law, chosen saddle, assumed elder event or interval among these inputs. The lower dimension bound is retained from the compact-manifold conventional sources. C291's allowance of n=0 does not widen this theorem.

The unchanged C291 target `Lifetime.lean` and the frozen `Specifications/Field.lean` use the same literal formulas for the following objects, with their own namespaces:

| Object | Literal formula to transport |
|---|---|
| `E n` | `EuclideanSpace R (Fin n)` |
| `latticeVec n L z` | sum over i of `EuclideanSpace.single i (L * (z i : R))` |
| `IsSmooth n g` | for every finite natural j, `ContDiff R j g` |
| `IsLPeriodic n L g` | `g(x+latticeVec n L z)=g x` for every x,z |
| `hessian n g x v w` | `iteratedFDeriv R 2 g x ![v,w]` |
| `IsCriticalPoint` | `fderiv R g x=0` |
| `HessianHasInertia` | complementary subspaces of the specified dimensions, negative and positive definiteness on the respective subspaces |
| `IsNondegMax` | criticality and inertia n |
| `IsMorseDistinct` | every critical point has some such inertia, together with the stated distinct-positive-torus-distance critical-height clause |

Thus the Field-to-Lifetime transport used here is pointwise unfolding of these exact formulas, with no modification of the height, period, norm, derivatives or probability measure. This is a conventional identity check, not an executed Lean `rfl`/elaboration receipt. The local `Lifetime.lean` copy has SHA-256 `90f4892608e953ecc696bb32ea159d1c178ceb8a1c6edfd11acfceb14af462c6`; the Field file has SHA-256 `f22c91e082cd7e738ba47c9c3534e47ac687d066f0b78586d15103cf1132535e`.

Let E be this Euclidean space, X=E/(L Z^n), pi:E->X the literal `torus_proj`, and F:X->R the literal `torus_descend`. Periodicity is transported to `torus_isPeriodic` by the identical lattice-vector formula. Therefore

```text
F(pi x)=g(x),       Mbar=pi M,       m=g(M)=F(Mbar).
```

The existing `TorusTopology.lean` constructs the compact quotient, its continuous surjective projection and covering map, descent, and strict/closed higher-endpoint path equivalences. We additionally use the standard smooth quotient atlas of a Euclidean space by a discrete translation lattice: sufficiently small projected Euclidean balls are charts, with transition maps translations. In these charts F is literally a translate of g. In particular coordinate criticality and Hessians are exactly those of g; there is no Hessian rescaling. This smooth-atlas construction is an explicit conventional import, not a statement that the topology companion already formalizes it.

For clarity the proof's remaining classical inputs are:

1. **Finite-dimensional smooth calculus and inverse function theorem.** The Hessian of a smooth real function is symmetric and is the derivative of its coordinate gradient. A nonsingular Hessian makes a critical point isolated by the inverse function theorem. Negative definite Hessian gives a strict local maximum, for example by Taylor's formula.
2. **The local Morse lemma.** At a critical point with nonsingular Hessian, a smooth local coordinate change makes F-F(q) equal to a sum of positive coordinate squares minus a sum of negative coordinate squares. This is the actual local theorem for a smooth function, not a supplied finite-event or elder certificate.
3. **Elementary compact topology.** Continuous functions attain extrema on nonempty compact sets; connected components are closed; nested nonempty compact connected sets in a compact Hausdorff space have connected nonempty intersection; an infinite subset of a compact metric space has an accumulation point. Open subsets of manifolds are locally path connected, and in a locally path-connected space connected components are path connected and open.

These are the explicit geometric/topological imports. The first two are the classical local-Morse/finite-dimensional inputs already admitted in scope by FH/ST. No new primary-book audit is claimed. No critical-free flow or handle-attachment theorem is needed by the argument below; their earlier use in FH/ST is not turned into a premise here. We do not assume a barcode theorem, an elder basis, critical-level attainment, an H0 comparison field or a component-counting certificate.

Only the nondegeneracy conjunct of `IsMorseDistinct` is needed for this one-summand geometric theorem. The full source hypothesis is retained. In particular no unproved equivalence between the literal `torusDist` formula and quotient inequality is needed in this proof, and no uniqueness of a saddle is concluded from that unused second conjunct.

## 3. The theorem and exact acceptance boundary

Define the *literal existing* C263 set and number

```text
Clear(M) = {a : there is y with g(y)>m and a path M->y
                       all of whose heights are strictly greater than a},
delta = superlevelBar_deathHeight g M.
```

C263 uses a real supremum of the nonempty clearance set and a default zero if that set is empty. Its proved nonemptiness theorem applies here, so the empty default will not occur.

Set

```text
U = {x in X : F(x)>delta},
C = {q in X : JoinedIn U Mbar q},
D = closure_X C.
```

**Theorem (compact-Morse boundary data at literal death).** Under exactly the inputs of §2,

```text
delta < m,
D is closed,       Mbar is in D,
F(q) <= m          for all q in D,
F(q) <= delta      for all q in frontier_X D,
there exist Q in X and a continuous path gamma:Mbar->Q such that
  F(Q)>m and F(gamma(t))>=delta for all t in [0,1].
```

The endpoint Q can be chosen to be a nondegenerate local maximum. The path attains height delta somewhere. Consequently these data instantiate `elderTrap_of_boundary` and, over any fixed coefficient field k, the existing `elderBoundaryDirectSummand` gives one actual ordinary singular-H0 interval direct summand on [-m,-delta).

The conclusion provides one split for this supplied maximum. It does not construct a simultaneous split for all maxima, identify a uniquely labeled quotient saddle, or prove an exhaustive once-counted barcode. No existence of D, Q or gamma, no relation delta=F(S), and no target H0 equality is an input.

## 4. Genuine Morse geometry follows from the literal hypotheses

Because g is smooth, its Hessian bilinear form B is symmetric. At a critical point the inertia predicate supplies complementary negative and positive subspaces V,W with E=V+W. This does imply nondegeneracy, even though no cross-term orthogonality was included in the predicate. If z=v+w lies in the radical of B, then

```text
B(v,v)=-B(w,v)=-B(v,w)=B(w,w).
```

Strict negative and strict positive definiteness force v=w=0. Thus z=0. This verifies the nonsingularity needed by the classical Morse lemma; it is not assumed through a different Morse interface. At M the negative subspace has dimension n and hence equals E, so the Hessian is negative definite.

The quotient charts described in §2 transport these facts to F. Its critical set is closed because the derivative is continuous in local charts. Every critical point is isolated by the inverse function theorem applied to the coordinate gradient. A closed discrete critical set in compact metric X is finite: otherwise an accumulating subsequence would limit to another critical point, contrary to that point's isolation. Denote this finite set by Crit(F).

For every real a, the closed superlevel A_a={F>=a} is compact and locally path connected. Here is the critical-level detail. At a point with F>a a small neighborhood lies inside A_a. At a point with F=a and nonzero derivative, the submersion coordinate form identifies a local piece with a closed half-space. At a critical point with F=a, the Morse lemma identifies it near the origin with

```text
{(u,v) : ||u||^2-||v||^2 >= 0}.
```

Its intersection with any centered sufficiently small ball is star shaped about the origin, hence path connected. This supplies arbitrarily small relatively open path-connected neighborhoods at the cone vertex. Away from the vertex its boundary is regular, so the preceding half-space argument applies. At a local maximum the cone may be the single point, which is also path connected. Thus all cases give local path connectivity of A_a. It follows that every connected component of A_a is path connected.

This uses the actual Morse quadratic cone, not the invalid general assertion that compact connected sets are path connected.

## 5. Strict death drop below the nondegenerate maximum

By continuity and hfinite, C263 proves Clear(M) nonempty, bounded above, and

```text
a < delta  if and only if  a is in Clear(M).             (1)
```

Use the negative definite Hessian at the Euclidean representative M. Taylor's formula provides a radius rho>0 such that g(x)<m for every 0<||x-M||<=rho. The sphere ||x-M||=rho is nonempty and compact because n>=1. Let c0 be the maximum of g on that sphere. Then c0<m. The entire closed ball has height at most m.

Any y with g(y)>m lies outside that ball. Every continuous path from M to y meets its sphere by the intermediate value theorem applied to ||gamma(t)-M||. Hence no such path stays strictly above c0. More generally every clearance member a satisfies a<c0: at a sphere crossing it must be below a value at most c0. Thus c0 is an upper bound for Clear(M), and its nonempty real supremum obeys

```text
delta <= c0 < m.                                        (2)
```

This argument takes place in the literal Euclidean space used by C263 and requires no injectivity of an arbitrarily chosen torus representative. Periodicity does not affect the first crossing of the fixed ball. In particular Mbar belongs to every strict superlevel below or equal to delta.

By the exact `torus_strict_higher_path_iff`, (1) is also the quotient statement

```text
a<delta iff Mbar can be joined in {F>a} to some point y with F(y)>m.
                                                               (3)
```

At a=delta this strict quotient connection is impossible.

## 6. Fixing an older maximum across levels approaching death

For any a<delta, let U_a be the path component of Mbar in O_a={F>a}. By (2), Mbar belongs to O_a; by (3), U_a contains some y with F(y)>m. Since O_a is an open subset of the manifold X, it is locally path connected. Its path components are therefore both open and closed relative to O_a. In particular U_a is open in X and

```text
closure_X(U_a) intersect O_a = U_a.                       (4)
```

The nonempty compact closure of U_a has a maximizer Q_a of F. Its height is at least F(y)>m>a. Equation (4) places Q_a back in U_a. Since U_a is open in X, Q_a is a local maximum of F on X, not just a constrained maximum of a closed set. It is critical, and the Morse condition makes its Hessian negative definite. Thus it is one of the finitely many members of

```text
Older = {Q in Crit(F) : Q is a local maximum and F(Q)>m}.   (5)
```

Moreover Mbar and Q_a have an actual path inside O_a, by the defining property of U_a. We have proved nonemptiness of Older and this path statement, rather than assuming that a higher endpoint was already a higher critical maximum.

Choose a_j=delta-1/(j+1), j=0,1,... . For each j choose Q_j as above. Since Older is finite, some fixed Q in Older occurs for infinitely many j. Enumerate those indices as a strictly increasing sequence j_l. It is unbounded, so a_(j_l) increases to delta. Write b_l=a_(j_l). For every l there is a path from Mbar to this one Q in {F>b_l}.

The endpoint Q is not prescribed in advance and need not be the global maximum. This finite-subsequence step is what prevents a sequence of merely higher endpoints from approaching height m and losing the strict inequality needed by the interval constructor.

## 7. Closed death-level attainment

Let K_l be the connected component of Mbar in the compact closed superlevel A_(b_l)={F>=b_l}. Each K_l is closed in A_(b_l), hence compact in X, and is connected. The path just constructed places Q in K_l.

Since b_(l+1)>=b_l, K_(l+1) is a connected subset of A_(b_l) containing Mbar. By maximality of the connected component, K_(l+1) is contained in K_l. The nested compact connected intersection

```text
K = intersection over l of K_l
```

is nonempty and connected; it contains both Mbar and Q. Every x in K satisfies F(x)>=b_l for all l, hence F(x)>=delta. Thus K is a connected subset of A_delta containing both endpoints. They belong to the same connected component of A_delta.

Section 4 proves that A_delta is locally path connected even if delta is a critical value. Its connected components are therefore path connected. There exists an actual continuous path gamma:Mbar->Q with F(gamma(t))>=delta for all t. Since Q belongs to Older, F(Q)>m.

This is the required attained closed path. The proof did not take a limit in a space of paths and did not infer path connectivity directly from connectedness of K.

For completeness, its minimum is exactly delta. The compact parameter interval and continuity give an attained minimum. If the minimum were strictly greater than delta, the same quotient path would be a strict higher-endpoint path at delta, contradicting (3). Thus some parameter has F(gamma(t))=delta. Closed attainment is consistent with the exclusion of strict clearance at delta.

## 8. Constructing the exact closed domain and frontier bound

Recall U={F>delta}, C the path component of Mbar in U, and D=closure_X C. By (2), Mbar is in C. Local path connectivity of U makes C open in X and closed relative to U. Therefore

```text
D intersect U = C,        C subset interior_X D.          (6)
```

For q in C, if F(q)>m then its defining path from Mbar inside U would be a strict higher-endpoint path at delta, contradicting (3). Hence F<=m throughout C. The set {F<=m} is closed, so

```text
F<=m throughout D.                                      (7)
```

The domain D is closed by construction and contains Mbar. If q is in frontier_X D and F(q)>delta, then q lies in D intersect U=C by (6), and consequently in the interior of D. This contradicts q being on the frontier of the closed set D. Thus

```text
F(q)<=delta for every q in frontier_X D.                 (8)
```

The older maximum Q lies outside D by (7) and F(Q)>m. Equations (2), (7), (8), F(Mbar)=m, Mbar in D and the actual path of §7 are exactly the geometric hypotheses of `elderTrap_of_boundary`. No desired separation, elder relation, death equality or H0 equation was supplied among the theorem's inputs.

Unlike the special asymmetric chart, this D can contain multiple younger branches. Its active intersection need not be a single path component. That does not invalidate the boundary constructor: its hypotheses require clopen separation and a height ceiling, not a unique interior component.

## 9. Consumption by the existing ordinary-H0 constructor

Fix any field k. Its Field structure is nonzero; characteristic two is allowed. Apply the unchanged `elderTrap_of_boundary` with

```text
X, F, D, m, delta, Mbar, Q,
IsClosed D, frontier bound (8), delta<m, F(Mbar)=m,
Mbar in D, ceiling (7), m<F(Q), gamma, closed path inequality.
```

This constructs T : ElderTrap F Mbar Q m delta D. The unchanged `elderBoundaryDirectSummand` (equivalently `elderDirectSummand T`) gives

```text
superlevel_h0Filtration F (ModuleCat.of k k)
  is naturally isomorphic to
elderInterval k m delta direct_sum kernel(elderRetraction T).       (9)
```

The existing code constructs the interval fibers and maps, the point-class difference section, the D-indicator retraction through the actual `ordinaryH0_filtrationIso`, all naturality squares, and their direct-sum isomorphism. It does not assume those conclusions. The interval is active exactly for -m<=t<-delta. The death endpoint is excluded even though the spatial filtration uses closed superlevels.

The section is [Mbar]-[Q]. Individual ordinary H0 point classes do not die; the difference vanishes at the closed merger level. In characteristic two it is the corresponding sum. The prebirth naturality square follows from the actual ceiling F<=m on D; no prebirth point can enter its indicated region. The death square follows from the actual closed gamma.

Equation (9) is a conventional application of an existing source theorem. No new Lean expression was elaborated, no target registered, and no compiler or kernel was run in C292. The existing formal sources retain their exact historical execution, review and alignment scopes.

## 10. Literal-source applicability and retained boundaries

For C291 one may set g=I4LifetimeField.actualField n L omega. Its `actualField_smooth` and `actualField_periodic` supply the first two predicates under L>0. The carrier remains `SmoothSample n L`, the measure remains `smoothLaw n L`, and the spatial field remains the literal `smoothSourceField` through the canonical Euclidean coordinate equivalence. Nothing in this proof changes the covariance, normalization, Gaussian law or field.

However C291's `actualGaussianFieldInterface` has no Morse-genericity field. The predicate hMorse on this omega remains an explicit additional deterministic hypothesis. This proof establishes neither its probability-one validity under the literal law nor a measurable choice of D, Q, gamma or the splitting. There is no stochastic conclusion without that further work.

The dimension-independent result here derives from compact Morse geometry. It does not transplant AE's quantitative two-dimensional chart, the finite full-square Gaussian source, or its factorial estimates to arbitrary n. The local sphere proof and Morse cone argument also cover n=1; there are no transverse variables to invent in that case. n=0 remains outside the stated scope.

No limit is taken in (9). The auxiliary sequence of levels b_l approaches the fixed deterministic death of one fixed function; it is not a random-field approximation, a small-lifetime limit, a thermodynamic limit, or a cutoff limit. The existing fixed-law small-lifetime theorems, fixed-target conditional couplings, and varying-L/cutoff process families keep their respective parameter orders and full normalizers.

We conclude exactly one actual interval summand for each supplied nonessential maximum on the source Morse locus. We do not conclude a coherent simultaneous decomposition, an endpoint-preserving bijection, exhaustive once-counted bars, a unique quotient saddle partner, or identification with a pre-assumed Field/Lifetime elder relation. Such further work must preserve quotient points versus multiple periodic lifts and elder death versus branch adjacency. The domain and endpoint constructed here can depend on M; no measurable global family of choices is asserted.

The result does not prove that all small bars are local regular folds, an all-small-bars converse, singular-mark or remote complements, field-first stochastic transfer, regional shrinking-window multiple-witness collision estimates, a quantitative remainder, or universality. Global factorial bounds do not supply regional collision estimates. Source #468, the elder-registration study, the numerical owners and their explicit stops retain their scopes. No scientific or institutional alignment status changes.

## 11. Evidence scope

Exact source bodies already fetched and verified during read-only reconnaissance were copied without network rereads to `inputs/`. The identity file binds repository, immutable cut, source path, Git blob, byte length and SHA-256. C291 inputs were copied from the unchanged publication package after matching their previously verified hashes. The source map's historical PENDING/HOLD labels remain unedited history.

This document is an author proof composition awaiting substantive nonauthor review. No simulated numerical test can certify its Morse/topological steps, and none is presented as such. The isolated ball, fixed-older-maximum subsequence and critical-level cone arguments are the mathematical controls against the precise failure modes identified in §§5–7. Source review is not human or provider-distinct acceptance, compilation, kernel checking, scientific promotion, or a transfer of another owner's scope.
