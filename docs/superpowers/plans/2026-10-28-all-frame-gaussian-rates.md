# All-frame Gaussian rare-lifetime rates

User direction: continue mathematical improvements until a genuine limit is
reached. Continue PR522/523; preserve their exact source bytes and review scope.

## Target

Remove the coordinate-axis restriction uniformly over all orthonormal frames,
obtain matching finite-long-lifetime lower tails, and extend to a declared
spectral class: stationary centered real torus Gaussian fields with even
nonnegative a_n, positive a_n on the cube ||n||_infinity<=3, and
sum sqrt(a_n)(1+|n|)^4 finite. Constants depend on the fixed spectrum.

## Current construction and checks to finish

Translate M to0,S=ru; omega=2pi/L. Let s_i=sin(omega x_i)/omega,
q=sum2(1-cos(omega x_i))/omega^2, S=s(ru), w=rS/|S|^2,
l=w dot s, z=P_(S perpendicular)s, lambda=r/|S|=1+O(r^2).
For j=0,1 use trial field

    h_j=b-5kr l^2+6k l^3-2k q^2/r-|z|^2/r+j Gamma q^3/r,
    Gamma=(2k_++1)/(4/omega^2).

Hard penalty and its gradient vanish exactly at both pins. Scalar pin errors
at S are value O(r^5), full gradient O(r^4); M is exact. The desingularized
pin error is therefore O(r^2). An exact uniformly bounded right inverse on
the fixed Fourier cube [-2,2]^d corrects it by C4/RKHS norm O(r^2).
At contact, its rank follows from the degree<=3 polynomial grid argument.

Global essential deficit uses q>=|s|^2=l^2/lambda^2+|z|^2. Once
lambda^4<=20/19, the quadratic form with coefficients (2/lambda^4,-3,5)
has minimum eigenvalue>=1/14. Thus deficit>=k(l^4+r^2l^2)/(14r)+|z|^2/r.
Away from0, r times the deficit tends to2kq^2+|z|^2, uniformly positive.
Near0 use the sine chart (l,z); correction with zero value/gradient atM
costs only O(r^2)(l^2+|z|^2). Fixed C4 zero-pin residuals satisfy Hermite
and transverse-gradient cancellation in this chart, hence preserve the
event, types and weight floor for smallr. Final support is cube[-3,3]^d.

For j=1, -Gamma q^3 in the deficit is locally order6 and can be absorbed
in a fixed small chart. At p=(L/2,0,...), s=0 and q=4/omega^2, so deficit
is strictly negative. A positive inner shell separates M from every older
point and forces finite lifetime>=c/r, hence X>=c/(k_+r^4).

The generic Gaussian upper proof needs only C4 square-root summability and
the contact/transverse jet rank, already supplied by positive cube2 modes.
Conditional exponential-square moments, full normalizer bounds, symmetric
Cameron-Martin translation and finite-mode RKHS cost yield all claimed rates.

- [x] Obtain adversarial author-support checks of explicit construction.
- [x] Write full proof, source manifest, exact controls and verification.
- [x] Run normal/optimized controls, obtain fresh same-family technical
  critique, and resolve the three literal corrections identified.
- [x] Prove the moderate-gap extension and explicit nonuniformity obstruction.
- [x] Reuse the existing cusp model and prove its actual global
  essential/finite split at every fixed positive critical ratio; derive
  fixed-ratio finite-moment divergence and conditional genericity/H0 reading.
- [x] Search the remaining sharp-rate and small-gap frontiers for prior work.
- [ ] Publish the nine additive files as a Draft stacked on PR523. This is
  the local prepublication checkpoint; no different-family acceptance,
  Ready transition or merge is included.

## Execution outcome and remaining boundary

The final packet is `frontiers/all_frame_gaussian_rates_20261028/`.
Its main proof and critical appendix retain exact source identities and
separate internal technical readbacks. Normal/optimized finite controls
pass identically. Existing proof and governance files are unchanged.

Source search found that quartic contact, the typed cusp normalizer and
the factor288 were already proved; they are explicitly credited rather
than presented as new. The new global split uses a fixed-neighborhood C4
Hermite inequality and an off-contact critical-height mesh argument.

The remaining quantitative boundary is the optimal fixed-gap exponential
coefficient and joint tiny-gap analysis of the global essential factor.
The latter is not supplied by the existing local 13/27 elder-share limit.
The present matching bounds also do not decide the critical constant in
the logarithmic moment transition. Cross-spectrum/dimension/volume
uniformity, general counting integration and different-family scientific
review remain separate obligations.

Fallback already established: smooth local positive/barrier profiles can be
uniformly approximated by finite Fourier modes and corrected with a frozen
cube2 pin right inverse. This gives existential all-frame bounds even if the
more explicit template above has a defect. Do not publish an unproved shortcut.
