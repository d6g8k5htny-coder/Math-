"""Shared fixed contract, bounded parsing and custody; no numerical enclosure logic."""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import re
import time

HERE=Path(__file__).resolve().parent
PINS={'moment_kernel.py':'68c3caf28190e8be58464cabfc39ab565449d9bb64716ab139ac0dd0a181193e',
      'verify_certificate.py':'a0afbfdf9ca323db38e06171c138f683669c42fe99f6892d6233ab03802d4715'}
SOURCES={'method_v2':'8bdea4b42e9efd2d846cd1aa73691e8194fa26cd937ac02b79991334f88204f6',
         'original':'f38c085ab5b15368e6989a1fd6298490f3b671f5a6c3a01bcdc81b516022bc33'}
REQUEST={'d':2,'L':'24/1','goal':'1/100','gamma_cells':4096,
         'gamma_interval':['0/1','2/1'],'gamma_split':'1/1','root_bits':96,
         'max_seconds':180,'max_exp_calls':8192,'max_certificate_bytes':8388608,
         'kernel':{'L_lo':'24/1','L_hi':'24/1','cutoff':32,'bits':96,
                   'pi_terms':24,'exp_pairs':24,'width_goal':None,
                   'input_role':'UNASSIGNED_PARAMETER_INPUT',
                   'limits':{'max_work':100000,'max_seconds':3,
                             'max_rational_bits':8192,'max_squarings':16}}}
FILES=('coefficient.py','verify_coefficient.py','contract.py','moment_kernel.py',
       'verify_certificate.py','REQUEST.json','SOURCE_MAP.json','PROOF.md','test_coefficient.py','README.md')

def dumps(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False)

def strict_json(data):
    def pairs(items):
        out={}
        for k,v in items:
            if k in out:raise ValueError('DUPLICATE_JSON_KEY')
            out[k]=v
        return out
    def constant(s):raise ValueError('NONFINITE_JSON_CONSTANT')
    try:return json.loads(data,object_pairs_hook=pairs,parse_constant=constant)
    except (ValueError,UnicodeError,RecursionError) as e:raise ValueError('INVALID_JSON: '+type(e).__name__) from None

def check_request(r):
    if dumps(r)!=dumps(REQUEST):raise ValueError('FROZEN_REQUEST_MISMATCH')

def q(s):
    if not isinstance(s,str) or len(s)>3000 or not re.fullmatch(r'-?\d+/[1-9]\d*',s):raise ValueError('RATIONAL_SYNTAX')
    x=F(s)
    if text(x)!=s or max(x.numerator.bit_length(),x.denominator.bit_length())>8192:raise ValueError('RATIONAL_CANONICAL_OR_SIZE')
    return x

def text(x):return str(x.numerator)+'/'+str(x.denominator)
def pack(v):return [text(x) for x in v]

def interval(v):
    if not isinstance(v,list) or len(v)!=2:raise ValueError('INTERVAL_SHAPE')
    a,b=map(q,v)
    if a>b:raise ValueError('INTERVAL_ORDER')
    return a,b

def keys(x,names):
    if not isinstance(x,dict) or set(x)!=set(names):raise ValueError('SCHEMA_KEYS')

def source_identity():
    result={name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in FILES}
    if any(result[name]!=h for name,h in PINS.items()):raise ValueError('UPSTREAM_SOURCE_CHANGED')
    return result

class Budget:
    def __init__(self):self.start=time.monotonic();self.calls=0
    def tick(self,call=False):
        if call:self.calls+=1
        if self.calls>8192:raise ValueError('GAMMA_CALL_LIMIT')
        if time.monotonic()-self.start>180:raise ValueError('OUTER_TIME_LIMIT')
