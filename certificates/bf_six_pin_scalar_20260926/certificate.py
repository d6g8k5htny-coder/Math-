"""Exact arithmetic for the scalar bound proved in PROOF.md.

This checks the finite arithmetic and scope, not the Gaussian-regression theorem
or the infinite-series proof. It does not execute sources, use floats, or award
scientific status. Python 3.11+, standard library only.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
import json
from math import factorial
from pathlib import Path
import re
import sys

HEADER = {
    "schema": 1,
    "model": "unperiodized planar Bargmann-Fock; covariance exp(-|x-y|^2/2)",
    "dimension": 2,
    "conditioning": "linear values (f,f_t,f_s) at M=(0,0), S=(r,0)",
    "quantity": "Var(f_ts(M) | six linear pins) / r^2",
    "coverage": "all real radii in the displayed interval; relies on the written analytic proof",
    "analytic_dependency": "PROOF.md Sections 1-3: Gaussian regression and all-order series inequalities",
    "scientific_effect": "NONE",
    "review": "REVIEW_REQUIRED",
    "formal_kernel_checked": False,
}


def rational(text: str) -> F:
    if not isinstance(text, str) or not re.fullmatch(r"-?(0|[1-9][0-9]*)(/[1-9][0-9]*)?", text):
        raise ValueError("canonical rational string required")
    value = F(text)
    if str(value) != text:
        raise ValueError("canonical rational string required")
    return value


def uniform_bounds(radius: str) -> tuple[F, F]:
    r = rational(radius)
    if not 0 < r < 1:
        raise ValueError("radius must lie strictly between zero and one")
    return (1-r*r)/2, F(1,2)


def certificate(radius: str = "1/40") -> dict:
    lower, upper = uniform_bounds(radius)
    return dict(HEADER, radius={"lower":"0", "lower_open":True, "upper":radius},
                normalized_variance={"lower":str(lower), "upper":str(upper)})


def validate(data: dict) -> dict:
    if not isinstance(data, dict) or set(data) != set(HEADER) | {"radius", "normalized_variance"}:
        raise ValueError("unexpected or missing certificate fields")
    for key, value in HEADER.items():
        if type(data[key]) is not type(value) or data[key] != value:
            raise ValueError("scope or evidence declaration changed: " + key)
    radius = data["radius"]
    if not isinstance(radius,dict) or set(radius) != {"lower","lower_open","upper"}:
        raise ValueError("invalid radius fields")
    if radius["lower"] != "0" or radius["lower_open"] is not True:
        raise ValueError("zero radius must be excluded")
    lower, upper = uniform_bounds(radius["upper"])
    bound = data["normalized_variance"]
    if not isinstance(bound,dict) or set(bound) != {"lower","upper"}:
        raise ValueError("invalid bound fields")
    declared_lo, declared_hi = rational(bound["lower"]), rational(bound["upper"])
    if declared_lo > lower:
        raise ValueError("lower endpoint exceeds the proved uniform lower bound")
    if declared_hi < upper:
        raise ValueError("upper endpoint is below the proved uniform upper bound")
    if declared_lo > declared_hi:
        raise ValueError("reversed interval")
    return data


def upper_slack_coefficient(n: int) -> F:
    """Coefficient of x^n in x(e^x-1)/2 - (e^x-1-x), n>=3.

    The formula's positivity for every n>=3 is proved in PROOF.md; a loop over
    finitely many n does not establish the infinite-series argument.
    """
    if type(n) is not int or n < 3:
        raise ValueError("integer n>=3 required")
    return F(n-2, 2*factorial(n))


def schur_identity() -> bool:
    """Exact polynomial checks in formal variables r,c, not numerical samples."""
    def add(a,b):
        out=dict(a)
        for key,value in b.items(): out[key]=out.get(key,0)+value
        return {k:v for k,v in out.items() if v}
    def mul(a,b):
        out={}
        for (i,j),v in a.items():
            for (k,l),w in b.items():
                key=(i+k,j+l);out[key]=out.get(key,0)+v*w
        return {k:v for k,v in out.items() if v}
    one={(0,0):1}; c={(0,1):1}; minus_c={(0,1):-1}; zero={}
    gram=[[one,c],[c,one]];adj=[[one,minus_c],[minus_c,one]]
    det={(0,0):1,(0,2):-1}
    for i in range(2):
        for j in range(2):
            product=add(mul(gram[i][0],adj[0][j]),mul(gram[i][1],adj[1][j]))
            if product != (det if i==j else zero): return False
    cross=[zero,{(1,1):1}]
    quadratic={}
    for i in range(2):
        for j in range(2): quadratic=add(quadratic,mul(mul(cross[i],adj[i][j]),cross[j]))
    return quadratic == {(2,2):1}


def strict_json(text: str) -> dict:
    def object_pairs(pairs):
        out={}
        for k,v in pairs:
            if k in out: raise ValueError("duplicate JSON key: "+k)
            out[k]=v
        return out
    def reject_constant(value): raise ValueError("non-finite JSON constant: "+value)
    return json.loads(text,object_pairs_hook=object_pairs,parse_constant=reject_constant)


def main(argv=None) -> int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--radius",default="1/40")
    p.add_argument("--check",type=Path)
    args=p.parse_args(argv)
    try:
        if args.check:
            if args.check.stat().st_size>65536: raise ValueError("certificate too large")
            data=validate(strict_json(args.check.read_text(encoding="utf-8")))
        else: data=validate(certificate(args.radius))
        if not schur_identity(): raise ValueError("Schur polynomial identity failed")
        print(json.dumps(data,indent=2,sort_keys=True))
        return 0
    except (ValueError,TypeError,OSError) as exc:
        print("REFUSED: "+str(exc),file=sys.stderr)
        return 1

if __name__ == "__main__": raise SystemExit(main())
