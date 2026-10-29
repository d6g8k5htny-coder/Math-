# Actual ordered critical-pair Campbell measure and its canonical mark law

26October2026. OpenAI author-side conventional source application. This note reuses completed mathematical results; it is not a new independent review, a Lean implementation of Kac–Rice, or a closure of the original research goal. All writes remain in scratch.

## 1. Reused theorem and the actual law

Write `μ = smoothLaw 2 L` on `Ω = SmoothSample 2 L`, with `L ≠ 0`, and `F_ω = smoothSourceField 2 L ω`. The source is the literal countable real Fourier series with one random constant mode and independent sine/cosine coefficients:

    F_ω(x) = Z_L^(-1/2) ω_0
      + Σ_(k∈H) sqrt(2 exp(-|αk|²/2)/Z_L)
          [ω_(k,cos) cos(αk·x) + ω_(k,sin) sin(αk·x)],   α=2π/L.

`inputs/SourceFourierSeries.lean` defines these coefficients, `inputs/SpectralWeights.lean:sourceWeight_eq_physical` identifies the physical exponential weights, and `inputs/SourceSmoothCarrier.lean:sampleInclusion_map` identifies the carrier measure with the original independent coefficient law. The all-order source majorants prove almost-sure absolute uniform convergence of every derivative series; every carrier sample is smooth. No truncation, samplewise mean removal or additional volume normalization is made.

This exact law was already admitted to the conventional Gaussian manifold theorem in `original_finite_l_gaussian_binding_20261017/PROOF.md` §§3–4, source SHA256 `ad9ab5afea28062dfc661d0d19b43f20e67cfd67cb6910d3cc6c3fb8b81398d8`, with the actual `REVIEW.md` verdict **ACCEPT_SCOPED**. That proof checks the entire positive spectrum, dense smooth span and every smooth norm summability condition, including the random zero mode. Its mathematical import GAD is `gaussian_short_bar_theory_20261017/smooth_gaussian_manifold_admission/PROOF.md`, SHA256 `8d992e194f0a898e563c4c3d05b8079cde292f9e87d7ff51030ad12ef5faf319`, Git blob `d61fd11a826856baecb4cf4cd8a76ad5c25350dd`.

We use GAD §6's **all-Borel finite-original-block pair Rice identity**, including its every-target finite-tail Bayes identification, not its later elder or asymptotic conclusions. Its retained classical imports are the equal-dimensional smooth Sard theorem, the weighted equal-dimensional area/change-of-variables formula with multiplicity for nonnegative Borel integrands, and the ordinary Gaussian/Tonelli facts stated in §12. Both the integrated and focused reviews accepted that finite-incidence argument at the exact source. Those reviews are OpenAI nonauthor reviews and carry no provider-distinct credit.

The current hypothesis `L ≠ 0` also allows `L < 0`. The quotient by `Lℤ²` is the same flat torus as that with period `|L|`. Amplitudes depend only on `L²`; replacing `L` by `|L|` leaves cosines unchanged and changes the sign of every sine coordinate when `L < 0`. The independent standard Gaussian coefficient law is invariant under those coordinate sign flips. Alternatively the admitted series argument applies directly to the signed frequency, whose smooth span and norm sums are unchanged. The local calculations below retain the literal signed-frequency coefficients.

`c6_palm_route_20260929/PROOF.md` §5.1 independently records the canonical-kernel/global-Borel-mark convention. Its Lemma5.1 concerns an extra critical point under an already pinned law. We do not substitute that result for the unconditioned ordered-pair theorem used here.

## 2. An actual open position neighborhood

For distinct positions `z=(x,y)` in physical flat charts define

    O_z(ω) = (F_ω(x), F_ω(y), ∂₁F_ω(x), ∂₁F_ω(y), ∂₂F_ω(x), ∂₂F_ω(y)),
    a_z(m) = the same six derivatives of the deterministic mode coefficient,
    Σ_z = Σ_m a_z(m) a_z(m)ᵀ.

This covariance is the actual covariance of `O_z`, by the independent variance-one coordinates and the absolutely summable coefficient products. All finite derivative/coordinate families are jointly Gaussian. Every `a_z(m)` is smooth in `z`; the existing summable derivative majorants dominate its coefficient products locally uniformly. Consequently `z ↦ Σ_z` is continuous. This is exactly the source derivative-covariance continuity argument already proved in `SourceDerivativeContinuity`.

Fix any sufficiently small `r > 0` for which the established `sourceEndpoint_parameter_limits` supplies `IsUnit(sourcePinCovarianceAt L r)`, and also require `r < |L|/4`. Let `z_r = ((-r/2,0),(r/2,0))`. The proved continuous linear equivalence `T_r = confluentEquiv r` satisfies

    sourceConfluentPinsAt L r = T_r O_(z_r),
    G_r = T_r Σ_(z_r) T_rᵀ.

`G_r` is a covariance matrix, hence positive semidefinite; its invertibility makes it positive definite. Since `T_r` is invertible, `Σ_(z_r)` is positive definite. This deduction uses the actual small-radius covariance theorem and the literal observation equivalence, not an assumed full-rank raw law.

Positive definiteness is open. Shrink to a relatively compact open position neighborhood `U_r` of `z_r`, with closure inside a separated chart domain and inside `{z : Σ_z > 0}`. Its closure has a positive covariance eigenvalue floor. This provides the requested open neighborhood; no uniform neighborhood size as `r → 0` is claimed.

There is an actual finite original coefficient minor on a further such neighborhood. If the vectors `{a_(z_r)(m)}` did not span `ℝ⁶`, a nonzero vector `v` would annihilate every column, forcing

    vᵀΣ_(z_r)v = Σ_m (v·a_(z_r)(m))² = 0,

contradicting positive definiteness. Choose six columns forming a basis. Their `6×6` matrix `M(z)` has nonzero determinant at `z_r`, so the same selected original columns remain invertible after shrinking `U_r`. This is a finite block of the original independent Gaussian coordinates; it is not a finite-mode approximation to the field. Every selected coordinate retains its original amplitude inside `a_z(m)`.

The four gradient rows have full row rank as well. Thus the finite-incidence Sard statement reused from GAD §6 applies on this neighborhood. In particular the actual critical pairs there are nondegenerate almost surely. Their Hessian types therefore coincide with geometric maximum and saddle types. The separate global a.s. Morse/finiteness source join is not needed as a new premise of this local extended identity; its already established conventional result is compatible with it.

## 3. Canonical raw kernel on the whole coefficient carrier

For `z∈U_r` and every raw target `t∈ℝ⁶` define the literal coefficient posterior map

    R_raw(z,t,ω)_m = ω_m + a_z(m)ᵀ Σ_z⁻¹ (t - O_z(ω)),
    K_raw(z,t) = (R_raw(z,t,·))_# μ.                         (1)

For each source summability order, the deterministic correction in (1) is a finite linear combination of the six observation coefficient sequences. The coefficient-product majorant proof used by `pinLift_goodSample` shows that it belongs to the same good carrier. Thus (1) has values in the original `Ω`, not only in a formal sequence space. The map is jointly Borel in `z,t,ω` from the coefficient formulas and continuity of `Σ_z⁻¹`. Its mean is the actual noncentered regression mean `a_z(m)ᵀΣ_z⁻¹t`.

The raw observation of (1) is exactly `t` for every `ω`. The residual coefficient process is jointly Gaussian with `O_z`; its cross covariance vanishes coordinatewise. Finite restrictions give independence and the countable coordinate sigma-field gives whole-process independence. Hence (1) is the canonical full-carrier regular conditional kernel for `id_Ω` given `O_z`, specified at every `t`. This is the same construction and proof already implemented for the confluent rows in `SourceSmoothConditionalKernel`, applied to the actual raw rows. General-position raw-row packaging is a remaining Lean application task, not a new conventional Gaussian theorem assumed here.

There is also a pointwise identification with the kernel produced by the actual Rice calculation. Split the six selected original coefficients as `ξ∈ℝ⁶` and the remaining original coefficients as `η`, so `ξ` and `η` have their original independent Gaussian laws. Zeroing finitely many coefficients preserves the good carrier. Thus for almost every tail `η`, every finite overwrite `ξ` gives a sample in `Ω`. The reassembly map is Borel in the coefficient carrier.

At fixed `z`, write `O_z = M(z)ξ + O_tail,z(η)`. The exact fiber measure before normalization is

    H_(z,t)(A) = ∫ [φ₆(M(z)⁻¹(t-O_tail,z(η))) / |det M(z)|]
                   1_A(reassemble(M(z)⁻¹(t-O_tail,z(η)),η)) P_tail(dη).    (2)

Its total mass is the strictly positive Gaussian density `p₆(z;t)` of `O_z` at `t`, for **every** `t`. The tail is Bayes reweighted in (2); retaining its prior law after conditioning would be wrong. Completing the finite Gaussian observation square, as in the reused GAD §6/focused-review §5 proof, shows that for any finite family of original coefficient coordinates, `H_(z,t)/p₆(z;t)` has mean and covariance

    E[ω_m | t] = a_z(m)ᵀΣ_z⁻¹t,
    Cov(ω_m,ω_n | t) = 1_(m=n) - a_z(m)ᵀΣ_z⁻¹a_z(n).

The identity is valid at each literal `t`: only the finite joint Gaussian vector of tail observations and chosen coordinates enters the calculation. Its finite-coordinate characteristic functions equal those of (1). The Borel sigma-field of the good carrier is generated by its countably many coefficient coordinates, so

    H_(z,t) = p₆(z;t) K_raw(z,t)                     for every z,t.      (3)

This also proves the coefficient-carrier extension of the old field-mark statement: the finite-dimensional area formula accepts Borel coefficient/tail marks before any projection to the field. Recovering individual coefficients from a field is unnecessary. A formal pushforward to a norm-Borel `C³` torus space still needs the separately owned topology join; (2)–(3) themselves are statements on the actual measurable coefficient carrier.

## 4. The actual geometric Campbell identity

Let `H_x(ω)` and `H_y(ω)` be the literal physical Hessians, and define

    W_z(ω) = |det H_x(ω) det H_y(ω)|
             1_{H_x(ω) negative definite, det H_y(ω)<0}.            (4)

For each realization, form its actual ordered critical maximum/saddle pair counting measure and mark each pair by its two actual heights and by `ω`. Its expectation restricted to `U_r` is the measure `C`. Thus for every nonnegative Borel `ψ`,

    C(ψ) = E_μ Σ_{(x,y)∈U_r, x maximum, y saddle}
                     ψ(x,y,F_ω(x),F_ω(y),ω).                     (5)

This defines the left side through actual critical points, independently of any desired kernel formula. The reused incidence theorem ensures measurability of its nonnegative root sums. Overlap partitions and compact exhaustions are as in GAD §6. Degenerate critical pairs have zero probability by its finite-block Sard argument with the actual full-rank gradient rows above.

To apply that theorem concretely with heights, the selected coefficient solution at prescribed heights is

    ξ(z,u,v,η) = M(z)⁻¹((u,v,0,0,0,0) - O_tail,z(η)).             (6)

This incidence map has six parameters `(x₁,x₂,y₁,y₂,u,v)` and six selected coefficient outputs. At a critical pair, differentiating `O_z(ξ,η)=(u,v,0,0,0,0)` gives

    M(z) dξ = d(u,v,0,0,0,0) - (D_z O_z) dz.

The two value rows of `D_z O_z` vanish there. Its four gradient rows are, up to a row permutation, `diag(H_x,H_y)`. Therefore the absolute incidence Jacobian is exactly

    |det H_x det H_y| / |det M(z)|.                             (7)

The weighted equal-dimensional area formula with the original `ξ` Gaussian density, followed by Tonelli in the independent original tail, is precisely GAD's already proved finite-incidence identity. Insert the strict type indicator and the Borel mark `ψ`; (2)–(3) then give

    C(ψ) = ∫_(z∈U_r) ∫_(u,v∈ℝ²) p₆(z;u,v,0,0,0,0)
                ∫_Ω W_z(ω) ψ(z,u,v,ω)
                    K_raw(z,(u,v,0,0,0,0))(dω) du dv dz.         (8)

Both sides may initially be `+∞`. There is one physical Hessian determinant per endpoint. There is no unordered-pair factor: the first point has the maximum role, the second the saddle role. No radius, polar-coordinate or confluent-density change of variables has occurred in (8).

All classical theorem hypotheses are now concrete: original finite Gaussian coordinates with a density; independent original smooth tail; an actual selected six-column minor invertible on the open neighborhood; a smooth finite incidence map; arbitrary Borel nonnegative weights; and the physical determinant Jacobian (7). No Campbell identity, Palm kernel, density estimate or desired event bound was added as a source assumption.

For completeness (8) is locally finite on compact position subsets, including after integrating all heights. On such a subset the actual raw covariance and inverse have uniform bounds. The conditional Gaussian Hessian mean is linear in `(u,v)` and the residual covariance is uniformly bounded. Its fourth moments therefore have a uniform polynomial bound of degree four in the heights. The Gaussian density satisfies `p₆(z;u,v,0) ≤ C exp(-c(u²+v²))`. Their product is integrable. This is the ordinary local Gaussian moment argument in GAD §6, with the actual covariance floor supplied above.

## 5. Derive a geometric mark disintegration, including the zero branch

For `s=(z,u,v)` put `K_s=K_raw(z,(u,v,0,0,0,0))` and

    Z(s) = ∫ W_z dK_s,       q(s) = p₆(z;u,v,0,0,0,0),
    λ(ds) = q(s) Z(s) dz du dv.                                  (9)

`Z` is Borel. It is finite at every parameter: under `K_s` the actual Hessian entries form a finite Gaussian vector, possibly with singular residual covariance, and hence have finite fourth moments. For a symmetric `2×2` matrix, `|det H| ≤ ‖H‖_F²/2`; Cauchy–Schwarz bounds the expectation of the product in (4). No nondegeneracy of the conditional Hessian covariance is required for finiteness.

Define a probability mark kernel at every parameter by the explicit branch

    P_mark(s,A) = [∫_A W_z dK_s]/Z(s)       if Z(s)>0,
                 δ_zeroSample(A)           if Z(s)=0.             (10)

The zero branch is needed for a globally defined probability kernel on the whole parameter neighborhood. A nonnegative integrable weight with zero integral is zero `K_s`-almost everywhere, so its unnormalized weighted measure is zero on that branch. Consequently for every parameter, including `Z=0`,

    q(s) ∫_A W_z dK_s = q(s) Z(s) P_mark(s,A).                   (11)

Equation (8), first for rectangles and then for nonnegative Borel functions, therefore proves

    C(ds,dω) = λ(ds) P_mark(s,dω).                               (12)

The marginal `λ` is obtained from the actual geometric Campbell measure by setting the field mark to one in (8). Thus (10) is a genuine version of its Palm mark/disintegration kernel, derived from the geometric count. It has not been designated a Palm law by definition alone. The zero branch has zero Campbell intensity and its arbitrary Dirac value has no effect on (12).

Disintegrations are unique only `λ`-almost everywhere. We name (10) the **canonical Gaussian/Rice mark version**; we do not claim that every geometric Palm version agrees with it at an individual prescribed height/position. The density `q(s)>0` cancels from the positive branch of the normalization: `(q W)/(q Z)=W/Z`. In particular no additional power of `r` enters the probability law.

## 6. Pointwise raw/confluent equality and the prescribed null pin

At `z_r`, let `a(m)=a_(z_r)(m)`, `Σ=Σ_(z_r)` and `T=T_r`. The actual confluent coefficient column is `T a(m)` and its Gram is `G=TΣTᵀ`. For every vector `y`,

    (T a(m))ᵀ G⁻¹ (T y)
      = a(m)ᵀ [Tᵀ(TΣTᵀ)⁻¹T] y
      = a(m)ᵀΣ⁻¹y.                                            (13)

Indeed `(TΣTᵀ)⁻¹=T⁻ᵀΣ⁻¹T⁻¹`. This identity concerns the same original coefficient sample, with the actual noncentered target retained. Substitute `y=t-O_(z_r)(ω)` into (13). The literal raw posterior coefficient map (1) equals `posteriorSample hL r (T t) ω` coordinate by coordinate, for every `t` and every `ω`. Hence

    K_raw(z_r,t) = sourceSmoothKernel hL r (T_r t)               for every t. (14)

This is stronger than equality of two regular conditional versions almost everywhere. It uses the same coefficient lift, so it is valid at the prescribed null pin without a continuity-of-marks claim or a zero-fiber substitution.

The already proved `prescribed_target` states

    T_r(b,b-r³/6,0,0,0,0) = d_r = (b-r³/12,0,0,0,0,2).

Thus (14) at that literal target is exactly `K_s = sourceSmoothLaw hL r b`. The weight (4) at `z_r` is definitionally the actual `sourceSmoothWeight L r`, by its raw physical Hessian definitions. The established `sourceSmoothPalm_estimates hL b` supplies `Z(s)≥c r²>0`, finiteness and the corresponding full-carrier density. Therefore the positive branch of (10) is

    P_mark(z_r,b,b-r³/6) = sourceSmoothWeightedLaw hL r b.        (15)

This proves that our qualified normalized determinant-weighted whole-carrier law is the canonical Gaussian/Rice Palm mark version of the **actual** ordered maximum/saddle pair Campbell measure, at the exact prescribed pins. Its whole-carrier event bounds and endpoint pushforward consequently apply to this named geometric mark version. They do not automatically identify an arbitrary Palm version chosen by modifying a null set.

No height-centering approximation was made. There is no Jacobian to compute in (15): all normalization was performed using the raw density in (8), and the deterministic raw/confluent observation change in (13) only identifies posterior measures. A density transformation would require its own ordinary determinant if the base parameter variables were changed; that operation was not used here.

## 7. What is checked in Lean and what remains formal work

`RawConfluentLift.lean` is a small new scratch companion proving three generic finite-matrix facts: `inverse_congruence`, `inverse_congruence_mulVec`, and `coefficient_lift_congr`. It imports only `Mathlib.LinearAlgebra.Matrix.NonsingularInverse` and `Mathlib.Basic.Real.Basic`. The final `algebra-03.json` records a new-scope `lake env lean -DwarningAsError=true` exit0, with all three direct axiom reports limited to `propext`, `Classical.choice`, `Quot.sound`. Source SHA before/after is `b5ff1c3837f80f186733bc2f4d6c03b0c11bcdf6da85b2b51806aaf99bf1dff6`. The first two failed attempts and their exact source snapshots/logs remain. The Python wrapper itself exits0 after writing metadata even for failed Lean attempts; the actual Lean exit is the recorded `exit_code`, namely1,1,0. No standalone named-module kernel replay or production qualification is claimed for this scratch companion.

The conventional application (8)–(15) is now concrete under the already reviewed GAD classical imports and exact same-law source admission. Its absent Lean obligations must not be converted into custom axioms or `admit`s:

1. Register general-position raw observations, their jointly measurable coefficient posterior kernel and the actual open-neighborhood covariance/minor result. Apply (13) to the literal six-row `confluentEquiv`; the generic algebra is done, while the source-row packaging is new formal work.
2. Represent the actual geometric critical-pair counting/Campbell measure, and instantiate a **proved** finite-incidence area theorem in Lean. The present package has no Lean area/Kac–Rice theorem. Assuming the desired Campbell identity would not close this obligation.
3. Formalize the Borel weighted-kernel normalization/disintegration with its exact zero-normalizer branch. Existing `PalmReweighting` already proves the positive-normalizer probability/event identities and should be reused.
4. Complete the separately owned actual source-to-norm-Borel periodic/torus field map before claiming Lean measurability of geometric norm or capture/ODE events. The coefficient-carrier result above does not assert that unfinished formal topology identification.

Global a.s. Morse/finiteness is already a conventional consequence of the same accepted law admission; its new Lean source join is owned separately. Conditional Morse at every null pin, geometric noncapture/elder/lifetime selections, P0.2/GT5 and later parent closure are additional conclusions and are not supplied by (15). Review/process requirements are tracked separately and do not invalidate reusable completed mathematics.
