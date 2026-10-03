"""C103 author controls; explicit checks stay active under Python -O."""
from fractions import Fraction as F
import argparse
import subprocess
import sys

COUNT = 0


def require(ok, message):
    global COUNT
    COUNT += 1
    if not ok:
        raise RuntimeError(message)


def equal(got, wanted, name):
    require(got == wanted, f"{name}: got {got}, expected {wanted}")


def det(matrix):
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def filtered(matrix, index):
    value = det(matrix)
    if index == 1:
        return max(-value, F(0))
    return value if matrix[0][0] < 0 and value > 0 else F(0)


MUTANTS = (
    "cutoff", "jet-jacobian", "determinant-k4", "normalizer",
    "one-margin", "square-torus", "double-count", "discard-correlation",
)


def positive_checks(mutant=None):
    a, u, beta = F(1, 12), F(1, 32), F(1, 4)
    if mutant == "cutoff":
        a = F(1, 11)
    e = 1 - 4 * u
    admissibility = (1-a, 1-u, e, e-2*a, e-3*a, 1-2*u, beta)
    require(all(x > 0 for x in admissibility), "admissibility")
    powers = (8*u, 1-3*a+4*u, e-4*a, 1-5*a+e/2,
              2*e/3-4*a, 1-5*a+e/3, beta, 1-4*a,
              -3*a+2*(e-beta), 2-5*a-4*u, 2-7*a-2*u, 3*a, F(1))
    expected = (F(1,4), F(7,8), F(13,24), F(49,48), F(1,4),
                F(7,8), F(1,4), F(2,3), F(1), F(35,24),
                F(65,48), F(1,4), F(1))
    for got, wanted in zip(powers, expected):
        equal(got, wanted, "cutoff power")
    equal(min(powers), beta, "minimum power")
    equal(5 - (0 if mutant == "normalizer" else 2) - 3, 0,
          "actual rare scalar/full normalizer ledger")
    equal(6-2-3, 1, "scaled far exception")

    # C102's Taylor constants specialize exactly to C91's k=1 constants.
    equal(F(9,64)+F(1,16)+F(2)**4/24, F(167,192), "K0 at k=1")
    equal(F(33,128)+F(1,16)+F(2)**3/6, F(635,384), "K1 at k=1")
    equal(F(17,48)+F(1,24)+F(2)**2/2, F(115,48), "K2 at k=1")

    for k in (F(1,3), F(1,2), F(1), F(2), F(3)):
        for r in (F(1,20), F(1,7)):
            jac = (r/k) * (1/k) * (1/k**2)
            if mutant == "jet-jacobian":
                jac = r
            equal(jac/r, k**-4, "physical jet Jacobian")
        for lam in (F(-1), F(0), F(1,4), F(1), F(3)):
            for gamma in (F(-2), F(0), F(1), F(3)):
                for B in (F(-2), F(0), F(1), F(4)):
                    M = ((F(-6), -gamma/2), (-gamma/2, -lam-B/2))
                    S = ((F(6), gamma/2), (gamma/2, -lam+B/2))
                    hM = 6*lam+3*B-gamma**2/4
                    hS = 6*lam-3*B+gamma**2/4
                    weight = max(hM,F(0))*max(hS,F(0))
                    equal(filtered(M,2)*filtered(S,1), weight, "filtered model weight")
                    require(weight <= 36*max(lam,F(0))**2, "quadratic weight")
                    # H/r=k D_k^-1 L D_k^-1; det cancels exactly.
                    HM = ((k*M[0][0],M[0][1]),(M[1][0],M[1][1]/k))
                    HS = ((k*S[0][0],S[0][1]),(S[1][0],S[1][1]/k))
                    physical_weight = filtered(HM,2)*filtered(HS,1)
                    if mutant == "determinant-k4":
                        physical_weight *= k**4
                    equal(physical_weight,weight,"no additional determinant k4")
                    # CUB shear and sector-bound k cancellation.
                    for C in (F(-1),F(0),F(2)):
                        D = gamma**2-12*B
                        J = 8*gamma**3-144*B*gamma+576*C
                        Bsh = B/k-gamma**2/(12*k)
                        Dsh = (C/k**2-gamma*(B/k)/(4*k)+gamma**3/(72*k**2))/2
                        equal(Bsh,-D/(12*k),"CUB B shear")
                        equal(Dsh,J/(1152*k**2),"CUB D shear")
                        equal(48*k**4*Dsh**2,48*J**2/1152**2,"cubic-root k cancellation")

    # Exact strip substitutions and polynomial integration identities.
    for lam in (F(1,4),F(1),F(5)):
        for gamma in (F(-2),F(0),F(3)):
            for s in (F(0),12*lam,24*lam,48*lam):
                BM=(s-24*lam+gamma**2)/12
                BS=(24*lam+gamma**2-s)/12
                equal(24*lam-gamma**2+12*BM,s,"maximum edge substitution")
                equal(24*lam+gamma**2-12*BS,s,"saddle edge substitution")
                equal(s*(48*lam-s)/16,
                      (6*lam+3*BM-gamma**2/4)*(6*lam-3*BM+gamma**2/4),
                      "edge weight")

    # Whole-chord margins: min is -h and doubled endpoint is 4h.
    h=F(1,16); mu=1-h
    for t in (F(0),F(1,4),F(1,2),F(1),F(3,2),F(2)):
        q=h*(2*t**3-3*t**2)
        require(q>=-h,"chord minimum")
    equal(h*(2*F(2)**3-3*F(2)**2),4*h,"chord endpoint")
    unsafe_error=F(1,2)
    criterion = unsafe_error < (mu if mutant == "one-margin" else min(mu,4*h))
    require(not criterion,"one margin cannot certify endpoint above birth")

    # A transformed torus uses inverse-image lattice, not original lattice.
    # L=3,r=1/4,k=2,R=identity: inverse lattice generators are (12,0),(0,6).
    lattice=((F(12),F(0)),(F(0),F(6)))
    if mutant=="square-torus":
        lattice=((F(3),F(0)),(F(0),F(3)))
    for y,wanted in zip(lattice,((F(3),F(0)),(F(0),F(3)))):
        image=(F(1,4)*y[0],F(1,4)*F(2)*y[1])
        equal(image,wanted,"inverse-image lattice transport")

    alpha1,alpha2=F(2),F(3)
    failure_mass=alpha1+(2 if mutant=="double-count" else 1)*alpha2
    equal(failure_mass,F(5),"one indicator per failure")

    # Correlated positive weights cannot be replaced by independent moments.
    # Two equiprobable outcomes (W,N)=(1,1),(3,3).
    actual=F(1,2)*1*1+F(1,2)*3*3
    used=F(2)*F(2) if mutant=="discard-correlation" else actual
    equal(used,F(5),"joint weighted moment retained")


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--mutant",choices=MUTANTS)
    args=parser.parse_args()
    positive_checks(args.mutant)
    if args.mutant:
        raise RuntimeError("mutant unexpectedly reached completion")
    # Actual mutated replays in both modes; every rejection must be an explicit
    # RuntimeError from the intended invariant, not an assert or syntax error.
    for flags in ([],["-O"]):
        for name in MUTANTS:
            result=subprocess.run([sys.executable,*flags,__file__,"--mutant",name],
                                  capture_output=True,text=True)
            require(result.returncode!=0 and "RuntimeError:" in result.stderr,
                    f"mutant survived {flags} {name}")
            require("mutant unexpectedly" not in result.stderr,
                    f"mutant was not caught by invariant: {name}")
    print("C103 author rational controls PASS")
    print(f"explicit_checks={COUNT}; mutants=8; mutant_modes=normal,-O")
    print("cutoff_minimum=1/4; near_scaled=0; far_scaled=1; jet_Jacobian=k^-4")
    print("retained=two_margins,original_joint_weight,inverse_image_torus_lattice")
    print("scope=finite_exact_controls_not_analytic_or_human_acceptance")


if __name__=="__main__":
    main()
