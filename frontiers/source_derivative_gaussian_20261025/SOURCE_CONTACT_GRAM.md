# Contact pin covariance certificate: frozen before code

25 October 2026. OpenAI/Codex root and /root/regression_kernel.
This is a prerequisite of the actual conditioning research, scientific effect NONE.

The primary GP-DER-044 source identity is recorded in the sibling determinant
packet's SOURCE_GAUSSIAN_MOMENTS.md. The concrete Fourier definitions and their
immutable hashes are in this directory's INPUT_BINDING.json. SourceFourierSeries
uses false=cos and true=sin on halfLattice modes with positive amplitudes.
SourceCovariance.scalarSeries_covariance gives the exact coefficient Gram sum.
SourceDerivativeGaussian's separately frozen contract connects differentiated
mode coefficients to the literal smooth source.

Frozen sole new ContactJetCovariance.lean: in row order
(f,fx,fy,fxx,fxy,fxxx,fyy), use columns
(DC,cos(1,0),cos(0,1),cos(1,1),sin(1,0),sin(2,0),sin(0,1)).
Before multiplying each column by its nonzero amplitude, the explicit rows are

    [1,1,1,1,0,0,0]
    [0,0,0,0,c,2*c,0]
    [0,0,0,0,0,0,c]
    [0,-c^2,0,-c^2,0,0,0]
    [0,0,0,-c^2,0,0,0]
    [0,0,0,0,-c^3,-8*c^3,0]
    [0,0,-c^2,-c^2,0,0,0].

Prove injectivity of its transpose (including arbitrary nonzero column
amplitudes) for c!=0. A determinant formula is optional; it is not a premise.
Prove the infinite Gram consequence: any coefficient array coeff : Fin 7 ->
iota -> Real with each row summable, and seven selected columns exactly equal
to the displayed columns times nonzero amplitudes, has positive-definite
Gram matrix G_ij = sum' m, coeff_i(m)*coeff_j(m). No independence, positivity
or invertibility of G may be assumed. Derive the needed summability and the
sum-of-squares quadratic-form identity. A 6+1 block Schur-complement positivity
consequence may be added, proved from PosDef rather than assumed.

In the actual source c=2*pi/L!=0, DC amplitude=sqrt(1/sourceZ), and other
amplitudes=sqrt(2*sourceWeight/sourceZ)>0. The listed lattice modes satisfy the
canonical half-lattice convention. These coefficient-row identities and exact
physical covariance identification must still be proved for an actual-source
PosDef claim; a generic certificate alone does not discharge that application.
Do not claim the physical pin Gram or reference variance from an uninstantiated
certificate. Contact A=fxxy is allowed correlated or degenerate; only Q's
conditional variance must be positive for the normalizer reference theorem.

Narrow pinned imports, no old-source changes, no custom axioms or assumed
conclusion. Preserve initial failed attempts and reuse existing verification.
Root alone integrates source inventory/evidence; scientific review is separate.
