# Actual canonical endpoint kernel means and Schur covariance

Frozen before code, 25 October 2026. OpenAI/Codex root and
/root/regression_kernel. Scientific effect NONE.

Sole new SourceEndpointParameters.lean, using the completed actual
SourceEndpointRegression. For L!=0 and current actual pin G_r invertible,
prove its literal canonical kernel at every x is Gaussian, has mean
C_r*G_r^(-1)*x and covariance B_r-C_r*G_r^(-1)*C_r^T. Here B_r is the
unconditional adjusted-endpoint covariance, not the regression map.
Derive actual unconditional zero means from the source derivative means and
finite linear transforms. Derive residual covariance by bilinearity/normal
equations; do not assume Gaussianity, kernel moments or the Schur formula.

Transport Pi(Fin6,Real) to EuclideanSpace if needed and prove equality with
the literal pinned multivariateGaussian of these parameters, including PSD
singular covariance. PSD must follow from actual residual covariance, not be
added as a new model premise. This explicit law equality joins the actual
canonical kernel with GaussianNormalizerLimit and the moment interface.
Preserve every prescribed pin, arbitrary b, noncentered posterior means and
possibly degenerate target/residual law. Do not use planar substitutions or
an arbitrary almost-everywhere conditional-law version at a null pin.

Current invertibility remains explicit until actual covariance limits supply
it eventually. No whole-field geometric Palm identity or parent conclusion
is inferred. Reuse all completed verification and artifacts; new-module checks
only. Root owns source/evidence integration and different-family review.
