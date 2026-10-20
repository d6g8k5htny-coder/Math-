# C299 author record — negative partial-gradient ridge

Actual author: OpenAI/Codex delegated agent `/root/adapter_feasibility_c292`.
Root coordinates source ownership, review, final execution, publication and
custody. This author has source exposure and is not a nonauthor reviewer of this
unit. Organizational independence 0; human mathematical reading is not claimed.
Scientific effect NONE.

The authorized bounded endpoint is one actual ridge `r : E d → V`, obtained from
the literal smooth function and negative definite restriction of its literal
Hessian. The same function must satisfy `r 0 = 0`, `ContDiffAt ℝ 2 r 0`, an
eventual vanishing equation for the actual restricted gradient, and the literal
differentiated Hessian equation. Reduced-Hessian positivity, uniform signs,
concavity, tubes, paths, quotient transport and full closed-superlevel LPC are
outside this endpoint and remain open.

The direct ridge route replaces the prior orientation's self-adjoint congruence
proposal for this unit. The complete 6961-byte paper proposal was read from
Math-#487 comment 6292079965, along with relevant sections of its distinct paper
review and API follow-up 6292239804. The formal handoff is Main#419 comment
6292136858. An initial attempt to fetch that last comment from Math- returned
404; fetching its actual Main repository succeeded. No source-owner acceptance
was inferred from the paper publication. Root subsequently supplied the fresh
C299 claim and explicit authorization.

## Literal inputs and minimal dependency reuse

`INPUT_REUSE.json` records fresh byte hashes and copies of exactly the C293
`final-project` sources Lifetime, TorusTopology and MorseFiniteCritical. Their
copied compiled objects are bound to C293's successful final build receipt
`20261018T030043Z-build-MorseFiniteCritical-84e29842/RECEIPT.json`; every source
and object hash was freshly compared before copying. The copied files are read
only. This is development reuse, not a new dependency rebuild.

The relevant previously proved bridge is
`TorusMorseFinite.literal_hessian_eq_fderiv`. C293's finite critical-set theorem
is not reopened or reproved. The proof pattern for the restricted-block inverse
uses the existing finite-dimensional Riesz equivalence and injective-endomorphism
construction. It does not infer invertibility of a restriction from invertibility
of the full Hessian.

The pin is Mathlib `d13f23b723b8a846827a245b89c10fc7d3f11612`, Lean 4.34.1.
Pinned `ImplicitContDiff.lean` was fully read; its
`ContDiffAt.implicitFunction`, value, eventual equation, derivative and C2
regularity APIs are actual library declarations. The proof instantiates them
with the actual partial gradient instead of assuming its inverse certificate.

## Construction and hypotheses

For a subspace `V`, restrict ambient continuous covectors with the continuous
linear map obtained by composition with `V.subtypeL`. Define

`G(w,v) = (Df(p+w+v))|V`.

Its derivative in `v` at zero is the literal Hessian restricted to `V × V`.
If that block annihilates `v`, evaluating the resulting covector on `v`
contradicts strict negativity unless `v = 0`. Riesz identifies the continuous
dual with `V`; injectivity of a finite-dimensional endomorphism then constructs
the exact continuous linear equivalence used by IFT.

The all-finite literal smoothness predicate supplies C3 of `f`, hence C2 of
`G`, and IFT produces a C2 ridge. Criticality supplies `G(0,0)=0`. Differentiating
the eventual ridge equation gives the Hessian equation; no differentiation of
an unproved identity is used.

The ambient parameter is intentional. Restricting it later to the actual
complementary positive subspace gives the paper's `W → V` ridge. This first
unit needs neither a complement nor its positivity, so it assumes neither.
No Hessian-orthogonality, dimension positivity, sphere nonemptiness, periodicity,
global compactness, critical-value distinctness, stochastic input, numerical
normalizer or limit interchange is introduced. The zero subspace is covered by
the same injectivity/finite-dimensional construction.

## Execution discipline and initial state

`run_lean.py` writes the exact candidate source snapshot and a
`PRE_EXECUTION_CONTRACT.json` before each Lean spawn. The record includes source,
runtime, source-bound reused objects, pinned dependency revisions, command,
working directory, environment policy, resource caps and expected result.
The author cap is 600 seconds, two threads and Lean's 4096 MB option. Lean/Lake
and loader override keys are stripped before setting the explicit import path.
Shared caches are read only; no package update is permitted.

Candidate 1 has SHA256
`729b57030c9d595b6ee9061b7cc6c730a6de713044ab0f7509637ed029771375`.
Its bounded compile began at 2026-10-20T13:48:43Z in author run
`20261020T134843Z-89c13163`. At the time of this initial note no terminal result
has been observed. No compilation, kernel, control, final review or scientific
success is claimed here. Every actual failed attempt and full stream is retained
under the author execution directory.

## Additive terminal record and candidate 2

Candidate 1 terminated at 2026-10-20T13:58:43.933989Z with return code -15
after the contracted 600 seconds (observed 600.041933625 seconds). Both streams
were empty, the source was unchanged, and no object was produced. The retained
one-second native process sample at 13:52:03Z shows 791 of 792 samples in
`read()` during module/IR import. This is an import capability timeout, with no
observed proof elaboration verdict. Its receipt and raw sample remain intact.

After that receipt, and under Root's explicit permission, the author made only
the two source-reading repairs also independently identified by the reviewer:
transport the derivative base point using `map_zero` and `add_zero`, and use
explicit simplification instead of `rfl` to identify the negative derivative
block. These were not falsely attributed to compiler diagnostics.

Candidate 2 is 8149 bytes, SHA256
`b3c22e590f761953ba322ad2903978e3982179204ad5c4a166dffc5fa1558322`.
`CANDIDATE2_FREEZE.json`, `CANDIDATE2.diff` and its separate source snapshot bind
the exact changes. No public binder or conclusion changed; the module still has
four definitions and five theorems. No candidate-2 Lean execution or native
retry has occurred at this record. Candidate 2 is held unchanged for the next
source-bound execution route coordinated by Root.

## Additive hosted failure and candidate 3

Root supplied the actual hosted development result from run `39438543701`,
head prefix `c8d66bde`, and authorized repairs only in C299. The author fully
read `hosted-development1/extracted/build-CriticalRidge.stdout` and its receipt.
The build reached elaboration and failed with exit code 1 after 17.856697
seconds, without a timeout or new object. The three fresh upstream builds had
produced the same source-bound object hashes recorded in the development reuse
manifest. This hosted execution belongs to its actual executor; it is not
claimed as a local author run.

The complete 4227-byte diagnostic stream has SHA256
`6287a34ab9f1cfb469f5152c2e523c7f3f1bbc9ab7573f7f01e924120b10877a`.
It identifies the initial concrete nested-operator instance/unification failure
in the direct `compL.flip` construction of `restrictCovector`; subsequent
evaluation/calculus declarations also failed. Independent diagnostics identify
the obsolete `ContinuousLinearMap.zero_apply` name, insufficient unfolding of
the selected ridge/product zero in the eventual IFT equation, and reversed
arguments to `hasFDerivAt_const` (whose actual pinned order is constant, point).
The final diagnostic that a declaration uses `sorry` is elaborator recovery
from failed declarations. The submitted source itself contains no `sorry`,
`admit` or `axiom`.

The author used the systematic-debugging workflow: full actual diagnostics
first, then the pinned construction and derivative APIs, then a bounded repair.
Relevant actual reads include `Operator/Bilinear.lean`'s
`Continuous.clm_comp_const` and composition map, `ContDiff/Comp.lean`'s
`ContDiff.clm_comp`, `FDeriv/CompCLM.lean`'s `HasFDerivAt.clm_comp`,
`FDeriv/Const.lean:115`, and the actual IFT equations.

Candidate 3 constructs the same restriction map directly as a continuous
linear map with `toFun ℓ := ℓ.comp V.subtypeL`, pointwise linearity, and the
existing continuity theorem. Its calculus proofs use the library's direct
composition rules with the constant inclusion. This avoids the failing
polymorphic `flip` term and does not change the mathematical map. It also makes
the three independent diagnostic corrections described above. No hypothesis,
conclusion, public binder, declaration name or declaration count changed.

Candidate 3 is 8485 bytes, SHA256
`2a93240fa5034544a1dbcf5ec0a10ab11be1ca5d05f60b4df0e2663fa769f442`.
Its exact source snapshot, full diff and failure bindings are retained in
`CANDIDATE3_FREEZE.json` and `CANDIDATE3.diff`. It was frozen at
2026-10-20T14:30:52.127723Z and sent directly to the designated nonauthor
reviewer, as Root requested. No candidate-3 compilation, native retry or
external mutation was performed by this author. Elaboration of this repair
remains to be tested by the separately coordinated hosted route.


## Additive second hosted failure and candidate 4

The author read the complete candidate-3 diagnostic stream and actual receipt
from hosted run `39440510935`. Elaboration failed with exit code 1 after
12.745656 seconds, without timeout or a new object. The 3059-byte
stdout has SHA256 `a784390b5d21162fef912eb6fefc803a57dfd4ca887a8d2402ce453b275746d6`.
The raw hosted failure, original candidate-3 snapshot and its earlier records
remain unchanged. This was the separate hosted executor's run, not an author
local run.

The residual derivative proof used a bilinear composition rule with a constant
second argument. Ordinary `convert` generated dependent equalities for product
group/module/topology instances and a separate derivative equality; the next
tactics did not discharge all of them. Candidate 4 removes that unnecessary
bilinear expansion: the already-defined continuous linear restriction map is
differentiated directly and composed with the existing chain derivative.

The two affected declarations now use declaration-local
`backward.isDefEq.respectTransparency false`, an elaboration setting used by
the pinned Mathlib itself at `Analysis/Calculus/FDeriv/Congr.lean:222` and
`Analysis/Calculus/FDeriv/Basic.lean:517`. It permits the elaborator to unfold
definitionally equal concrete instances; it introduces no premise or axiom and
does not relax kernel checking. The option is not installed globally. The
actual constant restriction derivative API is
`ContinuousLinearMap.hasFDerivAt` in `FDeriv/Linear.lean:57`, followed by the
chain rule `HasFDerivAt.comp` in `FDeriv/Comp.lean:107`.

The IFT's eventual equality is normalized explicitly to the selected ridge and
actual product zero, then composed pointwise with `hG0`. The final graph
base-point proof explicitly rewrites `hr0` before using the known derivative.
These changes address the actual displayed equality/instance mismatches; they
do not replace the IFT or differentiated identity. The unused-simp diagnostic
disappears with the removed bilinear proof rather than a disabled linter.

Candidate 4 was frozen at `2026-10-20T14:51:33.461601+00:00`: 8664 bytes,
SHA256 `f3a515bd0a984c8a8affbfc79f4768e7a357b7798eee8990a5a34adbdcf6f0f7`. Exact source-signature text equality was checked for all nine
public declarations against candidate 3. The snapshot, full diff and actual
failure identities are recorded in `CANDIDATE4_FREEZE.json`. No Lean execution,
native retry, remote write, compile success or kernel success is claimed for
this candidate. The actual next hosted check remains necessary.


## Additive third hosted failure and candidate 5

Actual hosted run `39443604910` tested candidate 4 and failed at elaboration
with exit code 1 after 17.057773 seconds. No object was produced;
this was not a wall-clock timeout. The complete 3405-byte diagnostic stdout
has SHA256 `dd5794a1cb3365b1f4a25e170496e0b697b5b45f4f6a8b5cd9350fbde1946351`. The author read the complete
stream and receipt. The direct restriction-CLM chain application still failed
to align its generalized and normed instances. The declaration-local broad
transparency setting also caused new typeclass/definitional-reduction heartbeat
failures. The earlier source review was a source verdict and did not establish
elaboration. All candidate-4 source, review and failure evidence is retained.

Candidate 5 removes both broad transparency settings, without raising any
resource cap. The restricted-gradient derivative returns to the candidate-3
bilinear composition application, which actually elaborated. Its conversion
now uses the pinned `convert!` default-transparency congruence strategy and
discharges every generated goal: definitional instance equalities by `rfl`,
and the derivative-map equality by removing the zero composite then
pointwise extensionality. This is a narrow conversion site, not a module or
declaration-wide transparency change. Pinned `Tactic/Convert.lean` documents
that `convert!` uses default rather than reducible post-transparency, and
`ImplicitContDiff.lean:44` uses this tactic for product derivative conversion.

The graph chain rule now names its actual function and derivative arguments
explicitly and supplies proof holes in the exact types expected by the normed
chain-rule API. Each hole converts the already-proved derivative; the graph
base point follows from `Prod.ext rfl hr0`. This avoids passing a generalized
`HasFDerivAt` value directly into an unresolved normed application. The IFT
eventual-equality normalization from candidate 4 remains.

Candidate 5 was frozen at `2026-10-20T15:02:54.565085+00:00`: 8966 bytes,
SHA256 `669b94138531a694f134d24ee9d34ecf6cda5ccec125e2bac279f9e49e1a4aae`. All nine public declaration-signature texts are exactly
unchanged. The full diff, source snapshot, and actual preceding failure
identities are in `CANDIDATE5_FREEZE.json`. No native retry, Lean execution,
external mutation, cap increase, compile PASS or kernel PASS is claimed for
this candidate. This is a bounded uncompiled repair; if the separately
coordinated hosted attempt still fails, the current formal unit remains HOLD
at its actual finite disposition rather than being presented as complete.


## Additive fourth hosted failure and candidate 6

The author read the full hosted-development4 diagnostic stdout and receipt.
Candidate 5 failed with exit code 1 after 21.013988 seconds, with
no new object or wall-clock timeout. The complete 1601-byte stdout has SHA256
`1cc98e9540608d20c0f1a9b66a0fdb3fcb4b5910ec671da7b1e8624c508d4d7c`. It reports one remaining derivative
value equality (`case hr`) and two unreachable-tactic warnings promoted to
errors. There is no reported internal typeclass or reduction resource limit
in this attempt. Prior sources and all actual failures remain preserved.

The remaining `hr` branch is explained by the actual pinned
`ContinuousLinearMap.prod_ext`, registered as an extensionality theorem at
`Topology/Algebra/Module/ContinuousLinearMap/PiProd.lean:342`: product-domain
extensionality generates left and right inclusion cases. The prior sequential
`ext q z; rfl` closed only the first. Candidate 6 instead applies
`ContinuousLinearMap.ext` explicitly twice, first to one actual product
argument and then one covector argument. The resulting value equality reduces
by the definitions of restriction, composition, flip and `compL`; no product
branch is left by the generic extensionality tactic. Actual definitions and
value equations were read in `ContinuousLinearMap/Basic.lean:460-489` and
`Analysis/Normed/Operator/Bilinear.lean:146-160,304-312`.

The two trailing `<;> rfl` calls at the final graph conversion were removed
exactly where the compiler reported them unreachable. No linter was disabled;
no option, cap, new theorem or new hypothesis was introduced.

Candidate 6 was frozen at `2026-10-20T15:15:17.859057+00:00`: 9053 bytes, SHA256
`9ff65416927182f6dad06646f04821b3af6bdd131740d93bf229354a81e19c38`. All nine public declaration-signature texts are exactly unchanged.
Its full diff and actual preceding failure bindings are in
`CANDIDATE6_FREEZE.json`, with a separate immutable source snapshot. This
source-only repair has no compilation or kernel verdict; no native retry or
external write was performed. The authorized final development attempt and
its actual evidence remain Root's responsibility.
