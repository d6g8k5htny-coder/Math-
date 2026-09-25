# D1 Section 9 amendment — Borel marked Kac–Rice via finite-measure monotone class

**Object:** D1-BOREL-KR-AMEND-20260925-v1  
**Author:** OpenAI / ChatGPT  
**Disposition:** AUTHOR-SIDE AMENDMENT; exact-source nonauthor re-review required.  
**Scientific effect:** NONE.

## 1. Source and defect addressed

This note amends only Section 9 of the frozen author-side candidate
\`UNIFORM-MATRIX-CAP-LIFETIME-20260924-v1\`, Drive id
\`1foDgiDi4XIKOfbrZEE8dWKV_BkZU8LIb\`, 40,261 bytes, SHA256
\`9350ad6eaba6626b93c3dedeef9e2ff816e5cdf1c8318e85fb27499141c84bc7\`.

The frozen parent body is not edited here.

Nonauthor review on main PR112 / comment 5839550742 returned **AMEND** for
the continuous-cylinder to bounded-Borel marked Kac–Rice interface. The
specific defects were:

1. the parent cited Armentano–Azaïs–León Theorem 7.1 for a weighted identity
   that theorem does not state;
2. the elder equality/path indicator is Borel but is not asserted to be lower
   semicontinuous, so the paper's lower-semicontinuous weighted theorem cannot
   simply be applied to that indicator;
3. the source did not explicitly construct the regular conditional law of the
   whole field on \(C^2\) given the two gradients;
4. the monotone-class extension was named but its measure class, generating
   algebra, finiteness and closure properties were not written.

This amendment supplies exactly those interfaces. It does not review or amend
the cap theorem, Theorem A, the residual-field estimates, normalizer, all-mark
domination, coefficient calculation, or any numerical gate.

## 2. Off-diagonal domain and unweighted Kac–Rice

Fix \(\varepsilon>0\) and let

\[
  U_\varepsilon=\{(x,y)\in X\times X:\operatorname{dist}(x,y)\ge\varepsilon\}.
\]

Write
\[
  G_{x,y}(f)=(\nabla f(x),\nabla f(y))\in\mathbb R^{2d}.
\]

On \(U_\varepsilon\), the covariance of \(G_{x,y}\) is positive definite:
the relevant derivative evaluations occur at two distinct sites and are
linearly independent; the periodized field has strictly positive variance in
every Fourier mode. Compactness of \(U_\varepsilon\) then gives a uniform
positive covariance floor. The field is smooth, so the standard hypotheses for
the unweighted zero-count Kac–Rice formula hold.

Thus the unweighted expected number of ordered critical-point pairs in any
compact Borel \(A\subset U_\varepsilon\) is

\[
 \mathbb E N(A)
 =
 \int_A p_{G_{x,y}}(0)\,
   \mathbb E\!\left[
      |\det H_x\,\det H_y|\mid G_{x,y}=0
   \right]\,d(x,y).
 \tag{KR0}
\]

For the external source, use Armentano–Azaïs–León, *On a general Kac–Rice
formula for the measure of a level set* (arXiv:2304.07424v3): Theorem 2.2 is
the Gaussian unweighted base. Theorem 7.1 is **not** used for the weighted
elder identity.

## 3. A canonical conditional field kernel on \(C^2(X)\)

Let \(\mathcal F=C^2(X)\) with its usual separable Banach norm (use a fixed
finite atlas and the suprema of derivatives through order two). The random
field is an \(\mathcal F\)-valued Gaussian random variable.

For each \(z=(x,y)\in U_\varepsilon\) and \(v\in\mathbb R^{2d}\), define the
Gaussian regression field

\[
 F_{z,v}
 =F+
 \operatorname{Cov}(F,G_z)\operatorname{Cov}(G_z)^{-1}
       (v-G_z).
 \tag{K1}
\]

Here \(\operatorname{Cov}(F,G_z)\) is interpreted pointwise and for all
derivatives through order two. The Fourier summability used elsewhere in the
parent proof makes those regression coefficients continuous in \(C^2\), and
the compact covariance floor makes the inverse continuous on
\(U_\varepsilon\). Therefore

\[
 (z,v)\longmapsto \mathcal L(F_{z,v})
\]

is a Borel probability kernel on \(\mathcal F\), continuous against bounded
continuous cylinder functions. It is a concrete version of the regular
conditional law

\[
 \mathcal L(F\mid G_z=v).
 \tag{K2}
\]

No conditioning on a positive-probability event is being assumed.

## 4. Continuous cylinder weights: the only imported weighted step

A bounded continuous cylinder weight has the form

\[
 h(z,f)=\phi\!\left(
   z,\ell_1(f),\ldots,\ell_m(f)
 \right),
 \tag{C1}
\]

where \(\phi\) is bounded continuous and the \(\ell_i\) are finitely many
continuous evaluation/derivative functionals on \(C^2(X)\).

For such \(h\), the field mark is finite-dimensional and jointly Gaussian with
\(G_z\); the regression kernel (K2) is continuous in the imposed gradient
value. The weighted expected-integral identity follows from the established
weighted Kac–Rice result for continuous (hence lower-semicontinuous) weights.
One may cite Armentano–Azaïs–León Theorem 6.1 for this base class; its
lower-semicontinuity requirement is satisfied by (C1).

Hence
\[
 \mathbb E\!\sum_{\substack{z\in U_\varepsilon\\G_z=0}} h(z,F)
 =
 \int_{U_\varepsilon}p_{G_z}(0)
   \,\mathbb E\!\left[
      |\det H_x\det H_y|\,h(z,F_{z,0})
   \right]dz
 \tag{KRc}
\]
for every bounded continuous cylinder \(h\).

Theorem 6.1 is **not** applied directly to the elder indicator below.

## 5. Two finite measures on \(U_\varepsilon\times\mathcal F\)

Define finite measures \(\mu_\varepsilon,\nu_\varepsilon\) on
\(U_\varepsilon\times\mathcal F\) by

\[
 \mu_\varepsilon(A)
 =
 \mathbb E\!\sum_{\substack{z\in U_\varepsilon\\G_z=0}}
       \mathbf 1_A(z,F),
 \tag{M1}
\]

and

\[
 \nu_\varepsilon(A)
 =
 \int_{U_\varepsilon}p_{G_z}(0)
   \,\mathbb E\!\left[
      |\det H_x\det H_y|\,
      \mathbf 1_A(z,F_{z,0})
   \right]dz.
 \tag{M2}
\]

Finiteness follows from (KR0) on the compact off-diagonal domain; both total
masses equal the unweighted expected pair count.

Equation (KRc) states that the two measures integrate every bounded continuous
cylinder function equally.

## 6. Explicit functional monotone-class closure

Choose a countable dense set \(D\subset X\), a finite atlas with rational
coordinate subcharts, and evaluation functionals consisting of function values
and derivatives through order two at points of \(D\). These continuous
functionals separate points of \(C^2(X)\), and their countable cylinder
sigma-algebra equals \(\mathcal B(C^2(X))\). Together with a countable base of
\(U_\varepsilon\), bounded continuous cylinder functions generate

\[
 \mathcal B(U_\varepsilon)\otimes\mathcal B(C^2(X)).
\]

Let
\[
 \mathcal H
 =
 \left\{
  h:\;h\text{ bounded Borel and }
  \int h\,d\mu_\varepsilon=\int h\,d\nu_\varepsilon
 \right\}.
\]

Because \(\mu_\varepsilon\) and \(\nu_\varepsilon\) are finite:

* \(\mathcal H\) is a real vector space and contains the constants;
* if \(0\le h_n\uparrow h\) with all \(h_n\in\mathcal H\) bounded, then
  \(h\in\mathcal H\) by monotone convergence;
* equivalently, uniformly bounded pointwise limits are also preserved by
  dominated convergence.

The bounded continuous cylinder functions form a multiplicative algebra,
contain the constants, separate points, and generate the product Borel
sigma-algebra. The functional monotone-class theorem therefore gives

\[
 \mathcal H=L^\infty_{\mathrm{Borel}}
 (U_\varepsilon\times C^2(X)).
 \tag{M3}
\]

Thus (KRc) holds for **every bounded Borel field mark** on the compact
off-diagonal domain. This extension is our measure-theoretic step; it is not
attributed to a theorem that assumes lower semicontinuity of the final elder
mark.

## 7. The global elder/type mark is Borel on the product space

For a maximum candidate \(x\), define

\[
 d_f(x)=
 \sup_{\substack{\gamma(0)=x\\ f(\gamma(1))>f(x)}}
       \min_t f(\gamma(t)),
\]
with the empty supremum equal to \(-\infty\).

For variable \(x\), the event \(\{d_f(x)>a\}\) is a countable union of strict
polygonal-path tests: use the fixed finite atlas, rational interior vertices,
rational clearances, and a short chart segment from the variable \(x\) to the
first rational vertex. Whenever a continuous path has strict clearance above
\(a\), it has such a rational approximation. Hence
\((x,f)\mapsto d_f(x)\) is Borel as an extended-real map.

Evaluation \((y,f)\mapsto f(y)\) is continuous on \(X\times C^2(X)\).
Therefore
\[
 \{(x,y,f):d_f(x)=f(y)\}
\]
is Borel. Hessian evaluation is continuous into the finite-dimensional
symmetric matrices, and the sets of negative-definite matrices and matrices of
a fixed nondegenerate Morse index are Borel (indeed open away from the
singular locus). Thus the product mark

\[
 h_{\rm elder}(x,y,f)
 =
 \mathbf1\{d_f(x)=f(y)\}
 \mathbf1\{H_x<0\}
 \mathbf1\{\operatorname{index}(H_y)=d-1\}
 \tag{E1}
\]
is bounded Borel on \(U_\varepsilon\times C^2(X)\).

By (M3), (KRc) applies to (E1). On the almost-sure Morse,
distinct-critical-value locus used in the parent proof, (E1) selects exactly
the ordinary finite superlevel elder-death partner; an essential maximum has
no strictly higher endpoint and hence is excluded.

## 8. Height disintegration

Under the conditional kernel \(F_{z,0}\), the pair
\((F(x),F(y))\) is a nondegenerate two-dimensional Gaussian for distinct
\(x,y\) on \(U_\varepsilon\). Its mean, covariance and density vary
continuously in \(z\).

Disintegrating (M2) by those two heights therefore yields the original
full-pin Gaussian density multiplied by the corresponding conditional
expectation of
\[
 W=|\det H_x\det H_y|
   \mathbf1\{H_x<0,\operatorname{index}(H_y)=d-1\}
\]
for candidate pairs, and the same conditional expectation with the elder
indicator for selected pairs. The explicit regression kernel (K1) supplies a
canonical version at every imposed height vector; no assertion depends on an
arbitrary modification on a height-null set.

After the parent notation is restored, the selected density is the candidate
density multiplied by the tilted selection probability \(p_r\), with the
single determinant product already contained in \(W\). No second determinant
copy is introduced.

## 9. Exhaustion toward the diagonal

Apply the bounded-Borel identity first on \(U_\varepsilon\). The parent
Section 10 near-diagonal ledger gives a nonnegative locally integrable
\(C\,r\,dr\) majorant after the full pin density, determinant normalizer, mark
Jacobian and spatial polar factor are combined.

Letting \(\varepsilon\downarrow0\), the domains increase to all distinct
ordered pairs. Nonnegative monotone convergence therefore extends the measure
identity to the off-diagonal pair space. This step imports the stated
near-diagonal integrability estimate; this amendment does not re-prove it.

## 10. Corrected attribution and scope

Replace the parent Section 9 attribution by the following hierarchy:

1. Armentano–Azaïs–León Theorem 2.2: unweighted Gaussian Kac–Rice base on the
   separated pair domain.
2. Their Theorem 6.1: weighted identity for the bounded continuous cylinder
   base class, whose continuity satisfies that theorem's hypotheses.
3. Sections 3–7 of **this amendment**: regular conditional Gaussian kernel on
   \(C^2\) plus finite-measure functional monotone-class extension to the
   bounded Borel elder/type mark.
4. Parent Section 10: nonnegative exhaustion toward the diagonal.

Do **not** cite their Theorem 7.1 as the source of the elder-weighted identity.

This amendment establishes only the previously missing Section 9 interface,
conditional on the parent source's already stated finite-jet
nondegeneracy/smoothness and near-diagonal integrability inputs. It does not
convert those imported inputs into accepted theorems and does not alter any
scientific-status flag.

## 11. Reconnaissance record

Consensus search on 25 September 2026 located Armentano, Azaïs and León,
*On a general Kac–Rice formula for the measure of a level set* (2023, *Annals
of Applied Probability*) as the relevant primary paper. The external paper
provides general level-set/Kac–Rice results; this amendment deliberately
limits external reuse to the unweighted/continuous-weight base described
above. The Borel elder extension is written explicitly rather than attributed
wholesale to that paper.

**Reviewer task:** bind this exact file and the frozen parent digest. Check
(K1) as a Borel regular-conditional Gaussian kernel on \(C^2\); finiteness of
(M1)–(M2); generation of the product Borel sigma-algebra by the stated
countable cylinder algebra; closure (M3); the variable-endpoint elder Borel
argument; height disintegration; and the imported near-diagonal
nonnegative-monotone-convergence step. Return ACCEPT / AMEND / BLOCKED for each
interface. No tests or citation match substitute for that analytic review.
