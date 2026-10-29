import RegularLocalCollarControls

example : RegularLocalCollarControls.omittedNonzeroDerivativeMutation := by
  rw [show RegularLocalCollarControls.omittedNonzeroDerivativeMutation = False from
    propext (iff_false_intro
      RegularLocalCollarControls.not_omittedNonzeroDerivativeMutation)]
