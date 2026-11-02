# Frozen source contract: actual scalar curvature decomposition

Frozen 26 October 2026, base 37f8f01db8b7e30190f09bf784d1b4e3419da540.
Owner: /root/uniform_jet_moment_sources. Sole production file:
SourceCurvatureDecomposition.lean. The validated mathematical requirements below
are adopted as production requirements; the historical proposal qualification
is retained for provenance. New evidence belongs in curvature-evidence/.
No old source or input changes and no unchanged verification reruns.
Only standard Lean axioms; no sorry/admit/custom axiom/native_decide.
Scientific review must be separately authenticated by a different model family.

# Single-curvature decomposition and cubic small-curvature route

OpenAI/Codex author-side validation by `/root/uniform_jet_moment_sources`.
Read-only/scratch proposal only: no production freeze, ownership, scientific review
credit or parent-status promotion is implied. The previous full-four-jet/Vandermonde
proposal and its proved finite helper remain valid future work, but are unnecessary
for the route below.

## Validation result

The proposed route is mathematically sound. It requires only the already-proved
actual seven-contact covariance positivity, not full 15-jet positivity or a
conditional density of q given eight other raw jets. It does require proving an
actual independent scalar Gaussian direction and an exact full-carrier product
representation; neither conclusion may be inserted as a premise.

One qualification is essential: `q(Φ_x ρ)=m_r(x)` holds for `ρ=ρ_r η`, hence under
the residual law, but generally fails for an arbitrary smooth sample ρ. The proposed
all-ρ definition of Ψ correctly subtracts the actual `q(Φ_x ρ)` and therefore works
without that false universal identity.

## Fixed actual objects

For `L ≠ 0` and fixed r, use the existing objects:

- `μ := smoothLaw 2 L`, `S := SmoothSample 2 L`;
- `X_r := sourceConfluentPinsAt L r` and `G_r := sourcePinCovarianceAt L r`;
- `Φ_x η := I4SourceSmoothConditional.posteriorSample hL r x η`;
- `Q η := I4SourceContact.sourceContactQ L η`, the actual midpoint `fyy(0)`;
- `a_i(m) := I4SourceConfluentLimits.pinCoefficient L r i m`;
- `q_m := I4SourceContact.sourceContactCoefficient L 6 m`.

Define literal scalar regression objects, with no assumed law or variance conclusion:

`C_r i := Cov_μ(Q, X_{r,i})`, `β_r := C_r G_r⁻¹`,
`τ_r := Var_μ(Q) - β_r C_rᵀ`, `σ_r := Real.sqrt τ_r`,
`d_r(m) := q_m - ∑ i, β_{r,i} a_i(m)`, `χ_r(m) := d_r(m)/σ_r`.

These definitions can be total at all real r (using existing total inverse/division),
with theorem hypotheses carrying current `IsUnit G_r` and `0 < τ_r` as needed.
No arbitrary value at r=0 is identified with the confluent contact limit.

## Proposed first bounded source module

Suggested sole new file after owner freeze: `SourceCurvatureDecomposition.lean`.

Required genuine exports:

1. Exact actual coefficient/series and covariance formulas for C_r, d_r, and χ_r,
   with every-sample weighted summability. The actual q coordinate is jointly
   Gaussian with X_r and every finite coefficient family by existing scalar-series
   Gaussian APIs. No assumed Gaussian process is introduced.
2. `C_r → sourceContactCross L` as r→0+ from regularized pin coefficients and
   the fixed q coefficient; hence `τ_r → sourceContactSchur L > 0` using the
   completed G limit/inverse limit. Derive a common small-positive-radius interval
   with `IsUnit G_r`, `τ_r ≥ sourceContactSchur L / 2 > 0`, bounded β_r, and
   bounded prescribed-pin mean `m_r(b):=β_r(sourcePrescribedPins r b)`.
3. Actual identities `∑ χ_r²=1`, `∑ a_i χ_r=0`, and `∑ q_m χ_r(m)=σ_r`.
   The first follows from the literal residual coefficient Gram and normal equations;
   the latter two are the actual pin orthogonality and q variance identities.
4. Define `Z_r η := scalarSeries χ_r η.val`. Prove for every actual sample
   `Z_r η=(Qη-β_r X_rη)/σ_r`, with `HasLaw Z_r (gaussianReal 0 1) μ`.
5. Define `ρ_r η` by coefficients `η_m-χ_r(m) Z_rη`. Prove every-order goodSample
   preservation and measurability. For every finite coefficient restriction, prove
   joint Gaussianity of Z_r and the restricted residual, zero cross covariance,
   and independence; upgrade to independence from the entire residual process,
   then to the SmoothSample subtype. Residual coordinates need not be independent
   of each other. Derive
   `μ.map (fun η => (ρ_rη,Z_rη)) = (μ.map ρ_r).prod (gaussianReal 0 1)`.
6. Every-sample identities:
   `X_r(ρ_rη)=X_rη`, `Z_r(ρ_rη)=0`,
   `Φ_xη = Φ_x(ρ_rη) + χ_r Z_rη`,
   `Q(Φ_xη)=β_rx+σ_r Z_rη`, and `Q(Φ_x(ρ_rη))=β_rx`.
   Additions in these formulas denote the proved carrier-preserving coefficient shifts.
7. Define for every smooth sample ρ and real t:
   `Ψ_r(x,ρ,t) := Φ_xρ + χ_r * (t-Q(Φ_xρ))/σ_r`.
   Prove joint measurability, every-order carrier preservation, and for **all ρ,t**
   the exact identities `X_r Ψ_r(x,ρ,t)=x`, `Q Ψ_r(x,ρ,t)=t`.
8. Let `ν_r:=μ.map ρ_r`. Prove every-x equality of literal measures:
   `sourceSmoothKernel hL r x =
      (ν_r.prod (gaussianReal (β_rx) τ_r.toNNReal)).map (fun p => Ψ_r(x,p.1,p.2))`.
   Derive from the proved independent standard direction and exact reconstruction,
   rather than from almost-everywhere uniqueness of conditional laws.

The fixed-r decomposition may use current hG and hτ. Final actual small-r exports
must derive them from `L ≠ 0`; no pin/covariance/nondegeneracy conclusion remains
as an application assumption.

## Uniform majorants and moments for the product representation

Set `Γ_k(ω):=sourceDerivativeMajorant L k ω` and
`R(ω):=1+∑ k:Fin 6, Γ_k(ω)`.
The completed global derivative theorem bounds every derivative of order k by Γ_k.

On a common small-r interval, existing pin coefficient bounds and bounded β_r give

`|χ_r(m)| ≤ (|q_m| + 6 B * confluentModeMajorant L m)/sqrt(τ_min)`.

For every order n the order-weighted χ coefficients are summable by existing
summable-product arguments. For n≤5 the corresponding sums have a common finite
upper bound H. In particular `H/σ_r` is uniformly bounded since τ_r≥τ_min>0.

For prescribed x_r(b), put `S_r(ρ):=R(Φ_{x_r(b)}ρ)`, so S_r≥1. For all ρ,t,

`R(Ψ_r(x_r(b),ρ,t)) ≤ S_r(ρ)+(H/σ_r)|t-Q(Φ_{x_r(b)}ρ)|
                         ≤ A (|t|+S_r(ρ))`.

The second inequality uses the actual bound `|Q(Φ_xρ)|≤Γ_2(Φ_xρ)≤S_r(ρ)`;
it does not falsely assert Q(Φ_xρ)=m_r(b) for arbitrary ρ.

For ρ=ρ_rη, exact reconstruction gives

`S_r(ρ_rη) ≤ R(Φ_{x_r(b)}η)+H|Z_rη|`.

The already-qualified conditional Γ moments and the standard Gaussian moments
therefore imply uniform moments of every fixed integer order of S_r under ν_r.
No independence is needed in this moment comparison. To combine Γ_0,...,Γ_5,
use their finite sum of orderModeBound weights and the existing generic weighted
majorant moment theorem, or a finite sum power bound with a common interval.

The q density is bounded uniformly in all means and real t:

`gaussianPDFReal (β_rx) τ_r.toNNReal t ≤ (2π τ_min)^(-1/2)`.

With τ_min=sourceContactSchur L/2 this constant is `(π*sourceContactSchur L)^(-1/2)`.
The density statement preserves the actual nonzero mean β_rx.

## Deterministic weight obligation, separated from decomposition

For a smooth sample on the actual prescribed pin fiber, both endpoint x/y
gradients vanish. If R bounds global third derivatives, Peano/mean-value identities give

`|fxx(M)|, |fxx(S)|, |fxy(M)|, |fxy(S)| ≤ rR`,
`|fyy(M)-Q|, |fyy(S)-Q| ≤ rR`.

Thus for both actual endpoint Hessians,
`|det H|≤rR|Q|+2r²R²`, and the literal nonnegative typed determinant weight satisfies

`W_r ≤ 2r²R² Q²+8r⁴R⁴`.

This is a genuine actual-field estimate, with no quartic Hessian identification.
The completed ConfluentIntegralIdentities scalar endpoint formulas and the generic
axis derivative-chain helpers apply to every smooth field sample. The Γ_3 bound
is enough for the displayed coarse estimate; Γ_0,...,Γ_5 are retained for the
intended full parent regularity cutoff.

## Cubic small-curvature calculation

Fix K≥0, ε>0, b, and the near event `|Q|≤K r R^5`.
Split it by the regular event `rR^5≤ε`.

On the regular near event, `|Q|≤Kε`. Since S≥1 and `R(Ψ)≤A(|Q|+S)`,

`R(Ψ)≤D S`, where `D:=A(1+Kε)`, and `|Q|≤K r D^5 S^5`.

There is no delicate quintic fixed-point absorption: the two event inequalities
already bound |Q| by a fixed constant. The weight estimate becomes

`W_r≤(2K²D^12+8D^4) r⁴ S^12`.

The near q interval has length at most `2K D^5 r S^5`. Uniform density and Tonelli
under the exact product representation therefore give

`E_{sourceSmoothLaw}[W_r 1_(regular∩near)]≤C r⁵ E_{ν_r}[S^17]≤C' r⁵`.

The proposed conservative S^20 weight/moment25 version is also valid; moment17
already suffices for the displayed coarse weight bound. Dividing by the existing
actual normalizer lower bound `c r²` yields a weighted probability ≤C r³.

On the bad regularity event `rR^5>ε`, the 30th moment gives

`P_{sourceSmoothLaw}(bad)≤ε^(-6) r⁶ E[R^30]≤C r⁶`.

This uses integer powers only: on the event, 1≤ε^(-6)r⁶R^30. The completed
determinant second moment and normalizer plus Cauchy–Schwarz transfer yield
`sourceSmoothWeightedLaw(bad)≤C r³`.

Consequently the bounded next parent-driver statement is:

For `L≠0`, b and K≥0, there exist δ>0 and finite C≥0 such that for every
0<r<δ, the actual existing `sourceSmoothWeightedLaw hL r b` satisfies

`P(|sourceContactQ L| ≤ K*r*R^5) ≤ C*r^3`.

This conclusion must use the existing actual full-carrier law, physical determinant
weight and normalizer; an arbitrary Gaussian or synthetic weight is insufficient.

## Reusable source/API receipts; implementation costs

- `SourceContactSchur.lean`: actual Q definition, sourceContactSchur and
  `sourceContactSchur_pos hL`; no full-four-jet input needed.
- `SourceConfluentLimits.lean`: actual pin coefficients, every-sample series,
  regularized coefficients/continuity/contact values and summable majorant.
- `SourceSmoothConditionalKernel.lean`: actual full-carrier shift/K, arbitrary-finite
  scalar-series Gaussian theorem, generic scalarSeries-coordinate covariance,
  process-independence proof pattern, measurable subtype retraction, and exact
  full conditional law. Reuse its completed compiled artifact unchanged.
- `SourceConditionalMajorant.lean`: actual Γ_k, global derivative bound, all integer
  conditional moments, posterior weighted-majorant domination and Gaussian tails.
- `GaussianWeightedMajorants.lean`: all integer standard absolute moments and
  generic summable weighted Gaussian majorant moment bounds.
- `SourceSmoothPalm.lean`: sourceSmoothLaw, actual raw pin fiber, literal typed
  determinant weight, weight second moment, normalizer floor and reweighting transfer.

No mathematical obstruction was found. New formal costs are the scalar cross-limit,
literal residual variance/normalization algebra, one Gaussian-direction projection
with whole-process independence, exact product reconstruction, and the Peano weight
bound/product integral estimate. Existing residual covariance helpers in
SourceContactEndpointParameters are private: their argument is reusable mathematics,
but a small new scalar proof is required; do not claim a public generic API exists.

No production edits, old checks or baseline rebuilds were performed for this validation.
The source contracts for decomposition and final weighted event theorem should be
frozen before implementation, with explicit ownership and separate scientific review.
This route does not establish full LM005 15/9 covariance positivity, geometric Morse
properties, a geometric Palm identification or any stronger P0.2 statement beyond
the explicit actual weighted near-curvature estimate.
