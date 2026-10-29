# Compact cubic-gap marks: actual affine-target Rice numerator

26 October 2026. New conventional author-side addendum, scientific effect **NONE**. Binding brief: `SOURCE_COMPACT_MARK_CAPTURE_RICE.md` at commit `8d64490df8620b749ba2f224da535eeb6016c2d0`. The earlier `height-rice-application` proof and source evidence stay frozen. Completed applicable verification is reused, without replay. This note supplies the analytic affine-target extension; the companion author supplies the actual selected noncapture mark, its joint Borel measurability, and the deterministic rotated/amplitude-scaled capture implication.

## 1. Actual parameters, law and conclusion

Fix `L≠0` and `I=[k₀,k₁]`, where `0<k₀≤k₁<∞`. Every random object below is on the original smooth Fourier coefficient carrier with its unchanged source law `μ=smoothLaw 2 L`, including the random constant mode. A deterministic amplitude scaling in a capture argument changes no prior law in this note.

Let `z` range over the physical torus and let

\[
e=(\cos\theta,\sin\theta),\quad n=(-\sin\theta,\cos\theta),
\quad x=z-he/2,\quad y=z+he/2,
\]

where `h` is the actual position distance and `0<h<|L|/4`. Use directional raw pins in the order

\[
O_{z,e,h}=(F(x),F(y),F_e(x),F_e(y),F_n(x),F_n(y)).
\]

Their literal confluent transform `T_h` is the one already used in the frozen height proof [H]. At birth height `b` and cubic-gap mark `k`, prescribe

\[
t_{h,b,k}=(b,b-kh^3,0,0,0,0),\qquad
p_{h,b,k}=T_ht_{h,b,k}
 =(b-kh^3/2,0,0,0,0,12k).                                  \tag{1}
\]

This follows directly from the linear transform; the first row is the height average and the sixth is `12h⁻²[0−(−kh³)/h]=12k`.

Let `Q_{z,e,h,b,k}` be the canonical **whole-carrier** posterior at this literal target, given by the same actual original-coefficient regression as [H, §8]. This notation is not the old `sourceSmoothLaw hL h b`, whose definition fixes its sixth target at `2`. Let

\[
R=1+\sum_{j=0}^5\Gamma_j,\quad
\mathcal R=R^\sharp=8R,\quad q=F_{nn}(z),\quad H(b)=1+|b|,
\]

and let `W` be the physical strict maximum/saddle determinant weight at `(x,y)`:

\[
W=|\det D^2F(x)\det D^2F(y)|
  \mathbf1_{\{D^2F(x)\prec0,\ \det D^2F(y)<0\}}.
\]

For **any fixed** `ε>0` and `K∈ℝ`, put

\[
B_{z,e,h}(\varepsilon,K)
 =\{\varepsilon<h\mathcal R^5\}\cup\{-Kh\mathcal R^5\le q\}.
                                                                    \tag{2}
\]

There is one `δ>0`, independent of `z,e,k,b`, on which

\[
\begin{split}
E_Q[W\mathbf1_B]
 &\le h^5\{N_{17}H(b)^{17}+N_{19}H(b)^{19}\},              \tag{3}\\
p_{\rm raw,6}(x,y;t_{h,b,k})
 &\le C_dh^{-5}e^{-cb^2}.                                  \tag{4}
\end{split}
\]

Here `N₁₇,N₁₉,C_d,c` are finite constants uniform for `k∈I` and all midpoints/directions/heights; they can depend on `L,k₁,ε,K`. In particular,

\[
\mathcal D_B(z,e,h,b,k)
 :=p_{\rm raw,6}(x,y;t_{h,b,k})E_Q[W\mathbf1_B]
 \le C_d\{N_{17}H(b)^{17}+N_{19}H(b)^{19}\}e^{-cb^2}.         \tag{5}
\]

Consequently the integral of this displayed density over `b∈ℝ`, `k∈I` and all angles is bounded uniformly in `z` and `0<h<δ`. Section 7 distinguishes this density integral from a full Campbell count. Any true Borel bad mark included in (2) on the positive-weight pin support inherits (3)–(5); its event theorem is an explicit separately supplied join.

## 2. Reuse the covariance interval; change only the target

The frozen all-frame result [H, §8] has already established joint continuity and a uniform positive floor for the **actual augmented seven-observation covariance** of

`(confluent six pins, F_nn(z))`,

including its directional `h=0` Peano extension. Reuse its constants `γ>0`, `Λ<∞`, and one interval `0<h<δ≤min(1,|L|/4)`:

\[
\gamma I\le\mathcal G_{z,e,h}\le\Lambda I.                 \tag{6}
\]

No covariance row involves `b` or `k`. Thus the six-pin block `G`, its inverse-entry bound `K_G`, the regression row `β`, the transverse Schur variance `τ`, and all the direction envelopes from that proof are **unchanged**:

\[
G\ge\gamma I,\quad |(G^{-1})_{ij}|\le K_G,
\quad |\beta_i|\le B,\quad \tau\ge\gamma.                    \tag{7}
\]

The exact scalar conditional law is

\[
\nu=N(m,\tau),\qquad
m=\beta_0(b-kh^3/2)+12k\beta_5.                             \tag{8}
\]

The mean is retained. It is affine in `b,k` at fixed `(z,e,h)`, and is bounded by a constant times `H(b)` on `I`. No bound on its magnitude uniform in `b` is used. Its density obeys the same all-mean estimate

\[
\frac{d\nu}{dq}\le D=(2\pi\gamma)^{-1/2}.                   \tag{9}
\]

The original coefficient posterior is exactly

\[
\Phi_p(\omega)_m
 =\omega_m+\sum_{i=0}^5 a_i(m)
       [G^{-1}(p-X(\omega))]_i.                            \tag{10}
\]

It remains affine in the whole target, and (1) makes its dependence on `b,k` explicit. The prior, covariance, scalar direction and whole-residual process have not been rescaled, recentered or rotated to another Gaussian model.

## 3. New physical lemma: the weight/slab estimate needs no cubic target

This is the previously uncovered source join for varying `k`. The final source theorem `source_normalized_peano` [P] has hypotheses only on confluent rows `3,4`; it does **not** require row `5=2`. In contrast, several convenience error-bound exports specialize row 5 to 2 and cannot simply be quoted as statements about (1). The following direct argument supplies exactly what is needed, using only endpoint criticality.

Work in the physical orthonormal `(e,n)` frame and write

\[
u(t)=F_e(z+te),\qquad v(t)=F_n(z+te),\qquad -h/2\le t\le h/2.
\]

At the raw critical pins, `u(−h/2)=u(h/2)=v(−h/2)=v(h/2)=0`. The actual global derivative bound gives `|u''(t)|,|v''(t)|≤𝓡`. Therefore `u′,v′` are `𝓡`-Lipschitz and their interval integrals are zero. For `a=−h/2`,

\[
\begin{split}
|u'(a)|
 &=\left|\frac1h\int_a^{a+h}\{u'(a)-u'(s)\}\,ds\right|\\
 &\le\frac{\mathcal R}{h}\int_a^{a+h}(s-a)\,ds
   =\frac h2\mathcal R.                                   \tag{11}
\end{split}
\]

The right endpoint and both derivatives of `v` satisfy the same bound. Also the third directional derivative controls transport of `F_nn` from the midpoint:

\[
|F_{nn}(z\pm he/2)-q|\le(h/2)\mathcal R.                   \tag{12}
\]

Equivalently, the actual normalized endpoint entries

\[
a_\pm=h^{-1}F_{ee}(z\pm he/2),\quad
b_\pm=h^{-1}F_{en}(z\pm he/2),\quad
c_\pm=F_{nn}(z\pm he/2)
\]

satisfy `|a_±|,|b_±|≤𝓡` and `|c_±−q|≤h𝓡`. In this frame the physical Hessian determinant is

\[
\det D^2F(z\pm he/2)=h(a_\pm c_\pm-hb_\pm^2).
\]

The already established elementary determinant arithmetic [P] therefore gives

\[
0\le W\le2h^2\mathcal R^2q^2+8h^4\mathcal R^4.              \tag{13}
\]

Strict Hessian types and the physical determinant are preserved by the orthogonal frame change. Equation (13) is the physical weight, including its zero branch, not a normalized or midpoint-jet replacement. Since `|q|≤𝓡` and `h≤1`,

\[
W\le10h^2\mathcal R^4,\qquad
W^2\le100h^4\mathcal R^8=100\,8^8h^4R^8.                   \tag{14}
\]

If `W>0`, its maximum Hessian at `x` is negative definite, so `c_-<0`. Equation (12) implies `q<h𝓡`. Thus, writing `K_*=max(K,1)`,

\[
W>0,\ -Kh\mathcal R^5\le q
 \quad\Longrightarrow\quad |q|\le K_*h\mathcal R^5,         \tag{15}
\]

because `𝓡≥1`. This is the required symmetric-slab reduction. The argument used **neither endpoint heights nor any value of the cubic confluent row**. In particular its constants do not change when that row is `12k`. These new observations are conventional consequences of the original physical derivative bounds, not new Lean exports.

## 4. Moment degree is unchanged on the compact target family

Retain the all-frame summable coefficient envelope `A_m^♯`, derivative weight `w_{5,m}`, inverse bound `K_G` and weighted-series facts already established in [H]. Put

\[
B_5=\sum_mw_{5,m}A_m^\sharp,\quad C_5=36K_GB_5,
\quad w_m=w_{5,m}+C_5A_m^\sharp,\quad W_w=\sum_mw_m.
\]

Every sum is finite; the posterior summability and whole-carrier pushforward facts are the existing every-target results. For `h≤1` and `k∈I`,

\[
|p_i|\le |b|+12k_1\le d_IH(b),\qquad d_I=1+12k_1.           \tag{16}
\]

The same literal `36K` coefficient bound used in [H, §3] now gives

\[
\Gamma_5(\Phi_p\omega)
 \le C_5d_IH(b)+\Gamma_w(\omega),
\quad
\mathcal R(\Phi_p\omega)
 \le H(b)\{a_I+48\Gamma_w(\omega)\},
\quad a_I=8(1+6C_5d_I).                                    \tag{17}
\]

The original-coordinate Gaussian weighted-series moment theorem [G] yields, for every natural `n`, integrability and

\[
E_Q\mathcal R^n\le M_nH(b)^n,                              \tag{18}
\]

with, for `n≥1`,

\[
M_n=2^{n-1}\{a_I^n+48^nW_w^nm_n^{\rm abs}\},\qquad
m_n^{\rm abs}=E|N(0,1)|^n,
\quad M_0=1.
\]

These are uniform in all parameters under discussion on the **same** interval (6), with no shrink depending on `k` or `b`. In particular compact variation of the cubic pin changes constants, not the degree `n` in height.

The already constructed all-target scalar/whole-residual product law [H, §8] applies to the target (1). Let `ρ` have its original residual law, let `Ψ_p(q,ρ)` be the actual reconstruction and set `S(ρ)=𝓡(Φ_pρ)≥1`. The scalar direction and its direction-divided-by-sigma envelope `U_m` in [H] is still independent of `k,b`; put `J=Σ_{j=0}^5Σ_m w_{j,m}U_m`. The same coefficient triangle inequalities give

\[
\mathcal R(\Psi_p(q,\rho))\le A(|q|+S(\rho)),\quad A=1+8J,
\]

and, with `Z` standard Gaussian under the original law,

\[
S(\operatorname{residualSample}(\omega))
 \le\mathcal R(\Phi_p\omega)+8J|Z(\omega)|.
\]

Consequently

\[
\int S^n\,d\rho\le T_nH(b)^n,\qquad
T_n=2^{n-1}\{M_n+(8J)^nm_n^{\rm abs}\}\quad(n\ge1),          \tag{19}
\]

including integrability. No independence between the two terms in the last display is required. The product-law independence needed for the tube integral is exactly the completed independence of the scalar from the **whole** residual carrier. Its validity at every target, including (1), is part of the reused construction.

## 5. Uniform actual numerator

Let

\[
E_{\rm tail}=\{\varepsilon<h\mathcal R^5\},\qquad
E_{\rm reg}=\{h\mathcal R^5\le\varepsilon,
                    |q|\le K_*h\mathcal R^5\}.
\]

The every-target posterior support and invertibility of `T_h` give the raw target in (1), including all four zero gradients, `Q`-almost everywhere. Thus (13)–(15) apply on its support. We use the generic scalar-product theorem [T], with the new physical bound (13), rather than assert that an old fixed-sixth-pin source wrapper already covers the present target.

Set `D_*=A(1+K_*ε)`. On the pulled-back regular event, the completed regular-cutoff arithmetic gives

\[
\mathcal R\le D_*S,\quad
|q|\le K_*D_*^5hS^5,\quad
W\le(2K_*^2D_*^{12}+8D_*^4)h^4S^{12}.
\]

The scalar interval mass bound (9) and (19) with `n=17` therefore imply

\[
E_Q[W\mathbf1_{E_{\rm reg}}]
 \le N_{17}h^5H(b)^{17},
\quad
N_{17}=2D(K_*D_*^5)(2K_*^2D_*^{12}+8D_*^4)T_{17}.           \tag{20}
\]

For the regularity remainder, sixth-power Markov on (18) at `n=30` gives

\[
Q(E_{\rm tail})\le\varepsilon^{-6}h^6M_{30}H(b)^{30}.
\]

By (14),(18) and Cauchy–Schwarz,

\[
E_Q[W\mathbf1_{E_{\rm tail}}]
 \le10\varepsilon^{-3}\sqrt{M_8M_{30}}\,h^5H(b)^{19}.
                                                                    \tag{21}
\]

Equation (15) reduces the second obstruction in (2) to `E_reg` outside `E_tail`, whenever `W>0`; `W=0` contributes nothing. Summing (20),(21) proves (3), with `N₁₉=10ε⁻³√(M₈M₃₀)`. There is no extra factor depending on `k` except in uniformly controlled constants. No division by `E_QW` or height-uniform normalizer floor occurs.

## 6. Literal raw six-pin density, uniformly in k

Reuse the exact determinant `|det T_h|=12/h⁵` proved in [H, §6]. The observation rows and this transform are unchanged; (1) only changes the evaluation target. The raw Gaussian law is centered with six-pin covariance related to `G` by the same congruence. Therefore its exact density is

\[
p_{\rm raw,6}(x,y;t_{h,b,k})
 =\frac{12}{h^5}(2\pi)^{-3}(\det G)^{-1/2}
   \exp\{-\tfrac12p_{h,b,k}^TG^{-1}p_{h,b,k}\}.              \tag{22}
\]

The frame change on the four gradient rows is orthogonal, of absolute determinant one, so at the zero gradient target this is also the raw density in the original Cartesian gradient coordinates.

Using (6),

\[
(\det G)^{-1/2}\le\gamma^{-3},\quad
p^TG^{-1}p\ge\|p\|_2^2/\Lambda,
\]

and the literal target gives

\[
\|p\|_2^2=(b-kh^3/2)^2+(12k)^2
 \ge\tfrac12b^2-\tfrac14k_1^2\qquad(h\le1).                \tag{23}
\]

Thus (4) holds with, for example,

\[
c=(4\Lambda)^{-1},\qquad
C_d=12(2\pi)^{-3}\gamma^{-3}
                  \exp\{k_1^2/(8\Lambda)\}.
\]

The nonnegative `(12k)²` was only dropped to obtain an upper bound. The shift `−kh³/2` is retained in the exact density (22). Combining (3),(4) gives (5), and a Gaussian times this height polynomial is integrable uniformly in the compact marks and angles. The analytic estimates actually need only a bounded `k` range; the strictly positive `k₀` is needed by the separately owned amplitude-scaled geometric certificate.

## 7. Geometry, compact marks and the exact parameter Jacobian

The actual Campbell application [C] already identifies the canonical raw/confluent whole-carrier posterior pointwise for every literal target. Its bad-mark Rice integrand is a density with respect to **`dx dy du dv`**:

\[
p_{\rm raw,6}(x,y;u,v,0)E[W\mathbf1_{E}\mid u,v,0].          \tag{24}
\]

The floor (6) makes the actual raw observation covariance nonsingular throughout the short-pair domain. At any such pair, its actual original coefficient columns span all six observation rows; otherwise a nonzero row combination would have zero covariance. Select a finite six-column minor at that pair and retain it on a sufficiently small open neighborhood by continuity. The local finite-original-block identity in [C] applies on each such neighborhood. A countable open cover of the second-countable short-pair domain, with a disjoint Borel partition subordinate to it, extends that same nonnegative identity to the present domain. This uses the existing finite-incidence theorem and actual original coefficients, rather than assuming a new global Campbell formula.

For fixed physical positions with distance `h>0`, use `u=b`, `v=b−ℓ`. Then `du dv=db dℓ` in absolute value. Substituting `ℓ=kh³` at these fixed positions gives exactly

\[
du\,dv=h^3\,db\,dk.                                       \tag{25}
\]

This is **`h³`**, the height-target parameter Jacobian from `(b,k)` to `(u,v)`. Conversely the map `(b,ℓ)→(b,k=ℓ/h³)` itself has determinant `h⁻³`; saying which direction the density is being transformed avoids ambiguity. It is distinct from the raw observation multiplier `12/h⁵` in (22).

In short physical midpoint/separation charts,

\[
dx\,dy=dz\,d(he)=h\,dz\,dh\,d\theta.
\]

The full change from `(z,h,θ,b,k)` to `(x,y,u,v)` is block triangular in position and height parameters, even though `v=b−kh³` also depends on `h`. Its absolute determinant is therefore

\[
\boxed{dx\,dy\,du\,dv
       =h^4\,dz\,dh\,d\theta\,db\,dk.}                    \tag{26}
\]

The `h⁴` consists of the distinct position polar factor `h` and height-target factor `h³`. If a later analysis introduces a gap scale `s=(6ℓ)^{1/3}` or `s=ℓ^{1/3}`, its respective derivative is `dℓ=(s²/2)ds` or `dℓ=3s²ds`; that is a further stated change of variables, not an extra factor to insert alongside an unchanged `dk` integral. A normalized posterior law contains none of these base-measure Jacobians.

At fixed `k`, equation (5) is an evaluation of the density on a prescribed height-gap slice; it is not a count on that measure-zero slice. When integrating the full compact band `k∈I`, (25) is a genuine nonsingular height reparametrization at each `h>0`. After the companion furnishes a jointly Borel true noncapture mark with the positive-weight support inclusion `E_bad⊆B`, (5),(24),(26) give its local transformed Campbell density at most

\[
C_dh^4\{N_{17}H(b)^{17}+N_{19}H(b)^{19}\}e^{-cb^2}.          \tag{27}
\]

This is integrable over `z`, all angles, `k∈I`, all birth heights, and `0<h<δ`. In particular the corresponding local small-distance Campbell mass is at most a constant times `δ⁵` (or the same bound with any smaller upper distance). Without the actual mark/inclusion theorem this paragraph remains a conditional application; the analytic obstruction estimate (5) is unconditional. Neither the existence of a capture mark nor any elder/capture equivalence is being inferred from a density slice.

If the companion instead supplies thresholds `ε(k),K(k)` with `inf_I ε(k)>0` and `sup_I K(k)<∞`, take fixed `ε≤inf_I ε(k)` and `K≥sup_I K(k)`: their obstructions are contained in (2), so this proof applies. No deterministic LM004 robustness argument or flow/event measurability proof is duplicated here.

## 8. Reuse and non-claims

The exact inherited source inventory and its original qualification/review limitations remain in [H/REUSED_SOURCES.json]. This addendum reuses them and records its direct dependencies in its new `REUSED_SOURCES.json`. The new obligations resolved here are the compact affine-target moment/density constants, the target-independent physical critical-endpoint lemma (11)–(15), and the compact-mark parameter Jacobian (25)–(26). The old covariance, summability, product-law, source-admission and finite-incidence proofs have not been repeated or requalified.

This is not new Lean code, a Lean ODE/rotation theorem, a new independent/provider-distinct review, an elder/capture equivalence, or global parent/P0.2/GT5 closure. No old proof or source bytes, shared metadata, scientific register, build artifact, commit or external post was changed. A process requirement for reviewing this new conventional application is separate from the already completed reusable mathematics.
