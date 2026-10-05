# C107 author finite controls — design and boundary

These controls are author-side support for the frozen planar C107 proof. They confer no nonauthor independence or scientific acceptance. They use only Python's standard library, exact Fraction arithmetic, exact Gaussian-rational complex arithmetic, and finite symbolic Laurent polynomials. They perform no network access or source-tree writes.

Target analytic proof: PROOF.md, 29,606 UTF-8 bytes, SHA256 d94f8f2f7e809da37465729d3eca5f9793bce5fc5410d9f83e61db259ddf73df. Exact six-source custody is separately in SOURCE_IDENTITIES.json.

The checker will cover:

1. The six-coordinate endpoint polynomial inverse, including the r-squared corrections and the r=0 contact jet, on a fixed finite set of rational radii and data vectors.
2. The witness divided-difference polynomial inverse, including the 6 delta D quadratic term, negative cubic sign and -1/12 contact constant.
3. Cubic Hermite interpolation of value/axial derivatives, affine interpolation of transverse derivatives, and the integral cancellation identities in formula (25), using monomials through degree eight and shrinking rational chord lengths.
4. Actual periodic duals, represented as Laurent polynomials in two unit-circle variables. Rational points on both circles give exact complex phases, so value and physical derivative evaluation are exact. For each ordinary value/gradient basis datum on four distinct sites, construct the two-pair separator/Hermite dual and verify all twelve observations, fixed frequency support, and reality. These tests use a rational secant coordinate basis with endpoints 0 and 1; they test the chain rule and finite Fourier composition exactly, but are not a substitute for the proof's orthonormal-coordinate uniform stability argument.
5. The quotient derivative and inverse sine-chart derivative in that construction. Both axes are varied at the witness pair; ordinary physical coordinates are not identified with chart coordinates.
6. The singleton construction with three separators, including a distant-witness configuration for which a single global sine chart is noninjective. No inversion of that global chart is attempted.
7. The fourth-order zero of a repeated separator: all derivatives through total order three vanish, and a second derivative of a single factor does not.
8. The exact raw-to-V determinant, scalar covariance/regression-energy sharpness, and the exponents 7, 14, 42, 56 and 98.
9. The near-pair radial integral for rational cube window parameters, the full normalizer cancellation, separated-branch absorption factor, the moving-cutoff exponent, and ordered-pair counting inequalities.

Substantive mutants must be rejected by the corresponding operational checks. They include incorrect endpoint corrections, incorrect D polynomial terms, the wrong trapezoid constant, incorrect Hermite coefficients, omitted quotient and sine-chart derivative factors, insufficient repeated-separator order, a missing separated-witness separator, a missing raw Jacobian power, a missing small witness determinant, incorrect covariance/density/regression powers, extra normalization, and treating the ordered count as unordered.

The tests do not prove the reciprocal derivative estimates uniformly over the torus, the uniform C3 Hermite coefficient bound for arbitrary functions, the Gaussian Hilbert-space projection argument, covariance floors over all parameters, global smooth sample-path convergence, Kac–Rice or genericity hypotheses, the imported full normalizer, or any elder/barcode claim. The proof and its nonauthor mathematical review must establish those points. The finite rational fixtures neither approximate the original covariance nor assert a numerical lower covariance constant.

Execution is bounded and deterministic. Checks use explicit exceptions rather than Python assert, so optimization cannot disable them. Normal and -O runs should have byte-identical stdout; the script prints its Python version but no timestamps. The author run record will retain the exact script/design identities and runtime, and will distinguish successful execution from theorem verification.
