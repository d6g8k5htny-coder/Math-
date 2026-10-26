# Actual norm-Borel derivative and jet realization

The read-only proposal was adopted for production by
`SOURCE_SMOOTH_TOPOLOGY.md`, frozen at commit `9d999aa`. Sole production author:
OpenAI/Codex `/root/uniform_jet_moment_sources`; sole file `SourceSmoothTopology.lean`
in `/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025`.
Existing source modules and input artifacts remain unchanged and their applicable
verification is reused. This is coauthor mathematics, not independent scientific review.

## Exact source requirement

Published GP-DER-197 is available at `/workspace/scratch/GP-DER-197-published-source.txt`,
public main blob `13067e7547e4f1913dd55cf5173fe5b02b6f9816`. Its frozen body is declared
as 13,797 bytes / SHA256 `035d5a18018606bd8736dc5774a7adbed29de453b30a1780976e1e4f69285d4d`.
Section 1, lines 211–253 of that export, uses `X=C^3(T_L^2;ℝ)` with its usual C3 norm,
separable Banach/Borel field law, and continuity of gradient from C3 to C2 and C1.
Its source-level Borel globalization conversion requirement is separate from the
mathematics reused here; no scientific status or review transfer is asserted.

The previous literal coefficient carrier and its canonical conditional kernel are
correct for their measurable structures. Their scalar-coordinate product field map
alone does not prove a norm-topology field-space Borel map.

## Bounded implementation requirements

For every natural d,k and L≠0, define

`DerivativeOperator d k := ContinuousMultilinearMap ℝ (fun _ : Fin k => Fin d → ℝ) ℝ`,

and the normed bounded-continuous-function space
`DerivativeBCF d k := (Fin d → ℝ) →ᵇ DerivativeOperator d k`.

1. Form each deterministic `modeDerivativeBCF` from actual differentiated Fourier
   modes, their proved smoothness and the existing global `orderModeBound`.
2. For EVERY sample in `SmoothSample d L`, derive summability in BCF norm of
   `ω_m • modeDerivativeBCF m` from that sample's all-order weighted summability.
   The resulting BCF must equal the actual `iteratedFDeriv` at every source point.
3. Prove convergence of finite Fourier sums uniformly in the real source variable,
   via norm convergence in BCF. No a.e.-only replacement is allowed.
4. Derive strong measurability from strongly measurable finite coefficient sums and
   their every-sample limit. The generic limit API needs only a pseudometrizable
   topological additive codomain; no global separability of BCF is assumed.
5. State explicit Borel measurability for the NORM topology of the derivative BCF.
6. Repeat strong measurability in the WHOLE finite Banach jet tuple through K,
   then derive its norm-Borel measurability directly. Do not infer this from a
   product of coordinate measurable spaces: those Borel structures can differ
   when the full BCF spaces are nonseparable.
7. Include K=0, k=0 and d=0. The zeroth multilinear operator evaluated at the
   unique empty tuple must recover the literal field value.
8. Restrict along continuous compact-chart parameters by the continuous,
   norm-nonincreasing BCF restriction operator. The restricted values are the
   actual ambient derivatives at the chart image; differentiation of an arbitrary
   continuous parameterization is not asserted.
9. For d=2, compose the exact canonical smooth-source kernel with these proved
   norm-Borel maps. Export actual HasCondDistrib for derivatives, whole finite
   jets, compatible periodic jets, and every measurable norm-jet functional.
   Final small-positive-radius exports derive current invertibility from L≠0.

## Existing exact APIs used

- `SourceSmooth.lean`: actual all-order goodSample event and global mode bounds.
- `SourceDerivativeGaussian.lean`: actual every-sample derivative series.
- `SourceSmoothCarrier.lean`: every-sample source smoothness, unchanged carrier/law.
- `SourceSmoothConditionalKernel.lean`: literal all-pin conditional kernel and
  generic measurable-functional HasCondDistrib, with hL-only eventual specialization.
- Mathlib `Bounded/Normed.lean`: `ofNormedAddCommGroup`, norm bounds and continuous
  norm-nonincreasing restriction; `Bounded/Basic.lean`: Banach completeness,
  evaluation continuous linear maps, and norm/uniform convergence equivalence.
- Mathlib `stronglyMeasurable_of_tendsto`, applied to the countably generated
  finite-subset summation filter. Explicit norm Borel follows strong measurability.

Only new code is checked. Original failed scratch/compiler outputs and source
snapshots remain in this directory. A failed whole-file attempt is not counted as
a successful standalone artifact; final integrated production checks bind final bytes.

## Precise compatible-jet interface

The implementation defines `compatiblePeriodicJets d L K` by existence of one
actual C^K real-cover field f, lattice periodicity of f, and equality of every
jet component to the actual derivative of f. Boundedness is supplied by the BCF
components themselves. Actual source jets are proved members, and every derivative
is proved lattice periodic. The global zeroth jet recovers the field; equality of
source jet tuples is equivalent to equality of their global real-cover fields.

The metric is identified explicitly: a jet distance is ≤ε, for ε≥0, exactly when
the operator-norm derivative distance is ≤ε for every order through K and every
real source point. Thus the topology is the maximum uniform derivative topology.
The compatible subtype inherits that topology and its Borel structure; its actual
source lift and conditional law use the inherited norm Borel structure.

This is an accurate bounded-periodic C^K jet model. It is not a value-only
identification on an arbitrary compact set, nor a declaration that the whole
nonperiodic BCF ambient space is separable.

## Remaining C3-torus/capture application join

The present module does not itself construct the conventional C3 torus Banach type,
prove its completeness/separability, or install GP-DER-197's branch/flow selector.
To identify that conventional space with the compatible periodic jet model, the
successor interface must establish the following, rather than assume a measurable
realization:

1. Pullback of every C3 torus field along the exact quotient projection yields the
   corresponding bounded periodic real-cover C3 jets. Conversely a compatible
   periodic jet witness descends uniquely to the torus, with local derivative
   identification in the flat quotient charts. Zeroth-jet uniqueness gives the
   bijection.
2. Show that the induced maximum uniform derivative norm is equivalent to the
   chosen usual C3 norm. A sum convention differs from a maximum by at most a
   factor K+1; changes between Euclidean and source coordinate/operator norms need
   the appropriate finite-dimensional constants. Do not claim an isometry without
   fixing the norm convention.
3. Use compactness/periodicity to identify global-cover uniform norms with norms
   on a compact fundamental cell, including boundary compatibility. A global
   continuous torus-to-real representative must not be assumed: the existing
   `torusRepresentative` is measurable, and a continuous global section does not
   exist. Quotient descent or a finite compatible chart cover is the correct route.
4. For the dynamical interface, identify gradient and its C1 jets by the actual
   contractions of the first and second derivative fields. These contractions
   are continuous linear maps; prove their equality to the physical gradient
   vector field and its derivative before applying the C1-flow framework.
5. Only after that explicit homeomorphism/continuous interface may the given
   C3-Borel capture event be pulled back as a Borel coefficient-carrier event.

The existing torus projection/pullback and chart-transition results are reusable
mathematics. The a.e. torus C4 theorem does not itself supply this norm-valued Borel
map. The new norm-Borel derivative/jet theorem remains proved even while this
separate conventional-C3/dynamical application join is pending.
