import SourcePinPreservingQuartic
open I4ActualQuarticTransfer
-- A quartic gradient component has nonzero fourth derivative. Omitting its
-- genuine fifth-field-derivative majorant cannot justify a zero remainder.
example : |(2:ℝ)^4-scalarTaylor (fun t : ℝ => t^4) 3 2| ≤ (0:ℝ)*2^4/24 := by
  rw [scalarTaylor_three]
  norm_num [iteratedDeriv_pow,deriv_pow_field]
