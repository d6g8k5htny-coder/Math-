# Height-uniform actual Rice bad-event numerator

26 October 2026. OpenAI/Codex author-side conventional application. Frozen scope: `SOURCE_UNIFORM_HEIGHT_RICE_DEFECT.md` at commit `597c8502623725f25cef9de7ce48156acb44c30f`. Scientific effect **NONE**. This is neither a Lean implementation nor independent acceptance. Completed applicable source qualifications and reviews are reused; no old build, kernel replay, control or mathematical verification was repeated.

## 1. Statement on the actual law

Fix `L ≠ 0`. Throughout, `μ = smoothLaw 2 L` is the unchanged full real Fourier coefficient law on the actual smooth carrier, and `F` is its actual smooth field, including its random constant mode. Write

\[
x_r=(-r/2,0),\quad y_r=(r/2,0),\quad
p(r,b)=(b-r^3/12,0,0,0,0,2),\quad
t(r,b)=(b,b-r^3/6,0,0,0,0).
\]

Let `Q_{r,b} = sourceSmoothLaw hL r b`, the canonical full-carrier posterior at the **literal** confluent target `p(r,b)`. Let

\[
R=\operatorname{sourceGammaRadius}
  =1+\sum_{k=0}^{5}\Gamma_k,\qquad
q=\partial_{22}F(0),\qquad H(b)=1+|b|.
\]

Here each `Γ_k` is the source's measurable Fourier derivative majorant. In particular `R≥1`; it controls every actual directional derivative needed below. Let

\[
W_r=|\det D^2F(x_r)\det D^2F(y_r)|
  \mathbf1_{\{D^2F(x_r)\prec0,\ \det D^2F(y_r)<0\}},
\]

the actual physical strict maximum/saddle determinant weight, including its zero-type boundary. For fixed `ε>0` and `K∈ℝ`, define the actual measurable analytic obstruction

\[
B_{r}=\{\varepsilon<rR^5\}\ \cup\ \{-KrR^5\le q\}.             \tag{1}
\]

These are exactly `sourceRegularityBad` and `sourceCurvatureOneSided`. There exist `δ>0`, `N_17,N_19,C,c>0`, depending on `L,ε,K` but **not** on `b`, such that, for every `b∈ℝ` and `0<r<δ`,

\[
\begin{split}
E_{Q_{r,b}}[W_r\mathbf1_{B_r}]
 &\le r^5\{N_{17}H(b)^{17}+N_{19}H(b)^{19}\},                 \tag{2}\\
p_{\mathrm{raw},6}(x_r,y_r;t(r,b))
 &\le Cr^{-5}e^{-cb^2}.                                    \tag{3}
\end{split}
\]

Consequently

\[
\sup_{0<r<\delta}\int_{\mathbb R}
 p_{\mathrm{raw},6}(x_r,y_r;t(r,b))
 E_{Q_{r,b}}[W_r\mathbf1_{B_r}]\,db <\infty.                  \tag{4}
\]

The same bound holds for any measurable geometric bad event `E_{r,b}` for which the separately established deterministic geometric theorem gives `E_{r,b}⊆B_r` on the positive-weight pin support, up to `Q_{r,b}`-null sets. No event/ODE theorem is assumed in proving (1)–(4). The companion task owns the actual capture/noncapture inclusion; this note establishes the analytic numerator it can use. A conventional extension uniform over all directions, under the same original coefficient law, is proved in §8.

**Parameter measure.** The product `p_raw,6(z;u,v,0) E[W_z 1_E | u,v,0]` is the bad-mark Campbell/Rice density with respect to `dx dy du dv`, as in the actual geometric application [S9, §4, equation (8)]. Formula (4) is an integral of that density evaluated on the slice `(u,v)=(b,b-r³/6)`. It does not turn the slice into a positive-measure subset of the full parameter space. No radius or polar Jacobian is included in (3), (2), or the posterior probability law. The separate coordinate changes are described in §7.

## 2. One covariance interval independent of height

Set `X_r = sourceConfluentPinsAt L r`, `G_r = sourcePinCovarianceAt L r`. They are defined from the prior and contain no `b`. The actual source results [S6–S8,S13] give

\[
G_r\longrightarrow G_0=\operatorname{sourcePinCovariance}L>0
\quad(r\downarrow0).
\]

Positive definiteness follows from the actual contact Gram and its proved nondegeneracy, not from a posterior normalizer. Matrix convergence in this fixed finite dimension is also operator-norm convergence. There are therefore `δ_G∈(0,1]`, `0<λ_-≤λ_+<∞` such that

\[
\lambda_-I\le G_r\le\lambda_+I\quad(0<r<\delta_G).             \tag{5}
\]

For example, take a perturbation smaller than half the least eigenvalue of `G_0`. Thus `G_r` is invertible and every inverse entry is at most `K_G=λ_-^{-1}` in absolute value. This selection does not use a target-height limit.

The actual decomposition [S3] supplies `β_r=curvatureBeta L r`, `τ_r=curvatureVariance L r` and

\[
\beta_r\longrightarrow\beta_0,\qquad
\tau_r\longrightarrow\tau_0
 =\operatorname{sourceContactSchur}L>0.                       \tag{6}
\]

Shrinking to a common `δ≤δ_G`, independently of `b`, choose `B<∞` and `a=τ_0/2>0` such that

\[
|\beta_{r,i}|\le B,\qquad \tau_r\ge a.                       \tag{7}
\]

The conditional scalar mean is retained exactly:

\[
m_{r,b}=\beta_r\cdot p(r,b)
 =\beta_{r,0}(b-r^3/12)+2\beta_{r,5}.
\]

It is affine in `b`; (7) bounds its magnitude by a constant times `H(b)`. We never require it to be bounded by a constant uniform in `b`. In particular, the fixed-height wrappers' use of convergence of `m_{r,b}` is unnecessary for choosing our interval. Equivalently one can use those wrappers at `b=0` for their height-independent covariance, beta and variance conclusions alone.

## 3. Polynomial conditional moments from the literal affine posterior

Let `A_m=confluentModeMajorant L m`, `w_{5,m}=orderModeBound 5 2 L m`, and

\[
B_5=\sum_m w_{5,m}A_m,\quad C_5=36K_GB_5,\quad
w_m=w_{5,m}+C_5A_m,\quad W_w=\sum_mw_m.
\]

These weights are nonnegative and summable, and `B_5<∞`, by the completed source summability/product theorems [S1,S6]. The series are literal absolutely summable series on each good carrier sample; no formal manipulation of a possibly undefined series is being used.

For `r≤1`, all target coordinates satisfy

\[
|p_i(r,b)|\le |b|+2\le2H(b).                                 \tag{8}
\]

Apply `posterior_sampleMajorant_le` [S1] with the **uniform** inverse bound from (5) and the explicit `D=|b|+2`. For the actual posterior map `Φ_{r,b}=posteriorSample hL r p(r,b)`, this proves pointwise

\[
\Gamma_5(\Phi_{r,b}\omega)
 \le C_5(|b|+2)+\Gamma_w(\omega).                            \tag{9}
\]

This also follows directly from its literal coefficient formula

\[
\Phi_{r,b}(\omega)_m
 =\omega_m+\sum_i a_{r,i}(m)
       [G_r^{-1}(p(r,b)-X_r(\omega))]_i.
\]

Everything except `p(r,b)` is independent of `b`; hence the map is affine in height. The estimate (9) retains that shift. Under `μ` the coordinate variables, rather than the posterior coordinates, are standard Gaussians. The completed Gaussian weighted-series moment result [S2] gives

\[
E_\mu\Gamma_w^n\le W_w^n M^{\rm abs}_n,
\qquad M^{\rm abs}_n=E|N(0,1)|^n<\infty.                    \tag{10}
\]

Use the proved pointwise inequality `R≤1+6Γ_5` [S4]. From (8)–(9),

\[
R(\Phi_{r,b}\omega)
 \le H(b)\{1+12C_5+6\Gamma_w(\omega)\}.
\]

The posterior pushforward identity is exact at every target [S6]. Thus for every natural `n` there is `M_n<∞`, independent of `b,r`, such that

\[
E_{Q_{r,b}}R^n\le M_n H(b)^n.                               \tag{11}
\]

The integrability assertion is part of the conclusion. For `n≥1` one explicit choice is

\[
M_n=2^{n-1}\{(1+12C_5)^n+6^nW_w^nM^{\rm abs}_n\},\qquad M_0=1.
\]

The same interval works for every `n`. This proves the required height uniformity rather than extracting it from the old fixed-height existential statement. Neither positivity nor any lower bound for `E W_r` has been used.

## 4. Scalar times whole residual, uniformly in height

The completed actual decomposition [S3] is on the whole smooth coefficient carrier. It gives the scalar law

\[
\nu_{r,b}=N(m_{r,b},\tau_r),
\]

and a residual probability `ρ_r=curvatureResidualLaw hL r` independent of `b`, together with a measurable reconstruction `Ψ_{r,b}(q,ρ)` whose image of `ν_{r,b}⊗ρ_r` is exactly `Q_{r,b}` and for which the actual transverse derivative is `q`. These are the source theorems `curvatureReconstruct_hasLaw` and `curvatureReconstruct_Q`. Independence is proved from the actual jointly Gaussian scalar and all residual coefficient coordinates; it is not a marginal-independence assumption.

Let `χ_{r,m}=curvatureDirection L r m`, `σ_r=√τ_r`. The completed envelope calculation, using only (7) and the actual coefficient majorants, gives a **height-independent** nonnegative sequence `U_m` with

\[
|\chi_{r,m}|\le U_m,\qquad |\chi_{r,m}|/\sigma_r\le U_m,
\quad \sum_mw_{k,m}U_m<\infty\quad(k\ge0).                  \tag{12}
\]

For clarity, the source's explicit choice is

\[
U_m=(|c_m|+6BA_m)(a^{-1/2}+a^{-1}),
\]

where `c_m` is the actual `q` coefficient. It is `curvatureDirectionEnvelope L B`; its two domination conclusions are `curvatureDirection_envelope_at`. No mean bound is used. Set

\[
J=\sum_{k=0}^5\sum_m w_{k,m}U_m<\infty,
\quad A_*=1+J,
\quad S_{r,b}(\rho)=R(\Phi_{r,b}\rho)\ge1.
\]

The actual reconstruction and residual-image estimates [S3] now give

\[
\begin{split}
R(\Psi_{r,b}(q,\rho))&\le A_*(|q|+S_{r,b}(\rho)),             \tag{13}\\
S_{r,b}(\operatorname{curvatureResidualSample}(\omega))
 &\le R(\Phi_{r,b}\omega)+J|Z_r(\omega)|,                     \tag{14}
\end{split}
\]

where `Z_r` has standard Gaussian law under `μ`. Applying (11), (14) and the elementary two-term power bound proves

\[
\int S_{r,b}^n\,d\rho_r\le T_nH(b)^n,
\quad
T_n=2^{n-1}(M_n+J^nM^{\rm abs}_n)\quad(n\ge1).              \tag{15}
\]

This includes integrability and specifically supplies the degree-17 residual moment. No independence between the two terms in (14) is needed.

The scalar Gaussian density is bounded independently of its mean:

\[
\frac{d\nu_{r,b}}{dq}(q)
 \le D=(2\pi a)^{-1/2},\qquad
\nu_{r,b}([-h,h])\le2Dh\quad(h\ge0).                        \tag{16}
\]

Indeed the exponential in its density is at most one and `τ_r≥a`. This is the completed variance-floor lemma and actual specialization [S3]; it is valid for the literal noncentered `m_{r,b}` at every height.

## 5. Regular slab numerator and regularity tail

Put `K_*=max(K,1)` and

\[
E^{\rm reg}_r=\{rR^5\le\varepsilon,\ |q|\le K_*rR^5\}.
\]

On the actual pin support the completed physical determinant estimate [S4] is

\[
0\le W_r\le2r^2R^2q^2+8r^4R^4.                             \tag{17}
\]

Also `|q|≤R`. Therefore, for `r≤1`,

\[
W_r\le10r^2R^4,\qquad W_r^2\le100r^4R^8.                   \tag{18}
\]

The constant **100 here is the literal axial constant** for the source certificate `R`. Equations (11),(18) supply both weight and squared-weight integrability on our height-independent interval. Thus the regular-numerator proof does not need the old wrapper's height-dependent Palm interval even for its integrability input.

Apply the completed scalar-product calculation [S5], equivalently `I4SourceWeightedCurvature.sourceRegularCurvatureSlab_numerator_of_product` [S10], using the actual law, density, reconstruction and residual moment just established. To display its powers explicitly, let

\[
D_*=A_*(1+K_*\varepsilon).
\]

On `E_reg`, (13) gives `R≤D_*S`, and then

\[
|q|\le K_*D_*^5rS^5,\qquad
W_r\le(2K_*^2D_*^{12}+8D_*^4)r^4S^{12}.                    \tag{19}
\]

For each residual sample, integrate (19) over the scalar interval in (19). Its mass is at most `2D K_*D_*^5 r S^5` by (16). Tonelli/Fubini on the **literal product law**, followed by (15) at `n=17`, proves

\[
E_{Q_{r,b}}[W_r\mathbf1_{E^{\rm reg}_r}]
 \le N_{17}r^5H(b)^{17},                                   \tag{20}
\]

where one explicit constant is

\[
N_{17}=2D(K_*D_*^5)(2K_*^2D_*^{12}+8D_*^4)T_{17}.
\]

The actual final source wrapper is named `sourceRegularCurvatureSlab_numerator`; there is no declaration named `sourceWeightedCurvature_actual_regular_numerator`. The wrapper's existing fixed-height conclusion is reused through its already proved product calculation, with the newly established uniform constants, rather than asserted to have stronger quantifiers.

For `E_tail={ε<rR⁵}`, sixth-power Markov and (11) yield

\[
Q_{r,b}(E_{\rm tail})
 \le\varepsilon^{-6}r^6M_{30}H(b)^{30}.                    \tag{21}
\]

Cauchy–Schwarz and (18), followed by (11) at `n=8`, prove

\[
\begin{split}
E_{Q_{r,b}}[W_r\mathbf1_{E_{\rm tail}}]
 &\le(100r^4M_8H(b)^8)^{1/2}
       (\varepsilon^{-6}r^6M_{30}H(b)^{30})^{1/2}\\
 &=N_{19}r^5H(b)^{19},\quad
N_{19}=10\varepsilon^{-3}\sqrt{M_8M_{30}}.                  \tag{22}
\end{split}
\]

As an optional algebraic shortcut, (18) and `1_Etail≤ε⁻³r³R¹⁵` give the same degree/radius powers directly from the nineteenth moment. Equation (22) follows the specified eighth/thirtieth-moment route and does not use that shortcut as an assumption.

Finally, the completed source pin/strict-type calculation [S4] proves, whenever `W_r>0`,

\[
-KrR^5\le q\quad\Longrightarrow\quad |q|\le K_*rR^5.         \tag{23}
\]

For samples outside `E_tail`, (23) puts the second event in (1) inside `E_reg`. Samples with `W_r=0` contribute zero. The all-pin posterior support is already established at every target [S6]. Hence

\[
W_r\mathbf1_{B_r}\le W_r\mathbf1_{E_{\rm tail}}
                         +W_r\mathbf1_{E^{\rm reg}_r}
\quad Q_{r,b}\text{-a.e.},
\]

and (20),(22) prove (2). This is an **unnormalized** assertion. At no point has a height-dependent `E W_r` been divided out or assigned a uniform positive floor.

## 6. Literal raw density and its determinant

The raw vector is in the source order

\[
O_r=(F(x_r),F(y_r),F_x(x_r),F_x(y_r),F_y(x_r),F_y(y_r)).
\]

It is jointly Gaussian [S7]. It is centered because each row is an absolutely L¹-summable linear series of mean-zero original Gaussian coordinates [S1,S16]; exchanging that sum and expectation is justified by the summable coefficient majorant. For `r>0`, `X_r=T_rO_r`, where the literal `T_r` is `confluentTransform r`, and [S7] proves `T_rt(r,b)=p(r,b)`. To compute its determinant rather than assume its order, first replace each raw pair by its average and divided difference:

\[
(s,d,a,h,c,k)=
\left(\frac{v_0+v_1}2,\frac{v_1-v_0}r,
 \frac{v_2+v_3}2,\frac{v_3-v_2}r,
 \frac{v_4+v_5}2,\frac{v_5-v_4}r\right).
\]

Each pair transformation has determinant `1/r`, so this map has absolute determinant `r⁻³`. Up to coordinate permutations, the remaining map sends

\[
(s,d,a,h,c,k)\longmapsto(s,a,c,h,k,12r^{-2}(a-d)).
\]

Its absolute determinant is `12r⁻²`, because subtracting the `a` contribution leaves the replaced `d` coordinate multiplied by `−12r⁻²`. Thus exactly

\[
|\det T_r|=12/r^5.                                         \tag{24}
\]

In particular `O_r` is nonsingular, with covariance `Σ_r=T_r⁻¹G_rT_r⁻ᵀ`. The ordinary linear density change gives

\[
p_{\rm raw,6}(x_r,y_r;t(r,b))
 =\frac{12}{r^5}(2\pi)^{-3}(\det G_r)^{-1/2}
    \exp\{-\tfrac12p(r,b)^TG_r^{-1}p(r,b)\}.                \tag{25}
\]

This is the density of the original raw six pins, not the confluent density. From (5),

\[
(\det G_r)^{-1/2}\le\lambda_-^{-3},\qquad
p^TG_r^{-1}p\ge\|p\|_2^2/\lambda_+.
\]

For `r≤1`, with `a_r=r³/12`,

\[
\|p(r,b)\|_2^2=(b-a_r)^2+4
 \ge\tfrac12b^2-a_r^2,
\qquad a_r^2\le1/144.
\]

Substitution into (25) proves (3) with, for instance,

\[
c=\frac1{4\lambda_+},\qquad
C=12(2\pi)^{-3}\lambda_-^{-3}
       \exp\{1/(288\lambda_+)\}.
\]

The deterministic pin value `2` is retained in (25); dropping its nonnegative square only weakens our upper bound. The height shift `−r³/12` has not been suppressed. Equations (2),(3) give the stronger pointwise envelope

\[
p_{\rm raw,6}\,E[W_r\mathbf1_{B_r}]
 \le C\{N_{17}H(b)^{17}+N_{19}H(b)^{19}\}e^{-cb^2}.           \tag{26}
\]

A polynomial times a Gaussian is integrable, establishing (4), uniformly as `r↓0`.

## 7. The geometric application and distinct Jacobians

The existing actual Campbell application [S9] derives its identity from the finite-original-block area theorem [S12] for the exact source admitted in [S11]. It identifies the raw and confluent **coefficient posterior maps pointwise at every target**, not only almost everywhere in the height. At our literal target its unnormalized bad-mark intensity is exactly the left side of (26). This identifies the relevant density with respect to the physical `dx dy du dv` measure; no new Rice identity is a premise of this note.

Three different operations must be kept separate:

1. `T_r` changes the six observation coordinates. Its density multiplier is **`12/r⁵`**, equation (24). It cancels in a normalized posterior mark law, but is essential in the unnormalized Rice density.
2. The height coordinates `(u,v)=(b,b−ℓ)` have `du dv=db dℓ` in absolute value. If one subsequently parametrizes the **height gap** by `ℓ=s³/6`, then `dℓ=(s²/2)ds`. Thus a height-gap-to-radius-scale change contributes **`s²/2`**. It is not an extra factor in (25). If the symbol `r` is used for this gap scale, the resulting factor is `r²/2`; the position separation is still an independent variable until an explicit later reduction relates them.
3. In a physical flat chart, positions parametrized as `(x,y)=(z−he/2,z+he/2)` have `dx dy=dz d(he)=h dz dh dθ`. The **`h`** is the two-dimensional polar factor for position separation. It is distinct from the height-gap derivative. Evaluating a density at the relation `u−v=h³/6` alone does not supply either a new change-of-variables formula or a measure on that hypersurface.

Formula (26) is a uniform height-integrated **density** estimate on that specified slice. No global elder selection, pair-to-bar counting estimate, P0.2, GT5, or parent closure follows here.

## 8. Conventional extension uniform over all angles

This section proves the analytic angular extension; it does **not** claim a Lean rotation theorem. Rotating the argument is a change in observation rows of the **same original coefficient law**. General rotations need not preserve its Fourier weights or its distribution.

Let `e=(cosθ,sinθ)`, `n=(−sinθ,cosθ)`, with `θ∈S¹`; a midpoint `z` may also range over the fixed physical torus. Use endpoints `z±re/2`, derivatives along `e,n`, and transverse scalar `q_{z,θ}=∂_n²F(z)`. Let `X_{z,θ,r}` be the same literal six-row confluent transform of these actual raw observations. Define the seven-row coefficient vector

\[
A_m(z,\theta,r)=(a_{0,m},\ldots,a_{5,m},c_m),
\quad c_m=\partial_n^2f_m(z),                               \tag{27}
\]

where `f_m` is the actual deterministic Fourier coefficient function. The first three rows are endpoint averages of `f_m,∂_ef_m,∂_nf_m`. The remaining rows have the **exact directional Peano forms**

\[
\begin{split}
a_{3,m}&=\int_{-1/2}^{1/2}\partial_e^2f_m(z+tre)\,dt,\\
a_{4,m}&=\int_{-1/2}^{1/2}\partial_e\partial_nf_m(z+tre)\,dt,\\
a_{5,m}&=\int_{-1/2}^{1/2}(3/2-6t^2)
                 \partial_e^3f_m(z+tre)\,dt.                \tag{28}
\end{split}
\]

The last identity follows by two integrations by parts in the literal expression `12r⁻²[(∂_ef_m(y)+∂_ef_m(x))/2−(f_m(y)−f_m(x))/r]`; its kernel is nonnegative with mass one. Thus (27)–(28) extend continuously through `r=0`, where their observation vector is exactly

\[
(F,F_e,F_n,F_{ee},F_{en},F_{eee},F_{nn})(z).                 \tag{29}
\]

Every input vector `e,n` has source Pi norm at most one. The actual mode derivative bounds therefore imply, for example, the common nonnegative summable envelope

\[
|a_{i,m}|\le A_m^\sharp
 :=8\sum_{k=0}^3w_{k,m},\qquad |c_m|\le w_{2,m},             \tag{30}
\]

uniformly in `z,θ,r` (the factor 8 is conservative). Every product of this envelope with `w_{j,m}` is summable. Consequently all products of the seven rows are dominated by one summable sequence. Dominated convergence for these actual coefficient series makes

\[
\mathcal G(z,\theta,r)=\sum_m A_m(z,\theta,r)A_m(z,\theta,r)^T
                                                                    \tag{31}
\]

jointly continuous on the compact parameter set `torus×S¹×[0,r₀]`. This proves the required **joint directional confluent limit**, not just convergence separately at each angle.

Here is a source-specific proof of positive definiteness at `r=0`. All Fourier weights are strictly positive and the complete trigonometric span is dense in `C^∞`, as already established for this exact law in [S11, §3]. Any nonzero combination of independent finite-jet evaluation functionals can be realized nontrivially by a local polynomial times a cutoff. If it had zero variance, the positive sum of squared Fourier coefficients of that functional would force it to annihilate every Fourier mode, hence every smooth function by density, a contradiction. This also proves SPD for any vector of independent finite jets at finitely many distinct points. In the particular single-site case (29), independence is completely explicit: its seven symbols in directional variables `(s,t)` are `1,s,t,s²,st,s³,t²`, with the harmless powers of `i` from differentiation. They are linearly independent, since the change from Cartesian wave variables to `(s,t)` is invertible. Alternatively a polynomial annihilating the entire scaled lattice is identically zero: fix one integer coordinate, use infinitely many roots in the other, and then apply the same argument to its coefficient polynomials. The random zero mode supplies the constant symbol. Thus **the actual augmented seven-observation covariance** `𝒢(z,θ,0)` is positive definite everywhere.

The least eigenvalue is continuous. Compactness of `torus×S¹` and (31) therefore give `γ>0`, `Λ<∞` and one `δ_ang>0` with

\[
\gamma I\le\mathcal G(z,\theta,r)\le\Lambda I
\quad(0\le r<\delta_{\rm ang})                              \tag{32}
\]

for all `z,θ`. We can require `δ_ang<|L|/4` to stay in short physical charts. Its six-pin principal block has the same floor. The actual conditional variance of `q_{z,θ}` given the six pins is its Schur complement, and

\[
\tau_{z,\theta,r}
 =\inf_{v\in\mathbb R^6}(-v,1)^T\mathcal G(z,\theta,r)(-v,1)
 \ge\gamma.                                                \tag{33}
\]

Thus the transverse variance floor is uniform as well. The regression beta is uniformly bounded by (32), and the corresponding direction and direction-divided-by-sigma have a common weighted-summable envelope obtained explicitly from (30):

\[
U_m^\sharp=(w_{2,m}+6B_{\rm ang}A_m^\sharp)
                    (\gamma^{-1/2}+\gamma^{-1}).            \tag{34}
\]

No rotation-invariance assertion occurred in (27)–(34).

For completeness, the full-carrier source joins in this angular application are actual constructions. With these rows let `G` be their six-row Gram, `c` the `q` coefficient, `β=(Σ_m c_ma_m^T)G⁻¹`, `d_m=c_m−β·a_m`, `τ=Σ_m d_m²`, `χ_m=d_m/√τ`. The row sums and all weighted sums converge by (30),(34). The canonical posterior is the same coefficient formula `Φ_p(ω)=ω+a^TG⁻¹(p−Xω)`. Its correction belongs to every source summability order, so it stays in the original good carrier. The variable `Z=Σχ_mω_m` is standard Gaussian; the residual sample `ρ=ω−χZ` stays in that carrier. Its finite coordinates have zero covariance with `Z` and are jointly Gaussian with it. Finite-coordinate independence extends to the countably generated coefficient sigma-field, so `Z` and the **whole** residual sample are independent. Moreover `Σa_mχ_m=0`, `Σc_mχ_m=√τ`, and

\[
q(\Phi_p\omega)=\beta p+\sqrt\tau\,Z,\qquad
\Phi_p\omega=\Phi_p\rho+\chi Z.
\]

Consequently the measurable reconstruction

\[
\Psi_p(q,\rho)=\Phi_p\rho+
     (\chi/\sqrt\tau)\{q-q(\Phi_p\rho)\}
\]

maps `N(βp,τ)⊗Law(ρ)` exactly to the canonical posterior at **every** target `p`, with `q(Ψ)=q`. This repeats the already qualified general coefficient algebra [S3,S6] with the explicit directional rows; it does not condition only a finite midpoint-jet surrogate.

To avoid hiding a norm-change constant, put **`R♯=8R`**. If `g(s,t)=F(z+se+tn)`, then in the source Pi norm `‖Rot_θ‖≤√2`, so

\[
\|D^kg\|\le(\sqrt2)^k\Gamma_k\le8\Gamma_k
\quad(0\le k\le5).
\]

Hence the same one-dimensional Peano determinant argument gives

\[
W_r\le2r^2(R^\sharp)^2q_{z,\theta}^2
               +8r^4(R^\sharp)^4,
\quad W_r^2\le100r^4(R^\sharp)^8
               =100\,8^8r^4R^8.                           \tag{35}
\]

The orthogonal change of physical frame preserves the strict Hessian types and each determinant, so `W_r` is still the literal physical determinant weight. Equation (35), rather than an unqualified axial `100r⁴R⁸`, is the angular assertion in terms of the original certificate. The strict-type transverse upper estimate and symmetric-slab reduction use `R♯` in the same way.

The posterior-majorant argument of §3 with (30),(32) gives moments of `R` bounded by constants times `H(b)^n`, uniformly in `z,θ,r`. Multiplication by `8^n` gives the same conclusion for `R♯`. Equations (34) and the actual reconstruction give a uniform bound `R♯(Ψ)≤A_ang(|q|+S♯)`, where `S♯=R♯(Φ_pρ)≥1`, and a uniform degree-17 bound on `E(S♯)^17`. Thus §§4–5 prove

\[
E[W_r\mathbf1_{B^\sharp_{z,\theta,r}}]
 \le r^5\{N^{\rm ang}_{17}H(b)^{17}
                      +N^{\rm ang}_{19}H(b)^{19}\},         \tag{36}
\]

where `B♯={ε<r(R♯)^5} ∪ {−Kr(R♯)^5≤q_{z,θ}}`, with constants uniform over midpoint, angle and height. All dimension/norm factors are absorbed in these angular constants; they need not equal the axial constants.

The four gradient raw rows are transformed between Cartesian and `(e,n)` components by two orthogonal matrices, of absolute determinant one. At gradient target zero their raw density is therefore the original Cartesian raw density. The confluent transformation still has determinant (24), and (32) supplies uniform lower and upper eigenvalue bounds for its actual six-pin covariance. Section 6 consequently proves (3),(26) with constants also uniform in `z,θ`. This completes the **analytic all-angle numerator and height-integrated Rice-density estimate** on the original source.

The remaining join for any claim specifically about an all-angle geometric noncapture event is to instantiate its deterministic capture implication for the physical field in the rotated local chart with the certificate `R♯` and correspondingly chosen fixed constants `K,ε`. If that implication is only supplied axially by the companion task, (36) must be stated for the displayed analytic obstruction until this geometric join is supplied. There is no remaining covariance, mean, density, moment, or rotational-invariance hypothesis in (36).

## 9. Dependency and verification boundary

`REUSED_SOURCES.json` gives exact source paths, hashes, declaration names and retained evidence references. Source IDs in this proof refer to that file. This application uses the already reviewed exact finite-L source admission and only the finite-incidence Campbell portion of GAD; its later global conclusions are not invoked. Ordinary finite-dimensional Gaussian density change of variables, continuous eigenvalues of symmetric matrices, compactness, Cauchy–Schwarz, Markov, and nonnegative product integration are the conventional mathematical imports used in the new combination.

No source file, Lean file, build artifact, review verdict or scientific-status register was changed. The new work is the height-independent interval, its polynomial dependence on `b`, the literal density determinant/envelope, their integrable combination, and the explicit conventional angular source construction. Existing verification remains applicable and reusable. A provider-distinct review or other process obligation for this new conventional application is separate from the completed mathematics and is not represented as completed here.
