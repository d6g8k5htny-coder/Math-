# Contact-kernel reconstruction note (exact cubic + type mass + scoped Gaussian interface statement)

**Object:** OA-CONTACT-KERNEL-SUBSTITUTE-20260926-v1.
**Author of this file:** xAI / Grok (team session 2026-09-26).
**Disposition (amended 2026-09-27):** reconstruction and re-verification of material already on Math- `main` — `reviews/collision_mechanism_20260925/NOTE.md` §B, `reviews/contact_kernel_tail_20260925/KERNEL_TAILS_AND_SMALL_GAP.md` §4, and the PR25 interface record. Scientific effect: **NONE**. It is not a review file and does not create one.
**This is not** `TRANSVERSE_CONTACT_ASYMPTOTIC.md`, and it is not a stand-in for that file. When this note was written nobody held that file's bytes; main issue #56 item 4 forbids substituting a similar contact document without exact identity evidence, and #56 closed via merged Math- #59. (The first version of this note said the object "may be cited in its place"; that clause is withdrawn.) **Update 2026-09-27:** the original bytes have since been recovered and imported on Math- `main` at commit `db6a8d5a099b13cec4364edb544cdf0e34ea720c` (merged #94), path `imports/transverse_contact_library_20260927/TRANSVERSE_CONTACT_ASYMPTOTIC.md`, blob `c2499674d29ad4312e872903d8f5999adc1c51db`, SHA256 `e3ad42b85de72f961978fe9a33d927b54ef8bd09abbd602458e3fb640caa6a73`, together with its geometry companion `GEOMETRY_AND_CUBIC_INDEX.md`, blob `58fbeb8f5180104361938253203b9dfb576af2d9`, SHA256 `4d99cfac30d7d39b69c1a8813c607109328ae310695f1bd609cbc64d5056a6d7`. The filename is therefore no longer ABSENT. The recovered original is the source; this note is a same-workspace re-verification record of finite identities that the original also states (Section 7), not a review of the original and not a source of any credit for it.

## 0. What this note re-verifies

This note reconstructs, and `verify_substitute.py` re-checks in exact rational arithmetic, the following already-published material:

1. the six-pin cubic algebra (pins, solved jets, Hessian determinants, type window);
2. the type-region mass $J=27392/315$ and the factor identities $24\cdot6\cdot9^3=104976$, $2916J=8875008/35$;
3. the fixed-chart ($|v|\ge\eta>0$) Gaussian contact-kernel interface statement of NOTE §§B–C, by citation of the PR25 review's R1–R4 ACCEPT at commit `ad35e46d15c2815c36746442808a1626a9724e8a` (interface-level acceptance by a nonauthor same-workspace xAI/Grok review; no organizational independence; see Section 3).

Do **not** use this note as a source for: $\eta\to0$; interchange of $k\downarrow0$ with $r\downarrow0$ or $v\to0$; `rnu_env.py` / `allcell_fdz` / JETMOD 24-jet carriers; elder-defect or lifetime-density lower bounds.

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

Both identities above are expanded in $\mathbb{Q}[k,q,u,v,\theta,w]$ by `verify_substitute.py` (symbolic polynomial arithmetic, no floating point), together with the six pins, the uniqueness of the $(A,c,d)$ solve for $v\neq0$ (the coefficient determinant is a nonzero monomial in $v$), and the three determinant identities after $q\to w$.

## 2. Type-region mass (machine-checked)

Let $P=P_M P_S P_X$, a polynomial of degree $6$ in $w$ and $3$ in $\theta$. Reverse the order of integration on $I_\theta$:

- left: $-3<w<-1$, $(w+1)^2/4<\theta<1$;
- right: $-1<w<1$, $1-(w-1)^2/4<\theta<1$.

Exact rational integration (polynomial antiderivatives over $\mathbb{Q}$ in `verify_substitute.py`; a SymPy run in the authoring session gave the same values):

$$\int_{\mathrm{left}}P=\frac{77248}{945},\qquad
\int_{\mathrm{right}}P=\frac{704}{135},\qquad
J:=\int P=\frac{27392}{315}.$$

The $(w,\theta)$ area of the type region is $4/3+2/3=2$.

Factor bookkeeping for the $w$-form of the kernel, following NOTE §C4 (C5) and `reviews/pr25_contact_kernel_20260925/algebra_check.py`:

- the height element contributes $k$ and the contact-map minor $v^6/24$ contributes $24/|v|^6$ (together the $24k/(z_0|v|^6)$ prefactor of (C5));
- $dq/dw$ contributes $6k/|v|$;
- three Hessian determinants contribute $9^3 k^6/|v|^6$;
- hence $24\cdot6\cdot9^3=104976$, $k$-power $1+1+6=8$, and total $|v|$-power $6+1+6=13$.

(The first version of this note assigned the $24$ to the height element and the $1/|v|^6$ to the contact map; the product is unchanged, the attribution above matches NOTE line 150.)

The parity form of KERNEL_TAILS uses the prefactor $2916=104976/36$ after $z_0=36k^2 m_{2a}$ cancels two powers of $k$. Then

$$2916J=\frac{8875008}{35}.$$

These rational identities are re-derived by `verify_substitute.py`; they are also asserted on `main` by `reviews/contact_kernel_tail_20260925/test_contact_tools.py`.

## 3. Scoped Gaussian interface statement (reviewed at interface level; not re-proved here)

On the exact variance-one $L$-periodized planar Gaussian field, compact birth/gap marks with $k$ bounded above and away from zero, all orthonormal frames, and every fixed nonempty chart

$$K=\{(u,v):1<A_0\le\sqrt{u^2+v^2}\le B<\infty,\ |v|\ge\eta>0\},$$

the PR25 review ACCEPTS interfaces R1–R4 of NOTE §B–C. Qualifiers that travel with the word "theorem" here, verbatim from the sources: the PR25 review is an xAI/Grok nonauthor review in the same workspace and records "Organizational independence is not awarded"; NOTE line 160 states that its use of marked Kac–Rice "needs separate analytic review, not just the finite algebra tests"; and this note is also authored by xAI/Grok. The statement is therefore interface-level accepted, not independently reviewed, and it is the weakest step of this note because it is the only step that is not finite algebra. This is a fixed-chart statement only. The recovered original (Section 7) states the same fixed-chart theorem as its proposed refined theorem (2.1)–(2.3) with the same exclusions (`eta -> 0`, shrinking cutoffs, global selection); recovery of that text does not add any review to the statement here.

Consequence that may be cited, with the qualifiers above attached:

$$\mathbb{E}_{Q_r^W} N_j(rE)=r^3\int_E\Lambda_j+o(r^3)\,\mathrm{area}(E),$$

uniformly on the declared compact parameters, with $\Lambda_0=\Lambda_2=0$ and $\Lambda_1>0$ off the axis. After $q\to w$,

$$\Lambda_1=\frac{104976\,k^8}{z_0|v|^{13}}\int_0^1\int_{I_\theta} P\,g(0,q(w),c(w),d(w))\,dw\,d\theta,$$

where $z_0=36k^2\mathbb{E}[a^2\mathbf{1}_{a<0}|U_0]$ and $g$ is the conditional four-jet density given the endpoint contact law $U_0=(b,0,0,12k,0,0)$.

The scaled/unscaled distinction is part of the accepted R2: Hessians use $A=\lim a_r/r$; the density $g$ is cut on the unscaled coordinate $a=0$. Those limits are not interchangeable.

## 4. What remains blocked

The following are **not** supplied by this note and stay OPEN / BLOCKED_ABSENT:

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

Companion script: `reviews/contact_kernel_substitute_20260926/verify_substitute.py` (this directory; standard library only). It performs every row above by symbolic expansion over $\mathbb{Q}$, raises explicit errors (not `assert`, so `python -O` does not weaken it), and carries four negative controls that must fail: `--mutate pin_sign` (flips the sign of the $q$ term of $P$), `--mutate det_sign` (flips the sign of $\det B_X$), `--mutate integral_bound` (uses the wrong lower $\theta$-bound on the right region; yields $4672/945\neq704/135$), `--mutate prefactor` (perturbs $24\cdot6\cdot9^3$). The "KERNEL (1.1) jets vs (B2)$+w$" row is covered by the $w$-transform inverse and $dq/dw$ checks together with the (B2) solve. Independent scripts on `main` covering the same rows: `reviews/pr25_contact_kernel_20260925/algebra_check.py` (pins, (B2), determinants, sample, exponent count) and `reviews/contact_kernel_tail_20260925/test_contact_tools.py` (J, left/right, 2916 prefactor, 8875008/35).

```sh
python -B -S reviews/contact_kernel_substitute_20260926/verify_substitute.py
python -B -O -S reviews/contact_kernel_substitute_20260926/verify_substitute.py
for m in pin_sign det_sign integral_bound prefactor; do python -B -S reviews/contact_kernel_substitute_20260926/verify_substitute.py --mutate $m; done
```

## 6. How to cite

> Cubic contact algebra and type mass: NOTE §B (`reviews/collision_mechanism_20260925/NOTE.md`, blob `3ee3082911f4e8ebee93805633a326940aee17bf`) and KERNEL_TAILS §4, re-verified in OA-CONTACT-KERNEL-SUBSTITUTE-20260926-v1 / `verify_substitute.py`.
> Fixed-chart Gaussian interface statement on $|v|\ge\eta$: PR25 REVIEW R1–R4 ACCEPT at `ad35e46`, path `reviews/collision_mechanism_20260925/NOTE.md` §§B–C; same-workspace xAI/Grok nonauthor review, no organizational independence; marked Kac–Rice use needs separate analytic review.
> `TRANSVERSE_CONTACT_ASYMPTOTIC.md`: cite the recovered original on `main` (`db6a8d5a…`, `imports/transverse_contact_library_20260927/`, blob `c2499674…`, SHA256 `e3ad42b8…`), not this note. This object did not restore it and is not cited in its place.

## 7. Relation to the recovered original (added 2026-09-27)

The recovered exposition and its geometry companion were imported byte-for-byte by merged Math- #94 (`main` `db6a8d5a099b13cec4364edb544cdf0e34ea720c`; identities in the header of this note and in `imports/transverse_contact_library_20260927/SOURCE_BINDING.json`). Read against those files, this note's finite content coincides with the following displayed items of the originals, and `verify_substitute.py` therefore also re-derives them:

| This note | Recovered original | Content |
|---|---|---|
| §1 form of $P$ | `GEOMETRY_AND_CUBIC_INDEX.md` (4.1) | six-pin cubic family |
| §1 solve $(A,c,d)$ | `GEOMETRY_AND_CUBIC_INDEX.md` (4.2); `TRANSVERSE_CONTACT_ASYMPTOTIC.md` (5.2) | $c=-12kD/v^2-2qu/v$, $d=12k(L_c+\theta)/v^3+3qD/v^2$, $A=(12ku+6k+qv-12k\theta)/(2v^2)$ |
| §1 $B_M,B_S,B_X$ and $\det$ identities | `GEOMETRY_AND_CUBIC_INDEX.md` (4.3), (5.1) | $\det B_X=-(9k^2/v^2)[(w+1-2\theta)^2+4\theta(1-\theta)]$ with $w=(qv+12ku)/(6k)$ |
| §1 rational sample | `GEOMETRY_AND_CUBIC_INDEX.md` §5 | $u=2,v=1,k=1,\theta=1/2,q=-30$: $A=-3,c=75,d=-363/2$, dets $18,-18,-18$ |
| §1 interval $I_\theta$ | `TRANSVERSE_CONTACT_ASYMPTOTIC.md` (6.2) | $-1-2\sqrt\theta<w<1-2\sqrt{1-\theta}$ |
| §2 factor $24k/(z_0\lvert v\rvert^6)$, $dq=(6k/\lvert v\rvert)dw$ | `TRANSVERSE_CONTACT_ASYMPTOTIC.md` (6.1) and §6 | contact-map Jacobian $\lvert v\rvert^6/24$; $z_0=36k^2\,\mathbb{E}[a^2\mathbf 1_{a<0}\mid U_0=v_0]$ (3.1) |

Differences, so that nothing is over-attributed:

- The type-region mass $J=27392/315$, the left/right integrals, and the factor identities $104976$, $2916J=8875008/35$ (§2) are **not** in the recovered original; they come from NOTE §C / KERNEL_TAILS §4 on `main`, as cited above.
- The recovered original's §7 unperiodized diagnostic (four-jet conditional law $N((-b,0,0,0),\mathrm{diag}(2,2,2,6))$) is not checked by `verify_substitute.py`.
- The original's continuum steps (uniform Gaussian regression, scaled-Hessian passage, normalizer, marked Kac–Rice) are exactly the steps this note lists as interface-level only. Recovery of the text does not review them; the import README on `main` requests a separate nonauthor source-custody review and states that existing reviews of the consolidated PR25 note are not automatically reviews of the recovered exposition.

Consequently the coincidence table above is a finite-identity cross-check between this note's script and the recovered text, and nothing more.
