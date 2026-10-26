import SourceLifetimePairFiniteness
import Lean.Util.CollectAxioms

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let allowed : Array Name := #[`propext, `Classical.choice, `Quot.sound]
  for mod in #[`Lifetime, `SourceLifetimeGeometry, `SourceLifetimePairFiniteness] do
    let some idx := env.getModuleIdx? mod
      | throwError "Missing module {mod}"
    let names := ((env.constants.toList.filter fun (n, _) =>
      env.getModuleIdxFor? n == some idx).map Prod.fst).toArray.qsort Name.quickLt
    for n in names do
      let axs ← collectAxioms n
      for ax in axs do
        unless allowed.contains ax do
          throwError "Forbidden axiom {ax} in {n}"
      let kind := match env.find? n with
        | some (.thmInfo _) => "theorem"
        | some (.defnInfo _) => "definition_or_data"
        | some (.axiomInfo _) => "axiom"
        | some (.opaqueInfo _) => "opaque"
        | _ => "generated_inductive_data"
      logInfo m!"DECLARATION {mod} {kind} {n}: AXIOMS {axs}"
    logInfo m!"COMPLETE_MODULE_AXIOM_AUDIT {mod} declarations={names.size}; allowed={allowed}"

#print I4SourceLifetimePairFiniteness.actual_critical_coordinateGradient_zero
#print I4SourceLifetimePairFiniteness.coordinates_fundDomain_mem_sourceMorseCube
#print I4SourceLifetimePairFiniteness.smoothLaw_ae_finite_criticalFundDomain
#print I4SourceLifetimePairFiniteness.smoothLaw_ae_finite_pairSet_of_critical
#print I4SourceLifetimePairFiniteness.smoothLaw_ae_finite_candidatePairSet
#print I4SourceLifetimePairFiniteness.smoothLaw_ae_finite_windowPairSet
#print I4SourceLifetimePairFiniteness.smoothLaw_ae_finite_windowElderPairSet
#print I4SourceLifetimePairFiniteness.smoothLaw_ae_finite_unrestrictedPairSet
#print I4SourceLifetimePairFiniteness.smoothLaw_ae_finite_finiteBarPairSet
