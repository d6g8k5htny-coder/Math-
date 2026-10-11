import CompactSourceCutoffProof
import CompactSourceCutoffControls
import Lean

#print axioms SourceCompactCutoff.compact_cutoff_of_geometry
#print axioms SourceCompactCutoff.actual_source_compact_cutoff

-- Enumerate the imported modules' kernel constants, including private helpers
-- and generated declarations; do not infer coverage from two endpoint lines.
open Lean Elab Command in
run_cmd do
  let env := (← getEnv).setExporting false
  let allowed : Array Name := #[`propext, `Classical.choice, `Quot.sound]
  let modules : Array Name := #[`CompactSourceCutoffProof, `CompactSourceCutoffControls]
  let some proofIdx := env.getModuleIdx? `CompactSourceCutoffProof
    | throwError "missing proof module for private-helper guards"
  let mut allNames : Array Name := #[]
  for modName in modules do
    let some idx := env.getModuleIdx? modName
      | throwError "missing audited module: {modName}"
    let names := (env.constants.toList.filterMap fun (name, _) =>
      if env.getModuleIdxFor? name == some idx then some name else none).toArray.qsort Name.lt
    if names.isEmpty then
      throwError "empty declaration inventory for audited module: {modName}"
    logInfo m!"CUTOFF_AUDIT_MODULE {modName} COUNT {names.size}"
    for name in names do
      if (env.checked.get.find? name).isNone then
        throwError "missing kernel declaration: {name}"
      let axs ← Lean.collectAxioms name
      logInfo m!"CUTOFF_AUDIT_DECL {name} AXIOMS {axs}"
      for ax in axs do
        unless allowed.contains ax do
          throwError "forbidden transitive axiom {ax} in {name}"
      allNames := allNames.push name
  let required : Array Name := #[
    `SourceCompactCutoff.cutoffBump, `SourceCompactCutoff.beta,
    `SourceCompactCutoff.K, `SourceCompactCutoff.M,
    `SourceCompactCutoff.extension, `SourceCompactCutoff.V0,
    `SourceCompactCutoff.V1, `SourceCompactCutoff.CompactGeometry,
    `SourceCompactCutoff.compact_cutoff_of_geometry,
    `SourceCompactCutoff.actual_source_compact_cutoff]
  for name in required do
    unless allNames.contains name do
      throwError "required cutoff declaration omitted from audit: {name}"
  let privateHelpers : Array Name := #[
    `SourceCompactCutoff.compact_K_of_split, `SourceCompactCutoff.K_subset_radiusBall,
    `SourceCompactCutoff.support_extension, `SourceCompactCutoff.contDiff_extension,
    `SourceCompactCutoff.extension_rate]
  for helper in privateHelpers do
    unless allNames.any (fun name =>
        env.getModuleIdxFor? name == some proofIdx &&
        Lean.privateToUserName? name == some helper) do
      throwError "required proof-private helper omitted from audit: {helper}"
  logInfo m!"CUTOFF_AUDIT_STANDARD_ONLY_PASS COUNT {allNames.size}"
