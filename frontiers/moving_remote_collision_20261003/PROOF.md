# A quantitative moving-remote-cutoff bound for planar window collisions

**Object:** C107-MOVING-RHO-COLLISION-20261003-v1.  
**Disposition:** author-side proof candidate, requiring full nonauthor review.  
**Authors:** OpenAI Codex root and /root/c99_custody_audit; author-side construction discussion is shared. Same-provider independence credit: 0. Human mathematical review: NONE. Scientific/register effect: NONE.

## 1. Conditional setting and result

Fix \(L>0\), \(X=\mathbb R^2/(L\mathbb Z^2)\), a compact birth interval \(B\), and a compact \(K=[k_-,k_+]\subset(0,\infty)\). Use the variance-one periodized Gaussian field of P §2:

\[
 \mathbb E f(z)f(w)=\sum_{n\in\mathbb Z^2}a_n e^{2\pi i n\cdot(z-w)/L},
 \qquad a_n=\frac{e^{-2\pi^2|n|^2/L^2}}{\sum_j e^{-2\pi^2|j|^2/L^2}}.
 \tag{1}
\]

All \(a_n>0\), and \(\sum_n\sqrt{a_n}(1+|n|)^m<\infty\) for every fixed \(m\). In particular the field has smooth versions with all finite moments of each global \(C^m\) norm. The torus need not be rotationally invariant; frames below are observation coordinates only.

Let \((u,v)\) be any orthonormal frame, \(M=-ru/2\), \(S=ru/2\), and let \(Q_r=Q_{r,b,k,u,v}\) be the actual Gaussian law conditioned on

\[
 f(M)=b,\quad f(S)=b-kr^3,\quad \nabla f(M)=\nabla f(S)=0.
 \tag{2}
\]

For a symmetric matrix \(H\), put \(F_j(H)=|\det H|\mathbf1_{\{H\text{ has exactly }j\text{ negative eigenvalues and is nonsingular}\}}\). Set

\[
 W_r=F_2(H_M)F_1(H_S),\qquad Z_r=E_{Q_r}W_r,
 \qquad dQ_r^W=(W_r/Z_r)dQ_r.
 \tag{3}
\]

The retained parent interface is the full normalizer, not a normalizer restricted to a favorable event:

\[
 z_*r^2\le Z_r\le z^*r^2\quad(0<r\le r_*),
 \tag{4}
\]

uniformly on these fixed compact marks and all frames. This is P (5.4)–(5.5), read with E1 and REC. We also retain the smooth Gaussian conditioning and weighted Kac–Rice interface specified in §2. No elder event, cap theorem, topology trap, or persistence identification is used in this proof.

Write \(I_r=(b-kr^3,b)\) and \(D_\rho=\{x:\operatorname{dist}_X(x,0)\ge\rho\}\). For a deterministic Borel set \(E\subset D_\rho\), let

\[
 N(E)=\#\{x\in E:\nabla f(x)=0,\ f(x)\in I_r\},
 \tag{5}
\]

counting all Morse indices. The pins do not belong to \(D_\rho\) on the radius band below. The measure \(|E|\) means unnormalized torus area, with \(|X|=L^2\). Factorial pairs are ordered: \((N)_2=N(N-1)\).

**Theorem.** There are \(C<\infty\), \(r_*>0\), and \(0<\rho_0\le\min(1,L/32)\), depending only on \(L,B,K\) and the retained source interfaces, such that for

\[
 0<\rho\le\rho_0,\qquad 0<r\le\min(r_*,\rho/8),
 \tag{6}
\]

all frames and all deterministic Borel \(E\subset D_\rho\),

\[
 E_{Q_r^W}(N(E))_2\le C r^5\rho^{-98}|E|.                 \tag{7}
\]

More precisely, the ordered near pairs with \(0<\operatorname{dist}_X(x,x')<\rho/8\) have expectation at most \(Cr^5\rho^{-98}|E|\), and the complementary separated pairs have expectation at most \(Cr^6\rho^{-98}|E|^2\).

Consequently

\[
 Q_r^W\{N(E)\ge2\}\le\tfrac12Cr^5\rho^{-98}|E|,
 \qquad E_{Q_r^W}[N(E)\mathbf1_{N(E)\ge2}]\le Cr^5\rho^{-98}|E|.
 \tag{8}
\]

If \(0<\alpha<1/49\) and \(\rho=r^\alpha\), (6) holds for all sufficiently small \(r\), and uniformly for deterministic \(E_r\subset D_{r^\alpha}\),

\[
 r^{-3}E_{Q_r^W}(N(E_r))_2\le C r^{2-98\alpha}|E_r|\longrightarrow0.
 \tag{9}
\]

For example \(\alpha=1/100\) gives \(2-98\alpha=51/50\). No optimality is asserted for 98 or for the allowed powers \(\alpha\). Both witnesses in every counted pair must be outside the pin ball; mixed inner/outer pairs are not included.

## 2. Exact sources and consumption boundary

The six original snapshots in sources/ are bound by commit, original path, Git blob, UTF-8 byte length and SHA256 in SOURCE_IDENTITIES.json. The source cut is Math- commit 7e2344166e989ae94e5732e445f445598fc75c4c; the local custody clone's checkout HEAD is irrelevant to these explicitly addressed Git objects.

| Key | Exact source path at that cut | Consumption here |
|---|---|---|
| P | imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md | §2 Fourier model, §3 desingularized pins, §4 Fourier conditional moments, §5 gradient averages and full \(Z_r\) floor |
| E1 | imports/lifetime_parent_20260925/ERRATUM_CONGRUENCE.md | Corrected \(\operatorname{diag}(r^{-1/2},I)\) congruence whenever P's §5 normalizer is consumed |
| E2 | reviews/d1_section9_borel_repair_20260925/REPAIR.md | Exact continuous-cylinder/finite-measure Borel reading of the weighted Kac–Rice interface; no elder conclusion imported |
| REC | reviews/d1_chain_reconciliation_20260928/RECONCILIATION.md | Source reconciliation, normalizer reading, and §7 separation of the remote count from D1 selection |
| RM | frontiers/remote_window_20260924/PROOF.md | Model, actual pin/weight conventions and remote counting setup; no moving-cutoff mean-measure conclusion imported |
| RC | frontiers/remote_collision_20260928/PROOF.md | §§3–7 pair Kac–Rice/divided-difference mechanism; its fixed-\(\rho\) covariance floor is replaced quantitatively below |

These are conditional source interfaces, not a new acceptance of their parent theorems. RC §8 expressly excludes uniformity as \(\rho\downarrow0\); that missing quantitative dependence is the new assertion proved here. We use RC's two-point counting method but no conclusion about the global torus event or its first moment. The present result is planar and keeps fixed positive compact \(K\). It neither removes the region \(|x|<\rho\), nor supplies an elder or barcode identification.

## 3. Two regularized six-coordinate observation blocks

All differentiations in a local orthonormal frame mean physical derivatives. For endpoints \(a=-r/2,c=r/2\) on the \(u\) axis, write \(f(t,z)=f(tu+zv)\) locally and define

\[
 U_r(f)=\left(\frac{f(a,0)+f(c,0)}2,\frac{f(c,0)-f(a,0)}r,
 \frac{f_t(c,0)-f_t(a,0)}r,
 \frac6{r^2}\left[f_t(a,0)+f_t(c,0)-2\frac{f(c,0)-f(a,0)}r\right],
 \frac{f_z(a,0)+f_z(c,0)}2,\frac{f_z(c,0)-f_z(a,0)}r\right).
 \tag{10}
\]

For \(r>0\) this is an invertible linear transform of the six actual pin observations. Its target is

\[
 u_r=(b-kr^3/2,-kr^2,0,12k,0,0),                         \tag{11}
\]

and its confluent limit is \(U_0=(f,f_t,f_{tt},f_{ttt},f_z,f_{tz})(0)\). The coordinates have integral derivative representations of order at most three, including the trapezoid identity for the fourth coordinate. Thus their covariance and all cross-covariances extend continuously to \(r=0\), uniformly in frames. P §3 supplies, after decreasing \(r_*\),

\[
 cI\le\operatorname{Cov}(U_r)\le CI,\qquad |u_r|\le C. \tag{12}
\]

For clarity, a polynomial right inverse of (10), for arbitrary data \(A=(A_0,\ldots,A_5)\), is

\[
 p_U(t,z)=A_0-r^2A_2/8+(A_1-r^2A_3/24)t
             +(A_2/2)t^2+(A_3/6)t^3+z(A_4+A_5t).
 \tag{13}
\]

Direct substitution gives \(U_r(p_U)=A\), including \(r=0\), and its coefficients are bounded by \(C|A|\) for \(r\le1\).

For a near witness pair, use its unique short lift \(x'=x+\delta e\), \(0<\delta<\rho/8\), with local coordinates \(s\) along \(e\), \(z\) along either perpendicular unit vector. Use gradient components in this frame, and put

\[
 V_\delta=(g_\parallel,g_\perp,G_\parallel,G_\perp,h,D),\quad
 g=\nabla f(x),\quad G=\frac{\nabla f(x')-\nabla f(x)}\delta,
 \quad h=f(x),
 \quad D=\frac{f(x')-f(x)-(\delta/2)e\cdot(\nabla f(x)+\nabla f(x'))}{\delta^3}.
 \tag{14}
\]

For a smooth scalar function \(g_0(s)=f(x+se)\),

\[
 D=-\frac1{2\delta^3}\int_0^\delta s(\delta-s)g_0'''(s)\,ds,
 \tag{15}
\]

so \(D\to-\partial_e^3f(x)/12\). The other limits are \(g=\nabla f(x)\), \(G=H_xe\), and \(h=f(x)\). Again all coordinates are bounded integral derivative functionals through order three. For prescribed \(B=(g_\parallel,g_\perp,G_\parallel,G_\perp,h,D)\), the polynomial

\[
 p_V(s,z)=h+g_\parallel s+g_\perp z
              +\tfrac12(G_\parallel+6\delta D)s^2-2Ds^3+G_\perp sz
 \tag{16}
\]

satisfies \(V_\delta(p_V)=B\), with uniformly bounded coefficients for \(\delta\le1\), through \(\delta=0\). Equations (13) and (16) are only local polynomial data interpolants. The actual periodic Fourier duals are constructed next.

## 4. Explicit finite-Fourier interpolation with cost \(\rho^{-7}\)

### 4.1 Periodic separators and their inverse derivatives

Put \(\omega=2\pi/L\) and, for a site \(p\in X\),

\[
 \psi_p(z)=\sum_{j=1}^2[1-\cos(\omega(z_j-p_j))].        \tag{17}
\]

This is a globally defined real trigonometric polynomial. Its value and first derivatives vanish at \(p\), and on the whole torus

\[
 c_L\operatorname{dist}_X(z,p)^2\le\psi_p(z)
    \le C_L\operatorname{dist}_X(z,p)^2.                 \tag{18}
\]

This follows by taking each minimal coordinate displacement in \([-L/2,L/2]\) and using the elementary comparison \(1-\cos t\asymp t^2\) there. Likewise

\[
 |D\psi_p|\le C_L d_p,\quad |D^j\psi_p|\le C_L\ (j=2,3),
 \qquad d_p=\operatorname{dist}_X(z,p).                 \tag{19}
\]

Differentiating a reciprocal through order three and using (18)–(19) gives

\[
 |D^j(\psi_p^{-1})|\le C_L d_p^{-2-j}\quad(0\le j\le3),
 \tag{20}
\]

with constants enlarged on distances bounded below by a fixed positive number. For example the third derivative is a sum of terms \(\psi^{-2}D^3\psi\), \(\psi^{-3}D\psi D^2\psi\), and \(\psi^{-4}(D\psi)^3\); the first has order at worst \(d^{-4}\le C_Ld^{-5}\), and the others have order \(d^{-5}\). Therefore, if \(q=\prod_{i=1}^m\psi_{p_i}\) and every \(d_{p_i}\ge c\rho\) on a neighborhood, then

\[
 \|D^j(q^{-1})\|\le C\rho^{-2m-j}\quad(0\le j\le3).
 \tag{21}
\]

Repeated sites are allowed. The Fourier coefficient \(\ell^1\) norm of \(q\), and all its fixed-order derivatives, are bounded independently of the sites. Its frequency support has \(|n|_1\le m\).

### 4.2 A local sine chart and a separation-stable Hermite formula

At any center \(c\in X\), use the small physical lift and the chart

\[
 S_c(z)_j=\omega^{-1}\sin(\omega(z_j-c_j)).              \tag{22}
\]

On the fixed coordinate box \(|z_j-c_j|<L/16\) the chart is injective, its derivative is uniformly invertible, and the inverse and its derivatives through order three are bounded by constants depending only on \(L\). This follows directly from the coordinatewise arcsine inverse. Shrink \(\rho_0\) within the bound in (6), if necessary. All chart segments and neighborhoods below then stay in this box.

Let two physical sites lie in a ball of radius \(\rho/8\) about this center. Their distinct chart images have chord length \(h>0\). Since the chart and its inverse are Lipschitz on the box, \(h\) is comparable to their physical distance. Choose an orthonormal chart basis along this chord and perpendicular to it, and translate the first chart image to \((0,0)\); the second is \((h,0)\). This choice does not identify the chart chord with the physical chord. Orthogonal changes and bounded translations have uniformly bounded coefficients. The chart segment's inverse lies within distance \(\rho/4\) of the center: indeed \(|S_c(z)|\le|z-c|\) and the inverse has Lipschitz constant at most two. We can take a neighborhood of the segment whose inverse lies within \(\rho/3\).

For a \(C^3\) function \(F(t,y)\) on that neighborhood, the polynomial

\[
 P_F(t,y)=a_0+a_1t+a_2t^2+a_3t^3+y(b_0+b_1t)            \tag{23}
\]

matches its value and full first gradient at both chart sites if

\[
\begin{split}
 a_0&=F(0,0),& a_1&=F_t(0,0),\\
 a_2&=3[F(h,0)-F(0,0)]/h^2-[2F_t(0,0)+F_t(h,0)]/h,\\
 a_3&=[F_t(h,0)+F_t(0,0)]/h^2-2[F(h,0)-F(0,0)]/h^3,\\
 b_0&=F_y(0,0),& b_1&=[F_y(h,0)-F_y(0,0)]/h.
\end{split}                                                        \tag{24}
\]

There is no loss of a power of \(h\) in these coefficients. To see this without estimating the summands separately, put \(g(t)=F(t,0)\). Integration by parts gives

\[
 a_3=h^{-3}\int_0^h t(h-t)g'''(t)\,dt,\quad
 a_2=\frac1{2h}\int_0^h g''(t)\,dt-\tfrac32ha_3,
 \quad b_1=h^{-1}\int_0^h F_{ty}(t,0)\,dt.              \tag{25}
\]

Thus \(|a_3|\le\|F_{ttt}\|_\infty/6\), \(|a_2|\le\|F_{tt}\|_\infty/2+h\|F_{ttt}\|_\infty/4\), and \(|b_1|\le\|F_{ty}\|_\infty\). The coefficient norm of (23) is at most \(C_L\|F\|_{C^3}\), uniformly as \(h\downarrow0\). The limits are exactly the confluent Taylor coefficients \(g''(0)/2,g'''(0)/6,F_{ty}(0,0)\). These identities also prove stability when the chord direction changes: only orthonormal-coordinate derivatives occur.

### 4.3 Duals for both close pairs

Consider \(0<r\le\rho/8\), \(0<\delta<\rho/8\), \(x,x'\in D_\rho\). To prescribe arbitrary \(U_r\) data \(A\) while killing the witness block, take the local polynomial (13) and

\[
 q_P(z)=\psi_x(z)\psi_{x'}(z).
 \tag{26}
\]

It kills value and gradient at both witnesses. On the ball of radius \(\rho/3\) about 0, the distance to both witnesses is at least \(2\rho/3\). On that ball define \(g=p_U/q_P\). Equations (13), (21), and \(\rho\le1\) show \(\|g\|_{C^3}\le C\rho^{-7}|A|\). Transform \(g\) by the inverse chart \(S_0^{-1}\), apply (23)–(25) at the two pin images, and transform the resulting polynomial back to chart coordinates before forming

\[
 \phi_P(z)=q_P(z)P_g(S_0(z)).                            \tag{27}
\]

Here \(P_g\) includes the chart chord translation and rotation from §4.2. The chain rule gives exact equality of the physical values and gradients with \(p_U\) at both pins. Multiplication by \(q_P\) also gives value and gradient zero at both witnesses. Consequently

\[
 (U_r,V_\delta)(\phi_P)=(A,0).
 \tag{28}
\]

To prescribe arbitrary witness data \(B\) while killing pins, use (16) in the physical frame based at \(x\), and

\[
 q_W(z)=\psi_M(z)\psi_S(z),\qquad
 \phi_W(z)=q_W(z)P_{p_V/q_W}(S_x(z)).                    \tag{29}
\]

The distances from \(x\) to the pins are at least \(\rho-r/2\ge15\rho/16\). On the ball of radius \(\rho/3\) about \(x\) they therefore remain at least \(29\rho/48\). The same argument gives

\[
 (U_r,V_\delta)(\phi_W)=(0,B),\qquad
 \|\widehat{\phi_P}\|_{\ell^1}+\|\widehat{\phi_W}\|_{\ell^1}
       \le C\rho^{-7}(|A|+|B|).                         \tag{30}
\]

These are actual globally periodic real trigonometric polynomials. A degree-three polynomial in the two sine chart coordinates has frequencies \(|n|_1\le3\), even after the affine chord-coordinate change. Multiplication by two \(\psi\) factors gives \(|n|_1\le5\). In particular all duals lie in the single, parameter-independent real Fourier space \(|n|_1\le7\). The coefficient norm estimate follows from the polynomial coefficient bound and the bounded \(\ell^1\) norms of the sine factors, separator factors, and affine-coordinate coefficients. It does not treat nonperiodic monomials as RKHS elements.

The argument also controls simultaneous confluence \(r\to0\), \(\delta\to0\). For fixed positive \(\rho\), the Fourier coefficient vectors in (30) are bounded in a finite-dimensional space. Along any convergent parameter sequence they have convergent subsequences; applying the continuous limiting observation functionals from §3 proves (28)–(30) at the limiting parameter. At a vanishing chord one may equivalently use the confluent coefficients of (25). No globally continuous choice of a perpendicular frame or dual vector is needed. Explicitly, if the killed witnesses coalesce then \(q_P=\psi_x^2\) has a zero of order four and annihilates all witness contact derivatives through order three; if the pins coalesce then \(q_W=\psi_0^2\) similarly kills the full \(U_0\) jet. Passing the exact zero observations to the limit gives the same conclusion.

### 4.4 Separated witnesses, including distant points on the torus

If \(\operatorname{dist}_X(x,x')\ge\rho/8\), use the six raw witness observations

\[
 V^{\rm sep}=(\nabla f(x),\nabla f(x'),f(x),f(x')).       \tag{31}
\]

For the pin block the construction (26)–(28) still works, with no restriction on witness separation: both witnesses are at least \(\rho\) from 0. For one witness singleton, say \(x\), use

\[
 q_x=\psi_M\psi_S\psi_{x'},                            \tag{32}
\]

and a local affine physical polynomial \(p\) realizing its prescribed value and gradient. At \(x\), all three killed-site distances are at least \(c\rho\). Take the value and first derivative of \((p/q_x)\circ S_x^{-1}\) at the chart origin and use its affine Taylor polynomial. By (21) with \(m=3,j\le1\), its coefficients cost at most \(C\rho^{-7}\). Multiplication by \(q_x\) gives the exact value and gradient at \(x\) and kills those at the other three sites. Repeat at \(x'\). The resulting duals have frequency degree at most four. Together with the pin duals they give (30) for \((U_r,V^{\rm sep})\), in the same fixed degree-seven space. This only uses charts local to the surviving sites; no global injectivity or distant-pair nondegeneracy of the sine map is asserted.

## 5. Quantitative covariance, regression moments, and the height-difference tail

Let \(\mathcal L=(U_r,V)\), with \(V=V_\delta\) or \(V^{\rm sep}\) in its respective domain. Taking unit data in §4 yields 12 duals. For every \(a\in\mathbb R^{12}\), their linear combination \(\phi_a\) satisfies

\[
 \mathcal L\phi_a=a,\qquad \|\phi_a\|_{\mathcal H}\le C\rho^{-7}|a|,
 \tag{33}
\]

where \(\mathcal H\) is the Cameron–Martin space of (1). Indeed, on the fixed finite frequency set the strictly positive \(a_n\) make the Fourier coefficient norm and \(\mathcal H\) norm equivalent, with constants depending only on \(L\). The covariance-representer identity and Cauchy–Schwarz give

\[
 |a|^4=|(a\cdot\mathcal L)\phi_a|^2
 \le\operatorname{Var}(a\cdot\mathcal Lf)\|\phi_a\|_{\mathcal H}^2.
\]

All coordinates have uniform variance upper bounds by their integral derivative representations or by being raw values/gradients. Hence

\[
 c\rho^{14}I\le\operatorname{Cov}(U_r,V)\le CI.         \tag{34}
\]

Under the actual Gaussian law \(Q_r\), write \(\mu=E_{Q_r}V\), \(S=\operatorname{Cov}_{Q_r}V\). The lower Schur-complement bound follows explicitly from

\[
 w^TSw=\min_z(z,w)^T\operatorname{Cov}(U_r,V)(z,w)
             \ge c\rho^{14}|w|^2.
\]

The upper covariance bound is inherited by conditioning. The mean uses the stronger pin-only bound (12), not the small lower bound (34); the cross-covariance is uniformly bounded. Consequently

\[
 c\rho^{14}I\le S\le CI,\qquad |\mu|\le C.             \tag{35}
\]

Both versions of \(V\) have dimension six. The Gaussian density therefore satisfies

\[
 p_{V,Q_r}(v)\le C\rho^{-42}\exp(-c|v-\mu|^2).
 \tag{36}
\]

For the near block evaluated at \(v=(0,0,0,0,y,t)\), with \(y\in I_r\) and \(r\le r_*\le1\), the compact target condition gives

\[
 p_{V_\delta,Q_r}(0,0,0,0,y,t)\le C\rho^{-42}e^{-c't^2}.
 \tag{37}
\]

The constants in this Gaussian tail do not worsen with \(\rho\). This uses the upper bound in (35), whereas the prefactor uses its lower bound.

We need conditional moments correlated with this same height-difference variable, rather than an independent bound for \(W_r\). Define \(\mathcal K=C_L(1+\|f\|_{C^3(X)})\ge1\), with the constant enlarged below. For every fixed \(p\ge1\),

\[
 E_{Q_r}[\mathcal K^p\mid V=v]\le C_p\rho^{-7p}(1+|v|)^p.
 \tag{38}
\]

Here is a direct global-norm proof. Expand \(f\) in its real sine/cosine series with independent standardized original Gaussian coefficients \(\xi_j\); the deterministic \(C^3\) norms of the Fourier summands without \(\xi_j\) have summable amplitudes by (1). Under conditioning on \(U_r=u_r\), each \(\xi_j\) has conditional variance at most one and mean bounded by

\[
 |E[\xi_j\mid U_r=u_r]|\le(u_r^T\operatorname{Cov}(U_r)^{-1}u_r)^{1/2}\le C.
\]

This is covariance Cauchy–Schwarz, or orthogonal projection in the Gaussian coefficient Hilbert space. Now let \(c_j=\operatorname{Cov}_{Q_r}(\xi_j,V)\). Positivity of the joint conditional covariance gives \(c_jS^{-1}c_j^T\le\operatorname{Var}_{Q_r}\xi_j\le1\). The further regression shift is at most

\[
 |c_jS^{-1}(v-\mu)|
 \le(c_jS^{-1}c_j^T)^{1/2}[(v-\mu)^TS^{-1}(v-\mu)]^{1/2}
 \le C\rho^{-7}(1+|v|).                                \tag{39}
\]

The residual variance remains at most one. Thus the \(L^p\) norm of each conditioned coefficient is at most \(C_p\rho^{-7}(1+|v|)\), uniformly in \(j\). Minkowski's inequality against the summable Fourier \(C^3\) amplitudes proves (38), initially for finite series and then by \(L^p(C^3)\) convergence. Residual coefficients need not be independent. The canonical Gaussian regression version defines these bounds for every \(v\). This is a square-root regression-energy bound; using a crude norm of \(S^{-1}\) would unnecessarily double the moment exponent.

In particular, combining (37) with (38) at \(p=8\),

\[
 p_{V_\delta,Q_r}(0,0,0,0,y,t)
 E_{Q_r}[\mathcal K^8\mid V_\delta=(0,0,0,0,y,t)]
 \le C\rho^{-98}(1+|t|)^8e^{-c't^2}.                   \tag{40}
\]

The right side is bounded and integrable as a function of the actual height-difference coordinate \(t=D\). No factorization of the conditional field, endpoint weight, witness Hessians or height difference has been used. In the separated block the analogous bound is \(C\rho^{-98}\) at both zero gradients and heights in \(I_r\).

## 6. Pathwise determinants and the applicable pair Kac–Rice identity

Under (2), the fundamental theorem of calculus along the pin segment gives

\[
 |H_Mu|+|H_Su|\le Cr\mathcal K.
\]

For any real symmetric \(2\times2\) matrix and unit vector \(e\), \(|\det H|\le |He|\|H\|_{\rm op}\). Hence, irrespective of type indicators,

\[
 W_r\le Cr^2\mathcal K^4.                              \tag{41}
\]

If both witness gradients vanish, applying the same averaging identity along the short witness segment gives

\[
 |H_xe|,|H_{x'}e|\le\tfrac12\delta\mathcal K,\qquad
 |\det H_x\det H_{x'}|\le C\delta^2\mathcal K^4.
 \tag{42}
\]

Indeed \(0=\int_0^\delta H_{x+se}e\,ds\) implies

\[
 |H_xe|\le\delta^{-1}\int_0^\delta\|H_{x+se}-H_x\|\,ds
          \le\tfrac12\delta\|f\|_{C^3},
\]

and reversal proves the bound at \(x'\). Thus on the near-pair conditioning,

\[
 W_r|\det H_x\det H_{x'}|\le Cr^2\delta^2\mathcal K^8.
 \tag{43}
\]

For separated pairs the corresponding bound is \(Cr^2\mathcal K^8\).

For completeness, the weighted Kac–Rice interface is applied under \(Q_r\), before the determinant tilt. On the open set of distinct witness sites avoiding pins, the four-dimensional process \(G(x,x')=(\nabla f(x),\nabla f(x'))\) is smooth; its covariance is positive definite by (34), or the positive Fourier distinct-site argument on a general compact exhaustion. Its normal Jacobian is precisely \(|\det H_x||\det H_{x'}|\). The height-augmented covariance is positive definite by the same construction. Gaussian regression is continuous on each compact subset avoiding site collisions, and conditional moments are finite there by (38).

Use first \(\min(W_r,m)\), the open height-window indicators, and, if desired, the open nonsingular index strata as the mark. The endpoint factors \(F_j\) are continuous, including at singular matrices where their determinant tends to zero. This is exactly the lower-semicontinuous marked setup of RC §3 and Appendix A; for arbitrary Borel location subsets use the measure identity on locations. The whole-field Gaussian regression and finite-measure extension are read as in E2, rather than claiming an arbitrary Borel field mark is lower semicontinuous. Exhaust compact subsets off the diagonal and away from pins; then increase \(m\). Nonnegative monotone convergence gives, as an extended nonnegative equality, the pair formula

\[
 E_{Q_r^W}(N(E))_2=
 \frac1{Z_r}\int_{E\times E\setminus\mathrm{diag}}\int_{I_r}\int_{I_r}
 p_{(\nabla f(x),\nabla f(x'),f(x),f(x')),Q_r}(0,0,y,y')
 E_{Q_r}[W_r|\det H_x\det H_{x'}|\mid0,0,y,y']
 \,dy'\,dy\,dx'\,dx.                                 \tag{44}
\]

The subsequent finite estimate proves integrability. Standard nondegenerate smooth Gaussian critical-point genericity on these compact exhaustions is part of the same Kac–Rice interface, so the count in (5) may equivalently include all indices via the nonsingular strata. The endpoint determinant weight appears once in (44); each witness determinant appears once as the Jacobian. There is no additional full-pin density, no additional type conditioning, and no unordered-pair factor \(1/2\) in (44). The \(1/2\) in (8) comes only from the integer inequality after counting ordered pairs.

## 7. Integration near and away from the witness diagonal

For \(x'=x+\delta e\), \(0<\delta<\rho/8\), the raw witness vector to (14) transformation has absolute determinant \(\delta^{-5}\): two gradient-difference factors \(\delta^{-1}\) and one height-difference factor \(\delta^{-3}\). Orthogonal frame changes have absolute determinant one. At zero gradients \(t=(y'-y)/\delta^3\). Therefore

\[
 p_{\rm raw,Q_r}(0,0,y,y')=\delta^{-5}
 p_{V_\delta,Q_r}(0,0,0,0,y,(y'-y)/\delta^3),
 \qquad dy'=\delta^3dt.                                \tag{45}
\]

For \(y\in I_r\), the transformed second-height interval \(J_{y,\delta}=(I_r-y)/\delta^3\) has length \(kr^3/\delta^3\). The function \(g(t)=(1+|t|)^8e^{-c't^2}\) is bounded and integrable, so uniformly in the interval's location,

\[
 \int_{J_{y,\delta}}g(t)\,dt\le C\min(1,kr^3/\delta^3).
 \tag{46}
\]

Apply (40), (43), (45), and polar area \(dx'=\delta\,d\delta\,de\) to (44). Drop the condition \(x'\in E\) only after applying the uniform bound at points originally in the pair domain; extend that nonnegative bound over all directions and radii. Using the full lower floor (4) gives

\[
\begin{split}
 E_{Q_r^W}T_{\rm near}(E)
 &\le C\rho^{-98}|E|r^3
    \int_0^{\rho/8}\delta\min(1,kr^3/\delta^3)\,d\delta\\
 &\le C\rho^{-98}|E|r^3\cdot\tfrac32(kr^3)^{2/3}
 \le Cr^5\rho^{-98}|E|.                                \tag{47}
\end{split}
\]

The \(\delta\) power in the first line is exactly \(1-5+3+2=1\), from area, raw density Jacobian, height substitution, and both small witness determinants respectively. The endpoint \(r^2\) in (43) cancels the full normalizer \(r^2\). The remaining first-height length is \(kr^3\). The elementary integral is evaluated by splitting at \(\delta_0=(kr^3)^{1/3}\):

\[
 \int_0^\infty\delta\min(1,a/\delta^3)\,d\delta
       =\delta_0^2/2+a/\delta_0=\tfrac32a^{2/3},\qquad a=kr^3.
 \tag{48}
\]

For the separated domain, use (31), the separated form of (40), and the \(Cr^2\mathcal K^8\) bound. Both height intervals have length \(kr^3\), so directly from (44),

\[
 E_{Q_r^W}T_{\rm sep}(E)\le Cr^6\rho^{-98}|E|^2.       \tag{49}
\]

All distances \(\delta\ge\rho/8\), including torus cut-locus configurations, are covered by the singleton dual construction. There is no polar-coordinate assumption in (49). Since \(r\le r_*\le1\) and \(|E|\le L^2\), this term is absorbed into (7) using \(r|E|\le r_*L^2\). Equations (8) follow from \(\mathbf1_{N\ge2}\le(N)_2/2\) and \(N\mathbf1_{N\ge2}\le(N)_2\). Substitution of \(\rho=r^\alpha\) proves (9). This proves the theorem conditional on the explicitly retained interfaces.

## 8. Exponent ledger and limits of the conclusion

| Step | Uniform cost or gain | Reason |
|---|---|---|
| Surviving close pair: two separators | \(\rho^{-4}\) | Each inverse \(\psi\) costs distance\(^{-2}\) |
| Derivatives for cubic Hermite data | At most \(\rho^{-3}\) additional | Third derivatives of inverse separator product; no \(r^{-1}\) or \(\delta^{-1}\) interpolation loss |
| Surviving singleton: three separators and one derivative | \(\rho^{-7}\) total | Separated-pair branch |
| Finite-Fourier right inverse | \(\rho^{-7}\) | Fixed spectral set; positive fixed Fourier weights |
| Joint and conditional covariance floor | \(\rho^{14}\) | Duality squares the norm cost |
| Six-dimensional conditional density prefactor | \(\rho^{-42}\) | Square root of a six-dimensional determinant |
| Conditional eighth \(C^3\)-norm moment | \(\rho^{-56}\) | Square-root regression energy, then power eight |
| Density times required moment | \(\rho^{-98}\) | \(42+56=98\) |
| Endpoint weight / full normalizer | \(r^2/r^2\) | Two actual endpoint determinants and full \(Z_r\) |
| Near diagonal after all \(\delta\) factors | \(\delta^1\) | \(1-5+3+2=1\) |
| One height window and radial cutoff integral | \(r^3r^2=r^5\) | (46)–(48), with compact positive \(k\) |

Multiplying (7) by the upper bound in (4) also gives the unnormalized weighted count \(E_{Q_r}[W_r(N(E))_2]\le Cr^7\rho^{-98}|E|\). Neither bound includes a pin-density factor; this is a conditional-pair law, not an intensity integrated over pin configurations.

The proof gives a quantitative error for two witnesses both outside a moving ball whose radius is still much larger than \(r\). It does not estimate a pair with either witness inside that ball. In particular, mixed pairs with one inner and one outer witness, and outer presence conditional on an inner witness, are not controlled. It does not convert witness counts into persistence bars or prove an all-region collision theorem. It establishes no uniformity as \(k\downarrow0\), as marks or \(L\) vary, or in dimension above two. It supplies no all-height count or first-moment asymptotic for moving \(\rho\). A use in shrinking-witness/persistence identification must retain these missing interfaces explicitly.

The companion finite controls check algebraic constructions, Jacobian and exponent ledgers, and deliberately broken variants. They cannot certify the continuum interpolation estimates, Gaussian conditioning, or Kac–Rice hypotheses. Those are mathematical review obligations of this proof, not conclusions inferred from a program's exit code.
