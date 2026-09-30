#!/usr/bin/env python3
"""Exact finite probability bookkeeping; not a Gaussian-model simulation."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
FROZEN = '3c69e20a332457211b8b1182a4819ce9b1dda824801f3a90157751f41b8fedf8'

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

require(hashlib.sha256((HERE/'PROOF.md').read_bytes()).hexdigest() == FROZEN, 'frozen proof changed')
cases = 0
for t,a,lam,q,k in product([F(1,100),F(1,1000)],[F(1,3),F(3,4)],[F(1,4),F(2,3)],[1,2,3],[F(1,3),F(2)]):
    # Four abstract atoms: success X=1, ordinary failure X=lam,
    # rare finite long lifetime X=2, essential X=infinity.
    # t represents r^3 for the algebra. These probabilities are finite
    # normalization fixtures, not realizations or tail rates of the model.
    failure = a*t
    essential, long = t**3, t**4
    ordinary = failure-essential-long
    success = 1-failure
    require(min(ordinary,essential,long,success) > 0, 'positive atom probabilities')
    require(ordinary+essential+long+success == 1, 'full probability normalization')
    finite_moment = success + ordinary*lam**q + long*2**q
    clipped_moment = success + ordinary*lam**q + long + essential
    genuine_loss = ordinary*(1-lam**q)
    signed_deficit = ordinary*(1-lam**q) + long*(1-2**q)
    coefficient = a*(1-lam**q)
    remainder = -essential*lam**q + long*(2**q-lam**q)
    require(finite_moment == 1-coefficient*t+remainder, 'success/failure moment decomposition')
    require(genuine_loss == 1-clipped_moment, 'bounded actual loss')
    require(signed_deficit == 1-essential-finite_moment, 'finite signed deficit')
    require(genuine_loss-signed_deficit == long*(2**q-1), 'rare long-tail sign retained')
    conditional = finite_moment/(1-essential)
    require(conditional-(1-coefficient*t) == (remainder+essential*(1-coefficient*t))/(1-essential), 'finite-conditioning denominator')
    physical_moment = success*(k*t)**q + ordinary*(k*t*lam)**q + long*(2*k*t)**q
    require(physical_moment == (k*t)**q*finite_moment, 'physical lifetime power scaling')
    cases += 1

print(json.dumps({
    'status':'PASS',
    'rational_probability_cases':cases,
    'scope':'Finite normalization, clipped versus signed loss, and deterministic physical scaling only; analytic premises and model-realized probabilities are not tested.',
    'frozen_proof_sha256':FROZEN,
    'loss_corollary_sha256':hashlib.sha256((HERE/'LOSS_COROLLARY.md').read_bytes()).hexdigest(),
    'runner_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
},indent=2,sort_keys=True))
