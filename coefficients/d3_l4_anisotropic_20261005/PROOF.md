# An outward anisotropic coefficient enclosure: dimension 3, period 4

Object: **D3-L4-ANISOTROPIC-20261005-v1**  
Author/executor: **OpenAI / GPT-6 Astra Pro; Dylan Roy — delegated AI work**  
Disposition: **author-side mathematical and numerical certificate; nonauthor review pending**.  
Scientific effect: **NONE**. This evaluates the specified coefficient expression, not an independent acceptance of its parent lifetime theorem. No scientific register, proof body, lemma flag or audit verdict is changed.

## 1. Result, scope and dependencies

For the variance-one product-periodic covariance

\[
K_L(z)=\prod_{i=1}^3q_L(z_i),\quad
q_L(t)=\frac{\sum_{n\in\mathbb Z}e^{-(t+Ln)^2/2}}
                 {\sum_{n\in\mathbb Z}e^{-(Ln)^2/2}},\quad L=4,
\]

the coefficient of parent equation (15.2), with ordinary sphere area and the parent's ordered maximum/saddle convention, satisfies the outward rational-decimal enclosure

\[
\boxed{0.040415041992<c_{3,4}<0.040481934343.}                 \tag{1}
\]

The full machine enclosure is in `RESULTS.json`; (1) rounds its endpoints farther outward. The numerical quadrature value is about 0.04044848817, but the digits of that point value are **not** an accuracy claim. The certified ratio is

\[
0.967424069599< c_{3,4}/c_{3,\infty}<0.969025287026.          \tag{2}
\]

Here the subscript infinity denotes the nonperiodic **contact-covariance reference coefficient**, not an infinite-volume persistence theorem.

### Immutable source identities

All repository dependencies below are in `d6g8k5htny-coder/Math-` at commit
`2f8d721e300850e36ab17464dc541c977b3ffcbf` (Math-#297).

| Dependency | Identity |
|---|---|
| `reviews/iba1_periodic_jet_claude_20261005/periodic_jet_check.py` | 15870 bytes; SHA-256 `59b53e5c2e8fdcacc9983f705b9d301fcfcf9242ac6c4d8b7bfbcf0ada7caf9f`; git blob `a2beeeee90abfc2988cf8f491d54ea835b23a1c5` |
| `reviews/iba1_periodic_jet_claude_20261005/RESULTS.json` | SHA-256 `4dbf00f768486dbd3079463699b62ca461d4bf94ead398ce19671769467124f5` |
| `coefficients/side24_v1/PROOF.md` | git blob `44b66f04f89fcd87383b3603fa69f1feb64cdddd` |
| `coefficients/side24_v1/ENCLOSURE.json` | git blob `57af39a05e14ed0ba8ebc00a9b4aca4dffb067c7` |
| `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md` | git blob `dfed3b8d318a3ab1950957f393307733a4bef3f2` |

The equation being evaluated is

\[
c_{3,L}=\frac{\Gamma(7/6)}{24^{1/3}\sqrt\pi}
\int_{S^2}p_G(0)p_V(0)(\tau_u^2)^{2/3}D_u\,d\sigma(u).    \tag{3}
\]

The new computation reimplements #297's exact-periodic product-moment machinery with outward arithmetic and an algebraically equivalent precision restriction. It is checked against the unmodified pinned Schur-complement implementation. It does not substitute the latter's floating output for interval bounds.

For scale normalization we consume the existing SIDE24 certificate:

\[
\begin{split}
0.04177593184059834334&<c_{3,24}<0.04177593184059834335,\\
|c_{3,24}/c_{3,\infty}-1|&<10^{-106},\\
D_0&=29/6-\sqrt6.
\end{split}                                                   \tag{4}
\]

Thus a certified interval for the reference follows by dividing the lower endpoint by \(1+10^{-106}\) and the upper endpoint by \(1-10^{-106}\). This is an explicit dependency, not a fresh independent gamma certificate. Outward rounding retains a nonzero allowance even when 60-digit arithmetic cannot resolve a perturbation of size \(10^{-106}\).

## 2. Periodic moments and the third-derivative conditional variance

Let

\[
\begin{split}
a&=-q''(0),\qquad b=a^2,\qquad k=q^{(4)}(0)-3a^2,\\
k_6&=-q^{(6)}(0)-15q^{(4)}(0)a+30a^3,\qquad
h=k_6-k^2/a.
\end{split}
\]

These are the same coordinate spectral moments/cumulants as #297. The Hessian covariance is

\[
\operatorname{Cov}(H_{ij},H_{kl})
=b(\delta_{ij}\delta_{kl}+\delta_{ik}\delta_{jl}+\delta_{il}\delta_{jk})
+k\,\mathbf1_{i=j=k=l}.                                      \tag{5}
\]

For unit \(u\), write \(S_p=\sum_i u_i^p\), \(t_u=\partial_u^3f\), and \(G=\nabla f\). Cumulant contraction gives

\[
\operatorname{Cov}(G)=aI,\quad
\operatorname{Cov}(t_u,G)=-(3a^2u+ku^{\circ3}),\quad
\operatorname{Var}(t_u)=15a^3+15akS_4+k_6S_6.
\]

Consequently

\[
T(u):=\tau_u^2=\operatorname{Var}(t_u\mid G=0)
=6a^3+9akS_4+hS_6.                                           \tag{6}
\]

The field is centered. Odd and even derivative blocks are independent, so conditioning the even transverse block on the gradient adds no extra covariance correction.

Some outward-computed quantities, shown here only to readable precision, are

| Quantity | Value |
|---|---:|
| \(a\) | 0.989272393327749635 |
| \(q^{(4)}(0)\) | 3.107276066800260115 |
| \(-q^{(6)}(0)\) | 14.345615987938557548 |
| \(k\) | 0.171296462199018774 |
| \(k_6\) | -2.718684780011088295 |
| \(h\) | -2.748345445930609811 |

Until Section 7 the formulas may be read for the finite-image moment law. The uniform tail comparison in that section transfers the result to the exact infinite-image covariance.

Put \(A_*=9ak\). The checker verifies \(h<0\), \(A_*+h<0\), and \(A_*+2h/3<0\). Since \(S_4\in[1/3,1]\) and \(S_4^2\le S_6\le S_4\),

\[
\begin{split}
T_{\min}&=6a^3+A_*+h=4.585751444633847619\ldots,\\
T_{\max}&=6a^3+A_*/3+h/9=6.011972007580747043\ldots .
\end{split}                                                   \tag{7}
\]

The lower value is attained on a coordinate axis, and the upper value on a body diagonal. For the upper bound, maximize the decreasing function \(A_*s+hs^2\) on \([1/3,1]\). For the lower bound use \(hS_6\ge hS_4\). These are all-direction bounds, not extrema estimated from a mesh.

## 3. Exact conditional transverse precision

Choose an orthonormal frame \((u,w,v)\). Set

\[
P=I-uu^\top,\quad E=ww^\top-vv^\top,\quad F=wv^\top+vw^\top.
\]

On the conditioned linear subspace \(V=Hu=0\), write

\[
H=tP+xE+yF,\qquad A=\begin{pmatrix}t+x&y\\y&t-x\end{pmatrix}.
\]

The covariance operator of the full Hessian, in the Frobenius inner product, is
\(\mathcal C_H=2bI+b|I\rangle\langle I|+kP_{\rm diag}\). Its inverse quadratic form is

\[
\langle H,\mathcal C_H^{-1}H\rangle
=\frac{\operatorname{tr}(H^2)}{2b}
-\frac{k\sum_iH_{ii}^2}{2b(2b+k)}
-\frac{b(\operatorname{tr}H)^2}{(2b+k)(5b+k)}.                 \tag{8}
\]

A centered Gaussian conditioned on linear coordinates being zero has precision equal to the restriction of its full precision. Define a 3-by-3 matrix \(W\), whose columns are

\[
p_i=1-u_i^2,\qquad e_i=w_i^2-v_i^2,\qquad f_i=2w_iv_i.
\]

Then the conditional covariance \(C_u=\operatorname{Cov}(t,x,y\mid V=0)\) is the inverse of

\[
\boxed{B_u=C_u^{-1}=\operatorname{diag}(c_0,c_1,c_1)-\kappa W^\top W,}
                                                                  \tag{9}
\]

where

\[
c_1=1/b,\qquad
c_0=1/b-\frac{4b}{(2b+k)(5b+k)},\qquad
\kappa=\frac{k}{2b(2b+k)}.
\]

Because \(\sum H_{ii}^2\le\|H\|_F^2=2(t^2+x^2+y^2)\), one has \(W^\top W\preceq2I\). Therefore

\[
B_u\succeq B_-:=\operatorname{diag}(\beta_0,\beta_s,\beta_s),\quad
\beta_0=c_0-2\kappa>0.5764580152,\quad \beta_s=c_1-2\kappa>\beta_0.
                                                                  \tag{10}
\]

This proves uniform positive definiteness over the whole sphere. It does not infer uniform positivity from #297's finitely sampled Cholesky pivots.

Let \(\Delta_H\) be the determinant of the Hessian covariance in its six raw independent entries. In a coordinate frame,

\[
\Delta_H=b^3(2b+k)^2(5b+k).                                  \tag{11}
\]

Rotating a symmetric matrix preserves this covariance determinant. The raw-coordinate transformation \((t,x,y)\mapsto(A_{11},A_{12},A_{22})\) has absolute determinant 2. The Schur determinant identity thus gives

\[
\det\Sigma_{A\mid V}=4/\det B_u,\qquad
\det\Sigma_V=\Delta_H\det B_u/4.                            \tag{12}
\]

The frame-invariant Frobenius trace is \(2\operatorname{tr}C_u\), not the unweighted trace of the three raw independent entries. The source crosschecks test this as well as all covariance entries, \(T\), and \(\det\Sigma_V\).

## 4. The anisotropic negative-definite cone moment

Let \(J=\operatorname{diag}(1,-1,-1)\). By Sylvester inertia, the eigenvalues of the symmetric matrix \(C_u^{1/2}JC_u^{1/2}\) are \(\lambda,-\mu,-\nu\) with \(\lambda,\mu,\nu>0\).

Positive determinant splits into the positive- and negative-definite cones. The centered Gaussian symmetry \(A\mapsto-A\) assigns the same determinant-squared moment to each. Hence, for independent standard normals \(Z_i\),

\[
D_u=\frac12\mathbb E\big(\lambda Z_0^2-\mu Z_1^2-\nu Z_2^2\big)_+^2.  \tag{13}
\]

Write \(Z=Rn\), with \(n\) uniform on \(S^2\), \(R\) independent, and \(\mathbb E R^4=15\). For fixed azimuth \(\psi\), set
\(\beta=\mu\cos^2\psi+\nu\sin^2\psi\). The remaining spherical coordinate \(z=n_0\) is uniform on \([-1,1]\), and the positive quadratic form occurs for \(|z|>\sqrt{\beta/(\lambda+\beta)}\). Integrating its square explicitly gives

\[
\boxed{
D_u=\frac1{4\pi}\int_0^{2\pi}
\left[3\lambda^2-4\lambda\beta+8\beta^2
-\frac{8\beta^{5/2}}{\sqrt{\lambda+\beta}}\right]\,d\psi.}   \tag{14}
\]

There is no isotropy assumption in (14). In particular \(\mu\) and \(\nu\) need not coincide. In the nonperiodic reference, \((\lambda,\mu,\nu)=(5/3,1,1)\), and (14) gives exactly \(D_0=29/6-\sqrt6\). Half the untruncated determinant-square moment would give \(29/6\), which is wrong.

### Certified evaluation of the one-angle integral

Set

\[
m=(\mu+\nu)/2,\quad d=(\mu-\nu)/2,\quad
\delta=d/m,\quad t=m/(\lambda+m).
\]

Writing \(\mathbb E_\psi\) for the uniform angular average, (14) becomes

\[
D_u=\tfrac32\lambda^2-2\lambda m+4m^2+2d^2
-4m^2\sqrt t\,\mathbb E_\psi
 [(1+\delta\cos2\psi)^{5/2}(1+t\delta\cos2\psi)^{-1/2}].     \tag{15}
\]

Expand the product in powers of \(z=\delta\cos2\psi\). At degree \(n\) its coefficient is

\[
p_n(t)=\sum_{i=0}^{n}\binom{5/2}{i}\binom{-1/2}{n-i}t^{n-i}.
\]

Every retained angular monomial is integrated exactly: odd powers vanish, and
\(\mathbb E\cos^{2j}(2\psi)=\binom{2j}{j}/4^j\). The checker retains degrees through 16. For \(0<t<1\), \(|\binom{5/2}{i}|\le3\) and \(|\binom{-1/2}{j}|\le1\). With any outward bound \(\rho\ge|\delta|<1\), the entire omitted angular-average remainder is at most

\[
3\sum_{n\ge17}(n+1)\rho^n
=3\rho^{17}\frac{18-17\rho}{(1-\rho)^2}.                    \tag{16}
\]

Multiply (16) by \(4m^2\sqrt t\) for an absolute cone-moment error. The implementation bounds even the omitted odd terms, although their integrals are zero. The maximum \(\rho\) at the 128-by-128 quadrature nodes is below 0.041922. This mesh maximum is used only for node evaluations; the independent all-direction estimate in Section 6 controls between-node variation.

The positive eigenvalue is bracketed using the characteristic polynomial of \(C_uJ\), which is similar to \(C_u^{1/2}JC_u^{1/2}\). For each evaluated covariance, interval signs bracket its unique positive root in \((1,2)\); an interval derivative lower bound, residual bound and two interval Newton refinements enclose it. A nearest-rounded Newton predictor supplies no evidence by itself. The proof of inertia then gives

\[
m=(\lambda-\operatorname{tr}(C_uJ))/2,\qquad
d^2=m^2-\det(C_u)/\lambda\ge0.
\]

Using \(d^2\) avoids subtraction of two nearly equal negative eigenvalues. No eigenvalue derivative is needed in the angular error proof.

### Independent integral formulation for falsification

The substitution \((t,x,y)=r_0(-1,r\cos\psi,r\sin\psi)\), with \(r_0>0\) and \(0\le r<1\), integrates the Gaussian radial variable analytically and gives

\[
D_u=\frac{15\sqrt{\det B_u}}{4\pi}
\int_0^1\int_0^{2\pi}r(1-r^2)^2
 [(-1,r\cos\psi,r\sin\psi)^\top B_u(-1,r\cos\psi,r\sin\psi)]^{-7/2}
\,d\psi\,dr.                                                \tag{17}
\]

The separate floating disk-midpoint calculations in `CROSSCHECKS.json` test (14) against (17). They are diagnostics, not the enclosure in (1). The infinite radial integral is exact: no radial cutoff or Gaussian-tail truncation remains.

## 5. Directional integrand and symmetry reduction

Dividing (3) by its nonperiodic reference yields

\[
R(u)=\frac{2\sqrt3}{a^{3/2}\sqrt{\Delta_H}\,6^{2/3}D_0}
\frac{T(u)^{2/3}D_u}{\sqrt{\det B_u}},\qquad
\frac{c_{3,4}}{c_{3,\infty}}=\frac1{4\pi}\int_{S^2}R(u)\,d\sigma(u).
                                                                  \tag{18}
\]

Only the actual coordinate-reflection symmetry of the cubic periodic law is used. On the octant set

\[
u=(\sin\theta\cos\phi,\sin\theta\sin\phi,\cos\theta),\quad
w=(\cos\theta\cos\phi,\cos\theta\sin\phi,-\sin\theta),\quad
v=(-\sin\phi,\cos\phi,0),
\]

for \(0\le\theta,\phi\le\pi/2\). This smooth frame is used even at the polar parameter boundary; the physical moment is frame-invariant there.

Let \(N=128\), \(s=\pi/(2N)\), \(\theta_i=\phi_i=(i+1/2)s\), and
\(w_i=\cos(is)-\cos((i+1)s)\). The outward quadrature is

\[
Q_N=\frac1N\sum_{i=0}^{N-1}w_i\sum_{j=0}^{N-1}R(\theta_i,\phi_j).    \tag{19}
\]

The polar weights are exact integrals of \(\sin\theta\), evaluated outward. Consequently constant functions integrate exactly; this avoids an unnecessary sphere-area bias.

Representative conditional moments (rounded, with the full node enclosures in `CROSSCHECKS.json`) are

| Direction | \(T(u)\) | \(D_u\) | \(R(u)\) |
|---|---:|---:|---:|
| Coordinate axis | 4.5857514446 | 2.6031895133 | 0.9314637606 |
| Face diagonal | 5.8844456540 | 2.4053569351 | 0.9882982913 |
| Body diagonal | 6.0119720076 | 2.3415333593 | 0.9662041191 |

The calculation does not hold any of these values fixed while integrating the sphere.

## 6. Proved all-direction quadrature error

Equation (17) cancels the factor \(\sqrt{\det B_u}\) in (18), so the remaining covariance dependence is a positive integral of \(q^{-7/2}\), where \(q=X^\top B_uX\). This is useful both for derivative bounds and for an integrand envelope.

For either angular coordinate, the full frame rotates with generator norm at most one. Thus \(\|H'\|_F\le2\|H\|_F\) and \(\|H''\|_F\le4\|H\|_F\). Since only the diagonal-square term of (8) varies,

\[
|q'|/q\le q_1:=8\kappa/\beta_0,\qquad
|q''|/q\le q_2:=32\kappa/\beta_0.                            \tag{20}
\]

For the sphere power sums, tangent projection gives

\[
|S_4'|\le2,\quad |S_6'|\le3,\quad
|S_4''|\le16,\quad |S_6''|\le36.                            \tag{21}
\]

For example, \(\|\nabla_{S^2}S_4\|^2=16(S_6-S_4^2)\le4\), by the variance bound for a random variable in \([0,1]\) with weights \(u_i^2\). The analogous calculation uses \(u_i^4\) for \(S_6\). The second-derivative bounds follow from \(\|u'\|,\|u''\|\le1\) and the ordinary second derivative of \(u_i^p\).

Define

\[
t_1=\frac{2A_*+3|h|}{T_{\min}},\qquad
t_2=\frac{16A_*+36|h|}{T_{\min}}.                            \tag{22}
\]

Since \(B_u\succeq B_-\), the positive integral in (17) implies

\[
R(u)\le R_*:=\frac{2\sqrt3\,T_{\max}^{2/3}}
 {a^{3/2}\sqrt{\Delta_H}\,6^{2/3}D_0}
\frac{D(B_-^{-1})}{\sqrt{\det B_-}}
<1.143532183656.                                             \tag{23}
\]

The comparison covariance \(B_-^{-1}\) is diagonal with equal last two entries, so its moment is given directly by (14). It is used **only as an upper bound**; it is not the covariance used at the quadrature nodes.

Differentiating the positive integrand establishes the following uniform bounds for either coordinate:

\[
\begin{split}
|R'|&\le M_1=R_*\left(\tfrac23t_1+\tfrac72q_1\right),\\
|R''|&\le M_2=R_*\left(
\tfrac23t_2+\tfrac29t_1^2+\tfrac{14}3t_1q_1+
\tfrac{63}4q_1^2+\tfrac72q_2\right).
\end{split}                                                   \tag{24}
\]

The checker obtains \(M_1<4.161419802375\) and \(M_2<44.544592614265\). Differentiation under (17) is legitimate because the compact disk has the uniform positive quadratic-form lower bound (10); the derivatives have the displayed integrable majorants.

For a polar cell centered at \(m\),
\(\left|\int(\theta-m)\sin\theta\,d\theta\right|\le s^3/12\).
The second-order Taylor remainder contributes at most \(M_2s^3/24\) per cell. The ordinary midpoint average in \(\phi\) contributes at most \(s^2M_2/24\). Summing the polar cells gives the fully explicit ratio-error bound

\[
\boxed{
E_{\rm angular}\le\frac\pi2s^2\left(\frac{M_1}{12}+\frac{M_2}{24}\right)
+\frac{s^2M_2}{24}
<0.000800608712954.}                                        \tag{25}
\]

Thus its contribution to the coefficient error is less than
\(0.000033446175023320\). Neither the agreement of successive meshes nor the sampled maximum anisotropy is used to assert (25).

## 7. Image sum and transfer to the exact periodic law

As in #297, retain images \(|n|\le10\). The first omitted point is \(x=44\). For the probabilists' Hermite polynomials of even degrees through 6, \(|\mathrm{He}_j(x)|\le2x^j\) for \(x\ge10\). The consecutive majorant ratio for \(x^6e^{-x^2/2}\) is less than 1/2, verified outward. The two-sided omitted sum in each unnormalized derivative is bounded by

\[
T_{\rm img}=8\,44^6e^{-968}
<2.326738433\times10^{-410}.                                 \tag{26}
\]

Since both finite and full normalizing sums are at least 1, and the finite normalized moments have absolute value below 15, each coordinate-moment error is at most \(16T_{\rm img}\). Bounds \(a<1\), \(m_4<4\), \(m_6<15\), including the image allowances, are verified in the checker. Coordinate products of total degree at most 6 then have error at most \(80T_{\rm img}\): the largest case is \(m_4a\), with bound \((4+1)16T_{\rm img}\).

The sum of absolute contraction coefficients for at most six unit directions in dimension 3 is at most \((\sqrt3)^6=27\). Therefore any such derivative contraction differs by at most \(2160T_{\rm img}\). The svec factors cost at most 2, and the joint vector \((G,t_u,\operatorname{svec}H)\) has dimension 10. Its covariance operator difference is at most

\[
43200T_{\rm img}.                                           \tag{27}
\]

The finite-image Hessian covariance has minimum eigenvalue at least \(2b>1/5\). In the odd derivative block, the nontrivial two-dimensional block has determinant \(aT\) and trace \(a+\operatorname{Var}(t_u)\). Since \(k_6<0\),
\(\operatorname{Var}(t_u)\le15a^3+15ak\). The checker verifies

\[
\frac{aT_{\min}}{a+15a^3+15ak}>1/5.
\]

This is a uniform lower bound for the whole joint covariance. Hence its exact/finite relative Loewner error is bounded by
\(\epsilon=216000T_{\rm img}\).

Loewner comparisons pass to marginals and Schur complements by the variational characterization of a Schur complement. Comparing centered Gaussian densities and integrating the nonnegative homogeneous cone function gives the same comparison used in the pinned SIDE24 proof: the full coefficient integrand ratio lies between

\[
(1-\epsilon)^{25/6}/(1+\epsilon)^{9/2}
\quad\hbox{and}\quad
(1+\epsilon)^{25/6}/(1-\epsilon)^{9/2}.
\]

For \(\epsilon<10^{-3}\), these are within \(32\epsilon\) of 1 (elementary logarithm/exponential bounds suffice). The checker also verifies \(R_*c_{3,\infty}<1\). Therefore the **absolute coefficient** image error is below \(6912000T_{\rm img}\), and the deliberately looser amount actually added to the final interval is

\[
E_{\rm image}=10^8T_{\rm img}
<2.326738433\times10^{-402}.                                 \tag{28}
\]

For the point checks, the implementation additionally verifies uniform envelopes below 10 for T, R, and the cone moment (the latter follows from B <= diag(c0,c1,c1), B >= B_minus and the positive density integral). The same covariance comparison makes 10^9 T_img a conservative image allowance for each displayed point interval.

This comparison also avoids assuming that a finite spatial-image truncation is globally positive definite as a periodic kernel: only the explicitly positive finite jet covariance is used as the comparison Gaussian law.

## 8. Arithmetic, error ledger and replay

`certificate.py` uses only the Python standard library. Its interval endpoints are 60-significant-digit Decimals, with explicit FLOOR/CEILING contexts for arithmetic. Integer powers use repeated directed multiplication. Square root, exponential and logarithm are bracketed by adjacent representable values around correctly rounded nearest results. The fractional power \(x^{2/3}\) is evaluated via outward \(\exp((2/3)\log x)\), not a noninteger `Decimal.power` call.

Pi is enclosed by Machin's identity and alternating-series tails. Sine and cosine use 60 Taylor terms with explicit uniform remainders on \([0,2]\). Floats and booleans are rejected as certificate inputs. Matrix positivity, eigenvalue brackets, series-domain constraints and uniform estimate hypotheses are executable guards, not assertions disabled by `-O`.

The standard-library arithmetic contract is documented in the Python `decimal` reference, specifically directed rounding, `exp`, `ln`, `sqrt`, `next_minus`, and `next_plus`: `https://docs.python.org/3/library/decimal.html`. This is a trusted numerical-library dependency, not a claim that the Python interpreter has itself been formally verified.

At \(N_\theta=N_\phi=128\), the distinct contributions are:

| Contribution | Absolute coefficient bound |
|---|---:|
| Omitted periodic images | < 2.326738433e-402 |
| Cone-angle series remainder | < 7.215919417e-25 |
| Directional quadrature | < 3.3446175023320e-5 |
| Outward arithmetic plus imported reference scale | quadrature-interval **width** < 9.682246784e-21 |
| Gaussian radial cutoff | 0: the radial integral is exact |

The last nonzero row is a width, not an independently centered error radius. The implementation first encloses the entire node sum times its reference interval, then widens by the three explicit error allowances. It does not add an unexplained floating tolerance.

Normal `python -B -S certificate.py --n 128` and optimized `python -B -O -S certificate.py --n 128` runs produced byte-identical `RESULTS.json`. The seven unit tests pass in both modes. The tests cover the reference cone, rejection of half the untruncated moment, interval guards, long-exact-input outward powers, moment/positivity bounds, exact reference angular normalization and cubic reflection symmetry.

`source_crosscheck.py` verifies the SHA-256 of the upstream code before importing it. At five directions it checks that all entries of the original Schur complement (transformed to \((t,x,y)\)), its third-derivative conditional variance, determinant of V and Frobenius trace lie in the new intervals. It also tests a rational transverse-frame rotation and the separate disk integral. A separate 270-digit evaluation of the known nonperiodic closed form gives

\[
c_{3,\infty}\approx0.04177593184059834334293666542857555646668,
\]

inside the imported SIDE24 interval. That gamma evaluation is a diagnostic crosscheck; it is not used as the reference enclosure. The complete unmodified #297 replay was also executed, and its output SHA-256 matches the published `RESULTS.json` exactly.

The L=4 enclosure is disjoint from the reference and SIDE24 intervals. It establishes a reduction of between approximately 3.097% and 3.258% from the reference. The approximately 3.18% point estimate is not a separately certified many-digit result.

## 9. What is and is not closed

For the expression (3), this packet supplies the previously missing anisotropic 2-by-2 cone integral, an actual directional evaluation, a proved all-direction quadrature error, a uniform image-tail transfer and outward numerical arithmetic. No missing estimate is concealed behind a mesh-convergence heuristic.

The remaining scientific process is nonauthor review of this new derivation and implementation. In particular the determinant-coordinate factors in (12), the cone factor one-half in (13), the image transfer in Section 7, and the weighted quadrature bound (25) merit source-bound review. The work is not Lean-verified, no hosted CI result is claimed, and no repository-wide test suite or parent-theorem audit is claimed. It does not evaluate dimension 4, certify a finite-radius remainder, or alter a lifetime-theorem acceptance state.
