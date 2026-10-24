# C299 nonauthor source review — candidate 1

Actual reviewer: OpenAI Codex delegated agent `/root/c299_nonauthor_review`, for root chat `01a0bbb5-2fcb-77f0-b78b-4d220ddd7ab2`, acting for Dylan Roy. Native review checkpoint: 2026-10-20 13:53:34 UTC.

**Preliminary disposition: the mathematical statement and reconstructed argument are sound at the requested finite scope; two likely elaboration defects require resolution. Formal execution, kernel checks, complete declaration/axiom census and negative-control results are unconfirmed. This is not final formal acceptance.**

I did not author candidate 1, provide a proposed implementation, edit an author source, or execute Lean, a compiler, a mathematical program or project tests. After reading the frozen candidate, I sent source-derived findings to root. This report adds independent proof reconstruction and adversarial analysis as review. Source exposed, same provider, organizational independence credit 0, blind review 0, human review 0. No human review by Dylan is claimed. Scientific effect NONE.

## Exact reviewed object

- Author: `/root/adapter_feasibility_c292`.
- Module: `project/CriticalRidge.lean`, 7,922 bytes, SHA-256 `729b57030c9d595b6ee9061b7cc6c730a6de713044ab0f7509637ed029771375`.
- Frozen author snapshot: `execution/author/source-attempts/729b57030c9d595b6ee9061b7cc6c730a6de713044ab0f7509637ed029771375.lean`.
- I freshly hashed both the working file and the frozen snapshot; both matched that identity. This review applies to those bytes, regardless of subsequent changes to the working file.
- Complete module read: lines 1–180. Its visible source declares four definitions and five theorems, nine public declarations in total. This textual count is not a complete compiled environment census.
- Planned scope and provenance read: complete `PLAN.md`, `execution/author/INPUT_REUSE.json`, `execution/author/AUTHOR_NOTES.md`, and the candidate's `PRE_EXECUTION_CONTRACT.json` and `START.json`.

The authorized endpoint is one function `r : E d → V`, derived from literal `IsSmooth d f`, literal `IsCriticalPoint d f p` and strict negativity of the actual Hessian on each nonzero vector of `V`, satisfying all four conclusions together:

1. `r 0 = 0`.
2. `ContDiffAt ℝ 2 r 0`.
3. On one neighborhood of ambient zero, for every `z : V`, the actual derivative of `f` at `p + w + r w` vanishes on `z`.
4. For every ambient `w` and every `z : V`, the actual literal Hessian satisfies `H(w + Dr(0)w, z) = 0`.

The candidate states exactly this endpoint. In particular, the neighborhood in conclusion 3 precedes the universal quantifier over `z`; it is not a collection of direction-dependent neighborhoods. The same selected `r` satisfies all four conclusions. No input is a ridge, chart, inverse certificate, LPC premise or finite event list.

## Source-derived findings requiring follow-up

These are probable elaboration failures identified by reading the pinned signatures and candidate syntax. I have not observed compiler diagnostics for them.

**F1 — base point of the chain rule, candidate line 113.** The preceding `hDp` is a derivative assertion at `p`. The argument `hadd` differentiates `q ↦ p + ridgeAddition V q` at zero. Pinned `HasFDerivAt.comp` requires the outer derivative at the inner function's actual value, here `p + ridgeAddition V 0`. The candidate constructs `hDp.comp (0 : E d × V) hadd` before normalizing that base point. In a general real Euclidean space, the equality of this point with `p` uses `map_zero` and `add_zero`; it is not generally definitional equality. The following `simpa` cannot repair a type mismatch that occurs while constructing `hcomp`. The mathematical chain rule is valid, but the source should be checked at this exact line.

**F2 — restricted block identity, candidate lines 137–141.** After substituting `hDG.fderiv` and applying extensionality, `ridgeAddition V (0,v)` expands to ambient `0 + (v : E d)`, whereas `negativeHessianBlock` uses `(v : E d)`. The candidate closes by `rfl`; the additive identity is generally propositional. This is another likely elaboration defect, not an objection to the block identity itself.

Both findings were relayed to root without editing author code or supplying a proof patch. Any changed candidate needs an exact successor hash and assessment of the actual changes. A compiler result may confirm or disprove these predicted defects; this preliminary record must retain the distinction.

## Independent reconstruction of the argument

Write `i : V → E d` for the actual submodule inclusion, `R` for restriction of ambient continuous covectors along `i`, and `A(w,v) = w + i(v)`. The candidate defines the covector-valued map

`G(w,v) = R(Df(p + A(w,v)))`.

All three structural maps are continuous linear maps. The literal `IsSmooth` hypothesis supplies C3 regularity of `f`, hence C2 regularity of its derivative. Composing with the affine translation and with `R` gives C2 regularity of `G`. This uses an actual extra derivative; it does not attempt to obtain a C2 implicit ridge from only C2 regularity of `f`.

At zero the derivative of `G` is

`DG(0)[w,v](z) = D(Df)(p)[w + i(v)](i(z))`.

The already established C293 identity `literal_hessian_eq_fderiv` identifies this with the literal second iterated derivative used by `Lifetime.hessian`. Restricting to the second product input gives the actual block

`C(v)(z) = H(i(v), i(z))`.

If `C(v) = 0`, evaluation at `v` gives `H(i(v),i(v)) = 0`. Strict negativity forces `i(v) = 0`, and injectivity of subtype inclusion forces `v = 0`. Linearity turns this kernel statement into injectivity of `C`. The finite-dimensional real inner-product space `V` has the Riesz continuous equivalence `J : V ≃L[ℝ] V*`. Consequently `J⁻¹ ∘ C` is an injective endomorphism of `V`, hence a linear equivalence with continuous inverse. Composing it with `J` constructs the precise witness to `C.IsInvertible`. The source does not infer invertibility of a restricted block from invertibility of the ambient Hessian.

Criticality is used to obtain `G(0,0)=0`. The pinned product-domain implicit-function theorem then selects one total function `r : E d → V`, with `r(0)=0`, C2 regularity at zero, and the local equation `G(w,r(w))=0`. The theorem guarantees a local equation and local regularity; the candidate does not claim that its total extension is globally continuous or globally solves the equation.

The derivative of `w ↦ (w,r(w))` at zero is `w ↦ (w,Dr(0)w)`. On a neighborhood the composite `G(w,r(w))` equals the zero covector-valued function. Thus its derivative is zero. The chain rule and uniqueness of derivatives give

`DG(0) ∘ (id, Dr(0)) = 0`.

Evaluating this equality at arbitrary `w` and then arbitrary `z` gives precisely `H(w+i(Dr(0)w),i(z))=0`. Candidate lines 154–178 differentiate an actual eventual equality with regularity evidence, not an unproved identity or merely the base-point equation.

The restricted-block injectivity proof does not need Hessian symmetry. Symmetry and a complementary positive subspace will matter in the later reduced-positivity argument; neither is smuggled into this finite endpoint. The ambient parameter is a valid stronger parameterization for later restriction to a positive complement.

## Independent adversarial analysis

All examples in this section are hand-derived paper checks, not executed fixtures or Lean results.

**Nonzero cross block and the ambient parameter.** Let `f(x,y)=x²+2cxy−y²`, `p=(0,0)`, and let `V` be the vertical axis. For arbitrary real `c`, its Hessian matrix is `[[2,2c],[2c,−2]]`, and its restriction to `V` is strictly negative. At ambient parameter `w=(a,b)`, the partial-gradient equation requires the correction

`r(a,b) = (0, ca−b)`.

Then `w+r(w)=(a,ca)` and the derivative in every vertical direction is zero. The differentiated expression is also `(a,ca)`, and `H((a,ca),(0,t))=2cat−2cat=0`. Thus the endpoint handles a nonzero cross block. A spurious implementation that used the paper's restricted-parameter correction `(0,ca)` for every ambient `w` would fail when `b≠0`; the candidate's implicit construction avoids that error.

**An actually nonorthogonal complement.** With `f(x,y)=x²−y²`, the same negative vertical `V` can be complemented by `W=span(1,k)` for `0<|k|<1`. This `W` is positive for the Hessian and is neither Euclidean-orthogonal nor Hessian-orthogonal to `V`. The ambient ridge is `r(a,b)=(0,−b)`, so restricting it to `w=(t,kt)` gives correction `(0,−kt)` and `w+r(w)=(t,0)`. The differentiated restricted-gradient equation still holds. No orthogonality premise is needed.

**Zero negative subspace.** For `V={0}`, both `V` and its continuous dual are zero spaces. There is one correction function, identically zero. The strict-negative assumption is vacuous, the block is the unique invertible map between zero spaces, and both universal equations only evaluate on `z=0`. The construction never uses a nonempty unit sphere, a positive dimension or a nonzero vector chosen from `V`. This also covers ambient dimension zero.

**Full negative subspace.** If `V=E d` and `f(x)=−‖x‖²` at zero, one may take `r(w)=−w`, so `w+r(w)=0` and `w+Dr(0)w=0`. This checks the sign and explains why an ambient-parameter ridge need not be an embedded graph parameterization of positive dimension.

**Removing strict negativity is invalid even for a smooth critical function.** Let `f(x,y)=xy`, `p=0`, and `V` the vertical axis. The restricted Hessian is zero and is therefore nonpositive, while the full Hessian is nondegenerate. At any corrected point `(a,b+r(a,b))`, the vertical derivative is `a`, independently of the correction. It cannot vanish for every ambient parameter near zero. This shows why nonpositivity, full-Hessian nondegeneracy, or smooth criticality cannot replace the actual strict-negative block premise.

**Removing criticality is invalid.** On the line let `f(y)=y−y²`, `p=0`, and `V=ℝ`. The Hessian is strictly negative, but `Df(0)=1`. A continuous ridge with `r(0)=0` and the claimed eventual vanishing equation would in particular force the equation at zero, which is impossible. This is a direct test of the role of `hcritical`, rather than of the block-invertibility sublemma, which legitimately does not need criticality.

**The smoothness predicate is substantive.** Literal criticality alone is an equation about total `fderiv`, which can be zero at a nondifferentiable point. The candidate does not use that equation as a substitute for differentiability: it separately obtains the derivative and C2 regularity of `G` from `hsmooth`. Dropping smoothness is not justified by the source argument.

**Local versus global scope.** The eventual equation and C2-at-zero conclusion do not provide a global smooth ridge, uniqueness away from the chosen neighborhood, uniform Hessian signs, a superlevel path or a neighborhood basis. No such strengthening is present in the final signature.

## Import, source identity and verification boundaries

The three copied local source hashes were independently measured and matched `INPUT_REUSE.json`:

| Source | Bytes | SHA-256 |
|---|---:|---|
| `Lifetime.lean` | 51383 | `90f4892608e953ecc696bb32ea159d1c178ceb8a1c6edfd11acfceb14af462c6` |
| `TorusTopology.lean` | 12257 | `ddb145b3f791c181d4f2a51e54e711937297bd6476ba55bcd5252b7ddb57cfe1` |
| `MorseFiniteCritical.lean` | 9445 | `95a660134eda49eecfe6181884bd23b4e4ca210e228d2463de29e5f821df047b` |

I also independently hashed the three reused author-build objects; they match the declared historical objects: Lifetime `b3e14c2951b452222ca0c7b1448458cf785225971da704e4e3e6f0cc93107da4`, TorusTopology `ccb13e9469d55da8b5202706a1f013fa7a2755b2184542b8a0534f722d993125`, MorseFiniteCritical `34ff2a9ed529609dd48a22204b8eacc66eeb943805e2d6e8dee4481cde8ef4e2`.

I read the complete cited C293 receipt `final-runs/20261018T030043Z-build-MorseFiniteCritical-84e29842/RECEIPT.json`. It binds those sources and objects and records return code 0 for that historical build. It explicitly reused dependency metadata/hash evidence and was not a fresh replay of the imported Mathlib closure. Current equality of copied bytes supports the disclosed development reuse; it does not become a fresh dependency build or a C299 kernel result.

The local Mathlib checkout reports commit `d13f23b723b8a846827a245b89c10fc7d3f11612`. I fully read its 103-line `ImplicitContDiff.lean`, freshly hashed as `308611fd7f41cbf58cf72a284a5324b27a76088672b2fc148129eec5e064368f`, agreeing with the paper API binding. I selected and read the exact signatures for `ContinuousLinearMap.IsInvertible`, `LinearEquiv.ofInjectiveEndo`, `contDiff_succ_iff_fderiv`, `HasFDerivAt.comp`, and `HasFDerivAt.congr_of_eventuallyEq`. This establishes source compatibility of the invoked interfaces; it is not a complete mathematical reconstruction of every imported library theorem or a full clean-worktree check.

The module visibly contains no new `axiom`, `sorry` or `admit`. A source text scan cannot substitute for a compiled local-origin declaration census: private/generated declarations and their transitive axioms still need the planned audit. The nine visible public declarations are not the census denominator. Expected allowed standard axioms are `propext`, `Classical.choice` and `Quot.sound`; whether the actual compiled closure satisfies that restriction is unconfirmed here.

The candidate's observed author execution record is a pre-execution contract and a start receipt for run `20261020T134843Z-89c13163`, with a 600-second cap, two threads and Lean's 4096 MB option. I have not run or certified that invocation, inspected a successful terminal receipt, or treated elapsed time/empty streams as evidence of either proof success or mathematical failure. Fresh final local-module builds, named-module kernel checks, complete census, omitted-premise controls and exact hosted artifact binding remain separate acceptance work.

An omitted-premise fixture must fail because the omitted hypothesis is genuinely unavailable at the intended application, with the expected diagnostic bound to exact source and actual output. Import, resource or syntax failure cannot satisfy that control. The paper counterexamples above show that the endpoint's criticality and strict negativity requirements are substantive; they do not establish the effectiveness of any not-yet-run fixture.

## Source-paper custody qualification

I read the complete paper publication's proposal, prior mathematical review and freeze, and the complete API report plus its freeze, negative evidence and additive extraction clarification. I also read root's `SOURCE_PAPER_IDENTITIES.json` and `sources/EXTRACTION_NEGATIVE.json`.

The public proposal's directly fenced body is 6960 bytes, SHA-256 `6d9e532505307c5f115701b693046d8ebba6fea913a07f43fd8ecee6e3516558`. Appending exactly one LF reconstructs the declared 6961-byte author file, SHA-256 `96a13c7e14e781220915e927caa34ba9ca94e26bd12bb7d53e7459b759c9b141`. Raw fenced equality to that author file is false. The prior 20646-byte review (`de928866de9d077a980bc9c42744bfe557c2b6ff7c16b6c840449f4b21542657`) and 17303-byte API report (`1cc33f6368c628702dd447e1b20d8506deaf1b6132712a2feb13aaee6a02c4ae`) match directly. Root's initial failed extraction and duplicate-candidate counting error remain historical negative evidence.

Separately, the API audit's 44 stored excerpts omit exactly one terminal LF relative to line-ending-preserving selected source ranges. Its selected-line text comparisons are qualified by that convention; raw source-range byte equality remains false. Neither LF distinction changes the mathematical content, and neither is a compiler result.

## Remaining scope

Reduced-Hessian positivity, uniform signs, fiber concavity, tubes and literal paths, an arbitrarily small path-connected neighborhood basis, Euclidean all-point assembly, actual quotient-superlevel transport and C294's exact `hclosedLPC` discharge remain OPEN. Full ordinary-bar correspondence, elder/once-counting, exhaustive finite bars, field-first sampling, all-small-bars and regional-collision obligations remain OPEN. No scientific claim or independent-review gate is promoted by this preliminary review.

Proceed with the finite unit only after the two source-level elaboration concerns and the actual formal verification results are resolved at exact candidate identities. Full research goal remains ACTIVE_UNMET.
