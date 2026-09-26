# Contact-kernel substitute (exact cubic + type mass + scoped Gaussian theorem)

**Object:** OA-CONTACT-KERNEL-SUBSTITUTE-20260926-v1.
**Author of this file:** xAI / Grok (team session 2026-09-26).
**Disposition:** new reconstruction note. Scientific effect: **NONE** until an independent review file exists.
**This is not** `TRANSVERSE_CONTACT_ASYMPTOTIC.md`. That filename remains ABSENT. This object may be *cited in its place* only inside the scope below.

## 0. What this substitute is allowed to replace

Use this note instead of the missing TRANSVERSE exposition for:

1. the six-pin cubic algebra (pins, solved jets, Hessian determinants, type window);
2. the type-region mass $J=27392/315$ and the factor identities $24\cdot6\cdot9^3=104976$, $2916J=8875008/35$;
3. the Gaussian contact-kernel theorem on a **fixed chart** $|v|\ge\eta>0$, by citation of the already-reviewed PR25 R1–R4 ACCEPT at commit `ad35e46d15c2815c36746442808a1626a9724e8a`.

Do **not** use this note as a substitute for: $\eta\to0$; interchange of $k\downarrow0$ with $r\downarrow0$ or $v\to0$; `rnu_env.py` / `allcell_fdz` / JETMOD 24-jet carriers; elder-defect or lifetime-density lower bounds.

Cited live sources (not reconstructed):

- `reviews/collision_mechanism_20260925/NOTE.md` blob `3ee3082911f4e8ebee93805633a326940aee17bf`
- `reviews/pr25_contact_kernel_20260925/REVIEW.md` (R1–R4 ACCEPT, chart $|v|\ge\eta$)
- `reviews/contact_kernel_tail_20260925/KERNEL_TAILS_AND_SMALL_GAP.md` (type-mass algebra; tails remain separately unaccepted here)

## 1. Exact cubic (machine-checked)

Every real polynomial of total degree $\le3$ meeting the six pins
$M=(-1/2,0)$, $S=(1/2,0)$, heights $0,-k$ ($k>0$), zero gradients, is

$$P(s,t)=-\frac{k}{2}+2ks^3-\frac{3k}{2}s+\frac{A}{2}t^2+\frac{q}{2}\Bigl(s^2-\frac14\Bigr)t+\frac{c}{2}st^2+\frac{d}{6}t^3.$$

Direct substitution gives $P(M)=P_s(M)=P_t(M)=0$ and $P(S)=-k$, $P_s(S)=P_t(S)=0$.

Hessians at the pins:

$$B_M=\begin{pmatrix}-6k&-q/2\\-q/2&A-c/2\end{pmatrix},\quad
B_S=\begin{pmatrix}6k&q/2\\q/2&A+c/2\end{pmatrix}.$$

Let $X=(u,v)$ with $v\neq0$ be a third critical point of height $-k\theta$, $0<\theta<1$.
Write $D=u^2-1/4$ and $L_c=2u^3-3u/2-1/2$. Solving $\nabla P(X)=0$ and $P(X)=-k\theta$ for $(A,c,d)$ yields the unique solution

$$c=-\frac{12kD}{v^2}-\frac{2qu}{v},\qquad
d=\frac{12k(L_c+\theta)}{v^3}+\frac{3qD}{v^2},\qquad
A=\frac{qv+6k(2u+1-2\theta)}{2v^2}.$$

Type coordinate $w=(qv+12ku)/(6k)$ is equivalent to $q=6k(w-2u)/v$ and $|dq/dw|=6k/|v|$.
After this change,

$$\det B_M=\frac{9k^2}{v^2}P_M,\quad
\det B_S=\frac{9k^2}{v^2}\bigl(4(1-\theta)-(w-1)^2\bigr),\quad
\det B_X=-\frac{9k^2}{v^2}P_X,$$

with

$$P_M=4\theta-(w+1)^2,\quad
P_S=(w-1)^2-4(1-\theta),\quad
P_X=(w+1-2\theta)^2+4\theta(1-\theta).$$

On $0<\theta<1$ one has $P_X\ge4\theta(1-\theta)>0$, so $\det B_X<0$: the witness is a nondegenerate saddle.
$(B_M)_{11}=-6k<0$, so $B_M$ is negative definite iff $P_M>0$. $(B_S)_{11}=6k>0$, so $B_S$ is a saddle iff $P_S>0$. The intersection of those two open conditions is the nonempty interval

$$I_\theta=\bigl(-1-2\sqrt{\theta},\;1-2\sqrt{1-\theta}\bigr),$$

of length $2(1+\sqrt{\theta}-\sqrt{1-\theta})>0$ for every $\theta\in(0,1)$.

Sample (NOTE §B): $u=2,v=1,k=1,\theta=1/2,q=-30$ gives $w=-1$, $A=-3$, $c=75$, $d=-363/2$, determinants $18,-18,-18$.

Saddle-side identity used by the companion tail note:

$$R:=-2u^3-\tfrac32 u-1+2\theta+3w\bigl(u^2-\tfrac14\bigr)
=-2\bigl(u-\tfrac12\bigr)^3+3\bigl(u^2-\tfrac14\bigr)(w-1)-2(1-\theta).$$

Both identities above were expanded in $\mathbb{Q}[k,q,u,v,\theta,w]$ in this session and agreed.

## 2. Type-region mass (machine-checked)

Let $P=P_M P_S P_X$, a polynomial of degree $6$ in $w$ and $3$ in $\theta$. Reverse the order of integration on $I_\theta$:

- left: $-3<w<-1$, $(w+1)^2/4<\theta<1$;
- right: $-1<w<1$, $1-(w-1)^2/4<\theta<1$.

Exact rational integration (SymPy, this session):

$$\int_{\mathrm{left}}P=\frac{77248}{945},\qquad
\int_{\mathrm{right}}P=\frac{704}{135},\qquad
J:=\int P=\frac{27392}{315}.$$

The $(w,\theta)$ area of the type region is $4/3+2/3=2$.

Factor bookkeeping for the $w$-form of the kernel:

- height/contact element contributes $24k$;
- $dq/dw$ contributes $6k/|v|$;
- three Hessian determinants contribute $9^3 k^6/|v|^6$;
- the contact map Jacobian contributes $1/|v|^6$;
- hence $24\cdot6\cdot9^3=104976$ and total $|v|$-power $6+6+1=13$.

The parity form of KERNEL_TAILS uses the prefactor $2916=104976/36$ after $z_0=36k^2 m_{2a}$ cancels two powers of $k$. Then

$$2916J=\frac{8875008}{35}.$$

These four rational identities were re-derived independently in this session; they are not copied as implementation answers.

## 3. Scoped Gaussian theorem (already reviewed; not re-proved here)

On the exact variance-one $L$-periodized planar Gaussian field, compact birth/gap marks with $k$ bounded above and away from zero, all orthonormal frames, and every fixed nonempty chart

$$K=\{(u,v):1<A_0\le\sqrt{u^2+v^2}\le B<\infty,\ |v|\ge\eta>0\},$$

the PR25 review ACCEPTS interfaces R1–R4 of NOTE §B–C. That is the Gaussian contact-asymptotic statement the missing TRANSVERSE file was supposed to expand, **restricted to this chart**.

Consequence that may be used as a substitute citation:

$$\mathbb{E}_{Q_r^W} N_j(rE)=r^3\int_E\Lambda_j+o(r^3)\,\mathrm{area}(E),$$

uniformly on the declared compact parameters, with $\Lambda_0=\Lambda_2=0$ and $\Lambda_1>0$ off the axis. After $q\to w$,

$$\Lambda_1=\frac{104976\,k^8}{z_0|v|^{13}}\int_0^1\int_{I_\theta} P\,g(0,q(w),c(w),d(w))\,dw\,d\theta,$$

where $z_0=36k^2\mathbb{E}[a^2\mathbf{1}_{a<0}|U_0]$ and $g$ is the conditional four-jet density given the endpoint contact law $U_0=(b,0,0,12k,0,0)$.

The scaled/unscaled distinction is part of the accepted R2: Hessians use $A=\lim a_r/r$; the density $g$ is cut on the unscaled coordinate $a=0$. Those limits are not interchangeable.

## 4. What remains blocked

The following are **not** supplied by this substitute and stay OPEN / BLOCKED_ABSENT:

- $\eta\to0$ and any axis chart;
- exchanging $k\downarrow0$ with $r\downarrow0$ (KERNEL_TAILS (4.5) is a statement about the *limiting* kernel only);
- PR22 two-scale / fixed-annulus domination (ANNULUS_BRIDGE remains conditional);
- `rnu_env.py`, `allcell_fdz_enclosures.py`, `CL_ANTHROPIC_BUNDLE`, `cancelled_detgg`, `StationBox`, `explicit_interval_map_F_G12box`;
- any move of `lemma_closed`, prizes, or parent D1.

## 5. Verification record

This session re-checked, in $\mathbb{Q}$-arithmetic:

| Identity | Result |
|---|---|
| six pins on $P$ | PASS |
| unique solve $(A,c,d)$ vs NOTE (B2) | PASS |
| three $\det B_\bullet$ vs $(P_M,P_S,P_X)$ | PASS |
| KERNEL (1.1) jets vs (B2)$+w$ | PASS |
| $R$ vs saddle-side (3.1) | PASS |
| $P_X=(w+1-2\theta)^2+4\theta(1-\theta)$ | PASS |
| sample dets $18,-18,-18$ | PASS (prior PR25 script + this session) |
| $\int_{\mathrm{left}}P=77248/945$ | PASS |
| $\int_{\mathrm{right}}P=704/135$ | PASS |
| $J=27392/315$ | PASS |
| $24\cdot6\cdot9^3=104976$ | PASS |
| $2916J=8875008/35$ | PASS |
| type-region area $=2$ | PASS |

Companion script: `reviews/contact_kernel_substitute_20260926/verify_substitute.py`.

## 6. How to cite

> Cubic contact algebra and type mass: OA-CONTACT-KERNEL-SUBSTITUTE-20260926-v1.
> Gaussian theorem on $|v|\ge\eta$: PR25 REVIEW R1–R4 ACCEPT at `ad35e46`, path `reviews/collision_mechanism_20260925/NOTE.md` §§B–C.
> Missing filename `TRANSVERSE_CONTACT_ASYMPTOTIC.md` is still ABSENT; this object does not restore it.
