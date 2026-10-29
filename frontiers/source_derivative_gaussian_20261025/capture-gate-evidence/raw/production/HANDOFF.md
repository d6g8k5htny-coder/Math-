# SourceQuarticCaptureAlgebra production handoff

Sole production source owner: OpenAI/Codex /root/regression_kernel.
Contract: SOURCE_QUARTIC_CAPTURE_ALGEBRA.md frozen at
`ebf49a429ec737f24c29f7c0ca4d9a7b1457c5cd` before this production source.
Root owns manifests, Lake registration, commits and publication.

Final source:
`/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025/SourceQuarticCaptureAlgebra.lean`
SHA256 `ba338bba6fdd6fae70f5379c8ff58a424237baf090672a7e3303691ff2f0209a`.

Public API, namespace I4QuarticCaptureAlgebra:

* `rawRadius`, `regular`, `captureWidth`, `captureSigma` are the exact LM001
  U-radius, REG, adaptive width and central section scale.
* `quartic_strip_upper`, `quartic_strip_lower`: literal quartic horizontal
  boundary gates <=-1 and >=1 from r>0, r<=1 and the scalar threshold.
  REG is not required by these two polynomial results.
* `quartic_central_transit`: literal quartic X drift <=-3RW<0 on the central
  rectangle, from r>0, r<=1 and REG. No scalar threshold is required here.
* `euclidean_component_error_le`, `capture_strip_in_ball_two`, and
  `source_component_error_le` derive the Euclidean component error from the
  qualified maximum C1 bound, with the exact RW/4 tolerance.
* `sourceStripGates`, `sourceCentralGate` refer literally to
  `sourceScaledGradientRaw` of the actual smooth Fourier field.
* `source_actual_strip_gates`: physical pins, original source regularity cutoff
  and original negative-curvature cutoff give actual inward boundary signs.
* `source_actual_central_gate`: physical pins and source regularity cutoff give
  actual X drift <=-(11/4)RW<0 throughout the central rectangle. No curvature
  cutoff is needed for this central result.
* `source_actual_gates_estimates`, `source_actual_weighted_gates_estimates`:
  hL!=0 and fixed b alone give a sufficiently small positive radius interval
  on which the above cutoff implications hold almost everywhere under the
  actual base/weighted carrier laws. Current covariance-unit and pin-support
  premises are derived by reusing sourcePhysicalPins_eventually. Weighted
  transfer uses the literal prwMeasure absolute continuity.

Lineage and reused evidence:

* Generic geometry body copied once unchanged from qualified scratch
  GeometrySupport.lean, authored by /root/uniform_jet_moment_sources,
  source SHA57aa2d539844482449a30fa1d471c74e5e33b095d67a35ba836130a5ac9e7eb1.
* Forcing and Q2/Q3 bodies copied once from my qualified scratch
  CaptureAlgebra.lean and CaptureGates.lean. Their original source hashes,
  compile/kernel/axiom evidence, histories and premise-essential counterexample
  controls remain in /workspace/scratch/quartic-capture-algebra/EVIDENCE.json.
* Actual-source transfer and new almost-sure wrappers authored here by me.
* New transfer-buffer/projection/orientation controls authored in disjoint
  scratch by /root/palm_measure_transfer; old controls are reused, not rerun.
* All authors are OpenAI/Codex. No provider-distinct scientific-review credit
  is asserted. The already closed paper certificate has separate provenance.

Verification scope:

* compile01 checked the initial copied generic production artifact only.
* compile02 checked the full actual-source extension and failed on two API
  details (explicit coordinate simp source; helper namespace). Both records
  and complete source snapshots are retained.
* compile03 is the complete final clean Werror elaboration, source hash above.
* kernel01 replays only this new production module, trusting unchanged imports.
* audit01 prints all28 public proof targets; each has only propext,
  Classical.choice and Quot.sound. Six separate definitions are inventoried.
* New-only control records and final receipt are in this directory.

Theorems are finite algebra plus actual-field drift inequalities. No ODE
existence, selected branch, complete transit/capture, event measurability,
geometric Palm identification, elder/counting or P0.2 conclusion is claimed.
No old source, baseline qualification, or old stress campaign was edited/rerun.
