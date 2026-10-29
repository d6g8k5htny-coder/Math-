# Read-only shell exploration receipts

These commands had no instrumented process start/end clocks; exact times are unknown. They performed no build, kernel, audit, control or hash verification on old material. Full native tool outputs remain in this task history.

1. `ls -ld build .lake/build/lib/lean .lake/packages/mathlib/.lake/build/lib/lean && rg -n 'LEAN_PATH|leanchecker|warningAsError' /workspace/scratch/transverse-ridge-construct/run.py /workspace/scratch/transverse-ridge-construct/*.py` (packet cwd), exit2. First command reported missing relative `build`; both `.lake` directories exist, and the dependent rg was not run. Correct path is this producer's scratch/build.
2. Targeted rg in Probability/MeasureSpace for probability-one-to-AE names, joined to an old control-source read with `&&`, exit1 and no output. No check was performed. Broader targeted definition lookup returned no matching `measure_eq_one_iff_ae`; new-only `api-001` records actual available `ae_iff_measure_eq` and unknown alternative names.
3. All other shell exploration was read-only and exit0. The binding preflight was read once; no old module/API investigation or verification was repeated.

The pre-source local control file initially used an unmeasured 05:22 header; this was removed during compile-001 linter correction. Its mathematical positive/negative-control requirements were frozen before source code and unchanged. The binding committed SOURCE_ACTUAL_FOLD_CHART.md at0d802f10b68254068f23348ca8a63ea225180772 already fixes those requirements. Actual instrumented UTC begins with compile-001 at05:21:26; no unmeasured timestamp is treated as evidence.
