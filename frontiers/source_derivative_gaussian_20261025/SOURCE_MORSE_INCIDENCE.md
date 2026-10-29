# Frozen successor production contract: SourceMorseIncidence.lean

Frozen26October2026 before production code. Sole owner /root/source_morse_incidence; sole production
file SourceMorseIncidence.lean in this packet. Root owns shared manifests/lakefile/publication.
Validated scratch proposal below is adopted; its preimplementation wording is
provenance, not a claimed production result. All prior24qualifiedmodules/23inputs
and completed applicable checks are reused. No old source edits or checks.
No sorry/admit/customaxioms/native_decide; only standard3axioms and narrow imports.
New-only final compile, named kernel, complete public proof/instance axiom audits,
meaningful controls and honest command/source/artifact/failed-history receipts.
Scientific different-family review remains separate from author qualification.

Required final actual theorem: for hL:L!=0, smoothLaw2L almost surely has no
spatial point in the actual fundamental cube with both zero coordinate gradient
and zero actual Hessian discriminant. Use the proved equal-dimensional Sard
critical-image theorem already in pinned Mathlib, the literal four original
sin/cos coefficients, actual positive amplitudes/nonzero signed frequency,
all-order carrier erasure/replacement, exact Gaussian block/whole-tail law,
measurable actual bad event and Fubini/reconstruction. No a.s. Morse, parameter
nullity, density or desired source-law conclusion may remain as a final premise.
Generalize to all real-cover points by a valid countable compact exhaustion or
periodicity if useful. Reuse accepted conventional finite-L Morse/Sard and C293
mathematics; this is first new Lean source binding, not a repeat of those checks.
The formal finite-critical/quotient adapter should be derived from actual regular
zeros and a proved compactness/IFT theorem where available; identify any genuinely
remaining transport obligation instead of assuming finiteness or importing an
unproved Sard axiom. Do not touch occupied PR482/485 source or engineering lanes.
Conditional Morse at every null pin and distinct critical heights are not asserted
by the unconditional theorem. Preserve all completed scratch authorship/evidence.

# Actual source Morse application through equal-dimensional Sard

Author-side research, 26 October 2026. No independent scientific-review credit.
Production is not yet authorized. All implementation in this directory is new
scratch proof work; the earlier actual four-mode span, finite carrier split,
Gaussian independence, cube-event Borel proof and accepted analytic Morse and
C293 results are reused without repeating their completed checks.

## Corrected import boundary

The earlier reconnaissance statement that pinned Mathlib lacked a usable Sard
theorem was too broad. Root located the existing theorem
`MeasureTheory.addHaar_image_eq_zero_of_det_fderivWithin_eq_zero` in
`Mathlib/MeasureTheory/Function/Jacobian.lean:645` (pinned Mathlib
`d13f23b723b8a846827a245b89c10fc7d3f11612`). Its actual assumptions are a
finite-dimensional real normed space E, its Borel measurable structure, an
additive Haar measure mu, a set s, derivatives within s at every point and zero
derivative determinant there. It proves `mu (f '' s) = 0`. Neither s nor its
image needs a measurability premise. Thus it applies directly to an explicit
four-dimensional incidence map. No general parametric Sard development is needed.

The accepted conventional source-Morse argument in the parent
`PROOF_APPLICATION.md` remains applicable and unchanged. This work fills a
specific Lean mechanism; it does not replace or requalify that analytic proof.

## Literal incidence construction

Write E=`Fin 2 -> R`, P=E x E, c=`sourceC L`, and
`A=![sourceContactAmplitude L 1,sourceContactAmplitude L 2]`.
The source's original four modes are precisely x-cosine, x-sine, y-cosine,
y-sine (earlier `fourMode_eq`, `fourModeCoefficient_eq`). Both amplitudes are
strictly positive for L!=0 and c!=0, including negative L.

Freeze all other original coefficients to an arbitrary good smooth residual.
Its coordinate gradient is a globally C1 function g:E->E. For the coefficient
grouping a=(cosine coefficients, sine coefficients), the actual gradient is

    g_i(x) + (-A_i*c*sin(c*x_i))*a.cos_i
           + (A_i*c*cos(c*x_i))*a.sin_i.

For sigma:E_index->Bool select either cosine or sine in each coordinate.
The selected b_i(x) is nonzero on that patch; c_i(x) is the unused channel.
Four patches cover all spatial points by sin^2+cos^2=1. The selected/unused
parameter incidence map is the literal globally defined formula

    F(x,z) = ( (-(g_i(x)+c_i(x)*z_i)/b_i(x))_i, z ).

It is differentiable at every point of the patch. If H denotes the spatial
derivative of the affine gradient with its parameter frozen at F(x,z), its
derived normal equations are

    (DF(v,0)).unused = 0,
    diag(b(x))*((DF(v,0)).selected) = -H*v.

The diagonal map is injective on the patch. A nonzero Hessian nullvector
therefore gives a nonzero incidence-derivative nullvector. This proves det DF=0
without a four-by-four determinant expansion. Sard makes the image of the
degenerate incidence locus Haar-null. Conversely, an actual critical parameter
with b_i(x)!=0 is exactly F(x,a.unused), by solving the two critical equations.
Thus each patch's degenerate-critical-parameter set itself has outer measure zero.

The involutive linear `channelSwap sigma` returns selected/unused coefficients
to the fixed original ordering. Its whole-function gradient identity also
identifies the fixed-parameter derivatives. Haar-nullity is preserved by this
linear map using the already available differentiable-null-image theorem at
Jacobian.lean:556. This avoids requiring a new Gaussian permutation law. A
finite union proves Haar-nullity for the fixed original coefficient order.

## Gaussian and carrier joins

The original grouped four-Gaussian law is absolutely continuous with volume.
`FourChannelDensity.lean` derives this from the actual real Gaussian density
and two products, using `piFinTwo` to transport the two-coordinate Pi law. Its
two-coordinate lemma also permits arbitrary means and nonzero variances.
The actual source application uses the four independent N(0,1) coefficients;
the residual field is arbitrary and need not have mean zero after freezing.

Earlier `actual_finite_block_indep_erased` proves independence of the literal
finite block and the full erased smooth sample, not merely equality of a few
moments. Earlier `actual_derivative_finite_split` supplies the actual derivative
decomposition, with weighted summability proved explicitly.

New `FiniteReplacement.lean` replaces any finite original block by arbitrary
real coefficients, proves every-order goodSample preservation and joint
measurability, and reconstructs the literal original smooth sample from its
erased carrier and original finite coordinates. Therefore the preimage of the
already Borel compact-cube Morse event is a measurable residual/parameter
event. Its every-residual parameter section is null by the incidence argument.
Fubini and the exact independent product law give actual smoothLaw-nullity.
No target a.s. Morse assertion or assumed parameter-nullity is a source premise.

## Proposed actual export and remaining adapter work

The minimal production target, if separately frozen, is

```lean
theorem smoothLaw_ae_sourceMorseCube {L : R} (hL : L != 0) :
  (forall-ae omega under smoothLaw 2 L,
    forall x in sourceMorseCube L, 0 < sourceMorseDiscriminant L omega x)
```

The final actual adapter must still join the following identities explicitly:

1. The four selected original SourceMode indices are distinct, and the grouped
   finite-coordinate law is the displayed two-Pi-product Gaussian law.
2. Finite replacement's actual coordinate gradient is the displayed affine
   trigonometric family, by the previously proved literal derivative split and
   four-mode coefficient formulas; the residual gradient is C1 by actual C-infinity.
3. The spatial derivative of that actual coordinate gradient is the literal
   Hessian. Symmetry identifies the mixed entries, so zero of the existing
   five-observation discriminant implies a singular gradient derivative.
4. Apply the already measurable cube event to replacement, Fubini, exact
   block/erased-carrier independence and reconstruction.

These are concrete adapter obligations, not missing analytic transversality.
The new generic incidence theorems expose only honest differentiability,
nonvanishing-channel and singular-Hessian hypotheses. The actual export must
derive all of those from L!=0 and the actual smooth source.

The torus-coordinate norm identification, periodic descent and application of
the accepted C293 finite-critical theorem remain a separate actual adapter.
Distinct critical values are unnecessary for finiteness. This route does not
assert any fixed null conditional fiber is Morse, nor Palm/counting/elder or
capture/dynamics closure.

## Evidence boundary

The new Lean sources and retained failed/successful logs live beside this file.
For root-authored compile commands, numbered JSON receipts record command, cwd,
actual exit, unchanged source hashes and raw-log hash. The helper-authored files
retain their actual `lean_exit` logs and source-hash files; do not invent an
independent audit or machine receipt for them. Final module/kernel/axiom and
provider-distinct review qualification would be new production obligations.
