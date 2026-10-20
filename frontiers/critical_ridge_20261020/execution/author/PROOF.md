# C299 finite proof obligation and argument

This is the author explanation of the bounded partial-gradient ridge unit,
following the conventional route in Math-#487 comment 6292079965. It is not
independent review or evidence of a successful Lean execution.

Let `E = E d`, let `f : E → ℝ` satisfy the literal `IsSmooth d f`, let `p`
satisfy the literal `IsCriticalPoint d f p`, and let `V` be any real linear
subspace on which the literal Hessian is strictly negative on nonzero vectors.
No nonzero-dimension hypothesis is made.

Write `i : V →L[ℝ] E` for inclusion, `R` for the continuous linear restriction
map from ambient continuous covectors to continuous covectors on `V`, and
`H = fderiv ℝ (fderiv ℝ f) p`. C293 proves pointwise equality between this
bilinear map and the literal `iteratedFDeriv` Hessian.

Define

```
G : E × V → (V →L[ℝ] ℝ)
G(w,v) = R (Df(p + w + i(v)))
C : V →L[ℝ] (V →L[ℝ] ℝ)
C(v)(z) = H(i(v))(i(z)).
```

If `C(v)=0`, evaluation at `v` gives `H(i(v))(i(v))=0`. Strict negativity
forces `i(v)=0`, and inclusion is injective. Hence `C` is injective. The Riesz
continuous linear equivalence `J : V ≃L[ℝ] (V →L[ℝ] ℝ)` turns `C` into the
injective endomorphism `J.symm ∘ C`. Finite dimensionality makes that
endomorphism an equivalence, and composing with `J` supplies an exact
continuous linear equivalence whose forward map is `C`. This argument also
works for `V = ⊥`; no nonempty sphere or coercivity lower bound is used.

Literal smoothness at order three gives `ContDiff ℝ 2 (fderiv ℝ f)`.
Composition with affine addition and the fixed restriction map gives C2 of
`G`. Its derivative at zero is

```
DG(0)(w,v) = R (H(w + i(v))).
```

Consequently its derivative in its second argument is exactly `C`, with the
continuous inverse constructed above. The actual pinned smooth
`ContDiffAt.implicitFunction` theorem supplies one function `r : E → V`,
C2 at zero, with `r 0 = 0`, and

```
G(w, r w) = G(0,0)
```

eventually near zero. Literal criticality says `Df(p)=0`, so the right side
is zero. Evaluating this covector equality on each `z : V` is the desired
eventual restricted-gradient equation.

Finally, `w ↦ (w,r w)` has derivative `w ↦ (w, Dr(0)w)` at zero. The
composite `w ↦ G(w,r w)` agrees with the constant zero map in a neighborhood,
so its derivative is zero. Uniqueness of the Fréchet derivative, followed by
evaluation at `w : E` and `z : V`, gives

```
hessian d f p (w + (fderiv ℝ r 0 w : E)) z = 0.
```

All four conclusions concern the same selected implicit function. Restriction
of the ambient parameter to a supplied complementary positive subspace yields
the ridge needed in the subsequent paper argument without assuming the
complement is orthogonal. This unit does not yet prove reduced-Hessian
positivity, a common C2 domain for later paths, uniform Hessian bounds,
concavity, a tube or neighborhood basis, any quotient statement, or the
discharge of C294's closed-level LPC premise.
