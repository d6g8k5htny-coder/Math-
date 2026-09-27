# Pin-compatible thin-tube candidate

Read `PROOF.md`. This is an author-side d=2 Gaussian count candidate on the physical domain `(r*u,r^2*v)`, fixed `A<=|u|<=B`, `|v|<=K`, `A>1`, compact positive gap marks and fixed torus. It is not full RN/annulus closure.

The proposed bound is `E_QW N_j(T_r) <= C*r^-10*exp(-c/r^2)` for ALL heights. The main idea is a nondegenerate **two-component** residual gradient at scales `(r^3,r^2)` confronting a target of size `1/r`. All three Hessians remain in the weighted Kac-Rice expression. The full endpoint-only normalizer is divided out once.

Run from this directory, with Python standard library only:

```sh
python -B -S -m unittest -v
python -B -O -S -m unittest -v
python -B -S thin_tube.py
```

15 distinct test methods check exact polynomial identities on all45 monomials of degree<=8, six-pin completion, contact rows, a rank minor, a NONPERIODIC reference Schur complement, and deliberate bad variants. These tests do not constitute an analytic or proof-assistant verification of the candidate. No scientific status is changed. Review questions R1--R8 are at the end of the proof.
