import sys, math, time
sys.path.insert(0, '.'); sys.path.insert(0, '../dv')
import numpy as np
import ddcore as C, ddcub as CB
from decimal import Decimal as Dec
import vform3 as V3
def ref_box(u_lo, u_hi, w_lo, w_hi, v_lo, v_hi, n=(40, 40, 40)):
    us = np.linspace(u_lo, u_hi, n[0]+1); ws = np.linspace(w_lo, w_hi, n[1]+1); vs = np.linspace(v_lo, v_hi, n[2]+1)
    um = 0.5*(us[1:]+us[:-1]); wm = 0.5*(ws[1:]+ws[:-1]); vm = 0.5*(vs[1:]+vs[:-1])
    du = us[1]-us[0]; dw = ws[1]-ws[0]; dv = vs[1]-vs[0]
    tot = 0.0
    for u in um:
        tau = math.exp(u)
        Wg, Vg = np.meshgrid(wm, vm, indexing='ij')
        G = Wg**3
        vals = V3.weight(tau, G)*V3.F(tau, G, Vg)*tau*3*Wg*Wg
        tot += vals.sum()*du*dw*dv
    return V3.A3*tot
box = (math.log(0.3), math.log(0.5), 0.6, 1.4, 1.0, 3.0)
for n in ((20,20,20), (40,40,40), (80,80,80)):
    print('ref midpoint', n, '%.10f' % ref_box(*box, n=n))
t0 = time.time()
order = int(sys.argv[1]) if len(sys.argv) > 1 else 3
tol = Dec(sys.argv[2]) if len(sys.argv) > 2 else Dec('2e-6')
enc, ncells, totw, fails = CB.integrate_box(*[Dec(repr(x)) for x in box], n0=(1, 2, 2), order=order, tol=tol, max_cells=3000, log=sys.stdout)
print('TM cubature order %d: [%s, %s] width %.3e cells %d fails %d (%.0fs)' % (order, enc[0], enc[1], float(totw), ncells, fails, time.time()-t0))
