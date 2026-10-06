# Cap I4: d=3 spectral assembly

Dylan Roy — delegated AI work. Actual author: OpenAI / GPT-5.6 Sol,
`cap-i4-spectral-assembly-audit-20261006`. Scientific effect NONE.
Pickup: main#229 comment 6008801391.

This isolated child is based on entry-volume head
`c0e73e383791dc90fd5d21016a23fc9544f0cf9b` and consumes exact theorem
sources from the polar, angular, linear-volume, and entry-volume companions.

## Exact target

For every measurable nonnegative spectral test `G`, prove

    ∫ 1_{lambda>0} G(lambda,Lambda) d(a,b,d)
      = pi ∫_{0<lambda<Lambda} (Lambda-lambda) G(lambda,Lambda) d lambda d Lambda.

Coefficient ledger: entry factor 2, angular factor 2*pi, spectral/radius factor
1/4, hence exactly pi. No Gaussian law, residual product law, moment bound,
determinant tilt, cap event, or normalizer is instantiated here.

The contract is published before the implementation. The first hosted run is
expected to fail only because `CapI4SpectralAssembly` is absent.
