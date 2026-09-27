# ASCII note — `3e-2` means `3*e - 2`

**Object:** P15-ASCII-3E-MINUS-2-20260926-v1
**Scientific effect:** NONE. Does not reopen Theorem F. Additive clarification only.
**Source:** `PROOF.md` (F1) and (F11).

The proof writes `h_star=3-log(3e-2)` and `3-log(3e-2)=h_star`.
Intended reading: `3e-2 := 3*e - 2`.
Then `-log[3exp(-2)-2exp(-3)] = 3 - log(3*e - 2)` is an identity.

False reading `3e-2` as `3*exp(-2)` produces `5-log(3)`, which is not the constant used by (F3) or the tests.

Recommended ASCII: `h_star = 3 - log(3*e - 2)`.
`rho_star` and the 20-decimal window are unchanged.
Demand-one stays an obstruction.
