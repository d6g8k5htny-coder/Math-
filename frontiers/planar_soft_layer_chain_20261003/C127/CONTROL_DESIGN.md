# C127 finite-control design — frozen before implementation

These are exact algebra/power/falsifier controls, not analytic theorem tests.
Use Python standard library Fractions only; checks remain enabled under -O.
Emit bounded JSON, nonzero exit for rejected mutations; unknown mutant exit2.

1. Pin polynomial F11: six rational targets at multiple rational r, exact
   value/gradient substitutions in F2, recovering all six targets.
2. Hermite endpoint system: an independent rational cubic plus mixed z
   polynomial, all six endpoint data, reconstructed b2,b3,c1; test very
   small rational node distance without floating point.
3. Product correction: expand q(t)ell(t)^2 to degree2 at ell(0)=0;
   verify transverse second derivative is 2q0ell1^2 regardless q derivatives.
4. Finite-angle lower bound: theta<=pi/256<1/64 and sinc>=1-theta²/6;
   rational lower 1-(1/64)^2/6>1/2. Analytic sine inequality remains in proof.
5. Frequency/dual/covariance/density bookkeeping: degrees4,3,5; costs7,9;
   squared cost18; conditional dimension4 gives density power36.
6. Original weighted event power ledger: endpoint r4T6, remote T2,
   A-slab rT2, height r3, divide FULL r2 once; event r6T10rho^-36.
   Half event plus raw moment r3 yields counted r^(9/2)T5rho^-18.
7. Exact cutoff powers rho=r^(1/100),T=r^(-1/100),m600:
   event277/50, tail6, counted427/100, counted tail9/2,
   original627/100. Check margins versus target4/raw6.
8. Exact Stirling identity for integer counts and degrees1..10.
9. Countermodel: N=2 with probability r3, both regional counts1 there;
   factorial moments O(r3) coexist with mixed r3 rather than r4.
   The sequence r=1/n has mixed/r4=n unbounded. Independence would
   incorrectly replace r3 by r6. This is not a Gaussian counterexample,
   but a falsifier of inference from moment bounds alone.

Named mutations: pin_cubic_factor, hermite_cubic_factor,
correction_missing_two, conditional_dimension_three, omit_slab_width,
double_normalizer, omit_remote_determinant, cutoff_sign,
raw_numerator_wrong_direction, factorize_witness_events.
Each must be rejected by a mathematically relevant exact check.
No random search, simulation, fitted exponent, proof parsing or theorem claim.
