import TrustedTasks
import ClosedProofCore
import ExprCodec
import ExprDag
open Lean Meta Elab Tactic
open ClosedProof

namespace ClosedProof.Worker

def protocol := "ul-closed-proof-v1"
def endpointTaskIds : Array String := #["p15.PaletteNumberAttained", "p15.MinimalForbiddenCharacterisation", "p15.LocalRestriction", "p15.LocalDecomposability", "p15.LocalObstructionIsFullBlock", "p15.LocalPriceChain", "p15.IndependentBlockHazard", "p15.FullBlockCoverIff", "p15.CoverCostHazardBound", "p15.WholeGroundChromaticNumber", "p15.ElementaryPaletteFormula", "p15.TriangleNeedsThree", "p15.Benchmark816IsRealized", "p15.Benchmark816Palette", "p15.Benchmark816Cover", "p15.Benchmark816WholeGround", "p15.Benchmark816MinimalForbiddenCounts", "p15.Benchmark816Price", "p15.Benchmark816UnionBound", "p15.TwoCoordGeneratorPrices", "p15.DemandOneRefutation", "p15.LogOnePlusBelowIdentity", "p15.LogRatioBound", "p15.RatioExponentBound", "p15.RestrictedLocalBudget", "p15.RestrictedTransformedPriceBudget", "p15.RhoTestSufficient", "p15.CapTestAtTwoThirds", "p15.Benchmark816TransformedRange", "p15.Benchmark816RationalPrice", "p15.FullTransformedPriceBudget", "p15.RhoStarEnclosure", "p15.RhoStarBelowSixSevenths", "p15.HazardStarPositive", "p15.CoordinatewiseConcavity", "p15.HazardProductBound", "p15.HazardPhiBound", "p15.FullGroundPriceBound", "p15.PhiAtPStar", "p15.FullGroundBudgetIff", "p15.CapacityHazardIsBinomial", "p15.OddMajorityIdentity", "p15.CapacityWorstCase", "p15.HStarExceedsOne", "p15.LocalPriceBoundFull", "p15.GlobalAssemblyHazard", "p15.SharpnessOfRhoStar", "p15.DemandOneBoundary", "p15.SixSeventhsCertificate"]
def taskIds : Array String := #["logic_identity", "logic_conjunction", "nat_identity", "ring_square", "false_goal", "legitimate_false_hypothesis", "p15_two_coord_prices", "p15_log_bound"] ++ endpointTaskIds
def actionIds : Array String := #["intro_all", "constructor", "assumption", "all_assumption", "simp", "omega", "norm_num", "ring", "aesop", "linarith", "nlinarith", "positivity", "p15_prices_known", "p15_log_known"] ++ #["reuse_PaletteNumberAttained", "reuse_MinimalForbiddenCharacterisation", "reuse_LocalRestriction", "reuse_LocalDecomposability", "reuse_LocalObstructionIsFullBlock", "reuse_LocalPriceChain", "reuse_IndependentBlockHazard", "reuse_FullBlockCoverIff", "reuse_CoverCostHazardBound", "reuse_WholeGroundChromaticNumber", "reuse_ElementaryPaletteFormula", "reuse_TriangleNeedsThree", "reuse_Benchmark816IsRealized", "reuse_Benchmark816Palette", "reuse_Benchmark816Cover", "reuse_Benchmark816WholeGround", "reuse_Benchmark816MinimalForbiddenCounts", "reuse_Benchmark816Price", "reuse_Benchmark816UnionBound", "reuse_TwoCoordGeneratorPrices", "reuse_DemandOneRefutation", "reuse_LogOnePlusBelowIdentity", "reuse_LogRatioBound", "reuse_RatioExponentBound", "reuse_RestrictedLocalBudget", "reuse_RestrictedTransformedPriceBudget", "reuse_RhoTestSufficient", "reuse_CapTestAtTwoThirds", "reuse_Benchmark816TransformedRange", "reuse_Benchmark816RationalPrice", "reuse_FullTransformedPriceBudget", "reuse_RhoStarEnclosure", "reuse_RhoStarBelowSixSevenths", "reuse_HazardStarPositive", "reuse_CoordinatewiseConcavity", "reuse_HazardProductBound", "reuse_HazardPhiBound", "reuse_FullGroundPriceBound", "reuse_PhiAtPStar", "reuse_FullGroundBudgetIff", "reuse_CapacityHazardIsBinomial", "reuse_OddMajorityIdentity", "reuse_CapacityWorstCase", "reuse_HStarExceedsOne", "reuse_LocalPriceBoundFull", "reuse_GlobalAssemblyHazard", "reuse_SharpnessOfRhoStar", "reuse_DemandOneBoundary", "reuse_SixSeventhsCertificate"]

def task? : String → Option Expr
  | "logic_identity" => some (mkConst ``Tasks.logic_identity)
  | "logic_conjunction" => some (mkConst ``Tasks.logic_conjunction)
  | "nat_identity" => some (mkConst ``Tasks.nat_identity)
  | "ring_square" => some (mkConst ``Tasks.ring_square)
  | "false_goal" => some (mkConst ``Tasks.false_goal)
  | "legitimate_false_hypothesis" => some (mkConst ``Tasks.legitimate_false_hypothesis)
  | "p15_two_coord_prices" => some (mkConst ``Tasks.p15_two_coord_prices)
  | "p15_log_bound" => some (mkConst ``Tasks.p15_log_bound)
  | "p15.PaletteNumberAttained" => some (mkConst ``ClosedProof.Endpoints.PaletteNumberAttained)
  | "p15.MinimalForbiddenCharacterisation" => some (mkConst ``ClosedProof.Endpoints.MinimalForbiddenCharacterisation)
  | "p15.LocalRestriction" => some (mkConst ``ClosedProof.Endpoints.LocalRestriction)
  | "p15.LocalDecomposability" => some (mkConst ``ClosedProof.Endpoints.LocalDecomposability)
  | "p15.LocalObstructionIsFullBlock" => some (mkConst ``ClosedProof.Endpoints.LocalObstructionIsFullBlock)
  | "p15.LocalPriceChain" => some (mkConst ``ClosedProof.Endpoints.LocalPriceChain)
  | "p15.IndependentBlockHazard" => some (mkConst ``ClosedProof.Endpoints.IndependentBlockHazard)
  | "p15.FullBlockCoverIff" => some (mkConst ``ClosedProof.Endpoints.FullBlockCoverIff)
  | "p15.CoverCostHazardBound" => some (mkConst ``ClosedProof.Endpoints.CoverCostHazardBound)
  | "p15.WholeGroundChromaticNumber" => some (mkConst ``ClosedProof.Endpoints.WholeGroundChromaticNumber)
  | "p15.ElementaryPaletteFormula" => some (mkConst ``ClosedProof.Endpoints.ElementaryPaletteFormula)
  | "p15.TriangleNeedsThree" => some (mkConst ``ClosedProof.Endpoints.TriangleNeedsThree)
  | "p15.Benchmark816IsRealized" => some (mkConst ``ClosedProof.Endpoints.Benchmark816IsRealized)
  | "p15.Benchmark816Palette" => some (mkConst ``ClosedProof.Endpoints.Benchmark816Palette)
  | "p15.Benchmark816Cover" => some (mkConst ``ClosedProof.Endpoints.Benchmark816Cover)
  | "p15.Benchmark816WholeGround" => some (mkConst ``ClosedProof.Endpoints.Benchmark816WholeGround)
  | "p15.Benchmark816MinimalForbiddenCounts" => some (mkConst ``ClosedProof.Endpoints.Benchmark816MinimalForbiddenCounts)
  | "p15.Benchmark816Price" => some (mkConst ``ClosedProof.Endpoints.Benchmark816Price)
  | "p15.Benchmark816UnionBound" => some (mkConst ``ClosedProof.Endpoints.Benchmark816UnionBound)
  | "p15.TwoCoordGeneratorPrices" => some (mkConst ``ClosedProof.Endpoints.TwoCoordGeneratorPrices)
  | "p15.DemandOneRefutation" => some (mkConst ``ClosedProof.Endpoints.DemandOneRefutation)
  | "p15.LogOnePlusBelowIdentity" => some (mkConst ``ClosedProof.Endpoints.LogOnePlusBelowIdentity)
  | "p15.LogRatioBound" => some (mkConst ``ClosedProof.Endpoints.LogRatioBound)
  | "p15.RatioExponentBound" => some (mkConst ``ClosedProof.Endpoints.RatioExponentBound)
  | "p15.RestrictedLocalBudget" => some (mkConst ``ClosedProof.Endpoints.RestrictedLocalBudget)
  | "p15.RestrictedTransformedPriceBudget" => some (mkConst ``ClosedProof.Endpoints.RestrictedTransformedPriceBudget)
  | "p15.RhoTestSufficient" => some (mkConst ``ClosedProof.Endpoints.RhoTestSufficient)
  | "p15.CapTestAtTwoThirds" => some (mkConst ``ClosedProof.Endpoints.CapTestAtTwoThirds)
  | "p15.Benchmark816TransformedRange" => some (mkConst ``ClosedProof.Endpoints.Benchmark816TransformedRange)
  | "p15.Benchmark816RationalPrice" => some (mkConst ``ClosedProof.Endpoints.Benchmark816RationalPrice)
  | "p15.FullTransformedPriceBudget" => some (mkConst ``ClosedProof.Endpoints.FullTransformedPriceBudget)
  | "p15.RhoStarEnclosure" => some (mkConst ``ClosedProof.Endpoints.RhoStarEnclosure)
  | "p15.RhoStarBelowSixSevenths" => some (mkConst ``ClosedProof.Endpoints.RhoStarBelowSixSevenths)
  | "p15.HazardStarPositive" => some (mkConst ``ClosedProof.Endpoints.HazardStarPositive)
  | "p15.CoordinatewiseConcavity" => some (mkConst ``ClosedProof.Endpoints.CoordinatewiseConcavity)
  | "p15.HazardProductBound" => some (mkConst ``ClosedProof.Endpoints.HazardProductBound)
  | "p15.HazardPhiBound" => some (mkConst ``ClosedProof.Endpoints.HazardPhiBound)
  | "p15.FullGroundPriceBound" => some (mkConst ``ClosedProof.Endpoints.FullGroundPriceBound)
  | "p15.PhiAtPStar" => some (mkConst ``ClosedProof.Endpoints.PhiAtPStar)
  | "p15.FullGroundBudgetIff" => some (mkConst ``ClosedProof.Endpoints.FullGroundBudgetIff)
  | "p15.CapacityHazardIsBinomial" => some (mkConst ``ClosedProof.Endpoints.CapacityHazardIsBinomial)
  | "p15.OddMajorityIdentity" => some (mkConst ``ClosedProof.Endpoints.OddMajorityIdentity)
  | "p15.CapacityWorstCase" => some (mkConst ``ClosedProof.Endpoints.CapacityWorstCase)
  | "p15.HStarExceedsOne" => some (mkConst ``ClosedProof.Endpoints.HStarExceedsOne)
  | "p15.LocalPriceBoundFull" => some (mkConst ``ClosedProof.Endpoints.LocalPriceBoundFull)
  | "p15.GlobalAssemblyHazard" => some (mkConst ``ClosedProof.Endpoints.GlobalAssemblyHazard)
  | "p15.SharpnessOfRhoStar" => some (mkConst ``ClosedProof.Endpoints.SharpnessOfRhoStar)
  | "p15.DemandOneBoundary" => some (mkConst ``ClosedProof.Endpoints.DemandOneBoundary)
  | "p15.SixSeventhsCertificate" => some (mkConst ``ClosedProof.Endpoints.SixSeventhsCertificate)
  | _ => none

def action? (s : String) : TacticM Unit := do
  let stx ← match s with
    | "intro_all" => `(tactic| intros)
    | "constructor" => `(tactic| constructor)
    | "assumption" => `(tactic| assumption)
    | "all_assumption" => `(tactic| all_goals assumption)
    | "simp" => `(tactic| simp)
    | "omega" => `(tactic| omega)
    | "norm_num" => `(tactic| norm_num)
    | "ring" => `(tactic| ring)
    | "aesop" => `(tactic| aesop)
    | "linarith" => `(tactic| linarith)
    | "nlinarith" => `(tactic| nlinarith)
    | "positivity" => `(tactic| positivity)
    | "p15_prices_known" => `(tactic| (change UniversalLaw.Spec.P15.TwoCoordGeneratorPrices; unfold UniversalLaw.Spec.P15.TwoCoordGeneratorPrices; refine ⟨?_, ?_, ?_, ?_⟩ <;> simp [UniversalLaw.Spec.P15.genPrice, UniversalLaw.Spec.P15.twoCoordC, Finset.prod_const] <;> norm_num))
    | "p15_log_known" => `(tactic| (change UniversalLaw.Spec.P15.LogOnePlusBelowIdentity; intro x hx; have h := Real.log_lt_sub_one_of_pos (by linarith : (0 : ℝ) < 1 + x) (by intro h; linarith : (1 : ℝ) + x ≠ 1); linarith))
    | "reuse_PaletteNumberAttained" => `(tactic| exact ClosedProof.Endpoints.reuse_PaletteNumberAttained)
    | "reuse_MinimalForbiddenCharacterisation" => `(tactic| exact ClosedProof.Endpoints.reuse_MinimalForbiddenCharacterisation)
    | "reuse_LocalRestriction" => `(tactic| exact ClosedProof.Endpoints.reuse_LocalRestriction)
    | "reuse_LocalDecomposability" => `(tactic| exact ClosedProof.Endpoints.reuse_LocalDecomposability)
    | "reuse_LocalObstructionIsFullBlock" => `(tactic| exact ClosedProof.Endpoints.reuse_LocalObstructionIsFullBlock)
    | "reuse_LocalPriceChain" => `(tactic| exact ClosedProof.Endpoints.reuse_LocalPriceChain)
    | "reuse_IndependentBlockHazard" => `(tactic| exact ClosedProof.Endpoints.reuse_IndependentBlockHazard)
    | "reuse_FullBlockCoverIff" => `(tactic| exact ClosedProof.Endpoints.reuse_FullBlockCoverIff)
    | "reuse_CoverCostHazardBound" => `(tactic| exact ClosedProof.Endpoints.reuse_CoverCostHazardBound)
    | "reuse_WholeGroundChromaticNumber" => `(tactic| exact ClosedProof.Endpoints.reuse_WholeGroundChromaticNumber)
    | "reuse_ElementaryPaletteFormula" => `(tactic| exact ClosedProof.Endpoints.reuse_ElementaryPaletteFormula)
    | "reuse_TriangleNeedsThree" => `(tactic| exact ClosedProof.Endpoints.reuse_TriangleNeedsThree)
    | "reuse_Benchmark816IsRealized" => `(tactic| exact ClosedProof.Endpoints.reuse_Benchmark816IsRealized)
    | "reuse_Benchmark816Palette" => `(tactic| exact ClosedProof.Endpoints.reuse_Benchmark816Palette)
    | "reuse_Benchmark816Cover" => `(tactic| exact ClosedProof.Endpoints.reuse_Benchmark816Cover)
    | "reuse_Benchmark816WholeGround" => `(tactic| exact ClosedProof.Endpoints.reuse_Benchmark816WholeGround)
    | "reuse_Benchmark816MinimalForbiddenCounts" => `(tactic| exact ClosedProof.Endpoints.reuse_Benchmark816MinimalForbiddenCounts)
    | "reuse_Benchmark816Price" => `(tactic| exact ClosedProof.Endpoints.reuse_Benchmark816Price)
    | "reuse_Benchmark816UnionBound" => `(tactic| exact ClosedProof.Endpoints.reuse_Benchmark816UnionBound)
    | "reuse_TwoCoordGeneratorPrices" => `(tactic| exact ClosedProof.Endpoints.reuse_TwoCoordGeneratorPrices)
    | "reuse_DemandOneRefutation" => `(tactic| exact ClosedProof.Endpoints.reuse_DemandOneRefutation)
    | "reuse_LogOnePlusBelowIdentity" => `(tactic| exact ClosedProof.Endpoints.reuse_LogOnePlusBelowIdentity)
    | "reuse_LogRatioBound" => `(tactic| exact ClosedProof.Endpoints.reuse_LogRatioBound)
    | "reuse_RatioExponentBound" => `(tactic| exact ClosedProof.Endpoints.reuse_RatioExponentBound)
    | "reuse_RestrictedLocalBudget" => `(tactic| exact ClosedProof.Endpoints.reuse_RestrictedLocalBudget)
    | "reuse_RestrictedTransformedPriceBudget" => `(tactic| exact ClosedProof.Endpoints.reuse_RestrictedTransformedPriceBudget)
    | "reuse_RhoTestSufficient" => `(tactic| exact ClosedProof.Endpoints.reuse_RhoTestSufficient)
    | "reuse_CapTestAtTwoThirds" => `(tactic| exact ClosedProof.Endpoints.reuse_CapTestAtTwoThirds)
    | "reuse_Benchmark816TransformedRange" => `(tactic| exact ClosedProof.Endpoints.reuse_Benchmark816TransformedRange)
    | "reuse_Benchmark816RationalPrice" => `(tactic| exact ClosedProof.Endpoints.reuse_Benchmark816RationalPrice)
    | "reuse_FullTransformedPriceBudget" => `(tactic| exact ClosedProof.Endpoints.reuse_FullTransformedPriceBudget)
    | "reuse_RhoStarEnclosure" => `(tactic| exact ClosedProof.Endpoints.reuse_RhoStarEnclosure)
    | "reuse_RhoStarBelowSixSevenths" => `(tactic| exact ClosedProof.Endpoints.reuse_RhoStarBelowSixSevenths)
    | "reuse_HazardStarPositive" => `(tactic| exact ClosedProof.Endpoints.reuse_HazardStarPositive)
    | "reuse_CoordinatewiseConcavity" => `(tactic| exact ClosedProof.Endpoints.reuse_CoordinatewiseConcavity)
    | "reuse_HazardProductBound" => `(tactic| exact ClosedProof.Endpoints.reuse_HazardProductBound)
    | "reuse_HazardPhiBound" => `(tactic| exact ClosedProof.Endpoints.reuse_HazardPhiBound)
    | "reuse_FullGroundPriceBound" => `(tactic| exact ClosedProof.Endpoints.reuse_FullGroundPriceBound)
    | "reuse_PhiAtPStar" => `(tactic| exact ClosedProof.Endpoints.reuse_PhiAtPStar)
    | "reuse_FullGroundBudgetIff" => `(tactic| exact ClosedProof.Endpoints.reuse_FullGroundBudgetIff)
    | "reuse_CapacityHazardIsBinomial" => `(tactic| exact ClosedProof.Endpoints.reuse_CapacityHazardIsBinomial)
    | "reuse_OddMajorityIdentity" => `(tactic| exact ClosedProof.Endpoints.reuse_OddMajorityIdentity)
    | "reuse_CapacityWorstCase" => `(tactic| exact ClosedProof.Endpoints.reuse_CapacityWorstCase)
    | "reuse_HStarExceedsOne" => `(tactic| exact ClosedProof.Endpoints.reuse_HStarExceedsOne)
    | "reuse_LocalPriceBoundFull" => `(tactic| exact ClosedProof.Endpoints.reuse_LocalPriceBoundFull)
    | "reuse_GlobalAssemblyHazard" => `(tactic| exact ClosedProof.Endpoints.reuse_GlobalAssemblyHazard)
    | "reuse_SharpnessOfRhoStar" => `(tactic| exact ClosedProof.Endpoints.reuse_SharpnessOfRhoStar)
    | "reuse_DemandOneBoundary" => `(tactic| exact ClosedProof.Endpoints.reuse_DemandOneBoundary)
    | "reuse_SixSeventhsCertificate" => `(tactic| exact ClosedProof.Endpoints.reuse_SixSeventhsCertificate)
    | _ => throwError "unknown action"
  evalTactic stx

structure Checkpoint where
  root : MVarId
  target : Expr
  task : String
  saved : Tactic.SavedState

def field (j : Json) (n : String) : String := ((j.getObjVal? n).bind Json.getStr?).toOption.getD ""
def natField (j : Json) (n : String) : Nat := ((j.getObjVal? n).bind Json.getNat?).toOption.getD 0

def response (session : String) (id : Json) (ok : Bool) (status : String) (rest : List (String × Json) := []) : Json :=
  Json.mkObj <| [("protocol", toJson protocol), ("session", toJson session), ("id", id), ("ok", toJson ok), ("status", toJson status)] ++ rest

def goalsJson : TacticM Json := do
  let mut a : Array Json := #[]
  for g in (← getUnsolvedGoals) do
    let text ← g.withContext do return (← ppExpr (← g.getType)).pretty
    a := a.push (toJson text)
  return toJson a

def certificate (task : String) (target proof : Expr) (axioms : Array Name) : Json :=
  Json.mkObj [("schema", toJson "ul-closed-proof-certificate-v2"), ("task", toJson task), ("type", ExprCodec.exprToJson target), ("proof", ExprDag.encode proof), ("axioms", toJson (axioms.map Name.toString))]

partial def loop (session : String) (baseline : Environment) : TacticM Unit := do
  let stdin ← IO.getStdin
  let stdout ← IO.getStdout
  stdout.putStrLn <| (Json.mkObj [("event", toJson "ready"), ("protocol", toJson protocol), ("session", toJson session), ("max_states", toJson (64 : Nat)), ("source_exposed_tasks", toJson endpointTaskIds), ("training_eligible", toJson false), ("tasks", toJson taskIds), ("actions", toJson actionIds), ("action_sources", Json.mkObj [("p15_prices_known", toJson "change UniversalLaw.Spec.P15.TwoCoordGeneratorPrices; unfold UniversalLaw.Spec.P15.TwoCoordGeneratorPrices; refine ⟨?_, ?_, ?_, ?_⟩ <;> simp [UniversalLaw.Spec.P15.genPrice, UniversalLaw.Spec.P15.twoCoordC, Finset.prod_const] <;> norm_num"), ("p15_log_known", toJson "change UniversalLaw.Spec.P15.LogOnePlusBelowIdentity; intro x hx; have h := Real.log_lt_sub_one_of_pos (by linarith : (0 : ℝ) < 1 + x) (by intro h; linarith : (1 : ℝ) + x ≠ 1); linarith")])]).compress
  stdout.flush
  let mut states : Array (Option Checkpoint) := #[]
  let mut requests := 0
  repeat
    let line ← stdin.getLine
    if line.isEmpty then break
    requests := requests + 1
    let parsed := Json.parse line
    let j := parsed.toOption.getD Json.null
    let id := (j.getObjVal? "id").toOption.getD Json.null
    let mut answer := response session id false "rejected"
    let mut stop := false
    if requests > 256 || field j "protocol" != protocol || field j "session" != session || (j.getObjVal? "id" >>= Json.getNat?).toOption.isNone then
      answer := response session id false "rejected"
      if requests > 256 then stop := true
    else
      let op := field j "op"
      try
        if op == "shutdown" then
          answer := response session id true "stopped"
          stop := true
        else if op == "open" then
          let task := field j "task"
          if let some target := task? task then
            if (states.filter Option.isSome).size < 64 then
              let goalTarget ← whnf target
              let root ← mkFreshExprMVarAt {} {} goalTarget
              setGoals [root.mvarId!]
              let saved ← Tactic.saveState
              let sid := states.size
              states := states.push (some ⟨root.mvarId!, target, task, saved⟩)
              answer := response session id true "opened" [("state", toJson sid), ("task", toJson task), ("goals", ← goalsJson)]
        else if op == "drop" then
          let sid := ((j.getObjVal? "state" >>= Json.getNat?).toOption.getD 1000000000)
          if (states[sid]?.getD none).isSome then
            states := states.set! sid none
            answer := response session id true "dropped"
        else if op == "inspect" || op == "attempt" then
          let sid := ((j.getObjVal? "state" >>= Json.getNat?).toOption.getD 1000000000)
          if let some cp := (states[sid]?.getD none) then
            cp.saved.restore true
            if op == "inspect" then
              answer := response session id true "inspected" [("state", toJson sid), ("task", toJson cp.task), ("goals", ← goalsJson), ("root_assigned", toJson (← cp.root.isAssigned))]
            else
              let action := field j "action"
              let limit := natField j "heartbeat_limit"
              if actionIds.contains action && limit > 0 && (states.filter Option.isSome).size < 64 then
                let start ← IO.monoNanosNow
                let hbRef ← IO.mkRef (none : Option (Nat × Nat × Nat))
                let budgetExceeded ← IO.mkRef false
                try
                  let (cached, origin) ← tryCatchRuntimeEx (withOptions (fun o => maxHeartbeats.set o limit) <|
                    withTheReader Core.Context (fun c => { c with maxHeartbeats := limit * 1000 }) <|
                      withCurrHeartbeats do
                        let c ← readThe Core.Context
                        unless c.maxHeartbeats == limit * 1000 && maxHeartbeats.get c.options == limit do
                          throwError "heartbeat readback mismatch"
                        hbRef.set (some (maxHeartbeats.get c.options, c.maxHeartbeats, c.initHeartbeats))
                        action? action
                        return (c.maxHeartbeats, c.initHeartbeats)) (fun ex => do
                          if ex.isMaxHeartbeat then
                            budgetExceeded.set true
                            throwError "tactic heartbeat budget exhausted"
                          else if ex.isMaxRecDepth then
                            throwError "tactic recursion depth exhausted"
                          else
                            throw ex)
                  let after ← goalsJson
                  if (← getUnsolvedGoals).isEmpty then
                    let proof ← instantiateMVars (mkMVar cp.root)
                    match ← closedGate baseline cp.target proof with
                    | .ok axioms => answer := response session id true "closed" [("certificate", certificate cp.task cp.target proof axioms), ("goals", after), ("wall_ns", toJson ((← IO.monoNanosNow) - start)), ("heartbeat_limit", toJson limit), ("cached_heartbeats", toJson cached), ("heartbeat_origin", toJson origin)]
                    | .error e => answer := response session id false "rejected" [("reason", toJson e), ("wall_ns", toJson ((← IO.monoNanosNow) - start)), ("heartbeat_limit", toJson limit), ("cached_heartbeats", toJson cached), ("heartbeat_origin", toJson origin)]
                  else
                    let next ← Tactic.saveState
                    let nextId := states.size
                    states := states.push (some { cp with saved := next })
                    answer := response session id true "progress" [("state", toJson nextId), ("goals", after), ("wall_ns", toJson ((← IO.monoNanosNow) - start)), ("heartbeat_limit", toJson limit), ("cached_heartbeats", toJson cached), ("heartbeat_origin", toJson origin)]
                catch ex =>
                  let msg ← ex.toMessageData.toString
                  let readings ← hbRef.get
                  let hbFields := match readings with
                    | some (opt, cached, origin) => [("heartbeat_limit", toJson opt), ("cached_heartbeats", toJson cached), ("heartbeat_origin", toJson origin)]
                    | none => []
                  answer := response session id false (if ← budgetExceeded.get then "budget_exhaustion" else "tactic_error") ([("reason", toJson msg), ("wall_ns", toJson ((← IO.monoNanosNow) - start))] ++ hbFields)
        else if op == "verify" then
          if let some target := task? (field j "task") then
            let cert := (j.getObjVal? "certificate").toOption.getD Json.null
            if field cert "schema" == "ul-closed-proof-certificate-v2" && field cert "task" == field j "task" && (cert.getObjVal? "type").toOption == some (ExprCodec.exprToJson target) then
              if let .ok proof := (cert.getObjVal? "proof" >>= ExprDag.decode) then
                match ← closedGate baseline target proof with
                | .ok axioms =>
                  let actual := toJson (axioms.map Name.toString)
                  if (cert.getObjVal? "axioms").toOption == some actual then
                    answer := response session id true "accepted" [("axioms", actual)]
                | .error e => answer := response session id false "rejected" [("reason", toJson e)]
      catch ex =>
        answer := response session id false "rejected" [("reason", toJson (← ex.toMessageData.toString))]
    stdout.putStrLn answer.compress
    stdout.flush
    if stop then break

unsafe def runWithEnvironment (env : Environment) (args : List String) : IO UInt32 := do
  let session := args.headD ""
  if session.isEmpty then throw <| IO.userError "missing session"
  let term := (loop session env { elaborator := .anonymous, recover := false }).run { goals := [] }
  let _ ← term.toIO { fileName := "worker", fileMap := default } { env := env } {} {} {} {}
  return 0

-- Legacy source-run entry retained for the historical development test driver.
-- Supported clients use WorkerBootstrap so the heavy environment is loaded once.
unsafe def main (args : List String) : IO UInt32 := do
  enableInitializersExecution
  let env ← importModules (loadExts := true) #[{ module := `TrustedTasks }, { module := `ClosedProofCore }, { module := `ExprCodec }] {}
  runWithEnvironment env args
end ClosedProof.Worker

unsafe def main := ClosedProof.Worker.main
