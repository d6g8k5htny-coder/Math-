"""Mutants of note C3-R's control script: each applies one textual change to a copy of c3r_exact.py and runs it; the
controls must FAIL (exit code 1).  Standard library only.  The children run in the driver's interpreter mode.
Usage: python3 c3r_mutants.py            -> runs all mutants, prints a table, exit 0 iff every mutant is rejected."""
import os, sys, shutil, subprocess, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))

MUTANTS = [
    ('M1 T1-R term 4a\' -> 2a\'', "sigma * (5 + 4 * ap)", "sigma * (5 + 2 * ap)"),
    ('M2 v(a) without m theta', "return (1 - 2 * a - m * th) / (3 * (4 - 2 * a - m * th))", "return (1 - 2 * a) / (3 * (4 - 2 * a))"),
    ('M3 m = 1 rate 1/30 -> 1/29', "    sigma = Fr(1, 30)\n    require(sigma <= min(v1", "    sigma = Fr(1, 29)\n    require(sigma <= min(v1"),
    ('M4 a_eff = a for every m', "return a if m <= 3 else 2 * a / (m - 1)", "return a"),
]


def run_mutant(name, old, new):
    tmp = tempfile.mkdtemp(prefix='c3rmut_')
    src = open(os.path.join(HERE, 'c3r_exact.py')).read()
    if src.count(old) != 1:
        raise AssertionError('mutant %s: the text to change occurs %d times' % (name, src.count(old)))
    open(os.path.join(tmp, 'c3r_exact.py'), 'w').write(src.replace(old, new))
    flags = ['-B'] + (['-O'] if sys.flags.optimize else []) + (['-S'] if sys.flags.no_site else [])
    r = subprocess.run([sys.executable, *flags, os.path.join(tmp, 'c3r_exact.py')], capture_output=True, text=True, timeout=600)
    msg = [l for l in r.stderr.splitlines() if l.startswith('AssertionError')]
    shutil.rmtree(tmp, ignore_errors=True)
    return r.returncode, msg


if __name__ == '__main__':
    ok = True
    for (name, old, new) in MUTANTS:
        rc, msg = run_mutant(name, old, new)
        rejected = rc != 0
        ok = ok and rejected
        print('%s: %s (exit %d) %s' % (name, 'REJECTED' if rejected else 'NOT REJECTED', rc, '; '.join(msg)[:160]))
    print('mutants:', 'ALL REJECTED' if ok else 'SOME NOT REJECTED')
    sys.exit(0 if ok else 1)
