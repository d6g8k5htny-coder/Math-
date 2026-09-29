# Retraction record — CL-C7-TOTAL-K-SCALING-RECON-20260929-v1 (withdrawn 2026-09-29, same day)

**Scientific effect:** NONE. Author: Anthropic Claude (session `session_01NMeKEismAyeqgdB4sy2NJU`).

The v1 memo (Math-#150, first commit `2fa23ba`) conjectured `ρ_rej(ℓ) ≍ ℓ^{−1/4}` for the unrestricted rejected
density and an inverse-moment split at `−3/4`. **That conjecture was wrong**, and the error was the author's:
the selection bound `min{1,(r/k)³}` was inserted against the parent's crude majorant `H(b,k)` (P (13.4)), which
does not carry the `k²` vanishing of the candidate intensity at small gap marks (`Z_r/r² → (6k)² E[…]`, P (5.4) —
the origin of the `k^{4/3}` in the (15.2) gamma integral). With that factor restored the near rejected density is
`O(ℓ^{1/4}) + O(1)`, and the unrestricted difference is `O(1)`, not divergent.

The corrected result is the author-side candidate `frontiers/c7_total_bounded_20260929/PROOF.md` (Theorem K,
Corollary T), landed on the same PR. The v1 route is preserved there as the rejected checker mutant `M1`. The
retraction is recorded here rather than by history rewrite; the v1 bytes remain in the PR history.
