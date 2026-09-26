# D5 nested microdisk — divided-difference frame and soft factor

**Object:** OA-D5-MICRODISK-20260926-v1.
**Answers:** [Math #58](https://github.com/d6g8k5htny-coder/Math-/issues/58).
**Disposition:** author-side derivation. Scientific effect: **NONE**.
**Not claimed:** all-height $O(r^3)$ pin-neighborhood expected count, elder pairing, global RN, $\eta\to0$.

Parent geometry only: six endpoint pins $M=(-r/2,0)$, $S=(r/2,0)$, $f(M)=b$, $f(S)=b-kr^3$, $\nabla f(M)=\nabla f(S)=0$. Nested chart $X=M+r^2(P,Q)$ with $|(P,Q)|\le\kappa$. This sits inside the PR53 disk $|s|\le1/4$ and does not meet the reviewed annulus $\rho\ge A>1$.

## 1. Two regimes (do not mix)

**All-height.** $S:=f_{zz}(M)$ is $O(1)$. Then $f_z(X)=r^2 S Q+O(r^3)$ and $f_x(X)=O(r^3)$. The raw gradient map is mixed order $(r^3,r^2)$, Jacobian $r^5$. Physical Hessians have $\det H_M=-6kSr+O(r^2)$ and likewise at $S$ and $X$, so the unconstrained triple product is $O(r^3)$, not $O(r^6)$. This is the setting #58 asked for first.

**Contact cubic.** The field is the exact six-pin cubic of NOTE §B, equivalently $f(x,z)=b+r^3\mathcal{P}(x/r,z/r)$ with $\mathcal{P}$ from (B1). Then $f_{zz}(M)=r(A-c/2)=O(r)$ and both gradient components are $O(r^3)$. The rest of this note is exact on that cubic. It is the leading contact shape, not a general $C^6$ all-height theorem.

## 2. Exact nested expansion (contact cubic)

On $X=M+r^2(P,Q)$,

$$\begin{aligned}
f_x(X)&=r^3\Bigl(-6kP-\frac{qQ}{2}\Bigr)+r^4\Bigl(6kP^2+PqQ+\frac{cQ^2}{2}\Bigr),\\
f_z(X)&=r^3\Bigl(\bigl(A-\tfrac{c}{2}\bigr)Q-\frac{qP}{2}\Bigr)+r^4\Bigl(\frac{qP^2}{2}+cPQ+\frac{dQ^2}{2}\Bigr).
\end{aligned}$$

These identities are polynomial, not asymptotic: higher powers of $r$ are absent on a cubic. Write $\Phi=(f_x,f_z)/r^3$. Then

$$D\Phi/D(P,Q)=H_M^{\mathrm{scaled}}=\begin{pmatrix}-6k&-q/2\\-q/2&A-c/2\end{pmatrix}$$

at $r=0$, and the physical Hessians are $r$ times the scaled matrices of NOTE (B3):

$$H_M=r\begin{pmatrix}-6k&-q/2\\-q/2&A-c/2\end{pmatrix},\quad
H_S=r\begin{pmatrix}6k&q/2\\q/2&A+c/2\end{pmatrix}.$$

Unconstrained, $\det H_M=r^2\det B_M$ and $\det H_S=r^2\det B_S$, so the triple product is $O(r^6)$ before witness conditioning. The divided-difference frame as $X\to M$ is $H_M$ itself. It is nondegenerate iff $\det B_M\neq0$.

## 3. Soft factor after $\Phi=0$

Leading witness $\Phi=0$ and $Q\neq0$ forces the unique solve

$$q=-\frac{12kP}{Q},\qquad A-\frac{c}{2}=-\frac{6kP^2}{Q^2}.$$

Substitute into $H_M$:

$$\det H_M=0\qquad\text{identically.}$$

This is the extra soft transverse factor requested in #58: after the witness-gradient equations, $M$ is degenerate at leading order. The constrained companions are

$$\det H_S=6kr^2\frac{-12kP^2+cQ^2}{Q^2},$$

and $\det H_X$ starts at order $r^3$,

$$\det H_X=r^3\Bigl(\frac{144k^2P^3}{Q^2}-18Pck-6Qdk\Bigr)+O(r^4).$$

The unconstrained PR53 inner-disk count that used a raw $O(r^5)$ triple product is therefore **not** the constrained microdisk law. Leading constrained $\det H_M$ vanishes; repulsion lives in the $r^4$ (quartic / Hermite remainder) row, which this cubic does not contain.

## 4. Rate boundary — no $O(r^3)$ lemma

Jacobian $\partial(f_x,f_z)/\partial(P,Q)=r^4\det H_X$. Off $\{Q=0\}$ the leading $\Phi$-map from jets $(A,q)$ is invertible. The axis $Q=0$ makes that $2\times2$ minor vanish.

Crude density $\le C/(r^6 Q^2)$ times physical area $r^4\,dP\,dQ$ and $Z_r^{-1}=O(r^{-2})$ produces a count piece

$$r^2\int_{|Q|\le\kappa}\frac{dQ}{Q^2},$$

which diverges at $Q=0$. Cutting $|Q|\ge\delta$ gives $O(r^2)$, the same shape as the PR53 punctured-disk $O(r^2\log(1/r))$ ledger, not $O(r^3)$.

All-height (free $S=O(1)$) is no better: mixed Jacobian $r^5$ and unconstrained product $O(r^3)$ still leave an axis / $\{S=0\}$ obstruction, and do not yield a uniform $O(r^3)$ expected count on the microdisk.

**Conclusion for #58.** The nested frame is exact. The inner-disk paragraph of PR53 must be amended: constrained $\det H_M$ vanishes at leading contact order. An all-height $O(r^3)$ pin-neighborhood lemma is **not** supported. The remaining blow-up is the microdisk axis $Q=0$ together with the first pin-preserving quartic (C6 §4 notes that $(x^2-r^2/4)^2$ already contributes $O(r)$ to $f_x/r^2$).

## 5. Stitch

$|s|=r|(P,Q)|=O(r)$ on this chart, so the microdisk is disjoint from the reviewed annulus $\rho\ge A>1$ and from the PR53 outer cone $|q|\ge\kappa r$ inside $|s|\le1/4$. Gluing those three pieces is a later argument. This note supplies only the inner frame and the obstruction.

## 6. Verification

Exact on the six-pin cubic in $\mathbb{Q}[r,k,A,q,c,d,P,Q]$ (this session):

pins at $M,S$; $f_x,f_z$ expansions of §2; $H_M,H_S=r B_\bullet$; unconstrained $\det H_M=r^2\det B_M$; $\Phi=0$ solve of §3; constrained $\det H_M=0$; $\partial(f_x,f_z)/\partial(P,Q)=r^4\det H_X$.
