# Hard-negative fibre lift of the planar elder barrier

Author-side deterministic contribution by OpenAI `concave_fibre_geometry`, 30 September 2026. This is a mathematical extension candidate, not a source acceptance decision. It changes no existing source, status, integration disposition or probability/count claim. Its planar input is §§2–6 of `local_elder_geometry_20260930/PROOF.md`, corresponding to the requested PR170 cut. Source-cut verification and acceptance provenance are separate obligations handled by the parent task.

## 1. The planar input and the additional geometric condition

Let

\[
P(X,Z)=2kX^3-\frac{3k}{2}X-\frac{k}{2}
 +\frac{s}{2}Z^2+\frac a2(X^2-1/4)Z
 +\frac\beta2XZ^2+\frac c6Z^3,
\]

with \(k>0\), \(M=(-1/2,0)\), \(S=(1/2,0)\),
\[
B=\beta-a^2/(12k),\qquad
D=(c-a\beta/(4k)+a^3/(72k^2))/2.
\]
Assume the strict typed condition \(s<-|B|/2\), and exclude
\[
12kD^2+(s-B)^2(B+2s)=0,\qquad 12kD^2+B^3=0.
\]
Let \(\mathcal Y=\{S\}\cup C(P)\), where \(C(P)\) consists of the additional critical points in \(-k<P<0\), and put
\[
h_* = \max_{Y\in\mathcal Y}P(Y).
\]
The planar input proves that these are finitely many nondegenerate saddles, and that its compact caps and critical chords determine elder death exactly.

Write \(m=d-2\). For each \(i\), let \(f_i\) be a smooth height on a compact \(d\)-manifold, and let an embedded chart \(\Psi_i\) have normalized height
\[
g_i(x,z)=\frac{f_i(\Psi_i(x,z))-b_i}{r_i^3},
\qquad x\in\mathbb R^2,\ z\in\mathbb R^m,
\qquad r_i\longrightarrow0.
\]
The coordinate map may have different scales in different directions. The theorem requires only that the concrete tubes and paths below lie inside this embedded chart.

The following hypotheses suffice.

1. On every fixed soft disk needed below, there is a \(C^1\) interior fibre maximum graph \(z=\zeta_i(x)\), with \(\partial_zg_i(x,\zeta_i(x))=0\). Each fibre used below is convex, and \(\partial^2_{zz}g_i\) is negative definite throughout it. Consequently its unique maximum is the graph point. Define the reduced height
   \[
   G_i(x)=g_i(x,\zeta_i(x)).
   \]
2. The reduced heights converge to \(P\) in \(C^2\) on each fixed compact soft disk. The pins are exact:
   \[
   G_i(M)=0,\quad \nabla G_i(M)=0,\quad
   G_i(S)=-k,\quad \nabla G_i(S)=0.
   \]
3. For a sufficiently large **fixed** soft disk \(\overline B_R\), containing the planar collar and all doubled critical chords, there is a compact hard tube
   \[
   T_i=\{(x,z):x\in\overline B_R,\ z\in\overline F_i(x)\}
   \]
   lying in the chart interior. Its fibres are bounded convex domains containing \(\zeta_i(x)\), and they vary continuously as a tube. For some fixed \(D_0>k\), the hard boundary obeys the relative drop estimate
   \[
   g_i(x,z)\le G_i(x)-D_0\quad(x\in\overline B_R,\ z\in\partial F_i(x)). \tag{HD}
   \]
   A graph-centred ellipsoid tube, described below, is a concrete sufficient interpretation of this tube hypothesis.

No uniform lower bound on the hard Hessian eigenvalues is needed if (HD) is given directly. No control is required outside this tube. Strict negativity by itself, without (HD) or an equivalent closed-barrier condition, does not suffice.

The hard tube need not cover the whole of \(B_{R+1}\): the reduced height only needs to be defined there for the planar collar construction, whereas the full lift needs a tube over the smaller disk containing the resulting caps. The graph paths also remain in that smaller disk.

## 2. Deterministic conclusion

For each \(Y\in\mathcal Y\), let \(Y_i\) be the unique continued critical point of \(G_i\), taking \(S_i=S\), and let
\[
h_i=\max_{Y\in\mathcal Y}G_i(Y_i),\qquad
\widehat Y_i=\Psi_i(Y_i,\zeta_i(Y_i)),\qquad
\widehat M_i=\Psi_i(M,\zeta_i(M)).
\]
For all sufficiently large \(i\),
\[
\boxed{\quad d_{f_i}(\widehat M_i)=b_i+r_i^3h_i.\quad} \tag{EHD}
\]
Here \(d_f(M)=\sup_{\gamma(0)=M,\ f(\gamma(1))>f(M)}\min_t f(\gamma(t))\) is the ordinary global superlevel maximin. In particular,
\[
\frac{d_{f_i}(\widehat M_i)-b_i}{r_i^3}\to h_*.
\]
On the actual global Morse distinct-value locus, the unique graph point \(\widehat Y_i\) attaining \(h_i\) is the actual elder merge saddle. If \(C(P)\) is empty, this is exactly the lifted pinned saddle. If \(C(P)\) is nonempty, a continued window saddle has height strictly above \(-k\) and preempts the pinned saddle. Limiting ties do not obstruct the exact statement: one compares the finitely many actual heights at index \(i\).

The actual lifetime is therefore exactly
\[
b_i-d_{f_i}(\widehat M_i)=-r_i^3h_i,
\]
and its normalized limit is \(-h_*\). This is a deterministic geometry/lifetime result. It supplies no higher-dimensional tilted-law exhaustion, intensity, coefficient or count statement.

## 3. Graph regularity and full critical-point indices

At each fibre stationary point, negative definiteness makes \(g_{zz}\) invertible. The ordinary implicit function argument gives \(\zeta_i\in C^1\) for \(g_i\in C^2\), and
\[
D\zeta_i=-g_{zz}^{-1}g_{zx},\qquad
\nabla G_i=g_x,\qquad
\nabla^2G_i=g_{xx}-g_{xz}g_{zz}^{-1}g_{zx}. \tag{SC}
\]
Thus \(G_i\in C^2\) even though a \(C^2\) graph is unnecessary. Existence of an interior fibre maximum must be assumed or separately verified; strict concavity alone only gives uniqueness once such a point exists.

A point of the tube is full critical if and only if it lies on the graph and its soft point is critical for \(G_i\). At such a point, for soft and hard tangent vectors \(v,w\),
\[
(v,w)^T\nabla^2g_i(v,w)
=v^T\nabla^2G_i v
 +(w+g_{zz}^{-1}g_{zx}v)^Tg_{zz}(w+g_{zz}^{-1}g_{zx}v).
\]
This is an explicit invertible triangular change of variables, so full inertia adds \(m\) negative directions to reduced inertia. A reduced maximum lifts to a full maximum; a reduced saddle lifts to a nondegenerate full saddle with one positive direction and \(d-1\) negative directions, the superlevel merge index. No parametric Morse normal-form theorem is invoked.

## 4. A fixed soft collar works at every level above the actual highest saddle

For completeness, this records the properties of the planar construction that the lift actually needs.

The cubic gradient estimate off the second excluded algebraic set gives
\[
|\nabla P(x)|\ge c_0|x|^2\quad(|x|\ge R_0).
\]
Choose \(R_0\) to contain all window roots, the pins, and a small oval about \(M\). Choose \(R\) sufficiently large to contain all doubled chords and satisfy
\[
R-R_0>\frac{2k}{c_0R_0^2}+1.
\]
For all sufficiently large \(i\), reduced \(C^1\) convergence on \(\overline B_{R+1}\) gives
\[
|\nabla G_i(x)|\ge(c_0/2)|x|^2
\quad(R_0\le|x|\le R+1).
\]
There are no reduced critical points in \((h_i,0)\) inside \(B_{R+1}\). This is elementary finite-root stability: around any nondegenerate root \(Y\), the map
\(x\mapsto x-(\nabla^2P(Y))^{-1}\nabla G_i(x)\)
is a contraction on a sufficiently small closed ball and maps that ball into itself for large \(i\). It has exactly one root there. Outside these disjoint root balls, in a slightly enlarged compact height band containing \([-k,0]\), \(\nabla P\) has a positive lower bound; convergence excludes any other roots. The excluded transition set prevents an additional critical point at \(-k\), and the source proves that the only critical point at or above zero is \(M\).

Fix \(t_0\in(h_*,0)\) sufficiently close to zero. Uniformly negative Hessians in a small ball about the exact pin give a small disk \(K_{i,0}\) with
\[
G_i=t_0\text{ on }\partial K_{i,0},\qquad
t_0\le G_i\le0\text{ on }K_{i,0}.
\]
One can construct the disk without a Morse lemma: the radial derivative from \(M\) is strictly negative under the negative Hessian bound, so every ray meets level \(t_0\) once and the implicit function theorem gives its oval.

For every \(h_i<h<t_0\), transport this disk for time \(t_0-h\) by
\[
V_{i,h}=-\eta(x)\chi_h(G_i(x))\frac{\nabla G_i(x)}{|\nabla G_i(x)|^2},
\]
where \(\eta=1\) on \(B_R\) and has support in \(B_{R+1}\), while \(\chi_h=1\) on \([h,t_0]\), is supported in a critical-free strip inside \((h_i,0)\), and vanishes near zero. The field is smooth with compact support. The fixed annulus speed bound and the displayed choice of \(R\) prevent a boundary trajectory reaching \(\partial B_R\) during time \(t_0-h<k\). Its level consequently drops at exact speed one. The resulting disk \(K_{i,h}\subset B_R\) satisfies
\[
G_i=h\text{ on }\partial K_{i,h},\qquad
h<G_i\le0\text{ on }\operatorname{int}K_{i,h},\qquad M\in\operatorname{int}K_{i,h}. \tag{CAP}
\]
The strict interior inequality follows directly from the flow: an interior initial value is greater than \(t_0\), its drop rate is at most one, and the elapsed time is \(t_0-h\). The Jordan curve bounds a disk inside \(B_R\), because the connected exterior of \(B_R\) lies in its unbounded complementary component. The same sufficiently large index works for **all** \(h\in(h_i,t_0)\); there is no exchange of the index and level limits.

## 5. The compact full-dimensional cap

For such an \(h\), first consider the closed fibre barrel
\[
\mathcal B_{i,h}=\{(x,z):x\in K_{i,h},\ z\in\overline F_i(x)\}.
\]
It is compact, contains the birth point in its interior, and lies inside the embedded chart. Fibre maximality gives \(g_i(x,z)\le G_i(x)\le0\). On its lateral boundary,
\(g_i\le G_i=h\); on its hard boundary, (HD) and \(G_i\le0\) give \(g_i\le-D_0<-k\le h_i<h\). Thus every global path from the birth to an older point exits this barrel and has minimum at most \(h\). No exterior continuation can avoid crossing a boundary of a compact embedded barrel.

There is also a genuine compact superlevel cap, rather than just a barrel:
\[
\mathcal C_{i,h}=\{(x,z):x\in K_{i,h},\ z\in\overline F_i(x),\ g_i(x,z)\ge h\}.
\]
For each interior soft point, its hard section is nonempty, compact and convex by concavity; over the soft boundary it is the single graph point, because strict concavity and \(G_i=h\) give equality only at the maximum. Straight fibre segments retract the cap onto the graph over \(K_{i,h}\), so it is connected.

Its full boundary is exactly a regular level surface \(g_i=h\). No hard tube boundary is met. At a boundary point off the graph, a hard derivative is nonzero: if \(v=z-\zeta_i(x)\ne0\),
\[
v\cdot\partial_zg_i(x,z)
=\int_0^1v^Tg_{zz}(x,\zeta_i(x)+tv)v\,dt<0.
\]
At a boundary point on the graph, the critical-free strip \(h_i<G_i<0\) gives a nonzero soft derivative of \(G_i\), hence of \(g_i\). The cap lies entirely at height at most zero and has boundary at height \(h\). For any chosen target \(t>h_i\), choose \(h\in(h_i,\min(t,t_0))\): this is a compact full cap whose boundary is strictly below that target. These direct derivative checks supply all regularity used here.

The barrel argument already proves global normalized death \(\le h\) for every \(h>h_i\) sufficiently close to \(h_i\). Letting \(h\downarrow h_i\) gives the exact upper bound \(\le h_i\).

## 6. Exact lower bound on the graph, and actual pairing

For each \(Y\in\mathcal Y\), use the moving soft critical chord
\[
x_i(t)=M+t(Y_i-M),\qquad
q_i(t)=G_i(x_i(t)),\qquad 0\le t\le2.
\]
Exact criticality gives \(q_i'(0)=q_i'(1)=0\). Reduced \(C^2\) convergence gives convergence of these restrictions in \(C^2\) to
\[
q(t)=P(Y)(3t^2-2t^3).
\]
The limit has \(q''(0)=6P(Y)<0\), \(q''(1)=-6P(Y)>0\), negative derivative on \((0,1)\), positive derivative on \((1,2)\), and \(q(2)=-4P(Y)>0\). Second-derivative signs near the two exact derivative zeros, followed by first-derivative convergence away from those zeros, give the same strict monotonicity for \(q_i\) for all sufficiently large \(i\). Therefore its exact minimum is \(G_i(Y_i)\), and its endpoint is older than birth.

Lift the chord to the actual chart by
\[
\gamma_{i,Y}(t)=\Psi_i(x_i(t),\zeta_i(x_i(t))).
\]
This path has exactly the same height restriction \(b_i+r_i^3q_i(t)\). The graph may curve sharply and its hard coordinates need not converge; no approximation by a full-dimensional straight chord is made. Its inclusion in the tube is all that is needed. There are finitely many such paths, so one sufficiently large index works for all of them. The path corresponding to an actual maximizer of \(G_i(Y_i)\) gives normalized global death \(\ge h_i\), proving (EHD).

This also directly identifies the merge at that graph point. Just above \(h_i\), the chord's two sides lead respectively to the birth and to an older endpoint, and they are in different global superlevel components because death is \(h_i\). At level \(h_i\), the chord joins them at \(\widehat Y_i\). On the global distinct-critical-value locus, no other critical point has that same height. The Schur identity proves it is a full merge-index saddle. Hence it is the actual elder saddle under the same ordinary maximin convention as the planar theorem. No Morse–Smale assumption or separatrix identification is needed.

## 7. A quantitative test for anisotropic hard extent

A simple sufficient replacement for (HD) is a positive-definite matrix \(A_i(x)\), a fixed depth \(D_0>k\), and the graph-centred ellipsoid tube
\[
F_i(x)=\{\zeta_i(x)+v:v^TA_i(x)v<2D_0\}.
\]
Assume this compact tube lies in the chart interior and, throughout every fibre,
\[
g_{zz}(x,z)\preceq-A_i(x).
\]
Twice integrating along the hard segment from the stationary maximum gives
\[
g_i(x,\zeta_i(x)+v)\le G_i(x)-\frac12v^TA_i(x)v.
\]
On the hard boundary the drop is at least \(D_0\); above a planar cap, \(G_i\le0\), so hard boundary height is at most \(-D_0<-k\). This proves the needed barrier. The theorem only needs this boundary estimate above the cap family; imposing it over all \(B_R\) is a convenient checkable condition.

The semiaxes are \(\sqrt{2D_0/\lambda_j(A_i(x))}\). They may depend on \(i\), on the base point, and on direction. Thus anisotropic full-chart extent is harmless provided those ellipsoids actually fit. Uniform hard concavity combined with an arbitrarily thin chart is insufficient. In physical coordinates with straight hard fibres (or an affine map in the hard variables), if an unnormalized physical hard Hessian obeys \(f_{yy}\preceq-H_i(x)\), the corresponding physical requirement is a contained ellipsoid
\[
v^TH_i(x)v\le2D_0r_i^3.
\]
When \(H_i\) has order-one eigenvalues, its physical semiaxes have order \(r_i^{3/2}\). This is a sufficient geometric scale, not an assertion that the actual stochastic model supplies it.

For an arbitrary nonlinear chart, one must verify the normalized-coordinate hard Hessian/drop directly, or include the chart's extra second-derivative terms; a physical Hessian bound does not automatically transform by congruence away from a full critical point.

The logically weaker boundary condition is that hard boundary height is at most \(h_i\) over every cap used for levels decreasing to \(h_i\). A fixed margin below \(-k\) avoids depending on the unknown actual winning height and verifies this at once. Some closed full-dimensional barrier condition is indispensable if the exterior is arbitrary; strict hard concavity is one useful means of producing its vertical part.

## 8. Explicit vertical-escape counterexample without depth

Choose
\[
P(X,Z)=2X^3-\frac32X-\frac12-\frac12Z^2+\frac13Z^3.
\]
Here \(k=1,s=-1,a=\beta=0,c=2\), hence \(B=0,D=1\), and the excluded discriminants are \(10\) and \(12\). The four critical points have heights
\[
P(-1/2,0)=0,\quad P(1/2,0)=-1,\quad
P(-1/2,1)=-1/6,\quad P(1/2,1)=-7/6.
\]
Thus \(h_*=-1/6\).

Let \(\epsilon_i\downarrow0\), and let \(\chi\in C^\infty(\mathbb R,[0,1])\) be zero on \(( -\infty,1]\) and one on \([2,\infty)\). For definiteness use elder height \(A=\sqrt2\), and set
\[
H_i(w)=(1-\chi(w/\epsilon_i))(-w^2)
 +\chi(w/\epsilon_i)\,[A-(w-3\epsilon_i)^2],
\qquad F_i(X,Z,w)=P(X,Z)+H_i(w).
\]
On the chart \(\mathbb R^2\times(-\epsilon_i,\epsilon_i)\),
\[
F_i=P-w^2,
\]
so the hard Hessian is the uniformly strictly negative scalar \(-2\), the unique fibre maximum graph is \(w=0\), and its reduced height is exactly \(P\) on every compact soft set. Yet the exterior has an older strict maximum at \((M,3\epsilon_i)\), of height \(A\). Along \(0\le w\le3\epsilon_i\), the first blend term vanishes for \(w\ge2\epsilon_i\) and is otherwise at least \(-4\epsilon_i^2\); the second term is nonnegative for sufficiently small \(\epsilon_i\). Hence
\[
d_{F_i}(M,0)\ge-4\epsilon_i^2>-1/6.
\]
A maximin beginning at height zero is at most zero, so these actual death levels tend to zero, rather than to \(h_*\). The obstruction is already visible at the hard chart boundary:
\[
F_i(M,\epsilon_i)=-\epsilon_i^2\to0.
\]
For a compact-manifold version, protect a soft neighbourhood containing the pins, the four critical points and the vertical path; for each \(i\) its normalized radius can be finite but increasing to infinity. Multiply/extend smoothly outside a larger neighbourhood into a coordinate ball of a compact manifold. This retains convergence on every fixed normalized soft disk and changes neither the chart hypotheses nor the exhibited path bound. Additional \(m-1\) hard directions can be appended as \(-|z'|^2\), giving the same failure in every \(d\ge3\). Generic arbitrarily small perturbations away from the protected chart and the protected older maximum can impose the global Morse distinct-value locus while preserving the vertical-path lower bound (with, for example, \(-5\epsilon_i^2\) in place of \(-4\epsilon_i^2\)). The height counterexample itself does not need this extra locus.

It also realizes genuinely shrinking anisotropic charts. Choose any \(r_i\downarrow0\), take
\(\Psi_i(X,Z,w)=(r_iX,r_iZ,r_i^{3/2}w)\)
in a fixed coordinate ball, and set \(f_i\circ\Psi_i=b_i+r_i^3F_i\) on the protected region. For example, choose its normalized soft radius \(R_i=r_i^{-1/2}\); its physical radius is then \(r_i^{1/2}\), so it fits inside the fixed coordinate ball while containing every fixed normalized soft disk for all large \(i\). Extend outside the protected physical region. On the thin physical hard chart \(|y|<r_i^{3/2}\epsilon_i\), the physical hard Hessian is exactly \(f_{yy}=-2\). Thus even an order-one uniformly negative physical hard Hessian does not repair an inadequately thin hard domain.

## 9. What remains unproved by this deterministic lift

The actual higher-dimensional probabilistic model must still verify the interior graph, reduced pinned \(C^2\) convergence, a contained hard tube with adequate depth, and the required embedded chart. None is inferred from planar convergence alone, eigenvalue language alone, or a witness-count packet. The lemma requires no Gaussian exhaustion and supplies none. A hard-position limit additionally needs control of the graph coordinates \(\zeta_i(Y_i)\); the exact partner statement and soft-position limit do not need it. A unique limiting soft partner requires the same optional distinct limiting saddle-height condition as the planar proof (for example its additional \(D\ne0\) exclusion).
