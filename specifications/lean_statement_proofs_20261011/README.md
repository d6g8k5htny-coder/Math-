# Lean statement proofs (`specifications/lean_statement_proofs_20261011`)

**Scientific effect: NONE.** Organizational-independence credit: 0 (Anthropic / Claude). Alignment
status of every statement proved here: **PENDING_INDEPENDENT_REVIEW**. No claim, premise, obligation
or disposition changes status because of anything in this directory.

## What this packet is

Kernel-checked Lean 4 proofs of statements that are *already registered* in the statement packet
[`specifications/lean_statements_20261010`](../lean_statements_20261010) (`REGISTER.json`, modules
`Specifications/{Field,Lifetime,Side24,RN,P15}.lean`). That packet holds `def … : Prop`
declarations and interface `structure`s and nothing stronger; this packet depends on it by path
(`lakefile.toml`, `[[require]] path = "../lean_statements_20261010"`) and never edits it.

Every theorem in the inventory has as its *type* a registered Prop constant applied to exactly the
theorem's own parameters:

```lean
theorem rhoStarBelowSixSevenths : UniversalLaw.Spec.P15.RhoStarBelowSixSevenths := …
theorem fullBlockCoverIff {X : Type} [Fintype X] [DecidableEq X] (F : RealizedData X) :
    UniversalLaw.Spec.P15.FullBlockCoverIff F := …
```

A theorem of the shape `theorem foo (h : extra) : P` or `theorem foo : P → P` or
`theorem foo (n : ℕ) : P (n + 1)` is **refused**: an extra hypothesis or a narrowed argument is a
finding about the statement (report it), never a theorem of it.

## What a green run establishes, and what it does not

| established by a green `check.py --execute` | not established |
|---|---|
| each inventoried theorem was accepted by the Lean kernel (`lake build`, replayed by `leanchecker`) at Lean `v4.34.1` (commit `5045d005…`), Mathlib `d13f23b7…`, against the statement modules whose SHA-256 the receipt records | that any informal Layer 0 claim is true, aligned with its Lean statement, reviewed or accepted |
| its transitive axioms are within `propext`, `Classical.choice`, `Quot.sound` (`#print axioms`, and Lean's `collectAxioms` on every constant the modules add) | anything about the statement's fidelity to its source: alignment is PENDING_INDEPENDENT_REVIEW and is written only by an independent reviewer |
| its type, after `forallTelescope`, is a registered Prop constant applied to exactly the telescope's variables (Lean's `ConstantInfo`, not source text), and Lean's inventory equals the lexical scan's | any change to `REGISTER.json`: the register's labels (`specified` for every statement of the statement packet) are untouched; a register row of kind `theorem` naming this packet is the statement packet maintainers' decision, not this gate's |
| no `sorry`, `axiom`, `native_decide`, `unsafe`, `opaque` or proof-written-as-`def` anywhere in the modules; `maxHeartbeats` above 400000 only with a justifying comment | a LANDING_CLAIMS disposition (`HOLD_WITH_DOMAIN`, `FAIL_CLOSED`, `EXACT_COUNTEREXAMPLE`, `REVIEWED_SCOPED`, `ENGINEERING_HOLD`): transcribed in the register, never derived here |
| the negative controls refused for the intended reasons (sorry via the axiom audit; a custom axiom; an unregistered type; a smuggled hypothesis and a `P → P` implication; a tightened false arithmetic statement rejected by Lean) | the parent theorems, the identification of interface structures with the informal objects, independence (credit 0), or any prize claim |

Vocabulary (docs/FORMAL_VERIFICATION.md): the source-mode summary says `formalization_status:
"proved"` (the label of a committed proof package); `kernel-checked` appears **only** in a run
receipt (`.lake/evidence/receipt.json`). On the evidence ladder a kernel-checked theorem is L5
*for that Prop*; the informal claim it serves keeps the ladder level and formal-progress label the
register gives it.

## Registered Props without a theorem here, and why

Inventory at this commit: 60 theorems, 59 of the 141 registered `def … : Prop` declarations (`TriangleNeedsThree`
is proved twice). The other 82 fall into the groups below. None is weakened, restated or relabelled: the register
keeps every one at `specified`, and a group's reason is a statement about what Mathlib and this packet can reach
today, not about the truth of the Prop.

| group | Props (names without `UniversalLaw.Spec.<Module>.`) | why no theorem here |
|---|---|---|
| P15 parametrised predicates | `IsRealizedFamily`, `IsGood`, `IsKDecomposable`, `IsGeneratorCover`, `IsPaletteFeasible`, `IsMinimalForbidden`, `IsTransversal`, `IsProperDownset` | predicates with free arguments, not closed statements: a theorem of their type would assert them for every argument, which is false (`IsGood F Finset.univ` fails for every realized family). They are the vocabulary of the other Props, not targets. |
| P15 full-price note, formerly listed here | — | the hazard interpolation `CoordinatewiseConcavity`, `HazardProductBound` (F6), `HazardPhiBound` (F7), `FullGroundPriceBound` (F8), `FullGroundBudgetIff`, the full budget `LocalPriceBoundFull` (F12), `FullTransformedPriceBudget` (F2) and the enclosure `RhoStarEnclosure` (F3) have theorems in `P15Interpolation` since round 3: the concavity from the one-coordinate split of `μ_p(A)` (affine in `e^{-t_i}`, coefficients `0 ≤ S_in ≤ S_out` for a downset) and `concaveOn_of_deriv2_nonpos`, not from the undisplayed derivative formulas (F4)-(F5), which stay unspecified; (F6)-(F8), (F12) and (F2) as their consequences through `CapacityWorstCase`, `GlobalAssemblyHazard` and `FullBlockCoverIff`; (F3) by `Real.exp_bound` at degrees 26 and 16 compared by `norm_num` against the 20-digit rationals, a different certificate from the source's `full_price.py` procedure, which stays unspecified. Every theorem-shaped Prop of claim `p15-full-price` now has a theorem; the claim stays `specified`. |
| Side24 derivative bounds | `IsUnitTuple` (predicate), `DerivativePairingBound`, `DerivativeBoundAtLeastOne`, `DerivativeBoundAtZero` | explicit `iteratedFDeriv ℝ q (fun x => exp (-‖x‖² / 2))` in arbitrary unit directions: Mathlib has no closed form for the iterated Fréchet derivatives of a Gaussian (the Hermite expansion behind the pairing sums); the arithmetic of the pairing sums is kernel-proved on main (`UniversalLaw.Side24.pairing_sum_six`, …). |
| Side24 lattice sums | `ThetaSummable`, `LatticeImageSumBound`, `ImageBound` | summability of `n ↦ exp (-‖z + 24 n‖² / 2)` over `Fin d → ℤ` and the explicit tail `≤ 1458 e^{-288}`: Gaussian-decay summability over `ℤ^d` and a shell count; Mathlib's Jacobi-theta results are one-dimensional. |
| Side24 covariance and density | `NegDefCone` (predicate), `ReferenceOddAndPinBlocks`, `CovarianceOrdering`, `EntrywiseCovarianceBound`, `ReferenceCovarianceLowerBound`, `DensityComparison`, `IntegrandRatioBounds`, `ReferencePinDensityProduct` | built on the derivative contractions above (`jointCov`, `gradCov`, `pinCov`, `derivContraction`); the matrix arithmetic is kernel-proved on main, the evaluation of the Fréchet derivatives is not available. |
| Side24 interface statements | `ConeMomentD1Identity`, `ConeMomentD2Identity`, `TraceMoments`, `RayleighSquareLaw` (over `ConeMomentInterface`); `CoefficientEnclosure`, `ReferenceComparison` (over `PeriodicCoefficientInterface`) | quantify over an interface whose fields are given, not constructed: the Gaussian moment identities need the conditional law `A_u \| V_u = 0` built in Mathlib's Gaussian measure theory; the enclosure needs the numerical pipeline. `ConeMomentD2Algebra`, `ElementaryConeIntegral` and `ReferenceCoefficientIdentity` (proved) are the parts that need neither. |
| RN beyond (N1)-(N5), Lifetime, Field | the 22 RN Props other than `HolderCountBoundN1`, `HolderConsequenceN2`, `ConditionalMeanIdentityN3`, `UniformCounterexampleN4`, `ExponentialTailLayerCakeN5`; all 21 Lifetime and 10 Field Props | statements about the Gaussian field through interface structures (`PinnedLawInterface`, `GaussianFieldInterface`, …): the D5 window bounds, the dimension lift, the Palm and Fourier routes, the remote-collision and annulus-bridge bounds, the parent Theorems A/B/C, the planar elder gap, the remainder (R1), and the critical-point predicates. These are the programme's open research claims: a proof would be the research result itself, not a formalisation of an existing argument, and the interfaces do not carry the Kac–Rice data the informal arguments use. |

The register (`../lean_statements_20261010/REGISTER.json`) says the same per claim row in its `not_established` and
`next_step` fields; this table is the packet-side summary and decides nothing.

## Layout

```
README.md  SCOPE.md  check.py  test_check.py  replay.sh
lakefile.toml  lean-toolchain  lake-manifest.json  SpecificationProofs.lean
SpecificationProofs/<Module>.lean      namespace UniversalLaw.Proofs.<Module>; P15 is split by theme into
                                       P15Elementary, P15Structure, P15Hazard, P15Covers, P15Budget,
                                       P15Interpolation (in import order), Side24Elementary and RNProbability
                                       are one each
```

Rules for every module (enforced by `check.py`, see its module docstring):

* imports only `Specifications.<Module>`, Mathlib and sibling proof modules `SpecificationProofs.<Module>` of
  this packet (Lean forbids cycles; the axiom audit is transitive, so a reused `Aux` lemma is audited where it
  is used as well as where it is proved), nothing else;
* exactly one top-level `namespace UniversalLaw.Proofs.<Module>`; helpers are `private` or live under
  a `…Aux` namespace and are not inventory items;
* every non-aux theorem's docstring carries `Proves:` (naming the registered Prop), `Method:` and
  `Does not establish:`;
* no `sorry`, `admit`, `axiom`, `native_decide`, `unsafe`, `opaque`, `partial`, `implemented_by`,
  `extern`, `include`, `_root_`, metaprogramming commands, `#` commands, `debug.*`/`bootstrap.*`
  options or `autoImplicit`; declaration and scope keywords start their own line.

## How to run

```bash
export PATH="$HOME/.elan/bin:$PATH"
P=specifications/lean_statement_proofs_20261011
python3 -B -S $P/check.py                 # source mode (git identity, lexical scan, inventory); add --allow-dirty locally
python3 -B -S $P/test_check.py            # unit tests; the LeanHelpers class runs only when `lake` is on PATH
python3 -B -O -S $P/test_check.py
python3 -B -S $P/check.py --execute       # fresh lake build, leanchecker, #check/#print axioms, environment audit, controls, receipt
bash $P/replay.sh [--allow-dirty]         # all of the above in order
```

Compile one module while writing it: `cd $P && lake env lean -DwarningAsError=true
SpecificationProofs/<Family>.lean`. The gate refuses warnings in proof modules in the build log.
Never run `lake update`; `.lake/packages` may be a symlink to a prebuilt dependency tree locally (the
receipt records `packages_dir`), and each package directory must be at its locked revision.
`lakefile.toml` is pinned byte-exactly (Lake would accept a `moreLeanArgs = ["-Ddebug.skipKernelTC=true"]`
line that no "contains these lines" check sees).

Resource needs of `--execute`: the `leanchecker` replay of the Mathlib-importing environment holds
roughly 14 GB of anonymous memory (it was memcg-killed at 13.5 GB RSS on a shared 16 GB machine; on
an idle one it finishes in about a minute), the fresh `lake build` of the packet takes a few minutes
once the Mathlib oleans are present. The hosted runner (`ubuntu-latest`) is where the first receipt
for a commit exists. On a smaller machine `LEAN_PROOF_SKIP_LEANCHECKER=1 python3 -B -S $P/check.py
--execute --allow-dirty` runs every other stage; the variable is honoured only together with
`--allow-dirty` (never in CI), the receipt then reads `leanchecker: "SKIPPED_LOCAL_ONLY"` and, like
every `--allow-dirty` receipt, is not evidence about any commit.

CI: [`.github/workflows/lean-specification-proofs.yml`](../../.github/workflows/lean-specification-proofs.yml)
(`leanprover/lean-action`, `use-mathlib-cache: 'true'`; the statement packet, a path dependency,
builds from source) uploads `.lake/evidence/` as an artifact. A green workflow is a run, not a review.

## Receipt

`.lake/evidence/receipt.json` (`LEAN-PROOF-RECEIPT-20261011-v1`): `checked_commit`, `worktree`
(`CLEAN` or `UNVERIFIED` with `--allow-dirty`, in which case the receipt is not evidence about any
commit), the Lean version line, dependency revisions, SHA-256 of the register, the statement modules
and the proof modules, the theorem inventory (name, module, registered Prop, claim ids it serves,
axioms), the environment-audit class counts, the negative-control outcomes and the log digests.
`theorems.json` beside it carries the elaborated signatures.
