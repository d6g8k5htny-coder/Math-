# Microdisk quartic follow-through

**Object:** OA-D5-MICRODISK-QUARTIC-20260926-v1.
**Parent:** `NOTE.md` in this directory (PR82).
**Scientific effect:** NONE.

The contact cubic makes $\det H_M=0$ after $\Phi=0$. The first pin-preserving quartic restores a leading factor.

## 1. Pin-preserving monomial

Let $\lambda\in\mathbb{R}$ and

$$f=b+r^3\mathcal{P}(x/r,z/r)+\lambda\bigl(x^2-r^2/4\bigr)^2,$$

with $\mathcal{P}$ the six-pin cubic of NOTE §B. Value and gradient still vanish at $M,S$ except the exact height gap $f(S)=b-kr^3$. C6 §4 already recorded the axial row $f_x(ru,0)/r^2=4\lambda r\,u(u^2-1/4)$.

On the nested chart $X=M+r^2(P,Q)$,

$$f_x(X)=r^3\Bigl(-6kP-\tfrac{qQ}{2}\Bigr)+r^4\Bigl(6kP^2+PqQ+\tfrac{cQ^2}{2}+2\lambda P\Bigr)+O(r^5),$$

and $f_z$ is unchanged through $r^4$ (the monomial is independent of $z$). The physical Hessian at $M$ becomes

$$H_M=\begin{pmatrix}-6kr+2\lambda r^2&-qr/2\\-qr/2&r(A-c/2)\end{pmatrix}.$$

## 2. Constrained determinant

Leading $\Phi=0$ and $Q\neq0$ still force $q=-12kP/Q$ and $A-c/2=-6kP^2/Q^2$. Substitute:

$$\det H_M=-\frac{12\lambda k P^2 r^3}{Q^2}.$$

Identity in $\mathbb{Q}[r,k,c,d,P,Q,\lambda]$ (this session). The cubic soft factor is therefore lifted by one power of $r$ and by the quartic coupling $\lambda$. For $\lambda\neq0$ and $P\neq0$ the endpoint $M$ is nondegenerate at order $r^3$.

## 3. What this does not prove

- $\lambda$ is a jet of the Gaussian field, not a constant. Conditional law of $\lambda$ after $\Phi=0$ is not computed here.
- Axis $Q=0$ remains: the displayed formula diverges, which only restates that the leading $\Phi$-map drops rank on the pin-pair line.
- No expected-count rate. In particular this does **not** upgrade PR82 to an $O(r^3)$ pin lemma.
- C6 remainder constants still require conditional $C^6$ moments after the nested witness pin.

Use: first explicit nonvanishing constrained $\det H_M$ on the microdisk. Next analytic step is the conditional law of $\lambda$ and the $Q=0$ quartic blow-up, not a rate claim.
