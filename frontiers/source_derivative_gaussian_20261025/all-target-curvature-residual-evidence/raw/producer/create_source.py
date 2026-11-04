from pathlib import Path
base=Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
old=(base/'SourceCurvatureDecomposition.lean').read_text()
first=old[old.index('def curvatureResidualRadius '):old.index('def curvatureEnvelopeTotal ')]
second=old[old.index('theorem sourceDerivativeMajorant_curvatureReconstruct '):old.index('theorem curvaturePosterior_residual_eq_shift ')]
third=old[old.index('theorem curvatureResidualRadius_image_bound '):old.index('theorem curvatureResidualRadius_uniform_bounds ')]
s=first+second+third
s=s.replace('sourceContactQ_posterior_abs_le_radius','sourceContactQ_posterior_abs_le_allTargetRadius')
s=s.replace('sourceDerivativeMajorant_curvatureReconstruct','sourceDerivativeMajorant_allTarget_curvatureReconstruct')
s=s.replace('sourceGammaRadius_curvatureReconstruct','sourceGammaRadius_allTarget_curvatureReconstruct')
s=s.replace('curvatureResidualRadius','allTargetCurvatureResidualRadius')
s=s.replace('(sourcePrescribedPins r b)', 'p')
s=s.replace('(r b q : ℝ)', '(r : ℝ) (p : Fin 6 → ℝ) (q : ℝ)')
s=s.replace('(r b : ℝ)', '(r : ℝ) (p : Fin 6 → ℝ)')
s=s.replace('hL r b', 'hL r p')
s=s.replace('sourceSmoothLaw hL r p','sourceSmoothKernel hL r p')
s=s.replace('rw [sourceSmoothLaw,sourceSmoothKernel_apply]', 'rw [sourceSmoothKernel_apply]')
header='''import SourceCompactTargetMoments
import SourceCurvatureDecomposition

/-!
# Whole-carrier all-target curvature residual bounds

The radius is the original Gamma of the literal posterior sample at every
six-vector target. One interval chosen from L != 0 controls reconstruction,
residual images and all polynomial moments under the actual residual law.
The covariance direction is independent of the target; its existing envelope
is taken at b=0. Existing whole-carrier scalar/product laws and densities are
reused without a second construction. No weighted or normalized probability
conclusion is asserted.
-/

noncomputable section

open I4Foundation I4Source I4Smooth I4SmoothCarrier I4SourceGaussian
open I4SourceDerivativeGaussian I4SourceConfluentPins I4SourceConfluentLimits
open I4SourceEndpointRegression I4SourceEndpointEstimates I4SourceSmoothConditional
open I4SourceConditionalMajorant I4SourcePinCurvatureBounds I4SourceSmoothPalm
open I4SourceCurvatureDecomposition I4SourceCompactTargetMoments I4GaussianMajorant
open I4ContactGram MeasureTheory ProbabilityTheory Filter
open scoped BigOperators Topology

set_option autoImplicit false

namespace I4SourceAllTargetCurvatureResidual

/-- The original posterior radius, at every literal target. -/
'''
(base/'SourceAllTargetCurvatureResidual.lean').write_text(header+s)
