/-!
# SIDE24 coefficient — exact arithmetic facts of `coefficients/side24_v1/PROOF.md`

Informal object: `SIDE24-COEFFICIENT-D23-20260924-v1` (author OpenAI / ChatGPT).
Formal object: `FORMAL-SIDE24-ARITH-20260927-v1` (author Cursor cloud agent,
Anthropic Claude model family; AI-authored, author-side until a distinct
reviewer accepts the alignment ledger).

Every theorem below is an exact integer or rational identity or inequality
that the informal proof uses as a step. Each doc string names the section and
display of `PROOF.md` it encodes. The kernel checks the arithmetic; it does
not check that the informal step was correctly transcribed. That is the
alignment lane (`formal/FORMALIZATION_STATUS.json`, `components[].informal`).

Not encoded here (needs real analysis; see the Mathlib package
`formal/lean/mathlib`): Gaussian conditioning, the Gamma(7/6) Stirling
remainder, the exponential/logarithm enclosures, the integral identity of
Section 1, and the periodic-versus-reference comparison (3)-(4) as statements
about real numbers. The displayed decimal enclosure of `c_{d,24}` is therefore
NOT a theorem of this file.

Scientific effect: NONE.
-/

namespace MathFormalCore.Side24

/-! ## Section 1 — reference coefficient with exact cone moments -/

/-- Section 1: `V = Hu` has covariance `diag(3,1,…,1)`, so `p_G(0) p_V(0)` carries the
factor `1/sqrt 3`; the determinant of that diagonal block in every dimension is `3`. -/
theorem vCov_det : 3 * 1 = 3 := by decide

/-- Section 1, `m = 1`: `A = Q + sqrt(2/3) Z`, `Var Q = 2`, so `Var A = 2 + 2/3 = 8/3`. -/
theorem varA_m1 : (2 : Rat) + 2 / 3 = 8 / 3 := by decide +kernel

/-- Section 1, `m = 1`: centered Gaussian symmetry gives `D_1 = E[A^2 1{A<0}] = (1/2) Var A = 4/3`. -/
theorem coneMoment_d2 : (1 / 2 : Rat) * (8 / 3) = 4 / 3 := by decide +kernel

/-- Section 1, `m = 2`: `Var s = 5/3` and Gaussian fourth moment `E s^4 = 3 (Var s)^2 = 25/3`. -/
theorem s_fourthMoment : 3 * (5 / 3 : Rat) ^ 2 = 25 / 3 := by decide +kernel

/-- Section 1, `m = 2`: `E s^4 - 4 E s^2 = 25/3 - 20/3`, the rational part of the
Rayleigh-integrated determinant moment before the exponential term. -/
theorem s_moment_combination : (25 / 3 : Rat) - 20 / 3 = 5 / 3 := by decide +kernel

/-- Section 1, `m = 2`: the rational part of `D_2 = (1/2)[25/3 - 20/3 + 8 - 8 sqrt(3/8)]` is `29/6`. -/
theorem coneMoment_d3_rational : (1 / 2 : Rat) * (25 / 3 - 20 / 3 + 8) = 29 / 6 := by
  decide +kernel

/-- Section 1, `m = 2`: `(1/2) * 8 * sqrt(3/8) = 4 sqrt(3/8) = sqrt 6` because `4^2 * 3/8 = 6`. -/
theorem coneMoment_d3_sqrt : (4 : Rat) ^ 2 * (3 / 8) = 6 := by decide +kernel

/-- Section 1, display (1): `6^(2/3) / 24^(1/3) = (3/2)^(1/3)` reduces to `6^2 / 24 = 3/2`. -/
theorem cubeRoot_simplification : (6 : Rat) ^ 2 / 24 = 3 / 2 := by decide +kernel

/-- Section 1: the untruncated half determinant-squared moment is `29/6`; the truncation
term `sqrt 6` is essential, so `D_2 < 29/6`; `sqrt 6 > 0` since `6 > 0`. -/
theorem truncation_positive : (0 : Rat) < 6 := by decide +kernel

/-! ## Section 2 — uniform bound for every omitted periodic image -/

/-- Section 2: pairing coefficients of the sixth derivative of `exp(-|x|^2/2)`:
`1 + 15 + 45 + 15 = 76`. -/
theorem pairingSum : 1 + 15 + 45 + 15 = 76 := by decide

/-- Section 2: `q! / (2^j j! (q-2j)!)` for `q = 6`, `j = 0,1,2,3` equals `1, 15, 45, 15`. -/
theorem pairingCoefficients :
    720 / (1 * 1 * 720) = 1 ∧ 720 / (2 * 1 * 24) = 15 ∧
    720 / (4 * 2 * 2) = 45 ∧ 720 / (8 * 6 * 1) = 15 := by decide

/-- Section 2: integer points with maximum coordinate magnitude `j` number at most
`27 j^3` for `d ≤ 3`, and `|n|^6 ≤ 27 j^6`; the product constant is `27 * 27 = 729`. -/
theorem cubeCount_constant : 27 * 27 = 729 := by decide

/-- Section 2: ratio-at-most-one-half geometric summation doubles the first term: `2 * 729 = 1458`. -/
theorem geometric_doubling : 2 * 729 = 1458 := by decide

/-- Section 2, display (2): the integer factor `1458 * (76 * 24^6 + 15)` of the image bound `E`. -/
def imageConstant : Nat := 1458 * (76 * 24 ^ 6 + 15)

/-- Section 2, display (2): `E = 21175738586478 * 10^(-125)`. -/
theorem imageConstant_eq : imageConstant = 21175738586478 := by decide

/-- Factorial, defined here because the core prelude does not export one. -/
def fact : Nat → Nat
  | 0 => 1
  | n + 1 => (n + 1) * fact n

/-- Exact rational Taylor partial sum `sum_{k=0}^{n} x^k / k!` of the exponential. -/
def taylorExp (x : Rat) : Nat → Rat
  | 0 => 1
  | n + 1 => taylorExp x n + x ^ (n + 1) / (fact (n + 1) : Rat)

/-- Section 2: "The code proves `e^(288/125) > 10` using the positive rational Taylor sum
through 20." This is that exact rational inequality. Transferring it to the real
exponential uses `sum_{k≤n} x^k/k! ≤ exp x` for `x ≥ 0`, a real-analysis interface
recorded in the alignment ledger rather than proved in this core-only package. -/
theorem taylorExp_288_125_gt_ten : (10 : Rat) < taylorExp (288 / 125) 20 := by decide +kernel

/-- Section 2: `e^(-288) < 10^(-125)` follows from `e^(288/125) > 10` because `288 = 125 * (288/125)`
and `10^125` is the 125th power; the exponent bookkeeping is `125 * 288 / 125 = 288`. -/
theorem exponent_bookkeeping : 125 * 288 / 125 = 288 := by decide

/-- Section 2: successive terms of `sum_j j^9 e^(-288 j^2)` have ratio at most `512 e^(-864)`:
`(j+1)^9 / j^9 ≤ 2^9 = 512` for `j ≥ 1`, and `288((j+1)^2 - j^2) ≥ 288 * 3 = 864`. -/
theorem ratio_constants : 2 ^ 9 = 512 ∧ 288 * 3 = 864 := by decide

/-! ## Section 3 — full joint covariance and all orientations -/

/-- Section 3: the joint vector `(G, t, svec H)` has dimension at most `d + 1 + d(d+1)/2 = 10`
for `d = 3`. -/
theorem jointDimension_d3 : 3 + 1 + 3 * (3 + 1) / 2 = 10 := by decide

/-- Section 3: each covariance entry differs by at most `2E`; a `10 x 10` matrix with entries
bounded by `2E` has spectral norm at most `10 * 2E = 20E`. -/
theorem spectralNorm_constant : 10 * 2 = 20 := by decide

/-- Section 3: the odd block `[[1,-3],[-3,15]]` has eigenvalues `8 ± sqrt 58`:
trace `16 = 2 * 8` and determinant `15 - 9 = 6 = 8^2 - 58`. -/
theorem oddBlock_traceDet : (1 : Int) + 15 = 2 * 8 ∧ (1 : Int) * 15 - (-3) * (-3) = 8 ^ 2 - 58 := by
  decide

/-- Section 3: subtracting `I/3` from the odd block leaves first principal minor `2/3`. -/
theorem oddBlock_shift_minor : (1 : Rat) - 1 / 3 = 2 / 3 := by decide +kernel

/-- Section 3: subtracting `I/3` from the odd block leaves determinant `7/9`. -/
theorem oddBlock_shift_det : ((1 : Rat) - 1 / 3) * (15 - 1 / 3) - (-3) * (-3) = 7 / 9 := by
  decide +kernel

/-- Section 3: the smaller eigenvalue `8 - sqrt 58` exceeds `1/3` iff `sqrt 58 < 23/3`
iff `58 < (23/3)^2`. -/
theorem fiftyEight_lt_sq : (58 : Rat) < (23 / 3) ^ 2 := by decide +kernel

/-- Section 3, display (3): `60 E < ε = 10^(-108)`, cleared of denominators. -/
theorem sixtyE_lt_eps : 60 * imageConstant * 10 ^ 108 < 10 ^ 125 := by decide

/-- Section 3: the factor `60` is `3 * 20`: spectral bound `20E` divided by `λ_min(C_ref) ≥ 1/3`. -/
theorem sixty_factor : 3 * 20 = 60 := by decide

/-! ## Section 4 — cone moments under covariance comparison -/

/-- Transverse dimension `m = d - 1`. -/
def m (d : Nat) : Nat := d - 1

/-- Number of independent symmetric-matrix coordinates `n = m(m+1)/2`. -/
def n (d : Nat) : Nat := m d * (m d + 1) / 2

/-- Section 4 exponent `a = m + 2/3 + n/2`. -/
def a (d : Nat) : Rat := (m d : Rat) + 2 / 3 + (n d : Rat) / 2

/-- Section 4 exponent `b = d + n/2`. -/
def b (d : Nat) : Rat := (d : Rat) + (n d : Rat) / 2

/-- Section 4: `a + 2b < 14` and `2a + b < 13` in dimension two. -/
theorem exponentBounds_d2 : a 2 + 2 * b 2 < 14 ∧ 2 * a 2 + b 2 < 13 := by decide +kernel

/-- Section 4: `a + 2b < 14` and `2a + b < 13` in dimension three. -/
theorem exponentBounds_d3 : a 3 + 2 * b 3 < 14 ∧ 2 * a 3 + b 3 < 13 := by decide +kernel

/-- Section 4: `ε = 10^(-108)` is far below `1/28`: `28 < 10^108`. -/
theorem eps_below_one_over_28 : 28 < 10 ^ 108 := by decide

/-- Section 4: the ratio lies between `1 - 13ε` and `1 + 28ε`, hence within `1 ± 32ε`. -/
theorem ratioBounds_within_32 : 13 ≤ 32 ∧ 28 ≤ 32 := by decide

/-- Section 4, display (4): `32 ε < 10^(-106)`, cleared of denominators. -/
theorem thirtyTwoEps_lt : 32 * 10 ^ 106 < 10 ^ 108 := by decide

/-! ## Section 5 — outward rational grid and displayed endpoints -/

/-- Section 5: the displayed 20-digit endpoints are consecutive multiples of `10^(-20)`
(upper minus lower is exactly one grid step), in both dimensions. -/
theorem displayedEndpoints_adjacent :
    7340691930603427104 - 7340691930603427103 = 1 ∧
    4177593184059834335 - 4177593184059834334 = 1 := by decide

/-- Section 5: the 80-digit outward grid is finer than the displayed 20-digit grid. -/
theorem outwardGrid_refines : 10 ^ 20 ∣ 10 ^ 80 := by decide

/-- Displayed lower endpoint, `d = 2` (PROOF.md scope paragraph, `ENCLOSURE.json`). -/
def lower2 : Rat := 7340691930603427103 / 10 ^ 20
/-- Displayed upper endpoint, `d = 2`. -/
def upper2 : Rat := 7340691930603427104 / 10 ^ 20
/-- Displayed lower endpoint, `d = 3`. -/
def lower3 : Rat := 4177593184059834334 / 10 ^ 20
/-- Displayed upper endpoint, `d = 3`. -/
def upper3 : Rat := 4177593184059834335 / 10 ^ 20

/-- Section 3, display (3): `ε = 10^(-108)`. -/
def eps : Rat := 1 / 10 ^ 108
/-- Section 4, display (4): relative periodization bound `10^(-106)`. -/
def relBound : Rat := 1 / 10 ^ 106

/-- Section 3-4 constants as rationals: `60 E < ε` and `32 ε < 10^(-106)`. -/
theorem constants_chain :
    60 * (imageConstant : Rat) / 10 ^ 125 < eps ∧ 32 * eps < relBound := by decide +kernel

/-! The four numbers below are the exact outward reference enclosures that
`coefficients/side24_v1/coefficient.py` (`reference_coefficient(d)`) returns on the
`10^(-80)` grid, transcribed as numerators over `10^80`. Their correctness as
enclosures of the real number `c_{d,ref}` is NOT proved in this package; it is the
Machin/atanh/Taylor/Stirling interval computation of Section 5. What IS kernel-checked
here is the final step of `side24_coefficient`: applying the relative bound (4) to these
endpoints stays inside the displayed 20-digit interval. -/

/-- Reference lower endpoint, `d = 2`, from `coefficient.py`. -/
def refLo2 : Rat :=
  7340691930603427103013596295776273618445946768885664197004403216711382893223557 / 10 ^ 80
/-- Reference upper endpoint, `d = 2`, from `coefficient.py`. -/
def refHi2 : Rat :=
  7340691930603427103013596295777417013380655703769646772200313740800240533333043 / 10 ^ 80
/-- Reference lower endpoint, `d = 3`, from `coefficient.py`. -/
def refLo3 : Rat :=
  4177593184059834334293666542856911775587214492195145252592066752648167407187767 / 10 ^ 80
/-- Reference upper endpoint, `d = 3`, from `coefficient.py`. -/
def refHi3 : Rat :=
  4177593184059834334293666542857562482486657407720240268849039889886922519700256 / 10 ^ 80

/-- The reference enclosures are proper positive intervals. -/
theorem refIntervals_ordered : 0 < refLo2 ∧ refLo2 ≤ refHi2 ∧ 0 < refLo3 ∧ refLo3 ≤ refHi3 := by
  decide +kernel

/-- Section 5, `d = 2`: `refLo2 (1 - 10^(-106)) ≥ lower2` and `refHi2 (1 + 10^(-106)) ≤ upper2`.
This is the exact "periodization allowance applied before final outward rounding" step. -/
theorem transfer_d2 : lower2 ≤ refLo2 * (1 - relBound) ∧ refHi2 * (1 + relBound) ≤ upper2 := by
  decide +kernel

/-- Section 5, `d = 3`: the same transfer step. -/
theorem transfer_d3 : lower3 ≤ refLo3 * (1 - relBound) ∧ refHi3 * (1 + relBound) ≤ upper3 := by
  decide +kernel

end MathFormalCore.Side24
