import QuoClosedSuperlevelAdapter

/-!
UNEXECUTED NEGATIVE FIXTURE. Expected to fail elaboration at the final `exact`.
This checks that the public adapter still requires the Euclidean closed-level
LPC input. Failure caused by a missing import, environment fault, resource cap,
or any unrelated error does not count as the expected negative result.
This fixture is outside the candidate module and must not be imported by it.
It is an interface premise-omission check, not a mathematical counterexample
to a possible future theorem that derives Euclidean LPC from stronger inputs.
-/

noncomputable section

open Set Topology
open UniversalLaw.Spec.Lifetime TorusFiltration TorusMorseFinite
open TorusCriticalAttainment
open TorusCriticalAttainment.QuotientSuperlevelAdapter

-- There is deliberately no hEuclideanLPC argument or corresponding instance.
example (d : ℕ) (L : ℝ) (hL : 0 < L)
    (g : E d → ℝ) (hperiodic : IsLPeriodic d L g) (a : ℝ) :
    LocallyPathConnectedSpace
      {q : torus_quotient d L hL // a ≤ descendedHeight d L hL g hperiodic q} := by
  exact quotient_closedSuperlevel_lpc_of_euclidean d L hL g hperiodic a
