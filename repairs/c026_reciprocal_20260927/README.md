# C026 reciprocal: scoped finite-polynomial successor

**Disposition:** tested, noncontrolling successor. **Scientific effect: NONE.**
No original C026/C027 source, theorem, claim manifest, review verdict, or status
register is changed. This helper is not installed into the historical engine.

## Reproduced source defect

The original `c026 series.py` is 6,553 bytes, SHA-256
`4058cad4cc7c69201cb6f7ea392c1fae1099d087a7489a34e01ece064282519a`.
It is available as a [legacy Drive source](https://drive.google.com/file/d/1zl8NNCsaAa8tgFwhMf2-s1zwY0cOk8Z0/view)
and as a byte-identical [importable-name copy](https://drive.google.com/file/d/1ijBjqwJ0JCvDci28C3VlnwI0CevtUEqj/view).

With `NM=5`, its `LS(0,[1,1]).inv()` returns linear coefficient 0, rather than
-1. Multiplication by `1+r` therefore leaves linear coefficient 1, rather than
0. The original inverse regression exits 1 in both ordinary and optimized
Python. The convolution loop excludes the endpoint `j=k`; the separate original
loop-length expression also is not the declared inverse-output precision.

The inspected C026/C027 source pair contains no calls to `LS.inv()`. A separate
C027 replay at the scaled station `(-3,1)` reproduced all eight stored coarse-table
fields in ordinary and optimized Python. That is one non-certifying station,
not a reproduction of the entire 258-row table or a Gaussian theorem. It does
not establish that other callers elsewhere in the workspace avoid `LS.inv()`.

## Exact contract and derivation

The input is the COMPLETE finite polynomial

`A(r) = r^d * (a_0 + a_1*r + ... + a_m*r^m)`, with `a_0 != 0`.

For a requested largest inverse Laurent exponent `K`, the helper returns
`(-d, (b_0,...,b_(n-1)))`, where `n=max(0,K+d+1)` and

```
b_0 = 1/a_0
b_k = -(sum(a_j*b_(k-j), j=1,...,min(k,m)))/a_0
```

The constant coefficient of the product is `a_0*b_0=1`. For each `k>=1`, the
coefficient is `a_0*b_k + sum(a_j*b_(k-j))=0` by the recurrence. The nonzero
`a_0` makes each coefficient unique. In the inverse, coefficient index `k` has
Laurent exponent `k-d`; hence precisely `K+d+1` coefficients are needed when
that number is positive. This derives the inclusive convolution endpoint and
the output-precision offset sign independently of the original implementation.
All arithmetic uses integers and `Fraction`; invalid inputs raise explicit
exceptions, not optimization-removable assertions.

### Boundary that must not be erased

A complete finite polynomial is NOT an unknown-tail truncated Laurent series.
If the supplied coefficients are only a jet of an unknown function, omitted
coefficients cannot silently be declared zero. That caller needs a separate
precision/remainder argument before adopting this utility. In particular, this
change does not certify C026's truncation propagation, nine-pin conditioning,
Gaussian normalizers, window approximations, or the C027 intensity calculation.
No automatic monkey-patch or replacement of `LS.inv()` is performed.

## Reproduce the successor checks

From the repository root, using only Python's standard library:

```sh
python -B -S -m unittest discover -s repairs/c026_reciprocal_20260927 -p 'test_*.py' -v
python -B -O -S -m unittest discover -s repairs/c026_reciprocal_20260927 -p 'test_*.py' -v
```

Current-session local evidence: Python 3.13.5; 12 unit tests passed in each mode.
Before implementation, the same test file failed because the implementation was
absent. Two deliberate algorithm mutations were then rejected in both modes:
removing the convolution endpoint and reversing the offset sign in the output
length (four mutation runs, all exit 1, test failures rather than import errors).
The original inverse regression remains a recorded failure, not a passing test.

The entire existing Math repository suite was not run in the local scratch
environment. The dedicated PR workflow runs the new unit tests; its actual
results must be read separately. Earlier archived 2,890-test receipts are not
executions performed for this change. Nonauthor review is requested through
[the existing coordination thread](https://github.com/d6g8k5htny-coder/main/issues/86#issuecomment-5858478286);
no independent acceptance is implied by these local tests or by publication.

## Local source identities

- `reciprocal.py`: SHA-256 `1f6ec27e47e578eb54528ceb93b5630a67baed7e090fd9e9743670f560c3a79d`
- `test_reciprocal.py`: SHA-256 `1f86994fa46ed11d9828daa51a6776dc211e4d668bad2e70e999a47721c0129c`
