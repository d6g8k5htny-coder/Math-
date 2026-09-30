# Moments of the radial tail

For the microscopic point-intensity law, let `Q_t=R/t` conditional on `R>t`. The tail exponent **11** is the sharp moment boundary: every fixed real power below 11 is finite, and every power at or above 11 diverges in the actual conditional microscopic law.

If `c=C₂/C₀`, the source's uniform tail expansion gives

```text
E Q_t^p = 11/(11-p) − 2pc/((13-p)(11-p)) t^-2 + O_p(t^-4),  p<11
E log Q_t = 1/11 − 2c/143 t^-2 + O(t^-4).
```

[The derivation](MOMENT_CONSEQUENCE.md) also supplies every fixed finite-order power/log-moment expansion, checks the author's fixed quantile formula, and shows that `0<B_sign<4587821/876544` holds throughout the fixed dimension/frame scope. The stronger positive bound on `c` keeps its aligned planar assumptions.

The original pin-separation limit is taken **before** the large radial threshold limit. These results do not establish finite-separation rates or whole-cluster moments. They consume the exact analytic expansions of [PR #176](https://github.com/d6g8k5htny-coder/Math-/pull/176), whose source reviews remain separate.

This report credits the author's already-offered second-order and quantile corollaries, records exposure chronology, and adds their all-order derivation. It is not a duplicate of the active Slice B review. Same-provider review earns zero organizational-independence credit.

[Nonauthor analytic review](NONAUTHOR_REVIEW.md) · [Exact custody](COROLLARY_CUSTODY.json) · [Arithmetic controls](moment_consequence_checks.py) · [Lifetime companion](../../frontiers/lifetime_moment_boundary_20260930/README.md)

The review binds the original local custody manifest. The portable copy here changes only its four local source paths to sibling filenames and records the original manifest SHA-256. All listed artifact and source bytes retain the reviewed identities.
