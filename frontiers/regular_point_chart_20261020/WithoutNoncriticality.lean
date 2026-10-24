import RegularPointChart

namespace UniversalLaw.Spec.Lifetime

noncomputable section

variable {d : ℕ} {g : E d → ℝ} {x : E d}

-- This must be rejected: smoothness alone does not provide the required
-- `¬ IsCriticalPoint d g x` argument.
example (hg : IsSmooth d g) :
    OpenPartialHomeomorph (E d) (ℝ × (fderiv ℝ g x).ker) :=
  regularPointChart hg

end

end UniversalLaw.Spec.Lifetime
