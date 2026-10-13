import math, sys
sys.path.insert(0, '.')
import stein_bounds2
stein_bounds2.C3 = 90.0
u_lo, u_hi = math.log(1e-3), math.log(1e3)
Nu0 = 24; worst = []
for i in range(Nu0):
    hu = (u_hi - u_lo)/(2*Nu0); uc = u_lo + (2*i + 1)*hu
    tau = math.exp(uc)
    g_hi = min(9.0, (60/(12*tau*tau))**0.25 + 0.5); g_lo = 1e-3*g_hi
    w_lo, w_hi = math.log(g_lo), math.log(g_hi)
    for j in range(6):
        hw = (w_hi - w_lo)/12; wc = w_lo + (2*j + 1)*hw
        b = stein_bounds2.cell_bound(uc, hu, wc, hw)
        B = stein_bounds2.second_deriv_bounds(uc, wc)
        r = stein_bounds2.rho_derivs(uc, wc)
        H = stein_bounds2.EgQ_hybrid(uc, wc, stein_bounds2.Q_0)
        worst.append((b, uc, wc, hu, hw, B, r, H))
worst.sort(reverse=True)
for w in worst[:8]:
    b, uc, wc, hu, hw, B, r, H = w
    print('bound %.3e at tau=%.3g g=%.3g hu=%.2f hw=%.2f | Buu %.2e Buw %.2e Bww %.2e | rho %.2e rho_u %.2e rho_w %.2e rho_uu %.2e rho_ww %.2e | E|g| bound %.2e' % (b, math.exp(uc), math.exp(wc), hu, hw, B[0], B[1], B[2], r[0], r[1], r[2], r[3], r[5], H))
