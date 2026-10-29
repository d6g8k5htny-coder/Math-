# Finite trigonometric polynomials in the literal source coefficients

Add SourceFiniteTrig.lean, namespace I4SourceFiniteTrig. This bounded actual-source representation bridge follows the accepted interpolation mathematics; it does not reprove that mathematics or claim remote jet rank. Read /workspace/scratch/finite-trig-representation-preflight/REPORT.md for exact pinned APIs and rationale. Use Lean4.34.1/Mathlibd13f23b723b8a846827a245b89c10fc7d3f11612, unchanged original source, period and smooth sample carrier.

Reuse qualified46modules/1089targets/32inputs at published3e15af2eab94b2448ce28aeb4c926ada7d596a50, all existing Gram/series/conditional-law/geometry proofs and owner verification reuse. A new agent/session, process requirement or freeze label never warrants replay of applicable completed checks. Root owns shared metadata/config/cache/git/publication; producer owns only this new source and assigned scratch. Workers do not dispatch agents or edit old sources. Root dispatches one scratch-only source-conversion helper, whose needed frozen section is integrated once into the new module; producer owns list algebra, derivative adapter and the single final qualification.

## Exact representation and operations

Use structure TrigTerm with fields coeff:ℝ, frequency:Fin2→ℤ, offset:ℝ; TrigPoly is List TrigTerm. Define termEval L t x = t.coeff*cos(phase2L t.frequency x+t.offset), eval L p x as the finite list sum. Duplicate terms are permitted, with no normalization or equality test on real offsets.

Public functions: constant a=[(a,0,0)]; scale a p multiplies coefficients; translate L z p changes offset to offset−phase2L frequency z (semantic convention x↦f(x−z)); mul p q uses nested flatMap of two-term products. The pair (a,k,α),(b,l,β) becomes [(a*b/2,k−l,α−β),(a*b/2,k+l,α+β)]. Addition is list append, negation uses scale−1; no ring instance or generic Fourier library. These operation definitions and correctness permit every real L, including zero.

Required public written propositions (seven):
- eval_constant L a x: eval L(constant a)x=a.
- eval_append L p q x: eval L(p++q)x=eval L p x+eval L q x.
- eval_scale L a p x: eval L(scale a p)x=a*eval L p x.
- eval_translate L z p x: eval L(translate L z p)x=eval L p(x−z).
- eval_mul L p q x: eval L(mul p q)x=eval L p x*eval L q x.
- toSource_eval hL p x: finitePairing (fun m=>modeCoefficient2L m x)(toSource L p)=eval L p x.
- toSource_derivative hL p n x u: finitePairing (derivativeCoefficient2L n x u)(toSource L p)=iteratedFDeriv ℝ n(eval L p)x u.

Public toSource L p is a total Finsupp SourceMode2→₀ℝ, independent of proof hL. Only its two source correctness theorems require hL:L≠0. Keep the original observation-times-direction finitePairing convention from SourceFinitePinKernel. Do not define a replacement source, amplitude, conditional kernel or target law.

Convert each shifted cosine at frequency k and offsetθ into finite original source coefficients: k=0 uses none with coefficient cosθ/A_none. For k in halfLattice, canonical cosine coefficient cosθ/A and sine coefficient −sinθ/A. For k≠0 outside halfLattice, use −k and sine coefficient +sinθ/A. Divide by the actual representative's positive sourceModeAmplitude (both channels have same amplitude), proved privately from sourceZ_pos/sourceWeight_eq_physical/exp_pos/sqrt_pos under hL. No uniform amplitude floor, carrier or nonconstant-only restriction. Sum coefficient-scaled atoms across the list. Private atomSource, pairing-linearity, phase arithmetic, amplitude positivity and finite support helpers are allowed only as needed. Preserve every offset and correct negative-frequency sign.

Prove product semantics from the existing Real.two_mul_cos_mul_cos; sine is the shifted cosine at −π/2. Reuse existing Finsupp.linearCombination or bounded private finite pairing linearity, not a new algebra package. The all-order derivative adapter must use the actual accepted smoothSourceField_derivative_series: the finite shift of existing zeroSample is a literal SmoothSample2L whose field equals eval globally, and its series collapses to the finite pairing. Do not reprove differentiation of an infinite series. All n, directions and x are arbitrary, including n=0.

## Qualification and controls frozen before source

Only the new representation/coefficient bridge needs checking. Reuse unchanged SourceFinitePinKernel's qualified object and all old evidence. No freshnesscompile, helper kernel/audit/control campaign, artifact repackaging or old payload hashing.

Before source, producer freezes concrete controls for: empty/constant and append/scale semantics; translation convention at a nonzero shift; product retaining the full 1/2 factors; sine via offset−π/2; nonzero positive and negative frequencies with nontrivial offsets and literal canonical source conversion; zero frequency requiring actual none; actual coefficient field equality under hL; arbitrary-order derivative pairing and explicit n=0/first/second-order instances. Parameterized identities may provide stronger coverage than brittle numerical transcendental calculations. Include at least one actual finite trig product relevant to the future annihilator or local jet basis, without claiming its jet properties.

One negative mutation drops the 1/2 in the two-term product. At two constant-one inputs, the mutated evaluation is2 while the actual product is1; prove the finite arithmetic counterexample and require intended rejection at exactly one False with no unrelated errors. This is a finite trig normalization counterexample, not a claimed random field failure. Negative-frequency signs and zero mode are separately covered by positive coefficient controls.

Freeze final source before exhaustive actual-module-index standard3/classification, meaningful controls and exactly ONE own-module kernel. Reuse any applicable earlier strict Werror compile of the exact unchanged final source; a later freeze label alone does not justify another compile. Include every written private/public/generated/structure/foreign-namespace constant in actual-module inventory; only the seven intended public written propositions enter research registry. Data definitions/projections/constructor/extensionality/equation artifacts remain inventory-only. Any new public theorem beyond seven requires root acknowledgement. No Prop-valued bundles, sorry/admit/customaxioms/native_decide/implemented_by/umbrella import Mathlib.

Retain all attempts, failures, actual commands/exits/timings/full streams/source-object custody. Root alone copies the named qualified production object; no control/helper objects, and no compile merely to obtain ilean. Same-family technical review is useful but earns provider-distinct credit0. Scientific effectNONE.

This checkpoint constructs finite source representations and derivative pairings. Torus-coordinate separation, pin-annihilation and local 2jet inversion, actual remote residual positivity/Gaussian law, conditional global Morse on each prescribed positive-gap fiber with distinct endpoints, joint-value incidence/selection, canonical Lifetime/H0 labels, frames/Rice/Parent Lean remain later joins. No common null event across uncountably many targets is claimed.

Canonical authority links for onboarding/handoff (links are not proof of reading):
https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OWNER_MANDATE_20261015.md
https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OP-AUTONOMY-20260923-v2.1.md

Root-dispatched conversion helper owns ONLY /workspace/scratch/finite-trig-source-conversion. It proves private atomSource/canonical-source pairing and needed finite-pairing/actual-amplitude facts under onlyhL, preserving zero mode and both frequency signs. It supplies one frozen needed section, source identity, all development attempts and strict-elaboration evidence. Producer integrates that section once, does not import a helper object, and freezes all integrated source before the sole kernel. Helper has no separate kernel/audit/control campaign, public research-target credit, production cache/config/git or external actions. Its successful strict evidence is reused; final integrated module qualification covers the copied proof once. No new standalone generic Fourier theorem package.
