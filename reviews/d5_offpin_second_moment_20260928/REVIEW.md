# Nonauthor review: off-pin second factorial moment

Scientific effect: **NONE**. This file does not change `lemma_closed`, prizes,
premises, `STATUS`, `PROOF_INDEX`, `GRAPH`, or any author source.

## Verdicts

| ID | Statement | Verdict |
|---|---|---|
| P_eta | `E N_eta(N_eta-1) <= C_eta r^5` for window points in `{|X|>=eta}` minus pins, fixed `eta>0` | ACCEPT |
| Planar matching event | `c r^3 <= P(A_r) <= C r^3` in `d=2` | ACCEPT (same as #117) |
| Torus-wide `E N(N-1)` | pair intensity with a witness near a pin | CANDIDATE pending review and test (catalog C6) |
| Thin-tube first moment | tube inside a fixed scaled ball | superseded by scaled-ball synthesis |

## P_eta

`frontiers/remote_collision_20260928/PROOF.md` Lemma 1 uses only that both witnesses stay a fixed positive distance from the pins. Replacing the remote radius `rho` by `eta` does not change the divided-difference Jacobian or the ledger `delta min(1, r^3/delta^3)`.

## Candidate C6

Write `N = N_eta + N_<eta`. P_eta bounds the first summand. The remaining object is pair Kac-Rice with a witness in `{|X|<eta}`. A first-moment bound does not produce this second moment. Catalog C2, if later proved, would obstruct a global `O(r^5)` upper bound via `N(N-1) >= 2 1_{N>=2}`. That obstruction is conditional on C2 and is not recorded as a theorem here.

## Not claimed

Numerical constants. `k` down to 0. `d>2` first moment. Elder selection. Any STATUS / GRAPH / lemma_closed / prize change.
