import MorseFiniteCritical
import MorseFiniteControls
import Lean.Elab.Command
import Lean.Util.CollectAxioms

/-! Complete module-origin declaration census, including generated/private helpers.
The audit permits only Lean's standard propext, Classical.choice and Quot.sound.
Its successful execution is not provider-distinct review or scientific promotion. -/

#print axioms TorusMorseFinite.quotientCriticalSet_finite
#print axioms TorusMorseFinite.quotientCriticalSet_finite_of_inertia
#check @TorusMorseFinite.quotientCriticalSet_finite

open Lean Elab Command in
run_cmd do
  let env := (← getEnv).setExporting false
  let allowed : Array Name := #[`propext, `Classical.choice, `Quot.sound]
  let modules : Array Name := #[`Lifetime, `TorusTopology,
    `MorseFiniteCritical, `MorseFiniteControls]
  let constants := env.constants.toList
  let mut allNames : Array Name := #[]
  for modName in modules do
    let some idx := env.getModuleIdx? modName
      | throwError "missing audited module: {modName}"
    let names := (constants.filterMap fun (name, _) =>
      if env.getModuleIdxFor? name == some idx then some name else none).toArray.qsort Name.lt
    if names.isEmpty then throwError "empty declaration inventory: {modName}"
    liftIO <| IO.eprintln s!"MORSE_AUDIT_PROGRESS {modName} COUNT {names.size}"
    logInfo m!"MORSE_AUDIT_MODULE {modName} COUNT {names.size}"
    for name in names do
      if (env.checked.get.find? name).isNone then
        throwError "missing kernel declaration: {name}"
      let axs ← Lean.collectAxioms name
      logInfo m!"MORSE_AUDIT_DECL {name} AXIOMS {axs}"
      for ax in axs do
        unless allowed.contains ax do
          throwError "forbidden transitive axiom {ax} in {name}"
      allNames := allNames.push name
  let required : Array Name := #[
    `UniversalLaw.Spec.Lifetime.IsSmooth,
    `UniversalLaw.Spec.Lifetime.HessianHasInertia,
    `UniversalLaw.Spec.Lifetime.IsMorseDistinct,
    `TorusFiltration.torus_proj,
    `TorusFiltration.torus_compact,
    `TorusMorseFinite.literal_hessian_symmetric,
    `TorusMorseFinite.inertia_fderiv_injective,
    `TorusMorseFinite.inertia_fderiv_equiv,
    `TorusMorseFinite.literal_critical_isolated,
    `TorusMorseFinite.literal_fderiv_periodic,
    `TorusMorseFinite.quotientDerivative_continuous,
    `TorusMorseFinite.mem_quotientCriticalSet_iff,
    `TorusMorseFinite.quotientCriticalSet_closed,
    `TorusMorseFinite.quotientCriticalSet_discrete,
    `TorusMorseFinite.quotientCriticalSet_finite_of_inertia,
    `TorusMorseFinite.quotientCriticalSet_finite,
    `TorusMorseControls.nonsymmetricForm_bilinear,
    `TorusMorseControls.complementary_axes,
    `TorusMorseControls.nonsymmetric_signed_axes_singular,
    `TorusMorseControls.nonsmooth_literal_critical,
    `TorusMorseControls.half_open_not_compact]
  for name in required do
    unless allNames.contains name do
      throwError "required declaration omitted from audit: {name}"
  logInfo m!"MORSE_AUDIT_STANDARD_ONLY_PASS COUNT {allNames.size}"
