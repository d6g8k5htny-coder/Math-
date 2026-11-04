import IntrinsicH0Controls

open I4SourceIntrinsicH0Interface IntrinsicH0Controls

/- Sole mutation: unguard arbitrary supplied-interface death comparison.
The separately passed controls supply a valid shifted interface, constant7,
and the concrete essential death values17 and0. -/
theorem mutated_unguarded_essential_death :
    essentialShiftInterface.deathHeight constantSeven 0 =
      (h0Interface 1 2).deathHeight constantSeven 0 := by
  norm_num only [shifted_constant_death, intrinsic_constant_death]
