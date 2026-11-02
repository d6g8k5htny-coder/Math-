# Frozen finite-trigonometric atom conversion helper

26 October 2026. OpenAI/Codex `/root/conditional_remote_jet_preflight`, root-dispatched helper47. Scope is only `/workspace/scratch/finite-trig-source-conversion`. Actual pickup acknowledged to root and producer. Root's PRECODE is `f20c0b067a571c29ebaaa478986c2395e39af4e5`; native pickup `6414892543`, 11:27:54 UTC. Producer `/root/actual_fold_candidate_construct` confirmed its `CONTROL_CONTRACT.md` frozen before authorizing helper code. Read frozen `SOURCE_FINITE_TRIG.md`, `SOURCE_FINITE_TRIG_PLAN.md`, producer controls and the representation preflight first.

## Delivered and frozen

`NEEDED_SECTION.lean.txt` is the exact needed section, frozen at **11:33:22.934215 UTC**. It contains seven **private** declarations in the intended `I4SourceFiniteTrig` namespace context:

- `atom_amplitude_pos`
- `atom_pairing_single`
- `atom_pairing_add`
- `atom_pairing_pair`
- `atom_phase_neg`
- `atomSource`
- `atomSource_pairing`

The API agreed with producer is:

```lean
private def atomSource (L : ℝ) (k : Fin 2 → ℤ) (θ : ℝ) :
    I4Source.SourceMode 2 →₀ ℝ

private theorem atomSource_pairing {L : ℝ} (hL : L ≠ 0)
    (k : Fin 2 → ℤ) (θ : ℝ) (x : Fin 2 → ℝ) :
    I4SourceFinitePinKernel.finitePairing
      (fun m => I4Source.modeCoefficient 2 L m x) (atomSource L k θ) =
      Real.cos (I4Source.phase 2 L k x + θ)
```

`atomSource` is total in L, with no proof argument. Correctness requires only `L≠0`. The zero-frequency branch uses actual `none` with coefficient `cos θ / sourceModeAmplitude L none`. A frequency in the canonical half-lattice uses cosine coefficient `cos θ/A` and sine coefficient `-sin θ/A`; a nonzero frequency outside it uses canonical `-k` and sine coefficient `+sin θ/A`. Every denominator is the actual representative's source amplitude. Private amplitude positivity derives directly from the existing positive spectral weights/normalizer. No spectral floor, period change, source-law substitution, nonconstant-only restriction or remote-rank claim is made.

## Exact once-integration boundary

Copy `NEEDED_SECTION.lean.txt` **exactly once** inside producer's existing `namespace I4SourceFiniteTrig`, after imports/noncomputable setup and before `toSource`. It includes needed `open` declarations. Its content is exactly **lines 10–96** of the successful strict source `raw/attempt003/AtomConversion.lean`; it excludes import lines and the namespace/setup/end wrapper.

Producer's imports `SourceFinitePinKernel` and `SourceContactCovariance` suffice. Producer owns all list operations, `toSource`, derivative adapter, integrated source freeze, controls, inventory and the one final module qualification. Do not import this helper as a module, copy its object into production, or run a helper kernel/audit/control campaign. The final integrated module will contain these private proofs once. This helper earns no separate public research-target credit.

Exact new-source identities, recorded once for this delivery rather than by an old-payload hash replay:

| Artifact | Bytes | SHA256 |
|---|---:|---|
| `NEEDED_SECTION.lean.txt` | 3652 | `bb748238147162c2e68e6134361c9c4ad17610a2f2adb78d2510a08c786ddff3` |
| `raw/attempt003/AtomConversion.lean` | 3845 | `9754087702b4b416bad0bedcbc7e303e90fce88ab036f6d2e8a82c61aa2da8fd` |

`IDENTITY.json` records paths, integration bounds, source identities, scratch object custody and the successful result record. The successful `.olean` stays in `raw/attempt003/` as development custody only.

## New-only strict elaboration evidence

All three attempted sources are retained unchanged in `raw/attempt001`, `raw/attempt002`, `raw/attempt003`. Each contains `command.json`, `result.json`, full `stdout.log` and `stderr.log`; no output was truncated in the retained files. `run_attempt.py` is the exact runner.

Actual strict invocation form, with each attempt's own paths, was:

```text
lake env lean -DwarningAsError=true --root=<attempt-directory> <attempt-directory>/AtomConversion.lean -o <attempt-directory>/AtomConversion.olean
```

Working directory was `/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025`. Imports reused the qualified production `SourceFinitePinKernel` object and existing dependencies; no old source was compiled.

| Attempt | UTC start → end | Actual exit | Result |
|---|---|---:|---|
| 001 | 11:31:17.422651 → 11:31:20.949456 | 1 | Pinned linter/deprecation issues and a zero-branch simplification failure. |
| 002 | 11:32:02.391420 → 11:32:05.388166 | 1 | Zero-frequency phase simplification still needed `zero_mul`; associated unused-simp diagnostics. |
| 003 | 11:32:42.445341 → 11:32:45.986285 | **0** | Strict Werror elaboration succeeded, stdout/stderr both empty. |

The only changes between attempts corrected these concrete new-source diagnostics. Attempt003 is final; no successful check was rerun merely because the section was frozen or handed off. There was no standalone kernel, axiom audit, control suite or broader verification campaign.

## Evidence reuse, process and authority

Reuse root's completed **46 modules / 1089 targets / 32 inputs** at `3e15af2eab94b2448ce28aeb4c926ada7d596a50`, including the qualified `SourceFinitePinKernel` production object. `/workspace/AGENTS.md` requires reuse of completed applicable verification on unchanged material under the same assumptions/dependencies. A new session/handoff or a pending process requirement does not justify replay; new checking must identify a changed scope, defect or uncovered obligation. This helper checked only its new finite conversion source. Mathematical verification remains separate from pending different-family/provider-distinct process requirements.

Scientific effect **NONE**; same-family/provider-distinct credit **0**. No subagents, production cache/config changes, git actions or external posts occurred. Root retains shared cache/metadata/registration/commits/publication ownership. Canonical standing authority links for onboarding/handoff:

- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OWNER_MANDATE_20261015.md
- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OP-AUTONOMY-20260923-v2.1.md

Links alone do not establish successor reading. The helper is delivered and frozen; further changes require producer/root coordination rather than a second integration.
