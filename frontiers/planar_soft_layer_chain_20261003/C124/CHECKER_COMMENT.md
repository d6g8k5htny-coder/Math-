## C124 nonauthor review: independently designed executable controls

Dylan Roy — delegated AI review. Actual reviewer/control author: OpenAI/Codex c99_custody_audit; root publishes the frozen bytes. Full analytic review: [5974327730](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5974327730). These controls were frozen before execution and the C124 author checker/output remained unopened. Prior source exposure and organizational independence 0 are disclosed in that review. The finite controls do not prove the analytic source theorems.

Extraction: each file is the exact text within its five-backtick fence, including its final LF. independent_controls.py: 8,759B SHA256 1d77a571133c7803704ee5e0c0dfd5f13bb0d33249748b09291205646d2c2cdc; DESIGN.md: 3,213B SHA256 457b7a19db5ae1a9ee7dc24e08f4b277d4493d36787c9bb7d84747a3e49c0bdb; baseline stdout: 255B SHA256 988e0f97d1a4cda0cd92c01800991d5cbd89b84e6eaa6349e477ee75b7faf25e.

Python3.11.16, both `-B -S` and `-O -B -S`: baseline601checks/0failures. Each positional mutation GAMMA_POWER, UNWEIGHTED_BAND, DIAGONAL_RESIDUAL, UNCENTERED_RESIDUAL, UNSAFE_EPSILON, FACTOR_TAIL, NORMALIZER_POWER, H_SCHEDULE exited1 in both modes; UNKNOWN exited2. Twenty invocations and forty transcripts are bound by the immutable review evidence seal.

### independent_controls.py
`````python
#!/usr/bin/env python3
"""C124 nonauthor finite falsification controls; no author checker imported."""
from fractions import Fraction as F
from math import factorial
import json
import sys

MODES = ('GAMMA_POWER', 'UNWEIGHTED_BAND', 'DIAGONAL_RESIDUAL',
         'UNCENTERED_RESIDUAL', 'UNSAFE_EPSILON', 'FACTOR_TAIL',
         'NORMALIZER_POWER', 'H_SCHEDULE')
if len(sys.argv) > 2 or (len(sys.argv) == 2 and sys.argv[1] not in MODES):
    print('UNKNOWN_CONTROL_MODE')
    sys.exit(2)
mode = sys.argv[1] if len(sys.argv) == 2 else 'BASELINE'
counts = {}
failures = []


def check(group, truth, label):
    counts[group] = counts.get(group, 0) + 1
    if not truth:
        failures.append(group + ': ' + label)


# The chart Jacobian and pole cancellations are checked on signed gamma,
# including arbitrarily small rational values; no numeric tolerance is used.
for gamma in (F(-7), F(-1, 1000), F(-1), F(1, 1000), F(2, 3), F(5)):
    for b in (F(-2), F(0), F(1, 7)):
        for c3 in (F(-1, 5), F(0), F(3)):
            d = gamma**2 - 12*b
            j = 8*gamma**3 - 144*b*gamma + 576*c3
            c, rr = d/gamma**2, j/gamma**3
            psi = abs(c) + F(7, 3)
            lam = gamma**2 * psi / 24
            wl = (24*lam-d)*(24*lam+d)/16
            power = 4 if mode == 'GAMMA_POWER' else 6
            check('chart', wl*gamma**2/24 == gamma**power*(psi**2-c**2)/384,
                  'w d-lambda = gamma^6 polynomial d-psi')
            check('chart', gamma**6*abs(c)**3 == abs(d)**3, 'absolute c pole')
            check('chart', gamma**6*rr**2 == j**2, 'signed R pole')

# Correlated atomic measures, not products of marginal laws. The finite model
# uses exact band constants extracted from the actual weighted atomic bands.
for depth in (2, 3, 8, 20, 50):
    a = F(1, 2**depth)
    m = 0
    while 2**m*a < F(1, 4):
        m += 1
    check('dyadic', F(1, 4) <= 2**m*a < F(1, 2), 'terminal band')
    shells = [F(2)*a*F(1, 2**j) for j in range(m)]
    floors = [F(1, 4**j) for j in range(m)]
    check('dyadic', sum(shells) <= 4*a, 'width sum')
    check('dyadic', sum(floors) <= F(4, 3), 'finite-r floor sum')
    # A boundary-focused, strongly correlated finite population.
    atoms = [(a/2, F(1), F(1, 7)),
             (a, F(1), F(1, 13)),
             (2*a, F(2), F(1, 17)),
             (3*a, F(4), F(1, 19)),
             (F(1, 3), F(2**depth), F(1, 23)),
             (-F(3), F(4*2**depth), F(1, 29)),
             (F(10), F(1), F(1, 31))]
    band = lambda delta, p: sum(mass*n**p for u,n,mass in atoms if abs(u)<=delta)
    floor = F(1, 100)
    h3 = F(8)
    deltas = [2**j*a for j in range(m+1)]
    moment2 = sum(mass*n*n for u,n,mass in atoms)
    cc = max([band(delta,p)/(delta+floor) for delta in deltas for p in (0,2)]
             + [moment2/h3])
    actual = sum(mass for u,n,mass in atoms if abs(u)<=a*n)
    bound = cc*(5*a + F(7,3)*floor + 16*h3*a*a)
    check('dyadic', actual <= bound, 'correlated decomposition bound')
    part = band(a,0)
    for j in range(m):
        selected = [(u,n,mass) for u,n,mass in atoms
                    if 2**j*a < abs(u) <= 2**(j+1)*a and abs(u)<=a*n]
        check('dyadic', all(n>2**j for u,n,mass in selected), 'shell norm implication')
        part += sum(mass for u,n,mass in selected)
    outer = [(u,n,mass) for u,n,mass in atoms if abs(u)>2**m*a and abs(u)<=a*n]
    check('dyadic', all(n>1/(4*a) for u,n,mass in outer), 'outer norm implication')
    # Inner band can include points not in the moving band, so it is a cover.
    part += sum(mass for u,n,mass in outer)
    check('dyadic', actual <= part, 'all moving-band atoms covered')

# The unweighted small-ball condition cannot be multiplied by an independent
# moment. U uniform and N=ceil(log2(1/U)) gives a factor m on the stated event.
for m in (2,4,8,16,32):
    em = F(1,2**m*m)
    lower_mass = F(1,2**m)
    inferred = em if mode == 'UNWEIGHTED_BAND' else m*em
    check('correlation', lower_mass <= inferred, 'unweighted O(e) shortcut fails')

# Orthogonal projection onto the complement of (3/5,4/5). Its negative
# off-diagonal entries increase variance along (1,-1); they are not zero.
a0,a1 = F(3,5),F(4,5)
cov = ((1-a0*a0,-a0*a1),(-a0*a1,1-a1*a1))
check('projection', cov[0][0]+cov[1][1] == 1, 'rank-one trace')
check('projection', cov[0][0]*cov[1][1]-cov[0][1]**2 == 0, 'PSD rank-one')
actual_var = cov[0][0] + cov[1][1] - 2*cov[0][1]
used_var = cov[0][0]+cov[1][1] if mode == 'DIAGONAL_RESIDUAL' else actual_var
check('projection', used_var == F(49,25), 'correlation retained in linear-form variance')
for value in (F(-4),F(0),F(7)):
    mean, coeff, obs, obsmean = F(100),F(3,7),F(19),F(11)
    field = mean+coeff*(obs-obsmean)+value
    residual = field-coeff*(obs-obsmean)
    if mode != 'UNCENTERED_RESIDUAL':
        residual -= mean
    check('projection', residual == value, 'centered endpoint residual')

# Explicit Gaussian even moments and the exponential-series coefficient
# bound implied by Minkowski; no independence of Fourier residuals is used.
moment = 1
for n in range(1,81):
    moment *= 2*n-1
    check('exponential', moment <= (2*n)**n, 'Gaussian moment upper bound')
    divisor = 2 if mode == 'UNSAFE_EPSILON' else 12
    coefficient = F((2*n)**n, divisor**n*factorial(n))
    check('exponential', coefficient <= F(1,2**n), 'exponential series majorant')
check('exponential', sum(F(1,2**n) for n in range(81)) < 2, 'geometric series partial sum')

# Exact independent endpoint-scalar integration. r^2 J^4 times the cubic
# endpoint integral is r^5 J^10, and r^-3/Z_r has Z_r proportional to r^2.
for radius in (F(1,2),F(1,7),F(1,100)):
    for jr in (F(1),F(2),F(17,3)):
        for depth_const in (F(1),F(4),F(7,2)):
            for cross_const in (F(1),F(5,2)):
                upper = depth_const*radius*jr**2
                integral = upper**3/3 + cross_const*radius*jr**2*upper**2/2
                numerator = radius**2*jr**4*integral
                expected = radius**5*jr**10*(depth_const**3/3+cross_const*depth_const**2/2)
                check('scalar_tail', numerator == expected, 'r^5 J^10 numerator')
                zpower = 4 if mode == 'NORMALIZER_POWER' else 2
                scaled = numerator/radius**zpower/radius**3
                check('scalar_tail', scaled == jr**10*(depth_const**3/3+cross_const*depth_const**2/2),
                      'one full r^2 normalizer and r^-3 scaling')
weights = ((F(1),F(99,100)),(F(10),F(1,100)))
weighted_tail = sum(prob*j**10 for j,prob in weights if j>5)
tailprob = sum(prob for j,prob in weights if j>5)
moment10 = sum(prob*j**10 for j,prob in weights)
used_tail = moment10*tailprob if mode == 'FACTOR_TAIL' else weighted_tail
check('scalar_tail', weighted_tail <= used_tail, 'same residual tail indicator retained')

# Independently encode each term as powers (r,H,w), then substitute w.
rows = {
 'radius':(0,0,-8),'radius_error':(1,3,-4),
 'elder':(1,4,4),'elder_error':(F(3,2),5,2),
 'endpoint':(1,3,2),'endpoint_error':(F(3,2),4,1),
 'band':(1,0,4),'leak':(1,4,0),'outer_band':(2,3,8),
 'hessian1':(2,5,4),'hessian2':(2,7,2)}
expected = [(F(2,3),F(8,3)),(F(4,3),F(13,3)),
 (F(2,3),F(8,3)),(F(4,3),F(13,3)),(F(5,6),F(7,3)),
 (F(17,12),F(11,3)),(F(2,3),F(-4,3)),(F(1),F(4)),
 (F(4,3),F(1,3)),(F(5,3),F(11,3)),(F(11,6),F(19,3))]
wh = F(-1,4) if mode == 'H_SCHEDULE' else F(-1,3)
for (label,(pr,ph,pw)),want in zip(rows.items(),expected):
    got = (F(pr)-F(pw,12),F(ph)+pw*wh)
    check('ledger', got == want, label+' substituted powers')
    check('ledger', got[0]>F(2,3) or (got[0]==F(2,3) and got[1]<=F(8,3)),
          label+' target domination')
    check('ledger', F(pr)-F(pw,12)>=F(2,3),label+' fixed-layer endpoint')
for label,(pr,ph,pw) in {'rH':(1,1,0),'embedding':(1,0,1),
                         'e':(1,0,4),'H2e':(1,2,4),'rw2':(1,0,2)}.items():
    check('ledger', F(pr)-F(pw,12)>0,label+' cutoff decays')
check('ledger', F(3)+F(2,3)==F(11,3),'physical fixed-layer power')

# Variation norm on atomic signed measures is sum of absolute masses.
for nu0 in ((F(1),F(2)),(F(1,5),F(4,5)),(F(2),F(0))):
    for changes in ((F(1,10),F(-1,20)),(F(0),F(0)),(F(-1,10),F(1,10))):
        nu=tuple(a+b for a,b in zip(nu0,changes))
        if min(nu)<0:continue
        m,m0=sum(nu),sum(nu0)
        err=sum(abs(a-b) for a,b in zip(nu,nu0))
        normalized=sum(abs(a/m-b/m0) for a,b in zip(nu,nu0))
        check('normalization', normalized<=err/m+abs(m-m0)/m,'probability normalization')
        if m>=m0/2:
            check('normalization', normalized<=4*err/m0,'positive mass floor')

print(json.dumps({'mode':mode,'checks':sum(counts.values()),'groups':counts,
                  'failures':failures,'scope':'finite controls only; no analytic proof'},sort_keys=True))
sys.exit(1 if failures else 0)
`````

### DESIGN.md
`````markdown
# C124 independent review design and exposure record

Reviewer: OpenAI/Codex /root/c99_custody_audit, delegated child of root01a0bbb5 under existing C124 claim33e06044-3ffa-4d61-81d8-937ad54e3fb4. No C124 proof, control or design contribution. Prior exposure includes C99/C103 source/author-side project work, C101 author-control custody, C102/C104 analytic reviews, C107 authorship and subsequent engineering/analytic review/custody roles. The immediately preceding source-only frontier audit identified the published beta<2/3 boundary and need for quantitative tails, but did not inspect or contribute to this new JB/DB/ES derivation. No fresh-context, blind-source, provider-independent or human-review claim. Organizational independence0. Dylan's owner-reported ongoing review is acknowledged under5973603003; this review itself is AI work, not his human verdict.

Target PROOF.md20668B SHA90148657397dcce31e8039afa9015c022f74b2ed0d41e75f2f2339074a8a520f; source manifest SHAa0371bd1985358820250e0d75936d6ec5112f165824df7a9f6e29e25e3f46f6d. I read the entire proof and exact C82/C101/A4/P interfaces before this design. I have not opened C124 controls.py, CONTROLS.md, author outputs, or author development notes. Existing sources' own equations are inputs, not independently rediscovered theorems.

Analytic obligations: reconstruct JB from weighted-before-conditioning Q10 and fixed-width LB, verify gamma-six cancellation and actual finite-r error; reconstruct DB as a partition including m=0 and the outer band, with fixed moment order2; identify centered endpoint residual as joint Gaussian projection after U_r,A_M and verify summable Fourier/Lp and exponential-series constants without coefficient independence; retain the residual indicator in Q30's scalar integral and one full normalization; verify failure-marked model tail separately; map every ledger/cutoff to the imported geometry and distinguish fixed11/3 from global2/3 log8/3 and conditional normalization.

Independent finite controls will use Fraction, not author code: signed/small-gamma chart cancellation; finite atomic correlated band decompositions and geometric sums; explicit correlated Gaussian projection and noncentered-regression falsifiers; exact Gaussian even moments/exponential-series coefficient majorant; endpoint-scalar integral powers and a two-atom residual-weight correlation countermodel; independently composed rational r/H exponent ledger and cutoff powers; signed finite-measure normalization. Negative modes will delete a gamma power, discard weighted correlation, assume diagonal residual covariance, omit centering, enlarge epsilon beyond the stated safe coefficient, omit the residual tail indicator, drop one normalizer power, or change the H schedule. Unknown modes must be rejected. These controls can refute algebra/finite implications but do not prove LB, Gaussian series convergence, topology or infinite-dimensional analytic estimates.

Freeze this design and independent_controls.py before execution or any author-checker exposure. Run only these new bounded controls in normal and optimized Python modes. Do not rerun parent/master suites. Preserve any actual failures rather than edit the candidate.
`````

### normal-baseline.stdout
`````text
{"checks": 601, "failures": [], "groups": {"chart": 162, "correlation": 5, "dyadic": 103, "exponential": 161, "ledger": 39, "normalization": 16, "projection": 6, "scalar_tail": 109}, "mode": "BASELINE", "scope": "finite controls only; no analytic proof"}
`````
