import RegularPointChart

open scoped Topology

namespace UniversalLaw.Spec.Lifetime

noncomputable section

variable {d : ℕ} {g : E d → ℝ} {x : E d}

example (hg : IsSmooth d g) (hx : ¬ IsCriticalPoint d g x) :
    OpenPartialHomeomorph (E d) (ℝ × (fderiv ℝ g x).ker) :=
  regularPointChart hg hx

example (hg : IsSmooth d g) (hx : ¬ IsCriticalPoint d g x) (y : E d) :
    (regularPointChart hg hx y).1 = g y :=
  regularPointChart_fst hg hx y

example (hg : IsSmooth d g) (hx : ¬ IsCriticalPoint d g x) :
    regularPointChart hg hx x = (g x, 0) :=
  regularPointChart_self hg hx

example (hg : IsSmooth d g) (hx : ¬ IsCriticalPoint d g x) :
    x ∈ (regularPointChart hg hx).source :=
  mem_regularPointChart_source hg hx

example (hg : IsSmooth d g) (hx : ¬ IsCriticalPoint d g x) :
    (g x, 0) ∈ (regularPointChart hg hx).target :=
  mem_regularPointChart_target hg hx

end UniversalLaw.Spec.Lifetime
