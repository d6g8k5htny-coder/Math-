# Constructed ridge, literal rectangle boundary, and attained graph path

26 October 2026. Production source: `/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025/AdaptiveFoldBoundaryPath.lean`, 426 lines, 20,469 UTF-8 bytes. Final SHA256 `b3a196c31c0c7957119907ea864c33b937d1a783bc7109390d3ca24a644e0570`. Final compiled object: `build/AdaptiveFoldBoundaryPath.olean`, 1,348,480 bytes, SHA256 `d11b26ae6ca4c288cbe9936e2e3d03c09e698f8c7a3bee1142f52ff652aef71d`.

## Binding scope and inherited evidence

Read the authoritative `SOURCE_ADAPTIVE_FOLD_BOUNDARY_PATH.md` and `_PLAN.md` before writing producer code, with frozen published commit `e72bc0e221745c496b36c32d08147a4be6695a62` supplied by root. Read the optional `/workspace/scratch/ridge-barrier-join-preflight/REPORT.md` and local workspace/repository instructions. Native activation is Math514/6408734279; checkpoint 06:00 and terminal 07:00 UTC. The implementation was completed ahead of both times. The source/plan commit identity and activation are transcribed from dispatch, not independently republished or rehashed.

Binding owner clarification in `/workspace/AGENTS.md`: completed, applicable verification is reusable; a new agent, session or handoff does not justify repeating unchanged checks; identify the affected obligation before further verification; pending provider-distinct process review does not erase established mathematical evidence. This qualification covers only the new module, its newly integrated helper declarations, and genuinely new controls. The completed 32-module/25-input evidence, qualified transverse-ridge source cut d2e29ed/SHA715b01c2 (22 written proofs), scalar barrier qualification, old Cap and H0/elder mathematics are reused unchanged. No old build, kernel replay, audit, control or source/object hash recheck was performed.

Canonical onboarding links carried forward, without asserting a new remote read:

- [15 October standing owner mandate](https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OWNER_MANDATE_20261015.md)
- [Standing owner delegation](https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OP-AUTONOMY-20260923-v2.1.md)

Producer ownership was confined to the one new production module and this scratch directory. Root owns registration, manifests, commits, publication and external review requests. No subagent was dispatched by this producer; the separately root-dispatched vertical-loss helper was coordinated directly. No shared configuration, old source, or `/workspace/main/AGENTS.md` was edited.

## Exact mathematical result

`StructuralRectangleData` is a finite Prop bundle containing the specified literal potential C4 regularity on open O, rectangle inclusion, positive R/c, nonnegative M0/M1/M2, Gy negativity, strict opposite vertical-boundary signs, center and Gx bounds, all four ordered coordinate D2G bounds, Hy bound, axial D2H lower bound, three other ordered D2H bounds, scalar curvature-error budget, two literal gradient pins and literal normalized potential gap. No ridge, ridge regularity, profile curvature, scalar barrier, path or elder certificate is a premise.

`profileSlopeSecond_error` proves both finite estimates:

```text
|profileSlopeSecond - D2H[ex,ex]|
  <= M2*(2*|z'|+|z'|^2)+M1*|z''|
  <= M2*(2*(M1/c)+(M1/c)^2)+M1*((M2/c)*(1+M1/c)^2).
```

It uses the qualified bilinear tangent expansion with both ordered mixed entries and the qualified vertical-vector expansion. There is no mixed-partial symmetry or product-norm identity. `exists_transverse_ridge_scalar_barrier` calls the qualified `exists_unique_c2_transverse_ridge_with_jets` once, strengthens its acceleration bound to the frozen scalar expression, transports z(+-1/2)=0 using the literal G pins and unique root, derives actual profileSlopeSecond >=1 from the finite error and axial budget, transports literal H pins and V gap, and calls `AdaptiveFoldScalar.scalarBarrier_of_secondDerivative` unchanged. The returned `RidgeScalarData` retains open U containing J, C2 z, actual unique interior root graph in O, structural bounds, full profile jets, curvature and scalar barrier. Endpoint derivatives remain full derivatives because of the imported open collar.

`quadratic_loss_of_second_derivative` proves the scalar quadratic loss by concavity of f(t)+(c/2)*(t-z)^2. `vertical_quadratic_loss` applies it to the actual potential slices and actual Vy/Gy partials. These are the two integrated frozen helper bodies described below.

`exists_transverse_ridge_boundary_path` obtains exactly one U,z from the analytic constructor and retains it throughout. From the additional M0/c<=R and 1<=(c/2)*(R-M0/c)^2 inputs it returns that same analytic result and `RectangleBoundaryPathData`, containing:

- actual vertical quadratic loss throughout J x [-R,R];
- the literal left box closed and M=(-1/2,0) in it;
- V S < V M, ceiling V<=V M on the whole box, and V<=V S on its frontier;
- V M+1/4<=V(3/2,z(3/2));
- a Path from M to that older point, its pointwise graph formula, V>=V S everywhere, and its exact midpoint equal to S=(1/2,0).

The frontier proof splits into the four actual box sides. The left side uses the old scalar left-arm barrier; the right side uses the transported root; each horizontal side loses at least 1, by the actual quadratic loss and new scalar drop budget. The path is explicitly `(pathX t,z(pathX t))` with `pathX t=-1/2+2*t`. `pathMidpoint` is the literal unitInterval subtype `⟨(1/2:ℝ), by norm_num⟩`; Lean has no HDiv instance for the informal notation `(1/2 : unitInterval)`. This is exactly the intended midpoint, with no numerical approximation.

Only minimal ambient data are exported. Unique maximizer/frontier equality refinements, actual Gaussian normalization and wider-rectangle estimates, physical torus/chart transport, H0/elder inhabitants, ODE capture, source count/probability/density or Parent A/B claims are outside the result. No old elder/H0 theorem is reimported or reproved. Scientific effect: **NONE**.

## Final new-only qualification

All raw Lean runs use pinned `lake env lean -DwarningAsError=true` in the active source packet. Every verification invocation is wrapped by `run_stage.py`, with exact argv, cwd, UTC start/end, measured monotonic elapsed seconds, exit, final production source/object identities before and after, exact source snapshots and log identity. All failures are retained. `EXECUTION_RECORD_INDEX.json` collects the immutable per-run receipts; `SNAPSHOT_IDENTITIES.json` additionally binds all retained source snapshots. The latter hashes were recorded after execution and do not reconstruct historical times. There are no uninstrumented Lean qualification timings in this producer lane.

- `runs/compile-final/receipt.json`: strict object-producing final-source compile, exit 0, 05:17:44.769908–05:17:50.172609 UTC, elapsed 5.402677262 seconds. Final source was frozen before this invocation; no production source modification followed. Earlier `compile-005` is also strict success on exactly the final source, without object output.
- `runs/kernel-001/receipt.json`: **exactly one** named own-module replay, `leanchecker AdaptiveFoldBoundaryPath`, cached imported environment, exit 0, 05:18:14.380202–05:18:20.367018 UTC, elapsed 5.986791950 seconds. No second named replay was run.
- `runs/inventory-001/receipt.json`: complete own-module environment enumeration and `Lean.collectAxioms` classification, exit 0. All 95 own-module declarations have exact axiom rows and use only propext, Classical.choice, Quot.sound. This covers all 93 own-namespace declarations plus two newly generated equation lemmas stored in this new module under `AdaptiveFoldTransverseRidge.profile.eq_1` and `.profileSlope.eq_1`.
- `runs/direct-axioms-001/receipt.json`: exit 0, 89 direct named `#print axioms` rows; the remaining six generated `_proof_` auxiliaries are exhaustively covered by the collector, without disabling linters.
- `runs/controls-004/receipt.json`: final positive/actual-negative controls, strict exit 0, elapsed 3.837049081 seconds.
- `runs/false-without-drop-002/receipt.json`: intended mathematical mutation rejection, expected and actual exit 1, elapsed 2.875691044 seconds. Its only error is the residual goal `False` at the actual false rational frontier-bound instance; no missing-name/API/noncomputability error remains in this accepted rejection run.

Inventory counts distinguish source-authored mathematics from generated declarations: **8 explicitly written theorem proofs, 10 explicit definitions, 3 explicit finite Prop bundles, 74 generated declarations = 95 own-module declarations**. The eight written proofs include exactly the two integrated helper theorems. The generated declarations are 45 structure projection theorems, 8 equation theorems, 6 auxiliary proof theorems, 9 generated definitions (recOn/casesOn/flat constructors), 3 constructors and 3 recursors. By environment kind the totals are 67 theorems, 19 definitions, 3 inductives, 3 constructors and 3 recursors. The public proof suffix is exactly the eight names in `PUBLIC_PROOF_NAMES_APPEND.txt` and `.json`; the 67 environment theorem entries are not 67 newly written mathematical proofs.

Machine-readable `INVENTORY.json`, `GENERATED_DECLARATIONS.json`, `DEFINITIONS_AND_DATA.json`, `SOURCE_OBJECT_IDENTITIES.json`, `SOURCE_POLICY_SCAN.json`, `CONTROL_RECEIPT.json`, `AUTHOR_HELPER_LINEAGE.json` and the raw run receipts supply detailed bindings. The new source has narrow imports, no full Mathlib umbrella, admissions, custom axioms, native_decide, implemented_by or disabled linters. Controls use no object-producing option; only the production module's object resides in this scratch build directory. No control olean was placed in the packet or any shared import path.

## Controls and retained failures

`CONTROL_CONTRACT.md` was written before producer implementation. The passing `Controls.lean` proves actual Frechet derivative formulas for the polynomial family `V_b(x,y)=x^3/3-x/4-b*y^2`, literal G/H second derivative entries, and full structural bundle instantiation for every b>0. With b=4 it instantiates the complete public boundary/path constructor at R=1,c=8,M0=M1=M2=0,A=2, recovers z=0 on the constructed collar by the actual root equation, the older point `(3/2,0)`, the literal frontier bound, an actual Path with pointwise formula `(pathX t,0)`, its floor and exact midpoint, and the normalized pins/gap.

At b=1/100, c=1/50, the same family proves every structural analytic input and constructs the analytic ridge. The center margin holds, while the drop expression is 1/100<1. The actual frontier point (-1/2,1) has value 11/150, versus d=-1/12, exceeding d by 47/300. `FalseWithoutDrop.lean` attempts precisely the omitted-budget frontier consequence at this point, and normalization leaves `False`. This excludes deleting only the vertical-drop budget while retaining the other frozen inputs.

All 16 producer Lean invocations are preserved. Early source compile failures were: missing nonnegative coefficient supplied to an inequality tactic plus an unused binder (compile-001); deprecated tactic syntax, dependent substitution and exact subtype-point construction corrections (compile-002); two equality rewrites that changed the potential argument before applying transitivity (compile-004). compile-003 and compile-object-draft passed their then-current partial source. The control development failures are preserved in controls-001/002/003 (Frechet constant-division API, redundant tactic, scalar normalization and explicit argument inference). The initial false-without-drop-001 source had both the expected False and an unrelated missing noncomputable annotation; that run is not counted as the mathematical rejection qualification. The corrected false-without-drop-002 has only the expected False. No failing source or log was erased or relabeled as success.

## Helper lineage and process separation

The root-dispatched `/root/ridge_vertical_loss` supplied frozen `/workspace/scratch/ridge-vertical-loss/runs/run-006/VerticalLoss.lean`, whole-source SHA256 `40a313e48d747774916a240740d136d47ed84c9494b6fd5a2ea68eeacf8042d2`. The exact two declaration bodies are integrated once. Their integrated new-source byte segments match the helper's frozen declaration-section identities: quadratic loss SHA `8345c83c86a13943b092b622bbbd02634a604f0610388dab7c5f5a6acfad1d78`, literal wrapper SHA `e6dce24c11a073a774426a9e192f2d21aeae7a8d87b270efcabbe372251e9f75`. The helper's strict scratch compile metadata is `runs/run-006/metadata.json`; its full failures and report remain under the helper directory. It ran no helper kernel/audit/control; the integrated new module's one replay and complete inventory cover the new bodies. The public theorem constructs the root and instantiates the helper, so no supplied-ridge premise enters the public constructor.

Producer and helper are author-side OpenAI/GPT work, with zero different-family review credit. Root-side read-only process review is separate from provider-distinct scientific alignment. The latter remains pending and does not make the completed new mathematics unverified. Reuse this completed exact-source evidence for handoff/registration; do not replay unchanged checks merely because another agent or session receives the result.
