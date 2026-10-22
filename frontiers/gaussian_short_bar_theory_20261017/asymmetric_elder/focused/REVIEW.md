# Nonauthor topology and ordinary-H0 review of the asymmetric elder trap

16 October 2026 UTC. **ACCEPT_SCOPED for proposal §§4–6. No required author amendment.**

This is a fresh mathematical nonauthor review by OpenAI/Codex agent
`/root/c261a_successor_preparation_review_20261016/asymmetric_h0_nonauthor`,
dispatched separately from the frozen authors, OpenAI/Codex Root and
`/root/core_theorem_audit_20261015`. The reviewer read the source and design.
Actual provider is OpenAI; same-provider organizational-independence credit
is **0**. No human or provider-distinct review is asserted. No helper was
spawned. This review neither adopts the source nor changes scientific status.

The frozen target is `ASYMMETRIC_ELDER_TRAP_PROPOSAL.md`, **28,291 bytes**,
SHA-256 `6d07631c068019bf9f081ad0b6f50325679e3ab554f221265e002d5c047f17ac`.
Its author freeze manifest is **8,924 bytes**, SHA-256
`3f40928986289604dba4575030129b7682bd83eb924840e66ede5ff7d80e597b`.
The manifest and all 19 files bound in its `consumed_inputs` and `new_outputs`
were verified without alteration. Verification of bytes is distinguished from
reading or independently reviewing every mathematical input.

## Scope and premises

The assigned scope is the actual topological and ordinary singular-H0
argument in §§4–6, including its exact C263/C264 imports. The analytic
derivation of the asymmetric faces in §3 and quantitative good-event/point
process coupling in §§7–8 belong to the main review. Here the deterministic
premises are consumed explicitly: an embedded closed chart strip
`D=[-R,s]×[-R,R]`, the stated ridge and vertical-concavity conclusions,
`0<s≤R/2`, `m=F(M)>d=F(S)`, `F≤m` on D, the boundary gate
`∂D∩{F≥d}={S}`, and the ridge point P outside D with `F(P)>m` and ridge
minimum d. These geometric premises, rather than the desired elder relation
or an interval certificate, drive the argument.

The ambient surface has its usual Hausdorff manifold topology; the chart
image must be embedded with exactly the specified boundary and interior.
The periodic finite Fourier application is on the torus quotient. When the
Euclidean C263 definition is used, its function is the periodic Euclidean
lift. The actual strict and closed higher-path equivalences in
`TorusTopology.lean` transfer the predicates between that lift and quotient.
There is no identification of an arbitrary surface with Euclidean space,
and this paper argument is not asserted to elaborate as a new Lean theorem.

For the local cut, gate, and interval split, compactness or Morse behavior
outside the chart is not needed. Compact C4 Morse geometry with distinct
critical values is retained precisely where the proposal invokes an older
critical maximum, a unique global critical event, the source selector, and
the canonical finite elder-bar label. The coefficient field is nonzero.

## 1. Global separation and actual attained strict cut

For `α>d`, the strip boundary misses `Xα={F≥α}`. Thus

`Xα∩D = Xα∩int(D)`

is closed relative to Xα because D is closed and open relative to Xα because
`int(D)` is open. A path or connected subset cannot cross this partition.
This is a statement in the full ambient surface. Remote topology, paths
leaving the chart, and remote critical points cannot evade it. Compactness
of D follows from the closed finite rectangle and the embedded chart; its
closedness uses the Hausdorff ambient topology. The proposed no-bypass proof
does not assume that a local Hessian index already determines a global merger.

For `d<α≤m`, every point of `Xα∩D` joins its ridge point vertically within
Xα: strict concavity gives a fiber interval containing its maximizing ridge
point. On the ridge, the unimodal superlevel set is an interval containing
M, so the ridge path to M remains in Xα. Therefore this clopen set is one
full path component, not merely a connected subset. At α=m it is `{M}`;
for α>m it is empty. Since F≤m on D, every higher point lies outside D.
It follows that no closed path at any α>d joins M to a point above m.

The displayed ridge from M to P has minimum exactly d at S. It is an actual
closed-superlevel path in Xd. Any path in Xd from the interior point M to
any point above m must meet ∂D. At that meeting it must be S, by the gate
identity. One can take the first exit from `int(D)` on the compact parameter
interval; no compactness of a set of paths is invoked. The endpoint is
outside D, so this exit exists.

For the literal C263 clearance set, every h<d is witnessed by that same
ridge path. Every h≥d is excluded by its forced boundary crossing at height
at most d; h≥m is also excluded at the starting endpoint. Consequently

`C_M=(-∞,d)`, `C_M≠∅`, `deathHeight(F,M)=d<m`, and M is nonessential.

This proves the missing closed attainment directly. The exclusion of d
from the strict clearance set is compatible with a closed path of minimum
d. The nonempty branch of the guarded real supremum applies, so C263's
empty-set default 0 is irrelevant. On the periodic application, the strict
and closed quotient-transfer theorems preserve their respective predicates;
neither is used to change a strict inequality to a closed one.

**Verdict:** the no-bypass, strict-cut and attained-gate conclusions in §4
are valid under the displayed deterministic geometry.

## 2. The saddle is a merger and reaches an older maximum

The accepted local ridge calculus gives `Fyy(S)<0` and `f''(s)>0`.
At a stationary ridge point the Schur-complement identity is
`det Hess F(S)=Fyy(S) f''(s)<0`, so the planar saddle is nondegenerate
and has one negative and one positive direction.

The two upper local sectors have different global path components above d.
The left ridge sector joins M and stays on the inside side of D. The right
ridge sector joins P and stays on the outside side. A path between them at
an above-d level contradicts the same clopen partition. At d the explicit
ridge joins them through S. This supplies the global incidence needed to
exclude a loop saddle. The argument does not infer merger from index alone.

The older-maximum extension in §5 is valid with the explicit compact Morse
premises. A compact Morse surface has a finite critical set: critical points
are isolated and the critical set is closed and compact, so an infinite
set would have a critical accumulation point contradicting isolation.
Thus one may choose a regular h0 strictly between m and F(P). The regular
superlevel is a compact manifold with boundary, hence locally path
connected; its connected/path component containing P is both compact and
path connected. F attains its maximum there. That value is at least F(P)>h0,
so the maximizing point O is away from the regular-level boundary and is
an ambient interior local maximum. It is critical, and Morse nondegeneracy
makes it a nondegenerate maximum. A path within this component joins P to O
above h0>d. Concatenating it with the ridge gives the required older-maximum
path at d. This is ordinary compactness of one superlevel component, not
compactness of the collection of all paths.

The component containing M has no outside incidence above d and no higher
point before d; at d it meets a component with an older maximum. Hence d is
its first elder merger. This local strip happens to exclude any earlier
outside merger, but no assertion about first mergers of arbitrary maxima
is needed. Distinct critical values make S the unique critical point at d
on the surface/quotient. Periodic Euclidean lifts are deliberately not
unique. Without distinct values the gate and cut persist, while a remote
critical point at the same height may remain. The proposal states this
limitation correctly.

The exact finite-H0 selector (7) in the pinned conventional source requires
the compact Morse/distinct locus, critical endpoints, maximum/saddle types,
finite death `d<m`, and equality of death with F(S). These have the stated
join under the trap. That source's finite component/elder-basis induction
supplies its conventional barcode interpretation; this review does not
convert it into a Lean theorem or a source-adoption decision.

**Verdict:** §5 establishes the claimed merger, older extension and unique
critical event on its explicitly restricted compact Morse/distinct locus.

## 3. The ordinary-H0 interval is an actual direct summand

Let Hα be actual ordinary singular H0 over a nonzero field k, with maps
`Hα→Hβ` for β≤α. Let Iα=k for `d<α≤m`, zero otherwise. The interval becomes
`[-m,-d)` in the exact increasing parameter `t=-α`; the birth is included
and the death is excluded.

At active levels both M and the same fixed higher point P belong to Xα,
and `[M]-[P]` is nonzero because they are in different path components.
It maps to zero already at β=d by the closed ridge path. Thus the proposed
j is the actual H0 point-class difference, not a replacement component
module and not an assertion that the ordinary class [M] dies. Ordinary
augmentation keeps either individual point class nonzero. The argument is
unchanged in characteristic two, where subtraction is addition.

At active levels, D isolates exactly the M component. Under the actual
component/H0 isomorphism, the component coefficient function 1 inside D
and 0 outside defines a linear map q. It exists even with infinitely many
outside components: ordinary H0 is the direct sum of field copies indexed
by path components, and a linear functional on a direct sum is specified
by arbitrary values on its component generators. No local path connectivity
outside D, finite-dimensionality, or barcode theorem is required here.

For every ordered pair α≥β, the two naturality equations hold. The exhaustive
case analysis is:

| Source/target range | Section j | Retraction q |
|---|---|---|
| Both active | Fixed M/P classes transport to the same classes. | A point remains the same point; target clopen separation preserves its inside/outside indicator. |
| α>m, target active | The interval source is zero. | No source point lies in D since F≤m there. Its image is outside D and q kills it. This is the necessary prebirth square. |
| Active source, β≤d | The difference maps to zero by the ridge path in Xd⊆Xβ. | Target interval and q are zero. |
| Both interval spaces zero, including prebirth to after death | Both interval/source maps force the section square to zero. | Either both q's are zero or the interval map is zero with zero target. |

Descending height prevents an already-dead source from mapping back into
an active target. This covers all real levels, including exact birth and
death and any remote critical heights, not only regular levels.

At active α, `qα jα(1)=1-0=1`. At inactive α the identity of the zero space
is the zero map. Therefore `qj=id_I`. Pointwise kernel objects form a natural
submodule, and the two displayed maps

`v↦(qv,v-jqv)` and `(c,w)↦jc+w`

are inverse natural linear maps. Indeed `q(v-jqv)=qv-qjqv=0`, and the two
compositions simplify using qj=id. Consequently `H≅I⊕ker(q)` is an actual
interval direct summand. This is stronger than merely showing one vector
vanishes at d. It also remains properly weaker than an exhaustive barcode
decomposition or a canonical label theorem without the added finite-event
Morse/distinct premises. The source's maximum birth event and elder basis
give the multiplicity-one labeled interval under those premises. A splitting
can depend on the choice of outside reference P; canonical labeling is not
inferred just from a particular section/retraction.

**Verdict:** §6 gives a valid conventional direct-summand proof, with all
birth/death naturality obligations and the correct ordinary-H0 difference.

## 4. Exact formal imports actually read

The following are exact local copies bound by the author manifest to the
declared Math- source cut `319f9c45f66dbcce4a71b9c2f3e0fb62a666bfec`.
The relevant definitions and proofs were read directly, rather than only
the prose interface audit. No Lean compiler, kernel audit, proof replay,
or runtime check was executed.

| Exact file / SHA-256 | Relevant inspected substance | Reuse boundary |
|---|---|---|
| `SuperlevelBar.lean` / `346eea948e18d5904422904006827930e27d3141ccbc19ee8ac2c24bcf65a4a9` | Definitions of essentiality, strict paths and guarded real supremum; `strict_cut`, nonempty/cut/bounds and `cut_unique` proofs. | Actual Euclidean strict cut. It does not itself prove closed attainment, saddle incidence or any interval. |
| `ClosedSuperlevel.lean` / `90d1481b75d9c6d14e462c3fbf0bf7c7cdd0efb9eaad68d6732400658753b1c2` | Literal `{x|-t≤g x}`, inclusions and functor laws, actual singular-H0 filtration, path-component map and `JoinedIn` equivalence. | Correct sign, closed endpoints and actual inclusion maps. No Morse or barcode result. |
| `OrdinaryH0.lean` / `3d6b0d6b53413c484b1d010bccf0d53ae7f75becb2d747868f22dbd673fe0a88` | Actual simplicial/singular point classes; point transport; objectwise comparison; hom-ext proof; proved comparison naturality; `ordinaryH0_naturalIso`; augmentation and distinction; difference transport; `ordinaryH0_filtrationIso`, its naturality and difference-zero iff target `JoinedIn`. | The comparison is a proved natural isomorphism of actual singular H0 with component-indexed coproducts. It supplies precisely the comparison needed for q, not an already-implemented interval split. |
| `TorusTopology.lean` / `ddb145b3f791c181d4f2a51e54e711937297bd6476ba55bcd5252b7ddb57cfe1` | Descent and continuity, path lift with existential endpoint, general/strict/closed higher-path equivalences and global-max equivalence. | Preserves strict or closed predicates separately and supplies the lift/quotient semantic join. No arbitrary preselected lift endpoint or new attainment theorem. |
| `SuperlevelBarField.lean` / `8a2470431c3fda5e98859aa9372cbb8866ed5c5c722cea5dfc28cb577840bbad` | Interface fields and `elderPartner_iff` definition, essential/death record uniqueness, relation comparison. | The elder predicate is defined by endpoint type and height; its definitional equivalence is not an independent persistence interpretation. |
| `Specifications/Field.lean` / `f22c91e082cd7e738ba47c9c3534e47ac687d066f0b78586d15103cf1132535e` | Actual derivative-zero criticality, inertia, nondegenerate maximum, index saddle, Morse/distinct and interface definitions. | Smoothness, inertia/local-Morse meaning and quotient alignment remain explicit formal obligations. The separate Lifetime record is not inhabited by this review. |

The C264 naturality is substantive: it tests actual singular homology maps
on point classes, proves the objectwise comparison square, assembles a
natural isomorphism, and restricts it along the actual closed-superlevel
filtration. It is not a compatibility assumption added to a record. The
paper q uses that proved bridge correctly. Defining the field-valued interval,
its indicator natural map, its squares and its split remains new formal work,
as the proposal explicitly records.

The pinned conventional `finite_h0_lifetime/PROOF.md`, **27,064 bytes**, SHA-256
`5ea91111fa5f3d78d7c4188ebe84b3bc2c452b05dfdfc62c74b03123cb2696d1`,
was read in §§3–4: countable open connectivity and threshold, regular-band
flow/local Morse event imports, finite elder-basis induction and selector (7).
The proposal correctly consumes this as conventional mathematics with its
classical geometric imports. This review did not reprove those imports from
primary books, and did not reclassify this prose as a formal implementation.

## 5. New independent controls and what they do not establish

`independent_topology_controls.py` was newly written for this review. It does
not import or run the author controls or previously accepted controls. Its
observed execution exited **0**, with empty stderr, producing
`INDEPENDENT_TOPOLOGY_CONTROLS.json`.

It constructs 16 finite graph filtrations with varying remote connections,
18 levels including exact birth/death and prebirth levels, and coefficients
over Q, F2 and F3. It independently computes graph-chain boundary ranks and
component quotients, tests both j/q naturality on every ordered tested pair,
the prebirth squares explicitly, `qj=id`, kernel projection, inverse splitting
maps, strict higher-endpoint clearance and the closed widest-path threshold.
Remote ties are allowed to test that the split itself does not silently use
distinct-value uniqueness.

All **37,364 positive checks** passed. **Seven negative controls** were
rejected: death of the individual ordinary point class, augmentation as the
retraction, inclusion of the death endpoint, strict clearance at the attained
closed gate, exclusion of bypass from local saddle type alone, omission of
the prebirth square, and unique global critical level from the trap alone.
The bypass and invalid prebirth maps deliberately violate the needed geometry;
their failure confirms the relevant obligation was not dropped. These finite
models are controls of the algebra and conventions, not a numerical proof of
surface topology, all-parameter analysis, Morse theory or Lean code. The
continuous proof audit above is the basis of the scoped mathematical verdict.

The JSON also verifies the exact 19 author-bound files and manifest identity.
The final review manifest binds new reviewer outputs separately from those
unchanged inputs. No frozen source, previous review, Lean artifact, remote or
native record, runtime configuration, status or scientific register was edited.

## 6. Disposition

**ACCEPT_SCOPED:** §§4–6 prove the claimed deterministic isolated gate,
actual attained C263-compatible death, nonloop elder merger on the stated
compact Morse/distinct locus, and one actual ordinary-H0 interval summand.
No author amendment is required for this assigned scope. This verdict does
not independently accept the analytic or stochastic sections assigned to
the main reviewer.

The remaining formal quotient geometry, Hessian/inertia alignment, interval
object, indicator natural transformation and split are still unimplemented.
The canonical finite elder-bar label retains the explicit compact Morse and
distinct-value finite-event interpretation; the single split does not prove
all bars, all maxima, all lifetime marks, reverse microscopic regularity or
full persistence universality. No source adoption, production/native/remote
write, Lean execution, organizational independence or scientific promotion
is implied. Scientific effect **NONE**.
