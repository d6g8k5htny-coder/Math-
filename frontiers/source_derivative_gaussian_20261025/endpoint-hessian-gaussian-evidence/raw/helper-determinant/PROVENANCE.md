# Fixed determinant-three nullity section — frozen text

Frozen 2026-10-26 16:59:32 UTC by `/root/endpoint_determinant_null_text` for exactly one integration by `/root/remote_jet_gaussian_construct` into `SourceEndpointHessianGaussian.lean`, namespace `I4SourceEndpointHessianGaussian`.

Section: `DETERMINANT_NULLITY_SECTION.lean`.

SHA-256: `adeafa591d85a20a5ffe30989d97ed59e0e4534ec19cb83b24b39ff5a0cde7e8`.

Exact supplied declaration:

```lean
private theorem determinant3_zero_volume :
    volume {H : EuclideanSpace ℝ (Fin 3) | H 0 * H 2 - (H 1) ^ 2 = 0} = 0
```

Narrow imports (no umbrella Mathlib):

```lean
import Mathlib.MeasureTheory.Constructions.Pi
import Mathlib.MeasureTheory.Measure.Prod
import Mathlib.MeasureTheory.Measure.Haar.InnerProductSpace
```

The file's import/context/namespace wrapper is provided for integration clarity. The private theorem is the whole needed section; no additional declarations or generic polynomial library are supplied.

Pinned public API source was read from `/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025/.lake/packages/mathlib/Mathlib`:

- `MeasureTheory/Measure/Prod.lean`: `Measure.measure_prod_null_of_ae_null` (line 386), `MeasurePreserving.prod` (line 897).
- `MeasureTheory/Constructions/Pi.lean`: `volume_preserving_piFinSuccAbove` (line 818), `volume_preserving_piFinTwo` (line 857).
- `MeasureTheory/Measure/Haar/InnerProductSpace.lean`: `PiLp.volume_preserving_ofLp` (line 134).
- `MeasureTheory/Measure/Typeclasses/NullSingletonClass.lean`: `measure_singleton` and `Measure.ae_ne` (line 68).
- `Dynamics/Ergodic/MeasurePreserving.lean`: `MeasurePreserving.comp`, `MeasurePreserving.preimage_null`.
- `MeasureTheory/MeasurableSpace/Embedding.lean` and `Data/Fin/Tuple/Basic.lean`: the concrete piFin equivalence definitions, showing the composed coordinate map has exactly `(H 0, (H 1, H 2))` as its definition.

Proof route: closed determinant-zero set in ℝ×(ℝ×ℝ); for a≠0 every c-section is `{b²/a}`, so it is null; two applications of Fubini, with the outer exceptional a=0 set removed by scalar Lebesgue nullity; pull back through the stated three public volume-preserving coordinate maps. The ordinary mixed square is retained. No infinity multiplication or unmeasurable section shortcut is used.

Status: **UNCOMPILED TEXT ONLY**. No Lean execution, name probe, elaboration, compilation, test, kernel/audit/control campaign, object creation, repository modification, cache/registry/configuration/Git change, or external operation was performed. The one SHA-256 above freezes this new text only. Only final integrated new-module qualification can qualify it. Source/API reasoning identifies no mathematical gap; elaboration compatibility remains unclaimed.

Owner `/workspace/AGENTS.md` reuse instruction and all applicable old qualified49/50 mathematical evidence are preserved without rechecking. Native pickup `6421975582`, precode `81e3a89e595c849186d86d0c654b483c174c32ac`, frozen producer controls, checkpoint 17:45 UTC / terminal 19:00 UTC 2026-10-26 are carried as root/producer-supplied provenance, not independently verified. Scientific effect NONE; provider-distinct review credit 0.
