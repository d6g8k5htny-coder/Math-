# Independent nonauthor review of the higher-configuration dual floor and torus transfer

Date: 16 October 2026 UTC.

**Verdict: ACCEPT_SCOPED for Sections 3–4, equations (6)–(14), of the frozen proposal. No blocking mathematical defect and no required author amendment were found in this scope.** This is a conventional mathematical review of the all-parameter argument, supported by fresh exact finite controls. It is not acceptance of the remainder of the proposal, a field experiment, a formal proof, source admission, or scientific promotion.

Actual reviewer: OpenAI/Codex `/root/c261a_successor_preparation_review_20261016/higher_dual_nonauthor`, dispatched as an actual nonauthor for this frozen artifact. The reviewer is source-exposed and in the same provider organization as the authors. Organizational-independence credit is **0**. The author-side dual-floor attack was read as author evidence after the reviewer reconstructed the central estimates; it receives no nonauthor or independent-review credit here.

Reviewed source: `HIGHER_CONFIGURATION_GAUSSIAN_ROUTE.md`, **32,938 bytes**, SHA-256 `43bd77fd5320a717c77bba28c1a6eec080ff67db56c911c6ddea5351a1279b7e`. Section 3 occupies source lines 94–173; Section 4 occupies lines 175–195. The author freeze manifest is **9,362 bytes**, SHA-256 `8734cda7c1dc3d4d85221980daee7849fdf6a3f250632e68d4af11aad20b3700`.

The reviewed claims retain every stated qualification: planar Gaussian covariance `exp(-|h|^2/2)` at physical correlation length one; each fixed finite p; all distinct Euclidean configurations with minimum separation `0<eta<=1`; arbitrary independent orthonormal frames; and, for the torus transfer, the particular normalized finite Gaussian square truncations and the covariance comparisons already declared in Section 1. Nothing here supplies a p-uniform floor, a different Gaussian correlation scaling, a floor for arbitrary normalized positive spectra, or a numerical conditioning window.

## 1. Fourier normalization and the dual inequality

The stated unitary two-dimensional convention is consistent in both directions. Write

`A_a(xi)=sum_(i,beta) a_(i,beta) (i xi)^beta exp(i x_i.xi)`.

For real a the raw-jet variance is

`Var(L_a F)=(2pi)^(-1) integral |A_a(xi)|^2 exp(-|xi|^2/2) dxi`.

Fourier inversion gives `L_a g=(2pi)^(-1) integral A_a hat(g)`. Applying Cauchy–Schwarz with the two reciprocal Gaussian weights gives exactly equation (7), with

`||g||_*^2=(2pi)^(-1) integral exp(|xi|^2/2)|hat(g)(xi)|^2 dxi`.

There is no extra factor of `2pi`, its reciprocal, or a real/complex coordinate multiplicity. Complex phases do not change Cauchy–Schwarz. Every constructed dual is a polynomial times a Gaussian and therefore has absolutely convergent derivative inversion integrals. No abstract existence assertion about an infinite Gaussian coefficient carrier is needed.

The transform of `exp(-|s|^2/4)` is indeed `2 exp(-|xi|^2)` in two dimensions. Consequently the squared weighted transform of a polynomial multiple is a polynomial times `exp(-3|xi|^2/2)`, which is integrable at every fixed degree. In particular `A_D` is a positive finite number. Translation of the center contributes only a phase of modulus one, so it does not affect this norm.

An exact normalization cross-check is the covariance representer `R(x)=exp(-|x|^2/2)`: its transform is `exp(-|xi|^2/2)` and its squared star norm is one. More generally, for `g_a(x)=exp(-a|x|^2/2)` the same elementary radial Gaussian integral gives `||g_a||_*^2=1/[a(2-a)]` when `0<a<2`. This yields `4/3` for the broad Gaussian used in the dual construction. At a=2 the weighted integral diverges, which is why the chosen Gaussian width matters.

## 2. Interpolation, coefficient bound and exponent

For each fixed i, all factors are expressed in `s=x-x_i`. The reciprocal in the definition of P is needed only as a local Taylor series at zero, where `B_i(0)=1`; the final P is a globally defined polynomial. At the own center, multiplication of Taylor series yields `g_i,beta=s^beta/beta!+O(|s|^4)`. At another center, the explicit factor `|s-h_ij|^4` vanishes to order four, and every other factor is smooth there. These two facts prove all `10p` Kronecker derivative identities through total order three, including mixed derivatives and the factorial normalization.

The degree is at most `4(p-1)+3=4p-1`. The lower floor power in the proposal follows from the square of the norm bound; it is therefore `2(4p-1)=8p-2`. This power is conservative where the geometry is better conditioned, including the singleton case. No sharpness assertion is needed.

The coefficient estimate is valid uniformly over unbounded diameters and unequal separation scales. If `u=q_ij-1`, the weighted coefficient norm satisfies

`||u||_eta <= 2 eta(|h_1|+|h_2|)/|h|^2 + 2 eta^2/|h|^2 <= 2sqrt(2)+2 < 5`.

This uses only `|h|>=eta`. An upper bound on |h| is absent. Multiplication is submultiplicative in this norm, and total-degree truncation can only reduce it. Because u has no constant term, the formal identity for the reciprocal through degree three uses just

`T_3(1+u)^(-2)=T_3(1-2u+3u^2-4u^3)`.

Its norm is at most `1+10+75+500=586`. Each `q^2` has norm at most 36; the exponential reciprocal Taylor factor has norm `1+eta^2/2<=3/2`; and the monomial/factorial factor has norm at most one. Thus the stated `C_p^(0)=(3/2)21096^(p-1)` bounds `||Q||_eta`. For a polynomial of degree at most D and `eta<=1`, its ordinary coefficient sum is at most `eta^(-D)||Q||_eta`. This proves equation (10).

The Fourier triangle inequality now gives `||g_i,beta||_*<=A_D C_p^(0) eta^(-D)`. Applying the dual inequality separately to every Kronecker dual and summing the `10p` inequalities gives

`||a||_2^2 <= Var(L_a F) 10p A_D^2 (C_p^(0))^2 eta^(-2D)`.

This proves the raw covariance floor with the exact constant displayed in equation (11). The derivation does not replace covariance by its diagonal, assume a uniformly bounded global coordinate expansion, or extrapolate a numerical eigenvalue. A far point decreases the nonconstant coefficients of its normalized distance factor. Arbitrarily close pairs at different scales remain covered by the single lower separation eta.

## 3. Tensor normalization and contact selection

For derivative order d, the tensor Frobenius metric on the raw planar symmetric coordinates is `diag(binomial(d,j))`. The W in the proposal is exactly the positive square root of these metrics for d=0,1,2,3. The change of any orthonormal frame, including a reflection, is orthogonal after this weighting. It is generally not orthogonal in the raw unweighted coordinates at orders two and three.

If the raw covariance has floor lambda, weighting gives `W Sigma W >= lambda W^2 >= lambda I`. Orthogonal frame changes preserve the latter bound. Returning from the weighted frame jet to the seven selected contact entries has row Gram matrix, in the proposal's contact order,

`diag(1,1,1,1,1,1/2,1)`.

The mixed second derivative is the sole selected component with a scale loss. The selected third derivative is the pure directional derivative, so no `1/3` loss enters this selection. It follows that the contact covariance has floor at least lambda/2. The `/2` in equation (12) is correct for all independently selected frames. Block diagonal weighting, frame changes and selection give the same conclusion for p centers.

## 4. Torus lifting, graph cycles and image transfer

For fixed p and sufficiently small t the required inequality `p R_t < L/2` follows from `R_t=O(sqrt(log(1/t)))` and `L` of order `t^(-1/3)`. Each tree edge then has a unique shortest torus displacement. Assign lifts by integrating these displacements along a spanning tree of each graph component.

The difference between any two lifted vertices is the sum along the simple tree path between those vertices. The path contains at most q−1 edges, so its Euclidean norm is at most `(q-1)R_t<L/2`. This uses the simple path after cancellation, not a bound by two independent root paths. A vector of norm below L/2 has both coordinates strictly inside the fundamental displacement interval, so it is the unique shortest representative of the corresponding torus displacement. Every lifted pair therefore has the same distance as its torus pair and retains separation at least eta.

For an extra graph edge, the tree path plus that edge contains at most q edges. Its displacement cycle has norm at most `q R_t<L/2<L`; a nonzero vector of `L Z^2` has norm at least L. The cycle therefore has zero winding. This proves consistency around all extra edges, including components crossing either or both seams. The argument does not require comparable internal scales or bounded component diameter independent of t.

Apply equation (12) separately to components of sizes q<=p. Since `eta<=1` and `8q-2<=8p-2`, the finite minimum over q of their positive constants gives a common floor `c'_p eta^(8p-2)` for the block diagonal Euclidean covariance. Singleton components can use the constant one-contact floor. The arbitrary-frame conclusion is inherited component by component.

The extension of the accepted image estimate to the slowly growing lifted region is valid. If a lifted displacement h has norm at most pR_t=o(L), then for any nonzero lattice vector n, eventually `|h+Ln|>=L|n|/2`. Gaussian derivatives through order six are polynomials times a Gaussian; absorbing the polynomial into a weaker Gaussian and summing over nonzero n gives `C_p exp(-cL^2)`. The normalizing image denominator differs from one by the same type of bound. This estimate is uniform in h throughout the lifted region. The accepted normalized truncation error contributes `C_p delta_6` uniformly in h.

Between distinct graph components every torus distance exceeds R_t. The declared finite covariance derivative bound therefore gives `C_p[exp(-R_t^2/8)+delta_6]` for every cross-block entry. Contact covariances require derivatives of order at most six, exactly the order available. Directional-frame expansion costs only a fixed order-dependent coefficient bound. The fixed `7p` row dimension converts the entrywise estimates to operator norm at a p-dependent cost. This proves equation (13), with the target covariance equal to the direct sum of the component Euclidean covariances.

For an inverse logarithmic scale `eta` with a fixed finite logarithmic power, all three errors in Delta_t are little-o of `eta^(8p-2)`. In the declared family, `delta_6<=C exp(-Lambda^2/64)=t^(B/64+o(1))` with B>0; the far term is exactly `t^(A0/8)` with A0>0; and the image term decays faster than every power of t. These estimates beat any fixed power of the logarithm. The ceiling in K changes Lambda by at most `2pi/L`, which does not alter this conclusion. Weyl's inequality then gives equation (14), uniformly over all minimum-separated configurations and frames. If every pair lies beyond R_t, the target blocks are singletons and the same argument yields a constant floor.

This is an eventual statement for each fixed p. The proof would not support p growing with t, a graph radius of order L without a separate lifting argument, or a fixed nonzero covariance error compared against a vanishing separation floor.

## 5. New independent controls and preservation

The newly written `independent_dual_controls.py` uses only Python's standard library, exact rational polynomial arithmetic and exact Gaussian moments. It does not import, execute or replay either author helper script or any previously accepted control. Its final recorded run exited zero and produced `INDEPENDENT_DUAL_CONTROLS.json` with **253 passed checks, including 10 negative controls**.

The controls cover:

* Exact weighted Gaussian-polynomial norms. Squared norms of the base Gaussian, its x multiple, its x-squared multiple and its xy multiple are respectively `4/3`, `16/9`, `16/3` and `64/27`. General polynomial norms are integrated exactly after the Fourier derivative expansion, using independent real and imaginary polynomial parts and a residual Gaussian of variance `1/3` in each frequency coordinate.
* Twenty-one constructed duals over four fresh configurations: a singleton, a close diagonal pair, a three-center configuration with separation `1/4096` and a center at coordinate one million, and an oblique three-center configuration. They check the own-center jet, all other-center vanishing through order three, the actual weighted Fourier norm, the stated coefficient bounds and the resulting norm bound. A common translation by `(10^9,-10^8)` leaves every centered polynomial unchanged.
* Exact symmetric tensor metrics through order three for a rational rotation and a rational reflection, plus the contact selection Gram matrix. Raw unweighted orthogonality and omission of the half loss are rejected.
* A complete four-vertex cluster crossing both torus seams, and a separate multiscale example with two components. Every lifted pair is checked against its exact shortest displacement, including extra graph edges. A winding three-cycle when the small-cluster hypothesis is removed, and failure to lift across the seam, are detected.
* The chosen Gaussian width and Fourier amplitude. The critical narrow width produces a divergent weighted norm; an extra Fourier amplitude contradicts the reproducing norm normalization.

These are finite controls supporting selected identities and failure modes. Their success does not establish the all-parameter bounds by enumeration. The preceding analytic audit is the basis for the scoped verdict.

`FROZEN_INPUT_VERIFICATION.json` records byte readback against all **24** entries comprising the author freeze manifest and its declared consumed inputs/new outputs. All matched their expected byte counts and SHA-256 hashes. Source bytes and manifest identity were also checked on initial read. No author source, prior review, control, primary-source file, native or remote record, Lean artifact, ownership record, or scientific register was modified. All outputs of this review are new files in `higher-configuration-nonauthor-review/dual/`.

Required author amendments: **NONE for Sections 3–4**. Remaining review responsibility: Sections 5 onward and the complete candidate-process theorem remain with the integrating reviewer. This report supplies no verdict on those sections. Source admission **NONE**; scientific effect **NONE**; provider-distinct or organizationally independent review **NOT PROVIDED**.
