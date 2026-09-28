# D5: an all-height punctured endpoint-disk bound

**Object:** OA-D5-PUNCTURED-PIN-20260928-v1  
**Author:** OpenAI / ChatGPT, foreground continuation of Math-#103  
**Disposition:** AUTHOR-SIDE ANALYTIC CANDIDATE — NONAUTHOR REVIEW REQUIRED  
**Scientific effect:** NONE. No accepted status, prize, graph node, or closure flag is changed.  
**Publication:** local delivery only; this session did not push, comment, open a PR, or merge.

This note is an additive successor, not a replacement for any frozen source. It supplies an author-side proof of the Gaussian density/moment interface left conditional in Math-#103 and combines two deterministic bounds to treat the longitudinal axis as well as the transverse cone. The main statement concerns the punctured disk about M; Section 10.1 gives an explicit reflected corollary for S under the original weighted law. Neither is a global D5/RN or elder-pairing theorem.

## 1. Source identity and what is new

The existing candidate is Math-#103 at `be08396071d43a14fa4f3d6d1cb8bdd4cccaf6d2`, directory `reviews/d5_short_edge_20260928/`. Its `NOTE.md` is 10,710 bytes, SHA-256 `81c48f076c06d0a8cdd12d1fd2810b5f706da003b17bd470acc95565b3c86523`, Git blob `e5fde88b41c0f80e4ea1e0c7102af597bff03f74`. The original four files are not edited by this delivery.

Source background is `d6g8k5htny-coder/Math-` at `78d36001cfdd7dcb636ba927e973a2fd731527c2`:

- `frontiers/rn_annulus_bridge_20260925/PROOF.md`, blob `6f317515b3d417661f86e2fed09bc7d950899c2b`: exact field, six pins, original endpoint normalizer, and the full-field Gaussian regression method.
- `reviews/pin_micro_covariance_20260926/NOTE.md`, blob `36cc6cfcc0ab776bc22e5f1f480d4d264b1294a6`: prior anisotropic covariance proposal.
- `reviews/d5_pin_microdisk_20260927/NOTE.md`, blob `ac09361caac76d07f878c51ebddf6d2bea3f565f`: finite cubic identities and recorded nested-axis obstruction.
- `imports/transverse_contact_library_20260927/GEOMETRY_AND_CUBIC_INDEX.md`, blob `58fbeb8f5180104361938253203b9dfb576af2d9`: critical-segment Taylor/simplex argument.

The new components are the uniform endpoint-vanishing remainders in Section 4, the full-disk compactified gradient block, and the angle-free short-edge determinant estimate used on the axial strip. The analytic arguments are written out instead of treating older author-side claims as accepted premises. No general novelty or priority claim is made.

## 2. Exact statement

Fix a torus side length T>0 and the centered variance-one Gaussian field F on the square torus with covariance

\[
 K_T(h)=\frac{\sum_{n\in\mathbb Z^2}\exp(-|h+Tn|^2/2)}
 {\sum_{n\in\mathbb Z^2}\exp(-|Tn|^2/2)}.
\]

Fix a compact interval of b and constants 0<k_-<=k<=k_+<infinity. Frames range over O(2). Use physical coordinates in the frame with

\[
 M=(-r/2,0),\quad S=(r/2,0),\quad
 f(M)=b,\ f(S)=b-kr^3,\quad \nabla f(M)=\nabla f(S)=0.       \tag{P1}
\]

Let Q_r be the continuous Gaussian regression law of these exactly six observations. It is not an adjacency or elder-rule law. For a symmetric 2x2 matrix define F_j(H)=|det H| on nonsingular matrices of negative index j and zero otherwise. Set

\[
 W_r=F_2(H_M)F_1(H_S),\quad Z_r=\mathbb E_{Q_r}W_r,
 \qquad dQ_r^W=(W_r/Z_r)dQ_r.
\]

Write N_j(B) for the number of index-j critical points at **all heights** in B. The tilted law Q_r^W is not Gaussian.

**Candidate theorem.** For sufficiently small r>0, there is C finite, uniform in b,k,frame,j and Borel E contained in

\[
 D=\{(p,q):0<p^2+q^2\le 1/16\},
\]

such that

\[
 \boxed{\mathbb E_{Q_r^W}N_j(M+rE)\le Cr^3\,|E|.}        \tag{P2}
\]

Here |E| is two-dimensional Lebesgue area. Equivalently, the physical-area intensity is bounded by Cr at X=M+r(p,q), for every nonzero point of D. In particular, for fixed kappa, the subdisk p^2+q^2<=kappa^2 r^2 has expected count O(r^5), once kappa r<=1/4.

The conditioned pin M is excluded: including it would add a deterministic atom and make (P2) false. S is outside this disk. Constants and the small-radius cutoff depend on T and the compact mark ranges; none is evaluated numerically. This is not a uniform-in-T or k-down-to-zero claim. The S-centered version is established explicitly in Section 10.1 rather than assumed by symmetry. The theorem does not cover the collar to the reviewed annulus, intermediate scales, multiple-witness collisions, dimensions above two, or elder selection.

## 3. Uniform endpoint regression

Translate the longitudinal coordinate so M is x=0 and S is x=r. Put g(x)=f(M+(x,0)) and h(x)=f_z(M+(x,0)). The following unconditional linear observation vector is invertibly equivalent to the six raw observations for each r>0:

\[
 E_r=\left(g(0),g'(0),h(0),\frac{g'(r)-g'(0)}r,
 \frac{12}{r^3}\left[g(r)-g(0)-\frac r2(g'(r)+g'(0))\right],
 \frac{h(r)-h(0)}r\right).                              \tag{P3}
\]

Its exact target under (P1) is e=(b,0,0,0,-12k,0), independent of r. Its contact limit is

\[
 E_0=(f,f_x,f_z,f_{xx},-f_{xxx},f_{xz})(M).
\]

Taylor's integral formula gives E_r-E_0=O_{L^s}(r) for each finite s, uniformly in frames and locations.

Here and below these moment statements follow directly from the exact field, not a finite Fourier truncation. Poisson summation gives strictly positive Fourier variances proportional to exp(-|2 pi n/T|^2/2) at every n in Z^2. The sum of their square roots times (1+|n|)^m is finite for every m. A real sine/cosine expansion and Minkowski's inequality therefore give finite moments of every fixed C^m norm. Orthogonal changes of coordinates have bounded derivative coefficients, uniformly over O(2).

A zero-variance linear combination of distinct one-site derivative monomials would give a polynomial symbol vanishing on the entire rotated integer lattice. After undoing the rotation, fix one integer coordinate and use the one-variable polynomial identity theorem, then repeat for the other coordinate. The polynomial is zero identically, so the coefficients vanish. Thus the jet covariance is positive definite; its continuous dependence on the compact frame set makes the lower bound uniform.

Consequently Cov(E_r) and its inverse are uniformly bounded for small r. Its covariance with the field has bounded derivatives of every fixed order. The explicit Gaussian coupling

\[
 f_{Q_r}=f+\operatorname{Cov}(f,E_r)\operatorname{Cov}(E_r)^{-1}(e-E_r)
\]

shows that, for every fixed m,s, the C^m norm under Q_r has uniformly bounded s-th moment. Norms may be taken on the whole torus and hence cover the full triangle M,S,X and every Taylor segment used below.

At M define the four actual jets

\[
 J=(A_4,T_3,S_0,C_3)=(f_{xxxx},f_{xxz},f_{zz},f_{xzz})(M).
\]

These and the six contact monomials are distinct. The covariance of J after conditioning E_r therefore has uniform positive lower and finite upper eigenvalue bounds, and its conditional mean is bounded. This is a Schur-complement statement for the exact field.

## 4. Relative remainders: vanishing at the pin is retained

Let K_m be a fixed multiple of 1+||f||_{C^m} on the full Taylor domain. All K_m moments under Q_r are bounded by Section 3. The exact longitudinal cubic pin interpolant is

\[
 H(x)=b+k(2x^3-3rx^2).
\]

For |p|<=1/4,

\[
 g'(rp)=6kr^2p(p-1)+\frac{r^3A_4}{12}p(p-1)(2p-1)
              +O(r^4|p|K_5).                           \tag{P4}
\]

**Derivation of the relative error.** Set u(x)=g(x)-H(x)-(A_4/24)x^2(x-r)^2. Then u,u' vanish at 0,r, and u''''(0)=0. On [-r/4,r], |u''''(x)|<=C r K_5. Taylor expansion of u(r)=u'(r)=0 gives a two-by-two linear system implying u''(0)=O(r^3K_5) and u'''(0)=O(r^2K_5). Expanding u'(rp) now gives O(r^4(|p|+p^2+|p|^3)K_5), which proves (P4). An absolute O(r^4) error would not suffice after division by the vanishing spatial scale.

Likewise h(0)=h(r)=0 and h''(0)=T_3 imply

\[
 h(rp)=\frac{r^2}2p(p-1)T_3+O(r^3|p|K_4),\qquad
 h'(rp)=r(p-1/2)T_3+O(r^2K_4).                         \tag{P5}
\]

Taylor expansion in z=rq gives

\[
\begin{split}
 f_x(X)/r^2={}&6kp(p-1)+\frac{rA_4}{12}p(p-1)(2p-1)
                  +(p-1/2)qT_3+q^2 C_3/2+\epsilon_1,\\
 f_z(X)/r={}&\frac r2p(p-1)T_3+qS_0+\epsilon_2.
\end{split}                                                        \tag{P6}
\]

With constants uniform on |p|,|q|<=1/4, the pathwise errors can be bounded by

\[
\begin{split}
 |\epsilon_1|&\le C K_5\{r^2|p|+r|q|+r|p|q^2+r|q|^3\},\\
 |\epsilon_2|&\le C K_4\{r^2|p|+r|p q|+r q^2\}.
\end{split}                                                        \tag{P7}
\]

For example f_zz(rp,0)=S_0+O(r|p|K_3); the terms rpq C_3 and rq^2 f_zzz(M)/2 are included in epsilon_2. No midpoint coefficient is mislabeled as S_0: all four J entries are actual endpoint jets.

## 5. A stable gradient frame on the entire punctured disk

Set

\[
 \Delta=(q^2+r^2p^2)^{1/2}>0,\quad
 \alpha=rp/\Delta,\quad\beta=q/\Delta,\quad
 Y=\left(\frac{f_x(X)}{r^2\Delta},\frac{f_z(X)}{r\Delta}\right).
\]

Both alpha and beta may be signed, and alpha^2+beta^2=1. From (P6)-(P7),

\[
 Y=\left(6kp(p-1)/\Delta,0\right)+B J+R,\qquad
 \|R\|_{L^s(Q_r)}\le C_s r,                            \tag{P8}
\]

where

\[
 B=\begin{pmatrix}
 a(p)\alpha&c(p)\beta&0&(q/2)\beta\\
 0&b(p)\alpha&\beta&0
 \end{pmatrix},
\quad a=(p-1)(2p-1)/12,\ b=(p-1)/2,\ c=p-1/2.
\]

The error is uniform even when p or q is arbitrarily small: Delta>=|q| and Delta>=r|p| imply r^2|p|/Delta<=r and r|q|/Delta<=r. The other terms in (P7), divided by Delta, have the same bound up to fixed chart constants.

The three minors from the first three columns are ab alpha^2, a alpha beta, and c beta^2. For |p|<=1/4,

\[
 |a|\ge1/32,\quad |b|\ge3/8,\quad |c|\ge1/4.
\]

Hence Cauchy-Binet gives

\[
 \det(BB^T)\ge (ab)^2\alpha^4+c^2\beta^4
 \ge \tfrac12\min\{(ab)^2,c^2\}\ge 9/131072.             \tag{P9}
\]

The trace is bounded, so both singular values have a uniform positive lower bound. The fourth column can only increase BB^T. By Section 3, the covariance of BJ under Q_r is uniformly coercive. For every unit row v, use the L^2 triangle inequality on centered variables in (P8): the standard deviation of v dot Y is bounded below by that of v dot BJ minus ||v dot (R-E R)||_2. Reducing r_* absorbs this O(r) error. Thus

\[
 c_0 I\le\Sigma=\operatorname{Cov}_{Q_r}(Y)\le C_0 I.    \tag{P10}
\]

In particular q=0,p!=0 is covered by the A_4,T_3 minor. This is an **eight-observation all-height problem** (six endpoint observations plus two witness gradients), not a repair of a nine-observation frame with an additional witness value pin.

## 6. Density and full conditional sixth moment

Put chi=|p|/Delta. The mean of Y is d+O(1), where d=(6kp(p-1)/Delta,0). Since |p-1|>=3/4,

\[
 |d|\ge (9k_-/2)\chi,\qquad |d|\le C\chi.
\]

Use |d+v|^2>=|d|^2/2-|v|^2 and (P10) in the exact two-dimensional Gaussian density. The raw gradient Jacobian is r^3 Delta^2. We obtain

\[
 p_{\nabla f(X)\mid\text{pins}}(0)
 \le C r^{-3}\Delta^{-2}\exp(-c\chi^2).                \tag{P11}
\]

Let K dominate both the Hessian supremum K_2 and its Lipschitz constant L on the entire triangle; a fixed multiple of 1+||f||_{C^3} on the torus does so. We claim

\[
 \mathbb E_{Q_r}[K^6\mid\nabla f(X)=0]
 \le C(1+\chi^6).                                     \tag{P12}
\]

Here is the required full-field argument. Write m_f=E_{Q_r}f, m_Y=E_{Q_r}Y and C(x)=Cov_{Q_r}(f(x),Y). Each derivative of C through order three is uniformly bounded by Cauchy-Schwarz, Section 3 and the upper variance bound in (P10). Consequently ||C Sigma^{-1}||_{C^3} is bounded. The Gaussian residual

\[
 R_f=f-m_f-C\Sigma^{-1}(Y-m_Y)
\]

is independent of Y. The triangle inequality, the uniform centered sixth moment of Y, and the endpoint-only C^3 sixth moment show that E||R_f||_{C^3}^6 is bounded uniformly. Conditioning Y=0 replaces f by

\[
 m_f-C\Sigma^{-1}m_Y+R_f.
\]

Its deterministic mean has C^3 norm at most C(1+chi), which proves (P12). Independence of Hessians is nowhere asserted. The bound is under the additional witness-gradient constraint, not just the endpoint law. It covers the long segment joining M and S as well as the tiny neighborhood of X.

## 7. The original normalizer, once only

We need the endpoint-only bound Z_r>=c_Z r^2. By (P4)-(P5) and bounded endpoint-law moments,

\[
 f_{xx}(M)/r=-6k+O_{L^s}(r),\quad
 \det H_M/r=-6kS_0+O_{L^s}(r),\quad
 \det H_S/r=6kS_0+O_{L^s}(r).                           \tag{P13}
\]

For the S determinant use f_zz(S)=S_0+O_{L^s}(r), f_xx(S)/r=6k+O_{L^s}(r), and f_xz at both endpoints O_{L^s}(r). Products of errors are controlled by Holder and the already established higher moments.

S_0 under Q_r has bounded mean and variance bounded above and below by positive constants. Thus Q_r(-2<=S_0<=-1)>=p_0>0 uniformly. Remove the events where any error in (P13), or the f_xx(M)/r error, exceeds k_-. Their union has probability O(r^s). On the remaining event M is negative definite, S is indefinite, and both absolute determinants are at least 5k_- r. For small r the event has probability at least p_0/2. Therefore

\[
 Z_r\ge c_Z r^2>0.                                    \tag{P14}
\]

This is the original endpoint normalizer; it is never replaced by its value after conditioning at X.

## 8. Two pathwise determinant estimates

Let A=M,B=S,C=X be three distinct exact critical points. Write |B-A|=r, |C-A|=d<=r/4 and ell=|B-C|<=5r/4. L is a Hessian Lipschitz bound on the convex triangle, and K_2 bounds the Hessian operator norm there.

For any two critical points U,V, the fundamental theorem of calculus along their segment gives, for e=(V-U)/|V-U|,

\[
 \|H_U e\|\le L|V-U|/2.                               \tag{P15}
\]

### 8.1 Angle-sensitive bound

For a noncollinear triangle put sigma=|sin angle(B-A,C-A)|>0. Applying (P15) in the two directions at A gives

\[
 |\det H_A|\le L^2rd/(4\sigma),\qquad
 \|H_A\|\le L(r+d)/(2\sigma).
\]

The operator norm inequality follows by Cramer's rule: the coefficients of any unit vector in the two unit directions have modulus at most 1/sigma. Transport to B gives ||H_B||<=2Lr/sigma, hence |det H_B|<=4L^2r^2/sigma^2. The sine at C is r sigma/ell by the two triangle-area formulas. Another application of (P15) gives

\[
 |\det H_C|\le L^2d\ell^2/(4r\sigma)\le L^2rd/(2\sigma).
\]

Multiplication implies

\[
 |\det H_A\det H_B\det H_C|\le L^6r^4d^2/\sigma^4.
\]

At X=M+r(p,q), q!=0, this is

\[
 |\det H_M\det H_S\det H_X|
 \le L^6r^6 q^2(1+(p/q)^2)^3.                          \tag{P16}
\]

The intentionally loose constant one in the preceding triangle bound is valid; the displayed individual estimates actually multiply to one-half. Unlike a fixed-angle estimate, (P16) records the cost of a small angle explicitly.

### 8.2 Angle-free bound, including the axis

At A and C, use the short segment AC for one Hessian column and K_2 for its perpendicular column. At B use the length-r segment BA. In an orthonormal basis the determinant is bounded by the product of these column norms. Thus

\[
 |\det H_A|,|\det H_C|\le LdK_2/2,\quad
 |\det H_B|\le LrK_2/2,
\]

and

\[
 |\det H_M\det H_S\det H_X|
 \le \tfrac18 L^3K_2^3 r d^2
 \le C K^6 r^3(p^2+q^2).                              \tag{P17}
\]

This holds on collinear triangles as well. Retaining the two factors of d is essential: the coarser bound K_2^6 would not cancel the divergence as X tends to M on the axis.

## 9. Weighted Kac-Rice, with the hypotheses checked

For fixed r>0, work first on a compact region excluding M,S. The raw endpoint observations and grad f(X), at three distinct sites, are independent as derivative distributions: Fourier uniqueness makes a zero-variance combination the zero distribution; test functions localized near each site then force all coefficients to vanish. Thus the conditional gradient covariance is positive definite. The field has smooth paths and its continuous conditional laws are the explicit Gaussian regressions.

Use the Gaussian expected-count and weighted formulas in Armentano--Azais--Leon, arXiv:2304.07424v3, Theorems 2.2 and 7.1 and Remark 8. The zero-counted field is grad f under Q_r. An auxiliary jointly Gaussian field records H_M,H_S,H_X. The nonnegative mark is W_r times the indicator that H_X is nonsingular of index j. Endpoint filtered determinants are continuous through singular matrices, and the nonsingular index set is open, so the mark is lower semicontinuous. Conditional-law continuity follows from the same Gaussian regression. Unbounded polynomial marks are handled by truncation and monotone convergence.

This gives the intensity per unit **physical area**,

\[
 \rho_j^W(X)=Z_r^{-1}p_{\nabla f(X)\mid\text{pins}}(0)
 \mathbb E_{Q_r}[W_r F_j(H_X)\mid\nabla f(X)=0].         \tag{P18}
\]

The extra witness determinant is in F_j; it is not counted twice. Dropping endpoint and witness types gives upper bounds by (P16) and (P17). There is no witness value pin, no height-window integration, and no assumption that Q_r^W is Gaussian.

## 10. The actual crossover closes the punctured disk estimate

### Region I: |q|>=r|p|

Here q!=0 because the pin is excluded. Set t=p/q. Then r^2t^2<=1 and

\[
 t^2/2\le\chi^2=t^2/(1+r^2t^2)\le t^2,\qquad q^2/\Delta^2\le1.
\]

Combine (P11), (P12), (P14), (P16), (P18):

\[
 \rho_j^W(X)\le Cr(1+t^2)^3(1+t^6)e^{-ct^2/2}\le C'r.  \tag{P19}
\]

Every fixed polynomial is bounded after multiplication by this Gaussian factor. This region includes the entire old transverse cone and the nonaxial parts of arbitrarily small nested microdisks.

### Region II: |q|<r|p|

Here p!=0 and, taking r<=1,

\[
 \frac1{2r^2}\le\chi^2\le\frac1{r^2},\qquad
 \frac{p^2+q^2}{\Delta^2}\le\frac2{r^2}.
\]

Use the angle-free estimate (P17) instead. The exact powers give

\[
\begin{split}
 \rho_j^W(X)
 &\le Cr^{-2}\frac{p^2+q^2}{\Delta^2}(1+\chi^6)e^{-c\chi^2}\\
 &\le Cr^{-10}e^{-c/(2r^2)}\le C'r^2\le C'r.           \tag{P20}
\end{split}
\]

The penultimate inequality follows from the sixth positive term of the exponential series: e^{-c/(2r^2)}<=6!(2/c)^6 r^{12}. The power ledger before that absorption is -2 from Z, -3 from the raw gradient Jacobian, +3 from (P17), -2 from the spatial ratio, and -6 from the conditional moment. The longitudinal axis q=0 is included; no division by q is made in this region.

The two regions cover D. Their estimates are uniform down to arbitrary nonzero witness distance. Apply (P18) on increasing compact punctures and use monotone convergence. Since dX=r^2 dp dq, (P19)-(P20) prove (P2). The area of the nested scaled disk is at most pi kappa^2 r^2, giving O(r^5). This completes the author-side proof.

### 10.1 Explicit reflection to the other endpoint

For the disk about S, use the reflected local field

\[
 \widetilde f(x,z)=f(S-x e_1+z e_2).
\]

Its local endpoints are 0 and r, with target marks

\[
 \widetilde b=b-kr^3,\qquad \widetilde k=-k,
 \qquad \widetilde f(r,0)=\widetilde b-\widetilde k r^3=b.
\]

For r<=1, the new birth values remain in a fixed compact interval, and |tilde k| lies in [k_-,k_+]. Sections 3--6 apply verbatim: the endpoint targets need boundedness, and the mean penalty uses only |k|>=k_-, not its sign. Frames remain in O(2). Do **not** apply the Section 7 typing event to a saddle as though it were a maximum. Instead retain the original normalizer Z_r, already bounded below in (P14). Under reflection the original mark becomes F_1(H_0)F_2(H_r); it is the same random variable with its factors relabeled. Orthogonal conjugation preserves determinants and negative indices.

The deterministic estimates are index-free. The weighted Kac--Rice argument uses the relabeled original mark, and the same intensity bounds follow on the S-centered punctured disk. Thus (P2) holds with M replaced by S. The two physical radius-r/4 disks are disjoint. Summing their counts gives an O(r^3) bound for their union, and O(r^5) for the union of the fixed-kappa nested radius-kappa r^2 disks. No region between those disks or between them and the reviewed annulus is included.

## 11. What this candidate does and does not settle

The note provides analytic arguments, rather than leaving as imported hypotheses, for the uniform exact-field covariance, the full additional-conditioning sixth moment, the original normalizer, the two determinant estimates, and their intensity integration on the M-centered punctured disk, with the original weighted law explicitly reflected to the S-centered disk. It therefore goes beyond #103's conditional transverse-cone implication.

It does not upgrade any repository verdict. It has not had a nonauthor review or a proof-assistant check. In particular, it does not close the region between this r/4 endpoint disk and the reviewed scaled annulus, intermediate physical distances, a shrinking multiple-witness collision law, or the quantitative parent selection chain. No finite numerical constant or cutoff is supplied. Finiteness of unconditioned critical-point moments is not being substituted for a uniform estimate in a degenerating conditional family.

The distinction between six-plus-two and six-plus-three observations is substantive. An additional witness height would change the covariance block and Jacobian; this proof cannot be reused by silently inserting a value pin.

## 12. Finite controls and source-bound review request

The new standard-library controls independently differentiate exact pinned quartic fixtures, check the three principal minors and the rational Gram floor, verify the invertible six-pin target, retain the endpoint factor in a quintic remainder fixture, test crossover inequalities at tiny rational distances, and check the power ledger. They allow q=0 away from the pin. They do **not** verify a continuum quantifier, an infinite Fourier tail, a Gaussian supremum moment, or Kac-Rice applicability.

Run `python -B -S run_pin_validation.py --output NEW_DIRECTORY` from this directory. The runner executes the new test suite in normal and optimized mode and checks six deliberate source mutations in fresh temporary copies. `PIN_RESULTS.json` is its deterministic finite-results summary. The historical #103 controls are replayed separately in the delivery evidence, without modifying their source files.

A nonauthor reviewer should assess the following exact interfaces, independently of the finite control outcome: relative remainder (P4)-(P7); conditional jet Schur floor and L2 perturbation (P8)-(P10); whole-triangle C3 regression (P12); original normalizer (P14); angle-sensitive versus angle-free determinants (P16)-(P17); weighted Kac-Rice at the fixed zero level; and the crossover powers and puncture exhaustion. A failure in any interface prevents consumption of (P2) as a closed dependency. Review lineage and scientific acceptance remain separate from publication.

## 13. Reconnaissance memo

Primary framework read: Diego Armentano, Jean-Marc Azais, Jose Rafael Leon, *On a general Kac-Rice formula for the measure of a level set*, arXiv:2304.07424v3 (5 December 2023), https://arxiv.org/html/2304.07424v3 . Theorems 2.2/7.1 and Remark 8 provide the Gaussian weighted-count framework; this note checks the application conditions and supplies its own estimates.

Consensus discovery and abstract/bibliographic check: Louis Gass and Michele Stecconi, *The number of critical points of a Gaussian field: finiteness of moments*, arXiv:2305.17586, https://arxiv.org/abs/2305.17586 . Only its abstract and bibliographic record were read in this pass. It is relevant interpolation/moment context, not a source for a claimed uniform six-pin bound. No theorem from that paper is imported here.

The elementary Taylor and Gaussian-regression methods already occur in the local sources. The potential contribution is this explicit, source-bound endpoint-disk application, not ownership of those general methods. Novelty has not been comprehensively audited.
