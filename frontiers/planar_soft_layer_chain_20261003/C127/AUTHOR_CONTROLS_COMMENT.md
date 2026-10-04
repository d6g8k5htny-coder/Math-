# C127 author finite controls and execution

Actual performer: OpenAI/Codex root session `01a0bbb5-2fcb-77f0-b78b-4d220ddd7ab2`, delegated by Dylan Roy. Author controls, not an independent review or analytic theorem proof. Organizational independence0.

Proof candidate: [5975032676](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5975032676). Claim WE748. Exact rational controls check finite polynomial identities, the single-normalizer power ledger and negative controls. No project master or Lean was executed for this proof-only object.

Execution: **525 finite checks in each of normal and optimized Python**, **10 named mutants rejected in each mode**, unknown mutant exits2 in each mode;24 invocations total. Every expected negative exits1 with the specific failed predicate, not a tool error. Raw commands/stdout/stderr are preserved for the single final archive. These results do not prove Gaussian conditioning, Kac–Rice, or the analytic theorem.

## CONTROL_DESIGN.md

2219 bytes; SHA-256 `8841f29129305f3e170e420e3e794686c0388db150b76cfad4b2854fab73d8b8`.

<!-- C127-CONTROL-BEGIN-CONTROL_DESIGN_md -->
````markdown
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
````
<!-- C127-CONTROL-END-CONTROL_DESIGN_md -->

## verify_controls.py

7276 bytes; SHA-256 `4a589f4cdd4de9b0c05f920385502148684ee4605a982457f52e30566678aeb1`.

<!-- C127-CONTROL-BEGIN-verify_controls_py -->
````python
#!/usr/bin/env python3
"""Finite exact controls for C127; this program does not prove its analytic theorem."""
import argparse
from fractions import Fraction as Q
import json
import sys

MUTANTS = (
    "pin_cubic_factor", "hermite_cubic_factor", "correction_missing_two",
    "conditional_dimension_three", "omit_slab_width", "double_normalizer",
    "omit_remote_determinant", "cutoff_sign", "raw_numerator_wrong_direction",
    "factorize_witness_events",
)
class Mismatch(Exception):
    pass

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mutant", choices=MUTANTS)
    args = parser.parse_args()
    checks = 0
    def need(value, label):
        nonlocal checks
        checks += 1
        if not value:
            raise Mismatch(label)

    # Sparse exact bivariate polynomials (t,z); differentiation then evaluation.
    def ev(poly, t, z, dt=0, dz=0):
        total = Q(0)
        for (i, j), c in poly.items():
            if i < dt or j < dz:
                continue
            for h in range(dt):
                c *= i-h
            for h in range(dz):
                c *= j-h
            total += c*t**(i-dt)*z**(j-dz)
        return total

    try:
        for r in map(Q, ("1/2", "1/17", "1/100003")):
            for seed in range(-4, 5):
                a = [Q(seed+i, i+1) for i in range(6)]
                poly = {
                    (0, 0): a[0]-r*r*a[2]/8,
                    (1, 0): a[1]-r*r*a[3]/24,
                    (2, 0): a[2]/2,
                    (3, 0): a[3]/(3 if args.mutant == "pin_cubic_factor" else 6),
                    (0, 1): a[4], (1, 1): a[5],
                }
                l, h = -r/2, r/2
                fl, fh = ev(poly,l,0), ev(poly,h,0)
                gl, gh = ev(poly,l,0,1), ev(poly,h,0,1)
                zl, zh = ev(poly,l,0,0,1), ev(poly,h,0,0,1)
                got = ((fl+fh)/2,(fh-fl)/r,(gh-gl)/r,
                       6*(gl+gh-2*(fh-fl)/r)/(r*r),(zl+zh)/2,(zh-zl)/r)
                for i in range(6):
                    need(got[i] == a[i], "actual pin right inverse coordinate %d" % i)

        for h in map(Q, ("1/3","1/101","1/1000007")):
            for s in range(-3,4):
                b = [Q(s+i, i+2) for i in range(6)]
                poly = {(0,0):b[0],(1,0):b[1],(2,0):b[2],(3,0):b[3],
                        (0,1):b[4],(1,1):b[5]}
                f0,fh=ev(poly,0,0),ev(poly,h,0)
                d0,dh=ev(poly,0,0,1),ev(poly,h,0,1)
                b2=3*(fh-f0)/h**2-(2*d0+dh)/h
                factor=3 if args.mutant=="hermite_cubic_factor" else 2
                b3=(dh+d0)/h**2-factor*(fh-f0)/h**3
                c1=(ev(poly,h,0,0,1)-ev(poly,0,0,0,1))/h
                need(b2==b[2], "Hermite quadratic coefficient")
                need(b3==b[3], "Hermite cubic coefficient")
                need(c1==b[5], "Hermite mixed coefficient")

        # Product rule at ell(0)=0, with arbitrary q derivatives.
        for q0 in map(Q, ("1/7","1","5")):
            for q1 in map(Q, ("-3","0","11/3")):
                for q2 in map(Q, ("-2","4")):
                    for ell1 in map(Q, ("-1","1/2","2")):
                        ell2=Q(7,3)
                        q=[q0,q1,q2]
                        ell=[Q(0),ell1,ell2]
                        square=[sum((ell[i]*ell[k-i] for i in range(3)
                                     if 0<=k-i<3),Q(0)) for k in range(5)]
                        coefficient=sum((q[i]*square[2-i] for i in range(3)),Q(0))
                        derivative=2*coefficient
                        factor=1 if args.mutant=="correction_missing_two" else 2
                        need(derivative==factor*q0*ell1**2,
                             "finite-r quadratic correction includes factor two")
        need(1-Q(1,64)**2/6>Q(1,2), "sinc lower bound margin")
        need(4+1==5 and 1+2==3 and 1+3==4, "fixed frequency degrees")
        need(5+2==7 and 2*4+1==9, "Fourier dual losses")
        covariance_floor=2*9
        dimension=3 if args.mutant=="conditional_dimension_three" else 4
        density_loss=Q(covariance_floor*dimension,2)
        need(density_loss==36, "four-dimensional conditional density")

        # Exponent tuples: (r,T,rho), computed from the separate factors.
        endpoint=(Q(4),Q(6),Q(0))
        remote=(Q(0),Q(0 if args.mutant=="omit_remote_determinant" else 2),Q(0))
        slab=(Q(0),Q(0),Q(0)) if args.mutant=="omit_slab_width" else (Q(1),Q(2),Q(0))
        height=(Q(3),Q(0),Q(0))
        normalizer=(Q(-4 if args.mutant=="double_normalizer" else -2),Q(0),Q(0))
        density=(Q(0),Q(0),-density_loss)
        event=tuple(sum(v[i] for v in (endpoint,remote,slab,height,normalizer,density))
                    for i in range(3))
        need(event==(6,10,-36), "weighted event has one full normalizer and every factor")
        counted=(Q(3,2)+event[0]/2,event[1]/2,event[2]/2)
        need(counted==(Q(9,2),5,-18), "CS also includes ordinary count moment")
        rho_power=Q(1,100)
        norm_power=Q(1 if args.mutant=="cutoff_sign" else -1,100)
        evaluate=lambda powers: powers[0]+norm_power*powers[1]+rho_power*powers[2]
        need(evaluate(event)==Q(277,50), "moving-cutoff event power")
        result=evaluate(counted)
        need(result==Q(427,100), "counted mixed power")
        need(-600*norm_power==6, "event tail moment600")
        need(Q(3,2)-300*norm_power==Q(9,2), "counted tail power")
        numerator=result+(-2 if args.mutant=="raw_numerator_wrong_direction" else 2)
        need(numerator==Q(627,100), "return to original numerator multiplies by Z")
        need(result>4 and numerator>6, "strict margins")

        # Independent integer raw/factorial moment identity.
        stirling=[[1]]
        for q in range(1,11):
            prev=stirling[-1]
            row=[0]*(q+1)
            for j in range(1,q+1):
                row[j]=(prev[j-1] if j-1<len(prev) else 0)+(j*prev[j] if j<len(prev) else 0)
            stirling.append(row)
            for n in range(21):
                falling=1
                value=0
                for j in range(1,q+1):
                    falling*=n-j+1
                    value+=row[j]*falling
                need(value==n**q, "Stirling ordinary moment identity")

        for n in (2,3,5,11,101,1009):
            r=Q(1,n)
            mass=r**3
            joint=mass**2 if args.mutant=="factorize_witness_events" else mass
            need(joint==mass, "correlated regional countermodel")
            need(joint/r**4==n, "global moments do not imply regional r4")
            need(2*mass==Q(2)*r**3, "second factorial moment in countermodel")
            need(mass**2!=mass, "marginal multiplication is false")

    except Mismatch as exc:
        print(json.dumps({"status":"REJECTED","mutant":args.mutant,
                          "checks_before_rejection":checks,"reason":str(exc),
                          "analytic_theorem_proved_by_checks":False},sort_keys=True))
        return 1
    print(json.dumps({"status":"PASS_FINITE_CONTROLS","mutant":args.mutant,
                      "checks":checks,"exact_arithmetic":"fractions.Fraction",
                      "analytic_theorem_proved_by_checks":False},sort_keys=True))
    return 0

if __name__=="__main__":
    sys.exit(main())
````
<!-- C127-CONTROL-END-verify_controls_py -->
