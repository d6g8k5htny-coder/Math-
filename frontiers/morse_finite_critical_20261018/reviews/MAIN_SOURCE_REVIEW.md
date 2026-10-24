# C293 exact main-source nonauthor review

Review date: 2026-10-18 UTC. Reviewer: OpenAI Codex delegated agent
`/root/c292_geometry_review`, for Dylan Roy. Verdict:
**ACCEPT_SCOPED_MAIN_SOURCE**. I found no mathematical or theorem-interface
must-fix defect in the exact main source identified below. This is acceptance of
the source proof of finite projected literal critical points. Final frozen build,
control execution, axiom census, and kernel replay remain separate pending gates
at this report's issue time. This report does not declare C293 fully accepted or
published.

## Identity and actual exposure

All paths below are relative to
`$C293_ROOT`.
I read the complete 223-line main source and complete author notes after the
parent announced the exact freeze; I did not inspect or edit the developing main
file. I also read the source input manifest, scope document, relevant literal
definitions in Lifetime, the complete TorusTopology companion in the preceding
review work and its relevant quotient construction again here, and the relevant
pinned Mathlib API declarations. I read the clean author compile receipt and
verified its empty stream hashes and matching current development object hash.
I did not run Lean, leanchecker, or modify any author proof.

I previously reviewed C292's conventional proof, performed a read-only API
feasibility audit for the current finite-critical step, and wrote the prospective
C293 `reviews/REVIEW_PLAN.md`. That feasibility work discussed both a compact
representative-domain route and a closed/discrete quotient route. It was reported
to the parent before author implementation. I was exposed to the intended claim,
the definitions, proposed dependency routes, and control ideas, so this is not a
blind review. I did not coauthor this main file. The author and reviewer use the
same provider/organization, OpenAI; organizational-independence credit is **0**.

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `project/MorseFiniteCritical.lean` | 9445 | `95a660134eda49eecfe6181884bd23b4e4ca210e228d2463de29e5f821df047b` |
| `AUTHOR_NOTES.md` | 5606 | `7ff0f8c928cd5bf87e036079e5f3e5549d44499a89f1dc59b0793c956884f251` |
| `SOURCE_INPUTS.json` | 1481 | `6554ae0e27dd7a3bf9e280939710dff8948b6aef636c3920526668ccde299e0e` |
| `project/Lifetime.lean` | 51383 | `90f4892608e953ecc696bb32ea159d1c178ceb8a1c6edfd11acfceb14af462c6` |
| `project/TorusTopology.lean` | 12257 | `ddb145b3f791c181d4f2a51e54e711937297bd6476ba55bcd5252b7ddb57cfe1` |

These are locally recomputed byte identities, not substitutes for proof review.
The manifest identifies Lifetime with Math- cut
`db43694c9f9dbff2987e2e3c0a1260b5c48310ec`, path
`frontiers/source_lifetime_realization_20261017/inputs/Lifetime.lean`, blob
`f2508f7f2e3fd42f22f5aa52bc5ead5ff9e73b9a`; TorusTopology with cut
`c8ec07034608741585111603f1b506393c340908`, path
`companions/torus_filtration_20261011/TorusTopology.lean`, blob
`ed678ea322fe5315b3aaff44e4e2f06b018399d8`. This review made no fresh remote fetch.
The local files agree with the supplied byte-pinned inputs. Mathlib API review
used the existing checkout at
`$PINNED_PROJECT/.lake/packages/mathlib`,
whose recorded HEAD is `d13f23b723b8a846827a245b89c10fc7d3f11612`.
This source review is not a fresh whole-dependency-tree byte audit.

## Exact endpoint and hypotheses

`TorusMorseFinite.quotientCriticalSet` at lines 150–152 is exactly
`torus_proj d L hL '' {x : E d | IsCriticalPoint d g x}`. It is the image of all
literal Euclidean critical points on the actual period-lattice quotient from
TorusTopology. It is not a chosen list of points, an abstract finite event type,
or the whole Euclidean critical set.

The main endpoint `quotientCriticalSet_finite` at lines 217–221 quantifies over
every natural dimension `d`, every real `L` with explicit `hL : 0 < L`, and
`g : E d → ℝ`. Its other hypotheses are exactly the literal `IsSmooth d g`,
`IsLPeriodic d L g`, and `IsMorseDistinct d L g`. Its conclusion is finiteness of
that full projected critical set. The core theorem at lines 203–213 replaces
Morse-distinct by only its first clause: every literal critical point has some
`HessianHasInertia`. Distinct critical heights are not used, as the source says.
The endpoint validly includes dimension zero; C292 can instantiate positive
dimension without any new assumption.

The literal inputs have the expected force: `E d` is
`EuclideanSpace ℝ (Fin d)`; smoothness supplies `ContDiff ℝ n g` for each finite
natural n; criticality is `fderiv ℝ g x = 0`; the Hessian is
`iteratedFDeriv ℝ 2 g x ![v,w]`; inertia supplies complementary subspaces with
strict negative and positive quadratic values on their nonzero vectors.
Periodicity uses exactly the same coordinate lattice-vector formula as
TorusTopology. No desired finiteness, discreteness, local inverse, local normal
form, level-set path, death value, elder relation, pairing, or count premise is
hidden in these theorem signatures.

## Substantive reconstruction

1. **Literal Hessian and symmetry, lines 21–30.**
   `iteratedFDeriv_two_apply` identifies the literal second derivative with
   `fderiv ℝ (fderiv ℝ g) x v w` in the correct argument order. The C2 instance
   supplied by `hsmooth 2` gives `isSymmSndFDerivAt`; therefore cross terms may be
   interchanged. Symmetry is proved from smoothness, not assumed from the name
   “inertia.” This matters because the bare complementary-sign predicate is
   insufficient for a nonsymmetric bilinear form.

2. **Injectivity from complementary signs, lines 32–73.**
   Put B = D(Dg)(x), and suppose Bz = 0. Complementarity gives z = v+w with
   v in V and w in W. Evaluation on v and w yields
   B(v,v)+B(w,v)=0 and B(v,w)+B(w,w)=0. Symmetry makes the cross terms equal, so
   B(v,v)=B(w,w). Strict negativity on nonzero v and strict positivity on
   nonzero w force both to vanish, including the separate cases where one
   vector is zero. Hence z=0; applying this to u−v proves injectivity. The proof
   does not incorrectly assume V and W are B-orthogonal. The dimensional
   equalities in inertia are unnecessary for this kernel argument; discarding
   them does not weaken its validity.

3. **An actual continuous linear isomorphism, lines 75–92.**
   The derivative map has codomain the continuous dual of E, not E itself. The
   proof handles this type distinction with the real Riesz isomorphism J from
   `InnerProductSpace.toDual`. J inverse composed with B is an injective
   endomorphism of finite-dimensional E. `LinearEquiv.ofInjectiveEndo` makes it
   an algebraic equivalence, and the finite-dimensional continuity API makes it
   a continuous linear equivalence. Composition with J gives an equivalence
   E ≃L continuous-dual(E) whose underlying map is proved equal to B. The real
   field specialization avoids a complex conjugate-linearity mismatch.

4. **Euclidean isolation, lines 94–114.**
   C2 regularity supplies C1 regularity of Dg by
   `contDiff_succ_iff_fderiv`. The just-constructed equivalence is the actual
   derivative of Dg at x. The inverse function theorem's
   `ContDiffAt.toOpenPartialHomeomorph` provides an open source containing x
   on which Dg is injective. Any other literal critical y in that source has
   Dg(y)=0=Dg(x), hence y=x. This is a real derivation of isolation; the result
   is not supplied as a premise. No Morse normal form is invoked.

5. **Periodicity and descent, lines 116–147.**
   The literal equality `g(y+latticeVec)=g(y)` gives equality of the translated
   functions. `fderiv_comp_add_right` then proves periodicity of the actual
   derivative. `torus_proj_eq_iff` converts equality of quotient points to the
   same lattice translations, and the proof respects the relation in the
   required orientation. `quotientDerivative` is a `Quotient.lift` of Dg with
   an exact projection formula. Its continuity follows from C1 regularity and
   the quotient topology. A new smooth manifold atlas or a quotient tangent
   bundle is not needed for this zero-set argument.

6. **All quotient critical points and closedness, lines 150–175.**
   The membership equivalence between projected literal criticality and zero
   descended derivative is proved in both directions. The reverse direction
   uses surjectivity of the actual projection. Consequently the projected set
   is a continuous map's zero set and is closed. This avoids the invalid general
   inference that a continuous image of an arbitrary closed Euclidean set is
   closed. It also supplies criticality of every representative of a critical
   quotient class, which is used in the next step.

7. **Quotient discreteness, lines 177–199.**
   For q=π(x) critical, choose the open isolating source U of x. The covering
   projection is open, so π(U) is an open quotient neighborhood. If a critical
   quotient point lies in π(U), choose y in U mapping to it. The zero-set
   equivalence makes y itself critical, so y=x. Thus π(U) intersects the full
   quotient critical set in exactly {q}. This step does not require π to be
   injective on U: saturation of criticality supplies the needed conclusion.
   Conversely q belongs to that intersection using x. This establishes the
   exact `IsDiscrete` predicate, not merely isolatedness of selected lifts.

8. **Compactness and finiteness, lines 203–221.**
   TorusTopology proves compactness of the actual quotient from its full
   period lattice. Intersecting its compact universe with the closed critical
   set makes that set compact. `IsCompact.finite` applies to this compact,
   discrete set. The final literal Morse-distinct wrapper passes precisely
   `hmorse.1`. Closedness is essential to this compact/discrete argument and
   is present; ambient compactness alone would not suffice for an arbitrary
   discrete subset.

The relevant pinned APIs include
`Mathlib/Analysis/Calculus/ContDiff/FTaylorSeries.lean:949`,
`Analysis/Calculus/FDeriv/Symmetric.lean:534`,
`Analysis/InnerProductSpace/Dual.lean:137`,
`LinearAlgebra/FiniteDimensional/Basic.lean:413`,
`Analysis/Calculus/InverseFunctionTheorem/ContDiff.lean:30`,
`Analysis/Calculus/FDeriv/Add.lean:888`, and the discrete-subset/compactness
APIs. Source API inspection supports the mathematical reconstruction; final
elaboration and kernel evidence have their own gates.

## Negative cases and frozen controls source

The parent separately authorized inspection of its frozen, root-authored
`project/MorseFiniteControls.lean`. I read the complete file after that notice.
Its locally recomputed identity is 2843 bytes,
SHA-256 `e6171c949ec60a3aea21a8cc028180e16c82e4946a232107d9e82bf8018cdac1`.
I supplied prospective control ideas but did not author this control source.
Source review of these controls finds their statements and proofs appropriate:

- `nonsymmetricForm_bilinear`, `complementary_axes`, and
  `nonsymmetric_signed_axes_singular` exhibit
  B(v,w)=(v1−v2)(w1+w2), negative on the second axis, positive on the first,
  with nonzero left-radical vector (1,1) and unequal swapped cross terms.
  The axes' direct-sum property is proved through decomposition and trivial
  intersection, rather than bundled as a `Submodule.IsCompl` term. The
  mathematics is explicit and suffices to expose the error of inferring
  nonsingularity from complementary signs without symmetry. This is not a
  counterexample to a smooth scalar Hessian.
- `nonsmooth_literal_critical` uses the norm on the literal one-dimensional
  E space. It is nondifferentiable at zero while its default `fderiv` is zero,
  so it satisfies literal criticality there. This is a genuine interface
  caveat; it does not establish a periodic Morse counterexample or prove
  that removing smoothness from the full final theorem is false.
- `half_open_not_compact` and `closed_interval_compact` correctly distinguish
  [0,1) and [0,1]. They are ancillary to this chosen derivative-descent proof.
  Neither the main proof nor this review claims a half-open domain was used
  to obtain compactness.

Additional mathematical boundary checks in this review: a constant smooth
periodic function in positive dimension has every quotient point critical and
does not satisfy the nondegeneracy premise; Euclidean critical points of a
periodic Morse function need not be finite; and a discrete subset of a compact
space need not be finite unless compactness of the subset is secured. The main
statement avoids all three errors. These observations are review arguments,
not claims that extra Lean controls have executed.

This report does not inspect or approve a final expected-failure invocation
without nondegeneracy: those exact frozen sources, command, and diagnostic must
be reviewed later. A missing-premise elaboration rejection would establish an
interface boundary, not by itself a constructive counterexample. The parent's
first failed control elaboration is development history, not a successful
negative control.

## Observed development evidence and runner source review

I read `runs/20261018T022037Z-MorseFiniteCritical-67cf4c01/RECEIPT.json`
(1138 bytes, SHA-256
`2e52f99233bfc2b281054b27f6a637a647a964b9beb555ae9f5810a9f86c3bc3`).
It records the exact main source above, return code 0, no timeout, unchanged
source, elapsed 135.406404667 seconds, and empty stdout/stderr. I locally
confirmed empty-stream hashes and the recorded development object hash:
`build/MorseFiniteCritical.olean`, 493256 bytes,
`34ff2a9ed529609dd48a22204b8eacc66eeb943805e2d6e8dee4481cde8ef4e2`.
This is receipt/artifact verification of the author's development compile,
not an independent reviewer rerun or final kernel acceptance. The historical
first author attempt and its deprecation warnings are described in the author
notes; no conclusion here treats their existence as a main-source failure.

I also read the complete preparer and final runner as offered by the parent:

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `run_final_phase.py` | 11571 | `1418556d3f458ae5ad05f0fb60ac27b5478f4f984e2ca8b26ac9fc4736a524ab` |
| `prepare_final_inputs.py` | 3387 | `a007e797d6ab56f39bdfe00050d6a0e8b360b4b9bd208cf2dbd58369e4e89925` |

I found no current-source execution flaw requiring a change in those scripts.
The preparer freezes copies of all five listed modules, records hashes and
build order, validates the inherited dependency baseline, and starts with an
empty final build directory. The runner binds its source inventory, checks the
runtime and dependency inventory, builds only after required local imports have
accepted objects, enables warnings-as-errors for the new modules, and refuses an
implicit same-module rebuild. It checks source and imported-object identities
after execution, enforces bounded processes, and records streams and receipts.
The exact final source inventory must still match the reviewed hashes.

The dependency method deliberately reuses earlier content hashes when file
metadata match the C291 baseline, and hashes metadata-delta files. This is not
a fresh full-content sweep. The runner's standard `leanchecker -v` replay uses
the pinned runtime and shared imported objects; it is not a second independent
proof implementation or a claim of fresh verification of every dependency.
The axiom census must be read and assessed substantively; recording a successful
audit-module process alone does not establish acceptable axioms. These are
stated evidence boundaries, not detected proof defects.

## Disposition and remaining gates

No main-source amendment is requested. The implementation completes the full
deterministic dependency promised here: literal Hessian inertia plus smoothness
gives an actual derivative isomorphism, isolated literal critical points, and
finiteness of all projected critical points on the actual compact quotient.
The closed/discrete quotient route validly replaces the prospective
parallelepiped route; no representative-boundary argument is now missing.

Pending later exact-artifact review: final inventory and source identity,
warning-strict final builds, successful exact control execution, any
expected-rejection control and its actual reason, complete axiom output, standard
kernel replay receipts, and final preservation of these hashes. I do not promote
those gates from the author's development compile or this source verdict.

This result does not formalize the rest of C292: no Morse normal form,
closed-level local path connectedness, attainment of literal death, closed trap,
older endpoint/path, new persistence-module interval construction, all-bars
result, saddle pairing, collision law, or Gaussian almost-sure Morse theorem is
proved by this file. No scientific-status, organizational-independence, or
publication claim is made by this review.
