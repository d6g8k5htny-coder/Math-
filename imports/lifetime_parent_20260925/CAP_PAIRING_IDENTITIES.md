# Cap pairing — vector average, h'' cancellation, §7 r^5 skeleton

**Object:** GROK-HEAVY-CAP-PAIRING-20260926-v1
**Scientific effect:** NONE. Does not accept Theorem A.
**Sources:** `MARKED_CYLINDER_CAP_PROOF.md` blob `0633aca3c2a2882b0de4399da0a75d64c2e6b2e1`; parent §7.

## Vector average (cap (7))

`w(x)=grad_y f(x,0)` vanishes at `±r/2`. Subtract the average of `w'` on the pin interval:

    w'(x) - (1/r) int_{-r/2}^{r/2} w'(t) dt

has size at most `m` times the mean of `|x-t|`. At the cylinder end `x=2r`,

    int_{-r/2}^{r/2}|2r-t| dt = 2 r^2,

so `||w'(x)|| <= 2 m r` on `|x|<=2r`, and the bound is sharp. No common Rolle zero for all components is used.

Interpolation remainder for the two-node problem gives `||w(x)|| <= (m/2)|x^2-r^2/4| <= (15/8) m r^2` on `|x|<=2r`.

## h'' cancellation (cap (11))

On the ridge `grad_y f(x,h(x))=0`, set `v=(1,h')`, `g(x)=f(x,h(x))`, `F=g'`.
Then `v'=(0,h'')` is purely transverse, `Df[v']=0` on the ridge, and `(H_f v)_y=0`, so

    D^2 f[v,v'] = (H_f v)·v' = 0.

Hence every `h''` term drops:

    F'' = D^3 f[v,v,v]
        = f_xxx + 3 f_xxy[h'] + 3 f_xyy[h',h'] + f_yyy[h',h',h'].

This is cap (11) for vector `h`. It does not identify the ridge with a gradient trajectory.
`F''>1/4` remains a worst-case estimate (`||h'||<=24/121`).

## Parent §7 r^5 numerator (skeleton only)

From (6.2) and depth failure `lambda_1 <= D r U^2`,

    int_0^{D r U^2} lambda_1(lambda_1 + E r U) d lambda_1
      = r^3 [(D^3/3) U^6 + (E D^2/2) U^5].

The remaining factors in `W_r` already carry `r^2`, so the depth-failure numerator is `O(r^5)` after integrating the Gaussian-polynomial majorant from (3.5)+(7.2). Dividing by `Z_r = Theta(r^2)` (A3 floor structure) would give `O(r^3)` on compact marks.

This skeleton is **not** Theorem A. It still needs the A3 floor as a reviewed theorem, the cap implication with embedded chart + Morse/§8, and the scalar far branch for `m=1`.

## Pairing import

`G_r =>` elder pairing remains conditional on parent §1 embedded `2r` chart and parent §8 Morse / distinct values. Cap 2D numerical corollary is out of scope.
