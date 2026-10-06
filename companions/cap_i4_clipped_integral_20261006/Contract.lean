import CapI4ClippedIntegral
open MeasureTheory Set
open scoped ENNReal

example (a b T : ℝ) :
    (∫ x in (0 : ℝ)..a, x*(x+b)*(T-x)) =
      T*a^3/3 + T*b*a^2/2 - a^4/4 - b*a^3/3 :=
  CapI4ClippedIntegral.gap_integral_exact a b T

example (T L b : ℝ) (hT : 0 ≤ T) (hL : 0 ≤ L) (hb : 0 ≤ b) :
    0 ≤ ∫ x in (0 : ℝ)..min T L, x*(x+b)*(T-x) :=
  CapI4ClippedIntegral.clipped_integral_nonneg T L b hT hL hb

example (T L b : ℝ) (hT : 0 ≤ T) (hL : 0 ≤ L) (hb : 0 ≤ b) :
    (∫ x in (0 : ℝ)..min T L, x*(x+b)*(T-x)) ≤
      T*(L^3/3+b*L^2/2) :=
  CapI4ClippedIntegral.clipped_integral_le T L b hT hL hb

example (T b : ℝ) :
    (∫ x in (0 : ℝ)..T, x*(x+b)*(T-x)) = T^4/12+b*T^3/6 :=
  CapI4ClippedIntegral.full_chamber_integral T b

example (A T r D E U : ℝ) (hA : 0 ≤ A) (hT : 0 ≤ T)
    (hr : 0 ≤ r) (hD : 0 ≤ D) (hE : 0 ≤ E) (hU : 0 ≤ U) :
    A*r^2*T*U^3*(∫ x in (0 : ℝ)..min T (D*r*U^2),
      x*(x+E*r*U)*(T-x)) ≤
      A*r^5*T^2*((D^3/3)*U^9+(E*D^2/2)*U^8) :=
  CapI4ClippedIntegral.moving_prefactor_le A T r D E U hA hT hr hD hE hU

example (T L b : ℝ) (hT : 0 ≤ T) (hL : 0 ≤ L) (hb : 0 ≤ b) :
    (∫⁻ x : ℝ in Ioc 0 (min T L), ENNReal.ofReal (x*(x+b)*(T-x))) =
      ENNReal.ofReal (T*(min T L)^3/3+T*b*(min T L)^2/2-
        (min T L)^4/4-b*(min T L)^3/3) :=
  CapI4ClippedIntegral.clipped_lintegral_eq T L b hT hL hb
