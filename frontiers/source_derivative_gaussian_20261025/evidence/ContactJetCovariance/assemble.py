rank=open('/workspace/scratch/regression-kernel/contact-gram/RankProbe.lean').read()
gram=open('/workspace/scratch/regression-kernel/contact-gram/GramProbe.lean').read()
imports='''import Mathlib.LinearAlgebra.Matrix.PosDef
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Analysis.Normed.Ring.InfiniteSum
import Mathlib.Analysis.Normed.Module.FiniteDimension
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.Linarith

'''
header='''/-!
# Seven-mode certificate for contact-jet covariance

The row order is `(f, fx, fy, fxx, fxy, fxxx, fyy)`, with selected columns
`(DC, cos(1,0), cos(0,1), cos(1,1), sin(1,0), sin(2,0), sin(0,1))`.
Nonzero mode amplitudes are retained. The witness forces strict positivity of an
infinite coefficient Gram matrix by its sum-of-squares quadratic identity.

This is a coefficient certificate. Applying it to the literal smooth source requires
the exact derivative-coefficient identities and physical covariance identification;
these are not premises that may be silently omitted. See `SOURCE_CONTACT_GRAM.md`.
-/

open Matrix
open scoped BigOperators Matrix
set_option autoImplicit false

namespace I4ContactGram

'''
rankbody=rank[rank.index('def contactWitness'):rank.rindex('end I4ContactGram')]
grambody=gram[gram.index('noncomputable def coefficientGram'):gram.rindex('end I4ContactGram')]
final='''/-- Seven explicit independent mode columns force positivity of the entire infinite Gram sum.
No positive-definiteness or invertibility conclusion is an input premise. -/
theorem contact_coefficientGram_posDef {ι : Type*} (coeff : Fin 7 → ι → ℝ)
    (hcoeff : ∀ i, Summable (coeff i)) {c : ℝ} (hc : c ≠ 0)
    (mode : Fin 7 → ι) (a : Fin 7 → ℝ) (ha : ∀ s, a s ≠ 0)
    (hcolumns : ∀ i s, coeff i (mode s) = a s * contactWitness c i s) :
    (coefficientGram coeff).PosDef := by
  apply coefficientGram_posDef_of_separating coeff hcoeff
  intro z hz
  classical
  by_cases hex : ∃ m, (∑ i, z i * coeff i m) ≠ 0
  · exact hex
  · exfalso
    apply hz
    apply contactWitness_amplitude_transpose_injective hc a ha
    rw [Matrix.mulVec_zero]
    funext s
    have hm : (∑ i, z i * coeff i (mode s)) = 0 :=
      not_ne_iff.mp (not_exists.mp hex (mode s))
    simp_rw [hcolumns] at hm
    simpa [Matrix.mulVec, dotProduct, Matrix.mul_diagonal, mul_comm, mul_left_comm,
      mul_assoc] using hm

'''
schur=open('/workspace/scratch/regression-kernel/contact-schur/SchurProbe.lean').read()
schurbody=schur[schur.index('theorem block_posDef'):schur.rindex('end ContactSchurProbe')]
schurbody=schurbody.replace('theorem block_posDef_schur_pos', '''/-- A positive-definite six-plus-one block covariance has strictly positive scalar Schur complement. -/
theorem contact_schur_pos''',1)
open('ContactJetCovariance.lean','w').write(imports+header+rankbody+grambody+final+schurbody+'\nend I4ContactGram\n')
