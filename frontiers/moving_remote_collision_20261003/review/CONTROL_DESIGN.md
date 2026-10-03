# Independent control design, frozen before author-checker exposure

Reviewer: OpenAI Codex `/root/c107_nonauthor_review`, nonauthor of C107.
Same-provider / organizational independence credit: 0. Human review: NONE.
The reviewer read the full frozen analytic object, but no author checker, test
results, or checker design. No proof-design contribution was supplied before
freeze. This file records the independent design before implementation.

Frozen analytic target: `../PROOF.md`, 29,606 bytes, SHA256
`d94f8f2f7e809da37465729d3eca5f9793bce5fc5410d9f83e61db259ddf73df`.
Frozen source manifest: `../SOURCE_IDENTITIES.json`, 2,931 bytes, SHA256
`f03da4be8cae14588d7e6e1d215091293dbad199bc9a0013cccca995a4c05a8c`.
All six sources were independently compared byte-for-byte to `git show` at
Math- cut `7e2344166e989ae94e5732e445f445598fc75c4c` before this review.

## Controls to implement without reading author controls

1. **Actual periodic duals, not merely local polynomials.** Represent a
   trigonometric polynomial exactly over rational sin/cos variables, with exact
   physical derivative operators. Select torus points with rational sine and
   cosine using the tangent-half-angle parameterization. Construct a two-site
   Hermite polynomial after the sine-chart transformation, multiply by two
   periodic separators, and check exact surviving values/full physical
   gradients and exact killed values/gradients. Use a nonaxis chord and unequal
   coordinate cosines. Vary rational parameters so both the killed and surviving
   pairs approach confluence. Independently test the separated-witness singleton
   construction using three separators and an affine chart interpolant.
   Negative variants: omit the inverse-chart gradient chain rule; omit one
   killed-site separator; replace the periodic separator by an affine factor
   (a simple zero does not kill the gradient).
2. **Confluence and cancellation.** On rational univariate polynomial data of
   degrees 0 through at least 6, compute Hermite coefficients directly from
   endpoint jets and independently from the integral identities. Check exact
   normalized pin and witness right inverses for basis data. Use rational
   shrinking gaps to expose uncancelled terms. Negative variants: wrong cubic
   factor, wrong mixed coefficient, and omitted pin cubic correction.
3. **Regression-energy stress case.** Use an exact covariance model
   `U=G1`, `V=G1+epsilon G2`, `Z=G2`, with independent standard normals and
   `epsilon=rho^7`. Its conditional variance is `epsilon^2` and the regression
   shift is exactly `t/epsilon`; check the Schur floor and square-root energy
   identity by rational algebra. Reject a rho-independent or rho^-6 conditional
   moment bound. Separately check six-dimensional determinant/density and
   eighth-moment powers and a covariance with both small and O(1) eigenvalues
   to distinguish the density prefactor from the uniform tail scale.
4. **Collision geometry and integration.** Use the exact planar fold
   `f(s,z)=s^3/3-a^2 s+z^2/2` at `s=+-a`. Check the height-difference coordinate,
   both small Hessian determinants, and the raw-to-regularized six-coordinate
   determinant using rational elimination. Independently integrate the radial
   bound at `a=q^3` and compare dimensional powers. Reject a dropped witness
   determinant, a wrong raw Jacobian, and a nonsaturating second-window factor.
5. **Scope controls.** Check the alpha threshold strictly, including equality
   at `alpha=1/49` where this bound does not tend to zero after division by
   `r^3`. Check the integer factorial inequalities and separated-volume
   absorption for exact rational parameters. These do not validate any
   inner-ball, mixed-pair, elder, or barcode claim.

All finite checks will use the Python standard library and rational arithmetic.
The written analytic review will separately justify the continuum norm bounds,
all-frame uniformity, simultaneous confluence, Gaussian conditioning, full
normalizer, and the marked Kac–Rice/exhaustion hypotheses. Passing controls
cannot replace those arguments or provide organizational independence.
