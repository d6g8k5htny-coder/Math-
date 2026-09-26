# Reduced leftover 4-slot after six pins (planar BF)

**Object:** ND-REDUCED-4SLOT-20260926
**Warrant:** PROVEN finite-dimensional Gaussian identities on planar BF.
**Scientific effect:** NONE. Table 4.1 ABSENT. Theorem B remains PROVEN-MODULO repaired ND.

## Amendment to Var(L)=15/4

Unconditional Var(f_sss)=15, so Var(L)=Var(f_sss/2)=15/4.
That number is **not** the six-pin law.

Same-point identities:
- Cov(f_sss, f_s) = -3
- Cov(f_sss, f) = Cov(f_sss, f_t) = Cov(f_sss, f_tt) = Cov(f_sss, f_ts) = Cov(f_sss, f_ss) = 0
- Cov(f_sss(M), f_s(S)) = -3 exp(-r^2/2)

Schur of f_sss(M) against the pair (f_s(M), f_s(S)):
Kpp = [[1, E],[E, 1]], E=e^{-r^2/2}, Ktp = [-3, -3E].
Kpp^{-1} Ktp^T = [-3, 0]^T, hence the quadratic form is 9 for every r.
Therefore

    Var(f_sss(M) | six pins) = 15 - 9 = 6

identically in r. The far pin is collinear with the near pin in this covariance, so it does not change the variance. Hence

    Var(L | six pins) = 3/2

identically, not 15/4.

Companion cubic slot at M:
Cov(f_tss, f_t) = -1, and f_tss is orthogonal to both f_s pins (He_1(0)=0).
So Var(f_tss(M) | six pins) = 3 - 1 = 2 identically.
Joint Gram of (f_sss, f_tss) after six pins is diag(6, 2).

## 4-slot Gram at M after six pins

Coordinates (f_tt, f_ts, f_ss, L) given the six pins:

    diag ~ (r^4/6, r^2/2, 2, 3/2)

All four eigenvalues are strictly positive at every tested r>0.
Product scales as det = Theta(r^6) as r	o0 (two soft slots).
Measured: r=0.17 det=6.0e-6; r=0.30 det=1.76e-4; r=1 det=0.171.

## Off-axis test point X=M+z after six pins

Same 4-slot at X. For |z_s|>0 the minimum eigenvalue is larger than the on-axis value at the same |z_t|.
At r=0.3, z=(0,0.15): det=6.15e-3, min eig=1.85e-2.
On-axis z_s=0 between M and S the min eig can be 10^{-5} but stays positive.

Honest reduced frame:
- off-axis: keep (f_tt, f_ts, f_ss, L) with L-variance 3/2 at a pin and O(1) off-axis
- on-axis: drop the cubic W-block (Euler + slaving), as previously written

The 15-determinant of the unreduced frame remains identically zero. That refutation is unchanged.

## Table 4.1 / File-3 15-matrix

ABSENT on Math- and main default (no "Table 4.1", no "Condition (ND)", no "15-frame" hits).
Do not invent a 13x13 certificate of an unpublished matrix.
