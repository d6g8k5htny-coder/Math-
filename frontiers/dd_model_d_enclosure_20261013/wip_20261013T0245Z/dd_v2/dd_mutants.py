"""Mutants of note DD's certificate: each applies one textual change to a copy of the modules and runs the controls
(dd_controls.py), which must FAIL (exit code 1).  Standard library only.
Usage: python3 dd_mutants.py            -> runs all mutants, prints a table, exit 0 iff every mutant is rejected."""
import os, sys, shutil, subprocess, tempfile, json
HERE = os.path.dirname(os.path.abspath(__file__))
MODULES = ['ddcore.py', 'ddbounds.py', 'ddtaylor.py', 'ddint.py', 'ddvq.py', 'ddgauss.py', 'ddS.py', 'dd_exact.py', 'dd_controls.py']

MUTANTS = [
    ('M1 Gauss weight', 'ddgauss.py', "w1 = div(add(q(18), s30), q(36))", "w1 = div(add(q(18), s30), q(35))"),
    ('M2 kernel recursion', 'ddbounds.py', "        if k > 0: out[k] = out.get(k, 0) - k * c", "        if k > 0: out[k] = out.get(k, 0) - (k - 1) * c"),
    ('M3 I_quad coefficient', 'ddtaylor.py', "(0, 2): Fr(13, 486)}", "(0, 2): Fr(13, 487)}"),
    ('M4 c0', 'ddbounds.py', "RHO_C0 = mul(smul(Dec(24), C.SQRTPI)", "RHO_C0 = mul(smul(Dec(23), C.SQRTPI)"),
    ('M5 pointwise bound constant', 'ddbounds.py', "add_term(Fr(23, 3888), 0, 2)", "add_term(Fr(21, 3888), 0, 2)"),
    ('M6 Gauss error constant', 'ddbounds.py', "return q(Fr(2 ** (2 * n + 1) * math.factorial(n) ** 4, (2 * n + 1) * math.factorial(2 * n) ** 3))", "return q(Fr(2 ** (2 * n) * math.factorial(n) ** 4, (2 * n + 1) * math.factorial(2 * n) ** 3))"),
    ('M7 Bell polynomial', 'ddbounds.py', "    d = {1: {(0, 0): Fr(-5, 3), (1, 0): Fr(-24)}}", "    d = {1: {(0, 0): Fr(-5, 3), (1, 0): Fr(-23)}}"),
    ('M8 moment recursion', 'ddint.py', "        J.append((J[n - 2] * (n - 1) + xp * e) * inv2a)", "        J.append((J[n - 2] * n + xp * e) * inv2a)"),
    ('M9 half-space bound in Lemma 1', 'ddbounds.py', "    for k, ck in enumerate([1, 3, 3, 1]): add_term(Fr(4, 3) * ck, k, 0)", "    for k, ck in enumerate([1, 3, 3, 1]): add_term(Fr(1, 3) * ck, k, 0)"),
]

def run_mutant(name, fname, old, new):
    tmp = tempfile.mkdtemp(prefix='ddmut_')
    for m in MODULES: shutil.copy(os.path.join(HERE, m), tmp)
    src = open(os.path.join(tmp, fname)).read()
    if src.count(old) != 1:
        raise AssertionError('mutant %s: the text to change occurs %d times' % (name, src.count(old)))     # kept under -O (v2)
    open(os.path.join(tmp, fname), 'w').write(src.replace(old, new))
    flags = ['-B'] + (['-O'] if sys.flags.optimize else []) + (['-S'] if sys.flags.no_site else [])     # the children run in the driver's mode (v2)
    r = subprocess.run([sys.executable, *flags, os.path.join(tmp, 'dd_controls.py')], capture_output=True, text=True, timeout=900)
    fails = [l for l in r.stdout.splitlines() if l.startswith('FAIL')]
    shutil.rmtree(tmp, ignore_errors=True)
    return r.returncode, fails

if __name__ == '__main__':
    ok = True; rows = []
    for (name, fname, old, new) in MUTANTS:
        rc, fails = run_mutant(name, fname, old, new)
        rejected = rc != 0
        ok = ok and rejected
        rows.append((name, rc, fails))
        print('%s: %s (exit %d) %s' % (name, 'REJECTED' if rejected else 'NOT REJECTED', rc, '; '.join(fails)[:160]))
    print('mutants:', 'ALL REJECTED' if ok else 'SOME NOT REJECTED')
    sys.exit(0 if ok else 1)
