# Constructed C² transverse ridge: producer handoff

Production source: `/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025/AdaptiveFoldTransverseRidge.lean` (533 lines, 28,516 bytes). Source SHA256 `715b01c2ae3b6e2bceb4196e53361530c8c9c69550e7cf675904cd5661b3de20`. Compiled object: `build/AdaptiveFoldTransverseRidge.olean` (841,192 bytes), SHA256 `f3957a3afe2d4d1f492c3ddd9463f93526c821f3210a48094267d56a7a527749`.

Read the binding brief before code, frozen git object `66037c5c7083161f9a14fb4103227d15fc2cf6e6`, native activation `6408541927`, plus exact pinned preflight and `/workspace/AGENTS.md`. The completed applicable 31-module/25-input verification remains established and was not repeated. Qualification here covers only the new module and new controls. Provider-distinct review is a separate process obligation, not missing mathematics.

The producer edited only this new source and its own scratch directory. No old source, lakefile, manifest, commit, publication, or external message was changed. Root owns registration, packaging into the packet, commits, and posts.

## Mathematical result

`exists_unique_c2_transverse_ridge` constructs an open U containing the original closed interval and z:ℝ→ℝ from an actual C⁴ potential V on open O, rectangle inclusion, positive radius/concavity constant, literal negative vertical second partial and strict opposite transverse first-partial boundary signs. No supplied z or ridge continuity occurs in the input. The theorem is slightly stronger in allowing any l,u; the intended l≤u instance follows immediately.

Actual partials are defined from `fderiv` on ex=(1,0) and ey=(0,1). A compact structural collar is proved with `IsCompact.eventually_forall_of_forall_eventually`, using the strict derivative margin Gy<-c/2 and preserved boundary signs. IVT supplies an interior root; strict antitonicity supplies uniqueness. The choice is extended arbitrarily outside open U, where no conclusion is asserted. At each graph point the vertical derivative's inverse is explicitly reciprocal*id, and Mathlib's genuine C² IFT is applied. Its local function stays in the vertical strip by continuity and equals the chosen zero by uniqueness; this proves C² regularity without assuming it. All endpoint derivatives are full two-sided derivatives because the original closed interval lies inside open U.

`exists_unique_c2_transverse_ridge_with_jets` instantiates the helper chain identities with that constructed z, retains the nonzero actual Gy denominator and proves the requested first/second derivative formulas. Structural rectangle bounds at the center, on Gx, and on all four coordinate entries of D²G give |z|≤M0/c, |z'|≤M1/c, and |z''|≤(M2/c)(1+|z'|)². Bilinear expansion uses coordinates explicitly and makes no product/Euclidean norm identification.

Literal profile/profileSlope/profileSlopeFirst/profileSlopeSecond definitions and their three full HasDerivAt statements are included in the same constructed-ridge conclusion. They have the derivative shape consumed by `AdaptiveFoldScalarBarrier`; no scalar-barrier result is assumed, rechecked, or imported. Actual Gaussian-source structural signs, ambient boundary/path, H0/elder/counting, and Parent A/B conclusions remain separate future obligations.

## Qualification and controls

- The final source passes `lean -DwarningAsError=true`; the first object-producing compile is preserved at `runs/compile-final/receipt.json` and `output.log`. The original raw log label was `compile-object-draft`, but its bytes are exactly the final source. No source modification followed.
- Exactly one named own-module kernel replay (`leanchecker AdaptiveFoldTransverseRidge`), `kernel-001`, exit 0, actual UTC 05:02:33.836615–05:02:40.329047 on 26 October 2026. Cached imported mathematics was reused.
- `inventory-001`, exit 0: 52 declarations exhaust the module. These classify as 22 explicit public theorems, 10 public definitions and 20 generated declarations (14 simp theorems, 3 defining equations, 3 auxiliary proof theorems). Every declaration has an exact collectAxioms row and all use only propext/Classical.choice/Quot.sound.
- `direct-axioms-001`, exit 0: 49 direct named `#print axioms` rows cover all 32 public declarations and 17 generated stable names. The 3 `_proof_` auxiliaries are covered by the complete collector, without disabling linters.
- `controls-003`, exit 0:actual polynomial V=xy-y²/2 fully instantiates the main with-jets theorem with M0=1/2,M1=1,M2=0,c=1. Constructed z=x on U, full z'=1 at both original interval endpoints, z''(0)=0 and |z|≤1/2.
- `boundary-control-001`, exit 0:actual C⁴ V=3y-y²/2 has Gy=-1, positive lower boundary and no strip root. Its upper boundary value 2 violates the required negative sign.
- `false-control-001`, expected/actual exit 1:the attempted false strip witness y = 3 is mathematically rejected at the interval condition with the residual goal False, while the actual zero equation holds. This is a substantive boundary-sign control.

All post-final qualification receipts record exact source/object identities before and after commands; both remain unchanged. `SOURCE_OBJECT_IDENTITIES.json`, `INVENTORY.json`, `EXECUTION_RECORD_INDEX.json`, `CONTROL_RECEIPT.json` and `AUTHOR_HELPER_LINEAGE.json` are machine-readable summaries. All raw failures and source snapshots are retained.

Early interactive elaboration used raw tool receipts before the timing wrapper. Those commands, exits, exact source snapshots and logs are preserved in `runs/early-compile-*` and the final compile receipt. Exact process start/end times were not instrumented and remain null; actual filesystem log/object timestamps are separately labelled, and no timestamps were invented. The later named kernel, inventories and controls have measured real UTC receipts. `EARLY_API_RECEIPTS.json` preserves the failing API prototype and its source, and explicitly distinguishes an unrecorded Lean exit from a shell exit 0 in an exploratory #check call.

The precise pinned-API correction discovered by execution: `HasFDerivAt.comp_hasDerivAt` has an explicit scalar basepoint before its two proof arguments due a surrounding section binder. The proof calls `.comp_hasDerivAt x hp`. No API blocker remains.

## Helper lineage

The authorized `/root/transverse_ridge_jets` helper supplied derivative/quantitative scratch proofs given C² G and C² z. The checked derivative segment from frozen run 004 and quantitative-only segment from frozen run 007 were integrated exactly once, with attribution comments. Production construction and final theorem instantiate these helpers with the newly constructed z; no fake ridge premise enters the final theorem. Exact identities and reports are linked in `AUTHOR_HELPER_LINEAGE.json`. This is OpenAI author-side decomposition with zero independent-family review credit. Optional helper run 008 profile additions were excluded; the producer authored production profile jets independently.

No admissions, custom axioms, native_decide, full Mathlib umbrella import or disabled linters occur in the new source. New verification is complete and reusable. Do not repeat unchanged module checks merely for handoff or registration.
