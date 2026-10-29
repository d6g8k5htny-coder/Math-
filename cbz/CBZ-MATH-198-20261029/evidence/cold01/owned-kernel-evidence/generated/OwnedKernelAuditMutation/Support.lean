import Closure.Assembly
import Closure.DownsetMass
import Closure.FinalAudit
import Closure.HazardInterpolation
import Closure.LocalRatio
import Closure.PaletteCover
import Closure.ProductMass
import Closure.RatioGate
import Completion.Benchmark
import Completion.BenchmarkPrices
import Completion.BenchmarkUnion
import Completion.FinalAudit
import Completion.Numerics
import Completion.PaletteFormula
import Completion.Structural
import Completion.UnionBound
import General.Amalgamation
import General.BernoulliFinner
import General.Definitions
import General.FinalAudit
import General.Finner
import General.FinnerBridge
import General.Overlap
import General.Probability
import General.Safety
import General.Threshold
import General.WitnessLoad
import Integration.EndpointTasks
import SpecificationProofs.P15Elementary
import Specifications.P15
import Lean
open Lean
namespace OwnedKernelAuditMutation
def ownedModules : List Name := [
  (Name.str (Name.str Name.anonymous "Closure") "Assembly"),
  (Name.str (Name.str Name.anonymous "Closure") "DownsetMass"),
  (Name.str (Name.str Name.anonymous "Closure") "FinalAudit"),
  (Name.str (Name.str Name.anonymous "Closure") "HazardInterpolation"),
  (Name.str (Name.str Name.anonymous "Closure") "LocalRatio"),
  (Name.str (Name.str Name.anonymous "Closure") "PaletteCover"),
  (Name.str (Name.str Name.anonymous "Closure") "ProductMass"),
  (Name.str (Name.str Name.anonymous "Closure") "RatioGate"),
  (Name.str (Name.str Name.anonymous "Completion") "Benchmark"),
  (Name.str (Name.str Name.anonymous "Completion") "BenchmarkPrices"),
  (Name.str (Name.str Name.anonymous "Completion") "BenchmarkUnion"),
  (Name.str (Name.str Name.anonymous "Completion") "FinalAudit"),
  (Name.str (Name.str Name.anonymous "Completion") "Numerics"),
  (Name.str (Name.str Name.anonymous "Completion") "PaletteFormula"),
  (Name.str (Name.str Name.anonymous "Completion") "Structural"),
  (Name.str (Name.str Name.anonymous "Completion") "UnionBound"),
  (Name.str (Name.str Name.anonymous "General") "Amalgamation"),
  (Name.str (Name.str Name.anonymous "General") "BernoulliFinner"),
  (Name.str (Name.str Name.anonymous "General") "Definitions"),
  (Name.str (Name.str Name.anonymous "General") "FinalAudit"),
  (Name.str (Name.str Name.anonymous "General") "Finner"),
  (Name.str (Name.str Name.anonymous "General") "FinnerBridge"),
  (Name.str (Name.str Name.anonymous "General") "Overlap"),
  (Name.str (Name.str Name.anonymous "General") "Probability"),
  (Name.str (Name.str Name.anonymous "General") "Safety"),
  (Name.str (Name.str Name.anonymous "General") "Threshold"),
  (Name.str (Name.str Name.anonymous "General") "WitnessLoad"),
  (Name.str (Name.str Name.anonymous "Integration") "EndpointTasks"),
  (Name.str (Name.str Name.anonymous "SpecificationProofs") "P15Elementary"),
  (Name.str (Name.str Name.anonymous "Specifications") "P15")]
def explicitTargets : List Name := [
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "P15Closure") "paletteNumberAttained"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "P15Closure") "localRestriction"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "P15Closure") "localPriceChain"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "P15Closure") "independentBlockHazard"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "P15Closure") "fullBlockCoverIff"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "P15Closure") "coverCostHazardBound"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "P15Closure") "restrictedLocalBudget"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "P15Closure") "restrictedTransformedPriceBudget"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "P15Closure") "rhoTestSufficient"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "P15Closure") "fullTransformedPriceBudget"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "P15Closure") "coordinatewiseConcavity"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "P15Closure") "hazardProductBound"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "P15Closure") "hazardPhiBound"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "P15Closure") "fullGroundPriceBound"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "P15Closure") "fullGroundBudgetIff"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "P15Closure") "localPriceBoundFull"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "P15Closure") "globalAssemblyHazard"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "P15Closure") "fullTransformedPriceBudget_sixSevenths"),
  (Name.str (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "Proofs") "P15Elementary") "twoCoordGeneratorPrices"),
  (Name.str (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "Proofs") "P15Elementary") "logOnePlusBelowIdentity"),
  (Name.str (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "Proofs") "P15Elementary") "demandOneRefutation"),
  (Name.str (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "Proofs") "P15Elementary") "logRatioBound"),
  (Name.str (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "Proofs") "P15Elementary") "capTestAtTwoThirds"),
  (Name.str (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "Proofs") "P15Elementary") "ratioExponentBound"),
  (Name.str (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "Proofs") "P15Elementary") "rhoStarBelowSixSevenths"),
  (Name.str (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "Proofs") "P15Elementary") "sixSeventhsCertificate"),
  (Name.str (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "Proofs") "P15Elementary") "hStarExceedsOne"),
  (Name.str (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "Proofs") "P15Elementary") "phiAtPStar"),
  (Name.str (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "Proofs") "P15Elementary") "hazardStarPositive"),
  (Name.str (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "Proofs") "P15Elementary") "oddMajorityIdentity"),
  (Name.str (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "Proofs") "P15Elementary") "capacityWorstCase"),
  (Name.str (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "Proofs") "P15Elementary") "demandOneBoundary"),
  (Name.str (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "Proofs") "P15Elementary") "triangleNeedsThree"),
  (Name.str (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "Proofs") "P15Elementary") "capacityHazardIsBinomial"),
  (Name.str (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "Proofs") "P15Elementary") "sharpnessOfRhoStar"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "P15Completion") "minimalForbiddenCharacterisation"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "P15Completion") "localDecomposability"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "P15Completion") "localObstructionIsFullBlock"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "P15Completion") "wholeGroundChromaticNumber"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "P15Completion") "elementaryPaletteFormula"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "P15Completion") "benchmark816IsRealized"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "P15Completion") "benchmark816Palette"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "P15Completion") "benchmark816Cover"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "P15Completion") "benchmark816WholeGround"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "P15Completion") "benchmark816MinimalForbiddenCounts"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "P15Completion") "benchmark816Price"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "P15Completion") "benchmark816UnionBound"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "P15Completion") "benchmark816TransformedRange"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "P15Completion") "benchmark816RationalPrice"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "P15Completion") "rhoStarEnclosure"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "P15Completion") "badWitness_union_bound"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "P15Completion") "exists_minimalForbidden_subset"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "P15Completion") "minimalForbidden_union_bound"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "localCover_amalgamation_of_safety"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "localCover_amalgamation"),
  (Name.str (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "LocalGroundRegression") "twoBlock_emptyLocalCover"),
  (Name.str (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "LocalGroundRegression") "ambientLocalCover_fails"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "mem_selectedFinset"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "coe_bernoulliWeights"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "bernoulliWeights_sum"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "bernoulli_product_weight"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "bernoulli_sum_coe"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "bernoulli_good_sum_coe"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "bernoulli_restriction_sum_coe"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "restrictionIndicator_dependsOn"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "goodIndicator_le_prod_restrictionIndicator"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "bernoulli_tensor_good_coe"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "bernoulli_tensor_restriction_coe"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "bernoulli_tensor_good"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "bernoulli_tensor_restriction"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "muOf_le_prod_restrictionMass_rpow"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "nnreal_prod_rpow_le_affine"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "nnreal_weightedHolder"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "functionDependsOn_update"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "functionDependsOn_coordinateAverage"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "coordinateAverage_eq_of_not_mem"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "coordinateAverage_prod_rpow"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "productAverage_mono"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "finner_productAverage"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "functionDependsOn_coordinateAverage_erase"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "functionDependsOn_productAverage"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "productAverage_eq_of_complete"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "tensor_weights_sum"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "tensorAverage_const"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "tensorAverage_coordinateAverage"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "tensorAverage_productAverage"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "productAverage_eq_tensor"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "finner_tensor"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "restrictionMass_eq_ambient"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "restrictionMass_reindex"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "reindexedRestriction_isProper"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "genPrice_reindex"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "restrictionHazardStar_pos"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "restriction_fullGroundPriceBound"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "restriction_genPrice_le_hazard_ratio"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "restrictionMass_pos_of_muOf_pos"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "famPrice_le_sum_restriction_hazard_ratios"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "weightedHazard_of_productBound"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "witnessLoad_budget_of_weightedHazard"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "witnessLoad_budget_of_productBound"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "emptyWitnessFamily_coverCost"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "sum_block_functions"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "weight_eq_prod_blockWeight"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "localMass_nonneg"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "localMass_le_one"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "localMass_emptyBlock"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "muOf_le_prod_localMass"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "localMass_pos_of_muOf_pos"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "muOf_eq_zero_of_localMass_zero"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "independentBlockHazard"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "sum_phi_le_hazard"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "famPrice_nonneg"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "famPrice_biUnion_le"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "coverCost_le_family"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "emptyGenerator_cover"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "coverCost_le_one"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "exists_capped_cover_of_hazard"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "budget_of_union_cover"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "paletteSeparated_budget"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "paletteSeparated_coverCost"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "exists_minimalBad_subset"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "minimalBad_nonempty"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "proper_subset_good_of_minimal"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "crossing_block_inter_ssubset"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "paletteSafety_iff"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "decomposable_iff_union"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "decomposable_iff_unionCoverable"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "generatorCover_iff_historical"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "decreasing_of_downwardClosed_muOf_pos"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "high_mass_pos"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "decreasing_of_high_mass"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "mem_downwardHull"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "subset_downwardHull"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "decreasing_downwardHull"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "muOf_le_downwardHull"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "unionCoverable_downwardHull_iff"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "prizeStatement_iff_downset"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "cappedHazard_le_half_of_high_mass"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "famPrice_const"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "threshold_cover_of_paletteCertificate"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "ThresholdStatement_of_certificates"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "witnessCoordinateLoad_le_maximum"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "maximumWitnessLoad_empty"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "maximumWitnessLoad_pos"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "maximumWitnessLoad_attained"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "normalize_incident_load"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "witnessLoad_budget"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "witnessLoad_coverCost"),
  (Name.str (Name.str (Name.str Name.anonymous "UniversalLaw") "General") "maximumWitnessLoad_budget"),
  (Name.str (Name.str (Name.str Name.anonymous "ClosedProof") "Endpoints") "reuse_PaletteNumberAttained"),
  (Name.str (Name.str (Name.str Name.anonymous "ClosedProof") "Endpoints") "reuse_MinimalForbiddenCharacterisation"),
  (Name.str (Name.str (Name.str Name.anonymous "ClosedProof") "Endpoints") "reuse_LocalRestriction"),
  (Name.str (Name.str (Name.str Name.anonymous "ClosedProof") "Endpoints") "reuse_LocalDecomposability"),
  (Name.str (Name.str (Name.str Name.anonymous "ClosedProof") "Endpoints") "reuse_LocalObstructionIsFullBlock"),
  (Name.str (Name.str (Name.str Name.anonymous "ClosedProof") "Endpoints") "reuse_LocalPriceChain"),
  (Name.str (Name.str (Name.str Name.anonymous "ClosedProof") "Endpoints") "reuse_IndependentBlockHazard"),
  (Name.str (Name.str (Name.str Name.anonymous "ClosedProof") "Endpoints") "reuse_FullBlockCoverIff"),
  (Name.str (Name.str (Name.str Name.anonymous "ClosedProof") "Endpoints") "reuse_CoverCostHazardBound"),
  (Name.str (Name.str (Name.str Name.anonymous "ClosedProof") "Endpoints") "reuse_WholeGroundChromaticNumber"),
  (Name.str (Name.str (Name.str Name.anonymous "ClosedProof") "Endpoints") "reuse_ElementaryPaletteFormula"),
  (Name.str (Name.str (Name.str Name.anonymous "ClosedProof") "Endpoints") "reuse_TriangleNeedsThree"),
  (Name.str (Name.str (Name.str Name.anonymous "ClosedProof") "Endpoints") "reuse_Benchmark816IsRealized"),
  (Name.str (Name.str (Name.str Name.anonymous "ClosedProof") "Endpoints") "reuse_Benchmark816Palette"),
  (Name.str (Name.str (Name.str Name.anonymous "ClosedProof") "Endpoints") "reuse_Benchmark816Cover"),
  (Name.str (Name.str (Name.str Name.anonymous "ClosedProof") "Endpoints") "reuse_Benchmark816WholeGround"),
  (Name.str (Name.str (Name.str Name.anonymous "ClosedProof") "Endpoints") "reuse_Benchmark816MinimalForbiddenCounts"),
  (Name.str (Name.str (Name.str Name.anonymous "ClosedProof") "Endpoints") "reuse_Benchmark816Price"),
  (Name.str (Name.str (Name.str Name.anonymous "ClosedProof") "Endpoints") "reuse_Benchmark816UnionBound"),
  (Name.str (Name.str (Name.str Name.anonymous "ClosedProof") "Endpoints") "reuse_TwoCoordGeneratorPrices"),
  (Name.str (Name.str (Name.str Name.anonymous "ClosedProof") "Endpoints") "reuse_DemandOneRefutation"),
  (Name.str (Name.str (Name.str Name.anonymous "ClosedProof") "Endpoints") "reuse_LogOnePlusBelowIdentity"),
  (Name.str (Name.str (Name.str Name.anonymous "ClosedProof") "Endpoints") "reuse_LogRatioBound"),
  (Name.str (Name.str (Name.str Name.anonymous "ClosedProof") "Endpoints") "reuse_RatioExponentBound"),
  (Name.str (Name.str (Name.str Name.anonymous "ClosedProof") "Endpoints") "reuse_RestrictedLocalBudget"),
  (Name.str (Name.str (Name.str Name.anonymous "ClosedProof") "Endpoints") "reuse_RestrictedTransformedPriceBudget"),
  (Name.str (Name.str (Name.str Name.anonymous "ClosedProof") "Endpoints") "reuse_RhoTestSufficient"),
  (Name.str (Name.str (Name.str Name.anonymous "ClosedProof") "Endpoints") "reuse_CapTestAtTwoThirds"),
  (Name.str (Name.str (Name.str Name.anonymous "ClosedProof") "Endpoints") "reuse_Benchmark816TransformedRange"),
  (Name.str (Name.str (Name.str Name.anonymous "ClosedProof") "Endpoints") "reuse_Benchmark816RationalPrice"),
  (Name.str (Name.str (Name.str Name.anonymous "ClosedProof") "Endpoints") "reuse_FullTransformedPriceBudget"),
  (Name.str (Name.str (Name.str Name.anonymous "ClosedProof") "Endpoints") "reuse_RhoStarEnclosure"),
  (Name.str (Name.str (Name.str Name.anonymous "ClosedProof") "Endpoints") "reuse_RhoStarBelowSixSevenths"),
  (Name.str (Name.str (Name.str Name.anonymous "ClosedProof") "Endpoints") "reuse_HazardStarPositive"),
  (Name.str (Name.str (Name.str Name.anonymous "ClosedProof") "Endpoints") "reuse_CoordinatewiseConcavity"),
  (Name.str (Name.str (Name.str Name.anonymous "ClosedProof") "Endpoints") "reuse_HazardProductBound"),
  (Name.str (Name.str (Name.str Name.anonymous "ClosedProof") "Endpoints") "reuse_HazardPhiBound"),
  (Name.str (Name.str (Name.str Name.anonymous "ClosedProof") "Endpoints") "reuse_FullGroundPriceBound"),
  (Name.str (Name.str (Name.str Name.anonymous "ClosedProof") "Endpoints") "reuse_PhiAtPStar"),
  (Name.str (Name.str (Name.str Name.anonymous "ClosedProof") "Endpoints") "reuse_FullGroundBudgetIff"),
  (Name.str (Name.str (Name.str Name.anonymous "ClosedProof") "Endpoints") "reuse_CapacityHazardIsBinomial"),
  (Name.str (Name.str (Name.str Name.anonymous "ClosedProof") "Endpoints") "reuse_OddMajorityIdentity"),
  (Name.str (Name.str (Name.str Name.anonymous "ClosedProof") "Endpoints") "reuse_CapacityWorstCase"),
  (Name.str (Name.str (Name.str Name.anonymous "ClosedProof") "Endpoints") "reuse_HStarExceedsOne"),
  (Name.str (Name.str (Name.str Name.anonymous "ClosedProof") "Endpoints") "reuse_LocalPriceBoundFull"),
  (Name.str (Name.str (Name.str Name.anonymous "ClosedProof") "Endpoints") "reuse_GlobalAssemblyHazard"),
  (Name.str (Name.str (Name.str Name.anonymous "ClosedProof") "Endpoints") "reuse_SharpnessOfRhoStar"),
  (Name.str (Name.str (Name.str Name.anonymous "ClosedProof") "Endpoints") "reuse_DemandOneBoundary"),
  (Name.str (Name.str (Name.str Name.anonymous "ClosedProof") "Endpoints") "reuse_SixSeventhsCertificate")]
end OwnedKernelAuditMutation

open Lean
namespace OwnedKernelAuditMutation
structure Entry where
  name : Name
  info : ConstantInfo
  owner : Name
  source : String
structure Extra where
  name : Name
  owner : Name
  status : String
def hex (s : String) : String :=
  s.toUTF8.foldl (fun acc b => acc ++ (if b.toNat < 16 then "0" else "") ++ String.ofList (Nat.toDigits 16 b.toNat)) ""
def join (a b : String) : String := if a.isEmpty then b else a ++ "/" ++ b
def enc : Name → String
  | .anonymous => ""
  | .str p s => join (enc p) ("s" ++ hex s)
  | .num p n => join (enc p) ("n" ++ toString n)
def kind : ConstantInfo → String
  | .thmInfo _ => "theorem" | .defnInfo _ => "def" | .opaqueInfo _ => "opaque"
  | .axiomInfo _ => "axiom" | .inductInfo _ => "inductive" | .ctorInfo _ => "ctor"
  | .recInfo _ => "rec" | .quotInfo _ => "quot"
def ruleCount : ConstantInfo → Nat
  | .recInfo v => v.rules.length | _ => 0
def expressions (ci : ConstantInfo) : Array Expr := Id.run do
  let mut es := #[ci.type]
  if let some value := ci.value? true then es := es.push value
  if let .recInfo v := ci then
    for rule in v.rules do es := es.push rule.rhs
  return es
def closed (e : Expr) : Bool := !e.hasFVar && !e.hasMVar && !e.hasLooseBVars
def inventory : CoreM (Array Entry × Array Extra × Array (Name × Nat × Nat)) := do
  let env ← getEnv
  let header := env.header
  let mut found : NameSet := {}
  let mut seen : NameSet := {}
  let mut instances : NameSet := {}
  let mut entries : Array Entry := #[]
  let mut extras : Array Extra := #[]
  let mut modules : Array (Name × Nat × Nat) := #[]
  for h : idx in [0:header.moduleNames.size] do
    let owner := header.moduleNames[idx]
    if ownedModules.contains owner then
      if found.contains owner then throwError "duplicate owned module"
      found := found.insert owner
      let data := header.moduleData[idx]!
      if data.constNames.size != data.constants.size then throwError "module inventory size mismatch"
      modules := modules.push (owner, data.constNames.size, data.extraConstNames.size)
      for h : pos in [0:data.constNames.size] do
        let name := data.constNames[pos]
        let identity := Name.str owner (enc name)
        if instances.contains identity then throwError "duplicate owned module occurrence"
        let info := data.constants[pos]!
        let some canonical := env.checked.get.find? name | throwError "owned constant missing from checked environment"
        match Kernel.isDefEq env {} info.type canonical.type with
        | .ok true => pure () | _ => throwError "module occurrence type differs from imported constant"
        if info.name != name then throwError "constant name mismatch"
        entries := entries.push ⟨name, info, owner, "primary"⟩
        seen := seen.insert name
        instances := instances.insert identity
      for name in data.extraConstNames do
        match env.checked.get.find? name with
        | none =>
          if (env.find? name).isSome then throwError "elaborator-only extra is not kernel-owned"
          extras := extras.push ⟨name, owner, "ir_only"⟩
        | some info =>
          if instances.contains (Name.str owner (enc name)) then
            let some old := entries.find? (fun e => e.name == name && e.owner == owner) | throwError "missing seen constant"
            if old.source != "primary" then throwError "ambiguous logical extra ownership"
            extras := extras.push ⟨name, owner, "logical_existing"⟩
          else
            entries := entries.push ⟨name, info, owner, "extra"⟩
            extras := extras.push ⟨name, owner, "logical_added"⟩
            seen := seen.insert name
            instances := instances.insert (Name.str owner (enc name))
  if found.size != ownedModules.length then throwError "missing owned module"
  for target in explicitTargets do
    if !seen.contains target then throwError "explicit theorem missing from owned module inventory"
    let some (.thmInfo _) := env.checked.get.find? target | throwError "explicit target is not a theorem"
  return (entries.qsort (fun a b => if a.owner == b.owner then enc a.name < enc b.name else enc a.owner < enc b.owner), extras, modules)
def dumpInventory : CoreM Unit := do
  let (entries, extras, modules) ← inventory
  for (owner, primary, extra) in modules do
    IO.println s!"OWN_MODULE|{enc owner}|{primary}|{extra}"
  let owned := entries.foldl (init := ({} : NameSet)) (fun s e => s.insert e.name)
  for e in entries do
    let origin := if (← findDeclarationRanges? e.name).isSome then "user" else "aux"
    let body := if e.info.hasValue true then "body" else "primitive"
    let safety := if e.info.isUnsafe then "unsafe" else "safe"
    let totality := if e.info.isPartial then "partial" else "total"
    IO.println s!"OWN_CONST|{enc e.owner}|{enc e.name}|{kind e.info}|{origin}|{body}|{ruleCount e.info}|{safety}|{totality}|{e.source}"
    let mut deps : NameSet := {}
    for expr in expressions e.info do
      for dependency in expr.getUsedConstants do
        if owned.contains dependency then deps := deps.insert dependency
    let encoded := (deps.toArray.map enc).qsort (· < ·)
    IO.println s!"OWN_DEP|{enc e.owner}::{enc e.name}|{String.intercalate "," encoded.toList}"
  for e in extras do IO.println s!"OWN_EXTRA|{enc e.owner}|{enc e.name}|{e.status}"
  IO.println s!"OWN_INVENTORY_COMPLETE|{modules.size}|{entries.size}|{extras.size}"
structure Closure where
  seen : NameSet := {}
  axioms : NameSet := {}
partial def collect (env : Environment) (name : Name) : StateT Closure CoreM Unit := do
  unless (← get).seen.contains name do
    modify fun s => {s with seen := s.seen.insert name}
    let some ci := env.checked.get.find? name | throwError "transitive constant missing from kernel environment"
    if let .axiomInfo _ := ci then modify fun s => {s with axioms := s.axioms.insert name}
    for expr in expressions ci do expr.getUsedConstants.forM (collect env)
    if let .inductInfo v := ci then v.ctors.forM (collect env)
def checkType (env : Environment) (e : Expr) : CoreM Unit := do
  if !closed e then throwError "OWN_REJECT_OPEN_TYPE"
  let inferred ← match Kernel.check env {} e with
    | .ok t => pure t | .error _ => throwError "OWN_REJECT_TYPE_KERNEL"
  match Kernel.whnf env {} inferred with
  | .ok (.sort _) => pure ()
  | _ => throwError "OWN_REJECT_TYPE_SORT"
def checkedBody (env : Environment) (ci : ConstantInfo) : CoreM Unit := do
  let some value := ci.value? true | throwError "owned body missing"
  if !closed value then throwError "OWN_REJECT_OPEN_BODY"
  let inferred ← match Kernel.check env {} value with
    | .ok t => pure t | .error _ => throwError "OWN_REJECT_BODY_KERNEL"
  match Kernel.isDefEq env {} inferred ci.type with
  | .ok true => pure () | _ => throwError "OWN_REJECT_BODY_TYPE"
  let fresh := Name.str `OwnedKernelAuditMutation.Rechecked (enc ci.name)
  let declaration ← match ci with
    | .defnInfo v => pure (Declaration.defnDecl {v with name := fresh, all := [fresh]})
    | .thmInfo v => pure (Declaration.thmDecl {v with name := fresh, all := [fresh]})
    | .opaqueInfo v => pure (Declaration.opaqueDecl {v with name := fresh, all := [fresh]})
    | _ => throwError "unsupported body-bearing declaration"
  match env.addDeclCore 0 0 declaration none false with
  | .ok _ => pure () | .error _ => throwError "OWN_REJECT_DECLARATION"
def permitted (closure : Closure) : CoreM Unit := do
  for name in closure.axioms do
    if name != `propext && name != `Classical.choice && name != `Quot.sound then
      throwError "OWN_REJECT_FORBIDDEN_AXIOM"
def collectEntry (env : Environment) (ci : ConstantInfo) : StateT Closure CoreM Unit := do
  if ci.isAxiom then modify fun s => {s with axioms := s.axioms.insert ci.name}
  for expr in expressions ci do expr.getUsedConstants.forM (collect env)
  if let .inductInfo v := ci then v.ctors.forM (collect env)
  modify fun s => {s with seen := s.seen.insert ci.name}
def audit (selected : List (Name × Name)) : CoreM Unit := do
  let env ← getEnv
  let (entries, _, _) ← inventory
  let mut done : NameSet := {}
  let mut selectedEntries : Array Entry := #[]
  for (owner, name) in selected do
    let identity := Name.str owner (enc name)
    if done.contains identity then throwError "duplicate selected constant"
    done := done.insert identity
    let some e := entries.find? (fun e => e.name == name && e.owner == owner) | throwError "selected constant not owned"
    selectedEntries := selectedEntries.push e
    let ci := e.info
    if ci.isUnsafe || ci.isPartial then throwError "unsafe or partial owned declaration"
    if ci.isAxiom then throwError "new owned axiom"
    checkType env ci.type
    let mut bodyStatus := "absent"
    let mut declarationStatus := "primitive"
    if ci.hasValue true then
      checkedBody env ci
      bodyStatus := "checked"
      declarationStatus := "checked"
    if let .recInfo v := ci then
      for rule in v.rules do
        if !closed rule.rhs then throwError "open recursor reduction rule"
        match Kernel.check env {} rule.rhs with
        | .ok _ => pure () | .error _ => throwError "recursor rule body kernel check failed"
    IO.println s!"OWN_CHECK|{enc e.owner}|{enc name}|{kind ci}|checked|{bodyStatus}|{declarationStatus}|{ruleCount ci}"
  let (_, closure) ← (selectedEntries.forM (fun e => collectEntry env e.info)).run {}
  permitted closure
  let encoded := (closure.axioms.toArray.map enc).qsort (· < ·)
  IO.println s!"OWN_AXIOMS|{String.intercalate "," encoded.toList}"
  IO.println s!"OWN_CLOSURE|{closure.seen.size}"
  IO.println s!"OWN_AUDIT_COMPLETE|{selected.length}"
end OwnedKernelAuditMutation

