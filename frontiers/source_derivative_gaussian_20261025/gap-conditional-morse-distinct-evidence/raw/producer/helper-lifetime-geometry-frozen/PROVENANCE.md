# Stage59 Lifetime inertia and quotient geometry — text-only freeze

Author: OpenAI/Codex `/root/intrinsic_h0_packaging`, delegated by root to the
new directory `/workspace/scratch/gap-morse-lifetime-geometry-text` only.
The target is the one actual authorized production module
`SourceGapConditionalMorseDistinct`, namespace
`I4SourceGapConditionalMorseDistinct`.

Root's `/workspace/scratch/gap-conditional-morse-distinct-construct/ROOT_GO.json`
was read. Implementation authority was issued21:39:26.224202UTC26October2026
after proper PRECODE `a88e4c65fe2b02de9638c4482e4d50f767359205` and native
pickup [6427944131](https://github.com/d6g8k5htny-coder/Math-/pull/514#issuecomment-6427944131)
created21:37:44UTC; board mirror6427944709. The qualified baseline is
`f89543e2a81f56418a083c62a49e9689a189a139`,58modules/1128written=
1119Prop+9data/32inputs. The published12298B control contract is bound by
the supplied existing SHA
`aa42af6f306361343b0536bbd1cece548d0094a705bbadd56f76bb7d637564a9`.
These identities/process facts were transcribed from root's record; no old
identity was recomputed. Checkpoint23:15UTC26October and terminal03:15UTC
27October/invocation-end are unchanged.

## Agreed lexical context before proof text

Producer `/root/h0_older_clearance_construct` froze
`/workspace/scratch/gap-conditional-morse-distinct-construct/SHARED_CONTEXT59_V1.md`
before helper proof text. This helper personally read and ACKed that context,
then proposed the exact generic matrix adapter and four-control shape. The
producer explicitly ACKed that additional private interface as its V1
supplement before proof text. The shared context was not hashed here.

Insert `SECTION.lean.txt` exactly once inside the target namespace, in its
noncomputable section, with `autoImplicit false`, the producer's declared
opens and private alias `Point2 := Fin 2 → ℝ`. The actual Lifetime type `E 2`
remains `EuclideanSpace ℝ (Fin 2)` and is never silently replaced by `Point2`.
`IMPORTS.txt` lists exact additional public imports. No private data definition
or public declaration is added; local `let` definitions stay local.

Complete private declarations supplied:

1. `geometry59_spectral_quadratic`: public Hermitian spectral basis gives the
   literal coordinate quadratic form as the sum of eigenvalue-weighted squares.
2. `inertia_of_symmetric_matrix`: an arbitrary actual Lifetime field `g`, point
   `X`, real Hermitian2x2matrix, exact quadratic identity and nonzero determinant
   give `∃ j, Lifetime.HessianHasInertia 2 g X j`.
3. `actual_inertia_of_source_det`: exactly the V1 displayed actual-source
   `xx*yy-xy^2 ≠ 0` statement at `coordinates 2 X` yields genuine inertia.
4. `inertia_control_positive`: `diag(1,1)` under its exact quadratic identity.
5. `inertia_control_negative`: `diag(-1,-1)` under its exact quadratic identity.
6. `inertia_control_axis_saddle`: `diag(1,-1)` under its exact quadratic identity.
7. `inertia_control_zero_diagonal_saddle`: `[[0,1],[1,0]]`, whose quadratic
   form is `2*x0*x1`, under that exact identity.
8. `geometry59_projection_eq_lattice`: equal original AddCircle-product
   projections give the literal integer lattice shift of coordinate lifts.
9. `projection_eq_torusDist_zero`: equal projections of actual Lifetime
   coordinate lifts give the literal infimum-defined `torusDist = 0`.
10. `source_jets_of_projection_eq`: equal projections give unchanged source
    values and equality of the complete iterated derivative at every order.

The projection-distance lemma spells its unused positive-period binder
`_hL`; the agreed positional type is unchanged. Its lattice argument actually
works without positivity. The producer was notified to consume it positionally.
The source/jet and actual-Hessian adapters use the agreed positive-period
hypothesis. No extra global conclusion is exposed by this helper.

## Genuine inertia, including the zero-diagonal saddle

The generic adapter invokes the public real Hermitian spectral theorem.
Nonzero determinant implies every eigenvalue is nonzero by the public
determinant/product identity. It constructs actual submodules of `E 2`:

- `V`: eigenbasis coefficients vanish outside the negative eigenvalue indices.
- `W`: eigenbasis coefficients vanish at all negative eigenvalue indices.

Masked eigenbasis coordinate vectors explicitly decompose every vector into
`V+W`; injectivity of the orthonormal representation proves disjointness.
`Submodule.finrank_add_eq_of_isCompl` gives dimensions `j` and `2-j`, taking
`j = finrank V`. Weighted-square sums are strictly negative/positive on each
nonzero vector, using a nonzero represented coordinate. These are genuine
complementary signed submodules, not a record of asserted inertia. There is
no nonzero diagonal/pivot hypothesis or excluded saddle branch. In particular
the zero-diagonal offdiagonal matrix is covered by the same generic proof.

The actual source adapter derives its symmetric coordinate matrix internally
from the actual second derivative. Public smoothness/Schwarz symmetry supplies
`yx = xy`, and public `SourceActualFoldCandidate.actual_hessian_coordinates`
transports the actual bilinear form to coordinates. The source's determinant
hypothesis is precisely the determinant of this matrix. The adapter needs no
criticality hypothesis; the producer joins its agreed actual critical-gradient
adapter when proving the final `Lifetime.IsMorseDistinct` proposition.

Each of the four finite-form positives directly calls the new generic adapter.
Their premises are displayed exact quadratic identities. They are honest
finite-form controls, not claimed realized Gaussian samples, extra campaigns
or extra public research targets. No56foreign-private planar proof was read,
copied, named or assumed; no supplied inertia certificate appears.

## Literal quotient/lift transport

The quotient bridge uses the accepted public AddCircle coercion-zero criterion
to produce integers `n`. The public `coordinates_latticeVec` identifies the
same shift in Lifetime's Euclidean cover. One exact zero lattice-distance term
gives the upper bound on the defining conditional infimum, and norm
nonnegativity gives the lower bound. No alternative torus metric is substituted.

For jets, the unchanged original source's public lattice periodicity gives an
equality of entire translated functions. Public
`iteratedFDeriv_comp_add_right` then gives every-order jet equality directly,
including the value/gradient/Hessian cases the producer consumes. There is no
quotient path-lifting theorem, random lift, measurable selector, extra model,
or conditional law assertion.

## Public API reads and qualification boundary

Read-only accepted API lookup covered:

- `inputs/Lifetime.lean`: `E`, `hessian`, `HessianHasInertia`, `torusDist`.
- `inputs/SourceLifetimeGeometry.lean`: coordinates, lattice vectors and actual
  source-field definitions/periodicity.
- `inputs/SourceTorus.lean`: literal product AddCircle projection and public
  lattice/coercion argument.
- `SourceActualFoldCandidate.lean`: public coordinate criticality and actual
  Hessian transport; no old proof was reverified.
- Existing accepted Morse-incidence API/header searches for public names and
  second-derivative symmetry routing, without copying foreign-private proofs.
- Mathlib public `Analysis/Matrix/Spectrum`, `Analysis/Matrix/Hermitian`,
  `Analysis/InnerProductSpace/{Symmetric,PiL2}`, `Analysis/Normed/Lp/PiLp`,
  `LinearAlgebra/FiniteDimensional/Lemmas`, submodule lattice/span interfaces,
  ordered finite sums, and `ContDiff/FTaylorSeries` translation identities.

Only source reading, new text writing and first custody recording of these
new originals occurred. No Lean invocation,
`#check`/name probe, parser/check/test/build, kernel/audit/control campaign,
object creation, source integration, source58/helper inspection, old proof or
hash replay, shared metadata/config/cache/Git/external action occurred.
Helper execution counts are all **0**. This is complete candidate proof TEXT;
it has not been elaboration checked or qualified in isolation.

The first identities of the three newly authored originals are recorded in
`FROZEN_IDENTITIES.json` once after this freeze, with an immediately durable
per-file intent/identity journal. No recursive self-hash is claimed for the
identity record itself. The producer alone integrates the section **ONCE**,
keeps these originals unchanged, records every actual local amendment with a
complete patch, and qualifies the exact final owned production module and
its complete actual inventory/one own kernel/source-local controls. No helper
object, standalone campaign, public API or separate target credit exists.

Owner `/workspace/AGENTS.md` remains binding: completed applicable verification
is reusable; a new agent/session/handoff/Git/process label is not a replay
reason. Different actual family/process requirements stay separate from
established mathematics. Scientific effect **NONE**; same-family/provider-
distinct credit **0**. All earlier58 packaging and all other source/helper
directories remain unchanged.

Canonical authority is carried from the producer/root contract. Delivery of
these links does not itself establish that their contents were read:

- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OWNER_MANDATE_20261015.md
- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OP-AUTONOMY-20260923-v2.1.md
- https://github.com/d6g8k5htny-coder/main/blob/main/governance/OWNER_DECISION_20261025_REVIEW_FAMILIES.md
