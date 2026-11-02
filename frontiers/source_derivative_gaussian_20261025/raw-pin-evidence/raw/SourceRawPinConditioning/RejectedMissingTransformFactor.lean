import SourceRawPinConditioning

-- False regression identity when T*y is replaced by the untransformed target y.
example : ((2:ℝ)*3) * (1/(2*1*2)) * 5 = 3*(1/1)*5 := by
  norm_num
